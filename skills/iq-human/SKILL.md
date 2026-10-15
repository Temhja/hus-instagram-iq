---
name: iq-human
description: >-
  Humanizer for Arabic / Iraqi copy: strips invisible characters, tatweel,
  tashkeel and em dashes, flags stock "AI Arabic" phrases and fusha in spoken
  scripts with Iraqi rewrite directions, and scores the draft on a five-check
  panel. Use on every script, caption, DM or comment before it goes out, or
  when the user says "خليها طبيعية", "humanize this", "it sounds like AI",
  "make it sound Iraqi", or pastes AI-written Arabic.
---

# iq-human

Everything else in the pack runs its output through this before showing it.

```bash
python3 humanize.py draft.txt                     # report
python3 humanize.py draft.txt --fix -o draft.txt  # clean + report
python3 humanize.py caption.txt --mode caption    # caption register (lighter fusha allowed)
```

## What it does

**Fixes automatically** (mechanical, safe): zero-width spaces, BOM, soft
hyphens, bidi embeddings/overrides, tatweel (كـــبير), tashkeel (keeps shadda
by default because it shows pronunciation: سوّي), em/en dashes → «، ».

**Reports, never rewrites**: stock phrases (في عالم اليوم، يُعتبر، تعزيز،
رحلتك، أطلق العنان، حلول متكاملة…) each with an Iraqi direction; fusha words
in a spoken script (سوف، لذلك، يجب، هذه، ماذا…); LRM/RLM marks (often correct
in mixed lines, so they're kept and listed); AI-pattern emoji clusters.

**Five-check panel** (0–100 each, mean = human score, PASS ≥ 70):
register (Iraqi vs fusha markers), stock phrases per 100 words, typography,
rhythm (sentence-length variation), specificity (numbers, places, money).

This is a local heuristic. It is not GPTZero or any other detector and makes
no promise about their verdicts. Say so if the user asks.

## How to use it in a skill

1. Run with `--fix`.
2. Rewrite every reported stock phrase yourself, in the brand's voice. Don't
   swap one cliché for another; usually the fix is deleting the phrase and
   starting at the real sentence.
3. In `script` mode, rewrite reported fusha words into how the presenter
   actually says them (سوف أريك → راح اراويك, لماذا → ليش, يجب → لازم).
4. Re-run. Show the before/after score and the list of what changed.

## Register by brand

HUS personal brand: full Iraqi. Client brands: whatever their voice.md says.
A premium restaurant or a dental-equipment B2B brand may want clean,
light-MSA captions while their Reels stay Iraqi. Use `--mode caption` for that
and don't force dialect into a brand that doesn't speak it.

## Extending the lexicon

`lexicon.json` holds Iraqi markers, fusha markers, greetings, throat-clearing,
stock phrases with fixes, AI emoji, Baghdad places, money words, second-person
forms. When the user corrects a word (e.g. "always شيش, never سيخ"), add it to
the right list so every skill learns it.
