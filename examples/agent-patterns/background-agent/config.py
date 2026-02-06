"""
Configuration for the background agent.

Loads settings from environment variables. Copy .env.example to .env
and fill in your API key before running.

Book reference: Chapter 6, Section 1 - The 2 Agent Types You Need
"""

import os
from dataclasses import dataclass


@dataclass
class BackgroundAgentConfig:
    """Configuration for the background agent."""

    provider_name: str = "openrouter"
    api_key: str = ""
    model: str = "google/gemini-2.5-flash"
    max_retries: int = 3
    task_timeout_seconds: int = 300
    polling_interval_seconds: int = 10
    max_tokens_per_request: int = 2048
    token_budget: int = 50_000  # Total token budget per run
    cost_budget_usd: float = 1.00  # Cost ceiling per run

    @classmethod
    def from_env(cls) -> "BackgroundAgentConfig":
        """Load configuration from environment variables."""
        provider_name = os.environ.get("LLM_PROVIDER", "openrouter")
        api_key = os.environ.get("OPENROUTER_API_KEY", "")

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not set. "
                "Copy .env.example to .env and add your key. "
                "Get one at https://openrouter.ai/keys"
            )

        return cls(
            provider_name=provider_name,
            api_key=api_key,
            model=os.environ.get("MODEL", "google/gemini-2.5-flash"),
            max_retries=int(os.environ.get("BG_AGENT_MAX_RETRIES", "3")),
            task_timeout_seconds=int(
                os.environ.get("BG_AGENT_TIMEOUT", "300")
            ),
            polling_interval_seconds=int(
                os.environ.get("BG_AGENT_POLL_INTERVAL", "10")
            ),
            token_budget=int(
                os.environ.get("BG_AGENT_TOKEN_BUDGET", "50000")
            ),
            cost_budget_usd=float(
                os.environ.get("BG_AGENT_COST_BUDGET", "1.00")
            ),
        )
