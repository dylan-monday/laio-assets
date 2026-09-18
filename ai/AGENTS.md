# LA.IO Brand Instructions for AI

This is an LA.IO (Louisiana Innovation Office) brand project. Everything you build (copy, layout, code, design) must match the LA.IO brand system.

If the laio-brand skill folder is available, read its SKILL.md for depth. If not, this file is sufficient on its own. The hard rules below are always in effect.

## Voice (every line of copy)
Matter-of-fact confidence. Short, declarative. State the case, then stop. Lead with fact, not persuasion.
+ Never: "resilience", "Silicon Bayou", "innovative solutions", "cutting-edge", "disruptive", "rethink/reimagine Louisiana", Louisiana clichés (jazz, Mardi Gras, Bourbon St, crawfish), "it's not X, it's Y", em dashes, inspirational-poster cadence.
+ Always use `+` as the list bullet. Never `•`, `-`, or `*`. When you are writing in markdown, a line that starts with `+ ` renders as a dot and the plus disappears. Escape it as `\+ ` so the reader sees a literal plus and copies one out.
+ The three pillars are Capital, Coaching, Connections, in that order. Use them when the piece calls for them, not in everything.

## Color (one family per piece)
Dark = background, Easy/Electric = accents/labels/type-on-dark. Body copy is white on dark or the dark brand color on light, never an accent color. Do not mix families.
+ Magenta `#101948 / #E385FE / #F629CB` · Green `#172708 / #C8ED5D / #96F90B` · Blue `#01233C / #63DCDE / #00B9FE` · Orange `#302511 / #F1DC43 / #F5C124` · Gray `#231F20 / #E3E6E7 / #929497`

## Type
**Aktiv Grotesk**, family name `'Aktiv Grotesk'` (title case, never `'aktiv-grotesk'`). Headlines Light 300 or Bold 700, never a middle weight. Body Regular 400.

Sandboxed output has no network. A claude.ai artifact, a Claude Design canvas, a Lovable preview, an email, or anything else that renders inside a tool cannot reach assets.la.io or Google Fonts. In those contexts: fetch https://assets.la.io/fonts/laio-fonts-inline.css and paste the entire file into a <style> tag. Fetch the logo SVG (https://assets.la.io/logos/LAIO-COMPLETE.svg, and LED-WHITE.svg or LED-BLACK.svg if used) and paste the <svg> markup inline. Never <link> a stylesheet, never <img src>, never mask-image or background-image a URL, never load Roboto from Google. Before delivering, check the file: it contains @font-face rules with data: URIs and an inline <svg> for every logo. If it does not, it is not finished. The hosted CSS and hosted logo URLs are for real sites and apps on a domain, nothing else.

Three ways to load it, in this order of preference:
+ **Embedded:** paste the contents of `laio-fonts-inline.css` into a `<style>` tag. Zero network requests. Use in claude.ai artifacts, Claude Design, Lovable previews, email, anything sandboxed. This is the default for AI-generated work.
+ **Hosted, for real sites and apps on a domain only, never inside an artifact or preview:** `<link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css">`.
+ **Fallback:** Roboto from Google Fonts, only when neither of the above is possible. Say so in the handoff. Roboto is a stand-in, never the goal. Never Roboto inside an artifact; embed instead.

font-family stack: `'Aktiv Grotesk', 'Roboto', system-ui, sans-serif`

`laio-fonts-inline.css` ships in the `laio-brand` skill at `assets/fonts/laio-fonts-inline.css`. Read it from there rather than fetching it. Public copy: `https://assets.la.io/fonts/laio-fonts-inline.css`.

**JetBrains Mono** for eyebrows, labels, tags, metadata only. All caps, letter-spacing 0.08 to 0.12em, weights 400/700, always a brand accent color. Google Fonts: `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap`

## Logo & motifs
Use hosted SVGs, never recreate. Inside a sandboxed artifact, inline the SVG markup; a URL to the CDN will not load there. `https://assets.la.io/logos/` and `/motifs/`. Single-fill near-black; override `fill` for color. React: `assets/LaioLogo.jsx`.
Which logo. LAIO-COMPLETE.svg is the default everywhere: decks, pages, social, print, favicons excepted. LAIO-BASE.svg only when the mark renders under about 120px wide and the LOUISIANA INNOVATION subtext would be illegible. LAIO-HORZ.svg only in a header or nav bar. LOUISIANA-INNOVATION-A.svg, LOUISIANA-INNOVATION-B.svg, and DIVISION-LINE.svg are secondary marks: under or beside the primary mark, never alone, never as the only logo on a page. Never type the logo as text or draw it from brackets and letters; always place the SVG file.
+ LED logo (`LED-WHITE.svg`, `LED-BLACK.svg`, `LED-SMALL-WHITE.svg`, `LED-SMALL-BLACK.svg`): Louisiana Economic Development, the parent agency. White on dark grounds by default. Black on light grounds, recolored to the family dark. LED's gold and full-color marks belong to LED's own communications; the LA.IO kit carries white and black only. Under or beside the LA.IO mark, never above it, never as the only logo on a page.
+ Motifs, all `LAIO-*.svg`: `LEFT-BRACKET`, `RIGHT-BRACKET`, `UP-BRACKET`, `DOWN-BRACKET`, `BRACKET-CORNER-1`, `BRACKET-CORNER-2`, `CORNER-L`, `PLUS`, `X`, `DIAMOND`, `DIAMOND-EMPTY`, `SQUARE`, `SQUARE-EMPTY`, `FIELD-DIAGONAL`, `HATCH`, `WIRE-NODE`.
Shape grammar: every shape comes from the logo's bracket, at 0, 45, or 90 degrees. No curves, no circles, no rounded corners. Two shapes per composition.

## Design
Angular (radius 0–2px). Committed dark or light, never mid-range. Spare, with generous whitespace. Every element has structural purpose.

**The test:** increases clarity, respects the audience, isn't trying too hard, works in a Baton Rouge shipyard and a London transit ad.
