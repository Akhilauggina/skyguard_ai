# ---------------------------------------------------------------------------
# app/schemas/health.py
#
# Response schema for the GET /health endpoint. Kept minimal and generic —
# this describes infrastructure status, not a business domain.
# ---------------------------------------------------------------------------

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Shape of the JSON body returned by GET /health."""

    status: str = Field(..., description="Overall service status, e.g. 'ok'.", examples=["ok"])
    app_name: str = Field(..., description="Name of the application.")
    version: str = Field(..., description="Current application version.")
    environment: str = Field(..., description="Running environment (development/staging/production).")
