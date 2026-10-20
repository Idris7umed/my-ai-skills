# Arabic carousels

## Dialect

Write in the user's dialect. Detect it from their message; if they write in MSA or you can't tell, use a light, friendly MSA that any Arab reader understands. Never mix two dialects in one carousel.

| Dialect | Signals in the user's message | Example hook |
|---|---|---|
| Gulf / Saudi | وش، ليش، كذا، يبي، زين، مره | وش الفرق بين…؟ |
| Egyptian | إيه، ليه، كده، عايز، أوي، بتاع | إيه الفرق بين…؟ |
| Levantine | شو، ليش، هيك، بدّي، كتير | شو الفرق بين…؟ |
| Maghrebi | واش، علاش، هكا، بغيت | واش الفرق بين…؟ |
| MSA | formal grammar, ما، لماذا | ما الفرق بين…؟ |

Keep technical terms people actually say in English as English (API, AI, ChatGPT, iPhone) — wrapped in `<bdi>`. Don't force awkward Arabic coinages on a social audience.

Swipe word and CTA by dialect: Gulf `اسحب` / `احفظه وارسله لأحد يحتاجه`; Egyptian `اسحب` / `احفظه وابعته لحد محتاجه`; Levantine `اسحب` / `احفظه وابعته لحدا بيحتاجه`; MSA `اسحب` / `احفظه وشاركه مع من يحتاجه`.

## Spelling checks before delivery

Common slips to check in every headline: ة vs ه at word end (مرة not مره in a formal register — but keep the dialect spelling if the user writes that way consistently), ى vs ي (على, إلى), hamza on alef (إلى, أن, إن), لـ + ال = لل (للمبتدئين). Don't add tashkeel except to disambiguate a single word.

## RTL and bidi rules

- `<html lang="ar" dir="rtl">`. The template's logical CSS mirrors the brand bar, corner helpers and step lines automatically.
- Counter: `<bdi dir="ltr" class="counter">2 / 7</bdi>`. Without it you get "7 / 2".
- Any Latin run inside Arabic (brand names, @handles, URLs, code terms): `<bdi>…</bdi>`. Without it, punctuation next to it jumps to the wrong side, e.g. "؟API" instead of "API؟".
- A whole English line inside an Arabic slide (mixed mode): `<p class="sub" lang="en" dir="ltr">` — gets Inter and correct direction.
- Arabic question mark is `؟`, comma `،`, semicolon `؛`. Use them in Arabic text, not `? , ;`.
- Percent: in Arabic text write `٪` with Arabic-Indic digits or `%` with Western digits, not mixed.

## Numerals

Default: Western digits (1, 2, 3) — they dominate Arabic social media in the Gulf and most of the Levant and are what the original style uses. Use Arabic-Indic (١، ٢، ٣) if the user writes with them, if `brand.json` says `"numerals": "arabic-indic"`, or for a formal/governmental brand. Be consistent across the whole set, including the counter and list numbers (the `.n` and `.dot` elements).

## Typography

- No `letter-spacing` on Arabic text and no `text-transform` — spacing breaks the joining of letters. The template already sets `letter-spacing: 0` for Arabic headlines.
- Line height 1.3 for headlines, ~1.55 for body: Arabic has taller ascenders and deeper descenders than Latin.
- Arabic headlines are shorter in characters but wider per word; a 3-line Arabic headline is the limit at cover size. If it wraps to 4, cut words or step down a size class.
- Highlighting: highlight a whole word, never part of one — splitting a word into two spans breaks letter joining. Highlight the word that carries the meaning (the keyword, the number, the surprising word), not a connector.
- Fonts: Cairo (default — bold, clear, includes Latin glyphs so mixed terms match). Alternatives in `fetch_fonts.sh`: Tajawal (rounder, friendly), IBM Plex Sans Arabic (corporate, technical), Almarai (clean, neutral). Use the brand's font if it has one.

## Dual mode: adapting Arabic ↔ English

- Rewrite the hook, don't translate it. "وش يعني API؟" → "What even is an API?" — same curiosity, natural English.
- Idioms and proverbs: replace with an equivalent or drop them.
- English usually needs ~20–30% more horizontal space at the same font size; let the English set step down a size class rather than cutting the idea.
- Keep the highlighted word pointing at the same concept in both versions, even if its position in the sentence moves.
