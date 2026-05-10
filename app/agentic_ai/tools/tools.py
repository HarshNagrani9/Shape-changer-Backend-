from copy import deepcopy
from typing import Any

from langchain_core.tools import tool

from app.agentic_ai.schemas import ShapeState


def apply_shape_patch(current_shape: ShapeState, patch: dict[str, Any]) -> ShapeState:
    data = current_shape.model_dump()
    data.update({key: value for key, value in patch.items() if value is not None})
    return ShapeState(**data)


@tool
def update_shape(
    type: str | None = None,
    color: str | None = None,
    size: int | None = None,
    rotation: float | None = None,
    borderColor: str | None = None,
    borderWidth: int | None = None,
    opacity: float | None = None,
    backgroundColor: str | None = None,
) -> dict[str, Any]:
    """Update one or more properties of the current shape."""
    return {
        "type": type,
        "color": color,
        "size": size,
        "rotation": rotation,
        "borderColor": borderColor,
        "borderWidth": borderWidth,
        "opacity": opacity,
        "backgroundColor": backgroundColor,
    }


@tool
def reset_shape() -> dict[str, Any]:
    """Reset the shape to the default state."""
    return ShapeState().model_dump()


@tool
def get_shape_state(current_shape: dict[str, Any]) -> dict[str, Any]:
    """Return the current shape state."""
    return deepcopy(current_shape)


@tool
def undo_shape_change(shape_history: list[dict[str, Any]]) -> dict[str, Any]:
    """Restore the previous shape state from shape history."""
    if len(shape_history) < 2:
        return ShapeState().model_dump()

    return shape_history[-2]


SHAPE_TOOLS = [
    update_shape,
    reset_shape,
    get_shape_state,
    undo_shape_change,
]


def execute_shape_tool(
    name: str,
    arguments: dict[str, Any],
    current_shape: ShapeState,
    shape_history: list[ShapeState],
) -> ShapeState:
    if name == "update_shape":
        return apply_shape_patch(current_shape, arguments)

    if name == "reset_shape":
        return ShapeState()

    if name == "undo_shape_change":
        if len(shape_history) < 2:
            return ShapeState()
        return shape_history[-2]

    return current_shape
