# Checklist: AI Readiness Assessment

> Is your company ready to go AI-first?

Use this checklist before committing to an AI-first transformation. Work through each category with your leadership team to identify gaps and blockers. Items left unchecked represent areas that need investment before -- or during -- the transition. Not every box must be checked to start, but you should have a plan for each unchecked item.

*Derived from the [AI-First vs AI-Enabled](../frameworks/ai-first-vs-ai-enabled.md) and [7 Mental Models of AI-First](../frameworks/7-mental-models-of-ai-first.md) frameworks -- Chapters 1 and 2.*

---

## Strategic Readiness

- [ ] Applied the **Kill Test**: you can articulate whether removing AI would eliminate your product or merely degrade a feature
- [ ] Determined whether you are building **AI-first** (AI is the product) or **AI-enabled** (AI enhances an existing product) -- and committed to one approach
- [ ] Defined your AI value proposition in one sentence that doesn't include the word "also"
- [ ] Assessed whether your pricing reflects AI as core value (consumption-based or hybrid) rather than a premium add-on
- [ ] Identified which of the **5 signs of AI-first** apply to your company: founded after modern AI, data-driven architecture, distributed AI expertise, AI-core pricing, "built on" positioning
- [ ] Evaluated whether AI-enabled is actually the better choice for your context (large incumbent, heavily regulated, hardware-first, or human-judgment product)
- [ ] Established a quarterly re-evaluation cadence for your AI strategy as the landscape shifts

## Technical Readiness

- [ ] Adopted an **agent-first design** posture: APIs are structured for AI consumers with explicit error handling and structured responses, not just human-operated interfaces
- [ ] Designed systems for **probabilistic outputs**: confidence levels are surfaced, not hidden -- uncertainty is treated as a feature
- [ ] Built or planned **abstraction layers** that allow swapping models without rewriting applications
- [ ] Evaluated the **build vs. buy inversion**: checked whether building with foundation models is faster than procuring, integrating, and customizing vendor solutions
- [ ] Established infrastructure for **compound iteration**: automated evaluations, fast feedback loops, and regression test suites for AI outputs
- [ ] Defined a **permission spectrum** for AI autonomy: low-stakes actions run autonomously, high-stakes actions require human approval

## Organizational Readiness

- [ ] AI expertise is **distributed across teams**, not siloed in a single "AI/ML team"
- [ ] Leadership understands the distinction between AI-first and AI-enabled at the strategic level
- [ ] Product, engineering, and business stakeholders are aligned on which approach you are pursuing
- [ ] Team structure supports rapid iteration (hours-to-days cycles, not quarterly sprints) for AI features
- [ ] Roles are defined around **human-AI collaboration**: AI handles execution ("how"), humans provide judgment, taste, and direction
- [ ] A plan exists for retraining and upskilling existing staff rather than only hiring new AI talent

## Data Readiness

- [ ] Identified whether your **data architecture drives the product** (AI-first) or merely supports features (AI-enabled)
- [ ] Product interactions are structured to naturally generate **training signals** -- usage data is treated as a product, not a byproduct
- [ ] A **data flywheel** is designed or planned: more users generate more data, more data improves the product, a better product attracts more users
- [ ] Data freshness requirements are defined for all critical data sources
- [ ] Data is accessible across departments rather than fragmented in silos
- [ ] Data pipelines exist (or are planned) that can feed continuous model improvement without manual intervention

## Cultural Readiness

- [ ] The organization treats AI outputs as **probabilistic** rather than expecting deterministic perfection
- [ ] Teams are comfortable shipping AI features that are "good enough" and iterating, rather than waiting for 100% accuracy
- [ ] There is organizational tolerance for the **risk profile** of AI-first: model failure means business failure, not just feature degradation
- [ ] Marketing and communication use "built on AI" language rather than "now with AI" -- the framing reflects genuine commitment
- [ ] Post-incident analysis is standard practice: every AI failure is treated as a **training example**, not a blame event
- [ ] The company designs for **augmentation, not replacement** -- AI tools make people more capable rather than surveilling or displacing them

---

**Next step:** For items you checked, validate with specific evidence. For items you left unchecked, assign an owner and a target date. Revisit this assessment quarterly.
