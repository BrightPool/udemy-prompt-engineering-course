# Agent Mode & Parallelising Threads — build notes

Lecture `agent-mode`, Part 2 (ChatGPT Deep Dive), re-film, 08:00, James.
Source video `51999139`, transcript at
`scripts/udemy-sync/transcripts/04_deep-dive-on-chatgpt/026_51999139_chatgpt-agent-mode.txt`.

Deliverables:
- `decks/agent-mode/agent-mode.pptx` — 13 slides
- `decks/agent-mode/build_agent_mode.py` — the build script
- Lint: `clean - 13 slides, nothing to fix`

## The three principles

- **What it is** — agent mode is a goal you hand over rather than a question you ask: the
  model is given a computer and keeps taking actions until it decides the goal is met.
- **How it works** — it runs a loop. It proposes the next action, a tool runs it, the
  result comes back as more context, and it decides again from your goal plus everything
  that has happened since.
- **Why it matters** — you are delegating actions, not answers, so the risks change: a
  wrong step compounds silently across a long run, and anything it reads can try to
  redirect it.

## Research — what is verified, and from where

`platform.openai.com` 301-redirects to `developers.openai.com`, which is reachable by
plain fetch. Everything below is primary-sourced from those developer docs. Nothing in
the deck depends on `help.openai.com` or `openai.com`, both of which are Cloudflare-blocked
from this environment.

| Claim on a slide | Source | Confidence |
|---|---|---|
| Agents "plan, call tools, collaborate across specialists, and keep enough state to complete multi-step work" | `/api/docs/guides/agents` | verified |
| The five-step tool loop: request with tools → tool call → execute → second request with the output → final response *or more tool calls* | `/api/docs/guides/function-calling` | verified |
| The computer-use cycle: send the task → model returns structured actions (click, type, scroll…) → return a screenshot → repeat | `/api/docs/guides/tools-computer-use` | verified |
| Sandbox and allow-listing: "Use an isolated browser or VM and an allow list of sites and actions" | same | verified |
| **"Text in a page, document, or tool result cannot grant permission"** — quoted almost verbatim on slide 9 | same | verified |
| "Delay confirmation until the exact risky action"; keep users in control of purchases, data transmission and destructive changes | same | verified |
| Approvals pause rather than block: "The model can still decide that an action is needed, but the run pauses until you approve or reject it" | `/api/docs/guides/agents/guardrails-approvals` | verified |
| Prompt injection defined: "untrusted text or data enters an AI system, and malicious contents in that text or data attempt to override instructions to the AI" | `/api/docs/guides/agent-builder-safety` | verified |
| Parallel runs help on "several independent questions about the same piece of content"; a meta-agent has to merge them | `/cookbook/examples/agents_sdk/parallel_agents` | verified |
| "Start with one agent whenever you can" — splitting too early adds prompts, traces and approval surfaces without making the workflow better | `/api/docs/guides/agents/orchestration` | verified |

**The compounding-failure table on slide 8 is arithmetic, not a vendor claim.** It is
0.95^n rounded: 5 steps ≈ 3 in 4, 10 ≈ 3 in 5, 20 ≈ 1 in 3. The slide states the 19-in-20
assumption in a caption directly under the table so it cannot be mistaken for a measured
benchmark. Adjust the assumption aloud if you prefer — the shape of the point survives any
per-step figure below 100%.

## What changed since filming

- **Agent mode is bundled directly into ChatGPT** (James's note). The original lecture
  opens by describing it as a thing that "came out" and is switched on from a menu, with a
  monthly credit balance shown on screen. None of that is in the deck.
- **The original teaches the click path**: the plus symbol, the triple dots, activities /
  stop / take over browser, the credit count ("34 that remain… reset on August the 23rd"),
  and a named reset date. All of it drifts; all of it is now demo-half material.
- **Scheduling** is mentioned in the last 10 seconds of the original. It has its own
  lecture (`scheduled-tasks`) in the manifest, so the deck deliberately says nothing
  about it.
- **The word "trajectory"** appears in the original. The deck does not use it — it teaches
  "the actions it took, in order", which is the same idea in words a student already has.
  Say "trajectory" aloud if you like the term; it is not on a slide.
- **Prompt injection is not in the original lecture at all.** It is the biggest gap, and
  it is now the opener of the "why it matters" phase (slide 9). The earlier `web-search`
  and `deep-research` decks deliberately left it to this one, because search only *reads*
  a poisoned page whereas an agent can act on it.

## Boundaries against the neighbouring decks

`web-search`, `deep-research` and `data-analysis` are already built. Slide 3 is an explicit
boundary slide so the four do not blur:

| | What it does | What you are left with |
|---|---|---|
| Web search | Reads a few pages | An answer with sources |
| Data analysis | Runs code over your file | A number and a chart |
| Deep research | Reads many pages, at length | A cited report |
| Agent mode | Takes actions, one after another | Something actually done |

Wordings were checked against those three build scripts so the rows agree with what each
of their decks already taught.

## Deck arc

1. Title
2. What is it? — a goal you hand over, not a question you ask *(mock)*
3. Retrieving, computing, acting *(boundary table)*
4. The computer it is given *(layers: browser / terminal / filesystem / your sessions)*
5. How it works — propose, run, read, decide again ***(hero: `s.flow(..., loop=…)`)***
6. What it sees before each decision *(layers → one accented node)*
7. Where you stay in the loop *(approval-pause mock)*
8. How a long run goes wrong *(compounding table)*
9. Why it matters — anything it reads can try to steer it *(prompt-injection mock)*
10. Asking a model, running an agent *(trade-off table with a failure-mode row)*
11. Parallelising threads *(fan-out diagram, you as the merge step)*
12. When to reach for an agent *(two columns)*
13. Let's see it in action

## Review rounds

**Round 1 — hostile reviewer.** Five findings, all fixed.

1. Slide 2's example was booking a courier, which drags payment into the first slide of
   the deck and clashes with the approval slide later. Replaced with reading a support
   queue and filing a summary into a tracker — still unmistakably an *action* with a side
   effect, no money involved.
2. Slide 3's last cell read "A changed world", which is florid rather than concrete.
   Now "Something actually done".
3. **Slide 5's hero loop was semantically wrong.** `s.flow(loop=…)` draws the return arrow
   from the *last* box to the *first*, and the last box was "Finish — goal met", so the
   diagram looped out of a terminal state. Last box is now "Done yet? — stop, or go again"
   and the loop label was rewritten to "Every step starts again from your goal and all
   that has happened since", which is both true and the exact point slide 6 develops.
4. Slide 9's injected instruction was split across two lines with the highlight pill on
   only the first half, so the emphasis read as a typo. Rebuilt as one short highlighted
   line, with "(hidden text, white on white)" above it to make the attack concrete.
   Also removed a made-up price from the mocked page.
5. Layout: slide 11's lanes started at y=1.62 while every other content slide starts at
   1.56. Moved to 1.56 and the caption up to 4.16 to match slides 3 and 10.

**Round 2 — the student.** Five findings, all fixed. Because that is more than two
substantive findings, a third round was run.

1. Slide 5's caption sat at y=4.42, 1.17" below the loop label, stranded in the middle of
   the slide. Moved to 3.62.
2. Slide 7 said "Actions with consequences pause for you" — a student cannot act on that.
   Now names them: "Sending, buying, deleting — the steps you cannot take back."
3. Slide 9 ended on OpenAI's rule but gave the student nothing to type. Added the
   actionable half: "Only you change the task", which is a line they can put in a prompt.
4. Slide 10's caption claimed "Reading a wrong answer costs you nothing", which is false —
   it costs a re-read. Rewritten as the actual trade: a wrong answer costs a re-read, a
   wrong action costs whatever it did.
5. The lecture title promises parallel threads but the handoff never asked James to demo
   one. Added a third card, "Start a second — in its own thread, alongside".

**Round 3.** One finding. Slide 12's right column had a 55-character first item that wrapped
to three lines against the left column's two, leaving the two panels visibly uneven.
Shortened to "Work you would not hand an unsupervised new starter". Layout pass otherwise
clean: every content slide starts at y=1.56, nothing crosses y=5.10, and the linter is
clean at 13 slides.

## For James

1. **The bundling claim is yours, not the deck's.** Your note says agent mode is now
   bundled directly into ChatGPT. I could not primary-verify anything about the consumer
   UI from here (`help.openai.com` and `openai.com` are both Cloudflare-blocked), so
   nothing about *how it is switched on* appears on a slide. Please say the current
   arrangement aloud in the demo half. `[unverified — James to check on his account]`
2. **Credits and limits are off the slides entirely.** The original lecture shows "34
   credits remaining, reset on August the 23rd". If there is still a run allowance, say
   the current shape of it on camera rather than putting a number in the deck.
3. **Scheduling was cut on purpose.** The original closes on it, but `scheduled-tasks` is
   its own lecture in the manifest. Consider ending this one with a one-line pointer
   forward instead of a demo.
4. **The browser-takeover / sign-in demo is worth keeping**, and slide 4 is built to set
   it up: the fourth band, "Your signed-in sessions", is the accented one, and the caption
   says every action it takes is then an action taken as you. That is the moment to do it
   live.
5. **The "just do the work, don't ask permission" trick from the original is on slide 7,
   with a warning attached.** It is genuinely useful and students will use it, so the deck
   teaches it rather than pretending it does not exist — but the copy says plainly that
   you have removed the only thing checking the work. Worth reinforcing on camera before
   you demo it.
6. **Prompt injection is new material for this lecture.** If you want to demo it, a page
   with white-on-white instructions is enough to make the point, and it lands far harder
   live than on a slide. Slide 9 is written so the demo is optional.
7. **Model names are not on any slide.** Current lineup for the spoken track: the flagship
   is GPT-6 Astra, with the GPT-5.6 family (Sol, Terra, Luna, Cyber) below it. Agent
   quality tracks the underlying model, so it is worth saying which one is driving the run.
