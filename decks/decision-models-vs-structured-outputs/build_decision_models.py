#!/usr/bin/env python3
"""
"Decision Models vs Structured Outputs" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/decision-models-vs-structured-outputs/build_decision_models.py
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/decision-models-vs-structured-outputs/decision-models-vs-structured-outputs.pptx

Arc: an LLM writes its label token by token, a decision model picks one of
your labels and says how sure it is (what) - calibrated probabilities become
thresholds you can route on, and each tool has a job (why).

No prices, latencies or version numbers on the slides. Measured numbers are in
NOTES.md for James to say aloud.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))
from deckkit import (ACCENT, BODY_FONT, INK, NODE_ACC, NODE_BG, RULE,  # noqa: E402
                     SOFT_INK, SZ_CAPTION, SZ_DIAGRAM, Deck, title_case)

out = Path(sys.argv[1] if len(sys.argv) > 1 else
           Path(__file__).resolve().parent /
           "decision-models-vs-structured-outputs.pptx")

REVIEW = "The handle snapped on day two."


def label(s, x, y, w, text, size=SZ_CAPTION, color=INK, bold=False, align="c",
          h=0.26):
    return s.text(x, y, w, h, text, size=size, color=color, bold=bold,
                  font=BODY_FONT, align=align, anchor="m")


def panels(s, y, left_title, left, right_title, right, h, x=0.34, w=9.32,
           gap=0.40):
    """Two labelled panels, like deckkit's compare(), with a dot instead of a
    dash so no em dash reaches the slide."""
    col = (w - gap) / 2
    for cx, title, items, accent in ((x, left_title, left, False),
                                     (x + col + gap, right_title, right, True)):
        s.rect(cx, y, col, h, fill="FFFFFF", rounded=True,
               line=ACCENT if accent else RULE, line_w=1.0 if accent else 0.75)
        s.text(cx + 0.20, y + 0.14, col - 0.40, 0.30, title_case(title), size=14,
               color=ACCENT if accent else INK, bold=True, font=BODY_FONT)
        for i, item in enumerate(items):
            s.text(cx + 0.20, y + 0.54 + i * 0.32, col - 0.40, 0.30,
                   f"•  {item}", size=SZ_DIAGRAM, color=INK, font=BODY_FONT)


d = Deck()
d.title("Decision Models vs Structured Outputs",
        "Why a model that picks from your labels can classify faster and cheaper "
        "than one that writes JSON.")

# 2. Same review, two kinds of model.
s = d.what("write a label, or decide one")
m = s.mock(0.40, 1.56, 4.40, 2.40, generic=True)
m.user(REVIEW)
with m.bubble():
    m.assistant('{"sentiment": "negative"}')
m.fit()
s.caption(0.40, m.y + m.h + 0.12, 4.40,
          "Generates tokens a schema constrains. You pay for input and output, "
          "and get a label with no reliable confidence.")
m2 = s.mock(5.26, 1.56, 4.40, 2.40, app="Decision Model", tag="Example")
m2.label("State").line(REVIEW)
m2.label("Answers")
m2.line("sentiment = negative (0.97)", highlight=True)
m2.line("needs a reply = 0.94")
m2.fit()
s.caption(5.26, m2.y + m2.h + 0.12, 4.40,
          "Picks from labels you define, answers several questions per call, and "
          "says how sure it is.")

# 3. Calibration turns a probability into a routing rule.
s = d.why("calibrated scores become thresholds")
BX, BW, BY, BH = 0.34, 9.32, 1.92, 0.56
zones = [(0.0, 0.6, "Human review", NODE_BG, INK),
         (0.6, 0.85, "Spot check", NODE_BG, INK),
         (0.85, 1.0, "Auto-handle", NODE_ACC, ACCENT)]
for a, b, name, fill, ink in zones:
    s.rect(BX + BW * a, BY, BW * (b - a), BH, fill=fill,
           line=ACCENT if fill == NODE_ACC else RULE, line_w=1.0)
    label(s, BX + BW * a, BY, BW * (b - a), title_case(name), color=ink,
          bold=fill == NODE_ACC, h=BH)
for v in (0.0, 0.6, 0.85, 1.0):
    al = "l" if v == 0.0 else ("r" if v == 1.0 else "c")
    ox = 0 if v == 0.0 else (-0.6 if v == 1.0 else -0.30)
    label(s, BX + BW * v + ox, 1.58, 0.60, f"{v:g}", color=SOFT_INK, align=al)
s.caption(0.34, BY + BH + 0.10, 9.32,
          "Calibrated: answers given at 0.8 are right about 80% of the time.")
panels(s, 3.10, "Decision model for",
       ["Fixed labels, high volume", "Routing and moderation"],
       "Structured outputs for",
       ["Free text and extraction", "Reasoning in the answer"], h=1.24)
s.caption(0.34, 4.46, 9.32,
          "Limit: a decision model only answers the questions you define.")

d.handoff([("Structured outputs", "time and cost each call"),
           ("Decision model", "same reviews, same labels"),
           ("Compare", "speed, cost and confidence")],
          lead="That is the principle. Now we race them on real reviews.")

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
