"""Provider factory -- the single entry point for getting a provider.

The factory pattern keeps provider construction in one place. Application
code never imports a concrete provider directly; it asks the factory:

    provider = get_provider("openrouter")
    response = await provider.complete(messages)

This means adding a new provider (e.g. Anthropic) requires:
    1. Create providers/anthropic.py implementing LLMProvider
    2. Register it in the PROVIDERS dict below

No application code changes needed.

Related: Chapter 4 (Infrastructure) -- Factory pattern for provider selection.
"""

import logging
import os

from providers import LLMProvider, OpenRouterProvider, OpenAIDirectProvider

logger = logging.getLogger(__name__)

# Registry of available providers.
# Each entry maps a short name to a callable that returns an LLMProvider.
PROVIDERS: dict[str, type[LLMProvider]] = {
    "openrouter": OpenRouterProvider,
    "openai": OpenAIDirectProvider,
}


def get_provider(name: str = "openrouter", **kwargs) -> LLMProvider:
    """Get a provider by name.

    Reads API keys from environment variables.
    Defaults to OpenRouter -- the most flexible single-key option.

    Args:
        name: Provider name ('openrouter', 'openai').
        **kwargs: Passed to the provider constructor (model overrides, etc.).

    Returns:
        An initialized LLMProvider ready to use.

    Raises:
        ValueError: If the provider name is not recognized.

    Example::

        from factory import get_provider
        provider = get_provider("openrouter", model="meta-llama/llama-3-70b")
    """
    provider_cls = PROVIDERS.get(name)
    if provider_cls is None:
        available = ", ".join(sorted(PROVIDERS.keys()))
        raise ValueError(
            f"Unknown provider '{name}'. Available: {available}"
        )

    logger.info("Creating provider: %s", name)
    return provider_cls(**kwargs)


def list_available_providers() -> list[str]:
    """Return names of all registered providers."""
    return sorted(PROVIDERS.keys())


def get_default_provider_name() -> str:
    """Determine the best default provider based on available API keys.

    Checks environment variables and returns the first provider
    that has a configured API key, preferring OpenRouter.
    """
    if os.getenv("OPENROUTER_API_KEY"):
        return "openrouter"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return "openrouter"  # Will fail with a clear error message at init
