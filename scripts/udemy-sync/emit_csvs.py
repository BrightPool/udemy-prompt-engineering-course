"""
Roll up out/analysis/*.json (drift mode) and out/analysis_video_only/*.json
(video-only mode) into two CSVs:

  out/analysis.csv
    Per-lecture row with the full LLM analysis embedded as a JSON string in one
    column. Use this when you want everything in one place.

  out/analysis_flat.csv
    Per-lecture row where every scalar field is its own column. Lists are
    semicolon-joined; complex nested arrays (drift_segments, specific_diffs)
    collapse to a count. video_quality.* booleans get a `quality_` prefix and a
    rolled-up `quality_issue_count` column for quick "worst videos first"
    sorting.

Run:
  uv run --with python-dotenv python scripts/udemy-sync/emit_csvs.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "out"
ANALYSIS_DIRS = [OUT_DIR / "analysis", OUT_DIR / "analysis_video_only"]


def join_list(xs):
    if not xs:
        return ""
    return "; ".join(str(x).replace("\n", " ").replace(";", ",") for x in xs)


def quality_issue_count(q: dict | None) -> int:
    """Bools that are True + pacing != medium count as issues.

    no_exercises is excluded — most code-along lectures don't have exercises
    by design, so it's noise in the rollup. The raw `quality_no_exercises`
    column is still emitted if you want to filter on it directly.
    """
    if not q:
        return 0
    n = 0
    for k in (
        "talking_too_quickly",
        "over_talking_same_point",
        "monotonous_voice",
        "jumpy_video",
    ):
        if q.get(k):
            n += 1
    if q.get("pacing_speed") and q["pacing_speed"] != "medium":
        n += 1
    return n


# Stable column order for the flat CSV. Drift-only fields are empty for
# video_only rows, and vice versa.
FLAT_COLUMNS = [
    # identifiers (always populated)
    "lecture_id",
    "lecture_title",
    "section",
    "mode",
    "video_path",
    "notebook_paths",
    "notebook_paths_count",
    "model",
    "fps",
    # drift scalars
    "drift_score",
    "drift_reason",
    "drift_categories",
    "drift_segments_count",
    "student_blocking",
    "deprecated_topic",
    "deprecated_reason",
    "specific_diffs_count",
    "recommended_action",
    "confidence",
    "summary",
    "video_summary",
    "estimated_rerecord_minutes",
    "rerecord_scope",
    "prerequisite_changes_count",
    "prerequisite_changes",
    "talking_points_to_add_count",
    "talking_points_to_add",
    # video quality (prefixed so they sort together)
    "quality_issue_count",
    "quality_talking_too_quickly",
    "quality_over_talking_same_point",
    "quality_no_exercises",
    "quality_monotonous_voice",
    "quality_pacing_speed",
    "quality_jumpy_video",
]


def flatten(record: dict) -> dict:
    meta = record.get("_meta", {})
    quality = record.get("video_quality", {}) or {}
    # Fall back on data shape if _meta.mode is missing (older JSONs).
    mode = meta.get("mode") or ("drift" if "drift_score" in record else "video_only")
    row = {col: "" for col in FLAT_COLUMNS}

    row["lecture_id"] = meta.get("lecture_id", "")
    row["lecture_title"] = meta.get("lecture_title", "")
    row["section"] = meta.get("section", "") or ""
    row["mode"] = mode
    row["video_path"] = meta.get("video_path", "")
    nb = meta.get("notebook_paths", []) or []
    row["notebook_paths"] = join_list(nb)
    row["notebook_paths_count"] = len(nb)
    row["model"] = meta.get("model", "")
    row["fps"] = meta.get("fps", "")

    # Shared between modes
    row["deprecated_topic"] = record.get("deprecated_topic", "")
    row["deprecated_reason"] = record.get("deprecated_reason", "")
    row["confidence"] = record.get("confidence", "")
    row["summary"] = (record.get("summary") or "").replace("\n", " ")
    row["video_summary"] = (record.get("video_summary") or "").replace("\n", " ")
    row["estimated_rerecord_minutes"] = record.get("estimated_rerecord_minutes", "")

    tps = record.get("talking_points_to_add") or []
    row["talking_points_to_add"] = join_list(tps)
    row["talking_points_to_add_count"] = len(tps)

    # Drift-only fields
    if mode == "drift":
        row["drift_score"] = record.get("drift_score", "")
        row["drift_reason"] = (record.get("drift_reason") or "").replace("\n", " ")
        row["drift_categories"] = join_list(record.get("drift_categories") or [])
        row["drift_segments_count"] = len(record.get("drift_segments") or [])
        row["student_blocking"] = record.get("student_blocking", "")
        row["specific_diffs_count"] = len(record.get("specific_diffs") or [])
        row["recommended_action"] = record.get("recommended_action", "")
        row["rerecord_scope"] = record.get("rerecord_scope", "")
        pre = record.get("prerequisite_changes") or []
        row["prerequisite_changes"] = join_list(pre)
        row["prerequisite_changes_count"] = len(pre)

    # Video quality
    row["quality_issue_count"] = quality_issue_count(quality)
    for k in (
        "talking_too_quickly",
        "over_talking_same_point",
        "no_exercises",
        "monotonous_voice",
        "pacing_speed",
        "jumpy_video",
    ):
        row[f"quality_{k}"] = quality.get(k, "")

    return row


def main():
    records = []
    for d in ANALYSIS_DIRS:
        if not d.exists():
            continue
        for jf in sorted(d.glob("*.json")):
            try:
                records.append(json.loads(jf.read_text()))
            except Exception as e:
                print(f"WARN: skipping {jf}: {e}")

    print(f"Loaded {len(records)} analysis JSON files")

    # CSV 1: full JSON in a single column.
    full_path = OUT_DIR / "analysis.csv"
    with full_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "lecture_id", "lecture_title", "section", "mode",
            "video_path", "notebook_paths", "llm_analysis_json",
        ])
        for r in records:
            meta = r.get("_meta", {})
            w.writerow([
                meta.get("lecture_id", ""),
                meta.get("lecture_title", ""),
                meta.get("section", "") or "",
                meta.get("mode", ""),
                meta.get("video_path", ""),
                "; ".join(meta.get("notebook_paths") or []),
                json.dumps(r, separators=(",", ":")),
            ])
    print(f"  → {full_path.relative_to(HERE.parent.parent)}")

    # CSV 2: flat / scalar columns.
    flat_path = OUT_DIR / "analysis_flat.csv"
    with flat_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FLAT_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow(flatten(r))
    print(f"  → {flat_path.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main()
