#!/usr/bin/env python3
"""
"The ChatGPT Desktop App" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/desktop-app/build_desktop_app.py \
        decks/desktop-app/desktop-app.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/desktop-app/desktop-app.pptx

This lecture is the most drift-prone in the course: it is about a client
application, its platforms and its buttons. So the deck teaches one durable
idea - proximity - and every platform list, hotkey and menu path lives in
NOTES.md for the instructor to say aloud over the live demo.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "decks/desktop-app/desktop-app.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("The ChatGPT Desktop App",
        "The same assistant as the browser, sitting beside your work rather "
        "than in a tab.")

# ============================================================== WHAT IS IT?
s = d.what("ChatGPT as an application, not a page you go to")
m = s.mock(0.40, 1.52, 4.66, 3.50, tag="Over your work")
m.user("Tidy the paragraph I have selected.")
with m.bubble():
    m.assistant("Same argument, two sentences shorter.")
m.composer(pin=False)
s.beside(m, "Same account, same conversations, same models. What changes is "
            "where it sits: a keystroke away, on top of whatever you already "
            "have open, instead of somewhere you have to navigate to.")

s = d.content("What being next to your work buys you")
m = s.mock(0.40, 1.52, 4.66, 3.50, tag="Demonstration")
m.label("Attached from your screen")
m.line("The window you were looking at", highlight=True)
m.user("Why is this total not adding up?")
with m.bubble():
    m.assistant("Row 14 is text, not a number, so the sum",
                "quietly skips it. Everything else is right.")
m.composer(pin=False)
s.beside(m, "In a tab you describe the problem or copy it across, and you lose "
            "detail both ways. Beside your work you point at it. The question "
            "gets shorter and the answer gets more specific.")

s = d.content("What it is not")
s.compare(1.52,
          "Not this", ["A cleverer ChatGPT",
                       "A separate account and history",
                       "A one-operating-system product",
                       "A tool built for developers"],
          "This", ["The same models you already use",
                   "One history, shared everywhere",
                   "One of several places it runs",
                   "Useful to anyone with a screen"])
s.caption(0.34, 4.34, 9.32,
          "Nothing here is an upgrade in intelligence. It is the same assistant, "
          "reachable from more of the places you actually work.")

# ============================================================== HOW IT WORKS
s = d.how("summon it, point it, allow it")
s.steps(0.34, 1.52, 5.40, [
    "A keystroke brings it up over your work.",
    "You point it at a window, a file, a page.",
    "Your computer asks you to allow that, once.",
    "What it captured is attached to your message.",
    "The reply lands in your ordinary chat history.",
])
s.caption(6.10, 2.56, 3.56,
          "Only the permission step is new. The rest is the ordinary "
          "conversation you already know how to have, which is why there is no "
          "second tool to learn here.")

s = d.content("What arrives with a question you never had to type out")
bottom = s.layers(0.34, 1.52, 5.70,
                  [("A window you pointed at", "as a picture of it", True),
                   ("The app you were working in", "the text it can read"),
                   ("A file, folder or page you opened", "only where you aimed it"),
                   ("Your typed or spoken line", "the short part")], h=0.56)
s.arrow(3.00, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.70, 0.56, "One message you never wrote out",
       accent=True)
s.caption(6.30, 2.60, 3.36,
          "It is never handed your whole machine. It is handed what the app "
          "captured at the moment you asked, and from then on that is simply "
          "part of the conversation.")

s = d.content("Speaking to it while you carry on working")
m = s.mock(0.40, 1.52, 4.66, 3.50, tag="Spoken")
m.user("Read the draft back to me and say what is missing.")
with m.bubble():
    m.assistant("It never says who it is for, and paragraphs",
                "two and four make the same point.")
m.gap(0.06)
m.divider()
m.label("Kept in the same chat")
m.line("Read it back, search it later.")
m.fit()
s.beside(m, "Voice is a way into the conversation you already have, not a "
            "separate one. You can talk while your hands stay on the work, cut "
            "in mid-answer, and read the whole exchange back afterwards.")

s = d.content("Where the permission stops")
m = s.mock(5.06, 1.52, 4.60, 3.20, app="Permissions", tag="You decide")
m.label("Only after you allow it")
m.line("The window you aim it at")
m.line("A folder you open to it")
m.line("A page in its own browser")
m.line("Your microphone")
m.gap(0.06)
m.divider()
m.label("Not without aiming again")
m.line("Your other open applications")
m.line("Anything you closed before asking")
m.line("Your screen when you have not asked")
m.fit()
s.beside(m, "Every extra thing it can do arrives as a permission your computer "
            "asks you to grant. That is the real boundary: it reaches what you "
            "allowed and what you aimed it at, and stops there.")

# ============================================================== WHY IT MATTERS
s = d.why("the cost of asking a question falls to nearly nothing")
s.table(0.34, 1.58, 9.32, 1.90, [
    ["", "In a browser tab", "Beside your work"],
    ["Getting context in", "Describe it, or copy it across", "Aim at it"],
    ["Switching", "You leave what you were doing", "It comes to you"],
    ["Failure mode", "Vague answers to vague questions",
     "You send more than you meant to"],
], col_widths=[2.0, 3.6, 3.7])
s.caption(0.34, 3.70, 9.32,
          "The second failure mode is the quieter one. A window you had "
          "forgotten was attached goes to the model along with your question, "
          "and is stored in your history with it, under whatever data settings "
          "you already have.")

d.two_columns(
    "The trade you are agreeing to",
    ["Work you would have pasted in anyway",
     "A folder you set up for this task",
     "A page you were about to read line by line"],
    ["A screen with somebody else's data on it",
     "Everything on your machine, to save a click",
     "Anything you have not checked you are allowed to share"],
    left_heading="Worth pointing it at",
    right_heading="Stop and think first",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Summon it", "over something you are working on"),
     ("Point it at one window", "and watch what gets attached"),
     ("Talk to it", "while you carry on with the work"),
     ("Open the permissions", "and take one back")],
    lead="That is the principle. Now we do it live on my machine.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
