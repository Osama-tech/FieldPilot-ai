from abc import ABC, abstractmethod
from typing import Any, Optional


class LLMClient(ABC):
    @abstractmethod
    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]:
        ...


class GeminiLLMClient(LLMClient):
    def __init__(self, api_key: Optional[str]) -> None:
        self._api_key = api_key

    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]:
        raise NotImplementedError
