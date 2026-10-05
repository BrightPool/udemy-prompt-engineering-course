#!/usr/bin/env python3
"""
"Projects" - the principles half of the re-film.

Run:
    uv run --with python-pptx python \
        decks/projects/build_projects.py decks/projects/projects.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/projects/projects.pptx

James's note is a navigation change (creating a project now starts from the +
symbol), and navigation never goes on a slide - it lives in NOTES.md for the
demo half.

The load-bearing slide is "Two rings of context": account-wide settings sit in
the outer ring and follow you everywhere, project instructions and files sit in
the inner one and stop at its edge. Memory and Custom Instructions are separate
lectures, so they appear here only as the outer ring - this deck teaches the
boundary, not the settings.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import Deck, ACCENT, RULE, SOFT_INK, BODY_FONT  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "projects.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Projects",
        "How related chats share one brief, one shelf of files and one place "
        "to live.")

# ============================================================== WHAT IS IT?
s = d.what("a folder of chats with a brief attached")
m = s.mock(0.40, 1.52, 4.60, 3.58, app="Website relaunch", tag="Project")
m.label("Project instructions")
m.line("Plain English, no jargon. We sell to")
m.line("plumbers, not to developers.")
m.gap(0.06)
m.divider()
m.label("Files kept here")
m.line("brand-guidelines.pdf")
m.line("current-site-pages.csv")
m.gap(0.06)
m.divider()
m.label("Chats in this project")
m.line("Homepage headline options")
m.line("Rewrite the services page")
m.line("Questions for the developer")
m.fit()
s.beside(m, "A project is a folder that holds a set of related chats, together "
            "with the instructions and files all of those chats should share. "
            "Those standing instructions are the project's brief, and every "
            "chat you open inside the folder starts with it already in place.")

s = d.content("Nobody pasted the brief into this chat")
m = s.mock(0.40, 1.52, 4.60, 3.58, tag="In the project")
m.user("Write a headline for the services page.")
with m.bubble():
    m.assistant("Blocked drains sorted the same day.",
                "Plain words, and it names the job.")
m.composer(pin=False)
s.beside(m, "One line of typing, and the answer still follows the tone rule and "
            "the brand file. Both came from the folder, and both will be there "
            "for the next chat you start in it and the one after that.")

s = d.content("What it is not")
s.compare(1.52,
          "Not this", ["A cleverer model for serious work",
                       "Only a tidier sidebar",
                       "A wall your settings cannot cross"],
          "This", ["The same model, better briefed",
                   "Shared instructions and files",
                   "A smaller circle inside a bigger one"],
          h=2.10)
s.caption(0.34, 3.86, 9.32,
          "Tidiness is the reason most people open their first project, and it "
          "is the smallest thing a project does. The chats inside it are "
          "working from a brief the chats outside it never see.")

# ============================================================== HOW IT WORKS
s = d.how("every chat in here starts pre-briefed")
s.flow(0.34, 1.52, 9.32,
       [("You open a chat", "inside the project"),
        ("It picks up", "the project's brief"),
        ("It can reach", "the files kept here"),
        ("It answers", "in that context")],
       h=1.35, accent_last=True,
       loop="a chat you started outside can be moved in, and starts here too")
s.caption(0.34, 3.85, 9.32,
          "Nothing about the model changes when you step inside a project. What "
          "changes is what arrives alongside your message: the brief you wrote "
          "for this strand of work, and the files you left here for it.")

s = d.content("Two rings: your account, and this project")
# outer ring - the account
s.rect(0.34, 1.52, 9.32, 3.00, rounded=True, radius=0.08, line=RULE, line_w=0.75)
s.text(0.54, 1.62, 4.00, 0.24, "Everywhere: your account",
       size=12, color=SOFT_INK, font=BODY_FONT, bold=True)
s.node(0.54, 2.34, 2.44, 0.58, "Custom instructions", sub="written once")
s.node(0.54, 3.04, 2.44, 0.58, "Memory", sub="facts it saved")
s.node(0.54, 3.74, 2.44, 0.58, "Every other chat", sub="the rest of your history")
# inner ring - this project
s.rect(3.34, 1.92, 6.10, 2.44, rounded=True, radius=0.06,
       line=ACCENT, line_w=1.0)
s.text(3.54, 2.00, 4.00, 0.24, "Only here: this project",
       size=12, color=ACCENT, font=BODY_FONT, bold=True)
s.node(3.54, 2.34, 5.70, 0.56, "Project instructions",
       sub="the brief for this work only")
s.node(3.54, 3.00, 5.70, 0.56, "Project files",
       sub="the same references in every chat here")
s.node(3.54, 3.66, 5.70, 0.56, "The chats you keep here",
       sub="each one can build on the others")
s.caption(0.34, 4.62, 9.32,
          "The outer ring follows you everywhere. The inner one stops at the "
          "folder, and where the two disagree the more specific brief is the "
          "one that wins.")

s = d.content("Where the memory boundary sits")
s.compare(1.52,
          "Open", ["What it knows about you comes in",
                   "This work can inform later chats",
                   "Good for ordinary, everyday work"],
          "Sealed", ["Only chats in this folder count",
                     "Nothing in here goes back out",
                     "Good for client or private work"],
          h=2.10)
s.caption(0.34, 3.86, 9.32,
          "Whether a project can see the rest of your account, and whether the "
          "rest of your account can see the project, is a choice about the "
          "project as a whole, and it is worth making before you start filling "
          "it. Sealing the folder buys privacy and a clean slate, and costs "
          "you everything the assistant already knew.")

s = d.content("Where it stops")
m = s.mock(5.06, 1.52, 4.54, 3.30, app="Project scope", tag="Boundaries")
m.label("Carried into every chat")
m.line("The instructions you wrote for it")
m.line("The files you left in it")
m.line("What earlier chats here settled")
m.gap(0.06)
m.divider()
m.label("Not carried")
m.line("Chats you started outside it")
m.line("A full read of every file, every time")
m.line("Anything, once you leave the tool")
m.fit()
s.beside(m, "A project holds a limited number of files, and how many depends on "
            "your plan. The assistant does not read all of them every time "
            "either: it looks for the parts that match what you asked, so a "
            "file sitting in the folder is not the same as a file being read.")

# ============================================================== WHY IT MATTERS
s = d.why("one assistant, several jobs")
s.table(0.34, 1.52, 9.32, 2.30, [
    ["", "One long list of chats", "Chats grouped in a project"],
    ["Starting a chat", "Paste the background again",
     "The background is already there"],
    ["Finding it later", "Scroll, and search by memory",
     "It is in the folder you put it in"],
    ["Next time round", "Rebuild the setup from scratch",
     "Re-open the project you built"],
    ["Failure mode", "Every chat starts cold",
     "The wrong brief, quietly applied"],
], col_widths=[2.10, 3.50, 3.72])
s.caption(0.34, 4.06, 9.32,
          "A brief that is always on is also on when it does not fit, and a "
          "project set up for last year's version of the work keeps applying "
          "it until somebody edits the brief. That is what a project costs "
          "you: something to keep current.")

d.two_columns(
    "What deserves a project of its own",
    ["Work that runs for weeks",
     "Anything with its own files",
     "A client, a launch, a move",
     "A tone you want only here"],
    ["A one-off question",
     "Something you will not revisit",
     "Work with no shared background",
     "A brief that changes weekly"],
    left_heading="Set it up once",
    right_heading="Leave it in an ordinary chat",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Create a project", "name it after one job"),
     ("Give it a brief", "and one file to work from"),
     ("Ask it something", "the brief arrives too"),
     ("Move a chat in", "from outside the folder")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
