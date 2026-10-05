#!/usr/bin/env python3
"""
"ChatGPT Artefacts" - the principles half of the re-film (video 46579771, was "Canvas").

Run:
    uv run --with python-pptx python decks/artefacts/build_artefacts.py \
        decks/artefacts/artefacts.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/artefacts/artefacts.pptx

Spine: a chat reply is disposable prose - to change it you ask again and the whole
thing comes back new. An artefact is a durable document held inside the conversation,
addressed in parts, so a change has somewhere to land. Editing a region instead of
regenerating the whole thing is the mechanism worth teaching.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).with_name("artefacts.pptx"))
d = Deck()

# ---------------------------------------------------------------- open
d.title("ChatGPT Artefacts",
        "How a reply becomes a document you and the assistant edit in place, "
        "instead of prose you regenerate from the top.")

# ============================================================== WHAT IS IT?
s = d.what("a draft you can type into")
m = s.mock(0.40, 1.52, 4.72, 3.50)
m.user("Draft the launch email for the new pricing page.")
with m.bubble():
    m.assistant("Here is the draft.")
    m.gap(0.06)
    m.divider()
    m.label("Draft")
    m.line("Subject: Simpler pricing, from Tuesday")
    m.line("Hi there,")
    m.line("We have cut four tiers down to two.")
m.composer(pin=False)
s.beside(m, "A plain answer is prose in the transcript. An artefact is a document "
            "the reply hands you instead: it holds its own text, it stays where it "
            "is, and you can type into it yourself. You get one by asking for a "
            "draft, or because the assistant judged this was something you would "
            "go on to revise.")

s = d.content("Change one paragraph, not the whole draft")
m = s.mock(0.40, 1.52, 4.72, 3.50)
m.label("Selected in the draft")
m.line("We have cut four tiers down to two.", highlight=True)
m.gap(0.06)
m.user("Say what it saves a team of five.")
with m.bubble():
    m.assistant("Two tiers now, so a team of five stops",
                "paying for seats it never filled.")
    m.gap(0.04)
    m.label("Changed").line("Paragraph 2 only.")
m.fit()
s.beside(m, "Nobody asked for a better email. The ask was a replacement for one "
            "region, so that is all that came back - and the lines you already "
            "liked survive because nothing regenerated them.")

s = d.content("The same object, whatever it holds")
m = s.mock(0.40, 1.52, 4.72, 3.50, app="One artefact", tag="Contents")
m.label("An email")
m.line("Subject: Simpler pricing, from Tuesday")
m.gap(0.06)
m.divider()
m.label("A file of code")
m.line("app.get('/health', (req, res) => {")
m.line("  res.send(readStatus())")
m.line("})")
m.gap(0.06)
m.divider()
m.label("A plan, a spec, a table")
m.line("Anything you would open twice.")
m.fit()
s.beside(m, "An artefact does not care what it holds. Code is only where the stakes "
            "show up fastest: regenerate a file from the top and the fix you made "
            "three turns ago goes with it, quietly.")

s = d.content("Not a nicer-looking answer")
s.compare(1.52,
          "Not this", ["A tidier way to print a chat reply",
                       "A download you go and edit elsewhere",
                       "A second app you switch into"],
          "This", ["A document kept in the conversation",
                   "Edited in place by either of you",
                   "Read back at whatever it now says"],
          h=2.10)
s.caption(0.34, 3.90, 9.32,
          "The point is not that it looks different from a chat reply. It is that "
          "the text now has an identity - the same object next turn, and the turn "
          "after that.")

# ============================================================== HOW IT WORKS
s = d.how("point at a region, replace that region")
s.steps(0.34, 1.52, 5.60, [
    "The reply is kept as a document, apart from the messages.",
    "You point at a part of it, or at the whole draft.",
    "The model returns replacement text for that part.",
    "Everything outside it is left exactly as it was.",
    "The updated document is what the next turn reads.",
], h=0.56, gap=0.13)
s.caption(6.20, 2.62, 3.46,
          "There is no magic here. The whole difference between an artefact and a "
          "chat reply is that a change has an address - and an ask without one "
          "falls back to rewriting everything.")

s = d.content("What the next turn actually reads")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("The document as it now stands", "your own typing included", True),
                   ("The part you pointed at", "or all of it, if you pointed at nothing"),
                   ("The change you asked for", "typed just now")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "A rewrite with an address", accent=True)
s.caption(6.50, 2.43, 3.16,
          "The model cannot see the version you liked two edits ago. It sees the "
          "document as it is now, which is why a line you fixed by hand changes "
          "the answer to your next question.")

s = d.content("The loop has two editors")
s.flow(0.34, 1.52, 9.32,
       [("You edit", "by hand"),
        ("It saves", "as the current draft"),
        ("You ask", "for one change"),
        ("It replaces", "that part only")],
       h=1.40, accent_last=True,
       loop="and the next change starts from what you both left")
s.caption(0.34, 4.05, 9.32,
          "This is the part people miss. Your own typing is not a note in the "
          "margin - it becomes the document, so the assistant's next answer is "
          "built on a draft you changed without telling it.")

s = d.content("Where it stops")
m = s.mock(5.10, 1.52, 4.56, 3.10, app="One artefact", tag="Boundaries")
m.label("It holds")
m.line("The text as it now stands.")
m.line("The edits you typed yourself.")
m.line("Whatever the last change left behind.")
m.gap(0.06)
m.divider()
m.label("It does not hold")
m.line("A draft you replaced without copying.")
m.line("Anything from another conversation.")
m.line("Your very last keystroke, until it saves.")
m.fit()
s.beside(m, "An artefact is a current version, not an archive. Saving trails your "
            "typing by a moment, a temporary conversation may keep none of it, and "
            "a draft you overwrite is simply gone - so when one is good, take a "
            "copy before you ask for the next change.")

# ============================================================== WHY IT MATTERS
s = d.why("you stop losing the good parts")
s.table(0.34, 1.52, 9.32, 2.30, [
    ["", "A plain reply", "An artefact"],
    ["Unit of change", "The whole answer", "The part you point at"],
    ["Your good lines", "Rewritten with the rest", "Left exactly as they were"],
    ["Where work lives", "Scattered down the transcript", "One document, current version"],
    ["Failure mode", "Scrolling back for the good draft", "Editing a draft that moved"],
], col_widths=[1.9, 3.6, 3.6])
s.caption(0.34, 4.10, 9.32,
          "The cost is attention. Because the object keeps changing under you, the "
          "draft you are arguing with is not always the draft you last read.")

d.two_columns(
    "How you ask decides how much changes",
    ["Tighten the second paragraph.",
     "Swap the opening line for one that names the price.",
     "Rename this function, leave its callers alone."],
    ["Make it better.",
     "Try again.",
     "Rewrite this properly."],
    left_heading="Changes one region",
    right_heading="Regenerates the lot",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Open a draft", "and edit it by hand"),
     ("Point at one paragraph", "then ask for that paragraph only"),
     ("Ask vaguely on purpose", "and watch the whole thing come back new")],
    lead="That is the principle. Now we make one and edit it live.",
)

d.save(out)
print(f"wrote {out}")
