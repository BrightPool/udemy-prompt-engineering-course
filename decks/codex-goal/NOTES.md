# What is Codex and /goal - recording notes

Deck: `codex-goal.pptx` (7 slides), built by `build_codex_goal.py`. Official Codex and
ChatGPT app icons in `assets/`, copied from the macOS ChatGPT app bundle
(`/Applications/ChatGPT.app/Contents/Resources/icon-codex-light.png`, `icon-chatgpt.png`).

## Purpose

Shows when to use Codex instead of ChatGPT, then introduces `/goal`: a persistent
objective with a checkable stopping condition, instead of a prompt you steer turn by turn.
Leads straight into Adversarial Review of Outputs.

## Speaking notes

1. **What is Codex and /goal**
   - Two ideas: an agent that works in your files, and giving it an objective, not a prompt.
2. **Codex does the work, not just the talking**
   - ChatGPT: you are the loop (copy out, run, paste errors back). Codex: the agent is the
     loop (reads, edits, runs, hands back changes). Same account.
3. **When to reach for Codex**
   - Rule of thumb: if the work lives in files, give it to Codex.
4. **How it works - /goal keeps Codex working until it is done**
   - Plan, act, check, repeat across turns, for hours if needed. Walk the five commands:
     start, check progress, pause, resume, clear.
5. **A prompt steers one turn, a goal defines done**
   - A goal has an objective, limits, proof and a stop condition. If you cannot say how
     to check it, use a normal prompt.
6. **Anatomy of a good goal**
   - Interview transcripts to findings report. Point at the highlighted proof and stop
     lines: they are what let it run unattended.
7. **Let's see it in action**
   - Open a folder in Codex, set one goal, watch the loop. Tease next lecture: a second AI
     reviews the work before you do.

## Demo-half details (kept off the slides on purpose)

- Checked 2026-09-26 on codex-cli 0.156.1: `codex features list` shows `goals` as
  stable and on by default. Older builds needed `features.goals = true` in `config.toml`.
- Goals are available in the Codex CLI, desktop app and IDE extension.
- Cost: a goal can run for hours and spends usage the whole time. A vague stop line
  means it runs long or stops early. Say this out loud in the demo.

## Sources checked on 2026-09-26

- https://learn.chatgpt.com/use-cases/follow-goals
- https://www.morphllm.com/comparisons/chatgpt-vs-codex

## Review rounds

- Round 1, hostile reviewer: "/goal" was being title-cased to "/Goal" (fixed in
  `deckkit.title_case`: words starting with "/" are left as written); removed the
  unverified "same models" claim; fixed a table column collision, a wrapping command chip
  and an overlapping handoff card.
- Round 2, student: slide 6 described "four parts" that did not match slide 5's objective,
  limits, proof, stop; aligned the copy. Fixed two remaining wraps (a command label and a
  table row).

## Round: visual upgrade (2026-09-28)

- Slide 2: two bullet cards replaced by two step chains (ChatGPT, Codex) coloured by who does each step (you = grey, the AI = pink), with the official app icons.
- Slide 3: table replaced by task rows: task icon, why, arrow to the right tool's logo.
- Slide 4: flow replaced by a loop ring (Plan, Act, Check, Done?) around the Codex icon; commands listed beside it, typed exactly.
- Slide 5: compare panels replaced by two timelines (a prompt = you steer every turn; a goal = one hand-off, runs to the stop line) plus the four parts of a goal as icons.
- Slide 6: beside copy replaced by five icon callouts matching the goal's lines.
- Icons: Lucide (ISC licence) in `assets/`. Each row/station is a grouped shape.
