# What is ChatGPT? — deck notes

Lecture `what-is-chatgpt` · Part 2 · ChatGPT Deep Dive · re-film · 05:21 · James
Source video `37093452`. Deck: `what-is-chatgpt.pptx` (13 slides), built by
`build_what_is_chatgpt.py`. Linter: clean, 0 errors, 0 warnings.

## The three principles

- **What it is** — an assistant built on a model that predicts the next token, with a
  product wrapped around it that now also searches, computes and acts.
- **How it works** — pre-train to predict, tune on what humans ranked as better, then run
  each turn as a loop in which tool results come back as more text in the same context.
- **Why it matters** — once you see it as prediction plus tools, its failures stop looking
  random: nearly every bad answer is a missing tool or a context you did not supply.

## What changed since filming

| The video says | What is true now |
|---|---|
| "ChatGPT is based on GPT-4, a transformer model" | Still a transformer; the generation has moved several times over. The deck never prints a version number. |
| "GPT-4o is the workhorse, GPT-4.5 is creative, o1/o3-mini reason" (4:10–4:42) | That whole model list is gone. Replaced by slide 9, which teaches the durable split — answers straight away vs thinks first — and a reasoning-effort dial. |
| Features listed as chat history, text generation, DALL·E images, browsing, Custom GPTs | Replaced by the six James asked for: Web Search, Deep Research, Data Analysis, Agent Mode, Plugins, Skills (slide 3). |
| "Plugins" as the 2023 plugin store | Plugins are now installable bundles that can contain skills, connectors, or both. Connectors are backed by MCP servers. Verified on `learn.chatgpt.com/docs/plugins.md`. |
| "Custom GPTs … custom prompts with a set of tools" | The docs now route reusable prompts to **Skills**; `learn.chatgpt.com/docs/custom-prompts.md` is marked *"Deprecated. Use skills for reusable prompts."* |
| RLHF explained as "PPO, policy reward model" | Kept as mechanism, said in plain words on slide 6. The jargon was cut. |
| "$200 a month for pro" | No prices anywhere in the deck, per house convention. Plan names below. |

## Say these aloud, do not put them on a slide

Verified 2026-09-08 from `developers.openai.com/api/docs/models.md` and
`learn.chatgpt.com/docs/models`:

- **Current flagship: GPT-6 Astra** — "our most capable model, built for the hardest
  end-to-end work". Below it, the **GPT-5.6 family**: Sol (flagship professional work),
  Terra (balanced, the everyday all-rounder), Luna (cost-sensitive, high volume).
- **In ChatGPT** you do not usually pick a raw model name. There is a **Power** setting
  running from *Faster* to *Smarter*, with an **Advanced** option underneath for a specific
  model and reasoning effort. Reasoning efforts are **Light / Medium / High / Extra High**.
  **Max** gives one task more thinking time; **Ultra** splits a task across subagents in
  parallel. Docs note that most tasks need neither.
- **Plans**, as the docs list them: Free, Go, Plus, Pro, Business, Edu, Enterprise.
- If you want a line for slide 9: *"the model I am using today is GPT-6 Astra, and by the
  time you watch this it will be something else — which is exactly the point of this
  slide."*

Cost, if you want to say it on camera: a token's price depends on which of three buckets
it lands in — input, cached input (heavily discounted), output (the most expensive by
several times). Today's rates are on `developers.openai.com/api/docs/pricing`. No figures
in the deck.

## Scope: this deck is the overview, not the lessons

Every one of the six capabilities has its own lecture later in the manifest
(`web-search`, `deep-research`, `data-analysis`, `agent-mode`, `what-are-skills`,
`what-is-mcp`, `practicing-plugins`). Slide 3 gives each of them exactly one line and the
caption says outright that each gets its own lecture. Nothing here teaches any of them in
depth, deliberately — that would burn another agent's deck.

Slide 8 uses the `s.layers` "what reaches the model" frame the skill documents, but with
this lecture's own bands (standing instructions, memory, fetched files and pages, tool
results, your message) and its own closing node ("It all arrives as one prompt"), so it
will not read as a copy of the memory or web-search decks.

## Sources and confidence

| Claim | Source | Confidence |
|---|---|---|
| Model catalogue, flagship, family names | `developers.openai.com/api/docs/models.md` | verified, fetched 2026-09-08 |
| Power setting, reasoning efforts, Max/Ultra | `learn.chatgpt.com/docs/llms-full.txt` | verified, fetched 2026-09-08 |
| "ChatGPT is an AI agent that you communicate with in natural language" | `learn.chatgpt.com/docs/use-chatgpt.md` | verified |
| Web search is a first-party tool; "treat all web results as untrusted input" | `learn.chatgpt.com/docs/web-search.md` | verified — this is the source for slide 8's "nothing on this stack is privileged" |
| Skill = packaged instructions + resources; plugin = bundle of skills and/or MCP-backed connectors | `learn.chatgpt.com/docs/skills-and-plugins.md`, `/docs/plugins.md` | verified |
| Agent-style work runs in a browser, with the user reviewing before it acts | `learn.chatgpt.com/docs/browser.md` | verified |
| Plan names | `learn.chatgpt.com/docs/pricing.md` | verified |
| The token probabilities in the slide 2 mock (31/24/12/7%) | invented | **illustrative only** — they are a schematic of a distribution, not a measurement. Do not quote them as real numbers on camera. |

`help.openai.com` and `openai.com` are behind a Cloudflare challenge from this environment,
as the brief says. Nothing in the deck depends on them.

## Review rounds

**Round 1 — hostile reviewer.** Ten findings, all fixed.
1. Slide 4's caption restated the accent node underneath it; rewritten to say something new
   (which surface you pick changes the tools and the price, not the intelligence).
2. Slide 4's "The API" and "Inside other tools" had near-identical sub-labels; differentiated.
3. Slide 2's candidate tokens were padded with spaces, which renders ragged in a
   proportional font; switched to a middle-dot separator.
4. Slide 5's "It weighs instructions, not runs them" was ungrammatical; the third pair became
   "It obeys your instructions" / "It weighs them against the context".
5. Slide 3's Agent Mode row ended on the filler "step by step"; replaced with the verified
   mechanism (it works in a browser).
6. **Layout** — slide 6's caption sat at the top of a column 1.4" shorter than the steps
   beside it; centred against them.
7. **Layout** — slide 8 had the same imbalance; caption centred.
8. **Layout** — slide 8 started content at y=1.52" while every other slide started at 1.58";
   aligned.
9. **Layout** — the gap between a visual and the caption under it ranged from 0.10" to 0.26"
   across the deck; standardised to 0.16".
10. **Layout** — slide 9 had the shortest table in the deck under the most empty canvas;
    table grown from 1.90" to 2.30".

**Round 2 — the student.** Four findings, all fixed.
1. "Six additions that changed what it is" did not stand alone when the titles are read end
   to end; retitled "Six things that turned it into a system".
2. "Token" carried slide 2 without ever being defined for anyone who skipped Part 1; added
   the clause "a token being roughly a word, sometimes part of one".
3. "Context" was used on slides 7, 9 and 10 and never defined; slide 7's caption now defines
   it at first use.
4. Slide 6's step 3 read "Reinforce against a model of that judgement" — unfollowable at
   1.5x; now "Let it practise against that ranking".
   Layout re-checked after the moves: content tops are 1.58" everywhere (1.56" for the two
   mock panels, the house offset), bottoms 4.23"–4.99".

Round 2 turned up more than two substantive items, so per the review loop there was a third.

**Round 3 — full copy read-through.** Four findings, all fixed.
1. Slide 6's caption ended on production meta ("the reason this lecture is being
   re-recorded"); cut.
2. Slide 8's accent node restated its own title almost word for word; the slide was retitled
   "Every setting you touch ends up here" so the title and the node each do work.
3. Slide 9's caption said "the picker" — a UI reference; now "the model names".
4. Slide 12's mock referred to "the export", which was never introduced; now "your data".

Rebuilt and re-linted after every round. Final: clean, 13 slides.

## For James

1. **Your note says "cover GPT 5 instead of GPT-4x" — GPT-5 is itself now two generations
   back.** As of today the flagship is **GPT-6 Astra**, with the **GPT-5.6** family (Sol /
   Terra / Luna) underneath it. That is exactly why the deck prints no version number at all
   and teaches the dials instead. Say the current name aloud on slide 9 and the deck survives
   the next release. Flagging it because your note assumed GPT-5 was current.
2. **"Agent Mode" is not what OpenAI's own docs call it any more.** The current docs describe
   **Browser** and **Computer Use** as the mechanisms, and **ChatGPT Work** as the mode where
   it "plans a task, gathers context, uses tools, and carries the work through to a result
   you can review". "Agent Mode" is still the clearest name for students and it matches the
   lecture title in the manifest, so the deck keeps it — but if you want the deck and the
   product vocabulary to match, tell me and I will rename that row.
3. **"Deep Research" and "Data Analysis" are not named in the current developer docs either.**
   They appear only in passing. The capabilities plainly still exist; the product labels are
   what I could not primary-verify. Same decision as above — kept because the course has
   lectures with those names. *[unverified label — worth a glance at your own account]*
4. **Custom GPTs are gone from the deck.** The original lecture spent time on them
   (5:04–5:20). OpenAI's docs now say "Deprecated. Use skills for reusable prompts", so Skills
   took that slot on slide 3. Confirm you are happy losing the Custom GPTs mention entirely.
5. **The Chat / Work / Codex split is deliberately absent.** It is a genuinely useful frame
   and it is current, but it is also new vocabulary that would need a slide of its own, and it
   overlaps `agent-mode`. Slide 4 gestures at it with "One model, many surfaces" instead. Say
   more on camera if you want to.
6. **DALL·E and image generation are not in this deck.** The original lecture mentioned them
   at 4:00. There are separate image lectures in the course, and cramming a seventh capability
   into slide 3 would have cost the slide its shape. Mention it in the demo half if you want
   it kept.


---

## Diagram sources (added 2026-09-08)

Three figures were brought across from the original lecture deck
(`What is ChatGPT_.pptx`) at James's request, and are credited on-slide as
"Source: see NOTES.md":

| Asset | Slide | Origin |
|---|---|---|
| `assets/next-word.png` | What would be the next word in this sentence? | the original bootcamp deck (2023) |
| `assets/predicting-token.png` | Predicting the next word (token) | the original bootcamp deck (2023) |
| `assets/training-chatgpt.png` | Training ChatGPT | OpenAI's InstructGPT / RLHF figure, via the original deck |

**For James:** the original slides carried a live "Source" hyperlink each. I could
not recover the target URLs from the exported PPTX, so the on-slide credit is
generic. If you still have the links, drop them here and I will make the credits
specific - the RLHF figure in particular is OpenAI's and worth attributing properly.

The training figure is a 16:9 image, so it is fitted by height; scaling it to the
full slide width would run it off the bottom.
