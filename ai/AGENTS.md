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
+ Motifs, all `LAIO-*.svg`: `LEFT-BRACKET`, `RIGHT-BRACKET`, `UP-BRACKET`, `DOWN-BRACKET`, `BRACKET-CORNER-1`, `BRACKET-CORNER-2`, `CORNER-L`, `PLUS`, `X`, `DIAMOND`, `DIAMOND-EMPTY`, `SQUARE`, `SQUARE-EMPTY`, `FIELD-DIAGONAL`, `HATCH`, `WIRE-NODE`.
+ LED logo (`LED-WHITE.svg`, `LED-BLACK.svg`, `LED-SMALL-WHITE.svg`, `LED-SMALL-BLACK.svg`): Louisiana Economic Development, the parent agency. White on dark grounds by default. Black on light grounds, recolored to the family dark. Never the full-color or gold versions. Under or beside the LA.IO mark, never above it.

## Range
Six layout moves: the Split, the Diamond, the Frame, the Wire, the Grid, the Big Mark.
Shape grammar: every shape comes from the logo's bracket, at 0, 45, or 90 degrees. No curves, no circles, no rounded corners. Two shapes per composition.
Before any layout beyond a plain page, read `RANGE.md` in the laio-brand skill, also at `https://assets.la.io/ai/laio-brand/RANGE.md`. One reference per move in `references/`.

The plain page is the default: one family, Aktiv Grotesk, plus bullets, generous space. Use a move only when the content is short and structural enough to earn one, and pick it from the content: a statement gets the Frame, or the Big Mark on a cover or closer; one number, or two things compared, gets the Split; two to four parallel items get the Diamond; connections get the Wire; four photos or sectors get the Grid. In a deck, moves go on the opener, the closer, and a few key slides. Body copy over four lines, tables, charts, forms, and lists over four items are always plain pages. One move per canvas, never the same move twice in a row. The person asking will not name a move. Never ask which one they want, and never explain a move by name unless asked.

## Design
Angular (radius 0–2px). Committed dark or light, never mid-range. Spare, with generous whitespace. Every element has structural purpose.

**The test:** increases clarity, respects the audience, isn't trying too hard, works in a Baton Rouge shipyard and a London transit ad.
