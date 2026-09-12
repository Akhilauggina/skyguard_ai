from fastapi import APIRouter
from app.api.routes.alert import router as alert_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.prediction import router as prediction_router
from app.api.routes.station import router as station_router
from app.api.routes.weather_reading import router as weather_reading_router
from app.api.v1.endpoints.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(station_router)
api_router.include_router(weather_reading_router)
api_router.include_router(prediction_router)
api_router.include_router(dashboard_router)
api_router.include_router(alert_router)