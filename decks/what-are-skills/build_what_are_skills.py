#!/usr/bin/env python3
"""
"What are Skills?" - the principles half of a new lecture.

Run:
    uv run --with python-pptx python decks/what-are-skills/build_what_are_skills.py \
        decks/what-are-skills/what-are-skills.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/what-are-skills/what-are-skills.pptx

This is the first lecture in the Skills & Plugins section, so it teaches the
concept only - building one is the next lecture, and the connector protocol is
the one after that. The arc rides on the slide titles.

Two things the deck exists to land:
  1. A prompt is something you type this time. A skill is something the
     assistant has. Naming it is the whole change.
  2. A skill loads when its description matches what you are doing, which is
     why the description is the most important line in it.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "what-are-skills.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("What are Skills?",
        "How an instruction you keep re-typing becomes something the assistant "
        "already has.")

# ============================================================== WHAT IS IT?
s = d.what("instructions the assistant already has")
m = s.mock(0.40, 1.52, 4.60, 3.58, generic=True)
m.user("Review this launch email.")
with m.bubble():
    m.assistant("Checked against our house style: three passive")
    m.line("sentences, two words we avoid, no sign-off.")
m.divider()
m.label("Skill used")
m.line("house-style-check", highlight=True)
m.composer(pin=False)
s.beside(m, "A skill is a named set of instructions, kept somewhere the assistant "
            "can read. Nobody pasted the house style into that message. It was "
            "already there; the assistant saw that the request was the kind this "
            "skill covers, and applied it.")

s = d.content("A prompt, or a skill")
s.compare(1.52,
          "A prompt - typed this time",
          ["Lives inside one message",
           "Gone when the chat ends",
           "Re-typed the next time",
           "Improves only if you redo it"],
          "A skill - kept by the assistant",
          ["Lives in a file, under a name",
           "There in every conversation",
           "Named, or matched to the task",
           "Improve it once, everywhere"],
          h=2.14)
s.caption(0.34, 3.86, 9.32,
          "Often the very same words. What changes is their status: written "
          "down under a name, they stop being something you supply each time "
          "and become something the tool carries.")

s = d.content("What is inside one")
gap, w = 0.24, (9.32 - 0.24 * 3) / 4
for i, (label, sub) in enumerate([
        ("A name", "what you call it by"),
        ("A description", "when it should apply"),
        ("The instructions", "what to do, in order"),
        ("Its resources", "the files it needs")]):
    s.node(0.34 + i * (w + gap), 1.52, w, 1.16, label, sub=sub)
s.arrow(4.90, 2.78, 0.20, 0.22, direction="down")
s.node(0.34, 3.14, 9.32, 0.60,
       "One bundle, stored where the assistant can reach it", accent=True)
s.caption(0.34, 3.94, 9.32,
          "The major assistants have settled on this same shape, so the idea "
          "travels between them. And note what a bundle allows: it can carry a "
          "script that runs on your behalf, so a skill written by a stranger "
          "deserves the care you would give any other software you install.")

s = d.content("A skill is not a connector")
s.table(0.34, 1.52, 9.32, 1.96, [
    ["", "A skill", "A connector"],
    ["What it is", "Instructions and files you wrote", "A link to a system you already use"],
    ["What it changes", "How the job gets done", "What the assistant can reach"],
    ["Ask yourself", "\"How should this be done?\"", "\"Where does the work live?\""],
], col_widths=[1.9, 3.6, 3.8])
s.caption(0.34, 3.72, 9.32,
          "This is the one people get backwards, so hold the line: a skill is "
          "instructions, a connector is plumbing. They work together - a skill "
          "can tell the assistant to go and fetch something through a connector "
          "- but it is still the skill that decides what to do with whatever "
          "comes back.")

# ============================================================== HOW IT WORKS
s = d.how("matched by description, loaded on demand")
s.steps(0.34, 1.52, 5.60, [
    "You write it once, where the assistant can see it.",
    "Its name and description are always loaded.",
    "What you ask matches - or you name the skill yourself.",
    "Only then are the full instructions read.",
])
s.caption(6.30, 1.99, 3.36,
          "Nothing here is trained and nothing is remembered. The assistant "
          "opens a file at the moment it becomes relevant, the way you turn to "
          "the right page of a handbook - which also means a skill is "
          "instructions, not a guarantee that they are followed.")

s = d.content("Two ways a skill starts")
s.compare(1.52,
          "It matches what you asked",
          ["You describe the task yourself",
           "Weighed against each description",
           "The one that fits is loaded"],
          "You call it by name",
          ["You name the skill outright",
           "No matching, no judgement",
           "For work that must not vary"],
          h=1.90)
s.caption(0.34, 3.62, 9.32,
          "Both routes end in the same place; the difference is who decided. "
          "Lean on the first and the description is doing all the work for you - "
          "which is why a skill you can never get to fire is usually not a "
          "writing problem but a labelling one.")

s = d.content("What is loaded, and when")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("Every name and description", "always loaded", True),
                   ("The instructions that matched", "read on demand"),
                   ("A reference file", "only when opened"),
                   ("A bundled script", "runs; the result returns")], h=0.54)
s.arrow(3.10, bottom + 0.04, 0.30, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.58, "Only what this job needed", accent=True)
s.caption(6.50, 2.54, 3.16,
          "Twenty skills cost about what one costs, right up until one of them "
          "is used. "
          "A name and a line of description is all a skill takes up while it "
          "waits - so length is not what makes a skill expensive.")

s = d.content("The description is the line that decides")
r = s.message_row(0.34, 1.52, 9.31, 0.66)
r.label("What it does. Not when.")
r.line("description: Checks a draft against our house style guide.")
r = s.message_row(0.34, 2.40, 9.31, 1.12)
r.label("What it does, and when")
r.line("description: Checks a draft against our house style guide.")
r.line("Use when asked to review, edit or proofread copy, or when", highlight=True)
r.line("a draft is going out to a customer.")
s.caption(0.34, 3.72, 9.32,
          "The same skill, one clause apart. The first fires only when you "
          "happen to use its own words back at it. The second names the "
          "situations it belongs in - and that second half is what turns a "
          "description into a trigger.")

# ============================================================== WHY IT MATTERS
s = d.why("the instructions stop drifting")
s.table(0.34, 1.52, 9.32, 2.46, [
    ["", "Typed each time", "Written as a skill"],
    ["Where it lives", "In your head, or an old chat", "In one file, under a name"],
    ["What you get", "Whatever you remembered", "The same instructions each run"],
    ["Improving it", "Rewrite it from memory", "Edit the file once"],
    ["Sharing it", "Paste a paragraph", "Hand over the bundle"],
    ["Failure mode", "You forget a rule", "It fires when you did not want it"],
], col_widths=[1.9, 3.6, 3.6])
s.caption(0.34, 4.14, 9.32,
          "The failure mode is the row to remember. Written too broadly, a skill "
          "turns up in work it has nothing to do with; described too vaguely, it "
          "never turns up at all. Both are fixed in the same line.")

d.two_columns(
    "When to write one down",
    ["You have typed it more than twice",
     "It has rules a new colleague would need",
     "It needs a template, a checklist or a file",
     "Other people need the same result"],
    ["A one-off question",
     "Something you are still working out",
     "Work where you want a fresh angle each time"],
    left_heading="Worth a skill",
    right_heading="Just type it",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Open a real skill", "name, description, instructions"),
     ("Call it by name", "and watch it load"),
     ("Ask for the job", "let the description find it"),
     ("Then weaken that line", "and see it stop firing")],
    lead="That is the principle. Now we open a real one and use it.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
