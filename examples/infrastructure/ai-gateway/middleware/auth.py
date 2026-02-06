"""
Authentication middleware for the AI Gateway.

Validates API keys (or JWTs) before a request reaches any provider.
This is the first middleware in the chain --- unauthenticated requests
never touch the AI backend.

The book's gateway pattern (Chapter 4) uses the x-authorized-tools
header with signed JWTs for tool-level access control. This simplified
example demonstrates the same pattern with API key authentication.

Reference: Chapter 4 - The AI Tool Gateway Pattern
"""

import hashlib
import hmac
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AuthContext:
    """Carries identity information through the middleware chain."""
    api_key_id: str
    tier: str = "free"
    scopes: list[str] = field(default_factory=lambda: ["completions"])
    metadata: dict[str, Any] = field(default_factory=dict)


# ---- In-memory key store (replace with a database in production) ----------

_API_KEYS: dict[str, dict[str, Any]] = {
    "sk-demo-free-001": {
        "id": "key-free-001",
        "tier": "free",
        "scopes": ["completions"],
        "active": True,
    },
    "sk-demo-standard-001": {
        "id": "key-std-001",
        "tier": "standard",
        "scopes": ["completions", "streaming"],
        "active": True,
    },
    "sk-demo-enterprise-001": {
        "id": "key-ent-001",
        "tier": "enterprise",
        "scopes": ["completions", "streaming", "fine-tuning"],
        "active": True,
    },
}


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class AuthorizationError(Exception):
    """Raised when a valid key lacks the required scope."""


class AuthMiddleware:
    """
    Authenticate incoming requests by API key.

    In production, replace the in-memory store with your identity
    provider (Auth0, Supabase Auth, etc.). The interface stays the
    same --- validate credentials, return an AuthContext.

    Usage:
        auth = AuthMiddleware()
        ctx = auth.authenticate("Bearer sk-demo-standard-001")
        auth.require_scope(ctx, "streaming")
    """

    def __init__(self, keys: dict[str, dict[str, Any]] | None = None) -> None:
        self._keys = keys or _API_KEYS

    def authenticate(self, authorization_header: str) -> AuthContext:
        """
        Validate the Authorization header and return an AuthContext.

        Accepts "Bearer <key>" format.
        """
        if not authorization_header:
            raise AuthenticationError("Missing Authorization header")

        parts = authorization_header.split(" ", 1)
        if len(parts) != 2 or parts[0] != "Bearer":
            raise AuthenticationError("Authorization header must use Bearer scheme")

        api_key = parts[1]
        key_data = self._keys.get(api_key)

        if key_data is None:
            raise AuthenticationError("Invalid API key")
        if not key_data.get("active", False):
            raise AuthenticationError("API key is deactivated")

        return AuthContext(
            api_key_id=key_data["id"],
            tier=key_data.get("tier", "free"),
            scopes=key_data.get("scopes", ["completions"]),
        )

    @staticmethod
    def require_scope(ctx: AuthContext, scope: str) -> None:
        """Raise AuthorizationError if the context lacks the given scope."""
        if scope not in ctx.scopes:
            raise AuthorizationError(
                f"Key {ctx.api_key_id} lacks required scope: {scope}"
            )

    @staticmethod
    def hash_key_for_logging(api_key: str) -> str:
        """
        Return a safe hash of the key for structured logs.

        Never log raw API keys. This produces a deterministic but
        irreversible identifier for correlation.
        """
        return hashlib.sha256(api_key.encode()).hexdigest()[:12]
