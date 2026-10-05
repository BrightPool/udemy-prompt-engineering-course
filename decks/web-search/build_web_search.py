#!/usr/bin/env python3
"""
"Web Search" - the principles half of the re-film.

Run:
    uv run --with python-pptx python decks/web-search/build_web_search.py \
        decks/web-search/web-search.pptx
    uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
        decks/web-search/web-search.pptx

The arc rides on the slide titles - what is it / how it works / why it matters -
so there are no divider slides. The deck deliberately runs short: the lecture is
being cut to about a minute, and the demo half is three queries (one that
triggers a search, one that does not, then the first one again with an explicit
instruction to search).
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2] / ".claude/skills/principles-deck/scripts"
sys.path.insert(0, str(SKILL))
from deckkit import Deck  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1
           else Path(__file__).resolve().parent / "web-search.pptx")
d = Deck()

# ---------------------------------------------------------------- open
d.title("Web Search",
        "How an assistant answers from pages it fetched a moment ago.")

# ============================================================== WHAT IS IT?
s = d.what("a retrieval step before the answer")
m = s.mock(0.40, 1.52, 4.60, 3.58)
m.user("What did the Bank of England do to rates", "this week?")
with m.bubble():
    m.assistant("It held Bank Rate, citing services inflation.")
    m.line("Sources: 3", highlight=True)
m.composer(pin=False)
s.beside(m, "Web search is a step the assistant runs before it answers. It turns "
            "your question into search queries, reads what comes back, and writes "
            "the answer from that text rather than from memory.")

s = d.content("Which questions trigger a search")
s.compare(1.52,
          "Answered from memory", ["What is a p-value?",
                                   "Rewrite this paragraph.",
                                   "Who wrote Middlemarch?"],
          "Answered from the web", ["What did rates do this week?",
                                    "Who leads that department now?",
                                    "Has that policy changed yet?"],
          h=2.20)
s.caption(0.34, 3.92, 9.32,
          "The assistant makes this call itself. It reads your wording, judges "
          "whether the answer is time-bound, and picks a lane - so the same "
          "question can go either way on different days.")

# ============================================================== HOW IT WORKS
s = d.how("decide, query, read, answer")
s.flow(0.34, 1.52, 9.32,
       [("It decides", "does this need the web?"),
        ("It queries", "several searches at once"),
        ("It reads", "the pages that come back"),
        ("It answers", "citing what it read")],
       h=1.10, accent_last=True)
s.caption(0.34, 2.86, 9.32,
          "Step two is not one search. That question about the Bank of England is "
          "rewritten into several queries, fired at once, and the answer is "
          "stitched from whatever they turn up:")
for i, query in enumerate(["bank of england rate decision",
                           "bank rate held or cut this week",
                           "interest rate announcement latest"]):
    s.node(0.34 + i * 3.24, 3.66, 2.84, 0.78, query)

s = d.content("Your question, plus what it fetched")
bottom = s.layers(0.34, 1.52, 5.90,
                  [("Fetched page text", "read seconds ago", True),
                   ("Result snippets", "a line or two each"),
                   ("Your question", "typed just now")], h=0.66)
s.arrow(3.10, bottom + 0.04, 0.34, 0.22, direction="down")
s.node(0.34, bottom + 0.36, 5.90, 0.62, "Pages and question, together", accent=True)
s.caption(6.50, 2.30, 3.16,
          "The assistant never really visits a page. Text from those pages is "
          "pasted in beside your question, and the answer is written from the "
          "whole block - which is why a copy cached hours ago can be quoted as "
          "though it were live.")

s = d.content("Asking for the search you want")
m = s.mock(0.40, 1.52, 4.60, 3.58, tag="Explicit request")
m.user("Search the web before you answer.", highlight=True)
m.line("Only use sources published this month.")
with m.bubble():
    m.assistant("Searched. Three of the pages are from this")
    m.line("month - here is what they say, with dates.")
m.composer(pin=False)
s.beside(m, "You are not flipping a switch, you are removing the ambiguity. Say "
            "that you want it to search, say how fresh the pages must be, and the "
            "decision stops being a guess.")

# ============================================================== WHY IT MATTERS
s = d.why("grounded is not the same as true")
s.table(0.34, 1.52, 9.32, 2.30, [
    ["", "From memory", "From the web"],
    ["Freshness", "Frozen at training", "As fresh as the page"],
    ["Speed", "Immediate", "Waits on the fetch"],
    ["Checkable", "Nothing to open", "Open the source"],
    ["Failure mode", "Confidently out of date", "Confidently citing a bad page"],
], col_widths=[1.9, 3.6, 3.6])
s.caption(0.34, 4.02, 9.32,
          "Retrieval changes where an answer comes from, not whether it is right. "
          "Pages are written by people - some are stale, some are wrong, and some "
          "were written to be found rather than to be correct. The citation is the "
          "thing you check, not the thing you trust.")

d.two_columns(
    "When to ask for it",
    ["Anything that changed recently",
     "Prices, releases, rules, who holds a post",
     "Claims you will have to defend"],
    ["Reasoning over what you already gave it",
     "Rewriting or summarising your own text",
     "Settled facts, definitions, maths"],
    left_heading="Worth the fetch",
    right_heading="Skip the search",
)

# ---------------------------------------------------------------- handoff
d.handoff(
    [("Ask a live question", "watch it search"),
     ("Ask a settled one", "no search, no sources"),
     ("Ask the first again", "this time say: search the web"),
     ("Open a citation", "does it say what the answer says?")],
    lead="That is the principle. Now we do it live in the tool.",
)

path = d.save(out)
print(f"wrote {path}  ({len(d.prs.slides._sldIdLst)} slides)")
