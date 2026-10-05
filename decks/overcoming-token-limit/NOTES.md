# Overcoming the Token Limit - recording notes

Deck: `overcoming-token-limit.pptx` (5 slides), built by
`build_overcoming_token_limit.py`.

## Purpose

This lesson explains the context window as a finite working surface and shows a
version-independent workflow for long tasks: split, extract, store, synthesise and
verify.

## Speaking notes

1. **Overcoming the Token Limit**
   - Instructions, history, sources, tool results and the answer all use context.
2. **The context window is a finite working surface**
   - More input is useful only when the model can find and use the relevant signal.
3. **A long task becomes a sequence of bounded passes**
   - Process meaningful sections into one consistent intermediate format.
4. **Staging protects the signal you need later**
   - Keep source references because summaries can lose important nuance.
5. **Live handoff**
   - Split one long source, create structured summaries and verify the synthesis.

## Sources checked on 2026-09-15

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-4.1
- https://developers.openai.com/api/reference/cli/resources/responses/methods/create

## Review rounds

- Round 1, hostile reviewer: removed model-specific token numbers and kept the lesson stable across changing context-window sizes.
- Round 2, student: the Keynote render found one spellcheck underline; UK spelling removed it, and the corrected workflow was visually rechecked.

## Round: visual upgrade (2026-09-28)

- Slide 2: layers + paragraph replaced by two capacity bars (instructions, conversation, source, answer space) against a pink window-limit line. The second bar shows too much source pushing the answer space past the limit ("Cut Off"). One-line caption.
- Slide 3: numbered steps replaced by a pipeline: long source, split into four sections, each extracted into the same fields with a § reference, converging on one final answer checked against sources.
- Slide 4: table replaced by an icon-led comparison (one giant chat vs staged workflow), staged column tinted pink.
- Icons: Lucide (ISC licence), rendered into `assets/` by the build script. Related shapes are grouped. "Synthesize" made "Synthesise" for consistency.
