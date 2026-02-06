"""OpenRouter LLM provider implementation.

OpenRouter provides a unified API for accessing models from Anthropic,
Google, OpenAI, DeepSeek, and others through a single endpoint. It uses
the OpenAI-compatible chat completions format.

API docs: https://openrouter.ai/docs/api/reference/overview
Tool calling: https://openrouter.ai/docs/guides/features/tool-calling

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

DEFAULT_BASE_URL = 'https://openrouter.ai/api/v1'
DEFAULT_MODEL = 'google/gemini-2.5-flash'

# Models with reliable tool calling support (verified Feb 2026)
# Filter by tool support: https://openrouter.ai/models?supported_parameters=tools
TOOL_CAPABLE_MODELS = {
    'anthropic/claude-sonnet-4.5',
    'anthropic/claude-opus-4.5',
    'anthropic/claude-sonnet-4',
    'anthropic/claude-haiku-4.5',
    'openai/gpt-5.2',
    'openai/gpt-5',
    'openai/gpt-4o',
    'openai/gpt-4.1',
    'google/gemini-3-flash-preview',
    'google/gemini-2.5-flash',
    'google/gemini-2.0-flash-001',
}

# Models with known unstable tool calling — use with caution
UNSTABLE_TOOL_MODELS = {
    'deepseek/deepseek-chat',
    'deepseek/deepseek-v3',
    'deepseek/deepseek-v3.2',
    'deepseek/deepseek-chat-v3',
}


class OpenRouterProvider(LLMProvider):
    """OpenRouter API provider supporting multiple model providers.

    OpenRouter routes requests to the underlying provider (Anthropic,
    Google, OpenAI, etc.) while normalizing the API format. This means
    you can switch between Claude, Gemini, and GPT models without
    changing your code.

    When tools are included in a request, OpenRouter only routes to
    providers that support tool use for the selected model.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        model: str | None = None,
        default_max_tokens: int = 4096,
        default_temperature: float = 0.7,
        site_url: str | None = None,
        site_name: str | None = None,
    ):
        """Initialize OpenRouter provider.

        Args:
            api_key: OpenRouter API key (starts with sk-or-)
            base_url: Base URL (defaults to https://openrouter.ai/api/v1)
            model: Default model (e.g. 'google/gemini-2.5-flash')
            default_max_tokens: Default max tokens for responses
            default_temperature: Default temperature for sampling
            site_url: Your site URL for OpenRouter rankings (optional)
            site_name: Your site name for OpenRouter rankings (optional)
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url or DEFAULT_BASE_URL,
            model=model or DEFAULT_MODEL,
            default_max_tokens=default_max_tokens,
            default_temperature=default_temperature,
        )
        self.site_url = site_url
        self.site_name = site_name

    @property
    def provider_name(self) -> str:
        return 'openrouter'

    def _get_headers(self) -> dict[str, str]:
        """Get request headers.

        Required: Authorization (Bearer token)
        Optional: HTTP-Referer and X-Title for OpenRouter rankings
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        if self.site_url:
            headers['HTTP-Referer'] = self.site_url
        if self.site_name:
            headers['X-Title'] = self.site_name
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
        """Send a chat completion request to OpenRouter.

        The request format follows the OpenAI chat completions API.
        OpenRouter transforms it as needed for the underlying provider.
        """
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

        # Add tools in OpenAI function calling format.
        # OpenRouter requires tools in every request of a tool-calling
        # conversation (both the initial request and follow-up with results).
        prepared_tools = self._prepare_tools(tools)
        if prepared_tools:
            payload['tools'] = prepared_tools
            payload['tool_choice'] = 'auto'
            logger.info(
                'Sending %d tools to OpenRouter: %s',
                len(prepared_tools),
                [t['function']['name'] for t in prepared_tools],
            )

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
        """Send a streaming chat completion request.

        Streams responses as Server-Sent Events (SSE). Each event
        contains a delta with incremental content or tool calls.
        The stream ends with a 'data: [DONE]' sentinel.
        """
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

                    # Buffer for accumulating streamed tool calls.
                    # Tool call arguments arrive in fragments across
                    # multiple SSE events and must be reassembled.
                    tool_calls_buffer: dict[int, dict] = {}

                    async for line in response.aiter_lines():
                        if not line or not line.startswith('data: '):
                            continue

                        data_str = line[6:]  # Remove 'data: ' prefix
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
        """Parse a non-streaming API response into ChatResponse."""
        choice = data.get('choices', [{}])[0]
        message = choice.get('message', {})

        # Parse tool calls if present
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

        # Parse usage info
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
        """Parse a single SSE streaming chunk.

        Tool calls arrive fragmented across multiple chunks:
        - First chunk has the tool call id and function name
        - Subsequent chunks append to the arguments string
        - Final chunk has finish_reason='tool_calls'

        We buffer these fragments and emit the complete tool calls
        only when the finish_reason indicates they're ready.
        """
        choice = data.get('choices', [{}])[0]
        delta = choice.get('delta', {})
        finish_reason = choice.get('finish_reason')

        content = delta.get('content')

        # Accumulate tool call fragments
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

        # When finished, parse the accumulated tool calls
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
