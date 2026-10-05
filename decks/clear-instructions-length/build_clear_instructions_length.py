#!/usr/bin/env python3
"""Build the five-slide principles deck for specifying output length."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "clear-instructions-length.pptx")
d = Deck()

d.title(
    "Specifying Length",
    "How a measurable target helps ChatGPT choose the right level of detail.",
)

s = d.what("length is part of the output contract")
r = s.message_row(0.34, 1.52, 9.32, 0.92)
r.label("Open-ended")
r.line("Summarise this report. Keep it short.")
r = s.message_row(0.34, 2.66, 9.32, 1.24)
r.label("Measurable")
r.line("Summarise this report in 120 to 150 words for a senior manager.", highlight=True)
r.line("Prioritise the decision, the evidence and the main risk.")
s.caption(
    0.34,
    4.10,
    9.32,
    "A word range, item count or reading time gives both you and the model a "
    "shared target. Priority tells the model what deserves the limited space.",
)

s = d.how("length works with audience and priority")
s.layers(
    0.34,
    1.52,
    5.28,
    [
        ("Audience", "who will read it"),
        ("Purpose", "what they need to do"),
        ("Length target", "words, items or time"),
        ("Priority", "what survives the cut", True),
    ],
    h=0.54,
)
s.caption(
    6.05,
    1.78,
    3.58,
    "Length alone can create a neat answer that omits the important point. "
    "Pair the limit with a clear statement of what must remain.",
)

s = d.why("the answer fits the place where it will be used")
s.table(
    0.34,
    1.52,
    9.32,
    2.38,
    [
        ["", "Vague length", "Measurable length"],
        ["Interpretation", "Short means different things", "Target can be checked"],
        ["Editing", "Cut after generation", "Detail is selected up front"],
        ["Consistency", "Varies widely between runs", "Outputs are easier to compare"],
        ["Failure mode", "Too long for the channel", "Tight limit drops key context"],
    ],
    col_widths=[1.62, 3.52, 4.18],
)

d.handoff(
    [
        ("Ask for short", "run the vague version"),
        ("Set a word range", "make it measurable"),
        ("Name the priority", "protect key content"),
        ("Compare the outputs", "check fit and coverage"),
    ],
    lead="Now we use one report and compare an open-ended summary with a measured one.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
