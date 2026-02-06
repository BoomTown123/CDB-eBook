"""Shared LLM provider library for book examples.

Provides a provider abstraction layer, MCP client, and common data types
for interacting with LLM APIs. Based on production patterns from the
Yirifi Ops Agents Dashboard.

Usage:
    from shared import get_provider, ChatMessage, MessageRole

    provider = get_provider('openrouter', api_key='sk-or-...')
    response = await provider.chat([
        ChatMessage(role=MessageRole.USER, content='Hello!')
    ])
"""

from shared.llm_base import (
    ChatMessage,
    ChatResponse,
    LLMProvider,
    MessageRole,
    StreamChunk,
    ToolCall,
    ToolDefinition,
    UsageInfo,
)
from shared.llm_exceptions import (
    LLMAuthException,
    LLMException,
    LLMRateLimitException,
    LLMTimeoutException,
)
from shared.llm_factory import get_provider

__all__ = [
    'ChatMessage',
    'ChatResponse',
    'LLMProvider',
    'MessageRole',
    'StreamChunk',
    'ToolCall',
    'ToolDefinition',
    'UsageInfo',
    'LLMException',
    'LLMAuthException',
    'LLMRateLimitException',
    'LLMTimeoutException',
    'get_provider',
]
