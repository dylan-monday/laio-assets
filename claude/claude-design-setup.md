# LA.IO on Claude Design

Claude Design has a first-class **Design System** feature. You create an **LA.IO Design System** once (from a prompt + references), then pick it from the *Design System* dropdown on any new project (Prototype, Slide deck, From template) and everything comes out on brand.

Design systems are account-bound, so each person who designs LA.IO work creates their own copy. It takes a couple of minutes and the prompt below makes it identical every time.

## Steps

1. In Claude Design, start a **new Design System** the same way the other systems were made: from a prompt plus reference files.
2. Paste the **creation prompt** below.
3. Attach references:
   + `LAIO-COMPLETE.svg` (the logo) from `https://assets.la.io/logos/`
   + One or two motifs from `https://assets.la.io/motifs/` (e.g. `LAIO-LEFT-BRACKET.svg`, `LAIO-PLUS.svg`)
   + Optional but recommended: a screenshot of `https://assets.la.io/claude/` as a "brand in action" reference
4. Name it exactly: **LA.IO Design System**
5. On any New Project, choose **LA.IO Design System** from the *Design System* dropdown.

## Creation prompt (paste this)

```
Create a design system called "LA.IO Design System" for LA.IO (Louisiana Innovation Office), the operating brand for Louisiana's innovation ecosystem. It should feel technical, precise, confident, and aspirational. Use the attached LA.IO logo and references.

COLOR. Five color families, each with a dark ground, an "easy" accent, and an "electric" accent. Any single artifact uses ONE family: the dark stop as background, easy or electric as accents and structural elements. Never mix families in one piece. Body text is white on dark backgrounds, or the dark brand color on light, never an accent color. Default to the Magenta family for tech, AI, and digital work unless told otherwise.
  Magenta: #101948 / #E385FE / #F629CB
  Green:   #172708 / #C8ED5D / #96F90B
  Blue:    #01233C / #63DCDE / #00B9FE
  Orange:  #302511 / #F1DC43 / #F5C124
  Gray:    #231F20 / #E3E6E7 / #929497
Light neutral background option: #E3E6E7.

TYPOGRAPHY. Two typefaces, strictly separated.
  Aktiv Grotesk for headlines, body, and UI. Headlines use Light (300) or Bold (700) only, never a middle weight. Body is Regular (400). Load via Adobe Fonts ("aktiv-grotesk") or self-hosted woff2 at https://assets.la.io/fonts/.
  JetBrains Mono for eyebrows, labels, tags, and metadata only. Always all caps, letter-spacing about 0.1em, in a brand accent color. Never for body copy or paragraphs.

LOGO AND MOTIFS. Use the real LA.IO assets, never recreate the logo. The logo is a monospace wordmark bracketed by chevrons: < LA.IO >. Files are single-fill near-black (#231F20); recolor by overriding the fill. Logo: https://assets.la.io/logos/LAIO-COMPLETE.svg (also LAIO-BASE, LAIO-HORZ). Motifs (brackets, chevrons, plus, diamond, X): https://assets.la.io/motifs/. Use brackets and chevrons as framing devices and supergraphics: scale freely, crop intentionally, never scatter as decoration. Never frame the logo itself with additional brackets.

LAYOUT AND COMPONENTS. Angular and restrained. Border-radius 0 to 2px (small tags up to 3px). No gradients, no drop shadows. Commit to dark or light backgrounds, never mid-range. Generous whitespace; every element has structural purpose. Buttons are flat with a 2px radius. Cards are dark background with an accent border, or light background with an accent border. Use "+" as the list bullet, never a dot, hyphen, or asterisk.

VOICE for any generated copy. Matter-of-fact confidence, short declarative sentences, state the case then stop. Never use "resilience", "Silicon Bayou", "innovative solutions", "cutting-edge", "disruptive", em dashes, "it's not X, it's Y" constructions, or Louisiana cliches (jazz, Mardi Gras, Bourbon Street, crawfish).

The three pillars, when listed, always in this order: + Capital / + Coaching / + Connections.

Name the design system exactly: LA.IO Design System
```

## If something comes out off-brand

Tell Claude Design specifically: "stay in one color family", "headline should be Aktiv Grotesk Bold", "use + as the bullet", "remove the rounded corners", "accent color on the border only, not as a fill". The fuller reference is in `BRAND.md`.

Questions: dylan@mondayandpartners.com
