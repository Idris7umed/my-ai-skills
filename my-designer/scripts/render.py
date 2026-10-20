#!/usr/bin/env python3
"""Render every .slide in a carousel HTML file to PNG, run layout QA, and build a contact sheet.

Usage:
    python3 render.py carousel.html --out png/ [--no-sheet] [--words 40]

Exit code 1 if any QA check FAILs, so you can loop: fix -> re-render -> until clean.
Requires: playwright (chromium) and Pillow.
"""
import argparse, json, pathlib, sys

QA_JS = r"""
async (opts) => {
  await document.fonts.ready;
  const M = 80, out = [];
  const lang = document.documentElement.lang || 'ar';
  const wordLimit = opts.words || (lang === 'en' ? 35 : 40);

  // ---- fonts
  const faces = [...document.fonts].map(f => ({family: f.family.replace(/"/g,''), status: f.status}));
  const fontIssues = faces.filter(f => f.status === 'error').map(f => f.family);
  const wanted = lang === 'en' ? ['Inter'] : ['Cairo'];
  const loaded = new Set(faces.filter(f => f.status === 'loaded').map(f => f.family));
  for (const w of wanted) if (!loaded.has(w)) fontIssues.push(w + ' (not loaded — run fetch_fonts.sh)');

  // ---- helpers
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = ({r,g,b}) => { const f = v => { v/=255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); }; return .2126*f(r)+.7152*f(g)+.0722*f(b); };
  const ratio = (a,b) => { const [x,y] = [lum(a), lum(b)].sort((p,q)=>q-p); return (x+.05)/(y+.05); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > .5) return c; } return {r:0,g:0,b:0,a:1}; };
  const textRects = el => { const r = document.createRange(); r.selectNodeContents(el); return [...r.getClientRects()].filter(q => q.width > 2 && q.height > 2); };
  const inter = (a,b) => Math.max(0, Math.min(a.right,b.right)-Math.max(a.left,b.left)) * Math.max(0, Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));

  const slides = [...document.querySelectorAll('.slide')];
  let prevLayout = null;
  slides.forEach((s, i) => {
    const n = i + 1, S = s.getBoundingClientRect(), issues = [];
    const add = (level, msg) => issues.push({level, msg});
    const layout = s.dataset.layout || '';
    if (layout && layout === prevLayout) add('WARN', `same layout "${layout}" as previous slide`);
    prevLayout = layout;

    const texts = [...s.querySelectorAll('[data-qa="text"]')];
    const visuals = [...s.querySelectorAll('[data-qa="visual"]')].map(v => v.getBoundingClientRect());
    const bars = [...s.querySelectorAll('.bar')].map(b => b.getBoundingClientRect());

    texts.forEach(t => {
      const label = (t.innerText || '').trim().slice(0, 28);
      const inBar = !!t.closest('.bar');
      for (const r of textRects(t)) {
        if (r.left < S.left + M - 1 || r.right > S.right - M + 1 || r.top < S.top + M - 1 || r.bottom > S.bottom - M + 1)
          { add('FAIL', `text outside 80px safe area: "${label}"`); break; }
      }
      if (!inBar) {
        const rs = textRects(t), total = rs.reduce((x, r) => x + r.width * r.height, 0) || 1;
        if (rs.some(r => bars.some(b => inter(r, b) > 0))) add('FAIL', `text collides with brand bar: "${label}"`);
        const covered = rs.reduce((x, r) => x + Math.max(0, ...visuals.map(v => inter(r, v))), 0) / total;
        if (covered > 0.15) add('FAIL', `visual covers ${Math.round(covered*100)}% of "${label}" — move or shrink the visual`);
        else if (covered > 0) add('WARN', `visual touches "${label}" (${Math.round(covered*100)}%) — check the image`);
      }
      const cs = getComputedStyle(t), fg = parse(cs.color);
      if (fg) { const c = ratio(fg, bgOf(t)), big = parseFloat(cs.fontSize) >= 60, min = big ? 3 : 4.5;
        if (c < min) add('FAIL', `contrast ${c.toFixed(2)} < ${min} on "${label}"`); }
    });

    const barItems = [...s.querySelectorAll('.bar > *')].filter(e => getComputedStyle(e).display !== 'none').map(e => e.getBoundingClientRect());
    if (visuals.some(v => barItems.some(b => inter(b, v) > 0))) add('WARN', 'a visual sits behind the brand bar (counter / pill / handle / swipe) — move it or check readability');

    s.querySelectorAll('.safe').forEach(sf => {
      const kids = [...sf.children].map(c => c.getBoundingClientRect()).filter(r => r.height > 0);
      if (kids.length && !['cover-question','cover-number','cta','statement'].includes(layout)) {
        const used = Math.max(...kids.map(r => r.bottom)) - Math.min(...kids.map(r => r.top));
        if (used < sf.clientHeight * 0.45) add('WARN', `content fills only ${Math.round(100*used/sf.clientHeight)}% of the safe area — step up type sizes or add a visual`);
      }
      if (sf.scrollHeight > sf.clientHeight + 2) add('FAIL', `content taller than safe area by ${sf.scrollHeight - sf.clientHeight}px — cut words or shrink type`);
      if (sf.scrollWidth > sf.clientWidth + 2) add('FAIL', `content wider than safe area — a word or line doesn't fit`);
      const clone = sf.cloneNode(true); clone.querySelectorAll('.source').forEach(e => e.remove());
      const words = (clone.textContent || '').trim().split(/\s+/).filter(Boolean).length;
      if (words > wordLimit) add('WARN', `${words} words (budget ${wordLimit})`);
    });

    if (!s.classList.contains('last') && i === slides.length - 1) add('WARN', 'last slide is missing class="last" (swipe cue still shown)');
    const hl = s.querySelectorAll('.hl').length;
    if (hl > 1) add('WARN', `${hl} highlights — use one per slide`);
    out.push({slide: n, layout, issues});
  });
  return {lang, dir: document.documentElement.dir, fontIssues, slides: out};
}
"""


def contact_sheet(paths, dest, thumb_w=270, gap=16, bg=(40, 40, 40)):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in paths]
    th = [im.resize((thumb_w, round(im.height * thumb_w / im.width))) for im in ims]
    cols = min(5, len(th)); rows = -(-len(th) // cols); h = max(t.height for t in th)
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, rows * h + (rows + 1) * gap), bg)
    for i, t in enumerate(th):
        r, c = divmod(i, cols)
        sheet.paste(t, (gap + c * (thumb_w + gap), gap + r * (h + gap)))
    sheet.save(dest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-sheet", action="store_true")
    ap.add_argument("--words", type=int, default=0, help="word budget per slide (default 40 ar / 35 en)")
    a = ap.parse_args()

    html = pathlib.Path(a.html).resolve()
    out = pathlib.Path(a.out or html.parent / "png").resolve()
    out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 2000}, device_scale_factor=1)
        pg.goto(html.as_uri())
        pg.wait_for_load_state("networkidle")
        report = pg.evaluate(QA_JS, {"words": a.words})
        paths = []
        for i, el in enumerate(pg.query_selector_all(".slide"), 1):
            path = out / f"slide_{i:02d}.png"
            el.screenshot(path=str(path))
            paths.append(path)
        b.close()

    if paths and not a.no_sheet:
        contact_sheet(paths, out / "contact_sheet.png")

    fails = 0
    print(f"Rendered {len(paths)} slides -> {out}   (lang={report['lang']}, dir={report['dir']})")
    if report["fontIssues"]:
        fails += 1
        print("FAIL fonts:", ", ".join(report["fontIssues"]))
    for s in report["slides"]:
        if not s["issues"]:
            print(f"  slide {s['slide']:>2} [{s['layout']}] OK")
            continue
        seen = set()
        for it in s["issues"]:
            if it["msg"] in seen: continue
            seen.add(it["msg"])
            fails += it["level"] == "FAIL"
            print(f"  slide {s['slide']:>2} [{s['layout']}] {it['level']}: {it['msg']}")
    print("QA:", "CLEAN" if fails == 0 else f"{fails} FAIL(s) — fix and re-render")
    (out / "qa_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
