# Ask for Context - recording notes

Deck: `asking-for-context.pptx` (5 slides), built by `build_asking_for_context.py`.

## Purpose

This lesson teaches a small clarification gate: ask for information that could
materially change the result before writing the result.

## Speaking notes

1. **Ask for Context**
   - A short pause can prevent the model from filling gaps with guesses.
2. **A context check pauses the task at the right moment**
   - Ask the smallest useful set of questions before drafting.
3. **Missing information becomes part of the brief**
   - Combine the original request with the answers into one working brief.
4. **One short pause can prevent a full rewrite**
   - The trade-off is slower first output but fewer hidden assumptions.
5. **Live handoff**
   - Run an incomplete request, answer the questions and compare the result.

## Source checked on 2026-09-15

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5

## Review rounds

- Round 1, hostile reviewer: limited the pattern to questions that could change the output and added the failure mode of excessive clarification.
- Round 2, student: the Keynote render confirmed a clean contrast between immediate drafting and a context check.

## Round: visual upgrade (2026-09-28)

- Slide 2: copy beside the mock cut to one line.
- Slide 3: layers replaced with three grouped cards (Your Request with two "?" gaps, Its Questions, Complete Brief) joined by arrows, Lucide icons (ISC).
- Slide 4: table replaced with two timelines (Answer Now: draft, wrong audience, rewrite, draft 2; Ask First: questions, answers, draft 1) over a time axis, plus a failure-mode strip ("cap it at three").
