# `state.py`

This file defines the shared state that moves through the LangGraph workflow.

In LangGraph, every node receives a state object and returns updates to that state. This makes the agent easier to reason about because every important piece of context is visible in one structure.

## What The State Stores

- `session_id`: identifies the current chat session.
- `messages`: conversation messages used by LangChain and Gemini.
- `current_shape`: the latest shape shown on the frontend.
- `shape_history`: previous shape states, used for undo and memory.
- `tool_calls`: tool calls produced during the current request.
- `assistant_message`: final message returned to the user.
- `metadata`: optional debugging or tracing information.

## Why It Matters

Without shared state, the LLM would only respond to the latest prompt.

With state, the agent can understand requests like:

- "Make it bigger."
- "Undo that."
- "Use the same color as before."
- "Rotate it a little more."
