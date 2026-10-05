# The two-round adversarial review

**Mandatory. Every deck, every time.** A deck that has not been through both rounds is
not finished, however good the build script looked.

`check_deck.py` catches geometry. It cannot see that a slide is boring, redundant, wrong,
or that the mock says something the words contradict. That is what these rounds are for.

The loop is: build → lint → **round 1** → fix → rebuild → lint → **round 2** → fix →
rebuild → lint clean. Two full rounds minimum. If round 2 turns up more than two
substantive findings, do a third - the deck is not settling.

**Every round ends with a layout pass, and you fix what you find.** The linter is the
floor, not the ceiling: it cannot see a panel that is technically legal but visually
lopsided, a caption stranded far from what it describes, or three slides that each place
their visual at a different height. Open the deck, look at every slide, and correct the
layout in the build script before moving on. A round is not finished while a slide still
looks wrong.

Read each round's rubric **before** looking at the slides, and go slide by slide. Write
the findings down as a numbered list with slide numbers before changing anything;
reviewing and fixing at the same time is how findings get quietly dropped.

## Round 1 - the hostile reviewer

You are a colleague who thinks this deck is padded and slightly wrong. Prove it.

**Substance**
- Which slides could be deleted with no loss? Delete them. Sparse filler is worse than a
  shorter deck.
- Is any slide making two points? Split it or cut one.
- Is any claim actually false, or true only of one vendor's current build?
- Does the mechanism section explain *what reaches the model*, or just gesture at it?
- Is there a real limit or failure mode stated, or only benefits? A deck with no honest
  boundary is marketing.

**Drift**
- Any real screenshot? Remove it.
- Any menu path, version number, price, or button location? Move it to the demo half.
- Would every line still be true after a redesign? See [anti-drift.md](anti-drift.md).

**Craft**
- Any slide that is a large quotation or a lone sentence set big? Cut it. These read as
  fluff, not emphasis.
- Any slide that exists only to announce a section? Fold it into the next slide's title.
- Any mock trailing dead space? `.fit()` or `.composer(pin=False)`.
- More than one highlight pill in a mock? Keep the best one.
- A single point wearing a bullet? Suppress the glyph.

**Layout - fix these, do not just note them**
- Does every visual start at the same y? Content below the title belongs at 1.52", clear
  of the dashed divider at 1.39". Ragged start heights across slides read as sloppiness
  even when no single slide looks wrong.
- Is anything crowding the dashed rule under the title, or competing with it?
- Is copy beside a mock still using a hardcoded box? Switch it to `s.beside()`.
- Is a caption near the thing it describes, or stranded across the slide?
- Is the balance right - a narrow panel against a wide column of text, or two blocks of
  wildly different weight?
- Do the margins hold? 0.34" for slide chrome, 0.40" for mock panels, nothing past 5.10".
- Are optically similar slides actually aligned, or off by a tenth of an inch?

## Round 2 - the student

You have never seen this feature. You are watching at 1.5x on a laptop.

- **Where do I get lost?** Name the first slide where a term appears that was never
  defined. Define it earlier or cut it.
- **What would I ask?** If an obvious question goes unanswered, answer it.
- **Can I read it?** Nothing under 12pt on the white surface. Look at the smallest text
  on every slide and ask whether it survives a projector.
- **Does the arc hold?** Read only the titles, top to bottom. They should tell the whole
  story on their own. If they do not, the titles are decorative and need rewriting.
- **Is the mock believable?** Does the assistant's reply read like a real reply, or like
  placeholder text a slide author wrote?
- **Does the last slide make me want the demo?** It should name what happens next.

## Recording the outcome

State plainly what each round found and what you changed, for example:

> Round 1: cut 2 filler slides (the pull-quote and a restated definition), removed a
> version number on slide 6, tightened the mock on slide 4. Layout: slides 3 and 5
> started their panels at 1.44" and 1.61" - both moved to 1.52".
> Round 2: slide 8 used "context window" before defining it - added a clause on slide 7;
> raised the caption on slide 9 from 10pt to 12pt. Layout: the caption on slide 6 sat
> under the wrong column, moved it beside the diagram it describes.

If a round genuinely found nothing, say so - but a first round that finds nothing almost
always means the rubric was skimmed rather than applied.
