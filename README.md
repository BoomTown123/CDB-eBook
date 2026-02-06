# Blueprint for an AI-First Company

![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Frameworks](https://img.shields.io/badge/Frameworks-20-blue)
![Code Examples](https://img.shields.io/badge/Code%20Examples-14-green)
![Chapters](https://img.shields.io/badge/Chapters-12-orange)

Frameworks, code, and the complete AI writing system behind the book by [Saurav Bhatia](https://www.linkedin.com/in/sauravbhats) -- former founding executive of two digital banks, now building AI-first at [Yirifi.ai](https://yirifi.ai).

This isn't a collection of slides repackaged as markdown. Every framework comes from building real products -- digital banks that acquired 450,000 clients in four months, an AI startup where two people shipped 15 products in three months, and a $5 billion retail operation spanning 32 countries. The book was written using the same AI-first methods it teaches, and the entire production system is documented here.

---

## The AI Writing System

> 81,000 words. 775 citations. 14 AI agents. The entire system is documented.

This book was produced using a multi-agent AI writing system built on Claude Code, Perplexity, and Obsidian. The full system -- every prompt, script, skill, and architectural decision -- is open for you to study, adapt, or use.

| Metric | Count |
|--------|-------|
| Total words written | 81,000+ across 12 chapters |
| Inline citations with source URLs | 775 |
| Claude Code agent skills | 14 (writer, reviewer, researcher, quality auditor) |
| Research prompts (Perplexity) | 180+ |
| Python automation scripts | 17 |
| Adaptable templates | 17 |

What's documented: author voice encoding (6 files that teach an LLM to write like a specific human), 27 modular prompts across 5 categories, multi-agent orchestration, a research pipeline that generates citation-ready content, Obsidian vault architecture, a Flask + PostgreSQL analysis app with 70+ modules, and a 4-phase editorial review process.

**[Explore the AI Writing System >](ai-writing-process/)**

---

## What's in This Repository

| Section | Count | What You Get |
|---------|-------|--------------|
| [Frameworks](frameworks/) | 20 | Decision models for strategy, architecture, hiring, data, and governance |
| [Code Examples](examples/) | 14 | Agent patterns, infrastructure, prompts, and CI/CD configs in Python |
| [Checklists](checklists/) | 7 | Readiness assessments and audit tools you can use today |
| [Guides](guides/) | 6 | Step-by-step implementation walkthroughs |
| [Workflows](workflows/) | 4 | Repeatable operational processes |
| [Resources](resources/) | 6 categories | Curated tools, papers, case studies, courses, and communities |
| [AI Writing Process](ai-writing-process/) | 57 files | The complete system behind writing the book with AI |
| [Book Chapters](book/) | 12 | Chapter-by-chapter companion content |

---

## About the Author

Saurav Bhatia is the Founder and CEO of [Yirifi.ai](https://yirifi.ai), where his two-person team built 15 AI-powered microsites in three months -- a proof point for what AI-first development makes possible, and the central case study of this book.

Before Yirifi, Saurav spent nearly a decade at Standard Chartered Bank in Singapore and Hong Kong. As Interim CEO and Chief Customer & Product Officer of TRUST Bank -- Singapore's first digital bank -- he laid the foundation from scratch: regulatory approval, joint venture with NTUC, 100+ person team, and a product that acquired 450,000 clients within four months, capturing 9% market share. As founding CFO of Mox Bank in Hong Kong, he helped secure the virtual banking license and build what became the most downloaded app in Hong Kong across all categories -- 440,000 clients and $1.2 billion in deposits within two years.

He also served as Global Head of Digital Assets for Retail, Private and Wealth at Standard Chartered, and Global Head of Finance for the bank's $5 billion retail operation spanning 9 million clients in 32 countries. Before Standard Chartered, he held progressive leadership roles at Citibank over nine years.

Saurav holds an MBA from the National University of Singapore and completed the Oxford Blockchain Strategy Programme. He began his career as a founder in 1999.

[LinkedIn](https://www.linkedin.com/in/sauravbhats) | [X](https://x.com/sauravbhats) | [Blog](https://blog.sauravbhatia.com)

---

## About the Book

*Blueprint for an AI-First Company* is a practical guide to building companies where AI is the foundation, not an afterthought. 12 chapters, 4 parts, 81,000+ words, 775 inline citations with source URLs.

**Start where you need to:**

- **Evaluating AI strategy?** Start with Part I (Foundations)
- **Ready to build?** Jump to Part II (Building)
- **Scaling your AI team?** See Part III (Operating)
- **Long-term sustainability?** Read Part IV (Sustaining)

<details>
<summary>Full Table of Contents (12 chapters)</summary>

| # | Chapter | Part | Description |
|---|---------|------|-------------|
| 1 | [The AI-First Imperative](book/part-1-foundations/01-the-ai-first-imperative/) | Foundations | Why being AI-first matters now and the competitive advantages it creates |
| 2 | [The AI-First Mindset](book/part-1-foundations/02-the-ai-first-mindset/) | Foundations | How AI-first founders think differently about opportunities and building |
| 3 | [The AI Landscape](book/part-1-foundations/03-the-ai-landscape/) | Foundations | Navigating foundation models, providers, and making strategic choices |
| 4 | [Infrastructure for AI-First Operations](book/part-2-building/04-infrastructure-for-ai-first-operations/) | Building | The infrastructure stack -- databases, gateways, and auth |
| 5 | [Building with AI](book/part-2-building/05-building-with-ai/) | Building | How to build software with AI as a collaborator |
| 6 | [Agent Architecture](book/part-2-building/06-agent-architecture/) | Building | Two types of agents, when to use each, and the Agent Hub pattern |
| 7 | [The Microsite Pattern](book/part-2-building/07-the-microsite-pattern/) | Building | Domain microsites with shared infrastructure and AI agent access |
| 8 | [Teams for AI-First Companies](book/part-3-operating/08-teams-for-ai-first-companies/) | Operating | Structuring teams and building culture for AI-first success |
| 9 | [Data Strategy](book/part-3-operating/09-data-strategy/) | Operating | Building data advantages that compound |
| 10 | [AI-Augmented Operations and GTM](book/part-3-operating/10-ai-augmented-operations-and-gtm/) | Operating | Using AI to scale operations and customer-facing growth |
| 11 | [Ethics, Governance, and Risk](book/part-4-sustaining/11-ethics-governance-and-risk/) | Sustaining | Responsible AI with proper governance and risk management |
| 12 | [Staying Ahead](book/part-4-sustaining/12-staying-ahead/) | Sustaining | Building architecture that absorbs change rather than resisting it |

</details>

---

## Frameworks

20 decision frameworks extracted from the book, each with context on when and how to use it.

**Highlights:**

- [AI-First vs AI-Enabled](frameworks/ai-first-vs-ai-enabled.md) -- Assess where your company falls on the spectrum (Ch 1)
- [7 Failure Modes of Agents](frameworks/7-failure-modes-of-agents.md) -- Diagnose why an agent is failing (Ch 6)
- [8 Patterns for AI Coding](frameworks/8-patterns-for-ai-coding.md) -- Structure AI-assisted development workflows (Ch 5)
- [90-Day AI Fluency Program](frameworks/90-day-ai-fluency-program.md) -- Upskill your team on AI tools and thinking (Ch 8)

<details>
<summary>All 20 frameworks</summary>

| Framework | Chapter | Use When |
|-----------|---------|----------|
| [AI-First vs AI-Enabled](frameworks/ai-first-vs-ai-enabled.md) | Ch 1 | Assessing where your company falls on the spectrum |
| [7 Mental Models of AI-First](frameworks/7-mental-models-of-ai-first.md) | Ch 2 | Shifting how your team thinks about AI |
| [Probabilistic AI](frameworks/probabilistic-ai.md) | Ch 2 | Designing for non-deterministic outputs |
| [Build vs Buy Calculus](frameworks/build-vs-buy-calculus.md) | Ch 2 | Deciding whether to build or buy AI capabilities |
| [Human-AI Collaboration](frameworks/human-ai-collaboration.md) | Ch 2 | Defining roles between humans and AI systems |
| [Foundation Models](frameworks/foundation-models.md) | Ch 3 | Understanding major model families and trade-offs |
| [6 Questions Before Choosing a Model](frameworks/6-questions-before-choosing-a-model.md) | Ch 3 | Evaluating which model fits your use case |
| [5 Infrastructure Mistakes](frameworks/5-infrastructure-mistakes.md) | Ch 4 | Auditing your AI infrastructure decisions |
| [8 Patterns for AI Coding](frameworks/8-patterns-for-ai-coding.md) | Ch 5 | Structuring AI-assisted development workflows |
| [7 Failure Modes of Agents](frameworks/7-failure-modes-of-agents.md) | Ch 6 | Diagnosing why an agent is failing |
| [90-Day AI Fluency Program](frameworks/90-day-ai-fluency-program.md) | Ch 8 | Upskilling your team on AI tools and thinking |
| [Data Flywheel](frameworks/data-flywheel.md) | Ch 9 | Building compounding data advantages |
| [Data Moats](frameworks/data-moats.md) | Ch 9 | Identifying defensible data assets |
| [6 Data Strategy Mistakes](frameworks/6-data-strategy-mistakes.md) | Ch 9 | Avoiding common data strategy pitfalls |
| [Automation vs Augmentation](frameworks/automation-vs-augmentation.md) | Ch 10 | Choosing where AI replaces vs enhances humans |
| [8 GTM Mistakes with AI](frameworks/8-gtm-mistakes-with-ai.md) | Ch 10 | Reviewing your AI go-to-market approach |
| [Permission Model Framework](frameworks/permission-model-framework.md) | Ch 11 | Designing AI permission and access controls |
| [AI Governance Framework](frameworks/ai-governance-framework.md) | Ch 11 | Setting up organizational AI governance |
| [7 AI Risks and Mitigations](frameworks/7-ai-risks-and-mitigations.md) | Ch 11 | Identifying and addressing AI-related risks |
| [10 Principles of AI-First](frameworks/10-principles-of-ai-first.md) | Ch 12 | Grounding long-term AI-first strategy |

</details>

---

## Code Examples

14 working examples in Python covering agent patterns, infrastructure components, prompt templates, and CI/CD configuration.

**Highlights:**

- [Chat Agent](examples/agent-patterns/chat-agent/) -- Conversational AI agent pattern
- [Agent Hub](examples/agent-patterns/agent-hub/) -- Multi-agent orchestration
- [AI Gateway](examples/infrastructure/ai-gateway/) -- Unified API gateway for AI providers

<details>
<summary>All 14 code examples</summary>

| Example | Description | Language |
|---------|-------------|----------|
| [Chat Agent](examples/agent-patterns/chat-agent/) | Conversational AI agent pattern | Python |
| [Background Agent](examples/agent-patterns/background-agent/) | Async task processing agent | Python |
| [Agent Hub](examples/agent-patterns/agent-hub/) | Multi-agent orchestration | Python |
| [AI Gateway](examples/infrastructure/ai-gateway/) | Unified API gateway for AI providers | Python |
| [Unified Auth](examples/infrastructure/unified-auth/) | Human and agent authentication | Python |
| [Observability](examples/infrastructure/observability/) | AI-specific monitoring and tracing | Python |
| [Coding Prompts](examples/prompts/coding-prompts/) | AI coding prompt templates | Markdown |
| [Agent System Prompts](examples/prompts/agent-system-prompts/) | Agent system prompt templates | Markdown |
| [Evaluation Prompts](examples/prompts/evaluation-prompts/) | Model evaluation prompt templates | Markdown |
| [Claude Code Setup](examples/configs/claude-code-setup/) | Claude Code configuration files | Config |
| [CI AI Review](examples/configs/ci-ai-review/) | CI/CD pipeline with AI code review | Config |

</details>

---

## Checklists, Guides & Workflows

### Checklists

- [AI Readiness Assessment](checklists/ai-readiness-assessment.md) -- Is your company ready for AI-first?
- [Model Selection Checklist](checklists/model-selection-checklist.md) -- Choosing the right model for your use case
- [Agent Design Checklist](checklists/agent-design-checklist.md) -- Before building an agent
- [Infrastructure Audit](checklists/infrastructure-audit.md) -- Audit your AI infrastructure
- [Data Strategy Checklist](checklists/data-strategy-checklist.md) -- Building your data strategy
- [Governance Checklist](checklists/governance-checklist.md) -- AI governance readiness
- [GTM AI Readiness](checklists/gtm-ai-readiness.md) -- AI-augmenting your go-to-market

### Guides

- [Building Your First Agent](guides/building-your-first-agent.md) -- End-to-end walkthrough of agent development
- [Setting Up an AI Tool Gateway](guides/setting-up-ai-tool-gateway.md) -- Unified API gateway for multiple AI providers
- [Implementing Data Flywheels](guides/implementing-data-flywheels.md) -- Building compounding data feedback loops
- [Polyglot Persistence Setup](guides/polyglot-persistence-setup.md) -- Configuring multiple data stores for AI workloads
- [AI Coding Workflow](guides/ai-coding-workflow.md) -- Integrating AI into your development process
- [Team AI Fluency Rollout](guides/team-ai-fluency-rollout.md) -- Rolling out AI fluency across your organization

### Workflows

- [AI Coding Session Workflow](workflows/ai-coding-session-workflow.md) -- Structured flow for an AI-assisted coding session
- [Agent Failure Recovery](workflows/agent-failure-recovery.md) -- Diagnosing and recovering from agent failures
- [Model Evaluation Workflow](workflows/model-evaluation-workflow.md) -- Systematic process for evaluating models
- [90-Day Fluency Implementation](workflows/90-day-fluency-implementation.md) -- Week-by-week plan for team AI fluency

---

## Resources

- [Tools](resources/tools.md) -- AI tools and platforms referenced in the book
- [Research Papers](resources/research-papers.md) -- Key papers behind the concepts
- [Case Studies](resources/case-studies.md) -- Real-world AI-first company examples
- [Courses and Learning](resources/courses-and-learning.md) -- Recommended courses and learning paths
- [Communities](resources/communities.md) -- Communities for AI-first builders
- [Open Source Projects](resources/open-source-projects.md) -- Relevant open source projects

---

## Get the Book

*Blueprint for an AI-First Company* is available at [the book's website](#). The frameworks and code here are extracted from the book. The book provides the full narrative, case studies, and strategic context that these companion materials are built around.

---

## Contributing

Contributions are welcome. Whether you have a resource suggestion, a code example, or a correction, please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to participate.

---

## License

This repository is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](LICENSE).

Copyright 2026 Saurav Bhatia. All rights reserved.
