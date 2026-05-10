# `memory.py`

This file defines how the LangGraph agent stores context.

For the first version, the backend uses LangGraph's in-memory checkpointer:

```python
MemorySaver()
```

It also keeps a simple in-process session store for the current teaching version:

```python
load_session_state(session_id, current_shape)
save_session_state(state)
```

## What Memory Enables

Memory lets the agent understand follow-up messages:

- "Make it bigger."
- "Undo that."
- "Change it back."
- "Now make it green."

The user does not need to repeat the full shape description every time.

## MVP Memory

The MVP uses short-term memory.

This means memory works while the backend process is running, but it disappears when the server restarts.

## Production Memory

Later, this can be replaced with persistent storage:

- PostgreSQL
- Redis
- SQLite
- MongoDB
- Supabase

Persistent memory lets users refresh the page or return later and continue the same conversation.
