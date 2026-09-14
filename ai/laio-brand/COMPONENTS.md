# LA.IO Components

Copy-paste building blocks for LA.IO projects. Each block has a **React** version (for Claude Code / app projects) and, where useful, a **plain HTML/CSS** version (for Claude Design, artifacts, emails, decks). All follow the brand: angular, one color family, `+` bullets, Aktiv Grotesk + JetBrains Mono.

Pick one color family per project (see `SKILL.md`). Examples below use the **Magenta** family (`#101948` / `#E385FE` / `#F629CB`) — swap the three hexes to re-skin.

---

## 1. Setup — fonts, tokens, Tailwind

**Aktiv Grotesk**, family name `'Aktiv Grotesk'` (title case, never `'aktiv-grotesk'`). Headlines Light 300 or Bold 700, never a middle weight. Body Regular 400.

Three ways to load it, in this order of preference:

+ **Embedded:** paste the contents of `laio-fonts-inline.css` into a `<style>` tag. Zero network requests. Use in claude.ai artifacts, Claude Design, Lovable previews, email, anything sandboxed. This is the default for AI-generated work.
+ **Hosted, for real sites and apps on a domain only, never inside an artifact or preview:** `<link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css">`.
+ **Fallback:** Roboto from Google Fonts, only when neither of the above is possible. Say so in the handoff. Roboto is a stand-in, never the goal. Never Roboto inside an artifact; embed instead.

font-family stack: `'Aktiv Grotesk', 'Roboto', system-ui, sans-serif`

`laio-fonts-inline.css` ships in the `laio-brand` skill at `assets/fonts/laio-fonts-inline.css`, and in a claude.ai Project as uploaded knowledge.

**JetBrains Mono** for eyebrows, labels, tags, metadata only. All caps, letter-spacing 0.08 to 0.12em, weights 400/700, always a brand accent color. Google Fonts: `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap`

**`index.html` `<head>`, real site or app:**
```html
<link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://assets.la.io/colors/laio-colors.css">
```

**`<head>`, artifact or any sandbox (the default for AI-generated work):**
```html
<style>
  /* paste the full contents of laio-fonts-inline.css here */
</style>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

**Base CSS:**
```css
:root {
  --font-laio: 'Aktiv Grotesk', 'Roboto', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --radius-laio: 2px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font-laio);
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
}
```

**`tailwind.config.js`:**
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        laio: {
          'drk-purple': '#101948', 'easy-magenta': '#E385FE', 'electric-magenta': '#F629CB',
          'drk-green':  '#172708', 'easy-green':   '#C8ED5D', 'electric-green':   '#96F90B',
          'drk-blue':   '#01233C', 'easy-blue':    '#63DCDE', 'electric-blue':    '#00B9FE',
          'drk-orange': '#302511', 'easy-orange':  '#F1DC43', 'electric-orange':  '#F5C124',
          'drk-gray':   '#231F20', 'gray':         '#929497', 'easy-gray':        '#E3E6E7',
          'white':      '#FFFFFF',
        },
      },
      fontFamily: {
        laio: ['Aktiv Grotesk', 'Roboto', 'system-ui', 'sans-serif'],
        'laio-mono': ['JetBrains Mono', 'monospace'],
      },
      borderRadius: { laio: '2px', 'laio-tag': '3px' },
    },
  },
  plugins: [],
}
```

**`src/lib/laio-colors.js`:**
```js
export const LAIO_COLORS = {
  magenta: { dark: '#101948', easy: '#E385FE', electric: '#F629CB' },
  green:   { dark: '#172708', easy: '#C8ED5D', electric: '#96F90B' },
  blue:    { dark: '#01233C', easy: '#63DCDE', electric: '#00B9FE' },
  orange:  { dark: '#302511', easy: '#F1DC43', electric: '#F5C124' },
  gray:    { dark: '#231F20', mid:  '#929497', light:    '#E3E6E7' },
};
```

---

## 2. Logo

React: use the bundled `assets/LaioLogo.jsx` (inline SVG, `fill` + `width` props).
```jsx
import LaioLogo from './LaioLogo';
<LaioLogo fill="#E385FE" width={200} />   // Easy magenta on dark
<LaioLogo fill="#FFFFFF" width={160} />   // white on dark
```

On a real site or app:
```html
<img src="https://assets.la.io/logos/LAIO-COMPLETE.svg" alt="LA.IO — Louisiana Innovation" width="200">
```

Inside an artifact, preview, or anything sandboxed:
```html
<div style="color: #E385FE;">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 274.65 67.88" width="200" fill="currentColor" role="img" aria-label="LA.IO Louisiana Innovation">
    <g>
      <g>
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
        <path d="M131.74,32.01h8.52v8.52h-8.52v-8.52Z"/>
        <g>
          <path d="M65.87,12.58v21.29h13.75v6.65h-21.29V12.58h7.54Z"/>
          <path d="M106.06,35.11h-8.29l-1.51,5.41h-7.32l8.56-27.94h9.22l8.56,27.94h-7.72l-1.51-5.41ZM99.36,29.48h5.14l-2.48-8.87h-.18l-2.48,8.87Z"/>
          <path d="M159.15,40.53v-6.52h6.96v-14.9h-6.96v-6.52h21.47v6.52h-6.96v14.9h6.96v6.52h-21.47Z"/>
          <path d="M203.77,41.06c-7.19,0-12.55-5.9-12.55-14.5s5.37-14.5,12.55-14.5,12.55,5.9,12.55,14.5-5.37,14.5-12.55,14.5ZM203.77,18.7c-3.02,0-4.92,3.11-4.92,7.85s1.91,7.85,4.92,7.85,4.92-3.11,4.92-7.85-1.91-7.85-4.92-7.85Z"/>
        </g>
        <polygon points="14.73 33.94 41.3 60.51 33.94 67.88 0 33.94 33.94 0 41.3 7.36 14.73 33.94"/>
        <polygon points="259.93 33.94 233.35 7.36 240.72 0 274.65 33.94 240.72 67.88 233.35 60.51 259.93 33.94"/>
      </g>
    </g>
  </svg>
</div>
```
Set color on the parent. External URLs do not load in sandboxed previews.

---

## 3. Eyebrow (mono label)

Always all caps, accent color, JetBrains Mono. Never white/gray as standalone text. Never body copy.

```jsx
function Eyebrow({ children, color = '#E385FE' }) {
  return (
    <span style={{
      fontFamily: 'var(--font-mono)', fontWeight: 700,
      textTransform: 'uppercase', letterSpacing: '0.1em',
      fontSize: '0.75rem', color,
    }}>{children}</span>
  );
}
```
```html
<span style="font-family:'JetBrains Mono',monospace;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.75rem;color:#E385FE">Louisiana Innovation</span>
```

---

## 4. `+` List (the brand bullet)

Never `•`, `-`, or `*`.

```jsx
function LaioList({ items, accent = '#E385FE' }) {
  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {items.map((item, i) => (
        <li key={i} style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
          <span style={{ fontWeight: 700, color: accent, flexShrink: 0 }}>+</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}
// The three pillars:
<LaioList items={['Capital', 'Coaching', 'Connections']} />
```
```css
ul.laio-list { list-style: none; padding: 0; }
ul.laio-list li { display: flex; gap: 8px; margin-bottom: 8px; }
ul.laio-list li::before { content: '+'; font-weight: 700; color: #E385FE; }
```

---

## 5. Button

Flat, angular (2px radius max), no gradients, no shadows. Aktiv Grotesk Bold, slight tracking.

```jsx
function Button({ variant = 'primary', color = '#E385FE', children, onClick }) {
  const base = {
    padding: '10px 24px', borderRadius: '2px', cursor: 'pointer',
    fontFamily: 'var(--font-laio)', fontWeight: 700, letterSpacing: '0.04em',
  };
  const styles = {
    primary: { ...base, background: color, color: '#101948', border: 'none' },
    outline: { ...base, background: 'transparent', color, border: `1.5px solid ${color}` },
    ghost:   { ...base, background: 'transparent', color, border: 'none' },
  };
  return <button style={styles[variant]} onClick={onClick}>{children}</button>;
}
```

---

## 6. Hero

Full-bleed, dark, min 70vh. Eyebrow (mono, accent) → headline (Aktiv Bold/Light, clamp 48–96px, white) → optional subhead (Regular, white) → CTA. Optional cropped bracket supergraphic.

```jsx
function Hero({ eyebrow, headline, subhead, cta, bg = '#101948', accent = '#E385FE' }) {
  return (
    <section style={{
      minHeight: '70vh', background: bg, color: '#fff',
      padding: 'clamp(48px, 8vw, 120px) clamp(24px, 6vw, 80px)',
      display: 'flex', flexDirection: 'column', justifyContent: 'center',
    }}>
      {eyebrow && <span style={{
        fontFamily: 'var(--font-mono)', fontWeight: 700, textTransform: 'uppercase',
        letterSpacing: '0.1em', fontSize: '0.8rem', color: accent, marginBottom: 16,
      }}>{eyebrow}</span>}
      <h1 style={{ fontWeight: 700, fontSize: 'clamp(48px, 8vw, 96px)', lineHeight: 1.02, maxWidth: '16ch' }}>
        {headline}
      </h1>
      {subhead && <p style={{ marginTop: 24, fontSize: 'clamp(18px, 2vw, 20px)', maxWidth: '48ch' }}>{subhead}</p>}
      {cta && <div style={{ marginTop: 40 }}>{cta}</div>}
    </section>
  );
}
```

---

## 7. Stat card

Accent left-border (3px), no radius, no shadow. Mono label, bold value.

```jsx
function StatCard({ label, value, unit, accent = '#E385FE' }) {
  return (
    <div style={{ borderLeft: `3px solid ${accent}`, padding: '12px 20px' }}>
      <div style={{
        fontFamily: 'var(--font-mono)', textTransform: 'uppercase',
        letterSpacing: '0.1em', fontSize: '0.7rem', color: accent,
      }}>{label}</div>
      <div style={{ fontWeight: 700, fontSize: 'clamp(32px, 5vw, 56px)', lineHeight: 1 }}>
        {value}<span style={{ fontWeight: 300, fontSize: '0.5em' }}>{unit}</span>
      </div>
    </div>
  );
}
```

---

## 8. Nav

Horizontal, spare, no gradients. Dark: dark-family bg, white logo, links go accent on hover.

```jsx
function Nav({ links = [], cta, bg = '#101948', accent = '#E385FE' }) {
  return (
    <nav style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '20px clamp(24px, 6vw, 80px)', background: bg, color: '#fff',
    }}>
      <LaioLogo fill="#FFFFFF" width={140} />
      <div style={{ display: 'flex', gap: 28, alignItems: 'center' }}>
        {links.map((l) => <a key={l.href} href={l.href} style={{ color: '#fff', textDecoration: 'none' }}>{l.label}</a>)}
        {cta}
      </div>
    </nav>
  );
}
```

---

## 9. Footer

Minimal: logo, optional descriptor, optional links. No multi-column dump unless the project needs it.

```jsx
function Footer({ bg = '#101948', descriptor = true }) {
  return (
    <footer style={{ background: bg, color: '#fff', padding: '48px clamp(24px, 6vw, 80px)' }}>
      <LaioLogo fill="#FFFFFF" width={160} />
      {descriptor && <p style={{
        fontFamily: 'var(--font-mono)', textTransform: 'uppercase', letterSpacing: '0.1em',
        fontSize: '0.7rem', color: '#929497', marginTop: 16,
      }}>A Division of Louisiana Economic Development</p>}
    </footer>
  );
}
```
