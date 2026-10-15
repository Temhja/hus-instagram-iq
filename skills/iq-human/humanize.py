#!/usr/bin/env python3
"""
humanize.py - clean an Arabic (Iraqi) caption or script and score how written
or machine-made it reads. Detect and fix in one tool.

What it FIXES automatically (mechanical, always safe):
  - invisible characters that ride along from AI tools and copy-paste
    (zero-width space, BOM, soft hyphen, bidi embeddings/overrides)
  - tatweel stretching (كـــبير)
  - full tashkeel; shadda is kept by default because it tells you how to say
    the word (سوّي, هوّه). --strip-shadda removes it too
  - em/en dashes between words become "، "  (the single loudest AI tell)
  - runs of spaces

What it REPORTS but never rewrites (judgement, your call):
  - stock Arabic phrases, each with an Iraqi rewrite direction
  - fusha words in a script meant to be spoken in Iraqi
  - LRM/RLM/isolate marks (often legitimate in mixed Arabic-English lines)
  - AI-pattern emoji clusters

The five-check panel is a local heuristic. It is NOT GPTZero or any other
detector and makes no promise about their verdicts. Nothing is uploaded.

Usage
  python3 humanize.py draft.txt                  # report only
  python3 humanize.py draft.txt --fix -o clean.txt
  python3 humanize.py draft.txt --mode caption   # register check relaxed
  python3 humanize.py draft.txt --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import iqtext  # noqa: E402

DASH_RE = re.compile(r"\s*[—–]\s*")
SENT_RE = re.compile(r"[^.!?؟\n]+")
SHADDA = "ّ"


def fix(text, strip_shadda=False):
    changes = {}
    out = text
    for ch, name in iqtext.STRIP_ALWAYS.items():
        c = out.count(ch)
        if c:
            changes[name] = c
            out = out.replace(ch, "")
    # Keep the tatweel in "الـAI" / "بالـMeta": it's the standard way to join
    # an Arabic prefix to a Latin word. Strip it everywhere else.
    stretch = re.compile(iqtext.TATWEEL + r"(?![A-Za-z0-9])")
    c = len(stretch.findall(out))
    if c:
        changes["tatweel"] = c
        out = stretch.sub("", out)
    marks = iqtext.TASHKEEL if strip_shadda else re.compile(r"[ً-ِْٰ]")
    c = len(marks.findall(out))
    if c:
        changes["tashkeel marks"] = c
        out = marks.sub("", out)
    c = len(DASH_RE.findall(out))
    if c:
        changes["em/en dashes"] = c
        out = DASH_RE.sub("، ", out)
    out2 = re.sub(r"[ \t]{2,}", " ", out)
    if out2 != out:
        changes["double spaces"] = 1
    return out2, changes


def check_register(text, mode):
    iq, fu, r = iqtext.dialect_ratio(text)
    if r is None:
        return 60.0, "no dialect markers either way"
    if mode == "caption":
        s = 40 + 60 * r
    else:
        s = 100 * r
    return iqtext_clamp(s), f"{iq} Iraqi / {fu} fusha markers"


def iqtext_clamp(n):
    return max(0.0, min(100.0, n))


def check_slop(text):
    lex = iqtext.lexicon()
    hits = iqtext.count_hits(text, [p["phrase"] for p in lex["slop_phrases"]])
    n = max(1, len(iqtext.words(text)))
    total = sum(c for _, c in hits)
    per100 = total * 100 / n
    return iqtext_clamp(100 - per100 * 25), f"{total} stock phrase(s), {per100:.1f} per 100 words", hits


def check_typography(text):
    lex = iqtext.lexicon()
    pen, notes = 0, []
    inv = sum(text.count(c) for c in iqtext.STRIP_ALWAYS)
    if inv:
        pen += 30; notes.append(f"{inv} invisible chars")
    dashes = len(re.findall(r"[—–]", text))
    if dashes:
        pen += min(30, dashes * 10); notes.append(f"{dashes} em/en dash")
    letters = max(1, len(iqtext.ARABIC_LETTER.findall(text)))
    tk = len(re.findall(r"[ً-ِْ]", text))
    if tk / letters > 0.03:
        pen += 15; notes.append(f"heavy tashkeel ({tk})")
    if re.search(iqtext.TATWEEL + r"(?![A-Za-z0-9])", text):
        pen += 10; notes.append("tatweel")
    emo = sum(text.count(e) for e in lex["ai_emoji"])
    if emo >= 3:
        pen += min(25, emo * 5); notes.append(f"{emo} AI-pattern emoji")
    if text.count("؛") >= 2:
        pen += 10; notes.append("semicolons (؛) - nobody says those")
    return iqtext_clamp(100 - pen), ", ".join(notes) or "clean"


def check_burstiness(text):
    lens = [len(iqtext.words(s)) for s in SENT_RE.findall(text) if len(iqtext.words(s)) > 1]
    if len(lens) < 4:
        return 60.0, "too short to judge"
    m = statistics.mean(lens)
    cv = statistics.pstdev(lens) / m if m else 0
    s = (cv - 0.2) / (0.65 - 0.2) * 100
    return iqtext_clamp(s), f"sentence-length variation {cv:.2f} across {len(lens)} sentences (want 0.5+)"


def check_specificity(text):
    lex = iqtext.lexicon()
    n = len(iqtext.words(text))
    if n < 15:
        return 60.0, "too short to judge"
    nums = len(re.findall(r"\d+", iqtext.normalize(text)))
    places = sum(c for _, c in iqtext.count_hits(text, lex["baghdad_places"]))
    money = sum(c for _, c in iqtext.count_hits(text, lex["money_units"]))
    d = (nums + places + money) * 100 / n
    return iqtext_clamp(d / 6 * 100), f"{nums} numbers, {places} places, {money} money words ({d:.1f} per 100 words)"


def panel(text, mode):
    reg = check_register(text, mode)
    slop = check_slop(text)
    typo = check_typography(text)
    burst = check_burstiness(text)
    spec = check_specificity(text)
    checks = {
        "register": reg, "stock phrases": slop[:2], "typography": typo,
        "rhythm": burst, "specificity": spec,
    }
    score = round(statistics.mean(v[0] for v in checks.values()))
    return score, checks, slop[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("-o", "--out")
    ap.add_argument("--mode", choices=["script", "caption"], default="script")
    ap.add_argument("--strip-shadda", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()

    before, _, _ = panel(text, a.mode)
    cleaned, changes = fix(text, a.strip_shadda) if a.fix else (text, {})
    after, checks, slop_hits = panel(cleaned, a.mode)

    lex = iqtext.lexicon()
    fixes = {p["phrase"]: p["fix"] for p in lex["slop_phrases"]}
    fusha = iqtext.count_hits(cleaned, lex["fusha_markers"])
    prefs = [(t["avoid"], t["use"], t.get("note", ""), c) for t in lex.get("preferred_terms", [])
             for _, c in iqtext.count_hits(cleaned, [t["avoid"]])]
    marks = {name: cleaned.count(ch) for ch, name in iqtext.REPORT_ONLY.items() if cleaned.count(ch)}

    if a.fix and a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(cleaned)

    if a.json:
        print(json.dumps({
            "score_before": before, "score": after,
            "verdict": "PASS" if after >= 70 else "REWRITE",
            "checks": {k: {"score": round(v[0]), "detail": v[1]} for k, v in checks.items()},
            "fixed": changes,
            "stock_phrases": [{"phrase": p, "count": c, "fix": fixes.get(p, "")} for p, c in slop_hits],
            "house_terms": [{"avoid": a_, "use": u, "note": n, "count": c} for a_, u, n, c in prefs],
            "fusha_words": [{"word": w, "count": c} for w, c in fusha],
            "direction_marks_kept": marks,
            "text": cleaned if a.fix else None,
        }, ensure_ascii=False, indent=2))
        return

    verdict = "PASS" if after >= 70 else "REWRITE"
    print(f"HUMAN SCORE  {after}  {verdict}" + (f"   (was {before} before fixes)" if a.fix else ""))
    for k, (s, d) in checks.items():
        print(f"  {round(s):>3}  {k:<15} {d}")
    if changes:
        print("\nFIXED")
        for k, v in changes.items():
            print(f"  - {v} x {k}")
    if slop_hits:
        print("\nSTOCK PHRASES (rewrite these yourself)")
        for p, c in slop_hits:
            print(f"  - {p}  x{c}  ->  {fixes.get(p, '')}")
    if prefs:
        print("\nHOUSE TERMS")
        for a_, u, n, c in prefs:
            print(f"  - {a_} x{c}  ->  {u}  ({n})")
    if fusha and a.mode == "script":
        print("\nFUSHA IN A SPOKEN SCRIPT")
        print("  " + "، ".join(f"{w} x{c}" for w, c in fusha))
    if marks:
        print("\nDIRECTION MARKS KEPT (fine in mixed Arabic/English lines; check they're intended)")
        print("  " + ", ".join(f"{k} x{v}" for k, v in marks.items()))
    if a.fix and a.out:
        print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
