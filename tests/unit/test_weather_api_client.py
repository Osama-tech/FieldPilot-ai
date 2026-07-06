import httpx
import pytest
from pytest_httpx import HTTPXMock

from app.infrastructure.weather_api_client import WeatherAPIClient, WeatherAPIError


@pytest.mark.asyncio
async def test_fetch_weather_returns_weather_data_on_success(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "current": {
                "time": "2026-07-06T14:00",
                "temperature_2m": 34.5,
                "precipitation": 0.0,
                "wind_speed_10m": 12.3,
            }
        }
    )

    client = WeatherAPIClient()
    weather = await client.fetch_weather(30.0, 31.2)

    assert weather.wind_speed_kmh == 12.3
    assert weather.temperature_c == 34.5


@pytest.mark.asyncio
async def test_fetch_weather_raises_on_network_failure(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    client = WeatherAPIClient()

    with pytest.raises(WeatherAPIError):
        await client.fetch_weather(30.0, 31.2)


@pytest.mark.asyncio
async def test_fetch_weather_raises_on_malformed_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={"current": {"temperature_2m": 34.5}})

    client = WeatherAPIClient()

    with pytest.raises(WeatherAPIError):
        await client.fetch_weather(30.0, 31.2)