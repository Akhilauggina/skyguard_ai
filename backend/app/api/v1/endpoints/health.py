# ---------------------------------------------------------------------------
# app/api/v1/endpoints/health.py
#
# Simple, dependency-free health check endpoint. Used by load balancers,
# container orchestrators (e.g. Kubernetes liveness/readiness probes), and
# uptime monitors to verify the service process is up and responding.
#
# Deliberately does NOT check the database yet (no business logic / DB
# models exist in this foundation) — it only confirms the API process
# itself is alive and correctly configured.
# ---------------------------------------------------------------------------

from fastapi import APIRouter

from app.config.settings import settings
from app.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health check",
    description="Returns the current status of the SkyGuard AI service.",
    tags=["Health"],
)
def health_check() -> HealthCheckResponse:
    """Lightweight liveness check — always returns 'ok' if the app is running."""
    return HealthCheckResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )
