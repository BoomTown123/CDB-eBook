# Chapter Template

Use this as the starting point for every `00-Chapter-Intro.md` file. Copy it, fill in the placeholders, and write the hook.

---

```markdown
---
type: chapter
book: [YOUR-BOOK-SLUG]
part: [PART NUMBER]
chapter: [CHAPTER NUMBER]
title: "[CHAPTER TITLE]"
aliases:
  - "ch[XX]"
  - "Chapter [X]"
status: outline
target_words: [TARGET -- e.g., 6500]
summary: "[ONE SENTENCE SUMMARY OF THIS CHAPTER]"
key_concepts:
  - "[[concepts/[CONCEPT 1]]]"
  - "[[concepts/[CONCEPT 2]]]"
  - "[[concepts/[CONCEPT 3]]]"
related_chapters:
  - "[[ch[XX]|[RELATED CHAPTER TITLE]]]"
  - "[[ch[XX]|[RELATED CHAPTER TITLE]]]"
tags:
  - chapter
  - [PART TAG -- e.g., foundations, building]
  - [TOPIC TAG -- e.g., strategy, architecture]
---

# Chapter [X]: [CHAPTER TITLE]

[HOOK: 2-3 paragraphs that open with a compelling story, statistic, or
insight. Ground it in something specific -- a company, a number, a moment.
Do NOT open with "In this chapter..." or any throat-clearing.

End the hook by stating what this chapter covers and why the reader
should care right now.]

---

## What You'll Learn

**[[01-[Section-Name]|[Section Title]]]** -- [1-2 sentence preview.
Frame it as a tension or question, not a dry summary.]

**[[02-[Section-Name]|[Section Title]]]** -- [1-2 sentence preview.
Include a specific insight the reader will gain.]

**[[03-[Section-Name]|[Section Title]]]** -- [1-2 sentence preview.]

**[[04-[Section-Name]|[Section Title]]]** -- [1-2 sentence preview.]

[Add or remove entries to match your actual section count.]

---

## The Real Question

[2-3 paragraphs synthesizing the chapter's core argument. This is where
you address your target audience directly. What decision does this chapter
help them make? What misconception does it correct?

End with a forward-looking statement that creates momentum into the
first section.]
```

---

## Usage Notes

- **Status flow:** Start at `outline`, move to `drafting` when you begin writing the hook, then `revising` / `editing` / `done`.
- **Aliases:** The `ch[XX]` alias lets you link to this chapter from anywhere with `[[ch06]]` or `[[ch06|Agent Architecture]]`.
- **Key concepts:** Link to concept notes in your `concepts/` folder. Create concept notes as you write.
- **Section previews:** Write these after the sections are drafted so they reflect actual content, not aspirations.
