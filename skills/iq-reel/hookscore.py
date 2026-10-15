#!/usr/bin/env python3
"""
hookscore.py - score Iraqi-dialect Reel hooks before you shoot them.

A local heuristic, not a prediction of views. It rewards what holds a Baghdad
viewer in the first two seconds (a number, a place, a direct "you", a gap the
brain wants closed, a formula that is known to work, spoken Iraqi rather than
written fusha) and punishes what loses him (a greeting, "today we'll talk
about", stock phrases, a sentence too long to say in two seconds).

Usage
  python3 hookscore.py hooks.txt                # one hook per line, ranked
  python3 hookscore.py --hook "محد يگلك إن…"    # score one line
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(os.path.dirname(HERE), "iq-human")]
import iqtext  # noqa: E402

CURIOSITY = ["شنو", "ليش", "شلون", "وين", "منو", "محد", "سر", "الغلط", "غلط", "السبب", "تعرف", "شوف", "ما تگلك"]


def load_hooks():
    with open(os.path.join(HERE, "hooks.json"), encoding="utf-8") as f:
        return json.load(f)


def light(text):
    return iqtext.TASHKEEL.sub("", text).replace(iqtext.TATWEEL, "")


def classify(text, data=None):
    data = data or load_hooks()
    by_id = {h["id"]: h for h in data["hooks"]}
    cands = (light(text), iqtext.normalize(text))
    for hid in data["classify_order"]:
        rx = re.compile(by_id[hid]["match"])
        if any(rx.search(c) for c in cands):
            return by_id[hid]
    return None


def score(text, data=None):
    lex = iqtext.lexicon()
    reasons = []
    s = 15.0
    w = iqtext.words(text)
    n = len(w)

    if 5 <= n <= 12:
        s += 20; reasons.append(f"+20 length {n} words (sayable in ~2s)")
    elif 3 <= n <= 16:
        s += 10; reasons.append(f"+10 length {n} words (tight it to 12)")
    else:
        s -= 10; reasons.append(f"-10 length {n} words")

    h = classify(text, data)
    if h:
        s += 15; reasons.append(f"+15 formula #{h['id']} {h['name']} ({h['name_en']})")
    else:
        reasons.append("+0 no known formula (fine if it is a new one; check by hand)")

    if iqtext.has_number(text):
        s += 15; reasons.append("+15 has a number")
    if iqtext.count_hits(text, lex["money_units"]) or iqtext.count_hits(text, lex["baghdad_places"]):
        s += 10; reasons.append("+10 money unit or a real place")
    if iqtext.count_hits(text, lex["second_person"]):
        s += 10; reasons.append("+10 talks to 'you'")
    if iqtext.count_hits(text, CURIOSITY) or "؟" in text or "?" in text:
        s += 10; reasons.append("+10 opens a gap")

    iq, fu, r = iqtext.dialect_ratio(text)
    if r is None:
        reasons.append("+0 dialect neutral (no Iraqi or fusha markers)")
    elif r >= 0.7:
        s += 15; reasons.append(f"+15 spoken Iraqi ({iq} Iraqi / {fu} fusha markers)")
    elif r >= 0.4:
        s += 5; reasons.append(f"+5 mixed register ({iq} Iraqi / {fu} fusha)")
    else:
        s -= 15; reasons.append(f"-15 reads as written fusha ({iq} Iraqi / {fu} fusha)")

    norm = iqtext.normalize(text).strip()
    for g in lex["greetings"]:
        if norm.startswith(iqtext.normalize(g)):
            s -= 30; reasons.append(f"-30 opens with a greeting ({g})"); break
    tc = iqtext.count_hits(text, lex["throat_clearing"])
    if tc:
        s -= 25; reasons.append(f"-25 throat-clearing ({tc[0][0]})")
    slop = iqtext.count_hits(text, [p["phrase"] for p in lex["slop_phrases"]])
    for ph, _ in slop:
        s -= 10; reasons.append(f"-10 stock phrase ({ph})")

    s = max(0, min(100, round(s)))
    label = "STRONG" if s >= 75 else "OK" if s >= 50 else "WEAK"
    return {"hook": text, "score": s, "label": label,
            "formula": h["id"] if h else None,
            "formula_name": f"{h['name']} / {h['name_en']}" if h else None,
            "words": n, "reasons": reasons}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--hook")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.hook:
        lines = [a.hook]
    elif a.file:
        src = sys.stdin if a.file == "-" else open(a.file, encoding="utf-8")
        lines = [l.strip() for l in src if l.strip()]
    else:
        ap.error("give a file or --hook")
    data = load_hooks()
    res = sorted((score(l, data) for l in lines), key=lambda r: -r["score"])
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2)); return
    for r in res:
        f = f"#{r['formula']} {r['formula_name']}" if r["formula"] else "unclassified"
        print(f"{r['score']:>3}  {r['label']:<6}  {f}")
        print(f"     {r['hook']}")
        for why in r["reasons"]:
            print(f"       {why}")
        print()
    if res and res[0]["score"] < 50:
        print("Top hook is under 50. You don't have the hook yet - rewrite, don't polish.")


if __name__ == "__main__":
    main()
