"""Streaming Chat Agent - SSE streaming with tool calling via MCP.

Demonstrates the streaming response loop pattern from Chapter 6:
1. Stream content tokens from the LLM
2. Detect tool calls in the stream
3. Execute tools via MCP
4. Feed results back to the LLM
5. Continue streaming until no more tool calls

This is the core pattern used in production chat services where
low-latency, token-by-token delivery matters. The agent emits
Server-Sent Events (SSE) so any HTTP client or frontend can
consume the stream incrementally.

Run:
    python streaming_chat.py

Book reference: Chapter 6 - Agent Architecture
"""

import asyncio
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from collections.abc import AsyncIterator

# Add the shared library to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared import ChatMessage, MessageRole, ToolCall, get_provider
from shared.llm_base import LLMProvider
from shared.llm_exceptions import LLMException
from shared.mcp_client import MCPClient, MCPServerConfig, MCPToolError

from config import StreamingConfig

logger = logging.getLogger(__name__)

MAX_TOOL_ITERATIONS = 10


# ---------------------------------------------------------------------------
# Chat Events
# ---------------------------------------------------------------------------

@dataclass
class ChatEvent:
    """Event emitted during streaming chat.

    Each event has a type and a data payload. Events are designed to be
    serialized as Server-Sent Events (SSE) for HTTP streaming, but can
    also be consumed directly in Python via the async generator.

    Event types:
    - content:        Incremental text content (token by token)
    - tool_calls:     Tools the model wants to call
    - tool_executing: Tool execution has started
    - tool_result:    Result of tool execution
    - done:           Stream complete, final content available
    - error:          Error occurred during processing
    """

    event_type: str
    data: dict[str, Any]

    def to_sse(self) -> str:
        """Format as a Server-Sent Event.

        SSE format:
            event: <type>
            data: <json>
            <blank line>

        This is the standard format consumed by EventSource in browsers
        and httpx-sse / aiohttp in Python clients.
        """
        return f'event: {self.event_type}\ndata: {json.dumps(self.data)}\n\n'

    def __repr__(self) -> str:
        truncated = str(self.data)
        if len(truncated) > 80:
            truncated = truncated[:77] + '...'
        return f'ChatEvent({self.event_type!r}, {truncated})'


# ---------------------------------------------------------------------------
# Streaming Chat Agent
# ---------------------------------------------------------------------------

class StreamingChatAgent:
    """Chat agent that streams responses with automatic tool calling.

    The key pattern is the stream-execute-continue loop:

        while iterations remain:
            stream LLM response (yielding content tokens)
            if no tool calls -> done
            execute tools via MCP
            append tool results to message history
            continue streaming

    This allows the frontend to display partial text immediately while
    the agent works through multi-step tool use in the background.

    Works without an MCP server -- in that case, no tools are provided
    to the LLM and the agent simply streams text responses.
    """

    def __init__(
        self,
        provider: LLMProvider,
        mcp_client: MCPClient | None = None,
    ) -> None:
        """Initialize the streaming chat agent.

        Args:
            provider: LLM provider instance (from shared.llm_factory)
            mcp_client: Optional MCP client for tool calling.
                        If None, the agent streams text without tools.
        """
        self.provider = provider
        self.mcp_client = mcp_client

    # ------------------------------------------------------------------
    # Core streaming loop
    # ------------------------------------------------------------------

    async def stream_with_tools(
        self,
        user_message: str,
        system_prompt: str = 'You are a helpful assistant.',
    ) -> AsyncIterator[ChatEvent]:
        """Stream a response with automatic tool calling.

        This is the core pattern: stream LLM output, detect tool calls,
        execute them via MCP, feed results back, and continue streaming.
        Maximum MAX_TOOL_ITERATIONS rounds of tool calling to prevent
        infinite loops.

        Args:
            user_message: The user's input message.
            system_prompt: System prompt for the conversation.

        Yields:
            ChatEvent objects representing incremental updates.
        """
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=system_prompt),
            ChatMessage(role=MessageRole.USER, content=user_message),
        ]

        # Discover tools from the MCP server (empty list if no server)
        tools = []
        if self.mcp_client:
            try:
                mcp_tools = await self.mcp_client.list_tools()
                tools = [t.to_tool_definition() for t in mcp_tools]
                logger.info('Loaded %d tools from MCP server', len(tools))
            except Exception as exc:
                logger.warning('Failed to list MCP tools: %s', exc)
                yield ChatEvent('error', {
                    'message': f'MCP tool discovery failed: {exc}',
                    'code': 'MCP_TOOLS_ERROR',
                })
                # Continue without tools rather than failing entirely

        accumulated_content = ''

        for iteration in range(MAX_TOOL_ITERATIONS):
            logger.debug('Streaming iteration %d/%d', iteration + 1, MAX_TOOL_ITERATIONS)

            tool_calls_in_chunk: list[ToolCall] = []
            chunk_content = ''

            try:
                async for chunk in self.provider.chat_stream(
                    messages,
                    tools=tools or None,
                ):
                    # Yield content tokens as they arrive
                    if chunk.content:
                        chunk_content += chunk.content
                        yield ChatEvent('content', {'content': chunk.content})

                    # Collect tool calls (typically arrive at the end)
                    if chunk.tool_calls:
                        tool_calls_in_chunk = chunk.tool_calls

                    if chunk.is_final:
                        break

            except LLMException as exc:
                logger.error('LLM streaming error: %s', exc)
                yield ChatEvent('error', {
                    'message': str(exc),
                    'code': 'LLM_ERROR',
                })
                return

            accumulated_content += chunk_content

            # No tool calls means the model is done responding
            if not tool_calls_in_chunk:
                yield ChatEvent('done', {'content': accumulated_content})
                return

            # ---- Tool calling phase ----

            # Report which tools the model wants to call
            yield ChatEvent('tool_calls', {
                'tools': [tc.to_dict() for tc in tool_calls_in_chunk],
                'iteration': iteration + 1,
            })

            # Add the assistant message (with tool calls) to history
            messages.append(ChatMessage(
                role=MessageRole.ASSISTANT,
                content=chunk_content if chunk_content else None,
                tool_calls=tool_calls_in_chunk,
            ))

            # Execute each tool call via MCP
            for tool_call in tool_calls_in_chunk:
                yield ChatEvent('tool_executing', {
                    'tool': tool_call.name,
                    'id': tool_call.id,
                })

                result = await self._execute_tool(tool_call)

                yield ChatEvent('tool_result', {
                    'tool': tool_call.name,
                    'id': tool_call.id,
                    'result': result,
                    'is_large': len(result) > 500,
                })

                # Append the tool result to message history so the LLM
                # can incorporate it in the next streaming iteration
                messages.append(ChatMessage(
                    role=MessageRole.TOOL,
                    content=result,
                    tool_call_id=tool_call.id,
                    name=tool_call.name,
                ))

            # Reset accumulated content for the next streaming iteration.
            # The LLM will now produce a new response that incorporates
            # the tool results.
            accumulated_content = ''

        # If we exhaust all iterations, the model is stuck in a tool loop
        yield ChatEvent('error', {
            'message': 'Maximum tool iterations reached',
            'code': 'MAX_ITERATIONS',
        })

    # ------------------------------------------------------------------
    # Tool execution
    # ------------------------------------------------------------------

    async def _execute_tool(self, tool_call: ToolCall) -> str:
        """Execute a single tool call via MCP.

        Args:
            tool_call: The tool call requested by the LLM.

        Returns:
            String result to feed back to the LLM. On error, returns
            an error message string (the LLM can decide how to proceed).
        """
        if not self.mcp_client:
            return f'Error: No MCP server configured to execute tool {tool_call.name!r}'

        try:
            logger.info(
                'Executing tool: %s (id=%s)',
                tool_call.name,
                tool_call.id,
            )
            result = await self.mcp_client.call_tool(
                tool_call.name,
                tool_call.arguments,
            )

            if result.is_error:
                logger.warning(
                    'Tool %s returned error: %s',
                    tool_call.name,
                    result.text[:200],
                )
                return f'Tool error: {result.text}'

            return result.text

        except MCPToolError as exc:
            logger.error('MCP tool error for %s: %s', tool_call.name, exc)
            return f'Tool execution failed: {exc.message}'
        except Exception as exc:
            logger.error('Unexpected error executing %s: %s', tool_call.name, exc)
            return f'Unexpected error: {exc}'

    # ------------------------------------------------------------------
    # Non-streaming fallback
    # ------------------------------------------------------------------

    async def chat(
        self,
        user_message: str,
        system_prompt: str = 'You are a helpful assistant.',
    ) -> str:
        """Non-streaming chat for comparison or fallback.

        Collects the full streamed response into a single string.
        Tool calls are still executed, but results are not yielded
        incrementally.

        Args:
            user_message: The user's input message.
            system_prompt: System prompt for the conversation.

        Returns:
            The complete response text.
        """
        final_content = ''
        async for event in self.stream_with_tools(user_message, system_prompt):
            if event.event_type == 'done':
                final_content = event.data.get('content', '')
            elif event.event_type == 'error':
                raise LLMException(
                    message=event.data.get('message', 'Unknown error'),
                )
        return final_content


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

async def create_agent(config: StreamingConfig) -> StreamingChatAgent:
    """Create a StreamingChatAgent from configuration.

    Sets up the LLM provider and optionally initializes the MCP client
    if a server URL is configured.

    Args:
        config: Streaming configuration with provider and MCP settings.

    Returns:
        A ready-to-use StreamingChatAgent instance.
    """
    provider = get_provider(
        provider_name=config.provider_name,
        model=config.model,
        api_key=config.api_key,
        default_max_tokens=config.max_tokens,
        default_temperature=config.temperature,
    )

    mcp_client = None
    if config.mcp_server_url:
        headers = {}
        if config.mcp_api_key:
            headers['Authorization'] = f'Bearer {config.mcp_api_key}'

        mcp_config = MCPServerConfig(
            name='streaming-chat-mcp',
            url=config.mcp_server_url,
            headers=headers,
        )
        mcp_client = MCPClient(mcp_config)

        logger.info('Initializing MCP connection to %s', config.mcp_server_url)
        await mcp_client.initialize()
        logger.info('MCP connection established')

    return StreamingChatAgent(provider=provider, mcp_client=mcp_client)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

async def demo_streaming(agent: StreamingChatAgent) -> None:
    """Demonstrate streaming mode.

    Shows how events arrive incrementally -- content tokens appear
    one by one, tool calls are reported as they happen, and the
    final 'done' event carries the complete response.
    """
    print('=' * 60)
    print('STREAMING MODE')
    print('=' * 60)
    print()

    query = 'What is the capital of France? Explain briefly.'
    print(f'User: {query}')
    print()
    print('Assistant: ', end='', flush=True)

    async for event in agent.stream_with_tools(query):
        if event.event_type == 'content':
            # Print tokens as they arrive (the streaming experience)
            print(event.data['content'], end='', flush=True)

        elif event.event_type == 'tool_calls':
            tools = event.data['tools']
            names = ', '.join(t['name'] for t in tools)
            print(f'\n  [Tool calls: {names}]')

        elif event.event_type == 'tool_executing':
            print(f'  [Executing: {event.data["tool"]}...]')

        elif event.event_type == 'tool_result':
            result = event.data['result']
            preview = result[:100] + '...' if len(result) > 100 else result
            print(f'  [Result: {preview}]')

        elif event.event_type == 'done':
            print()  # Newline after streamed content
            print()
            print(f'[Stream complete: {len(event.data["content"])} chars]')

        elif event.event_type == 'error':
            print(f'\n[ERROR: {event.data["message"]}]')


async def demo_non_streaming(agent: StreamingChatAgent) -> None:
    """Demonstrate non-streaming mode for comparison."""
    print()
    print('=' * 60)
    print('NON-STREAMING MODE (for comparison)')
    print('=' * 60)
    print()

    query = 'What is the capital of Germany? One sentence.'
    print(f'User: {query}')
    print()

    response = await agent.chat(query)
    print(f'Assistant: {response}')
    print()


async def demo_sse_format(agent: StreamingChatAgent) -> None:
    """Show the raw SSE format for HTTP integration."""
    print()
    print('=' * 60)
    print('SSE FORMAT (for HTTP streaming)')
    print('=' * 60)
    print()

    query = 'Say hello in three languages.'
    print(f'User: {query}')
    print()
    print('Raw SSE events:')
    print('-' * 40)

    event_count = 0
    async for event in agent.stream_with_tools(query):
        event_count += 1
        sse_text = event.to_sse()

        # Show first few and last events to avoid flooding the terminal
        if event_count <= 5 or event.event_type in ('done', 'error'):
            print(sse_text, end='')
        elif event_count == 6:
            print(f'  ... (streaming {event.event_type} events) ...\n')

    print('-' * 40)
    print(f'Total events: {event_count}')


async def main() -> None:
    """Run the streaming chat demo.

    Demonstrates three modes:
    1. Streaming: tokens arrive incrementally
    2. Non-streaming: full response at once (uses streaming under the hood)
    3. SSE format: raw event format for HTTP integration
    """
    # Load .env if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
    )

    try:
        config = StreamingConfig.from_env()
    except ValueError as exc:
        print(f'Configuration error: {exc}')
        sys.exit(1)

    mcp_status = config.mcp_server_url or 'not configured (tools disabled)'
    print(f'Provider: {config.provider_name} | Model: {config.model}')
    print(f'MCP server: {mcp_status}')
    print()

    agent = await create_agent(config)

    await demo_streaming(agent)
    await demo_non_streaming(agent)
    await demo_sse_format(agent)


if __name__ == '__main__':
    asyncio.run(main())
