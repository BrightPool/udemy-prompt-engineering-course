#!/usr/bin/env python3
"""
"Custom Instructions" - the principles half of the re-film.

Run:
    uv run --with python-pptx python \
        decks/custom-instructions/build_custom_instructions.py \
        decks/custom-instructions/custom-instructions.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/custom-instructions/custom-instructions.pptx

The lecture is 01:18, so the deck runs short - eight slides, no padding. The
whole of James's note is a navigation change ("Customize ChatGPT" now lives
under Personalization), and navigation never goes on a slide: the current path
is in NOTES.md for the instructor to say aloud, so this deck survives the next
menu move.

The load-bearing slide is "How it works" - the standing instructions and the
message arriving as one flat context. Everything else is in service of it.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "custom-instructions.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Custom Instructions",
        "How a paragraph you write once is attached to every chat you start.")

# ============================================================== WHAT IS IT?
s = d.what("a standing prompt you write once")
m = s.mock(0.40, 1.52, 4.60, 3.58, tag="Every new chat")
m.system("British English. No preamble. I run marketing",
         "at a B2B software firm.")
m.divider()
m.user("Rewrite this launch email.")
with m.bubble():
    m.assistant("The date is the story, not the feature list.",
                "Open on it, then cut the second paragraph.")
m.composer(pin=False)
s.beside(m, "Nobody typed that top line into this chat. It is a short standing "
            "prompt you wrote once and saved, and it is attached to every new "
            "chat you open - so who you are, what you work on and how you want "
            "the answer shaped are in place before your first message.")

s = d.content("Yours to write, not the model's to save")
s.table(0.34, 1.52, 9.32, 2.00, [
    ["", "Custom instructions", "Memory", "Projects"],
    ["Who writes it", "You, once", "The assistant, as you talk",
     "You, per project"],
    ["Where it lands", "Every new chat", "Chats where it is on",
     "Chats inside that project"],
    ["Good for", "Standing rules", "Facts it picked up",
     "One body of work"],
], col_widths=[1.70, 2.62, 2.50, 2.50])
s.caption(0.34, 3.86, 9.32,
          "All three end up in the same place - text in front of the model - so "
          "the difference is who authored it and how far it reaches. Custom "
          "instructions are the only one you write deliberately, and the only "
          "one that follows you into every conversation.")

# ============================================================== HOW IT WORKS
s = d.how("your instructions are prompt text")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("The product's own rules", "set by whoever built it"),
                   ("Your standing instructions", "written once, saved", True),
                   ("Anything memory holds", "if you have it switched on"),
                   ("Your message", "typed just now")], h=0.56)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.60, "One prompt, top to bottom", accent=True)
s.caption(6.50, 2.25, 3.16,
          "The model never reads a settings page. Your instructions are pasted "
          "in above your message, and the whole block is read as one prompt. "
          "They work exactly the way anything you type works - which is why "
          "wording them is a prompting job, not a form to fill in.")

s = d.content("Wording the model can act on")
s.compare(1.52,
          "Does nothing", ["Be smart",
                           "Be professional",
                           "Give me good answers",
                           "Be concise but thorough"],
          "Changes the answer", ["Answer in British English",
                                 "No preamble - open with the answer",
                                 "Flag anything you are unsure of",
                                 "Ask before you assume a figure"],
          h=2.30)
s.caption(0.34, 4.04, 9.32,
          "An instruction is only worth writing if you could tell whether it had "
          "been followed. \"Professional\" describes a feeling; \"no preamble\" "
          "describes an output you can check. Write down the correction you keep "
          "having to make.")

# ============================================================== WHY IT MATTERS
s = d.why("a strong default, not a guarantee")
s.table(0.34, 1.52, 9.32, 1.90, [
    ["", "Without them", "With them"],
    ["Every new chat", "Re-type your context", "It is already there"],
    ["Consistency", "Whatever you re-typed that day",
     "The same baseline every time"],
    ["Failure mode", "Answers drift chat to chat",
     "Applied where they do not fit"],
], col_widths=[2.00, 3.55, 3.75])
s.caption(0.34, 3.66, 9.32,
          "Standing instructions steer the model, they do not bind it. A later "
          "line in the same chat outranks them, a long conversation drifts back "
          "towards the model's own habits, and rules written for your day job "
          "still arrive when you ask about something else. When one of them "
          "matters for this answer, say it again in the message.")

d.two_columns(
    "What earns a place in it",
    ["Who you are and what you work on",
     "The output shape you always want",
     "The correction you keep making",
     "The audience you usually write for"],
    ["Anything true only this week",
     "Detail that belongs to one task",
     "A long brief you will never re-read",
     "Anything you would not want on every chat"],
    left_heading="Write it once",
    right_heading="Say it in the message",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Write two lines", "who you are, how you want answers"),
     ("Open a fresh chat", "ask something ordinary"),
     ("Watch the shape change", "same question, different answer"),
     ("Contradict it in the message", "and watch the later line win")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
