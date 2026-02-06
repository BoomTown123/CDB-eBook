"""
Unified Auth --- main module.

Ties together human auth, agent auth, permissions, and audit logging
into a single interface. This is the entry point: callers use
UnifiedAuth without needing to know whether the actor is a human
or an agent.

The four principles this implements (from the book):
1. One model, different authentication methods
2. Permissions flow down, never up
3. Every action traces to a human
4. Tokens die with tasks

Reference: Chapter 4 - Unified Auth for Humans AND Agents

Usage:
    auth = UnifiedAuth()

    # Human logs in
    human = auth.login("alice@example.com", "demo-password")

    # Human triggers an agent (delegation)
    agent = auth.delegate_to_agent(
        human=human,
        agent_id="scheduling-agent-001",
        agent_type="scheduling",
        task_id="task-abc",
        scoped_resources={"calendar", "contacts"},
    )

    # Check if the agent can perform an action
    result = auth.check_agent_action(
        agent=agent,
        resource="calendar",
        action="read",
    )
    # result == "allowed"

    # Agent delegates to a sub-agent (attenuated permissions)
    sub_agent = auth.delegate_to_sub_agent(
        parent=agent,
        agent_id="room-agent-002",
        agent_type="room_availability",
        task_id="task-abc-sub1",
        scoped_resources={"calendar"},
        read_only=True,
    )

    # Task completes --- revoke all tokens
    auth.revoke_task("task-abc")
"""

from permissions import AccessTier, PermissionSet, ResourceAction
from human_auth import HumanAuth, HumanIdentity
from agent_auth import AgentAuth, AgentIdentity
from audit import AuditLog


class UnifiedAuth:
    """
    Single entry point for human + agent authentication.

    Both humans and agents flow through the same permission model,
    the same policy engine, the same audit system. Only the
    authentication method differs.
    """

    def __init__(self) -> None:
        self._human_auth = HumanAuth()
        self._agent_auth = AgentAuth()
        self._audit = AuditLog()

    # ---- Human authentication ---------------------------------------------

    def login(self, email: str, password: str) -> HumanIdentity:
        """Authenticate a human user."""
        try:
            identity = self._human_auth.login(email, password)
            self._audit.log_human_login(identity.user_id, email)
            return identity
        except Exception as exc:
            self._audit.log_human_login_failed(email, str(exc))
            raise

    def validate_session(self, session_token: str) -> HumanIdentity:
        """Validate an existing human session."""
        return self._human_auth.validate_session(session_token)

    def logout(self, human: HumanIdentity) -> None:
        """End a human session."""
        self._human_auth.logout(human.session_token)
        self._audit.log_human_logout(human.user_id)

    # ---- Agent delegation -------------------------------------------------

    def delegate_to_agent(
        self,
        human: HumanIdentity,
        agent_id: str,
        agent_type: str,
        task_id: str,
        scoped_resources: set[str] | None = None,
    ) -> AgentIdentity:
        """
        Human delegates to an agent.

        The agent gets a subset of the human's permissions, scoped to
        the resources this task requires. The full delegation chain is
        recorded in the audit log.
        """
        agent = self._agent_auth.delegate_from_human(
            human=human,
            agent_id=agent_id,
            agent_type=agent_type,
            task_id=task_id,
            scoped_resources=scoped_resources,
        )
        self._audit.log_delegation(
            parent_id=human.user_id,
            agent_id=agent_id,
            task_id=task_id,
            delegation_chain=agent.delegation_chain,
            scoped_resources=list(scoped_resources) if scoped_resources else None,
        )
        return agent

    def delegate_to_sub_agent(
        self,
        parent: AgentIdentity,
        agent_id: str,
        agent_type: str,
        task_id: str,
        scoped_resources: set[str] | None = None,
        read_only: bool = False,
    ) -> AgentIdentity:
        """
        Agent delegates to a sub-agent (permission attenuation).

        Permissions can only decrease. The delegation chain grows.
        """
        sub_agent = self._agent_auth.delegate_from_agent(
            parent=parent,
            agent_id=agent_id,
            agent_type=agent_type,
            task_id=task_id,
            scoped_resources=scoped_resources,
            read_only=read_only,
        )
        self._audit.log_delegation(
            parent_id=parent.agent_id,
            agent_id=agent_id,
            task_id=task_id,
            delegation_chain=sub_agent.delegation_chain,
            scoped_resources=list(scoped_resources) if scoped_resources else None,
        )
        return sub_agent

    # ---- Permission checks ------------------------------------------------

    def check_agent_action(
        self,
        agent: AgentIdentity,
        resource: str,
        action: str,
    ) -> str:
        """
        Check whether an agent can perform an action.

        Returns:
            "allowed"    --- FREE tier, execute autonomously
            "supervised" --- SUPERVISED tier, needs human approval
            "denied"     --- FORBIDDEN tier or no permission at all
        """
        resource_action = ResourceAction(action)
        tier = self._agent_auth.check_permission(agent, resource, resource_action)

        if tier == AccessTier.FREE:
            result = "allowed"
        elif tier == AccessTier.SUPERVISED:
            result = "supervised"
        else:
            result = "denied"

        self._audit.log_permission_check(
            actor_id=agent.agent_id,
            resource=resource,
            action=action,
            result=result,
            delegation_chain=agent.delegation_chain,
            task_id=agent.task_id,
        )

        return result

    # ---- Revocation -------------------------------------------------------

    def revoke_agent(self, agent: AgentIdentity, reason: str = "") -> None:
        """Immediately revoke a single agent's token."""
        self._agent_auth.revoke_token(agent.delegation_token)
        self._audit.log_token_revoked(agent.agent_id, reason)

    def revoke_task(self, task_id: str) -> int:
        """
        Revoke ALL tokens for a task. Atomic cleanup.

        When a task completes (or fails), call this to ensure no
        agent tokens persist beyond their purpose.
        """
        count = self._agent_auth.revoke_task(task_id)
        self._audit.log_task_revoked(task_id, count)
        return count

    # ---- Audit queries ----------------------------------------------------

    @property
    def audit_log(self) -> AuditLog:
        """Direct access to the audit log for queries."""
        return self._audit


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo() -> None:
    """
    Demonstrate the unified auth flow end-to-end.

    Shows: login -> delegation -> permission check -> sub-delegation
    -> permission attenuation -> task revocation -> audit trail.
    """
    auth = UnifiedAuth()
    print("=== Unified Auth Demo ===\n")

    # 1. Human logs in
    alice = auth.login("alice@example.com", "demo-password")
    print(f"1. Alice logged in: {alice.user_id} (role={alice.role})")

    # 2. Alice delegates to a scheduling agent
    sched_agent = auth.delegate_to_agent(
        human=alice,
        agent_id="scheduling-agent-001",
        agent_type="scheduling",
        task_id="task-abc",
        scoped_resources={"documents", "analytics"},
    )
    print(f"2. Delegated to agent: {sched_agent.agent_id}")
    print(f"   Delegation chain: {sched_agent.delegation_chain}")

    # 3. Check agent permissions
    read_docs = auth.check_agent_action(sched_agent, "documents", "read")
    delete_docs = auth.check_agent_action(sched_agent, "documents", "delete")
    read_users = auth.check_agent_action(sched_agent, "users", "read")
    print(f"3. documents:read = {read_docs}")
    print(f"   documents:delete = {delete_docs}")
    print(f"   users:read = {read_users} (not in scoped resources)")

    # 4. Sub-delegation with read-only attenuation
    sub_agent = auth.delegate_to_sub_agent(
        parent=sched_agent,
        agent_id="analysis-agent-002",
        agent_type="analysis",
        task_id="task-abc-sub1",
        scoped_resources={"documents"},
        read_only=True,
    )
    print(f"4. Sub-delegated to: {sub_agent.agent_id}")
    print(f"   Chain: {sub_agent.delegation_chain}")

    sub_read = auth.check_agent_action(sub_agent, "documents", "read")
    sub_write = auth.check_agent_action(sub_agent, "documents", "update")
    print(f"   documents:read = {sub_read}")
    print(f"   documents:update = {sub_write} (attenuated to read-only)")

    # 5. Task completes --- revoke everything
    revoked = auth.revoke_task("task-abc")
    print(f"5. Revoked {revoked} token(s) for task-abc")

    # 6. Audit trail
    print(f"\n=== Audit Log ({auth.audit_log.total_entries} entries) ===")
    for entry in auth.audit_log.query(limit=20):
        print(f"   [{entry.event_type.value}] actor={entry.actor_id} "
              f"resource={entry.resource} result={entry.result}")


if __name__ == "__main__":
    demo()
