# Section Writing Prompt Template

This is the prompt you use to generate actual manuscript content. It takes a section topic, research context, and word target as inputs and produces a complete section with citations, frontmatter, and references.

The key insight: the more context you feed the prompt (research stats, quotes, company examples), the more specific and grounded the output. Vague inputs produce vague prose.

**How to Use:**
1. Gather research for the section (stats, quotes, examples)
2. Fill in the prompt template with section details and research context
3. Submit with your master system prompt prepended
4. Review output against your voice guide and density test
5. Run through an editing pass before accepting

---

````markdown
# Write Section

> **Input:** Section topic, research context, target word count
> **Output:** Complete section with frontmatter, citations, and references

## The Prompt

Write section [X.X] of Chapter [X]: "[SECTION TITLE]"

### Context

This section covers [BRIEF DESCRIPTION OF WHAT THE SECTION ARGUES OR TEACHES].

**Key research to incorporate:**

[PASTE RESEARCH HERE -- statistics, quotes, company examples, data points.
The more specific the research, the more grounded the output.
Include source names and URLs for citation generation.]

**Example research format:**
- STAT: [Company] achieved [metric] in [timeframe] (Source: [Name], [URL])
- QUOTE: "[Direct quote]" -- [Person, Title] (Source: [Name], [URL])
- EXAMPLE: [Company] did [specific thing] which resulted in [outcome]

### Chapter Context

- **Chapter theme:** [One sentence on what this chapter covers]
- **Previous section:** [What came before -- so this section can build on it]
- **Next section:** [What comes after -- so this section can set it up]
- **Chapter argument:** [The overarching thesis this section supports]

### Requirements

- **Word target:** [1,000-1,200] words of prose content (not counting frontmatter or references)
- **Voice:** Follow the master system prompt strictly
- **Citations:** Markdown footnotes for all statistics, quotes, and specific claims
- **Structure:**
  - Opening that hooks -- not "In this section we will explore..."
  - 3-5 subheaded subsections that build on each other
  - At least 1 concrete, named company example
  - At least 1 framework, analogy, or structural pattern from the voice guide
  - Closing that synthesizes and lands -- not "In conclusion..."

### Frontmatter

```yaml
---
type: section
book: [YOUR-BOOK-SLUG]
part: [X]
chapter: [X]
section: [X]
title: "[SECTION TITLE]"
status: drafting
target_words: [TARGET]
research_sources:
  - "[[PATH TO RESEARCH FILE]]"
tags:
  - section
  - [TOPIC TAG]
---
```

### Citation Format

Inline:
```markdown
[COMPANY] reached [METRIC] in [TIMEFRAME][^source-tag].
```

References section at end:
```markdown
## References

[^source-tag]: Source Name -- [link text](https://example.com/source-url)
```

Rules:
- One footnote tag per source URL (reuse the same tag for the same source)
- Tag format: `[^short-descriptive-name]`
- Reference format: `Source Name -- [link text](URL)`

### Internal Research Tracking

At the very end, add:
```markdown
<!-- INTERNAL: Research Sources
- [[path/to/research/file|Description]]
-->
```

### Quality Checklist

Before submitting the section:

- [ ] Opens with a hook, not throat-clearing
- [ ] Every statistic has a footnote citation
- [ ] Every direct quote has a footnote citation
- [ ] References section at end with full URLs
- [ ] Within 10% of word target
- [ ] Voice matches master system prompt
- [ ] No kill list violations
- [ ] Both audiences would finish reading this
- [ ] At least one line is quotable
- [ ] Could NOT cut 20% more
````

---

*Adapted from the section writing prompts used for [Blueprint for An AI-First Company](../../README.md). The original system used 7 specialized writing prompts (chapter openings, body sections, frameworks, case studies, chapter closings, part intros, and transitions) that all followed this core structure.*
