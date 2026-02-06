# Analysis Pipeline

> **Context:** The book intelligence app runs automated analysis across all 81 sections of *Blueprint for An AI-First Company*, scoring 6 quality dimensions and tracking trends across drafts. This document covers what it analyzes, how the pipeline works, and how embeddings enable queries that keyword search can't.

---

Automated analysis sounds impressive until you realize what it actually means: running the same checks a human editor would run, except across 81 sections simultaneously, and remembering the results next time.

That's the pipeline. Not magic. Persistence and scale.

## What It Analyzes

Six quality dimensions, each measuring something specific and actionable:

| Dimension | What It Measures | Output | Why It Matters |
|-----------|-----------------|--------|----------------|
| **Voice** | Kill list violations, hedging language, AI-pattern phrases | Score 0-100 | One "it's important to note" in chapter 9 breaks the illusion that one human wrote the whole book. |
| **Citations** | Density per section, uncited claims, format consistency | Density ratio + gap list | Enterprise readers expect evidence. A claim without a citation is an opinion. |
| **Links** | Cross-chapter connectivity, orphan sections, hub identification | Connectivity % | Orphan sections -- no links in or out -- signal structural problems. |
| **Terms** | Overused words, inconsistent terminology, synonym suggestions | Flagged term list | "AI-first" vs "AI first" vs "AI-First" across 81 sections is the kind of inconsistency that makes copy editors twitch. |
| **Openings** | Pattern variety, repetitive starts across sections | Variety score | When 5 of 7 sections start with "Here's the thing," the reader notices before the writer does. |
| **Research** | Coverage gaps, unused research files, source diversity | Coverage % | Unused research means wasted pipeline time or missed evidence. |

Each dimension produces a score and a list of specific issues. The voice analyzer doesn't just say "score: 72." It says "score: 72 -- 'delve' found in paragraph 3, 'important to note' in paragraph 7, hedging ratio 4.2% (target: under 2%)." Actionable beats abstract.

## How the Pipeline Works

Four stages, each building on the previous:

### 1. Indexing

Content from the Obsidian vault is indexed into PostgreSQL. The file watcher (`file_watcher.py`) monitors the vault directory for changes -- new files, modified content, deleted sections. When it detects a change, it re-indexes that section: parses frontmatter, extracts content, computes a content hash, and updates the Section table.

The content hash is the key optimization. If the hash hasn't changed since the last index, nothing happens. No re-parsing, no re-analysis trigger. At 81 sections, this saves minutes per run.

### 2. Analysis

Each dimension runs its analysis algorithm against indexed content. The voice analyzer checks content against the kill list, counts hedging phrases, and flags AI patterns. The citation analyzer parses footnote syntax, counts density per 1,000 words, and identifies claims that should be cited but aren't. And so on for each dimension.

Results are cached in the Analysis table, keyed by three things: section ID, dimension, and draft version. This means chapter 7's voice score from Draft 2 is a different record than chapter 7's voice score from Draft 3. Both persist. Both are queryable.

Analysis only re-runs when the content hash changes. Edit section 7.3? Only section 7.3 gets re-analyzed. The other 80 sections keep their cached results.

### 3. Aggregation

The dashboard service rolls section-level scores into chapter-level and book-level metrics. Chapter 7's voice score is the weighted average of its section voice scores. The book's overall citation density is the aggregate across all 81 sections.

The weighting formula for chapter health:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Voice | 25% | Voice consistency is the book's identity. Highest weight. |
| Citations | 20% | Evidence-backed claims are the credibility foundation. |
| Research | 20% | Research coverage ensures the pipeline investment pays off. |
| Links | 15% | Cross-references build cohesion across chapters. |
| Openings | 10% | Variety matters, but less than substance. |
| Terms | 10% | Consistency matters, but automated fixes are easy. |

These weights came from experience, not theory. Voice and citations caused the most reader-visible problems in Draft 1. Links and openings caused problems too, but subtler ones.

### 4. Trending

Every analysis run stores results with a timestamp. This builds a time series: chapter 7's voice score on January 15, January 22, February 3. Plot that, and you can see whether your editorial passes are working.

This is the feature that justified the database over scripts. A script can tell you the score *right now*. The database can tell you the score *over time*. "Chapter 7 voice improved from 64 to 89 across 3 editorial passes" is information you can't get from a script that re-computes from scratch each run.

## Embedding-Based Analysis

pgVector enables queries that keyword search fundamentally cannot answer.

**Conceptual similarity.** "Find all sections discussing agent architectures" returns results even if they use phrases like "autonomous workflows," "multi-step AI pipelines," or "orchestrated tool use" instead of "agent architectures." The embeddings capture meaning, not just words.

**Overlap detection.** "Which sections are most similar to each other?" surfaces unintentional repetition. We caught two sections -- one in chapter 5, one in chapter 7 -- that covered nearly the same ground about model selection. Without embeddings, this wouldn't have been visible until a reader noticed.

**Research matching.** "What research is semantically relevant to this section?" goes beyond the explicit links in frontmatter. A research file about Harvey's legal AI might be relevant to a section about vertical AI companies even if the section doesn't mention Harvey by name. Embeddings surface these connections.

The embeddings are 1536-dimensional vectors generated by OpenAI's embedding model, stored in pgVector alongside relational data. A similarity query is one SQL call with a vector distance operator -- no separate service, no API call to an external system.

## Cache Strategy

Analysis is expensive. Not "run it once and wait 10 minutes" expensive, but "run it 20 times a day during editorial review and feel the friction" expensive.

The cache operates on a simple principle: **analyze on change, serve from cache otherwise.**

Each section's content hash is computed on indexing. When a skill or the dashboard requests analysis, the pipeline checks: has the content hash changed since the last analysis? If not, return the cached result. If so, re-analyze that section and cache the new result.

Draft versions are part of the cache key. Switching from Draft 2 analysis to Draft 3 analysis doesn't invalidate anything -- both exist as separate records. Comparing them is a query, not a recomputation.

---

**Deep dives:** [App Architecture](app-architecture.md) | [Skill API Integration](skill-api-integration.md) | [Quality Skills](../04-agent-system/quality-skills.md)
