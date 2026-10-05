# principles-deck

A Claude Code skill for building the **principles half** of a Prompt Engineering Bootcamp
re-film: a PowerPoint that teaches what a feature is, how it works and why it matters,
with tool UIs drawn as native vector mocks instead of screenshots.

The instructor demo of the real product is filmed separately. Keeping the two apart is the
point: when a vendor redesigns, only the demo needs re-filming, never the deck.

## Where it lives

This skill is checked into the course repo at
`.claude/skills/principles-deck/`, assets included. Anyone who clones
`udemy-prompt-engineering-course` gets it automatically - start a Claude Code session in
the repo root and it is available, no install step.

Ask for it by name, or just say what you want:

> Build a principles deck on ChatGPT custom instructions.

### Using it outside the repo

If you'd rather have it on every project, unzip the shared archive into your personal
skills directory instead:

```bash
unzip principles-deck.zip -d ~/.claude/skills/
```

Keep one copy or the other. Installing it globally *and* working inside the repo gives two
skills with the same name.

## Requirements

Code snippets need the Carbon CLI once per machine:

```bash
npm install -g carbon-now-cli
```


`python-pptx`, pulled on demand - nothing to install globally:

```bash
uv run --with python-pptx python scripts/example_deck.py out/memory.pptx
```

Fonts (Oswald, Source Code Pro) only matter on the machine that *opens* the deck, not the
one that builds it. Both are free from Google Fonts. Without them PowerPoint substitutes
and the deck looks off - worth installing once.

## What's inside

```
principles-deck/
  SKILL.md                      how to build a deck; read this first
  references/
    anti-drift.md               why mocks instead of screenshots - read before writing copy
    deck-structure.md           the what / how / why arc and slide budget
    style-spec.md               every colour, font, size and coordinate
    mock-ui-recipes.md          deckkit cookbook: mocks, diagrams, tables
    mock-patterns.md            the three canonical panels and their builders
    review-loop.md              the mandatory two-round adversarial review
    iterating.md                the build-look-adjust loop, and reading an existing deck
  assets/
    template.pptx               clean build target: 22 layouts, theme, footer, no slides
    reference-deck.pptx         the original "Give Direction" deck, 16 finished slides
    reference/pattern-*.png     the three canonical mock panels
    reference/slide-*.png       two finished slides in the house style
  scripts/
    deckkit.py                  the mock UI, diagram and deck library
    check_deck.py               layout linter: spacing, sizing, overlap, dead space
    code_image.py               syntax-highlighted code via the Carbon CLI
    example_deck.py             a complete worked deck on "Memory"
    pattern_gallery.py          the three mock patterns, rebuilt as vector shapes
```

## Quick start

```bash
cd .claude/skills/principles-deck
uv run --with python-pptx python scripts/example_deck.py out/memory.pptx
uv run --with python-pptx python scripts/check_deck.py  out/memory.pptx
open out/memory.pptx
```

Then copy `scripts/example_deck.py` and rewrite it for your concept.

Two things are not optional: the linter must exit clean, and every deck goes through the
two-round adversarial review in `references/review-loop.md`. The linter catches geometry;
the review catches slop, padding and drift, which is the failure mode that actually
costs a re-film.

## Extending it

The design tokens all live at the top of `scripts/deckkit.py`, lifted from the reference
deck. If the house style ever changes, change them there and every future deck follows.

If you add a mock component, add it to `references/mock-ui-recipes.md` in the same pass -
the reference files are what the model reads, so an undocumented component effectively
does not exist.
