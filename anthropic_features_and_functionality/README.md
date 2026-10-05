# Anthropic / Claude API Section

Three Python notebooks support a compact four-lecture section alongside the OpenAI API lessons. They reuse familiar tasks so students can see which ideas transfer and which API details change.

| Lecture | Notebook | Main demonstration |
| --- | --- | --- |
| Anthropic API Basics and Claude Features | [Features and Functionality](anthropic_features_and_functionality.ipynb) | Native Messages, multi-turn content, streaming, structured JSON and usage |
| Claude Prompting and Tool Use | [Prompting and Python Tools](claude_prompting_and_tools.ipynb) | Clear prompts, native tool schemas, two read-only Python functions and a bounded agent loop |
| Claude Computer Use via the API | [Computer Use](claude_computer_use.ipynb) | Current computer toolset, ordered actions, matching results and an optional isolated form demo |
| Choosing Models and Providers: Staying Tool Agnostic | Features notebook, optional OpenAI comparison | Same task and schema across providers, correctness checks, latency and provider-specific usage |

[Slides](../decks/claude-api-section/output/Anthropic%20%2B%20Claude%20API.pptx) · [Speaker notes](../decks/claude-api-section/NOTES.md) · [Recording plan](../docs/api_section_recording_plan.md)

## Google Colab

- [Features notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/anthropic_features_and_functionality/anthropic_features_and_functionality.ipynb)
- [Prompting and tools notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/anthropic_features_and_functionality/claude_prompting_and_tools.ipynb)
- [Computer-use notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/anthropic_features_and_functionality/claude_computer_use.ipynb)

These Colab links become available after the files are published to the repository's main branch. Until then, open the local notebooks or upload them to Colab.

## Running the lessons

Use Jupyter or Colab, then run cells in order. The notebooks install their Python packages with `%pip`. Provide `ANTHROPIC_API_KEY` through an environment variable or the hidden `getpass` prompt. API calls incur charges. The OpenAI comparison also requires a separate `OPENAI_API_KEY`.

The default features model is Haiku 4.5 for a small introductory demonstration. Inspect the live model list and each feature guide before changing the model. Optional features are off by default. The live computer-use exercise is also off by default and targets the current toolset on Sonnet 5.5. Its offline cells need no API key or running browser.

## Similarities and differences

Both providers support instructions, conversations, streaming, structured output and tools. OpenAI Responses uses `instructions`, `input` and typed output items. Claude Messages uses initial `system` guidance, `messages` and typed content blocks. Claude tool results return in a user message; OpenAI Responses has a separate function-call-output item. Preserve the native conversation format inside each provider adapter.

Developers must stay tool agnostic. Reuse the application task, Python business functions and acceptance criteria, then choose the provider, model, tools and context strategy using evidence from that task. A compatibility endpoint or gateway does not guarantee identical features. Verify the required model and tool support before switching.

## References

- [Claude Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Tool calls and results](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
- [Computer use and compatibility](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
