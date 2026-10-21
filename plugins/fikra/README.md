# Fikra — فكرة

**Stop asking Claude "is my idea good?" — make it argue instead.**
**لا تسأل Claude «فكرتي حلوة؟» — خلّه يناقشها بدل ما يمدحها.**

Claude tends to be nice about your ideas. Fikra replaces the compliment with a structured debate and a cheap real-world test. One conversation plays 4 roles on the same idea:

| Role | Job |
|---|---|
| 🟢 **Advocate — المؤيد** | Why could it work? Who is the customer that really needs it? |
| 🔴 **Skeptic — المشكك** | Tries to bring it down: who won't buy, who the competitors are, what you're not seeing. |
| 💰 **Investor — المستثمر** | Doesn't care how it looks. One question: will it make money? |
| ⚖️ **Judge — الحَكَم** | Lets them debate one round, then rules. |

The verdict is one of three:

- **BUILD — ابنها**
- **FIX FIRST — عدّلها أول** (with the one fix)
- **KILL — خلّها** (with what would have to change for it to come back)

It also gives you **one step you can do today in 10 minutes** to test the idea, with a success number set in advance. Come back a week later with the result and it tells you whether the verdict changed.

> The 4 roles are one conversation playing four parts, not four separate agents.
> الأدوار مو 4 وكلاء منفصلين، هي محادثة وحدة تلعب أربع أدوار.

---

## Install

### Claude Code (plugin)

```
/plugin marketplace add Idris7umed/my-ai-skills
/plugin install fikra@idris7umed
```

Then share an idea, or run `/fikra:fikra`.

### Claude app, as a skill

Download [`fikra.skill`](../../fikra.skill) and upload it in **Settings → Capabilities → Skills**.

### Claude app, as a Project (no install)

Copy the prompt from [`project-instructions.md`](skills/fikra/assets/project-instructions.md) (Arabic and English versions) into a **Project's instructions**.

Inside a Project, the instructions stay in place, so when you come back a week later in the same Project, Claude has the context. In a new chat outside the Project it won't remember, so paste the **idea card** Fikra gives you at the end of every verdict.

### طريقة التركيب

- **Claude Code:** `/plugin marketplace add Idris7umed/my-ai-skills` وبعدها `/plugin install fikra@idris7umed`
- **تطبيق Claude:** نزّل `fikra.skill` وارفعه من **Settings ← Capabilities ← Skills**
- **بدون تركيب:** انسخ البرومبت من [`project-instructions.md`](skills/fikra/assets/project-instructions.md) وحطّه في تعليمات Project

---

## Files

```
plugins/fikra/
├── .claude-plugin/plugin.json          # plugin manifest
└── skills/fikra/
    ├── SKILL.md                        # instructions Claude follows
    ├── references/examples.md          # worked examples (Gulf Arabic + English)
    └── assets/project-instructions.md  # ready-to-paste Project prompt (AR + EN)
```

---

← [All skills](../../README.md)
