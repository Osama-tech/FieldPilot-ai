"""Infrastructure client for fetching current weather conditions from Open-Meteo."""

import httpx
from pydantic import ValidationError

from app.domain.models import WeatherData

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAPIError(Exception):
    """Raised when the weather API call fails or returns an unexpected shape."""


class WeatherAPIClient:
    async def fetch_weather(self, latitude: float, longitude: float) -> WeatherData:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,precipitation,wind_speed_10m",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(OPEN_METEO_URL, params=params)
                response.raise_for_status()
        except httpx.HTTPError as e:
            raise WeatherAPIError(str(e)) from e

        try:
            current = response.json()["current"]
            return WeatherData(
                wind_speed_kmh=current["wind_speed_10m"],
                precipitation_mm=current["precipitation"],
                temperature_c=current["temperature_2m"],
            )
        except (KeyError, ValidationError) as e:
            raise WeatherAPIError(f"Unexpected response format: {e}") from e