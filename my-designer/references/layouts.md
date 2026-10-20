# Layouts and visuals

Every slide shares this frame. Only the `.safe` block and the visuals change.

```html
<section class="slide" data-layout="LAYOUT-NAME">
  <!-- visuals first (behind content) -->
  <header class="bar top"><span class="pill" data-qa="text">CATEGORY</span><bdi dir="ltr" class="counter">3 / 7</bdi></header>
  <div class="safe"> ... </div>
  <footer class="bar bottom"><span class="mark"><bdi>@handle</bdi></span><span class="swipe">SWIPE-WORD <span class="arrow"></span></span></footer>
</section>
```

- Swipe word: Arabic `اسحب` (or the dialect equivalent the user uses), English `Swipe`. The arrow direction is automatic.
- Logo instead of handle: `<span class="mark"><img src="data:image/png;base64,..."> <bdi>@handle</bdi></span>` — embed the logo as a data URI so the HTML stays self-contained.
- Last slide: add `class="slide last"` (hides the swipe cue).
- Size variants: on `size-square`, drop one size step on headlines (`h-cover` → `h-xl`) and keep 4 items max on lists. On `size-story`, keep content inside the middle 1080×1350 zone too — Instagram overlays UI at the top and bottom of stories; add `style="inset:300px 80px 340px"` to `.safe`.

## Text layouts

**Cover — question** `data-layout="cover-question"`
```html
<div class="safe center">
  <p class="label" data-qa="text">Small label</p>
  <h1 class="h-cover" data-qa="text">Why does <span class="hl">coffee</span> crash you?</h1>
  <p class="sub" data-qa="text">One-line promise</p>
</div>
```

**Cover — number** `data-layout="cover-number"`
```html
<div class="safe">
  <div class="bignum" data-qa="text">7</div>
  <h1 class="h-xl" data-qa="text">habits that <span class="hl">actually</span> stick</h1>
</div>
```

**Statement** `data-layout="statement"` — one big sentence, for a turning point or a bold claim.
```html
<div class="safe"><h2 class="h-xl" data-qa="text">Most people quit on <span class="hl">day 3</span>.</h2>
<p class="body" data-qa="text">Supporting line.</p></div>
```

**Cards with icons** `data-layout="cards"` — 2 to 4 cards.
```html
<div class="safe">
  <h2 class="h-m" data-qa="text">Headline with <span class="hl">one</span> highlight</h2>
  <div class="cards">
    <div class="card"><div class="ico"><svg><use href="#i-bolt"/></svg></div>
      <div><h3 data-qa="text">Card title</h3><p data-qa="text">Short line</p></div></div>
  </div>
</div>
```
Icons available: `i-check i-x i-bolt i-clock i-star i-target i-bulb i-chart i-heart i-shield`.

**Numbered list** `data-layout="list"` — 3 to 5 items.
```html
<div class="safe">
  <h2 class="h-m" data-qa="text">Title</h2>
  <ol class="numlist"><li data-qa="text"><span class="n">01</span><span>Item</span></li></ol>
</div>
```

**Before / after** `data-layout="compare"` — also works for myth vs fact, wrong vs right.
```html
<div class="safe">
  <h2 class="h-m" data-qa="text">Title</h2>
  <div class="compare">
    <div class="before"><span class="tag" data-qa="text">Before</span><p data-qa="text">...</p></div>
    <div class="after"><span class="tag" data-qa="text">After</span><p data-qa="text">...</p></div>
  </div>
</div>
```

**Chip grid** `data-layout="chips"` — tools, keywords, options. Use `.chip.on` for the recommended one.
```html
<div class="safe"><h2 class="h-m" data-qa="text">Title</h2>
<div class="chips"><span class="chip" data-qa="text">Item</span><span class="chip on" data-qa="text">Pick</span></div></div>
```

**Steps** `data-layout="steps"` — 3 to 4 steps with a connecting line.
```html
<div class="safe"><h2 class="h-m" data-qa="text">Title</h2>
<div class="steps"><div class="step"><div class="dot">1</div><div><h3 data-qa="text">Step</h3><p data-qa="text">Detail</p></div></div></div></div>
```

**Big number / stat** `data-layout="stat"` — add the source line.
```html
<div class="safe"><div class="bignum" data-qa="text">73%</div>
<h2 class="h-m" data-qa="text">of people ...</h2><p class="source" data-qa="text">Source: Org, 2025</p></div>
```

**CTA (last slide)** `data-layout="cta"`
```html
<div class="safe center">
  <h2 class="h-l" data-qa="text">Comment <span class="hl">GUIDE</span></h2>
  <p class="body" data-qa="text">and I'll send you the full checklist</p>
  <div><span class="cta-key" dir="ltr">GUIDE</span></div>
</div>
```
Alternatives: "Save this + send it to someone who needs it", or one question for the audience. One prompt only.

## Visuals

Add inside the slide, before the bar. Use `data-qa="visual"` for shapes that must not touch text, `data-qa="bg"` for full-bleed textures and soft glows.

| Class | Best for | Notes |
|---|---|---|
| `v-grid` (bg) | tech, data, systems | full-bleed |
| `v-glow` (bg) | depth behind any visual | combine with another shape |
| `v-circles` | focus, ideas, sound, ripples | corner placement |
| `v-arch` | calm, wellness, frames | corner or behind a big number |
| `v-sun` | beginnings, mornings, growth | `at-bot-center` |
| `v-tri` | direction, tech, warnings | corner |
| `v-stripes` | energy, warnings, sport | corner |
| `v-dotgrid` | structure, planning | corner |
| `v-stack` (`<i></i><i></i><i></i>` inside) | lists, collections, tools | corner |
| `v-dots` (`<i style="background:#...">` inside, not absolute) | items that each have a color | place inside `.safe` |

Placement helpers: `at-top-end at-top-start at-bot-end at-bot-start at-bot-center` — logical, so they mirror in RTL. The bottom corners hold the handle and the swipe cue, so prefer top corners for big shapes; if a shape must sit low, lift it clear of the bar (e.g. `style="bottom:200px"`) — render.py warns when a visual sits behind a bar item. For `v-arch`, place it so most of the arch is visible (e.g. `style="bottom:-60px; inset-inline-end:-80px"`); a corner crop that shows only one edge reads as a glitch. Put the visual in the corner away from where the headline starts reading: in RTL headlines start at the right, so `at-top-start` (right) is often the wrong choice for a big shape near a top-aligned headline.

Device / product mockups: a simple phone frame is `<div class="v at-bot-end" data-qa="visual" style="width:420px;height:820px;border-radius:64px;border:14px solid var(--surface);background:linear-gradient(var(--accent),var(--bg));"></div>`. Put an uploaded screenshot inside as a data-URI `<img>` with `object-fit:cover`.

Photos: only uploaded or user-approved generated images, embedded as data URIs, with a dark gradient overlay (`linear-gradient(transparent, var(--bg))`) under text for contrast.
