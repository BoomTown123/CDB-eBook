"""OpenRouter provider implementation.

OpenRouter aggregates 200+ models behind a single OpenAI-compatible API.
This makes it ideal as a default provider: one API key gives you access
to Google, Meta, Mistral, and many other models.

API docs: https://openrouter.ai/docs
"""

import logging
import os

import httpx

from .base import LLMProvider, Message, Response

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash"


class OpenRouterProvider(LLMProvider):
    """LLM provider backed by OpenRouter.

    OpenRouter routes requests to the underlying model provider
    (Google, OpenAI, Anthropic, etc.) and handles authentication,
    rate limiting, and billing through a single API key.

    Args:
        api_key: OpenRouter API key. Falls back to OPENROUTER_API_KEY env var.
        model: Model identifier (e.g. 'google/gemini-2.5-flash').
        site_url: Optional HTTP-Referer for OpenRouter analytics.
        site_name: Optional X-Title for OpenRouter analytics.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        site_url: str | None = None,
        site_name: str | None = None,
    ):
        self._api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self._api_key:
            raise ValueError(
                "OpenRouter API key required. Set OPENROUTER_API_KEY or pass api_key."
            )
        self._model = model
        self._site_url = site_url
        self._site_name = site_name

    @property
    def name(self) -> str:
        return "openrouter"

    async def complete(self, messages: list[Message], **kwargs) -> Response:
        """Send a completion request to OpenRouter.

        Uses the standard OpenAI chat completions format, which
        OpenRouter supports natively.
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        if self._site_url:
            headers["HTTP-Referer"] = self._site_url
        if self._site_name:
            headers["X-Title"] = self._site_name

        payload = {
            "model": kwargs.pop("model", self._model),
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            **kwargs,
        }

        logger.info("OpenRouter request: model=%s, messages=%d", payload["model"], len(messages))

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(OPENROUTER_API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        choice = data["choices"][0]["message"]
        usage = data.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)

        logger.info("OpenRouter response: tokens=%d", total_tokens)

        return Response(
            content=choice["content"],
            model=data.get("model", payload["model"]),
            tokens_used=total_tokens,
        )
