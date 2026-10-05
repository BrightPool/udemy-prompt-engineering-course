# Web Search - deck notes

Lecture: Part 2 · ChatGPT Deep Dive · re-film · video_id `46777369` · owner James
Deck: `decks/web-search/web-search.pptx` (9 slides), built by `build_web_search.py`.

## The three principles

- **What it is** - Web search is a retrieval step the assistant runs *before* it answers:
  it turns your question into search queries, reads what comes back, and writes the answer
  from that fetched text rather than from memory.
- **How it works** - The model first judges whether the question is time-bound; if it is,
  the question is rewritten into several queries fired at once, and the text those pages
  return is placed into the same context as your question before a word is generated.
- **Why it matters** - A grounded answer arrives with sources you can open, which is the
  only cheap way to check it; but the pages were written by people, so retrieval fixes
  staleness, not truthfulness.

## Research: what is true now

Primary sources: OpenAI Help Centre ("Searching the web with ChatGPT", "Offline web search
for ChatGPT workspaces", "Lockdown Mode") and the OpenAI API web-search tool guide.
Mechanism detail cross-checked against Search Engine Land's teardowns of ChatGPT's
retrieval stack.

1. **The model decides.** OpenAI's own wording: ChatGPT "may choose to search the web based
   on what you ask, or you can manually choose search when it is available." So the default
   is a model judgement, and a manual choice exists but is described as conditional - which
   is exactly why James's three-query structure works as a demo.
2. **One question becomes several queries.** The tool rewrites the question into multiple
   targeted queries ("fan-out") and can run several rounds; reasoning models search, read,
   and decide whether to search again. Non-reasoning modes do one shallow pass. This is the
   single most useful mechanism fact for the deck, and it is on slide 4.
3. **What reaches the model is text, not a page.** Three tiers: a ~200-character index
   snippet, a cached Markdown copy of a previously fetched page, or a live fetch. Cached
   copies are served stale-while-revalidate, and copies well over a month old have been
   observed. Slide 5 teaches this without naming the tiers.
4. **Citations vs sources.** Inline citations are the subset the answer leans on; the full
   list of URLs consulted is larger. In the API these are `url_citation` annotations and the
   `sources` field. On slides this stays as "sources you can open".
5. **OpenAI's own accuracy caveat.** Search results and citations "can be incomplete,
   outdated, or incorrect"; OpenAI advises opening a cited source to check it supports the
   answer and to check when it was published or updated. That is the honest boundary the
   deck is built around, and it is what slide 9 asks the instructor to do live.
6. **Retrieved pages can carry instructions, not just facts.** OpenAI states that indexed or
   cached web content "can still contain inaccurate information, incomplete information,
   outdated information, or malicious instructions", and that Lockdown Mode does not prevent
   prompt injection reaching ChatGPT through fetched content. Deliberately left off the
   slides - see `## For James`.
7. **Search context is capped** (128k tokens in the API, regardless of the model's window),
   and search is billed as a tool call on top of tokens. Not on the slides: pricing and
   figures date fastest. The durable version is on slide 7 - "Speed: waits on the fetch".

## What changed since filming

| The original lecture says | What is true now |
|---|---|
| Search is "a new addition" that "looks at multiple sources" | Multi-source is ordinary; the fan-out into several rewritten queries is the interesting part |
| "It's not actually possible to turn this feature off" - search fires even when toggled off | The model decides per question. It genuinely does *not* search for settled questions, which is why the second of James's three queries lands |
| Demonstrated by toggling search on, and by dropping to an older model to stop it searching | The reliable lever is now the wording of the prompt, not a control. Ask for a search and you get one |
| "It has your IP address, so it does a local search" (the Birmingham restaurants bit) | Cut. It was a UI/geolocation aside, it dates, and it duplicated nothing in the principle |
| Sources presented as a list you click through | Same, plus OpenAI's own advice to check the publish/update date, not just that a link exists |

## Review round 1 - the hostile reviewer

Findings and fixes (all made in the build script, then rebuilt and re-linted clean):

1. **Slides 3 and 7 argued the same axis twice.** Slide 3 compared "answered from memory"
   with "answered from the web" by *properties*; slide 7's table did the same with better
   rows. Rewrote slide 3 as concrete example *questions* - which is also the setup for
   James's first two demo queries. Title changed to "Which questions trigger a search".
2. **Slide 4 was carrying two ideas**, and after fixing slide 3 the three "signals that tip
   the decision" nodes were redundant with it. Replaced them with the fan-out - one question
   rewritten into three real-looking queries - which is mechanism the deck did not otherwise
   have.
3. **Slide 6's mock had no highlight.** Moved the instruction onto its own line so the pink
   pill sits on the phrase that does the work.
4. Layout: slide 5's caption sat at y=1.60 against a diagram running to 4.69 - top-heavy.
   Moved to 2.30 so it is optically centred against the stack, and trimmed it from four
   sentences to three, ending on the stale-cached-copy point.
5. Layout: three lint warnings before the round (a user line overflowing a non-wrapping
   `.line()`, 1.55" of dead space on slide 4, an over-long mock tag). All fixed.

## Review round 2 - the student

1. **Undefined acronym.** Slide 4's example queries included "mpc vote split latest". MPC is
   never defined. Replaced with queries a viewer can parse, and tied the caption explicitly
   back to the Bank of England question from slide 2 so the fan-out has a visible source.
2. **A metaphor used twice.** Slide 3's caption and slide 6's body both opened on "flipping
   a switch". Kept it on slide 6, where overriding the decision is the point; rewrote slide 3.
3. **The mocked reply read like placeholder text.** "Here is what three sources published
   this month say" → "Searched. Three of the pages are from this month - here is what they
   say, with dates."
4. **Handoff card 4 was tangled** ("check it says what the answer says") → "does it say what
   the answer says?"
5. Layout: nudged slide 4's query nodes to 3.66 to clear the now two-line caption above them.

Round 2 turned up four substantive findings, so per `review-loop.md` a third round ran.

## Review round 3

1. **The deck named the trust cost but never the time cost.** Added a "Speed / Immediate /
   Waits on the fetch" row to slide 7's table (table 1.90" → 2.30", caption moved to 4.02").
2. **"Search adds nothing" overclaimed** as a column heading - search costs time even where
   it adds little. Changed to "Skip the search".
3. Layout pass: content on every non-title slide now starts at y=1.52", and the lowest
   element on slides 3/4/5/6/7 lands between 4.34" and 4.69". Nothing crosses 5.10".

Final lint: `clean - 9 slides, nothing to fix`.

## Deliberately left out

- Any control, toggle, icon or menu path. The deck teaches that the model chooses and that
  you can override the choice in the prompt; where the manual control currently lives is a
  demo-half thing and a spoken line.
- Model names, knowledge-cutoff dates, context-window figures, per-search pricing.
- Deep research. It is a separate lecture; this deck stops at "several queries, fired at
  once" and never uses the words "deep research".
- Prompt injection via retrieved pages (see below).

## For James

1. **The old lecture's headline claim is now wrong on camera.** It says "it's not actually
   possible to turn this feature off - it will search regardless". That is no longer true,
   and the fact that it is no longer true is what makes your second query (the one that does
   *not* search) work. Worth saying out loud that this changed, if you want the re-film to
   read as an update rather than a correction.
2. **Pick the two questions before you roll.** The demo depends on one question genuinely
   triggering a search and one genuinely not. The decision is a judgement and can go either
   way on different days, so test both immediately before filming. Slide 3 offers safe
   candidates: "Who wrote Middlemarch?" for the no-search case, "What did rates do this
   week?" for the search case.
3. **The manual control.** OpenAI's help centre says you can "manually choose search when
   it is available" - the availability wording is theirs, and I could not verify the control
   is present on every tier and surface. The deck says nothing about it. If you want to show
   it, do it in the demo half and describe it in words rather than pointing at it.
4. **Prompt injection is off the slides - is that right?** OpenAI states that fetched or
   cached pages can carry "malicious instructions", and that Lockdown Mode does not stop a
   prompt injection reaching ChatGPT through page content. That is a genuine failure mode of
   web search and arguably belongs somewhere in the course, but not in a one-minute lecture.
   Tell me if you want it as its own short lecture in Part 2 or as a line in Agent Mode.
5. **Overlap check with AI Hallucinations.** Your note on that lecture is to add, at 3:33,
   that search grounds answers but results are written by people. This deck's slide 7 makes
   the same point from the other side ("grounded is not the same as true"). They reinforce
   rather than repeat, but they should not use the same sentence - worth saying them
   differently on the day.
6. **The Birmingham/IP restaurants segment is cut.** It was about a third of the original
   runtime and it was mostly about geolocation being wrong, not about search. Say if you
   want it kept as a throwaway line.
