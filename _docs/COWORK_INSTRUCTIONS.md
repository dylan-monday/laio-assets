# LA.IO Lovable Brand System — Cowork Instructions

## What this project is

This directory is the brand asset and documentation system for LA.IO (Louisiana Innovation Office), managed by Dylan Thuras at Monday and Partners. It feeds a Lovable account used to build digital products for the LA.IO ecosystem — microsites, partner tools, dashboards, event pages, and more.

The three markdown documents in this directory are living brand system documents. They are the single source of truth for how every Lovable project should look, sound, and behave. Everything in the asset folders (logos, fonts, motifs, colors) is referenced by those documents.

Your job is to help keep this directory organized, complete, and consistent — and to make sure the documents accurately reflect whatever assets exist on disk.

---

## Directory structure

```
/
├── LAIO_BRAND.md                  ← master brand reference (attach to every Lovable project)
├── LOVABLE_CUSTOM_INSTRUCTIONS.md ← paste into Lovable account-level custom instructions
├── LOVABLE_STARTER_TEMPLATE_SPEC.md ← build spec for the Lovable starter template project
├── COWORK_INSTRUCTIONS.md         ← this file
├── colors/
│   └── LA_IO_COLORS_RGB.ase       ← official Adobe color swatch file
├── fonts/
│   └── (Aktiv Grotesk font files — woff2, ttf, or otf)
├── logos/
│   └── (SVG and PNG logo variants)
├── motifs/
│   └── (individual bracket/mark SVG elements)
└── reference/
    └── (compositional reference images — PNGs showing brand in action)
```

---

## Ongoing tasks — do these whenever files change

### 1. Audit the asset directory and report gaps

Scan all folders and compare what exists against what the spec calls for. Report:

**Logos needed** (per LOVABLE_STARTER_TEMPLATE_SPEC.md):
- `laio-wordmark.svg` — base black wordmark
- `laio-wordmark-white.svg` — white variant
- `laio-mark-left.svg` — left bracket only `<`
- `laio-mark-right.svg` — right bracket only `>`
- `laio-horizontal.svg` — horizontal layout with stacked text
- `laio-favicon.ico`
- PNG exports (multiple sizes: 64, 128, 256, 512px wide)

**Motifs needed**:
- `bracket-pair.svg` — `< >` together
- `chevron-right.svg` — `>`
- `chevron-left.svg` — `<`
- `chevron-down.svg` — `v`
- `chevron-up.svg` — `^`
- `diamond-filled.svg` — `◆`
- `diamond-outline.svg` — `◇`
- `cross.svg` — `+`
- `corner-tl.svg` — top-left corner mark `⌐`
- `corner-tr.svg` — top-right corner mark
- `corner-br.svg` — bottom-right corner mark `¬`

**Fonts needed**:
- `AktivGrotesk-Light.woff2` (weight 300)
- `AktivGrotesk-Regular.woff2` (weight 400)
- `AktivGrotesk-Bold.woff2` (weight 700)
- TTF versions of the same (for InDesign/print use)

Note: Web projects load Aktiv Grotesk via Adobe Fonts kit — `https://use.typekit.net/usf5bjl.css` — not from these files. The woff2 files in this directory are for self-hosted or offline contexts only. Adobe Fonts serves the family as `'aktiv-grotesk'` (lowercase, hyphenated).

**Colors**:
- `LA_IO_COLORS_RGB.ase` — exists, confirmed
- `laio-tokens.json` — needs to be generated (see task 2)

For any file that's missing, note it clearly. Do not create placeholder files — just report what's absent.

### 2. Generate laio-tokens.json from the ASE file

When asked, parse `colors/LA_IO_COLORS_RGB.ase` and write `colors/laio-tokens.json` in this exact structure:

```json
{
  "laio": {
    "magenta": {
      "dark":     { "value": "#101948", "rgb": [16, 25, 72],    "name": "LA.IO DRK PRPL" },
      "easy":     { "value": "#E385FE", "rgb": [227, 133, 254], "name": "LA.IO EASY MAGENTA" },
      "electric": { "value": "#F629CB", "rgb": [246, 41, 203],  "name": "LA.IO ELECTRIC MAGENTA" }
    },
    "green": {
      "dark":     { "value": "#172708", "rgb": [23, 39, 8],     "name": "LA.IO DRK GRN" },
      "easy":     { "value": "#C8ED5D", "rgb": [200, 237, 93],  "name": "LA.IO EASY GRN" },
      "electric": { "value": "#96F90B", "rgb": [150, 249, 11],  "name": "LA.IO ELECTRIC GRN" }
    },
    "blue": {
      "dark":     { "value": "#01233C", "rgb": [1, 35, 60],     "name": "LA.IO DRK BLUE" },
      "easy":     { "value": "#63DCDE", "rgb": [99, 220, 222],  "name": "LA.IO EASY BLUE" },
      "electric": { "value": "#00B9FE", "rgb": [0, 185, 254],   "name": "LA.IO ELECTRIC BLUE" }
    },
    "orange": {
      "dark":     { "value": "#302511", "rgb": [48, 37, 17],    "name": "LA.IO DRK ORNG" },
      "easy":     { "value": "#F1DC43", "rgb": [241, 220, 67],  "name": "LA.IO EASY ORANGE" },
      "electric": { "value": "#F5C124", "rgb": [245, 193, 36],  "name": "LA.IO ELECTRIC ORANGE" }
    },
    "gray": {
      "dark":     { "value": "#231F20", "rgb": [35, 31, 32],    "name": "LA.IO DRK GRAY" },
      "mid":      { "value": "#929497", "rgb": [146, 148, 151], "name": "LA.IO GRAY" },
      "light":    { "value": "#E3E6E7", "rgb": [227, 230, 231], "name": "LA.IO EASY GRAY" },
      "white":    { "value": "#FFFFFF", "rgb": [255, 255, 255], "name": "White" }
    }
  }
}
```

Write this to `colors/laio-tokens.json`.

### 3. Validate SVG files as they're added

When new SVG files appear in `logos/` or `motifs/`, check each one:

- Does it have a `viewBox` attribute? (Required)
- Does it use a single fill color? (Brand spec: all marks should be single-fill, `#231F20` or `currentColor`)
- Does it have any embedded raster images, gradients, or filters? (Flag these — they should not be in base mark files)
- Is the filename lowercase with hyphens, no spaces? (Rename if not)
- Does it match the naming convention in the spec above?

Report findings. Do not modify files without being asked — just flag issues.

### 4. Update LAIO_BRAND.md when the asset directory changes

When Dylan adds new files and asks you to sync the docs, update the asset directory section of `LAIO_BRAND.md` to reflect what's actually present. Mark items as available with a checkmark, missing items with a note.

Also update the `LaioLogo.jsx` component spec in `LOVABLE_STARTER_TEMPLATE_SPEC.md` if new logo variants are confirmed present — specifically, replace the placeholder comment with the actual SVG path data from `logos/laio-wordmark.svg` once that file exists.

### 5. Generate the Lovable project init prompt for any new project

When asked to set up a new Lovable project, generate a ready-to-paste first message using this template, filled in with project-specific details:

```
This is an LA.IO brand project. Please read LAIO_BRAND.md before generating anything.

Setup:
1. Configure tailwind.config.js with the full LAIO color token set
2. Set up globals.css with Aktiv Grotesk font stack (files in /public/assets/fonts/) and Roboto fallback via Google Fonts
3. Create src/lib/laio-colors.js with the full color constants
4. Create skeleton components: LaioLogo.jsx, Button.jsx, Nav.jsx, Hero.jsx, Footer.jsx
5. Use the [FAMILY] color family for this project

Project: [DESCRIPTION]
Audience: [AUDIENCE]
Color family: [FAMILY — Magenta / Green / Blue / Orange / Gray]
Key sections needed: [LIST]

Voice reminders:
+ No em dashes. Rewrite any sentence that needs one.
+ No "it's not X, it's Y" constructions.
+ Use + as the list bullet, never • or -.
+ The three pillars when referenced: + Capital / + Coaching / + Connections
+ Never use: resilience, Silicon Bayou, innovative solutions, disrupting
+ State the case. Don't sell it.
```

---

## Things Cowork should never do in this directory

- Do not modify `LAIO_BRAND.md`, `LOVABLE_CUSTOM_INSTRUCTIONS.md`, or `LOVABLE_STARTER_TEMPLATE_SPEC.md` without being explicitly asked
- Do not rename logo or motif files without confirming with Dylan first — filenames matter because the spec references them by name
- Do not create placeholder or dummy asset files
- Do not add color values that aren't in `LA_IO_COLORS_RGB.ase` — that file is the authority
- Do not reorganize the folder structure without being asked

---

## Current status (as of setup)

### Documents
- [x] `LAIO_BRAND.md` — complete, includes color system, voice rules, motif guidance, asset delivery guidance
- [x] `LOVABLE_CUSTOM_INSTRUCTIONS.md` — complete, ready to paste into Lovable account settings
- [x] `LOVABLE_STARTER_TEMPLATE_SPEC.md` — complete, includes Tailwind config, component specs, init prompt

### Colors
- [x] `colors/LA_IO_COLORS_RGB.ase` — present and parsed
- [ ] `colors/laio-tokens.json` — needs to be generated

### Fonts
- [ ] Aktiv Grotesk woff2 files — confirm present (web delivery handled via Adobe Fonts kit)

### Logos
- [ ] All logo SVG variants — not yet added

### Motifs
- [ ] All bracket/mark SVG elements — not yet added

### Reference
- [ ] Compositional reference images — not yet added

---

## How to work with Dylan on this

Dylan is the creative director. He makes all brand decisions. Your role is execution, organization, and surfacing gaps clearly.

When Dylan drops new files into the directory, he'll ask you to audit, validate, or sync the docs. Do exactly what's asked, report clearly, and flag anything that looks inconsistent with the brand spec — but don't change things unilaterally.

When something in the docs conflicts with what Dylan says in conversation, the conversation wins. Update the docs to reflect the new direction and note what changed.
