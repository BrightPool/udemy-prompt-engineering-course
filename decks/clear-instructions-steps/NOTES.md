# Specifying the Steps - recording notes

Deck: `clear-instructions-steps.pptx` (5 slides), built by
`build_clear_instructions_steps.py`.

## Purpose

This lesson explains when to specify an observable workflow because one work
product must feed the next. It avoids treating a private reasoning transcript as
the goal.

## Speaking notes

1. **Specifying the Steps**
   - Ordered steps help when the process contains real dependencies.
2. **Steps describe the work products between start and finish**
   - Each step produces something that can be checked.
3. **The output of one step becomes the next input**
   - Source notes become claims, an evidence map and finally a summary.
4. **A required process becomes easier to inspect**
   - Use a fixed workflow when order and auditability matter.
5. **Live handoff**
   - Compare a final-outcome request with the same task written as a workflow.

## Source checked on 2026-09-15

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5

## Review rounds

- Round 1, hostile reviewer: distinguished required work products from unnecessary micromanagement and added the rigid-process failure mode.
- Round 2, student: the Keynote render confirmed that the dependency chain and its checkpoints read clearly from left to right.

## Updated 2026-09-26 (James): ChatGPT example

- Slide 2 is now a ChatGPT mock of one three-step request: (1) web search three packaging trends, (2) draft an email for every customer in customers.csv, (3) save a summary to the desktop with emails created and what is outstanding.
- Slide 3's flow follows the same run, with a check under each handover (sources listed, every row covered, gaps named).
- Demo note: saving to the desktop needs ChatGPT with file or computer access (desktop app / agent). Without it, ask for the summary as a downloadable file.

## Round: visual upgrade (2026-09-28)

- Slide 2: beside the ChatGPT mock, an icon chain (search, email, monitor) shows the three outputs feeding each other.
- Slide 3: icon stations with an input chip above each (The Web, customers.csv, The Emails) and a check pill below each handover.
- Slide 4: table replaced by two lanes: outcome only (a hidden "?" process) vs specified workflow (numbered stages with a check at each), each with its best use and risk.
- Icons: Lucide (ISC licence) in `assets/`.

## Updated 2026-09-28 (James): cars data activity

- The worked example is now `data/cars.csv` (20 made-up sales rows, no prices). Step 1 enriches each row from our hosted, fixed price page:
  https://understandingdata.com/courses/prompt-engineering-course/data/car-prices/v1/
  (real UK starting prices recorded 28 Sep 2026; v1 never changes, so every run gets the same answer).
- `data/DEMO_PROMPTS.md`: the one-prompt version (on the slide) and a seven-step version for camera. `data/EXPECTED_RESULTS.md` + `data/cars_enriched_answer_key.csv`: the answers to check live.
- Talking point: the Porsche 911 is the most expensive car but nowhere near top for revenue; the Ford Puma leads.
- Regenerate: `data/build_answer_key.py` (answer key) and `data/publish_to_site.py` (site data + CSVs).
