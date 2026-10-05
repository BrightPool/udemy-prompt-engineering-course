# Anthropic and Claude API

## Slide 1: Anthropic + Claude
The API in Python

We already know the broad pattern: provide instructions and inputs, choose a model, then inspect the output. In this compact section we will apply that knowledge to Anthropic and Claude. We will use the native Python API, build a small agent with tools, explain computer use and compare providers using our own task. The three companion notebooks cover the walkthrough, prompting and tools, and an optional computer-use exercise.

- https://platform.claude.com/
- https://platform.claude.com/docs/en/build-with-claude/working-with-messages

## Slide 2: Anthropic API Basics

Install the anthropic Python SDK and supply an Anthropic API key through the environment or a hidden notebook prompt. MODEL is an available model ID discovered during setup. Claude Messages requires max_tokens. Initial guidance goes in system and the user task goes in messages. The response contains typed content blocks. Our helper selects text blocks and checks that the turn ended normally. The core notebook starts with a small Haiku example to keep this introductory demonstration short and inexpensive. API usage has its own billing.

- https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- https://platform.claude.com/
- https://platform.claude.com/docs/en/about-claude/pricing

## Slide 3: OpenAI Responses and Claude Messages

The familiar concepts carry across providers, but the native request bodies differ. These rows compare the introductory OpenAI Responses and Claude Messages patterns. OpenAI input can hold conversation messages and other items. Claude returns content blocks, which may include text, tool use or other block types. Claude Messages expects prior content for a continued conversation, whereas Responses also offers response-ID linking. Newer Claude models can support system messages later in a conversation with additional rules. Managed Agents products are separate interfaces. Keep the provider-specific details inside an adapter when your application supports both.

- https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://developers.openai.com/api/docs/guides/conversation-state

## Slide 4: Prompting Claude

The five principles we learned earlier still apply. Claude prompting guidance emphasises clear instructions and useful examples. XML tags can make sections such as reviews or documents easy to distinguish from instructions. They are an organisational technique, not a guarantee of better results or protection against untrusted content. In our notebook, we ask for a short reason rather than an unrestricted explanation. Carry the intent of a good OpenAI prompt across, then test its wording with the selected Claude model. Supported controls can differ across models, so the examples omit sampling settings that some newer models reject.

- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview

## Slide 5: Familiar Features, Native Configuration

Both providers support several familiar capabilities, but configuration differs. Claude provides streaming helpers and structured outputs using output_config.format. Its supported image and PDF inputs use typed content blocks. The walkthrough also includes token counting and an optional cache example. Cache hits reuse an eligible input prefix, rather than the final answer. Feature availability and minimum cache lengths vary by model. The compact recording should show streaming and structured JSON, with the other demonstrations available as optional follow-along material.

- https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- https://platform.claude.com/docs/en/build-with-claude/streaming
- https://platform.claude.com/docs/en/build-with-claude/vision
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching

## Slide 6: Client Tools: The Model Requests, Python Runs

Client tools follow the same general loop as OpenAI function calling: describe a function, let the model request it, execute it in your application and return the result. Claude uses tool_use blocks and tool_result blocks. Preserve the complete assistant response, then put all matching tool results first in the next user message. OpenAI Responses uses different function-call and function-call-output item shapes. The model does not execute our Python functions. The application owns validation, execution and the turn limit.

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- https://developers.openai.com/api/docs/guides/migrate-to-responses

## Slide 7: A Small Claude Agent with Two Tools

Our small customer-support task is identical to the earlier gateway example so we can compare behaviour. Two read-only Python functions supply the product and delivery facts. The notebook defines native Claude tool schemas, validates arguments and runs a bounded loop. Its checks confirm that both expected tools ran and returned the sample data. Then read the final answer to check that it includes the correct stock and the fifteen-pound total. We record usage for every model turn, including tool requests. No order is placed.

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls

## Slide 8: Client Tools and Hosted Tools

Execution ownership matters when comparing providers. A custom client function runs in our application. Computer-use actions also run in an environment we control. Supported Claude server tools, such as web search and hosted code execution, run on Anthropic infrastructure. OpenAI also provides hosted tools, but their names, request formats and environments differ. The features notebook includes optional search and code-execution examples with separate model settings. A tool appearing in both providers does not make the configurations interchangeable.

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- https://developers.openai.com/api/docs/guides/tools-code-interpreter

## Slide 9: Claude Computer Use via the API

Computer use remains available through Claude’s API. The current computer_toolset_20260801 exposes member tools such as screenshot, left_click and type. Claude returns tool_use blocks with toolset_name set to computer. Your application executes every call in order and returns matching tool_result blocks with that same toolset name. The current toolset requires no beta header on supported models. Older models may require older tool versions. Check the compatibility table before choosing a model. The companion notebook uses the current toolset and disables members its teaching adapter does not implement.

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool

## Slide 10: An Isolated Computer-Use Exercise

The optional exercise uses a small local form and synthetic details. It launches a fresh headless browser context, blocks external page traffic and exposes a limited set of screenshot, mouse and keyboard operations. The task is to fill the fields and click Preview. The application checks the final field values rather than trusting the model’s claim that it finished. RUN_DEMO is false by default. Students can first inspect a simulated tool batch and offline validation checks. Enabling the live demo requires an available compatible model, API billing and the browser dependency installation.

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool

## Slide 11: A Fair Model and Provider Comparison

Use the same task and acceptance criteria when comparing models. Our walkthrough includes a small optional classification evaluation using both native APIs and the same result schema. It records task correctness, latency and usage, without claiming that three examples establish a universal winner. For an agent, evaluate the tool trace and total task cost across all turns. Check required context, modalities and tools before selecting a model. Tokenizers differ, so equal token counts do not imply equal work or dollar cost. Avoid fixed benchmark, context-length or pricing claims in this evergreen introduction. Use the live provider guides for current limits.

- https://platform.claude.com/docs/en/about-claude/models/overview
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/build-with-claude/token-counting
- https://developers.openai.com/api/docs/guides/migrate-to-responses

## Slide 12: Developers Must Stay Tool Agnostic

Developers must be tool agnostic and willing to change their choice when evidence shows that another model, tool or context strategy performs better for the task. Tool agnostic means keeping those choices open and testable. It does not mean every API feature is interchangeable. Put provider-specific SDK calls and schemas inside adapters, keep your business logic and acceptance tests separate, and check capabilities before switching. A gateway or framework can help, but still evaluate its feature support. Choose using your task’s quality requirements, tools, latency and cost.

- https://platform.claude.com/docs/en/about-claude/models/overview
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://openrouter.ai/docs/quickstart

