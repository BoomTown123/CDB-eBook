# Code Review Skill

> An example Claude Code skill for performing structured code reviews. Save this as `.claude/skills/code-review/SKILL.md` in your project.
>
> Reference: [Skills, Commands, Agents, SDK](../../../../book/part-2-building/05-building-with-ai/03-skills-commands-agents-sdk.md) | [Pattern 8: Review Ruthlessly](../../../../book/part-2-building/05-building-with-ai/04-the-8-patterns-for-effective-ai-coding.md)

---

## SKILL.md File

Save the following as `.claude/skills/code-review/SKILL.md`:

```yaml
---
name: code-review
description: >
  Performs a structured code review on staged changes or a specified file.
  Checks for correctness, security, performance, and adherence to project
  conventions defined in CLAUDE.md.
---
```

## Review Process

When the user invokes `/code-review` or asks for a code review, follow this process:

### Step 1: Gather Context

1. Read the project's CLAUDE.md for coding conventions and architecture decisions.
2. Identify the files to review:
   - If the user specified files, review those.
   - If no files specified, review all staged changes (`git diff --cached`).
   - If nothing is staged, review uncommitted changes (`git diff`).
3. For each changed file, read the full file (not just the diff) to understand context.

### Step 2: Review Each File

For each file, check:

**Correctness**
- Does the code do what it claims?
- Are there logic errors, off-by-one errors, or incorrect assumptions?
- Does it handle edge cases (nulls, empty inputs, boundary values)?
- Does error handling cover the failure modes?

**Security**
- Is user input validated before use?
- Are SQL queries parameterized (no string concatenation)?
- Are there hardcoded secrets or credentials?
- Are authentication/authorization checks present where needed?
- Is there potential for injection (SQL, XSS, command)?

**Performance**
- Are there N+1 query patterns?
- Are there unbounded loops or growing lists?
- Are external calls timed out?
- Are there caching opportunities being missed?

**Conventions**
- Does the code follow the patterns defined in CLAUDE.md?
- Are names descriptive and consistent with the codebase?
- Does the architecture follow the project's layer boundaries?
- Are there duplicated blocks that should be extracted?

### Step 3: Report Findings

Categorize each finding:

- **CRITICAL** -- Must fix before committing. Security vulnerabilities, bugs, broken tests.
- **WARNING** -- Should fix. Performance issues, missing error handling, convention violations.
- **SUGGESTION** -- Consider improving. Better patterns, clearer names, additional tests.
- **POSITIVE** -- Done well. Reinforce good patterns.

### Step 4: Present the Review

Present findings in this format:

```
## Code Review: {files reviewed}

**Summary:** {1-2 sentence overview}

### Critical ({count})
{Each finding with file, line, issue, and suggested fix}

### Warnings ({count})
{Each finding with file, line, issue, and suggested fix}

### Suggestions ({count})
{Brief list}

### What Looks Good
{1-2 positive observations}
```

Limit to 15 findings maximum. Prioritize by severity.

---

## Usage

After placing this skill in your project, invoke it with:

```
/code-review
```

Or with specific files:

```
/code-review src/app/api/orders.py src/app/services/order_service.py
```

Or with a focus area:

```
/code-review --focus security
```

---

## Customization

Add project-specific checks by editing the SKILL.md file:

```
Additional checks for this project:
- All API endpoints must have rate limiting decorators
- Database migrations must include downgrade() logic
- HTMX partials must not include the base layout
```

The skill automatically reads your CLAUDE.md for conventions, so project-specific rules defined there will be applied without duplicating them in the skill.
