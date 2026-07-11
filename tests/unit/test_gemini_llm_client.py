import pytest

from app.infrastructure.gemini_llm_client import GeminiLLMClient
from app.infrastructure.llm_types import LLMFinalTextResponse, LLMToolCallResponse, UserMessage


class FakeFunctionCall:
    def __init__(self, name: str, args: dict) -> None:
        self.name = name
        self.args = args


class FakeGenerateContentResponse:
    def __init__(self, text: str = None, function_calls: list = None) -> None:
        self.text = text
        self.function_calls = function_calls or []


class FakeModels:
    def __init__(self, response: FakeGenerateContentResponse) -> None:
        self._response = response

    async def generate_content(self, model: str, contents: list, config) -> FakeGenerateContentResponse:
        return self._response


class FakeAio:
    def __init__(self, response: FakeGenerateContentResponse) -> None:
        self.models = FakeModels(response)


class FakeGenaiClient:
    def __init__(self, response: FakeGenerateContentResponse) -> None:
        self.aio = FakeAio(response)


@pytest.mark.asyncio
async def test_send_message_returns_final_text_response() -> None:
    fake_response = FakeGenerateContentResponse(text="It is safe to spray.")
    fake_client = FakeGenaiClient(fake_response)
    llm_client = GeminiLLMClient(client=fake_client, model="fake-model")

    result = await llm_client.send_message([UserMessage(text="Is it safe?")], tools=[])

    assert isinstance(result, LLMFinalTextResponse)
    assert result.text == "It is safe to spray."


@pytest.mark.asyncio
async def test_send_message_returns_tool_call_response() -> None:
    fake_call = FakeFunctionCall(name="calculator", args={"size_hectares": 10})
    fake_response = FakeGenerateContentResponse(function_calls=[fake_call])
    fake_client = FakeGenaiClient(fake_response)
    llm_client = GeminiLLMClient(client=fake_client, model="fake-model")

    result = await llm_client.send_message([UserMessage(text="How much chemical?")], tools=[])

    assert isinstance(result, LLMToolCallResponse)
    assert result.tool_call.tool_name == "calculator"
    assert result.tool_call.arguments == {"size_hectares": 10}