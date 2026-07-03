from typing import Optional

import httpx

from app.domain.models import WeatherData


class WeatherAPIClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    async def fetch_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> Optional[WeatherData]:
        raise NotImplementedError
