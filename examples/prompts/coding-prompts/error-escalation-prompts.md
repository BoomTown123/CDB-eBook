# Error Escalation Prompts

> Prompts for handling errors and debugging with AI assistance. These implement **Pattern 6: Error Escalation** from the [8 Patterns for Effective AI Coding](../../../book/part-2-building/05-building-with-ai/04-the-8-patterns-for-effective-ai-coding.md).

The escalation ladder: share the error message, let AI propose a fix, provide more context if still broken. After two or three failed attempts at the same problem, take over manually. The AI is stuck in a loop and will not escape it.

---

## Prompt 1: First-Pass Error Fix

**When to use:** You hit an error and want the AI to take the first crack at fixing it. This is the bottom rung of the escalation ladder.

**Pattern:** Error Escalation + Context First

```
I'm getting this error:

```
{Paste the full error message, including stack trace}
```

The code that triggered it:
---
{Paste the relevant code section}
---

What I was trying to do: {Brief description}
What I expected to happen: {Expected behavior}
What actually happened: {Actual behavior}

Diagnose the root cause and propose a fix. Show me the fix before
applying it -- I want to understand what went wrong before changing
anything.
```

**Tips:**
- Always paste the full error message and stack trace. Truncated errors lead to guessed solutions.
- "Show me the fix before applying it" prevents the AI from making changes you do not understand. Understanding the fix is more important than getting it quickly.
- Most AI coding errors are fixable in one round if you provide the complete error output. The AI is genuinely good at debugging its own mistakes.

---

## Prompt 2: Second-Attempt with More Context

**When to use:** The AI's first fix did not work. Time to provide additional context before trying again.

**Pattern:** Error Escalation + Iterative Refinement

```
Your previous fix did not resolve the issue.

What you suggested:
---
{Paste the fix that was applied}
---

The new error after applying your fix:
```
{Paste the new error message}
```

Additional context that might be relevant:
- {e.g., This function is called from a background task, not an HTTP request}
- {e.g., The database connection uses a connection pool, not direct connections}
- {e.g., This runs inside a Docker container with limited filesystem access}

Related files that might be involved:
- {path/to/related-file}: {what it does and why it might matter}

Try a different approach. If the same type of fix is not working,
consider whether the root cause is elsewhere in the system.
```

**Tips:**
- "Try a different approach" is the key instruction. Without it, the AI often tweaks the same broken approach. You need to explicitly tell it to change direction.
- The additional context section is where you provide information you initially thought was irrelevant. Runtime environment, connection pooling, container constraints -- these often turn out to be the actual root cause.
- If the second attempt also fails, you are approaching the three-strike threshold. Prepare to take over.

---

## Prompt 3: Three-Strike Diagnostic

**When to use:** Two fixes have failed. Before taking over manually, get the AI to do a structured diagnostic. This is the top of the escalation ladder.

**Pattern:** Error Escalation + Architecture Ownership

```
Two attempted fixes have failed for this issue. Before I take over
manually, I need a structured diagnostic.

Original error:
---
{Original error}
---

Fix attempt 1: {What was tried}
Result: {What happened}

Fix attempt 2: {What was tried}
Result: {What happened}

Produce a diagnostic report:

1. **Root cause hypotheses**: List 3-5 possible root causes, ranked
   by likelihood. For each, explain what evidence supports or
   contradicts it.

2. **What we know**: List every confirmed fact from the error messages,
   logs, and behavior observed.

3. **What we don't know**: List the information gaps that are preventing
   a fix. For each gap, suggest how to get that information (specific
   commands, log queries, debugger breakpoints).

4. **Recommended next step**: Based on the hypotheses and gaps, what
   single investigation step would most quickly identify the root cause?

Do NOT suggest another fix. I want a diagnostic, not a guess.
```

**Tips:**
- "Do NOT suggest another fix" is critical at this stage. Three guesses in a row is a cycle. Break the cycle by switching from fix mode to diagnostic mode.
- The "What we don't know" section is the most valuable part. It tells you exactly what to investigate when you take over. This converts the AI from a fix-generator to a diagnostic tool.
- After getting the diagnostic, take over manually. Run the suggested investigation steps. If the diagnostic surfaces the root cause, you can return to the AI with new context for a targeted fix.

---

## Prompt 4: Environment and Configuration Debugging

**When to use:** The error is not in the code itself but in the environment, configuration, or deployment.

**Pattern:** Error Escalation + Context First

```
The code works in {environment where it works, e.g., local development}
but fails in {environment where it fails, e.g., staging/production}.

Error in the failing environment:
```
{Paste error}
```

Environment differences I know about:
- {e.g., Local: SQLite, Production: PostgreSQL}
- {e.g., Local: Python 3.11, Production: Python 3.9}
- {e.g., Local: runs directly, Production: runs in Docker}

Configuration files:
---
{Paste relevant config for both environments}
---

Help me identify which environment difference is causing the failure.

Check for:
1. Version mismatches (language, library, database)
2. Missing environment variables or secrets
3. File path differences (absolute vs relative, OS-specific)
4. Network configuration (ports, hostnames, DNS)
5. Permission differences (file access, database roles)

For each potential cause, suggest a specific command I can run in the
failing environment to confirm or rule it out.
```

**Tips:**
- Environment bugs are among the hardest to debug because the AI cannot see your environment. Providing explicit environment differences makes up for this limitation.
- "Specific command to confirm or rule it out" gives you an action plan. Run the commands, paste the results back, and the AI can narrow down the cause.
- Configuration files often contain the answer. Paste both working and failing configs so the AI can diff them.

---

## Prompt 5: Log-Based Debugging

**When to use:** The error is intermittent or the stack trace is unhelpful. You need to work from logs.

**Pattern:** Error Escalation + Review Ruthlessly

```
I have an intermittent issue: {brief description}.

It happens approximately {frequency, e.g., 5% of requests} under
{conditions, e.g., high load, specific data patterns}.

Here are the relevant logs from a successful request:
---
{Paste logs from a working case}
---

Here are the relevant logs from a failing request:
---
{Paste logs from a failing case}
---

Compare the two log sequences and:

1. Identify where the failing request diverges from the successful one
2. List what data or state differs at the divergence point
3. Suggest what additional logging would help isolate the root cause
   (include the exact log statements and where to place them)
4. Hypothesize what conditions trigger the failure based on the patterns

If the current logs are insufficient for diagnosis, tell me exactly
what additional information to capture and I'll provide it.
```

**Tips:**
- Side-by-side log comparison (working vs failing) is one of the AI's strongest debugging capabilities. It excels at pattern matching across structured text.
- "What additional logging would help" is the practical next step when logs are insufficient. The AI can suggest targeted instrumentation that you would add and then rerun.
- For intermittent issues, frequency and conditions are essential context. "5% of requests under high load" suggests a very different root cause than "every third request regardless of load."

---

## The Escalation Ladder Summary

| Step | Action | When |
|------|--------|------|
| 1 | Share error, let AI fix | First failure |
| 2 | Add context, request different approach | Same error persists |
| 3 | Request diagnostic, take over manually | Two fixes failed |
| -- | **Human takes the wheel** | **Three strikes reached** |

Know when to let AI iterate and when to step in. The cost of the fourth attempt exceeds the cost of debugging it yourself.

---

## Related Prompts

- [Context Loading](context-loading.md) -- more context often prevents errors in the first place
- [Test-Driven Prompts](test-driven-prompts.md) -- write regression tests after fixing bugs
- [Review Prompts](review-prompts.md) -- review fixes to prevent introducing new issues
