#!/usr/bin/env python3
"""
"Scheduled Tasks" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/scheduled-tasks/build_scheduled_tasks.py \
        decks/scheduled-tasks/scheduled-tasks.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/scheduled-tasks/scheduled-tasks.pptx

01:39 lecture, so the deck stays short: nine slides, no padding.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else "decks/scheduled-tasks/scheduled-tasks.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Scheduled Tasks",
        "How a prompt becomes a standing instruction that runs when you are not there.")

# ============================================================== WHAT IS IT?
s = d.what("a prompt with a clock attached")
m = s.mock(0.40, 1.52, 4.60, 3.58)
m.user("Every weekday at 7am, send me the three",
       "biggest stories in data engineering.")
with m.bubble():
    m.assistant("Done. I'll run this every weekday at 7am",
                "and send you the three stories.")
m.label("Saved as a task").line("Every weekday at 07:00", highlight=True)
m.composer(pin=False)
s.beside(m, "There is no new syntax to learn. You write the request you would have "
            "written anyway and say when it should run, and the wording is stored "
            "alongside the schedule.")

s = d.content("Not a reminder, a result")
s.compare(1.52,
          "A reminder", ["Pings you at a time",
                         "Hands the job back to you",
                         "Says the same thing each day"],
          "A scheduled task", ["Runs the prompt at that time",
                               "Does the work first",
                               "Hands you today's answer"])

# ============================================================== HOW IT WORKS
s = d.how("the clock starts the run, not you")
s.flow(0.34, 1.52, 9.32,
       [("You describe", "the work, and when"),
        ("It stores", "wording and schedule"),
        ("The time comes", "it runs on its own"),
        ("You are told", "an answer is waiting")],
       h=1.15, accent_last=True,
       loop="then again at the next scheduled time")
s.caption(0.34, 3.86, 9.32,
          "You are not part of the run. At the appointed time the saved wording is "
          "sent on its own, and the first you hear of it is a notification with the "
          "answer already written.")

s = d.content("What a run has to go on")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("The wording you saved", "read back exactly as typed", True),
                   ("The schedule", "the hour, and the time zone you set it in"),
                   ("Whatever it can reach", "the live web, apps you connected")],
                  h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "Runs with nobody to ask", accent=True)
s.caption(6.50, 2.55, 3.16,
          "You are not in the room to say \u201cno, the other one\u201d. Whatever the "
          "instruction leaves implicit is guessed at, quietly, on every run.")

s = d.content("Where it stops")
m = s.mock(5.06, 1.52, 4.60, 3.30, app="Scheduled task", tag="Boundaries")
m.label("It can").line("Run once, or repeat on a schedule.")
m.line("Watch for a change and tell you.")
m.line("Use the apps you have connected.")
m.gap(0.06)
m.divider()
m.label("It cannot").line("Ask you what you meant.")
m.line("Reach files kept in a project.")
m.line("Run without limit - there is a cap on")
m.line("how many you may keep active.")
m.fit()
s.beside(m, "Every one of these comes from the same fact: you are not in the run. "
            "It cannot check with you, so an instruction that needs a decision "
            "either guesses at it or stops and waits for your approval.")

# ============================================================== WHY IT MATTERS
s = d.why("a vague instruction fails on a schedule")
s.table(0.34, 1.52, 9.32, 1.90, [
    ["", "Asked in a chat", "Left running as a task"],
    ["Ambiguity", "You correct it in seconds", "Guessed at on every run"],
    ["A poor answer", "You spot it at once", "It waits in a notification"],
    ["Failure mode", "Wrong once", "Wrong every day, unread"],
], col_widths=[1.9, 3.6, 3.6])
s.caption(0.34, 3.70, 9.32,
          "So write it for a stranger who cannot ask you anything: name the source, "
          "the format and the length. Self-contained is not a nicety here, it is the "
          "whole difference between a task that works and one that quietly does not.")

s = d.content("Tasks outlive the reason you made them")
m = s.mock(0.40, 1.52, 5.00, 3.42, app="Your tasks", tag="Standing")
m.label("None of these expire")
m.table([["Task", "Runs", "State"],
         ["Weekday news digest", "Weekdays", "Active"],
         ["Monday client report", "Weekly", "Active"],
         ["Launch-week countdown", "Daily", "Active"],
         ["Standup nudge", "Weekdays", "Active"],
         ["Competitor price watch", "Hourly", "Paused"]],
        col_widths=[3.0, 1.3, 1.1], row_h=0.30)
m.fit()
s.beside(m, "Every task keeps running until you stop it, and one can pause itself "
            "without telling you. So the list is not a screen you visit once: it is "
            "where you retire what has served its purpose and notice what has "
            "quietly stopped.")

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Say it in a sentence", "and watch it become a task"),
     ("Open the task", "reword it, change the schedule"),
     ("Find the whole list", "pause one, delete another")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
