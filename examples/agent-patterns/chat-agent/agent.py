"""
Chat Agent - Interactive conversational agent with tool use.

Demonstrates the chat agent pattern from Chapter 6:
- Human in the loop: user guides, agent assists
- Clarification capability: asks when uncertain
- Graceful handoff: admits when stuck
- Context persistence: maintains conversation history
- Tool use: invokes tools based on user needs

Uses the shared provider library for LLM access (OpenRouter by default).

Run:
    python agent.py

Book reference: Chapter 6 - Agent Architecture
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add shared library to path so `import shared` works
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.llm_factory import get_provider
from shared.llm_base import ChatMessage, MessageRole, ToolCall

from config import ChatAgentConfig
from prompts import CONTEXT_SUMMARY_PROMPT, SYSTEM_PROMPT
from tools import execute_tool, get_tool_definitions, get_tool_descriptions

logger = logging.getLogger(__name__)


class ChatAgent:
    """Interactive chat agent with tool-calling capability.

    Design principles (from Chapter 6, Section 6):
    - Clarify before acting on ambiguous requests
    - Confirm before irreversible actions
    - Hand off gracefully when stuck
    - Show progress during multi-step operations
    - Summarize context periodically to manage token limits
    """

    def __init__(self, config: ChatAgentConfig) -> None:
        self.config = config
        self.provider = get_provider(
            provider_name=config.provider_name,
            model=config.model,
            api_key=config.api_key,
        )
        self.messages: list[ChatMessage] = []
        self.turn_count: int = 0

        # Initialize with system prompt including tool descriptions
        system_content = SYSTEM_PROMPT.format(
            tool_descriptions=get_tool_descriptions()
        )
        self.messages.append(
            ChatMessage(role=MessageRole.SYSTEM, content=system_content)
        )

    async def _maybe_summarize_context(self) -> None:
        """Summarize conversation history to manage token limits.

        From Chapter 6: "Summarize context every 10 turns to avoid token
        limits while maintaining continuity."
        """
        if self.turn_count % self.config.context_summary_interval != 0:
            return
        if self.turn_count == 0:
            return

        # Build conversation text for summarization
        conversation_text = "\n".join(
            f"{m.role.value}: {m.content}"
            for m in self.messages[1:]  # Skip system prompt
            if m.content
        )

        summary_response = await self.provider.chat(
            messages=[
                ChatMessage(
                    role=MessageRole.USER,
                    content=CONTEXT_SUMMARY_PROMPT.format(
                        conversation_text=conversation_text
                    ),
                )
            ],
            max_tokens=256,
        )

        summary = summary_response.content

        # Replace history with summary, keeping system prompt
        self.messages = [
            self.messages[0],
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=f"Conversation summary: {summary}",
            ),
        ]
        print(f"  [Context summarized at turn {self.turn_count}]")

    def _handle_tool_calls(self, tool_calls: list[ToolCall]) -> list[ChatMessage]:
        """Execute tool calls and return results.

        Implements the tool-use loop: the LLM decides which tools to call,
        we execute them and feed results back for the next response.
        """
        tool_results: list[ChatMessage] = []
        for tc in tool_calls:
            print(f"  [Calling tool: {tc.name}({tc.arguments})]")
            result = execute_tool(tc.name, tc.arguments)

            tool_results.append(
                ChatMessage(
                    role=MessageRole.TOOL,
                    content=result,
                    tool_call_id=tc.id,
                    name=tc.name,
                )
            )
        return tool_results

    async def chat(self, user_message: str) -> str:
        """Process a user message and return the agent's response.

        The core loop:
        1. Add user message to history
        2. Call the LLM (may request tool calls)
        3. If tools requested, execute them and call LLM again
        4. Return the final text response
        5. Periodically summarize context
        """
        self.messages.append(
            ChatMessage(role=MessageRole.USER, content=user_message)
        )
        self.turn_count += 1

        # Summarize context periodically to stay within token limits
        await self._maybe_summarize_context()

        # Get tool definitions for each request
        tool_defs = get_tool_definitions()

        # Call the LLM with tool definitions
        response = await self.provider.chat(
            messages=self.messages,
            tools=tool_defs,
            max_tokens=self.config.max_tokens_per_response,
            temperature=self.config.temperature,
        )

        # Tool-use loop: execute tools until the LLM produces a text response
        max_tool_rounds = 5  # Prevent infinite tool loops
        tool_round = 0

        while response.has_tool_calls and tool_round < max_tool_rounds:
            tool_round += 1

            # Add the assistant's tool-call message to history
            self.messages.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )

            # Execute tools and add results
            tool_results = self._handle_tool_calls(response.tool_calls)
            self.messages.extend(tool_results)

            # Call LLM again with tool results
            response = await self.provider.chat(
                messages=self.messages,
                tools=tool_defs,
                max_tokens=self.config.max_tokens_per_response,
                temperature=self.config.temperature,
            )

        # Final text response
        assistant_content = response.content or "(No response generated)"
        self.messages.append(
            ChatMessage(role=MessageRole.ASSISTANT, content=assistant_content)
        )

        return assistant_content


async def main() -> None:
    """Run the interactive chat loop.

    This is the human-in-the-loop pattern: the user drives the conversation,
    the agent assists with tools and knowledge.
    """
    # Load .env file if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv is optional if env vars are set another way

    try:
        config = ChatAgentConfig.from_env()
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)

    agent = ChatAgent(config)

    print("Chat Agent ready. Type 'quit' to exit, 'handoff' to simulate handoff.")
    print(f"Provider: {config.provider_name} | Model: {config.model} | Max turns: {config.max_conversation_turns}")
    print("-" * 60)

    while agent.turn_count < config.max_conversation_turns:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye.")
            break

        if user_input.lower() == "handoff":
            # Graceful handoff pattern: transfer context to a human
            print("\n[HANDOFF] Transferring to human support.")
            print("[HANDOFF] Context: ", json.dumps(
                {
                    "turns": agent.turn_count,
                    "last_messages": [
                        (m.content or "")[:100]
                        for m in agent.messages[-4:]
                        if m.role in (MessageRole.USER, MessageRole.ASSISTANT)
                    ],
                },
                indent=2,
            ))
            break

        response = await agent.chat(user_input)
        print(f"\nAgent: {response}")

    if agent.turn_count >= config.max_conversation_turns:
        print(f"\n[Session limit reached: {config.max_conversation_turns} turns]")


if __name__ == "__main__":
    asyncio.run(main())
