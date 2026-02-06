# Agent Hub

Central orchestrator that routes requests to specialist agents.

**Book reference:** Chapter 6 - Agent Architecture, Section 2

## What This Demonstrates

The Agent Hub pattern provides centralized control with distributed execution. It is architecturally similar to an API gateway or Kubernetes control plane: the hub decides what agents can do; agents decide how to do it.

This example implements the six hub responsibilities from the book:

1. **Permission management** - Centralized agent registry (simplified)
2. **Unified observability** - Routing logs with timing and confidence scores
3. **Lifecycle management** - Agent initialization and health tracking
4. **Tool registry** - Agent discovery and capability listing
5. **Rate limiting** - Request counting with session limits
6. **Circuit breakers** - Error tracking with automatic fallback

## Two-Model Architecture

This example uses a **two-model pattern** through OpenRouter:

| Role | Model | Purpose |
|------|-------|---------|
| Router | `google/gemini-2.5-flash` | Cheap/fast intent classification |
| Agents | `anthropic/claude-sonnet-4.5` | Capable specialist execution |

Both models are accessed through the same provider (OpenRouter) -- only the model ID differs. This keeps routing costs low (Gemini Flash is very cheap) while giving specialist agents a highly capable model for actual work.

Uses the **shared provider library** (`examples/shared/`) for LLM access, which provides a provider abstraction layer with proper error handling, streaming support, and multi-provider compatibility.

## Files

| File | Purpose |
|------|---------|
| `hub.py` | Central hub with routing, observability, rate limiting, and circuit breakers |
| `router.py` | Intent classification using a cheap/fast model to select specialist agents |
| `agents/research.py` | Research specialist: factual questions and information lookup |
| `agents/writer.py` | Writing specialist: content creation (emails, reports, posts) |
| `agents/analyst.py` | Analysis specialist: data analysis, metrics, trend identification |
| `agents/__init__.py` | Agent package exports |
| `config.py` | Configuration via environment variables |

## Quick Start

```bash
# Install dependencies (from repo root)
pip install -r examples/shared/requirements.txt
pip install -r examples/agent-patterns/agent-hub/requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your OpenRouter API key (https://openrouter.ai/keys)

# Run
python hub.py
```

## How It Works

```
User message
    |
    v
[Rate limit check]
    |
    v
[Router classifies intent]  <-- Cheap model (gemini-2.5-flash via OpenRouter)
    |
    +-- "research" --> ResearchAgent
    +-- "writer"   --> WriterAgent
    +-- "analyst"  --> AnalystAgent
    |
    v
[Circuit breaker check]
    |
    +-- OPEN --> Fall back to alternate agent
    +-- CLOSED --> Proceed
    |
    v
[Specialist agent processes request]  <-- Capable model (claude-sonnet-4.5 via OpenRouter)
    |
    v
[Log routing decision]
    |
    v
[Return response]
```

The router uses Gemini Flash (cheap, fast) for intent classification. Once the intent is determined, the request is dispatched to a specialist agent running Claude Sonnet (capable) with a domain-tuned system prompt. Both models are accessed through OpenRouter's unified API.

## Key Design Decisions

- **Two-model architecture**: cheap/fast model for routing, capable model for execution. Routing should be near-instant and cost very little.
- **Shared provider library**: Uses `examples/shared/` for LLM access, making it easy to swap providers or models without changing business logic.
- **Circuit breakers**: if a specialist agent fails repeatedly, the hub automatically falls back to an alternate agent rather than returning errors.
- **Routing with confidence**: the router returns a confidence score. Low-confidence routes get retried before dispatching.
- **Observability built in**: every routing decision is logged with timing, confidence, and reasoning for post-hoc analysis.
- **Async throughout**: all LLM calls are async, matching the shared provider's async interface.
- **Type `status`** in the interactive loop to see hub metrics at any time.

## Example Interactions

```
You: What is the Agent Hub pattern?
  [Hub] Routed to 'research' (confidence: 0.95, 180ms)
  Agent: The Agent Hub pattern is a centralized orchestration...

You: Write a summary email about our Q4 results
  [Hub] Routed to 'writer' (confidence: 0.92, 150ms)
  Agent: Subject: Q4 Results Summary...

You: Compare our conversion rates month over month
  [Hub] Routed to 'analyst' (confidence: 0.88, 160ms)
  Agent: To compare conversion rates...
```

## Extending This Example

- Add more specialist agents (code, support, legal, etc.)
- Implement real permissions (API keys, scopes per agent)
- Add conversation memory per user session
- Connect observability to OpenTelemetry / Jaeger
- Implement the hub-as-sidecar or hub-as-control-plane variants
- Add multi-agent coordination for requests that span domains
- Add tool calling via the shared library's `ToolDefinition` support
