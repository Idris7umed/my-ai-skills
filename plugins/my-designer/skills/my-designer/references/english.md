# English carousels

## Tone

Match the user. If they write casually, write casually; if the brand is B2B or the request mentions LinkedIn, use a professional, direct tone. Save the choice as `tone_en` in `brand.json`.

- Short words, active verbs, second person ("you"). Cut "very", "really", "in order to", "it's important to".
- Sentence case for headlines, not Title Case — it reads faster and feels less like an ad.
- No hashtags or emoji on the slides themselves; they belong in the caption.
- Avoid clichés that signal generic content: "game-changer", "unlock", "level up", "in today's fast-paced world", "let's dive in".

## Hook patterns for the cover

| Pattern | Example |
|---|---|
| Curiosity question | Why does coffee make you *more* tired? |
| Number + promise | 7 habits that actually stick |
| Contrarian claim | Stop *journaling* every morning |
| Mistake | You're *storing* bread wrong |
| Before → after | From 0 to *10k* followers in 90 days |
| "Nobody tells you" | What nobody tells you about *freelancing* |

The italicized word is the highlight candidate. The cover headline should be under 9 words.

## Slide 2

Either deliver the promise immediately ("Here's the short answer: …") or name the pain sharply ("You sleep 8 hours and still wake up tired."). Never spend slide 2 on an introduction.

## Typography

- Inter 900 headlines with tight tracking (`-0.03em`, set by the template) and line height ~1.04; body at 600 weight.
- English sets wider than Arabic at the same size. If a cover headline wraps to 4 lines, step down to `h-xl`.
- Highlight one whole word or a short 2-word phrase. `white-space: nowrap` on `.hl` keeps it on one line, so don't highlight long phrases.
- Numbers in lists: `01 02 03` (the template's `.n`) reads more designed than `1. 2. 3.`

## Caption pack (English)

- First line: a second hook that works on its own before "…more" (under ~125 characters).
- Body: 2–4 short lines, white space between them.
- One CTA matching the last slide.
- 3–5 hashtags: one broad, the rest specific to the niche. On LinkedIn, 3 max.
- Alt text: one plain sentence per slide describing what it says, for screen readers.
