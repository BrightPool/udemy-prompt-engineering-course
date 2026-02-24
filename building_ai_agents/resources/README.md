# Building AI Agents: Resources

This folder keeps data, prompts, and reference docs out of notebooks so you can focus on building agents.

## What goes here

| Folder / File | What it contains |
|---------------|-----------------|
| `data/knowledge_base/*.md` | Markdown docs used by the customer support agent |
| `data/customer_support_sample.json` | Sample customers, products, and orders |
| `data/sql_analysis_sample.json` | Sample analytics database (customers, products, orders, line items) |
| `data/docs_watcher_content.json` | Simulated page versions for the docs watcher agent |
| `prompts/*.txt` | System instructions loaded at runtime |
| `function-calling-flow.md` | The standard OpenAI tool-calling loop (reference) |
| `tool-schema-pattern.md` | Pydantic pattern for strict function tools (reference) |

## How notebooks use these files

Notebooks load data from this folder at runtime so you can focus on agent logic:

```python
import json, pathlib

RESOURCES = pathlib.Path("resources")

# Load JSON data
data = json.loads((RESOURCES / "data" / "customer_support_sample.json").read_text())

# Load knowledge base docs
kb = {}
for md_file in (RESOURCES / "data" / "knowledge_base").glob("*.md"):
    kb[md_file.name] = md_file.read_text()

# Load system prompt
instructions = (RESOURCES / "prompts" / "customer_support_agent_instructions.txt").read_text()
```
