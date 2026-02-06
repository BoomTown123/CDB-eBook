# Streaming Chat with Tool Calling

SSE streaming agent that executes tools via MCP during response generation.

**Book reference:** Chapter 6 - Agent Architecture, Section 1

## What This Demonstrates

Production chat agents need two things simultaneously: **low-latency token streaming** so users see text immediately, and **tool calling** so the model can look things up, run calculations, or take actions mid-response. This example shows how to combine both.

The core pattern is a **stream-execute-continue loop**:

1. Stream content tokens from the LLM (yielding SSE events)
2. Detect tool calls in the stream
3. Execute tools via MCP (Model Context Protocol)
4. Feed results back into the message history
5. Continue streaming until the model produces a final text response

The agent degrades gracefully without an MCP server -- it simply streams text responses without tools.

## Event Types

The agent emits `ChatEvent` objects, each with a type and JSON data payload. These serialize directly to the [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) format.

| Event | Data | Description |
|-------|------|-------------|
| `content` | `{"content": "token"}` | Incremental text token from the LLM |
| `tool_calls` | `{"tools": [...], "iteration": 1}` | Tools the model wants to call |
| `tool_executing` | `{"tool": "search", "id": "tc_1"}` | Tool execution has started |
| `tool_result` | `{"tool": "search", "id": "tc_1", "result": "...", "is_large": false}` | Result of tool execution |
| `done` | `{"content": "full response"}` | Stream complete with accumulated content |
| `error` | `{"message": "...", "code": "..."}` | Error during processing |

### SSE Wire Format

Each event serializes to standard SSE:

```
event: content
data: {"content": "The capital"}

event: content
data: {"content": " of France"}

event: tool_calls
data: {"tools": [{"id": "tc_1", "name": "search", "arguments": {"q": "Paris population"}}], "iteration": 1}

event: tool_executing
data: {"tool": "search", "id": "tc_1"}

event: tool_result
data: {"tool": "search", "id": "tc_1", "result": "Population: 2.1 million", "is_large": false}

event: content
data: {"content": "Paris has a population of 2.1 million."}

event: done
data: {"content": "Paris has a population of 2.1 million."}
```

## Files

| File | Purpose |
|------|---------|
| `streaming_chat.py` | StreamingChatAgent with the stream-execute-continue loop |
| `config.py` | Configuration via environment variables |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |

## Quick Start

### Without MCP (streaming only)

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env: set OPENROUTER_API_KEY (leave MCP_SERVER_URL blank)

# Run
python streaming_chat.py
```

### With MCP (streaming + tools)

```bash
# Edit .env: set both OPENROUTER_API_KEY and MCP_SERVER_URL
python streaming_chat.py
```

The agent will initialize the MCP connection, discover available tools, and provide them to the LLM. When the model decides to call a tool, execution happens transparently between streaming chunks.

## Architecture

```
User message
    |
    v
+-------------------+
| stream_with_tools  |  <-- async generator (core loop)
+-------------------+
    |
    |  for iteration in range(MAX_TOOL_ITERATIONS):
    |
    v
+-------------------+
| chat_stream()     |  <-- LLM provider streaming API
+-------------------+
    |
    +-- content tokens --> yield ChatEvent('content', ...)
    |
    +-- tool_calls detected?
        |
        NO  --> yield ChatEvent('done', ...) --> return
        |
        YES --> yield ChatEvent('tool_calls', ...)
                |
                v
            +-------------------+
            | _execute_tool()   |  <-- MCP client
            +-------------------+
                |
                +-- yield ChatEvent('tool_result', ...)
                |
                +-- append tool result to messages
                |
                +-- continue loop (stream next response)
```

### Key design decisions

- **MAX_TOOL_ITERATIONS = 10** prevents infinite tool loops. If the model keeps requesting tools after 10 rounds, the agent emits an error event and stops.
- **Graceful MCP degradation.** If no MCP server is configured, or if tool discovery fails, the agent continues without tools rather than crashing.
- **Tool errors become text.** When a tool fails, the error message is returned to the LLM as the tool result. The model can then explain the failure to the user or try a different approach.
- **SSE-native events.** Every `ChatEvent` has a `to_sse()` method, making it trivial to pipe the async generator into an HTTP response (e.g., with FastAPI `StreamingResponse` or Starlette).

## MCP Integration

The agent uses the shared `MCPClient` to communicate with MCP servers via the [streamable-http transport](https://modelcontextprotocol.io/specification). The flow:

1. **Initialize** -- `MCPClient.initialize()` performs the JSON-RPC handshake
2. **Discover tools** -- `MCPClient.list_tools()` returns available tools as `MCPTool` objects
3. **Convert for LLM** -- `MCPTool.to_tool_definition()` produces `ToolDefinition` objects in OpenAI function-calling format
4. **Execute on demand** -- `MCPClient.call_tool()` runs a tool and returns a `ToolResult`

Any MCP-compatible server works. The agent does not need to know what tools are available ahead of time -- it discovers them at startup.

## HTTP Integration Example

To serve this over HTTP with FastAPI:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post('/chat/stream')
async def stream_chat(request: ChatRequest):
    agent = await create_agent(config)

    async def event_generator():
        async for event in agent.stream_with_tools(request.message):
            yield event.to_sse()

    return StreamingResponse(
        event_generator(),
        media_type='text/event-stream',
    )
```

## Related Examples

- **chat-agent/** -- Non-streaming chat agent with tool use (simpler starting point)
- **background-agent/** -- Long-running agent without human in the loop
- **agent-hub/** -- Multi-agent routing and orchestration
