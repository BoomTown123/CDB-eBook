# Test-Driven Prompts

> Prompts for test-driven development with AI. These implement **Pattern 5: Test-Driven Prompting** from the [8 Patterns for Effective AI Coding](../../../book/part-2-building/05-building-with-ai/04-the-8-patterns-for-effective-ai-coding.md).

The core principle: describe expected behavior, not implementation details. Let the AI choose the "how" while you define the "what." Behavior descriptions are more robust than implementation prescriptions. The AI may find better approaches than you would specify.

---

## Prompt 1: Behavior-First Test Generation

**When to use:** You know what the code should do but haven't written the implementation yet. Start with tests.

**Pattern:** Test-Driven Prompting + Concrete Examples

```
Write tests for a {COMPONENT_TYPE} that does the following:

Behaviors to test:
1. Given {INPUT/STATE}, it should {EXPECTED OUTCOME}
2. Given {INPUT/STATE}, it should {EXPECTED OUTCOME}
3. Given {EDGE CASE}, it should {EXPECTED OUTCOME}
4. Given {ERROR CONDITION}, it should {EXPECTED OUTCOME}

Testing framework: {e.g., pytest, Jest, Go testing}

Existing test patterns in this project:
---
{Paste an example test from your project that shows conventions}
---

Requirements:
- Each test should be independent and not rely on other tests
- Use descriptive test names that explain the behavior being verified
- Include setup/teardown where necessary
- Do NOT write the implementation -- only the tests

After writing the tests, list which behaviors are covered and which
edge cases might be missing.
```

**Tips:**
- Framing as "Given X, it should Y" forces you to think in behaviors rather than implementation. This is the most important habit in AI-assisted TDD.
- Pasting an existing test file shows the AI your project's test conventions, naming patterns, and assertion style. This applies Pattern 2 (Concrete Examples).
- Asking the AI to identify missing edge cases after writing tests often surfaces cases you had not considered. The AI is good at enumeration.

---

## Prompt 2: Test-First Implementation

**When to use:** Tests are already written and failing. You need the AI to write code that makes them pass.

**Pattern:** Test-Driven Prompting + Iterative Refinement

```
Here are the failing tests:
---
{Paste the test file}
---

Here is the current test output:
---
{Paste the test runner output showing failures}
---

Write the minimum implementation that makes all tests pass.

Constraints:
- {e.g., Must use the existing database connection from db.py}
- {e.g., Must follow the repository pattern used elsewhere}
- {e.g., No new dependencies}

Do NOT modify the tests. Do NOT add functionality beyond what the
tests require. If a test seems incorrect, tell me rather than
working around it.
```

**Tips:**
- "Minimum implementation" is deliberate. Without this constraint, the AI tends to over-engineer -- adding features, abstractions, and handlers that no test requires. This is one of the most common failure modes (80-90% of AI code suffers from avoidance of refactors).
- "Do NOT modify the tests" is critical. The AI will sometimes silently change test assertions to match its implementation rather than the other way around.
- Pasting the actual test output gives the AI concrete failure messages to work from, which produces more targeted fixes than just showing the test code.

---

## Prompt 3: Edge Case Expansion

**When to use:** You have working code with basic tests, and need to harden it against edge cases and failure modes.

**Pattern:** Test-Driven Prompting + Review Ruthlessly

```
Here is the current implementation:
---
{Paste the implementation}
---

Here are the existing tests:
---
{Paste the test file}
---

All current tests pass. Now I need to harden this code.

Generate additional tests for:
1. Boundary conditions (empty inputs, maximum sizes, zero values)
2. Error cases (network failures, invalid data, timeouts)
3. Concurrency issues (if applicable)
4. Security concerns (injection, overflow, unauthorized access)

For each test, explain:
- What specific failure mode it guards against
- Whether the current implementation would pass or fail
- If it would fail, what change is needed

Prioritize tests by risk: which missing test would cause the
worst production incident if the edge case occurred?
```

**Tips:**
- Security edge cases are especially important with AI-generated code. Only 55% of AI-generated code is secure, with XSS vulnerabilities appearing 86% of the time.
- Asking the AI to predict pass/fail before running tests verifies that both you and the AI understand the implementation. Mismatches reveal misunderstandings.
- Risk prioritization surfaces the most valuable tests first. Not all edge cases are equally dangerous.

---

## Prompt 4: Regression Test from Bug Report

**When to use:** A bug has been reported. Before fixing it, write a test that reproduces it.

**Pattern:** Test-Driven Prompting + Error Escalation

```
Bug report:
- Expected behavior: {What should happen}
- Actual behavior: {What actually happens}
- Steps to reproduce: {How to trigger the bug}
- Environment: {Relevant context -- browser, OS, data state}

Relevant code:
---
{Paste the function/module where the bug likely lives}
---

Write a test that:
1. Reproduces the exact bug (this test should FAIL currently)
2. Clearly documents what the correct behavior should be
3. Is specific enough that fixing an unrelated issue won't
   accidentally make it pass

Do NOT fix the bug yet. I want a failing test first, then we
will fix it in the next step.
```

**Tips:**
- Writing the regression test before the fix ensures the fix is real, not coincidental. This is standard TDD practice, and even more important with AI-generated fixes.
- "Specific enough that fixing an unrelated issue won't make it pass" prevents false confidence. A test that passes for the wrong reason is worse than no test.
- After the test is written and failing, use the Test-First Implementation prompt (Prompt 2) to have the AI write the fix.

---

## Prompt 5: Contract Tests for API Boundaries

**When to use:** Defining the contract between two systems, modules, or services before building either side.

**Pattern:** Test-Driven Prompting + Architecture Ownership

```
I'm defining the contract between {SYSTEM_A} and {SYSTEM_B}.

The interface:
- Endpoint/Function: {e.g., POST /api/v2/orders}
- Input shape: {JSON schema or type definition}
- Output shape: {JSON schema or type definition}
- Error responses: {Expected error codes and shapes}

Write contract tests that verify:
1. Valid requests produce correctly shaped responses
2. Each documented error case returns the right error code and message
3. Required fields are enforced (missing fields cause clear errors)
4. The contract is stable (response shape doesn't change unexpectedly)

These tests should be runnable against either a mock or the real
service. Use {TESTING_FRAMEWORK} and structure them so both teams
can run them independently.
```

**Tips:**
- Contract tests enforce architecture decisions at the boundary. This is where Pattern 4 (Architecture Ownership) and Pattern 5 (Test-Driven Prompting) work together.
- Both teams running the same contract tests prevents integration drift. The tests become the single source of truth for the interface.
- Include error responses in the contract. Most integration failures happen in error handling, not in the happy path.

---

## Related Prompts

- [Context Loading](context-loading.md) -- load project context before writing tests
- [Architecture Prompts](architecture-prompts.md) -- define the structure that tests will verify
- [Review Prompts](review-prompts.md) -- review both the tests and the implementation
