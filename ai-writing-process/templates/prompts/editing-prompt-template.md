# Editing Prompt Template

Editing prompts refine existing drafts rather than generating new content. The real system used separate editing passes for different focus areas -- voice consistency, AI pattern removal, audience balance, density, and clarity. Each pass catches different problems.

Run editing prompts *after* the initial draft, not during. Writing and editing use different parts of the brain -- even for AI.

**How to Use:**
1. Complete a draft section first
2. Choose your editing focus (voice, de-AI, density, audience, or clarity)
3. Paste the draft and relevant reference files into the prompt
4. Review the change log before accepting
5. Run multiple focused passes rather than one "fix everything" pass

---

````markdown
# Edit for [FOCUS AREA]

> **Input:** Draft section + relevant reference files
> **Output:** Revised section with change log

## The Prompt

Review and edit the following section. Focus: **[CHOOSE ONE -- voice consistency / AI pattern removal / audience balance / density / clarity]**.

### Draft Section

[PASTE FULL SECTION CONTENT HERE, INCLUDING FRONTMATTER AND REFERENCES]

### Reference Material

[PASTE THE RELEVANT REFERENCE FILE FOR YOUR FOCUS AREA:
- Voice consistency -> Voice Guide
- AI pattern removal -> Authenticity Markers / Kill List
- Audience balance -> Audience Empathy Guide
- Density -> Gold Standard Reference / Density Test
- Clarity -> Quick Reference]

### Focus Areas

Define 2-4 specific things to look for in this pass.

**[FOCUS 1]:** [What to look for -- e.g., "Kill list violations: scan for 'important to note,' 'delve into,' decorative adjectives"]

**[FOCUS 2]:** [e.g., "AI symmetry patterns: check for equal-length lists, perfectly parallel structure, every point weighted the same"]

**[FOCUS 3]:** [e.g., "Density: identify sentences that could be cut without losing meaning. Flag paragraphs that make the same point twice."]

**[FOCUS 4]:** [e.g., "Audience check: would both readers finish this? Is there an insight for each?"]

### Rules

- **Show changes with brief explanations** -- don't just rewrite silently
- **Don't add new content** -- only refine, tighten, or restructure existing material
- **Preserve all citations and references** -- don't drop footnotes during editing
- **Maintain word count** within +/- 10% of original (editing tightens; it shouldn't expand)
- **Preserve frontmatter** exactly as written

### Kill List (Customize Per Pass)

Remove or replace these on sight:

| Pattern | Replace With |
|---------|-------------|
| [YOUR KILL LIST ITEM #1] | [Replacement] |
| [YOUR KILL LIST ITEM #2] | [Replacement] |
| [YOUR KILL LIST ITEM #3] | [Replacement] |
| Throat-clearing openings | Start with the point |
| Same point stated multiple ways | One statement, move on |
| [ADD MORE AS YOU DISCOVER THEM] | [Fixes] |

### Output Format

Return three things:

**1. Revised Section**
Full text with all changes applied. Include frontmatter and references.

**2. Change Log**

| Location | What Changed | Why |
|----------|-------------|-----|
| [paragraph/line] | [description of change] | [reason -- tied to focus area] |
| [paragraph/line] | [description] | [reason] |

**3. Remaining Issues**
Flag anything you noticed but didn't fix (outside the current focus area, or requiring author judgment).

### Quality Checklist

- [ ] No kill list violations remain
- [ ] Voice matches the reference guide
- [ ] No new content introduced
- [ ] All citations preserved
- [ ] Word count within +/- 10% of original
- [ ] Changes are improvements, not just differences
````

---

*Adapted from the editing prompts used for [Blueprint for An AI-First Company](../../README.md). The original system ran 5 distinct editing passes (structural, voice, de-AI, density, and audience) on every section, each with its own focused prompt and reference files.*
