"""
Permission model for unified human + agent auth.

Implements the book's permission framework: operations classified as
FREE (autonomous), SUPERVISED (human-in-the-loop), or FORBIDDEN
(never automated). This maps directly to the Three-Tier Access Model
from the AI Tool Gateway pattern and the Permission Model Framework.

The key design principle: permissions flow DOWN, never up. An agent
can never have more access than the human who triggered it. Each
delegation hop attenuates permissions further.

Reference: Chapter 4 - Unified Auth for Humans AND Agents
Reference: Chapter 11 - The Permission Model Framework
"""

from dataclasses import dataclass, field
from enum import Enum


class AccessTier(str, Enum):
    """
    Three-tier access model from the book.

    FREE       --- execute autonomously (reversible operations)
    SUPERVISED --- requires human approval (production writes, external comms)
    FORBIDDEN  --- never execute via AI (data deletion, financial, audit mods)
    """
    FREE = "free"
    SUPERVISED = "supervised"
    FORBIDDEN = "forbidden"


class ResourceAction(str, Enum):
    """Standard CRUD + admin actions on any resource."""
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ADMIN = "admin"


@dataclass(frozen=True)
class Permission:
    """A single permission: resource + action + access tier."""
    resource: str
    action: ResourceAction
    tier: AccessTier = AccessTier.FREE

    def __str__(self) -> str:
        return f"{self.resource}:{self.action.value} [{self.tier.value}]"


@dataclass
class PermissionSet:
    """
    A collection of permissions assigned to an identity.

    Supports attenuation: you can create a subset that is equal to
    or narrower than the original. This enforces the principle that
    delegation can only reduce permissions, never increase them.
    """
    permissions: set[Permission] = field(default_factory=set)

    def has(self, resource: str, action: ResourceAction) -> bool:
        """Check whether this set includes the given resource+action."""
        return any(
            p.resource == resource and p.action == action
            for p in self.permissions
        )

    def get_tier(self, resource: str, action: ResourceAction) -> AccessTier | None:
        """Return the access tier for a specific permission, or None."""
        for p in self.permissions:
            if p.resource == resource and p.action == action:
                return p.tier
        return None

    def is_allowed(self, resource: str, action: ResourceAction) -> bool:
        """Check whether the action is FREE-tier (autonomous execution)."""
        tier = self.get_tier(resource, action)
        return tier == AccessTier.FREE

    def requires_approval(self, resource: str, action: ResourceAction) -> bool:
        """Check whether the action requires human-in-the-loop approval."""
        tier = self.get_tier(resource, action)
        return tier == AccessTier.SUPERVISED

    def is_forbidden(self, resource: str, action: ResourceAction) -> bool:
        """Check whether the action is explicitly forbidden."""
        tier = self.get_tier(resource, action)
        return tier == AccessTier.FORBIDDEN

    def attenuate(self, allowed_resources: set[str]) -> "PermissionSet":
        """
        Create a reduced permission set scoped to specific resources.

        This is how delegation works: the parent's permissions are
        filtered to only the resources the child task needs. Permissions
        can only decrease, never increase.
        """
        return PermissionSet(
            permissions={
                p for p in self.permissions if p.resource in allowed_resources
            }
        )

    def attenuate_to_read_only(self) -> "PermissionSet":
        """
        Reduce to read-only access across all resources.

        Useful for sub-agents that only need to query data, not modify it.
        """
        return PermissionSet(
            permissions={
                Permission(
                    resource=p.resource,
                    action=ResourceAction.READ,
                    tier=AccessTier.FREE,
                )
                for p in self.permissions
                if p.action == ResourceAction.READ
            }
        )


# ---------------------------------------------------------------------------
# Pre-built permission sets for common roles
# ---------------------------------------------------------------------------

VIEWER_PERMISSIONS = PermissionSet(
    permissions={
        Permission("users", ResourceAction.READ, AccessTier.FREE),
        Permission("documents", ResourceAction.READ, AccessTier.FREE),
        Permission("analytics", ResourceAction.READ, AccessTier.FREE),
    }
)

EDITOR_PERMISSIONS = PermissionSet(
    permissions={
        Permission("users", ResourceAction.READ, AccessTier.FREE),
        Permission("documents", ResourceAction.READ, AccessTier.FREE),
        Permission("documents", ResourceAction.CREATE, AccessTier.FREE),
        Permission("documents", ResourceAction.UPDATE, AccessTier.FREE),
        Permission("documents", ResourceAction.DELETE, AccessTier.SUPERVISED),
        Permission("analytics", ResourceAction.READ, AccessTier.FREE),
    }
)

ADMIN_PERMISSIONS = PermissionSet(
    permissions={
        Permission("users", ResourceAction.READ, AccessTier.FREE),
        Permission("users", ResourceAction.CREATE, AccessTier.SUPERVISED),
        Permission("users", ResourceAction.UPDATE, AccessTier.SUPERVISED),
        Permission("users", ResourceAction.DELETE, AccessTier.FORBIDDEN),
        Permission("documents", ResourceAction.READ, AccessTier.FREE),
        Permission("documents", ResourceAction.CREATE, AccessTier.FREE),
        Permission("documents", ResourceAction.UPDATE, AccessTier.FREE),
        Permission("documents", ResourceAction.DELETE, AccessTier.SUPERVISED),
        Permission("analytics", ResourceAction.READ, AccessTier.FREE),
        Permission("analytics", ResourceAction.ADMIN, AccessTier.SUPERVISED),
        Permission("billing", ResourceAction.READ, AccessTier.FREE),
        Permission("billing", ResourceAction.UPDATE, AccessTier.FORBIDDEN),
    }
)
