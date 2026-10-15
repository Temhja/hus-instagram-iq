---
name: iq-audit
description: >-
  Post-mortem on what HUS or a client brand already posted: rank posts by
  outlier multiple against the account's own median, connect results to the
  hook formula and format used, read the Insights metrics that matter
  (views, watch time, skip rate if shown, shares, saves, follows, DMs), and
  say what to make more of and what to stop. Use for "شنو اشتغل", "audit my
  last month", "monthly report", "why did this flop", or a client
  performance review.
---

# iq-audit

The pack's feedback loop. /iq-plan and /iq-reel get better only if this runs.
Monthly per brand; weekly during a campaign.

## Input

- `brands/<brand>/log.md` (what was planned: formula, hook, length).
- Performance per post: pasted Insights, a Metricool export, or Metricool
  directly if connected (read-only). Ask for whatever exists; never estimate
  missing numbers.

Per post, collect what's available:
views · reach · avg watch time · total watch time · skip rate (Instagram
shows this on Reels in some accounts; use it if present) · shares · saves ·
comments · follows from post · profile visits · DMs/WhatsApp leads (from the
team, not Instagram).

## Method

1. **Baseline** = median views of the brand's last 20–30 posts of the same
   format. Each post's multiple = views ÷ baseline.
2. **Rank** by multiple. Top third vs bottom third: which formulas, lengths,
   formats, presenters, first frames, topics.
3. **Retention read** (Reels): avg watch time ÷ length. Low with high views =
   hook worked, body didn't. High skip rate = first frame/hook failed.
4. **Business read**: shares + saves per 1K views (content value) and
   follows / DMs per 1K views (commercial value). For HUS and for clients,
   DMs and WhatsApp leads outrank views.
5. **Confidence**: say the sample size. 8 posts is a hint, not a pattern.
   Never call a difference between two posts a "finding".

## Output

```
AUDIT · brand: hus · Sep 15 – Oct 15 · 14 Reels · baseline 3.1K views

TOP
  6.2x  #3 محد يگلك      28s  watch 61%  saves 22/1K  DMs 9
  …
BOTTOM
  0.4x  unclassified     52s  watch 18%  greeting opener
  …

MORE OF   #3 and #6 hooks, sub-35s, screen-recording Meta Ads format
STOP      greetings / logo intros, 50s+ talking heads
TEST      #19 (reading a real comment) - not used yet, works in swipe.md
CONFIDENCE  14 posts - directional
```

Append the summary to `log.md` and hand MORE/STOP/TEST to /iq-plan. For a
client, offer to turn it into the monthly client report.
