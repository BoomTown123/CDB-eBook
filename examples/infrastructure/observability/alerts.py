"""
Alert definitions and thresholds for AI observability.

Defines the alerts that catch AI-specific failure modes before they
become incidents: cost spikes, latency degradation, quality drops,
error rate increases. Traditional monitoring misses these because
it tracks HTTP-level metrics, not AI-level ones.

Reference: Chapter 4 - The Infrastructure Stack
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from metrics import AIMetricsCollector, ModelStats


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Current state of an alert."""
    OK = "ok"
    FIRING = "firing"
    RESOLVED = "resolved"


@dataclass
class AlertRule:
    """
    A single alert rule with threshold and evaluation logic.

    Each rule checks a specific condition against collected metrics.
    When the condition is true, the alert fires. When it resolves,
    it transitions back to OK.
    """
    name: str
    description: str
    severity: AlertSeverity
    metric_name: str
    threshold: float
    comparison: str  # "gt", "lt", "gte", "lte"
    evaluation_window_seconds: float = 300.0
    tags: dict[str, str] = field(default_factory=dict)

    def evaluate(self, current_value: float) -> bool:
        """Return True if the alert condition is met."""
        if self.comparison == "gt":
            return current_value > self.threshold
        elif self.comparison == "lt":
            return current_value < self.threshold
        elif self.comparison == "gte":
            return current_value >= self.threshold
        elif self.comparison == "lte":
            return current_value <= self.threshold
        return False


@dataclass
class Alert:
    """A fired alert instance."""
    rule_name: str
    severity: AlertSeverity
    status: AlertStatus
    current_value: float
    threshold: float
    message: str
    fired_at: float = field(default_factory=time.time)
    resolved_at: float | None = None
    tags: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Default alert rules for AI operations
# ---------------------------------------------------------------------------

DEFAULT_ALERT_RULES: list[AlertRule] = [
    # Cost alerts
    AlertRule(
        name="ai.cost.daily_budget_warning",
        description="Daily AI spend approaching budget limit",
        severity=AlertSeverity.WARNING,
        metric_name="ai.cost.total",
        threshold=50.0,  # $50/day
        comparison="gt",
    ),
    AlertRule(
        name="ai.cost.daily_budget_critical",
        description="Daily AI spend exceeded budget limit",
        severity=AlertSeverity.CRITICAL,
        metric_name="ai.cost.total",
        threshold=100.0,  # $100/day
        comparison="gt",
    ),
    AlertRule(
        name="ai.cost.per_request_spike",
        description="Average cost per request unusually high",
        severity=AlertSeverity.WARNING,
        metric_name="ai.cost.per_request",
        threshold=0.10,  # $0.10 per request
        comparison="gt",
    ),

    # Latency alerts
    AlertRule(
        name="ai.latency.p95_warning",
        description="P95 latency exceeding target",
        severity=AlertSeverity.WARNING,
        metric_name="ai.latency.p95",
        threshold=5000.0,  # 5 seconds
        comparison="gt",
    ),
    AlertRule(
        name="ai.latency.p99_critical",
        description="P99 latency critically high",
        severity=AlertSeverity.CRITICAL,
        metric_name="ai.latency.p99",
        threshold=10000.0,  # 10 seconds
        comparison="gt",
    ),

    # Quality alerts
    AlertRule(
        name="ai.quality.degradation",
        description="Average quality score below acceptable threshold",
        severity=AlertSeverity.WARNING,
        metric_name="ai.quality.avg",
        threshold=0.7,
        comparison="lt",
    ),
    AlertRule(
        name="ai.quality.critical_drop",
        description="Quality score critically low --- possible model issue",
        severity=AlertSeverity.CRITICAL,
        metric_name="ai.quality.avg",
        threshold=0.5,
        comparison="lt",
    ),

    # Token usage alerts
    AlertRule(
        name="ai.tokens.high_usage",
        description="Token consumption rate unusually high",
        severity=AlertSeverity.WARNING,
        metric_name="ai.tokens.output.total",
        threshold=1_000_000.0,  # 1M tokens
        comparison="gt",
    ),
]


class AlertEvaluator:
    """
    Evaluate alert rules against current metrics.

    Runs on a schedule (every 60 seconds in production) and fires
    or resolves alerts based on current metric values.

    Usage:
        collector = AIMetricsCollector()
        evaluator = AlertEvaluator(collector)

        # Evaluate all rules
        fired = evaluator.evaluate_all()
        for alert in fired:
            print(f"[{alert.severity.value}] {alert.message}")

        # Check specific rule
        alert = evaluator.evaluate_rule(DEFAULT_ALERT_RULES[0])
    """

    def __init__(
        self,
        metrics_collector: AIMetricsCollector,
        rules: list[AlertRule] | None = None,
        on_fire: Callable[[Alert], None] | None = None,
        on_resolve: Callable[[Alert], None] | None = None,
    ) -> None:
        self._collector = metrics_collector
        self._rules = rules or DEFAULT_ALERT_RULES
        self._on_fire = on_fire or self._default_on_fire
        self._on_resolve = on_resolve or self._default_on_resolve
        self._active_alerts: dict[str, Alert] = {}

    @staticmethod
    def _default_on_fire(alert: Alert) -> None:
        print(f"ALERT FIRING [{alert.severity.value}]: {alert.message} "
              f"(value={alert.current_value:.4f}, threshold={alert.threshold:.4f})")

    @staticmethod
    def _default_on_resolve(alert: Alert) -> None:
        print(f"ALERT RESOLVED: {alert.rule_name}")

    def _get_metric_value(self, metric_name: str) -> float | None:
        """Extract the current value for a metric from the collector."""
        points = self._collector.export_points()
        for point in reversed(points):
            if point.name == metric_name:
                return point.value
        return None

    def evaluate_rule(self, rule: AlertRule) -> Alert | None:
        """Evaluate a single alert rule against current metrics."""
        value = self._get_metric_value(rule.metric_name)
        if value is None:
            return None

        is_firing = rule.evaluate(value)

        if is_firing:
            alert = Alert(
                rule_name=rule.name,
                severity=rule.severity,
                status=AlertStatus.FIRING,
                current_value=value,
                threshold=rule.threshold,
                message=f"{rule.description} ({rule.metric_name}={value:.4f}, "
                        f"threshold={rule.threshold:.4f})",
                tags=rule.tags,
            )

            if rule.name not in self._active_alerts:
                self._on_fire(alert)

            self._active_alerts[rule.name] = alert
            return alert

        elif rule.name in self._active_alerts:
            old_alert = self._active_alerts.pop(rule.name)
            old_alert.status = AlertStatus.RESOLVED
            old_alert.resolved_at = time.time()
            self._on_resolve(old_alert)

        return None

    def evaluate_all(self) -> list[Alert]:
        """Evaluate all alert rules. Return list of currently firing alerts."""
        firing: list[Alert] = []
        for rule in self._rules:
            alert = self.evaluate_rule(rule)
            if alert:
                firing.append(alert)
        return firing

    @property
    def active_alerts(self) -> list[Alert]:
        """Return all currently active (firing) alerts."""
        return list(self._active_alerts.values())


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def demo() -> None:
    """Demonstrate alert evaluation against simulated metrics."""
    import random
    from metrics import AIMetricsCollector, RequestMetrics

    collector = AIMetricsCollector()

    # Simulate some requests with varying characteristics
    for i in range(30):
        collector.record_request(RequestMetrics(
            request_id=f"req-{i:03d}",
            model="gpt-4o-mini",
            provider="openai",
            latency_ms=random.uniform(500, 8000),
            input_tokens=random.randint(200, 3000),
            output_tokens=random.randint(100, 1500),
            total_tokens=random.randint(300, 4500),
            cost_usd=random.uniform(0.001, 0.05),
            quality_score=random.uniform(0.6, 0.95),
            tags={"feature": "chat"},
        ))

    evaluator = AlertEvaluator(collector)

    print("=== Alert Evaluation Demo ===\n")
    firing = evaluator.evaluate_all()

    print(f"\n--- Summary ---")
    print(f"Rules evaluated: {len(DEFAULT_ALERT_RULES)}")
    print(f"Alerts firing:   {len(firing)}")
    print(f"Active alerts:   {len(evaluator.active_alerts)}")


if __name__ == "__main__":
    demo()
