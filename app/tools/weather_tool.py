"""Weather tool: validates input and delegates to WeatherAPIClient."""

from pydantic import BaseModel, Field, ValidationError

from app.domain.models import ToolResult
from app.infrastructure.weather_api_client import WeatherAPIClient, WeatherAPIError
from app.tools.base import Tool


class WeatherInput(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class WeatherTool(Tool):
    def __init__(self, weather_api_client: WeatherAPIClient) -> None:
        self._weather_api_client = weather_api_client

    async def execute(self, input_data: dict) -> ToolResult:
        try:
            parsed = WeatherInput(**input_data)
        except ValidationError as e:
            return ToolResult(success=False, error_message=str(e))

        try:
            weather = await self._weather_api_client.fetch_weather(
                parsed.latitude, parsed.longitude
            )
        except WeatherAPIError as e:
            return ToolResult(success=False, error_message=str(e))

        return ToolResult(success=True, data=weather.model_dump())

    def get_schema(self) -> dict:
        return {
            "name": "weather",
            "description": "Fetches current weather conditions (wind speed, "
            "precipitation, temperature) for a given latitude and longitude.",
            "parameters": WeatherInput.model_json_schema(),
        }