# OpenAI Features: API Tools Extension

Updated 1 October 2026 from `/Users/jamesaphoenix/Downloads/OpenAI Features (1).pptx`.

The deck contains 19 slides. The Managed Agents slide stays at slide 12. Four focused topic slides occupy 13-16, replacing the duplicate Advanced placeholder and adding three net slides. Existing material continues at 17-19.

The added slides follow the supplied Modern Writer template, with Oswald headings, Source Code Pro body text, pink emphasis, and clickable official-documentation links. Source references and teaching notes are embedded in the presentation.

## Companion notebooks

- `openai_features_and_functionality/code_interpreter.ipynb`: CSV analysis, a chart, file downloads and checked totals.
- `openai_features_and_functionality/computer_use.ipynb`: a controlled local form, screenshot/action loop and browser-state verification.
- `openai_features_and_functionality/managed_agents_api.ipynb`: saved agent, hosted session, streamed progress, follow-up and published artifacts.

Each notebook has a four-minute filming path, a synthetic example, an exercise, setup, resource cleanup and a summary. Their Colab links will become available after the notebooks are pushed to the repository's main branch.

## Validation

- PowerPoint package, 19-slide count, fonts, geometry and heading fit passed. All slides rendered; the four new slides were inspected individually.
- Code Interpreter passed Papermill execution with the live API, downloaded the CSV and PNG, verified North=420, South=360 and total=780, and deleted remote demo resources.
- Managed Agents passed Papermill execution with the live API, completed an initial turn and follow-up in the same session, downloaded the latest available file versions, checked the same totals, and deleted its session and saved agent.
- Computer Use passed Papermill with RUN_DEMO=False and fixture checks for call IDs, ordered actions, screenshot-only calls, safety stops, unsupported actions, navigation boundaries, cleanup and turn limits. No complete live UI run is claimed. An initial validation flag was accidentally passed as text, opening a local demo browser; that run was stopped before model-requested action execution, and strict boolean checks now reject that configuration.
- All three notebooks validate, compile, contain no execution outputs, and use the required getpass key setup and active upgrade installation cells.
- Tested SDK: openai 3.22.1. API/model access still depends on the learner's own project.

## Slide 13: Computer Use, Now Through the API

Connect this to the Computer Use lesson earlier in the course. The API gives our application the same ability to work through a visual interface. A useful example is testing a signup page: the agent looks at the screen, decides what to do, and checks the result after acting. With the Responses API, you provide and operate the environment; enabling a tool does not create a hosted desktop. The current docs recommend a code-execution integration for GPT-6 Astra, and also support the native computer tool with structured actions. Both approaches return observations to the model. The notebook uses the native computer tool to make the screenshot/action loop easy to see. Run only inside an isolated test environment, restrict the reachable destinations, and get human approval for consequential actions. This slide describes a capability; no real UI actions were performed while making the deck.

Source: https://developers.openai.com/api/docs/guides/tools-computer-use

## Slide 14: Code Interpreter: Python in a Sandbox

This is the most useful distinction for beginners: we do not have to write every line of the analysis ourselves. Give the model a file and a task, and Code Interpreter lets it write and run Python in an OpenAI-hosted sandbox. The result can include calculations, charts, a cleaned dataset, or another downloadable file. If a code step fails, the model can revise it and rerun. The configuration shown is the tools argument for a Responses API call with a supported model. Uploaded files must be attached or passed through the container's file_ids; the quoted CSV task is an illustrative prompt, not an executed result. In the companion notebook we upload a small sales CSV, request totals and a chart, check the calculation, and download the generated files. Files live in an ephemeral container, so save the outputs you need before it expires. Tool/container usage has separate API charges. Code Interpreter runs Python; programmatic tool calling on the next slides uses JavaScript to coordinate tools.

Source: https://developers.openai.com/api/docs/guides/tools-code-interpreter
Python logo source: https://www.python.org/community/logos/

## Slide 15: Shell Commands + File Edits

Code Interpreter is focused on Python. Shell gives an agent a terminal for broader work: run commands, inspect files, execute scripts and run tests. OpenAI supports a hosted shell container as well as a local runtime that your application operates. Apply Patch is the file-editing interface: the model requests create, update or delete operations as structured diffs, and your application or harness applies them and returns the outcome. A practical workflow is to edit a script, run its tests, inspect failures and revise the patch. The two tools complement each other, but enabling them is not a claim that every edit or command will succeed. Check the actual results and keep the permissions appropriate for the task.

Sources: https://developers.openai.com/api/docs/guides/tools-shell and https://developers.openai.com/api/docs/guides/tools-apply-patch

## Slide 16: Making Tool Use More Efficient

These are three distinct mechanisms. Tool Search reduces the need to include every full tool definition at the start: tools can be deferred and loaded when relevant. It searches the tools made available to the application, rather than discovering arbitrary services. Programmatic tool calling lets the model write JavaScript in an isolated hosted V8 runtime to coordinate enabled tools, loop over calls, filter large results and return a compact answer. This JavaScript runtime is different from Code Interpreter's Python sandbox and has no direct Node, filesystem or network access. Access goes through eligible enabled tools. Client-owned tools still run in your application. Tool Search happens at the top level before a program can invoke a newly loaded tool. Async tool calling is another option: the model can continue independent work while your application runs a slow function or custom tool, then you deliver its result later using the call ID. It is not a hosted job runner and is separate from background response generation. Current docs do not allow async calling to be configured together with programmatic calling; async is for direct function/custom calls, not built-in hosted tools. Check supported models and tool types before enabling either option.

Sources: https://developers.openai.com/api/docs/guides/tools-tool-search, https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling, https://developers.openai.com/api/docs/guides/async-tool-calling

