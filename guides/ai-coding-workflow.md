# Guide: Working with AI Coding Tools Effectively

> The eight patterns that separate productive AI-assisted development from expensive flailing --- with practical examples and tips for each.

*Based on the [8 Patterns for AI Coding](../frameworks/8-patterns-for-ai-coding.md) framework --- Chapter 5*

## What You'll Learn

How to use AI coding tools in a way that makes you genuinely faster rather than just feeling faster. A randomized controlled trial found developers were 19% slower with AI assistance but predicted they'd be 24% faster --- a 43-point perception gap. These eight patterns close that gap.

## Prerequisites

- An AI coding tool installed and configured (Claude Code, GitHub Copilot, Cursor, or equivalent)
- A codebase you are actively working in
- Git configured for your project (Pattern 7 depends on this)

## Step 1: Context First --- Set Up Before You Code

AI performs dramatically better with background information. Research shows 150--250 tokens is the sweet spot --- enough context to understand the task, not so much that signal drowns in noise.

Before any coding request, provide four things:
1. Your tech stack (language, framework, major libraries)
2. The problem you are solving (not the code you want --- the problem)
3. Constraints that matter (performance requirements, compatibility needs, existing patterns)
4. What you have already tried (prevents the AI from suggesting ruled-out approaches)

Use persistent context files (like CLAUDE.md) to codify project conventions once instead of repeating them every session. Keep the file under 300 lines. Include bash commands for building and testing, code style rules, and `file:line` references over code snippets (snippets become outdated). Never use an LLM for what a linter can do.

**Good context:** "This is a Next.js 14 app using TypeScript, Prisma with PostgreSQL, and Tailwind. I need role-based access control that integrates with our existing middleware in `src/middleware.ts`."

**Bad context:** "Help me with some code."

## Step 2: Concrete Examples --- Show, Don't Tell

AI models are pattern-matching systems. Give them patterns to match. Instead of "follow our coding conventions," show a file that follows them. Make rules measurable: "Function names use camelCase, components use PascalCase, constants use SCREAMING_SNAKE_CASE." Build a library of reference files and point to them when requesting new code.

## Step 3: Iterative Refinement --- Small Requests, Not Big Ones

Small, focused requests produce better results than massive ones. For a single function: one request. For a complete feature: 5--10 iterations. For multi-file changes: multiple sessions.

Request the data model first. Verify. Request business logic. Verify. Request the API layer. Verify. This feels slower. It is faster, because you catch errors early instead of debugging a 500-line output.

## Step 4: Architecture Ownership --- You Decide, AI Implements

You decide structure and design. AI implements your decisions. This is non-negotiable. Research shows 80--90% of AI-generated code suffers from "avoidance of refactors" --- the AI takes the path of least resistance, which compounds into architectural debt. It doesn't know your system's invariants, your scale requirements, or why that pattern exists.

The rule: if you can't draw the architecture on a whiteboard, you aren't ready to ask AI to implement it.

**What you own:** component boundaries, data models, API contracts, error handling strategies, performance approach. **What AI implements:** code within your boundaries, boilerplate, test cases, documentation for the decisions you made.

Start each significant session by writing a brief architecture note before opening the AI tool. Even bullet points work: "Three services: auth, permissions, audit-log. Permissions cached in Redis with 5-minute TTL. Audit-log is async via message queue." Now the AI has a plan to implement, not a blank slate.

## Step 5: Test-Driven Prompting --- Describe Behavior, Not Implementation

Tell the AI what the code should do, not how to do it. Instead of "use a hash map with O(1) lookup," say "it should find items instantly even with 10,000 entries." Write test cases first, then ask the AI to implement code that passes them.

## Step 6: Error Escalation --- Let AI Debug Before You Take Over

When something breaks, follow the escalation ladder:
1. Share the exact error message with the AI
2. Let the AI propose a fix
3. If still broken, provide more context (stack trace, related files, recent changes)
4. After two or three failed attempts at the same problem, take over manually

Two mistakes to avoid: giving up after one failed attempt (AI excels at debugging its own output --- give it a second chance with more context) and persisting past three attempts (the AI is stuck in a loop and won't escape it).

## Step 7: Checkpoint Commits --- Protect Working State

Commit working states before asking AI to make changes. This makes rollback trivial when --- not if --- AI produces something that breaks your code.

The practice: `git add -A && git commit -m "checkpoint: before AI changes"`. Checkpoint before starting sessions, after each verified change, before experimental requests, and before refactors. Without checkpoints, a bad suggestion touching 15 files requires manual revert. With checkpoints, it is a single `git reset --hard HEAD`.

Use plan mode when available. Claude Code's plan mode explores the codebase and designs an approach first, requesting approval before making edits. Read the plan. Think about it. Then approve or redirect.

## Step 8: Review Ruthlessly --- Trust But Verify

AI code needs the same or more review rigor as human code. Only 55% of AI-generated code is secure. XSS vulnerabilities appear 86% of the time. SQL injection appears 20% of the time. Trust in AI code dropped to 29-33% in 2025, down from 43%.

Review as if reviewing a junior developer who thinks they are a senior. Check correctness, style consistency, security vulnerabilities, performance implications, and edge cases. Let AI verify its own work through test suites and browser automation --- self-verification improves quality by 2--3x.

## Session Workflow Summary

1. **Start:** Create a checkpoint commit
2. **Context:** Provide project context or open your CLAUDE.md
3. **Plan:** Describe the architecture at a high level
4. **Iterate:** Make small, focused requests; verify each one
5. **Debug:** When errors occur, escalate through the ladder
6. **Checkpoint:** Commit after each verified working change
7. **Review:** Read every line of generated code before merging

## Key Decisions

| Situation | Do This | Not This |
|-----------|---------|----------|
| Starting a new feature | Write architecture notes first | Ask AI to "build the whole feature" |
| AI output has a bug | Share error, let AI try twice, then take over | Keep pasting the same error |
| Need to follow patterns | Show an example file | Describe the pattern in words |
| Large refactor | Break into 5--10 small changes | One massive "refactor everything" request |
| Reviewing AI output | Read every line, run tests | Glance at it and merge |

---

## Related Resources

- [8 Patterns for AI Coding](../frameworks/8-patterns-for-ai-coding.md) --- The framework summary this guide expands on
- [Human-AI Collaboration](../frameworks/human-ai-collaboration.md) --- The broader collaboration model these patterns implement
- [7 Failure Modes of Agents](../frameworks/7-failure-modes-of-agents.md) --- What goes wrong when agents operate without guardrails
- [Probabilistic AI](../frameworks/probabilistic-ai.md) --- Why AI outputs require the review rigor in Pattern 8

**Full chapter:** [Chapter 5: Building with AI](../book/part-2-building/05-building-with-ai/README.md)
