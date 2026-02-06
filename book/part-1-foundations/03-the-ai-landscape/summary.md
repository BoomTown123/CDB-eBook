# Chapter Summary: The AI Landscape

## Key Takeaways

1. **Think in layers, not models:** The AI stack has four layers—Foundation Models, Providers, Aggregators, Applications. Most differentiation lives in the application layer. Perplexity's 38-person team competes with Google by routing queries across models with 91.3% accuracy, not by having better models.

2. **Match capability to constraint:** Claude leads code (97.8% security compliance), GPT leads multimodal (85.4% MMMU), Gemini leads video (87.6%) and context (2M tokens), DeepSeek leads cost ($0.07/M tokens with 100% jailbreak success). No model wins everything. Your compliance requirements, latency tolerance, and cost structure eliminate options before benchmarks matter.

3. **Route, don't commit:** RouteLLM achieves 85% cost reduction while maintaining 90-95% of GPT-4 quality. Aggregators add 3-40ms latency but provide failover, unified APIs, and cost optimization. The question isn't which provider—it's how to build an abstraction layer for the right model per task.

4. **Exhaust cheap options before fine-tuning:** Prompt engineering costs nothing to iterate. RAG handles knowledge gaps without model modification. Fine-tuning is for the last mile—style, format, tool use—and 73% of projects fail ROI. The $5-10K monthly API threshold and LoRA's 3x GPU reduction change the math, but only after you've tried everything else.

5. **Architect for change, not correctness:** The model you choose today will be obsolete in 18 months. Prompt versioning, evaluation infrastructure, circuit breakers, and cost-aware routing are the patterns that survive. The abstraction trap is real—too little means vendor lock-in, too much means framework lock-in. Build the thin wrapper that normalizes the 80% case while preserving escape hatches.

---

Next: [Infrastructure for AI-First Operations](../../part-2-building/04-infrastructure-for-ai-first-operations/README.md)

---

[← Previous: Future-Proofing Your Stack](./07-future-proofing-your-stack.md) | [Chapter Overview](./README.md)
