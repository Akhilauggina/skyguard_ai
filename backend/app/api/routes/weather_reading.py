from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.weather_reading import (
    create_weather_reading,
    delete_weather_reading,
    get_all_weather_readings,
    get_station_readings,
    get_weather_reading_by_id,
    update_weather_reading,
)
from app.db.dependencies import get_db
from app.schemas.weather_reading import (
    LiveWeatherResponse,
    WeatherReadingCreate,
    WeatherReadingResponse,
    WeatherReadingUpdate,
)
from app.services.prediction_service import predict_weather
from app.services.weather_api_service import fetch_current_weather, get_default_station_id

router = APIRouter(
    prefix="/weather-readings",
    tags=["Weather Readings"],
)


@router.post(
    "",
    response_model=WeatherReadingResponse,
    status_code=201,
    summary="Create a new weather reading",
)
def create_reading(
    reading: WeatherReadingCreate,
    db: Session = Depends(get_db),
):
    return create_weather_reading(db, reading)


@router.get(
    "",
    response_model=list[WeatherReadingResponse],
    summary="Get all weather readings",
)
def get_all_readings(
    db: Session = Depends(get_db),
):
    return get_all_weather_readings(db)


@router.get(
    "/station/{station_id}",
    response_model=list[WeatherReadingResponse],
    summary="Get all weather readings for a station",
)
def get_readings_by_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    return get_station_readings(db, station_id)


@router.get(
    "/{id}",
    response_model=WeatherReadingResponse,
    summary="Get a weather reading by ID",
)
def get_reading(
    id: int,
    db: Session = Depends(get_db),
):
    return get_weather_reading_by_id(db, id)


@router.put(
    "/{id}",
    response_model=WeatherReadingResponse,
    summary="Update a weather reading by ID",
)
def update_reading(
    id: int,
    reading: WeatherReadingUpdate,
    db: Session = Depends(get_db),
):
    return update_weather_reading(db, id, reading)


@router.delete(
    "/{id}",
    summary="Delete a weather reading by ID",
)
def delete_reading(
    id: int,
    db: Session = Depends(get_db),
):
    return delete_weather_reading(db, id)


@router.post(
    "/fetch-live",
    response_model=LiveWeatherResponse,
    summary="Fetch live weather and create reading with prediction",
)
def fetch_live_weather(db: Session = Depends(get_db)):
    """
    Fetch current weather from OpenWeather API for Kolkata Airport,
    save it as a weather reading, run ML prediction, and return both results.
    """
    # Step 1: Fetch current weather from OpenWeather
    weather_data = fetch_current_weather()

    # Step 2: Get or create default station for live weather
    from app.crud.station import get_all_stations, create_station
    from app.schemas.station import StationCreate
    from datetime import date

    stations = get_all_stations(db)
    
    if not stations:
        # Create default station for Kolkata Airport
        station_create = StationCreate(
            station_code="KOLKATA_AIRPORT",
            name="Netaji Subhas Chandra Bose International Airport",
            city="Kolkata",
            state="West Bengal",
            latitude=22.654739,
            longitude=88.446722,
            status="ACTIVE",
            installation_date=date.today(),
        )
        station = create_station(db, station_create)
        station_id = station.id
    else:
        # Use first station
        station_id = stations[0].id

    # Step 3: Save weather reading
    from datetime import datetime, timezone

    reading_create = WeatherReadingCreate(
        station_id=station_id,
        temperature=weather_data["temperature"],
        pressure=weather_data["pressure"],
        humidity=weather_data["humidity"],
        recorded_at=datetime.now(timezone.utc),
    )

    reading = create_weather_reading(db, reading_create)

    # Step 4: Run ML prediction
    prediction_result = predict_weather(weather_data)

    # Step 5: Return combined response
    return LiveWeatherResponse(
        weather={
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "pressure": weather_data["pressure"],
            "wind_speed": weather_data["wind_speed"],
            "wind_direction": weather_data["wind_direction"],
            "visibility": weather_data["visibility"],
        },
        prediction={
            "prediction": prediction_result["prediction"],
            "score": prediction_result["score"],
        },
    )
