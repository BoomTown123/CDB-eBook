# Linking and Navigation

A 12-chapter book has a hidden problem that doesn't surface until you're halfway through: internal coherence. Chapter 9 introduces "data flywheel" as if it's new, but Chapter 1 already used the term in a different context. Chapter 6's agent architecture references patterns from Chapter 4, but there's no explicit connection. The reader notices. The author doesn't -- because at 81,000 words across weeks of writing, no one holds the entire manuscript in memory.

Obsidian's linking system solves this. Wiki-links create explicit connections between files. Backlinks surface implicit ones. Concept notes act as hubs that keep definitions consistent across chapters. The result: 1,199 internal links that make the manuscript's structure visible and auditable.

---

## Three Linking Layers

The vault uses three distinct types of links, each serving a different purpose:

| Layer | Syntax | Purpose | Example |
|-------|--------|---------|---------|
| **Section links** | `[[ch06/01-Chat-Agents]]` | Connect related sections across chapters | Section on agent economics links to infrastructure costs |
| **Concept links** | `[[concepts/Agent Hub]]` | Connect through atomic concept notes | Both Chapter 6 and Chapter 7 link to the same concept definition |
| **MOC links** | `[[MOC - Book Structure]]` | Navigate the whole vault structure | Entry points for finding chapters, concepts, or research |

Section links are the most common. Concept links are the most valuable -- they prevent the same idea from being defined inconsistently across chapters. MOC links are the least frequent but essential for onboarding anyone (human or AI) to the vault.

One enabler: chapter aliases. Chapter intro files have `aliases` in frontmatter (`ch06`, `Chapter 6`), so any note can write `[[ch06]]` instead of the full path. Across 1,199 links, that friction savings adds up.

---

## Concept Notes as Hubs

This is the structural insight that made the biggest difference. In `concepts/`, each file represents a single atomic idea -- Data Flywheel, Agent Hub, Build vs Buy Calculus, Probabilistic AI, Data Moats, AI Governance Framework, and others.

Each concept note contains:
- A clear definition (one paragraph)
- Why it matters
- A framework if applicable
- Chapter-by-chapter context showing how the concept appears differently in each chapter

The chapter-by-chapter context is the critical piece. "Data Flywheel" means something different in Chapter 9 (building one from user data) than in Chapter 1 (competitive advantage). The concept note captures both meanings and explicitly links to both chapters. When the writer agent is working on Chapter 9, it reads the concept note to understand how Chapter 1 already framed the idea -- and writes accordingly.

The vault has 9 concept notes. Before the linking enhancement, zero sections linked to concept notes. After: 68% of sections link to at least one concept. That 68% represents explicit semantic connections that didn't exist when the vault was just a folder of Markdown files.

---

## Bidirectional Linking

Obsidian's backlinks are the feature that separates it from every other Markdown editor. When Section 6.1 links to `[[concepts/Agent Hub]]`, the Agent Hub concept note automatically shows Section 6.1 in its backlinks panel. No manual work.

This means you can ask questions the manuscript can't answer otherwise:
- "Which sections discuss data moats?" -- Open the concept note, check backlinks.
- "What chapters reference Chapter 4's infrastructure patterns?" -- Open Chapter 4's intro, check backlinks.
- "Is this concept already defined somewhere?" -- Search before writing.

For AI-assisted writing, backlinks serve as a consistency check. If the reviewer agent sees that "data flywheel" appears in 4 sections, it can verify all 4 use the same definition. Without backlinks, that verification requires reading the entire manuscript.

---

## Vault Health Before and After

We ran a linking enhancement pass in January 2026 using Python scripts and manual curation. The numbers tell the story:

| Metric | Before Enhancement | After Enhancement |
|--------|-------------------|-------------------|
| Section-to-concept links | 0% | 68% |
| Average links per section | ~1 | 7.0 |
| Total vault links | ~630 | 1,199 |
| Concept notes | 5 | 9 |

The `enrich_section_frontmatter.py` script did the heavy lifting -- keyword-matching section content against concept definitions to batch-add 555 new links. The `graph_health_report.py` script then analyzed the results: link density per section, orphan files, missing bidirectional connections.

The graph view before enhancement showed sections as isolated nodes connected only to their chapter intro. After, sections clustered around concept hubs with visible cross-chapter connections. The difference is structural, not cosmetic -- it surfaces problems (orphan sections with no cross-references) and strengths (hub sections that connect multiple themes).

---

## Graph View as Editorial Tool

Obsidian's graph view isn't a visual novelty -- for a 12-chapter book, it's an editorial tool. Orphan sections (no cross-chapter links) show up as disconnected nodes, signaling content that either doesn't connect to anything else or has implicit connections that need to be made explicit. Hub sections (10+ links) cluster visibly, revealing which ideas multiple chapters build on. If two chapters are heavily interconnected but a third that should connect to them is isolated, you've found a structural gap before any human reads the draft.

---

**Related:** [Vault Architecture](vault-architecture.md) | [Dataview and Dashboards](dataview-and-dashboards.md) | [Vault Health](../07-automation/vault-health.md)
