# ---------------------------------------------------------------------------
# app/core/config.py
#
# Re-exports the central application settings from app.config.settings.
# This ensures consistent configuration loading and avoids duplicate or
# conflicting Settings definitions.
# ---------------------------------------------------------------------------

from app.config.settings import Settings, get_settings, settings

__all__ = ["Settings", "get_settings", "settings"]
