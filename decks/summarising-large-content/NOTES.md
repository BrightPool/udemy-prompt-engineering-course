# Summarising Large Content - recording notes

Deck: `summarising-large-content.pptx` (5 slides), built by `build_summarising_large_content.py`.
Pairs with the rewritten `ai_text_model_projects/summarizing_large_documents.ipynb`.

## Purpose

Teach adaptive progressive summarisation with backpressure: count tokens, compare with the model's context window minus a 5% safety margin, make one call when it fits, otherwise split, summarise each chunk, and send the joined summaries round again until they fit. The same code uses a bigger window automatically (fewer chunks, often one call) and backs off safely when the input is too large.

## Speaking notes

1. **Summarising Large Content**: from a page to a whole book without overflowing the context window.
2. **Count the tokens before you send**: a tokeniser (tiktoken for OpenAI models) counts what the model will see. Fits: one call. Too big: split it.
3. **How it works - budget every chunk**: context window, minus a 5% safety margin, minus the instructions, minus room for the answer, equals the chunk budget. Derive it from the model, never hardcode it.
4. **One call when it fits, a loop when it does not**: count, check against the budget, then either one call or split and map; the joined summaries go round again. The last call over the joined summaries is the reduce step. Define backpressure aloud: when input is too large, the pipeline slows down into more, smaller calls instead of failing.
5. **Handoff**: count the book, check the window, summarise adaptively.

Model names and window sizes belong in the notebook and spoken track, not on slides.

## Review rounds

- Round 1 (hostile): slide 4 was titled as a "why" slide but showed mechanism, retitled as a plain content slide with the why in the caption. The "One call" node did not show it is also the reduce step, sub-label changed to "summarise or combine". The loop label overlapped the Split node, moved below the loop line. Bar labels ("Instructions") wrapped, widened the segment. Layer note "the most each call reads" wrapped, shortened. Linter flagged thin accent arrows as a second title rule, thickened them.
- Round 2 (student): "Fits the budget?" was the only label not in Title Case, fixed. "Budget" is defined on slide 3 before it is used on slide 4. "Backpressure" kept off the slides and defined in the spoken track. Smallest text is 12pt.
