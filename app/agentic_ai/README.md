# Agentic AI Folder

This folder contains every backend file related to agentic AI behavior.

The goal is to keep the agent easy to understand:

- The API layer receives the request.
- The agent folder decides how reasoning, tools, memory, and graph execution work.
- Each Python file has a matching markdown file explaining its role.

## Files

- `state/state.py`: shared LangGraph state.
- `schemas/schemas.py`: request and response models.
- `prompts/prompts.py`: system prompt for the shape editing agent.
- `tools/tools.py`: functions the LLM can call.
- `memory/memory.py`: session memory and checkpointing.
- `graph/graph.py`: LangGraph workflow.

Each main folder contains:

- A Python file with implementation.
- A `README.md` file explaining what that implementation does.

## Learning Goal

This project is not just about building a shape editor.

It is meant to show how agentic AI works:

1. The user speaks naturally.
2. The LLM reasons about intent.
3. The LLM chooses a tool.
4. The backend executes the tool.
5. The result changes app state.
6. Memory allows the next message to depend on previous messages.
