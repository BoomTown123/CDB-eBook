# Workflow: Model Evaluation and Selection

> A step-by-step workflow for evaluating and selecting AI models using business constraints as elimination criteria --- not benchmark hype.

*Based on the [6 Questions Before Choosing a Model](../frameworks/07-six-questions-before-choosing-a-model.md) framework --- Chapter 3*

## When to Use This Workflow

- Before selecting a model for a new AI feature or product
- When evaluating whether to switch from your current model provider
- During quarterly re-evaluation of existing model choices
- When a team proposes adopting a new model based on benchmarks or demos

## Time to Complete

2--4 hours for the initial pass with stakeholders. An additional 1--2 weeks for production testing of shortlisted candidates.

## The Workflow

### Phase 1: Define Constraints (60--90 minutes)

Gather technical and business stakeholders. Answer all six questions in sequence. Each question eliminates options.

**Step 1: Define the use case in one sentence.** If you can't, stop --- you aren't ready. Simple classification doesn't need a frontier model. Multi-step reasoning requires frontier territory.

> **Decision point:** Frontier capabilities or mid-tier/budget? This eliminates half your candidates and can reduce costs by 10--200x.

**Step 2: Define your latency tier.**

| Tier | Latency | Implication |
|------|---------|-------------|
| Real-time | Sub-second | Eliminates most frontier models |
| Interactive | 1--3 seconds | Optimize for time-to-first-token |
| Internal | 3--10 seconds | Capability matters more than speed |
| Batch | Minutes+ | Cost per query matters most |

> **Decision point:** Eliminate any model that can't meet your threshold. Cost per million tokens varies by 200x across models.

**Step 3: Identify compliance requirements.** Healthcare requires HIPAA and BAAs. Financial services requires explainability. Government requires FedRAMP. Data residency may mandate self-hosted deployment.

> **Decision point:** Which models remain after compliance filtering?

**Step 4: Model the cost structure.** Under $50K annual token spend: APIs. $50K--$500K: hybrid. Above $500K: self-hosting (add $150K+ for engineering overhead). *[Supplementary guidance --- specific thresholds not from the book]*

> **Decision point:** Does volume eliminate any pricing model?

**Step 5: Assess explainability needs.** If your use case requires knowing why the AI reached a conclusion, this is a filter, not a preference.

**Step 6: Evaluate switching tolerance.** 42% of AI initiatives are abandoned before production, with vendor lock-in as a primary driver. Pre-define migration triggers now.

> **Decision point:** Multi-model routing from day one, or single provider with abstraction later?

### Phase 2: Shortlist and Test (1--2 weeks)

**Step 7:** Assemble 50--100 representative queries from your actual use case. Include edge cases. Define success criteria.

**Step 8:** Test each candidate with identical inputs. Measure accuracy, latency (p50/p95/p99), cost per query, and failure rate under realistic load.

**Step 9:** Weight criteria based on Phase 1 answers. Make the decision. Document rationale. Schedule quarterly re-evaluation.

### Phase 3: Implement with Exit Criteria

**Step 10:** Build an abstraction layer that allows swapping models without rewriting your application.

**Step 11:** Set alerts for latency degradation, accuracy drift, and cost spikes. Document exit criteria. Schedule quarterly reviews.

---

## Related Resources

- [Model Selection Checklist](../checklists/model-selection-checklist.md) --- The checkbox version for quick audits
- [6 Questions Before Choosing a Model](../frameworks/07-six-questions-before-choosing-a-model.md) --- The framework this workflow implements
- [Foundation Models Landscape](../frameworks/06-foundation-models.md) --- Understanding the models you are choosing between
- [Build vs Buy Calculus](../frameworks/04-build-vs-buy-calculus.md) --- Related decision framework for infrastructure

**Full chapter:** [Chapter 3: The AI Landscape](../book/part-1-foundations/03-the-ai-landscape/README.md)
