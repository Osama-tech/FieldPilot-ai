import pytest
from pydantic import ValidationError

from app.domain.models import FieldInfo, WeatherData


def test_weather_data_accepts_zero_wind_and_precipitation() -> None:
    weather = WeatherData(wind_speed_kmh=0, precipitation_mm=0, temperature_c=-5)

    assert weather.wind_speed_kmh == 0
    assert weather.temperature_c == -5


def test_weather_data_rejects_negative_wind_speed() -> None:
    with pytest.raises(ValidationError):
        WeatherData(wind_speed_kmh=-1, precipitation_mm=0, temperature_c=20)


def test_field_info_rejects_empty_field_id() -> None:
    with pytest.raises(ValidationError):
        FieldInfo(field_id="", size_hectares=10, crop_type="wheat")


def test_field_info_rejects_zero_size() -> None:
    with pytest.raises(ValidationError):
        FieldInfo(field_id="F1", size_hectares=0, crop_type="wheat")