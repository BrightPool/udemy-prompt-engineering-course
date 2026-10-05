#!/usr/bin/env python3
"""
Principles half of the "Deep Research" re-film.

Build:
    uv run --with python-pptx python decks/deep-research/build_deep_research.py \
        decks/deep-research/deep-research.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/deep-research/deep-research.pptx

Deliberately contains no invocation method, no control names and no run limits.
Those drift and belong in the demo half - see NOTES.md.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "principles-deck" / "scripts"))
from deckkit import Deck, ARROW  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else ROOT / "decks/deep-research/deep-research.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Deep Research",
        "How an assistant runs a long investigation for you and hands back a "
        "report you can check.")

# ============================================================== WHAT IS IT?
s = d.what("an investigation you delegate")
m = s.mock(0.40, 1.56, 4.85, 3.50)
m.user("Work out why cultural evolution became a research",
       "field and memetics did not.")
with m.bubble():
    m.assistant("Incentives (funding, journals), or theory?")
m.user("Incentives.")
m.line("Done in 9 minutes. 28 sources, cited inline.", highlight=True)
m.composer(pin=False)
s.beside(m, "You hand over a question worth an afternoon. It checks what you "
            "actually want, works for a while, and comes back with a written "
            "report rather than a chat reply.")

s = d.content("One lookup, or one investigation")
s.compare(1.56,
          "Web search", ["One question, one set of results",
                         "Reads what search returned",
                         "Answers in seconds",
                         "Grounds an ordinary reply"],
          "Deep research", ["One question, dozens of searches",
                            "Decides what to look up next",
                            "Runs for many minutes",
                            "Returns a written, cited report"])
s.caption(0.34, 4.32, 9.32,
          "Same web, very different amount of work. Reach for deep research when "
          "the answer has to be assembled rather than found.")

s = d.content("What comes back")
m = s.mock(0.40, 1.56, 4.90, 3.40, tag="Research report")
m.label("Why memetics stalled")
m.line("1. Its central claim resisted measurement. [3][7]")
m.line("2. Neighbouring fields absorbed the questions. [11]")
m.line("3. Funding followed the testable programme. [2][19]")
m.gap(0.06)
m.divider()
m.label("Where the sources disagree")
m.line("Two dispute the funding claim. [2][19]")
m.gap(0.06)
m.divider()
m.label("Sources")
m.line("28 pages, each tied to the line it supports.")
m.fit()
s.beside(m, "The output is a document, not a paragraph: sections, an argument, "
            "and a citation on each claim so you can check the ones that matter "
            "to you.")

# ============================================================== HOW IT WORKS
s = d.how("one question fans out into many searches")
MID_X, MID_W, MID_H = 3.20, 3.06, 0.56
mid_ys = [1.56, 2.25, 2.94, 3.63]
mid_labels = ["Funding and grants", "Journals and citations",
              "Critiques of the field", "Adjacent disciplines"]
for y, label in zip(mid_ys, mid_labels):
    s.node(MID_X, y, MID_W, MID_H, label)
centres = [y + MID_H / 2 for y in mid_ys]
axis = (centres[0] + centres[-1]) / 2                      # 2.89

s.node(0.34, axis - 0.55, 2.00, 1.10, "Your question",
       sub="asked once, in plain words")
s.node(7.62, axis - 0.55, 2.04, 1.10, "One cited report",
       sub="claims tied to pages", accent=True)

# fan out: stem, vertical rail, one arrow into each search
s.rect(2.34, axis - 0.006, 0.38, 0.012, fill=ARROW)
s.rect(2.72, centres[0], 0.012, centres[-1] - centres[0], fill=ARROW)
for c in centres:
    s.arrow(2.78, c - 0.06, 0.42, 0.12)
# converge: an arrow out of each search onto a rail, then into the report
for c in centres:
    s.arrow(6.26, c - 0.06, 0.94, 0.12)
s.rect(7.20, centres[0], 0.012, centres[-1] - centres[0], fill=ARROW)
s.arrow(7.20, axis - 0.06, 0.42, 0.12)
s.caption(3.20, 4.32, 3.06,
          "Plus two dozen more, written as it learns what to ask next.")

s = d.content("The loop it runs")
s.steps(0.34, 1.56, 5.50, [
    "It turns your question into a plan.",
    "It writes its own search queries.",
    "It opens pages and reads them.",
    "It notices what is still missing.",
    "It searches again, until it stops learning.",
])
s.caption(6.20, 1.62, 3.46,
          "The loop is the whole idea. A single search answers the question you "
          "typed. This one decides what to ask next, and keeps going until more "
          "searching stops changing the answer. Step one is your cheapest moment "
          "to steer it.")

s = d.content("The report is written from what it read")
bottom = s.layers(0.34, 1.56, 5.70,
                  [("Your question", "restated as a plan"),
                   ("Pages it opened", "whatever the searches found", True),
                   ("Notes it kept", "from its earlier steps")], h=0.66)
s.arrow(3.00, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.70, 0.62, "Everything the report is built from",
       accent=True)
s.caption(6.30, 1.62, 3.36,
          "Nothing else reaches the model. A peer-reviewed paper and a personal "
          "blog arrive as the same kind of text, and the model has no way to tell "
          "nothing in the mechanism ranks one above the other.")

# ============================================================== WHY IT MATTERS
s = d.why("it buys the hours, and it charges for them")
s.table(0.34, 1.56, 9.32, 2.10, [
    ["", "Researching it yourself", "Delegating the research"],
    ["Your afternoon", "Spent finding sources", "Spent judging them"],
    ["What you must check", "Your own reading", "Its citations"],
    ["Your confidence", "Earned slowly", "Arrives fully formed"],
    ["Failure mode", "You stop too early", "Confidently thorough"],
], col_widths=[2.1, 3.6, 3.6])
s.caption(0.34, 3.92, 9.32,
          "The cost sits where the value does. It reasons and writes far more than "
          "it reads, and generated tokens are the expensive kind, so runs are "
          "metered. Spend one on a question worth an afternoon.")

s = d.content("Read the sources, not just the report")
m = s.mock(0.40, 1.56, 5.05, 3.40, tag="Sources")
m.label("Read and cited")
m.line("A university department page")
m.line("A peer-reviewed review article")
m.line("An encyclopaedia entry")
m.line("A personal blog, cited like the rest", highlight=True)
m.gap(0.06)
m.divider()
m.label("Never opened")
m.line("Paywalled journals")
m.line("Anything behind a sign-in")
m.fit()
s.beside(m, "It cites what it could open. A weak source looks like a strong one "
            "in a tidy report, so narrow where it may look before it starts.")

d.two_columns(
    "When to reach for it",
    ["A question worth an afternoon",
     "Ground you do not know yet",
     "Claims you want compared across sources"],
    ["A single fact you can look up",
     "A fast answer mid-conversation",
     "A question you cannot state clearly yet"],
    left_heading="Worth the wait",
    right_heading="Not worth it",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Start a run", "on a real question"),
     ("Watch it work", "the queries it writes itself"),
     ("Read the report", "then click a source through")],
    lead="That is the principle. Now we run one live.",
)

d.save(out)
print(out)
