# My Designer — مصممي

**Arabic + English brand carousels for Claude — كاروسيل بهويتك بالعربي والإنجليزي**

<p align="center">
<img src="examples/cover_ar.png" width="240"> <img src="examples/cover_en.png" width="240">
</p>

A Claude skill that designs a complete, branded Instagram / LinkedIn carousel in **Arabic, English, or both** from a single topic. You give it the topic; it writes the copy, designs the slides with your brand, renders ready-to-post PNGs (1080×1350), checks the layout automatically, and writes the caption, hashtags and alt text.

مهارة (Skill) لـ Claude تصمم لك كاروسيل كامل بهويتك **بالعربي أو الإنجليزي أو الاثنين**. تعطيها الموضوع، وهي تكتب المحتوى وتصمم الشرائح وتطلع لك صور PNG جاهزة للنشر، مع فحص تلقائي للتصميم وكابشن وهاشتاقات.

---

## Features

- **4 language modes:** Arabic (RTL), English (LTR), dual set (Arabic + English versions of the same carousel, adapted, not literally translated), and mixed (Arabic headline with an English subline).
- **Arabic dialects:** Gulf, Egyptian, Levantine, Maghrebi, and Modern Standard Arabic.
- **Correct RTL:** the brand bar mirrors automatically, the slide counter reads "2 / 7" (not "7 / 2"), and English terms inside Arabic text keep their punctuation in place.
- **10 layouts:** question cover, number cover, statement, icon cards, numbered list, before/after, chips, steps, big stat, call to action.
- **Automatic QA:** flags text covered by shapes, text outside the safe margins, low contrast, too many words, empty-looking slides, repeated layouts, and fonts that failed to load.
- **3 sizes:** portrait 4:5 (default), square 1:1, and story 9:16.
- **Reusable brand:** saves a `brand.json` you can upload next time to skip the brand questions.
- **Caption pack:** hook line, body, call to action, hashtags, and alt text for every slide.

---

## Install

### Claude app (claude.ai)

1. Download [`my-designer.skill`](my-designer.skill) from this repo (or zip the `my-designer` folder).
2. Go to **Settings → Capabilities → Skills**, click **Upload skill**, and upload the file.
3. Make sure **Code execution and file creation** is turned on in Settings, since the skill renders images.

### Claude Code

```bash
git clone https://github.com/Idris7umed/my-designer.git
cp -r my-designer/my-designer ~/.claude/skills/
```

To render locally, you also need Python 3, Playwright with Chromium, and Pillow:

```bash
pip install playwright pillow
python3 -m playwright install chromium
```

### طريقة التركيب

**في تطبيق Claude:**
1. نزّل ملف `my-designer.skill` (أو اضغط مجلد المهارة لملف ZIP).
2. روح **Settings ← Capabilities ← Skills** واضغط **Upload skill** وارفع الملف.
3. تأكد إن خيار **Code execution and file creation** مفعّل.

**في Claude Code:** استخدم الأوامر الموجودة فوق.

---

## How to use

Just ask Claude for a carousel. Examples:

| You write | You get |
|---|---|
| `Make me a carousel about 5 mistakes first-time managers make` | English set |
| `سو لي كاروسيل عن ليش القهوة تتعبك` | Arabic set (Gulf dialect) |
| `Carousel about sleep habits, in Arabic and English` | Two matching sets: `ar/` and `en/` |
| `عايز سلايدات عن أدوات AI، العنوان عربي وتحته سطر انجليزي` | Mixed set (Egyptian dialect) |

What happens next:

1. **Brand:** Claude asks once for your logo or handle and two colors (base + accent). Skip it and it uses a default. Upload a past post or your `brand.json` and it reads your style from that.
2. **Design:** it plans the slides, builds them, runs the QA check, and fixes any problems.
3. **Review:** you get the PNG slides, a contact sheet preview, the editable HTML source, `brand.json`, a quality score out of 100, and the caption pack.
4. **Iterate:** ask for changes ("make the cover bolder", "square size", "now the English version").

### طريقة الاستخدام

اكتب لـ Claude مثلاً: «سو لي كاروسيل عن …» أو «Make me a carousel about …» وخله يكمل.
بيسألك مرة وحدة عن شعارك أو حسابك ولونين لهويتك، وبعدها يعطيك الشرائح جاهزة للنشر مع الكابشن والهاشتاقات.

---

## Files

```
my-designer/          # the skill folder
├── SKILL.md              # Instructions Claude follows
├── assets/template.html  # Slide template: brand colors, layouts, visuals
├── scripts/fetch_fonts.sh  # Downloads Cairo + Inter fonts
├── scripts/render.py     # Renders PNGs, runs QA, builds the contact sheet
└── references/
    ├── arabic.md         # Dialects, RTL rules, numerals, Arabic typography
    ├── english.md        # Hooks, tone, English typography, captions
    └── layouts.md        # Markup for every layout and visual
```

---

Created by **[Idris7umed](https://github.com/Idris7umed)**.
Based on [arabic-brand-carousel](https://github.com/saoudphotos/arabic-brand-carousel) by [@saoudalajme](https://instagram.com/saoudalajme).
