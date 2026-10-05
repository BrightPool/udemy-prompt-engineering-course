# Skills Based Agents

Part 10: Advanced (Going Deeper), Building AI Agents - Coding. Owner: James.

Two slides accompany `building_ai_agents/skills_based_agents.ipynb`:

1. Skills Give Agents a Repeatable Process: a skill folder, its manifest and supporting files, discovery and the distinction between tools and workflows.
2. Attach the Skill, Then Run the Agent: add the files to the hosted sandbox, register the parent in capability_directories, submit a task and verify the results.

The notebook creates a sales-report skill with a readable SKILL.md and a Python helper. It sends those files and synthetic CSV data to an OpenAI-hosted Agents API environment with network access disabled. The short task explicitly asks for a manifest read to make the execution trace visible, then runs the report workflow. Checks confirm the manifest read, helper execution, output schema, exact report format and revenue totals.

## Filming

Allow roughly 4-5 minutes. Run package setup before recording. Show the manifest, highlight the capability_directories configuration, run the agent request, then show the report and the checks. The supporting script and stream helper are supplied; they do not need a line-by-line walkthrough. This builds on the Part 7 Managed Agents notebook.

## Verification

On 1 October 2026, the notebook passed end-to-end Papermill execution against the live Agents API using openai 3.22.1. The agent completed its root turn, read the skill manifest with a successful shell command, ran the supplied script successfully, and published all three expected artifacts. The notebook downloaded them and verified North=420, South=360, total=780 and the standard report format. It deleted its owned remote session after download.

The agent recovered from a missing rg command by using find; completion is not presented as evidence that every intermediate command succeeded. Local checks also passed for malformed/empty input, nonfinite values, exact decimal arithmetic, inline attachments and notebook structure. Source notebook execution outputs remain empty.

The two-slide deck passed package, slide-count, font, geometry and heading-fit checks. Both final slides were rendered and inspected. Editable text and code, external links and speaker notes are included.

The Colab link will become available after the notebook is pushed to the repository's main branch. No Git commit or push was requested or performed.

## Sources

- https://developers.openai.com/api/docs/guides/tools-skills#agents-api
- https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted
- https://developers.openai.com/api/docs/guides/agents-api/sessions/events
- https://developers.openai.com/api/docs/guides/agents-api/environments/files
- https://agentskills.io/specification

## Slide 1 speaker notes

This lesson builds on the managed agent harness from Part 7. A skill is a reusable folder with a SKILL.md manifest and optional supporting files. Its name and description tell the agent when the skill is relevant; full instructions describe how to perform the work. Keep scripts, reference material and templates alongside it and link to them from the manifest. Our example is a sales-report skill that tells an agent to calculate totals using a supplied Python script, create a standard report and check the arithmetic. The supporting script handles the repeatable calculations while the model decides how to use it for the task. Tools and skills have different roles: tools provide actions, while a skill packages a process for carrying out a task. Skill discovery does not guarantee correct execution, so we still evaluate the output. Show the manifest and the folder in building_ai_agents/skills_based_agents.ipynb, then run the notebook example.  Sources: https://developers.openai.com/api/docs/guides/tools-skills, https://agentskills.io/specification

## Slide 2 speaker notes

There are two setup steps in our managed Agents API example. First, install the skill folder and supporting files in the sandbox. The notebook supplies small files through environment.files; hosted environment files are prepared before setup commands run. Second, register the parent directory in environment.capability_directories. If the skill is /workspace/skills/sales-report/SKILL.md, the parent directory is /workspace/skills. The harness discovers the skill's metadata, and the model can read its full instructions and supporting files. The snippet is the environment configuration used when creating an Agents API session; skill_files is the list prepared in the notebook. Then submit a short task that explicitly asks for the sales-report skill. The notebook checks saved execution commands for a successful read of SKILL.md and a successful execution of summarize_sales.py, then downloads and verifies the report, CSV and JSON summary. Keep these checks separate from the model's own claim that it used a skill. This directory-discovery setup is distinct from Responses API hosted shell skill_reference attachments. Attach reviewed instructions and code, retain appropriate tool permissions, and check the final work.  Sources: https://developers.openai.com/api/docs/guides/tools-skills#agents-api, https://developers.openai.com/api/docs/guides/agents-api/environments/openai-hosted, https://developers.openai.com/api/docs/guides/agents-api/environments/files Companion notebook: building_ai_agents/skills_based_agents.ipynb

