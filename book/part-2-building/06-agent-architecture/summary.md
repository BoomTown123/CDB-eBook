# Chapter Summary: Agent Architecture

## Key Takeaways

1. **Two agent types, not one framework:** Chat agents optimize for speed and user satisfaction—Klarna's 2.3M monthly conversations, 11→2 minute response times. Background agents optimize for reliability and scale—running overnight, processing thousands of records unsupervised. The 5-question framework determines which: Does it need human judgment? Is someone waiting? Is it repetitive? Does it need volume? Is silent failure dangerous?

2. **Centralized control, distributed execution:** The Agent Hub pattern prevents the chaos of fifteen agents with conflicting permissions and scattered logs. Replit runs every agent session as a Temporal Workflow. Production benchmarks show p50 latency at 1,850ms, p95 at 4,200ms. Start with hub-as-control-plane—agents pull config, report telemetry, operate independently.

3. **Design for agents first, humans benefit too:** Four requirements humans forgive but agents don't—idempotency, structured responses, explicit error handling, programmatic authentication. AutoMCP's research showed 19 lines of fixes average took tool call success from 76.5% to 99.9%. Stripe extended idempotency keys to 30 days specifically for agent workflows.

4. **Seven failure modes, not traditional debugging:** Agents fail through hallucinated actions (Air Canada's $812 liability), scope creep (Chevrolet's $1 Tahoe), cascading failures (Replit's deleted production database), and resource exhaustion (73% of teams lack cost tracking, averaging 340% overruns). Build detection, prevention, recovery, and learning layers—in that order.

5. **Know when NOT to use agents:** 42% of companies abandoned AI initiatives in 2024. A Fortune 500 firm lost $4.2M on a support agent that passed internal testing but failed at scale. The ROI math: (Tasks x Time Saved x Rate) minus (Development + Operations + Compute + Risk). If marginal, start manual. Build agents when simpler approaches genuinely can't match the scale or reasoning required.

---

Next: [The Microservice Pattern](../07-the-microsite-pattern/README.md)

---

[← Previous: Agent Design Patterns](./06-agent-design-patterns.md) | [Chapter Overview](./README.md)
