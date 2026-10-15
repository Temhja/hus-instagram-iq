---
name: iq-caption
description: >-
  Write an Instagram caption in Iraqi Arabic (or bilingual Arabic/English) and
  show exactly what the feed shows before "المزيد". Use for "اكتبلي كابشن",
  "write the caption", "caption for this reel/post", hashtag choice, or when a
  Reel or carousel script is ready and needs its caption.
---

# iq-caption

The caption has one job above the cut and one job below it. Above: make the
scroller tap "المزيد" or stay on the video. Below: deliver, then one ask.

```bash
python3 caption.py caption.txt --keywords "اعلانات ممولة,بغداد"
python3 ../iq-human/humanize.py caption.txt --mode caption --fix -o caption.txt
```

## Before writing

Read `~/.claude/instagram-iq/brands/<brand>/voice.md` (or the Project doc
`ig/<brand>/voice.md`). It sets the register: HUS speaks Iraqi; a luxury or
B2B client may want lighter, cleaner Arabic. The register is the brand's
call, not a default.

## Structure

```
LINE 1      the hook restated for reading: number / place / tension.
            Never السلام عليكم, never a hashtag, never "شوفوا الفيديو".
LINE 2–3    the stake, still above the cut if possible.
— cut (~125 chars, approximate) —
BODY        the payoff in 2–5 short lines. Line breaks, not paragraphs.
ASK         one action. For lead gen in Iraq the strongest default is a
            keyword comment that triggers a DM, then WhatsApp:
            اكتب «سعر» بالتعليقات وأدزلك التفاصيل بالخاص.
TAGS        ≤ 5 targeted hashtags (Arabic + English if the audience searches
            both). Never #اكسبلور #explore #viral.
```

## Search

Instagram search reads captions. Put 1–2 phrases people actually type in the
first lines, in the spelling they type: often Iraqi spelling without hamza
(اعلانات not إعلانات) or English for technical terms (Meta Ads). If unsure
which spelling people search, write both naturally once.

## Bidi hygiene

A line that starts with English inside an Arabic caption renders
left-aligned and breaks the block. Start the line in Arabic, or prefix an RLM.
`caption.py` flags it.

## Rules

- One idea, one ask. Two asks halve both.
- Numbers and places over adjectives. No invented results, prices or
  testimonials. Unknown → `{{رقم}}` and flag it.
- Prices: if the brand doesn't post prices publicly, the ask is "dm/WhatsApp
  for the price", never a made-up range.
- Emoji: follow voice.md. Default zero or one; never 🚀✨💡 clusters.
- Run the linter and the humanizer; fix every ✗ before showing the user.

## Output

Show the feed preview box from `caption.py`, the full caption in a code block
(so RTL copy-paste stays clean), the checks, and offer two alternate first
lines with different formulas.
