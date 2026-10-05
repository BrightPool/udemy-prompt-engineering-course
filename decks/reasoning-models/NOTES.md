# Reasoning Models - build notes

Lecture `reasoning-models` (video `48150231`, 05:39, Part 2 - ChatGPT Deep Dive).
Renamed from **Chat Models vs Reasoning Models** / "Choosing Different Models, Reasoning
Effort and Why It Matters" to **Reasoning Models**, per James's note.

Deck: `decks/reasoning-models/reasoning-models.pptx` (12 slides)
Build: `decks/reasoning-models/build_reasoning_models.py`

```bash
uv run --with python-pptx python decks/reasoning-models/build_reasoning_models.py \
    decks/reasoning-models/reasoning-models.pptx
uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
    decks/reasoning-models/reasoning-models.pptx
```

---

## The three principles

- **What it is** - a model that generates its own working, in tokens, before it writes the
  reply you read.
- **How it works** - that working is text the model produces for itself; you are billed for
  it as output and you wait for it, and what you can open on screen afterwards is a summary
  of it rather than the writing itself.
- **Why it matters** - the pause buys a check on multi-step work, which is worth paying for
  when a mistake was likely and is pure loss when it was not.

---

## Research

### Verified from primary sources (reachable from this environment)

`developers.openai.com/api/docs/guides/reasoning` (the old `platform.openai.com/docs/guides/reasoning`
now 301s here):

- Reasoning models "use internal reasoning tokens before producing a response", which lets
  them "plan, use tools effectively, inspect alternatives, recover from ambiguity, and
  solve harder multi-step tasks".
- Reasoning tokens "occupy space in the model's context window and are **billed as output
  tokens**", and are reported separately as `output_tokens_details.reasoning_tokens`.
- Their content is **not visible via the API**.
- `reasoning.effort` "guides how much to think when performing a task", with supported
  values running from `none` through `max`. Lower effort favours latency and cost. Models
  "reason adaptively across reasoning efforts, using fewer tokens for simpler tasks".
- Recommended for "complex problem solving, coding, scientific reasoning, and multi-step
  agentic workflows"; explicitly discouraged for "latency-critical tasks that do not
  benefit from any reasoning", naming "voice, fast information retrieval, and
  classification".
- Guidance to reserve at least 25,000 tokens for reasoning plus output; a response can come
  back incomplete, and billed, if reasoning exhausts the budget before any visible output.

`developers.openai.com/api/docs/guides/reasoning-best-practices`:

- Reasoning models for deep analysis, accuracy-critical decisions, ambiguity and multi-step
  reasoning; GPT-class models for speed-sensitive, well-defined, cost-conscious work. The
  recommended pattern is both: reasoning for planning, fast models for execution.
- Prompting differs: skip "think step by step" (it is internal already and can hurt), keep
  instructions short and direct, start zero-shot, state constraints explicitly.
- Beneficial task shapes: ambiguous or incomplete information, extracting detail from large
  inputs, patterns across complex documents, multi-step agentic planning, code review and
  debugging, and evaluating another model's answer.

`platform.claude.com/docs/en/build-with-claude/extended-thinking` (cross-vendor check, so
the deck is not an OpenAI-only claim):

- Thinking is a per-request budget or effort setting; thinking tokens count toward the
  turn's output and are reported as `usage.output_tokens_details.thinking_tokens`.
- Higher budgets give "more comprehensive reasoning, with diminishing returns that depend
  on the task, and at the cost of increased latency".
- Adaptive thinking: the model "decides whether and how much to think on each request, and
  at lower effort settings it may skip thinking entirely on easy inputs".
- Responses contain **summarised** thinking blocks, not the raw reasoning.

That cross-vendor agreement - thinking is generated tokens, billed as output, controlled by
an effort dial, summarised rather than shown - is what the deck teaches, so it survives
either vendor redesigning.

### Not verifiable here `[unverified - James to check on his account]`

`help.openai.com` and `openai.com` both return an empty shell through Playwright as well as
through plain fetching, so nothing about the consumer ChatGPT UI is primary-verified. The
following is from search summaries only and is recorded for the **demo half**, not the deck:

- The Instant / Thinking / Pro mode split in the model picker was reportedly retired on
  **6 August 2026**. On Plus and Pro a single model is said to handle both quick replies and
  longer reasoning, with a **thinking effort slider** per answer; the reported levels are
  Instant, Medium, High and Extra High, with Pro Standard and Pro Extended on Pro plans.
  Free and Go reportedly get a **Think** button that is a per-message toggle.
- Auto-switching is reportedly now under **Configure** in the model picker menu
  ("Auto-switch to Thinking").

Several independent secondary sources agree on the substance (one model plus an effort
dial, replacing the mode picker), which is why the deck is framed around a dial rather than
around two families of model. **James: please confirm the exact control and its wording on
your own account before filming the demo half.**

---

## What changed since filming

| Original lecture (03:33-04:56 and elsewhere) | Now |
|---|---|
| Two families: "chat models" vs "reasoning models" | One model with a thinking-effort dial you set per question |
| Picker walkthrough: Auto / Fast / Thinking / Pro | The picker has reportedly been replaced by an effort control `[unverified]` |
| "GPT-5 has two modes" | Named modes and model names are out of the deck entirely |
| Provider roll-call slide (OpenAI / Anthropic / Meta / Google / Mistral) | Cut - it dates fast and is covered by the "Exploring Other Model Providers" lecture |
| "Test time compute scaling" as the headline term | Cut as jargon; the deck teaches the mechanism (tokens generated before the answer) instead |
| Thinking tokens shown as visible output | Corrected: what you can open is a *summary*; the raw reasoning is not exposed |

**3:33-4:56 is entirely demo-half material.** It is a click-through of the model picker, so
none of it is in the deck; the current state of that control is in the unverified section
above for James to say aloud.

The one place the deck contradicts the original: the source video says reasoning models
"will definitely outperform chat models" on hard problems. That is broadly right but the
deck states the boundary as well - effort does not supply facts the model never had, does
not stop it inventing a source, and does not improve an easy answer.

---

## Deck arc

1. Reasoning Models *(title)*
2. What is it? - a model that works the problem out first
3. The same question, sent two ways *(the spine: two panels, same prompt)*
4. What it is not
5. How it works - it writes to itself before it writes to you
6. Effort is a dial, not a switch
7. What the pause costs you *(three cost buckets, with the working sitting in the dearest)*
8. Why it matters - hard questions stop failing quietly
9. When the thinking time is worth it
10. What effort cannot fix
11. Thinking time is not your time
12. Let's see it in action *(handoff)*

The worked example on slides 3 and 7 is deliberately arithmetic a viewer can check: 40
clients at £1,200 is £48,000 a month; losing 3 and raising fees 10% gives 37 at £1,320, or
£48,840 - up 1.75%, £840. The fast panel guesses the direction wrong; the slow one does the
sum.

Cost is taught as the three durable buckets (input / cached input / output) with no
figures, per the deck brief. The point the deck adds is that reasoning tokens land in the
**output** bucket - the dearest one - despite never being read.

---

## Review rounds

Lint was clean after the first build and after every round.

**Round 1 - the hostile reviewer.** Six findings, five substantive.

1. Slide 3 (the deck's most important slide) had the fast panel printing
   `Working / None. The reply below is the first thing the model wrote.` - slide-author
   prose, not something a product would ever render. Replaced: the fast panel simply has no
   thinking row, and both panels use `Thought for 24 seconds` / nothing, which is the real
   affordance.
2. Slides 2 and 3 used three near-identical chat panels in a row. Slide 2 is now the
   minimal case (question, pause, answer) and slide 3 is the only place the working is
   exposed, so the two slides progress instead of rhyming.
3. Slide 5's band note said "generated, never shown", which contradicts slide 3 showing a
   summary. Changed to "summarised, not shown raw".
4. Slide 10's left column claimed more effort will not "Show you its real reasoning" - true,
   but a product decision rather than a limit of effort. Swapped for "Improve an easy
   answer".
5. Table header "Turn the dial up and..." read as an unfinished sentence; trimmed.
6. Two-column items on slide 9 were running past the column width; three were shortened.

*Layout.* Content start heights were ragged across the deck - 1.56", 1.58" and 1.60".
Standardised on the course convention: `0.40, 1.56` for mock panels, `0.34, 1.52` for
everything on the white surface. Captions now sit a consistent 0.22" below the visual they
describe. On slide 3 the two panels were different heights (2.40" and 2.90") because each
was fitted independently; the taller one is now built first and the shorter one takes its
height and gains a matching composer bar, so the pair reads as one comparison.

**Round 2 - the student.** Six findings, four substantive, which is why there is a round 3.

1. The slide 5 title, "the thinking is writing you never see", contradicted slide 3, where
   the working *is* on screen. Retitled to "it writes to itself before it writes to you"
   and the body copy now says plainly that what you can open is a summary.
2. "Reasoning tokens" appeared as a band label before the copy introduced the word; the
   copy now defines it ("one token at a time") in its first clause.
3. Slide 6 explained what the dial does but never answered the obvious "where is it?".
   Added a caption saying the control moves with every release and the trade-off does not -
   which is also the deck's licence not to show a menu path.
4. Slides 9 and 10 read as the same slide from the titles alone. Slide 10 became "What
   effort cannot fix", so 9 is about task shape and 10 about failure modes.
5. "three buckets" in the slide 7 caption did not match the table's wording; now "three
   rates".

*Layout.* On slide 6 two of the four flow nodes had two-line sub-labels and two had one, so
the row of node labels sat at two different heights. All four subs shortened to a single
line; the labels now align at 1.69".

**Round 3.** Three findings, one of them the most important in the build.

1. **The comparison did not prove its own point.** The fast panel answered "Roughly flat",
   and the correct answer is +1.75% - which *is* roughly flat. The slide therefore showed a
   fast model being right. The fast reply now gets the direction wrong ("Revenue dips
   slightly - a 10% rise will not cover losing 3 clients"), which is the slip this shape of
   question actually produces, and the caption says what went missing rather than calling
   the answer stupid.
2. The title subtitle argued for the feature instead of defining it; rewritten as a
   definition.
3. "A prefix sent again" on the cost table was API jargon for a beginner audience; now "A
   prompt you resend".

*Layout.* Nothing further; all visuals start at 1.52" (1.56" for mocks), captions sit 0.22"
below their visual, deepest content is 5.02" against the 5.10" floor.

---

## For James

1. **Confirm the current control before filming the demo half.** Everything about the
   ChatGPT picker is `[unverified]` here - `help.openai.com` and `openai.com` are both
   unreadable from this environment, even through a real browser. Search summaries
   consistently say the Instant / Thinking / Pro modes were replaced on 6 Aug 2026 by one
   model plus a thinking-effort slider (Instant / Medium / High / Extra High, with a Think
   button on Free and Go), and that auto-switching moved under **Configure**. Please check
   the wording on your own account; the deck deliberately never names any of it.
2. **The framing has shifted since you filmed.** The original lecture teaches two families
   of model. The durable framing now, and the one the deck uses, is one model with an
   effort dial. If you would rather keep "chat model vs reasoning model" as the spoken
   framing, say so and I will re-cut slides 4 and 6 - but the API docs from both OpenAI and
   Anthropic describe an effort setting, not a product split.
3. **Overlap to watch.** Slide 7 teaches the three cost buckets, which is also the spine of
   the "What are Tokens?" deck (Part 1). Here it exists only to land one point - reasoning
   tokens are billed as output, the dearest bucket, despite never being read. If the tokens
   lecture ends up covering the buckets in more detail, this slide can be compressed to
   that single row.
4. **One point to say aloud, not on a slide.** A reasoning request can hit its token ceiling
   while still thinking and come back with nothing usable - and you are still billed for
   the reasoning. It is a real failure mode but it is API-side, so it is out of the deck.
5. **The closing practice is yours, kept verbatim in spirit** - slide 11 is the "do not sit
   and wait for it, go and do something else" point from the end of the original recording,
   because it is the most actionable thing in the lecture.
