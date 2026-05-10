from typing import Any, TypedDict

from langchain_core.messages import BaseMessage

from app.agentic_ai.schemas import ShapeState, ToolCallRecord


class ShapeAgentState(TypedDict, total=False):
    session_id: str
    messages: list[BaseMessage]
    current_shape: ShapeState
    shape_history: list[ShapeState]
    tool_calls: list[ToolCallRecord]
    assistant_message: str
    metadata: dict[str, Any]
