import json
import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agentic_ai.memory import load_session_state, save_session_state
from app.agentic_ai.prompts import SHAPE_AGENT_SYSTEM_PROMPT
from app.agentic_ai.schemas import ChatRequest, ChatResponse, ShapeState, ToolCallRecord
from app.agentic_ai.state import ShapeAgentState
from app.agentic_ai.tools import SHAPE_TOOLS, execute_shape_tool

UNRELATED_REQUEST_MESSAGE = (
    "I can only help edit the shape. Ask me to change its shape, color, size, "
    "rotation, border, opacity, or background."
)

SHAPE_REQUEST_TERMS = {
    "shape",
    "circle",
    "square",
    "rectangle",
    "triangle",
    "star",
    "ellipse",
    "pentagon",
    "hexagon",
    "color",
    "colour",
    "fill",
    "size",
    "bigger",
    "larger",
    "smaller",
    "rotate",
    "rotation",
    "border",
    "outline",
    "stroke",
    "opacity",
    "transparent",
    "background",
    "canvas",
    "reset",
    "undo",
    "previous",
}

SHAPE_ACTION_TERMS = {
    "make",
    "turn",
    "change",
    "set",
    "convert",
    "update",
    "modify",
}

SHAPE_REFERENCE_TERMS = {
    "it",
    "its",
    "shape",
    "color",
    "colour",
    "fill",
    "border",
    "background",
    "canvas",
}


@lru_cache
def get_shape_model():
    load_dotenv()
    api_key = os.getenv("GEMINI_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("Missing GEMINI_KEY or GOOGLE_API_KEY in Backend/.env")

    os.environ["GOOGLE_API_KEY"] = api_key

    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=0,
    )
    return model.bind_tools(SHAPE_TOOLS)


async def run_shape_agent(request: ChatRequest) -> ChatResponse:
    state = load_session_state(request.session_id, request.current_shape)
    current_shape = state.get("current_shape", request.current_shape)
    shape_history = state.get("shape_history", [current_shape])

    if not is_shape_related_request(request.message):
        state["messages"] = [
            *state.get("messages", []),
            HumanMessage(content=request.message),
            AIMessage(content=UNRELATED_REQUEST_MESSAGE),
        ]
        state["assistant_message"] = UNRELATED_REQUEST_MESSAGE
        save_session_state(state)

        return ChatResponse(
            session_id=request.session_id,
            assistant_message=UNRELATED_REQUEST_MESSAGE,
            updated_shape=current_shape,
            tool_calls=[],
        )

    state["messages"] = [
        *state.get("messages", []),
        HumanMessage(content=request.message),
    ]
    state["current_shape"] = current_shape
    state["shape_history"] = shape_history

    try:
        ai_message = await get_shape_model().ainvoke(build_model_messages(state))
    except Exception as error:
        assistant_message = f"I could not reach Gemini: {error}"
        return ChatResponse(
            session_id=request.session_id,
            assistant_message=assistant_message,
            updated_shape=current_shape,
            tool_calls=[],
        )

    updated_shape = current_shape
    tool_calls = extract_tool_calls(ai_message)

    for tool_call in tool_calls:
        updated_shape = execute_shape_tool(
            tool_call.name,
            tool_call.arguments,
            updated_shape,
            shape_history,
        )

    if tool_calls:
        shape_history = update_shape_history(shape_history, updated_shape)
        assistant_message = build_tool_response(tool_calls, updated_shape)
    else:
        assistant_message = message_content_to_text(ai_message.content)

    state["messages"] = [
        *state["messages"],
        AIMessage(content=assistant_message),
    ]
    state["current_shape"] = updated_shape
    state["shape_history"] = shape_history
    state["tool_calls"] = tool_calls
    state["assistant_message"] = assistant_message
    save_session_state(state)

    return ChatResponse(
        session_id=request.session_id,
        assistant_message=assistant_message,
        updated_shape=updated_shape,
        tool_calls=tool_calls,
    )


def build_model_messages(state: ShapeAgentState):
    current_shape = state["current_shape"].model_dump()
    shape_history = [shape.model_dump() for shape in state.get("shape_history", [])[-5:]]

    context = {
        "current_shape": current_shape,
        "shape_history": shape_history,
        "instruction": (
            "If the user asks for a visual change, call exactly one of the provided tools. "
            "Return normal text only when you need clarification or the request is not a shape edit."
        ),
    }

    return [
        SystemMessage(
            content=(
                f"{SHAPE_AGENT_SYSTEM_PROMPT}\n\n"
                f"Current backend state:\n{json.dumps(context, indent=2)}"
            )
        ),
        *state.get("messages", [])[-8:],
    ]


def extract_tool_calls(ai_message) -> list[ToolCallRecord]:
    records: list[ToolCallRecord] = []

    for tool_call in getattr(ai_message, "tool_calls", []) or []:
        name = tool_call.get("name")
        arguments = tool_call.get("args") or {}

        if name:
            records.append(ToolCallRecord(name=name, arguments=arguments))

    return records


def update_shape_history(
    shape_history: list[ShapeState],
    updated_shape: ShapeState,
) -> list[ShapeState]:
    if shape_history and shape_history[-1] == updated_shape:
        return shape_history

    return [*shape_history, updated_shape]


def build_tool_response(tool_calls: list[ToolCallRecord], updated_shape: ShapeState) -> str:
    tool_names = ", ".join(tool_call.name for tool_call in tool_calls)
    return (
        f"Done. I used {tool_names} and updated the shape to "
        f"{updated_shape.type} with color {updated_shape.color}."
    )


def message_content_to_text(content) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            else:
                text_parts.append(str(item))
        return " ".join(text_parts).strip()

    return str(content)


def is_shape_related_request(message: str) -> bool:
    lowered = message.lower()
    if any(term in lowered for term in SHAPE_REQUEST_TERMS):
        return True

    has_action = any(term in lowered for term in SHAPE_ACTION_TERMS)
    has_reference = any(term in lowered for term in SHAPE_REFERENCE_TERMS)
    return has_action and has_reference
