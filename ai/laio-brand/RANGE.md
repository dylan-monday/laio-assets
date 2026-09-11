# LA.IO Range

SKILL.md teaches the rules. Follow only those and every layout lands in the same place: a dark page, a mono eyebrow, a plus list. This file adds range. It names six layout moves LA.IO already uses, with a clean reference file for each and the limits that keep them restrained.

Restraint over interpretation. Nothing here loosens a rule in SKILL.md unless section 5 states the exception.

Read SKILL.md first. Read this before any layout beyond a plain page: slides, heroes, social tiles, posters, report covers.

---

## 1. The shape grammar

Every LA.IO shape comes from the logo's bracket, set at 45 or 90 degrees.

+ **Chevron.** The bracket itself. `LAIO-LEFT-BRACKET`, `LAIO-RIGHT-BRACKET`, `LAIO-UP-BRACKET`, `LAIO-DOWN-BRACKET`.
+ **Diamond.** A square of bracket strokes turned to 45. `LAIO-DIAMOND`, `LAIO-DIAMOND-EMPTY`.
+ **Square.** The diamond set back to 0. `LAIO-SQUARE`, `LAIO-SQUARE-EMPTY`.
+ **Corner.** Half a square. The frame piece. `LAIO-BRACKET-CORNER-1`, `LAIO-BRACKET-CORNER-2`, `LAIO-CORNER-L`.
+ **Plus.** Two bracket strokes crossed at 90. `LAIO-PLUS`.
+ **X.** The plus at 45. `LAIO-X`.
+ **Diagonal field.** One bracket edge carried to the canvas edge. `LAIO-FIELD-DIAGONAL`, drawn for a 16:9 canvas at 100% width. Two 45-degree edges meeting at a point make a chevron field: the bracket itself at field scale. No file ships for it. Draw it as a polygon.
+ **45-degree hatch.** Bracket strokes repeated. `LAIO-HATCH`, one tile that repeats seamlessly.
+ **Wire node.** An open square one bracket stroke wide. `LAIO-WIRE-NODE`. Draw it at 8px and its line matches a 1px wire.

Angles are 0, 45, and 90. Nothing else rotates. No curves, no circles, no rounded corners.

Every file ships single-fill `#231F20` in `assets/motifs/` and at `https://assets.la.io/motifs/`. Recolor to the active family.

---

## 2. Six moves

Each move has a reference in `references/`: an HTML file to read and a PNG of the result. One family per reference. Read the structure, then build your own.

### The Split

One 45-degree field slices the canvas into two committed areas: dark against white, or dark against photo.

+ One field per composition.
+ The field carries the accent content: a number, a headline, or the plus points. The other side stays quiet.
+ **Variant, the chevron field.** The field may be a chevron: two 45-degree edges meeting at a point. That is the bracket itself at field scale. It is still one field.
+ **Don't:** a second field, or an edge at any angle other than 45.
+ **Reference:** `references/01-split.html`

### The Diamond

A bracket-derived container for a group of content.

+ Diamonds touch at points and never overlap.
+ Where two large diamonds meet, a small easy-color diamond may hold the logo.
+ **Variant, the half diamond.** A canvas edge may halve a diamond, leaving a triangle container. Overlapping diamonds stay banned.
+ **Don't:** rotate off 45, or set a diamond on a diamond of the same value.
+ **Reference:** `references/02-diamond.html`

### The Frame

Two corner brackets around a headline, top-left and bottom-right, or a chevron pair flanking a title.

+ Frames hold type only.
+ Brackets sit outside the type's bounding box. Clear space is the bracket's stroke width times four.
+ **Don't:** frame the logo, or close all four corners.
+ **Reference:** `references/03-frame.html`

### The Wire

Hairline connections with open-square terminals, for anything that relates: org charts, hub and spoke, callouts.

+ A 1px rule in the easy color. Terminals are small open squares (`LAIO-WIRE-NODE`).
+ Lines run at 0 or 90 degrees only.
+ **Don't:** arrows, curves, or diagonal wires.
+ **Reference:** `references/04-wire.html`

### The Grid

A four-up photo grid where the plus is the gutter.

+ The plus sits at the exact center in the accent color. Its arms are the gutters.
+ Photos are all duotoned in the family, or all untreated.
+ **Don't:** mix treatments, or use a plus that isn't the gutter.
+ **Reference:** `references/05-grid.html`

### The Big Mark

The logo at supergraphic scale, cropped past the edges.

+ Legibility is the only limit.
+ When a lockup is needed, pair it with an L-corner (`LAIO-CORNER-L`) holding the vertical LOUISIANA INNOVATION wordmark.
+ **Don't:** add brackets around it, or scale it up and leave it fully inside the frame.
+ **Reference:** `references/06-big-mark.html`

---

## 3. Type moves

+ **Accent word.** One per headline, set in the accent color or in Bold. Never both. Never two words.
+ **Big numerals.** Bold, with a Regular caption beneath.
+ **Progression glyph.** A row of three chevrons (`>>>`, from `LAIO-RIGHT-BRACKET`) may sit between two values to show one leading to the other. Never an arrow with a shaft.
+ **Bar charts.** Bars in the family accent on the family dark, one series highlighted in electric, gridlines in the easy color at low opacity, axis labels in mono.
+ **Stat cards.** Easy-color fill, dark family type, a mono eyebrow with a short dark rule under it. This is the one place an accent fills an area with dark type on it, and the one place a mono label runs in the dark color. It lives inside a card only.
+ **Vertical wordmark.** LOUISIANA INNOVATION rotated 90 degrees, locked to an L-corner. Use the `LOUISIANA-INNOVATION-A` or `-B` file. Never set it in type.

---

## 4. Photography

Two treatments only.

+ Duotone in the family color.
+ Sliced by a Split.

Never a soft overlay. Never a gradient. The logo may run over a photo at Big Mark scale.

---

## 5. Exceptions, stated

+ **Partner logos.** Recolor into the family by default. Original colors only when the partner requires it. The kit ships no partner logos. Projects add their own.
+ **LED logo.** The one outside logo the kit ships: `LED-WHITE.svg`, `LED-BLACK.svg`, `LED-SMALL-WHITE.svg`, `LED-SMALL-BLACK.svg` in `assets/logos/`. Louisiana Economic Development, the parent agency. White on dark grounds is the default. Black on light grounds, recolored to the family dark. Never the full-color or gold versions. Sits under or beside the LA.IO mark, never above it.
+ **Grain.** Allowed on a flat dark ground. A radial glow or vignette is a gradient and stays banned.
+ **Hex tiles.** Allowed for cartograms only.
+ **Stat cards.** May invert, as described in section 3.

---

## 6. Guardrails

+ Two shapes per composition, maximum. The logo and the type do not count.
+ Accent color covers under a third of the canvas, except inside a stat card.
+ One field per composition, straight or chevron.
+ Angles are 0, 45, and 90.
+ One family per composition.

The test from SKILL.md still applies. Would it work in a Baton Rouge shipyard and a London transit ad? If one move is carrying the layout, stop adding.
