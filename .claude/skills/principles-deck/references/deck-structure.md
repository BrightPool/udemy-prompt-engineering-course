# Deck structure

The narrative arc for a principles deck. Write the arc before you write any code.

## Shape

10 to 14 slides, roughly 6 to 9 minutes of the video. Three phases, each opened by a
phase-titled slide.

```
Title                       1 slide    concept + one-line definition
What is it?                 3          d.what(...) on the first, then plain titles
How it works                3          d.how(...)
Why it matters              2-3        d.why(...)
Let's see it in action      1          d.handoff(...)
```

**There are no divider slides.** A slide that only says "What is it?" is fluff. The phase
prefixes the title of the slide that answers it - `d.what("a store the model writes to")`
renders as *"What is it? - a store the model writes to"* - and the slides that follow in
that phase use plain `d.content()` titles.

## Title

Concept name in the title, and a subtitle that is a **complete one-sentence definition**.
If you cannot write that sentence, the deck is not ready.

> Memory - How an assistant carries facts about you between conversations.

## What it is

The job is to make the concept concrete before explaining anything.

1. **Definition slide.** Plain language, no jargon, paired with the simplest possible mock
   of the feature doing its thing. One exchange, two or three lines.
2. **A second look.** Show the consequence, not a second feature. For memory: the same
   question a week later, answered with a preference nobody re-typed. This is where the
   idea lands.
4. **What it is not.** Use `s.compare()` - the misconception on the left, the reality on
   the right. Say the principle here, on a slide that also shows something.

## How it works

Mechanism, at the level of "what actually reaches the model". Avoid both hand-waving and
implementation detail the student cannot act on.

1. **The steps.** Three to five, via `s.steps()`. Each step is one clause.
2. **What reaches the model.** The most valuable slide in the deck. Show the assembled
   context as message rows: retrieved memories, system instructions, then the user's line.
   Students consistently misunderstand this, and a mock makes it obvious.
3. **Where it stops.** Limits and boundaries, side by side - stored vs not stored,
   sees vs cannot see. Honest boundaries are what make the rest credible.

## Why it matters

Consequences for the student's own results.

1. **Impact on results.** A comparison table: without the feature vs with it. Include the
   **failure mode** row - how it goes wrong is more useful than how it goes right, and it
   is the row students remember.
2. **When to use it, when not to.** `d.two_columns()`. Be willing to say "not for this".
3. **The cost.** Every capability has one: memory must be maintained, search adds latency
   and a trust problem, long context costs tokens. Name it in the copy, not on a slide of
   its own.

## Let's see it in action

Every deck ends on `d.handoff()`. Title, accent rule, one lead line, then two to four
numbered cards naming exactly what the instructor is about to do live, so the cut feels
planned rather than abrupt.

```python
d.handoff([("Turn memory on", "and find where it lives"),
           ("Write one memory", "then open a fresh chat"),
           ("Inspect the store", "edit an entry, delete another")],
          lead="That is the principle. Now we do it live in the tool.")
```

## Rules of thumb

- **One idea per slide.** If a slide needs "and", split it.
- **Copy beside the mock, not under it.** Body box at `(5.25, 1.46, 4.42, 3.39)` for a
  left-hand mock; mirror for a right-hand one.
- **Mocks and diagrams earn their place.** If a visual does not show something the words
  cannot, replace it with a better visual - not with a wall of text.
- **No pull-quote slides.** A sentence set large on an empty slide is fluff. If an idea
  is worth a slide, it is worth a slide that also shows something.
- **A single point never wears a bullet.** One item is a sentence, not a list.
- **Write the spoken track first if you are stuck.** The slides are the residue of the
  explanation, not the explanation itself.
