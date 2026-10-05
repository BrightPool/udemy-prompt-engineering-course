# Practicing using Plugins in ChatGPT to Automate Tasks — build notes

**Slug:** `practicing-plugins` · Part 2 · Skills & Plugins · **NEW lecture, never filmed** ·
owner James · 12 slides · linter clean · the capstone of the section.

Build:

```bash
uv run --with python-pptx python decks/practicing-plugins/build_practicing_plugins.py \
    decks/practicing-plugins/practicing-plugins.pptx
uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py \
    decks/practicing-plugins/practicing-plugins.pptx
```

---

## The three sentences

- **What it is** — Chaining connectors is one ordinary request that happens to touch two
  systems: it reads from the first, does the work in the middle, and writes into the
  second, and the record of that run is what becomes a skill.
- **How it works** — You connect each system once, do the job by hand until the result is
  right, save that run under a name with the varying parts left out, then call it back by
  name or hand it to a clock.
- **Why it matters** — You cannot automate a task you have not done: a skill is the record
  of a workflow that already worked, which is why it goes on working — and a chain that
  nobody is watching fails at its weakest link, politely.

## Research

Everything below is **primary-verified** against first-party docs on 2026-09-08, on a plain
fetch. No headed Playwright was needed: `learn.chatgpt.com` and `developers.openai.com`
serve markdown by appending `.md` to the page URL, and `platform.claude.com` is reachable
directly. Nothing on a slide rests on a search summary.

### The lecture's spine is a documented feature, not an invention

`learn.chatgpt.com/docs/extend/record-and-replay` — **Record & Replay**, verbatim:

> "Record & Replay lets you demonstrate a workflow on your Mac and turn it into a reusable
> skill. Use it when the workflow is repetitive, depends on your preferences, or is easier
> to show than to describe in a prompt."

> "Pick a workflow that you already know how to complete. Record & Replay works best when
> the steps are stable and the success criteria are clear."

> "After you stop recording, ChatGPT or Codex inspects the captured workflow and drafts a
> skill. The skill explains **when to use the workflow, what inputs it needs, what steps to
> follow, and how to verify the result**."

Those four things are **exactly the four rows of slide 4's table**, plus the row about
which connectors it needs (below). And the replay instruction is exactly slide 6:

> "Start a new ChatGPT or Codex chat and ask it to use the generated skill. **Give it the
> values that are different this time**, such as the file to upload, the issue to create,
> or the date range for the report."

This is the strongest possible support for James's arc — the vendor has shipped a feature
whose entire premise is *do the work once, then the demonstration becomes the skill*.
**Deliberately not named on a slide** (macOS-only, requires Computer Use, and it is a
product surface that will move) but it is a superb on-camera line.

### A skill can declare the connectors it needs

`learn.chatgpt.com/docs/build-skills`, the optional `agents/openai.yaml`:

```yaml
dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

> "Add `agents/openai.yaml` to configure UI metadata in the ChatGPT desktop app, to set
> invocation policy, and to **declare tool dependencies** for a more seamless experience
> with using the skill."

So the saved workflow records not only the steps but the plumbing it assumes. That licenses
slide 4's row *"Which systems it touched → The connectors it needs"*, which is the row that
makes the skill a record of a *chained* run rather than a writing style.

### Scheduled runs and skills are documented as a pair

`learn.chatgpt.com/docs/automations` ("Scheduled tasks"):

- > "You can combine scheduled tasks with skills for more complex work."
- > "Scheduled tasks on the web can use uploaded files, connected tools, skills, and
  > plugins available to that chat. … **Put durable instructions in the task prompt or an
  > attached skill**, and keep required source material in an accessible project, upload,
  > or connected service."
- > "To keep scheduled tasks maintainable and shareable across teams, use skills to define
  > the action and provide tools and context. **Select or invoke a specific skill in the
  > task prompt when the workflow shouldn't rely on automatic tool selection.**"
- > "**Before you schedule a task, test the prompt manually in a regular chat first.** This
  > helps you confirm: The prompt is clear and scoped correctly. The selected or default
  > model, reasoning effort, and tools behave as expected. The resulting output is
  > reviewable." And: "review the first few outputs and adjust the prompt or cadence."
- > "Connect and authorize the app before creating the task."
- > "Scheduled tasks run unattended and use your default sandbox settings." Under a
  read-only or workspace-write sandbox, "tool calls fail if they require … accessing
  network, or working with apps on your computer."

Three slides come straight out of that block. **Slide 9's right-hand panel** ("Call the
skill by name") is the vendor's own advice about not relying on automatic selection when
nobody is watching. **Slide 8** is "test the prompt manually first", generalised into the
durable principle. **Slide 10** is the honest consequence of "runs unattended" plus "tool
calls fail": a run that cannot ask anyone anything reports success on an empty fetch.

One deliberate care point: I could **not** find a first-party statement that a connector's
authorisation *expires* on a schedule, so slide 10 does not claim it. The mock breaks on a
renamed folder instead — a failure I can derive from documented behaviour rather than
assert. If you want the expired-permission version on camera, say it as an example rather
than as a documented behaviour.

### The vendor-neutral half

`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` lists as a headline
benefit: *"**Compose capabilities:** Combine Skills for complex, multistep tasks"*, and
connectors on the Claude side are remote MCP servers (`remote-mcp-servers`,
`mcp-connector`). Anthropic's own Academy tutorial ("Teach Claude your way of working
using skills") makes James's exact argument in its opening paragraph:

> "Think about the last time you created something with Claude that turned out really well.
> … Instead of having to repeat this process the next time you complete a similar task,
> Skills let you package what you've learned."

> "**Creating a skill is an act of description.** By the time you've built one, you can
> name the format a task needs, the tone that fits your voice, and an example of what a
> good result looks like, and hand all three to Claude in one move."

Both labs, independently, describe a skill as the residue of work you already did well.
That is why slide 8's principle is framed as outliving the products.

### Honest limit worth knowing (not on a slide)

On the **Claude API**, skills run "in a sandboxed container with **no network access**",
so the chained-connector story there is a claude.ai / Cowork / Claude Code story, not an
API one. On claude.ai network access is "full, partial, or none" depending on settings.
Kept off the slides because it is surface-specific and will move.

## The arc

| # | Slide | Carries |
|---|---|---|
| 1 | From Connectors to a Saved Skill | title + one-sentence definition of the arc |
| 2 | *What is it?* — one job that crosses two systems | mock: one request, two connectors, one result; the "connectors — what this course calls plugins" clause |
| 3 | There is nothing to wire up | the misconception: not a builder canvas, an ordering |
| 4 | What the saved skill records | light table: what the run showed → what the skill writes down |
| 5 | *How it works* — do it once, then write down what you did | **the hero**: connect → do the job → save the run → run it again, with a return loop |
| 6 | What is fixed, and what you supply | two message rows: the constant half vs the values you give each time |
| 7 | What the email is actually written from | layers: what the connector returned, the skill, your inputs → "Nothing else reaches the email" |
| 8 | *Why it matters* — you cannot automate what you have not done | table: written from a description vs from a run that worked |
| 9 | A run with nobody in the room | the join to `scheduled-tasks`: you fill the gaps, or the skill must |
| 10 | How a saved chain fails | mock: a 07:00 run that reports success on an empty fetch |
| 11 | When to save a run, and when not to | two columns |
| 12 | Let's see it in action | handoff |

### What is deliberately *not* re-taught

Per the brief, each of these gets a clause and no more: what a skill is (`what-are-skills`,
glossed in one half-sentence on slide 4 for anyone joining here), the connector protocol
(`what-is-mcp`), how you build one (`creating-skill-*`), and scheduling (`scheduled-tasks`,
referenced on slide 9 without naming a position in the running order, so a reorder does not
break the line). Every slide is about the **composition**.

## Review rounds

**Round 1 — the hostile reviewer.** Ten findings, all fixed.

1. The title subtitle only promised the scheduled end ("runs without you"), but the arc
   also ends in a chat where you *are* present. Now "call back by name, or hand to a clock".
2. Slide 2 said chaining is "nothing more than one request" — undersells something the
   deck then spends three slides calling fragile. "Nothing more than" cut.
3. **Terminology drift**: the deck used "connection" and "connector" interchangeably across
   four slides. House rule is to call the feature by its name, so every instance is now
   **connector**.
4. Slide 6 had a pink arrow between the two message rows, which asserted a sequence that
   does not exist — the fixed half and the supplied half combine, they do not flow. Cut.
5. Slide 7's closing node read "All the email is written from" — ungrammatical. Rewritten
   (and later rewritten again in round 3, see below).
6. Slide 9's left panel was three things *you do* plus one abstraction ("Ambiguity costs
   you seconds"). Made parallel: "You catch it in seconds".
7. Slide 10's copy carried three points at once. Cut to two: it fails politely, and the fix
   is to tell the skill what an empty result means.
8. Layout: slide 7's caption sat at 2.36" against a diagram spanning 1.52"–4.69" — raised
   to 2.66" so its optical centre matches. Slide 4's caption had a 0.14" gap under its
   table where every other slide uses ~0.22"; moved to 3.80".
9. Layout: slide 2's mock overflowed the footer band by 0.29" and slide 10's `.fit()` left
   1.39" of dead canvas. Trimmed the reply on slide 2; gave slide 10's panel the saved
   instruction as a first block, which also makes the failure legible.
10. Layout: two `Row.label` strings ran past their fixed 1.9" box. Shortened.

**Round 2 — the student.** Six findings, four of them comprehension-level.

1. Slide 3's title was "Not a builder, an ordering" — "a builder" is Zapier jargon a
   beginner has never met. Now **"There is nothing to wire up"**, which the two panels then
   explain.
2. Slide 7's title was "What the writing step is based on", but "the writing step" was
   never named as a step anywhere on a slide (only inside a 12pt caption). Now **"What the
   email is actually written from"**, which is concrete and matches the mock.
3. The deck used the word "skill" from slide 4 without ever glossing it. Added one clause —
   "a skill is a named set of instructions the assistant keeps" — so this lecture stands
   alone without re-teaching `what-are-skills`.
4. Slide 11's title "When to wrap a run up" reads idiomatically as "when to finish". Now
   "When to save a run, and when not to". Its column item "quicker than the wrapper" coined
   a shorthand — banned by the house rules — now "quicker than saving it".
5. Slide 3's caption restated slide 2's "fetch, judge, write" almost verbatim. Trimmed.
6. Read the titles alone, top to bottom: the arc now tells the whole story without the
   bodies.

**Round 3** — run because round 2 exceeded the two-issue threshold. Five findings.

1. **Layout, the one that mattered.** On the hero flow, three of the four nodes had
   sub-labels that wrapped to two lines and the fourth ("as a named skill") did not, so
   `node()`'s vertical centring put that box's type 0.05" out of line with its neighbours —
   visible as a wobble across the most important diagram in the deck. Lengthened to "under
   a name you choose" so all four wrap identically; all four labels now sit at 1.71" and
   all four subs at 2.09".
2. Slide 12's fourth handoff card carried two actions ("call it by name, then set a time")
   while the other three carried one. The clock moved into the lead line, so the card list
   stays parallel and the lead still names all four beats.
3. Slide 6's second message row was 0.86" tall around 0.59" of content and sat 0.50" below
   the first (a gap left behind by the arrow cut in round 1). Row tightened to 0.72" and
   raised to 3.20"; caption follows at 4.16".
4. Slide 11: "The format matters more than the flair" was the wrong axis — the point is a
   fixed shape, not restraint. Now "The result has a shape it must fit".
5. Slide 7's closing node became "Nothing else reaches the email", which states the limit
   rather than restating the title.

Final layout pass: every content slide starts its visual at y = 1.52" (slide 11's
two-column layout starts at 1.58", which is the template's own body placeholder and matches
the other decks); nothing crosses y = 5.10"; the only dark table is the one inside a mock;
one highlight pill per mock; no screenshots, no menu paths, no version numbers, no prices;
the deck ends on `handoff`.

## For James

### The demo arc I would film

Four beats, one sitting, one worked example — **pull this week's client notes from the
shared drive, summarise each to a one-page house format, email the set to the account
team**. Two connectors, no code, and a result anyone in the audience recognises.

1. **Connect both systems, on camera.** Show the authorisation happening once, and say out
   loud that this is the only step that is about plumbing. Then never return to it.
2. **Do the job by hand.** Get it wrong once on purpose — the summary comes back too long,
   or in the wrong order — and fix it in the chat. This is the beat the whole deck is
   built to earn: the audience needs to see that the good run took a correction.
3. **Save that run as a skill.** Say what you are leaving out (the week, the client, the
   recipient) and what you are pinning down (the folder, the format, the "never send
   without a draft I have read"). Slide 6 is the map for this bit.
4. **New conversation. Call it by name.** Supply only the values that changed. Then, in the
   last thirty seconds, attach it to a time — and say the line from slide 9: *at 07:00
   there is nobody there to say "no, the other one".*

If Record & Replay is available on your machine, **beat 3 becomes a much better demo**: you
demonstrate the workflow and the product drafts the skill from the recording. That is the
lecture's thesis shipped as a feature, and it will land harder than typing a skill by hand.
It is macOS-only and needs Computer Use enabled, which is why it is nowhere on a slide —
check it on your account before you plan the take.

### Things I had to decide for you

1. **The deck's cover title.** The lecture is *"Practicing using Plugins in ChatGPT to
   Automate Tasks"*, which is a mouthful on a title card and puts "Plugins" in a position
   the deck then has to immediately qualify. The cover reads **"From Connectors to a Saved
   Skill"** — it names the arc, which is what the lecture actually is. **The manifest title
   is untouched.** Say the word and I will put the original back.

2. **"Plugin" is a real word again, and the brief is out of date.** The shared terminology
   block says *"Neither vendor uses 'plugin' any more."* That is **no longer true**, and the
   change is material to your section:

   - OpenAI's own documentation page is literally titled **"Skills & Plugins"**
     (`learn.chatgpt.com/docs/skills-and-plugins`), and defines: *"A **skill** packages
     instructions and supporting resources for a specific task or workflow. A **plugin** is
     an installable bundle that can include skills, connectors, or both. Connectors are
     backed by Model Context Protocol (MCP) servers."*
   - Anthropic's help centre now carries *"Use plugins in Claude"* and *"Browse skills,
     connectors, and plugins in one directory"*, with plugins described as bundling skills,
     connectors and sub-agents into one package.

   So the three words now have clean, agreed meanings across both vendors:
   **connector** = the link to an outside system · **skill** = the instructions ·
   **plugin** = the installable bundle of the two. Your section title *Skills & Plugins* is
   not a legacy name at all — it is the industry's current one, and it names precisely the
   two halves this lecture joins.

   I have kept the house convention as written (one acknowledgement on slide 2, "connector"
   throughout) because five decks in this section were built against it and consistency
   beats correctness-by-one-deck. **But this is worth a course-wide decision**, and if you
   take it, this deck gains a genuinely strong closing beat: the thing you built by hand in
   this lecture is what a plugin ships to somebody else. Tell me and I will re-cut slide 2
   and add it.

3. **The failure I put on slide 10.** The brief suggested "a connector's permission has
   lapsed at 07:00". I could not primary-verify that connectors expire, so the mock fails on
   a **renamed folder** instead — same lesson, derivable from documented behaviour ("runs
   unattended", "tool calls fail if they require accessing network"). The lapsed-permission
   version is a fine thing to *say*; I would not put it on a slide as fact.

4. **`what-is-mcp` running order.** The `what-are-skills` notes suggest moving `what-is-mcp`
   to position 2. This deck works under either order — it glosses "connector" itself on
   slide 2 and names no lecture positions anywhere. No action needed from me either way.

5. **Overlap check.** No collision with `scheduled-tasks`: that deck teaches the clock and
   what a run has to go on; slide 9 here teaches only the *join* (a workflow is ready for a
   clock when it no longer needs you in the room) and deliberately does not redraw the
   "what a run has to go on" layers diagram. No collision with `what-are-skills`: this deck
   never explains matching-by-description, progressive disclosure, or skill anatomy.

### Available for the demo half, deliberately absent from the slides

Record & Replay and its macOS/Computer Use requirement; `@` to pick a skill in ChatGPT and
`$` in Codex; `agents/openai.yaml` and the `dependencies.tools` block; the universal plugin
directory shared by ChatGPT and Codex; RRULE-based custom schedules; event triggers from
Gmail, Slack and GitHub; sandbox modes for unattended runs; and the fact that skills on the
Claude API run with no network access at all.
