"""OpenAI direct API provider implementation.

Uses raw httpx calls to the OpenAI API (no SDK dependency).
The API format is identical to what OpenRouter uses, since
OpenRouter normalizes everything to the OpenAI schema.

API docs: https://platform.openai.com/docs/api-reference/chat

Related: Chapter 4 (Infrastructure) — Provider Abstraction Pattern
"""

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx

from shared.llm_base import (
    ChatMessage,
    ChatResponse,
    LLMProvider,
    StreamChunk,
    ToolCall,
    ToolDefinition,
    UsageInfo,
)
from shared.llm_exceptions import (
    LLMException,
    LLMTimeoutException,
    raise_for_status,
)

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = 'https://api.openai.com/v1'
DEFAULT_MODEL = 'gpt-4o'


class OpenAIProvider(LLMProvider):
    """OpenAI API provider using raw httpx.

    Calls the OpenAI chat completions endpoint directly.
    Supports tool calling and streaming.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        model: str | None = None,
        default_max_tokens: int = 4096,
        default_temperature: float = 0.7,
        organization: str | None = None,
    ):
        super().__init__(
            api_key=api_key,
            base_url=base_url or DEFAULT_BASE_URL,
            model=model or DEFAULT_MODEL,
            default_max_tokens=default_max_tokens,
            default_temperature=default_temperature,
        )
        self.organization = organization

    @property
    def provider_name(self) -> str:
        return 'openai'

    def _get_headers(self) -> dict[str, str]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        if self.organization:
            headers['OpenAI-Organization'] = self.organization
        return headers

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        **kwargs,
    ) -> ChatResponse:
        """Send a chat completion request to OpenAI."""
        model = model or self.model
        url = f'{self.base_url}/chat/completions'

        payload: dict[str, Any] = {
            'model': model,
            'messages': self._prepare_messages(messages),
            'max_tokens': max_tokens or self.default_max_tokens,
            'temperature': temperature
            if temperature is not None
            else self.default_temperature,
        }

        prepared_tools = self._prepare_tools(tools)
        if prepared_tools:
            payload['tools'] = prepared_tools
            payload['tool_choice'] = 'auto'

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    url, json=payload, headers=self._get_headers()
                )

                if response.status_code != 200:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get('error', {}).get(
                        'message', 'Unknown error'
                    )
                    raise_for_status(
                        response.status_code,
                        error_msg,
                        provider=self.provider_name,
                        model=model,
                        raw_response=error_data,
                    )

                data = response.json()
                return self._parse_response(data)

        except httpx.TimeoutException as e:
            raise LLMTimeoutException(
                message='Request timed out',
                provider=self.provider_name,
                model=model,
            ) from e
        except httpx.RequestError as e:
            raise LLMException(
                message=f'Request failed: {e}',
                provider=self.provider_name,
                model=model,
            ) from e

    async def chat_stream(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        **kwargs,
    ) -> AsyncIterator[StreamChunk]:
        """Send a streaming chat completion request to OpenAI."""
        model = model or self.model
        url = f'{self.base_url}/chat/completions'

        payload: dict[str, Any] = {
            'model': model,
            'messages': self._prepare_messages(messages),
            'max_tokens': max_tokens or self.default_max_tokens,
            'temperature': temperature
            if temperature is not None
            else self.default_temperature,
            'stream': True,
        }

        prepared_tools = self._prepare_tools(tools)
        if prepared_tools:
            payload['tools'] = prepared_tools
            payload['tool_choice'] = 'auto'

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    'POST',
                    url,
                    json=payload,
                    headers=self._get_headers(),
                ) as response:
                    if response.status_code != 200:
                        error_body = await response.aread()
                        error_data = json.loads(error_body) if error_body else {}
                        error_msg = error_data.get('error', {}).get(
                            'message', 'Unknown error'
                        )
                        raise_for_status(
                            response.status_code,
                            error_msg,
                            provider=self.provider_name,
                            model=model,
                            raw_response=error_data,
                        )

                    tool_calls_buffer: dict[int, dict] = {}

                    async for line in response.aiter_lines():
                        if not line or not line.startswith('data: '):
                            continue

                        data_str = line[6:]
                        if data_str == '[DONE]':
                            yield StreamChunk(is_final=True)
                            break

                        try:
                            data = json.loads(data_str)
                            chunk = self._parse_stream_chunk(data, tool_calls_buffer)
                            if chunk:
                                yield chunk
                        except json.JSONDecodeError:
                            continue

        except httpx.TimeoutException as e:
            raise LLMTimeoutException(
                message='Stream request timed out',
                provider=self.provider_name,
                model=model,
            ) from e

    def _parse_response(self, data: dict[str, Any]) -> ChatResponse:
        """Parse API response into ChatResponse."""
        choice = data.get('choices', [{}])[0]
        message = choice.get('message', {})

        tool_calls = None
        if 'tool_calls' in message:
            tool_calls = []
            for tc in message['tool_calls']:
                args = tc.get('function', {}).get('arguments', '{}')
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
                tool_calls.append(
                    ToolCall(
                        id=tc.get('id', ''),
                        name=tc.get('function', {}).get('name', ''),
                        arguments=args,
                    )
                )

        usage = None
        if 'usage' in data:
            usage = UsageInfo(
                prompt_tokens=data['usage'].get('prompt_tokens', 0),
                completion_tokens=data['usage'].get('completion_tokens', 0),
                total_tokens=data['usage'].get('total_tokens', 0),
            )

        return ChatResponse(
            content=message.get('content'),
            tool_calls=tool_calls,
            finish_reason=choice.get('finish_reason'),
            usage=usage,
            model=data.get('model'),
        )

    def _parse_stream_chunk(
        self,
        data: dict[str, Any],
        tool_calls_buffer: dict[int, dict],
    ) -> StreamChunk | None:
        """Parse a streaming chunk."""
        choice = data.get('choices', [{}])[0]
        delta = choice.get('delta', {})
        finish_reason = choice.get('finish_reason')

        content = delta.get('content')

        if 'tool_calls' in delta:
            for tc in delta['tool_calls']:
                idx = tc.get('index', 0)
                if idx not in tool_calls_buffer:
                    tool_calls_buffer[idx] = {
                        'id': tc.get('id', ''),
                        'name': tc.get('function', {}).get('name', ''),
                        'arguments': '',
                    }
                else:
                    if 'function' in tc and 'arguments' in tc['function']:
                        tool_calls_buffer[idx]['arguments'] += tc['function'][
                            'arguments'
                        ]

        tool_calls = None
        if finish_reason == 'tool_calls' or (finish_reason and tool_calls_buffer):
            tool_calls = []
            for tc_data in tool_calls_buffer.values():
                try:
                    args = (
                        json.loads(tc_data['arguments']) if tc_data['arguments'] else {}
                    )
                except json.JSONDecodeError:
                    args = {}
                tool_calls.append(
                    ToolCall(
                        id=tc_data['id'],
                        name=tc_data['name'],
                        arguments=args,
                    )
                )

        if content is not None or tool_calls or finish_reason:
            return StreamChunk(
                content=content,
                tool_calls=tool_calls,
                finish_reason=finish_reason,
            )

        return None
