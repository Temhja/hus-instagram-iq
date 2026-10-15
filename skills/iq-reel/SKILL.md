---
name: iq-reel
description: >-
  Write an Instagram Reel in Iraqi (Baghdadi) Arabic from one raw idea: three
  scored hooks from 20 Iraqi formulas, the spoken script in the HUS framework
  (HOOK > LEAD > BODY > OPEN LOOP > CTA), separate on-screen text, and a timed
  beat sheet. Use for "اكتبلي ريل", "make a reel about X", "script for a
  video", "I need a hook", a voiceover, or any short-form video script for HUS
  or an agency client. Also handles repurposing: one long video, podcast or
  post into several Reels.
---

# iq-reel

One idea in, a Reel someone finishes out. Spoken Iraqi, not written fusha:
the presenter has to say every line out loud in one take.

Tools in this folder (stdlib Python, nothing uploaded):

```bash
python3 hookscore.py hooks.txt                 # rank hook options, one per line
python3 hookscore.py --hook "محد يگلك إن…"     # score one
python3 beats.py script.txt --target 30 --wpm 135   # timed beat sheet + flags
python3 ../iq-human/humanize.py script.txt --fix -o script.txt
```

## Brand and files

Every run is for one **brand** (default `hus`; agency clients get their own
slug, e.g. `alareesha`, `winway`, `lightric`). Files live in
`~/.claude/instagram-iq/brands/<brand>/`:
`voice.md` (read first), `swipe.md` (from /iq-viral), `log.md`, `plan.md`.
In claude.ai with no filesystem, look for Project docs named
`ig/<brand>/voice.md` etc.; if they are not there, ask the user to paste them.

## Before writing

1. **Read `voice.md`.** No voice file → ask for three of the brand's own
   reels or captions, infer the voice, write the file from
   `templates/voice.md`. A client brand speaks as the brand, not as HUS.
2. **Read `hooks.json`.** 20 formulas: template, Iraqi example, on-screen
   card, what it's for, how it gets ruined.
3. **Read `swipe.md` if it exists.** It's the brand's own evidence of what's
   over-indexing in its niche right now and outranks the defaults.
4. **Thin idea → one batched question:** what happened, to whom, what did it
   cost or return (رقم، مكان، زبون). Get one specific true thing before writing.

## The shape (HUS framework)

```
[HOOK]       0–3s    the claim. Spoken line + on-screen card, written separately.
                     Motion in frame 1. No greeting, no name, no logo sting.
[LEAD]       3–7s    why this viewer should care. One line.
[BODY]       7s–     one idea per beat; the frame changes every beat.
                     Deliver what the hook promised before the halfway mark.
[OPEN LOOP]  last 5s tease the next video or the payoff in the comments,
                     so following has a reason. (بالفيديو الجاي راح اراويك…)
[CTA]        last 3s ONE ask. Keyword comment, DM, WhatsApp, save, or follow.
```

Default length 30s (HUS's standard). Working range 15–45s.

## The loop

1. **Three hooks, three different formulas.** Spoken line + on-screen card
   each. Not three rewrites of one.
2. **Score them** with `hookscore.py`. Show the ranking with reasons. Top
   under 50 → you don't have the hook; rewrite instead of polishing.
3. **Write the script** on the winner, tagged with the five section tags.
   Short lines, the way the presenter talks. Contractions and dialect
   spelling (گ، چ، هسه، شنو، هواية، مو). One line = one beat = one cut.
4. **Time it**: `beats.py --target {length} --wpm {voice.md pace}`. The 130
   wpm default is an estimate, not a measured Iraqi norm; if voice.md has no
   measured pace, say timings are approximate. Fix every flag and re-run.
5. **Humanize**: `humanize.py --fix`. Rewrite every stock phrase it reports.
   Target ≥ 70.
6. **Print the block** (format below).
7. **Never publish.** On "yes", append to `log.md`: date, brand, formula id,
   hook line, target length.

## On-screen text is its own script

- ≤ 6 words per card. Arabic reads right-to-left; keep cards right-aligned
  and never split a phrase across a line break mid-idiom.
- Hook card up at frame 1.
- Safe zone on 1080×1920: keep text between y≈230 and y≈1440 and clear of the
  right-side action rail. These are approximations of Instagram's UI overlay;
  check against a real upload.
- Burned-in captions for the body (most first watches are muted). Use a font
  with clean Arabic numerals and dialect letters گ/چ (Cairo, Tajawal,
  IBM Plex Sans Arabic). Pick Arabic-Indic or Western digits per brand and
  never mix them in one video.
- Mixed Arabic/English cards (Meta Ads, ROAS): check the bidi order on a real
  phone; an English term at a line edge often jumps to the wrong side.

## Rules

- **One idea per Reel.** Two ideas = two Reels. Say so.
- **Numbers over adjectives.** هواية is not a number. Unknown number →
  leave `{{رقمك}}` and flag it. **Never invent** a client, figure, result or
  testimonial, for HUS or any client brand.
- **Real places beat generic ones**: المنصور، الكرادة، شارع فلسطين.
- **Client confidentiality**: no client names, spend or results on screen
  unless voice.md for HUS lists them under "proof I can use".
- **Sensitive calendar**: in Muharram (especially Ashura) and around Arbaeen,
  default to no comedy, no music-driven trend formats, no hard sell for
  Baghdad audiences. Flag it if the requested publish date falls there.
- **Copy the formula, never the video.** If the idea came from someone else's
  reel, same structure, the brand's own story and words.

## Repurpose mode

Given a long video, podcast transcript, talk or long post: pull every
standalone moment that has a number or a turn, rank by hook potential with
`hookscore.py`, and return the top 3–5 as Reel briefs (formula, hook,
one-line body, source timestamp). Only write full scripts for the ones the
user picks.

## Output

```
HOOKS (scored)
  90 STRONG  #3 محد يگلك       "محد يگلك إن أول ٢٠ إعلان إلك لازم يفشلون."
                                card: محد راح يگلك هذا
  75 STRONG  #1 اعتراف بالخسارة  "…"
  58 OK      #18 القائمة         "…"

Shooting #3: <why, in one line>

[script block with section tags]

ON-SCREEN
  0.0s  محد راح يگلك هذا
  …

REEL READY
brand:      hus
hook:       #3 scored 90 STRONG
length:     29.4s · 10 beats · 135 wpm (measured | estimated)
humanizer:  2 fixes · score 86 PASS
next:       /iq-caption

Reply "yes" to log it, or tell me what to change.
```
