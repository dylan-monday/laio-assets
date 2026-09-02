# laio-assets — repo instructions

Static asset host for LA.IO, served at `https://assets.la.io`.
No build step, no framework. Vercel serves this repo as flat files.

This project is part of the LA.IO brand system. All code must reflect the LA.IO
brand standards. Asset CDN: `https://assets.la.io`. Exceptional output is the
standard — flag anything that falls short before delivering.

For brand voice, color, and type rules, read `claude/CLAUDE.md`. That file is the
client-facing brand kit and it governs anything you write or design here.
This file covers how the repo and the deployment actually work.

---

## What is where

```
/                      index.html      directory of tools and kits
/ai                    ai/             the core brand system as fetchable URLs
/llms.txt                              machine-readable index of the above
/robots.txt                            points crawlers at llms.txt
/labs                  labs/           Louisiana Innovation Labs identity kit
/claude                claude/         brand kit for setting up LA.IO in Claude
/illustrator           (not in repo)   rewritten to the laio-illustrator project
/fonts /logos          static          Aktiv Grotesk woff2, brand SVGs
/motifs /colors        static          brand motifs, tokens, ASE
404.html                               custom 404
_build/                                scripts that generate the pages and kits
_docs/                                 Lovable and Cowork setup docs
```

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

Every override must be appended **after** it. That is why `/claude/(.*)` and
`/illustrator` appear later in the file. Put a new rule before the catch-all and
it silently does nothing.

Two consequences that have bitten this repo already:

+ **Exact paths need their own rule.** `/claude/(.*)` does not match bare
  `/claude`. Commit `3d66fa6` added an exact-match rule for `/illustrator` for
  this reason. The same gap still exists for `/claude`.
+ **HTML must not inherit the immutable cache.** Any page a human reads needs
  `max-age=0, must-revalidate`, or edits never reach returning visitors.
  Rules exist for `/`, `/ai`, `/ai/`, `/ai/index.html`, `/labs`, `/labs/`,
  `/index.html`, `/404.html`, `/labs/index.html`, `/llms.txt`, `/robots.txt`,
  and bare `/claude`.

Do not add `cleanUrls` or `trailingSlash`. Both conflict with the existing
`/illustrator` → `/illustrator/` redirect.

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

Detail, rhythm, complexity and scale each drift on their own oscillator with a
random period between two and six minutes. Rows fade by fractional opacity so
nothing pops. Runs at 30fps, pauses on tab blur, honors `prefers-reduced-motion`
with a single still frame.

If the model changes upstream, re-port it. Do not let the two drift silently.

---

## Regenerating the pages

`index.html`, `404.html`, `labs/index.html`, `ai/index.html`, `llms.txt`, and
`robots.txt` are **generated**. Edit the scripts, not the files, or your change
is lost the next time anyone runs them.

Adding a new asset means editing the `FONTS`, `LOGOS`, `MOTIFS`, `DATA`, or
`DOCS` lists near the bottom of `gen_pages.py`. Both `/ai` and `llms.txt` read
from the same lists, so they cannot drift apart.

```
python3 _build/gen_pages.py
```

See `_build/README.md` for rebuilding the Labs logo kit from master art.

---

## House rules for this repo

+ `border-radius: 0` on structural elements. 2px maximum anywhere.
+ `+` as the only bullet, in copy and in markdown.
+ One color family per page. The directory, 404, and Labs pages are all Blue:
  `#01233C` dark, `#63DCDE` easy, `#00B9FE` electric.
+ Aktiv Grotesk from `/fonts/` (self-hosted woff2, not the Typekit URL — this
  domain serves the files). JetBrains Mono from Google Fonts, all caps, accent
  color, labels and paths only.
+ Hosted logo SVGs are single-fill `#231f20`. To recolor one in a page, inline it
  and swap the fill for `currentColor`. See `_build/laio-complete.inline.svg`.
+ No em dashes.
+ No contact addresses on public pages. `team@louisiana.io` is internal.
