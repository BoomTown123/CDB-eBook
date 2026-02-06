# Section Template

Use this as the starting point for every section file (e.g., `01-Section-Name.md`). Copy it, fill in the placeholders, and write.

---

```markdown
---
type: section
book: [YOUR-BOOK-SLUG]
part: [PART NUMBER]
chapter: [CHAPTER NUMBER]
section: [SECTION NUMBER]
title: "[SECTION TITLE]"
status: outline
target_words: [TARGET -- e.g., 1200]
research_sources:
  - "[[research/Chapter_[XX]/answers/[FOLDER]/[FILE]]]"
tags:
  - section
  - [TOPIC TAG]
---

# [SECTION TITLE]

[OPENING HOOK: Start with something specific -- a company example, a
surprising number, a practitioner insight. Do NOT open with "In this
section we will explore..." or any variation of throat-clearing.

2-3 sentences that pull the reader in and set up the argument.]

## [FIRST SUBHEADING]

[YOUR CONTENT: Build your argument with evidence from research.
Cite statistics and direct quotes using footnotes.]

[EXAMPLE OR CASE STUDY: Ground the point in something real.
A named company, a specific number, a concrete outcome.]

## [SECOND SUBHEADING]

[YOUR CONTENT: Build on the previous subsection. Introduce a
framework, comparison, or deeper analysis as appropriate.]

[Include specific evidence. Numbers over adjectives.
"18 months" not "a long time."]

## [THIRD SUBHEADING]

[YOUR CONTENT: Aim for 3-5 subheaded subsections per
~1,200-word section. Adjust based on your word target.]

> **For [AUDIENCE 1 -- e.g., startup founders]:** [Specific, actionable
> guidance for this reader type. What should they do Monday morning?]
>
> **For [AUDIENCE 2 -- e.g., enterprise leaders]:** [Specific, actionable
> guidance for this reader type. Different context, different advice.]

[CLOSING: Land the section -- don't let it trail off. Make a point,
set up the next section, or give the reader a clear takeaway.
Do NOT write "In conclusion..." or summarize what you just said.]

---

## References

[^source-tag]: Source Name -- [link text](URL)
[^source-tag-2]: Source Name -- [link text](URL)

<!-- INTERNAL: Research Sources
- [[research/Chapter_[XX]/answers/[FOLDER]/[FILE]|Description]]
-->
```

---

## Usage Notes

- **Subheadings:** Use `##` for major breaks within the section. Typically 3-5 per section.
- **Citations:** Every statistic and direct quote needs a `[^footnote]`. Reuse the same tag when citing the same source multiple times.
- **Research block:** The HTML comment at the bottom tracks which research files informed this section. It is excluded from reader-facing output.
- **Audience callouts:** Use the blockquote format for audience-specific advice. Include only when genuinely different guidance applies.
- **Word target:** Frontmatter `target_words` drives your word count tracker. Adjust per section if some topics need more space.
