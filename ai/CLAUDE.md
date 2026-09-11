# LA.IO Brand Instructions for AI

This is an LA.IO (Louisiana Innovation Office) brand project. Everything you build (copy, layout, code, design) must match the LA.IO brand system.

If the laio-brand skill folder is available, read its SKILL.md for depth. If not, this file is sufficient on its own. The hard rules below are always in effect.

## Voice (every line of copy)
Matter-of-fact confidence. Short, declarative. State the case, then stop. Lead with fact, not persuasion.
+ Never: "resilience", "Silicon Bayou", "innovative solutions", "cutting-edge", "disruptive", "rethink/reimagine Louisiana", Louisiana clichés (jazz, Mardi Gras, Bourbon St, crawfish), "it's not X, it's Y", em dashes, inspirational-poster cadence.
+ Always use `+` as the list bullet. Never `•`, `-`, or `*`.
+ The three pillars, always in order: `+ Capital  + Coaching  + Connections`.

## Color (one family per piece)
Dark = background, Easy/Electric = accents/labels/type-on-dark. Body copy is white on dark or the dark brand color on light, never an accent color. Do not mix families.
+ Magenta `#101948 / #E385FE / #F629CB` · Green `#172708 / #C8ED5D / #96F90B` · Blue `#01233C / #63DCDE / #00B9FE` · Orange `#302511 / #F1DC43 / #F5C124` · Gray `#231F20 / #E3E6E7 / #929497`

## Type
**Aktiv Grotesk**, family name `'Aktiv Grotesk'` (title case, never `'aktiv-grotesk'`). Headlines Light 300 or Bold 700, never a middle weight. Body Regular 400.

Three ways to load it, in this order of preference:
+ **Embedded:** paste the contents of `laio-fonts-inline.css` into a `<style>` tag. Zero network requests. Use in claude.ai artifacts, Claude Design, Lovable previews, email, anything sandboxed. This is the default for AI-generated work.
+ **Hosted:** `<link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css">` for real sites and apps on any domain.
+ **Fallback:** Roboto from Google Fonts, only when neither of the above is possible. Say so in the handoff. Roboto is a stand-in, never the goal.

font-family stack: `'Aktiv Grotesk', 'Roboto', system-ui, sans-serif`

`laio-fonts-inline.css` ships in the `laio-brand` skill at `assets/fonts/laio-fonts-inline.css`. Read it from there rather than fetching it. Public copy: `https://assets.la.io/fonts/laio-fonts-inline.css`.

**JetBrains Mono** for eyebrows, labels, tags, metadata only. All caps, letter-spacing 0.08 to 0.12em, weights 400/700, always a brand accent color. Google Fonts: `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap`

## Logo & motifs
Use hosted SVGs, never recreate. `https://assets.la.io/logos/` and `/motifs/`. Single-fill near-black; override `fill` for color. React: `assets/LaioLogo.jsx`.

## Design
Angular (radius 0–2px). Committed dark or light, never mid-range. Spare, with generous whitespace. Every element has structural purpose.

**The test:** increases clarity, respects the audience, isn't trying too hard, works in a Baton Rouge shipyard and a London transit ad.
