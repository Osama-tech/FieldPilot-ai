import pytest

from app.domain.rule_provider import RuleProvider
from app.tools.risk_assessment_tool import RiskAssessmentTool


class FakeRuleProvider(RuleProvider):
    def __init__(self, rules: dict) -> None:
        self._rules = rules

    def get_rules(self) -> dict:
        return self._rules


DEFAULT_RULES = {
    "max_wind_speed_kmh": 24,
    "max_precipitation_mm": 5,
    "min_temperature_c": 5,
    "max_temperature_c": 35,
}


@pytest.mark.asyncio
async def test_execute_returns_safe_when_all_checks_pass() -> None:
    tool = RiskAssessmentTool(rule_provider=FakeRuleProvider(DEFAULT_RULES))

    result = await tool.execute(
        {"wind_speed_kmh": 12, "precipitation_mm": 0, "temperature_c": 22}
    )

    assert result.success is True
    assert result.data["decision"] == "safe"
    assert len(result.data["contributing_factors"]) == 3


@pytest.mark.asyncio
async def test_execute_returns_conditional_with_one_violation() -> None:
    tool = RiskAssessmentTool(rule_provider=FakeRuleProvider(DEFAULT_RULES))

    result = await tool.execute(
        {"wind_speed_kmh": 30, "precipitation_mm": 0, "temperature_c": 22}
    )

    assert result.success is True
    assert result.data["decision"] == "conditional"


@pytest.mark.asyncio
async def test_execute_returns_not_safe_with_two_violations() -> None:
    tool = RiskAssessmentTool(rule_provider=FakeRuleProvider(DEFAULT_RULES))

    result = await tool.execute(
        {"wind_speed_kmh": 30, "precipitation_mm": 10, "temperature_c": 22}
    )

    assert result.success is True
    assert result.data["decision"] == "not_safe"


@pytest.mark.asyncio
async def test_execute_rejects_invalid_weather_input() -> None:
    tool = RiskAssessmentTool(rule_provider=FakeRuleProvider(DEFAULT_RULES))

    result = await tool.execute(
        {"wind_speed_kmh": -5, "precipitation_mm": 0, "temperature_c": 22}
    )

    assert result.success is False
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_execute_handles_missing_rule_key() -> None:
    incomplete_rules = {"max_wind_speed_kmh": 24}
    tool = RiskAssessmentTool(rule_provider=FakeRuleProvider(incomplete_rules))

    result = await tool.execute(
        {"wind_speed_kmh": 12, "precipitation_mm": 0, "temperature_c": 22}
    )

    assert result.success is False
    assert result.error_message is not None