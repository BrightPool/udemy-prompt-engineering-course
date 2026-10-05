# OpenAI Playground

Four-slide introduction for Part 7: OpenAI Platform & API - Coding.

UI screenshots supplied by James, captured 1 October 2026. Model and tool availability can change.

## Slide 1: OpenAI Playground

A playground lets a developer test an API request through a browser before building the surrounding application. Show the model selector in this screenshot and run the same small task on two models available to the account. Inspect the answers against the same criteria. The reasoning effort and output controls are useful examples of settings to explore; supported settings vary by model. Keep the input fixed while changing one setting so the comparison is easy to explain. The selected model in the screenshot is a dated example, not a recommendation or a guarantee that every account can use it. Playground calls use API billing, separately from a ChatGPT subscription. Screenshot supplied by James, captured 1 October 2026.

- https://platform.openai.com/chat/edit
- https://developers.openai.com/api/docs/guides/prompt-engineering
- https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform

## Slide 2: Prototype a Customer Support Reply

Paste the review into the conversation and use the two-sentence instruction as the prompt guidance. Run it and inspect whether the reply acknowledges the broken handle without promising a refund. Edit the instructions and rerun the same review. Then try a different review, such as a late delivery or a compliment. This is rapid prototyping: we can learn whether a proposed feature produces useful output before writing its interface and integration. The slide contains a teaching prompt, not a recorded model output. Use several examples before treating the prompt as ready for the application. Students can follow this experiment entirely in the browser.

- https://platform.openai.com/chat/edit
- https://developers.openai.com/api/docs/guides/prompt-engineering

## Slide 3: Export the Request as Python

Use the Code button in the top right of the Playground to inspect code for the current prompt and configuration. The supplied View code screenshot shows a Python SDK request to the Responses API, including the model, output settings, reasoning configuration and streaming option. It provides integration code for the configuration; it does not build the rest of the application. This screenshot was taken from an empty draft, so input=[] contains no task and tools=[] enables no tools. Add prompt guidance and a user message before exporting a useful request, or fill those fields deliberately in the Python code. Install the SDK and supply the API key through an environment variable or secret manager. The full screenshot continues into a streaming event loop; our crop focuses on the request settings. Do not assume the pictured model and every setting are supported by all accounts or models. Screenshot supplied by James, captured 1 October 2026.

- https://developers.openai.com/api/docs/quickstart
- https://platform.openai.com/chat/edit

## Slide 4: Hosted Tools and Local Tools

The menus distinguish hosted tools from tools that need execution in your application. OpenAI handles its built-in hosted tools, such as web search, file search and image generation. Code Interpreter executes Python in a sandbox, and hosted shell uses an OpenAI-managed container. Programmatic Tool Calling, shown above the list in the full supplied screenshot, uses a hosted JavaScript runtime to orchestrate tool calls; it is different from Code Interpreter and still needs the appropriate execution mechanism for each called tool. Local functions, custom tools, apply-patch requests and local shell actions are requests for your integration to handle. The model asks for work, your application performs it, and your application returns the results. Local can mean a backend server or another environment you control, rather than the student’s laptop. MCP appears in the hosted menu, but remote MCP tool execution occurs on the connected MCP server. Choosing a local tool does not give the Playground permission to execute arbitrary code on your machine. The screenshot shows both tool menus in full. Screenshot supplied by James, captured 1 October 2026.

- https://developers.openai.com/api/docs/guides/tools
- https://developers.openai.com/api/docs/guides/function-calling
- https://developers.openai.com/api/docs/guides/tools-shell
- https://developers.openai.com/api/docs/guides/tools-code-interpreter
- https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp

## Asset sources

- OpenAI wordmark: https://cdn.openai.com/brand/OpenAI-Logos-2025.zip
- OpenAI brand guidelines: https://openai.com/brand/
- Python logo: https://www.python.org/static/community_logos/python-logo-master-v3-TM.png
- Python logo guidance: https://www.python.org/community/logos/
- Screenshots: the three original files supplied in this conversation, embedded without editing the UI. Native PowerPoint crops focus on the relevant controls.

OpenAI and Python marks belong to their respective owners.
