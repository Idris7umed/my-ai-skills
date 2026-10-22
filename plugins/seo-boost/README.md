# SEO Boost — ارفع ظهورك

**Check your page's SEO score, then fix it and see the new score.**
**افحص درجة السيو لصفحتك، وبعدها حسّنها وشوف الدرجة الجديدة.**

Give Claude a URL, an HTML file, or a draft article. SEO Boost runs a repeatable audit and gives a score out of 100. It then fixes what it can and runs the audit again, so you see **before → after**:

```
SEO SCORE: 33 → 94/100 (+61) (Excellent)
  content       89%  (was 25%)
  technical    100%  (was 45%)
  social       100%  (was 12%)
  readability  100%  (was 75%)
```

The score comes from a script, not a guess, so the same page always gets the same number.

---

## What it checks

| Category | Checks |
|---|---|
| **Content** | Title (length + keyword), meta description, single H1, heading structure, content depth, keyword placement and stuffing, image alt text, internal links, link text, clean URL |
| **Technical** | HTTP status and redirects, HTTPS, canonical, noindex, mobile viewport, `lang`/`dir`, charset, JSON-LD schema, HTML weight and response time, robots.txt + sitemap |
| **Social** | Open Graph tags, X/Twitter card |
| **Readability** | Paragraph length, sentence length, subheadings and lists |

## What it fixes

- 3 title options and 2 meta descriptions, with character counts
- One H1 plus a heading outline that matches search intent
- The content gaps to fill, without invented facts
- Alt text, internal link suggestions, and ready-to-paste tags (canonical, Open Graph, `lang`/`dir`)
- A JSON-LD block for the page type: Article, Product, LocalBusiness, Organization, Breadcrumb
- **If you give it the HTML file:** it applies the fixes to `improved.html` and re-scores it

## Built for Arabic too

- Matches Arabic keywords across spellings and prefixes, so قهوة, قهوه, القهوة, بالقهوة and وللقهوة count as the same keyword.
- Handles dialect vs. MSA search terms (جوال / موبايل), RTL `dir`, hreflang for bilingual sites, and Arabic vs. Latin slugs.

## What the score can't see

Backlinks, domain authority, competition, and Core Web Vitals. Use **PageSpeed Insights** for speed and **Google Search Console** for real ranking data. A high score means the page is set up well; it doesn't guarantee a ranking.

---

## Install

### Claude Code (plugin)

```
/plugin marketplace add Idris7umed/my-ai-skills
/plugin install seo-boost@idris7umed
```

Then ask: "check the SEO of https://…" or "improve this page for <keyword>".

### Claude app

Download [`seo-boost.skill`](../../seo-boost.skill) and upload it in **Settings → Capabilities → Skills**. Turn on **Code execution and file creation**, since the audit runs a script.

> In the Claude app, the sandbox can't reach most websites. If a URL won't load, paste the page source (Ctrl+U / Cmd+Option+U) or upload the HTML file.

### Run the audit yourself

```bash
pip install beautifulsoup4 requests
python3 skills/seo-boost/scripts/seo_audit.py https://example.com/page -k "main keyword"
```

### طريقة التركيب

- **Claude Code:** `/plugin marketplace add Idris7umed/my-ai-skills` وبعدها `/plugin install seo-boost@idris7umed`
- **تطبيق Claude:** نزّل `seo-boost.skill` وارفعه من **Settings ← Capabilities ← Skills**، وفعّل **Code execution and file creation**

---

## Files

```
plugins/seo-boost/
├── .claude-plugin/plugin.json      # plugin manifest
└── skills/seo-boost/
    ├── SKILL.md                    # instructions Claude follows
    ├── scripts/seo_audit.py        # the audit + score (URL, HTML or draft)
    └── references/
        ├── fixes.md                # how to fix each check
        ├── schema.md               # JSON-LD templates
        └── arabic-seo.md           # Arabic keywords, dialects, RTL, hreflang, slugs
```

---

← [All skills](../../README.md)
