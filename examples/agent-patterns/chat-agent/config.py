"""
Configuration for the chat agent.

Loads settings from environment variables. Copy .env.example to .env
and fill in your API key before running.

Uses the shared provider library — provider_name selects the backend
(OpenRouter by default, or OpenAI directly).

Book reference: Chapter 6, Section 1 - The 2 Agent Types You Need
"""

import os
from dataclasses import dataclass


@dataclass
class ChatAgentConfig:
    """Provider-agnostic configuration for the chat agent."""

    provider_name: str
    api_key: str
    model: str
    max_conversation_turns: int = 20
    max_tokens_per_response: int = 4096
    temperature: float = 0.7
    context_summary_interval: int = 10  # Summarize every N turns

    @classmethod
    def from_env(cls) -> "ChatAgentConfig":
        """Load configuration from environment variables.

        Reads provider name and API key from the environment.  Supports
        both OpenRouter (default) and OpenAI as backends.
        """
        provider_name = os.environ.get("LLM_PROVIDER", "openrouter").lower()

        # Resolve API key based on provider
        if provider_name == "openai":
            api_key = os.environ.get("OPENAI_API_KEY", "")
            default_model = "gpt-4o"
        else:
            api_key = os.environ.get("OPENROUTER_API_KEY", "")
            default_model = "google/gemini-2.5-flash"

        if not api_key:
            key_var = (
                "OPENAI_API_KEY" if provider_name == "openai"
                else "OPENROUTER_API_KEY"
            )
            raise ValueError(
                f"{key_var} not set. "
                "Copy .env.example to .env and add your key."
            )

        return cls(
            provider_name=provider_name,
            api_key=api_key,
            model=os.environ.get("MODEL", default_model),
            max_conversation_turns=int(
                os.environ.get("CHAT_AGENT_MAX_TURNS", "20")
            ),
            max_tokens_per_response=int(
                os.environ.get("CHAT_AGENT_MAX_TOKENS", "4096")
            ),
            temperature=float(
                os.environ.get("CHAT_AGENT_TEMPERATURE", "0.7")
            ),
        )
