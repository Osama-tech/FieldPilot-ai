import pytest

from app.agent.tool_registry import ToolRegistry, UnknownToolError, DuplicateToolError
from app.domain.models import ToolResult
from app.tools.base import Tool


class DummyTool(Tool):
    async def execute(self, input_data: dict) -> ToolResult:
        return ToolResult(success=True, data={"called": True})


def test_get_returns_registered_tool() -> None:
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register("dummy", tool)

    assert registry.get("dummy") is tool


def test_get_raises_for_unknown_tool_name() -> None:
    registry = ToolRegistry()

    with pytest.raises(UnknownToolError):
        registry.get("nonexistent")


def test_register_raises_for_duplicate_tool_name() -> None:
    registry = ToolRegistry()

    registry.register("dummy", DummyTool())

    with pytest.raises(DuplicateToolError):
        registry.register("dummy", DummyTool())