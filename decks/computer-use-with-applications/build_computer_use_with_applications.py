#!/usr/bin/env python3
"""Build the five-slide principles deck for Computer Use with desktop apps."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck, title_case  # noqa: E402

out = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else Path(__file__).resolve().parent / "computer-use-with-applications.pptx"
)

d = Deck()

d.title(
    "Computer Use with Desktop Applications",
    "How ChatGPT sees and operates the interfaces of applications you allow.",
)

s = d.what("the assistant works through the visible interface")
m = s.mock(0.40, 1.52, 4.60, 3.58, app="Desktop application", tag="Approved")
m.user("Sort this spreadsheet by deadline", "and flag overdue rows.")
with m.bubble():
    m.assistant("Done. The workbook is open for your review.")
m.label("Computer Use").line("Operated the visible interface.", highlight=True)
m.composer(pin=False)
s.beside(
    m,
    "Computer Use lets ChatGPT see a graphical interface and operate it in much "
    "the same way you would. It can click, type and navigate inside applications "
    "you approve for the task.",
)

s = d.how("each action follows what is on screen")
s.flow(
    0.34,
    1.52,
    9.32,
    [
        ("Observe", "the current screen"),
        ("Decide", "the next small action"),
        ("Operate", "click, type or navigate"),
        ("Check", "what changed"),
    ],
    h=1.10,
    accent_last=True,
    loop="repeat until the scoped task is complete",
)
s.caption(
    0.34,
    3.62,
    9.32,
    "The loop matters because interfaces change after every action. ChatGPT must "
    "look again before it can choose the next step, just as a person would.",
)

s = d.why("it reaches work with no direct integration")
rows = [
    ["Situation", "Best route", "Reason"],
    ["Reliable data operation", "Plugin or MCP tool", "Structured and repeatable"],
    ["Visual or app-only task", "Computer Use", "The interface is the route"],
    ["Sensitive change", "Human review", "The impact needs your judgement"],
    ["Failure mode", "Wrong window or control", "Pause, inspect and take over"],
]
rows[0] = [title_case(c) for c in rows[0]]
for r in rows[1:]:
    r[0] = title_case(r[0])
s.table(
    0.34,
    1.52,
    9.32,
    2.30,
    rows,
    col_widths=[2.70, 2.55, 4.07],
)
s.caption(
    0.34,
    4.02,
    9.32,
    "Computer Use fills the gaps between integrations. Keep each task narrow, "
    "approve only the applications it needs and stay present for sensitive work.",
)

d.handoff(
    [
        ("Choose one app", "one clear boundary"),
        ("Name the task", "the window and the outcome"),
        ("Approve access", "read the permission"),
        ("Watch closely", "take over if it strays"),
    ],
    lead="Now we use ChatGPT with a real desktop application.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
