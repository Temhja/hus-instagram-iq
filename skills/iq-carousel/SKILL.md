---
name: iq-carousel
description: >-
  Write an Instagram carousel (swipe post) in Arabic / Iraqi: the cover that
  earns the swipe, slide-by-slide copy, design notes for RTL layout at
  1080×1350, and the caption hand-off. Use for "سويلي كاروسيل", "swipe post",
  "carousel about X", "slides for Instagram", or turning a Reel or article into
  a saveable post.
---

# iq-carousel

Reels reach strangers; carousels go deep with people who already follow and
get **saved**. Build for the save.

## Before writing

Read the brand's `voice.md` (and `plan.md` if this slot came from /iq-plan).
Ask for the one specific thing if the idea is thin: the number, the example,
the before/after.

## Structure (6–9 slides; 10 only if each slide earns it)

```
1  COVER     the promise in ≤ 7 words + a visual reason to swipe.
             Formula from ../iq-reel/hooks.json works here too
             (#18 القائمة, #6 شوف الغلط, #9 قبل وهسه are the strongest covers).
2  STAKE     why it matters / what it costs to get it wrong. One line + proof.
3–7 BODY     one point per slide. Headline ≤ 8 words, support ≤ 25 words.
             Each slide must make sense if screenshotted alone.
8  SUMMARY   the whole thing on one slide. This is the slide people save.
9  ASK       one action: احفظه / دزه لصاحبك / اكتب «كلمة» / واتساب.
```

## RTL design notes (hand to the designer as-is)

- **1080×1350** (4:5). Keep ~80px margins; the grid crops to a centered 3:4,
  so put the cover headline in the middle band.
- Instagram swipes forward the same way in every language: the next slide
  comes in from the right. Put the swipe cue at the **left edge** (←, or
  "اسحب ←") so it points where the next slide comes from, and where an
  Arabic reader's eye ends the line.
- Right-align all Arabic text. Never center long Arabic paragraphs.
- Choose one digit system per brand (١٢٣ or 123) and stick to it.
- Fonts with full dialect coverage (گ چ ڤ): Cairo, Tajawal, IBM Plex Sans
  Arabic, Almarai. Weight contrast for hierarchy, not five sizes.
- Mixed lines (Meta Ads, ROAS, CPM): check bidi order in the export; a Latin
  term at the line end often jumps sides.
- Continuity: a visual element that runs across the slide seam (a line, a
  shape cut in half) gives the eye a reason to swipe; use it on slides 1→2
  and test it against a clean cover in /iq-audit.
- Brand colors and type from the brand's design system if one exists.

## Rules

- Proof slides use the brand's real numbers or screenshots only. Blur client
  names and spend unless cleared.
- No slide is a paragraph. If it needs a paragraph, it's two slides.
- Run every slide's copy through `../iq-human/humanize.py --mode caption`.

## Output

```
CAROUSEL · 8 slides · brand: hus · cover formula #18

S1  COVER   «٣ أشياء قبل ما تصرف دينار على إعلان»
            visual: …   swipe cue: left edge
S2  …
…
DESIGN NOTES  …
CAPTION  run /iq-caption with: <one-line brief>
```

Offer to build the slides as a Design artifact or hand off to the designer.
