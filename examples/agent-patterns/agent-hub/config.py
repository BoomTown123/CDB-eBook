"""
Configuration for the agent hub.

Loads settings from environment variables. Copy .env.example to .env
and fill in your API key before running.

Two-model architecture:
- router_model: cheap/fast model for intent classification (e.g. Gemini Flash)
- agent_model: capable model for specialist work (e.g. Claude Sonnet)
Both go through OpenRouter with different model IDs.

Book reference: Chapter 6, Section 2 - The Agent Hub Pattern
"""

import os
from dataclasses import dataclass, field


@dataclass
class AgentHubConfig:
    """Configuration for the agent hub and its specialist agents.

    The two-model pattern keeps routing costs low while giving specialist
    agents a capable model. Both models are accessed through the same
    provider (OpenRouter) -- only the model ID differs.
    """

    api_key: str
    provider_name: str = "openrouter"
    router_model: str = "google/gemini-2.5-flash"  # Cheap/fast for routing
    agent_model: str = "anthropic/claude-sonnet-4.5"  # Capable for execution
    max_tokens_per_response: int = 1024
    temperature: float = 0.7
    max_routing_retries: int = 2
    rate_limit: int = 50
    circuit_breaker_threshold: int = 3
    available_agents: list[str] = field(
        default_factory=lambda: ["research", "writer", "analyst"]
    )

    @classmethod
    def from_env(cls) -> "AgentHubConfig":
        """Load configuration from environment variables."""
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not set. "
                "Copy .env.example to .env and add your key. "
                "Get one at https://openrouter.ai/keys"
            )
        return cls(
            api_key=api_key,
            provider_name=os.environ.get("LLM_PROVIDER", "openrouter"),
            router_model=os.environ.get(
                "HUB_ROUTER_MODEL", "google/gemini-2.5-flash"
            ),
            agent_model=os.environ.get(
                "HUB_AGENT_MODEL", "anthropic/claude-sonnet-4.5"
            ),
            max_tokens_per_response=int(
                os.environ.get("HUB_MAX_TOKENS", "1024")
            ),
            rate_limit=int(os.environ.get("HUB_RATE_LIMIT", "50")),
            circuit_breaker_threshold=int(
                os.environ.get("HUB_CIRCUIT_BREAKER_THRESHOLD", "3")
            ),
        )
