#!/usr/bin/env python3
"""
"Memory" - the principles half of the re-film (video 48151545, 02:28).

Build:
    uv run --with python-pptx python decks/memory/build_memory.py decks/memory/memory.pptx
Lint:
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/memory/memory.pptx

The deck teaches what memory *is*; the instructor demos memory in the product separately.
No menu paths, no toggle names, no vendor build details - see decks/memory/NOTES.md
for the current navigation, which James says aloud in the demo half.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "decks/memory/memory.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Memory",
        "How an assistant carries what it knows about you from one conversation "
        "into the next.")

# ============================================================== WHAT IS IT?
s = d.what("a short profile of you, kept in writing")
m = s.mock(0.40, 1.56, 4.60, 3.58, app="Memory", tag="What it holds")
m.label("Preferences")
m.line("Writes in British English.", highlight=True)
m.line("Prefers short, direct answers.")
m.gap(0.06)
m.divider()
m.label("Your work")
m.line("Runs a two-person consultancy.")
m.line("Sells to technical buyers.")
m.gap(0.06)
m.divider()
m.label("Standing constraints")
m.line("Never invents a statistic.")
m.fit()
s.beside(m, "Memory is a small profile of you that the assistant writes and keeps - "
            "plain sentences, not a database and not a transcript, that "
            "it reads back before it answers.")

s = d.content("Nobody typed this into the prompt")
m = s.mock(0.40, 1.56, 4.60, 3.58, tag="A week later")
m.user("Draft the launch email.")
with m.bubble():
    m.assistant("Subject: Simpler pricing, from Monday",
                "We have reorganised our plans so you can",
                "see exactly what you are paying for.")
m.label("Drawn from memory").line("British English, technical buyers", highlight=True)
m.composer(pin=False)
s.beside(m, "This conversation never mentions spelling or audience. Both arrived "
            "from memory. Personalisation you cannot see in the prompt is still "
            "personalisation.")

s = d.content("What it is not")
s.compare(1.56,
          "Not this", ["The model learning about you",
                       "Your chat history, which is separate",
                       "A black box you cannot open"],
          "This", ["A few written lines about you",
                   "Placed in front of your question",
                   "Readable, correctable, deletable"])
s.caption(0.34, 4.32, 9.32,
          "Your conversations are kept and searchable in their own right, and the "
          "assistant can be allowed to draw on them - that is a separate setting.\n"
          "Memory is the short written summary, and nothing here touches the "
          "model's weights.")

# ============================================================== HOW IT WORKS
s = d.how("two doors into the same memory")
s.node(0.34, 1.56, 2.70, 1.00, "You tell it", sub="\"Remember that...\"")
s.node(0.34, 2.91, 2.70, 1.00, "It infers", sub="from ordinary chats")
s.arrow(3.14, 2.00, 0.72, 0.12)
s.arrow(3.14, 3.35, 0.72, 0.12)
s.node(3.95, 1.56, 2.55, 2.35, "Memory", sub="a few written lines")
s.arrow(6.62, 2.675, 0.62, 0.12)
s.node(7.32, 2.16, 2.34, 1.15, "Every later chat",
       sub="opens with those lines", accent=True)
s.caption(0.34, 4.16, 9.32,
          "One door is precise and you chose it. The other is convenient and you did "
          "not. They write to the same memory, which is why reading it now and again is "
          "the only way to know what the assistant believes about you.")

s = d.content("What arrives before you type")
bottom = s.layers(0.34, 1.56, 5.90,
                  [("Lines pulled from memory", "chosen for this question", True),
                   ("Standing instructions", "set once, applied always"),
                   ("Your message", "typed just now")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "Assembled, then sent", accent=True)
s.caption(6.50, 1.56, 3.16,
          "Only the lines judged relevant get pulled in, so \"it forgot\" usually "
          "means it did not pull that line, not that memory lost it.\n\n"
          "Once assembled, the model cannot tell which part you typed.")

s = d.content("Facts have a tense")
s.flow(0.34, 1.56, 9.32,
       [("You mention", "a trip in July"),
        ("It stores", "a plan"),
        ("July passes", "the line is now false"),
        ("It revises", "to a past trip")],
       h=1.22, accent_last=True,
       loop="or you revise a line yourself, by saying so in any chat")
s.caption(0.34, 3.90, 9.32,
          "Preferences age well. Dated facts do not. Memory nobody revises does not "
          "go blank, it goes quietly wrong, and the assistant applies the wrong line "
          "with exactly the confidence it applies the right ones.")

s = d.content("Where it stops")
m = s.mock(5.10, 1.56, 4.56, 3.10, app="Memory", tag="Scope")
m.label("Reads and writes")
m.line("Your ordinary conversations.")
m.line("Chats you scope to one project.")
m.line("Anything you ask it to keep.")
m.gap(0.06)
m.divider()
m.label("Does neither")
m.line("A conversation marked temporary.")
m.line("Any chat once you switch it off.")
m.line("Another vendor's assistant.")
m.fit()
s.beside(m, "Memory is opt-in, and how far it reaches is yours to set. You can hold it "
            "to a single project, or have a conversation that neither reads memory "
            "nor writes to it.")

# ============================================================== WHY IT MATTERS
s = d.why("forgetting is not the risk")
s.table(0.34, 1.56, 9.32, 2.24, [
    ["", "Without memory", "With memory"],
    ["Set-up", "Re-stated every time", "Stated once"],
    ["Answers", "Generic by default", "Shaped to your situation"],
    ["What goes wrong", "It forgets", "It remembers something untrue"],
    ["When you notice", "Straight away", "Only if you read memory"],
], col_widths=[2.1, 3.4, 3.8])
s.caption(0.34, 4.04, 9.32,
          "Forgetting announces itself. A stale line does not: it bends every answer "
          "slightly until somebody opens memory and deletes it. That is what "
          "memory costs you - something you have to maintain.")

d.two_columns(
    "What belongs in memory",
    ["Standing preferences - tone, spelling, units",
     "Facts about your work you would repeat weekly",
     "Constraints that apply to everything you ask"],
    ["Detail from one task you will not repeat",
     "A conclusion you have not checked yet",
     "Anything you would not want read aloud"],
    left_heading="Worth keeping",
    right_heading="Keep out",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Open memory", "and read what it already holds"),
     ("Say one thing worth keeping", "then start a fresh chat"),
     ("Correct a line", "and delete another")],
    lead="That is the principle. Now we open memory and edit it live.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
