# Memory - build notes

Lecture: **Memory**, Part 2 / ChatGPT Deep Dive, re-film, 02:28, video `48151545`.
James's note: *"Update the way a user navigates to memory."*

Deliverables: `decks/memory/memory.pptx` (11 slides), built by
`decks/memory/build_memory.py`. Linter clean, zero warnings.

## The three principles

- **What it is** - Memory is a small profile of you that the assistant writes and keeps
  in plain sentences, and reads back before it answers.
- **How it works** - Facts get in two ways (you say them, or it infers them from your
  ordinary chats), are stored as text, revised over time, and the relevant lines are
  placed in front of your message in every later conversation.
- **Why it matters** - It removes repeated set-up and shapes answers to your situation,
  but it inverts the failure mode: an assistant with memory is not forgetful, it is
  occasionally wrong with conviction, so the store is something you maintain.

## Why the navigation is not in the deck

James's note is about the **demo half**. The deck deliberately carries no menu path, no
toggle name and no screen layout, per `DECK_BRIEF.md` and the skill's anti-drift rule -
memory's settings screen has already been redesigned once since filming and will move
again. What the deck teaches instead is the durable half: memory is a small written
store, it is inspectable and editable, it is opt-in, and its reach is scopeable.

The current navigation is below, for James to say aloud on camera.

## Current state (researched September 2026)

**How a user reaches memory today**

- **Settings > Personalization > Memory**, the same on web and in the apps. This is the
  substantive change since filming: the lecture's route was *Settings > Personalization >
  Manage*, landing on a scrollable list of individual saved memories.
- From around **12 June 2026** that screen was replaced for many accounts by a single
  memory control plus a **memory summary**: a written, category-organised account of what
  ChatGPT thinks it knows about you, rather than a list of stored items.
- **Editing** on the new screen is done by writing, not by deleting rows: type the change
  into the text box at the bottom of the memory summary, or highlight a passage in the
  summary to correct it or tell it not to mention that again.
- **Refresh** the summary: Settings > Personalization > Memory Summary > Manage, then
  *Refresh* from the three-dot menu.
- **Delete everything and switch off**: *Delete and turn off memory*, from the three-dot
  menu on the memory summary.
- Rollout is staged **by plan and by region**, so some accounts still show the older
  screen with the *Reference saved memories* and *Reference chat history* toggles and a
  manageable list of individual memories.

**What is stored, and what is not**

- Two routes in: memories you explicitly ask for ("Remember that..."), and context the
  system synthesises in the background from your chat history. The background synthesis
  (OpenAI calls it *dreaming*) now also **revises** memories as time passes - a planned
  trip becomes a past trip once the date has gone. The original lecture does not cover
  this at all, and it is the single most interesting change; slide 7, "Facts have a
  tense", is built on it.
- ChatGPT does not store usernames or passwords, and is trained not to proactively store
  sensitive detail such as health information unless you explicitly ask it to.
- **Temporary Chat** neither reads existing memories nor creates new ones.
- **Project-only memory** scopes memory to a single project: chats in the project can
  reference each other but not conversations outside it, and vice versa.
- Free accounts get a lightweight, short-term continuity; Plus and Pro get the longer-term
  understanding.
- A user can see which sources personalised a given response - custom instructions, past
  chats, files, memories - from the control below that response.

**What still holds from the original lecture**

The core teaching survives intact: you can add, update and delete memories by just talking
to ChatGPT ("remember that my name is James", "update my age based on 13 September 1992"),
memory is injected into later conversations, and a fresh chat can answer from it. That is
the transcript's best material and it is preserved - it drives slides 3, 5 and 7.

**Sources.** OpenAI Help Centre *Memory FAQ*
(https://help.openai.com/en/articles/8590148-memory-faq), *Memory FAQ (Business Version)*,
*Temporary Chat FAQ*, and the OpenAI posts *Memory and new controls for ChatGPT* and
*Dreaming: Better memory for a more helpful ChatGPT*
(https://openai.com/index/chatgpt-memory-dreaming/). See `## For James` on how these were
read.

## Deck outline

| # | Slide | Carries |
|---|---|---|
| 1 | Memory | one-sentence definition |
| 2 | What is it? - a short profile of you, kept in writing | the store, shown |
| 3 | Nobody typed this into the prompt | the consequence, a week later |
| 4 | What it is not | three misconceptions corrected |
| 5 | How it works - two doors into the same store | explicit vs inferred |
| 6 | What actually reaches the model | assembled context, and selection |
| 7 | Facts have a tense | memories age and get revised |
| 8 | Where it stops | opt-in, scopeable, bounded |
| 9 | Why it matters - forgetting is not the risk | without/with table, the cost |
| 10 | What belongs in the store | keep in / keep out |
| 11 | Let's see it in action | handoff to the demo |

Deliberately **not** copied from the skill's worked example, which is also about memory.
Shared ground is unavoidable (the layers diagram and the without/with table are the
canonical forms for those two jobs), but the arc, the copy and slides 5, 7 and 8 are
specific to this lecture and to the 2026 behaviour.

## Review rounds

**Round 1 - hostile reviewer.** Found and fixed:

1. Slide 2's store panel had a flat list of four facts and left 1.77" of dead canvas.
   Regrouped it into *Preferences / Your work / Standing constraints*, which both fills
   the panel and makes a truer point: the store is organised, not a heap.
2. Slide 3's corner tag *"A new conversation"* overflowed its box. Shortened to
   *"A week later"*, which also carries more meaning.
3. Slide 5's flow arrows were drawn at h=0.10 and tripped the linter's `double-rule`
   check as accent rules competing with the dashed divider. Set to the default 0.12.
4. Slide 7 left 1.35" of dead canvas. Added the return loop - *"or you revise a line
   yourself, by saying so in any chat"* - which fills the slide and restores the
   transcript's best point (you can update memories by prompting).
5. Slide 10's *"Anything with an expiry date on it"* restated the whole of slide 7.
   Replaced with *"A conclusion you have not checked yet"*, a distinct risk.
6. The deck showed only benefits and staleness, never named the cost. Slide 9's caption
   now ends "That is what memory costs you - a store you have to maintain."
7. Slide 8's panel was short against its copy column. Added a third line.
8. **Layout:** content start heights were ragged - 1.52", 1.56", 1.58" and 1.70" across
   slides 5, 6, 7 and 9. All normalised to 1.56", the canonical mock height, so every
   visual in the deck starts on the same line.

**Round 2 - the student.** Found and fixed:

1. Slide 9's title used *"the failure mode inverts"* - jargon a beginner meets with no
   definition. Retitled *"forgetting is not the risk"*, which states the same insight in
   plain words and matches the table's *"What goes wrong"* row.
2. *"the store"* first appeared in slide 3's copy without ever being defined; slide 2 only
   said "profile". Slide 2's copy now names it: "a store of plain sentences".
3. Slide 4's caption claimed "Every assistant in the world gets the same model", which is
   not reliably true across plans and rollouts. Softened to "Everyone in the room is
   talking to the same model; only your lines differ."
4. **Layout:** slide 6's right-hand caption sat at 1.64" against layers starting at 1.56",
   so its top edge was 0.08" adrift. Aligned to 1.56".

Read as titles only, the arc holds: what it is, the consequence, what it is not, the two
doors, what reaches the model, ageing, limits, the inverted risk, what to put in it, demo.

## For James

1. **Verify the exact wording before you film.** `help.openai.com` and `openai.com` both
   return a Cloudflare 403 from this environment, so every specific above came from
   search-engine summaries quoting those pages rather than from the pages themselves. The
   shape is solid; the exact menu labels (*Memory Summary*, *Manage*, *Refresh*, *Delete
   and turn off memory*) deserve a 60-second check on your own account.
2. **Which UI do you demo?** The memory-summary screen is rolling out by plan and region,
   so your account may show it and a student's may not. Worth one spoken line
   acknowledging that the screen is mid-rollout, and demoing whichever you have.
3. **The lecture's "Manage Memories" list may be gone.** If your account shows the new
   summary, the original path (Settings > Personalization > Manage, delete rows one by
   one) no longer describes what a student will see, and the way to remove a fact is now
   to write the correction rather than delete a row. That is worth saying explicitly on
   camera, because students who took the old lecture will go looking for the list.
4. **Overlap with Custom Instructions.** That lecture's note is "Customize ChatGPT has
   moved to Settings > Personalization" - the same screen memory now lives on. Whichever
   of the two you film first should own the tour of that screen; the other should point
   at it. The decks do not overlap: mine touches standing instructions only as one layer
   of the assembled context on slide 6.
5. **Privacy is only gestured at.** The deck says "anything you would not want read
   aloud" and stops. If you want the stronger, reassuring facts on camera - it does not
   store usernames or passwords, and it is trained to leave sensitive detail such as
   health alone unless you ask - they are demo-half lines, not slides.
6. **Projects gets one line.** Slide 8 says memory can be held to a single project. If the
   Projects lecture covers project-only memory in depth, tell me and I will cut the line.
