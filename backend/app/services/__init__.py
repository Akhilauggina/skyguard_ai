# ---------------------------------------------------------------------------
# app/services/__init__.py
#
# PURPOSE OF THIS FOLDER:
# The business logic layer. Services orchestrate operations that may span
# multiple models, external calls, or complex rules — keeping API route
# handlers (app/api) thin and focused only on HTTP concerns (parsing
# requests, calling a service, returning a response). A typical service
# function takes a DB session and validated schema data, does the actual
# work, and returns plain Python objects or ORM instances.
#
# This project is currently foundation-only, so no services are implemented
# yet — this folder exists to establish the intended architecture.
# ---------------------------------------------------------------------------
