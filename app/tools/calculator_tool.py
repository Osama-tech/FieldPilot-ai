"""Calculator tool: computes total chemical volume required for a field."""

from pydantic import BaseModel, Field, ValidationError

from app.domain.models import ToolResult
from app.tools.base import Tool


class CalculatorInput(BaseModel):
    size_hectares: float = Field(gt=0)
    spray_rate_liters_per_hectare: float = Field(gt=0)


class CalculatorTool(Tool):
    async def execute(self, input_data: dict) -> ToolResult:
        try:
            parsed = CalculatorInput(**input_data)
        except ValidationError as e:
            return ToolResult(success=False, error_message=str(e))

        total_liters = parsed.size_hectares * parsed.spray_rate_liters_per_hectare
        return ToolResult(success=True, data={"total_liters": total_liters})