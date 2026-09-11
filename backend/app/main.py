# ---------------------------------------------------------------------------
# app/main.py
#
# FastAPI application entry point.
# Configures lifecycle events, CORS, database initialization,
# and mounts all API routers.
# ---------------------------------------------------------------------------

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config.settings import settings
from app.core.logging_config import configure_logging
from app.db.database import Base, engine

# Import all models so SQLAlchemy registers them with Base.metadata
from app.models import Alert, Prediction, Station, User, WeatherReading  # noqa: F401

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    configure_logging()

    logger.info(
        "Starting %s v%s (environment=%s, debug=%s)",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.APP_ENV,
        settings.DEBUG,
    )

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema verified successfully.")
    except Exception as exc:
        logger.warning(
            "Database initialization failed: %s",
            exc,
        )

    yield

    logger.info("Shutting down %s", settings.APP_NAME)


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SkyGuard AI — Weather Monitoring & Anomaly Detection API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

origins = settings.cors_origins_list

if not origins and settings.DEBUG:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register API Routes
# ---------------------------------------------------------------------------

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "Running",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": f"{settings.API_V1_PREFIX}/health",
    }