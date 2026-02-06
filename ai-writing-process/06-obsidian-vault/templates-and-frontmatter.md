# Templates and Frontmatter

Every section file in this book starts with YAML frontmatter -- a structured block of metadata that sits above the prose. This isn't bureaucratic overhead. It's how AI agents understand context without reading the entire manuscript, how Dataview generates live dashboards, and how the status pipeline knows which sections need work.

Without standardized frontmatter, every writing session starts with the agent guessing: What chapter is this? What section number? What's the word target? What research should I pull? With frontmatter, all of that is answered before the first sentence is written.

---

## Chapter Intro Frontmatter

The `00-Chapter-Intro.md` file in each chapter folder carries the heaviest metadata. It defines the chapter's identity for the entire system:

```yaml
---
type: chapter
book: ai-first-company
part: 2
chapter: 6
title: "Agent Architecture"
aliases:
  - "ch06"
  - "Chapter 6"
status: drafting
target_words: 6500
summary: "How to architect chat and background agents as a coordinated system"
key_concepts:
  - "[[concepts/Agent Hub]]"
  - "[[concepts/Probabilistic AI]]"
related_chapters:
  - "[[ch05|Building with AI]]"
  - "[[ch07|Microservice Pattern]]"
tags:
  - chapter
  - building
  - agents
---
```

The `aliases` field is what makes short linking work. Instead of typing the full path to a chapter intro, any note in the vault can write `[[ch06]]` and Obsidian resolves it. Small thing, but across 1,199 links it saves real friction.

The `key_concepts` field links to atomic concept notes -- the hub nodes that connect chapters through shared ideas. When the writer agent sees `[[concepts/Agent Hub]]`, it knows to reference that concept and maintain consistency with how other chapters discuss it.

---

## Section Frontmatter

Individual sections carry lighter metadata, focused on identity and status:

```yaml
---
type: section
book: ai-first-company
part: 2
chapter: 6
section: 1
title: "Chat Agents vs Background Agents"
status: drafting
target_words: 1200
research_sources:
  - "[[research/Chapter_06/answers/s_6.1_chat_agents/01_chat_agents.md]]"
tags:
  - section
  - agents
---
```

The `research_sources` field is the bridge between the research pipeline and the writing agent. When the writer agent opens this section, it reads the linked research files first -- pre-formatted stats, quotes, and company examples waiting to be woven into prose. No manual copy-pasting from browser tabs.

The `target_words` field constrains the agent. Without it, sections balloon to 2,000+ words as the agent tries to be thorough. With a 1,200-word target, the agent learns to be selective -- one strong example instead of three mediocre ones.

---

## The Status Workflow

Every file moves through 5 stages:

```
outline → drafting → revising → editing → done
```

This isn't just labels. Each status triggers different behavior:

| Status | What It Means | Who Touches It |
|--------|---------------|----------------|
| `outline` | Structure defined, no prose | Human |
| `drafting` | First draft in progress or complete | Writer agent |
| `revising` | Content complete, undergoing review | Reviewer agent |
| `editing` | Line-level polish, citations verified | Editorial skill |
| `done` | Publication-ready | Human (final sign-off) |

The Dashboard queries this field in real time. You open `Dashboard.md` and immediately see: 47 sections done, 22 revising, 12 drafting, 0 outline. No manual tracking spreadsheet. The frontmatter *is* the tracking system.

The publish-review skill automatically updates status to `revising` when it runs. The writer agent sets `drafting` when it produces a first draft. Status flows through the system without manual updates.

---

## Templater Templates

Obsidian's Templater plugin auto-fills frontmatter when creating new files. Instead of manually typing 15 YAML fields, you trigger a template and fill in 2-3 values. The rest auto-populates.

Four templates handle the core content types:

| Template | Location | Creates |
|----------|----------|---------|
| New Chapter | `templates/New Chapter.md` | Chapter intro with full metadata |
| Section Note | `templates/Section Note.md` | Section file with research links |
| Concept Note | `templates/Concept Note.md` | Hub note with chapter connections |
| Research Note | `templates/Research Note.md` | Research file with credibility scoring |

The Section Note template includes scaffolding beyond frontmatter -- placeholder sections for the opening hook, main argument, framework or analogy, and a references block. This structure mirrors the writing prompts, so the agent knows exactly where each type of content belongs.

---

## Frontmatter as System Contract

Here's the thing about frontmatter: it's not documentation. It's a contract between the human author, the AI agents, and the automation scripts. When the `enrich_section_frontmatter.py` script adds concept links, it reads frontmatter. When Dataview generates the Dashboard, it queries frontmatter. When the writer agent decides which research to pull, it reads frontmatter.

Break the contract -- misspell a field name, skip a required value, use a non-standard status -- and the system silently degrades. Sections vanish from dashboards. Research doesn't load. Status tracking goes stale.

The templates exist to prevent this. Use them.

---

**Related:** [Vault Architecture](vault-architecture.md) | [Frontmatter Reference Template](../templates/obsidian/frontmatter-reference.md)
