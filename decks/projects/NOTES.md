# Projects - build notes

Lecture: **Projects**, Part 2 / ChatGPT Deep Dive, re-film, 03:41, video `54676053`.
James's note: *"At 0:33 - adding a project now uses the + symbol. Cover organising chats
into projects, shared/project-level custom instructions, managing multiple related
conversations, project templates. No-code friendly."*

Deliverables: `decks/projects/projects.pptx` (11 slides), built by
`decks/projects/build_projects.py`. Linter clean, zero warnings.

## The three principles

- **What it is** - A project is a folder that holds a set of related chats together with
  the instructions and files all of those chats should share.
- **How it works** - Every chat opened inside the folder starts with the project's brief
  already in front of it and can reach the project's files and its sibling chats; your
  account-wide instructions and memory sit in the ring outside, and where the two
  disagree the more specific brief is the one that wins.
- **Why it matters** - Scoping means one assistant can hold several jobs at once without
  one job's rules leaking into another, and the setup you do once becomes the starting
  point every time you come back to that work.

## Why the navigation is not in the deck

The whole of James's note at 0:33 is a **navigation change**, so it belongs to the demo
half. The transcript says *"you can see you've got projects above your chat history...
click on New Project"*; creating a project now starts from the **+** symbol. That is a
sidebar position and a button, and both are exactly what `DECK_BRIEF.md` and the skill's
anti-drift rule keep off slides. No slide in this deck carries a menu path, a button, a
screen position, a plan name or a number that moves.

The current route, for James to say aloud on camera:

- **Sidebar > Projects > the + symbol**, then name the project. Alternatively, open the
  **Projects** page from the sidebar and use the **New** button in the top-right of the
  page header. `[unverified - James to check on his account]`
- The old path in the recording (a *New Project* entry sitting above chat history) no
  longer describes what a student sees.

## Current state (researched September 2026)

**What a project contains.** Three things, and they are the reason a project is not a
folder: a set of chats, a set of files that stay attached to the project, and a set of
project instructions that apply to every chat inside it.

**Project instructions vs global custom instructions.** Project instructions apply only
inside that project and take precedence over your account-wide custom instructions;
your global ones keep applying everywhere else. `[unverified - James to check on his
account]` The sources are consistent on precedence but vague on whether the global
instructions are *replaced* or merely *outranked where they conflict*, so slide 6 states
only the durable half: the more specific brief wins. Worth one spoken line if James can
confirm which it is.

**Project files.** Files live with the project and are available to every chat in it
without re-uploading. Per-project file limits are stated as 5 on Free, 25 on Go and Plus,
and 40 on Pro, Business, Edu and Enterprise, with a separate rate limit on uploads (and
only 10 files uploadable at once). `[unverified - James to check on his account]` The
deck says "a limited number of files, and how many depends on your plan" - the structure
is durable, the numbers are not.

Files are **retrieved**, not pre-loaded: content is searched when a question looks like it
needs it rather than synced into every conversation in advance. That is the basis for
slide 8's "a file sitting in the folder is not the same as a file being read", which is
also the most common student complaint (a project chat that appears to ignore a file it
has).

**Memory.** The lecture is right about the default: a project uses your ordinary memory,
and chats inside and outside can inform each other. What is new since filming is
**project-only memory**: chats in the project can reference each other but not
conversations outside it or your saved memories, and nothing from inside travels back out.
Reported constraints: it can only be chosen when the project is created, cannot be added
to an existing project, cannot be changed afterwards, and requires personal memory to be
switched on. `[unverified - James to check on his account]` The deck states the choice and
its trade-off, and deliberately does not state *when* the choice can be made, because
that is the part most likely to move.

**Shared projects.** Projects can now be shared, on business plans, with everyone in the
project drawing on the same chats, files and instructions, and with the shared project
holding its own private memory (personal memories are disabled in shared projects).
`[unverified - James to check on his account]` Not on a slide: the audience is
individuals, and it is a plan-gated feature. It is a good aside for the demo half.

**Availability.** Reports conflict on whether Projects is available on Free. One source
says Plus/Team/Enterprise only as of early 2026, another lists Free, Go, Plus, Pro and
Team as of May 2026. `[unverified - James to check on his account]` The deck names no
plan, so nothing depends on resolving this.

**Templates.** No first-party "create a project from a template" feature turned up in the
research. `[unverified - James to check on his account]` The deck therefore teaches the
principle James is actually after: a project you have briefed and stocked *is* the
template, which is the "Next time round: re-open the project you built" row on slide 9
and the "Set it up once" column on slide 10. See `## For James`.

**Sources.** `help.openai.com` returned a Cloudflare challenge through Playwright as well
as through plain fetching (403, "Just a moment..."), on both the Projects article and the
Projects collection, so **nothing above was read from a first-party page**. It all comes
from search-engine summaries quoting those pages plus secondary write-ups. `platform.
openai.com` is reachable but says nothing about the consumer Projects feature. Everything
plan-specific, label-specific or timing-specific is tagged unverified above.

**What still holds from the original lecture.** Most of it. The folder metaphor, the
project-scoped instructions and files, moving a chat you started outside into a project
afterwards, and the point that chats inside a project start to build on each other are all
still true and all still in the deck.

## Deck outline

| # | Slide | Carries |
|---|---|---|
| 1 | Projects | one-sentence definition |
| 2 | What is it? - a folder of chats with a brief attached | the container, shown |
| 3 | Nobody pasted the brief into this chat | the consequence |
| 4 | What it is not | three misconceptions corrected |
| 5 | How it works - every chat in here starts pre-briefed | the mechanism, plus moving a chat in |
| 6 | Two rings: your account, and this project | **the scoping slide** |
| 7 | Where the memory boundary sits | open vs sealed |
| 8 | Where it stops | limits, and retrieval |
| 9 | Why it matters - one assistant, several jobs | without/with, and the cost |
| 10 | What deserves a project of its own | when to, when not to |
| 11 | Let's see it in action | handoff to the demo |

**On slide 6.** The brief forbids reusing the "what actually reaches the model" framing,
which memory, web search and data analysis already use. This deck draws the same idea as
**two rings**: an outer ring holding what follows you into every chat you ever open
(custom instructions, memory, every other chat), and an inner ring holding what stops at
the folder (project instructions, project files, the chats you keep there). Nesting is a
truer picture for projects than a stack of bands anyway, because the point is a boundary
rather than an order of assembly.

**Boundaries with the neighbouring lectures.** Memory and Custom Instructions are separate
lectures and both decks are built. Neither is re-taught here: they appear only as two
labelled boxes in the outer ring, and the memory slide is about the *boundary*, not about
how memory works. The custom-instructions deck already carries the three-way table
(instructions / memory / projects), so this deck does not repeat it.

## Review rounds

**Round 1 - hostile reviewer.** Found and fixed:

1. Slide 6 never said what happens when the project's brief and your account-wide
   instructions disagree - the single most obvious question the diagram raises. The
   caption now answers it: the more specific brief wins.
2. Slide 6's outer ring held two boxes and bottomed out 0.84" above the ring's floor, so
   the composition was lopsided and the outer ring read as "settings" rather than "your
   whole account". Added *Every other chat*, and both columns now end on the same line.
3. Slide 7's caption said the open/sealed choice is one "you make when you set it up".
   That is currently true (project-only memory is a creation-time choice) and is exactly
   the kind of detail that moves. Rewritten as a choice "about the project as a whole".
4. Slide 5's return loop restated the flow it sat under. It now carries the transcript's
   best point instead - a chat you started outside can be moved in - and the flow boxes
   grew from 1.15" to 1.35" to take up dead canvas.
5. Slide 10's eight items each wrapped onto a second line and read ragged. All eight
   tightened to one line.
6. **Layout:** at four cards the handoff sub-labels get about 15 characters a line in a
   two-line box; *"and pick the conversation back up"* ran to three. All four shortened.
   Mock labels and the corner tag were over the label box's 28-character wrap
   (*"Instructions for this project"*, *"Inside the project"*, *"Carried into every chat
   in here"*), and two compare items on slides 4 and 7 were over the panel's 40-character
   line. All shortened; those were the seven linter warnings on the first build.

**Round 2 - the student.** Found and fixed:

1. "Brief" is doing a lot of work in this deck and was never defined - it appears in the
   subtitle and in slide 2's title before slide 2's copy explains it. The copy now names
   it: "those standing instructions are the project's brief".
2. Slide 6's title was *"Two rings of context"*, and "context" is jargon for this
   audience. Retitled *"Two rings: your account, and this project"*, which needs no
   glossary.
3. Slide 8's *"Every file, on every question"* is only parseable if you already know how
   retrieval works. Changed to "A full read of every file, every time".
4. Slide 2's mock labelled its top block *"Instructions"*, which reads as the assistant's
   own instructions. Now *"Project instructions"*.
5. **Layout:** the right-hand mock on slide 8 ran to x=9.66, the slide-chrome margin,
   rather than the 0.40" mock margin. Narrowed to end at 9.60.

**Round 3 - because round 2 found more than two substantive things.** One finding: the
title subtitle read *"How a set of related chats share..."*, which mismatches its own
subject. Rewritten as "How related chats share one brief, one shelf of files and one
place to live." Layout pass across all eleven slides found nothing else: every visual
starts at 1.52", nothing crosses 5.10", no caption is stranded, and the two compare
slides, the two mock slides and the two full-width diagram slides are each aligned with
their pair.

Read as titles only, the arc holds: what a project is, the consequence, what it is not,
the mechanism, the scope, the memory boundary, the limits, what it buys you, when to use
it, demo.

## For James

1. **The + symbol is a demo-half line.** Nothing in the deck contradicts it, and nothing
   in the deck needs changing when it moves again. Say the current route aloud over the
   live screen. The old *New Project* entry above chat history is gone, and students who
   took the previous version of this lecture will go looking for it, so it is worth one
   sentence naming the change.
2. **Templates.** Your note asks for project templates and I could not find a first-party
   template feature - only people using a well-set-up project *as* a template. If ChatGPT
   has since shipped an actual template picker, tell me and I will add a slide; otherwise
   the deck teaches the reusable-project version of the idea, which is what slide 9's
   "Next time round" row and slide 10's "Set it up once" column are for.
3. **Global vs project instructions.** The deck says the more specific brief wins where
   the two disagree. If you can confirm on your account whether your global custom
   instructions are still *present* inside a project or fully *replaced* by the project's,
   that is a genuinely useful 15 seconds on camera, and it is the one mechanism claim I
   could not verify first-hand.
4. **Which memory behaviour do you demo?** Project-only memory is reported to be a
   creation-time choice that cannot be changed later, so you will need a fresh project to
   show it. The deck states the trade-off without stating when the choice is offered, so
   whichever way your account behaves, the slides stay correct.
5. **Overlap with Memory.** The Memory deck's slide 8 carries one line saying memory can
   be held to a single project. That is the same fact as my slide 7. It is one line there
   and a whole slide here, which reads fine back to back, but if you would rather it were
   said only once, that deck's author offered to cut theirs.
6. **File limits.** Not on a slide, because the numbers move. If you want them said
   aloud: reportedly 5 files per project on Free, 25 on Go and Plus, 40 on Pro, Business,
   Edu and Enterprise. Check before you say a number.
7. **Shared projects** (business plans) are deliberately absent from the deck: the
   audience is individuals and the feature is plan-gated. It is a good "and if you are on
   a team plan..." aside during the demo.
