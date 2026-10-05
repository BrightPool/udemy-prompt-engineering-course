# What are Skills? — build notes

**Slug:** `what-are-skills` · Part 2 · Skills & Plugins · **NEW lecture, never filmed** ·
owner James · 12 slides · linter clean.

Build:

```bash
uv run --with python-pptx python decks/what-are-skills/build_what_are_skills.py \
    decks/what-are-skills/what-are-skills.pptx
uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
    decks/what-are-skills/what-are-skills.pptx
```

---

## The three sentences

- **What it is** — A skill is a named set of instructions, kept somewhere the assistant
  can read, so that a prompt you would otherwise re-type becomes something the tool has.
- **How it works** — Its name and description are always loaded; when what you ask matches
  that description (or you call the skill by name) the instructions are read, and its
  bundled files only when the instructions call for them.
- **Why it matters** — The instructions stop drifting: they live in one file you improve
  once, hand over whole, and get the same behaviour from every run.

## Research

Everything below is **primary-verified** against first-party docs on 2026-09-08. Nothing
on a slide rests on a search summary.

### Anthropic — `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`

(`docs.anthropic.com` now 301s to `platform.claude.com`.)

- Definition: *"Agent Skills are modular capabilities that extend Claude's functionality.
  Each Skill packages instructions, metadata, and optional resources (scripts, templates)
  that Claude uses automatically when relevant."*
- Every skill is a `SKILL.md` with YAML frontmatter. **Required fields: `name` and
  `description`** — nothing else is required. `name` ≤ 64 chars, lowercase/hyphens;
  `description` ≤ 1024 chars.
- The line the whole lecture hangs on: *"The `description` is what Claude matches your
  request against when determining whether to trigger the Skill, so it must say both what
  the Skill does and when to use it."*
- **Progressive disclosure**, three levels, with the doc's own token figures:

  | Level | When loaded | Cost |
  |---|---|---|
  | Metadata (`name` + `description`) | always, at startup | ~100 tokens per skill |
  | SKILL.md body | when the skill is triggered | under 5k tokens |
  | Bundled files and scripts | as needed | nothing until accessed |

  Scripts are the interesting case: they are run through bash and **only their output**
  enters the context, never their code. That is what slide 8's bottom band says.
- Surfaces: claude.ai (upload a zip in settings), Claude Code (`~/.claude/skills/` or
  `.claude/skills/`), the Claude API (`/v1/skills`, needs the code execution tool),
  plus AWS and Microsoft Foundry. **Custom skills do not sync across surfaces** — deliberately
  kept off the slides, it is exactly the kind of fact that will change.
- Security: *"Use Skills only from trusted sources"*; a malicious skill *"can direct Claude
  to invoke tools or execute code in ways that don't match the Skill's stated purpose"*.
  This is why slide 4's caption tells students to treat a stranger's skill like any other
  software they install.

### OpenAI — `developers.openai.com/api/docs/guides/tools-skills` and `learn.chatgpt.com/docs/build-skills`

(`platform.openai.com` 301s to `developers.openai.com`; the Codex/ChatGPT pages 308 to
`learn.chatgpt.com`. All reachable on a plain fetch — headed Playwright was not needed.)

- Definition: *"a versioned bundle of files plus a `SKILL.md` manifest (front matter +
  instructions)"*; *"modular instructions you can use to codify processes and conventions,
  from company style guides to multi-step workflows."*
- Same required frontmatter (`name`, `description`), and the docs say front-matter
  validation *"follows the Agent Skills specification standard"* — i.e. **the two vendors
  are implementing the same open format**. That is the basis for slide 4's claim that the
  shape travels between assistants, and it is the single most durable thing in the deck.
- Layout: `SKILL.md` required; optional `scripts/`, `references/`, `assets/`, and an
  optional `agents/openai.yaml` for UI metadata and tool (MCP) dependencies.
- Two invocation routes, matching slide 7: **explicit** (`@` in ChatGPT, `$` in the Codex
  CLI) and **implicit** (the model activates it when the task matches the description).
  The `@`/`$` characters are deliberately **off the slides** — that is UI, and it belongs
  in your demo.
- Limits, for the demo half if anyone asks: 50 MB zip, 500 files per version, 25 MB per
  uncompressed file, exactly one manifest.

### Reusable prompts are being retired in favour of skills

- Codex docs, verbatim: *"Custom prompts are deprecated. Use skills for reusable
  instructions that Codex can invoke explicitly or implicitly."*
- API side, from the Prompting guide: *"OpenAI is deprecating reusable prompt objects in
  the API. Prompt creation will be de-emphasized beginning June 3, 2026, and `v1/prompts`
  is scheduled to shut down on November 30, 2026."*
- **Not on a slide** — dates and endpoint names drift. But it is a strong line to say on
  camera, because it is the industry conceding the exact point the lecture makes: the
  saved-prompt idea was not enough, and skills are what replaced it.

### The working example in this repo

`.claude/skills/principles-deck/` is a real, working skill and has precisely the anatomy
slide 4 draws: `SKILL.md` (a `name`, a long trigger-heavy `description`, then the
instructions), `references/` (seven markdown files, ~34 KB, none of which is read unless
the instructions send you there), `scripts/` (`deckkit.py`, `check_deck.py` — run, never
read into context) and `assets/` (the .pptx template). **This deck was built by invoking
it**, which is worth saying out loud: the lecture about skills was produced by one.

Good on-camera line: the skill's own description is stuffed with trigger phrases
("principles deck", "re-film", "course slides", "mock UI slide") — not because they read
well, but because that line is the only part that is always loaded and it is the only
thing deciding whether the skill fires.

## The arc

| # | Slide | Carries |
|---|---|---|
| 1 | What are Skills? | title + one-sentence definition |
| 2 | *What is it?* — instructions the assistant already has | mock: a short request answered against rules nobody pasted |
| 3 | A prompt, or a skill | the core distinction, side by side |
| 4 | What is inside one | name / description / instructions / resources → one bundle |
| 5 | A skill is not a connector | the MCP boundary, drawn as a table |
| 6 | *How it works* — matched by description, loaded on demand | four steps |
| 7 | Two ways a skill starts | matched, or called by name |
| 8 | What is loaded, and when | progressive disclosure as stacked bands |
| 9 | The description is the line that decides | the same skill, one clause apart |
| 10 | *Why it matters* — the instructions stop drifting | typed each time vs written as a skill |
| 11 | When to write one down | worth a skill / just type it |
| 12 | Let's see it in action | handoff |

## Review rounds

**Round 1 — hostile reviewer.** Seven changes.

1. Slide 3's caption was making two points (the prompt/skill status change *and* the
   cross-vendor claim). Split: the caption now carries only the distinction, and the
   cross-vendor point moved to slide 4, where the anatomy it describes is on screen.
2. The deck had no honest boundary outside the failure-mode table row. Added three, each
   attached to the visual that earns it rather than as a filler slide: the security point
   on slide 4 (next to "Its resources"), "instructions, not a guarantee" on slide 6.
3. Slide 5's caption said "Students mix these up constantly" — talking about the audience,
   to the audience. Rewritten in direct address.
4. Slide 5 also ended on "has its own lecture", a forward reference that breaks if the
   section is ever reordered. Cut; it is a spoken line.
5. Slide 9 was a strawman: a vague description ("Helps with writing") against a good one.
   Rebuilt as **the same description, one clause apart** — the top row says what it does,
   the bottom adds "Use when…". The highlight pill moved onto the added clause, so the
   pill now points at the thing being taught.
6. Layout: slide 9's rows started at 1.56" while every other slide started at 1.52" —
   moved. Slide 8's caption raised from 2.22" to 2.54" so its centre lines up with the
   diagram beside it.
7. Slide 4's "Its resources" sub-label wrapped to two lines while its three neighbours ran
   to one, so that card's type sat lower than the rest. Shortened to fit.

Linter went from 6 warnings (text-overflow, from compare items and row labels running past
their boxes) to clean; every compare item was cut to fit one line.

**Round 2 — the student.** Six changes, three of them comprehension-level.

1. "Its name and description stay **in view**" reads as "visible to me on screen". Changed
   to "always loaded" on slide 6 and slide 8's top band.
2. Slide 7 said "Weighed against each one" — a dangling reference. Now "each description".
3. Slide 5's table had a mismatched third row: a quoted instruction against a pair of
   actions. Replaced with a parallel test the student can actually apply — *"How should
   this be done?"* vs *"Where does the work live?"*
4. "Rewrite it and hope" → "Rewrite it from memory" (glib, and not parallel with the cell
   beside it). "Rules a new colleague would need told" → "would need". "A link to a system
   that holds your work" → "you already use".
5. Layout: slide 6's caption re-centred against the four steps beside it (2.14" → 1.99").

**Round 3** — run because round 2 turned up three comprehension issues, over the
two-issue threshold. Five changes, one substantive.

1. Slide 9's caption overstated its own example. It claimed the weaker description gives
   the assistant "nothing to match your request against" — untrue, it says what the skill
   does. Corrected to the accurate and more useful claim: it fires only when you happen to
   use its own words back at it, and the "Use when…" half is what names the situations.
2. Slide 2's copy had two "it"s doing different jobs in one sentence. Rewritten.
3. Slide 8: "right up until one is used" → "one of them is used" (two senses of "one").
4. Slide 6: "Only then are the instructions **actually** read" — filler word cut.
5. Slide 4: "Note what it lets in" → "And note what a bundle allows".

Final layout pass: every content slide starts at y = 1.52", nothing crosses y = 5.10",
no dark tables outside a mock, one highlight pill per mock, no screenshots, no menu paths,
no version numbers, no prices.

## For James

**The angle I chose, and why.** You gave no brief, so: I have made this a lecture about
*status*, not about features. The whole deck turns on one line — **a prompt is something
you type this time; a skill is something the assistant has** — and everything else is
consequences of that. The three alternatives I rejected:

- *A tour of what skills can do.* Would date instantly and would collide with
  `practicing-plugins`.
- *A how-to.* That is `creating-skill-chatgpt`, the very next lecture. This deck
  deliberately never shows a `SKILL.md`, never shows `@` or `$`, and never says "here is
  how you make one".
- *A vendor comparison.* Both labs have converged on the same file format, so the
  comparison would be a slide of near-identical columns. Better said in one sentence
  (slide 4) than drawn.

The second half of the deck is built around the claim that **the description is the most
important line in a skill**. That is the durable, cross-platform point, it is the thing
students get wrong, and it sets up `ab-testing-skills` at the end of the section — because
once you accept that the description is a trigger, A/B testing it is the obvious next move.

**Proposed running order for Skills & Plugins.** The manifest order works, with one
suggestion:

1. `what-are-skills` — the concept (this deck)
2. `creating-skill-chatgpt` — build one, generalised
3. `creating-skill-claude` — build one in Claude Co-Work
4. `what-is-mcp` — the protocol behind connectors
5. `practicing-plugins` — connectors → wrap as a skill → invoke or schedule
6. `ab-testing-skills` — improve it systematically

**The suggestion:** consider moving `what-is-mcp` to position 2, directly after this one.
My slide 5 draws the skill/connector line but cannot resolve it, so students carry an open
question through two build lectures before it is answered. Conceptually MCP pairs with
*this* lecture — instructions versus reach — rather than with the building lectures. Your
call; I have written slide 5 so it works either way (it names no lecture and makes no
forward promise).

**Things I would rather you decided.**

1. **Do we say "skill" or "Skill"?** Anthropic capitalises it as a product noun ("Agent
   Skills", "a Skill"); OpenAI lower-cases it. I have used lower-case "skill" throughout
   for the generic idea, which reads better in British prose and stays vendor-neutral —
   but it is a course-wide convention worth fixing once, since it will appear in five
   lectures. Say the word and I will conform the deck.
2. **How hard to push the security point.** Slide 4 carries one clause about a stranger's
   skill running scripts on your behalf. Anthropic's docs are considerably more emphatic
   than that. I kept it to a clause because this is a beginner lecture and I did not want
   the takeaway to be "skills are dangerous" — but if you want it larger it deserves a
   slide of its own rather than a longer caption.
3. **The `v1/prompts` shutdown.** In the research section above, not on a slide. It is a
   great on-camera line ("the saved-prompt feature is being switched off in favour of
   this") but it is dated and vendor-specific, so it is yours to say or drop.
4. **"Connector" vs "plugin".** The section is called *Skills & Plugins* and the manifest
   note for `practicing-plugins` uses "plugins", but neither vendor's current docs call
   them that — Anthropic says connectors/MCP servers, OpenAI says connectors and apps. I
   used "connector" on slide 5. If the course keeps "plugin" as its own word, that is fine
   (the house convention allows our own names) but slide 5 should be re-cut to match so
   students are not learning two words for one thing.

**Deliberately absent from the deck**, and available for the demo half: where skills are
stored on each platform, the `@` and `$` invocation characters, zip and file-count limits,
the fact that custom skills do not sync between claude.ai, the API and Claude Code, and
anything about which plan tier is required.
