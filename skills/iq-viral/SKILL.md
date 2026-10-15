---
name: iq-viral
description: >-
  Find the reels that are actually over-performing in an Iraqi / Arab niche,
  rank them by how far each beat its OWN account's median (outlier multiple),
  name the Iraqi hook formula, and turn the winners into original scripts for
  HUS or a client brand. Use for "شنو دا يمشي", "find viral reels", "what's
  working in my niche", "reverse-engineer this account", "build a swipe file",
  "why is this reel doing numbers", or competitor content research for a
  client pitch.
---

# iq-viral

The research skill. Everything else writes; this one looks. Run it monthly
per brand, not daily. Formulas last a season.

```bash
python3 swipe.py captured.tsv --out ~/.claude/instagram-iq/brands/<brand>/swipe.md
```

## The idea

**Raw views are not evidence.** 400K on a 2M-follower account is a quiet day.
400K on a 6K-follower Baghdad account found something copyable. Rank on the
**outlier multiple** = views ÷ that account's recent median. Above 3x is a
signal. Under 1.5x is that account's normal day.

Collect accounts within ~10x of the brand's own size. A formula that works at
2M followers often works *because* of the 2M followers.

## Step 1: the account list (6–12, user approves)

- **4 direct**: same niche, same city or country, slightly ahead.
  For HUS: Iraqi marketing / ads / agency creators. For a client: its direct
  Baghdad competitors.
- **4 adjacent**: different niche, same audience. Formats get borrowed from
  here before the niche has them. Include at least one Gulf and one
  Levant/Egypt account; formats often reach Iraq from there first.
- **2–4 outsized**: big Arab or global accounts, for **format only**, never
  tone, cadence or dialect.
- Ask the user to open **their own Saved collection** too. It's pre-filtered
  by their taste.

## Step 2: look (reading, not scraping)

Use whatever browser tool this session actually has (Claude in Chrome, the
built-in browser, or the user pasting). Non-negotiable:

- **Never log in to Instagram for the user and never ask for a password.**
  Use the browser where they're already signed in, with them present, or
  have them paste.
- **Human speed, small volume.** ~10 accounts × ~12 reels. No crawler, no
  scraping service, no background loop. Automated collection breaks
  Instagram's terms and gets accounts action-blocked.
- **Copy the formula, never the video.** Attribute every row to its account.

Capture per reel (hook **verbatim, in their dialect, typos included**):

| column | notes |
| --- | --- |
| account | handle |
| followers | from the profile (12K / 1.2M fine) |
| median | eyeball the last 12 reels, take the middle view count |
| views | this reel |
| hook | first spoken line, or first text card if silent |
| length / cta / url | optional |

Median is the column that matters. Without it you're ranking by follower
count again.

## Step 3: rank

TSV with a header row, then run `swipe.py`. It computes the multiple,
classifies each hook against the 20 Iraqi formulas in `../iq-reel/hooks.json`,
scores it with `hookscore.py`, compares top third vs bottom third, and lists
unclassified hooks.

## Step 4: report three things, carefully

1. **Which formulas over-index** in the top third, with counts.
2. **What the top third share structurally** that the bottom doesn't: hook
   length, dialect vs fusha, payoff on screen vs in words, face vs
   screen-recording, where the ask sits.
3. **The unclassified rows.** Read them by hand. A shape that repeats is a
   formula missing from `hooks.json`; propose adding it with a regex.

State the sample size and confidence in plain words (the script prints it).
40+ reels across 6+ accounts supports a claim; 12 reels is anecdote.

## Step 5: make it shootable

For the top three formulas, write **the brand's own version**: its story, its
number, its dialect, in the shape that's working. Hand each to `/iq-reel` with
the formula id chosen. Never return "make one like this"; return a hook line
they could say tomorrow.

## Client-pitch mode

For a prospect (not yet a client): run the same process on the prospect's
competitors, then output a one-page finding: who is over-indexing, with what
formula, and 3 hook lines the prospect could own. Facts only, attributed,
no invented numbers.

Nothing is posted, followed, liked or messaged by this skill. It reads.
