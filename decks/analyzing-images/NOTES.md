# Analyzing Images with ChatGPT — build notes

Lecture: `analyzing-images` · Part 2, ChatGPT Deep Dive · re-film · 14:00 · James
Sources: transcript `40611478` (chatgpt-vision) and companion `42691388`
(vision-prompting-guide). Existing deck: `Vision Prompting Guide.pptx` (23 slides).

Deck: `analyzing-images.pptx`, 12 slides, built by `build_analyzing_images.py`.
Lint: **clean, 0 errors, 0 warnings.**

## The three principles

- **What it is** — you supply a picture and ask a question about it; the image is
  turned into tokens and placed in the context beside your words, so the answer is
  reasoning about the picture rather than a lookup of it.
- **How it works** — the picture is resized to fit a fixed budget, cut into a grid of
  32-pixel patches, and each patch becomes input tokens, so resolution decides both
  what the model can resolve and how much of the context the image consumes.
- **Why it matters** — it is reliable on questions about *meaning* and unreliable on
  questions about *measurement*, so the craft is asking a specific question, naming
  the output format, and making it quote what it can see before it interprets.

## Slide arc

| # | Title |
|---|---|
| 1 | Analyzing Images with ChatGPT |
| 2 | What is it? - a question about a picture you supply |
| 3 | What it reads well |
| 4 | How it works - one reading of the picture, taken before you ask |
| 5 | Your picture arrives as tokens, not as pixels |
| 6 | Crop and enlarge what you are asking about |
| 7 | Where it stops |
| 8 | Why it matters - a specific question beats "what is this" |
| 9 | Make it quote before it interprets |
| 10 | A second image gives it something to compare |
| 11 | When to attach a picture |
| 12 | Let's see it in action |

14:00 is the longest lecture in the set, but the deck is deliberately 12 slides. The
extra runtime belongs in the demo half — upload, vague ask, specific ask, quote-first
ask, second image — not in more principles.

## Research

Primary source, fetched and read in full: OpenAI's **Images and vision** guide.
`platform.openai.com/docs/guides/images-vision` now 301s to
`developers.openai.com/api/docs/guides/images-vision`; the `.md` suffix returns the
whole page as markdown, which is how it was read. Everything below is **verified**
against that page unless tagged otherwise.

**Mechanism (this is the spine of the deck).**
- Vision models "convert image inputs into billable input tokens". Images become
  tokens in the same context as the text — they are not inspected as a file.
- Two tokenisation schemes are documented. Newer models are **patch-based**: the
  image is covered with 32px × 32px patches, the patch count is multiplied by a
  per-model multiplier, and the result is the billable image input tokens. Older
  models are **tile-based**: a base token count plus 512px tiles.
- Before any of that, the image is **resized** to fit a pixel-dimension limit and,
  usually, a patch budget. Resizing preserves aspect ratio and never enlarges a
  smaller image.
- A `detail` parameter (`low` / `high` / `original` / `auto`) selects the sizing
  behaviour in the API. **Deliberately not on a slide** — it is an API parameter, not
  something a ChatGPT user sets, and the sizes attached to each level differ per
  model and move between releases. The durable point is that resolution is a dial.
- The docs state plainly: "Images may be resized before analysis, including with
  `original` detail." That sentence is what licenses slide 4's claim that the reading
  is taken before the question is considered.
- Multiple images per request are supported (documented ceiling is high), and each
  one costs its own tokens.

**Documented limitations** — slide 7's right-hand column is drawn from this list and
nothing was invented:
small text ("enlarge text within the image to improve readability"); rotated or
upside-down text; precise spatial localisation; approximate counting; graphs where
solid/dashed/dotted styles vary; non-Latin scripts; panoramic and fisheye images;
medical images; and "the model doesn't process original file names or metadata".
CAPTCHAs are blocked. *Handwriting* was in an early draft of that column and was
**removed** — it is widely true but not in the docs, so it did not survive.

**Cost.** Per the deck brief, no figures on a slide. Slide 4 teaches the structure
instead: patches become input tokens, they occupy the same finite context as your
words, and where you pay per token they bill like any other input. Today's rates and
the per-model multipliers are on the vendor's pricing and vision pages — worth a
glance before filming, not worth a slide.

## What changed since filming

Both transcripts have aged badly, in different ways.

1. **The original lecture's demo is a poor showcase and partly wrong.** It asks how
   many fingers are held up (counting — a documented weak point), then asks the model
   to identify people's **gender** from a photo and emit a CSV of male/female
   probabilities. That is exactly the kind of inference this deck should not teach,
   and it is the sort of thing a modern model will decline or hedge on. The new deck
   keeps the genuinely good idea buried in that demo — *ask for structured output from
   an image* — and re-points it at a chart on slides 8 and 9.
2. **The companion video is a model catalogue.** GPT-4 Vision, CLIP, Gemini 1.5 Pro,
   Claude 3, LLaVA 1.6, Qwen-VL, the 2023 dev day, "$6 an hour", "about 30 images",
   "5 minutes to process one minute of video on an M3". Every one of those numbers is
   now wrong, and the deck carries none of them. Multimodality is table stakes; the
   list has no teaching value left.
3. **"Temporal reasoning" as a headline feature** has become ordinary. It survives as
   slide 10, reframed as the durable point: a second image is something to compare
   against the first.
4. **The five-principles framing** from the companion video is preserved in substance
   rather than as a section: give direction → slide 8, specify format → slide 8,
   provide examples → slide 10, evaluate quality → slides 7 and 9, divide labour →
   slide 9. James may want to name the five principles aloud as he moves through
   those slides, since students met them earlier in the course.

## Review rounds

**Round 1 — hostile reviewer.** Nine findings, all fixed.
- *Substance:* slide 8's mock had a reply that was a bare label plus a two-row table —
  placeholder text pretending to be an answer. Gave the assistant a real line and a
  fuller table.
- *Accuracy:* "billed as input tokens, like any other input" implied a per-image charge
  that a subscription user does not see. Rewritten to lead with context consumption
  and qualify the billing.
- *Accuracy:* dropped "handwritten" from the limits column (see above).
- *Substance:* added the file-name-and-metadata fact to slide 7's caption — it is
  documented, surprising, and reinforces the "it only sees the picture" spine.
- *Layout:* the four chat mocks were 4.60", 4.86", 5.10" and 4.86" wide, so the copy
  column beside them started at a different x on every slide. All standardised to
  4.86" at x=0.40, copy column at x=5.81. One of the four ended in `.fit()` while the
  rest had a composer; all four now carry the composer.
- *Layout:* slide 6's diagram started at y=1.66 while every other slide started at
  1.52. Moved. Its arrow was 0.15" off the centreline between the tiles; recentred.
- *Layout:* slide 4's caption sat 0.08" under its heading; opened to 0.14".
- *Layout:* slide 5's caption was top-aligned against a diagram it should have been
  centred on; moved down 0.33".
- *Craft:* slide 6's right-hand tile had its accent region drawn exactly on the tile
  border, so it read as "this panel is highlighted" rather than "the same subject,
  enlarged". Inset it half a patch.
- *Craft:* two font literals (`"Source Code Pro"`) replaced with the `BODY_FONT`
  token; table column widths rebalanced on slide 3.

**Round 2 — the student.** Six findings, all fixed.
- "Patch" was used on three slides and never defined. Slide 4's caption now opens with
  the definition, at the point the word first appears.
- The word **vision** never appeared anywhere, so a student could not search for it.
  Named once, in slide 2's copy.
- Slide 9's prompt said "list the text you can actually read" without saying where
  from; now "read in the image".
- Slide 9's reply had uneven leading — a 0.06" gap inside one sentence — because the
  continuation used a separate call. Folded into one turn, so the gap now falls
  between the quotation and the answer, where it belongs.
- Slide 5's closing node said "A single run of tokens"; "run" is jargon. Now "One
  stream of tokens".
- Slide 7's accent column was headed "Check it yourself", which did not pair with
  "Safe to act on". Now "Verify before you act".

**Round 3** (triggered: round 2 found more than two substantive issues). One
substantive finding, fixed, plus one nit.
- **Slide 6 was factually wrong.** It claimed both pictures are "cut into the same
  number of patches", and that cropping therefore spends the same budget on a smaller
  area. That is not how it works: a patch covers a fixed square of the image, and a
  small crop is never enlarged automatically — so cropping alone buys less than the
  slide implied. Rewritten around the mechanism the docs actually describe, and the
  slide retitled **"Crop and enlarge what you are asking about"**, which is also the
  advice the docs give. Tile label changed to "Cropped and enlarged".
- Nit: slide 3's table header "And what comes back" read awkwardly across the row;
  shortened to "What comes back".

Layout pass at the end of each round: every content slide now starts at y=1.52, no
slide passes y=5.06, and the four chat mocks are geometrically identical.

## For James

1. **The original demo needs replacing, not re-filming.** The gender-from-photo CSV
   exercise should not go back into the course — it is a weak use of the capability
   and an uncomfortable one. Suggested replacement, which the deck is built to hand
   off to: upload a chart or a dense screenshot, ask "what is this?", then ask the
   specific question, then ask it to quote before answering. Same runtime, three
   visible improvements, and it lands the deck's argument.
2. **Model names.** The deck names no model, by design. Current lineup for anything
   you say aloud: the flagship is **GPT-6 Astra**, with the **GPT-5.6** family below
   it (**Sol**, **Terra**, **Luna**, **Cyber**). GPT-4o still exists for cheaper work.
   The old lecture's "GPT-4 Vision" is three generations back.
3. **Overlap to watch.** Slide 11's right column deliberately routes work to
   *file upload* ("a spreadsheet you could upload as a file"). That is the
   `data-analysis` lecture. Worth one sentence on camera pointing at it, but do not
   demo it here.
4. **Not covered, on purpose:** generating or editing images. That is a separate
   lecture and the boundary is stated in the build script.
5. **UI claims:** there are none in the deck, so nothing needs checking on your
   account. `help.openai.com` and `openai.com` are Cloudflare-blocked from this
   environment, so no consumer-UI page was consulted, and the deck teaches only
   mechanism that is verifiable in the developer docs.
6. **One thing worth saying aloud that is not on a slide:** the API exposes a `detail`
   setting that chooses how hard the model looks at an image. Students on the API
   track will meet it; ChatGPT users cannot set it. It was kept off the slides because
   the sizes behind each level differ per model and change between releases.
