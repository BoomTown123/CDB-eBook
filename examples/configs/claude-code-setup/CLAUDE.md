# CLAUDE.md

> This is an example CLAUDE.md file. Copy it to your project root and customize for your codebase. Keep it under 300 lines. Shorter is better.

## Project Overview

{PROJECT_NAME} is a {brief description, e.g., SaaS platform for project management built with Flask and HTMX}.

## Tech Stack

- **Backend:** Python 3.12 / Flask
- **Frontend:** HTMX + Jinja2 templates
- **Database:** PostgreSQL 16 with pgvector extension
- **Cache:** Redis 7
- **Infrastructure:** Railway (production), local Docker (development)
- **CI/CD:** GitHub Actions

## Project Structure

```
src/
  app/
    api/          # API route handlers
    models/       # SQLAlchemy models
    services/     # Business logic layer
    templates/    # Jinja2 templates
    static/       # CSS, JS, images
  config.py       # Configuration (reads from env vars)
  extensions.py   # Flask extensions initialization
tests/
  unit/           # Unit tests (mirror src/ structure)
  integration/    # Integration tests (require database)
  conftest.py     # Shared fixtures
migrations/       # Alembic database migrations
scripts/          # Utility scripts
```

## Commands

```bash
# Development
flask run --debug                    # Start dev server on port 5000
flask db upgrade                     # Run pending migrations
flask db migrate -m "description"    # Generate new migration

# Testing
pytest tests/unit                    # Unit tests only (~10 seconds)
pytest tests/integration             # Integration tests (~30 seconds, needs DB)
pytest --cov=src/app                 # Full suite with coverage report

# Linting and Formatting
ruff check src/ tests/               # Lint check
ruff format src/ tests/              # Auto-format
mypy src/                            # Type checking

# Database
docker compose up -d db              # Start local PostgreSQL
flask seed-db                        # Seed development data
```

## Coding Conventions

### Python
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- All functions must have type hints for parameters and return values
- Use `Result` pattern for error handling in service layer (never raise exceptions for expected failures)
- Maximum function length: 30 lines. Extract helper functions if longer.

### API Endpoints
- All responses use the shape: `{"data": ..., "error": ..., "meta": ...}`
- Error responses include a machine-readable `code` and human-readable `message`
- Authentication required on all endpoints except `/health` and `/auth/*`
- Rate limiting: 100 requests/minute per user for standard endpoints

### Database
- All queries go through the repository layer (`src/app/repositories/`)
- Never write raw SQL in route handlers or service functions
- Use parameterized queries only (never string interpolation)
- All tables must have `created_at` and `updated_at` timestamps

### Templates
- HTMX partials go in `templates/partials/`
- Full pages go in `templates/pages/`
- Shared components go in `templates/components/`
- Use `hx-boost` for navigation, `hx-swap` for partial updates

### Testing
- Every service function has at least one unit test
- Integration tests use a test database (not mocks) for database operations
- Test names follow: `test_{function_name}_{scenario}_{expected_outcome}`
- Fixtures in `conftest.py`, not duplicated across test files

## Architecture Decisions

- **Three-layer architecture:** Routes (thin) -> Services (business logic) -> Repositories (data access). Routes never call repositories directly.
- **No ORM queries in services:** Services call repository methods. This keeps the data access layer swappable and testable.
- **HTMX over React:** We chose HTMX for simplicity. No build step, no client-side state management. Server renders HTML. This is a deliberate trade-off: less interactivity, dramatically less complexity.
- **PostgreSQL for everything:** Including vector search (pgvector). We will not add a separate vector database until we exceed 5 million embeddings or 500 QPS on vector queries.

## Common Pitfalls

- The `auth_required` decorator must be the outermost decorator on any route that needs authentication. Putting it after `@validate_input` skips auth checks.
- Redis connections use a pool. Never create new connections per request. Use `extensions.redis_client`.
- Database migrations must be reversible. Always include `downgrade()` logic.
- HTMX partial responses must NOT include the base layout. Check `request.headers.get('HX-Request')` to determine response type.

## Environment Variables

Required in production:
- `DATABASE_URL` -- PostgreSQL connection string
- `REDIS_URL` -- Redis connection string
- `SECRET_KEY` -- Flask session secret (32+ random bytes)
- `API_KEY` -- External API authentication

Never hardcode these values. Always read from `config.py`.
