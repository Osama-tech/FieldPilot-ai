import pytest
import httpx
from pytest_httpx import HTTPXMock

from app.tools.weather_tool import WeatherTool


@pytest.mark.asyncio
async def test_execute_returns_weather_data_on_success(httpx_mock: HTTPXMock) -> None:
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

    tool = WeatherTool()
    result = await tool.execute({"latitude": 30.0, "longitude": 31.2})

    assert result.success is True
    assert result.data["wind_speed_kmh"] == 12.3
    assert result.data["temperature_c"] == 34.5


@pytest.mark.asyncio
async def test_execute_rejects_invalid_latitude(httpx_mock: HTTPXMock) -> None:
    tool = WeatherTool()
    result = await tool.execute({"latitude": 999, "longitude": 31.2})

    assert result.success is False
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_execute_handles_network_failure(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    tool = WeatherTool()
    result = await tool.execute({"latitude": 30.0, "longitude": 31.2})

    assert result.success is False
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_execute_handles_malformed_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={"current": {"temperature_2m": 34.5}})

    tool = WeatherTool()
    result = await tool.execute({"latitude": 30.0, "longitude": 31.2})

    assert result.success is False
    assert result.error_message is not None