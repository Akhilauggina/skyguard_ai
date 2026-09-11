# ---------------------------------------------------------------------------
# app/db/session.py
#
# Creates the SQLAlchemy engine and session factory used to talk to
# PostgreSQL, and exposes a `get_db` generator to be used as a FastAPI
# dependency for obtaining a request-scoped database session.
#
# NOTE: No tables/models exist yet in this foundation. This module makes the
# app "ready for PostgreSQL integration" as soon as DATABASE_URL in .env
# points at a real database and models are added under app/models.
# ---------------------------------------------------------------------------

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings

# The engine manages the actual connection pool to PostgreSQL.
# `pool_pre_ping=True` checks connections are alive before using them,
# which avoids errors from stale connections (e.g. after DB restarts).
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

# SessionLocal is a factory that produces new Session objects bound to
# the engine above. Each incoming request gets its own session (see
# `get_db` below) so sessions are never shared across requests.
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session for the lifetime of
    a single request, and guarantees it is closed afterwards — even if the
    request raises an exception.

    Usage in a future endpoint:
        from fastapi import Depends
        from app.db.session import get_db

        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
