# ---------------------------------------------------------------------------
# run.py
#
# Convenience launcher so the app can be started with:
#     python run.py
# as an alternative to:
#     uvicorn app.main:app --reload
#
# Host/port/reload are driven by settings so behavior stays consistent
# with the rest of the app's configuration.
# ---------------------------------------------------------------------------

import uvicorn

from app.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
