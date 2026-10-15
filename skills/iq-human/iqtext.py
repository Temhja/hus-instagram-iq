"""
iqtext.py - shared Arabic text helpers for the Iraqi Instagram pack.

Standard library only. No network. Imported by hookscore.py, beats.py,
caption.py, humanize.py and swipe.py, which look for it in their own folder
first and then in the sibling iq-human/ folder.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

TASHKEEL = re.compile(r"[ً-ْٰ]")
TATWEEL = "ـ"
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
WORD_RE = re.compile(r"\w+", re.UNICODE)
ARABIC_LETTER = re.compile(r"[ء-يٱ-ۓ]")
LATIN_LETTER = re.compile(r"[A-Za-z]")

# Invisible / control characters. Grouped by how the humanizer treats them.
STRIP_ALWAYS = {
    "​": "zero-width space",
    "⁠": "word joiner",
    "﻿": "byte-order mark",
    "­": "soft hyphen",
    "᠎": "mongolian vowel separator",
    "‪": "LRE (bidi embedding)",
    "‫": "RLE (bidi embedding)",
    "‬": "PDF (bidi pop)",
    "‭": "LRO (bidi override)",
    "‮": "RLO (bidi override)",
}
REPORT_ONLY = {
    "‌": "ZWNJ",
    "‍": "ZWJ",
    "‎": "LRM",
    "‏": "RLM",
    "⁦": "LRI", "⁧": "RLI", "⁨": "FSI", "⁩": "PDI",
}
# LRM / RLM / isolates are legitimate in mixed Arabic-English lines (they stop
# "Meta Ads" or a price from jumping to the wrong end of the line). Report
# them, never strip them silently.


def find_lexicon():
    for d in (HERE, os.path.join(os.path.dirname(HERE), "iq-human")):
        p = os.path.join(d, "lexicon.json")
        if os.path.exists(p):
            return p
    raise FileNotFoundError("lexicon.json not found next to this script or in ../iq-human/")


_LEX = None


def lexicon():
    global _LEX
    if _LEX is None:
        with open(find_lexicon(), encoding="utf-8") as f:
            _LEX = json.load(f)
    return _LEX


def normalize(text):
    """For matching only. Never use the result as output."""
    t = TASHKEEL.sub("", text).replace(TATWEEL, "")
    t = re.sub("[أإآ]", "ا", t)
    t = t.replace("ى", "ي").replace("ة", "ه")
    t = t.translate(ARABIC_DIGITS)
    for ch in list(STRIP_ALWAYS) + list(REPORT_ONLY):
        t = t.replace(ch, "")
    return t


def words(text):
    return WORD_RE.findall(normalize(text))


def phrase_regex(phrase):
    """Match a phrase as whole words, allowing one Arabic proclitic (و ف ب ل ك)
    and the article (ال) on the first word."""
    p = normalize(phrase)
    if p.startswith("\\") or p in ("%", "٪"):
        return re.compile(re.escape(p) if p in ("%", "٪") else p)
    return re.compile(r"(?<!\w)(?:[وفبلك])?(?:ال)?" + re.escape(p) + r"(?!\w)")


def count_hits(text, phrases):
    """Return [(phrase, count)] for every phrase present. Spelling variants
    that normalize to the same form are counted once."""
    n = normalize(text)
    out, seen = [], set()
    for ph in phrases:
        key = normalize(ph)
        if key in seen:
            continue
        seen.add(key)
        c = len(phrase_regex(ph).findall(n))
        if c:
            out.append((ph, c))
    return out


def has_number(text):
    return bool(re.search(r"\d", normalize(text)))


def script_mix(text):
    a = len(ARABIC_LETTER.findall(text))
    l = len(LATIN_LETTER.findall(text))
    return a, l


def dialect_ratio(text):
    """(iraqi_hits, fusha_hits, ratio 0..1 where 1 = fully Iraqi)."""
    lex = lexicon()
    iq = sum(c for _, c in count_hits(text, lex["iraqi_markers"]))
    # Words written with گ or چ, or carrying the هال- demonstrative prefix
    # (هالفيديو, هالغلط), are Iraqi spellings by definition.
    for w in WORD_RE.findall(TASHKEEL.sub("", text)):
        if ("گ" in w or "چ" in w or (w.startswith("هال") and len(w) > 4)) \
                and normalize(w) not in {normalize(m) for m in lex["iraqi_markers"]}:
            iq += 1
    fu = sum(c for _, c in count_hits(text, lex["fusha_markers"]))
    if iq + fu == 0:
        return iq, fu, None
    return iq, fu, iq / (iq + fu)
