# Architecture Prompts

> Prompts for architectural discussions and design decisions with AI. These implement **Pattern 4: Architecture Ownership** from the [8 Patterns for Effective AI Coding](../../../book/part-2-building/05-building-with-ai/04-the-8-patterns-for-effective-ai-coding.md).

The rule: if you cannot draw the architecture on a whiteboard, you are not ready to ask AI to implement it. Component boundaries, data models, API contracts, error handling strategies -- these are human decisions. The AI executes them.

---

## Prompt 1: Architecture Exploration (Before Deciding)

**When to use:** You have a feature or system to build but have not committed to an architecture. You want the AI to help you think through options, not to decide for you.

**Pattern:** Architecture Ownership + Context First

```
I need to design the architecture for {FEATURE/SYSTEM}.

Context:
- Current tech stack: {stack details}
- Scale requirements: {e.g., 1000 requests/second, 10M records}
- Team size: {e.g., 2 engineers, 15-person team}
- Timeline: {e.g., MVP in 2 weeks, production in 6 weeks}

Requirements:
1. {Functional requirement}
2. {Functional requirement}
3. {Non-functional requirement, e.g., latency under 200ms}

Constraints:
- {e.g., Must integrate with existing auth system}
- {e.g., Cannot add more than 2 new services}
- {e.g., Budget for infrastructure under $500/month}

Present 2-3 architectural approaches. For each one:
1. Describe the approach in 3-5 sentences
2. Draw a component diagram (ASCII or Mermaid)
3. List 3 advantages and 3 disadvantages
4. Identify the biggest risk
5. Estimate the implementation effort

Do NOT recommend one. I will decide after seeing the tradeoffs.
```

**Tips:**
- "Do NOT recommend one" is essential. The moment you let the AI choose your architecture, you have violated Pattern 4. You own structure. The AI surfaces options.
- Include team size and timeline. A two-person team with a two-week deadline should not get the same architecture as a fifteen-person team with six months. The AI will not factor this in unless you tell it.
- Asking for the "biggest risk" per approach forces the AI to think adversarially about each option. This surfaces failure modes you might not consider.

---

## Prompt 2: Architecture Decision Record (ADR)

**When to use:** You have made an architectural decision and want to document it clearly so the AI (and your team) can reference it in future sessions.

**Pattern:** Architecture Ownership + Concrete Examples

```
Write an Architecture Decision Record for the following decision.

Title: {e.g., Use event sourcing for order management}

Context:
- {Why this decision was needed}
- {What alternatives were considered}
- {What constraints shaped the decision}

Decision:
- {The chosen approach, in 2-3 sentences}

Consequences:
- {What becomes easier}
- {What becomes harder}
- {What new constraints this introduces}

Format the ADR using this template:

# ADR-{NUMBER}: {TITLE}
## Status: {Accepted/Proposed/Deprecated}
## Date: {YYYY-MM-DD}
## Context
## Decision
## Consequences
## Alternatives Considered
```

**Tips:**
- ADRs serve double duty: they document decisions for the team and provide persistent context for AI coding sessions. Point the AI to your ADR directory at the start of any session that touches that area.
- "Alternatives Considered" prevents relitigating the same decision. When someone (or an AI) asks "why didn't we use X," the ADR already has the answer.
- Keep ADRs short. One page maximum. The goal is a reference, not an essay.

---

## Prompt 3: Component Boundary Definition

**When to use:** You are about to implement a system and need to define clear boundaries between components before the AI starts writing code.

**Pattern:** Architecture Ownership + Test-Driven Prompting

```
I'm defining the component boundaries for {SYSTEM}.

The system has these components:
1. {Component A} -- {responsibility in one sentence}
2. {Component B} -- {responsibility in one sentence}
3. {Component C} -- {responsibility in one sentence}

For each component:
1. Define the public interface (functions/methods/endpoints it exposes)
2. Define what it depends on (other components, external services)
3. Define what it does NOT do (explicit exclusions)
4. Define the data it owns vs. data it reads from others

Then define the contracts between components:
- {A} calls {B} via: {interface description}
- {B} notifies {A} via: {interface description}

Rules:
- No component should depend on the internals of another
- Each component should be testable in isolation
- Data ownership must be clear -- no shared mutable state

Write these as interface definitions in {LANGUAGE}, not full
implementations. I want to review the boundaries before any
implementation begins.
```

**Tips:**
- Defining "what it does NOT do" is as important as defining what it does. Without explicit exclusions, the AI will drift responsibilities into whichever component it happens to be implementing.
- Interface definitions before implementation enforces the architecture. The AI implements to an interface, not around one.
- This pairs directly with the contract tests prompt in [Test-Driven Prompts](test-driven-prompts.md). Define boundaries here, then write contract tests to enforce them.

---

## Prompt 4: Migration and Refactoring Plan

**When to use:** You need to restructure existing code and want a plan that minimizes risk. Architectural changes are where AI-generated code is most dangerous -- 80-90% suffers from avoidance of refactors.

**Pattern:** Architecture Ownership + Checkpoint Commits

```
I need to refactor {MODULE/SYSTEM} from {CURRENT_STATE} to
{TARGET_STATE}.

Current architecture:
---
{Describe or paste the current structure}
---

Target architecture:
---
{Describe the desired end state}
---

Constraints:
- The system must remain functional throughout the migration
- {e.g., No downtime for users}
- {e.g., Database migrations must be reversible}
- {e.g., Old and new must coexist during transition}

Create a step-by-step migration plan where:
1. Each step is independently deployable
2. Each step can be rolled back without affecting other steps
3. Each step has a verification check (test or manual)
4. The order minimizes risk (least risky changes first)

For each step, specify:
- What changes
- What to verify after the change
- How to roll back if verification fails
- Estimated risk (low/medium/high)

Do NOT write the code. I want the plan reviewed before any
implementation starts.
```

**Tips:**
- "Each step is independently deployable" forces granularity. The AI's instinct is to plan a big-bang migration. Resist this.
- Rollback instructions per step implement Pattern 7 (Checkpoint Commits) at the architectural level. Every step should be reversible.
- Having the AI estimate risk per step helps you prioritize review effort. Spend more time reviewing "high risk" steps.

---

## Prompt 5: Technology Evaluation

**When to use:** You are considering adding a new technology to your stack and want structured analysis before committing.

**Pattern:** Architecture Ownership + Context First

```
I'm evaluating whether to use {TECHNOLOGY} for {USE CASE}.

Current stack: {relevant current technologies}
Team experience with {TECHNOLOGY}: {none/some/expert}
Scale requirements: {expected load, data volume, user count}

Evaluate this technology against these criteria:

1. Fit: How well does it solve the specific problem?
2. Complexity: What does it add to operational burden?
3. Lock-in: How hard is it to switch away later?
4. Maturity: Is it production-proven at our scale?
5. Team: Can our team operate it without hiring specialists?

For each criterion, rate it 1-5 and explain the rating.

Then answer:
- What is the simplest alternative that might work?
- What scale threshold would make this technology necessary?
- What would we regret in 12 months if we adopted this today?
- What would we regret if we did NOT adopt it?

Do NOT recommend adopt or reject. Present the analysis and let me
decide.
```

**Tips:**
- "What is the simplest alternative" implements the book's infrastructure principle: sophistication should lag revenue, not lead it.
- The "regret in 12 months" questions force the AI to think about long-term consequences, not just immediate capabilities.
- Team experience matters more than technical superiority. A technology your team cannot operate is worse than a less capable one they already know. This aligns with the book's Chapter 4 guidance on boring infrastructure.

---

## Related Prompts

- [Context Loading](context-loading.md) -- load project context before architecture discussions
- [Test-Driven Prompts](test-driven-prompts.md) -- write contract tests to enforce boundaries
- [Review Prompts](review-prompts.md) -- review architectural implementation for drift
