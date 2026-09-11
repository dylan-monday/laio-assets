# LA.IO Starter Template — Lovable Build Prompt

Paste this as the first message when building the starter template project.
Replace nothing — this is complete as written.

---

```
This is the LA.IO brand starter template. Apply all workspace brand instructions.

## Font setup

Add to index.html <head>:
<link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">

laio-fonts.css declares every Aktiv Grotesk weight. Do not write @font-face rules by hand.

If the preview cannot reach assets.la.io and shows a fallback font, also paste the full contents of https://assets.la.io/fonts/laio-fonts-inline.css into a <style> tag in index.html <head>. It embeds Light, Regular and Bold with zero network requests.

Family name 'Aktiv Grotesk' (title case, never 'aktiv-grotesk'). Headlines Light 300 or Bold 700, never a middle weight. Body Regular 400. Roboto is a fallback only when neither file can load. If you fall back to it, say so.

Add to src/styles/globals.css:

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
/**
 * LaioLogo.jsx
 * LA.IO complete wordmark — < LA.IO > with LOUISIANA INNOVATION subtext
 *
 * Props:
 *   fill      — any hex string or CSS color value (default: '#231F20')
 *   width     — rendered width in px; height scales proportionally (default: 220)
 *   className — additional CSS classes
 *   aria-label — accessible label (default: 'LA.IO Louisiana Innovation')
 *
 * Usage:
 *   <LaioLogo />
 *   <LaioLogo fill="#C8ED5D" width={320} />
 *   <LaioLogo fill="#FFFFFF" width={160} className="opacity-90" />
 *
 * Color application:
 *   Pass any LA.IO brand color as the fill prop. All paths share one fill.
 *   For dynamic theming, pass a CSS variable: fill="var(--brand-accent)"
 *
 * Sizing:
 *   Native viewBox is 274.65 × 67.88 (approx 4:1 ratio).
 *   Width drives the size; height is always proportional.
 *   Minimum legible width: ~120px.
 *
 * Minimum clear space:
 *   The square dot/pixel in the logo is the base unit.
 *   Maintain 3× that unit of clear space on all sides.
 *   Approximately: clear space = width × 0.035 on each side.
 */

export default function LaioLogo({
  fill = '#231F20',
  width = 220,
  className = '',
  'aria-label': ariaLabel = 'LA.IO Louisiana Innovation',
}) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 274.65 67.88"
      width={width}
      height={Math.round((width / 274.65) * 67.88)}
      className={className}
      role="img"
      aria-label={ariaLabel}
    >
      <g fill={fill}>

        {/* LOUISIANA INNOVATION subtext */}
        <g>
          <path d="M60.22,49.17v5.16h3.33v1.61h-5.16v-6.77h1.83Z"/>
          <path d="M69,56.07c-1.74,0-3.04-1.43-3.04-3.51s1.3-3.51,3.04-3.51,3.04,1.43,3.04,3.51-1.3,3.51-3.04,3.51ZM69,50.65c-.73,0-1.19.75-1.19,1.9s.46,1.9,1.19,1.9,1.19-.75,1.19-1.9-.46-1.9-1.19-1.9Z"/>
          <path d="M74.39,53.21v-4.04h1.82v3.74c0,1.03.17,1.62,1,1.62s1-.59,1-1.62v-3.74h1.83v4.04c0,1.98-1.19,2.86-2.83,2.86s-2.82-.88-2.82-2.86Z"/>
          <path d="M82.83,55.94v-1.58h1.69v-3.61h-1.69v-1.58h5.2v1.58h-1.69v3.61h1.69v1.58h-5.2Z"/>
          <path d="M91.65,53.6c.49.67,1.23,1,2.01,1,.66,0,1.04-.2,1.04-.58s-.32-.44-.61-.5l-1.39-.31c-1.01-.23-1.77-.77-1.77-1.96,0-1.32,1.02-2.2,2.59-2.2,1.2,0,2.1.49,2.74,1.25l-1.1,1.14c-.35-.52-.81-.91-1.64-.91-.51,0-.88.23-.88.57,0,.31.25.41.52.47l1.34.31c1.34.31,1.93.93,1.93,2.04,0,1.41-1.25,2.16-2.77,2.16-1.34,0-2.3-.43-3.03-1.18l1.02-1.29Z"/>
          <path d="M99.26,55.94v-1.58h1.69v-3.61h-1.69v-1.58h5.2v1.58h-1.69v3.61h1.69v1.58h-5.2Z"/>
          <path d="M111.03,54.63h-2.01l-.37,1.31h-1.77l2.07-6.77h2.24l2.07,6.77h-1.87l-.37-1.31ZM109.41,53.26h1.25l-.6-2.15h-.04l-.6,2.15Z"/>
          <path d="M119.44,53.12v-3.96h1.65v6.77h-1.71l-2.27-4.63v4.63h-1.66v-6.77h2.17l1.81,3.96Z"/>
          <path d="M127.45,54.63h-2.01l-.37,1.31h-1.77l2.07-6.77h2.24l2.07,6.77h-1.87l-.37-1.31ZM125.83,53.26h1.25l-.6-2.15h-.04l-.6,2.15Z"/>
          <path d="M137.49,55.94v-.81h1.91v-5.16h-1.91v-.81h4.76v.81h-1.9v5.16h1.9v.81h-4.76Z"/>
          <path d="M149.74,54.41v-5.24h.87v6.77h-.83l-3.35-5.59v5.59h-.87v-6.77h1.1l3.08,5.24Z"/>
          <path d="M157.96,54.41v-5.24h.87v6.77h-.83l-3.35-5.59v5.59h-.87v-6.77h1.1l3.08,5.24Z"/>
          <path d="M164.51,56.07c-1.63,0-2.82-1.43-2.82-3.51s1.18-3.51,2.82-3.51,2.82,1.43,2.82,3.51-1.18,3.51-2.82,3.51ZM164.51,49.86c-1.12,0-1.85,1.04-1.85,2.7s.73,2.7,1.85,2.7,1.85-1.04,1.85-2.7-.73-2.7-1.85-2.7Z"/>
          <path d="M172.17,55.94l-2.27-6.77h1.01l1.83,5.66h.04l1.81-5.66h.97l-2.27,6.77h-1.12Z"/>
          <path d="M182.14,53.96h-2.47l-.63,1.98h-.92l2.26-6.77h1.14l2.26,6.77h-.98l-.64-1.98ZM179.92,53.21h1.99l-.98-3.01h-.04l-.97,3.01Z"/>
          <path d="M188.67,55.94v-5.95h-2.4v-.82h5.76v.82h-2.43v5.95h-.93Z"/>
          <path d="M194.98,55.94v-.81h1.91v-5.16h-1.91v-.81h4.76v.81h-1.9v5.16h1.9v.81h-4.76Z"/>
          <path d="M205.58,56.07c-1.63,0-2.82-1.43-2.82-3.51s1.18-3.51,2.82-3.51,2.82,1.43,2.82,3.51-1.18,3.51-2.82,3.51ZM205.58,49.86c-1.12,0-1.85,1.04-1.85,2.7s.73,2.7,1.85,2.7,1.85-1.04,1.85-2.7-.73-2.7-1.85-2.7Z"/>
          <path d="M215.45,54.41v-5.24h.87v6.77h-.83l-3.35-5.59v5.59h-.87v-6.77h1.1l3.08,5.24Z"/>
        </g>

        {/* Center dot — period in LA.IO */}
        <path d="M131.74,32.01h8.52v8.52h-8.52v-8.52Z"/>

        {/* LA.IO main letterforms */}
        <g>
          <path d="M65.87,12.58v21.29h13.75v6.65h-21.29V12.58h7.54Z"/>
          <path d="M106.06,35.11h-8.29l-1.51,5.41h-7.32l8.56-27.94h9.22l8.56,27.94h-7.72l-1.51-5.41ZM99.36,29.48h5.14l-2.48-8.87h-.18l-2.48,8.87Z"/>
          <path d="M159.15,40.53v-6.52h6.96v-14.9h-6.96v-6.52h21.47v6.52h-6.96v14.9h6.96v6.52h-21.47Z"/>
          <path d="M203.77,41.06c-7.19,0-12.55-5.9-12.55-14.5s5.37-14.5,12.55-14.5,12.55,5.9,12.55,14.5-5.37,14.5-12.55,14.5ZM203.77,18.7c-3.02,0-4.92,3.11-4.92,7.85s1.91,7.85,4.92,7.85,4.92-3.11,4.92-7.85-1.91-7.85-4.92-7.85Z"/>
        </g>

        {/* Left bracket < */}
        <polygon points="14.73 33.94 41.3 60.51 33.94 67.88 0 33.94 33.94 0 41.3 7.36 14.73 33.94"/>

        {/* Right bracket > */}
        <polygon points="259.93 33.94 233.35 7.36 240.72 0 274.65 33.94 240.72 67.88 233.35 60.51 259.93 33.94"/>

      </g>
    </svg>
  )
}


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
