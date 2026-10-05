#!/usr/bin/env python3
"""
"Practicing using Plugins in ChatGPT to Automate Tasks" - the principles half.

Run:
    uv run --with python-pptx python decks/practicing-plugins/build_practicing_plugins.py \
        decks/practicing-plugins/practicing-plugins.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/practicing-plugins/practicing-plugins.pptx

The capstone of the Skills & Plugins section. Every lecture before it has taught
one piece; this one assembles them, so the deck spends its slides on the
composition rather than re-teaching a part.

The spine is one arc: connect -> do the job by hand -> save the run as a skill ->
invoke it by name, or hand it to a clock. The durable claim underneath it is that
you automate a task by first doing it once, well: a skill is the record of a
workflow that already worked, which is why it is worth writing down and why it
keeps working.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck, title_case  # noqa: E402

def tc_table(data):
    """Title Case the header row, and the row labels when the corner cell is empty."""
    head = [title_case(c) for c in data[0]]
    rows = [[title_case(r[0]) if data[0][0] == "" else r[0]] + list(r[1:])
            for r in data[1:]]
    return [head] + rows


out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "practicing-plugins.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("From Connectors to a Saved Skill",
        "How a job you do once, by hand, across two connected systems becomes "
        "something you can call back by name, or hand to a clock.")

# ============================================================== WHAT IS IT?
s = d.what("one job that crosses two systems")
m = s.mock(0.40, 1.52, 4.72, 3.58)
m.user("Take the four client notes added to the shared",
       "drive this week, summarise each to our one-page",
       "format, and email the set to the account team.")
with m.bubble():
    m.assistant("Read four notes from the drive. Summarised",
                "each to the one-page format. Draft email ready.")
m.label("Connectors used")
m.line("Shared drive, then email", highlight=True)
m.composer(pin=False)
s.beside(m, "Connectors - what this course calls plugins - are the links between "
            "the assistant and systems you already use. Chaining them is one "
            "request that happens to touch both ends: it reads from "
            "the first, does the work in the middle, and writes into the second.")

s = d.content("There is nothing to wire up")
s.compare(1.52,
          "What people expect",
          ["A separate automation mode",
           "Boxes wired on a canvas",
           "A trigger, a filter, an action",
           "Something you configure first"],
          "What it actually is",
          ["One ordinary conversation",
           "Two connectors already granted",
           "The same steps, said in order",
           "Something you do, then keep"],
          h=2.14)
s.caption(0.34, 3.90, 9.32,
          "You grant each connector once, then describe the job the way you "
          "would to a colleague who already has access to both systems. The "
          "ordering is the whole design, and each of the three parts of it is a "
          "separate thing to get right.")

s = d.content("What the saved skill records")
s.table(0.34, 1.52, 9.32, 2.10, tc_table([
    ["What the run showed", "What the skill writes down"],
    ["What you asked for", "What it is for, and when"],
    ["Which systems it touched", "The connectors it needs"],
    ["The order you did it in", "The steps, and what each needs"],
    ["The shape you accepted", "The format of a finished result"],
    ["You read it, it was right", "How to check it is right"],
]), col_widths=[4.4, 4.9])
s.caption(0.34, 3.80, 9.32,
          "A skill is a named set of instructions the assistant keeps, and every "
          "line this one gets is something the run already settled. You are not "
          "designing a workflow from a blank page, you are describing one that "
          "worked - including how you knew that it had, which is the line people "
          "leave out and the one that matters most later.")

# ============================================================== HOW IT WORKS
s = d.how("do it once, then write down what you did")
s.flow(0.34, 1.52, 9.32,
       [("Connect", "grant each system, once"),
        ("Do the job", "by hand, until it is right"),
        ("Save the run", "under a name you choose"),
        ("Run it again", "by name, or on a clock")],
       h=1.15, accent_last=True,
       loop="and each run shows you what the saved wording still leaves out")
s.caption(0.34, 3.62, 9.32,
          "The order is not negotiable. A workflow you have never completed "
          "successfully cannot be saved, because there is nothing yet to save. "
          "The skill is the record of a run that worked, which is precisely why "
          "it goes on working.")

s = d.content("What is fixed, and what you supply")
r = s.message_row(0.34, 1.52, 9.31, 1.42)
r.label("Kept in the skill")
r.line("Source: the client notes folder on the shared drive.")
r.line("Format: our one-page summary, in that order of sections.")
r.line("Destination: an email to the account team, and never sent")
r.line("without a draft you have read.")
r = s.message_row(0.34, 3.20, 9.31, 0.72)
r.label("Supplied each run")
r.line("Which week. Which client. Who receives it this time.", highlight=True)
s.caption(0.34, 4.16, 9.32,
          "Separating those two is most of the work. Whatever you leave in the "
          "middle - “the usual folder”, “the normal people” - becomes a decision "
          "the assistant quietly makes on your behalf, on every later run.")

s = d.content("What the email is actually written from")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("What the drive handed back", "four files, as text", True),
                   ("The skill, once it fired", "format and checks"),
                   ("What you supplied", "the week, the recipient")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62,
       "Nothing else reaches the email", accent=True)
s.caption(6.50, 2.66, 3.16,
          "The assistant never sees your drive. It sees what the connector "
          "handed back - so if the fetch caught three files rather than four, "
          "nothing further down the chain has any way of noticing.")

# ============================================================== WHY IT MATTERS
s = d.why("you cannot automate what you have not done")
s.table(0.34, 1.52, 9.32, 1.90, tc_table([
    ["", "Written from a description", "Written from a run that worked"],
    ["Based on", "What you imagine happens", "What happened, once"],
    ["First run", "Debugging in the dark", "A repeat of something known"],
    ["Failure mode", "It never quite worked", "The world moved, not the skill"],
]), col_widths=[1.9, 3.6, 3.8])
s.caption(0.34, 3.68, 9.32,
          "That is the point that outlives every product involved. Automation is "
          "not a shortcut past doing the work - it is what you get to do "
          "afterwards, on the back of one run you were willing to sign off. Skip "
          "the run and you are debugging a guess.")

s = d.content("A run with nobody in the room")
s.compare(1.52,
          "In a chat, you fill the gaps",
          ["You see it fetch the wrong file",
           "You say “no, the other one”",
           "You read it before it sends",
           "You catch it in seconds"],
          "On a schedule, the skill must",
          ["Call the skill by name",
           "Name the source and the folder",
           "Say what a finished result is",
           "Say what “nothing found” means"],
          h=2.14)
s.caption(0.34, 3.90, 9.32,
          "Running to a schedule has its own lecture; what matters here is the "
          "join between them. A skill that works only because you were sitting "
          "there to steer it is not yet ready to be handed to a clock - and the "
          "test for that is whether a stranger could run it from the wording alone.")

s = d.content("How a saved chain fails")
m = s.mock(0.40, 1.52, 5.06, 3.40, app="Scheduled run", tag="07:00")
m.label("The skill, run on its own")
m.line("Read the client notes added this week. Summarise")
m.line("each to the one-page format. Email the account team.")
m.gap(0.06)
m.divider()
m.label("What you were sent")
m.line("Summaries filed. Nothing to report this week.")
m.gap(0.06)
m.divider()
m.label("What had actually happened")
m.line("The drive folder was renamed on Tuesday. The")
m.line("fetch matched nothing. Nothing was summarised.")
m.line("The email went out regardless, on time.")
m.fit()
s.beside(m, "A chain fails at its weakest link, and a saved chain fails politely. "
            "Nobody was in the room to notice that a cheerful summary of nothing "
            "is not the same thing as a quiet week - so the skill has to be told "
            "what an empty result means and what to do about it.")

d.two_columns(
    "When to save a run, and when not to",
    ["You have now done it once, properly",
     "It crosses the same two systems each time",
     "The result has a shape it must fit",
     "Someone else needs the same result"],
    ["You are still working out the steps",
     "The systems change from job to job",
     "You want a different angle each time",
     "The job is quicker than saving it"],
    left_heading=title_case("Worth saving"),
    right_heading=title_case("Just do it in the chat"),
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Connect both systems", "granted once, up front"),
     ("Run the job by hand", "until the result is right"),
     ("Save it as a skill", "with what varies left out"),
     ("Call it back by name", "in a chat that knows nothing")],
    lead="Now the whole arc live: connect, run it once, save it, set a time.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
