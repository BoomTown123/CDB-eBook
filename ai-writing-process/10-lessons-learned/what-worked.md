# What Worked

The high-impact decisions that made the biggest difference. Not everything here was obvious upfront -- some only became clear after watching the alternative fail.

---

## 1. Voice System Before Everything

Building the 6-file voice system before writing a single chapter was the highest-ROI investment in the entire project. Two days of work. Saved weeks of editing.

Without it, every chapter requires paragraph-by-paragraph rewriting to remove AI patterns. With it, output sounds like the author from the first draft. Not perfect, but close enough that editing becomes refinement rather than reconstruction.

The system includes a gold standard sample (385 words of your best writing), a voice guide, audience empathy profiles, authenticity markers, a quick reference checklist, and a learnings file that grows with every chapter. Together they give every writing session the same constraints. Constraints produce consistency.

Build the voice system first. Before the outline. Before the research. Before you write a single section.

---

## 2. Research-First Pipeline

Writing after research instead of before research changed the economics of evidence. Early drafts were opinion-heavy, citation-light. The kind of prose that makes enterprise readers close the book.

Once the pipeline was in place -- 180+ Perplexity prompts, automated collection, synthesis scripts that extract stats and quotes with source URLs -- citation density went from sporadic to 1 per 105 words. Not because I was trying to cite more, but because citing became cheap. When stats arrive pre-formatted with footnote keys, you use them. When you have to manually hunt down a source mid-sentence, you skip it.

---

## 3. Separate Writer and Reviewer Agents

The same AI writing and reviewing its own work produces mild self-congratulation, not useful critique. It finds minor issues but misses structural problems.

The fix: distinct personas with different system prompts, tools, and success criteria. The reviewer's research gap analysis -- checking what research was *available* but not *used* -- was particularly valuable. It surfaced evidence the writer agent ignored because it didn't fit the argument being made.

In one chapter, the reviewer caught that 5 of 7 sections opened with "Here's the thing." Same company example used 4 times. Stats conflicting between sections. None visible from inside a single section. All obvious from the reviewer's cross-section vantage point.

---

## 4. Section Batching (Max 4 Per Agent)

Quality degraded noticeably past 4 sections in a single agent session. Voice drifted. Examples repeated. Research references got muddled.

Splitting into batches with handoff summaries maintained quality. The handoff protocol: themes established, narrative thread to continue, examples already used, style notes, open threads for the next batch. An 8-section chapter requires 2-3 sessions. More orchestration overhead, but less rework than one session that trails off.

---

## 5. The Kill List

A living document of phrases to delete on sight. Started small ("it's important to note," "let's delve into"). Grew with every chapter.

Chapter 3 taught the lesson hardest: 5 of 7 sections opened with "Here's the thing." A phrase from the voice guide's "use these" list, used so reflexively it became a tic. It went on the kill list -- not banned, but flagged when it appears more than once per chapter.

The kill list lives in the de-AI editing prompt and runs automatically. Without it, these patterns are invisible during writing and glaring during reading.

---

## 6. Automated Quality Audits

Six analysis skills running checks across all 81 sections: voice scoring, citation density, opening variety, link structure, term diversity, research coverage.

What made this work: the weighted health score. Voice (25%), citations (20%), research (20%), links (15%), openings (10%), vocabulary (10%). One number per chapter instead of six reports. The pipeline catches what human review misses: repeated patterns, inconsistent terminology, orphaned references. Human review catches what the pipeline misses: whether an argument actually lands. You need both.

---

## 7. Obsidian Over Google Docs

Wiki-linking, concept notes, graph view, Dataview queries -- these aren't nice-to-haves at book scale. They're structural necessities.

Graph view showed isolated sections. Backlinks answered "where else did I discuss this?" instantly. Dataview automated progress tracking. Frontmatter made every section queryable by status, word count, and concept coverage.

Trade-off: steeper learning curve, no real-time collaboration. For solo authorship with deep internal structure, worth it. For a team on a shorter document, Google Docs is fine.

---

## 8. Three Drafts, Not One Perfect Draft

Each draft improved the system as much as the manuscript. Draft 1 revealed which prompts produced generic output. Draft 2 exposed review pipeline gaps. Draft 3 was where the system matched the ambition.

- **Draft 1:** No voice encoding, no research pipeline. Read like competent AI prose -- exactly wrong for a book that needs to sound like one human with strong opinions.
- **Draft 2:** Voice system + research. Chapters started sounding like a specific author. But no automated quality measurement.
- **Draft 3:** Full quality pipeline + editorial review. Self-correcting: audit skills caught drift before it compounded.

Plan for 2-3 drafts. Use each one to improve your tooling, not just your prose.

---

## The Pattern

The common thread: front-loading effort to reduce rework. Voice files upfront. Research before writing. Kill lists before they're needed. Quality pipelines before problems compound.

Every shortcut tried early -- skipping voice files, writing without research, self-reviewing -- cost more to fix than doing it right from the start.

---

See also: [What Failed](what-failed.md) | [If Starting Over](if-starting-over.md) | [Architecture Decisions](../01-overview/architecture-decisions.md)
