# Architecture Decisions

Every decision here solved a specific problem we hit during writing. No theoretical architecture -- these are battle-tested choices from producing 81,000+ words and 775 citations across 12 chapters.

---

## Decision 1: Encode Voice as System Files, Not Inline Instructions

**Problem:** AI output sounded generic. "Write in my voice" in prompts produced corporate blog posts. Every session started from zero.

**Solution:** 7 dedicated voice reference files -- gold standard example, voice guide, blog-to-book adaptation, audience empathy profiles, authenticity markers, quick reference, and a learnings file that evolved with mistakes. Composed into every prompt as persistent context.

**Result:** Reviewers couldn't distinguish AI-assisted sections from hand-written ones after 2 iterations.

**Trade-off:** ~2 days upfront to build the voice system. Worth it by chapter 2.

---

## Decision 2: Modular Prompts Over Monolithic Instructions

**Problem:** One giant prompt for "write a chapter" produced inconsistent results. Voice, structure, citations, audience, research integration -- all competing for attention in one instruction.

**Solution:** 26 modular prompts across 5 categories: writing (9), editing (5), review (4), linking (3), fixing (5). Each does one thing. The orchestration skill composes them at runtime.

**Result:** When section openings were too formulaic, we fixed one prompt. When citations were inconsistent, a different one. No cascading side effects.

**Trade-off:** More complex orchestration. But debugging a 2,000-word monolithic prompt where one edit breaks something else is worse.

---

## Decision 3: Multi-Agent Batching Over Sequential Writing

**Problem:** Chapters with 6+ sections exceeded effective context windows. Quality degraded past section 4 -- voice drift, repeated examples, forgotten research.

**Solution:** Max 4 sections per agent. The first agent produces a handoff summary covering themes, examples used, narrative thread, and style notes. The next agent picks up from there.

**Result:** Consistent quality across 8-section chapters. No detectable voice drift between batches.

**Trade-off:** Handoff design is the hard part. Transitions between batches need human review.

---

## Decision 4: Research-First Writing, Not Write-Then-Research

**Problem:** Early drafts were opinion-heavy, citation-light. Confident but ungrounded. The enterprise audience wants evidence.

**Solution:** 180+ Perplexity research prompts run before writing starts. A research-reader skill with 9 extraction scripts -- snapshots, citation formatting, argument support with counter-arguments, unused research detection, credibility-scored stats, confidence-scored quotes. Every section begins with a research snapshot.

**Result:** Writing is faster because the agent synthesizes rather than guesses. 775 citations across 12 chapters without manual research.

**Trade-off:** 2-3 hours of research pipeline per chapter before writing starts.

---

## Decision 5: Obsidian as Writing Environment, Not Google Docs

**Problem:** Chapters reference each other. Concepts span sections. Research links to multiple chapters. Linear document tools can't represent this structure.

**Solution:** Obsidian vault with wiki-linking, concept notes as hubs, Maps of Content for navigation, Dataview for dynamic queries. 1,199 internal links, 68% section-to-concept coverage.

**Result:** Graph view reveals structural gaps. Backlinks answer "where else did I discuss this?" instantly.

**Trade-off:** Steeper learning curve. No real-time collaboration. Worth it for solo authorship with deep internal structure.

---

## Decision 6: Separate Writer and Reviewer Agents

**Problem:** Self-review produces blind spots. The writer-agent doesn't catch its own repetitive openings, over-used examples, or voice drift.

**Solution:** Distinct writer and reviewer personas. Different system prompts, different tools, different success criteria. The reviewer has deduplication scanning, phrase kill lists, fact verification, and research gap analysis.

**Result:** The reviewer caught patterns invisible to the writer -- 5 of 7 sections in one chapter started with "Here's the thing." Same company example used 4 times. Stats conflicting across sections.

**Trade-off:** Double the prompt engineering. Two personas, two toolsets, two instruction sets to maintain.

---

## Decision 7: Build a Book Intelligence App

**Problem:** At 81,000 words, scripts hit limits. You can't grep your way to "which chapters have voice drift?" or "what's my citation density trend?"

**Solution:** Flask + PostgreSQL + pgVector. 70+ modules for voice scoring, citation density, link health, term distribution, research coverage. A unified dashboard aggregates 6 dimensions into a chapter health score (0-100).

**Result:** Weighted scoring across voice (25%), citations (20%), research (20%), links (15%), openings (10%), vocabulary (10%). Progress tracking shows deltas between review passes.

**Trade-off:** A software project bolted onto a writing project. Only worth it at book scale. Under 30,000 words, scripts are enough.

---

## Decision 8: 4-Phase Editorial Review

**Problem:** "Review the chapter" is too vague. A single pass mixes structural issues with typos and misses both.

**Solution:** Four phases: deduplication/consistency scan, argument/evidence strengthening, voice/structure polish, final verification. Each phase has its own checklist and grep-based validation.

**Result:** The deduplication phase alone caught repeated statistics, conflicting numbers across sections, and over-reliance on single companies -- problems read-through reviews consistently miss.

**Trade-off:** Each chapter goes through 4 passes minimum. Slower, but you don't publish chapters where the same stat appears three times with different values.

---

## Summary Table

| Decision | Problem Solved | Key Trade-off |
|----------|---------------|---------------|
| Voice as system files | Generic AI output | 2-day upfront investment |
| 26 modular prompts | Inconsistent results | Orchestration complexity |
| Multi-agent batching | Context window degradation | Handoff design effort |
| Research-first pipeline | Opinion-heavy drafts | 2-3 hours pre-writing per chapter |
| Obsidian vault | Complex relationships | Learning curve |
| Separate writer/reviewer | Review blind spots | Double prompt engineering |
| Book intelligence app | Analysis at scale | Engineering investment |
| 4-phase editorial | Vague review criteria | Slower publication |

The pattern across all 8: front-load effort to reduce rework. Every shortcut we tried early -- skipping voice files, using one giant prompt, writing without research -- cost more time to fix than doing it right from the start.
