"""
Rate limiting middleware for the AI Gateway.

Enforces per-key request and token limits using the sliding window
algorithm. Each API key tier (free / standard / enterprise) gets
different limits, configured in config.yaml.

Why rate limiting matters for AI gateways specifically: a single
runaway agent can exhaust your monthly API budget in minutes. Rate
limits are not just about fairness --- they are cost circuit breakers.

Reference: Chapter 4 - Infrastructure for AI-First Operations
"""

import time
from dataclasses import dataclass, field


@dataclass
class RateLimitConfig:
    """Limits for a single tier."""
    requests_per_minute: int = 60
    tokens_per_minute: int = 100_000


@dataclass
class _Window:
    """Tracks usage within a rolling window."""
    requests: list[float] = field(default_factory=list)
    tokens: list[tuple[float, int]] = field(default_factory=list)


# Default tier configs --- loaded from config.yaml in production.
DEFAULT_TIER_LIMITS: dict[str, RateLimitConfig] = {
    "free": RateLimitConfig(requests_per_minute=10, tokens_per_minute=10_000),
    "standard": RateLimitConfig(requests_per_minute=60, tokens_per_minute=100_000),
    "enterprise": RateLimitConfig(requests_per_minute=300, tokens_per_minute=500_000),
}


class RateLimitExceeded(Exception):
    """Raised when a key exceeds its rate limit."""

    def __init__(self, message: str, retry_after_seconds: float = 0.0) -> None:
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class RateLimiter:
    """
    Sliding-window rate limiter keyed by API key ID.

    Tracks both request count and token count per minute. Either
    limit being exceeded blocks the request.

    In production, replace the in-memory dict with Redis for
    multi-instance deployments. The interface stays the same.

    Usage:
        limiter = RateLimiter()
        limiter.check_request("key-std-001", tier="standard")
        # ... after completion ...
        limiter.record_tokens("key-std-001", token_count=1500)
    """

    def __init__(
        self,
        tier_limits: dict[str, RateLimitConfig] | None = None,
        window_seconds: float = 60.0,
    ) -> None:
        self._tier_limits = tier_limits or DEFAULT_TIER_LIMITS
        self._window_seconds = window_seconds
        self._windows: dict[str, _Window] = {}

    def _get_window(self, key_id: str) -> _Window:
        if key_id not in self._windows:
            self._windows[key_id] = _Window()
        return self._windows[key_id]

    def _prune(self, window: _Window, now: float) -> None:
        """Remove entries older than the sliding window."""
        cutoff = now - self._window_seconds
        window.requests = [t for t in window.requests if t > cutoff]
        window.tokens = [(t, n) for t, n in window.tokens if t > cutoff]

    def _get_limits(self, tier: str) -> RateLimitConfig:
        return self._tier_limits.get(tier, self._tier_limits.get("free", RateLimitConfig()))

    def check_request(self, key_id: str, tier: str = "free") -> None:
        """
        Check whether this key can make another request right now.

        Raises RateLimitExceeded if either the request count or the
        token count has been exceeded within the current window.
        """
        now = time.monotonic()
        window = self._get_window(key_id)
        self._prune(window, now)
        limits = self._get_limits(tier)

        # Check request count
        if len(window.requests) >= limits.requests_per_minute:
            oldest = window.requests[0]
            retry_after = self._window_seconds - (now - oldest)
            raise RateLimitExceeded(
                f"Rate limit exceeded: {limits.requests_per_minute} requests/min "
                f"(tier={tier})",
                retry_after_seconds=max(0.0, retry_after),
            )

        # Check token count
        total_tokens = sum(n for _, n in window.tokens)
        if total_tokens >= limits.tokens_per_minute:
            oldest_token_time = window.tokens[0][0]
            retry_after = self._window_seconds - (now - oldest_token_time)
            raise RateLimitExceeded(
                f"Token limit exceeded: {limits.tokens_per_minute} tokens/min "
                f"(tier={tier})",
                retry_after_seconds=max(0.0, retry_after),
            )

        # Record this request timestamp
        window.requests.append(now)

    def record_tokens(self, key_id: str, token_count: int) -> None:
        """Record token usage after a successful completion."""
        now = time.monotonic()
        window = self._get_window(key_id)
        window.tokens.append((now, token_count))

    def get_usage(self, key_id: str, tier: str = "free") -> dict[str, int | float]:
        """Return current window usage for monitoring or response headers."""
        now = time.monotonic()
        window = self._get_window(key_id)
        self._prune(window, now)
        limits = self._get_limits(tier)

        request_count = len(window.requests)
        token_count = sum(n for _, n in window.tokens)

        return {
            "requests_used": request_count,
            "requests_limit": limits.requests_per_minute,
            "requests_remaining": max(0, limits.requests_per_minute - request_count),
            "tokens_used": token_count,
            "tokens_limit": limits.tokens_per_minute,
            "tokens_remaining": max(0, limits.tokens_per_minute - token_count),
        }
