import pytest

from app.domain.models import WeatherData
from app.infrastructure.weather_api_client import WeatherAPIError
from app.tools.weather_tool import WeatherTool


class FakeWeatherAPIClient:
    def __init__(self, weather: WeatherData = None, error: Exception = None) -> None:
        self._weather = weather
        self._error = error

    async def fetch_weather(self, latitude: float, longitude: float) -> WeatherData:
        if self._error:
            raise self._error
        return self._weather


@pytest.mark.asyncio
async def test_execute_returns_weather_data_on_success() -> None:
    fake_client = FakeWeatherAPIClient(
        weather=WeatherData(wind_speed_kmh=12.3, precipitation_mm=0.0, temperature_c=34.5)
    )
    tool = WeatherTool(weather_api_client=fake_client)

    result = await tool.execute({"latitude": 30.0, "longitude": 31.2})

    assert result.success is True
    assert result.data["wind_speed_kmh"] == 12.3


@pytest.mark.asyncio
async def test_execute_rejects_invalid_latitude() -> None:
    fake_client = FakeWeatherAPIClient()
    tool = WeatherTool(weather_api_client=fake_client)

    result = await tool.execute({"latitude": 999, "longitude": 31.2})

    assert result.success is False
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_execute_handles_weather_api_error() -> None:
    fake_client = FakeWeatherAPIClient(error=WeatherAPIError("Connection failed"))
    tool = WeatherTool(weather_api_client=fake_client)

    result = await tool.execute({"latitude": 30.0, "longitude": 31.2})

    assert result.success is False
    assert result.error_message is not None