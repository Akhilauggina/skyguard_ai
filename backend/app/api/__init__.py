# ---------------------------------------------------------------------------
# app/api/__init__.py
#
# PURPOSE OF THIS FOLDER:
# HTTP layer of the application — FastAPI routers and endpoint functions.
# Organized by API version (currently just "v1") so future breaking changes
# can live alongside older versions without disrupting existing clients.
# Route handlers here should stay thin: validate input via app/schemas,
# delegate real work to app/services, and return a schema-shaped response.
# ---------------------------------------------------------------------------
