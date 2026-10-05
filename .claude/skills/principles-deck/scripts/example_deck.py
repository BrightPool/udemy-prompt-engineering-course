#!/usr/bin/env python3
"""
Worked example: "Memory" - the principles half of a re-film.

Run:
    uv run --with python-pptx python scripts/example_deck.py out/memory.pptx
    uv run --with python-pptx python scripts/check_deck.py  out/memory.pptx

Read this top-to-bottom before writing your own deck. It shows the full
what / how / why arc and every component in deckkit.

Note there are no divider slides. The arc rides on the slide titles - d.what(),
d.how(), d.why() - so no slide exists purely to announce a section.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "out/memory.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Memory", "How an assistant carries facts about you between conversations.")

# ============================================================== WHAT IS IT?
s = d.what("a store the model writes to")
m = s.mock(0.40, 1.56, 4.60, 3.58)              # ChatGPT / Demonstration
m.user("Remember that I write in British English.")
with m.bubble():
    m.assistant("Saved. I'll use British spelling from now on.")
m.label("Memory updated").line("Writes in British English.", highlight=True)
m.composer(pin=False)
# copy is placed from the mock's final size, so it follows if the mock changes
s.beside(m, "Memory is a small set of facts the assistant saves about you, and "
            "re-reads at the start of every later conversation.")

s = d.content("The same question, a week later")
m = s.mock(0.40, 1.56, 4.60, 3.58, tag="New conversation")
m.user("Draft a one-line product blurb.")
with m.bubble():
    m.assistant("A colour-matched organiser for a tidier desk.")
m.composer(pin=False)
s.beside(m, "Nothing in the second conversation mentions spelling. The preference "
            "arrives from memory, not from the prompt.")

s = d.content("What it is not")
s.compare(1.56,
          "Not this", ["Re-training the model",
                       "A transcript of every chat",
                       "Something you cannot see"],
          "This", ["A short list of facts",
                   "Text, prepended to your prompt",
                   "Editable and deletable"])

# ============================================================== HOW IT WORKS
s = d.how("write, store, retrieve")
s.flow(0.34, 1.52, 9.32,
       [("You say", "something durable"),
        ("It writes", "a short fact"),
        ("It stores", "as plain text"),
        ("It retrieves", "on your next chat")],
       h=1.15, accent_last=True,
       loop="every later conversation starts here")
s.caption(0.34, 3.62, 9.32,
          "Nothing here touches the model's weights. The whole mechanism is a text "
          "file the product writes for you and reads back later.")

s = d.content("What actually reaches the model")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("Retrieved memories", "written weeks ago", True),
                   ("System instructions", "set by the product"),
                   ("Your message", "typed just now")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "One flat context", accent=True)
s.caption(6.50, 1.60, 3.16,
          "The model cannot tell which part you typed and which part came from "
          "the store. That is why a stale memory reads as confidence.")

s = d.content("Where it stops")
m = s.mock(5.10, 1.56, 4.56, 3.10, app="Saved memories", tag="Editable")
m.label("Stored").line("Writes in British English.").line("Works in UTC.")
m.line("Prefers short sentences.")
m.gap(0.06)
m.divider()
m.label("Not stored").line("Full text of past conversations.")
m.line("Anything you deleted.").line("Anything from another vendor's tool.")
m.fit()
s.beside(m, "Memory holds facts, not transcripts. It is opt-in, inspectable and "
            "editable, and it does not follow you to another vendor's tool.")
s.caption(0.34, 4.28, 9.32,
          "You can read the whole store in about a minute. That is the honest test "
          "of how much it knows about you.")

# ============================================================== WHY IT MATTERS
s = d.why("the failure mode inverts")
s.table(0.34, 1.58, 9.32, 1.90, [
    ["", "Without memory", "With memory"],
    ["Repeat setup", "Re-stated every time", "Stated once"],
    ["Consistency", "Drifts between chats", "Holds across chats"],
    ["Failure mode", "Forgetful", "Confidently stale"],
], col_widths=[1.9, 3.6, 3.6])
s.caption(0.34, 3.70, 9.32,
          "An assistant with memory is never blank - it is occasionally wrong with "
          "conviction, which is much harder to notice.")

d.two_columns(
    "When to lean on it",
    ["Stable preferences", "Units, tone, stack", "Facts you'd repeat weekly"],
    ["Anything time-bound", "Anything you'd not repeat to a stranger",
     "One-off task detail"],
    left_heading="Use memory for",
    right_heading="Keep out of memory",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Turn memory on", "and find where it lives"),
     ("Write one memory", "then open a fresh chat"),
     ("Inspect the store", "edit an entry, delete another")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
