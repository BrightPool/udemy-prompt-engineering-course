#!/usr/bin/env python3
"""Surface improvement themes from scraped reviews (out/reviews.json)."""
import json, re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).parent / "out"
rv = json.load(open(OUT / "reviews.json"))["reviews"]

crit = [r for r in rv if r["rating"] <= 3.5]
mid = [r for r in rv if 3.5 < r["rating"] < 4.5]
top = [r for r in rv if r["rating"] >= 4.5]
print(f"total={len(rv)} critical(<=3.5)={len(crit)} mid(4)={len(mid)} top(>=4.5)={len(top)}")


def is_en(t):
    letters = [c for c in t if c.isalpha()]
    if not letters:
        return False
    ascii_letters = [c for c in letters if ord(c) < 128]
    return len(ascii_letters) / len(letters) > 0.9 and len(t) > 15


STOP = set(
    "the a an and or but to of in is are was were be been for with on at this "
    "that it you we they my our your me as so not no very too more most just "
    "if then than out up about into can will would should could have has had "
    "do does did get got use used using need needs want course content video "
    "videos lecture lectures section sections udemy prompt prompts chatgpt gpt "
    "openai there their them what when where which who how all some any only "
    "also been being from they're really good great well lot make made like "
    "much many one two also even still over after before because while".split()
)

# Concrete complaint signals to count across critical+mid reviews
SIGNALS = {
    "outdated/old": r"\b(outdated|out of date|old|deprecated|no longer|doesn'?t work|not work|broken|update[d]?)\b",
    "too basic/beginner": r"\b(too basic|basic|beginner|introductory|surface|shallow|simplistic|nothing new)\b",
    "too advanced/fast": r"\b(too fast|fast paced|hard to follow|confusing|difficult to|advanced|overwhelming)\b",
    "audio/video quality": r"\b(audio|sound|microphone|mic|volume|video quality|resolution|screen)\b",
    "accent/clarity": r"\b(accent|hard to understand|pronunciation|mumbl|unclear speech)\b",
    "more examples/practice": r"\b(more example|hands.?on|practice|exercise|practical|project|real world|real.?life)\b",
    "code/notebook issues": r"\b(code|notebook|colab|error|api key|install|setup|github)\b",
    "pacing/length": r"\b(too long|too short|drag|repetitive|repeated|lengthy|padded)\b",
    "captions/language": r"\b(caption|subtitle|translat|english|language)\b",
    "quiz/assessment": r"\b(quiz|assessment|test|certificate|assignment)\b",
}

text = [r for r in (crit + mid) if is_en(r["content"])]
print(f"\nEnglish critical+mid reviews analysed: {len(text)}")

print("\n=== Complaint signal frequency (critical+mid English reviews) ===")
sig_counts = Counter()
for r in text:
    low = r["content"].lower()
    for name, pat in SIGNALS.items():
        if re.search(pat, low):
            sig_counts[name] += 1
for name, c in sig_counts.most_common():
    print(f"  {c:4d}  {name}")

print("\n=== Top distinctive terms ===")
words = Counter()
for r in text:
    for w in re.findall(r"[a-z]+", r["content"].lower()):
        if len(w) > 3 and w not in STOP:
            words[w] += 1
for w, c in words.most_common(40):
    print(f"  {c:4d}  {w}")

print("\n=== Sample low-star reviews (<=2.5) with substance ===")
subs = sorted(
    [r for r in crit if r["rating"] <= 2.5 and is_en(r["content"]) and len(r["content"]) > 80],
    key=lambda r: -len(r["content"]),
)
for r in subs[:25]:
    print(f"\n[★{r['rating']} {r['created'][:10]}] {r['content'][:500]}")
