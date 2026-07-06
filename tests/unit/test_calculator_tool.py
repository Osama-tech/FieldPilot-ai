import pytest

from app.tools.calculator_tool import CalculatorTool


@pytest.mark.asyncio
async def test_execute_returns_correct_total_liters() -> None:
    tool = CalculatorTool()

    result = await tool.execute({"size_hectares": 10, "spray_rate_liters_per_hectare": 2})

    assert result.success is True
    assert result.data["total_liters"] == 20


@pytest.mark.asyncio
async def test_execute_rejects_negative_size() -> None:
    tool = CalculatorTool()

    result = await tool.execute({"size_hectares": -5, "spray_rate_liters_per_hectare": 2})

    assert result.success is False
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_execute_rejects_zero_rate() -> None:
    tool = CalculatorTool()

    result = await tool.execute({"size_hectares": 10, "spray_rate_liters_per_hectare": 0})

    assert result.success is False
    assert result.error_message is not None