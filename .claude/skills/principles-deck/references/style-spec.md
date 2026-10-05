# Style spec

Every value here was extracted from `assets/reference-deck.pptx` ("Give Direction v∞").
Do not invent new colours, fonts or sizes - the point of the skill is that decks made
months apart are indistinguishable.

## Canvas

| | |
|---|---|
| Slide size | 9144000 x 5143500 EMU = **10" x 5.625"** (16:9) |
| Theme | Modern Writer |
| Slide chrome left margin | 0.34" |
| Mock panel left margin | 0.40" |
| Footer band | y = 5.10" and below - keep content out |

## Theme colours

| Role | Hex | Where |
|---|---|---|
| dk1 | `E91D63` | brand pink |
| lt1 | `FFFFFF` | slide background |
| dk2 | `424242` | all body and title text on white |
| lt2 | `999999` | muted text on white |

## Typography

Title and body formatting live on the **master's placeholder shapes**, not on the layouts
and not on the runs. Slides in the source deck carry no explicit `rPr` at all. So: fill
placeholders with text and set nothing else.

| Element | Font | Size | Notes |
|---|---|---|---|
| Title placeholder | Oswald | 30pt | bottom-anchored, `424242` |
| Section divider | Oswald | 30pt | **Title Case**: "What It Is" |
| Body placeholder | Source Code Pro | 18pt | 115% line spacing |
| Slide number (idx 12) | Source Code Pro | 10pt | at (9.27, 5.10) |
| Footer static text | Source Code Pro | 9pt | baked into every layout |
| **Mock UI** | **Arial** | 8.25 - 12pt | set explicitly by `deckkit` |
| Diagram labels | Source Code Pro | 13pt | `SZ_DIAGRAM`, **Title Case** via `title_case()` |
| Short tags under diagrams | Source Code Pro | 12pt | **Title Case**: "Pick Per Task" |
| Table cells | Source Code Pro | 12pt | `SZ_TABLE` |
| Captions | Source Code Pro | 12pt | `SZ_CAPTION` - the floor on white |

**Nothing on the white surface goes below 12pt.** The linter treats it as an error. Inside
a dark mock window the floor is 8pt, because that chrome is meant to read as small UI.

Arial inside the mocks is deliberate: it reads as "a piece of software" against the
Oswald/Source Code Pro slide furniture. Do not unify them.

## Slide-surface palette

Everything outside a mock window. Diagrams and tables live here, not in the dark palette.

| Token | Hex | Used for |
|---|---|---|
| `INK` | `424242` | body and label text on white |
| `SOFT_INK` | `6B6B6B` | captions, sub-labels |
| `RULE` | `D8D8DE` | hairlines, table rules, node outlines |
| `NODE_BG` | `F5F5F7` | diagram node fill |
| `NODE_ACC` | `FBE4EC` | diagram node fill, emphasised |
| `ACCENT` | `E91D63` | numerals, emphasis outlines |
| `ARROW` | `ED1763` | annotation and flow arrows |

`NODE_BG` and `NODE_ACC` are tints derived for the diagram kit; everything else comes
straight from the source deck.

## Tables

Light, editorial, horizontal rules only:

- cells `FFFFFF`, text `INK` at 12pt, Source Code Pro
- header row bold, `424242` rule beneath at 1.25pt
- body rows separated by `D8D8DE` hairlines at 0.75pt
- table style is **No Style, No Grid** (`{2D5ABB26-…}`) so PowerPoint draws no grid of
  its own

Never give a table the dark mock palette. A table is slide content, not a screenshot.

## Mock UI palette

| Token | Hex | Used for |
|---|---|---|
| `PANEL` | `303138` | window body, message rows |
| `HEADER` | `25262C` | title bar - **darker** than the body |
| `BUBBLE` | `3C3D46` | nested response bubble, composer input |
| `HL` | `71334D` | dim-pink pill behind emphasised text |
| `ACCENT` | `E91D63` | step numbers, accents |
| `ARROW` | `ED1763` | annotation arrows |
| `CHIP` | `E4E5EA` | light send button |
| `TEXT` | `F7F7FA` | primary text on dark |
| `MUTED` | `C6C7D0` | role labels, placeholder text, tags |

## Mock UI type scale

| Constant | pt | Used for |
|---|---|---|
| `SZ_APP` | 12.0 | app name in the title bar (bold) |
| `SZ_BODY` | 11.25 | message text |
| `SZ_LABEL` | 8.85 | "You" / "AI" labels, corner tag |
| `SZ_TINY` | 8.25 | fine print |

## Vertical rhythm

| Constant | inches |
|---|---|
| `HEADER_H` | 0.33 |
| `LINE_H` | 0.23 |
| `PAD_X` | 0.16 |
| `GAP` | 0.10 |

## Anatomy of a mock window

Reconstructed from slide 2 of the reference deck, the canonical example (also in
`assets/reference/slide-prompting-chatgpt.png`). Panel at (0.40, 1.56), 4.60 x 3.58.

| Shape | Geometry | Fill | Offset from panel |
|---|---|---|---|
| Panel body | roundRect | `303138` | 0, 0, w, h |
| Title bar | roundRect | `25262C` | 0, 0, w, 0.33 |
| Corner-squaring strip | rect | `25262C` | 0, 0.21, w, 0.12 |
| App name | text, Arial 12 bold | `F7F7FA` | 0.16, 0.09 |
| Corner tag | text, Arial 8.85, right | `C6C7D0` | w - 1.36, 0.11 |
| Role label | text, Arial 8.85 bold | `C6C7D0` | 0.16, flows |
| Message line | text, Arial 11.25 | `F7F7FA` | 0.16, flows |
| Response bubble | roundRect | `3C3D46` | 0.12, flows, w - 0.24 |
| Composer | roundRect | `3C3D46` | 0.16, h - 0.45, w - 0.32, 0.33 |
| Send chip | roundRect | `E4E5EA` | w - 0.46, h - 0.40, 0.23, 0.23 |
| Send glyph "↑" | text, centred | `25262C` | over the chip |

The corner-squaring strip is the trick that makes a rounded title bar sit correctly on a
rounded panel: it covers the bar's lower rounded corners so only the top two stay round.
`deckkit` draws it for you.

## Highlight pills

A `71334D` rounded rect sitting **behind** a line of text, inset 0.05" to the left and
about 0.10" wider than the glyphs. Used to point at the one fragment of a prompt or
response that the slide is about. `deckkit` estimates the width from the string; pass
shorter text if a pill runs long.

Use at most one highlight per mock. Two is not emphasis.

## Composition patterns from the reference deck

| Pattern | Mock box | Body box |
|---|---|---|
| Mock left, copy right | (0.40, 1.56, 4.60, 3.58) | (5.25, 1.46, 4.42, 3.39) |
| Copy left, mock right | (4.43, 0.20, 5.23, 4.91) | (0.34, 1.51, 3.95, 3.39) |
| Full-width message rows | (0.34, 1.56, 9.31, 0.85) stacked | (0.34, 3.43, 9.32, 1.63) |

The full-width pattern - two stacked rows with an arrow between - is how the reference deck
shows a prompt and its response side by side. It is the best layout for "what actually
reaches the model".
