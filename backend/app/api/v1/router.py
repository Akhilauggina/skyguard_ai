from fastapi import APIRouter

from app.api.routes.station import router as station_router

api_router = APIRouter()

api_router.include_router(station_router)