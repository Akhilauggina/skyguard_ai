# ---------------------------------------------------------------------------
# app/core/__init__.py
#
# PURPOSE OF THIS FOLDER:
# Cross-cutting, framework-level concerns that support the whole application
# but aren't "business logic" and aren't "configuration". Examples: logging
# setup, exception handlers, middleware, security/auth utilities (password
# hashing, JWT helpers), and application-wide constants. Nothing here should
# depend on any specific feature/domain — only on config and the standard
# library / third-party infra packages.
# ---------------------------------------------------------------------------
