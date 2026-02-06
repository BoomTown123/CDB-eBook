"""
Monitoring and alerting for the background agent.

Implements the alerting patterns from Chapter 6, Section 6:
- Failure alerts: on exceptions
- Timeout alerts: when tasks exceed duration budgets
- Anomaly alerts: when outputs deviate from expected
- Missing alerts: when expected tasks do not run (dead man's switch)

"If it doesn't report healthy within expected time, we assume it's failed."

Book reference: Chapter 6, Section 6 - Agent Design Patterns
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from tasks import Task, TaskStatus


class AlertLevel(Enum):
    """Severity levels for monitoring alerts."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Alert:
    """A monitoring alert from the background agent."""

    level: AlertLevel
    alert_type: str
    message: str
    task_id: str | None = None
    timestamp: float = field(default_factory=time.time)

    def __str__(self) -> str:
        task_info = f" [task={self.task_id}]" if self.task_id else ""
        return f"[{self.level.value.upper()}] {self.alert_type}{task_info}: {self.message}"


class AgentMonitor:
    """Monitor for background agent health and task execution.

    From Chapter 6: "Background agents running at 3 AM can accumulate
    errors for hours. If silent failure is dangerous, design reliable
    alerting into your background agent."

    In production, send alerts to PagerDuty, Slack, or a monitoring
    dashboard. This example logs to console and stores in memory.
    """

    def __init__(
        self,
        task_timeout_seconds: int = 300,
        token_budget: int = 50_000,
        cost_budget_usd: float = 1.00,
    ) -> None:
        self.task_timeout_seconds = task_timeout_seconds
        self.token_budget = token_budget
        self.cost_budget_usd = cost_budget_usd
        self.alerts: list[Alert] = []
        self.tokens_used: int = 0
        self.cost_used_usd: float = 0.0
        self._last_heartbeat: float = time.time()
        self._task_start_times: dict[str, float] = {}

    def record_heartbeat(self) -> None:
        """Record that the agent is alive.

        The dead man's switch pattern: if no heartbeat arrives within
        the expected window, assume the agent has failed.
        """
        self._last_heartbeat = time.time()

    def check_heartbeat(self, max_silence_seconds: int = 60) -> bool:
        """Check if the agent has reported recently.

        Returns False (and fires alert) if the agent has gone silent.
        """
        silence = time.time() - self._last_heartbeat
        if silence > max_silence_seconds:
            self._fire_alert(
                AlertLevel.CRITICAL,
                "missing_heartbeat",
                f"No heartbeat for {silence:.0f}s (limit: {max_silence_seconds}s). "
                "Agent may have crashed.",
            )
            return False
        return True

    def task_started(self, task: Task) -> None:
        """Record that a task has begun processing."""
        self._task_start_times[task.task_id] = time.time()
        self._fire_alert(
            AlertLevel.INFO,
            "task_started",
            f"Processing task: {task.task_type}",
            task_id=task.task_id,
        )

    def task_completed(self, task: Task) -> None:
        """Record successful task completion."""
        duration = self._task_duration(task.task_id)
        self._fire_alert(
            AlertLevel.INFO,
            "task_completed",
            f"Completed in {duration:.1f}s: {task.task_type}",
            task_id=task.task_id,
        )

    def task_failed(self, task: Task, error: str) -> None:
        """Record task failure. Escalate if retries exhausted."""
        level = AlertLevel.WARNING if task.retries < 3 else AlertLevel.CRITICAL
        self._fire_alert(
            level,
            "task_failed",
            f"Failed (attempt {task.retries}): {error}",
            task_id=task.task_id,
        )

    def task_quarantined(self, task: Task) -> None:
        """Record that a task has been quarantined after max retries."""
        self._fire_alert(
            AlertLevel.CRITICAL,
            "task_quarantined",
            f"Quarantined after {task.retries} retries: {task.task_type}. "
            "Requires human review.",
            task_id=task.task_id,
        )

    def check_timeout(self, task: Task) -> bool:
        """Check if a running task has exceeded its time budget.

        Returns True if the task has timed out.
        """
        start = self._task_start_times.get(task.task_id)
        if not start:
            return False

        elapsed = time.time() - start
        if elapsed > self.task_timeout_seconds:
            self._fire_alert(
                AlertLevel.CRITICAL,
                "task_timeout",
                f"Task exceeded {self.task_timeout_seconds}s budget "
                f"(running for {elapsed:.0f}s)",
                task_id=task.task_id,
            )
            return True
        return False

    def record_token_usage(self, tokens: int, cost_usd: float) -> None:
        """Track cumulative resource usage.

        From Chapter 6: "Implement time, token, cost budgets, and
        iteration limits. This isn't optional."
        """
        self.tokens_used += tokens
        self.cost_used_usd += cost_usd

        if self.tokens_used > self.token_budget:
            self._fire_alert(
                AlertLevel.CRITICAL,
                "token_budget_exceeded",
                f"Token budget exhausted: {self.tokens_used}/{self.token_budget}",
            )

        if self.cost_used_usd > self.cost_budget_usd:
            self._fire_alert(
                AlertLevel.CRITICAL,
                "cost_budget_exceeded",
                f"Cost budget exhausted: ${self.cost_used_usd:.4f}/${self.cost_budget_usd:.2f}",
            )

    def is_within_budget(self) -> bool:
        """Check if the agent is still within resource limits."""
        return (
            self.tokens_used < self.token_budget
            and self.cost_used_usd < self.cost_budget_usd
        )

    def get_summary(self) -> dict[str, Any]:
        """Return a monitoring summary for logging or dashboards."""
        alert_counts: dict[str, int] = {}
        for alert in self.alerts:
            key = alert.level.value
            alert_counts[key] = alert_counts.get(key, 0) + 1

        return {
            "tokens_used": self.tokens_used,
            "cost_used_usd": round(self.cost_used_usd, 4),
            "alerts": alert_counts,
            "total_alerts": len(self.alerts),
            "last_heartbeat_ago": round(time.time() - self._last_heartbeat, 1),
        }

    def _task_duration(self, task_id: str) -> float:
        """Calculate how long a task has been running."""
        start = self._task_start_times.get(task_id, time.time())
        return time.time() - start

    def _fire_alert(
        self,
        level: AlertLevel,
        alert_type: str,
        message: str,
        task_id: str | None = None,
    ) -> None:
        """Create and store an alert.

        In production, route alerts to external systems based on severity:
        - INFO: structured logs
        - WARNING: Slack channel
        - CRITICAL: PagerDuty / on-call
        """
        alert = Alert(
            level=level,
            alert_type=alert_type,
            message=message,
            task_id=task_id,
        )
        self.alerts.append(alert)
        print(f"  MONITOR: {alert}")
