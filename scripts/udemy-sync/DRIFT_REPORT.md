# Course Drift Report

Generated 2026-04-27 from a Gemini-Flash-powered audit of the Udemy course
**The Complete Prompt Engineering for AI Bootcamp (2026)**.

This report focuses on **drift between recorded videos and the matched
notebooks in this repo** — the highest-impact problem you asked us to solve
first. Quality and deprecated-topic findings live in `FINDINGS.md` and the
CSVs; they are not the focus here.

---

## TL;DR

- **209 videos** (14 GB) downloaded and analysed end-to-end.
- **85 lectures** had a notebook in this repo that we could compare against (drift mode).
- **34 of 85** are recommended for re-recording (`drift_score ≥ 6` or `student_blocking=true`).
- The work is concentrated: **20 of those 34** drift for the same single root cause — the OpenAI `chat.completions` → `responses` API migration. One scripted re-record campaign clears most of the queue.
- Estimated total finished-video re-record time: **~5 hours** (mostly `code_demo_only` scope, not full lectures).

---

## Where everything lives

### Videos (14 GB, gitignored)

```
scripts/udemy-sync/videos/<sectionIdx>_<section-slug>/<lectureIdx>_<lectureId>_<lecture-slug>.mp4
```

Section folders (21 total):

```
scripts/udemy-sync/videos/
├── 01_introduction/
├── 02_five-principles-of-prompting/
├── 03_how-does-ai-work/
├── 04_deep-dive-on-chatgpt/
├── 05_standard-text-model-practices/
├── 06_openai-features-and-functionality-coding/
├── 07_retrieval-embeddings-and-vector-databases-coding/
├── 08_building-ai-agents-coding/
├── 09_advanced-text-model-techniques-coding/
├── 10_deep-dive-on-langchain-coding/
├── 11_deep-dive-on-langgraph-coding/
├── 12_ai-text-model-projects/
├── 13_deep-dive-on-midjourney-v6/
├── 14_standard-image-model-practices/
├── 15_advanced-image-generation-techniques/
├── 16_ai-image-model-projects/
├── 17_prompt-optimization-and-evals/
├── 18_agent-architectures-coding/
├── 20_deep-dive-on-dall-e-3/
├── 21_deep-dive-on-other-ai-models/
└── 22_conclusion/
```

Filename template:

```
108_42637624_langchain-vector-databases-the-indexing-api-coding.mp4
│   │        └── lecture title (slugified)
│   └── lecture id (use to look up the analysis JSON)
└── lecture index within the course
```

### Analysis output

| Path | What |
|---|---|
| `scripts/udemy-sync/out/analysis/<lecture_id>.json` | Per-lecture **drift** record (85 files) |
| `scripts/udemy-sync/out/analysis_video_only/<lecture_id>.json` | Per-lecture **video-only** record for the 124 lectures with no matched notebook |
| `scripts/udemy-sync/out/analysis_flat.csv` | All 209 lectures, 33 columns, sortable |
| `scripts/udemy-sync/out/analysis.csv` | Same rows, full JSON in one cell |
| `scripts/udemy-sync/out/notebook_matches.json` / `.md` | Which Udemy resource maps to which `.ipynb` |
| `scripts/udemy-sync/out/curriculum_resolved.json` | Source-of-truth course tree (sections, learn URLs, signed mp4 URLs) |

### Pipeline scripts (re-runnable)

| Script | Purpose |
|---|---|
| `resolve_resources.mjs` | Pull curriculum + resolve every external resource URL |
| `download_videos.mjs` | Refresh signed URLs and download all 720p mp4s, 10 concurrent |
| `match_notebooks.mjs` | Map Colab/Github resources to notebooks in this repo |
| `analyze_drift.py` | Send video + notebook to Gemini, score drift |
| `emit_csvs.py` | Roll up all per-lecture JSONs into the two CSVs |
| `AGENT_PROMPT.md` | Handoff doc for the Udemy internal API |
| `FINDINGS.md` | Repo-side issues found while matching (e.g. `dsypy.ipynb` typo) |

To re-run drift detection from scratch (after a notebook or video changes):

```bash
# inside a logged-in playwright-cli `udemy` session
node scripts/udemy-sync/resolve_resources.mjs
node scripts/udemy-sync/match_notebooks.mjs
node scripts/udemy-sync/download_videos.mjs

set -a && source .env && set +a && \
  uv run --with google-genai --with pydantic --with python-dotenv \
  python scripts/udemy-sync/analyze_drift.py            # 86 drift candidates
uv run --with python-dotenv python scripts/udemy-sync/emit_csvs.py
```

The drift script is **idempotent** — only successful runs leave a JSON behind,
so a re-run picks up just the failures and any newly added lectures.

---

## How drift is scored

`gemini-flash-latest` watches the video at 0.5 fps + reads the notebook
(output cells stripped) and returns a structured JSON per lecture. The schema
that matters for drift:

| Field | Meaning |
|---|---|
| `drift_score` | 1 = identical, 10 = different topic |
| `drift_reason` | One sentence narrative — used to cluster across lectures |
| `drift_categories` | Tags like `api_surface_change`, `vector_store_swap`, `library_swap` |
| `drift_segments` | `[{start_timestamp, end_timestamp, description}]` — exact moments in the video where drift happens |
| `specific_diffs` | Up to 5 paired excerpts: video line + notebook cell, with explanation |
| `student_blocking` | True if a student following the notebook would hit an error not shown in the video |
| `recommended_action` | `rerecord_video` if `drift_score ≥ 6` OR `student_blocking` OR `deprecated_topic`; else `none` |
| `rerecord_scope` | `full_lecture` / `code_demo_only` / `intro_outro_only` / `none` |
| `estimated_rerecord_minutes` | Rough finished-video minutes for the re-record |
| `prerequisite_changes` | Things to fix in the repo *before* re-recording (e.g. install a package) |
| `talking_points_to_add` | Concepts in the notebook the current video doesn't cover — script seeds for the new take |

Weighting in the prompt: **model-name swaps add ≤ 1 point; method/library/vector-store swaps add ≥ 3 each.** This is why most major-drift lectures land on 7–8 rather than 9–10 — the model rarely flags the entire topic as gone, only specific code paths.

---

## Drift score distribution (85 lectures)

| Score | Count | Meaning |
|---|---|---|
| 1 | 25 | Identical — only cosmetic differences |
| 2 | 14 | Trivial differences (variable names, model strings) |
| 3 | 7 | Minor reordering, same APIs |
| 4 | 2 | One small method tweak |
| 5 | 3 | One non-trivial divergence |
| 6 | 2 | Notable divergence — student would notice |
| **7** | **16** | **Library/method swap, student confusion likely** |
| **8** | **16** | **Half the demo no longer matches the notebook** |
| 9 | 0 | (model rarely awarded — saved for "topic is gone") |
| 10 | 0 | |

The line is at **6**: 32 lectures sit above it, plus 2 more flagged on `student_blocking` alone, totalling **34 re-records**.

---

## Re-record queue, grouped by root cause

### Cluster C — OpenAI `chat.completions` → `responses` (20 lectures, ~3 hr)

The dominant pattern. Notebooks were migrated per `docs/chat-completions-migration.json`; the videos still teach the old API. One scripted re-record campaign clears all 20.

| Score | Scope | Lecture | Est. min |
|---|---|---|---|
| 8 | full_lecture | Agents - Coding | 12 |
| 8 | code_demo_only | Few Shot Learning - Coding | 10 |
| 8 | code_demo_only | Personas of Thought - Coding | 12 |
| 8 | code_demo_only | Claim Detection - Coding | 12 |
| 8 | code_demo_only | Role Prompting - Coding | 12 |
| 8 | code_demo_only | Prompt Chaining - Coding | 7 |
| 8 | code_demo_only | Prompt Optimization - Coding | 9 |
| 8 | code_demo_only | Parallelization of requests with Async OpenAI | 10 |
| 8 | code_demo_only | Qualitative Analysis - Coding | 7 |
| 8 | full_lecture | Emotion Prompting - Coding | 5 |
| 8 | full_lecture | Evaluator Optimizer - Coding | 16 |
| 8 | code_demo_only | Memetic Analysis with GPT-V | 6 |
| 8 | code_demo_only | LLM Orchestrators - Coding | 6 |
| 7 | code_demo_only | Routing - Coding | 7 |
| 7 | code_demo_only | Reason and Act (ReAct) - Coding | 8 |
| 7 | full_lecture | Rate Limits, Retrying and How to Overcome These Problems | 5 |
| 7 | full_lecture | Prompt Optimization: Advanced - Coding | 11 |
| 7 | code_demo_only | Chain of Thought - Coding | 8 |
| 7 | full_lecture | Prompt Optimization: 5 Principles of Prompting - Coding | 10 |
| 7 | code_demo_only | Parallelization - Coding | 5 |

### Cluster E — LangChain → newer LangGraph / LangChain v0.3 patterns (9 lectures, ~76 min)

Notebook code restructured around updated LangChain/LangGraph idioms. Includes the **Tool Usage and Persistence** lecture flagged in your Q&A.

| Score | Scope | Lecture | Est. min |
|---|---|---|---|
| 7 | code_demo_only | Customizing State in LangGraph - Coding | 10 |
| 7 | code_demo_only | Summarizing Large Amounts of Text - Coding | 6 |
| 7 | full_lecture | Summarizing An Entire Book - Coding | 8 |
| 7 | code_demo_only | Human In The Loop - Coding | 6 |
| 7 | code_demo_only | Eval metrics with DSPy - Coding | 10 |
| 7 | code_demo_only | Time Travel - Coding | 7 |
| 7 | full_lecture | Tool Usage and Persistence - Coding | 16 |
| 6 | full_lecture | Chat Models - Coding | 7 |
| 6 | full_lecture | Manually Updating The State - Coding | 6 |

### Cluster B — Vector store / RAG plumbing change (1 lecture, ~10 min)

| Score | Scope | Lecture | Est. min |
|---|---|---|---|
| 8 | code_demo_only | LangChain Vector Databases + The Indexing API - Coding | 10 |

This is the Q&A complaint — video uses Elasticsearch + SQLRecordManager, notebook uses Chroma + InMemoryRecordManager. The first half (FAISS) is fine — only the indexing section needs re-doing. `prerequisite_changes` notes to install `langchain-chroma` first.

### Cluster D — LangChain → LangGraph migration (1 lecture, ~15 min)

| Score | Scope | Lecture | Est. min |
|---|---|---|---|
| 8 | full_lecture | LangChain Agents & Tools - Coding | 15 |

Video teaches manual agent construction with LCEL + AgentExecutor; notebook uses the LangGraph agent primitives.

### Cluster F — Other API/method surface changes (2 lectures, ~18 min)

| Score | Scope | Lecture | Est. min |
|---|---|---|---|
| 8 | full_lecture | Draw Image Mask with Gradio | 10 |
| 7 | code_demo_only | Transcribing audio from a Youtube Video - Coding | 8 |

### Cluster A — Deprecated topic (1 lecture, ~6 min)

| Score | Scope | Lecture | Est. min |
|---|---|---|---|
| 7 | code_demo_only | Tagging Documents - Coding | 6 |

---

## Recommended sequencing

1. **Fix the prerequisites first** (`FINDINGS.md`):
   - Rename `prompt_optimization_and_evals/dsypy.ipynb` → `dspy.ipynb`
   - Resolve the DreamBooth case mismatches (or rename repo files to one-word `dreambooth`)
   - Decide what backs `chatgpt_chunking.ipynb` and the generic-named `notebook.ipynb`
2. **Knock out the Q&A complaints** (you have students actively asking):
   - LangChain Vector Databases + The Indexing API
   - Tool Usage and Persistence
3. **Run cluster C as one campaign** with a single template script for the API migration. ~20 short demos in roughly two studio sessions.
4. **Run cluster E as a second campaign** for the LangGraph/LangChain v0.3 patterns.
5. **Mop up clusters B/D/F/A** individually.

Total finished-video re-record budget: **~5 hours**.

---

## How to dig into any single lecture

For lecture id `<id>`:

1. Watch the video locally:
   `scripts/udemy-sync/videos/<sectionFolder>/*_<id>_*.mp4`
2. Read what Gemini found:
   `scripts/udemy-sync/out/analysis/<id>.json`
   - `drift_segments` tells you exact `MM:SS` ranges to focus on
   - `specific_diffs` pairs each video excerpt with its notebook cell counterpart
   - `talking_points_to_add` is your re-record script seed
3. Open the matched notebook (path is in `_meta.notebook_paths[0]`).
4. Open the live student page (also in `_meta.learn_url`) if you want to see what the student sees.
