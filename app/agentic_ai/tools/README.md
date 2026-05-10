# `tools.py`

This file defines the tools the LLM can call.

Tools are what turn the LLM from a text generator into an agent.

## Available Tools

### `update_shape`

Updates one or more visual properties of the shape.

Example:

```json
{
  "type": "circle",
  "color": "#ef4444"
}
```

### `reset_shape`

Returns the shape to the default state.

### `get_shape_state`

Lets the agent inspect the current shape state.

This is useful for relative requests like:

- "Make it bigger."
- "Rotate it more."
- "Use the current color but make the shape a circle."

### `undo_shape_change`

Restores the previous shape from shape history.

## Why Tools Matter

The LLM does not directly mutate the frontend.

Instead:

1. The LLM chooses a tool.
2. The backend validates the tool arguments.
3. The backend updates structured state.
4. The frontend re-renders from that state.

This is the core pattern behind agentic AI applications.
