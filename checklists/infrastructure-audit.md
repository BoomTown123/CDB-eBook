# Checklist: AI Infrastructure Audit

Use this checklist when evaluating your current AI infrastructure before scaling, after a production incident, or during quarterly architecture reviews. It translates the five infrastructure failure patterns from Chapter 4 into concrete items you can verify, supplemented with checks for observability, cost management, security, and reliability.

## Architecture Review

### Mistake 1: Over-Engineering Early

- [ ] Every infrastructure component maps to a specific, current problem (not a future "we'll need it when we scale" scenario)
- [ ] You are using off-the-shelf solutions where they meet your needs at current scale
- [ ] No custom-built systems exist for problems that managed services already solve
- [ ] Your team can ship an AI feature in days, not months of infrastructure setup
- [ ] Infrastructure costs are proportional to the value being delivered today
- [ ] You haven't built multi-region or multi-cluster deployments before validating in a single market

### Mistake 2: Single Points of Failure

- [ ] You can name your fallback plan if your primary AI provider goes down for 4+ hours
- [ ] Every AI feature has a defined degradation mode (e.g., chat agents fall back to simpler models)
- [ ] Critical paths have at least one alternative provider configured
- [ ] An abstraction layer exists that allows swapping providers in hours, not weeks
- [ ] Failover paths are tested at least quarterly
- [ ] No single cloud provider or datacenter failure can take down your entire AI capability

### Mistake 3: No Observability

- [ ] You can answer "why did this AI request fail?" for any request in the past 24 hours
- [ ] Structured logging is in place for every AI call from day one
- [ ] You can distinguish AI errors from system errors in your logs
- [ ] AI output quality is tracked with measurable metrics, not anecdotal reports
- [ ] You know this week's AI costs by feature without opening a spreadsheet

### Mistake 4: Ignoring Cost Signals

- [ ] Cost alerts are configured at 50%, 80%, and 100% of daily budgets
- [ ] Weekly cost reviews are scheduled and happening
- [ ] Every AI feature has an assigned cost target
- [ ] Per-feature cost attribution is in place so you know which capabilities are burning cash
- [ ] You find out about cost spikes within hours, not at month-end
- [ ] You have modeled how costs change at 2x, 5x, and 10x current usage

### Mistake 5: Security as an Afterthought

- [ ] A compromised agent credential can't cause a production data breach
- [ ] Each AI agent runs under its own service account with least-privilege permissions
- [ ] System prompts and administrative controls have change logging and audit trails
- [ ] Environment isolation separates development, staging, and production AI systems
- [ ] Agent permissions go through the same approval process as human access requests
- [ ] Quarterly access reviews are scheduled for all AI service accounts

## Observability

- [ ] Latency, throughput, and error rates are tracked per AI endpoint
- [ ] Token usage and model response times are logged per request
- [ ] Dashboards exist showing AI system health at a glance
- [ ] Alerts fire automatically when AI output quality degrades beyond defined thresholds
- [ ] Log retention policies are defined and meet your compliance requirements
- [ ] You can trace an end-user request through every AI component it touches

## Cost Management

- [ ] Monthly AI spend is tracked and trended over at least the past 3 months
- [ ] You know your cost-per-inference for each model and feature
- [ ] Budget forecasts account for non-linear cost scaling at usage thresholds
- [ ] Unused or underutilized AI resources are identified and reviewed monthly
- [ ] Model selection decisions include cost analysis, not just performance benchmarks
- [ ] You have a defined process for what happens when a feature exceeds its cost target

## Security

- [ ] AI inputs are validated and sanitized to prevent prompt injection
- [ ] PII and sensitive data are masked or excluded from AI model inputs where required
- [ ] AI outputs are checked before being presented to users in sensitive contexts
- [ ] Network segmentation isolates AI inference services from core data stores
- [ ] Third-party AI provider data handling agreements are reviewed and signed
- [ ] Incident response procedures exist specifically for AI-related security events

## Reliability

- [ ] SLAs are defined for AI-powered features (latency, availability, accuracy)
- [ ] Rate limiting and circuit breakers protect AI endpoints from cascading failures
- [ ] Graceful degradation paths are documented and tested for each AI feature
- [ ] Recovery time objectives (RTO) are defined for AI system outages
- [ ] Load testing has been performed at expected peak traffic levels
- [ ] Rollback procedures exist for AI model updates and configuration changes

---

**Source framework:** [The 5 Infrastructure Mistakes That Kill AI Initiatives](../frameworks/08-five-infrastructure-mistakes.md)

**Full chapter:** [Chapter 4: Infrastructure for AI-First Operations](../book/part-2-building/04-infrastructure-for-ai-first-operations/README.md)
