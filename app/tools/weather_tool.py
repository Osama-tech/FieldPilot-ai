"""Weather tool: fetches current conditions for a location from Open-Meteo."""

import httpx
from pydantic import BaseModel, Field, ValidationError

from app.domain.models import ToolResult, WeatherData
from app.tools.base import Tool

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherInput(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class WeatherTool(Tool):
    async def execute(self, input_data: dict) -> ToolResult:
        try:
            parsed = WeatherInput(**input_data)
        except ValidationError as e:
            return ToolResult(success=False, error_message=str(e))

        params = {
            "latitude": parsed.latitude,
            "longitude": parsed.longitude,
            "current": "temperature_2m,precipitation,wind_speed_10m",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(OPEN_METEO_URL, params=params)
                response.raise_for_status()
        except httpx.HTTPError as e:
            return ToolResult(success=False, error_message=str(e))

        try:
            current = response.json()["current"]
            weather = WeatherData(
                wind_speed_kmh=current["wind_speed_10m"],
                precipitation_mm=current["precipitation"],
                temperature_c=current["temperature_2m"],
            )
        except (KeyError, ValidationError) as e:
            return ToolResult(success=False, error_message=f"Unexpected response format: {e}")

        return ToolResult(success=True, data=weather.model_dump())