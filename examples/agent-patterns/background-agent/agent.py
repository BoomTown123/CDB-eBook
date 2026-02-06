"""
Background Agent - Autonomous task processor with monitoring.

Demonstrates the background agent pattern from Chapter 6:
- No human in the loop: triggered by schedule or events, not messages
- Idempotency: safe to re-run without duplicates
- Checkpointing: resume from interruption
- Resource budgets: token and cost limits
- Alerting: dead man's switch, failure escalation
- Graceful degradation: skip failures, continue processing

Run:
    python agent.py

Book reference: Chapter 6 - Agent Architecture
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path

# Add shared library to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared import ChatMessage, MessageRole, get_provider  # noqa: E402
from shared.llm_base import LLMProvider  # noqa: E402
from shared.llm_exceptions import LLMException  # noqa: E402

from config import BackgroundAgentConfig  # noqa: E402
from monitor import AgentMonitor  # noqa: E402
from tasks import TaskQueue, TaskStatus, create_sample_tasks  # noqa: E402

logger = logging.getLogger(__name__)


# Task-type prompts: each task type maps to a system instruction
TASK_PROMPTS: dict[str, str] = {
    "summarize": "Summarize the following text in one sentence.",
    "analyze_sentiment": (
        "Analyze the sentiment of the following text. "
        'Respond with JSON: {"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}'
    ),
    "extract_entities": (
        "Extract named entities from the following text. "
        'Respond with JSON: {"entities": [{"name": "...", "type": "..."}]}'
    ),
}


class BackgroundAgent:
    """Autonomous agent that processes a task queue without human interaction.

    Design principles (from Chapter 6, Section 6):
    - Assume failure: explicit success reporting, mandatory timeouts
    - Idempotency: running twice produces the same outcome
    - Checkpointing: crash-safe, resume from last good state
    - Resource budgets: stop before costs spiral
    - Dead man's switch: alert if agent goes silent
    """

    def __init__(self, config: BackgroundAgentConfig) -> None:
        self.config = config
        self.provider: LLMProvider = get_provider(
            provider_name=config.provider_name,
            model=config.model,
            api_key=config.api_key,
        )
        self.queue = TaskQueue()
        self.monitor = AgentMonitor(
            task_timeout_seconds=config.task_timeout_seconds,
            token_budget=config.token_budget,
            cost_budget_usd=config.cost_budget_usd,
        )

    async def _process_task(self, task_type: str, payload: dict) -> str:
        """Send a single task to the LLM and return the result.

        Each task type has its own system prompt. The agent does not
        engage in multi-turn conversation -- it processes and moves on.
        """
        system_prompt = TASK_PROMPTS.get(task_type)
        if not system_prompt:
            raise ValueError(f"Unknown task type: {task_type}")

        text = payload.get("text", "")
        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=system_prompt),
            ChatMessage(role=MessageRole.USER, content=text),
        ]

        response = await self.provider.chat(
            messages,
            max_tokens=self.config.max_tokens_per_request,
            temperature=0.0,  # Deterministic for background tasks
        )

        # Track resource usage
        if response.usage:
            tokens = response.usage.total_tokens
            # Rough cost estimate (adjust for your model/pricing)
            estimated_cost = tokens * 0.00001
            self.monitor.record_token_usage(tokens, estimated_cost)

        return response.content or ""

    async def run(self) -> dict:
        """Execute the main processing loop.

        Workflow:
        1. Load checkpoint (resume if prior run was interrupted)
        2. Process each pending task
        3. On failure: retry with backoff, quarantine after max retries
        4. Checkpoint after each task
        5. Stop if resource budget is exhausted
        6. Report final summary

        Returns a summary dict with task counts and monitor data.
        """
        logger.info("Background Agent starting...")
        print("Background Agent starting...")

        # Attempt to resume from checkpoint
        if self.queue.load_checkpoint():
            print(f"  Resumed from checkpoint: {self.queue.summary()}")

        # Process all pending tasks
        pending = self.queue.get_pending()
        print(f"  {len(pending)} task(s) to process.")

        for task in pending:
            # Budget check before each task
            if not self.monitor.is_within_budget():
                print("  BUDGET EXHAUSTED. Stopping.")
                logger.warning("Budget exhausted, stopping processing.")
                break

            self.monitor.record_heartbeat()
            self.monitor.task_started(task)
            task.status = TaskStatus.PROCESSING

            try:
                result = await self._process_task(task.task_type, task.payload)
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = time.time()
                self.monitor.task_completed(task)

            except LLMException as exc:
                task.retries += 1
                task.error = str(exc)
                logger.error(
                    "LLM error processing task %s: %s", task.task_id, exc
                )

                if task.retries >= self.config.max_retries:
                    # Quarantine: skip and continue (graceful degradation)
                    task.status = TaskStatus.QUARANTINED
                    self.monitor.task_quarantined(task)
                else:
                    # Mark for retry (would be re-picked up on next run)
                    task.status = TaskStatus.FAILED
                    self.monitor.task_failed(task, str(exc))

            except Exception as exc:
                task.retries += 1
                task.error = str(exc)
                logger.error(
                    "Unexpected error processing task %s: %s",
                    task.task_id,
                    exc,
                )

                if task.retries >= self.config.max_retries:
                    task.status = TaskStatus.QUARANTINED
                    self.monitor.task_quarantined(task)
                else:
                    task.status = TaskStatus.FAILED
                    self.monitor.task_failed(task, str(exc))

            # Checkpoint after each task so we can resume
            self.queue.save_checkpoint()

        # Final heartbeat and summary
        self.monitor.record_heartbeat()
        summary = {
            "tasks": self.queue.summary(),
            "monitor": self.monitor.get_summary(),
        }
        print(f"\nRun complete: {json.dumps(summary, indent=2)}")

        # Print results for completed tasks
        print("\n--- Results ---")
        for task in self.queue.tasks:
            if task.status == TaskStatus.COMPLETED:
                print(f"  [{task.task_id}] {task.task_type}: {task.result}")

        return summary


def main() -> None:
    """Run the background agent on sample tasks.

    In production, tasks would come from a message queue, scheduler,
    or webhook. This demo loads sample tasks to show the pattern.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    try:
        config = BackgroundAgentConfig.from_env()
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)

    agent = BackgroundAgent(config)

    # Load sample tasks (with idempotency keys)
    for task_type, payload, key in create_sample_tasks():
        agent.queue.add_task(task_type, payload, idempotency_key=key)

    print(f"Queued {len(agent.queue.tasks)} tasks.")
    print(f"Provider: {config.provider_name} | Model: {config.model}")
    print(f"Token budget: {config.token_budget} | Cost budget: ${config.cost_budget_usd:.2f}")
    print(f"Max retries: {config.max_retries} | Timeout: {config.task_timeout_seconds}s")
    print("-" * 60)

    asyncio.run(agent.run())


if __name__ == "__main__":
    main()
