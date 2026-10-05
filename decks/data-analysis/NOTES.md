# Data Analysis — deck notes

Lecture 023, Part 2 · ChatGPT Deep Dive · re-film · 03:27 · video `49725289`.
Deck: `data-analysis.pptx` (12 slides), built by `build_data_analysis.py`.

## The three principles

- **What it is** — Data analysis is the assistant writing a short Python program over the
  file you uploaded and reporting what that program returned, not an impression it formed
  by looking at your numbers.
- **How it works** — Your question and your file go to an isolated sandbox; the assistant
  writes code, runs it, reads the output (errors included, which it repairs and re-runs),
  and explains the result in plain English.
- **Why it matters** — Because the number came out of executed code you can read, it is
  reproducible and checkable; the thing to audit is whether the code asked your question,
  not whether the answer sounds right.

## Research: how it works now

Sources: OpenAI's Code Interpreter tool documentation
(`developers.openai.com/api/docs/guides/tools-code-interpreter`, fetched directly), plus
the OpenAI Help Centre articles *Data analysis with ChatGPT* (8437071), *File uploads FAQ*
(8555545) and *What types of files are supported?* (8983675), reached via search
summaries — **help.openai.com returns 403 to automated fetches**, so the numbers below
are second-hand and should be re-checked on filming day (see `## For James`).

- **The mechanism is unchanged and the original lecture is still correct.** ChatGPT writes
  Python and executes it in a sandboxed container, then narrates the result. Uploading a
  file or asking for a chart is enough to trigger it; there is no mode to switch on.
- **The old names are gone.** "Code Interpreter" and "Advanced Data Analysis" were
  user-facing labels that have since been folded into ChatGPT itself. Worth not saying
  them on camera as though they were a toggle.
- **The sandbox has no internet.** Code cannot make web requests, install from PyPI, or
  reach your machine or live systems. Anything the analysis needs must be uploaded or
  pulled in by the product (a connector) before the code runs — the code itself never
  browses.
- **The container is temporary.** OpenAI's API docs state containers expire after 20
  minutes of inactivity, after which the data is discarded and unrecoverable. Consumer
  ChatGPT behaves similarly: the workings do not live forever.
- **The model does not read all your rows.** It sees column names and a preview;
  everything else arrives as the output of code it ran. This is why it scales past what it
  could read — and why a wrong line of code yields a confident wrong answer.
- **File limits** (move constantly, kept off the slides): 512 MB hard cap per file;
  spreadsheets in practice slow or time out far below that, roughly around the tens of MB;
  rolling upload quotas and per-conversation file counts vary by tier.
- **Charts have moved on since filming.** Static charts still download as PNG/SVG, but bar,
  line, pie and scatter charts now often offer **Switch to interactive chart**, and
  processed data can be exported as CSV/XLSX.
- **Documented failure mode worth naming:** on a large file it may work on only part of the
  data without saying so, and will answer as though it used all of it. Hence the
  row-and-column-count check on slide 10.

## What changed since filming

| In the video | Now |
|---|---|
| Click "Analyzing" to expand the code | The analysis appears in a code box to the **left** of the text (James's note) — demo-half detail, deliberately absent from the deck |
| Download chart / right-click → save image as | Still works, plus interactive charts and CSV/XLSX export of processed data |
| Upload via the + sign or drag-and-drop | Unchanged, and now covered by the separate `adding-files` lecture — this deck assumes the file is already in |
| The KeyError → `print(df.columns)` → retry sequence | Still exactly how it behaves; kept as slide 3, because self-repair is the clearest evidence that real code is running |

## Review rounds

**Round 1 — hostile reviewer.** Six findings, all fixed:
1. Slide 2 ended on a composer bar while the adjacent slide 3 mock ended on `.fit()` —
   two product mocks, two different chromes. Dropped the composer.
2. Slide 6's node read "The model explains the output", which restated the diagram instead
   of making the point. Now "The model explains the output, **not your rows**".
3. Slide 7 listed "Files it writes back out" under *Can reach* — muddled, since a file it
   writes is an output. Now "Charts and files it writes back".
4. Slide 8's row was labelled "Ask it twice", which is wrong: asking again regenerates the
   code and may legitimately differ. Changed to "Run it again".
5. Layout: visuals started at 1.54" (table) and 1.60" (cards) against 1.52" everywhere
   else. All aligned to 1.52", captions moved with them.
6. Layout: the captions on slides 6 and 10 were top-aligned against visuals two inches
   taller, leaving them stranded at the top-right. Both re-centred against their visual.

**Round 2 — the student.** Four findings, all fixed:
1. "sandbox" appeared on slide 5 and was only defined on slide 7. Slide 5's caption now
   defines it at first use — and slide 7's copy was rewritten so the definition is not
   repeated.
2. "nulls" on slide 10 is developer jargon for a no-code audience → "the blanks".
3. "Pattern-matching on similar data" on slide 4 → "Recalling similar data it has seen".
4. Titles read top to bottom as a complete story; nothing else to change. Lint clean, no
   text under 12pt on white, no screenshot, menu path, price or version number anywhere.

## For James

1. **The code-box-on-the-left note is demo-half only.** Nothing in the deck says where
   anything sits on screen, by design. Show the panel live and say it out loud.
2. **Say the current limits aloud rather than putting them on a slide.** The ones to check
   on filming day: 512 MB per file, spreadsheets getting slow well below that, and the
   upload quota on your tier. I could not read help.openai.com directly (it 403s automated
   fetches), so treat those figures as unverified until you look.
3. **The bar-chart section is the biggest thing that has moved.** Consider demoing
   **Switch to interactive chart** and the CSV/XLSX export — neither existed at filming.
4. **`students.csv` has a "grade level" column**, and slide 9's first failure mode is
   "'grade' taken as a score when it is a year group". If you want the deck and the demo to
   rhyme, ask a deliberately ambiguous grade question live and show it guessing.
5. **Check the overlap with `adding-files` (54676155).** This deck starts after the file is
   uploaded; if the demo re-teaches the + sign, one of the two lectures is doing it twice.
6. **Do not contradict the "no internet" line on camera.** If you pull a file from a
   connector during the demo, the product fetched it — the sandbox code still cannot browse.
