# OpenAI Function Calling Flow

Use this exact loop for agentic tool use with the Responses API.

1. Send a model request with `tools` included.
2. Read `response.output` and detect `function_call` items.
3. Execute each function call in your app code.
4. Append each tool result as a `function_call_output` message with matching `call_id`.
5. Send another request with the updated conversation.
6. Repeat until the model returns a final text response with no tool calls.

## Practical rules

- Assume there can be zero, one, or many tool calls in a turn.
- Keep tool schemas strict and explicit.
- Keep tool names and descriptions concrete.
- Return tool outputs as strings (or file/image objects when needed).
- Keep the tool list small enough for model accuracy.

## Strict mode checklist

- Set `"strict": true` on each function tool.
- Ensure object schemas use `"additionalProperties": false`.
- Ensure fields are explicit and constrained.
- Prefer nullable required fields over optional hidden defaults when behavior needs consistency.
