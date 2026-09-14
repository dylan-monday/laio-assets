# _build

Scripts that generate the site pages and the Louisiana Innovation Labs logo kit.

Nothing here is served: `.vercelignore` at the repo root excludes `_build/`
from deploys. These scripts run on your machine, commit their output, and the
output is what deploys.

## Requirements

```
pip3 install cairosvg
pip3 install fonttools brotli
brew install ghostscript
```

Ghostscript is only needed for the EPS step in `build_kit.py`.
fonttools and brotli are only needed for `build_fonts.py`.

---

## Rebuilding the web font CSS

```
python3 _build/build_fonts.py
```

Aktiv Grotesk has to load without the Adobe Fonts kit, which is locked to la.io.
This builds two stylesheets from the woff2s in `fonts/`:

+ `fonts/laio-fonts.css`: all nine cuts as `@font-face` pointing at
  `https://assets.la.io/fonts/`. One `<link>` on any real site.
+ `fonts/laio-fonts-inline.css`: Aktiv Grotesk Light, Regular and Bold, plus
  JetBrains Mono Regular and Bold, subset to Latin and embedded as base64. For
  sandboxes that block every external host (claude.ai artifacts, Claude Design,
  Lovable previews, email builders). Paste it into a `<style>` tag. JetBrains
  Mono still loads from Google Fonts wherever that works; the embedded copy is
  for hosts that block everything.

JetBrains Mono (SIL OFL 1.1) is fetched from a pinned google/fonts commit on
every run, so the script needs network access. It exits if the download does
not match the pinned SHA-256. The variable font is instanced at 400 and 700
before subsetting.
+ `ai/laio-brand/assets/fonts/laio-fonts-inline.css`: the same inline file,
  shipped inside the skill. AI sandboxes often cannot reach assets.la.io at
  all, so the kit carries its own copy. Rezip `ai/laio-brand.zip` after a
  rebuild (command in the repo `CLAUDE.md`).

It also writes the Latin subsets to `fonts/subset/` and a check page to
`_build/font-test.html`. Serve the repo root over http to open it; the hosted
column does not load from `file://`.

The script prints each output's size and exits non-zero if the inline file
passes 200,000 bytes. Safe to rerun.

---

## Regenerating the pages

```
python3 _build/gen_pages.py
```

Writes `index.html`, `404.html`, `labs/index.html`, `ai/index.html`,
`ai/AGENTS.md`, `llms.txt`, and `robots.txt`.

**Edit the script and its sources, never the output.** Hand edits to those
files are overwritten the next time this runs. The /ai page inlines the CSS and
JS in `ai-page/` and reads its paste blocks from the setup `.md` files in `ai/`.
Run it twice; the second run must produce no diff.

Reads `logos/labs/manifest.json` for lockup dimensions, so run `build_kit.py`
first if the master art changed.

Files here:

+ `shared.css`: the Blue base stylesheet inlined into the home, 404, and Labs
  pages, including the Monday + Partners footer signature
+ `ai-page/`: the Magenta brand page's stylesheet and scripts. `page.css`,
  `rings.js` and `ui.js` are the original Claude kit page's, extracted as they
  were; `additions.css` and `inventory.js` hold what the merged page added
+ `laio-complete.inline.svg`: the LA.IO lockup with `fill: currentColor`, so it
  inherits page color. The CDN copy at `/logos/LAIO-COMPLETE.svg` is hardcoded
  `#231f20` and renders near-black on the navy.

---

## Rebuilding the Labs logo kit

```
python3 _build/build_kit.py ../_source/labs-logos
```

The `LILabs-*.svg` master art lives outside the repo, in `_source/labs-logos/`
of the LA-IO-Brand workspace. That is `../_source/labs-logos` from the repo
root, where the command above runs, and `../../_source/labs-logos` from
`_build/`. Writes to `logos/labs/`:
`svg/`, `eps/`, `png/`, `manifest.json`, and `LILabs-Logos.zip`.

Then rerun `gen_pages.py` so the page picks up any dimension changes.

### What it does to the art

+ **Recolors.** The master art is drawn in `#42b4e7` and `#03243c`, neither of
  which is in the LA.IO blue family. Mapped to `#00B9FE` and `#01233C`.
  Black variants keep `#231F20` (brand Gray Dark) and are not flattened to pure
  black.
+ **Renames one set.** `LILabs-Reverse-White_1` is actually the *black* file, not
  a second white. The whole set is emitted as
  `LILabs-Primary-Reverse-{Color,White,Black}`.
+ **Regenerates EPS.** The original Illustrator EPS files have the old blue baked
  into compressed private data, so text substitution cannot recolor them. Output
  EPS are rebuilt from the recolored SVG through Ghostscript as CMYK with a
  cropped bounding box.
+ **Renders PNG** at 1x, 2x, 3x, and 3000px wide, transparent. 1x is the source
  viewBox width.

### Lockup map

"Reverse" in this artwork means **filled panels**, not reversed-out for dark
backgrounds. All seven ship, each in color, white, and black.

| Output | Source stem | |
|---|---|---|
| Primary | `LILabs-Primary` | Full lockup, outlined panels |
| Primary-Reverse | `LILabs-Reverse` | Full lockup, filled panels |
| Stacked | `LILabs-Stacked` | Condensed, outlined panels |
| Stacked-Reverse | `LILabs-Stacked-Reverse` | Condensed, filled panels |
| LABS | `LILabs-LABS` | Panels alone |
| Icon | `LILabs-Icon` | Single panel, outlined |
| Icon-Reverse | `LILabs-Icon-Reverse` | Single panel, filled |

`kit-README.txt` is the plain-text readme dropped into the zip for LED. Edit it
here and rerun `build_kit.py`.

### Clear space

`PANEL = 65.3` in `gen_pages.py` is the LABS panel box width in source units,
shared across every lockup. The clear-space diagram is built from it. If the
master art is ever redrawn at a different scale, that constant moves.
