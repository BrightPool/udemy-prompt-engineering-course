#!/usr/bin/env python3
"""Build the five-slide principles deck for the ChatGPT desktop application."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else Path(__file__).resolve().parent / "chatgpt-desktop-application.pptx"
)

d = Deck()

d.title(
    "ChatGPT Desktop Application",
    "How ChatGPT works with selected files, folders and tools on your computer.",
)

s = d.what("a workspace beside your local files")
m = s.mock(0.40, 1.52, 4.60, 3.58)
m.user("Read briefing.md and turn it into", "a short slide deck.")
with m.bubble():
    m.assistant("Created briefing-deck.pptx", "beside the source file.")
m.label("Files used").line("briefing.md")
m.line("briefing-deck.pptx", highlight=True)
m.composer(pin=False)
s.beside(
    m,
    "When you open a folder for ChatGPT, its files become working material for "
    "that task. ChatGPT can read the source, create an output and save changes "
    "back into the location you selected.",
)

s = d.how("local access starts with a boundary you choose")
bottom = s.layers(
    0.34,
    1.52,
    5.90,
    [
        ("Your request", "the outcome you want", True),
        ("The selected folder", "files and project context"),
        ("Approved tools", "only the access the task permits"),
    ],
    h=0.66,
)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "One local task", accent=True)
s.caption(
    6.50,
    2.20,
    3.16,
    "The folder is the working boundary. File reads, edits and app access still "
    "follow the permissions and approvals attached to the task.",
)

s = d.why("the distance between asking and doing gets shorter")
s.table(
    0.34,
    1.52,
    9.32,
    2.30,
    [
        ["", "Browser chat", "Desktop application"],
        ["Source files", "Upload or paste copies", "Use a selected folder"],
        ["Outputs", "Download and organise", "Save beside the source"],
        ["Local apps", "Outside the browser", "Use approved applications"],
        ["Failure mode", "Missing local context", "A boundary set too broadly"],
    ],
    col_widths=[1.55, 3.65, 4.12],
)
s.caption(
    0.34,
    4.02,
    9.32,
    "Local access does not mean the model runs offline. It means the desktop app "
    "can supply permitted computer context and place finished work where you need it.",
)

d.handoff(
    [
        ("Open a working folder", "choose a narrow, useful boundary"),
        ("Ask it to read a file", "check the source"),
        ("Create or edit an output", "save beside the original"),
        ("Review the change", "confirm the file before sharing it"),
    ],
    lead="That is the principle. Now we let ChatGPT work with a real local folder.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
