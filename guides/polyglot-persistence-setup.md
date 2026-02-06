# Guide: Setting Up Polyglot Persistence

> A step-by-step guide to implementing a multi-database architecture where each workload runs on the database best suited for it --- without over-engineering from day one.

*Based on [Chapter 4: Infrastructure](../book/part-2-building/04-infrastructure-for-ai-first-operations/README.md) and [Chapter 9: Data Strategy](../book/part-3-operating/09-data-strategy/README.md)*

## What You'll Build

A polyglot persistence layer that matches each data type to the right database engine. By the end of this guide, you will have:

- A clear map of which data belongs in which database type
- A phased rollout plan that starts simple and adds complexity only when measured problems demand it
- Connection patterns that let your application talk to multiple databases cleanly
- A decision framework for when to add the next database to your stack

## Prerequisites

- A running PostgreSQL instance (this is your starting point for everything)
- A production application with real user traffic (or an imminent launch)
- Basic understanding of your data access patterns --- what gets read most, what gets written most, what needs to be fast
- Familiarity with your compliance requirements (some database choices have regulatory implications)

## Step 1: Audit Your Current Data Landscape

Before adding any database, you need to understand what you already have. Map every data type in your system against these five questions:

| Question | If Yes | Database Type |
|----------|--------|---------------|
| Does this data require ACID transactions? | Relational (PostgreSQL) | User accounts, billing, audit logs |
| Does the schema change frequently? | Document store (MongoDB, DynamoDB) | Agent conversations, JSON API responses |
| Is read latency critical (< 10ms)? | Cache layer (Redis, Memcached) | Session state, rate limiting, hot keys |
| Do you need semantic or similarity search? | Vector database (Pinecone, Weaviate, Qdrant) | Embeddings for RAG, recommendation features |
| Is this analytics, not operations? | Data warehouse (BigQuery, Snowflake) | Reporting queries, dashboards, ML training |

Most teams discover that 80% or more of their data belongs in a relational database. That is fine. The point of polyglot persistence isn't to use every database type --- it is to add the right one at the right time.

## Step 2: Start with PostgreSQL for Everything

This isn't a compromise. This is the correct starting point.

Notion manages 200 billion block entities on sharded PostgreSQL. OpenAI runs PostgreSQL as the backbone for ChatGPT. When OpenAI needed to handle read-heavy workloads at scale, they didn't replace Postgres --- they optimized it with read replicas and PgBouncer, reducing latency from 50ms to under 5ms.

For your first six months (at minimum):

1. **Put all transactional data in PostgreSQL.** User accounts, billing records, application state, configuration --- everything.
2. **Optimize before adding complexity.** Proper indexing, connection pooling (PgBouncer or PgPool), read replicas for heavy read workloads.
3. **Measure actual bottlenecks.** Do not guess. Use query analysis tools (`EXPLAIN ANALYZE`) to identify what is actually slow.
4. **Resist the urge to add a second database** unless you have a measured problem that PostgreSQL can't solve with tuning.

## Step 3: Add a Cache Layer When Latency Becomes Measurable

The first database you will likely add is Redis (or a comparable in-memory cache). The trigger: you have specific data that needs sub-10ms reads and your PostgreSQL queries can't deliver that consistently under load.

**What goes in the cache:**
- Session state and authentication tokens
- Rate limiting counters
- Frequently accessed configuration values
- Results of expensive queries that change infrequently

**What doesn't go in the cache:**
- Anything that requires durability guarantees
- Data that changes on every request (the cache invalidation overhead negates the benefit)
- Entire database tables "just in case"

**Implementation pattern:**
1. Identify the 3--5 hottest keys in your system (the data read most frequently)
2. Add Redis alongside PostgreSQL --- not as a replacement
3. Implement a read-through cache: check Redis first, fall back to PostgreSQL, populate Redis on miss
4. Set TTLs (time-to-live) that match your consistency requirements --- shorter for fast-changing data, longer for stable reference data
5. Monitor cache hit rates --- if they are below 80%, your cache strategy needs adjustment

## Step 4: Add a Document Store When Schema Flexibility Blocks Iteration

The trigger here is specific: you have a data type whose schema changes faster than your deployment cycle, and those schema migrations are slowing your team down.

Common candidates for document stores:
- **Agent conversation histories** --- variable structure depending on tools used, context windows, and interaction patterns
- **JSON-heavy API responses** --- especially when you are integrating with third-party systems whose schemas you don't control
- **User-generated content with variable fields** --- forms, surveys, or configuration objects where each record may have different attributes

**Key decisions:**
- **MongoDB** when you need flexible querying across document fields and your team has relational database experience (the learning curve is gentler)
- **DynamoDB** when you need predictable performance at any scale and your access patterns are well-defined (key-value or key-document lookups)

**Warning:** Do not use a document store because "flexibility sounds good." Flexibility without structure becomes chaos. If you haven't thought through your data model, the answer is to think harder about the model, not to use a schemaless database.

## Step 5: Add a Vector Database When AI Features Require Embeddings

This is usually the first genuinely new capability you add --- not a performance optimization, but a new kind of query that relational databases can't serve efficiently.

Vector database usage grew 377% in 2024 across enterprises. The trigger for adding one is straightforward: your product needs semantic search, similarity matching, or RAG (retrieval-augmented generation).

**Choosing a vector database:**
- **Pinecone** --- managed service, lowest operational overhead, sub-10ms latency at scale. Notion uses Pinecone to power semantic search across billions of embeddings.
- **Weaviate** --- open source, supports hybrid search (vector + keyword), good for teams that want more control
- **Qdrant** --- open source, Rust-based, strong performance characteristics for self-hosted deployments
- **pgvector** --- a PostgreSQL extension. If your embedding volumes are modest (under a few million vectors), this lets you avoid adding another database entirely. Try this first.

**Implementation sequence:**
1. Start with pgvector if your embedding count is under 2--3 million. This avoids adding infrastructure.
2. If query latency or scale exceeds pgvector's capabilities, migrate to a dedicated vector database.
3. Build your embedding pipeline: generate embeddings at write time, store them in the vector database, query at read time.
4. Implement hybrid search where relevant --- Perplexity AI uses Vespa to combine vector search, lexical search, and BM25 in a single system for their 400 million monthly queries.

## Step 6: Add a Data Warehouse When Analytics Queries Impact Production

The final trigger: your analytical queries (reports, dashboards, ML training jobs) are slowing down your operational database. This typically happens when you have enough data that aggregate queries scan millions of rows.

**The separation principle:** Operational workloads (fast reads and writes for your application) and analytical workloads (complex aggregations across large datasets) have fundamentally different performance profiles. Running them on the same database forces trade-offs that hurt both.

Notion discovered this firsthand. Their update-heavy workload (90% updates vs. inserts) made traditional data warehouses expensive. They built a data lake with Kafka CDC to Hudi to S3, achieving over a million dollars in annual savings while reducing ingestion time from days to minutes.

**Implementation steps:**
1. Set up change data capture (CDC) from your operational database to your analytics layer
2. Choose a destination: a managed data warehouse (BigQuery, Snowflake, Redshift) for SQL-friendly analytics, or a data lake (S3 + query engine) for more flexible processing
3. Establish a clear data freshness SLA --- how stale can analytics data be before it is a problem?
4. Route all reporting and ML training queries to the analytics layer, never to the production database

## Key Decisions Summary

| Decision Point | Recommended Path | Anti-Pattern to Avoid |
|----------------|------------------|----------------------|
| Starting architecture | PostgreSQL for everything | Spinning up 4+ databases before launch |
| When to add caching | Measured latency problems under load | "Pre-optimizing" with Redis on day one |
| When to add documents | Schema changes blocking deploys | Using document stores because "NoSQL scales" |
| When to add vectors | AI features requiring embeddings | Adding a vector DB without AI use cases |
| When to add analytics | Reporting queries hurting production | Running dashboards against production DB |

The goal isn't architectural elegance. The goal is a data architecture that accelerates your product without creating operational overhead that slows everything else down. Add complexity when you have measured problems, not imagined ones.

---

## Related Resources

- [Data Strategy Checklist](../checklists/data-strategy-checklist.md) --- Audit your data strategy across collection, quality, flywheel design, moats, and governance
- [Building Data Flywheels](../frameworks/data-flywheel.md) --- How your persistence layer feeds self-reinforcing data loops
- [Data Moats](../frameworks/data-moats.md) --- Assessing whether your data architecture creates defensible advantage
- [5 Infrastructure Mistakes](../frameworks/5-infrastructure-mistakes.md) --- Common infrastructure failures to avoid as you scale

**Full chapters:** [Chapter 4: Infrastructure](../book/part-2-building/04-infrastructure-for-ai-first-operations/README.md) | [Chapter 9: Data Strategy](../book/part-3-operating/09-data-strategy/README.md)
