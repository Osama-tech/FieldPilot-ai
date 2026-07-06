"""Abstraction for all agent tools. Every tool implements execute()
so the Agent can invoke any tool through the same interface."""

from abc import ABC, abstractmethod

from app.domain.models import ToolResult


class Tool(ABC):
    @abstractmethod
    async def execute(self, input_data: dict) -> ToolResult:
        raise NotImplementedError