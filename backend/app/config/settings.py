# ---------------------------------------------------------------------------
# app/config/settings.py
#
# Defines a typed, validated Settings object using pydantic-settings.
# Values are read from environment variables, which are in turn loaded from
# the ".env" file at the project root (see the `env_file` setting below).
#
# Usage elsewhere in the app:
#     from app.config.settings import settings
#     print(settings.DATABASE_URL)
# ---------------------------------------------------------------------------

from functools import lru_cache
from typing import Any, List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application settings.

    Every attribute here maps to an environment variable of the same name.
    Pydantic validates types automatically and raises a clear error at
    startup if a required value is missing or malformed — far better than
    discovering a bad config value deep inside a request handler.
    """

    # --- Application metadata ---------------------------------------------
    APP_NAME: str = "SkyGuard AI"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"  # development | staging | production
    DEBUG: bool = True

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        """Parse boolean debug flags or tolerate log levels like 'WARN' from environment."""
        if isinstance(v, str):
            val = v.strip().lower()
            if val in ("true", "1", "yes", "t", "on"):
                return True
            if val in ("false", "0", "no", "f", "off"):
                return False
            return val == "debug"
        return bool(v)

    # --- API -----------------------------------------------------------------
    API_V1_PREFIX: str = "/api/v1"

    # --- CORS ------------------------------------------------------------------
    # Raw comma-separated string from the .env file, e.g. "http://a.com,http://b.com"
    BACKEND_CORS_ORIGINS: str = ""

    # --- Database --------------------------------------------------------------
    # Ready for PostgreSQL: expects a SQLAlchemy-compatible connection URL,
    # e.g. postgresql+psycopg2://user:password@host:port/dbname
    DATABASE_URL: str = "postgresql+psycopg2://skyguard_user:skyguard_password@localhost:5432/skyguard_db"

    # --- Security ----------------------------------------------------------------
    SECRET_KEY: str = "change-this-to-a-long-random-string"

    # Tells pydantic-settings where to load environment variables from and
    # how to parse the .env file (UTF-8, case-sensitive keys).
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert the comma-separated BACKEND_CORS_ORIGINS string into a list."""
        if not self.BACKEND_CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    lru_cache ensures the .env file is parsed only once per process instead
    of on every import/request, which is both faster and avoids subtle bugs
    from re-reading the environment mid-run.
    """
    return Settings()


# Convenience singleton — most modules will just do:
#   from app.config.settings import settings
settings = get_settings()
