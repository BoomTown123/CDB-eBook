# App Architecture

> **Context:** The book intelligence app is a Flask + PostgreSQL application that provides persistent analysis, semantic search, and API access for the writing system behind *Blueprint for An AI-First Company*. This document covers the stack, the architecture layers, and why each decision was made.

---

Here's the thing about building infrastructure for a writing project: every component has to justify its existence. No one needs Kubernetes to write a book. But when 14 skills need to query analysis data, when you're tracking quality across 3 drafts, and when "find sections about X" means semantic similarity not keyword matching -- you need more than scripts in a folder.

This is the architecture we landed on. Not what we planned upfront. What we converged on after hitting real limits.

## The Stack

| Component | Technology | Why This One |
|-----------|-----------|-------------|
| Web framework | Flask | Lightweight API. No need for Django's batteries. |
| Database | PostgreSQL | Reliable, supports pgVector natively, handles concurrent queries. |
| Embeddings | pgVector | Vector similarity search without a separate service. One database, not two. |
| Containerization | Docker Compose | Reproducible setup. `docker compose up` and everything works. |
| ORM | SQLAlchemy | Type-safe queries, relationship handling, migration support. |
| Migrations | Alembic | Schema evolution without manual SQL. 5 migrations and counting. |

Why not a simpler stack? I considered FastAPI (heavier than needed for this), MongoDB (document store doesn't help with relational analysis data), and Pinecone for embeddings (external service when pgVector runs in the same database). Each alternative added complexity without solving a problem the chosen stack couldn't handle.

## Architecture Layers

The app follows a three-layer pattern. Not because it's trendy -- because skills shouldn't know about database schemas, and analysis logic shouldn't be tangled with HTTP routing.

```
API Layer (Flask routes)
    |-- Skills API        -- Claude Code skill integration
    |-- Analysis API      -- Chapter and section analysis
    |-- Search API        -- Full-text and semantic search
    |-- Dashboard API     -- Metrics and progress tracking
    |-- Indexing API      -- Content re-indexing triggers
        |
Service Layer (Business logic)
    |-- Analysis Pipeline -- Multi-phase content analysis
    |-- Skills Service    -- Skill data formatting
    |-- Search Service    -- Query engine (text + vector)
    |-- Dashboard Service -- Metric aggregation
    |-- Embedding Service -- Vector operations
        |
Repository Layer (Data access)
    |-- Section, Research, Analysis repositories
    |-- Embedding, Link, Quote, Statistic repositories
        |
Database (PostgreSQL + pgVector)
```

**API layer** handles HTTP concerns: request parsing, response formatting, authentication (basic API key -- this runs on localhost, not production). Each API module maps to one skill or one UI view. A skill calls `/api/analysis/chapter/7` and gets back JSON. It never constructs a SQL query.

**Service layer** holds the logic. The analysis pipeline knows how to score voice consistency. The search service knows how to combine full-text and semantic results. The dashboard service knows how to weight 6 quality dimensions into a single chapter health score. None of this logic touches Flask or SQLAlchemy directly.

**Repository layer** abstracts data access. Each model gets a repository with standard operations: get, list, create, update, query by section, query by chapter. When we added the statistics table in migration 4, only the repository layer changed. Services and APIs didn't notice.

## Data Models

Ten models capture everything the system tracks:

| Model | Purpose | Key Fields |
|-------|---------|------------|
| **Section** | Manuscript content | chapter, section_num, title, content, word_count, content_hash |
| **Research** | Research files linked to sections | chapter, section, file_path, content, source_urls |
| **Embedding** | pgVector embeddings | section_id, vector (1536-dim), model_version |
| **Analysis** | Cached analysis results | section_id, dimension, score, details, draft_version |
| **Link** | Vault link graph | source_section, target, link_type, resolved |
| **Quote** | Extracted quotes with attribution | section_id, text, speaker, source, confidence |
| **Statistic** | Extracted stats with credibility | section_id, claim, value, source, credibility |
| **Metric** | Quality scores over time | chapter, dimension, score, timestamp, draft |
| **IndexMeta** | Indexing state | file_path, last_indexed, content_hash |
| **DraftComparison** | Cross-draft deltas | chapter, dimension, draft_from, draft_to, delta |

The relationships matter. A Section has many Analyses (one per dimension per draft). An Analysis belongs to one Section and one draft version. This lets you query "voice scores for chapter 7 across all 3 drafts" without joins that would make a NoSQL advocate cry.

## The 5 Migrations

Schema evolved as the system grew. Each migration solved a specific problem:

1. **Initial schema.** Sections, research, metrics. Enough to store content and track basic scores.
2. **Analysis cache.** Added the Analysis table with per-dimension, per-draft caching. Deep review support with cross-section comparisons.
3. **pgVector extension.** `CREATE EXTENSION vector;` Embedding table with 1536-dimensional vectors. Semantic search became possible.
4. **Statistics and quotes.** Structured extraction from research files. Credibility and confidence scoring for each data point.
5. **Indexing metadata.** File watcher state. Content hashes to detect changes without re-reading files. Last-indexed timestamps.

Alembic handles these cleanly. `alembic upgrade head` on a fresh database runs all 5 in order. On an existing database, it runs only what's new. No manual SQL, no "did I remember to add that column" anxiety.

## Why This Architecture

Three design principles drove these choices:

**Skills call the API, not the database.** A Claude Code skill shouldn't need to know that voice scores live in the `analysis` table with `dimension = 'voice'`. It calls `/api/analysis/voice/ch07-s03` and gets a score, violations, and suggestions. If the schema changes, the API contract doesn't.

**Analysis results are cached, not recomputed.** Running voice analysis across 81 sections takes minutes. Running it when a skill asks a question takes seconds -- because the result is already in the Analysis table, keyed by section, dimension, and draft. Re-analysis only happens when the content hash changes.

**Embeddings live alongside relational data.** pgVector means "find sections semantically similar to X" and "get citation density for chapter 7" are queries against the same database. No separate vector service to maintain, no data sync issues, no additional infrastructure.

The architecture is more than a writing project needs. It's exactly what an 81,000-word, 3-draft, 14-skill writing *system* needs.

---

**Deep dives:** [Analysis Pipeline](analysis-pipeline.md) | [Skill API Integration](skill-api-integration.md) | [When Scripts Aren't Enough](why-build-an-app.md)
