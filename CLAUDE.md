# laio-assets — repo instructions

Static asset host for LA.IO, served at `https://assets.la.io`.
No build step, no framework. Vercel serves this repo as flat files.

This project is part of the LA.IO brand system. All code must reflect the LA.IO
brand standards. Asset CDN: `https://assets.la.io`. Exceptional output is the
standard — flag anything that falls short before delivering.

For brand voice, color, and type rules, read `ai/CLAUDE.md`. That file is the
client-facing brand kit and it governs anything you write or design here.
This file covers how the repo and the deployment actually work.

`README.md` is the short version for people. `ai/README.md` explains the brand
kit folder file by file. The **History** section at the end records how the
repo reached its current shape.

---

## What is where

```
/                      index.html      directory of tools and kits (generated)
/ai                    ai/             Brand Kit for AI: the one brand page (generated),
                                       CLAUDE.md, AGENTS.md (generated), setup docs,
                                       the laio-brand skill and its zip
/ai/lovable            ai/lovable/     Lovable workspace instructions, starter prompt,
                                       template spec, and guide
/llms.txt                              machine-readable index of the above (generated)
/robots.txt                            points crawlers at llms.txt (generated)
/labs                  labs/           Louisiana Innovation Labs identity kit (generated)
/claude                (redirect)      301s to /ai, see "Redirects" below
/illustrator           (not in repo)   rewritten to the laio-illustrator project
/fonts /logos          static          Aktiv Grotesk woff2 + CSS, brand SVGs
/motifs /colors        static          brand motifs, tokens, ASE
404.html                               custom 404 (generated)
.vercelignore                          keeps _build/ out of every deploy
_build/                                scripts that generate the pages, fonts, and kits
_build/ai-page/                        the /ai page's CSS and JS, inlined at build time
```

## The brand connector

`/mcp` is the LA.IO brand MCP connector. The LA.IO team adds it once through their
Claude org and any chat can then pull the real logo, colors, fonts and voice rules.

```
/mcp                   api/mcp.js      MCP server, Streamable HTTP, no auth
/render/*              api/render.js   SVG recolor to PNG, PDF and .ase, deterministic URLs
lib/                                   shared code: kit reader, color resolver, SVG, ASE
colors/laio-cmyk.json                  CMYK builds, the one source for print values
ai/laio-brand/VOICE.md                 speaker profiles, full ban list, standing rules
fonts/desktop/                         licensed desktop TTFs as a zip
```

**Every rule the connector serves is read from the kit at request time.** `lib/kit.js`
reads `ai/CLAUDE.md`, `ai/laio-brand/VOICE.md`, `colors/laio-tokens.json` and
`colors/laio-cmyk.json` off disk. Nothing is hand-copied into server code. Change a
kit file and the connector changes with it. Keep it that way.

`vercel.json` carries the `/mcp` and `/render` rewrites, the header rules for both
(appended last, because later rules win), and `functions.includeFiles`, which is what
puts the kit files inside the serverless bundle. Removing `includeFiles` breaks the
connector with a "kit not found" error.

Render URLs are deterministic and cached for a year. Same URL, same bytes, forever.

To run both locally: `node _build/devserver.mjs`, then hit
`http://localhost:5199/render/logo/complete.png?color=easy%20green` or POST JSON-RPC
to `http://localhost:5199/mcp`.

The page at `/ai` is unchanged. The connector is an addition to it, not a replacement.

---

`/illustrator` is **not a folder**. It is a rewrite in `vercel.json` pointing at
`laio-illustrator.vercel.app`, a separate Vercel project and separate repo.
Never add an `illustrator/` directory here.

---

## Deploying

Production branch is `main`. Push to `main` deploys to `assets.la.io`.
Work on a branch and open a PR. Vercel builds a preview per branch.

**Preview URLs cannot test `/illustrator`.** The illustrator app builds its login
redirect from the `Host` header and only prepends `/illustrator` when the host is
`assets.la.io`. On a `*.vercel.app` preview host it redirects to bare `/login`,
which falls outside the rewrite and lands on our 404. This is expected. Verify
`/illustrator` on production after merge, not on the preview.

Preview deployments also sit behind Vercel SSO on this team, so anything
unauthenticated (curl, an agent) gets a 302 to a login page on every route.

---

## vercel.json — read before editing

Header rules are matched **in order, and later matches win**. The first rule is a
catch-all:

```json
{ "source": "/(.*)", "headers": [ ... "max-age=31536000, immutable" ] }
```

Every override must be appended **after** it. That is why `/ai/(.*)` and
`/illustrator` appear later in the file. Put a new rule before the catch-all and
it silently does nothing.

Two consequences that have bitten this repo already:

+ **Exact paths need their own rule.** `/ai/(.*)` does not match bare `/ai`,
  so `/ai`, `/ai/` and `/ai/index.html` each have one. Commit `3d66fa6` added
  an exact-match rule for `/illustrator` for the same reason.
+ **HTML must not inherit the immutable cache.** Any page a human reads needs
  `max-age=0, must-revalidate`, or edits never reach returning visitors.
  Rules exist for `/`, `/ai`, `/ai/`, `/ai/index.html`, `/labs`, `/labs/`,
  `/index.html`, `/404.html`, `/labs/index.html`, `/llms.txt`, `/robots.txt`,
  and everything under `/ai/`.

Do not add `cleanUrls` or `trailingSlash`. Both conflict with the existing
`/illustrator` → `/illustrator/` redirect.

### Redirects

`/claude`, `/claude/`, and `/claude/:path*` redirect permanently to the same
path under `/ai`. The Claude kit lived at `/claude` until it merged into the
brand page, and links to it are out in the wild, including direct file URLs
such as `/claude/laio-brand.zip`. Vercel runs redirects before it checks the
filesystem, so they work with no `claude/` folder in the repo. Do not add one
back: nothing in it would ever be served.

### Caching

The catch-all `/(.*)` revalidates. `immutable, max-age=31536000` is scoped to
`/fonts`, `/logos`, `/motifs`, and `/colors`, whose filenames are stable.

This matters more than it looks. Before the fix, 404 responses inherited the
immutable catch-all, so anyone who requested a path *before* it existed had that
404 cached in their browser for a year. It happened in practice with `/llms.txt`.
Any new page added to this repo would have hit the same trap. Do not put the
immutable rule back on the catch-all.

---

## CORS

`Access-Control-Allow-Origin: *` is set on everything by the catch-all and has
been since commit `47276cc`. Assets hotlink from any origin. If someone reports
a CORS problem, verify the header before changing config — the answer is usually
that the header is already there.

---

## The homepage backdrop

`index.html` runs a full-bleed canvas of the **Weave / Rope** illustration model,
ported from `RENDERERS["weave.rope"]` in the Illustration Machine's `engine.js`
(repo `dylan-monday/laio-illustrator`). The formulas and constants are copied
verbatim: count, phase, rows, rotation, ellipse dimensions, the 0.45 edge
threshold and the `0.18 + 0.42 * (1 - edge)` ghost alpha.

Two deliberate departures, both forced by the difference between a finite
composition and a backdrop:

+ **The band extends past the viewport.** The model lays `count` ellipses across
  a fixed 880-unit band. Rendered full screen that band's end caps land inside
  the frame as a bright pile-up. We keep the model's pitch and extend the index
  range until it clears both edges.
+ **`edge` is measured off the viewport, not the band.** So the rope thins toward
  the sides instead of stopping.

Detail, rhythm, complexity and scale each ride two sines at unrelated rates, so
they wander rather than loop. Periods land between roughly 20 and 80 seconds:
fast enough that the pattern visibly rebuilds itself during a visit, slow enough
that nothing reads as animating. Rows fade by fractional opacity so nothing pops.

Stroke alpha is scaled inversely to `detail` (`1.46 - detail * 0.62`). A sparse
field of 40 ellipses and a dense one of 145 then read at the same weight, so what
changes is the pattern and not the brightness. Without this the page appears to
dim and brighten, which is the one thing a backdrop must not do.

Runs at 30fps, pauses on tab blur, honors `prefers-reduced-motion` with a single
still frame at a random point in the cycle.

If the model changes upstream, re-port it. Do not let the two drift silently.

---

## Regenerating the pages

`index.html`, `404.html`, `labs/index.html`, `ai/index.html`, `ai/AGENTS.md`,
`llms.txt`, and `robots.txt` are **generated**. Edit the scripts and their
sources, not the files, or your change is lost the next time anyone runs them.

Adding a new asset means editing the `FONTS`, `LOGOS`, `MOTIFS`,
`DATA`, or `DOCS` lists near the bottom of `gen_pages.py`. Both `/ai` and `llms.txt` read
from the same lists, so they cannot drift apart.

```
python3 _build/gen_pages.py
```

The /ai page is built from three kinds of source:

+ `_build/ai-page/page.css`, `rings.js` and `ui.js`: the stylesheet and scripts
  of the original hand-built Claude kit page, extracted as they were.
  `additions.css` and `inventory.js` hold what the merged page added. All five
  are inlined into `ai/index.html`.
+ The paste blocks: the first fenced code block in
  `ai/claude-ai-project-setup.md` and `ai/lovable/LAIO_LOVABLE_GUIDE.md`, and
  every `### Field name` heading with its fenced block in
  `ai/claude-design-setup.md`, one copy block per Claude Design form field.
  The build exits if those field names change. Edit the `.md`, then rebuild.
+ Everything else on the page, in the `/ai` section of `gen_pages.py`.

`ai/AGENTS.md` is a byte-identical copy of `ai/CLAUDE.md`, written by every
build so tools that look for `AGENTS.md` find the same instructions. Edit
`ai/CLAUDE.md` only.

See `_build/README.md` for rebuilding the Labs logo kit from master art, and for
`_build/build_fonts.py`, which writes both font CSS files plus the copy of
`laio-fonts-inline.css` that ships inside the skill.

`ai/laio-brand.zip` is a plain zip of `ai/laio-brand/`. Nothing builds it.
Rezip it after any change inside the skill folder, or the download goes stale:

```
cd ai && rm laio-brand.zip && zip -r -X laio-brand.zip laio-brand -x '*.DS_Store'
```

---

## The brand page at /ai

One page carries setup for every tool, the brand summary, and the full asset
inventory. It keeps the look of the hand-built Claude kit page it replaced.

+ **Magenta family.** The brand assigns Magenta to tech, AI, and digital, which
  fits an AI setup page. Dark ground `#101948`, easy `#E385FE`, electric
  `#F629CB`. The other pages in this repo are Blue; do not mix the two.
+ **Setup is Finder-based, not Terminal.** Clients are not all comfortable in
  Terminal. Each tab offers downloads and explicit Finder steps to reach the
  hidden `~/.claude/skills` folder (Go to Folder). A Terminal one-liner sits in a
  collapsed `<details>` for developers.
+ **Intro: orbital rings and the logo forming.** The logo's own chevrons ease
  into place over a spinning field of orbital rings, the logo dissolves, and the
  rings stay on as the live header backdrop. An earlier version framed the white
  logo with extra magenta brackets. It was rejected as off-brand, because the
  logo already contains its `< >`. The rings are a zero-dependency canvas model,
  in Magenta, set to a slow spin with each ring also turning at its own random
  speed and direction, and tilted toward the cursor.
+ **Reduced motion is fully respected.** With `prefers-reduced-motion: reduce`
  there is no intro, no spin, and no parallax: one static rings frame behind a
  fully visible page. All motion CSS sits behind
  `@media (prefers-reduced-motion: no-preference)`.
+ **Fonts load from this host.** Aktiv Grotesk comes from `/fonts/` by
  `@font-face`, never the Adobe kit, which is locked to la.io. JetBrains Mono and
  Karla come from Google Fonts.
+ **The M+P signature is type-set.** "MONDAY + PARTNERS" in Karla 700 with a
  Karla 800 `+` in the page's easy color, 0.22em tracking. Preferred over the SVG
  logo because the wordmark is just Karla plus a colored plus. The brand page
  uses easy magenta and carries the contact email. The homepage, Labs, and 404
  use easy blue and carry no email.
+ **Color swatches carry no use-case labels.** Family usage is guidance, not a
  hard rule, so captions like "Tech, AI, digital" were removed.
+ **Paste blocks are never typed twice.** Each lives in its `.md` file and is
  read into the page at build time. Before the merge, the page and the `.md`
  files had drifted apart.

---

## Update workflow

The repo is the only source. Nothing is synced in from the outer workspace.

1. Branch from `main`.
2. Edit the sources: `ai/*.md`, `ai/laio-brand/`, `ai/lovable/`,
   `_build/ai-page/`, or `_build/gen_pages.py`.
3. If the fonts changed, run `python3 _build/build_fonts.py`.
4. Run `python3 _build/gen_pages.py`. A second run must produce no diff.
5. If anything inside `ai/laio-brand/` changed, including through step 3,
   rezip the skill with the command above.
6. Commit, open a PR, merge. Vercel deploys `main` to assets.la.io. Verify on
   production, since previews sit behind Vercel SSO:
   `curl -sI https://assets.la.io/ai/`.

---

## House rules for this repo

+ `border-radius: 0` on structural elements. 2px maximum anywhere.
+ `+` as the only bullet, in copy and in markdown.
+ One color family per page. The directory, 404, and Labs pages are Blue:
  `#01233C` dark, `#63DCDE` easy, `#00B9FE` electric. The brand page at `/ai`
  is Magenta: `#101948` dark, `#E385FE` easy, `#F629CB` electric.
+ Type rules are the block in `ai/CLAUDE.md`, word for word in every doc and
  page. Change them there and everywhere else in the same commit. The paste
  blocks on `/ai` are read from the setup `.md` files at build time, so they
  follow once you rebuild. Family name is
  `'Aktiv Grotesk'`, loaded from `fonts/laio-fonts-inline.css` (embedded, for
  sandboxes) or `fonts/laio-fonts.css` (hosted, for real sites). Pages in this
  repo link the woff2s in `/fonts/` directly, since this domain serves them.
  JetBrains Mono from Google Fonts, all caps, accent color, labels and paths only.
+ Hosted logo SVGs are single-fill `#231f20`. To recolor one in a page, inline it
  and swap the fill for `currentColor`. See `_build/laio-complete.inline.svg`.
+ No em dashes.
+ No contact addresses on public pages, and no internal addresses in any file.
  This repo is served publicly, docs included. Only `_build/` is excluded, by
  `.vercelignore`.

---

## History

How the repo reached its current shape, oldest first.

+ **2026-09-11, PR #4: font delivery.** Aktiv Grotesk had loaded from an
  Adobe Fonts kit that only works on la.io, so AI tools failed and swapped in
  another font. `_build/build_fonts.py` now writes `fonts/laio-fonts.css`
  (hosted, all nine cuts) and `fonts/laio-fonts-inline.css` (base64, no
  network requests).
+ **PR #5: one set of type rules.** Every doc and page carries the same type
  block: embedded first, hosted on real sites, Roboto only as a stated
  fallback. The skill ships its own copy of the inline file, because cloud AI
  sessions often cannot reach assets.la.io. The inline file also embeds
  JetBrains Mono 400 and 700 for hosts that block Google Fonts.
+ **PR #6: one brand page.** The hand-built `/claude` setup page and the
  generated `/ai` inventory merged into one generated page at `/ai`, with tabs
  for Claude, Claude Design, Claude Code + Cowork, Lovable, and other AI.
  `claude/` became `ai/`, the Lovable docs moved into `ai/lovable/`, `_docs/`
  was retired, and `/claude` redirects to `/ai`. Paste blocks are read from
  the setup `.md` files, so the page cannot drift from them again.
+ **PR #7: cleanup.** Em dashes came out of `ai/CLAUDE.md`, the Lovable step
  names Workspace Knowledge, internal names came out of this public file, and
  `.vercelignore` keeps `_build/` off the site.
+ **Outside the repo.** The working copies that used to sit around it (the old
  Claude kit folder, `_docs/`, loose asset folders) were archived, and the Labs
  master art moved to `_source/labs-logos/` next to the repo. This repo is the
  only source.
