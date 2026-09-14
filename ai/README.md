# LA.IO Brand Kit for AI

The LA.IO brand system, packaged for any AI tool: Claude, Claude Design, Claude Code, Cowork, Lovable, ChatGPT, Gemini, Cursor, and the rest. Everything in this folder is served at `https://assets.la.io/ai/`.

## Start here

Open **https://assets.la.io/ai**. One page, five tabs:

+ **Claude** for a claude.ai Project
+ **Claude Design** for an LA.IO Design System
+ **Claude Code + Cowork** for the skill folder and `CLAUDE.md`
+ **Lovable** for workspace instructions and the starter template
+ **Other AI** for ChatGPT, Gemini, Cursor, or anything that can fetch a URL or take an attachment

Each tab has copy-paste setup, downloads, and a "Ready when" check. Below the tabs sit the brand summary and every asset URL with a copy button.

## What's in the kit

```
ai/
├── index.html                        the page (generated, do not edit)
├── CLAUDE.md                         brand instructions for any AI, the one file to hand a tool
├── AGENTS.md                         byte-identical copy of CLAUDE.md (generated, do not edit)
├── README.md                         this file
├── claude-ai-project-setup.md        claude.ai Project setup; its paste block feeds the Claude tab
├── claude-design-setup.md            Claude Design form fields; each one feeds a copy block in the Claude Design tab
├── laio-brand.zip                    the skill, zipped for download
├── laio-brand/                       the skill, source of truth
│   ├── SKILL.md                      entrypoint; auto-triggers in Cowork and Claude Code
│   ├── BRAND.md                      full brand reference
│   ├── COMPONENTS.md                 copy-paste component code (React + HTML/CSS)
│   └── assets/                       logos, motifs, color CSS + tokens, fonts/laio-fonts-inline.css, LaioLogo.jsx
└── lovable/
    ├── LAIO_LOVABLE_GUIDE.md         how to start a Lovable project; its paste block feeds the Lovable tab
    ├── LOVABLE_CUSTOM_INSTRUCTIONS.md  workspace-level brand instructions
    ├── LOVABLE_STARTER_PROMPT.md     first message that builds the starter template
    └── LOVABLE_STARTER_TEMPLATE_SPEC.md  what the starter template contains
```

## How each tool uses it

+ **Claude (claude.ai):** make a Project, paste the block from `claude-ai-project-setup.md` into custom instructions, and upload `BRAND.md`, `COMPONENTS.md`, and `laio-fonts-inline.css` as knowledge.
+ **Claude Design:** create an LA.IO Design System by filling three form fields from `claude-design-setup.md`. One of them links this repo on GitHub, so Claude Design reads the brand from here. Then pick it from the Design System dropdown. Account-bound, so each designer makes their own copy.
+ **Claude Code and Cowork:** put `laio-brand/` in `~/.claude/skills/` (or `.claude/skills/` in one project). For Claude Code, also drop `CLAUDE.md` into the project root.
+ **Lovable:** paste `lovable/LOVABLE_CUSTOM_INSTRUCTIONS.md` into Workspace Knowledge in your Lovable project settings once, build or duplicate the starter template, then follow `lovable/LAIO_LOVABLE_GUIDE.md`.
+ **Any other AI:** tell it to fetch `https://assets.la.io/ai/CLAUDE.md`. If it cannot fetch URLs, attach `CLAUDE.md` and `laio-fonts-inline.css` instead. Tools that read `AGENTS.md` by convention find the same file under that name.

## Hosted assets

Live brand assets are served from `https://assets.la.io` (logos, motifs, colors, fonts). The skill points to these URLs; local copies in `laio-brand/assets/` cover offline and self-hosted contexts.

Aktiv Grotesk loads two ways. Real sites and apps link `https://assets.la.io/fonts/laio-fonts.css`. Sandboxes (claude.ai artifacts, Claude Design, Lovable previews, email) paste `laio-fonts-inline.css` into a `<style>` tag. That file ships inside the skill at `laio-brand/assets/fonts/`, because many AI sandboxes cannot reach assets.la.io at all. Family name is `'Aktiv Grotesk'`. Roboto is a fallback only, and a handoff that uses it says so.

## Regenerating

Edit the source files. Never edit `index.html` or `AGENTS.md` here; both are overwritten on every build. The paste blocks on the page are read from the fenced blocks in the setup `.md` files, so change the `.md` and rebuild.

From the repo root:

```
python3 _build/build_fonts.py     # only when the fonts change
python3 _build/gen_pages.py       # writes ai/index.html, ai/AGENTS.md, llms.txt, robots.txt
cd ai && rm laio-brand.zip && zip -r -X laio-brand.zip laio-brand -x '*.DS_Store'
```

Rezip whenever anything inside `laio-brand/` changes, or the download goes stale.

Maintained by Monday + Partners. Questions: dylan@mondayandpartners.com
