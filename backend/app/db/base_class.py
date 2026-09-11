# ---------------------------------------------------------------------------
# app/db/base_class.py
#
# Defines the single declarative Base that every SQLAlchemy model (in
# app/models) must inherit from. Keeping it in its own tiny module avoids
# circular imports between app/db/session.py and app/models/*.
# ---------------------------------------------------------------------------

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Shared declarative base class for all ORM models.

    Example (future usage, once models are implemented):
        from app.db.base_class import Base

        class User(Base):
            __tablename__ = "users"
            ...
    """
    pass
