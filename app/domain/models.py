"""Core domain models. No framework or SDK imports allowed here."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    wind_speed_kmh: float = Field(ge=0)
    precipitation_mm: float = Field(ge=0)
    temperature_c: float


class FieldInfo(BaseModel):
    field_id: str = Field(min_length=1)
    size_hectares: float = Field(gt=0)
    crop_type: str


class ToolResult(BaseModel):
    success: bool
    data: Optional[dict] = None
    error_message: Optional[str] = None


class SprayRecommendation(BaseModel):
    decision: Literal["safe", "not_safe", "conditional"]
    reasoning: str
    contributing_factors: list[str]