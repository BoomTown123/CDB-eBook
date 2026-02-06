# Provider Abstraction Pattern

A minimal, self-contained example of the **provider abstraction pattern** for LLM APIs.

This pattern lets you switch between LLM providers (OpenRouter, OpenAI, Anthropic, etc.) without changing your application code. It is the simplest form of what Chapter 4 calls the "AI Gateway" -- focused purely on provider interchangeability.

**Related:** Chapter 4 -- Infrastructure for AI-First Companies

## Why Provider Abstraction Matters

Three problems that hit every AI-first company eventually:

1. **Vendor lock-in.** If your application code calls the OpenAI SDK directly, switching to Anthropic means rewriting every call site. A provider layer isolates the change to one file.

2. **Cost optimization.** You want to route simple queries to cheap models and complex ones to expensive models. With an abstraction layer, routing logic lives in one place -- not scattered across your codebase.

3. **Fallback and resilience.** When a provider goes down, you need to fail over to another. An abstract interface makes fallback logic trivial to implement.

## The Pattern

```
Application Code
       |
       v
  LLMProvider (abstract interface)
       ^
       |
  +-----------+-----------+
  |           |           |
OpenRouter  OpenAI    (future)
```

Three layers:

| Layer | File | Purpose |
|-------|------|---------|
| **Interface** | `providers/base.py` | Abstract `LLMProvider` class with `complete()` and `name` |
| **Implementations** | `providers/openrouter.py`, `providers/openai_direct.py` | Concrete providers that talk to specific APIs |
| **Factory** | `factory.py` | Creates providers by name, reads config from env vars |

Application code (like `demo.py`) never imports a concrete provider. It asks the factory for a provider by name and uses the abstract interface.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env with your actual keys

# 3. Run with default provider (OpenRouter)
python demo.py

# 4. Run with a specific provider
python demo.py --provider openai

# 5. Compare providers side-by-side
python demo.py --compare

# 6. Custom prompt
python demo.py --prompt "What is RAG?" --compare

# 7. Verbose mode (see HTTP request details)
python demo.py --compare -v
```

## How to Add a New Provider

Adding a provider (e.g. Anthropic) takes three steps:

### Step 1: Implement the interface

Create `providers/anthropic.py`:

```python
from .base import LLMProvider, Message, Response
import httpx

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key=None, model="claude-sonnet-4-20250514"):
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self._model = model

    @property
    def name(self) -> str:
        return "anthropic"

    async def complete(self, messages: list[Message], **kwargs) -> Response:
        # Anthropic uses a different message format -- the provider
        # handles that translation internally
        ...
```

### Step 2: Register in the factory

In `factory.py`, add one line:

```python
from providers.anthropic import AnthropicProvider

PROVIDERS = {
    "openrouter": OpenRouterProvider,
    "openai": OpenAIDirectProvider,
    "anthropic": AnthropicProvider,  # <-- add this
}
```

### Step 3: Update .env

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

That is it. Every existing call to `get_provider()` can now use `"anthropic"` without any other code changes.

## File Structure

```
provider-abstraction/
    providers/
        __init__.py          # Re-exports for clean imports
        base.py              # Abstract LLMProvider interface
        openrouter.py        # OpenRouter implementation
        openai_direct.py     # Direct OpenAI implementation
    factory.py               # Provider factory (single entry point)
    demo.py                  # Interactive demo script
    .env.example             # Template for API keys
    requirements.txt         # Python dependencies
    README.md                # This file
```

## When to Use This vs. the Full AI Gateway

| Feature | This Pattern | Full AI Gateway (Chapter 4) |
|---------|-------------|----------------------------|
| Provider switching | Yes | Yes |
| Cost-based routing | No | Yes |
| Request caching | No | Yes |
| Rate limiting | No | Yes |
| Observability/logging | Basic | Full tracing |
| Streaming support | No | Yes |
| Fallback chains | No | Yes |
| Semantic caching | No | Yes |

**Use this pattern when:**
- You are early stage and need to move fast
- You have 1-2 providers and want the option to switch
- You want a clean architecture without over-engineering

**Graduate to a full AI Gateway when:**
- You are routing thousands of requests per minute
- You need caching, rate limiting, or cost controls
- You have 3+ providers with complex routing rules
- You need production observability (traces, cost tracking)

## Design Decisions

**Why httpx instead of provider SDKs?** Both OpenRouter and OpenAI use the same REST API format. Using httpx directly keeps the dependency count low and makes the HTTP communication transparent -- important for a learning example.

**Why async?** LLM API calls are I/O-bound and often take 1-5 seconds. Async lets you run multiple provider calls concurrently (as `--compare` mode does implicitly). Real applications will want this for parallel tool calls and streaming.

**Why dataclasses for Message and Response?** They are simple, built into Python, and do not require any additional dependencies. In production you might graduate to Pydantic models for validation.
