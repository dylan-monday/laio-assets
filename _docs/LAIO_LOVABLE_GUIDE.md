# LA.IO Lovable — How to Start a Project

This is the only document you need. Everything else runs automatically.

---

## How your Lovable account is set up

Your account has brand instructions built in at the workspace level. Every project you create automatically knows:

+ The LA.IO color system and how to use it
+ Both typefaces and exactly when to use each
+ The voice rules — what to write and what never to write
+ The design principles — angular, spare, confident
+ Where to find every logo, motif, and color file

You don't configure any of this. It's already there.

---

## Starting a new project

**Step 1 — Duplicate the LA.IO Starter Template**
Find "LA.IO Starter Template" in your projects. Click the three-dot menu and duplicate it. Rename it for your project. Fonts, colors, logo component, and base components are already wired in.

**Step 2 — Paste this at the top of your first prompt**

Fill in the three blanks, then describe what you want to build:

```
This is an LA.IO brand project.

Project: [what it is — e.g. "event landing page for Innovation Day 2026"]
Audience: [who it's for — e.g. "founders, investors, state partners"]
Color family: [pick one: Magenta / Green / Blue / Orange / Gray]

[Describe what you want to build]
```

**Step 3 — Build normally**
Prompt Lovable the way you always do. The brand system handles the rest.

---

## Picking a color family

| Family | Dark background | Accent | Best for |
|--------|----------------|--------|----------|
| Blue | `#01233C` | `#63DCDE` | Partner tools, credibility-forward work |
| Green | `#172708` | `#C8ED5D` | Agriculture, energy, sustainability |
| Magenta | `#101948` | `#E385FE` | Tech, AI, high-energy digital |
| Orange | `#302511` | `#F1DC43` | Events, announcements, bold statements |
| Gray | `#231F20` | `#E3E6E7` | Neutral, functional, dashboard work |

One family per project. Don't mix.

---

## The two typefaces

**Aktiv Grotesk** — headlines and body copy. Already loaded.
+ Headlines: Light or Bold. Nothing in between.
+ Body copy: white on dark backgrounds, or dark color on white

**JetBrains Mono** — labels, eyebrows, tags, metadata only. Already loaded.
+ Always all caps
+ Always a brand accent color — never white or gray
+ Never for body copy or paragraphs

Example: a section eyebrow above a headline would be JetBrains Mono in the family's Easy accent color, all caps. The headline below it would be Aktiv Grotesk Bold in white.

---

## The logo

The starter template includes `LaioLogo.jsx` — drop it anywhere:

```jsx
<LaioLogo />                            // default black
<LaioLogo fill="#63DCDE" width={200} /> // Easy Blue on dark bg
<LaioLogo fill="#FFFFFF" width={160} /> // white on dark bg
```

All other logo files are at `https://assets.la.io/logos/` if you need them as image files.

---

## If something looks off-brand

Tell Lovable specifically what's wrong:

**Instead of:** "this doesn't look right"
**Say:** "remove the rounded corners, the headline should be Aktiv Grotesk Bold, use the Easy Blue accent on the border only not as a fill"

Common corrections:
+ "use `+` as the bullet, not `•`"
+ "the eyebrow label should be JetBrains Mono, all caps, in the accent color"
+ "remove the em dash, rewrite that sentence"
+ "stay in the Blue color family — remove the green"
+ "too much copy — cut it by half"
+ "the body copy color is wrong — white on dark backgrounds only"

---

## What LA.IO never sounds like

If Lovable generates copy with any of these, ask it to rewrite:

+ "resilience" or "resilient"
+ "innovative solutions" / "cutting-edge" / "disruptive"
+ "rethink Louisiana" — there is nothing to rethink
+ Louisiana cultural clichés: jazz, Mardi Gras, Bourbon Street
+ "it's not X, it's Y" constructions
+ Em dashes (—) anywhere in copy

---

## The three pillars

Whenever listing what LA.IO offers, always use this exact phrasing and order:

```
+ Capital
+ Coaching
+ Connections
```

---

## Questions or something looks wrong

Contact Dylan at Monday and Partners: dylan@mondayandpartners.com
