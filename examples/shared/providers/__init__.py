"""LLM provider implementations.

Each provider implements the LLMProvider interface using raw httpx
calls (no SDK dependencies). OpenRouter is the primary provider.
"""

from shared.providers.openai_provider import OpenAIProvider
from shared.providers.openrouter import OpenRouterProvider

__all__ = ['OpenRouterProvider', 'OpenAIProvider']
