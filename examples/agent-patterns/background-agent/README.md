# Background Agent

Autonomous task processor with checkpointing, monitoring, and resource budgets.

**Book reference:** Chapter 6 - Agent Architecture, Sections 1 and 6

## What This Demonstrates

Background agents execute well-defined tasks without human supervision. No one is watching. No one is waiting. They are triggered by schedules, events, or API calls -- not human messages.

This example implements the six background agent design patterns from the book:

1. **Idempotency** - Safe to run the same task twice (idempotency keys prevent duplicates)
2. **Checkpointing** - Saves progress after each task; resumes from interruption
3. **Alerting** - Dead man's switch, failure escalation, budget alarms
4. **Audit logging** - Every task start, completion, and failure is logged
5. **Graceful degradation** - Failed tasks are quarantined; processing continues
6. **Resource budgeting** - Token and cost limits prevent runaway execution

## Files

| File | Purpose |
|------|---------|
| `agent.py` | Main processing loop with retry logic and budget enforcement |
| `tasks.py` | Task definitions, queue management, and checkpointing |
| `monitor.py` | Monitoring, alerting, and the dead man's switch pattern |
| `config.py` | Configuration via environment variables |

Uses the shared provider library at `examples/shared/` for LLM access via OpenRouter.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your OpenRouter API key (https://openrouter.ai/keys)

# Run
python agent.py
```

## How It Works

```
[Load checkpoint if exists]
    |
    v
[For each pending task:]
    |
    +-- Check budget --> [STOP if exhausted]
    |
    +-- Record heartbeat
    |
    +-- Process task via LLM (OpenRouter)
    |       |
    |       +-- Success --> [Mark completed, log result]
    |       |
    |       +-- Failure --> [Retry with backoff]
    |                |
    |                +-- Max retries --> [Quarantine task, alert]
    |
    +-- Save checkpoint
    |
    v
[Report summary]
```

The agent processes a queue of tasks sequentially. After each task (success or failure), it saves a checkpoint to disk. If the process crashes, restarting picks up from the last checkpoint. Tasks that exceed the retry limit are quarantined rather than blocking the entire queue.

## Key Design Decisions

- **Provider abstraction** via `shared/` library. Swap providers by changing `LLM_PROVIDER` in `.env`.
- **File-based checkpointing** for simplicity. Production systems should use Temporal, Redis, or a database.
- **Idempotency keys** on each task prevent duplicate processing across restarts.
- **Token and cost budgets** stop the agent before costs spiral. From the book: "This isn't optional -- it's the difference between a manageable mistake and a resignation letter."
- **Dead man's switch** monitors heartbeats. If the agent goes silent, the monitor fires a critical alert.
- **Temperature 0.0** for deterministic outputs on batch tasks.
- **Async architecture** using `asyncio` for non-blocking LLM calls.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | (required) | OpenRouter API key |
| `LLM_PROVIDER` | `openrouter` | Provider name (`openrouter` or `openai`) |
| `MODEL` | `google/gemini-2.5-flash` | Model to use |
| `BG_AGENT_MAX_RETRIES` | `3` | Max retries per task |
| `BG_AGENT_TIMEOUT` | `300` | Task timeout in seconds |
| `BG_AGENT_POLL_INTERVAL` | `10` | Polling interval in seconds |
| `BG_AGENT_TOKEN_BUDGET` | `50000` | Max tokens per run |
| `BG_AGENT_COST_BUDGET` | `1.00` | Max cost (USD) per run |

## Sample Tasks

The demo includes five sample tasks across three types:

- `summarize` - Condense text into one sentence
- `analyze_sentiment` - Classify sentiment with confidence score
- `extract_entities` - Pull named entities from text

## Extending This Example

- Replace file-based queue with Redis, SQS, or Temporal workflows
- Add a scheduler (cron, APScheduler) for periodic execution
- Connect the monitor to Slack, PagerDuty, or a dashboard
- Add parallel task processing with asyncio.gather()
- Implement exponential backoff between retries
