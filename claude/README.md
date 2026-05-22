# LA.IO Claude Kit

The LA.IO brand system, packaged for the Claude ecosystem (Claude, Cowork, Claude Code, and design tools). Self-contained — everything needed to make on-brand LA.IO work lives in this folder.

## Start here

Open **`START-HERE.html`** in a browser. It's a designed quickstart with a tab for each Claude surface and copy-paste setup steps.

## What's in the kit

```
LAIO-Claude-Kit/
├── START-HERE.html              ← open this first (the quickstart)
├── README.md                    ← this file
├── CLAUDE.md                    ← drop into a Claude Code project root
├── claude-ai-project-setup.md   ← setup for a claude.ai Project
├── laio-brand.zip               ← the skill, zipped for download (offered in START-HERE.html)
└── laio-brand/                  ← THE SKILL (source of truth)
    ├── SKILL.md                 ← entrypoint; auto-triggers in Cowork & Code
    ├── BRAND.md                 ← full brand reference
    ├── COMPONENTS.md            ← copy-paste component code (React + HTML/CSS)
    └── assets/                  ← logos, motifs, color CSS + tokens, LaioLogo.jsx
```

## The model — one skill, four front doors

`laio-brand/` is the single source of truth. Each surface points at it:

+ **Claude Code** — put `laio-brand/` in `~/.claude/skills/` (global) or `.claude/skills/` (one project), and drop `CLAUDE.md` into the project root.
+ **Cowork** — put `laio-brand/` in `~/.claude/skills/` (same folder as Claude Code; no in-app upload). It triggers automatically on LA.IO work.
+ **Claude (claude.ai)** — make a Project, paste the instructions from `claude-ai-project-setup.md`, upload `BRAND.md` + `COMPONENTS.md` as knowledge.
+ **Design** — covered on whichever surface you design in, fed by the same components and hosted assets.

## Hosted assets

Live brand assets are served from `https://assets.la.io` (logos, motifs, colors, fonts). The skill points to these URLs; local copies in `laio-brand/assets/` cover offline and self-hosted contexts.

Maintained by Monday + Partners. Questions: dylan@mondayandpartners.com
