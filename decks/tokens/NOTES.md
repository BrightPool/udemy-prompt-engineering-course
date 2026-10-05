# What are Tokens? - deck notes

Principles half of the re-film. Source video `37093534` (05:05), transcript at
`scripts/udemy-sync/transcripts/03_how-does-ai-work/015_37093534_what-are-tokens.txt`.

Build: `uv run --with python-pptx python decks/tokens/build_tokens.py decks/tokens/tokens.pptx`
Lint: `uv run --with python-pptx python .claude/skills/principles-deck/scripts/check_deck.py decks/tokens/tokens.pptx`
→ **clean, 12 slides, 0 errors, 0 warnings.**

## The three principles

- **What it is.** A token is a run of characters common enough for the model to store as
  one unit, so a sentence's token count never matches its word count.
- **How it works.** Text is split into known chunks, each chunk becomes a number, the
  model predicts the next number and repeats - and every one of those numbers, yours and
  its own, has to fit inside a single context window.
- **Why it matters.** Every token is billed in one of three buckets - input, cached
  input, output - so a long prompt is cheap next to a long answer, and a stable reused
  opening is cheaper still.

## Deck outline

| # | Slide |
|---|---|
| 1 | Tokens (title) |
| 2 | What is it? - a chunk of characters, not a word |
| 3 | Why the count is never the word count |
| 4 | What a token is not |
| 5 | How it works - split, number, predict, repeat |
| 6 | What has to fit in the context window |
| 7 | Every turn re-sends the whole thread |
| 8 | When the window fills up |
| 9 | Why it matters - a token has three prices, not one |
| 10 | Why a repeated opening costs less |
| 11 | What that changes about how you prompt |
| 12 | Let's see it in action (handoff) |

## Research

Primary sources, all fetched 2026-09-08.

**Tokens and the rule of thumb** - `developers.openai.com/api/docs/concepts`:
"Tokens represent commonly occurring sequences of characters"; "1 token is approximately
4 characters or 0.75 words for English text"; for text generation models "the prompt and
the generated output combined must be no more than the model's maximum context length".

**Context window** - `developers.openai.com/api/docs/guides/conversation-state`: the
context window is "the total tokens that can be used for both input and output tokens
(and for some models, reasoning tokens)"; "This max tokens number includes input, output,
and reasoning tokens"; "Tokens generated in excess of the context window limit may be
truncated in API responses". Reasoning tokens count too - worth saying aloud, the deck
does not name them because they belong to the reasoning-models lecture.

**Compaction** - `developers.openai.com/api/docs/guides/compaction`: when a thread grows,
context can be compacted into an encrypted summary that "carries forward key prior state
and reasoning"; the compaction item is "opaque and not intended to be human-interpretable".
That is the source for slide 8's "compressed into a summary you cannot read".

**Prompt caching** - `developers.openai.com/api/docs/guides/prompt-caching`: a cache hit
needs "an identical rendered prefix"; "if content or a relevant setting changes before a
breakpoint, the prefix after that change cannot match"; minimum 1,024 visible input tokens
on GPT-5.6+ (2,048 on earlier models); cached prefixes stay eligible for 30 minutes on
GPT-5.6+ (5-10 minutes `in_memory`, up to 24h with the `24h` option, on earlier ones);
**cached reads cost 0.1x the standard rate, cache writes 1.25x**; changing model, tools,
schemas or reasoning settings invalidates reuse; guidance is to "keep stable developer
instructions and shared reference material first".

**BPE** - `github.com/openai/tiktoken`: "a fast BPE tokeniser for use with OpenAI's models".

**The token splits and every number on slide 3** were produced locally, not quoted from a
page: `tiktoken` with the `o200k_base` encoding, run in this repo's environment.

| Sample | Chars | Tokens | Chars/token |
|---|---|---|---|
| `Tokenisation splits text into pieces.` | 37 | 7 | 5.3 |
| `トークン化はテキストを断片に分割します。` (same sentence) | 20 | 16 | 1.3 |
| `def get_user_id(request): return request.session["user_id"]` | 64 | 14 | 4.6 |
| `The invoice total was 1,284,993.47 dollars.` | 43 | 14 | 3.1 |

Slide 2's split is the real one: `Unbelievably, tokenisation is unpredictable.` →
`Un | bel | ievably | , | token | isation | is | unpredictable | .` - four words, nine
tokens. Re-runnable at any time; if a future encoding changes the split, rerun and update
the build script rather than fudging the slide.

## What has changed since filming

1. **The models he walks through are gone from the top of the list.** The video reads out
   GPT-5.2 and GPT-5 Mini as the current comparison, and the pricing-page exercise at
   2:42-3:20 tells students to compare "O1 versus O3 Mini". Those model names are stale.
2. **Context windows have grown.** The video says 400,000 context / 128,000 max output.
   The current flagship line is listed at **1.05M context, 128K max output**. The deck
   therefore teaches "the window is finite and shared" and never states a size.
3. **Cached input did not exist in the lecture at all.** It is now a published third
   column on every price table and the single most actionable cost lever a student has.
   Slides 9 and 10 exist because of James's note.
4. **The docs moved.** `platform.openai.com/docs/*` 301-redirects to
   `developers.openai.com/api/docs/*`. Worth knowing if any older lecture links to the
   old path.

## Today's rates - for the spoken track, not for a slide

Per 1M tokens, read from the pricing page (`developers.openai.com/api/docs/pricing`) on
**2026-09-08**. Re-check on the day of filming; these move constantly, which is the whole
reason they are not on a slide.

| Model | Input | Cached input | Output |
|---|---|---|---|
| GPT-6 Astra | $10.00 | $1.00 | $50.00 |
| GPT-5.6 Sol | $4.00 | $0.40 | $20.00 |
| GPT-5.6 Terra | $2.00 | $0.20 | $12.00 |
| GPT-5.6 Luna | $0.20 | $0.02 | $1.20 |
| GPT-5.5 | $5.00 | $0.50 | $30.00 |
| GPT-5.4 | $2.50 | $0.25 | $15.00 |
| GPT-5.4-mini | $0.75 | $0.075 | $4.50 |
| GPT-5.4-nano | $0.20 | $0.02 | $1.25 |
| GPT-5.2 | $1.75 | $0.175 | $14.00 |
| GPT-5.1 | $1.25 | $0.125 | $10.00 |
| GPT-5 | $1.25 | $0.125 | $10.00 |
| GPT-5-mini | $0.25 | $0.025 | $2.00 |
| GPT-5-nano | $0.05 | $0.005 | $0.40 |

Two things to notice out loud when the pricing page is on screen:

- **Output is 5-8x input** across the whole line (Sol 4 → 20, Terra 2 → 12, 5.2 1.75 → 14).
  That ratio is what the middle bar on slide 9 is drawn from.
- **Cached input is exactly a tenth of input** on every row, matching the documented 0.1x
  cached read rate. The cache *write* costs 1.25x, so paying to fill a cache you only use
  once is roughly a wash; it pays from the second reuse onward.

The figures the video quotes (GPT-5.2 at $1.75/$14, GPT-5 Mini at $0.25/$2) happen to
still be correct today - the problem is not that they are wrong, it is that they are no
longer the models anyone would reach for, and neither figure mentions caching.

## Review rounds

**Round 1 - the hostile reviewer.** Six findings, all fixed:

1. Slide 3's table header read "Same idea, written four ways", which is false - a line of
   Python is not the same idea as an English sentence. Now "What you send".
2. Slide 3's caption ("cost a reader twice the budget it costs you") was muddled; rewritten
   to say plainly that the identical sentence costs twice as many tokens in Japanese.
3. Slide 9's three bars were empty grey rectangles, so the slide's central claim lived only
   in the caption. Each bar now carries its rate phrase inside it.
4. Slide 5's token chips carried leading spaces, which rendered as odd centring and taught
   nothing. Trimmed.
5. Layout: content tops were ragged - 1.52 (diagrams), 1.56 (mock, compare), 1.58 (table),
   1.62 (bars). Everything I control now starts at **1.56**; the only outlier left is
   `two_columns`, whose 1.58 heading position is fixed inside `deckkit`.
6. Layout: the `compare` panels on slides 4 and 11 were 2.60" tall with 1.62" of content,
   trailing an inch of empty panel. Both cut to 2.00" and their captions lifted.

**Round 2 - the student.** Three findings, so a third round was run per the rubric:

1. Slide 9 named "cached input" two slides before anything explained caching. The two
   why-slides were **reordered**: three prices → why a repeated opening costs less → what
   that changes about how you prompt. The habits slide now closes the argument and its
   caption picks up the caching point ("consistent about the order you give it in").
2. "Context window" appeared in a title before it was defined. Retitled to *"What has to
   fit in the context window"*, so the title itself implies the meaning and the caption's
   first sentence defines it outright.
3. The streaming chip row ended on an accented full stop, which reads as emphasis on
   punctuation. It now ends on an accented `…`, so the row reads as a reply still arriving.

**Round 3 - accuracy sweep.** One finding: slide 10 implied a cache lasts indefinitely.
Caption now says the cached rate applies "for a while afterwards", which is true across
providers without quoting anyone's TTL. Layout re-checked slide by slide at 150 dpi; the
lowest element in the deck is slide 6's closing node at y=4.96", clear of the 5.10" band.

## For James

1. **The tokeniser tool could not be verified from here.** `platform.openai.com/tokenizer`
   returns **403** to plain fetching *and* to a real browser (Cloudflare challenge), so I
   could not confirm the page still exists or what it now looks like.
   `[unverified - James to check on his account]`. It matters because handoff card 1 sends
   you there. If it has moved, the demo still works with any tokeniser, or with `tiktoken`
   in a notebook - the deck names no URL, so nothing on a slide breaks either way.
2. **The pricing figures above were extracted by a fetch tool summarising the docs pricing
   page, not read by eye.** The structure (three columns, cached = 0.1x input, output =
   5-8x input) is solid and matches the caching guide. Please glance at the page before
   you say a specific number on camera.
3. **The old pricing-page exercise needs rewriting for the demo.** "Type OpenAI pricing
   into Google, compare O1 versus O3 Mini" is dead. Suggested replacement, which is what
   handoff card 3 sets up: open the price table, point at the three columns, and pick any
   two models to show that output is several times input and cached input is a tenth of it.
4. **Overlap check.** Slide 7 ("every turn re-sends the whole thread") is close to
   territory the Memory lecture covers. I kept it because the point here is purely
   arithmetic - the thread is re-counted, so cost grows with thread length - and Memory's
   deck makes the opposite point, that a short written store survives *between* threads.
   Worth watching them back to back once.
5. **Reasoning tokens are named in the docs as counting against the window** but are not on
   any slide, since the Reasoning Models lecture owns that idea. One sentence in the spoken
   track on slide 6 would close the loop if you want it.


---

**Verified after this deck was written (orchestrator, 2026-09-08):** `platform.openai.com/tokenizer` DOES still load — the 403 above came from a headless browser. Using the headed Playwright session in DECK_BRIEF.md it returns the OpenAI Platform page normally. Item 1 of *For James* is resolved: the tokeniser tool is still there.


---

## Caching and quotas rework (2026-09-10)

**Slide 13 redesigned.** The old slide showed the same three blocks in two orders
and asked the student to infer why one was cheaper. It now shows caching as what
it actually is: a **prefix match**. Three bars, same prompt:

1. *First time* - nothing recognised, all of it at full price.
2. *Ask again* - the opening is recognised, only the tail is new.
3. *Edit the top* - one word changed early, the match breaks there and everything
   after it is full price again.

That third row is the point of the slide, and the old version never made it.

**New slide 14: "Which of these prices do you actually pay?"** Most students are
on a subscription and will never see a per-token bill, so the three-bucket slide
before it can mislead. This one splits it:

- *On a ChatGPT subscription* - no per-token bill; an allowance per model that
  refills on a rolling window with a weekly cap over it; hit one and you wait for
  the reset or switch model.
- *Building on the API* - you pay per token in the three buckets, caching is a
  real lever, and we return to it properly later in the course.

### For James - verify before filming

- **Verified** from the help centre (`20001354-gpt-56-and-gpt-6-pro-in-chatgpt`,
  updated within a day of writing): allowances are per plan **and per model**;
  some are stated **per week**; ChatGPT displays when an allowance resets; on Pro,
  reaching a model's weekly limit switches you to another model automatically.
- **[unverified]** the **5-hour rolling window** specifically. I could not find it
  stated on that page, so the slide says "a rolling window, with a weekly cap on
  top" rather than naming a number. Confirm the exact windows on your own account
  and say them aloud - no figure is printed on any slide, so nothing breaks if
  they change.
- Free and Go currently have unlimited everyday text chats, with separate limits
  on uploads, image generation, voice and data analysis. Worth one spoken line, as
  a chunk of the class will be on Free.
