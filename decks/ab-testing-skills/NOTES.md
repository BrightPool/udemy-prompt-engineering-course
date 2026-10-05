# A/B Testing - How to Systematically Improve Your Skills

`decks/ab-testing-skills/ab-testing-skills.pptx` - 13 slides, built by
`build_ab_testing_skills.py`. New lecture, never filmed, no transcript. Closes the
Skills & Plugins section.

## The three principles, one sentence each

- **What it is** - an A/B test is the same job run against two versions of a skill that
  differ in exactly one line, judged over a fixed set of cases against criteria you wrote
  down before you looked at anything.
- **How it works** - hold the request, the cases and the model still, move one line, run
  both versions over the same ten cases, and score each output against the criteria you
  already wrote.
- **Why it matters** - it turns "this feels better" into a tally you can act on, hand to
  a colleague, and re-run later, so the skill improves in a direction you can name.

## Research

Nothing on these slides is a product claim, so nothing here can drift with a redesign.
The method claims that do need grounding:

- **Define success before you evaluate.** Anthropic's own guidance opens with "Building a
  successful LLM-based application starts with clearly defining your success criteria and
  then designing evaluations to measure performance against them", and asks for criteria
  that are specific and measurable - "accurate sentiment classification", not "good
  performance". It lists A/B testing against a baseline as a quantitative method in its
  own right. Verified 2026-09-08 at
  `platform.claude.com/en/docs/test-and-evaluate/define-success`.
- **n=1 is worthless here.** The same skill, same input, run three times, does not give
  the same answer. This is directly observable by anyone in the audience and is the point
  Mike already demonstrates in the GSheets lecture ("this is the thing with LLMs, they
  don't always give you the same response back"). The deck does not explain *why* - the
  Hallucinations and Tokens lectures own that - it just establishes that a single good
  answer is one draw, not a result.
- **Why ten.** Ten is not defended as statistics anywhere and the deck does not pretend
  it is. It is defended as the number small enough that a no-code learner will actually
  do it, and large enough that a real difference turns up more than once. Mike's own
  worked result is the honest counter-example: his variation C came out 7.4% longer over
  ten observations, which is exactly the size of gap ten runs cannot separate from noise.
  Slide 11 says so directly ("a one- or two-case difference").
- **Judging without a framework.** The existing `What are Evals?` deck already teaches the
  programmatic / synthetic / human taxonomy. This lecture stays deliberately inside the
  "human" corner of that and never uses the word "eval" for a method, so the two do not
  collide.

Confidence: no `[unverified]` claims. There is no UI on any slide, no menu path, no
version number and no price.

## Boundary against the neighbouring lectures

| Lecture | Owns | This deck therefore |
|---|---|---|
| `what-are-skills` | what a skill is; the description decides when it fires | assumes it, never re-defines "skill" |
| `creating-skill-*` | writing one | assumes you already have one to change |
| `practicing-plugins` | chaining connectors, wrapping as a skill | not mentioned |
| `gsheets-prompt-testing` (Mike, 13:06) | the **mechanics** - sheet columns, template vs formatted prompt, playground, pivot table, word-count formula | teaches only the **method**, and never shows a spreadsheet |
| `What are Evals?` | the eval taxonomy and benchmarks | avoids the taxonomy entirely |

The split with Mike's lecture is the one worth stating out loud on camera: he shows you
how to run a prompt test in a sheet; this shows you how to decide what to change and how
to read the result. The running example is deliberately different too - Mike tests blog
post length, this tests a `meeting-notes` skill.

## Slides

1. Title
2. What is it? - the same job, two versions, one line apart
3. Why one good answer proves nothing
4. Choosing the ten cases
5. How it works - hold everything else still
6. The one line that moved
7. Criteria, written before you look
8. Ten runs, one tally *(the hero: a light results table)*
9. Three results, three decisions
10. Why it matters - the skill gets better on purpose
11. What the tally does not tell you
12. When it is worth ten runs
13. Let's see it in action

Lint: `clean - 13 slides, nothing to fix`.

## Review rounds

**Round 1 - the hostile reviewer.** Seven findings, all fixed.
1. Slide 3's caption said "the whole reason for running ten" before slide 4 had
   introduced ten. Rewritten to "more than one run".
2. Slide 6 carried a fifth band, "Who scores it - same person", which flatly contradicts
   slide 7's blind-scoring point. Cut.
3. *(layout)* That fifth band pushed the slide 6 caption to y=4.62, overlapping the last
   band and running to 5.07" - inside the footer band. Cut the band, caption to 4.28.
4. Slide 9's first node said "adopt it - and it becomes the new control", which is the
   closing node of slide 10's flow. Reworded to point back at the tally's trade-off.
5. *(layout)* Slides 9 and 10 started their visuals at 1.60" while slides 4, 6, 7, 8 and
   11 started at 1.52". Both moved to 1.52".
6. *(layout)* Slide 5's caption sat at 1.86" against a step stack running 1.52"-4.88",
   reading as stranded at the top. Moved to 2.60" to centre against the stack.
7. Slide 8's caption referred to "three slides ago", which had stopped being true.
   Also fixed a resulting overflow on slide 3 (the copy beside the mock needed more
   height than the mock left it) by tightening the copy and dropping the caption to 4.12".

**Round 2 - the student.** Five findings, all fixed.
1. Slide 2's mock *described* its outputs ("Nine bullets. Two decisions buried in the
   list.") rather than showing them, so it read as placeholder text. Replaced with actual
   note lines, which also makes the difference between A and B visible rather than
   asserted.
2. The obvious question - "what if I am the only person here?" - went unanswered next to
   an instruction to have someone else score blind. Slide 7's caption now says to strip
   the labels off all twenty outputs and score them as one shuffled list.
3. Slides 5 and 6 taught "control" and "variant"; slide 8's table then said "One line
   added". Column heading changed to "Variant".
4. Slide 9's "you have just saved yourself a habit" is ambiguous. Now "you have avoided a
   habit that does nothing".
5. The handoff said "the same ten, in the same order" - run order is irrelevant and the
   frozen list is not. Now "the same ten, nothing added".

**Round 3** (run because round 2 found more than two substantive issues). Three findings.
1. Slide 3's mock closed on "Three answers. One of them is wrong." Two of the three runs
   fail a criterion, so the line was simply false. Now "No two of them the same", which is
   the point anyway.
2. Slide 6's caption ended on "this is the whole discipline, and it is the part people
   skip" - a boast, not an argument. Replaced with the actual reason: two changes can mask
   each other, so a better result tells you nothing about which line did it.
3. Slide 8's tally scored four criteria but slide 7 only listed three, and "Under 200
   words" appeared from nowhere. Added it to slide 7 and re-flowed that slide.

Layout pass run in all three rounds against a shape-geometry dump (no LibreOffice on this
machine, so no rendered thumbnails - every box was checked numerically for start height,
overlap, footer collision and dead space).

## For James

**The demo I would run.** Everything on the slides is built around one worked example, so
the demo lands hardest if it is the same one:

- **The skill**: `meeting-notes` - takes a raw meeting transcript, returns notes.
- **The single change**: add one line to its instructions - *"List every decision first,
  under its own heading, before any action items."* Nothing else changes. Say out loud
  that you are resisting the urge to also fix the wording you dislike, because that is the
  whole lesson.
- **The ten cases**: ten real transcripts you already have - two ordinary ones, a couple
  of long rambling ones, one where two people talk over each other, one that is mostly
  small talk, and the one that produced bad notes last time. Show yourself choosing them
  *before* the change, and say you will not add an eleventh however tempting.
- **The criteria, written on camera before any output exists** - the four on slide 7:
  every decision appears and is labelled a decision; every action names an owner; nothing
  appears that nobody said; under 200 words.
- **The tally**: twenty runs is too long for the video. Run three or four live, then cut
  to the completed tally - the numbers on slide 8 are the shape to aim for, including the
  loss on "Under 200 words". That loss is the most valuable thing in the lecture and it is
  worth saying so.

**The boundary I drew against Mike's GSheets lecture** - please sanity-check it. Mike owns
the mechanics (sheet layout, template vs formatted prompt, the playground, the word-count
formula, the pivot table). I own the method (one change, criteria first, judge across
samples, read the result honestly). No spreadsheet appears anywhere in this deck, and the
running example is different from his on purpose. If you would rather this lecture *used*
his sheet as its tally, that is a one-line change to the demo half and no change to the
deck - but I would keep them separate, because the method needs to survive someone who
tallies on paper.

**Two things to decide.**
1. **Where this sits.** It currently closes Skills & Plugins, which works - you have just
   built a skill, now improve it. But Mike's GSheets lecture is the very next thing in the
   manifest and covers testing too, so the two testing lectures run back to back. If you
   would rather they were not adjacent, this one could move to sit beside the evals
   material in Part 17 instead. I have not assumed either way.
2. **The word "eval".** The deck never uses it, deliberately, so it does not collide with
   the existing `What are Evals?` lecture. If you want an explicit bridge, the natural
   spoken line is at slide 8: "there is a whole discipline called evals built on top of
   this, and we cover it later - but the tally is the honest core of it and it needs no
   tooling at all."

**Terminology.** Follows the section convention: "skill" lowercase throughout, and
"connector" is never needed here. The lecture title in the manifest is "A/B Testing - How
to Systematically Improve Your Skills"; the deck's title slide reads "A/B Testing Your
Skills" so it fits at 30pt without wrapping awkwardly. Rename the file if you would rather
they matched exactly.

## Round: visual upgrade (2026-09-28)

- Slide 2: copy beside the mock cut to one line.
- Slide 3: mock replaced with three run cards drawn as dot counts (decisions, actions, unowned), so the run-to-run variation is visible; odd runs outlined pink.
- Slide 4: compare panels replaced with two rows of ten case tokens (ten "Easy" vs six Real, three Hard, one Failed), a legend and a "freeze the list" lock strip.
- Slide 5: steps list replaced with a five-step icon timeline (pencil, lock, copy, play, chart) with numbered badges.
- Slides 6, 10, 11: captions cut to one line.
- Slide 7: caption replaced with a one-line "score blind, shuffle" strip with icon.
- Slide 8: table replaced with a control-vs-variant bar chart out of ten, with Win / Weigh / Loss tags.
- Slide 9: plain nodes replaced with icon cards (trophy, x, scale).
- Slide 12: two bullet columns replaced with two icon panels (flask: worth testing; pencil: just change it).
- Icons: Lucide (ISC), rendered into assets/. Related shapes are grouped.
