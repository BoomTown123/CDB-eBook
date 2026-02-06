"""
Tool definitions for the chat agent.

Each tool is defined as a ToolDefinition (from the shared provider library)
paired with a callable.  The agent decides which tool to invoke based on the
user's request.

These are simple examples. Production tools would connect to real APIs,
databases, or services.

Book reference: Chapter 6, Section 3 - Designing Agent Interfaces
"""

import json
import math
import sys
from pathlib import Path
from typing import Callable

# Add shared library to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.llm_base import ToolDefinition


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def search(query: str) -> str:
    """Simulate a search operation.

    In production, this would call a search API (e.g., web search,
    internal knowledge base, vector database).
    """
    # Simulated results for demonstration
    results = {
        "agent patterns": "Agent patterns include chat agents, background agents, and agent hubs. See Chapter 6.",
        "chat agent": "Chat agents enable humans to accomplish tasks through conversation. Speed matters.",
        "background agent": "Background agents execute tasks without human supervision. Reliability matters.",
    }

    query_lower = query.lower()
    for key, value in results.items():
        if key in query_lower:
            return json.dumps({"results": [value], "source": "knowledge_base"})

    return json.dumps({"results": [], "source": "knowledge_base", "note": "No results found."})


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression.

    Supports basic arithmetic. In production, you might use a sandboxed
    evaluator or a dedicated computation service.
    """
    # Allow only safe math operations
    allowed_names = {
        name: getattr(math, name)
        for name in ["sqrt", "pow", "sin", "cos", "pi", "e", "log"]
    }
    allowed_names.update({"abs": abs, "round": round})

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return json.dumps({"result": result, "expression": expression})
    except Exception as exc:
        return json.dumps({"error": str(exc), "expression": expression})


def read_file(filepath: str) -> str:
    """Read contents of a file.

    Demonstrates a tool with side effects that the agent should confirm
    before using on sensitive paths. Action confirmation pattern:
    read-only is low risk, but reading arbitrary paths still deserves
    a mention of what will be accessed.
    """
    try:
        with open(filepath, "r") as f:
            content = f.read(4096)  # Limit read size
        return json.dumps({"content": content, "path": filepath, "truncated": len(content) >= 4096})
    except FileNotFoundError:
        return json.dumps({"error": f"File not found: {filepath}"})
    except PermissionError:
        return json.dumps({"error": f"Permission denied: {filepath}"})


# ---------------------------------------------------------------------------
# Tool registry — ToolDefinitions + dispatch map
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[ToolDefinition] = [
    ToolDefinition(
        name="search",
        description="Search a knowledge base for information. Use when the user asks a factual question.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
            },
            "required": ["query"],
        },
    ),
    ToolDefinition(
        name="calculate",
        description="Evaluate a mathematical expression. Use for arithmetic, unit conversions, or formulas.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '2 + 2' or 'sqrt(144)'",
                },
            },
            "required": ["expression"],
        },
    ),
    ToolDefinition(
        name="read_file",
        description="Read the contents of a local file. Use when the user asks about a specific file.",
        parameters={
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to the file to read"},
            },
            "required": ["filepath"],
        },
    ),
]

# Maps tool names to their implementation functions
_TOOL_DISPATCH: dict[str, Callable[..., str]] = {
    "search": search,
    "calculate": calculate,
    "read_file": read_file,
}


def get_tool_definitions() -> list[ToolDefinition]:
    """Return all available tool definitions for the provider."""
    return TOOL_DEFINITIONS


def get_tool_descriptions() -> str:
    """Format tool descriptions for inclusion in the system prompt."""
    lines = []
    for tool_def in TOOL_DEFINITIONS:
        params = ", ".join(tool_def.parameters.get("required", []))
        lines.append(f"- {tool_def.name}({params}): {tool_def.description}")
    return "\n".join(lines)


def execute_tool(name: str, arguments: dict) -> str:
    """Look up and execute a tool by name.

    Args:
        name: The tool function name.
        arguments: Dictionary of keyword arguments for the tool.

    Returns:
        JSON-encoded result string.
    """
    func = _TOOL_DISPATCH.get(name)
    if func is None:
        return json.dumps({"error": f"Unknown tool: {name}"})
    return func(**arguments)
