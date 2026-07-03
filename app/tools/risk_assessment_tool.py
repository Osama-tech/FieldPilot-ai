from typing import Any

from app.domain.models import ToolResult
from app.domain.rule_provider import RuleProvider
from app.tools.base import BaseTool


class RiskAssessmentTool(BaseTool):
    name = "risk_assessment"

    def __init__(self, rule_provider: RuleProvider) -> None:
        self._rule_provider = rule_provider

    def execute(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
