# AI Tools & Platforms

> Tools and platforms referenced throughout *Blueprint for an AI-First Company*, organized by category. Each entry includes a brief description and official URL.

---

## AI Coding Tools

Tools that integrate AI directly into the software development workflow. Referenced extensively in Chapter 5 (Building with AI) and the [8 Patterns for AI Coding](../frameworks/8-patterns-for-ai-coding.md) framework.

| Tool | Description | URL |
|------|-------------|-----|
| **Cursor** | AI-first code editor with inline completions, chat, and agent capabilities. Grew from $1M to $100M revenue in one year. | https://cursor.com |
| **GitHub Copilot** | AI pair programmer integrated into VS Code and JetBrains IDEs. 78% task completion rate; ~30% suggestion acceptance rate; 55% faster task completion. | https://github.com/features/copilot |
| **Replit** | Browser-based IDE with AI agent capabilities including "Max Autonomy" mode for extended AI-driven coding sessions. | https://replit.com |
| **Claude Code** | Anthropic's CLI-based AI coding agent. Uses CLAUDE.md files for persistent project context across sessions. | https://docs.anthropic.com/en/docs/claude-code |
| **Windsurf** | AI-powered IDE by Codeium with Cascade, an agentic coding workflow that reasons across your entire codebase. | https://windsurf.com |

---

## Foundation Model Providers

The core model providers discussed in Chapter 3 (The AI Landscape) and the [Foundation Models](../frameworks/foundation-models.md) framework.

| Provider | Description | URL |
|----------|-------------|-----|
| **OpenAI** | Creator of GPT models. Strong multimodal capabilities (85.4% MMMU). Powers the majority of AI startup APIs. | https://openai.com |
| **Anthropic** | Creator of Claude 4.5 Sonnet. Leading code generation (97.8% security compliance on Claude 4.5 Sonnet) and analytical reasoning. | https://anthropic.com |
| **Google (Gemini)** | Gemini models with industry-leading context windows (2M tokens) and video understanding (87.6%). First FedRAMP High authorization for generative AI. | https://deepmind.google/technologies/gemini/ |
| **Mistral** | European AI lab offering open-weight and commercial models. Fastest time-to-first-token at 0.30 seconds. Founded 2023, $6B valuation within 18 months. | https://mistral.ai |
| **Meta (Llama)** | Open-weight Llama model family. Used by Shopify for 40-60M daily inferences. Preferred for on-premises deployments in regulated industries. | https://llama.meta.com |
| **DeepSeek** | Chinese AI lab offering extremely cost-efficient models ($0.07/M tokens with cache). V3 trained for roughly $6M versus $100M+ for comparable models. Requires security controls due to documented vulnerabilities. | https://www.deepseek.com |

---

## AI Infrastructure

Platforms for building, orchestrating, and monitoring AI applications. Referenced in Chapter 4 (Infrastructure) and Chapter 6 (Agent Architecture).

| Tool | Description | URL |
|------|-------------|-----|
| **LangChain** | Framework for building LLM-powered applications with chains, agents, and tool integrations. | https://www.langchain.com |
| **LangSmith** | LangChain's platform for debugging, testing, evaluating, and monitoring LLM applications in production. | https://www.langchain.com/langsmith |
| **Weights & Biases** | ML experiment tracking, model versioning, and dataset management platform. | https://wandb.ai |
| **Helicone** | Open source LLM observability platform for logging, monitoring, and optimizing AI API usage and costs. | https://www.helicone.ai |
| **Portkey** | AI gateway for routing, load balancing, and managing multiple LLM providers through a unified API. | https://portkey.ai |

---

## Vector Databases

Specialized databases for storing and querying embeddings, essential for RAG architectures. RAG adoption jumped from 31% to 51% in one year (referenced in the [10 Principles](../frameworks/10-principles-of-ai-first.md) framework).

| Database | Description | URL |
|----------|-------------|-----|
| **Pinecone** | Fully managed vector database designed for high-performance similarity search at scale. | https://www.pinecone.io |
| **Weaviate** | Open source vector database with built-in vectorization modules and hybrid search capabilities. | https://weaviate.io |
| **Chroma** | Lightweight, open source embedding database designed for AI-native applications and rapid prototyping. | https://www.trychroma.com |
| **Qdrant** | Open source vector similarity search engine with extended filtering support and distributed deployment. | https://qdrant.tech |
| **pgvector** | Open source PostgreSQL extension for vector similarity search, enabling vector storage alongside relational data. | https://github.com/pgvector/pgvector |

---

## AI Observability

Monitoring and evaluation platforms for AI systems in production. Addresses the observability gaps described in [5 Infrastructure Mistakes](../frameworks/5-infrastructure-mistakes.md) -- only 51% of organizations can confidently evaluate AI ROI.

| Tool | Description | URL |
|------|-------------|-----|
| **Arize** | ML observability platform for monitoring model performance, detecting drift, and troubleshooting production issues. | https://arize.com |
| **WhyLabs** | AI observability platform focused on data quality monitoring, model performance tracking, and LLM security. | https://whylabs.ai |
| **Arthur AI** | AI performance monitoring with built-in bias detection, explainability, and compliance reporting. | https://www.arthur.ai |

---

## AI Security

Security tools for protecting AI systems against prompt injection, jailbreaking, and data leakage. Addresses risks covered in [7 AI Risks and Mitigations](../frameworks/7-ai-risks-and-mitigations.md).

| Tool | Description | URL |
|------|-------------|-----|
| **Lakera** | Real-time AI security platform that detects prompt injections, data leakage, and content policy violations. | https://www.lakera.ai |
| **Robust Intelligence** | AI security and validation platform for testing model robustness, detecting adversarial attacks, and continuous monitoring. | https://www.robustintelligence.com |
| **Calypso AI** | AI security and trust platform providing inference-time monitoring, compliance automation, and risk management for enterprise AI. | https://calypsoai.com |

---

## Related Frameworks

- [Foundation Models Landscape](../frameworks/foundation-models.md) -- Detailed comparison of model strengths, weaknesses, and pricing
- [6 Questions Before Choosing a Model](../frameworks/6-questions-before-choosing-a-model.md) -- Decision framework for model selection
- [Build vs Buy Calculus](../frameworks/build-vs-buy-calculus.md) -- When to use vendor tools vs. building your own
- [5 Infrastructure Mistakes](../frameworks/5-infrastructure-mistakes.md) -- Common infrastructure failures to avoid
