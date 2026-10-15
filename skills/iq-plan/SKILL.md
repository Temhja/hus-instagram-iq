---
name: iq-plan
description: >-
  Plan the Instagram week for HUS or a client brand: what to post each day,
  which format, which hook formula, posting windows to test, the daily
  engagement list, and the Iraqi calendar checks (Friday weekend, Ramadan,
  Eids, Muharram/Ashura, Arbaeen, national exam periods). Use for "خطط
  الأسبوع", "plan my week", "content calendar", "what should we post", or a
  multi-brand weekly plan across agency clients.
---

# iq-plan

The control room. Run once a week, same day, per brand (or one pass across
all active brands).

## Input

Read for the brand: `voice.md`, `swipe.md` (from /iq-viral; outranks
anything here), `log.md` (don't repeat a theme from the last 2 weeks),
last week's `/iq-audit` result if any.

Then ask one batched question if missing:
1. What actually happened this week (shoots, client results, a mistake, a
   new service, a question clients keep asking)? Posts come from here.
2. How many posts can the team realistically produce (shoot + edit)?
3. Any dates, launches or client deadlines this week?

## The mix (4–5 posts, ≥ 3 Reels)

| type | per week | job |
| --- | --- | --- |
| **Proof** | 1 | a real result with a number. Reel. |
| **Teach** | 1–2 | one thing they can do today. Reel or carousel. |
| **Opinion** | 1 | a position some of the audience disagrees with. Reel. |
| **Story** | 1 / fortnight | agency or brand life with a cost or a turn. Reel. |
| **Offer** | 1 / fortnight | what you sell, plainly, with the ask. Carousel or stories. |

For HUS, map types onto the four content pillars (Meta Ads education as
screen recordings, general marketing, client acquisition, restaurant
marketing). Never two of the same type back to back.

Each slot = angle (not topic) + format + formula id from
`../iq-reel/hooks.json` + who shoots/edits it. "إعلانات" is a topic.
"المطعم الي ضيّع ٤٠ زبون لأن رد 'راسلنا خاص'" is an angle.

## When to post

There is no reliable published "best time" for Iraqi audiences. Do not state
one as fact. Instead:
- If the brand has Insights (Metricool connected, or the user pastes the
  "most active times" chart), use those.
- Otherwise give **windows to test** for two weeks and log results: evenings
  (after work and after dinner, Baghdad time) for consumer brands; morning
  and early afternoon on Sun–Thu for B2B. Label them as hypotheses.
- Iraq's weekend is Friday–Saturday. Weekly rhythm follows that, not Mon–Fri.
- Say plainly: the hook matters far more than the hour.

## Calendar checks (flag, don't decide)

- **Ramadan**: activity shifts late; content tone shifts; food brands plan
  around iftar and suhoor. Confirm dates for the current year.
- **Eid al-Fitr / Eid al-Adha**: greetings posts are expected; schedule
  ahead; teams are off.
- **Muharram (esp. Ashura) and Arbaeen**: many Baghdad audiences and brands
  pause entertainment content; no music trends, no hard promos. Check the
  brand's own policy.
- **Ministerial exam periods**: Iraq has cut internet during national
  exams in past years. Check the current year's schedule before planning
  launches.
- National days and the brand's own dates (anniversaries, openings).
Give dates only when verified for this year; otherwise say "confirm the date".

## Engagement list (20 min/day, before posting)

10 accounts: 5 reach (bigger Iraqi/Arab accounts the buyers follow),
3 peers (same size, same field), 2 buyers (actual prospects: restaurant
owners, clinics, retailers in Baghdad). Hand to /iq-engage for comments.
Never pitch a buyer in a comment.

## Output

```
WEEK OF <date>  ·  brand: hus  ·  capacity: 4 Reels + 1 carousel

SAT  —
SUN  REEL      TEACH    #18  ٣ أشياء قبل أول إعلان      shoot: HUS · edit: designer
MON  stories + engage
TUE  REEL      PROOF    #5   ٤٠٠ طلب لمطعم بشارع فلسطين  (client cleared? ✓/✗)
WED  CAROUSEL  TEACH    #6   شوف الغلط بهالإعلان
THU  REEL      OPINION  #10  اللوگو ما يبيع
FRI  —

TEST WINDOWS  …(hypotheses, log results)
CALENDAR      …flags
ENGAGE        5 reach / 3 peers / 2 buyers
```

Write to `brands/<brand>/plan.md` (or the Project doc). Nothing is scheduled
or posted. If Metricool is connected and the user asks, offer to create
drafts **for review** only after they approve each post.
