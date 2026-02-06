"""
Anthropic provider adapter for the AI Gateway.

Uses raw httpx instead of the anthropic SDK. Note how Anthropic's
system-message convention differs from OpenAI's --- the system prompt
is a top-level parameter, not a message role. The adapter handles
that translation so the gateway stays provider-agnostic.

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
    MessageRole,
    ToolCall,
    Usage,
)

logger = logging.getLogger("ai_gateway.anthropic")

_BASE_URL = "https://api.anthropic.com/v1"
_API_VERSION = "2023-06-01"


class AnthropicProvider(BaseProvider):
    """
    Anthropic adapter using raw httpx.

    Handles the API differences --- Anthropic takes `system` as a
    top-level parameter rather than a message role, and uses `max_tokens`
    as a required field. The adapter normalizes these differences so the
    gateway never has to care.
    """

    def __init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY environment variable is required")
        self._api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=_BASE_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": _API_VERSION,
                "content-type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def available_models(self) -> list[str]:
        return [
            "claude-opus-4-5-20251101",
            "claude-sonnet-4-20250514",
            "claude-haiku-3-5-20241022",
        ]

    def _build_payload(self, request: CompletionRequest, stream: bool = False) -> dict:
        """Build the JSON payload for Anthropic's messages endpoint.

        Anthropic's format differs from OpenAI:
        - System message is a top-level param, not in the messages array
        - Uses input_tokens/output_tokens instead of prompt_tokens/completion_tokens
        - Content blocks use {"type": "text", "text": "..."} format
        """
        system_text = ""
        messages = []
        for msg in request.messages:
            if msg.role == MessageRole.SYSTEM:
                system_text = msg.content
            else:
                messages.append({"role": msg.role.value, "content": msg.content})

        payload: dict = {
            "model": request.model,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
        if system_text:
            payload["system"] = system_text
        if stream:
            payload["stream"] = True
        if request.tools:
            payload["tools"] = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.parameters,
                }
                for t in request.tools
            ]
        return payload

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Send a completion request to Anthropic via raw HTTP."""
        start = time.monotonic()

        payload = self._build_payload(request)
        resp = await self._client.post("/messages", json=payload)

        if resp.status_code != 200:
            body = resp.text
            logger.error("Anthropic API error %d: %s", resp.status_code, body)
            raise RuntimeError(
                f"Anthropic API returned {resp.status_code}: {body}"
            )

        data = resp.json()
        latency_ms = (time.monotonic() - start) * 1000

        # Extract text from content blocks
        content = ""
        tool_calls = None
        for block in data.get("content", []):
            if block.get("type") == "text":
                content += block.get("text", "")
            elif block.get("type") == "tool_use":
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append(
                    ToolCall(
                        id=block["id"],
                        name=block["name"],
                        arguments=json.dumps(block.get("input", {})),
                    )
                )

        usage_data = data.get("usage", {})
        input_tokens = usage_data.get("input_tokens", 0)
        output_tokens = usage_data.get("output_tokens", 0)

        return CompletionResponse(
            content=content,
            model=data.get("model", request.model),
            provider=self.name,
            usage=Usage(
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
            ),
            tool_calls=tool_calls,
            latency_ms=latency_ms,
        )

    async def stream(self, request: CompletionRequest) -> AsyncIterator[str]:
        """Stream tokens from Anthropic using server-sent events.

        Anthropic uses a different SSE event format than OpenAI:
        - event: content_block_delta  (contains the text chunks)
        - event: message_stop         (signals end of stream)
        """
        payload = self._build_payload(request, stream=True)

        async with self._client.stream("POST", "/messages", json=payload) as resp:
            if resp.status_code != 200:
                body = await resp.aread()
                raise RuntimeError(
                    f"Anthropic API returned {resp.status_code}: {body.decode()}"
                )

            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                data_str = line[len("data: "):]
                try:
                    chunk = json.loads(data_str)
                    # Anthropic sends content_block_delta events with text
                    if chunk.get("type") == "content_block_delta":
                        delta = chunk.get("delta", {})
                        if delta.get("type") == "text_delta":
                            text = delta.get("text", "")
                            if text:
                                yield text
                except (json.JSONDecodeError, KeyError):
                    continue

    async def health_check(self) -> bool:
        """Verify Anthropic is reachable with a minimal request."""
        try:
            resp = await self._client.post(
                "/messages",
                json={
                    "model": "claude-haiku-3-5-20241022",
                    "max_tokens": 1,
                    "messages": [{"role": "user", "content": "ping"}],
                },
            )
            return resp.status_code == 200
        except Exception:
            return False
