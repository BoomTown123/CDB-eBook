# Review Prompt Template

Review prompts assess quality rather than making changes. They produce a structured assessment with grades, issues, and priority fixes. Use these after editing passes to decide whether a section is ready or needs another round.

The real system used a 10-dimension review framework with weighted scoring. You might start simpler -- 4-5 dimensions is enough for most books. Add dimensions as you discover what keeps going wrong.

**How to Use:**
1. Complete drafting and at least one editing pass before reviewing
2. Define your quality dimensions and weights
3. Submit the section with the review prompt
4. Use the output to decide: ship, edit again, or rewrite
5. Track review scores across chapters to spot systemic issues

---

````markdown
# Review: [REVIEW TYPE -- e.g., "Section Quality" / "Chapter Cohesion" / "Voice Consistency"]

> **Input:** Complete section or chapter + quality criteria
> **Output:** Structured assessment with grade, issues, and priority fixes

## The Prompt

Review the following [section/chapter] against the quality criteria below. Be honest -- the goal is to catch problems before readers do, not to validate the draft.

### Content to Review

[PASTE FULL SECTION OR CHAPTER CONTENT HERE]

### Reference Material

[PASTE RELEVANT REFERENCE FILES:
- Voice Guide (for voice consistency review)
- Audience Empathy Guide (for audience balance review)
- Gold Standard Reference (for density review)
- Previous chapter sections (for cohesion review)]

---

### Quality Dimensions

Define what "good" looks like for each dimension. Assign weights that reflect your priorities.

| Dimension | Weight | What "Good" Looks Like |
|-----------|--------|------------------------|
| [DIMENSION 1 -- e.g., "Voice Consistency"] | [X%] | [e.g., "Matches voice guide. No kill list violations. Signature phrases present."] |
| [DIMENSION 2 -- e.g., "Content Depth"] | [X%] | [e.g., "Claims backed by evidence. Named examples. No unsupported generalizations."] |
| [DIMENSION 3 -- e.g., "Audience Relevance"] | [X%] | [e.g., "Both readers would finish. Actionable for each. No audience-alienating content."] |
| [DIMENSION 4 -- e.g., "Density & Clarity"] | [X%] | [e.g., "Gold standard density. No cuttable sentences. Every paragraph has one job."] |
| [DIMENSION 5 -- e.g., "Structure"] | [X%] | [e.g., "Opening hooks. Sections build. Closing lands. Logical flow throughout."] |
| [DIMENSION 6 -- optional] | [X%] | [Criteria] |

Weights should total 100%.

---

### Review Checklist

**Structure:**
- [ ] Opening hooks the reader (not "In this section...")
- [ ] Sections build on each other logically
- [ ] Closing synthesizes and lands (not "In conclusion...")
- [ ] Subheadings tell the story on their own
- [ ] [YOUR STRUCTURAL CHECK]

**Content:**
- [ ] Claims supported by evidence or named examples
- [ ] Examples are concrete and named, not hypothetical
- [ ] Both audiences addressed
- [ ] At least one framework, analogy, or structural pattern
- [ ] [YOUR CONTENT CHECK]

**Voice:**
- [ ] Matches author voice guide
- [ ] No AI-generated patterns (equal-length lists, perfect symmetry)
- [ ] Kill list clean (no banned phrases)
- [ ] Signature phrases present
- [ ] [YOUR VOICE CHECK]

**Technical:**
- [ ] Frontmatter complete and accurate
- [ ] Citations formatted correctly (footnotes with references)
- [ ] Internal links resolve
- [ ] Word count within 10% of target
- [ ] [YOUR TECHNICAL CHECK]

---

### Output Format

**Overall Assessment:** [Pass / Needs Editing / Needs Rewrite]

**Grade:** [A / B / C / D]
- A = Ready to publish with minor polish
- B = Solid foundation, needs one focused editing pass
- C = Significant issues in 1-2 dimensions, needs targeted revision
- D = Fundamental problems, consider rewriting

**Dimension Scores:**

| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| [Dimension 1] | [X] | [Brief assessment] |
| [Dimension 2] | [X] | [Brief assessment] |
| [Dimension 3] | [X] | [Brief assessment] |
| [Dimension 4] | [X] | [Brief assessment] |

**Issues Found:**

| # | Location | Issue | Severity | Recommended Fix |
|---|----------|-------|----------|-----------------|
| 1 | [section/paragraph] | [specific description] | [High/Med/Low] | [actionable recommendation] |
| 2 | [location] | [description] | [severity] | [fix] |
| 3 | [location] | [description] | [severity] | [fix] |

**Strengths:**
- [What's working well -- 2-3 bullet points]
- [Specific examples of strong moments]

**Priority Fixes:**
The top 3 changes that would most improve this section:
1. [Most impactful fix]
2. [Second most impactful]
3. [Third most impactful]

**Quotable Lines:**
Lines from this section that are strong enough to highlight:
- "[Line]" -- [why it works]
- "[Line]" -- [why it works]
(If none found, flag this as an issue.)
````

---

*Adapted from the review prompts used for [Blueprint for An AI-First Company](../../README.md). The original system used a 10-dimension review framework across 4 editorial phases (structural editing, voice consistency, fact verification, and contradiction detection) with scores tracked across all 12 chapters.*
