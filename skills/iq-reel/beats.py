#!/usr/bin/env python3
"""
beats.py - turn an Iraqi-dialect Reel script into a timed beat sheet and flag
what will lose the viewer before you shoot.

Built around the HUS script framework:
    [HOOK] -> [LEAD] -> [BODY] -> [OPEN LOOP] -> [CTA]
Tag each section on its own line (English or Arabic tags both work:
[هوك] [ليد] [بودي] [لوب] [CTA]/[اكشن]). One spoken line = one beat = one cut.

Speech rate: Arabic word counts are lower than English for the same content
because prefixes and pronouns attach to the word. The default of 130 words per
minute is a STARTING ESTIMATE, not a measured Iraqi norm. Time yourself reading
one script out loud, then pass --wpm with your real number and put it in
voice.md. Until you do, treat every timing below as approximate.

Usage
  python3 beats.py script.txt --target 30
  python3 beats.py script.txt --target 30 --wpm 142
  python3 beats.py script.txt --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(os.path.dirname(HERE), "iq-human")]
import iqtext  # noqa: E402

SECTIONS = ["HOOK", "LEAD", "BODY", "OPEN LOOP", "CTA"]
ALIASES = {
    "HOOK": "HOOK", "هوك": "HOOK", "الهوك": "HOOK",
    "LEAD": "LEAD", "ليد": "LEAD", "المقدمة": "LEAD",
    "BODY": "BODY", "بودي": "BODY", "المحتوى": "BODY",
    "OPEN LOOP": "OPEN LOOP", "LOOP": "OPEN LOOP", "لوب": "OPEN LOOP", "اوبن لوب": "OPEN LOOP",
    "CTA": "CTA", "اكشن": "CTA", "الطلب": "CTA",
}
TAG_RE = re.compile(r"^\s*\[\s*([^\]]+?)\s*\]\s*$")
PAUSE = 0.3
ASKS = ["علّق", "علق", "اكتب", "اكتبلي", "دز", "دزلي", "راسلني", "راسلنا", "واتساب", "احفظ", "احفظه",
        "شارك", "شاركه", "تابع", "تابعني", "تابعنا", "الرابط", "اضغط", "اتصل"]
LOOP_WORDS = ["الفيديو الجاي", "الجاي", "الجزء الثاني", "الجزء الجاي", "باچر", "بالفيديو الجاي", "راح احچيلك", "راح اراويك", "تابعني حتى"]


def concrete(line):
    lex = iqtext.lexicon()
    return iqtext.has_number(line) or bool(iqtext.count_hits(line, lex["baghdad_places"])) \
        or bool(iqtext.count_hits(line, lex["money_units"]))


def parse(text):
    beats, section = [], None
    for raw in text.splitlines():
        if not raw.strip():
            continue
        m = TAG_RE.match(raw)
        if m:
            section = ALIASES.get(m.group(1).upper(), ALIASES.get(m.group(1), m.group(1).upper()))
            continue
        beats.append({"section": section, "line": raw.strip()})
    return beats


def run(text, target, wpm):
    beats = parse(text)
    flags, t = [], 0.0
    for i, b in enumerate(beats):
        n = len(iqtext.words(b["line"]))
        d = n / wpm * 60 + PAUSE
        b.update(words=n, start=round(t, 1), dur=round(d, 1), concrete=concrete(b["line"]))
        iq, fu, r = iqtext.dialect_ratio(b["line"])
        b["fusha"] = r is not None and r < 0.4
        t += d
    total = round(t, 1)

    if not beats:
        return {"beats": [], "total": 0, "flags": ["empty script"]}

    hook = beats[0]
    if hook["dur"] > 3.0:
        flags.append(f"HOOK runs {hook['dur']}s - cut it under 3s")
    for i, b in enumerate(beats):
        if b["dur"] > 4.0:
            flags.append(f"beat {i+1} runs {b['dur']}s - split it, change the frame")
        if b["fusha"]:
            flags.append(f"beat {i+1} reads as written fusha - say it the way you'd say it")
    run_ = 0
    for i, b in enumerate(beats):
        run_ = 0 if b["concrete"] else run_ + 1
        if run_ == 3:
            flags.append(f"beats {i-1}-{i+1}: three in a row with no number, place or money - add one")

    tagged = [b["section"] for b in beats if b["section"]]
    if tagged:
        present = [s for s in SECTIONS if s in tagged]
        missing = [s for s in SECTIONS if s not in tagged]
        if missing:
            flags.append("framework missing: " + ", ".join(missing))
        order = [SECTIONS.index(s) for s in dict.fromkeys(tagged) if s in SECTIONS]
        if order != sorted(order):
            flags.append("framework out of order - keep HOOK > LEAD > BODY > OPEN LOOP > CTA")
    else:
        if not any(iqtext.count_hits(b["line"], LOOP_WORDS) for b in beats[-3:]):
            flags.append("no open loop near the end - tease the next video before the CTA")

    cta_lines = [b for b in beats if b["section"] == "CTA"] or beats[-1:]
    asks = sum(len(iqtext.count_hits(b["line"], ASKS)) for b in cta_lines)
    if asks == 0:
        flags.append("CTA has no ask")
    elif asks > 1:
        flags.append(f"CTA has {asks} asks - keep one")

    if target:
        if total > target * 1.15:
            flags.append(f"runs {total}s against a {target}s target - cut {round(total-target,1)}s")
        elif total < target * 0.75:
            flags.append(f"runs {total}s against a {target}s target - thin; add a concrete beat or shorten the target")

    return {"beats": beats, "total": total, "wpm": wpm, "flags": flags}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--target", type=float, default=30)
    ap.add_argument("--wpm", type=float, default=130)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    res = run(text, a.target, a.wpm)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2)); return
    print(f"BEAT SHEET  ·  {len(res['beats'])} beats  ·  {res['total']}s  ·  {a.wpm:g} wpm"
          + ("  (default rate - calibrate with --wpm)" if a.wpm == 130 else ""))
    for i, b in enumerate(res["beats"], 1):
        mark = "●" if b["concrete"] else "○"
        sec = (b["section"] or "")[:9]
        print(f"{i:>2}  {b['start']:>5.1f}s  {b['dur']:>4.1f}s  {mark}  {sec:<9}  {b['line']}")
    print()
    if res["flags"]:
        print("FIX")
        for f in res["flags"]:
            print("  - " + f)
    else:
        print("CLEAN - shoot it.")


if __name__ == "__main__":
    main()
