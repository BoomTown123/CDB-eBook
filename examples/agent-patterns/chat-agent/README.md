# Chat Agent

Interactive conversational agent with tool use and conversation management.

**Book reference:** Chapter 6 - Agent Architecture, Sections 1 and 6

## What This Demonstrates

Chat agents enable humans to accomplish tasks through conversation. A human is waiting. Speed matters. The agent responds in seconds.

This example implements the five chat agent design patterns from the book:

1. **Clarification loops** - Asks before guessing when requests are ambiguous
2. **Graceful handoff** - Transfers to humans with full context when stuck
3. **Context persistence** - Maintains conversation history, summarizes periodically
4. **Action confirmation** - Matches verification level to action risk
5. **Progress visibility** - Reports status during multi-step operations

## Files

| File | Purpose |
|------|---------|
| `agent.py` | Async chat loop with conversation management and tool-use cycle |
| `tools.py` | Tool definitions using shared `ToolDefinition` objects |
| `prompts.py` | System prompts and prompt templates |
| `config.py` | Provider-agnostic configuration via environment variables |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your OpenRouter API key (get one at https://openrouter.ai/keys)

# Run
python agent.py
```

### Using OpenAI Instead

Edit your `.env` to switch providers:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
MODEL=gpt-4o
```

## How It Works

```
User message
    |
    v
[Add to conversation history]
    |
    v
[Summarize context if turn count % 10 == 0]
    |
    v
[Call LLM via shared provider with tools]
    |
    +-- LLM requests tool call --> [Execute tool] --> [Feed result back to LLM]
    |
    +-- LLM returns text --> [Display to user]
```

The agent maintains a message history and periodically summarizes it to stay within token limits (the "context persistence" pattern). When the LLM decides a tool would help, it enters a tool-use loop: call tool, feed result back, repeat until the LLM produces a text response.

All LLM calls go through the shared provider library (`examples/shared/`), which supports OpenRouter and OpenAI backends. The provider abstraction means you can switch between Gemini, Claude, and GPT models by changing one environment variable.

## Key Design Decisions

- **Provider abstraction** uses the shared library so the agent code has zero direct HTTP or SDK calls.
- **Async throughout** -- the agent class and main loop are async, matching the shared provider interface.
- **Context summarization** happens every 10 turns to prevent token overflow while preserving conversation continuity.
- **Tool-use loop** has a maximum of 5 rounds to prevent infinite tool chains.
- **Handoff** command (`handoff`) demonstrates graceful transfer with context serialization.
- **Session limits** enforce a maximum turn count to bound costs.

## Extending This Example

- Add real tools (web search API, database queries, file system access)
- Add a vector store for long-term memory across sessions
- Implement action confirmation for write operations
- Add streaming responses for better perceived latency (use `provider.chat_stream()`)
- Switch providers at runtime by changing `LLM_PROVIDER`
