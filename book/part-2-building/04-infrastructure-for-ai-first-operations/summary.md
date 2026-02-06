# Chapter Summary: Infrastructure for AI-First Operations

## Key Takeaways

1. **Start boring, add complexity when it hurts:** The Day 1 stack—Vercel, Supabase, direct API calls—costs under $500/month and gets you to production. Linear launched with three integrations. Notion hit one million users on seed funding. Infrastructure sophistication should lag revenue, not lead it.

2. **Postgres handles more than you think:** PostgreSQL with pgvector achieves 471 queries per second at 99% recall—11.4x better than dedicated vector databases on the same benchmark. Instacart pushed to 1 billion embeddings before reconsidering. The 5 million vector threshold is where most teams actually need specialized storage.

3. **Match autonomy to reversibility:** The three-tier access model—free, supervised, forbidden—isn't about limiting AI. It's about proportioning risk. The Postmark MCP attack compromised 1,500 users because tools lacked central oversight. 73% of enterprises experienced AI security breaches in 2024-2025.

4. **Agents need identity, not just API keys:** Non-human identities outnumber humans 50:1 in enterprise environments. Gartner predicts 25% of breaches will trace to AI agent abuse by 2028. OAuth 2.1 delegation chains ensure permissions flow down, never up—and every action traces to a human.

5. **Build what differentiates, buy everything else:** Linear built a custom sync engine because real-time collaboration IS their product. They buy managed PostgreSQL because databases aren't their moat. Self-hosting beats SaaS only around 80 million queries monthly. If you can't answer "yes" to two of three questions—differentiator, team capacity, scale certainty—buy.

---

Next: [Building with AI](../05-building-with-ai/README.md)

---

[← Previous: Build vs Buy for Infrastructure](./06-build-vs-buy-for-infrastructure.md) | [Chapter Overview](./README.md)
