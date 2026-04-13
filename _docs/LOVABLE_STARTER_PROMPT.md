# LA.IO Starter Template — Lovable Build Prompt

Paste this as the first message when building the starter template project.
Replace nothing — this is complete as written.

---

```
This is the LA.IO brand starter template. Apply all workspace brand instructions.

## Font setup

Add to index.html <head>:
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">

Add @font-face declarations to src/styles/globals.css:

@font-face {
  font-family: 'Aktiv Grotesk';
  src: url('https://assets.la.io/fonts/AktivGrotesk_Lt.woff2') format('woff2');
  font-weight: 300;
  font-style: normal;
}
@font-face {
  font-family: 'Aktiv Grotesk';
  src: url('https://assets.la.io/fonts/AktivGrotesk_Rg.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}
@font-face {
  font-family: 'Aktiv Grotesk';
  src: url('https://assets.la.io/fonts/AktivGrotesk_Bd.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
}

:root { --font-laio: 'Aktiv Grotesk', 'Roboto', system-ui, sans-serif; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-laio); font-weight: 400; -webkit-font-smoothing: antialiased; }

## Tailwind config

extend: {
  colors: {
    laio: {
      'drk-purple':'#101948', 'easy-magenta':'#E385FE', 'electric-magenta':'#F629CB',
      'drk-green':'#172708',  'easy-green':'#C8ED5D',   'electric-green':'#96F90B',
      'drk-blue':'#01233C',   'easy-blue':'#63DCDE',    'electric-blue':'#00B9FE',
      'drk-orange':'#302511', 'easy-orange':'#F1DC43',  'electric-orange':'#F5C124',
      'drk-gray':'#231F20',   'gray':'#929497',          'easy-gray':'#E3E6E7',
    }
  },
  fontFamily: {
    'laio': ['Aktiv Grotesk', 'Roboto', 'system-ui', 'sans-serif'],
    'laio-mono': ['JetBrains Mono', 'monospace'],
  },
  borderRadius: { 'laio': '2px' },
}

## Components to create

### src/components/ui/LaioLogo.jsx
[paste full contents of LaioLogo.jsx here]

### src/components/ui/Button.jsx
Variants: primary (filled), outline, ghost.
Props: variant, color (hex), children, onClick.
border-radius: 2px. font-family: Aktiv Grotesk Bold. letter-spacing: 0.04em.
No gradients, no shadows.

### src/components/ui/Eyebrow.jsx
Renders a label/eyebrow line above headlines.
Font: JetBrains Mono. Always all caps. letter-spacing: 0.1em.
Props: children, color (hex — should be a brand accent color).
Never renders in white or gray as standalone text.

### src/components/ui/LaioList.jsx
Renders a list using + as the bullet marker.
Props: items (array of strings or JSX).
Implementation: flex row with a bold + character and the item text.
Never uses • - or * as markers.

### src/components/layout/Nav.jsx
Props: theme ('dark' | 'light'), links (array of {label, href}), cta ({label, href}).
Dark: background is dark family color, LaioLogo white, links in Easy accent on hover.
Light: white background, LaioLogo dark, links dark on hover.
Horizontal layout. No hamburger for desktop. Clean, no gradients.

### src/components/layout/Hero.jsx
Full-bleed section. Min height 70vh.
Props: theme (color family key), headline, subhead, eyebrow, cta, backgroundImage.
Eyebrow: JetBrains Mono, all caps, Easy accent color.
Headline: Aktiv Grotesk Bold or Light, very large (clamp 48px to 96px), white.
Subhead: Aktiv Grotesk Regular, white, 18-20px.
No gradients. Dark background. Angular layout.

### src/components/layout/Footer.jsx
Minimal. Props: theme, showDescriptor (bool).
Contains: LaioLogo, optional "A Division of Louisiana Economic Development" line, optional nav links.
No multi-column layout unless project requires it.

### src/components/blocks/StatCard.jsx
Metric display. Props: label, value, unit, accent (hex).
Label: JetBrains Mono, all caps, accent color.
Value: Aktiv Grotesk Bold, large.
3px left border in accent color. border-radius: 0. No shadows.

### src/lib/laio-colors.js
export const LAIO_COLORS = {
  magenta: { dark:'#101948', easy:'#E385FE', electric:'#F629CB' },
  green:   { dark:'#172708', easy:'#C8ED5D', electric:'#96F90B' },
  blue:    { dark:'#01233C', easy:'#63DCDE', electric:'#00B9FE' },
  orange:  { dark:'#302511', easy:'#F1DC43', electric:'#F5C124' },
  gray:    { dark:'#231F20', mid:'#929497',  light:'#E3E6E7'    },
}
export const LAIO_THEMES = {
  magenta: { bg:'#101948', easy:'#E385FE', electric:'#F629CB' },
  green:   { bg:'#172708', easy:'#C8ED5D', electric:'#96F90B' },
  blue:    { bg:'#01233C', easy:'#63DCDE', electric:'#00B9FE' },
  orange:  { bg:'#302511', easy:'#F1DC43', electric:'#F5C124' },
  light:   { bg:'#E3E6E7', easy:'#231F20', electric:'#101948' },
}

## Demo page

Build App.jsx as a demo showing all components using the Blue color family (#01233C dark, #63DCDE accent).

The demo should show in sequence:
1. Nav (dark theme, Blue family)
2. Hero with JetBrains Mono eyebrow in #63DCDE, Aktiv Grotesk Bold headline in white
3. A row of three StatCards with #63DCDE accent borders
4. A content section with a LaioList using + bullets
5. Footer with LaioLogo and descriptor line

All copy should be on-brand: matter-of-fact, no em dashes, no filler words.
Use real LA.IO language — "Local Frequency. Global Signal." is a valid headline.

Name this project: LA.IO Starter Template
```
