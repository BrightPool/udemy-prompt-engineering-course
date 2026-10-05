# Prompt Testing in GSheets (without code) - deck notes

Principles half of the re-film. Source video `42183042` (13:06), transcript at
`scripts/udemy-sync/transcripts/17_prompt-optimization-and-evals/181_42183042_prompt-testing-in-gsheets-without-code.txt`.
Manifest note: **PRESERVE** - excellent no-code evaluation content. Owner: **Mike**.

Build: `uv run --with python-pptx python decks/gsheets-prompt-testing/build_gsheets_prompt_testing.py decks/gsheets-prompt-testing/gsheets-prompt-testing.pptx`
Lint: `uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py decks/gsheets-prompt-testing/gsheets-prompt-testing.pptx`
→ **clean, 12 slides, 0 errors, 0 warnings.**

## The three principles

- **What it is.** A prompt test is a grid: one row per run, one column saying which
  version produced it, one column holding the score - which is an evaluation harness, and
  nothing about it being a spreadsheet makes it less of one.
- **How it works.** A template with blanks becomes the prompt that was actually sent, the
  answer comes back into a cell as a frozen copy, and every row is scored the same way -
  by a formula, a second model, or a person.
- **Why it matters.** The sheet converts "this prompt feels better" into a number with its
  own uncertainty attached, in an ordinary file somebody else can open, re-read and re-run
  when the model changes underneath you.

## Deck outline

| # | Slide |
|---|---|
| 1 | Prompt Testing in a Spreadsheet (title) |
| 2 | What is it? - a grid where every row is one run |
| 3 | The same prompt, ten times |
| 4 | What the chat window does not keep |
| 5 | What a prompt test is not |
| 6 | How it works - the template is not the text you test |
| 7 | Getting the answer back into the cell |
| 8 | What goes in the score column |
| 9 | Reading ten runs honestly |
| 10 | Why it matters - you can show your working |
| 11 | Where the sheet runs out of road |
| 12 | Let's see it in action (handoff) |

## Boundary with `ab-testing-skills`

That lecture teaches the **method** - one change at a time, criteria fixed before you
look, judged across samples. This deck teaches the **instrument**: what the columns are,
how a template becomes a sent prompt, how the answer gets into a cell, what can fill the
score column, and where a sheet stops being the right tool. The method appears here only
where it is a property of the grid (the score column exists so every row is scored the
same way).

## Research - what has aged since filming

Filmed against GPT-4 in early 2024. Verified 2026-09-08.

### 1. A cell can now call a model itself - the biggest change
The lecture's whole loop is manual: copy the formatted prompt out of the sheet, paste it
into a playground, copy the answer back. Google Sheets now has a **native in-cell model
call**: `=AI("prompt", range)`, also available as `=Gemini(...)` - primary-verified at
`support.google.com/docs/answer/15877199`. Its documented limits are worth knowing before
Mike demos it:

- requires "an eligible Google Workspace or Google AI plan"; it is in the **Workspace
  Experiments** programme, i.e. **not generally available** to every account
- "the first 350 selected cells with AI functions will be generated" per go
- "short-term and long-term generation limits" - you can be temporarily locked out
- results are **static** and refreshed manually; "you can't undo or redo your function"
- "doesn't have access to your entire spreadsheet or other files in your Google Drive"

The static-result behaviour is a **feature** for our purposes and the deck says so: an
eval wants a frozen copy of one answer, not a cell that silently regenerates.
Third-party add-ons (GPT for Work / GPT for Sheets, 1M+ users, now credit-based, supports
both ChatGPT and Claude models) remain the route for accounts without the native function.
**No product or formula name appears on any slide** - slide 7 says "a formula in the cell
that calls a model for you", with the caps-and-queues caveat.
`[add-on pricing and the exact experiment gating - unverified, James/Mike to check on the
account they film with]`

### 2. Model names and the message-cap argument
The lecture recommends the API playground over ChatGPT partly because "GPT-4 lets you send
only 50 messages in three hours". That cap number is long dead and should not be spoken.
The **durable** version of the argument survives intact and is the one to say: a chat
window is personalised (memory, custom instructions), so it is the wrong instrument for a
controlled test; a playground or API call is not. Do not name GPT-4, GPT-3.5 or
"turbo preview" on camera. Current lineup for reference only: flagship **GPT-6 Astra**,
below it **GPT-5.6 Sol / Terra / Luna / Cyber**, with GPT-4o still around for cheaper work.

### 3. Temperature is no longer a universal dial
The lecture sets temperature to 1 and max length to 4,000. On current reasoning models the
documented dial is **`reasoning.effort`** (`none` … `max`, defaults model-dependent;
`developers.openai.com/api/docs/guides/reasoning`), not temperature. Slide 3 says
"lowering the temperature narrows this spread; it does not close it", which is true and
stays true; if Mike demos a reasoning model he should say effort, not temperature.

### 4. The pricing aside
The transcript quotes "$3 this month, $130 last month, about five cents a call". No dollar
figures on any slide, per house rule. Today's per-million-token rates, for the spoken
track only (fetched `developers.openai.com/api/docs/pricing`, standard tier):
GPT-6 Astra $10 in / $1 cached / $50 out; Sol $4 / $0.40 / $20; Terra $2 / $0.20 / $12;
Luna $0.20 / $0.02 / $1.20; GPT-4o $2.50 / $1.25 / $10. The durable teaching is the three
buckets - input, cached input, output - and that ten runs of a long blog post is mostly
**output** tokens, the expensive bucket. That is the honest reason a ten-run sheet costs
more than it looks like it should.

### 5. The lecture's own headline finding has probably expired - and that is the point
The control's winning variation was "make it really long or I lose my job" in caps, citing
**EmotionPrompt** (Li et al., arXiv 2307.11760, "Large Language Models Understand and Can
be Enhanced by Emotional Stimuli", ~10.9% average improvement on generative tasks). That
paper was run against models that are now several generations superseded, and current
vendor prompting guidance no longer mentions emotional stimuli, tips or all-caps at all
(`developers.openai.com/api/docs/guides/prompt-engineering`). Modern models also follow
explicit length instructions far better than GPT-4 did, so the transcript's *failed*
variation ("more than 2,000 words") may well pass now.

**Do not treat this as a problem with the lecture - it is the lecture's thesis proving
itself.** Techniques expire; the sheet is what tells you when. The deck therefore labels
its example strips "Control" and "Variation" and asserts no finding about any technique.
The current vendor guide makes the same argument in its own words: build "tests and
evaluation suites that measure prompt behavior so you can monitor performance as you
iterate, or when you change and upgrade model versions".
`[whether the caps trick still helps on today's models - genuinely unknown, and the ideal
thing for Mike to re-run live on camera]`

### 6. Vocabulary aligned to the existing "What are Evals?" deck
`~/Downloads/.../What are Evals_.pptx` splits evals into **Programmatic / Synthetic /
Human**, and names reliability as "how often does it fail if you run it 10 or even 100
times". Slide 8 uses that same three-way split in plain language ("a formula counts it" /
"a second model rates it" / "a person reads it") so the two lectures agree.

## Numbers on the slides

The ten-run strips on slides 3 and 9 and the summary table on slide 9 are **illustrative**
(means 1,085 vs 1,160, +6.9%, ranges 890–1,310 and 930–1,420). They are shaped like a real
weak result - a few per cent apart, ranges overlapping almost entirely - so the slide can
make the honesty point. They are computed in the build script from the two lists at the
top, so changing the lists changes the table automatically. They are not a claim about any
technique, and no technique is named beside them.

## Review rounds

**Round 1 (hostile reviewer).** Slide 4's title "Why it cannot live in the chat window"
overstated the case - it can, it just keeps nothing - retitled "What the chat window does
not keep". Slide 1's subtitle did not name the instrument; rewritten. Slide 5's compare
panels ran ~1" of empty box below the last item, so a fourth pair was added
(reproducibility: "one person's read of one answer" / "a number anyone can recompute") and
the panel height cut to fit. Slide 8's caption listed only the upsides of the three
scoring methods; added the honest limit (a model judge drifts; a human one is slow and
biased unless the criteria were written down first). Slide 9 had 1.38" of dead canvas -
added the summary table, which is the lecture's pivot and was missing anyway.
Layout: visuals started anywhere between 1.52" and 1.70"; all now derive from one `TOP`
constant at 1.56". Slide 6's down-arrow was off the stack's centre line (3.10" against a
centre of 3.12") - now computed from the stack width.

**Round 2 (the student).** The title subtitle had been split across two paragraphs, which
re-enables the bullet glyph - collapsed to one line. "Eval" was first used on slide 5 but
never defined; slide 2's caption now names it where the idea is introduced. Slide 3's
accent node restated the caption above it; replaced with the question the slide provokes
("can I make it stop varying?"). Slide 4's mock label "Ask again, same words" did not read
as a fresh run - now "Same prompt, minutes later" (and shortened again after the linter
flagged the label overflowing its box).

**Round 3** (run because round 2 turned up three substantive items). Three names were in
use for the same thing - "prompt sent", "filled-in prompt", "the exact characters that
were sent"; unified on **the prompt that was sent** across slides 2, 6 and 7. Slide 3
coined "randomness setting" where the thing has a name; now says temperature. Slide 9's
caption said "seven per cent" against a table reading +6.9% (now "about seven per cent")
and carried two pairs of quotation marks, rephrased away. Layout pass found nothing
further; every visual starts at 1.56", nothing crosses 5.10", no dark tables, one accent
element per slide.

## For James

1. **Long format, not wide.** Your brief describes "one column per prompt version". The
   lecture's actual sheet - and the pivot at the end of it - is long format: one row per
   run, tagged with a `Version` column. The deck teaches the long shape because that is
   what the pivot needs and what the video shows. Say the word if you want it flipped.
2. **The headline result in the original video is probably no longer true** (research
   note 5). I have deliberately not asserted it either way on a slide. My recommendation
   is that Mike re-runs the caps/emotion variation live, whatever the outcome - a
   technique visibly expiring on camera is the strongest possible advert for the lecture.
3. **In-cell model calls change the demo, not the deck** (research note 1). The native
   Sheets function is still gated behind an experiments programme, so whether Mike can
   film it depends on the account. The deck works either way; slide 7 covers both routes
   without naming one.
4. This lecture and `ab-testing-skills` are adjacent by design. If that deck ends up also
   showing a grid, mine is the one that should keep it - the note says PRESERVE, and the
   grid is this lecture's whole subject.

## For Mike

- **The deck is deliberately self-contained**; nothing in it depends on a callback to one
  of James's other lectures, and every term it uses it defines.
- **Three things not to say on camera**, because they date the video and are already wrong:
  the 50-messages-in-three-hours cap, any model name or version number, and any dollar
  figure. The durable versions are all above.
- **Slides 3 and 9 use the same visual on purpose.** Slide 3 shows the spread inside one
  version; slide 9 adds a second strip and the summary. It is a callback, so it is worth
  saying "same picture as before, one more row" when you reach it.
- **The best line to land is slide 9's**: the sheet will show you a difference long before
  it can tell you the difference is real. Everything students get wrong with this technique
  is over-reading ten noisy rows.
- The demo half is where the length lives - the deck is 12 slides against a 13-minute
  lecture on purpose.

## Round: visual upgrade (2026-09-28)

Paragraph captions were cut to one line; the detail they carried is below, to say aloud.
- Slide 2: a drawn spreadsheet (column letters, row numbers, pink score column) with callouts for One Row One Run / Which Version / The Score. "That grid is an eval."
- Slide 3: a dot plot of the ten control runs on a word-count axis, with range band and mean. Temperature note kept: lower temperature narrows the spread, it does not close it.
- Slide 4: the paragraph beside the mock became three icon rows of what the chat loses (exact prompt, other answers, a record to share).
- Slide 5: "Not this / This" became paired rows with cross and tick icons.
- Slide 6: a visual equation, template + row values = the prompt sent, with the edit under test in pink. Say: you edit the template, but the sent prompt is what reached the model.
- Slide 7: icon flow (prompt, model, answer, score) plus the two routes: copy and paste (works anywhere) vs a formula in the cell (faster, with caps and queues). Record which model produced each row.
- Slide 8: three judges with consistency and judgement meters. Say: a model judge drifts; a human is slow and biased unless criteria were written first.
- Slide 9: control and variation dot plots on one axis, with the overlap bracketed and +6.9% called out.
- Slide 10: icons added to the table rows. Slide 11: a sheet-to-engineer spectrum bar replacing the two bullet columns.
- Icons: Lucide (ISC licence) in `assets/`, as icon-<name>-<p|i|g>.png. Related shapes are grouped.
