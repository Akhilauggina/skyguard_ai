# ---------------------------------------------------------------------------
# app/db/__init__.py
#
# PURPOSE OF THIS FOLDER:
# Everything related to the database connection layer: the SQLAlchemy
# engine, session factory, declarative Base class, and the FastAPI
# dependency used to obtain a request-scoped DB session. ORM *models*
# (table definitions) live in app/models, not here — this folder is purely
# about the plumbing that connects the app to PostgreSQL.
# ---------------------------------------------------------------------------
