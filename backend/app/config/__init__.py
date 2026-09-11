# ---------------------------------------------------------------------------
# app/config/__init__.py
#
# PURPOSE OF THIS FOLDER:
# Holds everything related to application configuration — reading the .env
# file, defining typed settings, and exposing a single cached "settings"
# object that the rest of the app imports from. Keeping configuration in its
# own layer (separate from "core") makes it obvious where to look when an
# environment variable needs to be added or changed.
# ---------------------------------------------------------------------------
