# ---------------------------------------------------------------------------
# app/core/logging_config.py
#
# Centralized logging setup for the application. Called once at startup
# (see app/main.py) so every module can simply do:
#     import logging
#     logger = logging.getLogger(__name__)
# and have consistent formatting/levels across the whole app.
# ---------------------------------------------------------------------------

import logging
import sys

from app.config.settings import settings


def configure_logging() -> None:
    """Configure the root logger's format, level, and output stream."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    logging.getLogger(__name__).info(
        "Logging configured (env=%s, level=%s)", settings.APP_ENV, logging.getLevelName(log_level)
    )
