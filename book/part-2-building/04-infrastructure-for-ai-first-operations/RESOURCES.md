# Chapter 4: Infrastructure for AI-First Operations -- Resources

> Curated resources for deeper exploration of topics covered in this chapter.

## Frameworks from This Chapter

- [5 Infrastructure Mistakes That Kill AI Initiatives](../../../frameworks/08-five-infrastructure-mistakes.md) -- Over-engineering early, single points of failure, no observability, ignoring cost signals, and security as an afterthought.

## Tools & Platforms

### Day 1 Stack (Under $500/month)
- [Vercel](https://vercel.com/) -- Serverless deployment platform; auto-injects Supabase credentials and unifies billing.
- [Supabase](https://supabase.com/) -- Managed PostgreSQL with built-in auth, pgvector support, and real-time capabilities; 1.7 million developers.
- [Flask](https://flask.palletsprojects.com/) -- Python micro web framework; Yirifi's backend choice for all 15 microsites.
- [HTMX](https://htmx.org/) -- HTML-first frontend approach; no React or complex frontend frameworks required.

### Databases & Storage
- [PostgreSQL](https://www.postgresql.org/) -- Primary relational database; with pgvector achieves 471 QPS at 99% recall on 50M vectors.
- [pgvector](https://github.com/pgvector/pgvector) -- PostgreSQL extension for vector similarity search; 11.4x better than dedicated vector databases on benchmarks.
- [pgvectorscale](https://github.com/timescale/pgvectorscale) -- Enhanced pgvector performance from Timescale.
- [Redis](https://redis.io/) -- In-memory caching and session management; add when same data is read 10x+ per write.
- [Pinecone](https://www.pinecone.io/) -- Managed vector database; cost-effective at $100-200/month below 80M queries/month threshold.
- [Qdrant](https://qdrant.tech/) -- Open-source vector database for self-hosting at scale.
- [Milvus](https://milvus.io/) -- Open-source vector database designed for billion-scale similarity search.
- [Weaviate](https://weaviate.io/) -- Open-source vector database with built-in ML model integrations.
- [Neo4j](https://neo4j.com/) -- Graph database for relationship-heavy workloads (knowledge graphs, recommendation systems).
- [MongoDB](https://www.mongodb.com/) -- Document store for flexible schema requirements beyond PostgreSQL JSONB.
- [SQLite](https://www.sqlite.org/) -- Lightweight database; used by Yirifi for ontology knowledge graph.

### Security & Auth
- [Lasso Security MCP Gateway](https://www.lasso.security/) -- First open-source MCP security gateway; proxy and orchestrator embedding security filters across MCP servers.
- [Auth0 for AI Agents](https://auth0.com/blog/auth0-for-ai-agents-generally-available/) -- Agent-specific authentication flows from Okta/Auth0.
- [Microsoft Entra Agent ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id) -- Dedicated identity types for AI agents; same conditional access as human users.
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) -- De facto standard for agent-tool communication; adopted by Anthropic, OpenAI, Google, and Microsoft.

### Observability & Cost Tracking
- [Helicone](https://www.helicone.ai/) -- LLM observability with built-in caching (20-30% cost reduction); 50-80ms latency trade-off.
- [Langfuse](https://langfuse.com/) -- Open-source LLM observability platform.
- [LangSmith](https://smith.langchain.com/) -- LLM monitoring and evaluation from LangChain.
- [CloudZero](https://www.cloudzero.com/) -- AI cost tracking; research found only 51% of organizations can evaluate AI ROI.

## Further Reading

- [How Instacart Built Modern Search Infrastructure on Postgres](https://www.instacart.com/company/tech-innovation/how-instacart-built-a-modern-search-infrastructure-on-postgres) -- Pushed pgvector to 1 billion embeddings; 6% drop in zero-result searches after migration from FAISS.
- [Linear's Custom Sync Engine](https://www.fujimon.com/blog/linear-sync-engine) -- Why Linear built custom sync (competitive advantage) but buys managed PostgreSQL (commodity).
- [Advanced Authentication and Authorization for MCP Gateway (Red Hat)](https://developers.redhat.com/articles/2025/12/12/advanced-authentication-authorization-mcp-gateway) -- The `x-authorized-tools` JWT wristband pattern for gateway enforcement.
- [MCP First Anniversary](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) -- History and evolution of the Model Context Protocol standard.
- [Claude Code Documentation](https://code.claude.com/docs/en/overview) -- Claude Code as both MCP client and server; headless mode for CI/CD automation.
- [The Complete Guide to LLM Observability Platforms](https://www.helicone.ai/blog/the-complete-guide-to-LLM-observability-platforms) -- LLM observability market projected from $1.4B (2023) to $10.7B (2033).
- [Notion: Building a Scalable AI Feature Evaluation System](https://www.zenml.io/llmops-database/building-a-scalable-ai-feature-evaluation-system) -- Notion's hundreds of evaluation datasets with LLM-as-judge scoring.

## Research & Data

- [MIT Study: 95% of GenAI Pilots Fail](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/) -- $30-40 billion invested in 2024 pilots; infrastructure decisions killed good ideas before shipping.
- [Adversa AI: 2025 AI Security Incidents Report](https://www.prnewswire.com/news-releases/adversa-ai-unveils-explosive-2025-ai-security-incidents-reportrevealing-how-generative-and-agentic-ai-are-already-under-attack-302517767.html) -- 73% of enterprises experienced AI-related security breaches; $4.8M average incident cost.
- [Cloud Security Alliance: Agentic AI Identity and Access Management](https://cloudsecurityalliance.org/artifacts/agentic-ai-identity-and-access-management-a-new-approach) -- Non-human identities outnumber humans 50:1 in enterprise environments.
- [Gartner Prediction: 25% of Breaches from AI Agent Abuse by 2028](https://www.strata.io/blog/agentic-identity/new-identity-playbook-ai-agents-not-nhi-8b/) -- Via Strata Identity analysis.
- [CloudZero State of AI Costs 2025](https://www.cloudzero.com/state-of-ai-costs/) -- Average monthly AI spend jumped from $62,964 to $85,521 (36% YoY); 45% of companies spending $100K+/month.
- [pgvector vs Qdrant Benchmarks (Tigerdata)](https://www.tigerdata.com/blog/pgvector-vs-qdrant) -- pgvectorscale achieving 471 QPS at 99% recall on 50M vectors.
- [OAuth Token Exchange RFC 8693](https://self-issued.info/docs/draft-ietf-oauth-token-exchange-10.html) -- Delegation chain specification for agent-to-agent permission passing.
- [DPoP (Demonstration of Proof-of-Possession)](https://curity.io/resources/learn/dpop-overview/) -- Cryptographic proof preventing stolen token reuse.
- [Global Market Insights: Vector Database Market](https://www.gminsights.com/industry-analysis/vector-database-market) -- Vector database market reached $2.2B in 2024.

## Community & Learning

- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/draft/basic/authorization) -- Official MCP spec including OAuth 2.1 authorization.
- [GitHub Actions: Claude Code Action](https://github.com/anthropics/claude-code-action) -- Mention `@claude` in PRs/issues to trigger AI analysis with gateway controls.
- [Supabase Auth: Build vs Buy](https://supabase.com/blog/supabase-auth-build-vs-buy) -- Analysis of authentication build vs buy economics.

### Infrastructure Decision Thresholds

| Component | Buy Threshold | Build/Self-Host Threshold |
|-----------|---------------|---------------------------|
| Vector Database | < 80M queries/month | > 80-100M queries/month |
| AI Gateway | < $10K/month LLM spend | > $10K/month LLM spend |
| Authentication | Always buy (security risk) | Only delegation logic custom |
| Observability | < 50K events/month | > 50K events/month with DevOps capacity |
| General AI Infra | Pre-product-market fit | Scale stage (18+ months) |
