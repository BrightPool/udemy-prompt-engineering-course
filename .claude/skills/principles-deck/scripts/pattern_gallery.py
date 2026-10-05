#!/usr/bin/env python3
"""
The three canonical mock panels, rebuilt as vector shapes.

    uv run --with python-pptx python scripts/pattern_gallery.py out/patterns.pptx

Open this beside assets/reference/pattern-*.png to see what each builder produces.
Reach for these before hand-rolling a mock - the same idea should look the same in
every lecture.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from code_image import code_image  # noqa: E402
from deckkit import SOFT_INK, SZ_CAPTION, BODY_FONT, Deck  # noqa: E402
from pptx.util import Inches  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "generated"

out = Path(sys.argv[1] if len(sys.argv) > 1 else "out/patterns.pptx")
d = Deck()

d.title("Mock patterns", "The three panels every principles deck is built from.")

# -- 1. chat demo: a turn with a listed answer -----------------------------
s = d.content("Chat demo")
s.chat_demo(
    0.40, 1.56, 5.05, 3.49,
    prompt="Can I have 10 product names for a pair of shoes that can fit any foot size?",
    results=["1.  FlexiFit", "2.  UniversalSole", "3.  SizeMaster", "4.  PerfectFit",
             "5.  AdaptiStep", "6.  OneSizeStride", "7.  OmniFit", "8.  VersaSole",
             "9.  InfiniteStep", "10.  AllFitFootwear"],
)
s.caption(5.85, 1.62, 3.80,
          "s.chat_demo(...) - the product doing one thing. Defaults to "
          "ChatGPT / Demonstration. Use it whenever the point is what the tool "
          "does, not how a prompt is built.")

# -- 2. prompt example: a structured prompt and its tabular answer ----------
s = d.content("Prompt example")
s.prompt_example(
    4.43, 0.20, 5.23, 4.85,        # the source deck's full-height right panel
    prompt=(
        "Brainstorm a list of product names for a shoe that fits any foot size, "
        "in the style of Steve Jobs. Format as a markdown table.\n"
        "\n"
        "## Examples\n"
        "Product description: A refrigerator that dispenses beer\n"
        "Product names: iBarFridge, iFridgeBeer, iDrinkBeerFridge\n"
        "\n"
        "Rate the product names on catchiness, uniqueness and simplicity, 1-5."
    ),
    table=[["Product name", "Catchiness", "Uniqueness"],
           ["iFitShoe", "4", "3"],
           ["iAdapt", "3", "4"],
           ["iUniversalStep", "2", "5"]],
    col_widths=[2.2, 1.2, 1.2],
)
s.caption(0.34, 1.62, 3.85,
          "s.prompt_example(...) - a prompt worth reading in full, and what came "
          "back. Defaults to AI Assistant / Example. Blank lines in the prompt "
          "are preserved, which is what makes a multi-part prompt legible.\n\n"
          "This is the source deck's own composition: title and copy left, a "
          "full-height panel right.")

# -- 3. image generator: a prompt beside what it produced ------------------
s = d.content("Image generator")
s.image_generator(
    0.34, 1.56, 5.90, 3.48,
    prompt="neon pink and blue sneakers, sleek iridescent details, product "
           "photography, studio lighting, 35mm, dslr",
    negative="soft, misshapen, corners, straps, laces",
)
s.caption(6.50, 1.62, 3.16,
          "s.image_generator(...) - pass image paths to fill the tiles, or leave "
          "them empty to show the shape of the idea. Generated art is the one "
          "place a bitmap belongs.")

# -- 4. the exercise banner -----------------------------------------------
s = d.exercise("Rebuild this gallery yourself", minutes=2)
s.steps(0.34, 1.16, 5.20, [
    "Run scripts/pattern_gallery.py.",
    "Open the result beside assets/reference/pattern-*.png.",
    "Change one mock and rebuild.",
    "Run check_deck.py until it is clean.",
], h=0.66, gap=0.12)
s.caption(5.90, 1.16, 3.76,
          "d.exercise(title, minutes=n) - a 0.76\" band, title left, drawn clock "
          "and timing right. Built on BLANK, so no dashed divider and no bulleted "
          "placeholder. Use it every time the lecture asks the student to do "
          "something; the repetition is the point.")

# -- 5. code, via Carbon ---------------------------------------------------
s = d.content("Code snippets")
try:
    _png, _ratio = code_image("""
from deckkit import Deck

d = Deck()
s = d.what("a chunk of characters, not a word")
d.save("out/deck.pptx")
""", ASSETS, "gallery-snippet")
    _b = s.raw.shapes.add_picture(str(_png), Inches(0.34), Inches(1.60),
                                  Inches(5.40), Inches(5.40 / _ratio))
    _bottom = 1.60 + 5.40 / _ratio
except Exception as exc:                     # Carbon CLI not installed
    s.rect(0.34, 1.60, 5.40, 1.40, fill="F5F5F7", rounded=True, line="D8D8DE")
    s.text(0.54, 1.60, 5.00, 1.40,
           f"Carbon CLI unavailable: {exc}\n\nnpm install -g carbon-now-cli",
           size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT, anchor="m")
    _bottom = 3.00
s.caption(6.10, 1.60, 3.56,
          "code_image() wraps the Carbon CLI with the house theme - one-dark, "
          "Source Code Pro, transparent ground, no window chrome, 3x export - and "
          "caches by a hash of the code. Never set code as flat monospace text; "
          "highlighting is what makes it readable from the back of a room.")

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
