# Pre-Warming Chats - recording notes

Deck: `pre-warming-chats.pptx` (5 slides), built by
`build_pre_warming_chats.py`.

## Purpose

This lesson explains pre-warming as a compact setup exchange that establishes shared
context before the main request. It does not imply that the model becomes smarter.

## Speaking notes

1. **Pre-Warming Chats**
   - Start by establishing the goal, audience and source material.
2. **The conversation starts with a compact briefing**
   - Ask the model to restate the brief so mistakes can be corrected early.
3. **The current request sits on top of earlier context**
   - Later turns can reuse the brief without repeating every detail.
4. **Shared context improves continuity across turns**
   - Watch for stale assumptions and a conversation that has grown too large.
5. **Live handoff**
   - Prepare a fresh ChatGPT conversation, confirm the context and then give the task.

## Sources checked on 2026-09-15

- https://learn.chatgpt.com/docs/prompting
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5

## Review rounds

- Round 1, hostile reviewer: explicitly described the mechanism as conversation context and added stale-history risk.
- Round 2, student: the Keynote render confirmed that the three-turn mock and the context stack can be followed without extra interface explanation.

## Round: visual upgrade (2026-09-28)

- Slide 2: the briefing mock now shows all four parts (goal, audience, source, constraints), with an icon key beside it: "A Good Brief Has Four Parts". Copy cut to one line.
- Slide 3: the layers became an icon context stack (latest request on top), bracketed as "The model reads the whole stack, every turn", plus a restate-the-brief tip strip.
- Slide 4: the table became two timelines, cold request (fix afterwards, start over) vs prepared conversation (confirm, then tasks 1-3 on one shared brief), with the stale-history failure mode as a warning strip.
- Icons: Lucide (ISC licence), rendered into `assets/`. Related shapes are grouped so they move together.
