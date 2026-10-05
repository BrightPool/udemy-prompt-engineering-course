# Iterating on a deck

The build script is the source of truth, but you do not have to get it right in one pass.
Iterate. Build, look, adjust, rebuild - the whole cycle is seconds.

## The loop

```bash
uv run --with python-pptx python my_deck.py            out/deck.pptx
uv run --with python-pptx python scripts/check_deck.py out/deck.pptx
open out/deck.pptx        # or leave it open; PowerPoint reloads on focus
```

Change the script, re-run, look again. Because the deck is regenerated from scratch every
time, there is no state to get out of sync and no half-edited file to clean up.

**Always edit the script, never the .pptx.** A hand-edit in PowerPoint is lost the next
time anyone runs the build, and it is invisible to the linter and to review.

## Reading a deck you did not just build

To inspect an existing deck - a re-film in progress, or one Mike sent over - dump its
structure rather than opening it:

```python
from pptx import Presentation
from pptx.util import Emu

p = Presentation("out/deck.pptx")
for i, s in enumerate(p.slides, 1):
    print(i, s.slide_layout.name)
    for sh in s.shapes:
        pos = "inherit" if sh.left is None else f"{Emu(sh.left).inches:.2f},{Emu(sh.top).inches:.2f}"
        txt = sh.text_frame.text[:60].replace("\n", " / ") if sh.has_text_frame else ""
        print(f"    ({pos}) {txt!r}")
```

That, plus `check_deck.py`, tells you almost everything without a rendering step.

## Seeing the slides

There is no reliable headless renderer here, so use one of these:

- **Open it.** Fastest. PowerPoint and Keynote both reload the file when the window
  regains focus, so you can keep it open across rebuilds.
- **LibreOffice**, if installed, converts to PNG for a quick look:
  ```bash
  soffice --headless --convert-to pdf --outdir out out/deck.pptx
  ```
- **Trust the linter for geometry.** It knows the footer band, the type floor, overlaps,
  dead space and bullet policy. It does not know whether a slide is worth keeping - that
  is the review's job.

## Tightening a slide that looks wrong

| Symptom | Fix |
|---|---|
| Panel trails empty space | `m.fit()` or `m.composer(pin=False)` |
| Content floats high, footer band empty | enlarge the visual, or add the missing substance |
| Caption looks tiny | it is - the floor is 12pt on white |
| Text spills its box | shorten it, or use `.para()` instead of `.line()` |
| A lone bullet | one point is a sentence; the policy suppresses it automatically |
| Two dividers under a title | drop your accent rule, or build the slide on `BLANK` |
| Columns collapse to the left edge | use `s.move_ph()`, never `ph.top = ...` |
| Copy beside a mock is misaligned | use `s.beside(mock, text)`; stop hardcoding the box |
| Copy has a ragged hanging indent | the bullet's `marL`/`indent` survived - `_bullet_policy` clears both |

## Measure, do not hardcode

Anything whose size depends on content should compute it. `beside()` derives its box from
the mock's real geometry, `caption()` measures its own height, `mock.fit()` shrinks the
panel to what was written into it. Hardcoded coordinates are fine for a fixed frame - the
0.34" margin, the footer line - but the moment a number depends on copy or on a visual
that can resize, derive it. Hardcoded numbers are the thing that silently rots.

## Changing the house style

Tokens live at the top of `scripts/deckkit.py`. Change them there and every future deck
follows. Do not hardcode a hex value in a build script - that is how two decks made a
month apart stop matching.

## When to stop

When the linter is clean, both review rounds are done, and reading only the slide titles
top to bottom tells the whole story. Not before.
