"""Direct OpenAI provider implementation.

Calls the OpenAI API directly using httpx -- no SDK dependency.
This keeps the example minimal and shows that the OpenAI chat
completions format is just a REST API under the hood.

API docs: https://platform.openai.com/docs/api-reference/chat
"""

import logging
import os

import httpx

from .base import LLMProvider, Message, Response

logger = logging.getLogger(__name__)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o"


class OpenAIDirectProvider(LLMProvider):
    """LLM provider that calls OpenAI directly.

    Uses raw HTTP via httpx rather than the openai Python SDK.
    This keeps the dependency footprint small and makes the
    request/response cycle transparent for learning purposes.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: Model identifier (e.g. 'gpt-4o', 'gpt-4o-mini').
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
    ):
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY or pass api_key."
            )
        self._model = model

    @property
    def name(self) -> str:
        return "openai"

    async def complete(self, messages: list[Message], **kwargs) -> Response:
        """Send a completion request to OpenAI.

        The request format is identical to OpenRouter -- both use
        the OpenAI chat completions schema. This makes it easy to
        swap providers without changing payload structure.
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": kwargs.pop("model", self._model),
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            **kwargs,
        }

        logger.info("OpenAI request: model=%s, messages=%d", payload["model"], len(messages))

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(OPENAI_API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        choice = data["choices"][0]["message"]
        usage = data.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)

        logger.info("OpenAI response: tokens=%d", total_tokens)

        return Response(
            content=choice["content"],
            model=data.get("model", payload["model"]),
            tokens_used=total_tokens,
        )
