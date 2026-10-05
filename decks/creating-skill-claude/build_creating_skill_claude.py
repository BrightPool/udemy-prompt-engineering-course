#!/usr/bin/env python3
"""
"Creating a Skill in Claude Cowork" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/creating-skill-claude/build_creating_skill_claude.py \
        decks/creating-skill-claude/creating-skill-claude.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/creating-skill-claude/creating-skill-claude.pptx

The angle: the anatomy of a skill is taught generically in the ChatGPT lecture, so
this one carries the idea that is genuinely load-bearing and genuinely Anthropic's
framing - progressive disclosure. Only every skill's name and description are always
in front of the model; everything else is read from the folder when the job needs it.
The worked example is real: the principles-deck skill in this repository, which built
this very deck.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else "decks/creating-skill-claude/creating-skill-claude.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Creating a Skill in Claude Cowork",
        "How a folder of instructions and files turns Claude into a specialist "
        "for one job you keep repeating.")

# ============================================================== WHAT IS IT?
s = d.what("a folder you hand Claude, not a box you type into")
m = s.mock(0.40, 1.56, 4.72, 3.40, app="Skill folder", tag="Example")
m.label("The folder")
m.line("principles-deck/")
m.line("     SKILL.md")
m.line("     references/")
m.line("     scripts/")
m.line("     assets/")
m.gap(0.08)
m.divider()
m.label("The only compulsory part")
m.line("SKILL.md, holding a name and a description", highlight=True)
m.fit()
s.beside(m, "A prompt is text you send once. A skill is a folder Claude keeps to "
            "hand. One file in it is compulsory: it names the job and says when "
            "to do it. Everything else is there because that job needs it.")

s = d.content("The skill that built these slides")
s.table(0.34, 1.56, 9.32, 2.44, [
    ["What is in it", "Written as", "When it loads"],
    ["A name and a description", "two lines of prose", "always"],
    ["The instructions", "a page of plain English", "when a request matches"],
    ["The reference material", "a shelf of documents", "if a step calls for one"],
    ["The tools", "scripts and a template", "run or opened, never read"],
], col_widths=[2.7, 3.3, 3.3])
s.caption(0.34, 4.22, 9.32,
          "Every deck in this course re-film came out of that folder. The two parts "
          "that matter most, the description and the instructions, are ordinary "
          "prose: you do not have to write the scripts to build a skill.")

s = d.content("What a skill is not")
s.compare(1.56,
          "Not this", ["Teaching the model something new",
                       "Text you paste in again each time",
                       "Something you carry into every chat"],
          "This", ["Instructions it opens when relevant",
                   "A folder that stays where it is",
                   "Opened only when the job matches it"])

# ============================================================== HOW IT WORKS
# The mechanism itself belongs to "What are Skills?", which runs first in this
# section. These three slides teach what that mechanism means for the person
# writing the skill - what to put in the folder, how to shape the page, and how
# to write a description you can actually test.
s = d.how("you write a page, and bundle everything else")
s.table(0.34, 1.56, 9.32, 2.10, [
    ["", "The instruction page", "The bundled files"],
    ["What goes there", "the steps of the job", "the detail behind one step"],
    ["How long", "about a page", "as long as they need to be"],
    ["Your test", "would you say it every time?", "would you say it only sometimes?"],
], col_widths=[2.0, 3.7, 3.6])
s.caption(0.34, 3.92, 9.32,
          "Be generous with the folder and mean with the page. Every line of the "
          "instruction page is read in full each time the skill fires, so a page "
          "that says too much is worse than one that says less and points at the "
          "shelf behind it.")

s = d.content("The instruction page is a table of contents")
m = s.mock(0.40, 1.56, 4.90, 3.30, app="The instruction page", tag="Example")
m.label("The steps")
m.line("Write the arc, then build it with the kit.")
m.line("Lint it. Review it twice. Fix what you find.")
m.gap(0.08)
m.divider()
m.label("Where the detail lives")
m.line("For the house style, see the style spec.")
m.line("For a mock window, see the recipe book.")
m.line("For the review, see the two-round rubric.")
m.fit()
s.beside(m, "Our own skill's instructions are barely more than the steps of the "
            "job and a set of pointers. Write those pointers for a colleague who "
            "has not opened the folder, because that is what Claude is.")

s = d.content("Writing a description you can test")
s.steps(0.34, 1.56, 5.80, [
    "Write it in the third person, not as \"I can\".",
    "Say what it does and when to reach for it.",
    "Use the words you would actually type.",
    "Read it beside your other skills' descriptions.",
    "Test it: ask for the job without naming it.",
], h=0.56, gap=0.14)
s.caption(6.50, 1.62, 3.16,
          "The last step is the only one that tells you anything.\n\nIf the skill "
          "does not fire, the description is not describing the request you "
          "actually make. Change the description, not the request.")

s = d.content("Where a skill stops")
m = s.mock(5.02, 1.56, 4.64, 3.20, app="Scope of a skill", tag="Boundaries")
m.label("What it changes")
m.line("How Claude does a job you repeat")
m.line("Which files and scripts it reaches for")
m.gap(0.08)
m.divider()
m.label("What it does not")
m.line("The model itself, or what it knows")
m.line("Anything, if the description never matches")
m.line("Its own trustworthiness: you vouch for it")
m.line("Installing itself everywhere you work")
m.fit()
s.beside(m, "A skill is instructions and code, so it inherits their risks. It runs "
            "with the access you have. Install skills you wrote, or ones you trust, "
            "exactly as you would treat software.")

# ============================================================== WHY IT MATTERS
s = d.why("it carries what a prompt cannot")
s.table(0.34, 1.56, 9.32, 2.44, [
    ["", "A saved prompt", "A skill"],
    ["What it holds", "one block of text",
     "instructions plus the files they need"],
    ["When it arrives", "when you remember to paste it",
     "when the job matches its description"],
    ["Repeatability", "as good as your memory", "the same steps every time"],
    ["Failure mode", "forgotten, or half pasted",
     "fires on the wrong job, or never fires"],
], col_widths=[2.1, 3.5, 3.7])
s.caption(0.34, 4.22, 9.32,
          "Both can go wrong. The difference is that a skill goes wrong in one "
          "place you can open, so you fix it once and every later job is fixed too.")

s = d.content("Written once, used in more than one place")
s.flow(0.34, 1.56, 9.32, [
    ("Write it once", "as a folder"),
    ("Add it where you work", "each place, once"),
    ("Hand the folder on", "and a colleague has it too"),
], h=1.45, accent_last=True)
s.caption(0.34, 3.36, 9.32,
          "Anthropic published the format as an open standard, so the same folder "
          "can sit in Claude Cowork, in a chat, in Claude Code, and in other agent "
          "products that adopted it. What travels is the folder, not the "
          "installation: you add it once in each place you want it.")

d.two_columns(
    "When a skill earns its place",
    ["A job you repeat", "Work with a house standard",
     "Steps you keep re-explaining", "Anything with files attached to it"],
    ["A one-off request", "Something you do once a year",
     "A preference that belongs in your settings",
     "Work you cannot yet describe"],
    left_heading="Make one for",
    right_heading="Do not bother for",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Name the job", "one thing you repeat"),
     ("Write the description", "what it does, and when"),
     ("Add the files it needs", "a reference, a template"),
     ("Trigger it by accident", "without naming the skill")],
    lead="That is the principle. Now we build one in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
