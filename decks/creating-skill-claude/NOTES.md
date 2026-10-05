# Creating a Skill in Claude Cowork (Anthropic) - deck notes

**Slug:** `creating-skill-claude` · Part 2 · Skills & Plugins · NEW VIDEO, no transcript
**Deck:** `creating-skill-claude.pptx`, 12 slides, built by `build_creating_skill_claude.py`
**Lint:** clean, 0 errors, 0 warnings.

## The three principles

- **What it is** - a skill is a folder you hand Claude: one `SKILL.md` naming the job and
  saying when to do it, plus the references, scripts and templates that job depends on.
- **How it works (for the author)** - because most of the folder is not loaded until it
  is needed, you write a short instruction page and bundle everything else behind it, and
  you write the description as a testable sentence rather than a label.
- **Why it matters** - a skill carries what a prompt cannot, goes wrong in one place you
  can open and fix once, and travels as a folder rather than being trapped in one chat.

## The angle I chose, and why

James gave no brief, so this is a proposal.

The manifest already has `creating-skill-chatgpt` teaching the **anatomy** generically
(name, description, instructions, resources), `what-are-skills` teaching the concept, and
`what-is-mcp` teaching connectors. Re-teaching anatomy here would be the third telling of
the same thing in one section, so this deck does not.

**Division of labour with `what-are-skills`, settled after both decks were drafted:** that
lecture runs first and **owns the mechanism** - matched by description, loaded on demand,
what is loaded and when. This deck assumes the student already knows *that* loading is on
demand, and teaches **what to do about it when you are the one writing the skill**: what
goes in the page and what goes in the folder, how to shape the instruction page, and how
to write a description you can test. That is material the concept lecture cannot cover,
because it never builds one.

The worked example is **`.claude/skills/principles-deck/` in this repository** - the real
skill that built every deck in this re-film, including this one. It is the strongest
example available: it has all four parts, it is in daily use, and it can be opened on
camera. Slides 3 and 6 refer to it directly.

I deliberately left three things to their own lectures: plugins (which in Cowork bundle
skills, connectors and sub-agents), connectors/MCP, and A/B testing a skill.

## Research, and confidence

All primary-verified from first-party pages on 2026-09-08. `docs.anthropic.com` now
redirects to `platform.claude.com/docs`; `support.claude.com` articles redirect to
`academy.claude.com` in places.

**Verified:**

- **A skill is a folder with a `SKILL.md`.** Required frontmatter is `name` and
  `description` only. `name`: max 64 chars, lowercase/numbers/hyphens, cannot contain
  "anthropic" or "claude". `description`: max 1,024 chars, must say *what it does and
  when to use it*, and must be written in the **third person** because it is injected into
  the system prompt. (platform.claude.com Agent Skills overview + best practices)
- **Progressive disclosure, in three levels.** Level 1 metadata (name + description),
  always loaded at startup, roughly **~100 tokens per skill**. Level 2, the `SKILL.md`
  body, read only when the skill is triggered, target **under 5k tokens / under 500 lines**.
  Level 3, bundled files, **zero cost until accessed**; scripts are *run*, so only their
  output enters context, never their code. Docs' own line: "until a Skill is triggered,
  only its name and description occupy context."
- **Where skills work:** claude.ai (chat), **Claude Cowork**, Claude Code, and the Claude
  API. Anthropic ships pre-built document skills (pptx, xlsx, docx, pdf); custom skills
  are yours.
- **Skills do NOT sync across surfaces.** Docs are explicit: a skill uploaded to claude.ai
  is not available on the API, Claude Code skills are filesystem-based and separate from
  both. This is on slide 8 as a stated boundary and in slide 10's caption.
- **Sharing scope differs by surface:** claude.ai is per-user (no org-wide admin
  distribution of custom skills); the API is workspace-wide; Claude Code is personal or
  per-project.
- **Security.** "Use Skills only from trusted sources." A malicious skill can direct
  Claude to run code or invoke tools outside its stated purpose; treat installing one like
  installing software. This is slide 8's "you vouch for it" line.
- **Claude Cowork** (product page, claude.com/product/cowork): "Claude Cowork completes
  tasks you can steer from anywhere. Give it a goal, and it works across your files and
  tools." It "runs on web, desktop, and mobile". The page names skills, plugins
  ("Bundle any skills, connectors, and sub-agents together to turn Claude into a
  specialist"), connectors and scheduled tasks.
- **The format is an open standard.** agentskills.io: "The Agent Skills format was
  originally developed by Anthropic, released as an open standard, and has been adopted
  by a growing number of agent products." Adopters listed there include Cursor, VS Code /
  GitHub Copilot, Gemini CLI, OpenCode, Goose and ChatGPT & Codex. This is slide 10.

**For the spoken track, not on a slide (drifts, or is plan-gated):**

- **Claude can build the skill by watching you.** The help centre's "Creating custom
  skills" article: "Record yourself doing a task and let Claude build the skill from what
  it observes", available on **Pro, Max and Team plans in Cowork in Claude for Mac**. Also
  "Edit with Claude" for iterating on a skill by highlighting text. This is the single
  best demo beat for a no-code audience, but it is plan-gated and Mac-only, so it stayed
  off the slides. Say it aloud.
- Upload format for the chat surface is a **ZIP whose root is the skill folder itself**,
  not a subfolder. Pure click-path detail; demo half.
- Enterprise organisations can turn on **skill content scanning** for custom skills
  uploaded in claude.ai and Cowork.
- Runtime differs by surface: Claude Code skills have full network access, API skills have
  none and cannot install packages.

Nothing in the deck is sourced only from search summaries.

## What each review round changed

### Re-cut of the how phase (after cross-deck comparison)

The first draft's slides 5-7 taught the mechanism - "only the description is always
loaded", "what Claude is holding when the job starts", "the description is the line worth
agonising over". Compared against `what-are-skills`, that collided three times in adjacent
lectures. The mechanism was handed to that deck; these three were re-cut to the authoring
consequences:

| Was | Is now |
|---|---|
| How it works - only the description is always loaded | **How it works - you write a page, and bundle everything else** |
| What Claude is holding when the job starts | **The instruction page is a table of contents** |
| The description is the line worth agonising over | **Writing a description you can test** |

- **Slide 5** is now the authoring rule and its test: the steps of the job go on the
  instruction page, the detail behind one step goes in a bundled file. The test row is the
  usable part: *would you say it every time* (page) or *only sometimes* (file)?
- **Slide 6** teaches the pattern the docs recommend and our own skill uses: the
  instruction page is barely more than the steps plus a set of pointers, each naming a file
  and saying what it is for. The mock shows that shape from `principles-deck/SKILL.md`.
- **Slide 7** treats the description as a writing task with a test, in five steps: third
  person, what plus when, the words you would actually type, read it beside your other
  descriptions, then ask for the job **without naming the skill**. Only the last step tells
  you anything.

The layers diagram ("what actually reaches the model") was cut with the mechanism. That is
normally the most valuable slide in a principles deck, so it matters that
`what-are-skills` carries it - flagged below.

**Round 1 - the hostile reviewer.**

1. *Slides 2 and 3 made the same list.* The folder tree on 2 and the table on 3 both
   enumerated `SKILL.md` / `references` / `scripts` / `assets`. Slide 3's table was
   rewritten to be about the **material and its size** ("a page of plain English", "a shelf
   of documents") rather than the file names, so the two slides now do different jobs.
2. *Slide 6's caption was factually wrong and would drift.* It counted "six other reference
   files, two scripts" - the folder actually holds seven references and four scripts, and
   those counts change every time the skill is edited. Counts removed.
3. *Slide 3's caption was clumsy and arguably wrong* ("nothing in it is code you had to
   write"). Replaced with the point it was reaching for: the description and the
   instructions are ordinary prose, so you do not have to write the scripts.
4. *The deck promised Cowork and delivered generic skills.* Slide 10 now names Claude
   Cowork, a chat and Claude Code as the places the same folder can sit.
5. *An honest boundary was missing.* The docs are explicit that skills do not sync between
   surfaces; added to slide 8 ("Installing itself everywhere you work") and stated
   precisely in slide 10's caption: what travels is the folder, not the installation.
6. *Slide 9's caption said a skill "fails in public"*, which is vague. Rewritten to the
   actual benefit: it goes wrong in one place you can open.
7. **Layout.** Visuals started at 1.52", 1.55", 1.56", 1.58" and 1.70" across the deck -
   all normalised to **1.56"**, with the two how-phase captions both at 1.62". Slide 2's
   folder listing used space-padded pseudo-columns, which do not align in Arial; rebuilt as
   an indented tree with the glosses moved into the copy. On slide 10 one node's sub-label
   wrapped to two lines while its neighbours did not, throwing the three labels out of
   alignment by 0.06"; shortened, and the surface names moved into the caption.

**Round 2 - the student.**

1. *Slide 4 used "in front of the model" and "loaded on demand" one slide before either
   was defined.* Reworded to "Something you carry into every chat" and "Opened only when
   the job matches it", which stand on their own.
2. *Two different panels were both labelled "Skill folder"* (the listing on slide 2 and the
   limits panel on slide 8), which reads as the same window showing different things. The
   limits panel is now "Scope of a skill".
3. Copy fix: "the words you would actually type when you wanted it" to "when you want it".

Two substantive findings in round 2, so no third round.

**Round 3 - hostile, over the re-cut.**

1. *I dropped "Where a skill stops" while replacing the how phase.* The limits slide sat
   inside that block and went out with it, leaving the deck with no honest boundary and no
   security line. Restored, unchanged, as slide 8.
2. *Slide 6's copy no longer fitted its mock.* With the fixed `beside()` measuring the
   text, the copy needed 3.12" against a 2.44" panel, so it clamped to the top of the
   canvas and the pairing read bottom-heavy. Cut a sentence; the block now centres on the
   mock at 2.44".
3. *Slide 5's caption still re-explained on-demand loading*, which the earlier lecture now
   owns. Trimmed to the authoring rule plus its one justification.

Lint clean after each rebuild, against the current `deckkit`/`check_deck.py` (the
text-overflow check now measures placeholder copy, which is what caught finding 2).

## For James

1. **The product is spelled "Claude Cowork", one word.** The manifest title says
   "Claude Co-Work". The deck uses Cowork; worth fixing the lecture title to match.
2. **I chose the angle - progressive disclosure - because you have no brief here.** If you
   would rather this lecture be the hands-on "here is how you make one" and let
   `what-are-skills` carry the mechanism, tell me and I will swap the emphasis. As it
   stands, this deck is the mechanism and the demo half is the making.
3. **Best demo beat, and it is not on a slide:** in Cowork on Claude for Mac you can
   **record yourself doing a task and have Claude write the skill from what it observed**
   (Pro, Max, Team). For a no-code audience that is the moment the lecture lands. It is
   plan-gated and Mac-only, which is why it stayed off the slides - please check it is
   available on your account before you plan the demo around it.
4. **The worked example is this repository's own skill.** `.claude/skills/principles-deck/`
   built every deck in the re-film. Opening that folder on camera, showing the description,
   then showing the seven reference documents it did *not* read, would make slides 3 and 6
   concrete in about ninety seconds.
5. **Overlap, now resolved.** `what-are-skills` owns the mechanism (it runs first and it
   is the concept lecture); this deck owns the authoring consequences. `creating-skill-chatgpt`
   owns the generic anatomy and `practicing-plugins` owns wrapping connectors into a skill;
   I stayed off both. **One thing to check when you review that deck:** the "what actually
   reaches the model" layers diagram now lives only in `what-are-skills`. If it is not
   there, the section loses the single clearest picture of how a skill loads.
6. **Slide 3's table describes our skill in round terms** ("a page", "a shelf of
   documents") on purpose, so it does not go stale when you edit the skill. If you want
   exact counts on camera, say them aloud rather than putting them on the slide.
7. **The handoff cards** end on "Trigger it by accident, without naming the skill". That
   only works if the description is good, which is slide 7's whole point - a good demo is
   to ask for the job in your own words and let it fire, then break the description and
   watch it not fire.
