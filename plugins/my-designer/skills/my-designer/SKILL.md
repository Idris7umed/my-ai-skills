---
name: my-designer
description: "Builds a branded Instagram / LinkedIn carousel in Arabic, English, or both from any topic. The user gives a topic; the skill analyzes it, writes the copy (in the user's dialect or tone), designs the slides with the user's brand, renders PNGs ready to post, runs automatic layout QA, and writes the caption, hashtags and alt text. Asks only for brand details it cannot infer. Use for ANY carousel, slides-for-Instagram, swipe post, or 'كاروسيل / سلايدات / بوست شرائح' request, in either language, even if the user only says 'make me a post about X'."
---

# My Designer — مصممي (Arabic + English Brand Carousel)

The user gives a topic. You do the analysis, the writing and the design. Ask only for what you cannot infer, in one short message. Reply to the user in the language they wrote in.

Files in this skill:
- `assets/template.html` — the slide template: brand tokens, direction-aware brand bar, layouts, visuals. Start every carousel from a copy of it.
- `scripts/fetch_fonts.sh` — downloads Cairo + Inter into a `fonts/` folder next to the HTML.
- `scripts/render.py` — renders each slide to PNG, runs layout QA, builds a contact sheet.
- `references/arabic.md` — read for any Arabic or mixed carousel (dialects, RTL/bidi, numerals, typography).
- `references/english.md` — read for any English carousel (hooks, tone, type rules).
- `references/layouts.md` — layout and visual catalog with the markup for each.

## Step 1: Language mode (infer, don't ask)

Pick one mode:

| Mode | When | Output |
|---|---|---|
| `ar` | User writes in Arabic, or asks for Arabic | One RTL set |
| `en` | User writes in English, or asks for English | One LTR set |
| `dual` | User asks for "Arabic and English", "both", "bilingual", or their audience is clearly mixed | Two matching sets: `ar/` and `en/` |
| `mixed` | User asks for both languages *on the same slide* | One RTL set, Arabic headline + short English subline |

Default to the language of the request. Ask only if the user's request and their stated audience conflict.

In `dual` mode, **adapt, don't translate.** Each set must read like it was written natively: an Arabic hook built on a dialect expression should become an equivalent English hook, not a literal rendering. Keep the same slide count, order, layouts, visuals and highlighted *concept* so the two sets look like siblings.

## Step 2: Brand details (ask only if missing)

Look first, in this order: an uploaded `brand.json` from a past carousel → brand details earlier in this conversation → an uploaded post or carousel (read colors, fonts, layout from the image). Use what you find.

If nothing is available, ask once, in one message, in the user's language:
- Brand mark: a logo file, a wordmark, or a handle.
- Colors: a base color and an accent color.
- (Optional) the size: portrait 4:5 is the default.

If the user doesn't know or doesn't answer, use the defaults and say so in one line: near-black base `#12101C`, off-white text `#F4F1EA`, accent `#A78BFA`. Never ask about fonts, layout or structure — decide those.

After the first carousel, save the brand as `brand.json` (see the format in `assets/template.html` comments) and include it in the delivery, so the user can upload it next time and skip this step.

## Step 3: Analyze the topic

Decide before designing:
- Core idea in one sentence.
- Audience and what they want from it.
- Angle: surprise, how-to, list, comparison, myth vs fact, story, or opinion.
- Slide count: 7 by default, up to 10 for lists, minimum 5.
- Facts and numbers: verify them (search if a search tool is available). If a claim depends on news, research or an official document, put a short source line on that slide. If you can't verify a number, leave it out rather than guess.

## Step 4: Plan the slides

Write the plan as a table (slide → layout → headline → highlight word → body) before building. It makes the dual-mode mapping explicit and catches repeated layouts.

- **Slide 1 (cover)** — a hook that stops the scroll. Choose the cover type that fits:
  - Question with a highlighted keyword (curiosity).
  - Big number with a bold promise (lists).
  - Visual hero (tech, product, anything that benefits from imagery).
  - One bold word or short claim (opinion, warning).
- **Slide 2** — the payoff promise or the problem. Many people only see slides 1–2; slide 2 must give a reason to keep swiping.
- **Slides 3 to N-1** — one idea per slide. Don't use the same layout on two consecutive slides.
- **Last slide** — one engagement prompt only: a comment keyword, "save it + send it to someone", or a question for the audience. Brand mark shown large. No swipe cue.
- **Word budget**: under 40 words per slide in Arabic, under 35 in English (English sets wider, so it fills faster).

## Step 5: Build

1. Copy `assets/template.html` to the working folder as `carousel.html` (or `ar/carousel.html` and `en/carousel.html` in dual mode).
2. Run `bash scripts/fetch_fonts.sh <working-folder>` so `fonts/Cairo.ttf` and `fonts/Inter.ttf` sit next to the HTML. If the brand uses another font, put its file in `fonts/` and change the `@font-face` rule. Never rely on Google Fonts `<link>` imports — they fail offline and the PNG would fall back to a system font.
3. Set the brand tokens in `:root`, set `<html lang dir>` (`ar`/`rtl` or `en`/`ltr`; `mixed` uses `ar`/`rtl`), and set the size class on `<body>` (`size-portrait` 1080×1350, `size-square` 1080×1080, `size-story` 1080×1920).
4. Build the slides from the layouts in `references/layouts.md`. Mark text with `data-qa="text"` and decorative visuals with `data-qa="visual"` — the QA script depends on these attributes.

Design rules that apply to every slide:
- **Brand bar** (built into the template with logical CSS, so it mirrors itself in RTL): category pill at the reading-start top corner, slide counter at the reading-end top corner, brand mark at reading-start bottom, swipe cue in the accent color at reading-end bottom (all except the last slide).
- **Counter and numbers**: always wrap the counter in `<bdi dir="ltr">` — without it, RTL renders "2 / 7" as "7 / 2". Wrap any Latin term inside Arabic text (API, iPhone, @handle) in `<bdi>`.
- **Emphasis**: one highlighted word or phrase per slide, in the accent color with the hand-drawn underline (`<span class="hl">`). A slide may use its own accent when it covers a distinct item (a color, tool, step); set `style="--accent:#..."` on that slide. Otherwise one accent for the whole series.
- **Type sizes** (portrait): cover headline 110–130 px, content headline 80–110 px, body 40–50 px, label above headline 36–44 px. The template's classes already use these; scale down rather than wrap a headline onto 4+ lines.
- **Margins**: at least 80 px safe area on every edge (the template's `.safe` box enforces it).
- **Visuals**: one visual element on the cover and on key slides. Large, behind or beside the text — never under the headline. A soft accent glow behind it adds depth. Use photos only if the user uploads them or approves generating them. Remove any decoration that doesn't support the idea.

## Step 6: Render and QA

```bash
python3 scripts/render.py <working-folder>/carousel.html --out <working-folder>/png
```

The script renders each `.slide` to `slide_01.png`, `slide_02.png`… at 1080 px width, builds `contact_sheet.png`, and prints a QA report. It checks: text overlapping a visual, text escaping the safe area or clipping, low contrast (WCAG < 4.5 for body, < 3 for headlines), word count over budget, two consecutive identical layouts, and whether the brand fonts actually loaded. Fix every `FAIL`, re-render, and repeat until clean. Then **look at the contact sheet yourself** (view the image) — the script can't judge whether a highlight lands on the right word or whether a layout feels cramped.

In dual mode, run it once per language folder.

## Step 7: Score

Score the carousel out of 100 with this rubric, and for each lost point give the reason and a concrete fix:

| Criterion | Points |
|---|---|
| Cover is understood in under 2 seconds and makes you want to swipe | 20 |
| Readability: size, contrast, line length, no clutter | 20 |
| One idea per slide, logical flow, strong slide 2 | 15 |
| Brand consistency: colors, fonts, aligned brand bar on every slide | 15 |
| Language quality: natural dialect / native English, no spelling errors, correct RTL | 15 |
| Single, clear call to action on the last slide | 10 |
| Clean QA report, no overlaps | 5 |

## Delivery

Send the user, for review:
- The PNG slides (the final deliverable — fonts are baked in, ready to post) and the contact sheet as a quick preview.
- `carousel.html` as the editable source, and `brand.json`.
- A **caption pack** written in the chat, in each language of the set: a first line that works as a second hook (it shows before "...more"), 2–4 short lines of body, one call to action, 3–5 relevant hashtags (mix one broad, a few niche), and one-sentence alt text per slide for accessibility.

Then, in one or two sentences, explain why you chose this cover and layout, and offer one next change. Export variations (other sizes, the other language) only after the user approves the design.
