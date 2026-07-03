from typing import Callable

from app.domain.models import ToolResult

ToolFn = Callable[..., ToolResult]

_REGISTRY: dict[str, ToolFn] = {}


def register_tool(name: str, fn: ToolFn) -> None:
    _REGISTRY[name] = fn


def get_tool(name: str) -> ToolFn:
    return _REGISTRY[name]


def list_tools() -> list[str]:
    return list(_REGISTRY.keys())
