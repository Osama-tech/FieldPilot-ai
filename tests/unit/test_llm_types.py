import pytest
from pydantic import TypeAdapter, ValidationError

from app.infrastructure.llm_types import (
    LLMMessage,
    LLMResponse,
    LLMToolCallRequest,
    ModelToolCallMessage,
    UserMessage,
)

message_adapter = TypeAdapter(LLMMessage)
response_adapter = TypeAdapter(LLMResponse)


def test_user_message_requires_text() -> None:
    with pytest.raises(ValidationError):
        UserMessage()


def test_message_adapter_rejects_mismatched_fields() -> None:
    with pytest.raises(ValidationError):
        message_adapter.validate_python({"kind": "user", "tool_result": {"x": 1}})


def test_message_adapter_parses_correct_kind() -> None:
    parsed = message_adapter.validate_python(
        {"kind": "model_tool_call", "tool_call": {"tool_name": "weather", "arguments": {}}}
    )

    assert isinstance(parsed, ModelToolCallMessage)
    assert parsed.tool_call.tool_name == "weather"


def test_response_adapter_rejects_missing_required_field() -> None:
    with pytest.raises(ValidationError):
        response_adapter.validate_python({"kind": "final_text"})


def test_response_adapter_parses_tool_call_response() -> None:
    parsed = response_adapter.validate_python(
        {
            "kind": "tool_call",
            "tool_call": {"tool_name": "calculator", "arguments": {"size_hectares": 10}},
        }
    )

    assert parsed.tool_call.tool_name == "calculator"