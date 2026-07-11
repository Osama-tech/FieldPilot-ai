"""Abstraction for LLM providers. Concrete implementations (e.g.
GeminiLLMClient) translate provider-specific request/response formats
into the neutral types defined in llm_types.py."""

from abc import ABC, abstractmethod

from app.domain.llm_types import LLMMessage, LLMResponse


class LLMClient(ABC):
    @abstractmethod
    async def send_message(
        self, conversation_history: list[LLMMessage], tools: list[dict]
    ) -> LLMResponse:
        raise NotImplementedError