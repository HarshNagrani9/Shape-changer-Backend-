from langgraph.checkpoint.memory import MemorySaver

from app.agentic_ai.schemas import ShapeState
from app.agentic_ai.state import ShapeAgentState


checkpointer = MemorySaver()

_session_store: dict[str, ShapeAgentState] = {}


def load_session_state(session_id: str, current_shape: ShapeState) -> ShapeAgentState:
    if session_id not in _session_store:
        _session_store[session_id] = {
            "session_id": session_id,
            "messages": [],
            "current_shape": current_shape,
            "shape_history": [current_shape],
            "tool_calls": [],
            "assistant_message": "",
            "metadata": {},
        }

    return _session_store[session_id]


def save_session_state(state: ShapeAgentState) -> ShapeAgentState:
    _session_store[state["session_id"]] = state
    return state
