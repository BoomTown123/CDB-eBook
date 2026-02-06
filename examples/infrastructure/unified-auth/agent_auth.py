"""
Agent authentication with scoped, delegated permissions.

Implements the book's core auth principle: an agent should never have
more permissions than the human who triggered it. Agents authenticate
via delegation tokens --- not shared credentials --- scoped to the
specific task and resources they need.

The delegation chain is cryptographically traceable:
    Alice -> Scheduling Agent -> Room Agent -> Calendar API

Each hop attenuates (reduces) permissions. When the task completes,
all tokens expire.

Reference: Chapter 4 - Unified Auth for Humans AND Agents
    "The 4 Principles of Unified Auth"
"""

import secrets
import time
from dataclasses import dataclass, field
from typing import Any

from permissions import AccessTier, PermissionSet, ResourceAction
from human_auth import HumanIdentity


@dataclass
class AgentIdentity:
    """
    Authenticated agent with delegated permissions.

    Every agent identity traces back to a human principal via the
    delegation_chain field. No orphan agents: when something goes
    wrong, you can answer "who let this agent do that?" immediately.
    """
    agent_id: str
    agent_type: str
    permissions: PermissionSet
    delegation_chain: list[str]
    delegation_token: str = ""
    token_expires_at: float = 0.0
    task_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_token_valid(self) -> bool:
        return time.time() < self.token_expires_at

    @property
    def principal(self) -> str:
        """The human at the root of the delegation chain."""
        return self.delegation_chain[0] if self.delegation_chain else "unknown"


# Default token lifetime --- short by design. Tokens die with tasks.
AGENT_TOKEN_DURATION_SECONDS: float = 300.0  # 5 minutes

_ACTIVE_AGENT_TOKENS: dict[str, AgentIdentity] = {}


class DelegationError(Exception):
    """Raised when delegation violates auth principles."""


class AgentAuth:
    """
    Issue and validate delegation tokens for AI agents.

    The core pattern: a human (or parent agent) creates a scoped
    delegation token for a child agent. The child's permissions are
    always equal to or less than the parent's. Tokens are short-lived
    and task-bound.

    Usage:
        agent_auth = AgentAuth()

        # Human triggers an agent
        agent = agent_auth.delegate_from_human(
            human=alice_identity,
            agent_id="scheduling-agent-001",
            agent_type="scheduling",
            task_id="task-abc",
            scoped_resources={"calendar", "contacts"},
        )

        # Agent delegates to a sub-agent (permissions attenuate)
        sub_agent = agent_auth.delegate_from_agent(
            parent=agent,
            agent_id="room-agent-002",
            agent_type="room_availability",
            task_id="task-abc-sub1",
            scoped_resources={"calendar"},
            read_only=True,
        )
    """

    def __init__(
        self,
        token_duration: float = AGENT_TOKEN_DURATION_SECONDS,
    ) -> None:
        self._token_duration = token_duration
        self._active_tokens = _ACTIVE_AGENT_TOKENS

    def delegate_from_human(
        self,
        human: HumanIdentity,
        agent_id: str,
        agent_type: str,
        task_id: str,
        scoped_resources: set[str] | None = None,
    ) -> AgentIdentity:
        """
        Create an agent identity delegated from a human user.

        The agent inherits a subset of the human's permissions,
        scoped to the resources this task requires. If no resources
        are specified, the agent gets ALL of the human's permissions
        (still bounded by the human's own access).
        """
        if not human.is_session_valid:
            raise DelegationError("Cannot delegate from an expired human session")

        # Attenuate permissions to requested resources
        if scoped_resources:
            permissions = human.permissions.attenuate(scoped_resources)
        else:
            permissions = human.permissions

        token = f"agent-{secrets.token_hex(16)}"
        expires_at = time.time() + self._token_duration

        agent = AgentIdentity(
            agent_id=agent_id,
            agent_type=agent_type,
            permissions=permissions,
            delegation_chain=[human.user_id, agent_id],
            delegation_token=token,
            token_expires_at=expires_at,
            task_id=task_id,
        )

        self._active_tokens[token] = agent
        return agent

    def delegate_from_agent(
        self,
        parent: AgentIdentity,
        agent_id: str,
        agent_type: str,
        task_id: str,
        scoped_resources: set[str] | None = None,
        read_only: bool = False,
    ) -> AgentIdentity:
        """
        Create a sub-agent identity delegated from a parent agent.

        Permissions can only decrease:
        - Scope to fewer resources (scoped_resources)
        - Reduce to read-only (read_only=True)
        - Never increase beyond the parent's permissions

        The delegation chain grows: [Alice, ParentAgent, ChildAgent].
        """
        if not parent.is_token_valid:
            raise DelegationError("Cannot delegate from an expired agent token")

        # Start with parent's permissions
        permissions = parent.permissions

        # Attenuate to requested resources
        if scoped_resources:
            permissions = permissions.attenuate(scoped_resources)

        # Optionally reduce to read-only
        if read_only:
            permissions = permissions.attenuate_to_read_only()

        token = f"agent-{secrets.token_hex(16)}"

        # Sub-agent token can never outlive its parent
        expires_at = min(
            time.time() + self._token_duration,
            parent.token_expires_at,
        )

        agent = AgentIdentity(
            agent_id=agent_id,
            agent_type=agent_type,
            permissions=permissions,
            delegation_chain=parent.delegation_chain + [agent_id],
            delegation_token=token,
            token_expires_at=expires_at,
            task_id=task_id,
        )

        self._active_tokens[token] = agent
        return agent

    def validate_token(self, token: str) -> AgentIdentity:
        """Validate an agent delegation token."""
        agent = self._active_tokens.get(token)
        if agent is None:
            raise DelegationError("Invalid or expired agent token")
        if not agent.is_token_valid:
            del self._active_tokens[token]
            raise DelegationError("Agent token has expired")
        return agent

    def check_permission(
        self,
        agent: AgentIdentity,
        resource: str,
        action: ResourceAction,
    ) -> AccessTier | None:
        """
        Check what tier an action falls into for this agent.

        Returns the AccessTier (FREE / SUPERVISED / FORBIDDEN) or None
        if the agent has no permission for this resource+action at all.
        """
        return agent.permissions.get_tier(resource, action)

    def revoke_token(self, token: str) -> None:
        """Immediately revoke an agent's token. Real-time revocation."""
        self._active_tokens.pop(token, None)

    def revoke_task(self, task_id: str) -> int:
        """
        Revoke ALL tokens associated with a task.

        When a parent task dies abnormally, this atomically removes all
        downstream agent access. Revocation latency should be measured
        in milliseconds, not minutes.
        """
        to_revoke = [
            token for token, agent in self._active_tokens.items()
            if agent.task_id == task_id
        ]
        for token in to_revoke:
            del self._active_tokens[token]
        return len(to_revoke)
