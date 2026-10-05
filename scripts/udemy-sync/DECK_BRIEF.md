# Deck brief — one lecture, one agent

Standard instructions for building the principles deck for a single lecture. Every
sub-agent in the re-film fan-out follows this, so 23 decks come back as one course rather
than 23 personal styles.

Your lecture's row is in `scripts/udemy-sync/out/lecture_manifest.json`. The overall goal
is `~/Desktop/GOAL-course-refilm.md`.

## What you are producing

**The principles half of the video**: a deck that teaches what the thing is, how it works
and why it matters. The instructor demos the live product separately, on camera. Anything
that would date belongs in that demo half, not in your deck.

Deliverables:
1. `decks/<slug>/<slug>.pptx` — the deck
2. `decks/<slug>/build_<slug>.py` — the build script that produced it
3. `decks/<slug>/NOTES.md` — your research notes, what changed since filming, and
   anything James needs to decide

## Steps

**1. Read the source.** If `video_id` is set, the transcript is at
`scripts/udemy-sync/transcripts/<section>/*<video_id>*.{json,txt}`. Read the `.txt` for
the argument; use
`python scripts/udemy-sync/transcribe.py show <video_id> --at M:SS` to inspect any moment
James's note references. If there is no video, this is a new lecture — research and
propose.

**2. Read James's note** in the manifest. It is the single most important input: it says
what is wrong with the current lecture. Honour it exactly.

**3. Research the current state.** These lectures were filmed against older product
versions. Establish what is true *now* — the mechanism, the limits, the failure modes.
You are researching the concept, not the click path.

**Sources: know what you can and cannot verify.** Tested from this environment:

| Source | Status |
|---|---|
| `platform.openai.com` (API docs) | reachable — plain fetch **and** Playwright |
| `docs.anthropic.com` | reachable |
| most of the open web | reachable |
| `help.openai.com` (help centre) | reachable **only** via headed Playwright (below) |
| `openai.com` (blog, announcements) | reachable **only** via headed Playwright (below) |

Plain fetch returns 403 and *headless* Playwright gets stuck on "Just a moment…". A
**headed, persistent Chrome** clears the challenge. Verified working:

```bash
source ~/.zshrc >/dev/null 2>&1
eval 'playwright-cli -s=docs open --browser chrome --headed --persistent'
eval 'playwright-cli -s=docs goto "https://help.openai.com/en/articles/8590148-memory-faq"'
eval 'playwright-cli -s=docs snapshot'
```

Use this for any first-party OpenAI page. It opens a visible browser window on James's
machine, so open it once and reuse the session. Do not log into anything and do not touch
his ChatGPT account - you are reading public documentation only.

So anything about ChatGPT's *consumer UI* — screen names, menu labels, whether a
particular list or panel still exists — **cannot be primary-verified here**. Search
summaries quoting those pages are second-hand and can be stale or wrong.

**Playwright is available** for pages that need a real browser (JS-rendered docs, most
sites). It does NOT defeat the Cloudflare challenge on OpenAI's help centre — do not try.

```bash
source ~/.zshrc >/dev/null 2>&1
eval 'playwright-cli -s=docs open'                       # once per session
eval 'playwright-cli -s=docs goto "<url>"'
eval 'playwright-cli -s=docs snapshot'                   # readable page text
```

Use a session name of `docs`. Do not log into anything, do not accept prompts to sign in,
and do not touch James's ChatGPT account — you are reading public documentation only. If
Playwright also fails, fall back to search summaries and tag the claim as unverified.

Two rules follow:
- **Never put an unverifiable UI claim on a slide.** It was already banned; this makes it
  non-negotiable. The deck teaches mechanism, which you *can* verify.
- **Mark confidence in `NOTES.md`.** Anything sourced only from search summaries gets
  tagged `[unverified - James to check on his account]`. Do not launder a search snippet
  into a confident statement of fact.

**4. Separate principle from UI.** Write down, in one sentence each: what it is, how it
works, why it matters. If you cannot, research more before building anything.

**5. Build the deck** with the `principles-deck` skill. Invoke it — do not improvise a
deck. It carries the house style, the template, the mock builders and the linter. Key
rules it enforces:
   - what is it? / how it works / why it matters, as title prefixes (`d.what/how/why`)
   - no divider slides, no pull-quote slides
   - vector mocks, never screenshots; canonical builders where they fit
   - light tables, 12pt minimum on white, nothing past y=5.10"
   - ends on `d.handoff(...)` — "Let's see it in action"

**6. Lint until clean.**
```bash
uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py decks/<slug>/<slug>.pptx
```
Zero errors. Warnings need a stated reason.

**7. Two rounds of adversarial review**, per `references/review-loop.md`, including the
layout pass. Rebuild and re-lint between rounds. Record in `NOTES.md` what each round
found and changed.

## Shared facts, verified 2026-09-08

Checked directly against `platform.openai.com/docs/models` (reachable). Do not
re-research these; do not print them on a slide.

- **The flagship is GPT-6 Astra** ("our most capable model, built for the hardest
  end-to-end work"; for complex reasoning and coding). Below it sits the **GPT-5.6**
  family: **Sol** (flagship for complex professional work), **Terra**, **Luna**, **Cyber**.
  GPT-4o still exists for older/cheaper work.
- **GPT-5 is two generations back.** James's original notes say "update to GPT-5" - that
  instruction was written before this lineup. Teach the generational point, never a
  version number; the current names live in `NOTES.md` for the instructor.
- **Reasoning effort is a documented dial**, at `/docs/guides/reasoning#reasoning-effort`.
- **Memory** (primary-verified from the Memory FAQ, 2026-09-08): controls live at
  **Settings > Personalization > Memory**. The current surface is a written **memory
  summary** you correct by typing into a box at its foot or highlighting a line; the
  legacy list is demoted to a "saved memories" link beneath it. Memories now update
  automatically (the FAQ's own example: "I'm training for a marathon" later corrected by
  "I sprained my ankle"). Sources for a reply are shown under the **book icon**. Full
  deletion requires removing every source, "including past chats, archived chats, files".
- **ChatGPT is now three modes** (primary-verified, help centre article
  `20001275-chatgpt-work-and-codex`, and `11752874-chatgpt-agent`):
  - **Chat** - "fast, conversational assistance and everyday questions"
  - **Work** - "an agent designed for longer, multi-step work and finished deliverables"
  - **Codex** - "dedicated to software development and technical work" (desktop app)

  And explicitly: **"ChatGPT agent is no longer available. Use ChatGPT Work."** So the
  capability our course calls "Agent Mode" now lives in **Work**. Teach the loop, never
  the label; the mapping goes in NOTES.md for the spoken track.
- OpenAI's current developer docs do **not** use the labels "Agent Mode", "Deep Research"
  or "Data Analysis". The capabilities exist; the names in our course are ours. Keep the
  course's names for consistency, and do not claim they are what the product calls them.

## House conventions

- **British English** in our own copy (artefacts, colour, organise, parallelising).
  Product names and UI labels stay verbatim as the vendor spells them
  ("Customize ChatGPT", "Personalization").
- **Mock windows**: `ChatGPT` / `Demonstration` when showing the product,
  `AI Assistant` / `Example` for a generic prompt pattern. Turns are
  `User` / `AI Assistant` / `System`.
- **No specific prices, no version-specific UI positions, no menu paths** in the deck.
  Those date fastest and belong in the demo half. Teach the *principle* and put the
  current specifics in `NOTES.md` for the instructor to say aloud.

  **Cost, specifically.** Do not put dollar figures on a slide. Teach instead that a
  token's price depends on which of three buckets it falls into:

  | Bucket | What it is | Relative cost |
  |---|---|---|
  | **Input tokens** | what you send - your prompt, files, history | baseline |
  | **Cached input tokens** | repeated prefix content the provider already has | heavily discounted |
  | **Output tokens** | what the model generates | the most expensive, several times input |

  That structure is durable: the numbers move constantly, the three buckets do not. It
  also teaches something actionable - a long prompt is cheap next to a long answer, and
  reusing a stable prefix is cheaper still, which is why caching exists. Put today's
  actual rates in `NOTES.md`, not on a slide.
- **Do not clone the reference example.** The skill's docs demo `s.layers(...)` with a
  "what actually reaches the model" slide ending in a node called *One flat context*.
  That pattern is genuinely central — memory, web search, custom instructions and
  projects all come down to what lands in the context — so you are encouraged to use it.
  But students watch these lectures back to back, and three identical slides read as
  copy-paste.

  So: keep the *frame*, never the *words*. The title must name what is specific to your
  lecture ("What arrives before you type", "Your question plus the pages it fetched"), the
  bands must be that feature's actual components, and the closing node must be your own
  phrasing. If your slide would survive being pasted into another lecture unchanged, it is
  too generic to earn its place.
- **Skills & Plugins terminology (VERIFIED 2026-09-08 - corrects an earlier note).**
  Read directly from `developers.openai.com/plugins.md`. All three words are current
  and they mean different things:

  | Term | What it is |
  |---|---|
  | **skill** | a repeatable workflow - instructions the assistant follows |
  | **MCP server** | what gives a plugin "tools and access to external systems" |
  | **plugin** | the distributable bundle: "plugins combine skills, MCP servers, and optional UI" |

  OpenAI's own doc section is titled **Plugins**, with pages "Package your plugin:
  assemble skills and MCP server dependencies into a distributable plugin" and
  "Skills: add repeatable workflows around MCP tools".

  So **James's section name "Skills & Plugins" is current and correct**, not legacy.
  An earlier version of this brief claimed neither vendor uses "plugin" any more.
  That was wrong. Use all three words with the meanings above; do not use "plugin"
  and "connector" as synonyms - a connector/MCP server is the link, a plugin is the
  bundle that ships around it.
  - "skill" stays lowercase in our prose; capitalise only when quoting a vendor.

- **Code goes through Carbon, always.** Never flat monospace text on a rectangle.
  Use `code_image()` from the skill's `scripts/code_image.py` - it wraps the Carbon
  CLI with the house theme and caches by content hash. Needs `npm install -g
  carbon-now-cli` once per machine.
- **Exercises use `d.exercise(title, minutes=n)`.** One banner, every deck, so the
  pink band always means "your turn". Do not hand-build an exercise header.
- **Call the feature by its name.** Do not invent a shorthand for it - no "the store",
  "the surface", "the layer". Students learn the word the product uses, and a coined term
  makes the lecture harder to search and harder to follow. Write "memory", "projects",
  "web search".
- **Length**: 10 to 14 slides. A short lecture gets a short deck — the 00:35 Shortcuts
  lecture does not need 12 slides.

## What to escalate rather than guess

Put these in `NOTES.md` under `## For James` instead of inventing an answer:
- The note references a UI that you cannot verify still exists.
- Research contradicts what the original lecture teaches.
- The lecture seems to overlap another one in the manifest.
- A new lecture has no brief and you had to choose the angle.

## Report back

Finish with a short summary: the three one-sentence principles, the slide count, the lint
result, what each review round changed, and anything in `## For James`. Keep it tight —
it is read alongside 22 others.
