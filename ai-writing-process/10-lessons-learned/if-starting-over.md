# If Starting Over

Not the full 14-skill, 70-module system. The lean version that captures 80% of the value with 20% of the infrastructure.

---

## The Premise

The system documented in this repository evolved over 3 drafts, 12 chapters, and several months. Much of it solves problems that only appear at scale -- 81,000 words, 775 citations, consistency across chapters written weeks apart.

Your first book doesn't need all of it. It needs the parts that prevent expensive mistakes and the parts that make AI output sound like you. Everything else can wait.

---

## Phase 1: Voice Foundation (Before Writing Anything)

Non-negotiable. Skip this and you'll rewrite your entire first draft.

1. **Find your gold standard.** 300-500 words of your best writing. Something that sounds unmistakably like you.
2. **Analyze it.** Extract sentence length patterns, metaphor usage, paragraph openings, tone shifts, default phrases.
3. **Create 4 files:** Voice guide (your DNA), authenticity markers (phrases to use and kill), audience personas (who you're writing for), quick reference (one-page session checklist).
4. **Build the master system prompt** incorporating all 4 files.
5. **Test on 2-3 throwaway sections.** Compare output to your gold standard. Iterate until the output sounds like you on a good day.

**Time:** 1-2 days. Highest-leverage work in the entire project.

---

## Phase 2: Research Pipeline

Evidence-first changes the quality of everything downstream.

1. **Set up an Obsidian vault** with Part / Chapter / Section folders. The folder structure is your outline.
2. **Create chapter outlines** with section titles and 1-2 sentence argument descriptions.
3. **Generate 10-15 research prompts per chapter.** Specific: not "research AI agents" but "find statistics on enterprise AI agent adoption rates and ROI metrics from 2023-2025."
4. **Run the research.** Perplexity Pro. Manual is fine under 10 chapters; automate above that.
5. **Build synthesis files** per section: statistics with source URLs, quotes with attribution, company examples with specifics.

**Key rule:** Research before writing. Evidence shapes the argument, not decorates it.

**Time:** 2-3 hours per chapter.

---

## Phase 3: Writing System

Fewer prompts than you think, but the ones you have need to be good.

1. **5 writing prompts:** Section body (the workhorse), chapter opening, chapter closing, framework, case study.
2. **3 editing prompts:** Voice check, de-AI pass, tighten prose.
3. **Separate writer and reviewer agents.** Different system prompts, different success criteria.
4. **Max 4 sections per session.** Handoff summaries between batches: themes, examples used, narrative thread, style notes.

**Time:** 8-12 hours to build. You'll refine across your first 3-4 chapters.

---

## Phase 4: Quality Pipeline

Start minimal. Add checks as patterns emerge.

1. **Build a kill list** from your first 3 chapters. Read output carefully, note every phrase the AI overuses.
2. **Voice check script.** Grep for kill list violations. Count opening patterns.
3. **Citation audit script.** Find uncited statistics. Flag sections below target density.
4. **Run both after every chapter.** Takes 2 minutes.
5. **Add more checks as needed.** Don't build them upfront -- build them when you first encounter the problem they solve.

**Time:** 4-6 hours initial, grows incrementally.

---

## Phase 5: Editorial

One pass per focus. Mixing structural editing with copy editing catches neither well.

1. **Structure and argument.** Does each section make one clear point? Does the chapter build a sustained argument?
2. **Prose and voice.** Does it sound like you? Metaphors sustained, not mixed? Sentence lengths varied?
3. **Grammar and consistency.** Terminology, formatting, citations, cross-references.
4. **Cross-chapter check every 4 chapters.** Grep for company names, statistics, technical terms. Catch contradictions cheap.

**Time:** 4-8 hours per chapter. The longest phase. Worth it.

---

## What to Skip

Valuable for this project at scale. Not valuable on day one:

- **The intelligence app.** Flask + PostgreSQL is overkill until 50,000+ words. Use scripts and SQLite if you need persistence.
- **14 specialized skills.** Start with 3: write, review, research-reader. Add when you're repeating the same multi-step process for the third time.
- **6 analysis skills.** Start with voice check and citation audit. The rest solve problems you won't have until chapter 6+.
- **Dataview dashboards.** A word count script and a manual checklist cover 90% of tracking needs.
- **Complex linking systems.** Concept notes and MOCs become valuable at book scale. Basic cross-chapter references are enough for your first 4 chapters.

Build infrastructure in response to problems, not in anticipation of them.

---

## The Minimum Stack

| Tool | Role |
|------|------|
| **Claude Code** (Opus-class model) | Writing, editing, review |
| **Perplexity Pro** | Research and citation generation |
| **Obsidian** | Vault-based manuscript management |
| **3-4 Python scripts** | Word count, citation audit, voice check, PDF generation |
| **Voice system** (4 files) | Author voice encoding |
| **8 prompts** (5 writing, 3 editing) | AI instruction set |

Setup time: 3-5 days before your first real chapter.

---

## Scale When You Need To

The scaling sequence that worked:

1. **Chapters 1-3:** Voice system + research + basic prompts. Learning what works.
2. **Chapters 4-6:** Kill list + quality scripts + reviewer agent. Patterns emerging that need systematic fixes.
3. **Chapters 7-9:** Cross-chapter consistency + editorial workflow. Manuscript big enough for internal contradictions.
4. **Chapters 10-12:** Full quality pipeline + intelligence app if needed. Polishing, not building.

The voice system is non-negotiable from day one. Everything else can wait until the problem it solves actually shows up.

---

See also: [What Worked](what-worked.md) | [What Failed](what-failed.md) | [End-to-End Flow](../01-overview/end-to-end-flow.md) | [Building a Voice System](../02-author-voice/building-a-voice-system.md)
