# The three mock patterns

The source deck uses the same three panels over and over. They are built into `deckkit`
as one-call builders so the same idea looks the same in every lecture. **Reach for these
before hand-rolling a mock.**

Reference images sit next to each builder - open them beside your output:

| Pattern | Builder | Reference image | Gallery |
|---|---|---|---|
| Chat demo | `s.chat_demo(...)` | `assets/reference/pattern-chat-demo.png` | slide 2 |
| Prompt example | `s.prompt_example(...)` | `assets/reference/pattern-prompt-example.png` | slide 3 |
| Image generator | `s.image_generator(...)` | `assets/reference/pattern-image-generator.png` | slide 4 |

Rebuild the gallery any time you want to see all three:

```bash
uv run --with python-pptx python scripts/pattern_gallery.py out/patterns.pptx
```

---

## 1. Chat demo

**The product doing one thing.** Labelled `ChatGPT` / `Demonstration` by default. Use it
when the point is *what the tool does*, not how a prompt is built.

```python
s.chat_demo(
    0.40, 1.56, 5.05, 3.49,
    prompt="Can I have 10 product names for a pair of shoes that fit any foot size?",
    results=["1.  FlexiFit", "2.  UniversalSole", ...],   # numbered, two columns
)
```

| Argument | Does |
|---|---|
| `prompt` | the user's turn, wrapped |
| `results` | a numbered multi-column list inside the response bubble |
| `reply` | a single sentence instead of a list |
| `note` | a trailing labelled line, e.g. `("Memory updated", "Writes in British English.")` |
| `highlight` | `"reply"` or `"note"` - puts the pink pill behind that line |
| `composer` | `True` flows an input bar and fits the panel; `False` just fits |
| `generic=True` | switches the window to `AI Assistant` / `Example` |

## 2. Prompt example

**A prompt worth reading in full, and what came back.** Labelled `AI Assistant` /
`Example` by default. Blank lines inside `prompt` are preserved, which is what makes a
multi-part prompt (examples, criteria, steps) legible.

```python
s.prompt_example(
    4.43, 0.20, 5.23, 4.85,          # the source deck's full-height right panel
    prompt="Brainstorm...\n\n## Examples\n...\n\nRate the names 1-5.",
    table=[["Product name", "Catchiness", "Uniqueness"],
           ["iFitShoe", "4", "3"]],
    col_widths=[2.2, 1.2, 1.2],
)
```

This pattern wants a **tall** panel. The source deck runs it full height down the right
of the slide, with the title and copy on the left - that composition is why it can carry
a long prompt at a readable size. It does **not** call `.fit()` by default; pass
`fit=True` for a short prompt.

The table inside is deliberately **dark** - it is mocked product output, not slide
content. The light editorial table is `s.table()`. Do not mix them up: the linter allows
a dark table inside a mock and flags one anywhere else.

## 3. Image generator

**A prompt beside the images it produced.**

```python
s.image_generator(
    0.34, 1.56, 5.90, 3.48,
    prompt="neon pink and blue sneakers, sleek iridescent details, studio lighting",
    negative="soft, misshapen, corners, straps, laces",
    images=["out/shoe1.png", "out/shoe2.png"],   # optional
)
```

Pass file paths in `images` to fill the tiles; leave it empty and the grid draws labelled
placeholders, which is often enough to make the point. Generated illustration is the one
place a bitmap belongs in these decks - see [anti-drift.md](anti-drift.md).

---

## Positioning

All three sit below the layout's dashed divider at y = 1.39", so content starts at
**y = 1.52" or lower**; the linter warns at anything between. The one exception is the
full-height composition in pattern 2, which starts at y = 0.20" and runs past the divider
deliberately, with the title beside it rather than above it.

Keep the start height consistent across a deck. Panels that begin at slightly different
heights from slide to slide read as sloppy even when no single slide looks wrong - the
layout pass in [review-loop.md](review-loop.md) exists to catch exactly that.
