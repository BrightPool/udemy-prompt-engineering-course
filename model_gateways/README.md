# Model Gateways

Python notebooks for Part 10, Model Gateways.

- [OpenRouter features and agent](openrouter_features_and_agent.ipynb): the complete walkthrough, including model discovery, comparison, streaming, structured JSON, provider routing, fallbacks, tools and customer credit accounting. Optional sections cover reasoning, async requests, embeddings, caching, web tools, multimodal inputs, media generation, Responses, batch jobs and LangChain.
- [Building a small agent with OpenRouter](building_a_small_agent_with_openrouter.ipynb): a shorter, self-contained lesson with two read-only Python tools, a bounded agent loop, tool evidence and actual cost reconciliation.

Run the setup cells, enter an OpenRouter key with the private prompt, and continue in order. The core walkthrough makes paid requests. Optional features are off by default. Media and hosted tools have separate pricing; inspect current model and endpoint information before enabling them.

Both notebooks use Python kernels. The feature tour includes a clearly labelled TypeScript reference for the Vercel AI SDK, which is a JavaScript/TypeScript toolkit.

## Teaching order

For the gateway lesson, show the client configuration, live catalogue, two-model comparison and routing example. Introduce actual usage reporting and explain that your application owns customer credit conversion and accounting.

For the agent lesson, use the focused notebook. Explain the task, schemas and two sample functions, then run the loop. Inspect the tool trace, confirm the £15 total and show the cost of every model turn.

The longer feature tour is a reference and a set of optional demos. It is not intended to be narrated in full in a single short lecture.

## Google Colab

The Colab links in the decks point to these files on the repository's `main` branch. They become available after the new notebooks are committed and pushed. The files are currently local additions; publication was not requested.
