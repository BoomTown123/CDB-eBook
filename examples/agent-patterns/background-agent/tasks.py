"""
Task definitions and queue management for the background agent.

Demonstrates background agent patterns from Chapter 6:
- Idempotency: safe to run the same task twice
- Checkpointing: resume from where we left off
- Graceful degradation: skip failures, continue processing

Book reference: Chapter 6, Section 6 - Agent Design Patterns
"""

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class TaskStatus(Enum):
    """Lifecycle states for a background task."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    QUARANTINED = "quarantined"  # Max retries exceeded


@dataclass
class Task:
    """A unit of work for the background agent."""

    task_type: str
    payload: dict
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: TaskStatus = TaskStatus.PENDING
    retries: int = 0
    result: Any = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    completed_at: float | None = None

    def to_dict(self) -> dict:
        """Serialize for checkpointing."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "payload": self.payload,
            "status": self.status.value,
            "retries": self.retries,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class TaskQueue:
    """Simple file-backed task queue with checkpointing.

    Implements the checkpointing pattern from Chapter 6:
    "Long-running tasks will fail mid-execution. Without checkpoints,
    restart from zero."

    In production, use a proper queue (Redis, SQS, Temporal) instead
    of file-based persistence.
    """

    def __init__(self, checkpoint_path: str = "checkpoint.json") -> None:
        self.checkpoint_path = Path(checkpoint_path)
        self.tasks: list[Task] = []
        self._idempotency_keys: set[str] = set()

    def add_task(self, task_type: str, payload: dict, idempotency_key: str | None = None) -> Task:
        """Add a task to the queue.

        Implements idempotency: if a task with the same key already exists,
        skip it. "The first duplicate invoice costs more than the implementation."
        """
        if idempotency_key and idempotency_key in self._idempotency_keys:
            # Idempotency check: already processed or in queue
            for task in self.tasks:
                if task.task_id == idempotency_key:
                    return task
            # Key exists but task not found (already completed in prior run)
            dummy = Task(task_type=task_type, payload=payload, task_id=idempotency_key)
            dummy.status = TaskStatus.COMPLETED
            return dummy

        task = Task(task_type=task_type, payload=payload)
        if idempotency_key:
            task.task_id = idempotency_key
            self._idempotency_keys.add(idempotency_key)

        self.tasks.append(task)
        return task

    def get_pending(self) -> list[Task]:
        """Return tasks that are ready to process."""
        return [t for t in self.tasks if t.status == TaskStatus.PENDING]

    def get_failed(self) -> list[Task]:
        """Return tasks that failed but may be retried."""
        return [t for t in self.tasks if t.status == TaskStatus.FAILED]

    def save_checkpoint(self) -> None:
        """Persist queue state to disk.

        Enables resumption after crashes. The checkpoint captures every
        task's status so we can skip completed items on restart.
        """
        state = {
            "tasks": [t.to_dict() for t in self.tasks],
            "idempotency_keys": list(self._idempotency_keys),
            "saved_at": time.time(),
        }
        self.checkpoint_path.write_text(json.dumps(state, indent=2))

    def load_checkpoint(self) -> bool:
        """Restore queue state from disk. Returns True if checkpoint existed."""
        if not self.checkpoint_path.exists():
            return False

        state = json.loads(self.checkpoint_path.read_text())
        self._idempotency_keys = set(state.get("idempotency_keys", []))

        for t_data in state.get("tasks", []):
            task = Task(
                task_type=t_data["task_type"],
                payload=t_data["payload"],
                task_id=t_data["task_id"],
                status=TaskStatus(t_data["status"]),
                retries=t_data["retries"],
                result=t_data.get("result"),
                error=t_data.get("error"),
                created_at=t_data["created_at"],
                completed_at=t_data.get("completed_at"),
            )
            self.tasks.append(task)

        return True

    def summary(self) -> dict[str, int]:
        """Return counts by status."""
        counts: dict[str, int] = {}
        for task in self.tasks:
            key = task.status.value
            counts[key] = counts.get(key, 0) + 1
        return counts


def create_sample_tasks() -> list[tuple[str, dict, str]]:
    """Generate sample tasks for demonstration.

    Returns (task_type, payload, idempotency_key) tuples.
    """
    return [
        (
            "summarize",
            {"text": "AI-first companies design around AI from day one, not as an afterthought."},
            "sum-001",
        ),
        (
            "summarize",
            {"text": "Chat agents need speed. Background agents need reliability."},
            "sum-002",
        ),
        (
            "analyze_sentiment",
            {"text": "The product launch exceeded all expectations."},
            "sent-001",
        ),
        (
            "analyze_sentiment",
            {"text": "Response times are unacceptable and customers are leaving."},
            "sent-002",
        ),
        (
            "extract_entities",
            {"text": "Klarna handled 2.3 million conversations using GPT-4 in February 2024."},
            "ent-001",
        ),
    ]
