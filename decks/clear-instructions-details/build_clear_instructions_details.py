#!/usr/bin/env python3
"""Build the five-slide principles deck for detailed instructions."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "clear-instructions-details.pptx")
d = Deck()

d.title(
    "Writing Clear Instructions",
    "How useful detail turns a vague request into an output you can judge.",
)

s = d.what("detail defines what a good answer must contain")
r = s.message_row(0.34, 1.52, 9.32, 0.92)
r.label("Vague request")
r.line("Write a product update.")
r = s.message_row(0.34, 2.66, 9.32, 1.24)
r.label("Detailed request")
r.line("Write a product update for existing customers.", highlight=True)
r.line("Explain the new export, why it saves time and the one action to try today.")
s.caption(
    0.34,
    4.10,
    9.32,
    "Useful detail narrows the decision space. The answer can now be checked "
    "against an audience, a purpose and required content.",
)

s = d.how("four details make the request checkable")
s.layers(
    0.34,
    1.52,
    5.28,
    [
        ("Audience", "who will use the answer"),
        ("Purpose", "what the answer should achieve"),
        ("Required content", "facts that must appear"),
        ("Output shape", "format and tone", True),
    ],
    h=0.54,
)
s.caption(
    6.05,
    1.78,
    3.58,
    "Add the details that change the result. Extra instructions that do not "
    "affect success create noise and make the prompt harder to maintain.",
)

s = d.why("clear criteria make revision faster")
s.table(
    0.34,
    1.52,
    9.32,
    2.38,
    [
        ["", "Vague instruction", "Detailed instruction"],
        ["Target", "Model must infer it", "Audience and goal are explicit"],
        ["Coverage", "Important points may vanish", "Required points can be checked"],
        ["Revision", "Feedback stays subjective", "You can name the missed rule"],
        ["Failure mode", "Generic output", "Too many constraints"],
    ],
    col_widths=[1.62, 3.52, 4.18],
)

d.handoff(
    [
        ("Start vague", "run the short request"),
        ("Add the audience", "say who it is for"),
        ("Add success criteria", "name required content"),
        ("Compare the drafts", "judge against the brief"),
    ],
    lead="Next, we improve one ChatGPT request by adding only the details that matter.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
