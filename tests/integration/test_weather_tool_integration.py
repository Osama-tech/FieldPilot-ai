import pytest

from app.infrastructure.weather_api_client import WeatherAPIClient
from app.tools.weather_tool import WeatherTool


@pytest.mark.asyncio
async def test_execute_returns_real_weather_data() -> None:
    tool = WeatherTool(weather_api_client=WeatherAPIClient())

    result = await tool.execute({"latitude": 30.0, "longitude": 31.2})

    assert result.success is True
    assert isinstance(result.data["wind_speed_kmh"], (int, float))
    assert isinstance(result.data["temperature_c"], (int, float))