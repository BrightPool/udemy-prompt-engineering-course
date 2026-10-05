# Mock UI recipes

Cookbook for `scripts/deckkit.py`. All coordinates are inches on a 10 x 5.625 canvas.

## Deck and slides

```python
from deckkit import Deck

d = Deck()                                   # opens assets/template.pptx
d.title("Web Search", "One-line definition.")
s = d.what("a retrieval step")               # "What is it? - a retrieval step"
s = d.how("query, fetch, ground")            # "How it works - query, fetch, ground"
s = d.why("answers stop going stale")        # "Why it matters - ..."
s = d.content("Slide title")                 # plain title, same workhorse layout
d.two_columns("Title", ["left", "items"], ["right", "items"],
              left_heading="Do", right_heading="Don't")
d.handoff([("Do this", "note"), ("Then this", "note")], lead="One line.")
d.prompt_template("Prompt Template", "Summarise {document} for {audience}.")
d.save("out/deck.pptx")                      # drops empty placeholders, then writes
```

`d.content()` returns a `Slide`. Its body placeholder is removed at save time unless you
call `.body()`, so a mock-only slide has no stray "Click to add text" box.

## Body copy beside a mock

```python
m = s.mock(0.40, 1.56, 4.60, 3.58)
...
m.composer(pin=False)          # the panel is now shorter than 3.58
s.beside(m, "Copy that sits in whatever space the mock left over.")
```

`beside()` reads the mock's **final** geometry and puts the copy in the larger of the two
side margins, vertically centred against the panel. Use it instead of a hardcoded box:
`.fit()` and `.composer(pin=False)` resize the panel, and a hardcoded box does not follow.

For a full-width block with no visual beside it, `s.body(text)` still works, and
`s.body(text, box=(x, y, w, h))` remains the manual escape hatch.

Both route through the bullet policy: one paragraph renders flush with no glyph and no
hanging indent; two or more keep their bullets.

## A tool window

Window labelling follows a fixed house convention, wired in as defaults:

| | App | Tag | Call |
|---|---|---|---|
| Showing the product | `ChatGPT` | `Demonstration` | `s.mock(...)` |
| Showing a prompt pattern | `AI Assistant` | `Example` | `s.mock(..., generic=True)` |

Turns are always **User**, **AI Assistant**, **System**.

```python
m = s.mock(0.40, 1.56, 4.60, 3.58)     # ChatGPT / Demonstration
m.user("What shipped in the last release?")
with m.bubble():                       # nested lighter response panel
    m.assistant("Three things shipped.", "Answer, with sources.")
m.composer(pin=False)                  # input bar, panel shrinks to fit
```

`.user()`, `.assistant()` and `.system()` write the role label and its lines together.
Use them instead of `.label()` + `.line()` so the labels stay consistent across decks.

Content flows downward from an internal cursor; you never compute a y coordinate.

| Method | Does |
|---|---|
| `.user()` / `.assistant()` / `.system()` | a labelled turn - **prefer these** |
| `.label(text)` | a bare label, for anything not a turn ("Memory updated") |
| `.line(text, highlight=False)` | one non-wrapping line of message text |
| `.para(text)` | wrapped block; estimates its own height |
| `.columns(items, cols=2)` | numbered results in columns |
| `.divider()` | hairline rule |
| `.gap(0.10)` | vertical space |
| `with .bubble():` | wraps the block in a `3C3D46` response panel |
| `.composer(text, pin=True)` | input bar; `pin=False` flows it after the content |
| `.fit(pad=0.16)` | shrink the window to its content |

**Always end with `.fit()` or `.composer(pin=False)`.** A panel sized by hand almost always
trails dead space, which is the most common way these slides look wrong.

## Full-width exchange rows

For "what actually reaches the model" - no window chrome, just stacked rows.

```python
row = s.message_row(0.34, 1.56, 9.31)
row.label("Context assembled for this turn")
row.line("Writes in British English.", highlight=True)

row = s.message_row(0.34, 2.53, 9.31)
row.label("You").line("Draft a one-line product blurb.")

s.arrow(4.60, 2.44, 0.80, 0.10)        # pink arrow between the rows
```

## Mechanism steps

```python
s.steps(0.34, 1.56, 5.60, [
    "You say something durable.",
    "The assistant writes a short fact into the store.",
    "Later conversations load those facts first.",
])
```

Returns the y after the last pill, so you can continue below it. Three to five steps; each
one clause. Pair with a `s.caption()` in the empty column.

## Vector concept art

Draw the concept. These are the reason a principles deck can avoid screenshots without
becoming a wall of prose.

```python
# left-to-right pipeline, with an optional return loop
s.flow(0.34, 1.55, 9.32,
       [("You ask", "a question"), ("It searches", "the web"),
        ("It reads", "results"),   ("It answers", "with sources")],
       h=1.10, accent_last=True, loop="every later turn starts here")

# stacked bands - the best way to draw "what actually reaches the model"
bottom = s.layers(0.34, 1.52, 5.90,
                  [("Retrieved memories", "written weeks ago", True),
                   ("System instructions", "set by the product"),
                   ("Your message", "typed just now")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "One flat context", accent=True)

# two labelled panels - misconception vs reality
s.compare(1.56, "Not this", ["Re-training the model"],
                "This",     ["A short list of facts"])

# numbered pills, and numbered cards
s.steps(0.34, 1.56, 5.60, ["First", "Second", "Third"])
s.cards(0.34, 2.40, 9.32, [("Do this", "note"), ("Then this", "note")])
```

Each `layers` item is `"Label"`, `("Label", "note")` or `("Label", "note", accent)`.
Pass the accent as a flag - there is no magic string prefix.

## Model output as a table

```python
s.table(0.34, 1.58, 9.32, 1.90, [
    ["", "Without", "With"],
    ["Repeat setup", "Every time", "Once"],
    ["Failure mode", "Forgetful", "Confidently stale"],
], col_widths=[1.9, 3.6, 3.6])
```

Light and editorial: white cells, 12pt ink text, horizontal rules only, row 0 bold.
`col_widths` are relative. **Never** give a table the dark mock palette.

## Code snippets - always via Carbon

**Never set code as flat monospace text.** Syntax highlighting is what makes a
snippet readable at a glance on a projector. Every code snippet in every deck goes
through `scripts/code_image.py`, so they all share one theme, font and proportion.

One-off setup: `npm install -g carbon-now-cli`

```python
from code_image import code_image

png, ratio = code_image('''
import tiktoken
enc = tiktoken.get_encoding("o200k_base")
''', out_dir=ASSETS, name="tiktoken")
picture(s, png, 0.34, 1.66, 5.60, ratio=ratio)
```

House settings are fixed in `code_image.py`: `one-dark` theme, **Source Code Pro**
(the deck's own body font), transparent ground, no window controls, no traffic
lights, no shadow, 3x export. Renders are cached by a hash of the code, so
rebuilding a deck is free unless the snippet changed.

## Exercise slides

When the lecture stops explaining and asks the student to *do* something, say so
with the same header every time:

```python
s = d.exercise("See a sentence become tokens", minutes=1)
# content starts at y = 1.46
```

A full-width accent band carries a letterspaced eyebrow (`EXERCISE · 1 MINUTE`)
above the title in white Oswald. Built on `BLANK`, so no dashed divider and no
bulleted placeholder. Students learn the band means "your turn".

## Captions and annotations

```python
s.caption(6.20, 1.70, 3.40, "Note on the white area. Height is measured\nfrom the text.")
s.arrow(4.73, 2.39, 0.95, 0.12, direction="right")
```

`caption()` sizes its own height from the copy, so it never claims unused space or trips
the footer band. Pass `h=` only to override.

`caption()` is for the slide's white space and uses Source Code Pro. Text inside a mock
uses Arial - do not mix them up.

## Escape hatch

```python
s.rect(x, y, w, h, fill="303138", rounded=True)
s.text(x, y, w, h, "text", size=11.25, color="F7F7FA", font="Arial", align="c")
s.raw            # the underlying python-pptx Slide
```

Use tokens from `deckkit` (`PANEL`, `BUBBLE`, `TEXT`, ...) rather than typing hex, so a
future palette change stays a one-line edit.

## Gotchas

- `.line()` does not wrap. Use `.para()` for anything longer than the panel width.
- Highlight pill widths are **estimated** from character count. If one looks long, shorten
  the string rather than nudging geometry.
- Keep everything above y = 5.10", where the footer and slide number sit.
- `.bubble()` inserts its background behind the text added inside the block, so open the
  context manager *before* writing the lines it should contain.
- Mock panels start at x = 0.40, slide chrome at x = 0.34. That 0.06" difference is in the
  source deck and is intentional.
- Repositioning a placeholder: use `s.move_ph(idx, top=…)`, never `ph.top = …`. A cloned
  placeholder has no geometry of its own, so setting one value creates an xfrm with x=0
  and width=0, and the text vanishes.
- A column with one item gets its bullet suppressed automatically. If you build a list
  some other way, do the same - a single point never wears a bullet.
