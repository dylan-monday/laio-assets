---
name: laio-brand
description: >-
  The LA.IO (Louisiana Innovation Office) brand system. Use whenever building,
  writing, or designing anything for LA.IO or its ecosystem partners — websites,
  landing pages, event pages, dashboards, partner tools, decks, emails, social
  copy, or any on-brand asset. Provides the voice rules, color families,
  typography, logo and motif library, ready-to-paste component code, and hosted
  asset URLs. Trigger on any mention of LA.IO, Louisiana Innovation, or a request
  to make something "on brand" for this client.
---

# LA.IO Brand System

LA.IO (Louisiana Innovation Office) is the operating brand for Louisiana's innovation ecosystem. This skill makes everything you produce — copy, layout, code, design — match the brand exactly.

**Read this whole file before generating anything for LA.IO.** Load the deeper references only when you need them (see end).

> The brand in one sentence: *Louisiana doesn't sell itself. It states what's true, and the truth is enough.*

---

## Voice — applies to every line of copy

Matter-of-fact confidence. Short, declarative sentences. State the case, then stop. No persuasion, no hype, no hedging. Show the work and trust the reader to connect the dots.

**Never write these — rewrite if they appear:**

+ "resilience" / "resilient" (victim language)
+ "Silicon Bayou" or any `[Place] + [Tech nickname]` construction
+ "innovative solutions" / "cutting-edge" / "disruptive" / "transformative"
+ "rethink" / "reimagine" Louisiana — there is nothing to rethink
+ Louisiana cultural clichés: jazz, Bourbon Street, Mardi Gras, crawfish, "laissez les bons temps rouler"
+ "it's not X, it's Y" / "it's not just X, it's Y" constructions
+ "problems" as a framing device — Louisiana addresses challenges, not problems
+ Em dashes (—) anywhere. If a sentence needs one, rewrite the sentence.
+ Inspirational-poster cadence ("Together we can…", "The future is bright…")
+ Acknowledging a negative perception in order to correct it

**Always:**

+ Use `+` as the list bullet. Never `•`, `-`, or `*`.
+ Keep copy spare. Every sentence earns its place or gets cut.
+ Lead with fact, not persuasion.

**The three pillars — always this exact phrasing and order:**

```
+ Capital
+ Coaching
+ Connections
```

**Calibration — these lines are canonically on-brand:**

+ The Future Flows Through Louisiana
+ The Robots are Coming … and Louisiana is Ready.
+ Local Frequency. Global Signal.
+ Louisiana has always built what the world needs next.
+ Louisiana Innovation Creates Global Solutions

---

## Color — five families, one per piece

Stay within **one** family per project/page/deck. Do not mix families without a strong structural reason. Dark stop = background. Easy / Electric = accents, labels, interactive elements, type on dark. Body copy is white on dark, or the dark brand color on light — **never** an accent color.

| Family | Dark (bg) | Easy (accent) | Electric (high-energy) | Best for |
|--------|-----------|---------------|------------------------|----------|
| Magenta | `#101948` | `#E385FE` | `#F629CB` | Tech, AI, high-energy digital |
| Green | `#172708` | `#C8ED5D` | `#96F90B` | Agriculture, energy, sustainability |
| Blue | `#01233C` | `#63DCDE` | `#00B9FE` | Partner tools, credibility-forward work |
| Orange | `#302511` | `#F1DC43` | `#F5C124` | Events, announcements, bold statements |
| Gray | `#231F20` | `#E3E6E7` | `#929497` (mid) | Neutral, functional, dashboards |

Accent colors are architectural — borders, bars, dividers, mono labels — not full-section fills. Hosted tokens: `https://assets.la.io/colors/laio-colors.css` (CSS vars) and `https://assets.la.io/colors/laio-tokens.json`. Local copies in `assets/colors/`.

---

## Typography — two typefaces, strictly separated

**Aktiv Grotesk** — headlines, body, UI. Bias to the extremes: Light (300) or Bold (700) for headlines, never a middle weight. Regular (400) for body.

```html
<link rel="stylesheet" href="https://use.typekit.net/usf5bjl.css">
```
```css
font-family: 'aktiv-grotesk', 'Roboto', system-ui, sans-serif; /* Adobe kit serves it lowercase-hyphenated */
```
Self-hosted fallback (offline/print): woff2 at `https://assets.la.io/fonts/AktivGrotesk_{Lt,Rg,Bd}.woff2`, declared as `'Aktiv Grotesk'` (title case).

**JetBrains Mono** — eyebrows, labels, tags, metadata **only**. All caps, letter-spacing `0.08`–`0.12em`, weights 400/700, always a brand **accent** color (never white/gray as standalone). Never body copy.

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

---

## Logo & motifs

Use the hosted SVGs — never recreate the logo in code. All are single-fill near-black (`#231F20`); apply brand color by overriding `fill`.

```
https://assets.la.io/logos/LAIO-COMPLETE.svg   ← full wordmark + LOUISIANA INNOVATION
https://assets.la.io/logos/LAIO-BASE.svg        ← < LA.IO > no subtext
https://assets.la.io/logos/LAIO-HORZ.svg        ← horizontal
https://assets.la.io/logos/LOUISIANA-INNOVATION-A.svg
https://assets.la.io/logos/LOUISIANA-INNOVATION-B.svg
https://assets.la.io/logos/DIVISION-LINE.svg
```

For React, use `assets/LaioLogo.jsx` (inline SVG, `fill` + `width` props). Logo latitude is wide: large, cropped, bleeding off edges, supergraphic — as long as it stays legible.

Motifs (brackets, chevrons, diamonds, plus, X, corners) at `https://assets.la.io/motifs/` and in `assets/motifs/`. Use as framing devices, section markers, and supergraphics. Scale freely, crop intentionally, never scatter as decoration. The `+` is the brand bullet and can be built from corner pieces at any scale.

---

## Design principles

+ **Angular.** `border-radius: 0`, `2px` max on structural elements. Rounded only on small tags/badges.
+ **Committed.** Dark or light background, never mid-range. One family. One typographic register per layout.
+ **Structural.** Every element has a reason to exist. No decoration for its own sake.
+ **Spare.** Generous whitespace. Busy layouts have failed.

**The test for every layout:** Does it increase clarity? Does it respect the audience's intelligence? Is it trying too hard (if yes, cut back)? Would it work in a Baton Rouge industrial facility *and* a London transit ad?

---

## When to load more

This file is enough for most copy and quick design calls. For deeper work, read the bundled references:

+ **`BRAND.md`** — full brand reference: thesis, audiences, photography direction, the badge system, complete color/voice/design detail.
+ **`COMPONENTS.md`** — copy-paste component code (React + plain HTML/CSS): logo, button, eyebrow, `+`-list, hero, stat card, nav, footer, plus Tailwind config and font setup.
+ **`assets/`** — local logo/motif SVGs, color CSS + tokens, and `LaioLogo.jsx` for offline or self-hosted contexts.
