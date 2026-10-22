---
name: seo-boost
description: "Checks a web page's SEO score (0-100) with a repeatable audit, then improves it: rewrites the title, meta description and headings, fills content gaps, adds alt text, internal links, Open Graph and schema (JSON-LD), applies the fixes to the HTML when given a file, and re-scores to show the before and after. Works on a URL, an HTML file, or a draft article, in Arabic or English. Use whenever someone asks to check, audit, score, analyze, optimize or improve SEO, wants to rank higher on Google, asks about meta titles/descriptions, keywords or schema, or says 'سيو', 'تحسين محركات البحث', 'كيف أطلع أول في قوقل', 'افحص موقعي', 'قيّم السيو'."
---

# SEO Boost — ارفع ظهورك

Two jobs: **score** a page honestly, then **improve** it and prove the improvement with a second score. Reply in the user's language and dialect; keep technical terms (title, meta description, H1, schema) in English where that's what people use.

`scripts/seo_audit.py` produces the score. Never estimate a score by eye — run the script, so the number is repeatable and the before/after comparison is fair.

## Step 1: Get the page and the keyword

**Input types:**
- **URL** → `python3 scripts/seo_audit.py <url> -k "<keyword>" --save before.json`. In URL mode the script also checks HTTP status, redirects, response time, robots.txt and sitemap.
- **HTML file** (uploaded, or page source the user pasted) → save it and run `seo_audit.py page.html --url <real-url-if-known> -k "<keyword>" --save before.json`.
- **Draft article** (text or markdown, not yet published) → `seo_audit.py draft.md -k "<keyword>"`. This is content-only mode: technical and social checks are skipped and the score covers content and readability.

**If the URL can't be fetched** (the sandbox often blocks outside sites, or the site blocks bots): get the HTML another way — a web-fetch or browser tool if one is available (you need the raw HTML with the `<head>`, not extracted text), or ask the user to open the page, press Ctrl+U / Cmd+Option+U, and paste or upload the source. Then use HTML-file mode with `--url`.

**JavaScript-rendered sites** (React/Vue SPAs, some site builders): if the raw HTML is nearly empty but the page clearly has content, say so. Google can render JS, but slower and less reliably; server-rendered or static HTML is the fix, and the audit should be run on the rendered HTML (copy it from the browser's Elements panel).

**Keyword:** use the one the user gives. If none is given, infer the main keyword from the title/H1 and what the page sells or explains, state it in one line ("افترضت الكلمة المفتاحية: …"), and continue. Pass Arabic synonyms or spelling variants with `|`, e.g. `-k "جوال|موبايل"`. Ask a question only if the page's topic is genuinely unclear.

## Step 2: Report the score

Present the result in this shape (translate labels to the user's language):

```
📊 SEO score: 58/100 — Needs work
   Content 61% · Technical 54% · Social 25% · Readability 83%
```

Then:
1. **Top fixes** — the 5 biggest point gains from the script's "FIXES" list, each in one plain line with the points it's worth. Skip jargon; say *why* it matters in a few words ("Google shows this text under your link").
2. **What's already good** — 2–3 items, briefly.
3. **What the score can't see** — one line: it checks on-page and technical basics, not backlinks, site authority, competition, or Core Web Vitals. For speed, point to PageSpeed Insights; for real ranking data, Google Search Console.

Never claim a score guarantees a ranking.

## Step 3: Improve

Read `references/fixes.md` for how to fix each check, `references/schema.md` for JSON-LD templates, and `references/arabic-seo.md` for any Arabic page. Then produce the fixes, highest impact first:

- **Title** — 3 options, 30–60 characters, keyword near the start, written to earn the click (benefit, number, year or location when true). Show the character count for each.
- **Meta description** — 2 options, 70–160 characters, keyword included naturally, ends with a reason to click.
- **H1 and heading outline** — one H1; H2s for each section the searcher expects. If a search tool is available, look at the top results for the keyword to see what they cover and what intent they serve (guide, product, local service, comparison) and match that intent. Don't invent search volumes or difficulty scores.
- **Content gaps** — the specific sections or questions missing, as a list the user can write from. When asked, write the sections, without inventing facts, prices or statistics.
- **Alt text** for each image that lacks it (describe the image; include the keyword only where it's genuinely what the image shows).
- **Internal links** — 3+ suggested anchors and the kind of page each should point to.
- **Technical tags** — ready-to-paste snippets for whatever failed: canonical, viewport, `lang`/`dir`, charset, Open Graph, Twitter card, and the JSON-LD block for the page type.

**If you have the HTML file:** apply the fixes to a copy (`improved.html`), keeping the page's own content and design, then re-run:

```
python3 scripts/seo_audit.py improved.html --url <url> -k "<keyword>" --compare before.json
```

Show the before → after line and per-category changes. If something can't be fixed in the HTML (thin content needs the owner's knowledge, slow server, missing sitemap), list it as a remaining step. Deliver `improved.html` as a file.

**If it's a live site you can't edit:** give the snippets plus where they go, in general terms — the SEO fields of their CMS or SEO plugin (title, description, slug, social image), the page editor for headings and alt text, the theme/header settings for tags in `<head>`. Don't invent menu paths for a platform you aren't sure about.

**If it's a draft:** return the improved draft (headings, intro with the keyword, shorter paragraphs, lists) plus the title and meta description to use when publishing, and re-score it with `--compare`.

## Rules

- No keyword stuffing. If usage is already high, the fix is fewer repetitions and more related terms, not more keyword.
- No invented facts, reviews, ratings or statistics — in content or in schema. Schema must describe what's actually on the page (e.g. no `aggregateRating` without real reviews shown on the page).
- Rich results aren't guaranteed by schema. FAQ rich results are now shown mainly for authoritative government and health sites, and HowTo rich results were retired; FAQ sections are still useful content.
- One page at a time. For a whole-site request, audit the homepage plus 2–3 key pages (a product/service page and a blog post), then list site-wide issues once.
- Re-run the script after every round of changes. The score shown to the user always comes from the script.
