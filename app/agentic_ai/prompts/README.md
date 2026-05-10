# `prompts.py`

This file contains the system prompt for the shape editing agent.

The system prompt tells Gemini what role it is playing and how it should behave.

## What The Prompt Teaches The LLM

- It is editing a visual shape.
- It should use tools for visual changes.
- It should use memory for follow-up requests.
- It should ask a clarifying question when needed.
- It should keep replies short and practical.

## Why It Matters

The prompt is part of the agent brain.

Tools define what the agent can do, but the prompt teaches the model when and why to use those tools.
