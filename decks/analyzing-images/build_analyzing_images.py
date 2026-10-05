#!/usr/bin/env python3
"""
"Analyzing Images with ChatGPT" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/analyzing-images/build_analyzing_images.py \
        decks/analyzing-images/analyzing-images.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/analyzing-images/analyzing-images.pptx

Boundary: this deck is about the model *reading* an image you supply. Generating
images is a different lecture, and files-plus-code is `data-analysis`.

The spine is the honest one: it does not see pixels the way you do, it sees a
grid of patches turned into tokens. Everything it is good at, and every way it
fails, falls out of that single fact.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import (  # noqa: E402
    Deck, ACCENT, BODY_FONT, BUBBLE, INK, MUTED, NODE_BG, RULE, SZ_LABEL,
)

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "analyzing-images.pptx")
d = Deck()


# ---------------------------------------------------------------- helpers
def attach(m, w=1.45, h=0.85, label="attached image", n=1, gap=0.14):
    """Draw `n` supplied-image tiles in the user's turn, then advance the cursor.

    `s.image_generator()` shows a prompt producing pictures; this lecture needs
    the reverse - a picture arriving as input - so the tile is a placeholder for
    whatever the student uploaded, never a screenshot.
    """
    x = m._inset()
    for i in range(n):
        tx = x + i * (w + gap)
        m.s.rect(tx, m.cursor, w, h, fill=BUBBLE, rounded=True, radius=0.05)
        m.s.text(tx, m.cursor, w, h,
                 label if n == 1 else f"{label} {i + 1}",
                 size=SZ_LABEL, color=MUTED, align="c", anchor="m")
    m._y += h + 0.10
    return m


def patch_tile(s, x, y, w, h, cols, rows, mark):
    """An image drawn as the grid of patches it is actually cut into.

    `mark` is (col, row, col_span, row_span) - the region of the picture the
    student is actually asking about, outlined in the accent colour.
    """
    s.rect(x, y, w, h, fill=NODE_BG, line=RULE, line_w=0.75)
    cw, ch = w / cols, h / rows
    for i in range(1, cols):
        s.rect(x + i * cw, y, 0.008, h, fill=RULE)
    for j in range(1, rows):
        s.rect(x, y + j * ch, w, 0.008, fill=RULE)
    c, r, cs, rs = mark
    s.rect(x + c * cw, y + r * ch, cs * cw, rs * ch, line=ACCENT, line_w=1.5)


# ---------------------------------------------------------------- open
d.title("Analyzing Images with ChatGPT",
        "How an assistant answers questions about a picture you hand it.")

# ============================================================== WHAT IS IT?
s = d.what("a question about a picture you supply")
m = s.mock(0.40, 1.52, 4.86, 3.58)
attach(m, 1.70, 0.85)
m.user("What is this chart showing, and what stands out?")
with m.bubble():
    m.assistant("Monthly signups, January to December. Growth",
                "is flat until August, then roughly doubles.")
m.composer(pin=False)
s.beside(m, "You attach a picture and ask a question about it. The image is "
            "turned into tokens and placed in the context beside your words, so "
            "what comes back is reasoning about the picture rather than a lookup "
            "of it. That is what people mean by vision.")

s = d.content("What it reads well")
s.table(0.34, 1.52, 9.32, 2.28, [
    ["Ask it to", "What comes back"],
    ["Describe", "what is in the frame, and what is happening"],
    ["Read", "text printed clearly enough to see"],
    ["Interpret", "the shape of a chart, the point of a diagram"],
    ["Compare", "what differs between two pictures"],
    ["Critique", "what is confusing about a layout"],
], col_widths=[1.7, 7.6])
s.caption(0.34, 4.02, 9.32,
          "Every row is a question about meaning, not measurement. Hold on to "
          "that distinction - it predicts almost every case where the answer "
          "comes back wrong.")

# ============================================================== HOW IT WORKS
s = d.how("one reading of the picture, taken before you ask")
s.flow(0.34, 1.52, 9.32,
       [("You attach", "an image and a question"),
        ("It is resized", "to fit a fixed budget"),
        ("It is cut up", "into a grid of patches"),
        ("Each patch", "becomes tokens")],
       h=1.25, accent_last=True)
s.text(0.34, 3.00, 4.40, 0.28, "Why it is resized", size=13, color=INK,
       bold=True, font=BODY_FONT)
s.caption(0.34, 3.42, 4.40,
          "A patch is one small square of the picture, and every model has a "
          "ceiling on how many of them an image may use. A big picture is "
          "scaled down until it fits, and detail that falls below the grid is "
          "not blurred - it is absent.")
s.text(5.26, 3.00, 4.40, 0.28, "What it costs", size=13, color=INK,
       bold=True, font=BODY_FONT)
s.caption(5.26, 3.42, 4.40,
          "Patches become input tokens. They take up the same finite context "
          "as your words, and where you pay per token they are billed like any "
          "other input - a screenshot costs what a long prompt costs.")

s = d.content("Your picture arrives as tokens, not as pixels")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("Tokens from your image", "one fixed reading", True),
                   ("Anything already in the chat", "earlier images included"),
                   ("Your question", "typed just now")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "One stream of tokens", accent=True)
s.caption(6.50, 2.43, 3.16,
          "This is the honest version of \"it can see\". It cannot look again, "
          "zoom in, or go back for a corner it skipped. It gets one reading of "
          "the picture, taken before it knew what you would ask.")

s = d.content("Crop and enlarge what you are asking about")
patch_tile(s, 1.55, 1.52, 2.70, 1.75, 8, 5, (5, 2, 1, 1))
s.arrow(4.67, 2.33, 0.66, 0.14)
patch_tile(s, 5.75, 1.52, 2.70, 1.75, 8, 5, (0.5, 0.5, 7, 4))
s.text(1.55, 3.42, 2.70, 0.28, "The whole screen", size=13, color=INK,
       bold=True, font=BODY_FONT, align="c")
s.text(5.75, 3.42, 2.70, 0.28, "Cropped and enlarged", size=13,
       color=INK, bold=True, font=BODY_FONT, align="c")
s.caption(0.34, 3.86, 9.32,
          "A patch covers a fixed square of the picture, so what matters is how "
          "much of your subject falls inside one. Send the whole screen and the "
          "thing you are asking about sits inside a patch or two; crop to that "
          "region and enlarge it, and the same subject is spread across the "
          "whole grid. That is the cheapest fix for \"it misread the small "
          "text\".")

s = d.content("Where it stops")
s.compare(1.52,
          "Safe to act on", ["What is in the picture",
                             "Printed text at a readable size",
                             "The direction a chart is heading",
                             "Whether two images differ"],
          "Verify before you act", ["Exact counts of anything",
                                    "Small text, or text that is rotated",
                                    "Precisely where things sit",
                                    "Dashed against solid lines",
                                    "Numbers off a dense table"],
          h=2.44)
s.caption(0.34, 4.10, 9.32,
          "Everything on the right is a precision task, and precision is the "
          "first thing a patch grid throws away. It is not carelessness - the "
          "detail was gone before the model read the picture. It never reads "
          "the file name or the metadata either, only the picture itself.")

# ============================================================== WHY IT MATTERS
s = d.why("a specific question beats \"what is this\"")
m = s.mock(0.40, 1.52, 4.86, 3.58)
m.user("Read each bar's label and value into a table.",
       "Write \"unclear\" if a label is not legible.")
with m.bubble():
    m.assistant("Read straight off the axis where I could:")
    m.table([["Bar", "Value"], ["Q1", "1,240"], ["Q2", "unclear"]],
            col_widths=[1.0, 1.0])
m.composer(pin=False)
s.beside(m, "\"What is this?\" gets you a caption. Name what you want read, name "
            "the shape you want it in, and give it a way to say it could not see "
            "something. The reply stops being plausible and starts being "
            "checkable.")

s = d.content("Make it quote before it interprets")
m = s.mock(0.40, 1.52, 4.86, 3.58, generic=True)
m.user("First, list the text you can actually read in the",
       "image, word for word. Mark anything you cannot",
       "read as unclear. Then answer: which region is",
       "below target?")
with m.bubble():
    m.assistant("Read: \"North 112%\", \"South 98%\". The third",
                "row is not legible.")
    m.line("Answer: South, of the two I can read.", highlight=True)
m.composer(pin=False)
s.beside(m, "Quoting first splits one hard job into two easy ones: read, then "
            "reason. You can see what it read, so a wrong answer tells you "
            "whether it misread the picture or misread you - and \"unclear\" "
            "becomes an allowed answer instead of a guess.")

s = d.content("A second image gives it something to compare")
m = s.mock(0.40, 1.52, 4.86, 3.58)
attach(m, 1.70, 0.85, "image", n=2)
m.user("What changed between the first and the second?")
with m.bubble():
    m.assistant("The headline moved above the form, and the",
                "second button is gone.")
m.composer(pin=False)
s.beside(m, "Images arrive in the order you attach them, in one context, so the "
            "second is something the model can hold against the first - a before "
            "and after, frames of a sequence, an example you want matched. Each "
            "one brings its own tokens, so attach the ones that carry the "
            "argument.")

d.two_columns(
    "When to attach a picture",
    ["A screen or scene you cannot easily describe",
     "A chart whose shape you want described",
     "A layout or design you want criticised",
     "Two versions you want compared"],
    ["A spreadsheet you could upload as a file",
     "Anything whose exact numbers must be right",
     "A count you would have to defend",
     "A document whose text you could export"],
    left_heading="Worth attaching",
    right_heading="Send something else",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Attach one image", "ask a deliberately vague question"),
     ("Ask again, specifically", "name the reading, name the format"),
     ("Make it quote first", "then answer from its own list"),
     ("Attach a second", "and ask what changed")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
