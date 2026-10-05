"""
Analyze drift between Udemy course videos and the matched notebooks in this repo.

Reads:  scripts/udemy-sync/out/notebook_matches.json
        scripts/udemy-sync/videos/.../*.mp4
        the matched .ipynb files in this repo
Writes: scripts/udemy-sync/out/analysis/<lecture_id>.json   (one per lecture)

Resume-safe: skips any lecture whose result JSON already exists.

Run:
  uv run --with google-genai --with pydantic --with python-dotenv \
    python scripts/udemy-sync/analyze_drift.py             # all matched lectures
  uv run ... python scripts/udemy-sync/analyze_drift.py --limit 3
  uv run ... python scripts/udemy-sync/analyze_drift.py --lecture 44009372
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Literal

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# --------------------------------------------------------------------------- paths
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
OUT_DIR = HERE / "out"
ANALYSIS_DIR = OUT_DIR / "analysis"
VIDEO_ONLY_DIR = OUT_DIR / "analysis_video_only"
VIDEOS_DIR = HERE / "videos"
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_ONLY_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-flash-latest"  # Google-maintained alias for the current stable Flash
CONCURRENCY = 5
FPS = 0.5  # static lecture content -> low FPS

# --------------------------------------------------------------------------- schema
DriftCategory = Literal[
    "vector_store_swap",
    "api_surface_change",
    "library_swap",
    "method_call_change",
    "model_change",
    "code_structure_change",
    "content_missing_from_video",
    "content_missing_from_notebook",
]

PacingSpeed = Literal["slow", "medium", "fast"]
RecommendedAction = Literal["rerecord_video", "none"]


class DriftSegment(BaseModel):
    start_timestamp: str = Field(description="MM:SS")
    end_timestamp: str = Field(description="MM:SS")
    description: str


class SpecificDiff(BaseModel):
    category: DriftCategory
    video_excerpt: str = Field(description="Quote with MM:SS timestamp")
    notebook_excerpt: str = Field(description="Quote with cell index, e.g. 'cell 4: ...'")
    explanation: str


class VideoQuality(BaseModel):
    talking_too_quickly: bool
    over_talking_same_point: bool
    no_exercises: bool
    monotonous_voice: bool
    pacing_speed: PacingSpeed
    jumpy_video: bool


class DriftAnalysis(BaseModel):
    video_name: str
    drift_score: int = Field(ge=1, le=10, description="1=identical, 10=different topic")
    drift_reason: str = Field(description="Concise narrative for grouping across lectures")
    drift_categories: list[DriftCategory]
    drift_segments: list[DriftSegment] = Field(max_length=8)
    student_blocking: bool
    deprecated_topic: bool
    specific_diffs: list[SpecificDiff] = Field(max_length=5)
    recommended_action: RecommendedAction
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str = Field(description="Two sentences for the human reviewer")
    video_quality: VideoQuality
    estimated_rerecord_minutes: int = Field(ge=0)
    rerecord_scope: Literal["full_lecture", "code_demo_only", "intro_outro_only", "none"]
    prerequisite_changes: list[str] = Field(max_length=5)
    talking_points_to_add: list[str] = Field(max_length=8)


class VideoOnlyAnalysis(BaseModel):
    """Lectures with no matched notebook — drift fields N/A; capture everything else."""

    video_name: str
    video_summary: str = Field(description="2-3 sentences on what this lecture teaches")
    deprecated_topic: bool = Field(
        description="True if the topic is no longer relevant in 2026 and should be removed"
    )
    deprecated_reason: str = Field(
        description="If deprecated_topic, one sentence why; else empty string"
    )
    video_quality: VideoQuality
    estimated_rerecord_minutes: int = Field(ge=0)
    talking_points_to_add: list[str] = Field(max_length=8)
    summary: str = Field(description="Two sentences for the human reviewer")
    confidence: float = Field(ge=0.0, le=1.0)


# --------------------------------------------------------------------------- prompt
PROMPT_TEMPLATE = """You are auditing a recorded Udemy lecture video against the Jupyter notebook \
that the student is supposed to follow alongside it.

# Inputs
- The video (attached).
- The notebook(s) text (below). Output cells have been stripped — you see only \
markdown + code cells.

# Your job
Decide how much DRIFT there is between what the video teaches and what the \
notebook contains. The notebook is the source of truth — the question is whether \
the video is still accurate enough that a student following the current notebook \
would have a coherent learning experience.

# Scoring rules (drift_score, 1-10)
- 1-2:  Code is identical in shape, libraries, methods, and concepts. Only \
        cosmetic differences allowed (variable names, model strings).
- 3-4:  Same libraries, same methods, but minor differences (e.g. model string \
        gpt-4 -> gpt-4o, slightly reordered code).
- 5-6:  One non-trivial method-call change OR one notable concept the video \
        explains that the notebook no longer has (or vice versa).
- 7-8:  A core method/API surface in the video has been replaced in the notebook \
        (e.g. chat.completions -> responses), OR a library has been swapped \
        (e.g. langchain -> langgraph). A student would be confused.
- 9-10: Vector store / framework swap (e.g. video uses Elasticsearch, notebook \
        uses Chroma), OR the topic itself is deprecated, OR the notebook \
        teaches a fundamentally different approach. Re-record is mandatory.

Important weighting:
- Model name swaps (e.g. gpt-4 -> gpt-4o, claude-3 -> claude-3.5) add at MOST \
  +1 to drift_score. Do not over-penalize these.
- Method-call changes, API surface changes, library swaps, and vector-store \
  swaps each add +3 or more.
- A topic that is fully deprecated (e.g. LangChain Indexing API) sets \
  deprecated_topic=true and drift_score=9 or 10 regardless of code similarity.

# recommended_action
Set "rerecord_video" if ANY of:
  - drift_score >= 6
  - student_blocking is true
  - deprecated_topic is true
Otherwise "none".

# video_quality
Independent assessment of presentation quality. These DO NOT affect \
recommended_action. Assess based on the audio and visuals of the video alone.

# Output
Respond with the structured JSON only — no prose outside the schema.

# Lecture context
Lecture title: {lecture_title}
Section: {section}
Notebook(s) attached: {notebook_paths}

# Notebook content (output cells stripped)
{notebook_text}
"""


VIDEO_ONLY_PROMPT_TEMPLATE = """You are reviewing a recorded Udemy lecture video. There is NO \
matching Jupyter notebook for this lecture in the course repo, so do not look for code drift.

# Your job
Capture:
- A short summary of what the lecture teaches.
- Whether the topic is deprecated (should the lecture be removed entirely from the 2026 course?).
- Presentation quality signals (pacing, voice, edits).
- Talking points the instructor missed that would improve a re-record.
- A rough re-record duration if quality issues warrant one.

# deprecated_topic
Set true if the lecture covers something that is no longer relevant in 2026 \
(e.g. an API that has been removed, a deprecated tool, or content that has been \
superseded by a different approach). Otherwise false.

# Output
Respond with the structured JSON only — no prose outside the schema.

# Lecture context
Lecture title: {lecture_title}
Section: {section}
"""


# --------------------------------------------------------------------------- helpers
def strip_notebook(path: Path) -> str:
    """Return a compact text rendering of a notebook with output cells removed."""
    nb = json.loads(path.read_text())
    parts: list[str] = [f"=== NOTEBOOK: {path.relative_to(REPO_ROOT)} ===\n"]
    for i, cell in enumerate(nb.get("cells", []), start=1):
        ctype = cell.get("cell_type", "")
        src = cell.get("source", [])
        if isinstance(src, list):
            src = "".join(src)
        src = src.rstrip()
        if not src:
            continue
        parts.append(f"--- cell {i} ({ctype}) ---\n{src}\n")
    return "\n".join(parts)


def find_video_for_lecture(lecture_id: int) -> Path | None:
    matches = list(VIDEOS_DIR.glob(f"*/*_{lecture_id}_*.mp4"))
    return matches[0] if matches else None


def wait_for_active(client: genai.Client, file, *, timeout_s: float = 600.0):
    """Poll until uploaded file is ACTIVE (ready for inference)."""
    start = time.time()
    while file.state.name == "PROCESSING":
        if time.time() - start > timeout_s:
            raise TimeoutError(f"File {file.name} stuck PROCESSING after {timeout_s}s")
        time.sleep(3)
        file = client.files.get(name=file.name)
    if file.state.name != "ACTIVE":
        raise RuntimeError(f"File {file.name} ended in state {file.state.name}")
    return file


def _call_with_video(
    client: genai.Client, video_path: Path, prompt: str, schema: type[BaseModel]
):
    """Upload the video, call Gemini with the schema, always clean up."""
    uploaded = client.files.upload(file=str(video_path))
    try:
        uploaded = wait_for_active(client, uploaded)
        video_part = types.Part(
            file_data=types.FileData(
                file_uri=uploaded.uri, mime_type=uploaded.mime_type
            ),
            video_metadata=types.VideoMetadata(fps=FPS),
        )
        return client.models.generate_content(
            model=MODEL,
            contents=[video_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.2,
            ),
        )
    finally:
        try:
            client.files.delete(name=uploaded.name)
        except Exception as e:
            print(f"  WARN: failed to delete {uploaded.name}: {e}", file=sys.stderr)


def analyze_one(client: genai.Client, lecture: dict) -> dict:
    """Drift analysis: video + matched notebook(s)."""
    lecture_id = lecture["lecture_id"]
    video_path = find_video_for_lecture(lecture_id)
    if not video_path:
        raise FileNotFoundError(f"No video found for lecture {lecture_id}")

    nb_paths: list[Path] = []
    for m in lecture["notebook_matches"]:
        if not m.get("repo_path"):
            continue
        p = REPO_ROOT / m["repo_path"]
        if p.exists():
            nb_paths.append(p)
    if not nb_paths:
        raise FileNotFoundError(f"No matched notebook on disk for lecture {lecture_id}")

    notebook_text = "\n\n".join(strip_notebook(p) for p in nb_paths)
    prompt = PROMPT_TEMPLATE.format(
        lecture_title=lecture["lecture_title"],
        section=lecture.get("section") or "—",
        notebook_paths=", ".join(str(p.relative_to(REPO_ROOT)) for p in nb_paths),
        notebook_text=notebook_text,
    )
    response = _call_with_video(client, video_path, prompt, DriftAnalysis)
    parsed = response.parsed
    if parsed is None:
        return {"_raw": response.text, "_error": "parse_failed"}
    result = parsed.model_dump()
    result["_meta"] = {
        "lecture_id": lecture_id,
        "lecture_title": lecture["lecture_title"],
        "section": lecture.get("section"),
        "learn_url": lecture.get("learn_url"),
        "video_path": str(video_path.relative_to(REPO_ROOT)),
        "notebook_paths": [str(p.relative_to(REPO_ROOT)) for p in nb_paths],
        "model": MODEL,
        "fps": FPS,
        "mode": "drift",
    }
    return result


def analyze_one_video_only(client: genai.Client, lecture: dict) -> dict:
    """Video-only analysis: no notebook input, slimmer schema."""
    lecture_id = lecture["lecture_id"]
    video_path = find_video_for_lecture(lecture_id)
    if not video_path:
        raise FileNotFoundError(f"No video found for lecture {lecture_id}")

    prompt = VIDEO_ONLY_PROMPT_TEMPLATE.format(
        lecture_title=lecture["lecture_title"],
        section=lecture.get("section") or "—",
    )
    response = _call_with_video(client, video_path, prompt, VideoOnlyAnalysis)
    parsed = response.parsed
    if parsed is None:
        return {"_raw": response.text, "_error": "parse_failed"}
    result = parsed.model_dump()
    result["_meta"] = {
        "lecture_id": lecture_id,
        "lecture_title": lecture["lecture_title"],
        "section": lecture.get("section"),
        "learn_url": lecture.get("learn_url"),
        "video_path": str(video_path.relative_to(REPO_ROOT)),
        "notebook_paths": [],
        "model": MODEL,
        "fps": FPS,
        "mode": "video_only",
    }
    return result


# --------------------------------------------------------------------------- driver
def _build_drift_plan(args) -> list[dict]:
    matches = json.loads((OUT_DIR / "notebook_matches.json").read_text())
    clean = {"exact_path", "basename_unique"}
    plan = []
    for lec in matches:
        good = [
            m for m in lec["notebook_matches"]
            if m.get("repo_path") and (args.include_ambiguous or m["confidence"] in clean)
        ]
        if good:
            lec["notebook_matches"] = good
            plan.append(lec)
    return plan


def _build_video_only_plan() -> list[dict]:
    """Every lecture in the curriculum that is NOT in the cleanly-matched drift plan."""
    curriculum = json.loads((OUT_DIR / "curriculum_resolved.json").read_text())
    matches = json.loads((OUT_DIR / "notebook_matches.json").read_text())
    clean = {"exact_path", "basename_unique"}
    matched_ids = {
        lec["lecture_id"]
        for lec in matches
        if any(
            m.get("repo_path") and m["confidence"] in clean
            for m in lec["notebook_matches"]
        )
    }
    plan = []
    for lec in curriculum["lectures"]:
        if lec["id"] in matched_ids:
            continue
        if not lec.get("video"):
            continue  # quiz/practice/etc. - no video to analyze
        plan.append({
            "lecture_id": lec["id"],
            "lecture_title": lec["title"],
            "section": lec.get("section", {}).get("title") if lec.get("section") else None,
            "learn_url": lec.get("learn_url"),
        })
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["drift", "video_only"], default="drift")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--lecture", type=int, default=None, help="Run only one lecture id")
    ap.add_argument("--include-ambiguous", action="store_true",
                    help="(drift mode) include ambiguous-basename matches")
    ap.add_argument("--force", action="store_true", help="Re-run even if JSON exists")
    args = ap.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY not set (check .env)")

    client = genai.Client()

    if args.mode == "drift":
        plan = _build_drift_plan(args)
        out_dir = ANALYSIS_DIR
        worker_fn = analyze_one
        info_label = "drift"
    else:
        plan = _build_video_only_plan()
        out_dir = VIDEO_ONLY_DIR
        worker_fn = analyze_one_video_only
        info_label = "deprecated"

    if args.lecture:
        plan = [l for l in plan if l["lecture_id"] == args.lecture]
    if args.limit:
        plan = plan[: args.limit]

    print(f"Plan: {len(plan)} lectures (mode={args.mode}, concurrency={CONCURRENCY}, fps={FPS})")

    def runner(lec):
        out_path = out_dir / f"{lec['lecture_id']}.json"
        if out_path.exists() and not args.force:
            return ("SKIP", lec, "already_done")
        # Skip cleanly if the video isn't on disk (e.g. Udemy hasn't transcoded
        # the .mov yet). Don't write a placeholder JSON so a future re-run will
        # pick it up if the video appears.
        if not find_video_for_lecture(lec["lecture_id"]):
            return ("SKIP", lec, "no_video")
        try:
            result = worker_fn(client, lec)
            out_path.write_text(json.dumps(result, indent=2))
            short = result.get("drift_score") if args.mode == "drift" else result.get("deprecated_topic")
            return ("DONE", lec, short)
        except Exception as e:
            traceback.print_exc()
            return ("FAIL", lec, str(e))

    done = skipped = failed = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = [pool.submit(runner, lec) for lec in plan]
        for i, fut in enumerate(as_completed(futures), 1):
            status, lec, info = fut.result()
            tag = {"DONE": "DONE ", "SKIP": "SKIP ", "FAIL": "FAIL "}[status]
            if status == "DONE":
                done += 1
                print(f"{tag} [{i}/{len(plan)}] {lec['lecture_id']} {lec['lecture_title']!r:60s} {info_label}={info}")
            elif status == "SKIP":
                skipped += 1
                print(f"{tag} [{i}/{len(plan)}] {lec['lecture_id']} {lec['lecture_title']!r:60s} ({info})")
            else:
                failed += 1
                print(f"{tag} [{i}/{len(plan)}] {lec['lecture_id']} {lec['lecture_title']!r:60s} -> {info}")

    print(f"\nFinished. done={done} skipped={skipped} failed={failed} total={len(plan)}")


if __name__ == "__main__":
    main()
