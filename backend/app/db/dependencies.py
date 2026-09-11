"""
Database dependency.

Every API request gets its own SQLAlchemy Session.

Flow:

Request
   ↓
get_db()
   ↓
SessionLocal()
   ↓
CRUD Operations
   ↓
close()
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Creates a new database session for every request.

    FastAPI automatically closes it after the request completes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()