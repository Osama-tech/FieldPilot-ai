"""Abstraction for all agent tools. Every tool implements execute()
so the Agent can invoke any tool through the same interface."""

from abc import ABC, abstractmethod

from app.domain.models import ToolResult


class Tool(ABC):
    @abstractmethod
    async def execute(self, input_data: dict) -> ToolResult:
        raise NotImplementedError


    @abstractmethod
    def get_schema(self) -> dict:
        """Return {'name': str, 'description': str, 'parameters': dict}
        describing this tool for LLM function calling."""
        raise NotImplementedError