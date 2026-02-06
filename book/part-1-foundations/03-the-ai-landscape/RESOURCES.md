# Chapter 3: The AI Landscape -- Resources

> Curated resources for deeper exploration of topics covered in this chapter.

## Frameworks from This Chapter

- [Foundation Models Landscape](../../../frameworks/foundation-models.md) -- The 4-layer AI stack (Foundation Models, Providers, Aggregators, Applications) and model capability comparisons.
- [6 Questions Before Choosing a Model](../../../frameworks/6-questions-before-choosing-a-model.md) -- The sequential decision framework: use case, latency tolerance, compliance, cost structure, explainability, and switching tolerance.

## Tools & Platforms

### Foundation Models
- [Claude (Anthropic)](https://www.anthropic.com/) -- 97.8% security compliance for code generation; 200K token context windows; 90% cache hit discount.
- [GPT (OpenAI)](https://openai.com/) -- 85.4% multimodal MMMU benchmark leader; SOC 2, HIPAA with signed BAAs.
- [Gemini (Google)](https://deepmind.google/technologies/gemini/) -- 87.6% on Video-MMMU; 2M token context windows; 99.9% SLA commitments.
- [DeepSeek](https://www.deepseek.com/) -- $0.07/million tokens with cache hits; 671B parameter Mixture of Experts model trained for ~$6M.
- [Llama (Meta)](https://ai.meta.com/llama/) -- Open-weight model; Shopify runs 40-60 million LLaVA inferences per day using fine-tuned Llama.
- [Mistral](https://mistral.ai/) -- Leads time-to-first-token at 0.30 seconds; open-weight models for European regulatory environments.

### Providers & Cloud Wrappers
- [OpenAI API](https://platform.openai.com/) -- Ecosystem leader; SOC 2, HIPAA with BAAs; Batch API offers 50% discount.
- [Anthropic API](https://docs.anthropic.com/) -- Prompt caching at 90% discount; safety-focused; rate limit considerations.
- [Google Vertex AI](https://cloud.google.com/vertex-ai) -- 99.9% SLA with financial credits; FedRAMP High authorization.
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service) -- Enterprise wrapper with Azure compliance and private networking.
- [AWS Bedrock](https://aws.amazon.com/bedrock/) -- Multi-model access through AWS infrastructure; pre-negotiated cloud discounts.
- [together.ai](https://www.together.ai/) -- Third-party host for open-source models with different cost/performance trade-offs.
- [Fireworks AI](https://fireworks.ai/) -- Model serving platform; helped Notion achieve 350ms latency.
- [Replicate](https://replicate.com/) -- Open-source model hosting with pay-per-use pricing.

### Aggregators & Routing
- [OpenRouter](https://openrouter.ai/) -- Single API to 100+ models; 5% markup; `:nitro` for speed, `:floor` for lowest price.
- [LiteLLM](https://docs.litellm.ai/) -- Open-source self-hosted gateway; 3ms P50 / 17ms P90 latency overhead.
- [Portkey](https://portkey.ai/) -- Enterprise LLM gateway starting at $49/month; 250+ LLMs; semantic caching and audit trails.
- [RouteLLM](https://openreview.net/forum?id=DWf4vroKWJ) -- Research showing 85% cost reduction while maintaining 90-95% of GPT-4 quality.
- [Helicone](https://www.helicone.ai/) -- LLM observability platform; built-in caching can cut costs 20-30%.
- [Langfuse](https://langfuse.com/) -- Open-source LLM observability and evaluation platform.

### Fine-Tuning & Evaluation
- [LoRA (Low-Rank Adaptation)](https://arxiv.org/abs/2106.09685) -- Reduces GPU memory requirements by up to 3x for fine-tuning.
- [PromptLayer](https://promptlayer.com/) -- Prompt versioning and management as code.
- [Maxim](https://www.getmaxim.ai/) -- Prompt versioning and AI evaluation platform.
- [Vespa](https://vespa.ai/) -- Distributed search and ranking engine; powers Perplexity's 200 billion URL index.

## Further Reading

- [How Perplexity Built an AI Google Competitor (ByteByteGo)](https://blog.bytebytego.com/p/how-perplexity-built-an-ai-google) -- Deep dive into Perplexity's multi-model routing, Vespa search stack, and "smallest viable model" approach.
- [Stanford HAI AI Index Report 2025](https://hai.stanford.edu/ai-index/2025-ai-index-report) -- Performance gap between top and 10th-ranked model shrank from 11.9% to 5.4%.
- [Menlo Ventures: 2025 State of Generative AI in the Enterprise](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/) -- Enterprise spending on generative AI grew 3.2x to $37 billion; 76% of use cases now purchased.
- [Hacker News Discussion on LangChain Abstractions](https://news.ycombinator.com/item?id=40739982) -- Developer backlash against over-abstraction; the emergence of LangGraph as a response.
- [Expanding Harvey's Model Offerings](https://www.harvey.ai/blog/expanding-harveys-model-offerings) -- Harvey's multi-model approach: different models excel at different legal subtasks.
- [Choosing the Right Model in Cursor](https://frontendmasters.com/blog/choosing-the-right-model-in-cursor/) -- Practical guide to multi-model usage in AI coding tools.
- [Claude Code vs Cursor (Qodo)](https://www.qodo.ai/blog/claude-code-vs-cursor/) -- Replit's Head of AI on why Claude is "by far the best model" for code generation.

## Research & Data

- [LMSYS Chatbot Arena](https://lmsys.org/) -- Community-driven model evaluation; Elo differences under 50 points are "basically a toss-up."
- [Lost in the Middle (arXiv)](https://arxiv.org/abs/2307.03172) -- Research on performance degradation when relevant information sits in the middle of long contexts.
- [Cisco: Security Evaluation of DeepSeek](https://blogs.cisco.com/security/evaluating-security-risk-in-deepseek-and-other-frontier-reasoning-models) -- 100% attack success rate on DeepSeek-R1; fails to block any harmful prompts.
- [Qualys DeepSeek Security Assessment](https://blog.qualys.com/vulnerabilities-threat-research/2025/01/31/deepseek-failed-over-half-of-the-jailbreak-tests-by-qualys-totalai) -- DeepSeek generates insecure code at 4x the rate of competitors.
- [Bain & Company: DeepSeek Analysis](https://www.bain.com/insights/deepseek-a-game-changer-in-ai-efficiency/) -- DeepSeek V3 trained for ~$6M versus estimated $100M+ for GPT-4.
- [IDC: The Future of AI is Model Routing](https://www.idc.com/resource-center/blog/the-future-of-ai-is-model-routing/) -- By 2028, 70% of top AI-driven enterprises will use multi-model architectures.
- [CFM Case Study (HuggingFace)](https://huggingface.co/blog/cfm-case-study) -- Capital Fund Management achieved solutions 80x cheaper than large LLMs with LoRA fine-tuning.
- [Glean AI Evaluator](https://www.glean.com/blog/glean-ai-evaluator) -- How Glean measures context relevance and recall rates for enterprise search evaluation.

## Community & Learning

- [LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/) -- Community-driven, open platform for evaluating LLMs through human preference.
- [Hugging Face](https://huggingface.co/) -- Open-source AI community; hosts models, datasets, and case studies like CFM's LoRA fine-tuning.
- [Data-Centric AI (datacentricai.org)](https://datacentricai.org/) -- Community and resources focused on improving AI through data quality rather than model architecture.

### Provider Comparison Summary

| Provider | Strength | Key SLA | Cache Discount |
|----------|----------|---------|----------------|
| OpenAI | Ecosystem depth, brand | ~99.3% uptime | 50% automatic |
| Anthropic | Safety, long context | Rate limit tiers | 90% on hits (25% write premium) |
| Google Vertex | Enterprise SLA | 99.9% with financial credits | Varies |
| DeepSeek | Cost ($0.07/M tokens) | No enterprise SLA | N/A |
| Meta (Llama) | Open weights, self-host | Self-managed | N/A |
