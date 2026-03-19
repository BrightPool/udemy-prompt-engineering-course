# Building a Coding Agent from Scratch

**By James Phoenix** | O'Reilly Author of "Prompt Engineering for Generative AI"

Ever wondered how tools like Claude Code and Cursor actually work under the hood? Spoiler: it's just an LLM in a loop with 5 simple tools.

In this hands-on module, James walks you through building a fully functional coding agent from scratch using the OpenAI Agents SDK. You'll start with a plain chatbot and, lesson by lesson, add one tool at a time until you have an agent that can explore codebases, read and write files, run shell commands, search code with regex, and pull in live documentation from any library.

No magic. No frameworks hiding the complexity. Just you, an LLM, and a handful of Python functions.

---

## What You'll Build

A coding assistant that can:

- Explore project directories and discover files
- Read source code and understand context
- Create, edit, and append to files with surgical precision
- Run shell commands to test, verify, and interact with the system
- Search across entire codebases using pattern matching
- Look up live documentation for any library via MCP

By the end, you'll understand that the tools you use every day (Claude Code, Cursor, Windsurf) are built on these exact same primitives.

---

## Lessons

| # | Notebook | What You'll Learn | Tool Added |
|---|----------|-------------------|------------|
| 1 | [basic_chat.ipynb](basic_chat.ipynb) | The agent loop: user input, LLM reasoning, response | None (foundation) |
| 2 | [file_reader.ipynb](file_reader.ipynb) | Tool calling with `@function_tool`, auto-generated JSON schemas | `read_file` |
| 3 | [file_explorer.ipynb](file_explorer.ipynb) | Tool composition: the agent chains tools autonomously | `list_files` |
| 4 | [command_runner.ipynb](command_runner.ipynb) | System interaction: running commands, capturing output | `run_command` |
| 5 | [file_editor.ipynb](file_editor.ipynb) | The full read-edit-verify cycle for code generation | `edit_file` |
| 6 | [code_search.ipynb](code_search.ipynb) | Pattern-based search across codebases | `search_code` |
| 7 | [mcp_context7.ipynb](mcp_context7.ipynb) | Extending your agent with MCP servers for live docs | Context7 MCP |

Each lesson builds directly on the last. By Lesson 6, you have a complete coding agent with 5 hand-written tools. Lesson 7 shows how to extend it further using the Model Context Protocol.

---

## The 5 Essential Primitives

These are the only tools a coding agent needs. Every professional AI coding tool is built on this same foundation:

| Tool | What It Does |
|------|-------------|
| `read_file` | Read file contents (with truncation for safety) |
| `list_files` | List directory contents to discover project structure |
| `run_command` | Execute shell commands with timeout and output limits |
| `edit_file` | Create, append, or replace file contents (single-match safety) |
| `search_code` | Regex search across codebases with file type filtering |

The power isn't in any individual tool. It's in how the LLM composes them: list a directory, read the relevant files, search for a pattern, edit the code, run the tests, verify the output. All decided by the model, not by you.

---

## Prerequisites

- Python 3.10+
- An OpenAI API key
- The OpenAI Agents SDK:

```bash
pip install openai-agents
```

For Lesson 7 (MCP), you'll also need Node.js installed (for `npx`).

---

## Quick Start

1. Clone this repo and navigate to this folder
2. Install dependencies: `pip install openai-agents`
3. Open `basic_chat.ipynb` and follow along
4. Work through each notebook in order (1 through 7)

Each notebook is self-contained and will prompt you for your OpenAI API key at runtime.

---

## Key Concepts Covered

- **The Agent Loop**: How LLMs decide when and which tools to call
- **Tool Calling**: Converting Python functions into LLM-callable tools with `@function_tool`
- **Tool Composition**: How agents autonomously chain multiple tools together
- **Safety Patterns**: Output truncation, command timeouts, single-match edits
- **Model Context Protocol (MCP)**: Plugging in external tool servers without writing tool code
- **Stateless Execution**: Each `Runner.run()` call is independent

---

## About James

James Phoenix is the co-author of [Prompt Engineering for Generative AI](https://www.oreilly.com/library/view/prompt-engineering-for/9781098153427/) (O'Reilly Media, 5,000+ copies sold). He has written ~350,000 lines of production code, built SaaS platforms handling 917 RPS across multiple LLM providers, and taught 304,646+ learners on Udemy alongside 45+ bootcamps at General Assembly.

He builds in public at [twitch.tv/jamesaphoenix](https://twitch.tv/jamesaphoenix).

---

## Part of the Udemy Course

This module is part of James's Udemy course on prompt engineering and AI agents. The full course covers prompt engineering fundamentals, advanced techniques, AI agent architectures, and hands-on projects.

Questions or feedback? Reach out at jamesaphoenix@googlemail.com.
