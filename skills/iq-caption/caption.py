#!/usr/bin/env python3
"""
caption.py - lint an Arabic/Iraqi Instagram caption and show what the feed
shows before "... المزيد / more".

The feed cut is an APPROXIMATION (default 125 characters). It moves with the
device, font size, line breaks and the Arabic/Latin mix. Aim to land the hook
well inside it, never engineer a caption to end exactly at the cut.

Checks
  1. first line is not a greeting or throat-clearing
  2. the visible window carries something concrete (number, place, money)
  3. one clear ask (comment a keyword / DM / WhatsApp / save / share)
  4. hashtags: at most 5 (Instagram's cap announced Dec 2025 - verify it is
     still current), none of the filler tags, none in the first line
  5. no raw link pasted in the caption (not clickable on Instagram)
  6. mixed-direction lines that start with Latin text inside an Arabic caption
     (they render left-aligned and break the block; start the line in Arabic
     or add an RLM)
  7. search keywords present in the visible window (if --keywords given)
  8. length under 2,200 characters

Usage
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "اعلانات ممولة,بغداد"
  python3 caption.py caption.txt --truncate 110 --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(os.path.dirname(HERE), "iq-human")]
import iqtext  # noqa: E402

LIMIT = 2200
HASHTAG_LIMIT = 5
HASHTAG_RE = re.compile(r"#[\w_]+", re.UNICODE)
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|iq|net|org|io|co|app|me)\b\S*", re.I)
FILLER = {"#explore", "#explorepage", "#viral", "#fyp", "#foryou", "#trending", "#reels", "#instagood",
          "#اكسبلور", "#اكسبلورر", "#explore_page", "#ترند", "#تيك_توك", "#لايك", "#متابعة", "#فولو", "#viralreels"}
ASKS = [
    (r"(علّق|علق|اكتب|اكتبلي|اكتبولي)[^.\n]{0,25}(كلمة|«|\"|')", "comment a keyword"),
    (r"(دزلي|دزّلي|راسلني|راسلنا|ابعثلي|بالخاص|خاص)", "DM"),
    (r"(واتساب|واتس|whatsapp)", "WhatsApp"),
    (r"(احفظ|احفظه|احفظها|سيف)", "save"),
    (r"(شارك|شاركه|دزه لـ|دزها لـ|منشن)", "share / tag"),
    (r"(تابعني|تابعنا|فولو)", "follow"),
    (r"(الرابط بالبايو|الرابط بالبايو|اللينك بالبايو|link in bio)", "link in bio"),
    (r"(اتصل|اتصلوا|رقمنا)", "call"),
]


def first_line(text):
    for l in text.splitlines():
        if l.strip():
            return l.strip()
    return ""


def lint(text, truncate, keywords):
    lex = iqtext.lexicon()
    visible = text.strip()[:truncate]
    flags, ok = [], []

    fl = first_line(text)
    n = iqtext.normalize(fl)
    if any(n.startswith(iqtext.normalize(g)) for g in lex["greetings"]):
        flags.append("first line is a greeting - the hook goes there")
    elif iqtext.count_hits(fl, lex["throat_clearing"]):
        flags.append("first line is throat-clearing")
    else:
        ok.append("first line goes straight in")
    if HASHTAG_RE.search(fl):
        flags.append("hashtag in the first line - wastes the visible window")

    if iqtext.has_number(visible) or iqtext.count_hits(visible, lex["baghdad_places"]) \
            or iqtext.count_hits(visible, lex["money_units"]):
        ok.append("visible window has something concrete")
    else:
        flags.append("nothing concrete before the cut - put the number or the place up top")

    found = sorted({name for rx, name in ASKS if re.search(rx, text, re.I)})
    if not found:
        flags.append("no ask - one clear action at the end")
    elif len(found) > 2:
        flags.append("asks: " + ", ".join(found) + " - pick one")
    else:
        ok.append("ask: " + ", ".join(found))

    tags = HASHTAG_RE.findall(text)
    if len(tags) > HASHTAG_LIMIT:
        flags.append(f"{len(tags)} hashtags - cap is {HASHTAG_LIMIT}")
    bad = [t for t in tags if t.lower() in FILLER]
    if bad:
        flags.append("filler hashtags: " + " ".join(bad))

    if LINK_RE.search(text):
        flags.append("raw link in caption - not clickable; move it to the bio or a DM keyword")

    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        a, l = iqtext.script_mix(s)
        if a and re.match(r"^[#@]?[A-Za-z0-9]", s) and not s.startswith("‏"):
            flags.append(f"line {i} starts with Latin text in an Arabic caption - renders left-aligned; start in Arabic or prefix RLM")

    if keywords:
        miss = [k for k in keywords if not iqtext.count_hits(visible, [k])]
        if miss:
            flags.append("search keywords not in the visible window: " + "، ".join(miss))
        else:
            ok.append("keywords in the visible window")

    if len(text) > LIMIT:
        flags.append(f"{len(text)} characters - over the {LIMIT} limit")

    return {"visible": visible, "length": len(text), "hashtags": tags, "flags": flags, "ok": ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--truncate", type=int, default=125)
    ap.add_argument("--keywords", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    kws = [k.strip() for k in a.keywords.split(",") if k.strip()]
    r = lint(text, a.truncate, kws)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2)); return
    print(f"FEED PREVIEW  (first ~{a.truncate} chars, approximate)")
    print("┌" + "─" * 44)
    for l in r["visible"].splitlines():
        print("│ " + l)
    print("│ … المزيد")
    print("└" + "─" * 44)
    print(f"{r['length']} chars · {len(r['hashtags'])} hashtags\n")
    for o in r["ok"]:
        print("  ✓ " + o)
    for f in r["flags"]:
        print("  ✗ " + f)


if __name__ == "__main__":
    main()
