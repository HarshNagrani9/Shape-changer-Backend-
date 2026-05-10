# `graph/graph.py`

This file is responsible for the agent workflow.

This file now contains the Gemini-backed agent orchestration.

It connects:

- Request state from FastAPI
- Memory loading
- The system prompt
- Gemini through LangChain
- Tool calling
- Tool execution
- Shape validation through Pydantic
- Memory saving
- Final response generation

## Current Flow

```text
run_shape_agent(request)
  |
  v
load_session_state(...)
  |
  v
build_model_messages(...)
  |
  v
Gemini + LangChain tool binding
  |
  v
extract_tool_calls(...)
  |
  v
execute_shape_tool(...)
  |
  v
save_session_state(...)
  |
  v
return ChatResponse(...)
```

## Why This File Matters

This file is where the agent becomes more than a normal API.

A normal API directly executes known code.

An agentic API lets the LLM reason, choose tools, and move through a controlled workflow.

## Environment Variable

Gemini is loaded using:

```text
GEMINI_KEY
```

If `GEMINI_KEY` is not found, the code also checks:

```text
GOOGLE_API_KEY
```
