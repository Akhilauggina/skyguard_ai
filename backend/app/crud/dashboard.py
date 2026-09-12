from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.station import Station
from app.models.weather_reading import WeatherReading


def get_dashboard_stats(db: Session):
    total_stations = db.query(func.count(Station.id)).scalar()

    active_stations = (
        db.query(func.count(Station.id))
        .filter(Station.status == "ACTIVE")
        .scalar()
    )

    inactive_stations = (
        db.query(func.count(Station.id))
        .filter(Station.status != "ACTIVE")
        .scalar()
    )

    total_readings = db.query(func.count(WeatherReading.id)).scalar()

    total_alerts = db.query(func.count(Alert.id)).scalar()

    return {
        "total_stations": total_stations,
        "active_stations": active_stations,
        "inactive_stations": inactive_stations,
        "total_readings": total_readings,
        "total_alerts": total_alerts,
    }