---
name: iq-engage
description: >-
  Handle Instagram engagement in Iraqi Arabic: triage comments under the
  brand's own posts (keyword / "بكم" price ask / lead / question / support /
  spam), draft every reply and the DM that follows, write comments on other
  accounts' posts, and move buyers from DM to WhatsApp. Use for "رد على
  التعليقات", "reply to my comments", "draft the DMs", "people asking بكم",
  "comment on this post", "collab pitch", or follow-up messages.
---

# iq-engage

Three jobs: the thread under your post, the DMs it creates, and the comments
you leave elsewhere. **This skill drafts. The user sends.** Never send, post
or reply on the user's behalf.

## Before writing

Read the brand's `voice.md` (the keyword CTA and what it delivers live
there). For a client brand, also confirm: is pricing public? who handles
WhatsApp? what are the opening hours?

## 1. The thread under the brand's post

Sort every comment into one bucket, then draft:

| bucket | signal | public reply | then |
| --- | --- | --- | --- |
| **keyword** | typed the CTA word | short confirm: «دزيتلك بالخاص 👌» | DM delivers what was promised, immediately |
| **price** | بكم / السعر / شگد | never "راسلنا خاص" alone. Give a public anchor if allowed («تبدي من {{سعر}}، التفاصيل بالخاص»), else «دزيتلك السعر بالخاص» | DM the price + one question |
| **lead** | describes a need / asks to book | warm one-liner, no pitch | DM, qualify, move to WhatsApp |
| **question** | how / why | answer publicly; it helps every reader | optional DM |
| **praise / support** | thanks, emoji, tags | a real reply, not "شكراً حبيبي" ×20 | none |
| **critic / complaint** | negative | calm, factual, offer to fix in DM. Never argue publicly | DM, escalate to owner |
| **spam / troll** | links, bots, insults | none: hide, don't reply | flag to user |

The "بكم" reply matters most in Iraq: a public "راسلنا خاص" with no follow-up
loses the buyer. If the brand won't post prices, the DM must land within
minutes. Say so if the brand's setup can't do that, and recommend an
auto-reply on the keyword (drafted here, configured by the user).

Output the thread as a table: comment → bucket → public reply → DM draft.

## 2. DMs

- **Keyword delivery**: deliver first, then one question. No essay.
- **First message to a lead**: their words back to them + one qualifying
  question (budget, timeline, location in Baghdad).
- **WhatsApp handoff** when there's intent: «حتى أدزلك النماذج والأسعار، هذا
  رقمنا على الواتساب: {{رقم}}». Use only the number from voice.md.
- **Follow-ups**: two max, 2 and 5 days apart, each adding something new.
- **Collab pitch**: what you'll make for them, why their audience, one
  specific idea. No "نحب نتعاون وياكم".

## 3. Comments on other accounts

Nine types; pick by what the post actually is:
add a number · add a counter-example · ask the sharp follow-up · share the
mistake you made with this · agree and extend with a Baghdad specific ·
respectful disagreement · summarize the post in one line · tag the use case ·
answer someone else's question in the thread.
Never "🔥🔥", never a pitch, never a link. Write something the creator might
pin. In Arabic threads, comment in the thread's register.

## Rules

- Run every draft through `../iq-human/humanize.py --mode caption`.
- No invented prices, availability, delivery times or discounts.
- Confidential client details stay out of public replies.
- Gender and form of address: default to the neutral/masculine Iraqi form
  unless the commenter's name or profile makes it clear; when it does,
  address them correctly (حبيبي / حبيبتي, عيني works for both).
