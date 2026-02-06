"""
Human user authentication for unified auth.

Handles the interactive authentication path: username/password, SSO,
MFA. The output is a session token that carries the user's identity
and permissions --- the same permission model that agents use.

In production, replace this with your identity provider (Supabase Auth,
Auth0, Okta, etc.). The interface stays the same: authenticate
credentials, return an identity with a PermissionSet.

Reference: Chapter 4 - Unified Auth for Humans AND Agents
    "One Model, Different Authentication Methods"
"""

import hashlib
import secrets
import time
from dataclasses import dataclass, field
from typing import Any

from permissions import AccessTier, PermissionSet, ADMIN_PERMISSIONS, EDITOR_PERMISSIONS, VIEWER_PERMISSIONS


@dataclass
class HumanIdentity:
    """
    Authenticated human user.

    Carries the user's ID, role, permission set, and session metadata.
    When this user triggers an agent, the agent inherits a subset of
    these permissions (see agent_auth.py).
    """
    user_id: str
    email: str
    role: str
    permissions: PermissionSet
    session_token: str = ""
    session_expires_at: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_session_valid(self) -> bool:
        return time.time() < self.session_expires_at


# ---- In-memory user store (replace with a real database) ------------------

_USERS: dict[str, dict[str, Any]] = {
    "alice@example.com": {
        "user_id": "usr-alice-001",
        "password_hash": hashlib.sha256(b"demo-password").hexdigest(),
        "role": "admin",
        "active": True,
    },
    "bob@example.com": {
        "user_id": "usr-bob-002",
        "password_hash": hashlib.sha256(b"demo-password").hexdigest(),
        "role": "editor",
        "active": True,
    },
    "carol@example.com": {
        "user_id": "usr-carol-003",
        "password_hash": hashlib.sha256(b"demo-password").hexdigest(),
        "role": "viewer",
        "active": True,
    },
}

_ROLE_PERMISSIONS: dict[str, PermissionSet] = {
    "admin": ADMIN_PERMISSIONS,
    "editor": EDITOR_PERMISSIONS,
    "viewer": VIEWER_PERMISSIONS,
}

_ACTIVE_SESSIONS: dict[str, HumanIdentity] = {}

SESSION_DURATION_SECONDS: float = 3600.0  # 1 hour


class AuthenticationError(Exception):
    """Raised when human authentication fails."""


class HumanAuth:
    """
    Authenticate human users and issue session tokens.

    This is the interactive authentication path. The output is a
    HumanIdentity with a PermissionSet that can later be delegated
    to agents via agent_auth.py.

    Usage:
        auth = HumanAuth()
        identity = auth.login("alice@example.com", "demo-password")
        print(identity.permissions)

        # Later: validate session
        identity = auth.validate_session(identity.session_token)
    """

    def __init__(
        self,
        users: dict[str, dict[str, Any]] | None = None,
        session_duration: float = SESSION_DURATION_SECONDS,
    ) -> None:
        self._users = users or _USERS
        self._sessions = _ACTIVE_SESSIONS
        self._session_duration = session_duration

    def login(self, email: str, password: str) -> HumanIdentity:
        """
        Authenticate with email + password and return a session.

        In production, this would go through your IdP with MFA, SSO, etc.
        The point of this example is the *output*: a HumanIdentity with
        a PermissionSet that feeds into the unified auth model.
        """
        user = self._users.get(email)
        if user is None:
            raise AuthenticationError("Invalid credentials")

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if not secrets.compare_digest(password_hash, user["password_hash"]):
            raise AuthenticationError("Invalid credentials")

        if not user.get("active", False):
            raise AuthenticationError("Account is deactivated")

        role = user["role"]
        permissions = _ROLE_PERMISSIONS.get(role, VIEWER_PERMISSIONS)

        session_token = f"sess-{secrets.token_hex(16)}"
        expires_at = time.time() + self._session_duration

        identity = HumanIdentity(
            user_id=user["user_id"],
            email=email,
            role=role,
            permissions=permissions,
            session_token=session_token,
            session_expires_at=expires_at,
        )

        self._sessions[session_token] = identity
        return identity

    def validate_session(self, session_token: str) -> HumanIdentity:
        """Validate an existing session token."""
        identity = self._sessions.get(session_token)
        if identity is None:
            raise AuthenticationError("Invalid or expired session")
        if not identity.is_session_valid:
            del self._sessions[session_token]
            raise AuthenticationError("Session expired")
        return identity

    def logout(self, session_token: str) -> None:
        """Invalidate a session immediately."""
        self._sessions.pop(session_token, None)
