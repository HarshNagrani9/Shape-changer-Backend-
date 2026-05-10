# `schemas.py`

This file defines the Pydantic models used by the backend.

Pydantic validates incoming API data and ensures the frontend and backend agree on the shape of the data.

## Main Models

### `ShapeState`

Represents the visual shape shown on the frontend.

It stores:

- Shape type
- Fill color
- Size
- Rotation
- Border color
- Border width
- Opacity
- Canvas background color

### `ChatRequest`

The request body sent by the frontend to FastAPI.

It contains:

- `session_id`: memory key for the conversation.
- `message`: latest user message.
- `current_shape`: current frontend shape state.

### `ChatResponse`

The response FastAPI sends back to the frontend.

It contains:

- `assistant_message`: text shown in the chat.
- `updated_shape`: shape state after tool execution.
- `tool_calls`: debug-friendly list of tools used by the agent.

## Why It Matters

Schemas protect the backend from invalid data and make tool execution safer.

For example, `size` cannot be less than 40 or greater than 400, and `opacity` must stay between 0 and 1.
