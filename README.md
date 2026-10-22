# My AI Skills — مهاراتي

Claude skills by **Idris7umed**, in Arabic and English. Each one is a plugin in a single marketplace: add it once, and every new skill shows up for you.

مهارات لـ Claude بالعربي والإنجليزي. كلها في مكان واحد: تضيفها مرة وحدة، وأي مهارة جديدة تنزل لك.

<p align="center">
<img src="examples/cover_ar.png" width="200"> <img src="examples/cover_en.png" width="200">
</p>

## Skills

| Skill | What it does | Install |
|---|---|---|
| [**My Designer — مصممي**](plugins/my-designer) | Designs branded Instagram / LinkedIn carousels in Arabic, English, or both, and renders ready-to-post PNGs with automatic layout QA. | `/plugin install my-designer@idris7umed` |
| [**Fikra — فكرة**](plugins/fikra) | Pressure-tests an idea with 4 roles (Advocate, Skeptic, Investor, Judge) and returns BUILD / FIX FIRST / KILL plus a 10-minute test to run today. | `/plugin install fikra@idris7umed` |
| [**SEO Boost — ارفع ظهورك**](plugins/seo-boost) | Scores a page's SEO out of 100 (URL, HTML file or draft), then fixes the title, meta description, headings, alt text and schema, and re-scores to show before → after. | `/plugin install seo-boost@idris7umed` |

## Install

### Claude Code

Add the marketplace once:

```
/plugin marketplace add Idris7umed/my-ai-skills
```

Then install any skill from the table above, for example:

```
/plugin install fikra@idris7umed
```

### Claude app (claude.ai)

Download a skill's `.skill` file from this repo ([`my-designer.skill`](my-designer.skill), [`fikra.skill`](fikra.skill), [`seo-boost.skill`](seo-boost.skill)) and upload it in **Settings → Capabilities → Skills**.

### طريقة التركيب

**في Claude Code:** أضف المتجر مرة وحدة:

```
/plugin marketplace add Idris7umed/my-ai-skills
```

وبعدها ركّب المهارة اللي تبيها، مثلًا: `/plugin install fikra@idris7umed`

**في تطبيق Claude:** نزّل ملف `.skill` للمهارة، وارفعه من **Settings ← Capabilities ← Skills**.

## Repo layout

```
.claude-plugin/marketplace.json   # the marketplace: lists every plugin
plugins/<skill>/                  # one folder per skill, with its own README
<skill>.skill                     # ready-to-upload package for the Claude app
examples/                         # preview images
evals/                            # test prompts
```

---

Created by **[Idris7umed](https://github.com/Idris7umed)** · [@idris7umed](https://instagram.com/idris7umed)
