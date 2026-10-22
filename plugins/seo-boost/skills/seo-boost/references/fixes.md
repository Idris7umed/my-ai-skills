# How to fix each check

The check IDs match `seo_audit.py --json` output.

## Content

**title** — Unique per page, 30–60 characters so Google doesn't cut it off. Pattern that works: `Keyword: specific benefit | Brand` or `Keyword in City — Brand`. Put the brand last (or drop it if the title is tight). Avoid "Home", "Welcome", or the brand alone.

**title_kw / h1_kw / meta_kw / kw_intro** — Use the exact keyword or a natural variant once in each of: title (first half), H1, the first paragraph, and the meta description. That's enough; more is not better.

**meta_desc** — 70–160 characters. Say what the page gives the reader and why to click: a number, a result, a differentiator, a call to action. Google may rewrite it, but a good one is used more often.

**h1** — Exactly one, describing the page topic. Logos and taglines shouldn't be H1s; style them with CSS instead.

**headings** — H2 per main section, H3 for sub-points, no skipping (H2 → H4). Headings phrased the way people search ("How long does cold brew last?") help with long-tail queries.

**length** — Depth matters more than word count. Thin pages (<300 words) usually lack answers to obvious questions. Add: what it is, who it's for, how it works / how to use it, price or what affects price, common questions, next step. For product pages, specs + use cases + FAQ + shipping/returns.

**kw_density** — Natural range is roughly 0.3–1.5 mentions per 100 words. Above 2.5 reads as stuffing; replace repeats with synonyms, related terms and pronouns.

**img_alt** — Describe what the image shows in 5–15 words: `alt="Cold brew coffee in a glass jar with ice"`. Decorative images can use `alt=""`, but the script counts empty alt as missing, so only do that for true decorations (dividers, background shapes).

**internal_links** — Link to 3+ related pages with anchor text that names the destination ("our coffee grinder guide"), not "click here". Also link *to* this page from related pages.

**anchor_text** — Replace "click here / read more / اضغط هنا / اقرأ المزيد" with descriptive text.

**slug** — Short, lowercase, hyphenated, keyword-bearing: `/cold-brew-coffee`, not `/Page_ID?id=3`. Changing a live URL needs a 301 redirect from the old one — say so whenever you suggest a slug change on a published page.

## Technical

**status / redirects** — The page should return 200. Internal links should point straight at final URLs (no redirect chains).

**https** — Serve everything over HTTPS; redirect HTTP → HTTPS.

**canonical** — `<link rel="canonical" href="https://example.com/page">` with the page's own absolute URL, unless it's a deliberate duplicate.

**indexable** — Remove `<meta name="robots" content="noindex">` (or an `X-Robots-Tag: noindex` header) from pages that should rank. Staging sites often ship with noindex left on.

**viewport** — `<meta name="viewport" content="width=device-width, initial-scale=1">`. Google indexes the mobile version.

**lang** — `<html lang="en">`; Arabic pages `<html lang="ar" dir="rtl">`.

**charset** — `<meta charset="utf-8">` as the first thing in `<head>`.

**schema** — One JSON-LD block for the page type. Templates: `schema.md`. Validate at validator.schema.org and test eligibility with Google's Rich Results Test.

**weight** — Large HTML (>300 KB) or slow responses (>1 s) hurt crawling and Core Web Vitals. Use PageSpeed Insights for LCP / INP / CLS — this script can't measure them.

**crawl_files** — `robots.txt` at the root with a `Sitemap: https://example.com/sitemap.xml` line; the sitemap lists canonical URLs. Submit the sitemap in Google Search Console.

## Social

**og** — Controls how links look on WhatsApp, LinkedIn, X, Facebook:
```html
<meta property="og:title" content="…">
<meta property="og:description" content="…">
<meta property="og:image" content="https://example.com/share-1200x630.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="article">
```

**twitter** — `<meta name="twitter:card" content="summary_large_image">`

## Readability

**paragraphs** — 2–4 sentences each; most readers are on phones.
**sentences** — One idea per sentence. Arabic writing often chains clauses with و — split them.
**scannable** — A subheading every ~300 words; lists for steps, features or options; a table for comparisons.
