# Deep Research - build notes

Deck: `decks/deep-research/deep-research.pptx` (11 slides)
Build: `uv run --with python-pptx python decks/deep-research/build_deep_research.py decks/deep-research/deep-research.pptx`
Lint: `uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py decks/deep-research/deep-research.pptx` -> clean, 0 errors, 0 warnings.

## The three principles

- **What it is** - an investigation you delegate: one question worth an afternoon goes
  in, and a written, cited report comes back instead of a chat reply.
- **How it works** - it turns your question into a plan, writes its own search queries,
  opens and reads pages, notices what is still missing, and searches again until more
  searching stops changing the answer.
- **Why it matters** - it moves your afternoon from finding sources to judging them, and
  the price of that is time, tokens, and a report whose weakest source looks exactly like
  its strongest.

## Research: what is true now

Primary sources were partly unreachable to automated fetching (help.openai.com and
openai.com both return 403 to a non-browser client), so the OpenAI Help Centre detail
below comes from search-engine summaries of that page rather than a direct read. The
developer docs and the encyclopaedia entry were read directly.

**Mechanism.** Deep research is agentic and multi-step: it "finds, analyzes, and
synthesizes hundreds of sources to create a comprehensive report at the level of a
research analyst", and the run is a genuine tool loop - each web-search call carries an
action of `search`, `open_page` or `find_in_page`. Output messages carry annotations
(`url`, `title`, `start_index`, `end_index`) that bind a cited span of the report to the
page it came from. That is the durable shape the deck teaches.
(<https://developers.openai.com/api/docs/guides/deep-research>)

**Clarify, then plan.** An intermediate model clarifies intent before the research starts.
Since early 2026 ChatGPT also proposes a **research plan you can review and modify before
it runs**, you can follow progress live, and you can **interrupt mid-run** to refine focus
or add sources. This step did not exist when the lecture was filmed and is the single most
useful control a student has.

**Scoping.** You can point it at uploaded files, restrict searches to trusted sites, and
connect it to apps/MCP (Feb 2026) and to SharePoint, OneDrive, Dropbox and Google Drive
(Mar 2026). Deck teaches this as "narrow where it may look before it starts" - no product
names on the slide.

**Duration.** 5 to 30 minutes typically; the API docs say runs "can take tens of minutes"
and recommend background mode and raised timeouts. James's filmed estimate ("a few minutes
to 10, 20 minutes") is still broadly right.

**Model.** Launched on an o3 variant; moved to a GPT-5.2-based deep research model in
February 2026, with better steering and scope limiting. No model name appears on a slide.

**Honest limits, from OpenAI itself.** It "occasionally produces factual errors", "may
also reference rumors, and may not accurately convey uncertainty". Separately, the wider
literature on chatbot citations is unkind: fabricated or malformed references are common
enough to have caused retractions, and RAG-style grounding reduces but does not remove it.
It also cannot open what it cannot reach - paywalled journals, anything behind a sign-in.
Slides 7 and 9 carry this.

**Benchmark, for the spoken track only.** The o3-based version scored 26.6% on Humanity's
Last Exam against GPT-4o's 3.3%. Not on a slide - benchmark numbers date fast.

Sources:
[OpenAI: deep research API guide](https://developers.openai.com/api/docs/guides/deep-research) ·
[OpenAI Help Centre: Deep research in ChatGPT](https://help.openai.com/en/articles/10500283-deep-research-in-chatgpt) ·
[ChatGPT Deep Research (encyclopaedia entry)](https://en.wikipedia.org/wiki/ChatGPT_Deep_Research) ·
[ChatGPT Business release notes](https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes) ·
[Fabrication and errors in ChatGPT bibliographic citations](https://www.nature.com/articles/s41598-023-41032-5)

## What changed since filming

| In the 2024/25 recording | Now |
|---|---|
| "It's a button here that you press" | No dedicated button. Ask for deep research in plain words. The **legacy deep research mode was removed on 26 March 2026**; only the current experience remains. |
| Pick a model first, "the pro model is much better" | Model choice is no longer the lever. The deep research model is selected for you. |
| "$200 a month pro account" gate | All paid tiers and even free accounts get some runs; the numbers move constantly. No price or quota on a slide. |
| Clarifying questions on submit | Still there, **plus** a proposed research plan you can edit before it starts, live progress, and mid-run interruption. |
| Searches the open web only | Can also be scoped to uploaded files, trusted sites, connected apps and cloud drives. |
| "It looked at 28 different sources" | Still the right order of magnitude. The deck reuses 28 as an example run, not a spec. |

## Review rounds

**Round 1 - the hostile reviewer.** Five findings, all fixed.
1. Slides 3 and 8 were the same comparison twice (time / breadth / output). Slide 3 kept
   as the boundary against the sibling `web-search` lecture; slide 8's table rewritten
   onto consequences - where your afternoon goes, what you must check, your confidence,
   failure mode.
2. The slide 2 mock jumped from a clarifying question to a finished report with no sense
   of the wait. The highlight line now reads "Done in 9 minutes. 28 sources, cited inline."
3. The plan step - the cheapest place to steer a run - was implicit only. Named in the
   slide 6 caption.
4. Layout: content tops were ragged at 1.52 / 1.56 / 1.58. Slides 5, 7 and 8 moved to
   1.56, so every slide but the layout-fixed two-column one now starts at the same y.
5. Layout: the slide 5 caption opened with an ellipsis and read as a fragment; rewritten
   and re-seated under the column it describes.

Two earlier lint errors were fixed before round 1: the slide 2 mock overran the footer
band, and the fan diagram's thin horizontal connectors were being read as accent rules
competing with the title divider (they are now arrows, which is also more legible).

**Round 2 - the student.** Four findings, all fixed.
1. The fan on slide 5 implied the searches run in parallel, which contradicts the loop on
   slide 6. Caption now says they are "written as it learns what to ask next".
2. Slide 7 claimed the model "has no way to tell you which source it leaned on hardest" -
   not true, citations do that. Corrected to the real gap: nothing in the mechanism ranks
   one source above another.
3. "Confidence" as a table row label is opaque at 1.5x. Now "Your confidence".
4. An obvious student question - "can I control where it looks?" - went unanswered.
   Slide 9's copy now ends on it, phrased so it survives a redesign.

Layout pass, both rounds: every content top is 1.56 (slide 10 is 1.58, fixed by the
two-column layout's placeholder). Nothing crosses y=5.10; the lowest content sits at
4.98. Copy beside a mock uses `s.beside()` on all three mock slides.

## Deliberately not on a slide

- **How to trigger it.** James's note is the reason. It has changed once and will change
  again. Say it out loud in the demo half.
- **Run quotas per tier, and any price.** Both stale within months.
- **Model names and benchmark scores.**
- **Cost figures.** The durable teaching is the three token buckets - input, cached input
  (discounted), output (the expensive one). Deep research is output-heavy: it reasons and
  writes far more than it reads, which is exactly why it is metered by run rather than
  sold as an unlimited button. Slide 8's caption teaches that shape without a number.

## For James

1. **Check the invocation wording on the day.** I could not read OpenAI's help centre
   directly (it blocks automated fetching), so my description of "ask for deep research"
   rests on secondary summaries of that page. Confirm it live before the take - the deck
   is safe either way because it never says how to start a run.
2. **Do not quote a quota.** The per-tier run limits I could find date to mid-2025 and are
   almost certainly wrong now. If you want to mention them, read them off the screen.
3. **Drop the "$200 pro account" framing from the old script.** Deep research is no longer
   gated the way it was, and model choice is no longer the lever it was.
4. **Demo the research plan.** It did not exist when you filmed, it is the strongest
   control a student has, and interrupting a run mid-flight to redirect it is the single
   most impressive thing to show. Slide 6 sets it up as "step one is your cheapest moment
   to steer it".
5. **Boundary with the `web-search` lecture.** Slide 3 draws the line explicitly (one
   lookup inside one answer vs. an investigation across dozens). If the web-search deck
   also draws it, one of the two should defer so the pair does not repeat itself.
6. **Your Claude-summarising trick is not in the deck.** Pasting the report into another
   model to get something less dry is a good aside and fits the course's model-agnostic
   line, but it is a workflow tip, not a principle. Worth 20 seconds in the demo half.
7. **The memetics example is reused throughout** (slides 2, 4, 5) so the mocks tell one
   continuous story. If you demo a different question live, say so, or use the same one.
