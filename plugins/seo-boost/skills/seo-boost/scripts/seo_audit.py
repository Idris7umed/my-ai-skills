#!/usr/bin/env python3
"""SEO audit with a transparent, repeatable score (0-100). Arabic + English aware.

Usage:
  python3 seo_audit.py https://example.com/page [--keyword "main keyword"]
  python3 seo_audit.py page.html --url https://example.com/page [--keyword "..."]
  python3 seo_audit.py draft.md --keyword "..."           # content-only audit
  add --json for machine-readable output, --compare before.json to show before -> after

The score is a checklist score: points earned / points possible, with checks that
don't apply (e.g. no keyword given, no URL known) excluded. It measures on-page and
technical hygiene, not Google ranking.
Requires: beautifulsoup4, requests (requests only for URL mode).
"""
import argparse, json, re, sys, time, pathlib
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

PASS, WARN, FAIL, NA = "pass", "warn", "fail", "n/a"
AR_CHARS = re.compile(r"[\u0600-\u06FF]")
TASHKEEL = re.compile(r"[\u064B-\u0652\u0670\u0640]")  # harakat + tatweel
GENERIC_ANCHORS = {"click here", "here", "read more", "more", "link", "this", "learn more",
                   "اضغط هنا", "هنا", "اقرأ المزيد", "المزيد", "اضغط", "الرابط", "اعرف المزيد", "للمزيد"}


def norm(s: str) -> str:
    """Lowercase + Arabic normalization so 'أفضل' == 'افضل', 'قهوة' == 'قهوه'."""
    s = TASHKEEL.sub("", s.lower())
    s = re.sub("[أإآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    return re.sub(r"\s+", " ", s).strip()


AR_PREFIX = re.compile(r"^(?:[بكل])?(?:ال)?")


def stem_ar(w: str) -> str:
    """Strip attached و/ف, ب/ك/ل and ال so 'والقهوه', 'بالقهوه', 'وللقهوه' all match 'قهوه'.
    Applied identically to page text and keyword, so matching stays consistent."""
    if not AR_CHARS.search(w) or len(w) < 4:
        return w
    if w[0] in "وف":
        w = w[1:]
    if w.startswith("لل") and len(w) > 3:
        return w[2:]
    s = AR_PREFIX.sub("", w)
    return s if len(s) >= 2 else w


def match_form(text: str) -> str:
    """Normalized, prefix-stripped token string padded with spaces, for whole-word matching."""
    toks = re.findall(r"[\w\u0600-\u06FF]+", norm(text))
    return " " + " ".join(stem_ar(t) for t in toks) + " "


def kw_variants(kw: str):
    """Keyword match forms; separate variants with |."""
    out = []
    for k in kw.split("|"):
        m = match_form(k).strip()
        if m and m not in out:
            out.append(m)
    return out


def has_kw(text, variants):
    t = match_form(text)
    return any(f" {v} " in t for v in variants)


def count_kw(text, variants):
    t = match_form(text)
    return sum(t.count(f" {v} ") for v in variants)


def words(text):
    return re.findall(r"[\w\u0600-\u06FF]+", text)


def md_to_html(md: str) -> str:
    html, para = [], []
    def flush():
        if para:
            html.append("<p>" + " ".join(para) + "</p>"); para.clear()
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush(); n = len(m.group(1)); html.append(f"<h{n}>{m.group(2)}</h{n}>")
        elif re.match(r"^\s*([-*]|\d+\.)\s+", line):
            flush(); html.append("<li>" + re.sub(r"^\s*([-*]|\d+\.)\s+", "", line) + "</li>")
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
    flush()
    return "<html><body>" + "\n".join(html) + "</body></html>"


def fetch(url):
    import requests
    ua = {"User-Agent": "Mozilla/5.0 (compatible; SEOBoostAudit/1.0)"}
    t0 = time.time()
    r = requests.get(url, headers=ua, timeout=20, allow_redirects=True)
    meta = {"status": r.status_code, "final_url": r.url, "elapsed": round(time.time() - t0, 2),
            "bytes": len(r.content), "x_robots": r.headers.get("X-Robots-Tag", ""),
            "redirects": len(r.history)}
    base = f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
    try:
        rb = requests.get(base + "/robots.txt", headers=ua, timeout=10)
        meta["robots_txt"] = rb.status_code == 200 and "user-agent" in rb.text.lower()
        sm = re.findall(r"(?im)^sitemap:\s*(\S+)", rb.text) if rb.status_code == 200 else []
        meta["sitemap"] = bool(sm) or requests.get(base + "/sitemap.xml", headers=ua, timeout=10).status_code == 200
    except Exception:
        meta["robots_txt"] = meta["sitemap"] = None
    r.encoding = r.encoding or r.apparent_encoding
    return r.text, meta


def audit(html, url=None, keyword=None, net=None, content_only=False):
    soup = BeautifulSoup(html, "html.parser")
    checks = []

    def add(cat, cid, name, pts, status, detail, fix=""):
        earned = pts if status == PASS else (pts / 2 if status == WARN else 0)
        checks.append({"category": cat, "id": cid, "check": name, "points": pts,
                       "earned": 0 if status == NA else earned, "status": status, "detail": detail, "fix": fix})

    variants = kw_variants(keyword) if keyword else []
    title = (soup.title.get_text(" ", strip=True) if soup.title else "")
    md_el = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    mdesc = (md_el.get("content") or "").strip() if md_el else ""

    body = soup.body or soup
    for t in body.find_all(["script", "style", "noscript", "template", "svg"]):
        t.decompose()
    main = soup.find("main") or soup.find("article") or body
    main_copy = BeautifulSoup(str(main), "html.parser")
    for t in main_copy.find_all(["nav", "footer", "header", "aside"]):
        t.decompose()
    text = main_copy.get_text(" ", strip=True)
    wlist = words(text)
    wc = len(wlist)
    lang_ar = len(AR_CHARS.findall(text)) > 0.3 * max(1, len(re.findall(r"\w", text)))
    lang = "ar" if lang_ar else "en"

    # ---------------- CONTENT ----------------
    tl = len(title)
    if not content_only:
        if not title:
            add("content", "title", "Title tag", 8, FAIL, "No <title>.", "Add a unique title, 30–60 characters, main keyword near the start.")
        elif 30 <= tl <= 60:
            add("content", "title", "Title tag", 8, PASS, f"{tl} chars: “{title}”")
        elif 20 <= tl <= 70:
            add("content", "title", "Title tag", 8, WARN, f"{tl} chars (ideal 30–60): “{title}”", "Tighten or extend the title to 30–60 characters so it isn't cut off or too thin.")
        else:
            add("content", "title", "Title tag", 8, FAIL, f"{tl} chars: “{title}”", "Rewrite the title to 30–60 characters.")
        if variants:
            ok = has_kw(title, variants)
            add("content", "title_kw", "Keyword in title", 5, PASS if ok else FAIL,
                "Found." if ok else "Keyword missing from title.", "" if ok else "Put the main keyword in the title, ideally in the first half.")
        dl = len(mdesc)
        if not mdesc:
            add("content", "meta_desc", "Meta description", 6, FAIL, "Missing.", "Add a 70–160 character description that states the benefit and invites the click.")
        elif 70 <= dl <= 160:
            add("content", "meta_desc", "Meta description", 6, PASS, f"{dl} chars.")
        else:
            add("content", "meta_desc", "Meta description", 6, WARN, f"{dl} chars (ideal 70–160).", "Adjust the description to 70–160 characters.")
        if variants and mdesc:
            ok = has_kw(mdesc, variants)
            add("content", "meta_kw", "Keyword in meta description", 2, PASS if ok else WARN,
                "Found." if ok else "Missing.", "" if ok else "Mention the keyword naturally in the description (Google bolds it).")

    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    if len(h1s) == 1:
        add("content", "h1", "Single H1", 6, PASS, f"“{h1s[0]}”")
    elif len(h1s) > 1:
        add("content", "h1", "Single H1", 6, WARN, f"{len(h1s)} H1s.", "Keep one H1 for the page topic; turn the others into H2.")
    else:
        add("content", "h1", "Single H1", 6, FAIL, "No H1.", "Add one H1 that states the page topic.")
    if variants and h1s:
        ok = any(has_kw(h, variants) for h in h1s)
        add("content", "h1_kw", "Keyword in H1", 3, PASS if ok else WARN, "Found." if ok else "Missing.",
            "" if ok else "Include the keyword (or a close variant) in the H1.")

    levels = [int(h.name[1]) for h in soup.find_all(re.compile("^h[1-6]$"))]
    skips = [f"H{a}→H{b}" for a, b in zip(levels, levels[1:]) if b > a + 1]
    h2n = levels.count(2)
    if h2n >= 2 and not skips:
        add("content", "headings", "Heading structure", 4, PASS, f"{h2n} H2s, no skipped levels.")
    elif h2n >= 1:
        add("content", "headings", "Heading structure", 4, WARN, f"{h2n} H2s; skipped: {', '.join(skips) or 'none'}.",
            "Break the content into sections with H2s (and H3s under them) without skipping levels.")
    else:
        add("content", "headings", "Heading structure", 4, FAIL, "No H2 subheadings.", "Add H2 subheadings for each main section.")

    if wc >= 600:
        add("content", "length", "Content depth", 6, PASS, f"{wc} words.")
    elif wc >= 300:
        add("content", "length", "Content depth", 6, WARN, f"{wc} words.", "Expand to cover the questions searchers ask (aim for depth, not padding).")
    else:
        add("content", "length", "Content depth", 6, FAIL, f"{wc} words — thin content.", "Thin page: add useful sections (answers, examples, steps, FAQs).")

    if variants:
        intro = " ".join(wlist[:100])
        ok = has_kw(intro, variants)
        add("content", "kw_intro", "Keyword in first 100 words", 3, PASS if ok else WARN, "Found." if ok else "Missing.",
            "" if ok else "Mention the keyword early, in the first paragraph.")
        n = count_kw(text, variants)
        rate = 100 * n / max(1, wc)  # mentions per 100 words
        if wc < 150:
            add("content", "kw_density", "Keyword usage", 3, PASS if 1 <= n <= 3 else (WARN if n == 0 else FAIL),
                f"{n} uses in {wc} words.", "" if 1 <= n <= 3 else ("Mention the keyword at least once." if n == 0 else "Too many repetitions for a short page."))
        elif 0.3 <= rate <= 1.5:
            add("content", "kw_density", "Keyword usage", 3, PASS, f"{n} uses ({rate:.1f} per 100 words).")
        elif rate > 2.5:
            add("content", "kw_density", "Keyword usage", 3, FAIL, f"{n} uses ({rate:.1f} per 100 words) — looks stuffed.", "Cut repetitions; use synonyms and related terms instead.")
        else:
            add("content", "kw_density", "Keyword usage", 3, WARN, f"{n} uses ({rate:.1f} per 100 words).",
                "Use the keyword and close variants a little more naturally." if rate < 0.3 else "Slightly high; vary the wording with synonyms.")

    imgs = soup.find_all("img")
    if imgs:
        missing = [i.get("src", "?")[:60] for i in imgs if not (i.get("alt") or "").strip()]
        cov = 1 - len(missing) / len(imgs)
        st = PASS if not missing else (WARN if cov >= 0.8 else FAIL)
        add("content", "img_alt", "Image alt text", 4, st, f"{len(imgs) - len(missing)}/{len(imgs)} images have alt text.",
            "" if st == PASS else "Add descriptive alt text to: " + ", ".join(missing[:5]))
    else:
        add("content", "img_alt", "Image alt text", 4, NA, "No images.")

    if not content_only:
        host = urlparse(url).netloc if url else None
        anchors = soup.find_all("a", href=True)
        internal = [a for a in anchors if a["href"].startswith(("/", "#", "./", "../")) or (host and urlparse(urljoin(url, a["href"])).netloc == host)]
        internal = [a for a in internal if not a["href"].startswith("#")]
        n_int = len(internal)
        add("content", "internal_links", "Internal links", 3, PASS if n_int >= 3 else (WARN if n_int >= 1 else FAIL),
            f"{n_int} internal links.", "" if n_int >= 3 else "Link to 3+ related pages on your site with descriptive anchor text.")
        generic = sorted({a.get_text(" ", strip=True) for a in anchors if norm(a.get_text(" ", strip=True)) in {norm(g) for g in GENERIC_ANCHORS}})
        add("content", "anchor_text", "Descriptive link text", 2, PASS if not generic else WARN,
            "OK." if not generic else f"Generic anchors: {', '.join(generic[:5])}",
            "" if not generic else "Replace generic link text with words that describe the target page.")
        if url:
            path = urlparse(url).path.strip("/")
            slug = path.split("/")[-1] if path else ""
            bad = []
            if len(path) > 75: bad.append("long")
            if re.search(r"[A-Z]", path): bad.append("uppercase")
            if "_" in slug: bad.append("underscores")
            if re.search(r"\?|=|&", url.split("#")[0].split("?", 1)[-1] if "?" in url else ""): bad.append("query parameters")
            if re.search(r"%D8|%D9", path): bad.append("encoded Arabic (works, but shares as a long %-string)")
            add("content", "slug", "Clean URL", 2, PASS if not bad else WARN, f"/{path}" + (f" — {', '.join(bad)}" if bad else ""),
                "" if not bad else "Use a short, lowercase, hyphenated slug" + (" (a Latin transliteration often shares better than encoded Arabic)" if "encoded Arabic" in " ".join(bad) else "") + ".")

    # ---------------- TECHNICAL ----------------
    if not content_only:
        if net:
            st = net["status"]
            add("technical", "status", "HTTP status", 5, PASS if st == 200 else FAIL,
                f"{st}" + (f" after {net['redirects']} redirect(s)" if net["redirects"] else ""),
                "" if st == 200 else "The page must return 200 OK.")
            if net["redirects"] > 1:
                checks[-1]["status"] = WARN; checks[-1]["earned"] = 2.5; checks[-1]["fix"] = "Point links straight at the final URL to avoid redirect chains."
        if url:
            ok = url.startswith("https://")
            add("technical", "https", "HTTPS", 4, PASS if ok else FAIL, url.split("://")[0].upper(), "" if ok else "Serve the page over HTTPS.")
        can = soup.find("link", rel=lambda v: v and "canonical" in (v if isinstance(v, list) else [v]))
        if can and can.get("href"):
            href = can["href"]
            if url and urljoin(url, href).rstrip("/") != (net or {}).get("final_url", url).rstrip("/"):
                add("technical", "canonical", "Canonical URL", 4, WARN, f"Points elsewhere: {href}", "Make sure the canonical points to this page unless it's intentionally a duplicate.")
            elif not href.startswith("http"):
                add("technical", "canonical", "Canonical URL", 4, WARN, f"Relative: {href}", "Use an absolute canonical URL.")
            else:
                add("technical", "canonical", "Canonical URL", 4, PASS, href)
        else:
            add("technical", "canonical", "Canonical URL", 4, FAIL, "Missing.", 'Add <link rel="canonical" href="https://…this page…">.')
        rob = soup.find("meta", attrs={"name": re.compile("^(robots|googlebot)$", re.I)})
        rob_c = (rob.get("content", "") if rob else "") + " " + ((net or {}).get("x_robots") or "")
        if "noindex" in rob_c.lower():
            add("technical", "indexable", "Indexable", 6, FAIL, f"noindex found ({rob_c.strip()}).", "Remove noindex if this page should appear in Google.")
        else:
            add("technical", "indexable", "Indexable", 6, PASS, "No noindex.")
        vp = soup.find("meta", attrs={"name": "viewport"})
        add("technical", "viewport", "Mobile viewport", 4, PASS if vp else FAIL, "Present." if vp else "Missing.",
            "" if vp else '<meta name="viewport" content="width=device-width, initial-scale=1">')
        html_tag = soup.find("html")
        hl = (html_tag.get("lang") if html_tag else "") or ""
        hd = (html_tag.get("dir") if html_tag else "") or ""
        if not hl:
            add("technical", "lang", "Language declared", 3, FAIL, "No lang attribute.", f'<html lang="{lang}"' + (' dir="rtl">' if lang_ar else ">"))
        elif lang_ar and not (hl.lower().startswith("ar") and hd.lower() == "rtl"):
            add("technical", "lang", "Language declared", 3, WARN, f'lang="{hl}" dir="{hd}" on Arabic content.', 'Arabic pages need <html lang="ar" dir="rtl">.')
        else:
            add("technical", "lang", "Language declared", 3, PASS, f'lang="{hl}"' + (f' dir="{hd}"' if hd else ""))
        cs = soup.find("meta", charset=True) or soup.find("meta", attrs={"http-equiv": re.compile("content-type", re.I)})
        add("technical", "charset", "Charset", 1, PASS if cs else WARN, "Declared." if cs else "Not declared.", "" if cs else '<meta charset="utf-8">')
        ld = BeautifulSoup(html, "html.parser").find_all("script", type="application/ld+json")  # fresh parse: body scripts were stripped above
        types, bad = [], 0
        for s in ld:
            try:
                d = json.loads(s.string or "")
                for item in (d if isinstance(d, list) else d.get("@graph", [d])):
                    t = item.get("@type") if isinstance(item, dict) else None
                    if t: types.append(t if isinstance(t, str) else ",".join(t))
            except Exception:
                bad += 1
        if types and not bad:
            add("technical", "schema", "Structured data", 4, PASS, "JSON-LD: " + ", ".join(types))
        elif bad:
            add("technical", "schema", "Structured data", 4, WARN, f"{bad} JSON-LD block(s) fail to parse.", "Fix the JSON syntax (validate at validator.schema.org).")
        else:
            add("technical", "schema", "Structured data", 4, FAIL, "No JSON-LD.", "Add schema for the page type (Article, Product, LocalBusiness, Organization…).")
        size = (net or {}).get("bytes") or len(html.encode())
        slow = (net or {}).get("elapsed")
        perf_bad = size > 1_000_000 or (slow and slow > 2.5)
        perf_warn = size > 300_000 or (slow and slow > 1.0)
        add("technical", "weight", "HTML weight / response", 2, FAIL if perf_bad else (WARN if perf_warn else PASS),
            f"{size/1024:.0f} KB HTML" + (f", {slow}s response" if slow else ""),
            "" if not (perf_bad or perf_warn) else "Reduce HTML size / server response time; check PageSpeed Insights for Core Web Vitals.")
        if net and net.get("robots_txt") is not None:
            ok = net["robots_txt"] and net["sitemap"]
            add("technical", "crawl_files", "robots.txt + sitemap", 2, PASS if ok else WARN,
                f"robots.txt: {'yes' if net['robots_txt'] else 'no'}, sitemap: {'yes' if net['sitemap'] else 'no'}",
                "" if ok else "Publish robots.txt with a Sitemap: line and an XML sitemap.")
        alts = soup.find_all("link", rel="alternate", hreflang=True)
        if alts:
            add("technical", "hreflang", "hreflang", 0, PASS, ", ".join(sorted({a['hreflang'] for a in alts})))

    # ---------------- SOCIAL ----------------
    if not content_only:
        def og(p): return soup.find("meta", attrs={"property": p}) or soup.find("meta", attrs={"name": p})
        have = [p for p in ("og:title", "og:description", "og:image") if og(p)]
        add("social", "og", "Open Graph tags", 6, PASS if len(have) == 3 else (WARN if have else FAIL),
            f"{len(have)}/3: {', '.join(have) or 'none'}", "" if len(have) == 3 else "Add og:title, og:description and og:image (1200×630) so shares show a proper card.")
        tc = soup.find("meta", attrs={"name": "twitter:card"})
        add("social", "twitter", "X/Twitter card", 2, PASS if tc else WARN, tc.get("content") if tc else "Missing.",
            "" if tc else '<meta name="twitter:card" content="summary_large_image">')

    # ---------------- READABILITY ----------------
    paras = [p.get_text(" ", strip=True) for p in main_copy.find_all("p") if p.get_text(strip=True)]
    if paras:
        avg_p = sum(len(words(p)) for p in paras) / len(paras)
        add("readability", "paragraphs", "Paragraph length", 3, PASS if avg_p <= 80 else (WARN if avg_p <= 120 else FAIL),
            f"avg {avg_p:.0f} words/paragraph", "" if avg_p <= 80 else "Split long paragraphs (2–4 sentences each) — easier to scan on mobile.")
    sents = [s for s in re.split(r"[.!?؟\n]+", text) if len(words(s)) > 2]
    if sents:
        avg_s = sum(len(words(s)) for s in sents) / len(sents)
        lim = 30 if lang_ar else 25
        add("readability", "sentences", "Sentence length", 3, PASS if avg_s <= lim else WARN,
            f"avg {avg_s:.0f} words/sentence", "" if avg_s <= lim else "Shorten long sentences; one idea per sentence.")
    subs = len(soup.find_all(["h2", "h3"])); lists = len(soup.find_all(["ul", "ol", "table"])) + (1 if soup.find("li") and not soup.find(["ul", "ol"]) else 0)
    if wc >= 150:
        per = wc / max(1, subs)
        ok = per <= 350
        add("readability", "scannable", "Scannability", 4, PASS if ok and lists else (WARN if ok or lists else FAIL),
            f"{subs} subheadings, {lists} lists/tables, ~{per:.0f} words per section",
            "" if ok and lists else "Add a subheading every ~300 words and use lists or tables where content is a set of items or steps.")

    possible = sum(c["points"] for c in checks if c["status"] != NA)
    earned = sum(c["earned"] for c in checks)
    score = round(100 * earned / possible) if possible else 0
    cats = {}
    for c in checks:
        if c["status"] == NA: continue
        k = cats.setdefault(c["category"], [0, 0]); k[0] += c["earned"]; k[1] += c["points"]
    grade = "Excellent" if score >= 90 else "Good" if score >= 75 else "Needs work" if score >= 50 else "Poor"
    return {"url": url, "keyword": keyword, "language": lang, "word_count": wc, "title": title,
            "meta_description": mdesc, "h1": h1s, "score": score, "grade": grade,
            "categories": {k: {"earned": round(v[0], 1), "possible": v[1], "pct": round(100 * v[0] / v[1]) if v[1] else 0} for k, v in cats.items()},
            "checks": checks, "mode": "content-only" if content_only else ("url" if net else "file")}


def print_report(r, before=None):
    icon = {PASS: "✅", WARN: "⚠️ ", FAIL: "❌", NA: "➖"}
    head = f"SEO SCORE: {r['score']}/100 ({r['grade']})"
    if before:
        d = r["score"] - before["score"]
        head = f"SEO SCORE: {before['score']} → {r['score']}/100 ({'+' if d >= 0 else ''}{d}) ({r['grade']})"
    print(head)
    print(f"mode={r['mode']}  language={r['language']}  words={r['word_count']}" + (f"  keyword=“{r['keyword']}”" if r["keyword"] else "  (no keyword given: keyword checks skipped)"))
    for k, v in r["categories"].items():
        b = (before or {}).get("categories", {}).get(k)
        print(f"  {k:<12} {v['pct']:>3}%" + (f"  (was {b['pct']}%)" if b else "") + f"  [{v['earned']}/{v['possible']}]")
    print()
    for c in r["checks"]:
        print(f"{icon[c['status']]} [{c['category']}] {c['check']}: {c['detail']}")
    todo = sorted([c for c in r["checks"] if c["status"] in (FAIL, WARN)], key=lambda c: c["points"] - c["earned"], reverse=True)
    if todo:
        print("\nFIXES, biggest impact first:")
        for i, c in enumerate(todo, 1):
            print(f"{i}. (+{c['points'] - c['earned']:g} pts) {c['check']}: {c['fix']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="URL, .html file, or .md/.txt draft")
    ap.add_argument("--keyword", "-k", help="main keyword; separate variants with |")
    ap.add_argument("--url", help="the page's real URL when auditing a saved HTML file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--save", help="write the JSON result to this path (for --compare later)")
    ap.add_argument("--compare", help="a previous --save JSON to show before -> after")
    a = ap.parse_args()

    net, url, content_only = None, a.url, False
    if re.match(r"^https?://", a.target):
        try:
            html, net = fetch(a.target)
        except Exception as e:
            sys.exit(f"Could not fetch {a.target}: {e}\nSave the page's HTML to a file and run: seo_audit.py page.html --url {a.target}")
        url = net["final_url"]
    else:
        p = pathlib.Path(a.target)
        raw = p.read_text(encoding="utf-8", errors="replace")
        if p.suffix.lower() in (".md", ".txt", ".markdown") or "<html" not in raw.lower() and "<body" not in raw.lower() and "<h1" not in raw.lower():
            html, content_only = md_to_html(raw), True
        else:
            html = raw
    r = audit(html, url=url, keyword=a.keyword, net=net, content_only=content_only)
    before = json.loads(pathlib.Path(a.compare).read_text()) if a.compare else None
    if a.save:
        pathlib.Path(a.save).write_text(json.dumps(r, ensure_ascii=False, indent=2))
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print_report(r, before)


if __name__ == "__main__":
    main()
