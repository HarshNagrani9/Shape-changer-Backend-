from fastapi import APIRouter

from app.agentic_ai.graph import run_shape_agent
from app.agentic_ai.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return await run_shape_agent(request)
