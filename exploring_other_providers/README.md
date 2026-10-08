# Exploring Other Providers

Notebooks for the Exploring Other Providers section: model gateways (OpenRouter), the Anthropic Claude API and native Gemini video analysis.

## Model gateways

- [OpenRouter setup, costs and a simple agent](openrouter_features_and_agent.ipynb): three short demonstrations covering API-key setup and the OpenAI SDK base URL, a native OpenRouter SDK request with its returned cost, and a Python agent SDK example that calls an addition tool. A small optional section adds image generation, video generation and embeddings through the same gateway.
- [A/B test the model, keep the prompt](openrouter_model_ab_testing.ipynb): a follow-on using the native OpenRouter Python and agent SDKs with LangChain's AgentEvals. Compare GPT-6.1 Sol and Gemini 3.8 Flash on one conversation, then optionally run the same 50 fictional threads per model asynchronously. Ground truth checks completed tool-call count, expected tools and arguments, and summary coverage. Includes Wilson confidence intervals, sample-size planning and an exact paired comparison. The 100-run batch starts disabled.

Run the cells in order in Jupyter or Colab with Python 3.10 or later. Enter an OpenRouter key with the hidden prompt. The examples make paid requests and install compatible client and agent SDK versions. Text and agent examples use `openai/gpt-6.1-sol`; the optional examples use specialist models and are disabled by default.

Show the base URL change, inspect the native SDK response and request cost, then run the agent and point out the printed tool call followed by the final answer.

For the A/B testing follow-on, introduce ground truth and the three pass rules, show the recorded tool calls and summaries, then compare the eval table. Highlight that only `model` changes in `call_model`. Scale from one thread to the same 50 threads per model, then explain confidence intervals and the paired comparison. The gateway makes model selection another optimisation lever alongside changing prompts. The two-slide introduction and recording notes are in `/Users/jamesaphoenix/Desktop/course-decks/openrouter-model-testing/`.

## Gemini video analysis

- [Using Gemini for Video Analysis](gemini_video_analysis.ipynb): Google's native `google-genai` SDK and Interactions API, upload polling, timestamped Q&A, conversation history, Pydantic structured timelines and answers, explicit unknown handling and token usage. An optional dense-sampling example starts disabled.

Run in Jupyter or Colab with Python 3.10+. Enter a Gemini API key at the hidden prompt. The default downloads Google's public pottery clip, about 12 seconds and 70 MB, or set `VIDEO_PATH` to your own MP4. The main lesson makes four generation requests. It deletes the lesson's uploaded file and stored interactions at the end.

Start with the dated provider and pricing comparison, then follow the deck's upload, wait, ask sequence. Show that an uploaded URI saves transfer while conversation history and caching have separate roles. Inspect the timeline and the answer that acknowledges missing evidence. The companion deck is in `/Users/jamesaphoenix/Desktop/course-decks/gemini-video-analysis/`.

## Anthropic / Claude API

Four Python notebooks support a compact Claude section alongside the OpenAI API lessons. They reuse familiar tasks so students can see which ideas transfer and which API details change.

| Lecture | Notebook | Main demonstration |
| --- | --- | --- |
| Anthropic Console + Messages/Agents | [OpenAI vs Anthropic vs Gemini](openai_vs_anthropic_vs_gemini.ipynb) | The OpenAI concepts mapped across all three providers, then the real differences: prompt caching control and model strengths |
| Anthropic API Basics and Claude Features | [Features and Functionality](anthropic_features_and_functionality.ipynb) | Native Messages, multi-turn content, streaming, structured JSON and usage |
| Claude Prompting and Tool Use | [Prompting and Python Tools](claude_prompting_and_tools.ipynb) | Clear prompts, native tool schemas, two read-only Python functions and a bounded agent loop |
| Claude Computer Use via the API | [Computer Use](claude_computer_use.ipynb) | Current computer toolset, ordered actions, matching results and an optional isolated form demo |
| Choosing Models and Providers: Staying Tool Agnostic | Features notebook, optional OpenAI comparison | Same task and schema across providers, correctness checks, latency and provider-specific usage |

### Google Colab

- [OpenAI vs Anthropic vs Gemini notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/exploring_other_providers/openai_vs_anthropic_vs_gemini.ipynb)
- [Features notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/exploring_other_providers/anthropic_features_and_functionality.ipynb)
- [Prompting and tools notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/exploring_other_providers/claude_prompting_and_tools.ipynb)
- [Computer-use notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/exploring_other_providers/claude_computer_use.ipynb)
- [OpenRouter setup, costs and agent notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/exploring_other_providers/openrouter_features_and_agent.ipynb)
- [OpenRouter model A/B testing notebook](https://colab.research.google.com/github/BrightPool/udemy-prompt-engineering-course/blob/main/exploring_other_providers/openrouter_model_ab_testing.ipynb)

### Running the lessons

Use Jupyter or Colab, then run cells in order. The notebooks install their Python packages with `%pip`. Provide `ANTHROPIC_API_KEY` through an environment variable or the hidden `getpass` prompt. API calls incur charges. The OpenAI comparison also requires a separate `OPENAI_API_KEY`.

The default features model is Haiku 5.5 for a small introductory demonstration. Inspect the live model list and each feature guide before changing the model. Optional features are off by default. The live computer-use exercise is also off by default and targets the current toolset on Haiku 5.5. Its offline cells need no API key or running browser.

### Similarities and differences

Both providers support instructions, conversations, streaming, structured output and tools. OpenAI Responses uses `instructions`, `input` and typed output items. Claude Messages uses initial `system` guidance, `messages` and typed content blocks. Claude tool results return in a user message; OpenAI Responses has a separate function-call-output item. Preserve the native conversation format inside each provider adapter.

Developers must stay tool agnostic. Reuse the application task, Python business functions and acceptance criteria, then choose the provider, model, tools and context strategy using evidence from that task. A compatibility endpoint or gateway does not guarantee identical features. Verify the required model and tool support before switching.

### References

- [Claude Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Tool calls and results](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
- [Computer use and compatibility](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
