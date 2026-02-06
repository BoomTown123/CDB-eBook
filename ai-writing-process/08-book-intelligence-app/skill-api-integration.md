# Skill API Integration

> **Context:** Claude Code skills run in ephemeral contexts -- they can read files and run scripts, but they can't persist state or query historical data. The book intelligence app provides a persistent backend that skills call via HTTP. This document covers the integration pattern, the endpoints, and when the API layer is worth building.

---

Let's be honest about something: Claude Code skills are powerful but stateless. A skill can read your vault, run a Python script, and format a response. What it can't do is remember what it found last time, compare today's analysis to last week's, or query a database of pre-computed metrics.

That's the gap the API fills. Skills stay lightweight. The app handles persistence.

## The Problem

Without the API, every skill invocation starts from scratch. The review-chapter skill would need to:

1. Parse all sections in the chapter from raw markdown files
2. Run voice analysis (check kill list, count hedging, flag AI patterns)
3. Run citation analysis (parse footnotes, count density, find gaps)
4. Run link analysis (extract wiki-links, check resolution, calculate connectivity)
5. Run opening analysis (classify patterns, check for repetition)
6. Run research coverage analysis (match research files to sections)
7. Aggregate scores
8. Format results

That's minutes of work, repeated identically every time. And it can't tell you whether the scores improved since your last editorial pass.

With the API, the same skill makes one HTTP call and gets everything back in under a second -- pre-computed, cached, with historical context.

## How Skills Use the API

Each skill maps to one or more API endpoints:

| Skill | Endpoint | What It Returns |
|-------|----------|----------------|
| `review-chapter` | `GET /api/analysis/chapter/{n}` | All 6 dimension scores, chapter health, priority issues, trend data |
| `check-voice` | `GET /api/analysis/voice/{section}` | Voice score (0-100), specific violations with line numbers, hedging ratio |
| `check-citations` | `GET /api/analysis/citations/{section}` | Citation density, uncited claims list, format inconsistencies |
| `map-research` | `GET /api/research/coverage/{chapter}` | Research-to-section matrix, unused files, coverage percentage |
| `audit-links` | `GET /api/links/connectivity/{chapter}` | Link graph, orphan sections, hub identification, broken links |
| `find-similar` | `POST /api/search/semantic` | Sections ranked by semantic similarity to a query string |
| `compare-drafts` | `GET /api/analysis/compare/{chapter}` | Score deltas between draft versions, dimension-by-dimension |

The pattern is consistent: the skill handles user interaction and output formatting. The API handles data and computation. Clean separation.

## The Flow

Here's what happens when you invoke `/review-chapter 7`:

```
1. Skill receives command
   |
2. Skill calls GET /api/analysis/chapter/7
   |
3. API checks: is the cached analysis current?
   |-- Content hashes match last analysis? Return cached results.
   |-- Content changed? Trigger re-analysis for changed sections only.
   |
4. API returns JSON:
   {
     "chapter": 7,
     "health_score": 81,
     "dimensions": {
       "voice": {"score": 87, "violations": 3, "details": [...]},
       "citations": {"score": 78, "density": 8.2, "gaps": [...]},
       "links": {"score": 84, "connectivity": 0.72, "orphans": []},
       ...
     },
     "trend": {"previous_score": 74, "delta": +7},
     "priority_issues": [...]
   }
   |
5. Skill formats results for the user
   |
6. Results stored in Metric table for historical tracking
```

The re-analysis check in step 3 is the key optimization. If you haven't edited chapter 7 since the last review, the response is instant -- a database read, not a full analysis run. If you edited section 7.3, only that section gets re-analyzed. The other sections keep their cached scores.

## Deep Review Mode

Beyond the standard per-dimension analysis, the app supports deep review -- a cross-cutting analysis that looks at patterns no single dimension captures:

**Semantic similarity between sections.** Using pgVector embeddings, the deep review identifies sections that cover overlapping ground. We caught sections in chapters 5 and 7 that were 87% similar in embedding space -- essentially the same argument made twice. That's invisible to keyword-based tools.

**Cross-chapter argument consistency.** Does chapter 3's claim about agent adoption rates match chapter 9's? Deep review flags statistics that appear in multiple sections with different values. This caught a case where "65% of enterprises" in chapter 4 became "72% of enterprises" in chapter 10 -- same source, transcription error.

**Citation source diversity.** Are you leaning too heavily on one source? Deep review counts how many sections cite each URL. When one Contrary Research report appeared in 11 of 12 chapters, the deep review flagged it. The report was good -- but over-reliance on any single source undermines credibility.

**Company example distribution.** Which companies appear in which chapters? Deep review surfaces when a company example (say, Harvey) is used 6 times while others appear once. It also identifies chapters with no real company examples -- a gap that generic AI writing tends to produce.

## Dashboard Integration

The web UI provides a visual layer on top of the API. It's minimal -- this isn't a SaaS product, it's a local development tool -- but it shows three things at a glance:

1. **Book health overview.** All 12 chapters with their composite scores, color-coded. Red below 60, yellow 60-79, green 80+.
2. **Chapter detail.** Per-dimension scores with sparklines showing trends across editorial passes. Click a dimension to see specific issues.
3. **Priority queue.** Across the entire book, the top 10 issues ranked by impact. "Chapter 4 has 7 uncited statistics" ranks higher than "Chapter 11 uses 'delve' once."

The dashboard consumes the same API that skills use. No separate data path. What the dashboard shows is exactly what the skills query.

## Practical Considerations

**Everything runs locally.** Docker Compose brings up Flask and PostgreSQL on `localhost`. No cloud dependency. No data leaves your machine. Skills call `http://localhost:5000/api/...` and get responses from a container running on the same laptop.

**Setup is one command.** `docker compose up -d` starts both services. First run takes a minute for the database initialization and initial indexing. Subsequent starts take seconds.

**The API is not authenticated in any meaningful way.** It runs on localhost behind Docker networking. If you need real auth, add it. For a solo writing project on a development machine, it's overhead without benefit.

## When to Build This

The API layer adds value when multiple skills query the same analyzed data. Here's the decision framework:

| Your Situation | Recommendation |
|---------------|----------------|
| 1-3 skills, no shared state needed | File-based caching. Skills write/read JSON files. |
| 4-6 skills, some shared state | SQLite with a shared query module. No HTTP, no Docker. |
| 7+ skills, historical tracking, semantic search | The full app. API layer, PostgreSQL, pgVector. |
| Team of writers querying the same data | The full app, mandatory. Concurrent access needs a real database. |

We crossed the threshold at skill number 8. The first 7 skills managed with a mix of scripts and cached JSON files. Adding the review-chapter skill -- which needed data from 5 other analysis dimensions -- made the file-based approach unsustainable. One API call replaced 5 script invocations and a manual aggregation step.

The question isn't whether the app is technically impressive. It's whether the engineering hours save more writing hours than they cost. For this project, the answer became yes somewhere around Draft 2. For yours, it might never be yes. And that's fine.

---

**Deep dives:** [App Architecture](app-architecture.md) | [Analysis Pipeline](analysis-pipeline.md) | [Quality Skills](../04-agent-system/quality-skills.md) | [Building Custom Skills](../04-agent-system/building-custom-skills.md)
