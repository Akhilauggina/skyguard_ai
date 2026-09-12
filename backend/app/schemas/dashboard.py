from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_stations: int
    active_stations: int
    inactive_stations: int
    total_readings: int
    total_alerts: int