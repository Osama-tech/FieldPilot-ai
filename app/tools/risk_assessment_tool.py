"""Risk assessment tool: evaluates weather against safety rules to produce a spray recommendation."""

from pydantic import ValidationError

from app.domain.models import SprayRecommendation, ToolResult, WeatherData
from app.domain.rule_provider import RuleProvider
from app.tools.base import Tool


class RiskAssessmentTool(Tool):
    def __init__(self, rule_provider: RuleProvider) -> None:
        self._rule_provider = rule_provider

    async def execute(self, input_data: dict) -> ToolResult:
        try:
            weather = WeatherData(**input_data)
        except ValidationError as e:
            return ToolResult(success=False, error_message=str(e))

        try:
            rules = self._rule_provider.get_rules()
            max_wind = rules["max_wind_speed_kmh"]
            max_precip = rules["max_precipitation_mm"]
            min_temp = rules["min_temperature_c"]
            max_temp = rules["max_temperature_c"]
        except KeyError as e:
            return ToolResult(success=False, error_message=f"Missing safety rule: {e}")

        contributing_factors = []
        violations = 0

        if weather.wind_speed_kmh <= max_wind:
            contributing_factors.append(
                f"Wind speed OK: {weather.wind_speed_kmh} km/h <= {max_wind} km/h"
            )
        else:
            contributing_factors.append(
                f"Wind speed exceeds limit: {weather.wind_speed_kmh} km/h > {max_wind} km/h"
            )
            violations += 1

        if weather.precipitation_mm <= max_precip:
            contributing_factors.append(
                f"Precipitation OK: {weather.precipitation_mm} mm <= {max_precip} mm"
            )
        else:
            contributing_factors.append(
                f"Precipitation exceeds limit: {weather.precipitation_mm} mm > {max_precip} mm"
            )
            violations += 1

        if min_temp <= weather.temperature_c <= max_temp:
            contributing_factors.append(
                f"Temperature OK: {weather.temperature_c}\u00b0C within allowed range"
            )
        else:
            contributing_factors.append(
                f"Temperature outside allowed range: {weather.temperature_c}\u00b0C "
                f"(allowed {min_temp}-{max_temp}\u00b0C)"
            )
            violations += 1

        if violations == 0:
            decision = "safe"
        elif violations == 1:
            decision = "conditional"
        else:
            decision = "not_safe"

        recommendation = SprayRecommendation(
            decision=decision,
            reasoning=f"{violations} safety rule(s) violated out of 3 checks.",
            contributing_factors=contributing_factors,
        )

        return ToolResult(success=True, data=recommendation.model_dump())