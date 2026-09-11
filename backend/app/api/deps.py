# ---------------------------------------------------------------------------
# app/api/deps.py
#
# Shared FastAPI dependencies used across endpoint modules (e.g. DB session,
# and — in the future — current-user/auth dependencies). Centralizing them
# here means endpoint files can do a single `from app.api.deps import ...`
# instead of reaching into app/db or app/core directly.
# ---------------------------------------------------------------------------

from app.db.session import get_db  # noqa: F401  (re-exported for endpoint modules)

# Future dependencies (e.g. authentication) will be added here, such as:
#   def get_current_user(...): ...
