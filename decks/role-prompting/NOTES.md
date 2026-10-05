# Role Prompting - recording notes

Deck: `role-prompting.pptx` (5 slides), built by `build_role_prompting.py`. Re-film: the
old video used an outdated ChatGPT UI. The principle (a persona shapes style and tone) is
kept; the new deck adds an honest limit on what a role can do.

## Purpose

Role prompting tells the model who it is answering as. It reliably changes tone, focus
and framing. It does not add knowledge, and on average it does not improve factual
accuracy.

## Speaking notes

1. **Role Prompting**
   - Telling the model who it is changes the tone, focus and framing of its answer.
2. **A role sets the perspective of the answer**
   - Same headline, two requests. Without a role: a polite, generic review. With a
     conversion copywriter role: a blunt verdict and a rewrite led by the outcome.
3. **How it works - a role shifts emphasis, not knowledge**
   - Changes vocabulary, priorities, what a good answer looks like, the questions asked
     back. Does not change what the model knows or whether facts are right.
   - Cite the study: 162 roles, 2,410 factual questions, no average accuracy gain.
4. **Why it matters - specific roles beat vague ones**
   - "You are an expert" barely changes anything. A specific role plus task, audience
     and constraints does. Failure mode: a convincing voice can hide a wrong fact.
   - Optional aside: in the API, the role usually goes in the instructions (system
     message), not the user turn.
5. **Live handoff**
   - In ChatGPT: ask with no role, add a specific role with audience and goal, compare.

## Sources checked on 2026-09-26

- Zheng et al., "When 'A Helpful Assistant' Is Not Really Helpful: Personas in System
  Prompts Do Not Improve Performances of Large Language Models", Findings of EMNLP 2024:
  https://arxiv.org/abs/2311.10054
- Old lecture analysis: scripts/udemy-sync/out/analysis_video_only/49729433.json

## Review rounds

- Round 1, hostile reviewer: the role example also adds context (B2B launch), so the
  caption now says "same headline", not "same question". Shortened the slide 4 title,
  replaced a meaningless "Nothing else" cell, matched the two mock heights.
- Round 2, student and layout: the Keynote render showed the middle table column
  running into the third; widened it.

## For James

- The "With a role" example deliberately bundles role + audience, which is the advice
  on slide 4. If you want a pure role-only comparison for the demo, drop "for a B2B launch".

- Round 3, James: slide 2 is now a pure role-only comparison. One request, three windows: act as a copywriter, a senior engineer, a product manager. The table example uses "Act as" phrasing too.

## Round: visual upgrade (2026-09-28)

- Slide 2: role badges (copywriter, senior engineer, product manager) above the three "Act as" windows; user line shortened to "Review: Friday login launch."; one-line caption.
- Slide 3: compare panels replaced by icon rows (what a role changes vs doesn't) and a stat card for the EMNLP 2024 study (162 roles, 2,410 questions, no average accuracy gain).
- Slide 4: table replaced by a vague-to-specific spectrum with three example roles, plus a failure-mode callout.
- Icons: Lucide (ISC licence) in `assets/`.
