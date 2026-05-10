from typing import Literal

from pydantic import BaseModel, Field


ShapeType = Literal[
    "circle",
    "square",
    "rectangle",
    "triangle",
    "star",
    "ellipse",
    "pentagon",
    "hexagon",
]


class ShapeState(BaseModel):
    type: ShapeType = "square"
    color: str = "#2563eb"
    size: int = Field(default=170, ge=40, le=400)
    rotation: float = 0
    borderColor: str = "#111827"
    borderWidth: int = Field(default=0, ge=0, le=40)
    opacity: float = Field(default=1, ge=0, le=1)
    backgroundColor: str = "#f8fafc"


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    current_shape: ShapeState


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict


class ChatResponse(BaseModel):
    session_id: str
    assistant_message: str
    updated_shape: ShapeState
    tool_calls: list[ToolCallRecord] = []
