# Exploring Other Model Providers - build notes

New lecture. No source video, no transcript. James's note: *"We are MODEL AGNOSTIC.
Cover the other AI labs: Anthropic (Claude), xAI (Grok), Google (Gemini)."*

## The three principles

- **What it is** - several independent labs build these assistants, and each ships both a
  chat product and an API of essentially the same shape.
- **How it works** - every one of them assembles a request the same way (a system
  instruction, the conversation so far, files and tool results, your message) and exposes
  the same handful of controls under different names.
- **Why it matters** - because the interface is shared, the skill is portable: what you
  learned on one assistant works on the others, and you choose per task rather than
  committing to one vendor.

## Research

Primary-verified 2026-09-08 unless tagged otherwise.

### The shared surface (this is the whole lesson)

Every claim on the deck's mechanism slides was checked against at least two vendors'
first-party docs.

| Concept | Anthropic | Google | xAI |
|---|---|---|---|
| System instruction | system message / `system` | `system_instruction` | `system` role |
| Reasoning effort dial | `output_config.effort`, five levels (`low`…`max`) | `thinking_level` | `reasoning_effort` (`low`…`xhigh`) |
| Tool use | documented, all current models | function calling, code execution, computer use | tool messages, agentic tool calling |
| Long context | 1M tokens on the current top tier | 1M tokens documented since Gemini 2.0 Flash | 500k-1M depending on model |
| Cached input discount | prompt cache reads at a fraction of base input | implicit caching, automatic on 2.5+ | cached input priced separately |

Sources:
- `platform.claude.com/docs/en/models/overview` (docs.anthropic.com now 301s here)
- `platform.claude.com/docs/en/build-with-claude/effort`
- `ai.google.dev/gemini-api/docs/models`, `/text-generation`, `/caching`
- `docs.x.ai/overview`, `docs.x.ai/developers/model-capabilities/text/reasoning`

Two things worth James saying aloud that are too specific for a slide:

1. **xAI's API is OpenAI-compatible.** `docs.x.ai/overview` shows the OpenAI Python client
   pointed at `base_url="https://api.x.ai/v1"`. That is the single most concrete proof of
   the lecture's thesis - the same code, one line changed. It is also exactly the kind of
   detail that could change, so it stayed off the slides.
2. **Anthropic's effort parameter recently moved** from a top-level field into
   `output_config`. A good live example of why the deck teaches "reasoning effort" the
   concept and never a parameter name.

### Characterising the labs (slide 3)

Deliberately about the *company*, never the model. Each line is a structural fact that has
held for years, not a capability claim:

- **Anthropic (Claude)** - a research lab that put model safety and behaviour at the
  centre of its public positioning.
- **Google (Gemini)** - the lab sits inside a search and productivity company, so the
  assistant is wired to documents and mail.
- **xAI (Grok)** - built alongside a live social feed, so it leans on what is being posted
  now.
- **OpenAI (ChatGPT)** - took the chat assistant mainstream; the product this course
  demonstrates on.

### Consumer feature parity [partly unverified - James to check]

Primary-verified from `support.claude.com`: Claude.ai documents projects, memory, web
search, connectors, artifacts, file upload and skills. Verified from
`support.google.com/gemini`: Gems are configured with a persona, task, context and format,
and accept uploaded files - i.e. the Gemini equivalent of custom instructions plus
projects.

Gemini's Canvas, Deep Research, Gemini Live, scheduled actions and connected apps, and
Grok's DeepSearch, Think mode and voice, came from **search summaries only**. I did not
put any of them on a slide, and the deck's parity claim is made at the level of
categories, which holds regardless. If James wants to name them on camera, worth a
30-second check first.

### Time-sensitive material, kept off the slides

- Current flagship names across all four labs. Per the shared brief, OpenAI's lineup is
  led by GPT-6 Astra over the GPT-5.6 family; Anthropic's page currently leads with Claude
  Opus 5 and Claude Fable 5.1. **None of this belongs on a slide** and it will be wrong
  before the course is re-cut.
- Today's per-token rates. Anthropic publishes them per model; Google and xAI publish
  their own. The deck teaches the three buckets only.
- Search results repeatedly render xAI's docs under the title "SpaceXAI Docs". The
  first-party pages themselves say **xAI** throughout, so the deck says xAI. Flagging in
  case a corporate change is in flight. [unverified]

### The two existing decks

`What is Anthropic Claude_.pptx` and `What is Google Gemini_.pptx` are a useful negative
example. They carry "the current best model", "GPT-4 Level Performance" and
"200k Token Window!" - three claims that were all wrong within months. Nothing from either
deck was reused.

## Review rounds

**Round 1 - the hostile reviewer.** Six findings, all fixed.

1. *Substance, the big one:* the deck had 11 slides and three of them made the same
   two-column claim - slide 5's "what differs between labs", slide 8's "you relearn", and
   slide 10's "changes every few weeks". **Cut slide 10 entirely** and folded its lesson
   (leaderboards and flagship names churn; the concepts do not) into slide 9's caption,
   where it directly supports "not one of these is a benchmark score". Deck went 11 → 10.
2. *Layout:* on slide 3 the four lab cards had characterisations of unequal length, so the
   two-line subs pushed their labels up and the left and right cards in each row sat 0.10"
   out of alignment. Rewrote all four to the same line count; they now align exactly.
3. *Layout:* visuals started at three different heights across slides 4, 6 and 9
   (1.56 / 1.66 / 1.62) and their captions at 1.72 / 1.80 / 1.80. All unified to 1.56 and
   1.70.
4. *Layout:* slide 6's three cost bands left the slide top-heavy; bands grown from 0.74"
   to 0.86" so the composition carries down the page.
5. *Craft:* slide 2's mock answer mixed three sentence forms; made consistent
   ("Section N - what it commits you to").
6. *Copy:* slide 4 ended on "the address changes", which is jargon. Now "the lab on the
   other end changes; the anatomy of the request does not".

**Round 2 - the student.** Four substantive findings, which is why a third round ran.

1. *Factual inconsistency:* the closing slide said "find the same **four** dials" while
   slide 5 teaches five concepts. Now "find the same controls".
2. *Unanswered question:* a beginner reading "run your own prompt on two of them" hears
   "buy four subscriptions". Slide 9's caption now ends "most people settle on two, and
   rarely pay for more than one".
3. *Titles at 1.5x:* "more than one lab sells this same box" and "Who builds them" were
   both opaque read cold. Now "the same kind of assistant, from several labs" and (after
   round 3) "Four labs, and what shaped each one".
4. *Clarity:* slide 6's cost notes read "baseline / heavily discounted / several times
   input" - the last one is ambiguous. Now "the baseline / a fraction of that / several
   times that".

**Round 3 - hostile reviewer again, plus the layout pass.** Five findings.

1. *Substance:* slide 7's "Assumes it already remembers you" was a bad example - memory
   exists on Claude and Gemini too, so it is not a portability failure. Replaced with
   "Points at a saved setup by name", which genuinely does not travel.
2. *Copy:* slide 2 opened on "OpenAI is not the only lab building these" - a negation
   about a competitor, with "these" having no antecedent that early. Rewritten to stand on
   its own.
3. *Craft:* slide 9's caption had grown to thirteen lines of 12pt beside a diagram.
   Trimmed by a third.
4. *Layout:* slide 7's caption sat 0.16" under the compare panels and 0.07" off the footer
   band. Panels shortened to 2.74" and the caption raised to 4.50".
5. *Title:* "The four labs you will meet" promised an encounter the course does not
   deliver for all four. Now names what is actually on the slide.

Linter clean after every round: `clean - 10 slides, nothing to fix`.

## For James

1. **Where it should sit in the running order.** As placed, this is the last lecture of
   Part 2's ChatGPT arc and the pivot into Skills & Plugins - and that is the right slot.
   The whole deck is built as a *widening* move that only works once students already know
   what a system instruction, a context window and reasoning effort are. Moving it earlier
   would break slides 4, 5 and 6, all of which assume the Part 1 tokens lecture and the
   Reasoning Models lecture have already landed. **Recommendation: keep it exactly where
   the manifest has it.**

2. **Overlap with the Skills & Plugins lectures - one real collision.** Slide 5's "Tools"
   row and slide 4's "Files and tool results" band are the first time the course explains
   that a model can call out to something. `what-is-mcp` and `what-are-skills` both need
   to teach that too. I kept this deck's treatment to one table row and one diagram band
   deliberately, so those lectures have room. Worth telling whoever builds them that the
   concept has already been introduced here and should be *deepened*, not re-introduced.
   The softer overlap is `creating-skill-chatgpt`, whose note says "generalise across
   platforms - Anthropic and OpenAI both have connectors". That is this lecture's thesis
   applied to one feature; it will land better because this one came first, but the two
   should not both spend a slide arguing for model-agnosticism.

3. **A deliberate omission you may disagree with.** There is no slide comparing what the
   labs are good at, and no model named anywhere. Your note asked for the labs to be
   covered, and the temptation is a strengths table - but that is the single fastest-dating
   thing we could put on a slide, and this lecture would need re-cutting every quarter.
   The deck characterises the *companies* instead (slide 3), which has held for years. If
   you want to say "Claude is currently the one I reach for when writing" on camera, that
   is the right place for it: a spoken aside costs one take to update, a slide costs a
   rebuild.

4. **Worth saying on camera, kept off the slides.** The xAI API accepts the OpenAI SDK
   with one changed line (`base_url="https://api.x.ai/v1"`). It is the most concrete
   possible demonstration of the lecture's whole point, and it is a ten-second aside.

5. **Suggested demo for the second half**, matching the closing slide: take the contract
   prompt from slide 2, run it in a second assistant, open its settings and point at the
   system-instruction box, the tool list and the effort control, then read both answers
   side by side and talk about style rather than which one "won".

## Updated 2026-09-26 (James)

- Slide 3 is a logo row, no boxes. Claude and ChatGPT icons come from the installed macOS apps; the Gemini mark ("Google Gemini icon 2025.svg") and Grok mark ("Grok-2025-logo.svg", cropped to the square mark) from Wikimedia Commons. Files in `assets/`.
- Slide 4 copy condensed to two lines.
- Slide 6 "Three cost buckets" replaced with a 3-minute exercise: for Claude, Gemini, Grok and ChatGPT, find the cheapest paid plan and the API price per million input/output tokens. Links (checked 2026-09-26): claude.com/pricing, claude.com/pricing#api, gemini.google/subscriptions, ai.google.dev/gemini-api/docs/pricing, grok.com/plans, docs.x.ai/developers/models, chatgpt.com/pricing, openai.com/api/pricing (OpenAI pages block scripted checks but are the standard pricing pages).
- Removed "The prompt is the portable part, not the product" (too generic).
- "Choosing per task" caption replaced with leaderboard links: arena.ai/leaderboard (LMArena), artificialanalysis.ai/leaderboards/models, openrouter.ai/rankings, epoch.ai/benchmarks.

## Round: visual upgrade (2026-09-28)

- Slide 2: the paragraph beside the mock became a 2x2 grid of the four lab logos ("Same shape, four labs") and one line.
- Slide 4: the request stack now has an icon per part (Lucide, ISC licence) and fans out from "One request" to the four lab logos.
- Slide 5: the dials table became icon rows (tokens, context window, system instruction, tools, reasoning effort).
- Slide 6: each pricing row is grouped.
- Slide 7: bullet columns became two icon panels, "Transfers Unchanged" (pink) and "You Relearn".
- Slide 8: the numbered steps became icon question cards; trophy icon on the leaderboard heading.
- Related shapes are grouped throughout. Icons live in `assets/icon-<name>-<ink|pink|white>.png`.
