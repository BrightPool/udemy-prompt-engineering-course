#!/usr/bin/env python3
"""
"Reasoning Models" - the principles half of the re-film (video 48150231, 05:39).

Renamed from "Chat Models vs Reasoning Models". The spine is the trade-off James
asked for: a model that answers immediately against a model that works first, and
what that working costs in time and money.

Build:
    uv run --with python-pptx python decks/reasoning-models/build_reasoning_models.py \
        decks/reasoning-models/reasoning-models.pptx
Lint:
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/reasoning-models/reasoning-models.pptx

Deliberately vendor-neutral: no model names, no effort-level labels, no picker
positions. Those move every few months and belong in the demo half - the current
state of the ChatGPT picker is recorded in decks/reasoning-models/NOTES.md.
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import Deck, MUTED  # noqa: E402


class Vis:
    """Minimal geometry holder so s.beside() can sit copy next to a diagram.

    beside() wants .x/.y/.w/.h; a diagram helper returns only its bottom edge,
    so wrap the box we drew rather than hardcoding a body placeholder beside it.
    """

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h


out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "reasoning-models.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Reasoning Models",
        "A model that generates its own working before it answers, trading time "
        "and tokens for a better shot at a hard question.")

# ============================================================== WHAT IS IT?
s = d.what("a model that works the problem out first")
m = s.mock(0.40, 1.56, 4.60, 3.58)
m.user("Raise prices, or add a cheaper tier?")
m.label("Thought for 24 seconds")
m.gap(0.06)
with m.bubble():
    m.assistant("Add the cheaper tier first - it",
                "measures the price sensitivity a",
                "rise can only guess at.")
m.composer(pin=False)
s.beside(m, "A reasoning model does not start answering straight away. It first "
            "generates a stretch of working - approaches tried, sums checked, "
            "wrong turns abandoned - and only then writes the reply you read.")

# --- the spine of the deck: the same question, two ways -------------------
s = d.content("The same question, sent two ways")
RIGHT = s.mock(5.05, 1.56, 4.55, 3.30, tag="After thinking")
RIGHT.user("Lose 3 of 40 clients, raise fees 10%?")
RIGHT.label("Thought for 24 seconds")
RIGHT.line("40 x \u00a31,200 = \u00a348,000; 37 x \u00a31,320 = \u00a348,840.",
           color=MUTED)
RIGHT.gap(0.04)
with RIGHT.bubble():
    RIGHT.assistant("Up about 1.75% - \u00a3840 a month more.")
RIGHT.composer(pin=False)

# Same height and the same chrome as the panel beside it. A comparison drawn in
# two differently sized windows reads as a layout slip, not as the point.
LEFT = s.mock(0.40, 1.56, 4.55, RIGHT.h, tag="Instant reply")
LEFT.user("Lose 3 of 40 clients, raise fees 10%?")
with LEFT.bubble():
    LEFT.assistant("Revenue dips slightly - a 10% rise",
                   "will not cover losing 3 clients.")
LEFT.composer()

s.caption(0.34, max(LEFT.y + LEFT.h, RIGHT.y + RIGHT.h) + 0.16, 9.32,
          "Same question, same account, two settings. The instant reply is not "
          "stupid, it is unchecked: it never did the two sums on the right, and it "
          "guessed the direction wrong.")

s = d.content("What it is not")
s.compare(1.52,
          "Not this", ["A bigger, newer model",
                       "A model that searches the web",
                       "A separate product you buy"],
          "This", ["The same model, given room",
                   "Working written before the reply",
                   "An effort dial you can turn"],
          h=2.20)
s.caption(0.34, 3.94, 9.32,
          "Thinking is a setting, not a different tool. One model can answer in a "
          "second or work for a minute, and how much it thinks is something you "
          "choose per question.")

# ============================================================== HOW IT WORKS
s = d.how("it writes to itself before it writes to you")
s.layers(0.34, 1.52, 5.40,
         [("Your question", "what you typed"),
          ("Reasoning tokens", "summarised, not shown raw", True),
          ("The reply", "what appears on screen")],
         h=0.80)
s.beside(Vis(0.34, 1.52, 5.40, 2.74),
         "There is no separate thinking machine. The model produces text the only "
         "way it can, one token at a time - it just produces a first batch for "
         "itself. You pay for those tokens and you wait for them.")

s = d.content("Effort is a dial, not a switch")
s.flow(0.34, 1.52, 9.32,
       [("No thinking", "replies at once"),
        ("A little", "a quick check"),
        ("More", "options weighed"),
        ("A lot", "careful working")],
       h=1.00)
s.table(0.34, 2.84, 9.32, 1.60, [
    ["Turn the dial up", "On an easy question", "On a hard question"],
    ["you wait", "the same answer, slower", "worth the wait"],
    ["you generate more tokens", "you pay for nothing", "you pay for care"],
    ["the model checks itself", "there was nothing to catch", "it catches its slips"],
], col_widths=[2.7, 3.3, 3.3])
s.caption(0.34, 4.66, 9.32,
          "Where the dial sits changes with every release. That it exists, and what "
          "it trades away, does not.")

s = d.content("What the pause costs you")
s.table(0.34, 1.52, 9.32, 2.20, [
    ["Tokens in one answer", "Do you read them?", "Billed as"],
    ["Your prompt and history", "you wrote them", "input, the baseline"],
    ["A prompt you resend", "you wrote it once", "cached input, discounted"],
    ["The model's working", "no", "output, the dearest rate"],
    ["The reply", "yes", "output, the dearest rate"],
], col_widths=[3.0, 2.7, 3.6])
s.caption(0.34, 3.94, 9.32,
          "Working you never read is billed at the same rate as the reply you do, "
          "and output is the dearest of the three rates. That is the whole trade: "
          "you are paying, in cash and in waiting, for care.")

# ============================================================== WHY IT MATTERS
s = d.why("hard questions stop failing quietly")
s.table(0.34, 1.52, 9.32, 2.00, [
    ["", "Answered at once", "Answered after thinking"],
    ["An easy question", "right, immediately", "right, after a wait"],
    ["A multi-step problem", "plausible, sometimes wrong", "worked through, then checked"],
    ["An ambiguous brief", "picks one reading", "notices there are two"],
    ["Failure mode", "confidently wrong", "slow, dear, over-thought"],
], col_widths=[2.5, 3.3, 3.5])
s.caption(0.34, 3.74, 9.32,
          "The gain is not that it knows more. It is that a slip gets caught before "
          "you read it, which only helps on work where a slip was likely in the "
          "first place.")

d.two_columns("When the thinking time is worth it",
              ["Multi-step sums and money maths",
               "Reviewing or debugging code",
               "Planning work in stages",
               "Weighing options when unsure",
               "Checking someone else's answer"],
              ["Recalling a fact or definition",
               "Summarising a document",
               "Drafting and rewriting copy",
               "Reformatting or tidying text",
               "Quick back-and-forth chat"],
              left_heading="Worth the wait",
              right_heading="Slower for no gain")

s = d.content("What effort cannot fix")
s.compare(1.52,
          "More effort will not", ["Give it facts it never had",
                                   "Stop it inventing a source",
                                   "Improve an easy answer"],
          "More effort will", ["Catch its own arithmetic slips",
                               "Weigh options before choosing",
                               "Notice a brief is ambiguous"],
          h=2.20)
s.caption(0.34, 3.94, 9.32,
          "Careful reasoning from something invented is still wrong, so effort is "
          "no defence against a made-up figure. What you can expand on screen is a "
          "summary of the working, not the working itself.")

s = d.content("Thinking time is not your time")
s.steps(0.34, 1.52, 5.40,
        ["Send the slow, careful job first.",
         "Move to a second window and work.",
         "Collect the finished answer later."],
        h=0.74, gap=0.18)
s.beside(Vis(0.34, 1.52, 5.40, 2.58),
         "A model working for two minutes is not two minutes you have to spend. "
         "Start the job that needs care, then get on with something a fast model "
         "can handle while it runs. Waiting is a habit, not a requirement.")

# ============================================================== HANDOFF
d.handoff([("Ask an easy question", "at both settings"),
           ("Ask a hard one", "and watch it work"),
           ("Open the working", "see what it checked")],
          lead="That is the principle. Now we turn the dial in the tool.")

d.save(out)
print(f"wrote {out}")
