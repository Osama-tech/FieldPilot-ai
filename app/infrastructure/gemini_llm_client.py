"""Gemini implementation of LLMClient. Owns all translation between our
neutral LLMMessage/LLMResponse contracts and the google-genai SDK's types."""

from google import genai
from google.genai import types

from app.infrastructure.llm_client import LLMClient
from app.infrastructure.llm_types import (
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
                contents.append(
                    types.Content(
                        role="model",
                        parts=[
                            types.Part(
                                function_call=types.FunctionCall(
                                    name=message.tool_call.tool_name,
                                    args=message.tool_call.arguments,
                                )
                            )
                        ],
                    )
                )
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
            call = response.function_calls[0]
            return LLMToolCallResponse(
                tool_call=LLMToolCallRequest(tool_name=call.name, arguments=dict(call.args))
            )

        return LLMFinalTextResponse(text=response.text)