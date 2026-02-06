"""
Audit logging for all auth events.

Every authentication, delegation, permission check, and revocation
gets an immutable audit record. This supports the book's third
principle of unified auth: "Every Action Traces to a Human."

When something goes wrong, you need to answer "who let this agent
do that?" in seconds, not days. The audit log provides that answer.

Reference: Chapter 4 - Unified Auth for Humans AND Agents
"""

import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class AuditEventType(str, Enum):
    """Categories of auditable auth events."""
    HUMAN_LOGIN = "human.login"
    HUMAN_LOGOUT = "human.logout"
    HUMAN_LOGIN_FAILED = "human.login_failed"
    AGENT_DELEGATED = "agent.delegated"
    AGENT_SUBDELEGATED = "agent.subdelegated"
    PERMISSION_CHECK = "permission.check"
    PERMISSION_DENIED = "permission.denied"
    TOKEN_REVOKED = "token.revoked"
    TASK_REVOKED = "task.revoked"
    SESSION_EXPIRED = "session.expired"


@dataclass
class AuditEntry:
    """
    A single immutable audit record.

    Contains the full delegation chain so you can trace any action
    back to the human principal without joining multiple tables.
    """
    timestamp: str
    event_type: AuditEventType
    actor_id: str
    actor_type: str  # "human" or "agent"
    resource: str = ""
    action: str = ""
    result: str = ""  # "allowed", "denied", "supervised"
    delegation_chain: list[str] = field(default_factory=list)
    task_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize to JSON for log ingestion."""
        data = asdict(self)
        data["event_type"] = self.event_type.value
        return json.dumps(data, default=str)


class AuditLog:
    """
    Append-only audit log for auth events.

    In production, write to an append-only store (database with
    immutable rows, object storage, or a dedicated audit service).
    Never allow modification or deletion of audit records --- that
    is a FORBIDDEN-tier operation in the permission model.

    Usage:
        audit = AuditLog()

        audit.log_human_login(user_id="usr-alice-001", email="alice@example.com")

        audit.log_delegation(
            parent_id="usr-alice-001",
            agent_id="scheduling-agent-001",
            task_id="task-abc",
            delegation_chain=["usr-alice-001", "scheduling-agent-001"],
            scoped_resources=["calendar", "contacts"],
        )

        audit.log_permission_check(
            actor_id="scheduling-agent-001",
            resource="calendar",
            action="read",
            result="allowed",
            delegation_chain=["usr-alice-001", "scheduling-agent-001"],
        )

        # Query
        events = audit.query(actor_id="scheduling-agent-001")
        chain_events = audit.trace_delegation_chain("scheduling-agent-001")
    """

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def _now(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def _append(self, entry: AuditEntry) -> None:
        """Append an entry. In production, write to persistent storage."""
        self._entries.append(entry)

    # ---- Human events -----------------------------------------------------

    def log_human_login(self, user_id: str, email: str) -> None:
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=AuditEventType.HUMAN_LOGIN,
            actor_id=user_id,
            actor_type="human",
            details={"email": email},
        ))

    def log_human_login_failed(self, email: str, reason: str) -> None:
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=AuditEventType.HUMAN_LOGIN_FAILED,
            actor_id="unknown",
            actor_type="human",
            details={"email": email, "reason": reason},
        ))

    def log_human_logout(self, user_id: str) -> None:
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=AuditEventType.HUMAN_LOGOUT,
            actor_id=user_id,
            actor_type="human",
        ))

    # ---- Agent delegation events ------------------------------------------

    def log_delegation(
        self,
        parent_id: str,
        agent_id: str,
        task_id: str,
        delegation_chain: list[str],
        scoped_resources: list[str] | None = None,
    ) -> None:
        """Log when a human or agent delegates to an agent."""
        event_type = (
            AuditEventType.AGENT_DELEGATED
            if len(delegation_chain) == 2
            else AuditEventType.AGENT_SUBDELEGATED
        )
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=event_type,
            actor_id=parent_id,
            actor_type="human" if len(delegation_chain) == 2 else "agent",
            delegation_chain=delegation_chain,
            task_id=task_id,
            details={
                "agent_id": agent_id,
                "scoped_resources": scoped_resources or [],
            },
        ))

    # ---- Permission events ------------------------------------------------

    def log_permission_check(
        self,
        actor_id: str,
        resource: str,
        action: str,
        result: str,
        delegation_chain: list[str] | None = None,
        task_id: str = "",
    ) -> None:
        """Log every permission check, whether allowed or denied."""
        event_type = (
            AuditEventType.PERMISSION_DENIED
            if result == "denied"
            else AuditEventType.PERMISSION_CHECK
        )
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=event_type,
            actor_id=actor_id,
            actor_type="agent",
            resource=resource,
            action=action,
            result=result,
            delegation_chain=delegation_chain or [],
            task_id=task_id,
        ))

    # ---- Revocation events ------------------------------------------------

    def log_token_revoked(self, agent_id: str, reason: str = "") -> None:
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=AuditEventType.TOKEN_REVOKED,
            actor_id=agent_id,
            actor_type="agent",
            details={"reason": reason},
        ))

    def log_task_revoked(self, task_id: str, tokens_revoked: int) -> None:
        self._append(AuditEntry(
            timestamp=self._now(),
            event_type=AuditEventType.TASK_REVOKED,
            actor_id="system",
            actor_type="system",
            task_id=task_id,
            details={"tokens_revoked": tokens_revoked},
        ))

    # ---- Queries ----------------------------------------------------------

    def query(
        self,
        actor_id: str | None = None,
        event_type: AuditEventType | None = None,
        task_id: str | None = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """Query the audit log with optional filters."""
        results = self._entries
        if actor_id:
            results = [e for e in results if e.actor_id == actor_id]
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if task_id:
            results = [e for e in results if e.task_id == task_id]
        return results[-limit:]

    def trace_delegation_chain(self, agent_id: str) -> list[AuditEntry]:
        """
        Find all audit entries involving a specific agent in any
        delegation chain. Answers: "what did this agent do, and who
        authorized it?"
        """
        return [
            e for e in self._entries
            if agent_id in e.delegation_chain or e.actor_id == agent_id
        ]

    @property
    def total_entries(self) -> int:
        return len(self._entries)
