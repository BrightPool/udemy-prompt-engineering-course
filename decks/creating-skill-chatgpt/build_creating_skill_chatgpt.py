#!/usr/bin/env python3
"""
"Creating a skill in ChatGPT" - the principles half of a new lecture.

Presentation-led: this deck carries most of the teaching, and the instructor
demos the authoring loop live afterwards.

Run:
    uv run --with python-pptx python decks/creating-skill-chatgpt/build_creating_skill_chatgpt.py \
        decks/creating-skill-chatgpt/creating-skill-chatgpt.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/creating-skill-chatgpt/creating-skill-chatgpt.pptx
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else ROOT / "decks/creating-skill-chatgpt/creating-skill-chatgpt.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Creating a Skill in ChatGPT",
        "How a routine you repeat every week becomes one instruction - and what "
        "has to be connected before it can run.")

# ============================================================== WHAT IS IT?
s = d.what("a routine you already repeat, written down once")
m = s.mock(0.40, 1.56, 5.00, 3.40)
m.user("Every Monday I take the client call notes",
       "out of Drive and write them up as a status",
       "update in our house format.")
with m.bubble():
    m.assistant("I can save that as a skill.",
                "Name, description, the steps, and your format.")
m.label("Saved").line("weekly-client-status", highlight=True)
m.composer(pin=False)
s.beside(m, "You are not writing software. You are dictating a procedure you "
            "already know, so the assistant can re-read it next week instead "
            "of asking you again.")

s = d.content("The two halves of one workflow")
s.node(0.34, 1.56, 4.40, 1.32, "The skill",
       sub="the steps, the format, and the words that make it fire")
s.node(5.26, 1.56, 4.40, 1.32, "The connector",
       sub="an authorised link to a folder, an inbox, a calendar")
s.arrow(2.42, 2.96, 0.22, 0.30, direction="down")
s.arrow(7.34, 2.96, 0.22, 0.30, direction="down")
s.node(0.34, 3.36, 9.32, 0.70,
       "Neither half is much use on its own", accent=True)
s.caption(0.34, 4.24, 9.32,
          "The skill knows the how and nothing about your files. The connector "
          "reaches your files and knows nothing about your format. One vendor "
          "bundles the pair and calls it a plugin - the two halves are the same "
          "either way.")

s = d.content("What you decide when you write one")
s.table(0.34, 1.56, 9.32, 2.42, [
    ["The part", "The question it answers", "Get it wrong and"],
    ["Name", "What do I call this routine?", "you cannot find it again"],
    ["Description", "When should this fire?", "it never runs, or runs uninvited"],
    ["Instructions", "What are the steps, in order?", "the output drifts each run"],
    ["Resources", "What files must it carry?", "it invents your format"],
], col_widths=[1.7, 3.9, 3.7])
s.caption(0.34, 4.18, 9.32,
          "Four decisions. Whether you type them into a form yourself or let the "
          "assistant draft them from a conversation, these are the four you are "
          "signing off - and every tool that offers skills asks for them.")

# ============================================================== HOW IT WORKS
s = d.how("do the job once, then save what worked")
s.flow(0.34, 1.56, 9.32,
       [("Do the job", "once, in an ordinary chat"),
        ("Ask for it saved", "as a skill"),
        ("Read the four parts", "before you keep it"),
        ("Try it", "in a fresh conversation")],
       h=1.20, accent_last=True,
       loop="anything that did not fire comes back as a sharper description")
s.caption(0.34, 3.90, 9.32,
          "The best source for a skill is a conversation where the work already "
          "came out right. Save that, then cut it back to the steps that mattered.")

s = d.content("Why one description fires and another does not")
s.compare(1.56,
          "Too vague to match",
          ["\"Helps with client reporting\"",
           "No words you would ever type",
           "Describes your job, not the task"],
          "Specific enough to match",
          ["\"Call notes into a status update\"",
           "Names the words you would type",
           "Says when not to use it"],
          h=2.34)
s.caption(0.34, 4.10, 9.32,
          "The description is the only part read before the skill runs; the "
          "instructions stay invisible until it fires. A skill that never "
          "triggers is worse than no skill, because you think it is working.")

s = d.content("The test is a sentence you did not write")
m = s.mock(0.40, 1.56, 5.00, 3.40, tag="New conversation")
m.user("Can you write up Thursday's call with the Hendersons?")
m.label("Matched").line("weekly-client-status", highlight=True)
with m.bubble():
    m.assistant("Notes pulled from the client folder.",
                "Status update drafted in the house format.")
m.composer(pin=False)
s.beside(m, "Nobody named the skill. The assistant matched this sentence "
            "against the description.\n"
            "So test in the words a colleague would use, not the ones you "
            "wrote it with.\n"
            "You can name it outright. You will not remember to.")

s = d.content("A Monday morning, end to end")
s.flow(0.34, 1.56, 9.32,
       [("You ask", "in one sentence"),
        ("The skill loads", "steps and format"),
        ("The connector fetches", "the notes you named"),
        ("It files the result", "back where it belongs")],
       h=1.45, accent_last=True)
s.caption(0.34, 3.40, 9.32,
          "Same shape for filing an invoice, chasing a signature, or turning a "
          "spreadsheet into the weekly summary. The routine is ordinary office "
          "work - what changed is that you describe it once instead of doing it.")

s = d.content("What connecting an account actually grants")
m = s.mock(5.05, 1.56, 4.60, 3.30, tag="Approval")
m.system("Wants to read the notes in your client folder")
m.line("Weekly call notes - Hendersons")
m.gap(0.06)
m.divider()
m.system("Wants to save a new file to that folder")
m.line("Client status - Hendersons")
m.gap(0.06)
m.divider()
m.label("Your call").line("Allow this once, or from now on.")
m.fit()
s.beside(m, "A connector is reach into a real account, not a copy of it. "
            "Reading happens quietly; anything with consequences should stop "
            "and ask.\n"
            "Connect one folder, not everything you own - and assume it can "
            "read whatever you pointed it at.")

# ============================================================== WHY IT MATTERS
s = d.why("the routine stops being re-explained")
s.table(0.34, 1.56, 9.32, 2.30, [
    ["", "Without a skill", "With a skill"],
    ["Setting the job up", "Re-typed every time", "Written down once"],
    ["The format", "Drifts between runs", "Comes from the file it carries"],
    ["Handover", "Lives in your head", "Someone else can run it"],
    ["Failure mode", "Inconsistent output", "Fires when you did not want it"],
], col_widths=[1.9, 3.6, 3.6])
s.caption(0.34, 4.06, 9.32,
          "The honest cost: a skill that is subtly wrong is wrong every single "
          "run, and quietly. Read what it produced for the first few weeks "
          "before you stop reading.")

s = d.content("One person writes it, the team runs it")
s.steps(0.34, 1.56, 5.30,
        ["Write it once, from a job that went well.",
         "Share it, and the team runs your version.",
         "Their accounts and permissions, not yours.",
         "Installing someone else's installs their instructions."],
        h=0.66)
s.caption(6.00, 2.40, 3.66,
          "A shared skill is not a document. It is instructions an assistant "
          "will follow while connected to real accounts, so read one before you "
          "install it - the same care you would give any file from outside the "
          "company.")

d.two_columns(
    "When a routine is worth writing down",
    ["A job you repeat every week",
     "A format that must not drift",
     "Steps a colleague could follow",
     "Work that needs a connected account"],
    ["A one-off request",
     "A job you are still working out",
     "Anything you would not hand to a colleague"],
    left_heading="Write a skill",
    right_heading="Leave it as a prompt",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Connect one account", "and see what it can reach"),
     ("Save a routine as a skill", "name, description, steps, format"),
     ("Open a fresh chat", "and ask in a colleague's words")],
    lead="That is the principle. Now we build one live, against a real folder.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
