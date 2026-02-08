# Chapter 6: Agent Architecture -- Resources

> Curated resources for deeper exploration of topics covered in this chapter.

## Frameworks from This Chapter

- [7 Failure Modes of Agents](../../../frameworks/10-seven-failure-modes-of-agents.md) -- Hallucinated actions, scope creep, context loss, infinite loops, cascading failures, resource exhaustion, and stale data -- with mitigations for each.

## Tools & Platforms

### Agent Frameworks & Orchestration
- [Temporal](https://temporal.io/) -- Workflow orchestration engine; used by Replit for agent task management serving 30M users.
- [Claude Code](https://code.claude.com/) -- Agentic coding tool with plan mode, subagents, and hooks for automated review checkpoints.
- [Anthropic Agent SDK](https://docs.anthropic.com/) -- SDK for building production AI agents with structured tool calling.
- [AutoMCP](https://github.com/anthropics/anthropic-cookbook) -- Automated MCP tool generation; 19 lines of fixes took success rate from 76.5% to 99.9%.
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) -- 1,000+ connectors for agent-tool integration; standard for chat and background agents.

### Chat Agent Platforms
- [Intercom Fin](https://www.intercom.com/fin) -- AI customer support agent; improved from 25% to 66% resolution rate through iterative design.
- [Klarna AI Assistant](https://www.klarna.com/) -- Handled 2.3M conversations in first month; 700 FTE equivalent; $40M projected annual savings.

### Background Agent Infrastructure
- [Kafka](https://kafka.apache.org/) -- Event streaming platform; Netflix processes billions of daily events for inter-service communication.
- [RabbitMQ](https://www.rabbitmq.com/) -- Message broker for async agent communication patterns.

### Agent Monitoring & Safety
- [Helicone](https://www.helicone.ai/) -- LLM observability for tracking agent costs and performance.
- [LangSmith](https://smith.langchain.com/) -- Agent tracing and evaluation from LangChain.

## Further Reading

- [Klarna AI Assistant Press Release](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/) -- 2.3 million conversations in first month; response time from 11 minutes to under 2 minutes.
- [Klarna CEO: "Gone Too Far with AI"](https://www.bloomberg.com/news/articles/2025-05-06/klarna-begins-hiring-humans-again-after-ai-drive) -- Why Klarna reversed course and started hiring humans again after over-automating.
- [Microsoft AI Red Team Taxonomy (April 2025)](https://www.microsoft.com/en-us/security/blog/) -- Formalized failure categories for AI agent systems.
- [Air Canada Chatbot Ruling](https://www.bbc.com/news/business-68378898) -- Court ruled Air Canada liable for chatbot's hallucinated bereavement fare policy; $812.02 total tribunal order.
- [Chevrolet $1 Tahoe Incident](https://www.theverge.com/2023/12/19/24007651/chevy-chatbot-sold-car-one-dollar) -- Chatbot agreed to sell a Chevrolet Tahoe for $1 after prompt manipulation.
- [Expanding Harvey's Model Offerings](https://www.harvey.ai/blog/expanding-harveys-model-offerings) -- Harvey's multi-model routing for different legal subtasks.

## Research & Data

- [BoldDesk: Agent Market Analysis 2025](https://www.bolddesk.com/) -- Conversational AI growing at 23% CAGR; autonomous AI agent market at 45% CAGR.
- [Deloitte: State of Agentic AI 2025](https://www2.deloitte.com/us/en/insights/focus/tech-trends.html) -- 42% of companies abandoned AI initiatives; 46% scrapped proof-of-concepts.
- [S&P Global: AI Adoption Mixed Outcomes](https://www.spglobal.com/market-intelligence/en/news-insights/research/ai-experiences-rapid-adoption-but-with-mixed-outcomes-highlights-from-vote-ai-machine-learning) -- 42% of companies abandoned most AI initiatives in 2025.
- [Adversa AI Security Report](https://www.prnewswire.com/news-releases/adversa-ai-unveils-explosive-2025-ai-security-incidents-reportrevealing-how-generative-and-agentic-ai-are-already-under-attack-302517767.html) -- 73% of enterprises experienced AI-related security breaches; 35% from prompt injection.
- Agent cost data: 73% of teams lack cost tracking; averaging 340% cost overruns on agent projects.
- Agent performance benchmarks: Chat agent p50 latency 1,850ms; p95 latency 4,200ms in production.

## Community & Learning

- [Replit Agent Documentation](https://docs.replit.com/replitai/agent) -- Temporal-based orchestration patterns serving 30M users; autonomy modes.
- [Cursor AI Documentation](https://docs.cursor.com/) -- Multi-model agent with PermissionOptions for access control.

### The 2 Agent Types

| Characteristic | Chat Agents | Background Agents |
|---------------|-------------|-------------------|
| **Who waits** | Human is waiting | No one is watching |
| **Speed priority** | Response in seconds | Throughput over latency |
| **Error handling** | Clarify and retry | Log, retry, alert |
| **Autonomy** | Human-in-the-loop | Autonomous with guardrails |
| **Success metric** | Satisfaction, resolution rate | Processing volume, accuracy |
| **Example** | Klarna support, Intercom Fin | Overnight data processing, report generation |

### The 5-Question Agent Decision Framework

Before building an agent, ask:
1. Does the task require reasoning (not just rules)?
2. Does it vary significantly across instances?
3. Does it scale to justify the overhead?
4. Can it tolerate occasional errors?
5. Does it follow a stable process?

If you answer "no" to any of these, consider alternatives to agents.

### Key Incidents Referenced

| Incident | Company | Failure Mode | Lesson |
|----------|---------|-------------|--------|
| Hallucinated bereavement policy | Air Canada | Hallucinated Actions | Companies liable for AI agent statements |
| $1 Tahoe sale | Chevrolet | Scope Creep | Agents need bounded authority |
| 4,000 fake records + deleted DB | Replit | Cascading Failures | Background agents need dead man's switches |
| Over-automation reversal | Klarna | Wrong agent type | Chat tasks need human nuance; one agent doesn't fit all |
