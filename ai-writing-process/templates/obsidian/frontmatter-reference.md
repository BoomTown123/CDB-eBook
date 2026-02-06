# Frontmatter Reference

Quick reference for all frontmatter fields used across content types. Copy the relevant block when creating new files.

---

## Content Types and Required Fields

### Chapter Intro (00-Chapter-Intro.md)

| Field | Required | Values / Notes |
|-------|----------|----------------|
| type | Yes | `chapter` |
| book | Yes | `[your-book-slug]` |
| part | Yes | Part number (1 to [N]) |
| chapter | Yes | Chapter number (1 to [N]) |
| title | Yes | Chapter title in quotes |
| aliases | Yes | `ch[XX]`, `Chapter [X]` |
| status | Yes | See status workflow below |
| target_words | Yes | Total chapter word target |
| summary | Yes | One sentence description |
| key_concepts | No | Links to `[[concepts/Name]]` notes |
| related_chapters | No | Links like `[[ch05\|Title]]` |
| tags | Yes | `chapter` + part tag + topic tags |

### Section (01-Section-Name.md)

| Field | Required | Values / Notes |
|-------|----------|----------------|
| type | Yes | `section` |
| book | Yes | `[your-book-slug]` |
| part | Yes | Part number |
| chapter | Yes | Chapter number |
| section | Yes | Section number within chapter |
| title | Yes | Section title in quotes |
| status | Yes | See status workflow below |
| target_words | Yes | Section word target |
| research_sources | No | Links to research answer files |
| tags | Yes | `section` + topic tags |

### Part Intro (00-Part-Intro.md)

| Field | Required | Values / Notes |
|-------|----------|----------------|
| type | Yes | `part-intro` |
| book | Yes | `[your-book-slug]` |
| part | Yes | Part number |
| title | Yes | Part title in quotes |
| status | Yes | See status workflow below |
| summary | Yes | 1-2 sentence part description |
| tags | Yes | `part` + topic tag |

## Status Workflow

```
outline --> drafting --> revising --> editing --> done
```

| Status | Meaning |
|--------|---------|
| `outline` | Structure defined, content not started |
| `drafting` | Content being written |
| `revising` | Content review and structural improvement |
| `editing` | Final editorial and copy-editing pass |
| `done` | Publication ready |

## Tag Conventions

- Use flat tags only (no hierarchical `parent/child` tags)
- Maintain a central tag index document in `planning/`
- Core structural tags: `chapter`, `section`, `part`, `concept`, `research`
- Add topic tags for your book's major themes: one tag per theme
- Keep the total tag vocabulary under [YOUR LIMIT -- e.g., 30 tags]

