from abc import ABC, abstractmethod
from typing import Any

from app.domain.models import ToolResult


class BaseTool(ABC):
    name: str

    @abstractmethod
    def execute(self, **kwargs: Any) -> ToolResult:
        ...
