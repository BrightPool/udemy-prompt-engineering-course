# Building a Small Agent with OpenRouter

Six slides for Part 10, Model Gateways. The editable deck uses the supplied course theme and contains Python code, speaker notes and official links.

## Recording guide

1. State the task: check stock and the total price of a blue mug delivered to the UK.
2. Show the two read-only Python functions. Sample data gives £12 for the mug, stock of eight and £3 delivery, producing a £15 total.
3. Explain the loop: send tool definitions, validate and execute requested functions, return results using the original tool call IDs, then continue.
4. Show the gateway client and tool-capable model selection. OpenRouter routes requests; our application runs the agent loop.
5. Run the focused notebook, inspect both tool results, then read the final answer to check all quoted figures.
6. Show the returned account charge for every model turn, then its generation metadata and the idempotent example credit ledger. Change the model and compare the same task.

Use roughly three minutes of slides, followed by a short notebook walkthrough. Keep the demo simple so learners can see the full loop.

## Companion notebooks

- `model_gateways/building_a_small_agent_with_openrouter.ipynb`: the focused, self-contained Python lesson.
- `model_gateways/openrouter_features_and_agent.ipynb`: the full feature tour, also containing the agent example. The link embedded in the deck opens this larger notebook.

Both use a Python kernel. The tools operate on sample data and do not place an order or use a browser. The loop allows at most four model turns and four tool calls in a turn. Source notebooks contain no saved execution output or API keys.

The ledger is a teaching example. A production credit system also needs persisted atomic transactions, reservations, reconciliation and an explicit policy for extra tools or BYOK charges. Unknown generation cost stays pending.

## Links and publication

Colab links will work after the new notebooks are committed and pushed to the repository's `main` branch. The files are currently local additions.

Native Google Slides publication is pending installation and connection of the Google Drive plugin. This package contains the prepared local deck and previews. Google Slides conversion has not been performed or checked.

## Sources

- https://openrouter.ai/docs/quickstart
- https://openrouter.ai/docs/guides/features/tool-calling
- https://openrouter.ai/models
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation
