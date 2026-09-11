# ---------------------------------------------------------------------------
# app/schemas/__init__.py
#
# PURPOSE OF THIS FOLDER:
# Pydantic schemas used for request/response validation and serialization
# at the API boundary. These are distinct from app/models (SQLAlchemy ORM
# classes): a schema describes "what shape of JSON goes in/out of an
# endpoint", while a model describes "what a database row looks like".
# Keeping them separate lets the API contract evolve independently of the
# database schema.
#
# This project is currently foundation-only, so no schemas are defined yet
# beyond the generic health-check schema used by the /health endpoint.
# ---------------------------------------------------------------------------
