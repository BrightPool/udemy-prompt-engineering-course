#!/usr/bin/env python3
"""
"Prompt Testing in a Spreadsheet" - the principles half of the re-film.

Run:
    uv run --with python-pptx python \
        decks/gsheets-prompt-testing/build_gsheets_prompt_testing.py \
        decks/gsheets-prompt-testing/gsheets-prompt-testing.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/gsheets-prompt-testing/gsheets-prompt-testing.pptx

Arc: a prompt test is a grid, one row per run (what) - the template becomes a
formatted prompt, the answer comes back into a cell, and every row gets the same
score (how) - so a preference becomes evidence somebody else can check, right up
to the point where the sheet runs out of road (why).

Companion lecture "A/B Testing" teaches the method - one change at a time,
criteria fixed before you look. This deck teaches the instrument.

No screenshots, no menu paths, no add-on or formula names, no prices. The current
mechanisms and rates are in NOTES.md for the instructor to say aloud.

Visual upgrade (2026-09-28): drawn sheet, dot plots for spread, icon flows and
meters instead of paragraphs. Icons are Lucide (ISC licence), rendered into
assets/ as icon-<name>-<p|i|g>.png (pink, ink, grey).
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402
from deckkit import (  # noqa: E402
    ACCENT, BODY_FONT, INK, NODE_ACC, NODE_BG, RULE, SOFT_INK, SZ_CAPTION,
    SZ_DIAGRAM, Deck, title_case, _rgb,
)

out = Path(sys.argv[1] if len(sys.argv) > 1
           else "decks/gsheets-prompt-testing/gsheets-prompt-testing.pptx")
ASSETS = Path(__file__).resolve().parent / "assets"

X, W = 0.34, 9.32
TOP = 1.56          # every visual starts here, clear of the dashed divider
LINE = 12 * 1.2 / 72

# Ten runs of the same prompt, and ten of the same prompt with one edit. The
# numbers are illustrative of the *shape* of a real result - a few per cent
# between the means, ranges that overlap almost completely - not a finding about
# any particular technique.
CONTROL = [1120, 980, 1240, 1050, 890, 1310, 1020, 960, 1180, 1100]
VARIANT = [1190, 1040, 1330, 990, 1420, 1080, 1150, 930, 1260, 1210]


def mean(v):
    return round(sum(v) / len(v))


# ------------------------------------------------------------------ helpers
def group(s, first, name):
    """Group every shape added since index `first`, so it moves as one unit."""
    shapes = s.raw.shapes
    g = shapes.add_group_shape(list(shapes)[first:])
    g.name = name
    return g


def icon(s, name, x, y, size, tone="p"):
    s.raw.shapes.add_picture(str(ASSETS / f"icon-{name}-{tone}.png"),
                             Inches(x), Inches(y), Inches(size), Inches(size))


def badge(s, name, x, y, d=0.44, accent=True):
    """Round icon badge: pink on tint when accented, ink on grey otherwise."""
    dot = s.raw.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y),
                                 Inches(d), Inches(d))
    dot.fill.solid()
    dot.fill.fore_color.rgb = _rgb(NODE_ACC if accent else NODE_BG)
    dot.line.color.rgb = _rgb(ACCENT if accent else RULE)
    dot.line.width = Pt(1.0)
    dot.shadow.inherit = False
    g = d * 0.58
    icon(s, name, x + (d - g) / 2, y + (d - g) / 2, g, "p" if accent else "i")


def oval(s, x, y, d, fill, line=None):
    o = s.raw.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y),
                               Inches(d), Inches(d))
    o.fill.solid()
    o.fill.fore_color.rgb = _rgb(fill)
    if line:
        o.line.color.rgb = _rgb(line)
        o.line.width = Pt(1.0)
    else:
        o.line.fill.background()
    o.shadow.inherit = False
    return o


def code(s, x, y, w, h, lines):
    """Monospace lines, each (text, colour, bold). Prompt text, not a label."""
    box = s.raw.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for i, (text, colour, bold) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.0
        r = p.add_run()
        r.text = text
        r.font.name = BODY_FONT
        r.font.size = Pt(12)
        r.font.bold = bold
        r.font.color.rgb = _rgb(colour)
    return box


def note(s, name, x, y, w, head, sub):
    """A pink call-out: icon badge, bold head, one soft line under it."""
    first = len(s.raw.shapes)
    s.rect(x, y, w, 0.70, fill=NODE_ACC, rounded=True, radius=0.06, line=ACCENT,
           line_w=0.75)
    badge(s, name, x + 0.16, y + 0.13, d=0.44)
    s.text(x + 0.76, y + 0.10, w - 0.90, 0.28, title_case(head), size=14,
           color=INK, bold=True, font=BODY_FONT)
    s.text(x + 0.76, y + 0.38, w - 0.90, 0.26, sub, size=SZ_CAPTION,
           color=SOFT_INK, font=BODY_FONT)
    group(s, first, head)


class Axis:
    """A shared word-count axis for the dot plots."""
    LO, HI = 850, 1450

    def __init__(self, s, x0, x1, y):
        self.s, self.x0, self.x1, self.y = s, x0, x1, y
        s.rect(x0, y, x1 - x0, 0.012, fill=SOFT_INK)
        for v in range(900, 1450, 100):
            tx = self.at(v)
            s.rect(tx - 0.006, y, 0.012, 0.08, fill=SOFT_INK)
            s.text(tx - 0.40, y + 0.10, 0.80, 0.24, f"{v:,}", size=SZ_CAPTION,
                   color=SOFT_INK, font=BODY_FONT, align="c")

    def at(self, v):
        return self.x0 + (v - self.LO) / (self.HI - self.LO) * (self.x1 - self.x0)

    def strip(self, y, values, colour, fill, band_fill):
        """Range band, one dot per run, and a mean tick."""
        s, dd = self.s, 0.20
        lo, hi = self.at(min(values)), self.at(max(values))
        s.rect(lo - dd / 2, y - 0.04, hi - lo + dd, dd + 0.08, fill=band_fill,
               rounded=True, radius=0.12)
        for v in values:
            oval(s, self.at(v) - dd / 2, y, dd, fill, line=colour)
        m = self.at(mean(values))
        s.rect(m - 0.015, y - 0.14, 0.03, dd + 0.28, fill=colour)
        return m


d = Deck()

# ---------------------------------------------------------------- 1 open
d.title("Prompt Testing in a Spreadsheet",
        "Turn a hunch about a prompt into a number, using a grid instead of code.")

# ============================================================== 2 WHAT IS IT?
# A drawn sheet, with the three columns that make it an eval called out.
s = d.what("a grid where every row is one run")
cols = [("", 0.36), ("Run", 0.55), ("Version", 1.25), ("Prompt Sent", 3.05),
        ("Answer Saved", 3.06), ("Words", 1.05)]
data = [
    ["1", "Control", "Blog post on time blocking", "Time blocking is a way…", "1,120"],
    ["2", "Control", "Blog post on time blocking", "Most advice about time…", "980"],
    ["3", "Variation", "…plus: at least 2,000 words", "Blocking your calendar…", "1,190"],
    ["4", "Variation", "…plus: at least 2,000 words", "Time blocking asks you…", "1,420"],
]
letters, rh, lh = "ABCDE", 0.34, 0.24
first = len(s.raw.shapes)
cx = X
for ci, (_, cw) in enumerate(cols):
    # the letter strip, like any spreadsheet
    s.rect(cx, TOP, cw, lh, fill="ECECF0", line=RULE, line_w=0.5)
    if ci:
        s.text(cx, TOP, cw, lh, letters[ci - 1], size=SZ_CAPTION, color=SOFT_INK,
               font=BODY_FONT, align="c", anchor="m")
    cx += cw
for ri in range(len(data) + 1):
    y = TOP + lh + ri * rh
    cx = X
    for ci, (head, cw) in enumerate(cols):
        hot = ci == 5 and ri > 0                 # the score column
        tint = ci == 2 and ri > 0                # the version column
        fill = "ECECF0" if ci == 0 else (NODE_ACC if hot else ("F5F5F7" if tint else "FFFFFF"))
        s.rect(cx, y, cw, rh, fill=fill, line=RULE, line_w=0.5)
        text = str(ri) if ci == 0 and ri else (head if ri == 0 else data[ri - 1][ci - 1] if ci else "")
        if text:
            s.text(cx + 0.08, y, cw - 0.12, rh, text, size=SZ_CAPTION,
                   color=ACCENT if hot else (SOFT_INK if ci == 0 else INK),
                   bold=(ri == 0 or hot), font=BODY_FONT, anchor="m",
                   align="c" if ci in (0, 1, 5) else "l", wrap=False)
        cx += cw
group(s, first, "Sheet")
sheet_bottom = TOP + lh + (len(data) + 1) * rh
# Call-outs under the three columns that matter.
callouts = [("rows-3", X, "One Row, One Run", "every answer kept"),
            ("git-branch", X + 3.20, "Which Version", "control or variation"),
            ("hash", X + 6.40, "The Score", "same test each row")]
for name, cxo, head, sub in callouts:
    first = len(s.raw.shapes)
    y = sheet_bottom + 0.30
    badge(s, name, cxo, y)
    s.text(cxo + 0.56, y - 0.02, 2.36, 0.26, head, size=13, color=INK, bold=True,
           font=BODY_FONT)
    s.text(cxo + 0.56, y + 0.22, 2.36, 0.24, title_case(sub), size=SZ_CAPTION,
           color=SOFT_INK, font=BODY_FONT)
    group(s, first, head)
s.caption(X, sheet_bottom + 1.02, W, "That grid is an eval. No code required.")

# ============================================================== 3 same prompt x10
s = d.content("The same prompt, ten times")
first = len(s.raw.shapes)
ax = Axis(s, 1.50, 9.40, 2.62)
s.text(X, 2.05, 1.10, 0.30, title_case("control"), size=SZ_DIAGRAM, color=INK,
       bold=True, font=BODY_FONT, anchor="m")
m = ax.strip(2.10, CONTROL, INK, "FFFFFF", NODE_BG)
s.text(m - 0.80, 1.62, 1.60, 0.26, f"Mean {mean(CONTROL):,}", size=SZ_CAPTION,
       color=INK, bold=True, font=BODY_FONT, align="c")
s.text(9.40 - 2.4, 2.98, 2.4, 0.24, title_case("words per answer"),
       size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT, align="r")
group(s, first, "Control spread")
s.caption(X, 3.34, W, "Same prompt, same model, same settings. Ten different answers.")
note(s, "thermometer", X, 3.90, W, "Lower temperature narrows the spread",
     "It does not close it. The fix for a wide spread is more rows.")

# ============================================================== 4 chat window
s = d.content("What the chat window does not keep")
m = s.mock(0.40, TOP, 4.60, 3.58)
m.user("Blog post on time blocking. Make it long.")
with m.bubble():
    m.assistant("Time blocking is a way of committing",
                "specific hours to specific work…")
m.gap(0.06)
m.divider()
m.label("Same prompt, minutes later").line("A different answer. The first one is")
m.line("somewhere in the history, unlabelled.")
m.composer(pin=False)
lx = 5.50
s.text(lx, TOP + 0.04, 4.10, 0.30, title_case("lost in the chat"), size=14,
       color=ACCENT, bold=True, font=BODY_FONT)
for i, (name, head, sub) in enumerate([
        ("file-text", "The Exact Prompt", "what you actually sent"),
        ("layers", "The Other Answers", "the nine it could have given"),
        ("share-2", "A Record to Share", "something a colleague can check")]):
    first = len(s.raw.shapes)
    y = TOP + 0.52 + i * 0.66
    badge(s, name, lx, y, accent=False)
    s.text(lx + 0.58, y - 0.02, 3.50, 0.26, head, size=13, color=INK, bold=True,
           font=BODY_FONT)
    s.text(lx + 0.58, y + 0.22, 3.50, 0.24, title_case(sub), size=SZ_CAPTION,
           color=SOFT_INK, font=BODY_FONT)
    group(s, first, head)
s.text(lx, TOP + 2.60, 4.10, 0.30, "The sheet keeps all three.", size=14,
       color=INK, bold=True, font=BODY_FONT)

# ============================================================== 5 not / this
s = d.content("What a prompt test is not")
pairs = [("A prompt that reads better", "The same input, run many times"),
         ("One good run, screenshotted", "Every answer kept, weak ones too"),
         ("One person's read of one answer", "A number anyone can recompute"),
         ("A framework you install first", "A file anyone can open and check")]
s.text(0.84, TOP, 3.80, 0.28, title_case("not this"), size=13, color=SOFT_INK,
       bold=True, font=BODY_FONT)
s.text(5.64, TOP, 3.80, 0.28, title_case("this"), size=13, color=ACCENT,
       bold=True, font=BODY_FONT)
for i, (bad, good) in enumerate(pairs):
    first = len(s.raw.shapes)
    y = TOP + 0.44 + i * 0.58
    s.rect(X, y - 0.06, W, 0.50, fill=NODE_BG if i % 2 == 0 else "FFFFFF",
           rounded=True, radius=0.06)
    icon(s, "x", 0.44, y + 0.05, 0.28, "g")
    s.text(0.84, y, 3.90, 0.38, title_case(bad), size=SZ_CAPTION, color=SOFT_INK,
           font=BODY_FONT, anchor="m")
    icon(s, "check", 5.26, y + 0.05, 0.28, "p")
    s.text(5.64, y, 3.98, 0.38, title_case(good), size=SZ_CAPTION, color=INK,
           bold=True, font=BODY_FONT, anchor="m")
    group(s, first, f"Pair {i + 1}")
s.caption(X, TOP + 2.92, W, "What makes it an eval: every row is scored the same way.")

# ============================================================== 6 template
# A visual equation: template + this row's values = the prompt actually sent.
s = d.how("the template is not the text you test")
cards = [
    ("braces", "Prompt Template", 0.34, 3.00, [
        ("Write a blog post on", INK, False), ("{topic} in a {style}", ACCENT, True),
        ("tone.", INK, False), ("At least 2,000 words.", ACCENT, True)]),
    ("table", "Row Values", 3.80, 2.36, [
        ("topic: time blocking", INK, False), ("style: friendly", INK, False)]),
    ("send", "The Prompt Sent", 6.62, 3.04, [
        ("Write a blog post on", INK, False), ("time blocking in a", INK, False),
        ("friendly tone.", INK, False), ("At least 2,000 words.", ACCENT, True)]),
]
ch = 4 * LINE + 0.30
for name, head, x, w, lines in cards:
    first = len(s.raw.shapes)
    badge(s, name, x, TOP, accent=(head == "The Prompt Sent"))
    s.text(x + 0.56, TOP + 0.08, w - 0.56, 0.28, head, size=13, color=INK,
           bold=True, font=BODY_FONT)
    s.rect(x, TOP + 0.58, w, ch, fill=NODE_ACC if head == "The Prompt Sent" else NODE_BG,
           rounded=True, radius=0.05,
           line=ACCENT if head == "The Prompt Sent" else None, line_w=0.75)
    code(s, x + 0.16, TOP + 0.72, w - 0.24, ch - 0.20, lines)
    group(s, first, head)
for sym, x in (("+", 3.34), ("=", 6.16)):
    s.text(x, TOP + 0.58, 0.46, ch, sym, size=26, color=ACCENT, bold=True,
           font=BODY_FONT, align="c", anchor="m")
note(s, "tag", X, TOP + 0.58 + ch + 0.36, W, "The edit under test lives in the template",
     "Keep both columns: the template you edit, and the prompt that was sent.")

# ============================================================== 7 answer back
s = d.content("Getting the answer back into the cell")
steps = [("file-text", "The Prompt Sent", "one cell"),
         ("cpu", "The Model", "answers it"),
         ("table", "The Answer", "back into a cell"),
         ("hash", "The Score", "one number")]
colw = W / 4
for i, (name, head, sub) in enumerate(steps):
    first = len(s.raw.shapes)
    cx = X + i * colw + colw / 2
    badge(s, name, cx - 0.30, TOP, d=0.60, accent=(i == 3))
    s.text(cx - colw / 2, TOP + 0.70, colw, 0.26, head, size=13, color=INK,
           bold=True, font=BODY_FONT, align="c")
    s.text(cx - colw / 2, TOP + 0.96, colw, 0.24, title_case(sub),
           size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT, align="c")
    group(s, first, head)
    if i < 3:
        s.arrow(cx + 0.46, TOP + 0.24, colw - 0.92)
s.text(X, TOP + 1.42, W, 0.26, title_case("two ways across the gap"), size=13,
       color=INK, bold=True, font=BODY_FONT, align="c")
for i, (name, head, sub) in enumerate([
        ("clipboard", "Copy and Paste", "works anywhere"),
        ("square-function", "A Formula in the Cell", "faster, with caps and queues")]):
    first = len(s.raw.shapes)
    x = X + 0.60 + i * 4.36
    y = TOP + 1.78
    badge(s, name, x, y, accent=False)
    s.text(x + 0.56, y - 0.02, 3.40, 0.26, head, size=13, color=INK, bold=True,
           font=BODY_FONT)
    s.text(x + 0.56, y + 0.22, 3.40, 0.24, title_case(sub), size=SZ_CAPTION,
           color=SOFT_INK, font=BODY_FONT)
    group(s, first, head)
note(s, "tag", X, TOP + 2.52, W, "Record which model produced each row",
     "An unlabelled answer cannot be re-checked once the model moves on.")

# ============================================================== 8 score column
s = d.content("What goes in the score column")
judges = [("calculator", "A Formula Counts It", "words, a phrase, a format", 3, 1),
          ("bot", "Another Model Rates It", "fast and cheap, but drifts", 2, 2),
          ("user-round", "A Person Reads It", "the only judge of taste", 1, 3)]
colw = W / 3


def meter(s, x, y, label, n):
    s.text(x, y, 1.40, 0.24, title_case(label), size=SZ_CAPTION, color=SOFT_INK,
           font=BODY_FONT)
    for k in range(3):
        on = k < n
        oval(s, x + 1.46 + k * 0.28, y + 0.03, 0.18, ACCENT if on else "FFFFFF",
             line=ACCENT if on else RULE)


for i, (name, head, sub, consistency, judgement) in enumerate(judges):
    first = len(s.raw.shapes)
    cx = X + i * colw + colw / 2
    badge(s, name, cx - 0.32, TOP, d=0.64)
    s.text(cx - colw / 2, TOP + 0.76, colw, 0.28, head, size=13, color=INK,
           bold=True, font=BODY_FONT, align="c")
    s.text(cx - colw / 2, TOP + 1.04, colw, 0.24, title_case(sub),
           size=SZ_CAPTION, color=SOFT_INK, font=BODY_FONT, align="c")
    mx = cx - 1.10
    meter(s, mx, TOP + 1.46, "consistency", consistency)
    meter(s, mx, TOP + 1.80, "judgement", judgement)
    group(s, first, head)
s.caption(X, TOP + 2.44, W,
          "Count it with a formula where you can. Pay for judgement only where you must.")

# ============================================================== 9 two strips
s = d.content("Reading ten runs honestly")
first = len(s.raw.shapes)
ax = Axis(s, 1.50, 7.70, 3.06)
rows = [("control", CONTROL, INK, "FFFFFF", NODE_BG, 1.86),
        ("variation", VARIANT, ACCENT, NODE_ACC, "FDF1F5", 2.46)]
for lab, vals, colour, fill, band, y in rows:
    s.text(X, y - 0.05, 1.10, 0.30, title_case(lab), size=SZ_DIAGRAM, color=colour,
           bold=True, font=BODY_FONT, anchor="m")
    ax.strip(y, vals, colour, fill, band)
    s.text(7.95, y - 0.05, 1.70, 0.30, f"Mean {mean(vals):,}", size=13,
           color=colour, bold=True, font=BODY_FONT, anchor="m")
# The overlap, bracketed on the axis.
olo, ohi = ax.at(max(min(CONTROL), min(VARIANT))), ax.at(min(max(CONTROL), max(VARIANT)))
s.rect(olo, 1.62, ohi - olo, 0.012, fill=ACCENT)
s.text(olo, 1.62 - 0.02 - 0.24, ohi - olo, 0.24, title_case("overlap"),
       size=SZ_CAPTION, color=ACCENT, bold=True, font=BODY_FONT, align="c")
group(s, first, "Control vs variation")
delta = mean(VARIANT) / mean(CONTROL) - 1
s.text(7.95, 3.00, 1.70, 0.40, f"+{delta * 100:.1f}%", size=22, color=ACCENT,
       bold=True, font=BODY_FONT, anchor="m")
s.caption(X, 3.72, W,
          "Means 7% apart, ranges almost fully overlapping. Worth fifty more runs, "
          "not a conclusion.")

# ============================================================== 10 WHY IT MATTERS
s = d.why("you can show your working")
rows = [
    ["", "Without a sheet", "With a sheet"],
    ["The decision", "Whoever argues best", "The mean across runs"],
    ["The evidence", "One good screenshot", "Every run, kept"],
    ["A new model lands", "Start the argument again", "Re-run the same rows"],
    ["Failure mode", "Confident untested habits", "Over-reading ten noisy runs"],
]
rows[0] = [title_case(c) for c in rows[0]]
for r in rows[1:]:
    r[0] = title_case(r[0])
tx = X + 0.56
s.table(tx, TOP, W - 0.56, 2.30, rows, col_widths=[1.9, 3.4, 3.46])
rh = 2.30 / 5
for i, name in enumerate(["scale", "archive", "refresh-cw", "triangle-alert"]):
    icon(s, name, X + 0.06, TOP + rh * (i + 1) + (rh - 0.30) / 2, 0.30,
         "p" if i == 3 else "i")
s.caption(X, 4.10, W,
          "Not certainty. A record of what was tried that outlives whoever ran it.")

# ============================================================== 11 spectrum
s = d.content("Where the sheet runs out of road")
first = len(s.raw.shapes)
bx0, bx1, by = 1.10, 8.90, TOP + 0.26
bar = s.rect(bx0, by, bx1 - bx0, 0.16, fill=NODE_BG, rounded=True, radius=0.08)
bar.fill.gradient()
bar.fill.gradient_angle = 0
bar.fill.gradient_stops[0].color.rgb = _rgb("ECECF0")
bar.fill.gradient_stops[1].color.rgb = _rgb(ACCENT)
badge(s, "sheet", X, TOP, d=0.66, accent=False)
badge(s, "code-xml", X + W - 0.66, TOP, d=0.66)
s.text(bx0, by + 0.24, bx1 - bx0, 0.26,
       title_case("more cases, more often, higher stakes"), size=SZ_CAPTION,
       color=SOFT_INK, font=BODY_FONT, align="c")
group(s, first, "Spectrum")
for side, (head, items, colour) in enumerate([
        ("A sheet is the right tool", ["One prompt, tens of runs",
                                       "A judgement only a person can make",
                                       "Showing your working to a team"], INK),
        ("Hand it to an engineer", ["Hundreds of cases, re-run often",
                                    "Every model upgrade re-checked",
                                    "Scoring that must never vary"], ACCENT)]):
    first = len(s.raw.shapes)
    x = X + side * 4.84
    y = TOP + 1.04
    s.text(x, y, 4.48, 0.30, title_case(head), size=14, color=colour, bold=True,
           font=BODY_FONT)
    for k, item in enumerate(items):
        yy = y + 0.44 + k * 0.46
        oval(s, x + 0.02, yy + 0.08, 0.12, colour)
        s.text(x + 0.26, yy, 4.20, 0.30, title_case(item), size=SZ_CAPTION,
               color=INK, font=BODY_FONT, anchor="m")
        if k < len(items) - 1:
            s.rect(x + 0.26, yy + 0.38, 4.20, 0.008, fill=RULE)
    group(s, first, head)

# ---------------------------------------------------------------- 12 handoff
d.handoff(
    [("Build the grid", "one row per run, one column per version"),
     ("Add one variation", "changed in the template, not the row"),
     ("Run it ten times", "and score every row the same way")],
    lead="That is the instrument. Now we build one and run a real test in it.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
