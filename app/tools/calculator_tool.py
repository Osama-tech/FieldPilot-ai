from typing import Any

from app.domain.models import ToolResult
from app.tools.base import BaseTool


class CalculatorTool(BaseTool):
    name = "calculator"

    def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
