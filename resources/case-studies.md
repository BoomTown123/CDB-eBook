# Case Studies

> Companies and case studies referenced in *Blueprint for an AI-First Company*, organized by category. Each entry includes what the book discusses and which chapters reference them.

---

## AI-First Companies

Companies built from the ground up with AI at their core. If you remove the AI, the product doesn't exist. Central examples in Chapter 1 (The AI-First Imperative) and the [AI-First vs AI-Enabled](../frameworks/ai-first-vs-ai-enabled.md) framework.

| Company | What the Book Discusses | Chapters / Frameworks |
|---------|------------------------|----------------------|
| **Harvey** | Legal AI platform that reached $8B valuation and $100M ARR. Uses "citation-first output" with 74% answer quality on BigLaw Bench. Expert seeding strategy -- hired lawyers from major firms to define workflows. LexisNexis partnership for exclusive content. Compliance-native architecture anticipating EU AI Act, ABA 2024, UK SRA standards. | Ch 1 (AI-First Imperative), Ch 2 (Mindset), Ch 9 (Data Strategy), Ch 11 (Ethics & Governance) |
| **Glean** | Enterprise knowledge platform with $7.2B valuation and $100M+ ARR. Knowledge graph takes 12-18 months to mature. Integration depth across enterprise data sources creates switching costs. $30/month per user, claims 2-4 hours per week savings. | Ch 1 (AI-First Imperative), Ch 9 (Data Strategy) |
| **Perplexity** | AI-native search. 312M queries in May 2024, 780M by May 2025, growing to 1.4B by June 2025. DAU/MAU ratio of 53% far exceeds benchmarks. Network learning effect -- each query improves accuracy for future queries. Demonstrates cold start breakthrough via network effects. | Ch 1 (AI-First Imperative), Ch 9 (Data Strategy) |
| **Midjourney** | AI image generation. Launched 2022 with 11 employees, hit $200M annual revenue by 2023. No separate "AI team" -- the entire company is the AI team. Example of AI expertise distributed throughout the organization. | Ch 1 (AI-First Imperative) |
| **Cursor** | AI-first code editor. Revenue grew from $1M (2023) to $100M (2024), projected $200M in 2025. Implements explicit PermissionOptions with allowlists, denylists, and "YOLO mode." Tab completion model achieved 28% higher accept rates with 21% fewer suggestions. OpenAI engineering teams adopted it. | Ch 1, Ch 2 (Mindset), Ch 5 (Building with AI), Ch 9 (Data Strategy) |
| **Mistral** | European AI lab. Founded 2023, reached $6B valuation within 18 months. Fastest time-to-first-token at 0.30 seconds. Offers both open-weight and commercial models. | Ch 1, Ch 3 (AI Landscape) |

---

## AI-Enabled Companies

Established companies that added AI capabilities to existing products. The core product survives without AI, but AI makes it significantly better.

| Company | What the Book Discusses | Chapters / Frameworks |
|---------|------------------------|----------------------|
| **Salesforce** | Marketing says "Now the world's number one generative AI CRM" -- classic AI-enabled positioning. Agentforce platform allows banking agents to retrieve transactions autonomously but requires human approval for credits and merchant notifications. Built CRM since 1999. | Ch 1, Ch 11 (Ethics & Governance) |
| **Notion** | Turn off Notion AI and the workspace still functions for notes, docs, and wikis. Product existed since 2016. AI priced as $10/month add-on per member. Example of AI as enhancement, not foundation. | Ch 1 (AI-First Imperative) |
| **Adobe** | Describes designers becoming "creative directors for an incredibly fast, versatile, but literal-minded AI assistant." Illustrates the Creative Director Model for human-AI collaboration. | Ch 2 (Mindset) |
| **Shopify** | CEO Tobi Lutke issued mandatory AI policy in April 2025 -- before requesting headcount, demonstrate why AI can't handle the task. Runs 40-60M LLaVA inferences daily using fine-tuned open models. | Ch 2 (Mindset), Ch 3 (AI Landscape) |
| **Canva** | Magic Studio serves 220M+ monthly users. Magic Write feature saw 8B uses since launch. Demonstrates the compound iteration mental model -- multiplication effect of AI across a large user base. | Ch 2 (Mindset) |
| **Grammarly** | Shows multiple suggestions instead of one "right answer." Targets 95% user-generated accuracy. 10 suggestions yield 98% accuracy, 44% activation rate. Example of designing for probabilistic outputs. | Ch 2 (Mindset) |
| **Figma** | Data shows 84% of designers collaborate with developers weekly as AI compresses the gap between concept and prototype. But fewer than half feel AI makes them better at their jobs -- the efficiency trap. | Ch 2 (Mindset) |

---

## Infrastructure & Operations Cases

Companies whose AI infrastructure and operational decisions provide key lessons for the book.

| Company | What the Book Discusses | Chapters / Frameworks |
|---------|------------------------|----------------------|
| **Klarna** | Bought OpenAI models for customer service. Month one: 2.3M conversations, resolution time dropped from 11 to 2 minutes, equivalent to 700 agents, projected $40M profit improvement. By mid-2025, began rebalancing toward human agents -- AI excelled at routine but couldn't handle fraud claims, disputes, or emotional scenarios. | Ch 2 (Mindset), Ch 9 (Data Strategy), Ch 10 (Operations & GTM), Ch 11 (Ethics) |
| **Morgan Stanley** | Took GPT-4 and trained it on 70,000+ proprietary research reports. 98% of advisor teams actively use the tool. "Makes you as smart as the smartest person in the organization." Classic Boost path -- vendor model plus proprietary data. | Ch 2 (Mindset) |
| **Bloomberg** | Spent $3.5-8M training BloombergGPT (50B parameter model). 9-person team. Data privacy drove the Build decision -- "Using an API like OpenAI's isn't suitable for us." Serves clients paying $25K+ annually. | Ch 2 (Mindset) |
| **OpenAI** | Spent $9B to generate $4B revenue in 2024. Multiple major outages (June 2025: 12 hours, 21 components; December 2024: 9 hours from Azure datacenter power failure). Illustrates single-point-of-failure risks and platform dependency. | Ch 4 (Infrastructure) |
| **Vercel (v0)** | Iterates on prompts "almost daily" using automated evaluations. Each edge case becomes a test case preventing regression. Example of compound iteration at speed. | Ch 2 (Mindset) |

---

## Data Strategy Cases

Companies whose data strategies -- both successes and failures -- illustrate core data principles in the book.

| Company | What the Book Discusses | Chapters / Frameworks |
|---------|------------------------|----------------------|
| **Tesla** | 2M+ vehicles capture "Autopilot Snapshot" clips of edge cases automatically. Automatically surfaces the 0.01% of cases that train networks. Earns $7K per vehicle as a data collector vs. Waymo spending $150K per vehicle. However, FSD "hasn't improved all year" based on 2025 data -- data collection without proper curation creates noise. | Ch 9 (Data Strategy) |
| **Spotify** | 1.4 trillion events daily from 678M users. 520 experiments on mobile home screen alone each year. Multi-task training shows transferable learning across podcasts and music. Users engaging AI recommendations show 40% higher retention, 140 vs. 99 minutes daily usage. | Ch 9 (Data Strategy) |
| **Duolingo** | Birdbrain AI estimates probability of correct answers. When learners struggle, difficulty updates in real-time for all current and future learners (network learning). 59% DAU growth (21M to 34M users), 80%+ organic acquisition, near-zero customer acquisition costs. Rewrote Session Generator from 750ms to 14ms. | Ch 9 (Data Strategy) |
| **Netflix** | Handles 4,000+ daily deployments with automated canary rollouts. Deploys in under 15 minutes vs. traditional enterprises at 8-90 days. Illustrates the velocity gap in data-driven iteration. | Ch 9 (Data Strategy) |
| **Zillow** | Shut down Zillow Offers in 2021 after AI property valuation failed. Wrote down $500M+, $304M Q3 losses, 25% workforce reduction. Two-thirds of purchased homes valued below purchase price. Models relied on data 30+ days old for near real-time decisions. | Ch 10 (Operations & GTM) |
| **Stitch Fix** | Experienced client declines, recovered with hybrid AI-human model. ML generates recommendations, human stylists add nuance. Result: 40% increase in average order value, 40% increase in repeat purchases, 30% reduction in returns. Recovery took 12-18 months. | Ch 9 (Data Strategy) |

---

## Governance & Risk Cases

Companies and incidents that illustrate AI governance, ethics, and risk management lessons.

| Company / Incident | What the Book Discusses | Chapters / Frameworks |
|--------------------|------------------------|----------------------|
| **IBM** | AI Ethics Board established 2019. Policy Advisory Committee, distributed accountability with ethics focal points in every business unit. AI Risk Atlas embedded in watsonx. Five years of governance refinement. | Ch 11 (Ethics & Governance) |
| **JPMorgan** | Elevated AI governance to 14-member Operating Committee in 2025. CDAO at the table -- one of few Fortune 1000 CDAOs at that level. AI innovation as operating committee mandate. | Ch 11 (Ethics & Governance) |
| **Air Canada** | Chatbot invented a "bereavement fare" policy. Canadian tribunal ruled the airline liable ($812.02). Established precedent: companies are liable for what their AI agents say. | Ch 6 (Agent Architecture), Ch 11 (Ethics) |
| **Chevrolet Dealership** | ChatGPT-powered chatbot with insufficient guardrails. Users manipulated it to agree to sell a Tahoe for $1 and recommend Tesla. Went viral. Illustrates scope creep failure mode. | Ch 6 (Agent Architecture) |
| **Samsung** | Three engineers entered proprietary source code into ChatGPT within 20 days. Samsung banned all generative AI tools company-wide. Illustrates privacy leakage risk. | Ch 11 (Ethics & Governance) |
| **X (Grok)** | Grok chatbot started injecting political claims into unrelated conversations in May 2025. Hardcoded administrative instructions overrode evidence-based programming. No audit trails. | Ch 4 (Infrastructure) |
| **Clearview AI** | 30.5M euro GDPR fine for facial recognition database built from 30B+ images collected without consent. | Ch 9 (Data Strategy), Ch 10 (Operations & GTM) |

---

## Related Frameworks

- [AI-First vs AI-Enabled](../frameworks/ai-first-vs-ai-enabled.md) -- The foundational distinction for categorizing these companies
- [Build vs Buy Calculus](../frameworks/build-vs-buy-calculus.md) -- Infrastructure decisions illustrated by Klarna, Morgan Stanley, and Bloomberg
- [Data Flywheel](../frameworks/data-flywheel.md) -- The mechanism behind Tesla, Spotify, and Duolingo's data advantages
- [7 AI Risks and Mitigations](../frameworks/7-ai-risks-and-mitigations.md) -- Risk categories illustrated by the governance cases
- [7 Failure Modes of Agents](../frameworks/7-failure-modes-of-agents.md) -- Agent failure patterns illustrated by Air Canada and Chevrolet
