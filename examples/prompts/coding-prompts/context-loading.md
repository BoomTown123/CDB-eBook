# Context Loading Prompts

> Prompts for loading project context into AI coding tools at the start of a session. These implement **Pattern 1: Context First** from the [8 Patterns for Effective AI Coding](../../../book/part-2-building/05-building-with-ai/04-the-8-patterns-for-effective-ai-coding.md).

The optimal context window is 150-250 tokens of bounded, specific information. More context does not mean better answers. These prompts help you hit the sweet spot -- enough to understand the task, not so much that signal drowns in noise.

---

## Prompt 1: Project Onboarding

**When to use:** Starting the first session on a project, or when the AI has no prior context.

**Pattern:** Context First + Concrete Examples

```
You are working on {PROJECT_NAME}, a {LANGUAGE/FRAMEWORK} application.

Tech stack:
- Backend: {e.g., Flask/Python, Express/Node}
- Frontend: {e.g., HTMX, React, Vue}
- Database: {e.g., PostgreSQL with pgvector}
- Infrastructure: {e.g., Vercel, AWS, Railway}

Project structure:
{Paste output of `tree -L 2 src/` or equivalent}

Coding conventions:
- {e.g., Functions use snake_case, classes use PascalCase}
- {e.g., All API endpoints return JSON with {data, error, meta} shape}
- {e.g., Tests live in tests/ mirroring the src/ structure}

Current task: {Brief description of what you are working on}

Before writing any code, confirm you understand the project structure
and ask any clarifying questions.
```

**Tips:**
- Keep the tech stack section to 4-6 bullet points. Listing every dependency dilutes the signal.
- Use `tree` output rather than describing the structure in prose -- the AI parses directory trees more reliably.
- If your project has a CLAUDE.md or similar memory file, point the AI there instead of repeating its contents.

---

## Prompt 2: Session Resume

**When to use:** Resuming work on a project where you have an existing CLAUDE.md or memory file, but need to focus the AI on today's specific task.

**Pattern:** Context First + Iterative Refinement

```
Read the project documentation in CLAUDE.md before starting.

Today I'm working on: {SPECIFIC FEATURE OR BUG}

Relevant files:
- {path/to/main-file.py} -- {what this file does}
- {path/to/related-file.py} -- {why it's relevant}
- {path/to/test-file.py} -- {existing tests for this area}

What I've already tried:
- {Approach 1 and why it didn't work}
- {Approach 2 and its limitations}

Constraints:
- {e.g., Must maintain backward compatibility with v2 API}
- {e.g., Cannot add new dependencies without approval}
- {e.g., Response time must stay under 200ms}

Start by reading the relevant files, then propose an approach
before writing code.
```

**Tips:**
- "What I've already tried" prevents the AI from repeating failed approaches. This is one of the highest-value context items you can provide.
- Listing 2-4 relevant files is better than saying "look at the whole codebase." Bounded context produces bounded (better) output.
- The "propose before writing" instruction applies Pattern 3 (Iterative Refinement) -- get alignment before implementation.

---

## Prompt 3: Codebase Exploration

**When to use:** When you need the AI to understand a part of the codebase you are unfamiliar with, before making changes.

**Pattern:** Context First + Architecture Ownership

```
I need to understand how {FEATURE/MODULE} works in this codebase
before making changes.

Please:
1. Read the following files and summarize what each one does:
   - {path/to/file1}
   - {path/to/file2}
   - {path/to/file3}

2. Map the data flow: how does a {e.g., user request} move through
   these files from entry point to response?

3. Identify:
   - Key functions/classes and their responsibilities
   - External dependencies this module relies on
   - Any error handling patterns in use
   - Tests that cover this area

4. List anything that looks fragile or would break if modified
   without care.

Do NOT suggest changes yet. I want to understand the current state
before deciding what to modify.
```

**Tips:**
- The explicit "do NOT suggest changes yet" is important. Without it, the AI will jump to solutions before you have an accurate mental model.
- This prompt is a prerequisite for Pattern 4 (Architecture Ownership). You cannot own architectural decisions if you do not understand the current architecture.
- Use this before any refactoring session. Understanding precedes improvement.

---

## Prompt 4: Dependency and API Context

**When to use:** When your task involves integrating with external APIs or libraries that the AI may have outdated knowledge about.

**Pattern:** Context First + Concrete Examples

```
I'm integrating with {API/LIBRARY NAME} version {VERSION}.

Here is the relevant documentation:
---
{Paste the specific API docs section, or key type signatures}
---

Here is an existing working example from our codebase:
---
{Paste a working integration example from your project}
---

The new requirement: {What you need to build}

Use the documentation and existing example as your reference.
Do NOT use patterns from older versions of this API. If you are
unsure about any API method, say so rather than guessing.
```

**Tips:**
- Pasting actual documentation beats telling the AI to "check the docs." The AI's training data may be months old, and APIs change.
- A working example from your own codebase is the strongest possible context. It shows both the API usage and your project's conventions simultaneously.
- The "say so rather than guessing" instruction reduces hallucinated API calls -- one of the most common AI coding failures (440,445 hallucinated dependencies found in 2.23M code references analyzed).

---

## Prompt 5: Multi-File Change Context

**When to use:** When a change spans multiple files and the AI needs to understand how they connect.

**Pattern:** Context First + Checkpoint Commits

```
I need to make a change that will touch multiple files. Before
starting, let me map out the change.

The goal: {What the change accomplishes}

Files that will need changes:
1. {path/to/file1} -- {what changes and why}
2. {path/to/file2} -- {what changes and why}
3. {path/to/file3} -- {what changes and why}

Dependencies between changes:
- {file1} must be updated before {file2} because {reason}
- {file3} can be updated independently

Tests that will verify correctness:
- {path/to/test1} -- {what it validates}
- {path/to/test2} -- {what it validates}

Let's work through these one file at a time. Start with {file1}.
After each file, I'll verify the change before moving to the next.
```

**Tips:**
- Mapping multi-file changes upfront prevents the AI from losing track of the big picture when focused on individual files.
- The "one file at a time" instruction enforces Pattern 7 (Checkpoint Commits). Commit after each file succeeds.
- Specifying the dependency order prevents breaking changes from being applied in the wrong sequence.

---

## Related Prompts

- [Test-Driven Prompts](test-driven-prompts.md) -- for defining behavior after loading context
- [Architecture Prompts](architecture-prompts.md) -- for making structural decisions with loaded context
- [Error Escalation Prompts](error-escalation-prompts.md) -- for when context loading reveals unexpected issues
