#!/usr/bin/env python3
"""
"Shortcuts" - the principles half of the re-film.

A 00:35 lecture, so this is deliberately the shortest deck in the course: six
slides. No key combination appears anywhere - those differ by platform, they
move when the interface is redesigned, and the demo half shows the live list.

Run:
    uv run --with python-pptx python decks/shortcuts/build_shortcuts.py \
        decks/shortcuts/shortcuts.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/shortcuts/shortcuts.pptx
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/principles-deck/scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "decks/shortcuts/shortcuts.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Shortcuts",
        "How the ChatGPT interface answers the keyboard as well as the mouse.")

# ============================================================== WHAT IS IT?
s = d.what("the same interface, reached without the mouse")
m = s.mock(0.40, 1.56, 4.70, 3.40, tag="Shortcut list")
m.line("Toggle the sidebar")
m.line("Open a new chat")
m.line("Focus the message box")
m.line("Search your chats")
m.line("Copy the last response")
m.line("Copy the last code block")
m.line("Stop the response")
m.gap(0.08)
m.divider()
m.line("Open this list", highlight=True)
m.fit()
s.beside(m, "Each line here is something you already do with the pointer. The "
            "keyboard is a second set of controls over the same interface, and "
            "ChatGPT keeps its own list of them.")

s = d.content("The one worth memorising")
s.layers(0.34, 1.56, 5.86,
         [("Move around", "sidebar, chats, search"),
          ("Start and stop", "new chat, stop, focus"),
          ("Take the answer away", "copy the reply or the code"),
          ("Open this list", "the only one to memorise", True)],
         h=0.66)
s.caption(6.46, 2.43, 3.20,
          "Learn the shape of the list rather than the list itself. Three of "
          "these bands are things you do dozens of times a day; the fourth is "
          "how you look the other three up.")

# ============================================================== HOW IT WORKS
s = d.how("a shortcut is a second door to one action")
s.node(1.35, 1.56, 3.10, 0.95, "Click the control",
       sub="your hand leaves the keys")
s.node(1.35, 2.81, 3.10, 0.95, "Press the shortcut",
       sub="your hands stay put")
s.arrow(4.55, 1.975, 0.70)
s.arrow(4.55, 3.225, 0.70)
s.node(5.35, 1.56, 3.30, 2.20, "The same action runs",
       sub="the interface cannot tell which door you used", accent=True)
s.caption(1.35, 4.04, 7.30,
          "Nothing about the answer changes. A shortcut is not a hidden feature or "
          "a power-user mode: it is the ordinary action, minus the trip to the "
          "pointer and back.")

# ============================================================== WHY IT MATTERS
s = d.why("the small moves stop costing anything")
s.table(0.34, 1.56, 9.32, 2.10, [
    ["", "Reaching for the mouse", "Reaching for the keyboard"],
    ["Start a new chat", "Find the control, then aim", "Hands never leave the keys"],
    ["Find an old chat", "Scroll the list", "Type what you remember"],
    ["Reuse an answer", "Select it, then copy", "One press takes the last one"],
    ["What it costs you", "A pause you stop noticing", "A minute learning four of them"],
], col_widths=[2.2, 3.56, 3.56])
s.caption(0.34, 3.90, 9.32,
          "The honest limit: these combinations differ between platforms, and they "
          "move when the interface is redesigned. That is exactly why the one to "
          "commit to memory is the one that shows you the current list.")

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Open the list", "live, on this machine"),
     ("Run the four jobs", "sidebar, new chat, input, copy"),
     ("Check your platform", "the keys are not the same everywhere")],
    lead="That is the principle. Now let's open the real list and use it.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
