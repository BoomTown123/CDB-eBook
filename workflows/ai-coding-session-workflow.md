# Workflow: AI-Assisted Coding Session

> A step-by-step workflow for a single AI-assisted coding session, incorporating all eight patterns that separate productive development from expensive flailing.

*Based on [Chapter 5: Building with AI](../book/part-2-building/05-building-with-ai/README.md)*

---

## When to Use This Workflow

Use this every time you write or modify code with AI assistance -- Claude Code, GitHub Copilot, Cursor, or any AI coding tool. A randomized controlled trial found developers were 19% slower with AI assistance, but believed they were 20% faster. This workflow closes that perception gap.

---

## The Workflow

### Phase 1: Before You Start

**Step 1: Set context (Pattern 1: Context First).** Before your first prompt, tell the AI: your tech stack, the problem, constraints, and what you have tried. 150-250 tokens of context hits the sweet spot. If your project has a CLAUDE.md or rules file, confirm it is current.

**Step 2: Checkpoint (Pattern 7: Checkpoint Commits).** Commit your working code before any AI interaction: `git add -A && git commit -m "checkpoint: before AI session"`. You will checkpoint again after each successful change.

**Step 3: Plan the architecture (Pattern 4: Architecture Ownership).** Decide component boundaries, data models, API contracts, and error handling before asking AI to implement. You own structure -- 80-90% of AI-generated code suffers from "avoidance of refactors" when the AI decides structure independently.

### Phase 2: The Coding Loop

**Step 4: Small requests (Pattern 3: Iterative Refinement).** One function per request. One concern per request. For a complete feature: 5-10 iterations. The discipline feels slower. It is faster.

**Step 5: Show examples (Pattern 2: Concrete Examples).** Paste an existing component that follows your conventions. "Function names use camelCase, constants use SCREAMING_SNAKE_CASE" beats "use consistent naming."

**Step 6: Describe behavior (Pattern 5: Test-Driven Prompting).** Say "it should find items instantly even with 10,000 entries" instead of "use a hash map with O(1) lookup." Let the AI choose the how.

**Step 7: Review and checkpoint (Patterns 7+8: Checkpoint + Review Ruthlessly).** Review like you are reviewing a junior developer. Check correctness, security, edge cases. Run tests. Only 55% of AI-generated code is secure. If it passes, commit immediately.

> **Decision point:** Change working? Yes -- commit, return to Step 4. No -- continue to Step 8.

### Phase 3: When Things Break

**Step 8: Escalate errors (Pattern 6: Error Escalation).** Share the error message with the AI. Let it propose a fix -- AI excels at debugging its own mistakes. If the first fix fails, provide more context. After 2-3 failed attempts at the same problem, take over manually. The AI is stuck.

> **Decision point:** Fixed within 2-3 attempts? Yes -- review, checkpoint, return to Step 4. No -- fix manually, checkpoint, return to Step 4.

### Phase 4: Close the Session

**Step 9: Final review.** Run the full test suite. Review the cumulative diff since your pre-session checkpoint. Check for hardcoded secrets and insecure defaults. Commit with a descriptive message.

---

## Tips

- **Keep rules files actionable.** "Write clean code" isn't a rule. "All public functions have JSDoc comments with param types" is.
- **Do not use an LLM for what a linter can do.** Formatting and import ordering are tool problems.
- **Checkpoint commits prevent the biggest time waste** -- redoing AI work after a bad change.
- **Start fresh after 30-50 messages.** Context degrades in long sessions. Summarize progress and continue in a new conversation.

## Related Resources

- [8 Patterns for AI Coding](../frameworks/8-patterns-for-ai-coding.md) -- The complete framework with research and rationale
- [Human-AI Collaboration Framework](../frameworks/human-ai-collaboration.md) -- The broader collaboration model
- [7 Failure Modes of Agents](../frameworks/7-failure-modes-of-agents.md) -- What goes wrong without guardrails
