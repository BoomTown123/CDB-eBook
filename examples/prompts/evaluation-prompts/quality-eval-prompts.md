# Quality Evaluation Prompts

> Prompts for evaluating the quality of AI-generated outputs across multiple dimensions. Use these for ongoing quality monitoring, evaluating new prompts, or auditing agent performance.
>
> Reference: [8 Patterns for AI Coding](../../../frameworks/09-eight-patterns-for-ai-coding.md) | [7 Failure Modes of Agents](../../../frameworks/10-seven-failure-modes-of-agents.md)

---

## Prompt 1: Multi-Dimensional Quality Rubric

**When to use:** Evaluating a single output across all quality dimensions. Use as a general-purpose quality check for any AI output.

```
Evaluate the following AI-generated output using this quality rubric.

Task that produced this output:
---
{Paste the original prompt or task description}
---

Output to evaluate:
---
{Paste the AI-generated output}
---

Score each dimension 1-5 and provide specific evidence for each score:

ACCURACY (1-5):
- Are all factual claims correct?
- Are there any hallucinations or fabricated information?
- Are citations/references real and verifiable?
- Evidence: {cite specific correct or incorrect claims}

RELEVANCE (1-5):
- Does the output address the actual question asked?
- Is there irrelevant information that should be removed?
- Are there relevant aspects the output missed?
- Evidence: {cite specific relevant or irrelevant sections}

COMPLETENESS (1-5):
- Are all parts of the task addressed?
- Are there gaps that would require follow-up?
- Is the depth appropriate for the task?
- Evidence: {cite what was covered and what was missed}

CLARITY (1-5):
- Is the output well-organized and easy to follow?
- Is the language precise and unambiguous?
- Would the intended audience understand it without additional context?
- Evidence: {cite specific clear or unclear passages}

ACTIONABILITY (1-5):
- Can the reader act on this output directly?
- Are next steps clear?
- If code: does it run? If instructions: can they be followed?
- Evidence: {cite what is actionable and what requires more work}

Overall quality score: {weighted average based on task type}
Pass/Fail: {based on minimum acceptable scores per dimension}
Improvement priorities: {ranked list of what to fix first}
```

**Tips:**
- Weight the dimensions differently depending on the task type. Code generation should weight accuracy and actionability higher. Customer communication should weight clarity and relevance higher.
- "Specific evidence" is the key requirement. A score without evidence is opinion. A score with evidence is evaluation.
- Set minimum acceptable thresholds per dimension. For example: accuracy must be 4+, everything else 3+. Define what "pass" means before evaluating.

---

## Prompt 2: Code Quality Evaluation

**When to use:** Evaluating AI-generated code specifically, covering dimensions that matter for production software.

```
Evaluate the following AI-generated code for production readiness.

Task description:
---
{What the code was supposed to do}
---

Generated code:
---
{Paste the code}
---

Evaluate on these code-specific dimensions:

CORRECTNESS (pass/fail for each):
- [ ] Compiles/runs without errors
- [ ] Produces correct output for standard inputs
- [ ] Handles edge cases (nulls, empty inputs, boundaries)
- [ ] Error handling covers failure modes
- Failed checks: {list specific failures}

SECURITY (1-5):
- Input validation present and correct?
- SQL parameterized (no string concatenation)?
- No hardcoded secrets or credentials?
- Auth checks on protected operations?
- XSS/injection vectors?
- Findings: {list specific security issues}

PERFORMANCE (1-5):
- Time complexity appropriate for expected scale?
- No N+1 queries or unnecessary loops?
- Memory usage bounded?
- External calls properly timed out?
- Findings: {list specific performance issues}

MAINTAINABILITY (1-5):
- Names descriptive and consistent?
- Functions focused on single responsibility?
- Logic readable without excessive comments?
- Follows project conventions?
- Findings: {list specific maintainability issues}

TEST COVERAGE (1-5):
- Are tests included or easily writable?
- Do tests cover happy path and error paths?
- Are tests independent and repeatable?
- Findings: {list untested paths}

Production readiness: {READY / NEEDS_WORK / NOT_READY}
Estimated effort to production-ready: {hours}
Top 3 issues to fix first: {ranked list}
```

**Tips:**
- Run the code before evaluating. A review that says "looks correct" without execution is incomplete. Pattern 8 (Review Ruthlessly) means testing, not just reading.
- The pass/fail format for correctness is intentional. Correctness is binary per check -- code either handles nulls or it does not.
- "Estimated effort to production-ready" translates quality into business terms. A score of 3/5 is abstract. "4 hours of rework needed" is actionable.

---

## Prompt 3: Agent Output Quality Monitoring

**When to use:** Ongoing quality monitoring of an agent in production. Run periodically on a sample of agent outputs.

```
You are monitoring the quality of {AGENT_NAME}, a {agent type}
agent that {what it does}.

Here is a sample of {N} recent outputs from the agent.

Output 1:
- Task: {what was requested}
- Output: {what the agent produced}
- Outcome: {did the user accept it / was it escalated / was there a complaint}

Output 2:
{...}

Output 3:
{...}

Evaluate the batch:

1. SUCCESS RATE: What percentage of outputs successfully resolved
   the task without human intervention?

2. FAILURE ANALYSIS: For outputs that failed or were escalated:
   - Categorize the failure type (wrong answer, refusal to answer,
     hallucination, tone issue, scope creep, other)
   - Identify patterns -- are failures concentrated in a specific
     task type or input pattern?

3. QUALITY TRENDS: Compared to {previous evaluation period}:
   - Is quality improving, stable, or declining?
   - Are new failure patterns emerging?
   - Are previously common failures decreasing?

4. ESCALATION APPROPRIATENESS: For outputs that escalated to humans:
   - Were the escalations appropriate (agent correctly identified
     its limits)?
   - Were there outputs that should have escalated but didn't?
   - Were there unnecessary escalations the agent could have handled?

5. RECOMMENDATIONS:
   - Top 3 system prompt changes to improve quality
   - Specific examples to add to the prompt as few-shot guidance
   - Any new constraints or escalation rules needed

Include specific output IDs/examples for every finding.
```

**Tips:**
- Sample size matters. Evaluate at least 50 outputs per monitoring period. Smaller samples miss failure patterns.
- Track escalation appropriateness as its own metric. An agent that escalates too much is expensive. An agent that escalates too little is risky. The balance is the measure of a well-tuned system prompt.
- This evaluation feeds directly back into system prompt iteration. The recommendations section should produce concrete prompt changes you can test in the next period.

---

## Setting Quality Thresholds

Define minimum acceptable quality for your use case:

| Use Case | Accuracy | Relevance | Completeness | Clarity | Actionability |
|----------|----------|-----------|-------------|---------|--------------|
| Customer support | 5 | 5 | 4 | 5 | 4 |
| Code generation | 5 | 4 | 4 | 3 | 5 |
| Research briefs | 4 | 5 | 4 | 4 | 3 |
| Data analysis | 5 | 4 | 5 | 4 | 4 |
| Content drafting | 3 | 4 | 3 | 5 | 3 |

These are starting points. Adjust based on the cost of errors in your specific context. Customer support accuracy must be 5 because wrong answers destroy trust. Content drafting accuracy can be 3 because a human editor will refine it.

---

## Related Prompts

- [Model Comparison Prompts](model-comparison-prompts.md) -- compare model quality side-by-side
- [Safety Evaluation Prompts](safety-eval-prompts.md) -- evaluate safety alongside quality
- [Review Prompts](../coding-prompts/review-prompts.md) -- code-specific review checklists
