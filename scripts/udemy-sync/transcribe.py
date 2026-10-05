#!/usr/bin/env python3
"""
transcribe.py - word-level transcripts for the course videos.

Local Whisper (faster-whisper). No API, no cost, re-runnable. Word timestamps are
the point: most of the re-film notes are time-anchored ("update 3:33-4:56",
"at 0:33 secs"), so we need to jump to a moment and read what was actually said.

    # the 19 lectures in the re-film goal
    uv run --with faster-whisper python scripts/udemy-sync/transcribe.py run --goal

    # everything (background job; ~0.55x realtime)
    uv run --with faster-whisper python scripts/udemy-sync/transcribe.py run --all

    # one lecture, or anything matching a substring
    uv run --with faster-whisper python scripts/udemy-sync/transcribe.py run --match memory

    # read back what was said around a timestamp (no model needed)
    python scripts/udemy-sync/transcribe.py show 48151545 --at 1:12 --window 40

Outputs, per video, under transcripts/<section>/:
    <name>.json   segments + per-word timings + metadata
    <name>.srt    subtitles
    <name>.txt    plain prose

Existing transcripts are skipped unless --force, so re-runs are cheap.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIDEOS = ROOT / "videos"
OUT = ROOT / "transcripts"

# Proper nouns Whisper otherwise mangles ("ChatGPT" -> "chat TPT").
VOCAB = (
    "ChatGPT, OpenAI, GPT-5, GPT-4o, o3, Anthropic, Claude, Gemini, Grok, xAI, "
    "Midjourney, DALL-E, Stable Diffusion, Veo, LangChain, LangGraph, Pinecone, "
    "LLM, tokens, tokenizer, tokenization, context window, embeddings, RAG, MCP, "
    "prompt engineering, few-shot, chain of thought, temperature, hallucination, "
    "custom instructions, canvas, artefacts, agent mode, deep research, "
    "scheduled tasks, connectors, plugins, skills, evals."
)

# Lectures in the re-film goal (see ~/Desktop/GOAL-course-refilm.md).
GOAL_IDS = [
    "37093534",  # What are Tokens?
    "37093540",  # AI Hallucinations
    "37093452",  # What is ChatGPT?
    "48150231",  # Chat models vs reasoning models
    "46777369",  # Web Search
    "49251317",  # Deep Research
    "54676155",  # Adding Files
    "49725289",  # Data Analysis
    "40611478",  # Analyzing Images (vision)
    "42691388",  # Vision prompting guide (companion)
    "46579771",  # Canvas -> Artefacts
    "48151545",  # Memory
    "54676053",  # Projects
    "39480068",  # Custom Instructions
    "39228730",  # Shortcuts
    "48151369",  # Scheduled Tasks
    "51999139",  # Agent Mode
    "44003766",  # Desktop Application
    "42183042",  # Prompt Testing in GSheets (Mike)
]


def videos() -> list[Path]:
    return sorted(VIDEOS.glob("*/*.mp4"))


def lecture_id(p: Path) -> str:
    parts = p.stem.split("_")
    return parts[1] if len(parts) > 1 else p.stem


def out_paths(p: Path) -> tuple[Path, Path, Path]:
    d = OUT / p.parent.name
    return d / f"{p.stem}.json", d / f"{p.stem}.srt", d / f"{p.stem}.txt"


def ts(seconds: float, comma: bool = True) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    sep = "," if comma else "."
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def parse_at(v: str) -> float:
    """'3:33' or '1:02:04' or '213' -> seconds."""
    bits = [float(x) for x in str(v).split(":")]
    out = 0.0
    for b in bits:
        out = out * 60 + b
    return out


def extract_audio(video: Path, wav: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)],
        check=True,
    )


def write_outputs(video: Path, segments: list[dict], meta: dict) -> Path:
    js, srt, txt = out_paths(video)
    js.parent.mkdir(parents=True, exist_ok=True)

    js.write_text(json.dumps({**meta, "segments": segments}, indent=1))

    lines = []
    for i, s in enumerate(segments, 1):
        lines += [str(i),
                  f"{ts(s['start'])} --> {ts(s['end'])}",
                  s["text"].strip(), ""]
    srt.write_text("\n".join(lines))

    txt.write_text("\n".join(
        re.sub(r"\s+", " ", s["text"]).strip() for s in segments) + "\n")
    return js


def cmd_run(args) -> int:
    from faster_whisper import WhisperModel

    picked = videos()
    if args.goal:
        picked = [p for p in picked if lecture_id(p) in set(GOAL_IDS)]
    if args.id:
        picked = [p for p in picked if lecture_id(p) in set(args.id)]
    if args.match:
        picked = [p for p in picked if args.match.lower() in p.stem.lower()]
    if args.section:
        picked = [p for p in picked if p.parent.name.startswith(args.section)]
    if not picked:
        print("nothing matched", file=sys.stderr)
        return 1

    todo = []
    for p in picked:
        js, _, _ = out_paths(p)
        if js.exists() and not args.force and js.stat().st_mtime >= p.stat().st_mtime:
            continue
        todo.append(p)

    print(f"{len(picked)} selected, {len(picked) - len(todo)} already done, "
          f"{len(todo)} to transcribe  (model={args.model})")
    if not todo:
        return 0

    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    failures, started = [], time.time()

    for n, video in enumerate(todo, 1):
        print(f"[{n}/{len(todo)}] {video.parent.name}/{video.stem}", flush=True)
        t0 = time.time()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                wav = Path(tmp) / "audio.wav"
                extract_audio(video, wav)
                segs, info = model.transcribe(
                    str(wav),
                    language="en",
                    beam_size=args.beam_size,
                    vad_filter=True,
                    word_timestamps=True,
                    initial_prompt=VOCAB,
                )
                segments = [
                    {
                        "start": round(s.start, 3),
                        "end": round(s.end, 3),
                        "text": s.text,
                        "words": [
                            {"start": round(w.start, 3), "end": round(w.end, 3),
                             "word": w.word, "prob": round(w.probability, 3)}
                            for w in (s.words or [])
                        ],
                    }
                    for s in segs
                ]
            meta = {
                "lecture_id": lecture_id(video),
                "title": re.sub(r"^\d+_\d+_", "", video.stem).replace("-", " "),
                "section": video.parent.name,
                "video_path": str(video.relative_to(ROOT.parent.parent)),
                "duration_s": round(info.duration, 2),
                "model": args.model,
                "word_timestamps": True,
            }
            js = write_outputs(video, segments, meta)
            took = time.time() - t0
            print(f"      {len(segments)} segments, {info.duration:.0f}s audio in "
                  f"{took:.0f}s ({info.duration / max(took, 0.01):.1f}x) -> "
                  f"{js.relative_to(ROOT)}", flush=True)
        except Exception as e:                      # keep going, report at the end
            print(f"      FAILED: {e}", file=sys.stderr, flush=True)
            failures.append((video, e))

    mins = (time.time() - started) / 60
    print(f"\ndone in {mins:.1f} min - {len(todo) - len(failures)} ok, "
          f"{len(failures)} failed")
    for v, e in failures:
        print(f"  FAILED {v.stem}: {e}", file=sys.stderr)
    return 1 if failures else 0


def find_transcript(needle: str) -> Path | None:
    for js in sorted(OUT.glob("*/*.json")):
        if needle in js.stem or needle.lower() in js.stem.lower():
            return js
    return None


def cmd_show(args) -> int:
    js = find_transcript(args.needle)
    if not js:
        print(f"no transcript matching {args.needle!r} - run `transcribe.py run` first",
              file=sys.stderr)
        return 1
    data = json.loads(js.read_text())
    segs = data["segments"]
    print(f"# {data['title']}  ({data['duration_s']:.0f}s, {data['section']})")

    if args.at is None:
        for s in segs:
            print(f"[{ts(s['start'], comma=False)[3:]}] {s['text'].strip()}")
        return 0

    at = parse_at(args.at)
    lo, hi = at - args.window / 2, at + args.window / 2
    print(f"# around {args.at} (+/- {args.window / 2:.0f}s)\n")
    for s in segs:
        if s["end"] < lo or s["start"] > hi:
            continue
        mark = " <<<" if s["start"] <= at <= s["end"] else ""
        print(f"[{ts(s['start'], comma=False)[3:]}] {s['text'].strip()}{mark}")
    return 0


def cmd_status(args) -> int:
    vids = videos()
    done = {p.stem for p in OUT.glob("*/*.json")}
    goal = [p for p in vids if lecture_id(p) in set(GOAL_IDS)]
    goal_done = [p for p in goal if p.stem in done]
    print(f"videos on disk:      {len(vids)}")
    print(f"transcribed:         {len(done)}")
    print(f"goal lectures:       {len(goal_done)}/{len(goal)}")
    missing = [p for p in goal if p.stem not in done]
    if missing:
        print("\nstill to do (goal):")
        for p in missing:
            print(f"   {lecture_id(p):>9}  {p.stem}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="transcribe videos")
    r.add_argument("--all", action="store_true", help="every video on disk")
    r.add_argument("--goal", action="store_true", help="only the re-film lectures")
    r.add_argument("--id", nargs="*", help="specific lecture ids")
    r.add_argument("--match", help="substring of the filename")
    r.add_argument("--section", help="section directory prefix, e.g. 04")
    r.add_argument("--model", default="small.en",
                   help="whisper model (base.en, small.en, medium.en)")
    r.add_argument("--device", default="cpu")
    r.add_argument("--compute-type", default="int8")
    r.add_argument("--beam-size", type=int, default=5)
    r.add_argument("--force", action="store_true", help="redo existing transcripts")
    r.set_defaults(func=cmd_run)

    s = sub.add_parser("show", help="print a transcript, or the part around a timestamp")
    s.add_argument("needle", help="lecture id or part of the filename")
    s.add_argument("--at", help="timestamp, e.g. 3:33")
    s.add_argument("--window", type=float, default=40.0, help="seconds of context")
    s.set_defaults(func=cmd_show)

    st = sub.add_parser("status", help="what is transcribed so far")
    st.set_defaults(func=cmd_status)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
