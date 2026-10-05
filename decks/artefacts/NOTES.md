# ChatGPT Artefacts — deck notes

Lecture 029, Part 2 · ChatGPT Deep Dive · re-film · 04:58 · video `46579771`
(was "ChatGPT Canvas"). Deck: `artefacts.pptx` (12 slides), built by `build_artefacts.py`.

## The three principles

- **What it is** — An artefact is a durable document held inside the conversation: it
  has its own body of text, it stays put between turns, and both you and the assistant
  can edit it in place.
- **How it works** — A change is aimed at a region — you point at part of the document
  (or at all of it), the model returns replacement text for that part only, everything
  outside it is left exactly as it was, and the updated document is what the next turn
  reads.
- **Why it matters** — Regeneration throws away the lines you liked along with the ones
  you didn't; a targeted edit lets work accumulate, which is why how you phrase the ask
  decides how much of the draft survives it.

## Research: what this surface is now

**Sources are primary and verified.** `help.openai.com` and `openai.com` return 403 to
plain fetches *and* to headless Playwright (Cloudflare interstitial). What got through was
a **headed, persistent Chrome profile**:

```bash
playwright-cli -s=art2 open --browser chrome --headed --persistent
playwright-cli -s=art2 goto "https://help.openai.com/en/articles/..."
```

Worth putting in `DECK_BRIEF.md` — the documented `playwright-cli -s=docs open` recipe is
not enough for these two hosts.

### Canvas no longer exists on current models — this is the headline

From the ChatGPT release notes (`help.openai.com/en/articles/6825453`), **28 May 2026**,
verbatim:

> "With this update, canvas will no longer be available in GPT-5.5 Instant or GPT-5.5
> Thinking. Writing and coding functionality is now supported directly in chat responses
> through **writing blocks** and **code blocks**. Paid users can continue using canvas for
> a limited time through legacy models until those models are sunset."

Corroborating evidence:
- The old help article `9930697-what-is-canvas` now **404s**.
- Searching the help centre for "canvas" returns **no canvas article at all**.
- Its replacement is *Working with writing blocks and code blocks in ChatGPT*
  (`articles/20001246`, "Updated: last month"), which never uses the word canvas.

### What the surface does today (all from article 20001246, verbatim capabilities)

- **Writing blocks** are "editable areas for draft text, such as emails, messages, social
  posts, and documents". You can: select the block and **edit the text directly**; copy;
  **ask ChatGPT to revise selected text or the entire draft**; open it in a **full-screen
  editing view**; **undo or redo** recent AI-assisted edits; send supported email drafts;
  save supported document drafts to your Library.
- **Formatting supported**: bold, italic, headings, links, bulleted and numbered lists,
  checklists.
- **Code blocks**: copy; language label; edit supported blocks directly; ask ChatGPT to
  edit; open full screen; switch between **Code** and **Preview**; **run** supported
  Python and see console output; share a read-only link.
- **Preview** covers HTML pages, React components, SVG, Mermaid diagrams, Vega/Vega-Lite
  charts. Previews and execution run in a sandbox; ChatGPT may ask permission before
  reaching outside resources, and workspace admins can disable execution and network.
- **Persistence** — the single most useful mechanism fact: "Edits to supported writing
  blocks and code blocks **save with the conversation after a short delay**. ChatGPT can
  then use the **latest version** when you ask follow-up questions." In Temporary Chat,
  edits may not persist.
- **Availability varies** by plan, device, workspace settings, model and rollout — which
  is exactly why none of it is on a slide.

Two further release-note entries, both primary:
- **19 Feb 2026** — Interactive Code Blocks: write and edit in-line, preview diagrams and
  mini apps, review code in split-screen.
- **8 Jun 2026** — Full-screen writing blocks for longer-form work: essays, PRDs, reports,
  blog posts; save the document to your Library; wider layout, table of contents for long
  documents, download support, undo/redo fixes.

### What I could *not* verify

- **Version history.** The old canvas had a browsable change history (James demos it at
  ~2:20 in the current lecture). The current help article documents only **undo/redo of
  recent AI-assisted edits**, and "version history" appears nowhere in the release notes.
  I have not claimed either way on a slide — slide 9 teaches "a current version, not an
  archive, so copy a good draft out", which is true regardless.
  `[unverified — James to check on his account]`
- **The old shortcut buttons** — adjust length, reading level, add emojis, final polish,
  port to a language, fix bugs, add logs, add comments. None appear in the current help
  article. They look gone, replaced by asking in plain language against a selection.
  `[unverified — James to check on his account]`
- **Multiplayer editing.** Not documented. I removed a slide line claiming it *doesn't*
  exist, because that is a negative claim a redesign could falsify.

## What changed since filming

| In the video | Now |
|---|---|
| "Canvas", released 3 Oct 2024 | **Retired on current models** (28 May 2026). The surface is writing blocks and code blocks, inline in the response |
| Turn it on by picking "GPT-4o with canvas" from the model picker | No mode to select. A block appears when the reply is something you'd revise, or because you asked for a draft |
| "This is in beta at the moment" | Long out of beta; the successor is the default behaviour |
| Shortcut buttons: reading level, length, emojis, polish, port to a language, fix bugs, add logs | Undocumented today — ask in plain language, against a selection |
| "It's actually a regeneration from the top down" (~1:35) | **Still the key insight, and now the spine of the deck.** A vague ask still regenerates; an ask aimed at a selection does not |
| Version history you can walk back through | Undo/redo of recent AI-assisted edits is what's documented — see above |
| Canvases listed at the top of the chat | Blocks live in the response; long documents can be saved to Library |
| Comparison to "Claude artefacts" | Still a fair comparison, and it is where our lecture title comes from |

## Review rounds

**Round 1 — the hostile reviewer.** Seven findings, all fixed:
1. Slide 9 claimed the object "does not hold ... two people typing at the same moment" and
   "every draft you passed through" — two negative claims a shipped feature could falsify.
   Replaced with mechanism-true limits (a draft you replaced without copying, anything
   from another conversation, your last keystroke until it saves).
2. Slide 4's copy restated slide 3's point instead of making its own. Rewritten to carry
   the content-agnostic point and the stakes of regenerating code.
3. Slide 5's title was "What it is not" — the identical title the data-analysis deck uses,
   and it announces a section rather than making a point. Now "Not a nicer-looking answer".
4. Slide 5's compare panels were 2.60" tall for 1.58" of content and the slide died at
   4.12". Panels cut to 2.10" and a caption added, so the slide fills like the rest.
5. Layout: slide 6's caption was top-aligned at 2.00" against a column of steps running
   1.52"–4.84", leaving it stranded at the top right. Re-centred to 2.62". Same fault on
   slide 7 — moved 1.90" → 2.43".
6. Layout: slide 8 was top-heavy — the flow ended at 3.26" with a full inch of dead space
   below the caption. Flow grown 1.10" → 1.40", caption moved to 4.05".
7. Layout: slide 10's table started at 1.55" against 1.52" on every other slide.

**Round 2 — the student.** Five findings, all fixed:
1. The obvious first question — *how do I get one?* — went unanswered. Slide 2's copy now
   says: by asking for a draft, or because the assistant judged you'd revise the answer.
2. Three words were doing one job across the deck: *address*, *point at*, *region*. Slide 6
   step 2 now says "point at", matching the phase title, and "address" survives only in the
   caption where it explains why pointing matters.
3. Slide 6 step 1 said "apart from the thread" — "thread" is never defined. Now "apart from
   the messages".
4. Slide 9's "Your newest keystroke, for a moment" was cryptic inside a list of what the
   object does not hold. Now "Your very last keystroke, until it saves."
5. Slide 3's mock ended on "One paragraph. The rest is as you left it" — the slide author
   narrating the point, not product output. Cut to "Paragraph 2 only."

**Round 3** (required: round 2 found more than two substantive issues). Two findings, both
fixed:
1. Slides 2, 3 and 4 were three consecutive user→assistant chat mocks with near-identical
   structure — at 1.5x they read as the same slide three times. Slide 4 rebuilt as the
   artefact object itself listing what it can hold (email, code, plan), with no exchange.
   Title changed to "The same object, whatever it holds".
2. "the lot" appeared in slide 6's caption and slide 11's column heading. Slide 6 now ends
   "falls back to rewriting everything."

Layout pass after each round; lint clean after each rebuild. Final: `clean - 12 slides,
nothing to fix`.

## For James

1. **The rename is right, but "Artefacts" is our word, not OpenAI's — and "Canvas" is no
   longer theirs either.** As of 28 May 2026 canvas is gone from current models; the
   product calls this **writing blocks** and **code blocks**. The deck deliberately names
   no vendor label at all, so it cannot go stale. **Please say the mapping aloud once in
   the demo half**, e.g. *"the course calls these artefacts; in ChatGPT today you'll see
   them called writing blocks and code blocks — Canvas was retired."* Without that line a
   student searching for "canvas" will find nothing.
2. **Your best line in the original lecture is now the spine.** At ~1:35 you notice
   "it's actually a regeneration from the top down" and call it a limitation. That is
   exactly the mechanism the deck teaches: a vague ask regenerates, an ask aimed at a
   selection does not. Worth landing hard on camera.
3. **Check version history on your account.** The old canvas had a browsable change
   history; the current help article documents only undo/redo of recent AI-assisted edits.
   If a real history still exists, tell me and I will add it to slide 9's "It holds".
4. **Check whether the shortcut buttons still exist** (reading level, adjust length, add
   emojis, port to a language, fix bugs, add logs). They are undocumented now. If they are
   gone, the demo half should show the plain-language equivalent instead.
5. **Overlap to keep an eye on.** Code blocks can *run* Python, which is the `data-analysis`
   lecture's territory. This deck stays off it entirely — nothing here mentions running
   code or sandboxes; running code as an artefact capability is worth one sentence in your
   demo at most, with a pointer back to the data-analysis lecture.
6. **Availability caveat, for the spoken track only.** OpenAI states the available actions
   vary by plan, device, workspace settings, model and rollout — so if a control is missing
   on a student's account, that is expected, not broken.
7. **Demo suggestion, from slide 12.** The third card asks you to be vague on purpose
   ("make it better") and let the whole draft come back new. That contrast, filmed back to
   back with a selected-paragraph edit, is the whole lecture in thirty seconds.
