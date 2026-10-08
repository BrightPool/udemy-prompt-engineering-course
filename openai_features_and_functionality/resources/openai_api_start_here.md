# OpenAI Playground and Responses API: Start Here

Use this guide before the adjacent API coding lessons. You can test a prompt in the browser before writing Python.

## OpenAI Playground

A playground lets you experiment with model inputs and settings, inspect results, and refine a prompt before integrating it into an application.

- [Open OpenAI Playground](https://platform.openai.com/chat/edit)
- [Playground entry point](https://platform.openai.com/playground)
- [OpenAI Playground slides](../../decks/openai-playground/output/OpenAI%20Playground.pptx)
- [Prompting guide](https://developers.openai.com/api/docs/guides/prompt-engineering)

**Exercise:** use the review “The mug looks lovely, but its handle broke on the first day.” Compare “Analyse this review” with “In one sentence, name the main customer issue.” Check whether the answer identifies the broken handle. Keep the model and input fixed while changing the instruction. Then try several other reviews.

API runs incur charges. API billing is separate from a ChatGPT subscription. [Billing explanation](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform).

## Introduction to the Responses API

Responses is the interface we use to send model inputs and receive typed output items. OpenAI recommends it for new projects, while Chat Completions remains supported. A basic Python request uses `client.responses.create(model=MODEL, instructions=..., input=...)`. `response.output_text` collects text in the SDK. Tool calls and other typed items need their own handling.

- [Introduction to the Responses API slides](../../decks/responses-api-intro/output/Introduction%20to%20the%20Responses%20API.pptx)
- [Responses API guide](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [Python quickstart](https://developers.openai.com/api/docs/quickstart)
- [Responses API & Messages notebook](../responses_api_and_messages.ipynb)
- [Conversation-state guide](https://developers.openai.com/api/docs/guides/conversation-state)

Messages are one kind of input/output item. For continued conversations, send relevant history or use `previous_response_id`. Resend instructions you still require when linking turns.

## Decisions API companion lesson

After Structured Outputs, compare generated JSON with a bounded decision. The [Decisions API notebook](../decisions_api.ipynb) introduces Predicate, Choice and Score, checks a ticket against ground truth, and measures the same model on Decisions and Responses. It also explains Jev by TypeSafe and why decision models attracted developer interest.

The three-slide introduction and recording notes are in `/Users/jamesaphoenix/Desktop/course-decks/decisions-api/`. The optional 20-pair benchmark starts disabled. [Decisions Playground](https://platform.openai.com/decisions?lang=python) · [Decisions guide](https://developers.openai.com/api/docs/guides/decisions).

## Suggested order

1. Setting up an OpenAI Account & API Key.
2. **OpenAI Playground**, the browser introduction.
3. **Introduction to the Responses API**, the short conceptual lecture.
4. **Responses API & Messages - Coding**, the conversation-state notebook.
5. [Core Features Walkthrough](../core_features_walkthrough.ipynb) and [Chat Completions vs Responses API](../chat_completions_vs_responses_api.ipynb).

The slides and notebooks are companion resources. Course videos still require recording and upload where indicated in the recording plan.
