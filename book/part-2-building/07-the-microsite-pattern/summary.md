# Chapter Summary: The Microsite Pattern

## Key Takeaways

1. **Architecture follows organization, not the other way around:** 90% of microservices fail because teams create distributed complexity without distributed ownership. Uber consolidated 2,200 services into 70 domains with DOMA—cutting platform support costs 10x and feature integration time from three days to three hours.

2. **Standardize structure, accelerate everything:** Every microsite follows the same three-layer contract (controller, service, repository). Backstage templates and Cruft enforcement mean new microsites deploy in 15 minutes. The test: can a new engineer ship to production on day one?

3. **Centralize what's dangerous, distribute what benefits from autonomy:** Four things centralize (auth, permissions, observability, infrastructure). Five things belong to domain teams (business logic, API design, data models, UI/UX, deployment cadence). Netflix's Passport pattern terminates auth at the edge; Amazon's two-pizza teams own everything else.

4. **AI agents need tiered access, not blanket permissions:** The DIRECT/GATEWAY/EXCLUDE model ensures new endpoints default to invisible. MCP's 1,000+ connectors provide protocol-level security. Identity passthrough captures who requested what—when regulators ask what your AI did, you have the complete answer.

5. **Make the right thing easy and the wrong thing hard:** 63% of teams now produce APIs in less than a week through contract-first development. Breaking change detection via oasdiff fails builds automatically. Governance built into pipelines actually happens; governance documented in wikis doesn't.

---

Next: [Teams for AI-First Companies](../../part-3-operating/08-teams-for-ai-first-companies/README.md)

---

[← Previous: Governance Patterns](./08-governance-patterns.md) | [Chapter Overview](./README.md)
