"""
AI Gateway --- main entry point.

Routes AI completion requests through authentication, rate limiting,
cost tracking, and structured logging before they reach any provider.
Supports provider fallback: if OpenRouter is down, requests automatically
route to OpenAI or Anthropic.

All providers use raw httpx --- no SDK packages required. OpenRouter is
the primary provider (single API key, many models). Direct OpenAI and
Anthropic connections serve as fallbacks.

This demonstrates the AI Tool Gateway pattern from Chapter 4. In a
production deployment, you would run this behind an API gateway
(Kong, Envoy, etc.) and replace the in-memory stores with Redis /
PostgreSQL.

Reference: Chapter 4 - The AI Tool Gateway Pattern

Usage:
    export OPENROUTER_API_KEY="sk-or-..."
    python gateway.py
"""

import asyncio
import uuid
from dataclasses import dataclass

import yaml

from middleware.auth import AuthContext, AuthMiddleware
from middleware.cost_tracker import CostTracker
from middleware.logger import GatewayLogger
from middleware.rate_limit import RateLimiter
from providers.anthropic import AnthropicProvider
from providers.base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    Message,
    MessageRole,
)
from providers.fallback import FallbackProvider
from providers.openai import OpenAIProvider
from providers.openrouter import OpenRouterProvider


@dataclass
class GatewayConfig:
    """Parsed gateway configuration."""
    default_provider: str = "openrouter"
    default_model: str = "google/gemini-2.5-flash"
    fallback_enabled: bool = True
    max_retries: int = 2
    retry_delay: float = 1.0
    log_level: str = "INFO"


def load_config(path: str = "config.yaml") -> GatewayConfig:
    """Load gateway configuration from YAML."""
    try:
        with open(path) as f:
            raw = yaml.safe_load(f)
    except FileNotFoundError:
        return GatewayConfig()

    routing = raw.get("routing", {})
    middleware = raw.get("middleware", {})

    return GatewayConfig(
        default_provider=routing.get("default_provider", "openrouter"),
        default_model=routing.get("default_model", "google/gemini-2.5-flash"),
        fallback_enabled=routing.get("fallback_enabled", True),
        max_retries=routing.get("max_retries", 2),
        retry_delay=routing.get("retry_delay_seconds", 1.0),
        log_level=middleware.get("logger", {}).get("level", "INFO"),
    )


class AIGateway:
    """
    Central AI gateway that sits between callers and AI providers.

    The gateway enforces a middleware chain on every request:
    1. Authentication --- is this caller allowed in?
    2. Rate limiting  --- has this caller exceeded their quota?
    3. Routing        --- which provider handles this model?
    4. Completion     --- call the provider (with fallback on failure)
    5. Cost tracking  --- how much did this request cost?
    6. Logging        --- structured log line for observability

    This order matters. Auth and rate limits run *before* touching any
    provider API, so invalid or throttled requests never cost you money.

    Usage:
        gateway = AIGateway()
        response = await gateway.complete(
            authorization="Bearer sk-demo-standard-001",
            messages=[Message(role=MessageRole.USER, content="Hello")],
            model="google/gemini-2.5-flash",
        )
    """

    def __init__(self, config_path: str = "config.yaml") -> None:
        self._config = load_config(config_path)

        # --- Middleware ---
        self._auth = AuthMiddleware()
        self._rate_limiter = RateLimiter()
        self._cost_tracker = CostTracker()
        self._logger = GatewayLogger(level=self._config.log_level)

        # --- Providers ---
        self._providers: dict[str, BaseProvider] = {}
        self._init_providers()

    def _init_providers(self) -> None:
        """Initialize available providers based on env vars.

        Provider priority: OpenRouter first (single key, many models),
        then direct OpenAI and Anthropic as fallbacks.
        """
        import os

        if os.environ.get("OPENROUTER_API_KEY"):
            self._providers["openrouter"] = OpenRouterProvider()

        if os.environ.get("OPENAI_API_KEY"):
            self._providers["openai"] = OpenAIProvider()

        if os.environ.get("ANTHROPIC_API_KEY"):
            self._providers["anthropic"] = AnthropicProvider()

        if not self._providers:
            raise EnvironmentError(
                "At least one provider API key must be set "
                "(OPENROUTER_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY)"
            )

    def _get_provider(self, model: str) -> BaseProvider:
        """Select the right provider for a model, with fallback wrapping."""
        # Find providers that support this model
        candidates = [
            p for p in self._providers.values() if p.supports_model(model)
        ]

        if not candidates:
            # Fall back to all available providers
            candidates = list(self._providers.values())

        if self._config.fallback_enabled and len(candidates) > 1:
            return FallbackProvider(
                providers=candidates,
                max_retries=self._config.max_retries,
                retry_delay=self._config.retry_delay,
            )

        return candidates[0]

    async def complete(
        self,
        authorization: str,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> CompletionResponse:
        """
        Process a completion request through the full middleware chain.

        This is the main entry point. Every request flows through:
        auth -> rate limit -> provider -> cost tracking -> logging.
        """
        request_id = str(uuid.uuid4())[:8]
        resolved_model = model or self._config.default_model

        # 1. Authenticate
        auth_ctx: AuthContext = self._auth.authenticate(authorization)

        # 2. Log the incoming request
        self._logger.log_request(
            request_id=request_id,
            key_id=auth_ctx.api_key_id,
            model=resolved_model,
        )

        # 3. Rate limit check
        self._rate_limiter.check_request(auth_ctx.api_key_id, tier=auth_ctx.tier)

        # 4. Build the provider request
        request = CompletionRequest(
            messages=messages,
            model=resolved_model,
            temperature=temperature,
            max_tokens=max_tokens,
            metadata={"request_id": request_id, "key_id": auth_ctx.api_key_id},
        )

        # 5. Route to provider (with fallback)
        try:
            provider = self._get_provider(resolved_model)
            response = await provider.complete(request)
        except Exception as exc:
            self._logger.log_error(
                request_id=request_id,
                error=str(exc),
                model=resolved_model,
            )
            raise

        # 6. Track cost
        cost = self._cost_tracker.record(
            key_id=auth_ctx.api_key_id,
            model=response.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
        )

        # 7. Record tokens for rate limiting
        self._rate_limiter.record_tokens(
            auth_ctx.api_key_id, response.usage.total_tokens
        )

        # 8. Log the completed response
        self._logger.log_response(
            request_id=request_id,
            provider=response.provider,
            model=response.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            latency_ms=response.latency_ms,
            cost_usd=cost.total_cost,
        )

        return response

    async def health(self) -> dict[str, bool]:
        """Check health of all configured providers."""
        results: dict[str, bool] = {}
        for name, provider in self._providers.items():
            results[name] = await provider.health_check()
        return results

    def get_cost_summary(self, key_id: str) -> dict:
        """Return cost summary for a specific API key."""
        from dataclasses import asdict

        return asdict(self._cost_tracker.get_summary(key_id))

    def get_rate_limit_status(self, key_id: str, tier: str = "free") -> dict:
        """Return current rate limit usage for a key."""
        return self._rate_limiter.get_usage(key_id, tier)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

async def demo() -> None:
    """
    Demonstrate the gateway end-to-end.

    Run with:
        export OPENROUTER_API_KEY="sk-or-..."
        python gateway.py
    """
    gateway = AIGateway()

    print("=== AI Gateway Demo ===\n")

    # Check provider health
    health = await gateway.health()
    print(f"Provider health: {health}\n")

    # Send a completion through the full middleware chain
    response = await gateway.complete(
        authorization="Bearer sk-demo-standard-001",
        messages=[
            Message(role=MessageRole.SYSTEM, content="You are a helpful assistant."),
            Message(role=MessageRole.USER, content="What is an AI gateway?"),
        ],
        model="google/gemini-2.5-flash",
    )

    print(f"Provider:  {response.provider}")
    print(f"Model:     {response.model}")
    print(f"Tokens:    {response.usage.total_tokens}")
    print(f"Latency:   {response.latency_ms:.0f}ms")
    print(f"Response:  {response.content[:200]}...")
    print()

    # Show cost tracking
    summary = gateway.get_cost_summary("key-std-001")
    print(f"Total spend for key: ${summary['total_cost']:.6f}")

    # Show rate limit status
    status = gateway.get_rate_limit_status("key-std-001", tier="standard")
    print(f"Rate limit: {status['requests_used']}/{status['requests_limit']} requests")


if __name__ == "__main__":
    asyncio.run(demo())
