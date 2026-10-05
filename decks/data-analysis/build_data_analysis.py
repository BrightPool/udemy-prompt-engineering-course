#!/usr/bin/env python3
"""
"Data Analysis" - the principles half of the re-film (lecture 023, video 49725289).

Run:
    uv run --with python-pptx python decks/data-analysis/build_data_analysis.py \
        decks/data-analysis/data-analysis.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/data-analysis/data-analysis.pptx

Spine: the model does not eyeball your spreadsheet. It writes code, runs the code,
and reads what came back - which is why the number is reproducible, and why the
thing to check is the code rather than the confidence.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "principles-deck"
sys.path.insert(0, str(SKILL / "scripts"))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).with_name("data-analysis.pptx"))
d = Deck()

# ---------------------------------------------------------------- open
d.title("Data Analysis",
        "How an assistant answers questions about your file by writing code, "
        "running it, and reading the result.")

# ============================================================== WHAT IS IT?
s = d.what("it writes code, it does not eyeball your file")
m = s.mock(0.40, 1.52, 4.60, 3.50)
m.user("How many students are in this file?")
with m.bubble():
    m.label("Analysis")
    m.line("df = pd.read_csv('students.csv')")
    m.line("len(df)")
    m.divider()
    m.line("50", highlight=True)
m.assistant("There are 50 students in the file.")
m.fit()
s.beside(m, "You ask a question in plain English. The assistant turns it into a "
            "few lines of Python, runs them over the file you uploaded, and "
            "reports what the code returned.")

s = d.content("When the code fails, you watch it fail")
m = s.mock(0.40, 1.52, 4.60, 3.50)
m.user("How many are male and how many female?")
with m.bubble():
    m.line("df['Agenda'].value_counts()")
    m.line("KeyError: 'Agenda'", highlight=True)
    m.gap(0.08)
    m.line("print(df.columns)")
    m.line("df['gender'].value_counts()")
    m.divider()
    m.line("female  25    male  25")
m.assistant("25 female and 25 male.")
m.fit()
s.beside(m, "A guess cannot fail loudly. Real code can, so a wrong column name "
            "surfaces as an error instead of as a plausible number. It reads "
            "the error, checks the real columns and runs again.")

s = d.content("What it is not")
s.compare(1.52,
          "Not this", ["Skimming your rows and estimating",
                       "Recalling similar data it has seen",
                       "A guess dressed up as a total"],
          "This", ["A short program the assistant wrote",
                   "Run over the file you uploaded",
                   "A number you could reproduce yourself"])

# ============================================================== HOW IT WORKS
s = d.how("ask, write, run, read, explain")
s.flow(0.34, 1.52, 9.32,
       [("You ask", "of your file"),
        ("It writes", "some Python"),
        ("It runs", "in a sandbox"),
        ("It reads", "the output"),
        ("It explains", "in plain English")],
       h=1.10, accent_last=True,
       loop="an error sends it back to the code")
s.caption(0.34, 3.72, 9.32,
          "The sandbox is a temporary, isolated computer with a copy of your "
          "file on it. The loop matters as much as the line: if the code errors, "
          "or the result looks wrong, the assistant edits it and runs it again - "
          "the same thing an analyst does, at speed.")

s = d.content("What the model sees of your file")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("A preview of your file", "column names, a few rows", True),
                   ("Your question", "typed just now"),
                   ("What the code printed", "numbers, errors, a chart")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62,
       "The model explains the output, not your rows", accent=True)
s.caption(6.50, 2.26, 3.16,
          "Most of your rows never enter the prompt. The file goes to the "
          "sandbox; only the output comes back. That is how it handles more "
          "data than it could ever read - and why one wrong line of code "
          "yields a confident wrong answer.")

s = d.content("Where the sandbox stops")
m = s.mock(5.10, 1.52, 4.56, 3.30, app="Sandbox", tag="Boundaries")
m.label("Can reach").line("The files you uploaded")
m.line("A standard Python data stack")
m.line("Charts and files it writes back")
m.gap(0.06)
m.divider()
m.label("Cannot reach").line("The internet")
m.line("Your machine or your live systems")
m.line("Anything you did not give it")
m.fit()
s.beside(m, "Your original file is never touched, nothing outside the "
            "container is available unless you upload it, and the container is "
            "temporary - it expires, and the workings expire with it.")

# ============================================================== WHY IT MATTERS
s = d.why("the answer becomes checkable")
s.table(0.34, 1.52, 9.32, 2.24, [
    ["", "Eyeballed answer", "Executed code"],
    ["The number comes from", "The model's impression", "A line you can read"],
    ["Run it again", "May well differ", "Same code, same answer"],
    ["What you check", "Does it sound right?", "Did it ask the right question?"],
    ["Failure mode", "Confident guess", "Right code, wrong assumption"],
], col_widths=[2.4, 3.3, 3.6])
s.caption(0.34, 3.98, 9.32,
          "Running code does not make an answer true. It makes the answer "
          "auditable, which is a different and more useful guarantee.")

s = d.content("How it goes wrong")
s.cards(0.34, 1.52, 9.32,
        [("Misreads a column", "'grade' taken as a score when it is a year group"),
         ("Drops rows quietly", "blanks and mixed types vanish inside a filter"),
         ("Misparses the file", "one stray comma and every column shifts along")],
        h=1.86)
s.caption(0.34, 3.60, 9.32,
          "Each of these returns a tidy, confident, wrong answer, because the "
          "code ran perfectly - it just answered a question you did not ask.")

s = d.content("Checking it in thirty seconds")
s.steps(0.34, 1.52, 5.44,
        ["Ask for the row and column counts first.",
         "Read the filter, the grouping, the blanks.",
         "Ask for the same number a second way."],
        h=0.80, gap=0.18)
s.caption(6.16, 2.34, 3.50,
          "You are not auditing the arithmetic - the computer got that right. "
          "You are auditing whether the question the code asked is the question "
          "you meant to ask.")

d.two_columns(
    "When to reach for it",
    ["A file you already hold", "Exploratory questions and charts",
     "Cleaning or reshaping a messy export"],
    ["Data you are not permitted to upload", "A report you rerun every week",
     "Numbers you will publish unchecked"],
    left_heading="Good fit",
    right_heading="Use something else",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Upload a file", "and ask one plain question"),
     ("Open the code", "read what it actually did"),
     ("Ask for a chart", "then change one thing about it")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
