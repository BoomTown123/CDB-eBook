# Chapter 9: Data Strategy — Flywheels, Moats, and Ethics — Resources

> Curated resources for deeper exploration of topics covered in this chapter.

## Frameworks from This Chapter

- [Data Flywheel](../../../frameworks/12-data-flywheel.md) — The 5-component flywheel (Collection, Storage, Analysis, Application, Feedback) and how to build self-reinforcing data loops that compound advantage.
- [Data Moats](../../../frameworks/13-data-moats.md) — The moat test framework for evaluating whether your data advantage is measured in days, months, or years of defensibility.
- [6 Data Strategy Mistakes](../../../frameworks/14-six-data-strategy-mistakes.md) — Six patterns that kill data flywheels, from building before product-market fit to platform risk and single-point dependencies.

## Tools & Platforms

- **PostgreSQL** — Recommended starting database for AI-first companies; Notion manages 200 billion blocks on sharded Postgres; OpenAI runs PostgreSQL as the backbone for ChatGPT (referenced in Section 4: Polyglot Persistence)
- **Redis** — Cache layer for speed-critical data like session state and rate limiting (referenced in Section 4: Polyglot Persistence)
- **Vector Databases** — Usage grew 377% in 2024 across enterprises per Databricks; stores embeddings for semantic search (referenced in Section 4: Polyglot Persistence)
- **LexisNexis** — Harvey's exclusive partnership for primary law databases and Shepard's Citations that competitors cannot obtain (referenced in Sections 1 and 3)
- **NVIDIA Data Flywheel Blueprint** — Achieved inference cost reductions up to 98.6% while maintaining comparable accuracy (referenced in Section 5: Privacy by Design)
- **Hugging Face HuggingChat** — Demonstrates consent-by-design approach; conversations remain private and are never used for training (referenced in Section 5: Privacy by Design)
- **Apple Differential Privacy** — Local differential privacy adding noise on-device before transmission; used for Genmoji improvements and QuickType suggestions (referenced in Section 5: Privacy by Design)
- **Duality Technologies** — Federated learning with embedded Privacy Enhancing Technologies including secure aggregation and configurable privacy-accuracy balances (referenced in Section 5: Privacy by Design)
- **Mistral AI** — All services run exclusively within the EU; refuses to train on customer data without explicit consent; open-source models enable data sovereignty (referenced in Section 5: Privacy by Design)

## Further Reading

- **Harvey's Cold Start Strategy** — How Harvey went from zero proprietary legal data in mid-2022 to $8B valuation and $100M ARR by designing a flywheel architecture before having data
- **IBM Watson Health Failure** — Over $4B invested, sold for approximately $1B; more data without a flywheel to compound it
- **Klarna's AI Playbook** — 48% revenue growth 2022-2024 while reducing operating expenses by 20%; AI contributed $40M in profitability gains in 2024, but customer service AI eventually plateaued
- **Spotify Data Architecture** — 1.4 trillion events daily from 678 million users; multi-task training improves podcast and music discovery; AI users show 40% higher retention and 140 min/day usage vs 99 min
- **Duolingo Birdbrain System** — AI estimates probability of correct answers in real-time; drove 59% DAU growth (21M to 34M users), 80%+ organic acquisition
- **Tesla FSD Data Collection** — 2M+ vehicles capture edge case clips automatically; earns $7K per vehicle as data collector vs Waymo's $150K per vehicle
- **Cursor Growth Trajectory** — Grew from $1M revenue in 2023 to $100M in 2024; Tab completion model achieved 28% higher accept rates with 21% fewer suggestions
- **Stitch Fix Recovery** — Hybrid AI-human model resulted in 40% increase in average order value, 40% more repeat purchases, 30% fewer returns

## Research & Data

- **AWS CDO Survey** — 93% of CDOs say data strategy matters for GenAI, yet 57% haven't made necessary changes
- **Appen State of AI Report 2024** — Data accuracy in the U.S. declined from 63.5% in 2021 to 26.6% in 2024; 48% identify data management as most significant obstacle
- **MIT NANDA Study** — 95% of enterprise AI pilots fail to reach production with measurable value
- **Nature: Model Collapse Research** — AI trained on AI-generated content degrades over time; models exhibit "narrower range of output over time" when trained recursively
- **DLA Piper GDPR Survey** — GDPR fines reached EUR 1.2 billion in 2024, up 38% from the previous year
- **CNIL Guidance 2025** — French regulator clarified that AI training on personal data from public sources can use legitimate interest but requires documentation before training begins
- **EU AI Act** — High-risk system compliance deadline: August 2, 2026; fines up to EUR 35 million or 7% of global revenue
- **AT&T/NVIDIA Case Study** — Fine-tuned models achieved 94% accuracy vs 78% for generic GPT-4 by activating existing customer service data
- **Perplexity Growth Data** — 312M queries (May 2024) to 1.4B (June 2025); DAU/MAU ratio of 53% far exceeds benchmarks
- **AI Startup Failure Analysis** — 92% failure rate within 18 months; 43% built products nobody wanted; 60-70% of AI wrappers generate zero revenue

## Community & Learning

- **GDPR Compliance Resources** — Key requirements for AI systems include legitimate processing basis, data protection impact assessments, transparency, and deletion rights
- **CCPA/CPRA (California)** — Expands "sharing" to include behavioral advertising; penalties reach $7,988 per intentional violation
- **Eight New U.S. State Privacy Laws (2025)** — Delaware, Iowa, Nebraska, New Hampshire, New Jersey, Tennessee, Minnesota, and Maryland
- **Hugging Face Model Cards** — Standardized documentation covering training datasets, performance metrics, known biases, and intended uses; serve as "boundary objects" accessible across disciplines

### Companies Referenced in This Chapter

Harvey, IBM (Watson Health), Spotify, Duolingo, Klarna, Tesla, Cursor, AT&T, Perplexity, Notion, Discord, OpenAI, Glean, fileAI, Stitch Fix, Mistral AI, Hugging Face, Apple, NVIDIA, Duality Technologies, DuckDuckGo, Yirifi, Waymo, Ghost Autonomy
