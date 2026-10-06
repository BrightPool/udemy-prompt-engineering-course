#!/usr/bin/env python3
"""
"Summarising Large Content" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/summarising-large-content/build_summarising_large_content.py
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/summarising-large-content/summarising-large-content.pptx

Arc: count the tokens before you send, because the window decides whether one
call is enough (what) - size every chunk from the window minus a safety margin,
the instructions and the answer (how) - map then reduce, and repeat until it
fits, so bigger windows mean fewer calls with no code change (why).

No model names or window sizes. Today's numbers live in NOTES.md and the notebook.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))
from pptx.enum.dml import MSO_LINE_DASH_STYLE  # noqa: E402
from deckkit import (ACCENT, ARROW, BODY_FONT, INK, NODE_ACC, NODE_BG, RULE,  # noqa: E402
                     SZ_CAPTION, Deck, title_case)

out = Path(sys.argv[1] if len(sys.argv) > 1 else
           Path(__file__).resolve().parent / "summarising-large-content.pptx")


def label(s, x, y, w, text, size=SZ_CAPTION, color=INK, bold=False, align="c",
          h=0.26):
    return s.text(x, y, w, h, text, size=size, color=color, bold=bold,
                  font=BODY_FONT, align=align, anchor="m")


d = Deck()
d.title("Summarising Large Content",
        "How to summarise anything from a page to a whole book without "
        "overflowing the model's context window.")

# 2. Fit vs overflow, measured before sending.
s = d.what("count the tokens before you send")
X0, LIMIT = 0.34, 7.40


def bar(y, parts, title, color):
    label(s, X0, y, 5.0, title_case(title), size=14, bold=True, color=color,
          align="l", h=0.30)
    by, bh, x = y + 0.38, 0.52, X0
    for name, frac, over in parts:
        w = LIMIT * frac
        seg = s.rect(x, by, w, bh, fill=None if over else
                     (NODE_ACC if name == "Book" else NODE_BG),
                     line=ACCENT if over or name == "Book" else RULE, line_w=1.0)
        if over:
            seg.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        label(s, x, by, w, title_case(name), color=ACCENT if over else INK,
              bold=over, h=bh)
        x += w


bar(1.56, [("Instructions", 0.18, False), ("Book", 0.52, False),
           ("Summary", 0.18, False)], "Fits: one call", INK)
bar(2.86, [("Instructions", 0.18, False), ("Book", 0.82, False),
           ("Overflow", 0.20, True)], "Too big: split it", ACCENT)
s.rect(X0 + LIMIT - 0.01, 1.86, 0.025, 2.20, fill=ARROW)
label(s, X0 + LIMIT - 1.00, 4.10, 2.00, title_case("Window limit"), color=ACCENT,
      bold=True)
s.caption(0.34, 4.46, 6.20,
          "A tokeniser counts exactly what the model will see, so you know "
          "before you pay.")

# 3. The chunk budget.
s = d.how("budget every chunk")
s.layers(0.34, 1.52, 5.90,
         [("Context window", "set by the model"),
          ("Minus 5% safety margin", "counts are estimates"),
          ("Minus instructions", "your prompt"),
          ("Minus output reserve", "room to answer"),
          ("Chunk budget", "max per call", True)], h=0.50)
s.caption(6.50, 1.60, 3.16,
          "Derive the chunk size from the model, never hardcode it. Change "
          "the model and the budget follows.")

# 4. The adaptive loop: fits goes straight to one call, too big goes round.
s = d.content("One call when it fits, a loop when it does not")
C1, C2, C3, CW = 0.34, 3.70, 7.06, 2.60
R1, R2, RH = 1.56, 2.92, 0.86
s.node(C1, R1, CW, RH, "Count", sub="tokens in the text")
s.node(C2, R1, CW, RH, "Fits the Budget?")
s.node(C3, R1, CW, RH, "One call", sub="summarise or combine", accent=True)
s.node(C2, R2, CW, RH, "Split", sub="into budget-sized chunks")
s.node(C3, R2, CW, RH, "Map", sub="summarise each chunk")
for ax in (C1 + CW + 0.10, C2 + CW + 0.10):
    s.arrow(ax, R1 + RH / 2 - 0.06, 0.56, 0.12)
label(s, C2 + CW + 0.04, R1 + RH / 2 - 0.34, 0.70, "Yes", color=ACCENT, bold=True)
s.arrow(C2 + CW / 2 - 0.05, R1 + RH + 0.06, 0.10, R2 - R1 - RH - 0.12,
        direction="down")
label(s, C2 + CW / 2 + 0.10, R1 + RH + 0.12, 0.60, "No", color=ACCENT, bold=True,
      align="l")
s.arrow(C2 + CW + 0.10, R2 + RH / 2 - 0.06, 0.56, 0.12)
# Return loop: joined chunk summaries go back to Count.
ly = R2 + RH + 0.24
s.rect(C3 + CW / 2, R2 + RH, 0.012, ly - R2 - RH, fill=ARROW)
s.rect(C1 + CW / 2, ly, C3 - C1, 0.012, fill=ARROW)
s.arrow(C1 + CW / 2 - 0.05, R1 + RH + 0.04, 0.10, ly - R1 - RH - 0.04,
        direction="up")
label(s, C1 + CW / 2 + 0.12, ly + 0.06, 3.60, "Joined summaries go round again",
      color=ACCENT, align="l")
s.caption(0.34, ly + 0.46, 9.32,
          "Bigger windows mean fewer passes with no code change; too much input "
          "backs off into chunks. Each pass can drop nuance, so keep chunk summaries.")

d.handoff([("Count the book", "with a tokeniser"),
           ("Check the window", "minus the safety margin"),
           ("Summarise adaptively", "one call or map and reduce")],
          lead="That is the principle. Now we run it on a whole book.")

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
