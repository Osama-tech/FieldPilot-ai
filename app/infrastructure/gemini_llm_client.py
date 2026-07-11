"""Gemini implementation of LLMClient. Owns all translation between our
neutral LLMMessage/LLMResponse contracts and the google-genai SDK's types."""

from google import genai
from google.genai import types

from app.domain.llm_client import LLMClient
from app.domain.llm_types import (
    LLMFinalTextResponse,
    LLMMessage,
    LLMResponse,
    LLMToolCallRequest,
    LLMToolCallResponse,
    ModelTextMessage,
    ModelToolCallMessage,
    ToolResultMessage,
    UserMessage,
)


class GeminiResponseError(Exception):
    """Raised when Gemini returns a response with neither a tool call nor text content."""


class GeminiLLMClient(LLMClient):
    def __init__(self, client: genai.Client, model: str) -> None:
        self._client = client
        self._model = model

    def _translate_tools(self, tools: list[dict]) -> list[types.Tool]:
        declarations = [
            types.FunctionDeclaration(
                name=tool["name"],
                description=tool["description"],
                parameters_json_schema=tool["parameters"],
            )
            for tool in tools
        ]
        return [types.Tool(function_declarations=declarations)]

    def _translate_history(self, conversation_history: list[LLMMessage]) -> list[types.Content]:
        contents = []
        for message in conversation_history:
            if isinstance(message, UserMessage):
                contents.append(
                    types.Content(role="user", parts=[types.Part(text=message.text)])
                )
            elif isinstance(message, ModelTextMessage):
                contents.append(
                    types.Content(role="model", parts=[types.Part(text=message.text)])
                )
            elif isinstance(message, ModelToolCallMessage):
                parts = [
                    types.Part(
                        function_call=types.FunctionCall(
                            name=call.tool_name, args=call.arguments
                        )
                    )
                    for call in message.tool_calls
                ]
                contents.append(types.Content(role="model", parts=parts))
            elif isinstance(message, ToolResultMessage):
                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=message.tool_name, response=message.tool_result
                            )
                        ],
                    )
                )
        return contents

    async def send_message(
        self, conversation_history: list[LLMMessage], tools: list[dict]
    ) -> LLMResponse:
        contents = self._translate_history(conversation_history)
        gemini_tools = self._translate_tools(tools)

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=gemini_tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )

        if response.function_calls:
            tool_calls = [
                LLMToolCallRequest(tool_name=call.name, arguments=dict(call.args))
                for call in response.function_calls
            ]
            return LLMToolCallResponse(tool_calls=tool_calls)

        if response.text:
            return LLMFinalTextResponse(text=response.text)

        raise GeminiResponseError(
            "Gemini returned neither a tool call nor text content."
        )