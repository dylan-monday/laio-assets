# LA.IO on Claude Design

Claude Design has a first-class **Design System** feature. You create an **LA.IO Design System** once (from a prompt + references), then pick it from the *Design System* dropdown on any new project (Prototype, Slide deck, From template) and everything comes out on brand.

Design systems are account-bound, so each person who designs LA.IO work creates their own copy. It takes a couple of minutes and the prompt below makes it identical every time.

## Steps

1. In Claude Design, start a **new Design System** the same way the other systems were made: from a prompt plus reference files.
2. Paste the **creation prompt** below.
3. Attach references:
   + `LAIO-COMPLETE.svg` (the logo) from `https://assets.la.io/logos/`
   + `laio-fonts-inline.css` from `https://assets.la.io/fonts/laio-fonts-inline.css`. This is Aktiv Grotesk embedded in one file. Claude Design uses it for all Aktiv Grotesk rendering, since it cannot load the typeface from any URL.
   + One or two motifs from `https://assets.la.io/motifs/` (e.g. `LAIO-LEFT-BRACKET.svg`, `LAIO-PLUS.svg`)
   + The six Range reference PNGs, `01-split.png` to `06-big-mark.png`, from `https://assets.la.io/ai/laio-brand/references/`. One example of each layout move.
   + Optional but recommended: a screenshot of `https://assets.la.io/ai/` as a "brand in action" reference
4. Name it exactly: **LA.IO Design System**
5. On any New Project, choose **LA.IO Design System** from the *Design System* dropdown.

## Creation prompt (paste this)

```
Create a design system called "LA.IO Design System" for LA.IO (Louisiana Innovation Office), the operating brand for Louisiana's innovation ecosystem. It should feel technical, precise, confident, and aspirational. Use the attached LA.IO logo, laio-fonts-inline.css, and references.

COLOR. Five color families, each with a dark ground, an "easy" accent, and an "electric" accent. Any single artifact uses ONE family: the dark stop as background, easy or electric as accents and structural elements. Never mix families in one piece. Body text is white on dark backgrounds, or the dark brand color on light, never an accent color. Default to the Magenta family for tech, AI, and digital work unless told otherwise.
  Magenta: #101948 / #E385FE / #F629CB
  Green:   #172708 / #C8ED5D / #96F90B
  Blue:    #01233C / #63DCDE / #00B9FE
  Orange:  #302511 / #F1DC43 / #F5C124
  Gray:    #231F20 / #E3E6E7 / #929497
Light neutral background option: #E3E6E7.

TYPOGRAPHY. Two typefaces, strictly separated.
  Aktiv Grotesk for headlines, body, and UI, family name 'Aktiv Grotesk' (title case, never 'aktiv-grotesk'). Headlines Light 300 or Bold 700, never a middle weight. Body Regular 400.
  Three ways to load it, in this order of preference:
  + Embedded: paste the contents of laio-fonts-inline.css into a <style> tag. Zero network requests. Use in claude.ai artifacts, Claude Design, Lovable previews, email, anything sandboxed. This is the default for AI-generated work.
  + Hosted: <link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css"> for real sites and apps on any domain.
  + Fallback: Roboto from Google Fonts, only when neither of the above is possible. Say so in the handoff. Roboto is a stand-in, never the goal.
  font-family stack: 'Aktiv Grotesk', 'Roboto', system-ui, sans-serif
  In this design system, always use the embedded method: the attached laio-fonts-inline.css renders Aktiv Grotesk in every design. Paste its full contents into a <style> tag. Do not load Aktiv Grotesk from any URL.
  JetBrains Mono for eyebrows, labels, tags, metadata only. All caps, letter-spacing 0.08 to 0.12em, weights 400/700, always a brand accent color. Google Fonts: https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap

LOGO AND MOTIFS. Use the real LA.IO assets, never recreate the logo. The logo is a monospace wordmark bracketed by chevrons: < LA.IO >. Files are single-fill near-black (#231F20); recolor by overriding the fill. Logo: https://assets.la.io/logos/LAIO-COMPLETE.svg (also LAIO-BASE, LAIO-HORZ). Motifs (brackets, chevrons, plus, diamond, X): https://assets.la.io/motifs/. Use brackets and chevrons as framing devices and supergraphics: scale freely, crop intentionally, never scatter as decoration. Never frame the logo itself with additional brackets.

LAYOUT MOVES. Beyond a plain page, build with six moves, one attached reference each: the Split (one 45-degree field divides the canvas), the Diamond (45-degree containers that touch at points), the Frame (two corner brackets around a headline), the Wire (1px connectors with open-square terminals), the Grid (four photos with the plus as the gutter), and the Big Mark (the logo at supergraphic scale, cropped past the edges). Every shape comes from the logo's bracket. Angles are 0, 45, and 90 only; nothing else rotates. No curves, no circles. Two shapes per composition, one field, one family.

LAYOUT AND COMPONENTS. Angular and restrained. Border-radius 0 to 2px (small tags up to 3px). No gradients, no drop shadows. Commit to dark or light backgrounds, never mid-range. Generous whitespace; every element has structural purpose. Buttons are flat with a 2px radius. Cards are dark background with an accent border, or light background with an accent border. Use "+" as the list bullet, never a dot, hyphen, or asterisk.

VOICE for any generated copy. Matter-of-fact confidence, short declarative sentences, state the case then stop. Never use "resilience", "Silicon Bayou", "innovative solutions", "cutting-edge", "disruptive", em dashes, "it's not X, it's Y" constructions, or Louisiana cliches (jazz, Mardi Gras, Bourbon Street, crawfish).

The three pillars, when listed, always in this order: + Capital / + Coaching / + Connections.

Name the design system exactly: LA.IO Design System
```

## If something comes out off-brand

Tell Claude Design specifically: "stay in one color family", "headline should be Aktiv Grotesk Bold", "use + as the bullet", "remove the rounded corners", "accent color on the border only, not as a fill". The fuller reference is in `BRAND.md`.

Questions: dylan@mondayandpartners.com
