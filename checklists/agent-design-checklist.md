# Checklist: Agent Design

> Before building an AI agent -- design decisions, failure prevention, and operational readiness.

Use this checklist before writing the first line of agent code. Agents fail differently than traditional software because they reason probabilistically and act autonomously. The seven failure modes documented here are drawn from real incidents, not hypotheticals. Working through each section forces you to design the failure path before the happy path.

*Derived from the [7 Failure Modes of Agents](../frameworks/7-failure-modes-of-agents.md) framework -- Chapter 6.*

---

## Agent Type Selection

- [ ] Determined whether you are building a **chat agent** (user-facing, conversational) or a **background agent** (autonomous, unsupervised)
- [ ] Understood the different risk profiles: chat agents are more susceptible to hallucinated actions, scope creep, and context loss; background agents are more prone to infinite loops, cascading failures, resource exhaustion, and stale data
- [ ] Defined the agent's **autonomy level** using the permission spectrum: what can it do without approval, what requires confirmation, what is never allowed
- [ ] Established "done when" criteria -- the agent has a clear definition of task completion, not an open-ended mandate
- [ ] Determined whether the agent needs to interact with other agents, and if so, designed the communication pattern (hub-and-spoke with circuit breakers, not peer-to-peer)

## Tool Design

- [ ] Created an **allowlist** of valid tools, APIs, and functions the agent can call -- anything not on the list is rejected by default
- [ ] Built a **tool registry** that validates all tool calls before execution; unknown tools fail fast with clear error messages
- [ ] Defined explicit input/output schemas for each tool so the agent can't pass malformed or unexpected parameters
- [ ] Tiered tool permissions by risk level: read-only operations are permitted freely, write operations require confirmation, destructive operations (DELETE, DROP) are **never permitted** in production
- [ ] Ensured tools return structured responses with explicit error codes that the agent can reason about, not ambiguous messages

## Context Management

- [ ] Set a context degradation threshold: for chat agents, context summarization triggers every **10 turns** to prevent drift
- [ ] Built explicit **state checkpointing** for background agents running multi-step or multi-day workflows
- [ ] Provided a mechanism for users to trigger "remind yourself what we discussed" to recover lost context
- [ ] Defined maximum conversation or task length -- context degrades meaningfully after 30-50 messages without active management
- [ ] Designed context storage so that critical information (user intent, constraints, prior decisions) is preserved outside the conversation window

## Failure Prevention

Work through each of the seven failure modes and confirm mitigations are in place.

### Hallucinated Actions

- [ ] All tool calls are validated against the tool registry before execution -- the agent can't call APIs, functions, or tools that don't exist
- [ ] Responses that reference policies, prices, or commitments are grounded in source documents, not generated from the model's training data
- [ ] Understood the liability precedent: your company is legally responsible for what its agents say (Air Canada, February 2024)

### Infinite Loops

- [ ] Set a **maximum iteration count** (default: 10) for any looping or retry behavior
- [ ] Set a **maximum timeout** (default: 5 minutes) for any single task or subtask
- [ ] Built alerting that triggers after **3 iterations without progress** -- not just after the limit is hit
- [ ] Retry logic includes exponential backoff, not blind retries at full speed

### Scope Creep

- [ ] Each task has explicit **"done when" criteria** that the agent checks against
- [ ] Out-of-scope actions require explicit user confirmation before execution
- [ ] Permissions are tiered by task type -- the agent can't escalate its own authority
- [ ] Tested with adversarial prompts to confirm the agent doesn't agree to requests outside its mandate (Chevrolet dealership incident, December 2023)

### Context Loss

- [ ] Context summarization runs automatically at defined intervals (every 10 turns for chat agents)
- [ ] Background agents checkpoint state explicitly at each major step
- [ ] Contradiction detection is in place: the agent flags when its current response conflicts with earlier statements
- [ ] Long-running tasks are broken into discrete stages with state persisted between stages

### Cascading Failures

- [ ] Agents are **isolated by default** -- one agent's failure can't directly trigger failures in dependent agents or systems
- [ ] Inter-agent communication routes through a **hub with circuit breakers**: if one agent fails 3 times, it is isolated until manually reviewed
- [ ] No agent has DELETE or DROP TABLE permissions in production databases
- [ ] Understood the worst case: an agent with production database access and no isolation caused complete deletion of a production database after 9 days of erratic behavior (Replit incident, July 2025)

### Resource Exhaustion

- [ ] Assigned a **token budget** per task with hard limits
- [ ] Built alerting at **80% of budget** consumption -- before the limit is reached, not after
- [ ] Tasks exceeding limits are terminated with a clear explanation to the user or operator
- [ ] **Cost monitoring infrastructure is in place before the agent is deployed** -- not planned for later (73% of teams lack real-time cost tracking; enterprise overruns average 340%)

### Stale Data

- [ ] Defined **freshness requirements** for every data source the agent depends on
- [ ] The agent checks data age before acting on any external data
- [ ] Refresh intervals are set for all data sources and enforced automatically
- [ ] Timestamp checking and inconsistency monitoring are active -- the agent flags when data sources contradict each other or appear outdated

## Testing and Monitoring

- [ ] Built the **four-layer resilience framework**: Detection (dashboards and alerts for each failure mode), Prevention (guardrails in agent design), Recovery (graceful degradation and human handoff), Learning (post-incident analysis)
- [ ] Started with **Detection first** -- you can't prevent what you can't see
- [ ] Designed the **failure path before the happy path**: every agent has a graceful degradation plan and a human handoff trigger
- [ ] Tested the agent with adversarial inputs, not just golden-path scenarios
- [ ] Established a post-incident analysis process where every agent failure becomes a training example and a new test case
- [ ] Defined escalation criteria: what conditions trigger automatic human handoff vs. alert-only vs. agent self-recovery
- [ ] Monitoring covers all seven failure modes with distinct dashboards or alert channels -- not a single generic "agent health" metric

---

**Next step:** For each unchecked item, determine whether it is a blocker (must be resolved before deployment) or a follow-up (can be addressed in the first iteration cycle). No agent should reach production without the Failure Prevention section fully checked.
