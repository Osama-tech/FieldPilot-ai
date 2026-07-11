"""Provider-neutral message and response contracts for LLMClient.
Concrete clients (e.g. GeminiLLMClient) translate their provider's native
types into these shapes and back, so the Agent layer never depends on
any specific LLM provider's SDK."""

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


class LLMToolCallRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_name: str
    arguments: dict


class UserMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["user"] = "user"
    text: str


class ModelTextMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["model_text"] = "model_text"
    text: str


class ModelToolCallMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["model_tool_call"] = "model_tool_call"
    tool_calls: list[LLMToolCallRequest] = Field(min_length=1)


class ToolResultMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["tool_result"] = "tool_result"
    tool_name: str
    tool_result: dict


LLMMessage = Annotated[
    Union[UserMessage, ModelTextMessage, ModelToolCallMessage, ToolResultMessage],
    Field(discriminator="kind"),
]


class LLMFinalTextResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["final_text"] = "final_text"
    text: str


class LLMToolCallResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["tool_call"] = "tool_call"
    tool_calls: list[LLMToolCallRequest] = Field(min_length=1)


LLMResponse = Annotated[
    Union[LLMFinalTextResponse, LLMToolCallResponse],
    Field(discriminator="kind"),
]