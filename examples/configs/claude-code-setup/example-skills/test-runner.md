# Test Runner Skill

> An example Claude Code skill for running tests and analyzing results. Save this as `.claude/skills/test-runner/SKILL.md` in your project.
>
> Reference: [Skills, Commands, Agents, SDK](../../../../book/part-2-building/05-building-with-ai/03-skills-commands-agents-sdk.md) | [Pattern 5: Test-Driven Prompting](../../../../book/part-2-building/05-building-with-ai/04-the-8-patterns-for-effective-ai-coding.md)

---

## SKILL.md File

Save the following as `.claude/skills/test-runner/SKILL.md`:

```yaml
---
name: test-runner
description: >
  Runs the project test suite, analyzes failures, and suggests fixes.
  Supports targeted test runs for specific files or directories.
  Implements Pattern 5 (Test-Driven Prompting) by ensuring tests
  pass before moving on.
---
```

## Test Process

When the user invokes `/test` or asks to run tests, follow this process:

### Step 1: Determine Test Scope

1. Read the project's CLAUDE.md for test commands and conventions.
2. Determine what to test:
   - `/test` with no arguments: Run the full test suite.
   - `/test unit`: Run unit tests only.
   - `/test integration`: Run integration tests only.
   - `/test path/to/file.py`: Run tests for a specific file.
   - `/test --changed`: Run tests only for files changed since the last commit.

### Step 2: Run Tests

Execute the appropriate test command from CLAUDE.md:

```bash
# Full suite
pytest --cov=src/app -v

# Unit only
pytest tests/unit -v

# Integration only
pytest tests/integration -v

# Specific file
pytest tests/unit/test_order_service.py -v

# Changed files only
pytest --co -q | grep "$(git diff --name-only | sed 's/src/tests/' | sed 's/.py//')" | xargs pytest -v
```

Capture the full output including:
- Number of tests run
- Number passed, failed, errored, skipped
- Coverage percentage (if available)
- Execution time

### Step 3: Analyze Results

If all tests pass:
```
All {count} tests passed in {time}s.
Coverage: {percentage}%

Uncovered areas:
- {list files/functions with low coverage, if coverage data available}
```

If tests fail, for each failure:

1. **Identify the failure**: File, test name, error message.
2. **Read the test**: Understand what it expects.
3. **Read the implementation**: Understand what the code does.
4. **Diagnose the root cause**: Is this a test issue or an implementation issue?
5. **Suggest a fix**: Provide the specific code change with an explanation.

### Step 4: Present Results

```
## Test Results

**Status:** {PASS / FAIL}
**Tests:** {passed} passed, {failed} failed, {skipped} skipped
**Time:** {seconds}s
**Coverage:** {percentage}%

### Failures ({count})

#### {test_name}
- **File:** {test file path}
- **Error:** {error message, 1-2 lines}
- **Root cause:** {explanation}
- **Suggested fix:**
  ```python
  {code fix}
  ```

### Coverage Gaps
{List of files or functions below the coverage threshold}

### Recommendation
{What to do next: fix failures, add tests, or proceed}
```

### Step 5: Fix and Re-run (If Requested)

If the user asks to fix failures:
1. Apply the suggested fix.
2. Re-run only the previously failing tests.
3. If they pass, run the full suite to check for regressions.
4. Report the final status.

Do NOT fix tests by changing assertions to match incorrect behavior. If the implementation is wrong, fix the implementation. If the test is wrong, confirm with the user before changing the test.

---

## Usage

After placing this skill in your project:

```
/test                    # Run full suite
/test unit               # Unit tests only
/test integration        # Integration tests
/test --changed          # Tests for changed files
/test --fix              # Run tests and fix failures
```

---

## Customization

Adapt the test commands and conventions for your project's test framework:

**For Jest (JavaScript/TypeScript):**
```bash
npx jest --verbose                    # Full suite
npx jest --testPathPattern=unit       # Unit tests
npx jest --coverage                   # With coverage
npx jest --changedSince=HEAD~1        # Changed files
```

**For Go:**
```bash
go test ./... -v                      # Full suite
go test ./internal/... -v             # Specific package
go test -cover ./...                  # With coverage
go test -run TestOrderService ./...   # Specific tests
```

**For Rust:**
```bash
cargo test -- --nocapture             # Full suite
cargo test --lib                      # Unit tests only
cargo test integration_               # Integration tests
```

Update the SKILL.md file with your project's specific commands so the skill runs the correct test framework automatically.
