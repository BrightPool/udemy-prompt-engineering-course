# Creating a Skill in ChatGPT — build notes

New lecture (never filmed, no transcript). Part 2 · Skills & Plugins. Presentation-led,
so the deck carries most of the teaching: **13 slides**.

Deliverables:
- `decks/creating-skill-chatgpt/creating-skill-chatgpt.pptx`
- `decks/creating-skill-chatgpt/build_creating_skill_chatgpt.py`

Lint: **clean — 13 slides, nothing to fix.**

## The three principles

1. **What is it?** Creating a skill is dictating a routine you already repeat, once, in a
   form the assistant can re-read later.
2. **How it works?** You run the job in an ordinary conversation, save that as a skill,
   then check the four things every vendor asks for — a name, a description that decides
   when it fires, the instructions, and the files it needs — and a connector supplies the
   real account the instructions act on.
3. **Why it matters?** The routine stops being re-explained: written once, it holds its
   format, it can be handed to someone else, and its failure mode flips from inconsistent
   output to firing when you did not want it.

## Research — what is true now (2026-09-08)

All of the following is **primary-verified**, read directly from first-party pages
(OpenAI help centre via headed Playwright per the brief; Anthropic docs by fetch).
None of it is on a slide — it is here for the spoken track and the demo half.

### OpenAI / ChatGPT

- **Skills in ChatGPT** (`help.openai.com/en/articles/20001066-skills-in-chatgpt`):
  "Skills are reusable, shareable workflows that help ChatGPT complete specific tasks more
  consistently. A skill can include instructions, examples, and code. After a skill is
  created and installed, ChatGPT can automatically use one or more skills when they are
  helpful."
- **Where they live today:** sidebar > Plugins > Plugin Directory > **Skills** tab, with
  Installed / Created by me / Shared with me / Shared by {workspace}. Eligible accounts
  ship with one skill by default, **`skill-creator`** — asking ChatGPT to create a skill
  uses it. Four routes in: **Create with chat**, **Create with editor**, **Upload from
  your computer**, or install one shared with you. (Deliberately off the slides — this is
  exactly the sort of thing that moves.)
- **Availability:** "Skills are available to eligible ChatGPT **Business, Enterprise,
  Healthcare, and Edu** users, subject to workspace settings and product availability."
  See `## For James` — this matters for what students can follow along on.
- **Plugin = skills + apps** (`help.openai.com/en/articles/20001256`): "A plugin can
  include: **Skills** that provide instructions and workflow guidance. **Connected apps**
  that link external accounts, information, and actions. **App templates**…". Since
  **9 July 2026** the app directory is the **Plugin Directory**; apps remain the
  integrations, plugins are the packaging.
- **Apps / connectors** (`help.openai.com/en/articles/11487775`): "Apps connect ChatGPT to
  services you already use, such as Google Drive or Slack." Capabilities: search, deep
  research, admin-configured sync, and **write actions** (create/update in the connected
  service).
- **Permissions ladder** — Always ask / Allow read actions / Allow low-risk actions /
  Allow all actions. The default is **Important actions**: reading happens automatically,
  and ChatGPT asks before anything with "a meaningful effect outside ChatGPT". Their own
  examples of an important action: sending or editing an email or invitation, deleting
  content, making a purchase, uploading or moving a file, changing sharing permissions.
  On an approval card the options are **Deny / Allow (once) / Allow low-risk actions /
  Always allow**.
- The honest boundary, in their words: "App permissions **do not grant an app new
  access**… Changing an app permission only changes when ChatGPT asks before using the
  access the app already has." And: "A plugin cannot use an app to access content outside
  the permissions granted to the relevant individual provider account."
- **Uploaded skills are scanned** before use; some are marked *Needs Review*, some
  *Blocked*. Their guidance: review a skill you did not write, especially one from outside
  your organisation — the scan "should not replace your own review".
- Also noted, not used: "Suspicious or hidden instructions in app content can also cause
  ChatGPT to ask for approval or block the request" (prompt injection, live in the
  product). And the **shared facts** in the brief: OpenAI's API docs mark reusable prompt
  objects deprecated, with skills the durable replacement.

### Anthropic / Claude — the same shape, different clicks

- `platform.claude.com` Agent Skills: a skill is a folder with a `SKILL.md`; required
  fields are exactly **`name`** and **`description`**, then instructions, then bundled
  resources and scripts.
- The description does the same job it does in ChatGPT: "The `description` is what Claude
  matches your request against when determining whether to trigger the Skill, so it must
  say both **what the Skill does and when to use it**." claude.ai caps it at ~200
  characters; the API at 1024.
- **Progressive disclosure**: name + description always loaded (~100 tokens), instructions
  loaded only when it fires, bundled files only when read. Custom skills **do not sync**
  across claude.ai / API / Claude Code.
- **Connectors** (`support.claude.com`, custom connectors / remote MCP): OAuth, "Claude
  can only access resources that you've given the server permission to access", plus
  explicit warnings to connect only to trusted servers, limit the scopes requested, and
  watch for hidden instructions in a server's content.

**Conclusion the deck teaches:** the anatomy is identical across both vendors — name,
description, instructions, resources — and so is the split between the instructions and
the authorised reach. Only the click path differs. Nothing in this deck breaks when either
vendor redesigns.

Confidence: no `[unverified]` claims. Everything above came from a first-party page read
this session.

## Slides

| # | Title |
|---|---|
| 1 | Creating a Skill in ChatGPT |
| 2 | What is it? – a routine you already repeat, written down once |
| 3 | The two halves of one workflow |
| 4 | What you decide when you write one |
| 5 | How it works – do the job once, then save what worked |
| 6 | Why one description fires and another does not |
| 7 | The test is a sentence you did not write |
| 8 | A Monday morning, end to end |
| 9 | What connecting an account actually grants |
| 10 | Why it matters – the routine stops being re-explained |
| 11 | One person writes it, the team runs it |
| 12 | When a routine is worth writing down |
| 13 | Let's see it in action |

The worked example throughout is one everyday, no-code routine: **the weekly client call
notes come out of Drive, get written up in the house format, and get filed back.**

## Review rounds

**Round 1 — the hostile reviewer.** Five findings, all fixed:
1. Slide 4's table had an unlabelled first column — headed it *The part*.
2. Slide 3's accent node ("Together, one sentence does the whole routine") was the third
   use of "one sentence" in four slides — rewritten to *Neither half is much use on its
   own*, which also says something the other slides do not.
3. Slide 8 read as a generic pipeline and looked like slide 5's flow — retitled *A Monday
   morning, end to end* so it names the everyday routine rather than a mechanism.
4. Layout: content tops were ragged (1.52 / 1.55 / 1.56 / 1.58) — all normalised to 1.56,
   and every caption set to a ~0.20" gap below the visual above it.
5. Layout: slide 11's caption was stranded at the top of the right column against a tall
   four-step stack — moved to 2.40 so it optically centres against the steps.

**Round 2 — the student.** Three substantive findings, all fixed (which triggered a third
round per the review loop):
1. Slide 4 implied you fill in four fields in order, which contradicts slide 5's "just
   talk to it" — caption rewritten: whether you type them or the assistant drafts them,
   these four are what you sign off.
2. Slide 7 never answered the obvious question, *how did it know to use the skill?* Copy
   now says plainly that nobody named it — the sentence was matched against the
   description — and that you *can* name it outright but will not remember to.
3. "Grant the narrowest scope" on slide 9 is jargon for a no-code audience — replaced with
   *connect one folder, not everything you own*. Same fix applied to slide 11's caption
   ("a script a colleague sent you" → "any file from outside the company").
4. Also: slide 4's Resources row now asks *What files must it carry?* rather than "what
   must it have to hand".

**Round 3 — layout and a fresh hostile pass.** Two findings, both fixed:
1. **The linter cannot see this one:** `check_deck.py` skips placeholders for its
   text-overflow check, so `s.beside()` copy is never measured. Slides 7 and 9 had grown
   past their boxes in round 2 (3.12" and 3.44" of copy in 3.04" and 2.96" boxes). Both
   trimmed; I re-ran the linter's own estimator over the placeholders by hand and every
   box now fits. Worth knowing for the other 22 decks.
2. Slide 3's caption ran to 5.00", a tenth of an inch off the footer band — the accent
   node and caption moved up 0.06–0.08" each, ending at 4.86".

## For James

**Running order for the Skills & Plugins section.** My proposal:

1. **What are Skills?** — the concept.
2. **What is MCP? (Plugins for OpenAI)** — the connection, before anything relies on one.
3. **Creating a skill in ChatGPT** (this one) — the making of one, with a connector in the
   worked example.
4. **Creating a Skill in Claude Co-Work** — the same job, second vendor, so the anatomy
   lands as universal rather than as an OpenAI thing.
5. **Practicing using Plugins in ChatGPT to Automate Tasks** — two connectors chained,
   wrapped as a skill, then scheduled.
6. **A/B Testing — How to Systematically Improve Your Skills.**
7. **Prompt Testing in GSheets.**

MCP before creating, because my slide 3 needs the student to accept "a connector is
authorised reach" — I define it in a clause, but it is smoother if it has already been
taught properly. If you would rather keep the two *creating* lectures adjacent, move MCP
to position 5; nothing in my deck breaks.

**Things you should check on your own account before filming:**

- **Skills may not be visible on a personal plan.** The help centre says skills are for
  eligible **Business, Enterprise, Healthcare and Edu** users. If you film the demo on a
  Business workspace but your students are on Plus, say so on camera — otherwise the
  section teaches something half the audience cannot open. This is the biggest open
  question in the lecture and I could not resolve it for you.
- **Vocabulary has moved.** Since July 2026 the App Directory is the **Plugin Directory**,
  and a **plugin** is the wrapper around skills + connected apps. I name "plugin" exactly
  once (slide 3 caption) and otherwise say **connector** for the reach, so I do not
  trample the MCP lecture. Worth one sentence aloud so students recognise the word when
  they see it on screen.
- **`skill-creator`** ships enabled — the fastest live demo is to just ask ChatGPT in
  chat to save the routine as a skill, which is what slide 5 sets up.

**Decisions I made for you, flag if you disagree:**

- **Angle.** No brief existed for the *how you make one* half, so I built the lecture
  around the **authoring loop** — run the job, save what worked, read the four parts, test
  in a fresh conversation — rather than a field-by-field tour of an editor. The editor
  will be redesigned; the loop will not.
- **Worked example.** Client call notes out of Drive → status update in the house format →
  filed back. Everyday office work, per your note about Drive, and no engineering.
- **Boundaries with the neighbours.** *What are Skills?* owns the anatomy, so I teach the
  four **decisions** instead and give the description slide a craft angle (why one fires
  and another does not) rather than restating that it matters. *What is MCP?* owns the
  protocol, so I never open one up. *Other Providers* owns model agnosticism, so it gets a
  clause on slide 3 and nothing more.
- **The approval card on slide 9 is schematic.** The real one currently offers Deny /
  Allow once / Allow low-risk actions / Always allow, and the default posture is that
  reads run automatically while consequential actions stop and ask. I kept the buttons off
  the slide; say the four aloud if you want the detail.
- **The failure-mode row** on slide 10 says a skill's failure mode is "fires when you did
  not want it". That is the honest boundary I chose to lead with, alongside the caption
  that a wrong skill is wrong every run and quietly. If you would rather lead with
  "silently does not fire", that is a one-line change in the build script.
