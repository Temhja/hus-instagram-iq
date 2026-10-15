# HUS Instagram IQ

Ten Claude skills that run Instagram **in Iraqi Arabic**, for HUS and for
every agency client. Built on HUS's own script framework
(HOOK → LEAD → BODY → OPEN LOOP → CTA), 20 Iraqi hook formulas, an Arabic
humanizer, and outlier-multiple research. Multi-brand: one `voice.md` per
brand.

**Nothing gets posted until a human says yes.** The skills write and analyse.
People post.

## The ten

| command | job |
| --- | --- |
| `/iq-reel` | One idea → 3 scored Iraqi hooks → tagged script → on-screen cards → timed beat sheet. Also repurposes long content into Reel briefs. |
| `/iq-viral` | Ranks niche reels by outlier multiple (views ÷ the account's own median), names the Iraqi formula, writes the swipe file. Client-pitch mode included. |
| `/iq-caption` | Caption with a feed-cut preview, one ask, ≤5 hashtags, bidi checks. |
| `/iq-carousel` | Cover + slides + RTL design notes for 1080×1350. |
| `/iq-story` | Daily story sequence, sticker by job, DM → WhatsApp funnel. |
| `/iq-engage` | Comment triage (keyword / "بكم" / lead / question / complaint / spam), replies, DMs, WhatsApp handoff, comments on other posts. |
| `/iq-profile` | 12-part score out of 100 (WhatsApp, location, buyer highlights), fix-first rewrite. |
| `/iq-plan` | The week per brand: angles, formats, formulas, test windows, Iraqi calendar flags, engagement list. |
| `/iq-audit` | Post-mortem by outlier multiple + retention + DMs per 1K views. Feeds /iq-plan. |
| `/iq-human` | Arabic humanizer: strips invisible chars / tatweel / tashkeel / em dashes, flags stock "AI Arabic" and fusha, enforces house terms. |

## Tools (Python 3, standard library only, nothing uploaded)

```
iq-reel/hookscore.py    score hooks 0-100 with reasons
iq-reel/beats.py        timed beat sheet + framework checks
iq-caption/caption.py   feed preview + 8 checks
iq-viral/swipe.py       outlier ranking + formula classification
iq-human/humanize.py    clean + five-check human score
iq-human/lexicon.json   Iraqi/fusha markers, stock phrases, house terms (extend it)
iq-reel/hooks.json      the 20 formulas (extend it from /iq-viral findings)
```

## Install

**Easiest: paste this into Claude Code**

```
https://github.com/Temhja/hus-instagram-iq

Install this skill pack, then confirm /iq-reel works.
```

**Claude Code, as a plugin**

```
/plugin marketplace add Temhja/hus-instagram-iq
/plugin install hus-instagram-iq
```

**Claude Code, by hand**

```bash
git clone https://github.com/Temhja/hus-instagram-iq.git
cp -r hus-instagram-iq/skills/iq-* ~/.claude/skills/
```

Install all ten together; the tools share files across folders.

**Claude app (desktop / web)**: zip each `skills/iq-*` folder and upload it under
Settings → Capabilities → Skills. For `iq-reel`, `iq-caption` and `iq-viral`,
first copy `iq-human/iqtext.py` and `iq-human/lexicon.json` into the folder
(and for `iq-viral` also `iq-reel/hookscore.py` and `iq-reel/hooks.json`), so
each zip works on its own.

Then fill `templates/voice.md` for your brand, or send Claude three of your
own reels and say «اكتب voice.md من هذني».

## Brands

```
~/.claude/instagram-iq/brands/
  hus/        voice.md  swipe.md  log.md  plan.md
  <client>/   voice.md  …
```

Say the brand in the request ("/iq-reel for alareesha: …"); default is `hus`.

## Honest limits

- Hook scores and human scores are local heuristics, not view predictions or
  third-party AI-detector verdicts.
- Speech timing defaults to 130 wpm, an estimate. Measure the presenter.
- The feed cut (~125 chars), the 5-hashtag cap and safe-zone pixels are
  approximations of a UI Instagram changes; re-check periodically.
- No posting time is presented as fact for Iraqi audiences; /iq-plan gives
  windows to test.

## Credit

Structure adapted from "The Instagram agent skill" by Jake Schincariol (MIT).
Iraqi formulas, lexicon, tools and workflows are new. See LICENSE.
