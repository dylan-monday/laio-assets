# LA.IO on Claude Design

Claude Design has a **Design System** feature. You create an **LA.IO Design System** once, then pick it from the *Design System* dropdown on any new project, and everything comes out on brand.

Design systems are account-bound, so each person who designs LA.IO work creates their own. It takes a couple of minutes. Claude Design reads the brand straight from the LA.IO repo on GitHub: the skill, the fonts, the logos, the motifs, the color tokens, and the six layout references.

Verified 2026-09-11: this setup renders Aktiv Grotesk and produces a correct Split.

## Steps

1. In Claude Design, create a new Design System.
2. Fill three fields in the form, exactly as below. Leave the other three empty: *Link code from your computer*, *Upload a .fig file*, and *Add fonts, logos and assets*.
3. Create it.
4. On any new project, pick **LA.IO Design System** from the *Design System* dropdown.

## The three fields

### Company name and blurb

```
LA.IO Design System: LA.IO (Louisiana Innovation Office), the operating brand for Louisiana's innovation ecosystem. Slides, one-pagers, web pages, and social graphics.
```

### Link code from GitHub

```
https://github.com/dylan-monday/laio-assets
```

### Any other notes

```
Read ai/laio-brand/SKILL.md first, then BRAND.md and RANGE.md in the same folder. Fonts are in fonts/laio-fonts-inline.css; use that file for Aktiv Grotesk and never load the typeface from a URL. The six layout moves are in RANGE.md with one worked example each in ai/laio-brand/references/. Logos in logos/, motifs in motifs/, color tokens in colors/. Angles are 0, 45, and 90 only. One color family per piece. Plus as the bullet. No em dashes. Name the system exactly LA.IO Design System.
```

## If something comes out off-brand

Tell Claude Design specifically: "stay in one color family", "headline should be Aktiv Grotesk Bold", "use + as the bullet", "remove the rounded corners", "accent color on the border only, not as a fill". The fuller reference is in `BRAND.md`.

Ask for one slide and you may get a deck. Say how many.

Questions: dylan@mondayandpartners.com
