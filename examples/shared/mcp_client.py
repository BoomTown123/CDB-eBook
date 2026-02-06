"""MCP HTTP client for JSON-RPC 2.0 communication.

Simplified version of the production MCP client for use in examples.
Communicates with MCP servers via the streamable-http transport,
which uses HTTP POST with Server-Sent Events responses.

MCP spec: https://modelcontextprotocol.io/specification
Related: Chapter 6 (Agent Architecture) — Tool Integration via MCP
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from typing import Any

import httpx

from shared.llm_base import ToolDefinition

logger = logging.getLogger(__name__)


class MCPException(Exception):
    """Base exception for MCP errors."""

    def __init__(
        self,
        message: str,
        server_name: str | None = None,
        code: int | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.server_name = server_name
        self.code = code


class MCPConnectionError(MCPException):
    """Connection to MCP server failed."""

    pass


class MCPToolError(MCPException):
    """Tool execution failed."""

    pass


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    timeout: float = 30.0


@dataclass
class MCPTool:
    """A tool available from an MCP server."""

    name: str
    description: str
    input_schema: dict[str, Any]
    server_name: str

    def to_tool_definition(self) -> ToolDefinition:
        """Convert to LLM ToolDefinition for use with providers."""
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.input_schema,
            server_name=self.server_name,
        )


@dataclass
class ToolResult:
    """Result from executing an MCP tool."""

    content: list[dict[str, Any]]
    is_error: bool = False

    @property
    def text(self) -> str:
        """Get text content from result."""
        texts = []
        for item in self.content:
            if item.get('type') == 'text':
                texts.append(item.get('text', ''))
        return '\n'.join(texts)


class MCPClient:
    """HTTP client for communicating with MCP servers via JSON-RPC 2.0.

    Uses the streamable-http transport: sends JSON-RPC requests as
    HTTP POST and receives responses as Server-Sent Events.

    Lifecycle:
        1. Create client with MCPServerConfig
        2. Call initialize() to perform the MCP handshake
        3. Call list_tools() to discover available tools
        4. Call call_tool() to execute tools

    Example:
        config = MCPServerConfig(
            name='my-server',
            url='https://mcp.example.com/mcp',
            headers={'Authorization': 'Bearer sk-...'},
        )
        client = MCPClient(config)
        await client.initialize()
        tools = await client.list_tools()
        result = await client.call_tool('search', {'query': 'hello'})
    """

    MCP_SESSION_HEADER = 'mcp-session-id'

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self._tools_cache: list[MCPTool] | None = None
        self._session_id: str | None = None
        self._is_initialized: bool = False

    @property
    def server_name(self) -> str:
        return self.config.name

    def _parse_sse_response(self, response_text: str) -> dict[str, Any]:
        """Parse SSE formatted response to extract JSON-RPC data.

        MCP servers using streamable-http transport return:
            event: message
            data: {"jsonrpc":"2.0","id":"...","result":{...}}
        """
        for line in response_text.split('\n'):
            line = line.strip('\r\n ')
            if line.startswith('data:'):
                data_str = line[5:].strip()
                if data_str:
                    return json.loads(data_str)
        raise MCPException(
            message=f'No data found in SSE response: {response_text[:200]}',
            server_name=self.config.name,
        )

    async def _send_request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        capture_session: bool = False,
        is_notification: bool = False,
    ) -> Any:
        """Send a JSON-RPC 2.0 request to the MCP server.

        Args:
            method: RPC method name (e.g. 'initialize', 'tools/list')
            params: Method parameters
            capture_session: Capture session ID from response headers
            is_notification: Send as notification (no id, no response)
        """
        request_id = None if is_notification else str(uuid.uuid4())

        payload: dict[str, Any] = {
            'jsonrpc': '2.0',
            'method': method,
        }
        if request_id:
            payload['id'] = request_id
        if params:
            payload['params'] = params

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            **self.config.headers,
        }
        if self._session_id:
            headers[self.MCP_SESSION_HEADER] = self._session_id

        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.post(
                    self.config.url,
                    json=payload,
                    headers=headers,
                )

                if is_notification:
                    if response.status_code not in (200, 202, 204):
                        raise MCPConnectionError(
                            message=f'HTTP {response.status_code}: {response.text}',
                            server_name=self.config.name,
                        )
                    return None

                if response.status_code != 200:
                    raise MCPConnectionError(
                        message=f'HTTP {response.status_code}: {response.text}',
                        server_name=self.config.name,
                    )

                if capture_session:
                    session_id = response.headers.get(self.MCP_SESSION_HEADER)
                    if session_id:
                        self._session_id = session_id

                content_type = response.headers.get('content-type', '')
                if 'text/event-stream' in content_type:
                    data = self._parse_sse_response(response.text)
                else:
                    data = response.json()

                if 'error' in data:
                    error = data['error']
                    raise MCPException(
                        message=error.get('message', 'Unknown error'),
                        server_name=self.config.name,
                        code=error.get('code'),
                    )

                return data.get('result')

        except httpx.TimeoutException as e:
            raise MCPConnectionError(
                message=f'Request timed out: {e}',
                server_name=self.config.name,
            ) from e
        except httpx.RequestError as e:
            raise MCPConnectionError(
                message=f'Connection failed: {e}',
                server_name=self.config.name,
            ) from e

    async def initialize(self) -> dict[str, Any]:
        """Initialize the MCP connection.

        Performs the MCP handshake:
        1. Send initialize request (captures session ID)
        2. Send initialized notification
        """
        self._session_id = None
        self._is_initialized = False

        result = await self._send_request(
            'initialize',
            {
                'protocolVersion': '2024-11-05',
                'capabilities': {},
                'clientInfo': {
                    'name': 'book-example-client',
                    'version': '1.0.0',
                },
            },
            capture_session=True,
        )

        await self._send_request('notifications/initialized', is_notification=True)

        self._is_initialized = True
        logger.info(
            'MCP initialized: server=%s info=%s',
            self.config.name,
            result.get('serverInfo', {}),
        )

        return result

    async def list_tools(self, force_refresh: bool = False) -> list[MCPTool]:
        """List available tools from the server.

        Results are cached after the first call. Pass force_refresh=True
        to re-fetch from the server.
        """
        if self._tools_cache is not None and not force_refresh:
            return self._tools_cache

        result = await self._send_request('tools/list')
        tools_data = result.get('tools', [])

        self._tools_cache = [
            MCPTool(
                name=tool['name'],
                description=tool.get('description', ''),
                input_schema=tool.get('inputSchema', {}),
                server_name=self.config.name,
            )
            for tool in tools_data
        ]

        logger.info(
            'MCP tools listed: server=%s count=%d',
            self.config.name,
            len(self._tools_cache),
        )

        return self._tools_cache

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> ToolResult:
        """Execute a tool on the MCP server.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments as a dictionary

        Returns:
            ToolResult with execution output

        Raises:
            MCPToolError: If tool execution fails
        """
        try:
            result = await self._send_request(
                'tools/call',
                {
                    'name': tool_name,
                    'arguments': arguments,
                },
            )

            content = result.get('content', [])
            is_error = result.get('isError', False)

            return ToolResult(content=content, is_error=is_error)

        except MCPException as e:
            raise MCPToolError(
                message=f'Tool execution failed: {e.message}',
                server_name=self.config.name,
                code=e.code,
            ) from e

    async def ping(self) -> bool:
        """Check if the server is reachable."""
        try:
            await self._send_request('ping')
            return True
        except MCPException:
            return False
