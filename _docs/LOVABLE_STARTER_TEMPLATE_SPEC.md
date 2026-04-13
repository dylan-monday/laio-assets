# LA.IO Lovable Starter Template — Build Spec

This document defines the starter template project. Fork this project at the start of any new LA.IO Lovable build.

---

## Project setup

### File structure
```
/
├── LAIO_BRAND.md              ← attach to every project
├── tailwind.config.js
├── src/
│   ├── styles/
│   │   ├── globals.css        ← font imports, CSS custom properties
│   │   └── laio-tokens.css    ← color + type tokens as CSS vars
│   ├── components/
│   │   ├── ui/
│   │   │   ├── LaioLogo.jsx
│   │   │   ├── LaioMark.jsx   ← bracket/chevron elements
│   │   │   ├── Button.jsx
│   │   │   ├── Badge.jsx
│   │   │   └── Divider.jsx
│   │   ├── layout/
│   │   │   ├── Nav.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Section.jsx
│   │   └── blocks/
│   │       ├── StatCard.jsx
│   │       ├── FeatureBlock.jsx
│   │       ├── PartnerGrid.jsx
│   │       └── ContentBlock.jsx
│   └── lib/
│       └── laio-colors.js     ← color constants for JS use
```

---

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        laio: {
          // Magenta family
          'drk-purple':        '#101948',
          'easy-magenta':      '#E385FE',
          'electric-magenta':  '#F629CB',
          // Green family
          'drk-green':         '#172708',
          'easy-green':        '#C8ED5D',
          'electric-green':    '#96F90B',
          // Blue family
          'drk-blue':          '#01233C',
          'easy-blue':         '#63DCDE',
          'electric-blue':     '#00B9FE',
          // Orange family
          'drk-orange':        '#302511',
          'easy-orange':       '#F1DC43',
          'electric-orange':   '#F5C124',
          // Gray / Neutral
          'drk-gray':          '#231F20',
          'gray':              '#929497',
          'easy-gray':         '#E3E6E7',
          'white':             '#FFFFFF',
        },
      },
      fontFamily: {
        laio: ['Aktiv Grotesk', 'Roboto', 'system-ui', 'sans-serif'],
      },
      fontWeight: {
        light: '300',
        regular: '400',
        bold: '700',
      },
      borderRadius: {
        'laio': '2px',      // brand standard — angular
        'laio-tag': '3px',  // tags and badges only
      },
    },
  },
  plugins: [],
}
```

---

## globals.css

Two font loading options depending on deployment context. Use Option A for all Lovable projects.

**Option A — Adobe Fonts embed (preferred for Lovable / web projects)**

Add to `index.html` `<head>`:
```html
<link rel="stylesheet" href="https://use.typekit.net/usf5bjl.css">
```

Then in `globals.css`:
```css
:root {
  --font-laio: 'aktiv-grotesk', 'Roboto', system-ui, sans-serif;
  --radius-laio: 2px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: var(--font-laio);
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
}
```

Note: Adobe Fonts serves Aktiv Grotesk as `'aktiv-grotesk'` (lowercase, hyphenated) — not `'Aktiv Grotesk'`. Use that exact string.

**Option B — Self-hosted woff2 (for offline, print-adjacent, or non-Adobe contexts)**

woff2 files live in `fonts/` in this asset directory. Copy the three needed weights to `/public/assets/fonts/` in the Lovable project:
+ `AktivGrotesk-Light.woff2` (300)
+ `AktivGrotesk-Regular.woff2` (400)
+ `AktivGrotesk-Bold.woff2` (700)

```css
@font-face {
  font-family: 'Aktiv Grotesk';
  src: url('/assets/fonts/AktivGrotesk-Light.woff2') format('woff2');
  font-weight: 300;
  font-style: normal;
}
@font-face {
  font-family: 'Aktiv Grotesk';
  src: url('/assets/fonts/AktivGrotesk-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}
@font-face {
  font-family: 'Aktiv Grotesk';
  src: url('/assets/fonts/AktivGrotesk-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
}

:root {
  --font-laio: 'Aktiv Grotesk', 'Roboto', system-ui, sans-serif;
  --radius-laio: 2px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: var(--font-laio);
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
}
```

---

## laio-colors.js (for JS/logic use)

```js
export const LAIO_COLORS = {
  magenta: {
    dark:     '#101948',
    easy:     '#E385FE',
    electric: '#F629CB',
  },
  green: {
    dark:     '#172708',
    easy:     '#C8ED5D',
    electric: '#96F90B',
  },
  blue: {
    dark:     '#01233C',
    easy:     '#63DCDE',
    electric: '#00B9FE',
  },
  orange: {
    dark:     '#302511',
    easy:     '#F1DC43',
    electric: '#F5C124',
  },
  gray: {
    dark:     '#231F20',
    mid:      '#929497',
    light:    '#E3E6E7',
    white:    '#FFFFFF',
  },
}

// Suggested pairings (bg → accent)
export const LAIO_THEMES = {
  magenta: { bg: LAIO_COLORS.magenta.dark, accent: LAIO_COLORS.magenta.easy },
  green:   { bg: LAIO_COLORS.green.dark,   accent: LAIO_COLORS.green.easy },
  blue:    { bg: LAIO_COLORS.blue.dark,    accent: LAIO_COLORS.blue.easy },
  orange:  { bg: LAIO_COLORS.orange.dark,  accent: LAIO_COLORS.orange.easy },
  light:   { bg: LAIO_COLORS.gray.light,   accent: LAIO_COLORS.gray.dark },
}
```

---

## Component specs

### LaioLogo.jsx

Production component with real path data is in this asset directory as `LaioLogo.jsx`.
Copy it directly into `src/components/ui/LaioLogo.jsx` in any Lovable project.

Props: `fill` (hex or CSS color, default `'#231F20'`), `width` (px, default `220`), `className`, `aria-label`

```jsx
// Usage examples
<LaioLogo />
<LaioLogo fill="#C8ED5D" width={320} />
<LaioLogo fill="#FFFFFF" width={160} />
<LaioLogo fill="var(--brand-accent)" width={200} />
```

Native viewBox: `274.65 × 67.88` (approx 4:1 ratio). Height always scales proportionally from width.
Minimum legible width: 120px. Do not use `<img>` — always inline SVG for fill control.

### Button.jsx
```jsx
// Variants: 'primary' (filled), 'outline', 'ghost'
// No border-radius beyond 2px — brand standard is angular
// Props: variant, color (laio color hex), children, onClick

const styles = {
  primary: (color) => ({
    background: color,
    color: '#FFFFFF',
    border: 'none',
    padding: '10px 24px',
    borderRadius: '2px',
    fontFamily: 'var(--font-laio)',
    fontWeight: 700,
    letterSpacing: '0.04em',
    cursor: 'pointer',
  }),
  outline: (color) => ({
    background: 'transparent',
    color: color,
    border: `1.5px solid ${color}`,
    padding: '10px 24px',
    borderRadius: '2px',
    fontFamily: 'var(--font-laio)',
    fontWeight: 700,
    letterSpacing: '0.04em',
    cursor: 'pointer',
  }),
}
```

### Hero.jsx
```jsx
// Full-bleed dark hero with headline, optional subhead, optional CTA
// Props: theme (LAIO_THEMES key), headline, subhead, cta, backgroundImage
// Default: dark background, Easy accent headline, white body

// Layout:
// - 100vw width, min 70vh height
// - Padding: 80px horizontal, 120px vertical (desktop)
// - Headline: Aktiv Grotesk Bold or Light, very large (clamp 48px to 96px)
// - Accent color applied to a structural bar above headline OR headline itself
// - LaioLogo in upper left, white fill
// - Optional bracket mark as supergraphic (cropped, large-scale)
```

### StatCard.jsx
```jsx
// For numeric/metric display — dashboards, reports, event stats
// Props: label, value, unit, accent (color hex)
// Layout: label (small, muted), value (large, bold), accent left-border

// Style: dark or light background, accent color as 3px left border
// No rounded corners. No drop shadows.
```

### Nav.jsx
```jsx
// Props: theme ('dark' | 'light'), links (array of {label, href})
// Dark theme: background laio-drk-[family], logo white, links Easy accent on hover
// Light theme: white background, logo dark, links dark on hover
// No hamburger menus unless explicitly mobile-first — prefer horizontal nav

// Structure:
// [LaioLogo] ............. [Link] [Link] [Link] [CTA Button]
```

### Footer.jsx
```jsx
// Minimal — brand signal, not information dump
// Props: theme, descriptor (bool — shows "A Division of Louisiana Economic Development")
// Contains: LaioLogo, optional descriptor line, optional links, badge embed slot
// No multi-column footer unless the project has substantial secondary navigation
```

---

## Prompt to initialize a new project

## List styling — the + bullet

All lists in LA.IO projects use `+` as the marker, never `•`, `-`, or `*`.

In CSS:
```css
ul.laio-list {
  list-style: none;
  padding: 0;
}
ul.laio-list li::before {
  content: '+ ';
  font-weight: 700;
  margin-right: 4px;
}
```

In Tailwind + JSX:
```jsx
function LaioList({ items }) {
  return (
    <ul className="space-y-2">
      {items.map((item, i) => (
        <li key={i} className="flex gap-2">
          <span className="font-bold shrink-0">+</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}
```

The three pillars always appear as:
```jsx
<LaioList items={['Capital', 'Coaching', 'Connections']} />
```

---

## Prompt to initialize a new project

Use this as the first message in any new Lovable project:

```
Initialize this project as an LA.IO brand project. Apply the following setup:

1. Configure tailwind.config.js with the full LAIO color token set (see LAIO_BRAND.md)
2. Set up globals.css with Aktiv Grotesk font stack and Roboto fallback via Google Fonts
3. Create src/lib/laio-colors.js with the full color constants and theme pairings
4. Create skeleton components: LaioLogo.jsx, Button.jsx, Nav.jsx, Hero.jsx, Footer.jsx
5. This project uses the [BLUE / GREEN / MAGENTA / ORANGE] color family — configure accordingly

This project is: [describe the project]
Primary audience: [audience]
Color family for this project: [family]

Do not deviate from the brand system documented in LAIO_BRAND.md. Apply the voice rules to any generated copy.

Voice reminders for this project:
- Never use em dashes. Rewrite any sentence that requires one.
- Never use "it's not X, it's Y" constructions.
- Use + as the list bullet, never • or -.
- The three pillars are: + Capital / + Coaching / + Connections — always in that order.
```

---

## Asset directory (to be populated)

```
/public/assets/
├── logos/
│   ├── laio-wordmark.svg           ← base black wordmark
│   ├── laio-wordmark-white.svg     ← white variant for dark backgrounds
│   ├── laio-mark-left.svg          ← left bracket only
│   ├── laio-mark-right.svg         ← right bracket only
│   ├── laio-horizontal.svg         ← horizontal layout variant
│   └── laio-favicon.ico
├── marks/
│   ├── bracket-pair.svg            ← < > together
│   ├── chevron-right.svg           ← >
│   ├── chevron-left.svg            ← <
│   ├── chevron-down.svg            ← v
│   ├── chevron-up.svg              ← ^
│   ├── diamond-filled.svg          ← ◆
│   ├── diamond-outline.svg         ← ◇
│   ├── cross.svg                   ← +
│   ├── corner-tl.svg               ← ⌐ top-left corner mark
│   ├── corner-tr.svg               ← top-right corner mark
│   └── corner-br.svg               ← ¬ bottom-right corner mark
└── fonts/
    ├── AktivGrotesk-Light.woff2
    ├── AktivGrotesk-Regular.woff2
    └── AktivGrotesk-Bold.woff2
```

All SVG mark files: single path, fill `#231F20`, no background. Apply color via CSS or prop.
