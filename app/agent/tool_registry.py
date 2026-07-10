"""Maps tool names to Tool instances so the Agent can invoke tools generically."""

from app.tools.base import Tool


class UnknownToolError(Exception):
    """Raised when the Agent requests a tool name that was never registered."""


class DuplicateToolError(Exception):
    """Raised when registering a tool name that is already in use."""


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, name: str, tool: Tool) -> None:
        if name in self._tools:
            raise DuplicateToolError(
                f"A tool is already registered under name '{name}'"
            )
        self._tools[name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise UnknownToolError(f"No tool registered under name '{name}'")
        return self._tools[name]