import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router

DEFAULT_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def get_cors_origins() -> list[str]:
    origins = os.getenv("FRONTEND_ORIGINS", "")
    configured_origins = [origin.strip() for origin in origins.split(",") if origin.strip()]
    return configured_origins or DEFAULT_CORS_ORIGINS


app = FastAPI(
    title="Agentic AI Shape Editor Backend",
    description="FastAPI backend for learning Gemini tool calling with LangChain and LangGraph.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Agentic AI Shape Editor Backend",
        "status": "running",
    }
