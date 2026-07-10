import pytest

from app.composition_root import build_tool_registry
from app.tools.calculator_tool import CalculatorTool
from app.tools.risk_assessment_tool import RiskAssessmentTool
from app.tools.weather_tool import WeatherTool


def test_build_tool_registry_registers_all_expected_tools() -> None:
    registry = build_tool_registry()

    assert isinstance(registry.get("calculator"), CalculatorTool)
    assert isinstance(registry.get("weather"), WeatherTool)
    assert isinstance(registry.get("risk_assessment"), RiskAssessmentTool)


@pytest.mark.asyncio
async def test_registered_calculator_tool_actually_works() -> None:
    registry = build_tool_registry()
    calculator = registry.get("calculator")

    result = await calculator.execute(
        {"size_hectares": 10, "spray_rate_liters_per_hectare": 2}
    )

    assert result.success is True
    assert result.data["total_liters"] == 20