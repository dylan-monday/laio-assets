# LA.IO Components

Copy-paste building blocks for LA.IO projects. Each block has a **React** version (for Claude Code / app projects) and, where useful, a **plain HTML/CSS** version (for Claude Design, artifacts, emails, decks). All follow the brand: angular, one color family, `+` bullets, Aktiv Grotesk + JetBrains Mono.

Pick one color family per project (see `SKILL.md`). Examples below use the **Magenta** family (`#101948` / `#E385FE` / `#F629CB`) — swap the three hexes to re-skin.

---

## 1. Setup — fonts, tokens, Tailwind

**`index.html` `<head>`:**
```html
<link rel="stylesheet" href="https://use.typekit.net/usf5bjl.css">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://assets.la.io/colors/laio-colors.css">
```

**Base CSS:**
```css
:root {
  --font-laio: 'aktiv-grotesk', 'Roboto', system-ui, sans-serif;
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
        laio: ['aktiv-grotesk', 'Roboto', 'system-ui', 'sans-serif'],
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

HTML (color via CSS mask so the single-fill SVG can take any brand color):
```html
<img src="https://assets.la.io/logos/LAIO-COMPLETE.svg" alt="LA.IO — Louisiana Innovation" width="200">
```
To recolor in HTML, inline the SVG and set `fill`, or use a CSS mask:
```css
.laio-logo {
  width: 200px; height: 50px;
  background: #E385FE;
  -webkit-mask: url('https://assets.la.io/logos/LAIO-COMPLETE.svg') center / contain no-repeat;
          mask: url('https://assets.la.io/logos/LAIO-COMPLETE.svg') center / contain no-repeat;
}
```

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
