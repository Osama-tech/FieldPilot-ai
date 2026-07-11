import pytest
from pydantic import TypeAdapter, ValidationError

from app.domain.llm_types import (
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
        message_adapter.validate_python(
            {"kind": "user", "text": "Is it safe?", "tool_result": {"x": 1}}
        )


def test_message_adapter_parses_correct_kind() -> None:
    parsed = message_adapter.validate_python(
        {
            "kind": "model_tool_call",
            "tool_calls": [
                {
                    "tool_name": "weather",
                    "arguments": {},
                }
            ],
        }
    )

    assert isinstance(parsed, ModelToolCallMessage)
    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0].tool_name == "weather"


def test_response_adapter_rejects_missing_required_field() -> None:
    with pytest.raises(ValidationError):
        response_adapter.validate_python({"kind": "final_text"})


def test_response_adapter_parses_tool_call_response() -> None:
    parsed = response_adapter.validate_python(
        {
            "kind": "tool_call",
            "tool_calls": [
                {
                    "tool_name": "calculator",
                    "arguments": {"size_hectares": 10},
                }
            ],
        }
    )

    assert len(parsed.tool_calls) == 1
    assert parsed.tool_calls[0].tool_name == "calculator"


def test_tool_call_response_requires_at_least_one_tool_call() -> None:
    with pytest.raises(ValidationError):
        response_adapter.validate_python(
            {
                "kind": "tool_call",
                "tool_calls": [],
            }
        )