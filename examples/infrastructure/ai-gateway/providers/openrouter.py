"""
OpenRouter provider adapter for the AI Gateway.

OpenRouter is the PRIMARY provider for this gateway. It gives you access
to dozens of models (OpenAI, Anthropic, Google, Meta, Mistral, etc.)
through a single OpenAI-compatible API, which means one API key covers
multiple backends and you get built-in model fallback at the routing
layer.

Why OpenRouter first:
- Single API key, many models --- reduces secret management overhead
- OpenAI-compatible format --- same payload shape as direct OpenAI calls
- Built-in rate limiting and usage tracking on their dashboard
- Easy to swap models without changing provider code

Reference: Chapter 4 - The AI Tool Gateway Pattern
"""

import json
import logging
import os
import time
from typing import AsyncIterator

import httpx

from .base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ToolCall,
    Usage,
)

logger = logging.getLogger("ai_gateway.openrouter")

_BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter adapter using raw httpx.

    OpenRouter uses the OpenAI-compatible chat completions format, so the
    payload shape is identical to the OpenAI provider. The only differences
    are the base URL, auth header, and optional metadata headers.

    Default model: google/gemini-2.5-flash --- fast, cheap, and capable
    enough for most gateway routing scenarios.
    """

    def __init__(self) -> None:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENROUTER_API_KEY environment variable is required"
            )
        self._api_key = api_key

        headers: dict[str, str] = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Optional metadata headers for OpenRouter dashboard attribution
        referer = os.environ.get("OPENROUTER_REFERER")
        if referer:
            headers["HTTP-Referer"] = referer
        title = os.environ.get("OPENROUTER_TITLE")
        if title:
            headers["X-Title"] = title

        self._client = httpx.AsyncClient(
            base_url=_BASE_URL,
            headers=headers,
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

    @property
    def name(self) -> str:
        return "openrouter"

    @property
    def available_models(self) -> list[str]:
        return [
            "google/gemini-2.5-flash",
            "google/gemini-2.5-pro",
            "anthropic/claude-sonnet-4",
            "anthropic/claude-haiku-3.5",
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "meta-llama/llama-3.3-70b-instruct",
            "mistralai/mistral-large",
        ]

    def _build_payload(self, request: CompletionRequest, stream: bool = False) -> dict:
        """Build the JSON payload --- OpenAI-compatible format."""
        messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in request.messages
        ]
        payload: dict = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if stream:
            payload["stream"] = True
        if request.tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters,
                    },
                }
                for t in request.tools
            ]
        return payload

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Send a completion request to OpenRouter via raw HTTP."""
        start = time.monotonic()

        payload = self._build_payload(request)
        resp = await self._client.post("/chat/completions", json=payload)

        if resp.status_code != 200:
            body = resp.text
            logger.error("OpenRouter API error %d: %s", resp.status_code, body)
            raise RuntimeError(
                f"OpenRouter API returned {resp.status_code}: {body}"
            )

        data = resp.json()
        latency_ms = (time.monotonic() - start) * 1000

        choice = data["choices"][0]
        message = choice["message"]
        usage_data = data.get("usage", {})

        # Parse tool calls if present
        tool_calls = None
        if message.get("tool_calls"):
            tool_calls = [
                ToolCall(
                    id=tc["id"],
                    name=tc["function"]["name"],
                    arguments=tc["function"]["arguments"],
                )
                for tc in message["tool_calls"]
            ]

        return CompletionResponse(
            content=message.get("content") or "",
            model=data.get("model", request.model),
            provider=self.name,
            usage=Usage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0),
            ),
            tool_calls=tool_calls,
            latency_ms=latency_ms,
        )

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream tokens from OpenRouter using server-sent events.

        Same SSE format as OpenAI since OpenRouter is API-compatible.
        """
        payload = self._build_payload(request, stream=True)

        async with self._client.stream(
            "POST", "/chat/completions", json=payload
        ) as resp:
            if resp.status_code != 200:
                body = await resp.aread()
                raise RuntimeError(
                    f"OpenRouter API returned {resp.status_code}: {body.decode()}"
                )

            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[len("data: "):]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content")
                    if content:
                        yield content
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

    async def health_check(self) -> bool:
        """Verify OpenRouter is reachable by listing models."""
        try:
            resp = await self._client.get("/models")
            return resp.status_code == 200
        except Exception:
            return False
