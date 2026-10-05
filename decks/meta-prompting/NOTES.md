# Meta Prompting - recording notes

Deck: `meta-prompting.pptx` (5 slides), built by `build_meta_prompting.py`.

## Purpose (rewritten 2026-09-26, James)

Meta prompting = once a ChatGPT conversation has produced the output you want, ask
ChatGPT to turn that conversation into a reusable prompt, so the task can be repeated
with the same result. The earlier version of this deck taught "ask the model to question
you first", which is the separate Ask for Context lecture.

## Speaking notes

1. **Meta Prompting**: turning a conversation that worked into a prompt you can reuse.
2. **The conversation becomes the prompt**: after ten turns of corrections the newsletter is
   right. "Turn this conversation into a reusable prompt" captures role, input, steps,
   format and what to avoid.
3. **Iterate once, then reuse the recipe**: iterate, capture, reuse, same output. When a run
   drifts, fix the prompt, not the output. Test it in a fresh chat.
4. **Repeatable tasks stop costing a conversation each**: corrections baked in, consistent
   structure, shareable. Failure mode: it copies a mistake or one-off detail too, so read
   it before saving.
5. **Live handoff**: get one great output, ask for the prompt, run it fresh.

## Review rounds

- Round 1, James: the concept was wrong (it described Ask for Context). Deck rewritten.
- Round 2, layout: flow labels wrapped into their sub-labels; shortened, and deckkit's node
  estimate padded so wrapped labels get room.

## Round: visual upgrade (2026-09-28)

- Slide 2: five correction bubbles flow into the ChatGPT prompt; caption "Every correction becomes a line in the prompt."
- Slide 3: icon stations (Iterate, Capture, Reuse, Same Output) plus an illustrative "turns per run" bar chart (10, then 1 each run) and three check takeaways.
- Slide 4: table replaced by an icon scorecard, the meta-prompt column highlighted.
- Icons: Lucide (ISC licence) in `assets/`.
