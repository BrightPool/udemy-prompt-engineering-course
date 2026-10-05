---
name: principles-deck
description: "Build the principles half of a course re-film as a PowerPoint, in the Prompt Engineering Bootcamp house style (Oswald / Source Code Pro / Modern Writer theme), with tool UIs drawn as native vector mocks and concepts drawn as vector diagrams instead of screenshots, so slides never drift when a vendor redesigns. Includes a layout linter and a mandatory two-round adversarial review. Covers what-it-is / how-it-works / why-it-matters decks for features like memory, custom instructions, web search, projects, canvas, connectors. MANDATORY TRIGGERS: principles deck, principles of, re-film, refilm, gslide re-film, course slides, bootcamp slides, what it is how it works why it matters, mock UI slide, mocked UI, avoid screenshots, teach the principles of."
---

# Principles Deck

Builds the **first half** of a course video: the durable, conceptual explanation of a
feature. The second half - the instructor demoing the real tool - is filmed separately.

The whole point is **anti-drift**. Vendors redesign constantly; a deck full of 2026
screenshots is dead by 2027. Principles do not expire, so this skill teaches principles
over schematic vector mocks and diagrams.

Read [references/anti-drift.md](references/anti-drift.md) before writing copy.

## Workflow

1. **Write the arc first.** Three phases: what is it, how it works, why it matters.
   They ride on slide titles - there are no divider slides. See
   [references/deck-structure.md](references/deck-structure.md).
2. **Copy the template.** `Deck()` opens `assets/template.pptx` - all 22 layouts, the
   theme and the footer, zero slides. Never build a presentation from scratch.
3. **Write a build script** with `scripts/deckkit.py`. Start from `scripts/example_deck.py`.
4. **Build and lint:**
   ```bash
   uv run --with python-pptx python your_deck.py    out/web-search.pptx
   uv run --with python-pptx python scripts/check_deck.py out/web-search.pptx
   ```
   The linter must exit clean. ERRORs are never acceptable; WARNings need a reason.
5. **Iterate.** Build, look, adjust, rebuild - the cycle is seconds and the deck is
   regenerated from scratch each time, so there is no state to desync. Always edit the
   build script, never the .pptx. See [references/iterating.md](references/iterating.md).
6. **Run two rounds of adversarial review.** Not optional - see
   [references/review-loop.md](references/review-loop.md). Rebuild and re-lint after each
   round, and say what each round found.

## The house style, in one table

Slide chrome inherits from the template master. **Never set a font on a title or body
placeholder** - inheritance is what keeps every deck identical.

| Element | Spec | Set by |
|---|---|---|
| Slide | 10" x 5.625" (16:9) | template |
| Title | Oswald 30pt, `424242`, bottom-anchored | inherited |
| Body | Source Code Pro 18pt, 115% line spacing | inherited |
| Footer | "The Complete Prompt Engineering for AI Bootcamp", 9pt | layout |
| Mock UI type | **Arial**, 8.25-12pt | `deckkit` |
| Diagrams, tables, captions | Source Code Pro, **12pt minimum** | `deckkit` |
| Accent | `E91D63` pink | `deckkit` |

Full tokens and geometry: [references/style-spec.md](references/style-spec.md).

## Building slides

```python
from deckkit import Deck

d = Deck()
d.title("Web Search", "How an assistant answers from pages it fetched a moment ago.")

s = d.what("a retrieval step before the answer")   # "What is it? - a retrieval..."
m = s.mock(0.40, 1.56, 4.60, 3.58)            # ChatGPT / Demonstration
m.user("What shipped in the last release?")
with m.bubble():
    m.assistant("Three things shipped.", "Answer, with sources.")
m.composer(pin=False)
# copy placed from the mock's FINAL size - never hardcode a box beside a mock
s.beside(m, "The model does not know today's news. It issues a query, reads "
            "results, and writes an answer grounded in them.")

s = d.how("query, fetch, ground")
s.flow(0.34, 1.55, 9.32, [("You ask", "a question"), ("It searches", "the web"),
                          ("It reads", "the results"), ("It answers", "with sources")],
       h=1.10, accent_last=True)

d.handoff([("Turn search on", "and find the control"),
           ("Ask a live question", "watch it fetch"),
           ("Check the sources", "click one through")],
          lead="That is the principle. Now we do it live in the tool.")
d.save("out/web-search.pptx")
```

Every component: [references/mock-ui-recipes.md](references/mock-ui-recipes.md).

## Slide types

| Call | Use for |
|---|---|
| `d.title(t, sub)` | opener |
| `d.what(t)` / `d.how(t)` / `d.why(t)` | opens a phase: "What is it? - <point>" |
| `d.content(t)` | workhorse: copy + mock or diagram |
| `d.two_columns(t, l, r, left_heading=…, right_heading=…)` | do / don't |
| `d.prompt_template(t, b)` | full-width monospace prompt block |
| `d.exercise(t, minutes=n)` | a hands-on slide, with the standard exercise banner |
| `d.handoff(items, lead=…)` | the closer: a full-page "Let's see it in action" |

There is deliberately **no large-quote slide and no section divider**. A slide that
carries only a sentence, or only announces "What is it?", is fluff. The phase goes in the
title of the slide that answers it, so every slide does work.

**Title Case for labels, sentence case for sentences.** James prefers Title Case wherever
text is a label rather than a sentence: slide titles, card and node headings, the short
tags under a diagram ("Pick Per Task", "Most of This Section", "Adversarial Review"),
table header cells, and handoff cards including their sub-labels ("Each Lecture Is One
Idea"). `cards()`, `node()`, `flow()`, `layers()` and `compare()` titles apply this
automatically, so write labels naturally. Anywhere else, wrap the label in `title_case()`
rather than typing the capitals, so small words and `/commands` stay correct. Full
sentences (captions, body copy, anything ending in a full stop, mock UI and prompt text)
stay in sentence case.

**Bullets mark a list.** A single point is a sentence and gets no glyph - `deckkit`
suppresses the bullet *and its hanging indent*, so the copy sits flush. Bullets survive
only where there are two or more points.

**Do not hardcode a box beside a mock.** Use `s.beside(mock, text)`: it measures the
mock's final geometry, so the copy follows when `.fit()` or `.composer(pin=False)`
changes the panel's size. Captions measure their own height for the same reason.

**Never two dividers under one title.** Most layouts already draw a dashed rule beneath
the title, so do not add an accent rule as well. The full-page closer sidesteps this by
building on `BLANK`, which carries neither the dash nor a bulleted body placeholder.

## Mock UI conventions

Three canonical panels are built in as one-call builders. **Use them before hand-rolling
a mock** - see [references/mock-patterns.md](references/mock-patterns.md), with reference
images in `assets/reference/pattern-*.png`:

| Builder | Panel |
|---|---|
| `s.chat_demo(...)` | a chat turn with a listed answer (ChatGPT / Demonstration) |
| `s.prompt_example(...)` | a long structured prompt and its tabular answer |
| `s.image_generator(...)` | a prompt beside the images it produced |

`scripts/pattern_gallery.py` renders all three side by side.

Always label the window and the turns. Defaults are wired in, so use them:

| | App | Tag | Turn labels |
|---|---|---|---|
| Showing the product | `ChatGPT` | `Demonstration` | User / AI Assistant / System |
| Showing a prompt pattern | `AI Assistant` | `Example` | User / AI Assistant / System |

`s.mock(...)` gives you the first; `s.mock(..., generic=True)` the second. Use
`m.user()`, `m.assistant()` and `m.system()` rather than hand-writing labels.

## Code snippets and exercises

Two house standards. Both are built in; do not hand-roll either.

**Code always goes through Carbon.** Never set code as flat monospace text on a
rectangle - syntax highlighting is what makes a snippet readable at a glance on a
projector. `scripts/code_image.py` wraps the Carbon CLI with fixed house settings
(one-dark, Source Code Pro, transparent ground, no window chrome, no shadow, 3x
export) and caches renders by a hash of the code, so rebuilds are free.

```bash
npm install -g carbon-now-cli      # one-off, per machine
```

```python
from code_image import code_image
png, ratio = code_image(snippet, out_dir=ASSETS, name="tiktoken")
picture(s, png, 0.34, 1.66, 5.60, ratio=ratio)   # see mock-ui-recipes for picture()
```

**Exercises always use the same banner.** When the lecture stops explaining and
asks the student to do something, say so identically every time:

```python
s = d.exercise("See a sentence become tokens", minutes=1)
# content starts at y = 1.10
```

A 0.76" accent band: title left in white Oswald, a drawn clock and
`EXERCISE · 1 MINUTE` right, tracked rather than space-padded. Built on `BLANK`,
so no dashed divider and no bulleted placeholder. Students learn the pink band
means "your turn".

## Vector art

Concepts get **drawn**, not described. Reach for these before writing another paragraph:

| Call | Draws |
|---|---|
| `s.flow(...)` | left-to-right pipeline, optional return loop |
| `s.layers(...)` | stacked bands - what reaches the model |
| `s.steps(...)` | numbered mechanism pills |
| `s.compare(...)` | two labelled panels, before/after |
| `s.cards(...)` | numbered cards across the width |
| `s.node()`, `s.arrow()` | build anything else |

Tables are **light**: white cells, ink text, horizontal rules only. Never the dark mock
palette - a table is slide content, not a screenshot.

## QA before filming

`check_deck.py` covers the mechanical half of this list. Run it; do not eyeball it.

- [ ] Linter exits clean.
- [ ] Two rounds of adversarial review done, and what they found is written down.
- [ ] Titles Oswald, body Source Code Pro, no font set in code.
- [ ] Mock UI text is Arial; nothing on the white surface below 12pt.
- [ ] No screenshot, logo, version number or menu path anywhere.
- [ ] Every mock fits its content (`.fit()` or `.composer(pin=False)`).
- [ ] Tables are light. No dark tables.
- [ ] Code is a Carbon image, never flat monospace text.
- [ ] Exercises use `d.exercise(...)`, not a hand-built header.
- [ ] No single point wearing a bullet; bullets only where there are 2+ points.
- [ ] No accent rule competing with a layout's dashed divider.
- [ ] Nothing crosses y = 5.10".
- [ ] Copy beside a mock uses `s.beside()`, not a hardcoded box.
- [ ] No divider slides; the phase is in the title.
- [ ] Mocks use a canonical builder where one fits.
- [ ] Content starts at y = 1.52" or below, clear of the dashed divider.
- [ ] Deck ends on the `handoff` slide.
