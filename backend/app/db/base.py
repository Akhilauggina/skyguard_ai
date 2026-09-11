# ---------------------------------------------------------------------------
# app/db/base.py
#
# Import aggregator used by Alembic's autogenerate feature.
#
# When migrations are introduced, Alembic's env.py will import
# `Base` from this module so it can "see" every model class and generate
# migrations automatically. As new models are added to app/models, import
# them below so they get registered on Base.metadata.
#
# Example (future usage, once models exist):
#     from app.db.base_class import Base
#     from app.models.user import User  # noqa
#     from app.models.flight import Flight  # noqa
# ---------------------------------------------------------------------------

from app.db.base_class import Base  # noqa: F401  (re-exported for Alembic)
from app.models import Alert, Prediction, Station, User, WeatherReading  # noqa: F401

