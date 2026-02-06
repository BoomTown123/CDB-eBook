"""Factory for creating LLM provider instances.

Provides a single entry point for getting a configured provider.
Unlike the production version (which uses Flask's current_app),
this version accepts arguments directly for portability.

Related: Chapter 4 (Infrastructure) — Provider Abstraction Pattern
"""

import os

from shared.llm_base import LLMProvider
from shared.llm_exceptions import LLMException
from shared.providers.openai_provider import OpenAIProvider
from shared.providers.openrouter import OpenRouterProvider


def get_provider(
    provider_name: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
    **kwargs,
) -> LLMProvider:
    """Get an LLM provider instance by name.

    If no provider_name is given, defaults to 'openrouter'.
    If no api_key is given, reads from environment variables.

    Args:
        provider_name: 'openrouter' or 'openai' (default: 'openrouter')
        model: Model to use (provider-specific, e.g. 'google/gemini-2.5-flash')
        api_key: API key (defaults to env var for the provider)
        **kwargs: Additional provider-specific arguments

    Returns:
        Configured LLMProvider instance

    Raises:
        LLMException: If provider name is unknown or API key is missing

    Example:
        # Uses OPENROUTER_API_KEY from environment
        provider = get_provider()

        # Explicit provider and key
        provider = get_provider('openai', api_key='sk-...')

        # With model override
        provider = get_provider('openrouter', model='anthropic/claude-sonnet-4.5')
    """
    provider_name = (provider_name or os.getenv('LLM_PROVIDER', 'openrouter')).lower()

    if provider_name == 'openrouter':
        api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise LLMException(
                message='OPENROUTER_API_KEY not set. Get one at https://openrouter.ai/keys',
                provider='openrouter',
            )

        return OpenRouterProvider(
            api_key=api_key,
            model=model or os.getenv('MODEL', 'google/gemini-2.5-flash'),
            site_url=os.getenv('SITE_URL'),
            site_name=os.getenv('SITE_NAME'),
            **kwargs,
        )

    elif provider_name == 'openai':
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise LLMException(
                message='OPENAI_API_KEY not set',
                provider='openai',
            )

        return OpenAIProvider(
            api_key=api_key,
            model=model or os.getenv('MODEL', 'gpt-4o'),
            organization=os.getenv('OPENAI_ORGANIZATION'),
            **kwargs,
        )

    else:
        raise LLMException(
            message=f'Unknown provider: {provider_name}. Use "openrouter" or "openai".',
            provider=provider_name,
        )


def get_available_providers() -> list[str]:
    """Get list of providers with API keys configured."""
    providers = []
    if os.getenv('OPENROUTER_API_KEY'):
        providers.append('openrouter')
    if os.getenv('OPENAI_API_KEY'):
        providers.append('openai')
    return providers
