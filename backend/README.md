# SkyGuard AI — Backend Foundation

A production-ready **FastAPI** backend foundation for SkyGuard AI, built with
Python 3.12+, SQLAlchemy, Pydantic, and Uvicorn. This is the project
scaffold only — no business logic or domain models are implemented yet.

## Folder structure

```
skyguard-ai/
├── .env                     # Local environment variables (not committed)
├── .env.example             # Template documenting required env vars
├── requirements.txt         # Python dependencies
├── run.py                   # `python run.py` launcher (alternative to uvicorn CLI)
└── app/
    ├── main.py              # FastAPI app creation, middleware, router mounting
    ├── config/               # Environment/config loading (pydantic-settings)
    │   └── settings.py
    ├── core/                  # Cross-cutting concerns: logging, (future) security
    │   └── logging_config.py
    ├── db/                     # SQLAlchemy engine, session, declarative Base
    │   ├── base_class.py
    │   ├── base.py            # Alembic model-import aggregator
    │   └── session.py
    ├── models/                 # SQLAlchemy ORM models (empty — foundation only)
    ├── schemas/                # Pydantic request/response schemas
    │   └── health.py
    ├── services/                # Business logic layer (empty — foundation only)
    └── api/
        ├── deps.py               # Shared FastAPI dependencies (e.g. get_db)
        └── v1/
            ├── router.py          # Aggregates all v1 endpoint routers
            └── endpoints/
                └── health.py       # GET /api/v1/health
```

Each folder's `__init__.py` contains a comment explaining its role in the
architecture — start there if you're getting oriented.

## Setup

```bash
# 1. Create and activate a virtual environment (Python 3.12+)
python3.12 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# edit .env and set a real DATABASE_URL, SECRET_KEY, etc.

# 4. Run the app
uvicorn app.main:app --reload
# or:
python run.py
```

The API will be available at `http://localhost:8000`.

## Endpoints

| Method | Path               | Description                          |
|--------|--------------------|---------------------------------------|
| GET    | `/`                | Root welcome/info endpoint            |
| GET    | `/api/v1/health`   | Health check                          |
| GET    | `/docs`            | Interactive Swagger UI (auto-generated) |
| GET    | `/redoc`           | ReDoc API documentation                |

## PostgreSQL readiness

`app/db/session.py` already creates a SQLAlchemy engine and session factory
from `DATABASE_URL` in `.env`, and `app/api/deps.py` exposes a `get_db`
dependency ready to be injected into future endpoints. To start persisting
data:

1. Point `DATABASE_URL` in `.env` at a real PostgreSQL instance.
2. Add ORM model classes under `app/models/`, inheriting from
   `app.db.base_class.Base`.
3. Import new models in `app/db/base.py` so Alembic can detect them.
4. Initialize Alembic (`alembic init alembic`) when migrations are needed.

## Notes

This scaffold intentionally contains **no business logic** — `models/` and
`services/` are empty placeholders establishing the intended architecture
for future feature work.
