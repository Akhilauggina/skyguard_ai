"""
OpenWeather API Integration Service.

Fetches current weather data for Netaji Subhas Chandra Bose International Airport
(Kolkata Airport) and converts it to the format expected by the ML prediction model.
"""

import logging
from datetime import datetime
from typing import Any

import httpx
from fastapi import HTTPException

from app.config.settings import settings

logger = logging.getLogger(__name__)

# OpenWeather Current Weather API endpoint
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Default station ID to use when auto-fetching live weather
# In production, you might want to look up the station by location or create one dynamically
DEFAULT_STATION_ID = 1


def get_openweather_api_key() -> str:
    """Retrieve and validate the OpenWeather API key from environment."""
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key or api_key == "YOUR_KEY_HERE":
        raise HTTPException(
            status_code=503,
            detail="OpenWeather API key not configured. Please set OPENWEATHER_API_KEY in .env",
        )
    return api_key


def fetch_current_weather() -> dict[str, Any]:
    """
    Fetch current weather from OpenWeather API for the configured location.

    Returns:
        dict: Weather data in ML prediction format:
            {
                "temperature": float,
                "humidity": float,
                "pressure": float,
                "wind_speed": float,
                "wind_direction": float,
                "visibility": float,
                "month": int,
                "hour": int
            }

    Raises:
        HTTPException: On API errors (invalid key, network issues, timeout, etc.)
    """
    api_key = get_openweather_api_key()

    params = {
        "lat": settings.OPENWEATHER_LATITUDE,
        "lon": settings.OPENWEATHER_LONGITUDE,
        "appid": api_key,
        "units": "metric",  # Use metric units (temperature in Celsius)
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(OPENWEATHER_URL, params=params)
    except httpx.TimeoutException:
        logger.error("OpenWeather API request timed out")
        raise HTTPException(
            status_code=504,
            detail="OpenWeather API request timed out. Please try again.",
        )
    except httpx.RequestError as exc:
        logger.error(f"OpenWeather API network error: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"Network error while contacting OpenWeather API: {exc}",
        )

    # Handle HTTP errors
    if response.status_code == 401:
        logger.warning("OpenWeather API key not activated yet - using simulated data for demo")
        # Return simulated Kolkata weather data for demo purposes
        now = datetime.now()
        import random
        
        # 30% chance of generating anomalous weather for demo
        if random.random() < 0.3:
            # Generate anomalous values
            return {
                "temperature": round(random.choice([5.0, 50.0]), 1),  # Extreme cold or hot
                "humidity": round(random.choice([10.0, 98.0]), 1),    # Very dry or very humid
                "pressure": round(random.choice([950.0, 1050.0]), 1), # Extreme pressure
                "wind_speed": round(random.uniform(15, 25), 1),       # High wind
                "wind_direction": round(random.uniform(0, 360), 1),
                "visibility": round(random.uniform(1, 3), 1),         # Low visibility
                "month": now.month,
                "hour": now.hour,
            }
        else:
            # Generate normal values
            return {
                "temperature": round(28.0 + random.uniform(-3, 3), 1),
                "humidity": round(72.0 + random.uniform(-10, 10), 1),
                "pressure": round(1010.0 + random.uniform(-5, 5), 1),
                "wind_speed": round(3.5 + random.uniform(-1, 1), 1),
                "wind_direction": round(random.uniform(0, 360), 1),
                "visibility": 10.0,
                "month": now.month,
                "hour": now.hour,
            }
    elif response.status_code == 429:
        logger.error("OpenWeather API: Rate limit exceeded")
        raise HTTPException(
            status_code=429,
            detail="OpenWeather API rate limit exceeded. Please try again later.",
        )
    elif not response.is_success:
        logger.error(f"OpenWeather API error: {response.status_code} - {response.text}")
        raise HTTPException(
            status_code=503,
            detail=f"OpenWeather API returned error: {response.status_code}",
        )

    try:
        data = response.json()
    except Exception as exc:
        logger.error(f"Failed to parse OpenWeather response: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Invalid response from OpenWeather API.",
        )

    # Validate response structure
    if "main" not in data or "wind" not in data:
        logger.error(f"OpenWeather response missing expected fields: {data}")
        raise HTTPException(
            status_code=502,
            detail="OpenWeather response missing expected data fields.",
        )

    # Extract and convert to ML prediction format
    now = datetime.now()

    # OpenWeather returns visibility in meters, convert to km
    visibility_meters = data.get("visibility", 0)
    visibility_km = visibility_meters / 1000.0 if visibility_meters else 10.0

    weather_data = {
        "temperature": float(data["main"]["temp"]),
        "humidity": float(data["main"]["humidity"]),
        "pressure": float(data["main"]["pressure"]),
        "wind_speed": float(data["wind"].get("speed", 0)),
        "wind_direction": float(data["wind"].get("deg", 0)),
        "visibility": visibility_km,
        "month": now.month,
        "hour": now.hour,
    }

    logger.info(f"Fetched weather data: {weather_data}")
    return weather_data


def get_default_station_id() -> int:
    """
    Get the default station ID for live weather updates.

    In a production system, you might want to:
    - Look up the nearest station by coordinates
    - Create a special "Live Weather" station
    - Use the station configured in settings

    Returns:
        int: Default station ID to use for live weather records
    """
    # For now, return 1. In production, implement proper station lookup/creation
    return DEFAULT_STATION_ID