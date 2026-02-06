"""Configuration for the streaming chat agent.

Loads settings from environment variables. Copy .env.example to .env
and fill in your API key before running.

Book reference: Chapter 6 - Agent Architecture, Section 1
"""

import os
from dataclasses import dataclass


@dataclass
class StreamingConfig:
    """Configuration for the streaming chat agent.

    Supports two modes:
    - Without MCP: Pure streaming text generation (no tools)
    - With MCP: Streaming text + tool calling via MCP server

    Set MCP_SERVER_URL to enable tool calling. The agent degrades
    gracefully when no MCP server is configured.
    """

    provider_name: str
    api_key: str
    model: str
    mcp_server_url: str | None = None
    mcp_api_key: str | None = None
    max_tokens: int = 4096
    temperature: float = 0.7

    @classmethod
    def from_env(cls) -> 'StreamingConfig':
        """Load configuration from environment variables.

        Required:
            OPENROUTER_API_KEY: API key for the LLM provider

        Optional:
            LLM_PROVIDER: 'openrouter' or 'openai' (default: 'openrouter')
            MODEL: Model identifier (default: 'google/gemini-2.5-flash')
            MCP_SERVER_URL: URL of the MCP server for tool calling
            MCP_API_KEY: API key for the MCP server
            MAX_TOKENS: Maximum tokens per response (default: 4096)
            TEMPERATURE: Sampling temperature (default: 0.7)

        Raises:
            ValueError: If required environment variables are missing.
        """
        provider_name = os.environ.get('LLM_PROVIDER', 'openrouter')

        # Resolve API key based on provider
        if provider_name == 'openai':
            api_key = os.environ.get('OPENAI_API_KEY', '')
            default_model = 'gpt-4o'
        else:
            api_key = os.environ.get('OPENROUTER_API_KEY', '')
            default_model = 'google/gemini-2.5-flash'

        if not api_key:
            key_name = (
                'OPENAI_API_KEY' if provider_name == 'openai' else 'OPENROUTER_API_KEY'
            )
            raise ValueError(
                f'{key_name} not set. '
                'Copy .env.example to .env and add your key.'
            )

        return cls(
            provider_name=provider_name,
            api_key=api_key,
            model=os.environ.get('MODEL', default_model),
            mcp_server_url=os.environ.get('MCP_SERVER_URL'),
            mcp_api_key=os.environ.get('MCP_API_KEY'),
            max_tokens=int(os.environ.get('MAX_TOKENS', '4096')),
            temperature=float(os.environ.get('TEMPERATURE', '0.7')),
        )
