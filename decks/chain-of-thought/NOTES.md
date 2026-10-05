# Chain of Thought - recording notes

Deck: `chain-of-thought.pptx` (5 slides), built by `build_chain_of_thought.py`.

## Purpose

This lesson updates the opening explanation of chain of thought. It separates an
observable workflow requested in a prompt from the reasoning a model performs before
returning an answer.

## Speaking notes

1. **Chain of Thought**
   - The phrase is often used for two related but different ideas.
2. **Two ideas share one name**
   - Prompted steps are visible work products; internal reasoning supports the answer.
3. **A reasoning request can stay outcome focused**
   - Give the goal, evidence, checks and expected answer shape.
4. **Visible checks are more useful than a long transcript**
   - Ask for assumptions, calculations, evidence and a concise rationale.
5. **Live handoff**
   - Compare a bare request with one that asks for checkable support.

## Sources checked on 2026-09-15

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-4.1

## Review rounds

- Round 1, hostile reviewer: avoided presenting one prompting recipe as universal and separated exact workflow requirements from model-selected reasoning.
- Round 2, student: the Keynote render confirmed that the distinction and the evidence checklist remain clear in five slides.
