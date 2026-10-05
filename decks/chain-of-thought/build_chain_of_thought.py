#!/usr/bin/env python3
"""Build the five-slide principles deck for chain-of-thought prompting."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "chain-of-thought.pptx")
d = Deck()

d.title(
    "Chain of Thought",
    "How step-by-step prompting differs from the reasoning a model performs internally.",
)

s = d.what("two ideas share one name")
s.table(
    0.34,
    1.52,
    9.32,
    2.18,
    [
        ["", "Prompted steps", "Internal reasoning"],
        ["What it is", "A workflow you ask the model to follow", "Work the model performs before answering"],
        ["What you see", "Plans, calculations or checkpoints", "Usually a final answer or brief summary"],
        ["Why it helps", "Makes required stages explicit", "Supports harder decisions and synthesis"],
    ],
    col_widths=[1.58, 3.77, 3.97],
)
s.caption(
    0.34,
    3.94,
    9.32,
    "For teaching and review, ask for useful visible artefacts: assumptions, "
    "calculations, evidence and a concise explanation of the conclusion.",
)

s = d.how("a reasoning request can stay outcome focused")
s.flow(
    0.34,
    1.52,
    9.32,
    [
        ("Define the problem", "goal and evidence"),
        ("Set checks", "criteria and constraints"),
        ("Model reasons", "using its capabilities"),
        ("Return the result", "answer plus useful support"),
    ],
    h=1.08,
    accent_last=True,
)
s.caption(
    0.34,
    3.72,
    9.32,
    "Modern reasoning models often work best from a clear outcome and success "
    "criteria. Specify exact steps only when the process itself matters.",
)

s = d.why("visible checks are more useful than a long transcript")
s.table(
    0.34,
    1.52,
    9.32,
    2.38,
    [
        ["Ask for", "What it gives you", "What to inspect"],
        ["Assumptions", "Inputs treated as true", "Missing or weak premises"],
        ["Calculations", "Numbers you can recompute", "Arithmetic and units"],
        ["Evidence", "Sources behind the answer", "Relevance and reliability"],
        ["Concise rationale", "A readable explanation", "Whether the conclusion follows"],
    ],
    col_widths=[2.15, 3.30, 3.87],
)

d.handoff(
    [
        ("Give a hard problem", "state the outcome"),
        ("Add success criteria", "name the checks"),
        ("Request useful support", "assumptions and evidence"),
        ("Verify the result", "recompute and inspect"),
    ],
    lead="Now we compare a bare request with one that asks for checkable support.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
