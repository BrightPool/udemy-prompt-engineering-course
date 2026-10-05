# Introduction to the Responses API

## Slide 1: Introduction to the Responses API

The Responses API is the interface we will use to send inputs to an OpenAI model and work with its output. It extends the older chat-oriented pattern with a common interface for supported modalities, tool calls and conversation state. OpenAI recommends Responses for new projects, while Chat Completions remains supported. We will start with a single text request, then see where messages fit. This gives us the foundation for the next lecture, Responses API and Messages.

- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://developers.openai.com/api/docs/guides/conversation-state

## Slide 2: A Basic Request and Response

The authenticated client sends a request to responses.create. The model selects which AI model handles it. Instructions describe how the model should behave. Input supplies the task or data. The response contains an ID, output items and usage information. In the Python SDK, output_text is a convenience property that collects text output. With tools, the raw output can also contain function calls or other typed items, so do not assume the first item is always a message. Before running this, install the SDK, set an API key and choose an available model.

- https://developers.openai.com/api/docs/quickstart
- https://developers.openai.com/api/docs/guides/migrate-to-responses

## Slide 3: Where Messages Fit

For a single task, input can be a string. For a conversation, input can be a list of messages with roles and content. The example shows the earlier user question, the assistant reply and the follow-up. Messages sit inside the Responses interface alongside other item types such as function calls and tool results. Your application can send the relevant history itself or link a turn using previous_response_id. When linking turns, resend the instructions you still require. The next notebook demonstrates both conversation patterns.

- https://developers.openai.com/api/docs/guides/conversation-state
- https://developers.openai.com/api/docs/guides/migrate-to-responses

