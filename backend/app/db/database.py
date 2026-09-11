# ---------------------------------------------------------------------------
# app/db/database.py
#
# Sets up the three core SQLAlchemy building blocks the whole app's
# database access depends on: the Engine, the SessionLocal factory, and
# the declarative Base class that future models will inherit from.
# No models or API routes are defined here — this file is pure database
# plumbing/setup only.
# ---------------------------------------------------------------------------

# create_engine: builds the object that manages the actual connection
# pool to PostgreSQL.
from sqlalchemy import create_engine

# sessionmaker: a factory that produces new Session objects, each one
# representing a single "conversation" with the database.
from sqlalchemy.orm import sessionmaker

from app.db.base_class import Base

# Import our settings object, which already read DATABASE_URL from .env
# via app/core/config.py.
from app.core.config import settings


# ---------------------------------------------------------------------------
# ENGINE
# The Engine is the starting point for any SQLAlchemy application. It is
# the object that actually knows how to talk to PostgreSQL: it manages a
# pool of real network connections so the app isn't opening/closing a new
# TCP connection to the database on every single query.
# ---------------------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,   # the connection string read from .env
    pool_pre_ping=True,      # test each connection is alive before using it,
                              # so a stale/dropped connection doesn't cause
                              # a confusing error mid-request
)


# ---------------------------------------------------------------------------
# SESSIONLOCAL
# SessionLocal is a factory (not a session itself). Calling SessionLocal()
# creates one new Session object, which is what you actually use to run
# queries, add new rows, and commit/rollback changes.
#
# We configure it once here, bound to our engine, so every part of the
# app that needs a database session creates it the same, correct way.
# ---------------------------------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,        # every session created will use our engine's connections
    autocommit=False,   # changes are NOT saved to the DB until we explicitly commit()
    autoflush=False,    # SQLAlchemy won't auto-send pending changes before every query
)


# ---------------------------------------------------------------------------
# BASE
# Shared declarative Base re-exported from app.db.base_class.
# ---------------------------------------------------------------------------
# Base is imported and re-exported from app.db.base_class
__all__ = ["engine", "SessionLocal", "Base"]