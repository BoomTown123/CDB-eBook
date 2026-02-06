# Chapter Writer Skill Template

A fill-in-the-blank starting point for building a chapter writing skill that orchestrates research, writing, review, and polish into a single workflow.

---

```markdown
---
name: chapter-writer
description: "Complete workflow to write a chapter from research to final draft."
---

# Chapter Writer

Write a complete chapter of [YOUR BOOK TITLE].

## Input
- **Chapter number** (1-[TOTAL CHAPTERS])
- **Mode:** step-by-step (default) or auto

## Steps

| Step | Name | Agent | Optional |
|------|------|-------|----------|
| 1 | Generate Research Prompts | research-prompt-agent | No |
| 2 | Run Research | [YOUR RESEARCH TOOL] | No |
| 3 | Write Sections | writer-agent | No |
| 4 | Review Sections | reviewer-agent | No |
| 5 | Create Diagrams | writer-agent | Yes |
| 6 | Write Intro + Summary | writer-agent | No |

## Section Batching

| Sections in Chapter | Strategy |
|---------------------|----------|
| 1-4 | Single agent writes all |
| 5-8 | 2 parallel agents (max 4 sections each) |
| 9+ | 3 parallel agents (max 4 sections each) |

## Handoff Protocol

When splitting work across agents, pass this context block:

```
## Handoff Summary

### Sections Written
- [List completed sections with brief content notes]

### Key Themes Established
- [What narrative threads were set up]

### Narrative Thread for Next Agent
- [What the next sections should build on]
- [Transitions to maintain]

### Style Notes
- [Any voice/formatting patterns to continue]
```

## Step 3: Write Sections

For each section:
1. Load research for this section
2. Write ~[TARGET WORDS] words
3. Add footnote citations for statistics and quotes
4. Update frontmatter status to `drafting`
5. Add References section at end

### Section Requirements
- [YOUR WORD TARGET] words per section
- Footnote citations for all statistics and direct quotes
- Voice matches your master system prompt
- Opens with a hook, not throat-clearing
- Closes with a landing, not trailing off
- [YOUR ADDITIONAL REQUIREMENTS]

## Step 4: Review Sections

For each section, check:
1. Research utilization -- what was available but unused?
2. Voice consistency against your voice guide
3. Citation completeness for claims
4. Narrative flow between sections
5. Verdict: **Pass** / **Needs Work** / **Major Revision**

## Modes

**Step-by-step:** Pause after each step for your approval.
**Auto:** Run all steps continuously, pause only at optional steps.
```

---

## Customization Checklist

- [ ] Replace `[YOUR BOOK TITLE]` with your book title
- [ ] Set `[TOTAL CHAPTERS]` to your chapter count
- [ ] Set `[TARGET WORDS]` per section
- [ ] Define `[YOUR RESEARCH TOOL]` (Perplexity, web search, etc.)
- [ ] Set directory paths for research prompts and output
- [ ] Add any book-specific section requirements
- [ ] Adjust batching thresholds for your chapter sizes
