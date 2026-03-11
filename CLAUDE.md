# CLAUDE.md

## Project Overview

**med_agent** - FastAPI application generated with [Full-Stack FastAPI + Next.js Template](https://github.com/vstorm-co/full-stack-ai-agent-template).

**Stack:** FastAPI + Pydantic v2, MongoDB (async), JWT auth, LangChain, Next.js 15
## Commands

```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload --port 8000
pytest
ruff check . --fix && ruff format .
# Frontend
cd frontend
bun dev
bun test```

## Project Structure

```
backend/app/
├── api/routes/v1/    # HTTP endpoints
├── services/         # Business logic
├── repositories/     # Data access
├── schemas/          # Pydantic models
├── db/models/        # Database models
├── core/config.py    # Settings├── agents/           # AI agents└── commands/         # CLI commands
```

## Key Conventions

- Use `db.flush()` in repositories (not `commit`)
- Services raise domain exceptions (`NotFoundError`, `AlreadyExistsError`)
- Schemas: separate `Create`, `Update`, `Response` models
- Commands auto-discovered from `app/commands/`

## Where to Find More Info

Before starting complex tasks, read relevant docs:
- **Architecture details:** `docs/architecture.md`
- **Adding features:** `docs/adding_features.md`
- **Testing guide:** `docs/testing.md`
- **Code patterns:** `docs/patterns.md`

## Environment Variables

Key variables in `.env`:
```bash
ENVIRONMENT=localSECRET_KEY=change-me-use-openssl-rand-hex-32OPENAI_API_KEY=sk-...LANGCHAIN_API_KEY=your-api-key```
