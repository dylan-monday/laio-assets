# LA.IO Project — Claude Code Instructions

This is an LA.IO (Louisiana Innovation Office) brand project. Everything you build — copy, layout, code, design — must match the LA.IO brand system.

The full system is the **`laio-brand` skill** (in `.claude/skills/laio-brand/`). Read its `SKILL.md` before generating anything; load `BRAND.md` and `COMPONENTS.md` from that folder when you need depth or component code. The hard rules below are always in effect.

## Voice (every line of copy)
Matter-of-fact confidence. Short, declarative. State the case, then stop. Lead with fact, not persuasion.
+ Never: "resilience", "Silicon Bayou", "innovative solutions", "cutting-edge", "disruptive", "rethink/reimagine Louisiana", Louisiana clichés (jazz, Mardi Gras, Bourbon St, crawfish), "it's not X, it's Y", em dashes (—), inspirational-poster cadence.
+ Always use `+` as the list bullet — never `•`, `-`, `*`.
+ The three pillars, always in order: `+ Capital  + Coaching  + Connections`.

## Color (one family per piece)
Dark = background, Easy/Electric = accents/labels/type-on-dark. Body copy is white on dark or the dark brand color on light — never an accent color. Do not mix families.
+ Magenta `#101948 / #E385FE / #F629CB` · Green `#172708 / #C8ED5D / #96F90B` · Blue `#01233C / #63DCDE / #00B9FE` · Orange `#302511 / #F1DC43 / #F5C124` · Gray `#231F20 / #E3E6E7 / #929497`

## Type
+ Aktiv Grotesk (Adobe kit `https://use.typekit.net/usf5bjl.css`, family `aktiv-grotesk`) — headlines (Light 300 or Bold 700, never a middle weight) + body (Regular 400).
+ JetBrains Mono — eyebrows/labels/tags only, all caps, accent color, never body copy.

## Logo & motifs
Use hosted SVGs, never recreate. `https://assets.la.io/logos/` and `/motifs/`. Single-fill near-black; override `fill` for color. React: `assets/LaioLogo.jsx`.

## Design
Angular (radius 0–2px). Committed dark or light, never mid-range. Spare — generous whitespace. Every element has structural purpose.

**The test:** increases clarity, respects the audience, isn't trying too hard, works in a Baton Rouge shipyard and a London transit ad.
