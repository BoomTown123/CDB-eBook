# Open Source Projects

> Open source projects relevant to the topics covered in *Blueprint for an AI-First Company*. Organized by category with descriptions and GitHub URLs.

---

## Frameworks

Application frameworks for building LLM-powered systems. Central to Chapter 4 (Infrastructure), Chapter 5 (Building with AI), and Chapter 6 (Agent Architecture).

| Project | Description | GitHub |
|---------|-------------|--------|
| **LangChain** | Framework for building LLM applications with composable chains, agents, tools, and memory. The most widely adopted LLM orchestration framework. | https://github.com/langchain-ai/langchain |
| **LlamaIndex** | Data framework for connecting LLMs to external data sources. Specializes in RAG pipelines, document indexing, and structured data retrieval. RAG adoption jumped from 31% to 51% in one year. | https://github.com/run-llama/llama_index |
| **AutoGen** | Microsoft's framework for building multi-agent conversational systems. Agents can collaborate, debate, and execute code autonomously. | https://github.com/microsoft/autogen |
| **CrewAI** | Framework for orchestrating multi-agent AI systems with role-based agents, task delegation, and collaborative workflows. | https://github.com/crewAIInc/crewAI |
| **Semantic Kernel** | Microsoft's SDK for integrating LLMs into applications. Supports plugins, planners, and memory across C#, Python, and Java. | https://github.com/microsoft/semantic-kernel |
| **Haystack** | End-to-end NLP framework by deepset for building search systems, RAG pipelines, and question answering applications. | https://github.com/deepset-ai/haystack |
| **DSPy** | Framework from Stanford NLP for programming (not prompting) language models. Optimizes prompts and weights algorithmically. | https://github.com/stanfordnlp/dspy |

---

## Open-Weight Models

Model families that can be self-hosted, fine-tuned, and deployed on your own infrastructure. Discussed in Chapter 3 (The AI Landscape) and the [Foundation Models](../frameworks/foundation-models.md) framework. European banks run open models for regulatory compliance; Shopify runs 40-60M daily inferences on fine-tuned open models.

| Project | Description | GitHub / Model Hub |
|---------|-------------|-------------------|
| **Llama** | Meta's open-weight model family. Most widely adopted open model for enterprise deployments. Used by Shopify, European banks, and healthcare organizations for on-premises workloads. | https://github.com/meta-llama/llama |
| **Mistral** | European AI lab's open-weight models. Fastest time-to-first-token (0.30s). Strong performance relative to model size. | https://github.com/mistralai/mistral-inference |
| **Phi** | Microsoft's small language model family. Designed for resource-constrained environments and edge deployment with strong performance per parameter. | https://github.com/microsoft/phi-3 |
| **Gemma** | Google DeepMind's open model family. Available in multiple sizes for research and commercial use. | https://github.com/google-deepmind/gemma |
| **Qwen** | Alibaba's open-weight model family with strong multilingual capabilities and multiple model sizes. | https://github.com/QwenLM/Qwen |

---

## Serving & Inference Tools

Tools for running models efficiently in production. Addresses the infrastructure challenges discussed in Chapter 4 and the cost considerations in the [Foundation Models](../frameworks/foundation-models.md) framework.

| Project | Description | GitHub |
|---------|-------------|--------|
| **vLLM** | High-throughput LLM serving engine with PagedAttention for efficient memory management. The standard for production LLM serving. | https://github.com/vllm-project/vllm |
| **Ollama** | Run LLMs locally with a simple CLI. Supports Llama, Mistral, Phi, Gemma, and other open models out of the box. | https://github.com/ollama/ollama |
| **LM Studio** | Desktop application for discovering, downloading, and running local LLMs with a chat interface. Available for Mac, Windows, and Linux. | https://github.com/lmstudio-ai/lms |
| **Text Generation Inference (TGI)** | Hugging Face's production LLM serving solution. Optimized for throughput with continuous batching and tensor parallelism. | https://github.com/huggingface/text-generation-inference |
| **llama.cpp** | C/C++ port of Meta's Llama model for efficient CPU and GPU inference. Enables model quantization for running on consumer hardware. | https://github.com/ggerganov/llama.cpp |
| **LocalAI** | Drop-in OpenAI API replacement for running models locally. Supports multiple model formats and backends. | https://github.com/mudler/LocalAI |

---

## Evaluation & Benchmarking

Tools for evaluating model quality and comparing performance. The book emphasizes that benchmarks are "marketing tools masquerading as objective measures" -- these tools help you evaluate on your own data.

| Project | Description | GitHub / URL |
|---------|-------------|-------------|
| **LMSYS Chatbot Arena** | Live human preference evaluation platform where users compare model outputs head-to-head. The book notes Elo differences under 50 points are "basically a toss-up." | https://github.com/lm-sys/FastChat |
| **Open LLM Leaderboard** | Hugging Face's automated benchmark for open-weight models across multiple evaluation tasks. | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |
| **HELM** (Holistic Evaluation of Language Models) | Stanford's comprehensive evaluation framework testing models across accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency. | https://github.com/stanford-crfm/helm |
| **Evals** | OpenAI's framework for evaluating LLMs with custom evaluation tasks. Extensible for domain-specific testing. | https://github.com/openai/evals |
| **DeepEval** | Open source LLM evaluation framework for unit testing LLM outputs with metrics for hallucination, relevance, faithfulness, and toxicity. | https://github.com/confident-ai/deepeval |
| **promptfoo** | Open source tool for testing and evaluating LLM outputs across prompts, models, and parameters. Supports automated CI/CD evaluation. | https://github.com/promptfoo/promptfoo |

---

## Security & Safety

Tools for protecting AI systems against the risks described in Chapter 11 and the [7 AI Risks and Mitigations](../frameworks/7-ai-risks-and-mitigations.md) framework.

| Project | Description | GitHub |
|---------|-------------|--------|
| **Garak** | LLM vulnerability scanner that probes models for hallucination, data leakage, prompt injection, toxicity, and jailbreaking. Named after the Star Trek character. | https://github.com/NVIDIA/garak |
| **Rebuff** | Self-hardening prompt injection detection framework. Uses multi-layered defense including heuristics, LLM analysis, and canary tokens. | https://github.com/protectai/rebuff |
| **LLM Guard** | Input/output validation framework for LLMs. Detects prompt injections, scans for PII, checks toxicity, and enforces content policies. | https://github.com/protectai/llm-guard |
| **AI Fairness 360** | IBM's toolkit for detecting and mitigating bias in AI models. Referenced in the book's discussion of algorithmic fairness. | https://github.com/Trusted-AI/AIF360 |
| **Fairlearn** | Microsoft's toolkit for assessing and improving fairness of AI systems. Supports multiple fairness metrics and mitigation algorithms. | https://github.com/fairlearn/fairlearn |
| **NeMo Guardrails** | NVIDIA's toolkit for adding programmable guardrails to LLM applications. Controls topics, prevents jailbreaking, and enforces safety policies. | https://github.com/NVIDIA/NeMo-Guardrails |

---

## Observability & Monitoring

Tools for monitoring AI systems in production. Addresses the observability gap described in the [5 Infrastructure Mistakes](../frameworks/5-infrastructure-mistakes.md) framework -- only 51% of organizations can evaluate AI ROI.

| Project | Description | GitHub |
|---------|-------------|--------|
| **Phoenix** | Arize's open source ML observability tool for monitoring model performance, detecting drift, and debugging LLM applications. | https://github.com/Arize-AI/phoenix |
| **OpenLLMetry** | Open source observability framework for LLM applications built on OpenTelemetry. Traces LLM calls, chains, and agent actions. | https://github.com/traceloop/openllmetry |
| **Langfuse** | Open source LLM engineering platform for tracing, evaluation, prompt management, and cost tracking. | https://github.com/langfuse/langfuse |
| **whylogs** | WhyLabs' open source library for logging and monitoring data and model quality with statistical profiling. | https://github.com/whylabs/whylogs |

---

## Data & RAG Infrastructure

Tools for building the data pipelines and RAG systems that power AI-first products. Supports the [Data Flywheel](../frameworks/data-flywheel.md) framework.

| Project | Description | GitHub |
|---------|-------------|--------|
| **Chroma** | Open source embedding database for AI-native applications. Lightweight and designed for rapid prototyping and production use. | https://github.com/chroma-core/chroma |
| **Weaviate** | Open source vector database with built-in vectorization and hybrid search. | https://github.com/weaviate/weaviate |
| **Qdrant** | Open source vector similarity search engine with extended filtering and distributed deployment. | https://github.com/qdrant/qdrant |
| **pgvector** | PostgreSQL extension for vector similarity search. Store embeddings alongside relational data. | https://github.com/pgvector/pgvector |
| **Unstructured** | Open source library for preprocessing and extracting content from documents (PDFs, HTML, images, etc.) for RAG pipelines. | https://github.com/Unstructured-IO/unstructured |

---

## Related Frameworks

- [Foundation Models Landscape](../frameworks/foundation-models.md) -- Context for open vs. closed model decisions
- [Build vs Buy Calculus](../frameworks/build-vs-buy-calculus.md) -- When open source tools make sense vs. vendor solutions
- [5 Infrastructure Mistakes](../frameworks/5-infrastructure-mistakes.md) -- Infrastructure patterns these tools help address
- [7 AI Risks and Mitigations](../frameworks/7-ai-risks-and-mitigations.md) -- Risk categories the security tools help mitigate
- [7 Failure Modes of Agents](../frameworks/7-failure-modes-of-agents.md) -- Agent failure patterns the observability tools help detect
