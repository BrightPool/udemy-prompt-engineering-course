# Adversarial Review of Outputs - recording notes

Deck: `adversarial-review.pptx` (7 slides), built by `build_adversarial_review.py`.
Follows "What is Codex and /goal"; the demo half is filmed in Codex.

## Purpose

Do not trust a first output because it reads well. Have a separate AI pass review the
work against checkable acceptance criteria, let the maker fix what failed, and only step
in once the loop has finished.

## Speaking notes

1. **Adversarial Review of Outputs**
   - A second AI checks the work against clear criteria, so you only review what passed.
2. **Fluent is not the same as correct**
   - The mock answer sounds confident and is wrong twice (highlighted). Models sound
     equally sure either way.
3. **How it works - a maker, a reviewer and a bar to clear**
   - Maker drafts, reviewer checks against criteria, maker fixes, repeat, you review the
     final. The reviewer runs with fresh context and is told to find problems.
4. **Acceptance criteria make the review real**
   - Reviewer prompt: do not rewrite, mark each criterion PASS/FAIL with evidence. The
     reply catches the same two errors from slide 2.
5. **You set the bar, then step away**
   - Your time goes into the two ends. The middle runs on its own, which is what /goal
     is for. Come back after ~30 minutes, or however long the task needs.
6. **Why it matters - it raises the floor, not the ceiling**
   - Walk the failure modes: shared blind spots, vague criteria, rubber-stamping,
     endless loops. You still do the final check.
7. **Let's see it in action**
   - Write the criteria, run the loop in Codex with /goal, come back and read the review
     first, then the work.

## Sources checked on 2026-09-26

- https://learn.chatgpt.com/use-cases/follow-goals (goals need a verifiable stopping
  condition and a way to validate progress)
- Codex icon: official asset from the ChatGPT desktop app bundle
  (`decks/codex-goal/assets/icon-codex-light.png`), used once, on slide 5.

## Review rounds

- Round 1, hostile reviewer: the highlighted correction on slide 2 sat inside the
  assistant's bubble, as if the model had corrected itself. Moved the correction into the
  copy and highlighted the wrong claims instead. Added a failure-mode table so the deck is
  not only benefits.
- Round 2, student: the Keynote render showed the time-axis label wrapping and the
  diagram sitting high. Recentred it and made the label a single line. Slides 2 and 4 now
  use the same example (Q3 churn), so the review visibly catches the errors from slide 2.

## For James

- The ~30 minute figure is from your brief. It is shown as "~30 min, or as long as it
  takes", so it isn't presented as a rule.

## Round: visual upgrade (2026-09-28)

- Slide 2: beside copy replaced by a "Checked against the sheet" panel: each claim, then what the sheet actually says (x / ? icons).
- Slide 3: flow boxes replaced by icon stations (maker drafts, reviewer checks, maker fixes, you review) with the return loop drawn between review and fix.
- Slide 4: beside copy replaced by a vague vs checkable pair.
- Slide 5: the two ends of the timeline are icon badges (you start, you return); caption shortened.
- Slide 6: failure-mode table replaced by icon rows: failure, symptom, arrow to the fix.
- Icons: Lucide (ISC licence) in `assets/`. Each row/station is a grouped shape.
