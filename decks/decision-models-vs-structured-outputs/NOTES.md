# Decision Models vs Structured Outputs - recording notes

Deck: `decision-models-vs-structured-outputs.pptx` (4 slides), built by `build_decision_models.py`.
Pairs with the rewritten `ai_text_model_projects/review_classification.ipynb`.

## Speaking notes

1. **Decision Models vs Structured Outputs**: a model that picks from your labels can classify faster and cheaper than one that writes JSON.
2. **Write a label, or decide one**: an LLM with structured outputs generates tokens that a schema constrains; you pay for input and output and the label has no reliable confidence. A decision model (a "System One" model such as TypeSafe's Jev, served through OpenRouter's Decisions API) takes state plus typed questions (choice, yes/no probability, score) and returns typed answers with probabilities. Several questions are answered in one call.
3. **Why it matters - calibrated scores become thresholds**: calibrated means answers given at 0.8 are right about 80% of the time, so a threshold is a real error rate. Route: auto-handle above roughly 0.85, spot check in the middle, human review below. Use a decision model for fixed labels at high volume, routing and moderation; use structured outputs for free text, extraction and reasoning in the answer. Limit: a decision model only answers the questions you define.
4. **Handoff**: structured outputs first, then the decision model on the same reviews, then compare speed, cost and confidence.

## Measured numbers (say aloud, do not put on slides)

Probe on 5 October 2026: one Jev call answering three typed questions (sentiment choice, needs-reply probability, severity score) returned in about 0.43 s for about $0.000017. Jev bills input tokens only. Use the notebook's own timing and cost table for the recording.

## Review rounds

- Round 1 (hostile): the decision mock showed "needs_reply: yes", but that question type returns a probability, not yes/no, changed to "needs a reply = 0.94". Space-padded columns misaligned in Arial, rewritten as "label (probability)". "A label with no confidence" was too strong, softened. Added an honest limit (it only answers questions you define). Handoff card labels wrapped unevenly, shortened.
- Round 2 (student): "calibrated" appeared on slide 2 before slide 3 defined it, removed from slide 2. The "Auto" zone label was unclear and cramped, widened the zone (0.85 to 1) and renamed "Auto-handle". Titles alone tell the story.
