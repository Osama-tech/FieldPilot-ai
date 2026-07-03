"""Core domain models. No framework or SDK imports allowed here."""

from typing import Literal, Optional

from pydantic import BaseModel


class WeatherData(BaseModel):
    wind_speed_kmh: float
    precipitation_mm: float
    temperature_c: float


class FieldInfo(BaseModel):
    field_id: str
    size_hectares: float
    crop_type: str


class ToolResult(BaseModel):
    success: bool
    data: Optional[dict] = None
    error_message: Optional[str] = None


class SprayRecommendation(BaseModel):
    decision: Literal["safe", "not_safe", "conditional"]
    reasoning: str
    contributing_factors: list[str]