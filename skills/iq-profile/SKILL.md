---
name: iq-profile
description: >-
  Score an Instagram profile out of 100 against a 12-part rubric tuned for
  Iraqi personal brands and Baghdad businesses (name-field search terms,
  WhatsApp contact, location/hours, buyer-question highlights), then rewrite
  it in fix-first order. Use for "قيّم بروفايلي", "audit my profile", "fix my
  bio", "optimize the Instagram page" for HUS or a client, or as the
  first deliverable when onboarding a new client.
---

# iq-profile

A stranger who arrives from one Reel decides in a few seconds whether to
follow or message. This scores what they see and fixes the expensive parts
first.

## Input

Ask for (or read from a screenshot / the user's browser, with them present):
name field, handle, bio, link, contact buttons, location, highlights (names
and order), the three pinned posts, last post date, the first 9 grid covers,
and the brand's goal (followers, DMs, WhatsApp orders, bookings).

Read `rubric.json`. Score each item honestly with one line of evidence.
Generous scores help nobody; most first-pass profiles land in the 30s–40s.

## Rewrite in fix-first order

Sort items by points lost, highest first, and rewrite:

1. **Name field**: 2–3 versions, each with a searchable Arabic term
   (+ one English term if the audience searches it). Check the live
   character counter in the app; limits change.
2. **Bio**: 3 versions in the brand's voice. Line 1 = who + outcome;
   line 2 = proof or offer + area; line 3 = the ask. Run each through
   `../iq-human/humanize.py --mode caption`.
3. **Highlights**: the set, names, order, and what goes in each.
4. **Pinned three**: which existing posts, or what to make if none qualify.
5. Everything else as a checklist.

## Rules

- No invented proof ("+500 عميل") unless voice.md lists it.
- Prices only if the brand publishes them.
- A client account is the client's voice, not HUS's.
- Don't change the handle unless it scores 0; a handle change breaks
  existing links and tags. Say what it costs if you recommend it.

## Output

```
PROFILE SCORE  46 / 100  ·  brand: <brand>

 4/12  name_field        "<current>"  - name only, no search term
 ...

FIX FIRST
 1. name field  (+8)   options: …
 2. bio         (+7)   options: …
 3. whatsapp    (+6)   …

AFTER FIXES  est. 78 / 100
```

For a new client, offer to turn the report into a one-page onboarding doc.
