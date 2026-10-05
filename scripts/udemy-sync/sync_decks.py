#!/usr/bin/env python3
"""
sync_decks.py - publish finished decks to ~/Desktop/course-decks for review.

The repo stays the source of truth: build scripts are code and live in
`decks/<slug>/`. This puts the openable deliverables where James can browse them:

    ~/Desktop/course-decks/
      james-required-feedback.md     <- ONE file, a section per lecture. James writes here.
      INDEX.md                       status of all 23
      memory/
        memory.pptx
        NOTES.md                     agent's research + what changed since filming

Safe to re-run. Decks and NOTES are refreshed; the feedback file is only ever
extended. A section James has typed into is never rewritten - each section is
compared against the text this script last generated for it (tracked in
.sync-state.json), and only untouched sections get refreshed with new agent
questions.

    python3 scripts/udemy-sync/sync_decks.py            # sync + status
    python3 scripts/udemy-sync/sync_decks.py --status   # status only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent      # repo root
DECKS = ROOT / "decks"
DEST = Path.home() / "Desktop" / "course-decks"
MANIFEST = ROOT / "scripts" / "udemy-sync" / "out" / "lecture_manifest.json"
FEEDBACK = DEST / "james-required-feedback.md"
STATE = DEST / ".sync-state.json"

BEGIN = "<!-- lecture:{slug} -->"
END = "<!-- /lecture:{slug} -->"


def newer(src: Path, dst: Path) -> bool:
    return not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime


def digest(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def for_james(notes: Path) -> list[str]:
    """Pull the '## For James' bullets out of an agent's NOTES.md."""
    if not notes.exists():
        return []
    m = re.search(r"^##+\s*For James\s*$(.*?)(?=^##\s|\Z)",
                  notes.read_text(errors="replace"), re.S | re.M | re.I)
    if not m:
        return []
    return [ln.rstrip() for ln in m.group(1).strip().splitlines() if ln.strip()]


def section(lec: dict, questions: list[str], state: str) -> str:
    slug = lec["slug"]
    meta = " · ".join(x for x in (lec["part"], lec["action"],
                                  lec["length"], lec["owner"]) if x)
    q = ("\n".join(questions) if questions else
         "_Nothing raised yet._")
    return f"""{BEGIN.format(slug=slug)}
## {lec['title']}

`{slug}/` · {meta} · **{state}**

<details><summary>Your original note</summary>

> {lec['note'] or '(none given)'}

</details>

**Agent's questions**

{q}

**Verdict:** ` good to film / needs changes / rebuild `

**Feedback:**


{END.format(slug=slug)}"""


def build_feedback(lectures: list[dict], states: dict, questions: dict) -> tuple[int, int]:
    """Create or extend the single feedback file without touching James's writing."""
    prev = json.loads(STATE.read_text()) if STATE.exists() else {}
    text = FEEDBACK.read_text() if FEEDBACK.exists() else ""
    added = refreshed = 0

    if not text:
        text = (
            "# Feedback — course re-film decks\n\n"
            "One section per lecture. Write under **Feedback:** in any section; a\n"
            "section you have typed into is never rewritten by a re-sync.\n\n"
            "Decks are in the folder beside this file. `INDEX.md` has the status table.\n\n"
            "---\n\n"
        )

    for lec in lectures:
        slug = lec["slug"]
        new = section(lec, questions.get(slug, []), states.get(slug, "not started"))
        b, e = BEGIN.format(slug=slug), END.format(slug=slug)
        m = re.search(re.escape(b) + r".*?" + re.escape(e), text, re.S)
        if not m:
            text = text.rstrip() + "\n\n" + new + "\n"
            added += 1
        elif digest(m.group(0)) == prev.get(slug):
            # untouched since we wrote it - safe to refresh with new questions
            if m.group(0) != new:
                text = text[:m.start()] + new + text[m.end():]
                refreshed += 1
        prev[slug] = digest(new)

    FEEDBACK.write_text(text)
    STATE.write_text(json.dumps(prev, indent=1))
    return added, refreshed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true", help="do not copy, just report")
    args = ap.parse_args()

    lectures = json.loads(MANIFEST.read_text())
    wanted = [l for l in lectures if l["deck"]]
    DEST.mkdir(parents=True, exist_ok=True)

    copied = 0
    states, questions, rows = {}, {}, []
    for lec in wanted:
        slug = lec["slug"]
        src = DECKS / slug
        pptx, notes = src / f"{slug}.pptx", src / "NOTES.md"
        out = DEST / slug

        if not args.status and src.exists():
            out.mkdir(parents=True, exist_ok=True)
            if pptx.exists() and newer(pptx, out / f"{slug}.pptx"):
                shutil.copy2(pptx, out / f"{slug}.pptx")
                copied += 1
            if notes.exists() and newer(notes, out / "NOTES.md"):
                shutil.copy2(notes, out / "NOTES.md")
                copied += 1
            # feedback now lives in one file at the top - retire any old per-folder copy
            stale = out / "james-required-feedback.md"
            if stale.exists():
                stale.rename(out / "_old-feedback-file.md")

        if pptx.exists() and notes.exists():
            state = "ready to review"
        elif pptx.exists():
            state = "deck only"
        elif src.exists():
            state = "building"
        else:
            state = "not started"
        states[slug] = state
        questions[slug] = for_james(notes)
        rows.append((state, lec))

    added = refreshed = 0
    if not args.status:
        added, refreshed = build_feedback(wanted, states, questions)

    order = {"ready to review": 0, "deck only": 1, "building": 2, "not started": 3}
    rows.sort(key=lambda r: (order[r[0]], r[1]["slug"]))
    ready = sum(1 for s, _ in rows if s == "ready to review")

    lines = [
        "# Course decks — the principles half of each re-film",
        "",
        f"_Synced {datetime.now():%Y-%m-%d %H:%M} · {ready} of {len(rows)} ready to review._",
        "",
        "Write feedback in **[james-required-feedback.md](james-required-feedback.md)** —",
        "one file, a section per lecture. Your writing there is never overwritten.",
        "",
        "| Lecture | Status | Action | Len | Deck |",
        "|---|---|---|---|---|",
    ]
    for state, lec in rows:
        mark = {"ready to review": "**ready**", "deck only": "deck only",
                "building": "building…", "not started": "—"}[state]
        slug = lec["slug"]
        link = (f"[{slug}]({slug}/{slug}.pptx)"
                if (DEST / slug / f"{slug}.pptx").exists() else "—")
        lines.append(f"| {lec['title']} | {mark} | {lec['action']} | "
                     f"{lec['length'] or '—'} | {link} |")

    no_deck = [l for l in lectures if not l["deck"]]
    if no_deck:
        lines += ["", "## No deck needed", ""]
        lines += [f"- **{l['title']}** — {l['note']}" for l in no_deck]

    (DEST / "INDEX.md").write_text("\n".join(lines) + "\n")

    print(f"{DEST}")
    print(f"  {ready}/{len(rows)} ready to review"
          + ("" if args.status else
             f", {copied} file(s) copied, {added} section(s) added, "
             f"{refreshed} refreshed"))
    for state, lec in rows:
        if state != "not started":
            print(f"   {state:<16} {lec['slug']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
