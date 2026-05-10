# Backend Flow

This backend is the FastAPI service for the Agentic AI Shape Editor.

The backend receives chat messages from the React frontend, sends them into an agentic AI workflow, executes shape-editing tools when the model requests them, stores memory, and returns the updated shape state back to the frontend.

## Tech Stack

- FastAPI: HTTP API layer.
- Google Gemini: LLM used for reasoning.
- LangChain: model wrapper, message objects, prompts, and structured tools.
- LangGraph: agent workflow, graph state, routing, and memory checkpointing.

## Folder Structure

```text
Backend/
  README.md
  requirements.txt
  app/
    main.py
    api/
      chat.py
    agentic_ai/
      README.md
      state/
        state.py
        README.md
      schemas/
        schemas.py
        README.md
      prompts/
        prompts.py
        README.md
      tools/
        tools.py
        README.md
      memory/
        memory.py
        README.md
      graph/
        graph.py
        README.md
```

## Backend Request Flow

```text
React Frontend
  |
  v
POST /api/chat
  |
  v
FastAPI chat route
  |
  v
LangGraph shape agent
  |
  v
Gemini decides whether to call tools
  |
  v
Shape tools validate and update structured state
  |
  v
LangGraph memory stores messages and shape state
  |
  v
FastAPI returns assistant message + updated shape
```

## API Contract

Endpoint:

```text
POST /api/chat
```

Request:

```json
{
  "session_id": "session_123",
  "message": "Make it a red circle",
  "current_shape": {
    "type": "square",
    "color": "#2563eb",
    "size": 170,
    "rotation": 0,
    "borderColor": "#111827",
    "borderWidth": 0,
    "opacity": 1,
    "backgroundColor": "#f8fafc"
  }
}
```

Response:

```json
{
  "session_id": "session_123",
  "assistant_message": "Done. I changed it to a red circle.",
  "updated_shape": {
    "type": "circle",
    "color": "#ef4444",
    "size": 170,
    "rotation": 0,
    "borderColor": "#111827",
    "borderWidth": 0,
    "opacity": 1,
    "backgroundColor": "#f8fafc"
  },
  "tool_calls": [
    {
      "name": "update_shape",
      "arguments": {
        "type": "circle",
        "color": "#ef4444"
      }
    }
  ]
}
```

## Agentic AI Flow

1. The frontend sends the latest user message and `session_id`.
2. FastAPI validates the request body with Pydantic schemas.
3. The chat route calls the LangGraph agent.
4. LangGraph loads previous memory for the same session.
5. Gemini receives the system prompt, chat history, current shape, and available tools.
6. Gemini either replies directly or calls a shape tool.
7. Tool calls are converted into backend JSON records.
8. The backend executes the selected tool and validates the updated shape state.
9. Updated state is saved into memory.
10. FastAPI returns the assistant response, updated shape, and tool-call JSON.

## Why This Structure Exists

The purpose of this project is to understand how agentic AI works.

Because of that, the backend is intentionally split into small files:

- `state/state.py`: what the graph remembers.
- `schemas/schemas.py`: what the API accepts and returns.
- `prompts/prompts.py`: how the agent is instructed.
- `tools/tools.py`: what actions the LLM can take.
- `memory/memory.py`: how context is stored.
- `graph/graph.py`: how the agent workflow is connected.

Each main agentic AI folder has its own `README.md` explaining what it does.

## Deploy Backend On Render

The backend repo includes:

```text
render.yaml
```

Render uses this file to deploy the FastAPI backend.

### Render Environment Variables

Set these in Render:

```text
GEMINI_KEY=your_real_gemini_key
GEMINI_MODEL=gemini-2.5-flash
FRONTEND_ORIGINS=https://your-vercel-app.vercel.app
```

Use only the frontend origin, not an API path:

```text
https://your-vercel-app.vercel.app
```

The backend route will be:

```text
https://your-render-service.onrender.com/api/chat
```

Use that URL in the frontend environment variable:

```text
VITE_CHAT_API_URL=https://your-render-service.onrender.com/api/chat
```
# Shape-changer-Backend-
# Shape-changer-Backend-
