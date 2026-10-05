# Avoiding Bias in a Chat - recording notes

Deck: `avoiding-bias.pptx` (5 slides), built by `build_avoiding_bias.py`.

## Purpose

This short lesson makes learners aware that an answer is shaped by more than the
latest question. Memory, custom instructions, prior chat history and question
framing can all change the context the model receives.

## Speaking notes

1. **Avoiding Bias in a Chat**
   - Bias can enter through the context around a question as well as the model itself.
2. **Four sources can shape the answer**
   - Memory and custom instructions persist useful preferences.
   - Earlier messages and the current wording also steer what feels relevant.
3. **Question framing changes what gets searched for**
   - Compare a request for supporting evidence with one that invites supporting and conflicting evidence.
4. **Awareness gives you a way to check the frame**
   - Inspect the source of context before accepting a confident answer.
5. **Live handoff**
   - Open a fresh chat, rewrite the question and compare what changes.

## Source checked on 2026-09-15

- https://learn.chatgpt.com/docs/personalize

## Review rounds

- Round 1, hostile reviewer: framed memory and instructions as useful context with bias risk, rather than presenting personalisation as inherently bad.
- Round 2, student: the Keynote render made all four sources visible before the question-framing example and kept the demo sequence concrete.

## Added 2026-09-26 (James): ownership words and loaded questions

- **Slide 4, Ownership words invite agreement.** Same plan, two framings. "I wrote this and I think it's strong" gets agreement; "List its three biggest weaknesses" gets critique. Say it plainly: models are tuned to be helpful, which often slides into agreeable (sycophancy).
- **Slide 5, Ask neutral questions.** Loaded vs neutral rewrites. Drop "I" and "my", put the options side by side ("Which is better for <goal>: X or Y?"), ask for the case against.
- Sources: Sharma et al., "Towards Understanding Sycophancy in Language Models" (Anthropic, 2023) https://arxiv.org/abs/2310.13548 ; OpenAI, "Sycophancy in GPT-4o" (2025) https://openai.com/index/sycophancy-in-gpt-4o/

## Round: visual upgrade (2026-09-28)

- Slide 2: the layer stack became a convergence diagram. Four icon cards (memory, custom instructions, chat history, your question) feed "The Model", which feeds "The Answer". One-line caption.
- Slide 3: the two message rows became an evidence-field visual. Pink dots support the plan, grey dots challenge it, and a dashed outline shows where each question sends the search (one side vs both).
- Slide 4: the mocks are unchanged; "Invites Agreement" / "Invites Critique" tags under each, caption cut to one line.
- Slide 5: the loaded/neutral table became paired rows (warning pill, arrow, pink neutral pill).
- Slide 6: the table became four icon cards, each with "useful when" and a pink "Check" question.
- Related shapes are grouped. Icons are Lucide (ISC licence) in `assets/`.
