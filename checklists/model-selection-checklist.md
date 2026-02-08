# Checklist: Model Selection

> Choosing the right AI model for your use case, constraints, and business reality.

Use this checklist before evaluating any model. Gather your technical and business stakeholders, answer every question in sequence, and document your answers. Each section eliminates options -- by the end, your realistic choices should narrow to two or three candidates you can test against actual workloads. Revisit quarterly as the landscape shifts.

*Derived from the [6 Questions Before Choosing a Model](../frameworks/07-six-questions-before-choosing-a-model.md) and [Foundation Models Landscape](../frameworks/06-foundation-models.md) frameworks -- Chapter 3.*

---

## Use Case Definition

- [ ] Described the specific job you are hiring AI to do in **one sentence** (if you can't, you aren't ready to evaluate models)
- [ ] Classified the task complexity: simple classification/extraction (doesn't need a frontier model) vs. multi-step reasoning or complex generation (requires frontier capabilities)
- [ ] Identified the primary capability required: code generation, analytical reasoning, creative synthesis, vision/multimodal, long-document processing, or video analysis
- [ ] Matched capability to model strengths: Claude for code and analytical reasoning, GPT for creative synthesis and vision, Gemini for video and long-context, DeepSeek for budget workloads with security controls
- [ ] Documented the known **failure modes** that matter for your use case: chaotic people-pleaser (GPT), repetitive patterns (Gemini), over-caution (Claude), security vulnerabilities (DeepSeek)
- [ ] Confirmed the use case is specific enough to benchmark -- not a vague "add AI to our product" directive

## Latency Requirements

- [ ] Defined your **latency tier**: sub-second (real-time voice, fraud detection), 1-3 seconds (chatbots, search), 3-10 seconds (internal tools), or minutes+ (batch processing)
- [ ] Verified that candidate models can meet your latency threshold (e.g., Mistral Large leads time-to-first-token at 0.30s; ChatGPT o1 averages 60.6s -- a 200x difference)
- [ ] Eliminated any models that can't meet your latency requirements regardless of other capabilities
- [ ] For real-time use cases, confirmed that **latency trumps marginal capability improvements** in your evaluation criteria
- [ ] Tested latency under realistic load conditions, not just single-query benchmarks

## Compliance Assessment

- [ ] Identified all regulatory frameworks that apply: HIPAA (healthcare), SOX/financial regulations, FedRAMP (government), GDPR/CCPA (data privacy), industry-specific requirements
- [ ] For regulated industries, treated compliance as the **first** elimination filter before all other considerations
- [ ] Verified that candidate models and providers offer the required compliance certifications (e.g., FedRAMP High authorization, Business Associate Agreements)
- [ ] Assessed whether data residency requirements mandate **self-hosted or on-premises** deployment (eliminates most cloud-only API providers)
- [ ] Evaluated whether open-weight models (Llama, Mistral, self-hosted DeepSeek) are required for full data control in strict jurisdictions
- [ ] Confirmed that using models with known security vulnerabilities (e.g., DeepSeek's 100% jailbreak success rate in testing) includes a plan for mitigating controls before deployment

## Cost Analysis

- [ ] Estimated your **query volume**: under 1,000/day (cost is rounding error), or 1M+/day (cost is existential)
- [ ] Evaluated the three pricing models against your volume: per-query (low/unpredictable volume), committed capacity (40-80% discounts at high volume), or self-hosted (high upfront, near-zero marginal)
- [ ] Calculated your annual token spend and compared against the **cost break-even thresholds**: under $50K/year favors APIs, $50K-$500K favors hybrid, above $500K favors self-hosting
- [ ] Accounted for the full cost spectrum: premium tier (Claude Opus at $15/$75 per million tokens), mid tier (GPT/Gemini Pro ~64% cheaper), budget tier (DeepSeek as low as $0.07/M tokens cached)
- [ ] For self-hosting, factored in the **$150K+ annual overhead** for engineering talent and operations on top of compute costs
- [ ] Built a cost model that projects 12 months forward based on expected growth in query volume

## Explainability Requirements

- [ ] Determined whether your use case requires knowing **why** the AI reached a conclusion, not just what it concluded
- [ ] For financial services: confirmed the model can produce audit trails that satisfy regulators
- [ ] For healthcare: confirmed the model supports documentation sufficient for clinical risk analysis
- [ ] For legal: confirmed the model can cite sources and ground responses in reference documents
- [ ] Evaluated whether candidate model architectures support traceability -- some architectures make explainability nearly impossible
- [ ] Decided whether explainability is a **hard filter** (eliminating models that can't provide it) or a soft preference

## Vendor Strategy

- [ ] Assessed your **switching tolerance**: if you choose wrong, how painful is it to change providers?
- [ ] Identified potential lock-in vectors: interface lock-in (workflow configurations, prompt libraries embedded in platforms) and organizational friction (user retraining, trust rebuilding)
- [ ] Pre-defined **migration triggers**: what price increase, performance degradation, or security incident justifies switching? Document these now, not under pressure later
- [ ] Evaluated a **multi-model strategy**: 37% of enterprises already support hybrid approaches because no single model meets all requirements
- [ ] Built or planned **routing infrastructure** and abstraction layers that allow adding or swapping models without rewriting your application
- [ ] Considered the startup vs. enterprise path: startups should start with closed APIs and optimize later; enterprises should plan for multi-model from day one
- [ ] Scheduled **quarterly re-evaluation** of model selection -- the model that was right six months ago may not be right today

---

**Next step:** With all six sections answered, your candidate list should be two or three models. Run those candidates against your actual workloads -- not generic benchmarks -- and make a decision based on production performance. Document your selection rationale so you can revisit it at the next quarterly review.
