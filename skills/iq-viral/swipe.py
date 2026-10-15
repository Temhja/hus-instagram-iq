#!/usr/bin/env python3
"""
swipe.py - rank reels by outlier multiple (views / that account's own median),
name the hook formula, score the hook, and write a swipe file.

Raw views are not evidence. 400K on a 2M-follower account is a quiet day;
400K on a 6K-follower Baghdad account found something copyable.

Input: a tab-separated file with a header row. Required columns:
  account  followers  median  views  hook
Optional: length  cta  url  date
Numbers may use Arabic-Indic digits, commas, or K/M suffixes (12K, 1.2M, ١٢ألف).

Usage
  python3 swipe.py captured.tsv
  python3 swipe.py captured.tsv --out ~/.claude/instagram-iq/brands/hus/swipe.md
  python3 swipe.py captured.tsv --json
"""

import argparse
import csv
import json
import os
import re
import statistics
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REEL = os.path.join(os.path.dirname(HERE), "iq-reel")
sys.path[:0] = [HERE, REEL, os.path.join(os.path.dirname(HERE), "iq-human")]
import iqtext  # noqa: E402
import hookscore  # noqa: E402


def num(v):
    s = iqtext.normalize(str(v)).strip().lower().replace(",", "").replace("٬", "")
    mult = 1
    for suf, m in (("k", 1e3), ("الف", 1e3), ("m", 1e6), ("مليون", 1e6)):
        if s.endswith(suf):
            mult, s = m, s[: -len(suf)].strip()
    try:
        return float(s) * mult
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.file, encoding="utf-8"), delimiter="\t"))
    data = hookscore.load_hooks()
    out, skipped = [], []
    for r in rows:
        v, m = num(r.get("views")), num(r.get("median"))
        if not v or not m:
            skipped.append(r.get("account", "?")); continue
        sc = hookscore.score(r.get("hook", ""), data)
        out.append({**r, "views_n": v, "median_n": m, "multiple": round(v / m, 1),
                    "hook_score": sc["score"], "formula": sc["formula"],
                    "formula_name": sc["formula_name"], "hook_words": sc["words"]})
    out.sort(key=lambda x: -x["multiple"])
    if not out:
        sys.exit("no usable rows - every row needs views and median")

    k = max(1, len(out) // 3)
    top, bottom = out[:k], out[-k:]
    accounts = {r["account"] for r in out}

    def counts(rs):
        c = {}
        for r in rs:
            if r["formula"]:
                c[r["formula_name"]] = c.get(r["formula_name"], 0) + 1
        return c

    tc, bc = counts(top), counts(bottom)
    over = sorted(((n, c, bc.get(n, 0)) for n, c in tc.items()), key=lambda x: -(x[1] - x[2]))
    med_top = statistics.median(r["hook_words"] for r in top)
    med_bot = statistics.median(r["hook_words"] for r in bottom)
    unclassified = [r for r in out if not r["formula"]]

    conf = "supports a claim" if len(out) >= 40 and len(accounts) >= 6 else \
           "directional only - collect more before acting on it" if len(out) >= 20 else \
           "too small - treat as anecdotes, not findings"

    lines = [f"SWIPE  ·  {len(out)} reels  ·  {len(accounts)} accounts  ·  baseline: account median  ·  {date.today()}",
             f"sample: {conf}", ""]
    lines.append("OUTLIERS (3x and above)")
    for r in [r for r in out if r["multiple"] >= 3]:
        f = f"#{r['formula']} {r['formula_name']}" if r["formula"] else "unclassified"
        lines.append(f"  {r['multiple']:>5}x  hook {r['hook_score']:>3}  {f:<34} {r['account']}  "
                     f"{int(r['views_n']):,} (median {int(r['median_n']):,})")
        lines.append(f"         «{r['hook']}»")
    lines += ["", "WHAT IS OVER-INDEXING (top third vs bottom third)"]
    for n, c, b in over[:5]:
        lines.append(f"  {n:<34} x{c} top · x{b} bottom")
    lines.append(f"  median hook length  {med_top:g} words top · {med_bot:g} bottom")
    lines += ["", f"UNCLASSIFIED ({len(unclassified)}) - read these by hand; a repeated shape here is a new formula"]
    for r in unclassified:
        lines.append(f"  {r['multiple']:>5}x  {r['account']}  «{r['hook']}»")
    if skipped:
        lines += ["", "SKIPPED (missing views or median): " + ", ".join(skipped)]

    report = "\n".join(lines)
    if a.json:
        print(json.dumps({"rows": out, "over_indexing": over, "confidence": conf}, ensure_ascii=False, indent=2, default=str))
    else:
        print(report)
    if a.out:
        p = os.path.expanduser(a.out)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write("# swipe.md\n\n```\n" + report + "\n```\n")
        print(f"\nwrote {p}")


if __name__ == "__main__":
    main()
