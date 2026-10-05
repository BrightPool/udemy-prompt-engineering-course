# Custom Instructions — deck notes

Lecture: Part 2 · ChatGPT Deep Dive · re-film · 01:18 · owner James · video_id `39480068`
Deck: `decks/custom-instructions/custom-instructions.pptx` (8 slides)
Build: `uv run --with python-pptx python decks/custom-instructions/build_custom_instructions.py decks/custom-instructions/custom-instructions.pptx`
Lint: `uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py decks/custom-instructions/custom-instructions.pptx` → **clean, 0 errors, 0 warnings**

## The three principles

- **What it is** — a short standing prompt you write once and save, which the product
  attaches to the top of every new chat you open.
- **How it works** — it is not a setting the model obeys; it is text pasted in above your
  message, so the model reads your instructions and your question as one flat prompt.
- **Why it matters** — it removes the preamble you would otherwise re-type in every chat,
  but it is steering rather than a contract: a later line in the same chat outranks it,
  long conversations drift back to the model's defaults, and vague traits do nothing.

## Slide order

1. Title
2. What is it? – a standing prompt you write once *(mock: a System line nobody typed, then an ordinary exchange)*
3. Yours to write, not the model's to save *(custom instructions vs memory vs projects)*
4. How it works – your instructions are prompt text *(`s.layers()` → one flat context — the load-bearing slide)*
5. Wording the model can act on *(vague vs checkable)*
6. Why it matters – a strong default, not a guarantee *(without/with table, incl. failure mode)*
7. What earns a place in it *(write it once / say it in the message)*
8. Let's see it in action

## Research — what is true now

Sources: OpenAI Help Centre "ChatGPT Custom Instructions" and "Customizing Your ChatGPT
Personality"; OpenAI Model Spec (chain of command, red-line principles); ChatGPT
changelog coverage of the July 2026 character-limit change.

- **Where it lives now.** Settings → Personalization → Custom Instructions, with
  "Enable customization" toggled on. The old top-right-profile-icon → "Customize ChatGPT"
  route is what the current recording shows. **Say the path aloud; it is deliberately not
  on any slide.**
- **Character limits.** 1,500 characters on Free and Go; 5,000 on Plus, Pro, Business,
  Enterprise and Education. The 5,000 ceiling was raised from 1,500 in July 2026.
  Available on all plans, across web, desktop, iOS and Android.
- **Field structure has consolidated.** The recording describes four separate boxes
  (name / what you do / traits / anything else). The Personalization panel now leads with
  a **base style and tone** preset plus warmth / enthusiasm / formatting-and-emoji
  controls, with **Custom Instructions** as the free-text field underneath. The four-box
  framing in the current video is stale; the *idea* (standing context + standing style)
  is not.
- **The Advanced capability toggles.** The recording shows an Advanced section for
  switching web search, image generation, code, canvas and advanced voice on or off for
  new chats. Those toggles have historically sat at the bottom of that panel and are easy
  to miss on a small viewport. See `## For James` — worth a glance before filming.
- **Precedence.** OpenAI's Model Spec ranks instructions root → system → developer → user
  → guideline, and says an instruction is *superseded* by a later instruction at the same
  authority level. Custom instructions are user-level standing text, so a contradicting
  line typed later in the same chat wins. The spec also states that
  "customization, personalization, and localization … should never override any principles
  above the 'guideline' level" — the honest basis for slide 6's "steering, not a contract".
- **Not shared.** Custom instructions are not exposed to viewers of a shared chat link.
- **Relationship to the sibling lectures.** Custom instructions are standing rules *you*
  write, global to every chat; memory is facts the assistant saves *itself*; project
  instructions are rules scoped to one project and take priority inside it. All three land
  in the same place — text in front of the model — which is the framing slide 3 uses.

## What changed since filming

| In the recording | Now |
|---|---|
| Profile icon → "Customize ChatGPT" | Settings → Personalization → Custom Instructions |
| Four boxes: name, what you do, traits, anything else | Style/tone presets and sliders, plus one free-text Custom Instructions field |
| No stated length limit | 1,500 chars (Free/Go) / 5,000 chars (paid tiers) |
| "Enable for New Chats" toggle | "Enable customization" toggle |

None of that is on a slide. The deck teaches the mechanism, which has not changed.

## Review rounds

**Round 1 — hostile reviewer.** Six findings, all fixed:
1. *(slide 4)* The layer stack put "Your standing instructions" above "The product's own
   rules", which contradicts the precedence taught on slide 6. Reordered to the true
   assembly order: product rules, your standing instructions (accented), memory, your
   message.
2. *(slide 5)* "Ask before assuming our pricing" imported a business context from slide 2
   for no reason, and overflowed its box. Now "Ask before you assume a figure".
3. *(slide 5)* "First line is the answer, no preamble" was tight in its column → "No
   preamble - open with the answer".
4. *(slide 6)* Table said "As good as your memory that day" — the word *memory* collides
   with the Memory feature defined two slides earlier. Now "Whatever you re-typed that day".
5. *(slide 6)* Caption ran to five clauses; trimmed one.
6. *Layout* — the slide 4 caption sat at y=1.60 against a diagram running to y=5.00, so
   the right column read top-heavy. Moved down.
   Also fixed a pre-lint failure on slide 2: the mock grew past the footer band once the
   composer flowed, so a redundant label line and one turn line were cut and the copy beside
   it rewritten to carry the "nobody typed this" point instead.

**Round 2 — the student at 1.5x.** Three findings, all fixed:
1. *(slide 4)* Title read "they arrive as part of the prompt" — a pronoun with its
   antecedent two slides back. Now "your instructions are prompt text", which states the
   mechanism in the title.
2. *Layout* — slide 3's caption sat 0.24" under the table, close enough that a wrapping
   cell could crowd it. Dropped to 3.86.
3. *Layout* — slide 4's caption still read high against the stack; moved to 2.25 so the
   two columns are optically centred on each other.

Round 2 turned up no substantive content findings, so no third round. Titles read top to
bottom now tell the whole story, and the smallest text on any white surface is 12pt.

## For James

1. **Say the path, do not show it.** The whole of your note is a navigation change, so
   nothing about it is on a slide. In the demo half, say: *Settings → Personalization →
   Custom Instructions, and make sure "Enable customization" is on.* If it moves again,
   that is one take, not a deck rebuild.
2. **The four boxes are gone — please confirm on camera.** The current recording walks
   through name / what you do / traits / anything else as separate fields. What I can
   verify is that Personalization now leads with a base style-and-tone preset plus warmth,
   enthusiasm and formatting controls, with Custom Instructions as a single free-text box.
   I could not fetch the Help Centre pages directly (Cloudflare blocks automated fetches),
   so please eyeball your own account before filming and adjust the spoken track.
3. **Does the Advanced capabilities section still exist?** The recording ends on toggling
   web search / image generation / code / canvas / advanced voice for new chats. I could
   not confirm whether that section survives in the current Personalization panel. If it
   does, it is worth 10 seconds in the demo; if it has gone, cut that beat — no slide
   depends on it either way.
4. **Retroactivity is genuinely ambiguous.** OpenAI's own help page says updates apply
   "immediately to all chats" in one place and "only future conversations" in its FAQ, and
   user reports side with the latter. The deck therefore says instructions are attached to
   *every new chat you open* and never claims anything about chats already in progress.
   Suggest you do the same on camera.
5. **Character limits are in this file, not on a slide** (1,500 free / 5,000 paid, raised
   July 2026) — mention them if you like, but they will move.
6. **Overlap check.** Slide 3 names Memory and Projects only to draw the boundary — who
   authors the text and how far it reaches. It teaches neither. Both sit earlier in the
   manifest, so students will already have met them; if you re-order the section, that
   slide becomes a forward reference and its caption is the only thing that needs a word
   changing.
7. **Suggested demo beat that pays off slide 6.** After showing the instructions working,
   contradict one of them in the message ("actually, give me the long version with a
   preamble") and let the later line win. It makes "steering, not a contract" concrete in
   about fifteen seconds, and it is the fourth card on the handoff slide.

## Deliberate deviations from the brief

- The slide 2 mock overrides the house tag `Demonstration` with `Every new chat`. Reason:
  the panel's entire point is that this is an *ordinary* chat with a line in it nobody
  typed, and the tag is what carries that. The app label stays `ChatGPT` and the turns
  stay `System` / `User` / `AI Assistant`.
- 8 slides rather than the brief's usual 10-14. The lecture is 01:18; padding it would be
  worse than a short deck.
