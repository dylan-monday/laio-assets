#!/usr/bin/env python3
"""Regenerate every generated file in the repo: index.html, 404.html,
labs/index.html, ai/index.html, ai/AGENTS.md, llms.txt and robots.txt.

    python3 _build/gen_pages.py

Reads logos/labs/manifest.json (written by build_kit.py) for lockup
dimensions, so run build_kit.py first if the master art changed.
"""
import json, datetime, os, re, shutil
from html import escape as html_escape

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSS  = open(os.path.join(HERE, "shared.css")).read()
LOGO = open(os.path.join(HERE, "laio-complete.inline.svg")).read().strip()
M    = json.load(open(os.path.join(REPO, "logos", "labs", "manifest.json")))
BASE="/logos/labs"
ABS="https://assets.la.io/logos/labs"
PANEL=65.3  # LABS panel box width in source units

# Monday + Partners signature for the Blue pages (home, 404, Labs). Karla 700,
# the + in Easy Blue, the same tracking as the brand page at /ai. No email here.
MPSIG = ('<div class="mpsig"><span class="made">Maintained by</span>'
         '<span class="mp-logo">MONDAY <span class="mp-plus">+</span> PARTNERS</span></div>')

WEAVE_CSS = '''
#weave{position:fixed;inset:0;z-index:0;pointer-events:none;display:block;
  -webkit-mask-image:radial-gradient(120% 95% at 50% 50%,rgba(0,0,0,.40) 0%,rgba(0,0,0,.72) 46%,#000 100%);
  mask-image:radial-gradient(120% 95% at 50% 50%,rgba(0,0,0,.40) 0%,rgba(0,0,0,.72) 46%,#000 100%)}
.wrap{position:relative;z-index:1}
'''

# Faithful port of RENDERERS["weave.rope"] from the Illustration Machine's
# engine.js. Same formulas, same constants, drawn to canvas instead of SVG so a
# full-bleed field of a few hundred ellipses stays cheap. Colors are the Blue
# family resolved dark / electric, matching resolveColors().
WEAVE_JS = '''
(function () {
  const c = document.getElementById('weave');
  if (!c) return;
  const x = c.getContext('2d');

  const PRIMARY = [0, 185, 254];    // Electric Blue, the ink in dark mode
  const GHOST_A = [99, 220, 222];   // Easy Blue
  const GHOST_B = [0, 185, 254];
  const MASTER  = 0.16;             // this is a backdrop, not the artwork

  // engine.js model space
  const BAND = 880, CX0 = 500, CY0 = 500;
  const MAXROWS = 4;

  let W = 0, H = 0, DPR = 1, raf = 0, running = false, last = 0;

  // Each knob rides two sines at unrelated rates, so it wanders instead of
  // looping. Periods land between roughly 20 and 80 seconds: fast enough that
  // the pattern visibly rebuilds itself while you are on the page, slow enough
  // that nothing ever looks like it is animating.
  const osc = [];
  for (let i = 0; i < 5; i++) {
    osc.push({
      p1: 0.000079 + Math.random() * 0.00023, ph1: Math.random() * Math.PI * 2,
      p2: 0.000048 + Math.random() * 0.00011, ph2: Math.random() * Math.PI * 2
    });
  }
  const drift = (i, t, lo, hi) => {
    const o = osc[i];
    const s = Math.sin(t * o.p1 + o.ph1) * 0.62 + Math.sin(t * o.p2 + o.ph2) * 0.38;
    return lo + ((s + 1) / 2) * (hi - lo);
  };

  const mix = (a, b, t) => [0,1,2].map(i => Math.round(a[i] + (b[i]-a[i]) * t));
  const rgba = (col, a) => 'rgba(' + col[0] + ',' + col[1] + ',' + col[2] + ',' + a + ')';

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 1.75);
    W = window.innerWidth; H = window.innerHeight;
    c.width = W * DPR; c.height = H * DPR;
    c.style.width = W + 'px'; c.style.height = H + 'px';
    x.setTransform(DPR, 0, 0, DPR, 0, 0);
  }

  function draw(t) {
    x.setTransform(DPR, 0, 0, DPR, 0, 0);
    x.clearRect(0, 0, W, H);

    // the knobs, four of them breathing on independent cycles
    const detail     = drift(0, t, 0.26, 0.96);
    const rhythm     = drift(1, t, 0.05, 1.00);
    const complexity = drift(2, t, 0.28, 1.00);
    const sizeT      = drift(3, t, 0.32, 0.86);
    const baseRot    = (t * 0.0000135) % Math.PI;   // one slow revolution

    // engine.js formulas, unchanged
    const countF  = 20 + detail * 130;
    const phase   = (1 + rhythm * 29) * Math.PI / 180;
    const rowsF   = 1 + complexity * (MAXROWS - 1);
    const stroke  = 0.4 + 0.30 * 2.0;
    const ew = 160 + sizeT * 590;
    const eh = 105 + sizeT * 395;
    const rowH   = eh * 2 * 0.18;
    const rowOff = phase * 0.5;
    const pitchM = countF > 1 ? BAND / (countF - 1) : BAND;

    // The model composes a finite band inside a 1000 box. A full-bleed backdrop
    // needs the rope to keep going, so we hold the model's pitch and extend the
    // index range until it clears both edges. Everything else is the model.
    const S = Math.max(H / 820, W / 2400);
    const pitch = pitchM * S, rw = ew * S, rh = eh * S, rowPx = rowH * S;
    const span = Math.max(3, Math.min(80, Math.ceil((W / 2 + rw * 0.40) / pitch)));
    const rows = Math.ceil(rowsF);
    const cyMid = H / 2 - ((rowsF - 1) * rowPx) / 2;

    const master = MASTER * (1.46 - detail * 0.62);   // hold perceived density flat
    x.lineWidth = stroke * S * (1 - detail * 0.22);

    for (let r = 0; r < rows; r++) {
      const rowOn = Math.min(1, rowsF - r);          // rows fade, never appear
      if (rowOn <= 0.004) continue;
      const cy = cyMid + r * rowPx;
      const centerRow = (rowsF > 1 && r === Math.floor(rows / 2));
      for (let i = -span; i <= span; i++) {
        const cx = W / 2 + i * pitch;
        const rot = baseRot + i * phase + r * rowOff;
        // edge is measured off the viewport, so the rope thins toward the sides
        // instead of stopping in a bright pile-up at the band's end cap
        const edge = Math.min(1, Math.abs(cx - W / 2) / (W * 0.62));
        const useGhost = !(centerRow && edge <= 0.45);
        let col, a;
        if (useGhost) { col = mix(GHOST_A, GHOST_B, 1 - edge); a = 0.18 + 0.42 * (1 - edge); }
        else          { col = PRIMARY;                          a = 0.85; }
        a *= master * rowOn * (1 - edge * 0.72);
        if (a < 0.002) continue;
        x.strokeStyle = rgba(col, a.toFixed(4));
        x.beginPath();
        x.ellipse(cx, cy, rw, rh, rot, 0, Math.PI * 2);
        x.stroke();
      }
    }
  }

  // 30fps is plenty for something this slow, and halves the cost
  const loop = (now) => {
    raf = requestAnimationFrame(loop);
    if (now - last < 33) return;
    last = now;
    draw(now);
  };
  const start = () => { if (!running) { running = true; raf = requestAnimationFrame(loop); } };
  const stop  = () => { running = false; cancelAnimationFrame(raf); };

  resize();
  window.addEventListener('resize', () => { resize(); if (!running) draw(performance.now()); });
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());

  if (window.matchMedia('(prefers-reduced-motion: no-preference)').matches) start();
  else draw(performance.now() + Math.random() * 200000);   // one still frame, random state
})();
'''


LOCKUPS=[
 ("Primary","Primary","Full lockup. Outlined panels."),
 ("Primary-Reverse","Primary Reverse","Full lockup. Filled panels."),
 ("Stacked","Stacked","Condensed lockup. Outlined panels."),
 ("Stacked-Reverse","Stacked Reverse","Condensed lockup. Filled panels."),
 ("LABS","LABS","Panels alone."),
 ("Icon","Icon","Single panel. Outlined."),
 ("Icon-Reverse","Icon Reverse","Single panel. Filled."),
]
by={ (e['type'],e['variant']):e for e in M }

def card(typ,var):
    e=by[(typ,var)]; n=e['name']
    light = var in ("Color","Black")
    stage_cls = "stage light" if light else "stage dark"
    # cap displayed width so icons don't blow up
    disp = min(e['w'], 300)
    pngs="".join(f'<a class="px" href="{BASE}/png/{n}@{l}.png" download>{t}</a>'
                 for l,t in [("1x","1×"),("2x","2×"),("3x","3×"),("3000","3000")])
    return f'''<div class="card">
  <div class="{stage_cls}"><img src="{BASE}/svg/{n}.svg" alt="{n}" style="width:{disp}px;max-width:100%"></div>
  <div class="vlabel mono">{var}</div>
  <div class="dl">
    <a class="btn" href="{BASE}/svg/{n}.svg" download>SVG</a>
    <a class="btn" href="{BASE}/eps/{n}.eps" download>EPS</a>
    <span class="pngs"><span class="pl mono">PNG</span>{pngs}</span>
  </div>
  <button class="path mono" data-copy="{ABS}/svg/{n}.svg" title="Copy SVG URL">
    <span class="pt">/logos/labs/svg/{n}.svg</span><span class="ci">COPY</span>
  </button>
</div>'''

sections=""
for typ,title,note in LOCKUPS:
    e=by[(typ,'Color')]
    dims=f"{round(e['w'])} × {round(e['h'])}"
    cards="".join(card(typ,v) for v in ("Color","White","Black"))
    sections+=f'''<section class="lock" id="{typ.lower()}">
  <div class="lhead">
    <h2 class="mono">{title}</h2>
    <span class="lnote">{note}</span>
    <span class="ldim mono">{dims}</span>
  </div>
  <div class="cards">{cards}</div>
</section>'''

COLORS=[("Electric Blue","#00B9FE","0 185 254","64 10 0 0"),
        ("Dark Blue","#01233C","1 35 60","98 81 47 54"),
        ("Black","#231F20","35 31 32","70 67 64 74")]
swatches="".join(f'''<div class="sw">
 <div class="chip" style="background:{h}"></div>
 <div class="swname">{n}</div>
 <div class="vals">
  <button class="val mono" data-copy="{h}"><b>HEX</b><span>{h}</span></button>
  <button class="val mono" data-copy="rgb({r.replace(' ',', ')})"><b>RGB</b><span>{r.replace(' ',' / ')}</span></button>
  <button class="val mono" data-copy="C{c.split()[0]} M{c.split()[1]} Y{c.split()[2]} K{c.split()[3]}"><b>CMYK</b><span>{c.replace(' ',' / ')}</span></button>
 </div></div>''' for n,h,r,c in COLORS)

pw=by[('Primary','Color')]['w']
ph=by[('Primary','Color')]['h']
csW=pw+2*PANEL; csH=ph+2*PANEL
ux=PANEL/csW*100; uy=PANEL/csH*100
aw=pw/csW*100;    ah=ph/csH*100
cs_pad=ux
updated=datetime.date.today().strftime("%B %-d, %Y")

html=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Louisiana Innovation Labs Identity Assets</title>
<meta name="description" content="Logo files and color values for the Louisiana Innovation Labs identity.">
<link rel="icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Karla:wght@700;800&display=swap" rel="stylesheet">
<style>
{CSS}
header{{padding:88px 0 0}}
.eyebrow{{font-size:11.5px;color:var(--electric);margin:0 0 28px}}
.eyebrow a{{text-decoration:none;opacity:.75}} .eyebrow a:hover{{opacity:1}}
h1{{font-weight:300;font-size:clamp(34px,5.2vw,58px);line-height:1.04;margin:0;letter-spacing:-.02em}}
h1 b{{font-weight:700;display:block}}
.lede{{margin:24px 0 0;max-width:46ch;font-size:17px;line-height:1.5;color:var(--body)}}
.topdl{{margin:40px 0 0;display:flex;gap:14px;flex-wrap:wrap;align-items:center}}
.zip{{display:inline-block;background:var(--electric);color:var(--dark);padding:13px 22px;
  font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.1em;font-weight:700;
  text-transform:uppercase;text-decoration:none;transition:background .15s}}
.zip:hover{{background:var(--easy)}}
.zipnote{{font-size:11px;color:rgba(255,255,255,.4);letter-spacing:.08em}}
hr.rule{{border:0;border-top:1px solid var(--rule);margin:72px 0 0}}

.lock{{padding:56px 0 0}}
.lhead{{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;
  border-bottom:1px solid var(--rule-soft);padding-bottom:16px;margin-bottom:28px}}
h2{{font-size:13px;color:var(--electric);margin:0;font-weight:700}}
.lnote{{font-size:14px;color:var(--body)}}
.ldim{{margin-left:auto;font-size:10.5px;color:rgba(255,255,255,.32)}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
@media(max-width:860px){{.cards{{grid-template-columns:1fr}}}}
.card{{border:1px solid var(--rule-soft)}}
.stage{{height:190px;display:flex;align-items:center;justify-content:center;padding:30px}}
.stage.light{{background:#fff}}
.stage.dark{{background:var(--dark);border-bottom:1px solid var(--rule-soft);
  background-image:linear-gradient(rgba(255,255,255,.03),rgba(255,255,255,.03))}}
.vlabel{{font-size:10px;color:var(--easy);padding:14px 14px 0}}
.dl{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px 14px 14px}}
.btn{{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.08em;
  border:1px solid var(--rule);color:#fff;padding:7px 11px;text-decoration:none;transition:.15s}}
.btn:hover{{background:var(--electric);border-color:var(--electric);color:var(--dark)}}
.pngs{{display:flex;align-items:center;gap:0;border:1px solid var(--rule)}}
.pl{{font-size:10.5px;padding:7px 9px;color:rgba(255,255,255,.45);border-right:1px solid var(--rule-soft)}}
.px{{font-family:'JetBrains Mono',monospace;font-size:10.5px;padding:7px 8px;text-decoration:none;
  color:var(--easy);border-right:1px solid var(--rule-soft);transition:.15s}}
.px:last-child{{border-right:0}}
.px:hover{{background:var(--electric);color:var(--dark)}}
.path{{display:flex;width:100%;align-items:center;justify-content:space-between;gap:10px;
  background:transparent;border:0;border-top:1px solid var(--rule-soft);
  padding:11px 14px;cursor:pointer;font-size:9.5px;color:rgba(255,255,255,.38);
  text-align:left;transition:.15s;font-family:'JetBrains Mono',monospace;
  text-transform:none;letter-spacing:.03em}}
.path:hover{{color:#fff;background:rgba(0,185,254,.07)}}
.pt{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.ci{{color:var(--electric);letter-spacing:.1em;flex-shrink:0}}
.path.copied .ci::after{{content:'✓ COPIED'}}
.path.copied .ci{{font-size:0}}
.path.copied .ci::after{{font-size:9.5px}}

.block{{padding:80px 0 0}}
h3{{font-size:13px;color:var(--electric);margin:0 0 8px;font-weight:700;
  font-family:'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase}}
.bnote{{font-size:14px;color:var(--body);margin:0 0 28px;max-width:52ch;line-height:1.5}}

.csbox{{background:#fff;padding:44px;display:flex;justify-content:center}}
.csfig{{position:relative;width:100%;max-width:620px}}
.csfig .art{{position:absolute;display:block}}
.csbound{{position:absolute;border:1px dashed rgba(0,185,254,.8)}}
.csunit{{position:absolute;background:rgba(0,185,254,.13);
  display:flex;align-items:center;justify-content:center}}
.csul{{font-family:'JetBrains Mono',monospace;font-size:9px;color:#01233C;
  letter-spacing:.08em;white-space:nowrap}}

.mins{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
@media(max-width:760px){{.mins{{grid-template-columns:1fr}}}}
.min{{background:#fff;padding:32px;display:flex;flex-direction:column;
  align-items:flex-start;gap:26px;min-height:200px}}
.minart{{flex:1;display:flex;align-items:center}}
.minlabel{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.09em;
  color:#01233C;text-transform:uppercase}}
.minlabel b{{color:#00A0DC}}
.cmp{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}}
@media(max-width:760px){{.cmp{{grid-template-columns:1fr}}}}
.cmpc{{background:#fff;padding:36px;text-align:center}}
.cmpc .cl{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.09em;
  margin-top:22px;text-transform:uppercase}}
.bad{{color:rgba(1,35,60,.42)}} .good{{color:#01233C}}
.cl b{{font-weight:400}}

.sws{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
@media(max-width:760px){{.sws{{grid-template-columns:1fr}}}}
.sw{{border:1px solid var(--rule-soft)}}
.chip{{height:96px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}}
.swname{{font-size:15px;padding:16px 16px 2px}}
.vals{{padding:0 8px 8px}}
.val{{display:flex;width:100%;gap:12px;align-items:center;background:transparent;border:0;
  border-top:1px solid var(--rule-soft);padding:9px 8px;cursor:pointer;
  font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.06em;
  color:rgba(255,255,255,.62);transition:.15s;text-align:left}}
.val:hover{{color:#fff;background:rgba(0,185,254,.07)}}
.val b{{color:var(--electric);font-weight:400;width:42px;flex-shrink:0}}
.val.copied span::after{{content:'  ✓';color:var(--electric)}}

footer{{margin-top:96px;border-top:1px solid var(--rule);padding:32px 0 72px;
  display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}}
.fnote{{font-size:12.5px;color:var(--body);max-width:44ch;line-height:1.5}}
.fmeta{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.08em;
  color:rgba(255,255,255,.34);text-align:right}}
.fmeta a{{color:var(--easy);text-decoration:none}}
.fright{{display:flex;flex-direction:column;align-items:flex-end;gap:14px}}
.fright .fmeta{{margin:0}}
@media(max-width:640px){{.fright{{align-items:flex-start}}}}
</style></head>
<body>
<div class="wrap">
<header>
  <p class="eyebrow mono"><a href="/">ASSETS.LA.IO</a> / LABS</p>
  <h1>Louisiana Innovation<b>Labs</b></h1>
  <p class="lede">Identity assets for the Labs sub-brand. Seven lockups, each in color, white, and black. SVG and EPS are vector and scale to any size. PNG is transparent.</p>
  <div class="topdl">
    <a class="zip" href="{BASE}/LILabs-Logos.zip" download>+ Download everything</a>
    <span class="zipnote mono">ZIP · 3.9 MB · 126 FILES</span>
  </div>
</header>
<hr class="rule">

{sections}

<section class="block">
  <h3>Clear space</h3>
  <p class="bnote">One LABS panel on all sides.</p>
  <div class="csbox">
    <div class="csfig" style="aspect-ratio:{csW}/{csH}">
      <div class="csunit" style="left:0;top:0;width:{ux}%;height:{uy}%"><span class="csul">1 PANEL</span></div>
      <div class="csbound" style="left:{ux}%;top:{uy}%;width:{aw}%;height:{ah}%"></div>
      <img class="art" src="{BASE}/svg/LILabs-Primary-Color.svg" alt="Clear space"
           style="left:{ux}%;top:{uy}%;width:{aw}%;height:{ah}%">
    </div>
  </div>
</section>

<section class="block">
  <h3>Minimum size</h3>
  <p class="bnote">Shown actual size.</p>
  <div class="mins">
    <div class="min">
      <div class="minart"><img src="{BASE}/svg/LILabs-Primary-Color.svg" alt="Primary at 120px" style="width:120px"></div>
      <span class="minlabel">Primary and Stacked · <b>120px / 1.25in wide</b></span>
    </div>
    <div class="min">
      <div class="minart"><img src="{BASE}/svg/LILabs-Icon-Color.svg" alt="Icon at 40px" style="width:40px"></div>
      <span class="minlabel">Icon · <b>40px / 0.5in wide</b></span>
    </div>
  </div>
  <div class="cmp">
    <div class="cmpc">
      <img src="{BASE}/svg/LILabs-Stacked-Color.svg" alt="Outlined at 90px" style="width:90px">
      <div class="cl bad">&#10005; &nbsp;Outlined below 100px</div>
    </div>
    <div class="cmpc">
      <img src="{BASE}/svg/LILabs-Stacked-Reverse-Color.svg" alt="Filled at 90px" style="width:90px">
      <div class="cl good">+ &nbsp;Filled below 100px</div>
    </div>
  </div>
</section>

<section class="block">
  <h3>Color</h3>
  <p class="bnote">Click any value to copy.</p>
  <div class="sws">{swatches}</div>
</section>

<footer>
  <p class="fnote">Logotype is custom artwork. Not a typeface. Do not recreate.</p>
  <div class="fright">
    <p class="fmeta">LAST UPDATED {updated.upper()}</p>
    {MPSIG}
  </div>
</footer>
</div>
<script>
document.addEventListener('click',function(e){{
  var b=e.target.closest('[data-copy]'); if(!b) return;
  navigator.clipboard.writeText(b.dataset.copy).then(function(){{
    b.classList.add('copied');
    setTimeout(function(){{b.classList.remove('copied')}},1400);
  }});
}});
</script>
</body></html>'''
os.makedirs(os.path.join(REPO,'labs'),exist_ok=True)
open(os.path.join(REPO,'labs','index.html'),'w').write(html)
print('labs page written',len(html),'bytes')


# ---------- directory page and 404 ----------
HEAD='''<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Karla:wght@700;800&display=swap" rel="stylesheet">'''

ENTRIES=[
 ("Brand Kit for AI","/ai",False,"The LA.IO brand system, set up for Claude, Lovable, and any other AI. Fonts, color, logos, motifs, instructions, and component code."),
 ("Illustration Machine","/illustrator",False,"Generates original illustration and background graphics in the LA.IO system."),
 ("Badge Builder","https://badgebuilder.la.io",True,"Builds embeddable, trackable LA.IO badges for partner sites."),
 ("Louisiana Innovation Labs","/labs",False,"Identity assets for the Labs sub-brand."),
]
rows=""
for name,href,ext,desc in ENTRIES:
    label="badgebuilder.la.io" if ext else href
    extra=' target="_blank" rel="noopener"' if ext else ''
    cls="row ext" if ext else "row"
    arrow='<span class="arw">↗</span>' if ext else ''
    rows+=f'''<a class="{cls}" href="{href}"{extra}>
  <span class="plus">+</span>
  <span class="rname">{name}</span>
  <span class="rpath mono">{label}{arrow}</span>
  <span class="rdesc">{desc}</span>
</a>'''

ROOT_CSS=f'''{CSS}{WEAVE_CSS}
body{{min-height:100vh;display:flex;flex-direction:column}}
.wrap{{width:100%;max-width:880px;flex:1;display:flex;flex-direction:column;
  justify-content:center;padding-top:56px;padding-bottom:40px}}
.eyebrow{{font-size:12px;color:var(--electric);margin:0 0 30px;letter-spacing:.16em;font-weight:700}}
.lede{{margin:0 0 52px;max-width:44ch;font-size:clamp(17px,2.1vw,21px);
  line-height:1.45;color:var(--body);font-weight:300}}
.rows{{border-top:1px solid var(--rule-soft)}}
.row{{display:grid;grid-template-columns:22px minmax(0,1fr) auto;
  grid-template-areas:"p n a" ". d d";
  gap:2px 4px;align-items:baseline;
  padding:20px 0;border-bottom:1px solid var(--rule-soft);
  text-decoration:none;transition:.16s}}
.row:hover{{background:rgba(0,185,254,.06);padding-left:10px;padding-right:10px;
  box-shadow:-10px 0 0 rgba(0,185,254,.06),10px 0 0 rgba(0,185,254,.06)}}
.plus{{grid-area:p;color:var(--electric);font-weight:400;font-size:17px;line-height:1.2}}
.rname{{grid-area:n;font-size:clamp(18px,2.4vw,23px);font-weight:400;letter-spacing:-.01em}}
.rpath{{grid-area:a;font-size:10.5px;color:var(--easy);white-space:nowrap;padding-left:24px}}
.row.ext .rpath{{color:var(--electric)}}
.arw{{padding-left:5px}}
.rdesc{{grid-area:d;font-size:14.5px;line-height:1.45;color:var(--body);max-width:46ch;margin-top:5px}}
.row:hover .rname{{color:var(--electric)}}
.foot{{position:relative;z-index:1;width:100%;max-width:880px;margin:0 auto;padding:0 32px 40px}}
@media(max-width:640px){{.foot{{padding:0 20px 32px}}}}
@media(max-width:640px){{
  .row{{grid-template-columns:20px minmax(0,1fr);grid-template-areas:"p n" ". a" ". d"}}
  .rpath{{padding-left:0;margin-top:5px}}
  .lede{{margin-bottom:36px}}
}}
'''

index=f'''<!doctype html>
<html lang="en"><head>{HEAD}
<title>assets.la.io</title>
<meta name="description" content="Brand assets, tools, and documentation for LA.IO and the Louisiana Innovation ecosystem.">
<style>{ROOT_CSS}</style></head>
<body>
<canvas id="weave" aria-hidden="true"></canvas>
<div class="wrap">
{LOGO}
<p class="lede">Brand assets, tools, and documentation for LA.IO and the Louisiana Innovation ecosystem.</p>
<nav class="rows">{rows}</nav>
</div>
<footer class="foot">{MPSIG}</footer>
<script>{WEAVE_JS}</script>
</body></html>'''
open(os.path.join(REPO,'index.html'),'w').write(index)

nf=f'''<!doctype html>
<html lang="en"><head>{HEAD}
<title>404 · assets.la.io</title>
<meta name="robots" content="noindex">
<style>{CSS}
body{{min-height:100vh;display:flex;flex-direction:column}}
.wrap{{width:100%;max-width:880px;flex:1;display:flex;flex-direction:column;justify-content:center}}
.foot{{width:100%;max-width:880px;margin:0 auto;padding:0 32px 40px}}
@media(max-width:640px){{.foot{{padding:0 20px 32px}}}}
.brand{{width:168px;margin-bottom:30px}}
.eyebrow{{font-size:12px;color:var(--electric);margin:0 0 30px;letter-spacing:.16em;font-weight:700}}
h1{{font-weight:300;font-size:clamp(28px,4.4vw,46px);line-height:1.15;margin:0;
  letter-spacing:-.02em;max-width:18ch}}
h1 a{{color:var(--electric);text-decoration:none;border-bottom:1px solid rgba(0,185,254,.35)}}
h1 a:hover{{border-bottom-color:var(--electric)}}
.code{{margin-top:44px;font-size:11px;color:rgba(255,255,255,.34);letter-spacing:.12em}}
</style></head>
<body><div class="wrap">
{LOGO}
<h1>Nothing here. Try <a href="/">assets.la.io</a>.</h1>
<p class="code mono">404</p>
</div>
<footer class="foot">{MPSIG}</footer>
</body></html>'''
open(os.path.join(REPO,'404.html'),'w').write(nf)
print('index + 404 written')

# ---------- /ai: Brand Kit for AI ----------
# One page for every tool. It replaced both the old Blue /ai inventory and the
# hand-built Claude kit page, and it keeps that page's look: its CSS
# and its rings + intro JS were extracted to _build/ai-page/ and are inlined
# here as they were. Paste blocks are read from the fenced blocks in the source
# .md files at build time, so the page cannot drift from the files people
# download. Never type paste text into this script.
AI   = os.path.join(REPO, "ai")
PAGE = os.path.join(HERE, "ai-page")

def _read(*parts):
    return open(os.path.join(*parts), encoding="utf-8").read()

def fence(rel):
    """The first fenced code block in a repo file, without the fences."""
    m = re.search(r"```[^\n]*\n(.*?)\n```", _read(REPO, rel), re.S)
    if not m:
        raise SystemExit(f"gen_pages: no fenced block in {rel}")
    return m.group(1)

def fields(rel, names):
    """Every '### Field name' heading directly followed by a fenced block, as
    (name, block) pairs. The Claude Design setup is a form, so its doc holds
    one block per field. Exits if the field names drift from the form's."""
    pairs = re.findall(r"^### ([^\n]+)\n+```[^\n]*\n(.*?)\n```", _read(REPO, rel), re.S | re.M)
    if [n for n, _ in pairs] != names:
        raise SystemExit(f"gen_pages: {rel} fields are {[n for n, _ in pairs]}, expected {names}")
    return pairs

# The three Claude Design form fields the setup fills. The other three stay empty.
DESIGN_FIELDS = ["Company name and blurb", "Link code from GitHub", "Any other notes"]

PROMPT = ("Fetch https://assets.la.io/ai/CLAUDE.md and follow it as the "
          "brand system for this project.")

FONTS = [
    ("AktivGrotesk_Th.woff2",   "Thin",         "100"),
    ("AktivGrotesk_ThIt.woff2", "Thin Italic",  "100"),
    ("AktivGrotesk_Lt.woff2",   "Light",        "300"),
    ("AktivGrotesk_LtIt.woff2", "Light Italic", "300"),
    ("AktivGrotesk_Rg.woff2",   "Regular",      "400"),
    ("AktivGrotesk_It.woff2",   "Italic",       "400"),
    ("AktivGrotesk_SBd.woff2",  "Semibold",     "600"),
    ("AktivGrotesk_Bd.woff2",   "Bold",         "700"),
    ("AktivGrotesk_BdIt.woff2", "Bold Italic",  "700"),
]

# The two ways to load Aktiv Grotesk, in order of preference. Listed before the woff2s.
FONT_CSS = [
    ("laio-fonts-inline.css", "Embedded",
     "Paste the contents into a <style> tag. Zero network requests. Use in claude.ai "
     "artifacts, Claude Design, Lovable previews, email, anything sandboxed. This is "
     "the default for AI-generated work."),
    ("laio-fonts.css", "Hosted",
     "For real sites and apps on a domain only, never inside an artifact or preview: "
     '<link rel="stylesheet" href="https://assets.la.io/fonts/laio-fonts.css">.'),
]

DATA = [
    ("colors/laio-tokens.json", "All five color families as JSON. Hex, RGB, and the brand name for each."),
    ("colors/laio-colors.css",  "The same values as CSS custom properties. Link it or paste it."),
]

LOGOS = [
    ("LAIO-COMPLETE.svg",           "Complete lockup",        "The default, everywhere. Use this unless a rule below says otherwise."),
    ("LAIO-BASE.svg",               "Base mark",              "Only when the mark is under about 120px wide and the subtext would be illegible."),
    ("LAIO-HORZ.svg",               "Horizontal lockup",      "Only in a header or nav bar."),
    ("LOUISIANA-INNOVATION-A.svg",  "Louisiana Innovation A", "Secondary mark, stacked. Under or beside the primary, never alone."),
    ("LOUISIANA-INNOVATION-B.svg",  "Louisiana Innovation B", "Secondary mark, condensed. Under or beside the primary, never alone."),
    ("DIVISION-LINE.svg",           "Division line",          "Secondary mark. Sits under the primary, never alone."),
    ("LED-WHITE.svg",               "LED, white",             "Louisiana Economic Development. The default, on dark grounds."),
    ("LED-BLACK.svg",               "LED, black",             "On light grounds. Recolor to the family dark."),
    ("LED-SMALL-WHITE.svg",         "LED small, white",       "The compact LED lockup, on dark grounds."),
    ("LED-SMALL-BLACK.svg",         "LED small, black",       "The compact LED lockup, on light grounds."),
]

# The one outside logo the kit ships. Shown once under the logo cards, and in llms.txt.
LED_NOTE = ("Louisiana Economic Development, the parent agency. White on dark grounds is "
            "the default. Black on light grounds, recolored to the family dark. LED's "
            "gold and full-color marks belong to LED's own communications; the LA.IO kit "
            "carries white and black only. Sits under or beside the LA.IO mark, never above it.")

MOTIFS = [
    ("LAIO-PLUS.svg",             "Plus"),
    ("LAIO-X.svg",                "X"),
    ("LAIO-DIAMOND.svg",          "Diamond"),
    ("LAIO-DIAMOND-EMPTY.svg",    "Diamond outline"),
    ("LAIO-LEFT-BRACKET.svg",     "Left bracket"),
    ("LAIO-RIGHT-BRACKET.svg",    "Right bracket"),
    ("LAIO-UP-BRACKET.svg",       "Up bracket"),
    ("LAIO-DOWN-BRACKET.svg",     "Down bracket"),
    ("LAIO-BRACKET-CORNER-1.svg", "Corner 1"),
    ("LAIO-BRACKET-CORNER-2.svg", "Corner 2"),
    ("LAIO-CORNER-L.svg",         "L-corner"),
    ("LAIO-SQUARE.svg",           "Square"),
    ("LAIO-SQUARE-EMPTY.svg",     "Square outline"),
    ("LAIO-FIELD-DIAGONAL.svg",   "Diagonal field"),
    ("LAIO-HATCH.svg",            "Hatch tile"),
    ("LAIO-WIRE-NODE.svg",        "Wire node"),
]

DOCS = [
    ("ai/CLAUDE.md",                              "Brand instructions",           "Voice, banned language, color, type, and asset URLs. The one file to hand an AI."),
    ("ai/AGENTS.md",                              "AGENTS.md",                    "The same file, for Cursor and other agents that look for AGENTS.md."),
    ("ai/laio-brand/BRAND.md",                    "Full brand system",            "The long form. Load when the work needs depth."),
    ("ai/laio-brand/COMPONENTS.md",               "Component code",               "Buttons, cards, eyebrows, and layout patterns as code."),
    ("ai/laio-brand/VOICE.md",                    "Voice guide",                  "Speaker profiles, the full ban list, and the standing rules for AI work."),
    ("ai/laio-brand.zip",                         "Packaged skill",               "The whole kit as a Claude skill. Unzip into ~/.claude/skills/."),
    ("ai/claude-ai-project-setup.md",             "claude.ai Project setup",      "Custom instructions and knowledge files for a Claude Project."),
    ("ai/claude-design-setup.md",                 "Claude Design setup",          "The three form fields that set up the LA.IO Design System from this repo."),
    ("ai/lovable/LAIO_LOVABLE_GUIDE.md",          "Lovable guide",                "How to start an LA.IO project in Lovable."),
    ("ai/lovable/LOVABLE_CUSTOM_INSTRUCTIONS.md", "Lovable workspace instructions","Brand rules for every project in a Lovable workspace."),
    ("ai/lovable/LOVABLE_STARTER_PROMPT.md",      "Lovable starter prompt",       "The first message that builds the LA.IO starter template."),
    ("ai/lovable/LOVABLE_STARTER_TEMPLATE_SPEC.md","Lovable starter template spec","What the starter template contains and how it is wired."),
    ("llms.txt",                                  "Machine-readable index",       "A plain list of everything on this page. Point a crawler or an agent at this."),
]

# ---- markup helpers ----
def code(text, wrap=False):
    cls = "code code-wrap" if wrap else "code"
    return (f'<div class="{cls}">\n<button class="copy">Copy</button>\n'
            f'<pre>{html_escape(text, quote=False)}</pre>\n</div>')

def dl(href, label, ghost=False):
    cls = "dl ghost" if ghost else "dl"
    name = href.rsplit("/", 1)[-1]
    return (f'<a class="{cls}" href="{href}" download="{name}">'
            f'<span class="ico">&darr;</span> {label}</a>')

def dlrow(*links):
    return '<div class="dl-row">\n' + "\n".join(links) + '\n</div>'

def urlrow(path, name, desc):
    url = "https://assets.la.io/" + path
    return (f'<div class="urow"><span class="uplus">+</span>'
            f'<div class="ubody"><a class="uname" href="/{path}">{name}</a>'
            f'<div class="udesc">{desc}</div></div>'
            f'<button class="ucopy" data-copy="{url}"><span class="upath">/{path}</span>'
            f'<span class="uci">Copy</span></button></div>\n')

docrows = "".join(urlrow(p, n, d) for p, n, d in DOCS)
fontrows = "".join(
    urlrow("fonts/" + f, f'{name} <span class="uw">CSS</span>', html_escape(desc))
    for f, name, desc in FONT_CSS) + "".join(
    urlrow("fonts/" + f, f'{label} <span class="uw">{w}</span>', "woff2. Self-hosted, open CORS.")
    for f, label, w in FONTS)
datarows = "".join(urlrow(p, p.split("/")[-1], d) for p, d in DATA)

logocards = "".join(f'''<div class="acard">
  <div class="astage{' dark' if 'WHITE' in f else ''}"><img src="/logos/{f}" alt="{name}" loading="lazy"></div>
  <a class="aname" href="/logos/{f}">{name}</a>
  <div class="adesc">{desc}</div>
  <button class="ucopy" data-copy="https://assets.la.io/logos/{f}"><span class="upath">/logos/{f}</span><span class="uci">Copy</span></button>
</div>
''' for f, name, desc in LOGOS)

motifcards = "".join(f'''<div class="mcard">
  <div class="mstage"><img src="/motifs/{f}" alt="{name}" loading="lazy"></div>
  <div class="mname">{name}</div>
  <button class="ucopy" data-copy="https://assets.la.io/motifs/{f}"><span class="upath">/motifs/{f}</span><span class="uci">Copy</span></button>
</div>
''' for f, name in MOTIFS)

# The LA.IO mark as the original page inlined it (hero and footer).
MARK = '''<svg class="laio-mark" viewBox="0 0 280.17 67.88" role="img" aria-label="LA.IO">
        <path d="M66.14,19.91v22.03h14.23v6.89h-22.03v-28.92h7.8Z"/>
        <path d="M107.72,43.23h-8.58l-1.56,5.6h-7.57l8.86-28.92h9.55l8.86,28.92h-7.99l-1.56-5.6ZM100.79,37.4h5.32l-2.57-9.18h-.18l-2.57,9.18Z"/>
        <path d="M134.3,40.02h8.81v8.81h-8.81v-8.81Z"/>
        <path d="M162.67,48.83v-6.75h7.21v-15.42h-7.21v-6.75h22.22v6.75h-7.21v15.42h7.21v6.75h-22.22Z"/>
        <path d="M208.85,49.38c-7.44,0-12.99-6.11-12.99-15.01s5.55-15.01,12.99-15.01,12.99,6.1,12.99,15.01-5.55,15.01-12.99,15.01ZM208.85,26.25c-3.12,0-5.1,3.21-5.1,8.12s1.97,8.12,5.1,8.12,5.09-3.21,5.09-8.12-1.97-8.12-5.09-8.12Z"/>
        <polygon points="14.73 33.94 41.3 60.51 33.94 67.88 0 33.94 33.94 0 41.3 7.36 14.73 33.94"/>
        <polygon points="265.45 33.94 238.87 7.36 246.24 0 280.17 33.94 246.24 67.88 238.87 60.51 265.45 33.94"/>
      </svg>'''

# ---- page head ----
AI_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LA.IO Brand Kit for AI</title>
<meta name="description" content="The LA.IO brand system, set up for Claude, Lovable, and any other AI. Voice, color, type, logos, motifs, and component code.">
<link rel="icon" type="image/png" href="/favicon.png">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Karla:wght@400;700;800&display=swap" rel="stylesheet">
<style>
'''

# ---- intro, top bar (as the original page had them) ----
INTRO = '''</style>
</head>
<body>

  <!-- orbital-rings backdrop: intro centerpiece, then live header background -->
  <canvas id="rings" aria-hidden="true"></canvas>

  <!-- ============ INTRO ============ -->
  <div id="intro" aria-hidden="true"></div>
  <div id="intro-logo" title="Skip (click)">
    <svg class="il-logo" viewBox="0 0 280.17 67.88" role="img" aria-label="LA.IO">
      <g class="il-letters">
        <path d="M66.14,19.91v22.03h14.23v6.89h-22.03v-28.92h7.8Z"/>
        <path d="M107.72,43.23h-8.58l-1.56,5.6h-7.57l8.86-28.92h9.55l8.86,28.92h-7.99l-1.56-5.6ZM100.79,37.4h5.32l-2.57-9.18h-.18l-2.57,9.18Z"/>
        <path d="M134.3,40.02h8.81v8.81h-8.81v-8.81Z"/>
        <path d="M162.67,48.83v-6.75h7.21v-15.42h-7.21v-6.75h22.22v6.75h-7.21v15.42h7.21v6.75h-22.22Z"/>
        <path d="M208.85,49.38c-7.44,0-12.99-6.11-12.99-15.01s5.55-15.01,12.99-15.01,12.99,6.1,12.99,15.01-5.55,15.01-12.99,15.01ZM208.85,26.25c-3.12,0-5.1,3.21-5.1,8.12s1.97,8.12,5.1,8.12,5.09-3.21,5.09-8.12-1.97-8.12-5.09-8.12Z"/>
      </g>
      <g class="il-chev il-l"><polygon points="14.73 33.94 41.3 60.51 33.94 67.88 0 33.94 33.94 0 41.3 7.36 14.73 33.94"/></g>
      <g class="il-chev il-r"><polygon points="265.45 33.94 238.87 7.36 246.24 0 280.17 33.94 246.24 67.88 238.87 60.51 265.45 33.94"/></g>
    </svg>
    <div class="il-tag mono">Louisiana Innovation</div>
  </div>

  <!-- ============ TOP BAR ============ -->
  <div class="topbar">
    <div class="wrap">
      <a class="mp-logo" href="https://mondayandpartners.com">MONDAY <span class="plus">+</span> PARTNERS</a>
      <span class="mono tag">LA.IO Brand Kit</span>
    </div>
  </div>
'''

HERO = f'''
  <!-- ============ HERO ============ -->
  <header class="hero">
    <div class="wrap">
      {MARK}
      <span class="mono eyebrow">One kit. Every tool.</span>
      <h1>The LA.IO brand, ready for <span class="accent">any AI.</span></h1>
      <p class="sub">Connect your AI, learn the brand in thirty seconds, take the files. Voice, color, type, logos, and component code, all from one kit.</p>
    </div>
  </header>
'''


# ---- the connector, the first thing on the page ----
# Copy lives in _build/sources/connector.md so the page can be reworded without
# touching this script. Parsed by "## Heading", one section each.
def md_sections(path):
    raw = _read(path)
    out, key, buf = {}, None, []
    for line in raw.split("\n"):
        m = re.match(r"^## (.+)$", line)
        if m:
            if key: out[key] = "\n".join(buf).strip()
            key, buf = m.group(1).strip(), []
        elif key is not None:
            buf.append(line)
    if key: out[key] = "\n".join(buf).strip()
    return out

CONN = md_sections(os.path.join(HERE, "sources", "connector.md"))

def _para(text):
    return "\n".join(f'      <p class="lead">{html_escape(b, quote=False)}</p>'
                      for b in text.split("\n\n") if b.strip())

_ex_intro, _ex_items = [], []
for line in CONN["Examples"].split("\n"):
    if line.startswith("+ "):
        _ex_items.append(f'        <li><span class="m">+</span><span>{html_escape(line[2:], quote=False)}</span></li>')
    elif line.strip():
        _ex_intro.append(line.strip())

_steps = []
for line in CONN["Admin steps"].split("\n"):
    m = re.match(r"^\d+\.\s*(.+?)\|(.+)$", line.strip())
    if not m: continue
    title, desc = m.group(1), m.group(2)
    desc = re.sub(r"`([^`]+)`", r'<code class="inline">\1</code>', html_escape(desc, quote=False).replace("&#x27;", "'"))
    _steps.append(f'        <li><div class="st">{html_escape(title, quote=False)}</div><div class="sd">{desc}</div></li>')

TAB_CONNECTOR = f'''<p class="for">For <b>anyone on claude.ai</b>. The fastest route and the one to use if you can.</p>
{_para(CONN["Lead"])}
<p class="note">{html_escape(" ".join(_ex_intro), quote=False)}</p>
<ul class="examples">
{chr(10).join(_ex_items)}
</ul>
<div class="ready"><span class="plus">+</span><p>{html_escape(CONN["Aside"], quote=False)}</p></div>

<h3 class="subhead">Turn it on</h3>
<ol class="steps">
  <li><div class="st">Check it is there</div><div class="sd">Open Settings, then Connectors. Look for <code class="inline">LA.IO Brand</code> marked <i>Custom</i>.</div></li>
  <li><div class="st">Click Connect</div><div class="sd">That is the whole setup. It does nothing until you do this.</div></li>
  <li><div class="st">Ask for something</div><div class="sd">Try <i>give me a transparent PNG of the LA.IO logo in Easy Blue</i>. A download link means it is working.</div></li>
</ol>

<h3 class="subhead">Not in your list? Send this to your Claude admin</h3>
{_para(CONN["Admin intro"])}
<ol class="steps">
{chr(10).join(_steps)}
</ol>
<div class="ready"><span class="plus">+</span><p><b>Working when:</b> {html_escape(" ".join(CONN["Test"].split()), quote=False)}</p></div>
<p class="note">{html_escape(CONN["Feedback"], quote=False)}</p>'''

# ---- the tabs ----
TAB_CLAUDE = f'''<p class="for">For <b>copy, content, and brand questions</b> on claude.ai. Best for writers and marketers. Set it up once, then every chat in the Project knows the brand.</p>
<ol class="steps">
  <li><div class="st">Create a Project</div><div class="sd">claude.ai &rarr; Projects &rarr; New Project. Name it <code class="inline">LA.IO</code>.</div></li>
  <li><div class="st">Paste the custom instructions</div><div class="sd">Open the Project, click <i>Set custom instructions</i>, and paste the block below.</div>
{code(fence("ai/claude-ai-project-setup.md"))}
  </li>
  <li><div class="st">Add the brand knowledge</div><div class="sd">Download all three files below. In the Project, click <i>Add content</i> (project knowledge) and upload them. <code class="inline">laio-fonts-inline.css</code> carries the Aktiv Grotesk typeface, so artifacts render in the brand font.</div>
{dlrow(dl("/ai/laio-brand/BRAND.md", "Download BRAND.md"), dl("/ai/laio-brand/COMPONENTS.md", "Download COMPONENTS.md", True), dl("/fonts/laio-fonts-inline.css", "Download laio-fonts-inline.css", True))}
  </li>
  <li><div class="st">Start a chat</div><div class="sd">Every conversation inside the Project is now on brand.</div></li>
</ol>
<p class="note">A Project reads its files once. When the kit changes, we will say so, and you re-paste the custom instructions and replace the three files. Nothing else to do.</p>
<div class="ready"><span class="plus">+</span><p><b>Ready when:</b> a fresh chat in the Project answers "what bullet does LA.IO use?" with a plus sign, and a one-slide artifact you ask for shows Aktiv Grotesk and the real LA.IO mark, not typed brackets.</p></div>'''

DESIGN_BLOCKS = "\n".join(f'<div class="fieldname">{html_escape(name)}</div>\n{code(block, wrap=True)}'
                          for name, block in fields("ai/claude-design-setup.md", DESIGN_FIELDS))

TAB_DESIGN = f'''<p class="for">For <b>Claude Design</b> (prototypes, slide decks, visuals). Claude Design has its own Design System feature. You build an <b>LA.IO Design System</b> once, then pick it from the <i>Design System</i> dropdown on any new project and everything comes out on brand. Each person makes their own. Claude Design reads the brand straight from the LA.IO repo on GitHub, so setup is three fields in one form.</p>
<ol class="steps">
  <li><div class="st">Create a new Design System</div><div class="sd">In Claude Design, create a new Design System. The form has six fields. Fill the three below, exactly as written. Leave <i>Link code from your computer</i>, <i>Upload a .fig file</i>, and <i>Add fonts, logos and assets</i> empty.</div></li>
  <li><div class="st">Fill the three fields</div><div class="sd">Copy each block into the form field with the same name.</div>
{DESIGN_BLOCKS}
  </li>
  <li><div class="st">Create it, then select it</div><div class="sd">Create the system. On any New Project (Prototype, Slide deck, and so on) choose <code class="inline">LA.IO Design System</code> from the <i>Design System</i> dropdown.</div></li>
</ol>
<p class="note">A Design System reads the repo once. When the kit changes, we will say so, and you delete the system and recreate it from the three fields. About two minutes.</p>
<div class="ready"><span class="plus">+</span><p><b>Ready when:</b> a project on the LA.IO Design System produces one-family, angular, Aktiv Grotesk layouts with the real LA.IO logo and plus-sign bullets.</p></div>'''

TAB_CODE = f'''<p class="for">For <b>hands-on work and real builds</b>. Cowork uses the skill for multi-step brand work with no code. Claude Code uses the same skill plus a <code class="inline">CLAUDE.md</code> to build sites and apps. Both read one skills folder, so you set it up once. The steps use Finder, no Terminal required.</p>
<ol class="steps">
  <li><div class="st">Download the files</div><div class="sd">Double-click the <code class="inline">.zip</code> to unzip it into a folder named <code class="inline">laio-brand</code>. Building in Claude Code? Grab <code class="inline">CLAUDE.md</code> too.</div>
{dlrow(dl("/ai/laio-brand.zip", "Download the skill (.zip)"), dl("/ai/CLAUDE.md", "Download CLAUDE.md", True))}
  </li>
  <li><div class="st">Open your skills folder</div><div class="sd">Open <b>Finder</b>. Press <span class="kbd">&#8984; &#8679; G</span> to open <i>Go to Folder</i>. Type the line below exactly and press Return.</div>
    <div class="pathbox">~/.claude/skills</div>
    <div class="sd" style="margin-top:12px">If a window opens, you are in the right place. If it says the folder cannot be found, type <code class="inline">~/.claude</code> instead, press Return, then right-click inside that window, choose <i>New Folder</i>, and name it exactly <code class="inline">skills</code>. Open the new <code class="inline">skills</code> folder.</div>
  </li>
  <li><div class="st">Drop the folder in</div><div class="sd">Drag the <code class="inline">laio-brand</code> folder into the <code class="inline">skills</code> folder. When you are done it lives here:</div>
    <div class="pathbox">~/.claude/skills/laio-brand</div>
    <div class="sd" style="margin-top:12px">This makes the skill available in every project, in Cowork and in Claude Code. Prefer it in one project only? Put it in a <code class="inline">.claude/skills</code> folder inside that project instead.</div>
    <details class="alt"><summary>Comfortable with Terminal? Do it in one line</summary>
{code("mkdir -p ~/.claude/skills && cp -R ~/Downloads/laio-brand ~/.claude/skills/")}
    </details>
  </li>
  <li><div class="st">Claude Code: add the always-on rules</div><div class="sd">Put the downloaded <code class="inline">CLAUDE.md</code> in the top folder of your project (next to your other files). If you already have a <code class="inline">CLAUDE.md</code>, paste these contents at the top of it. Cowork users can skip this step.</div></li>
  <li><div class="st">Restart and use it</div><div class="sd">Quit and reopen Cowork, or start a new Claude Code session. Then mention LA.IO and name the color family up front. The skill loads the voice, color, type, and component rules on its own, and Claude Code pulls <code class="inline">COMPONENTS.md</code> for ready-to-use code.</div>
{code("Draft three event-page headline options for LA.IO. Use the laio-brand skill.", wrap=True)}
  </li>
</ol>
<p class="note">Not on a Mac? The folder is the same idea (<code class="inline">.claude/skills</code> in your home folder). Email <a href="mailto:dylan@mondayandpartners.com">dylan@mondayandpartners.com</a> and we will walk you through it.</p>
<div class="ready"><span class="plus">+</span><p><b>Ready when:</b> the request above returns matter-of-fact headlines with plus-sign bullets and no em dashes, and asking Claude Code to scaffold a hero returns angular markup in one color family, Aktiv Grotesk type, and the real LA.IO logo.</p></div>'''

TAB_LOVABLE = f'''<p class="for">For <b>sites and apps built in Lovable</b>. The brand rules live at the workspace level, and a starter template carries the fonts, colors, logo component, and base components. Every new project starts from that template.</p>
<ol class="steps">
  <li><div class="st">Add the workspace instructions</div><div class="sd">Once per Lovable workspace. Paste the contents of <code class="inline">LOVABLE_CUSTOM_INSTRUCTIONS.md</code> into Workspace Knowledge in your Lovable project settings. Every project in the workspace then knows the voice, color, type, and design rules. Skip this if your workspace already has them.</div>
{dlrow(dl("/ai/lovable/LOVABLE_CUSTOM_INSTRUCTIONS.md", "Download workspace instructions"))}
  </li>
  <li><div class="st">Duplicate the LA.IO Starter Template</div><div class="sd">Find <i>LA.IO Starter Template</i> in your projects, open the three-dot menu, and duplicate it. Rename it for your project. Fonts, colors, the logo component, and base components are already wired in. No template in your workspace yet? Start a new project and paste <code class="inline">LOVABLE_STARTER_PROMPT.md</code> as the first message. The spec describes what the finished template contains.</div>
{dlrow(dl("/ai/lovable/LOVABLE_STARTER_PROMPT.md", "Download starter prompt", True), dl("/ai/lovable/LOVABLE_STARTER_TEMPLATE_SPEC.md", "Download template spec", True))}
  </li>
  <li><div class="st">Paste this at the top of your first prompt</div><div class="sd">Fill in the three blanks, then describe what you want to build.</div>
{code(fence("ai/lovable/LAIO_LOVABLE_GUIDE.md"))}
  </li>
  <li><div class="st">Build normally</div><div class="sd">Prompt Lovable the way you always do. The brand system handles the rest. If the preview shows a font other than Aktiv Grotesk, the preview cannot reach assets.la.io: ask Lovable to paste the contents of <code class="inline">laio-fonts-inline.css</code> into a <code class="inline">&lt;style&gt;</code> tag in <code class="inline">index.html</code>.</div></li>
</ol>
<div class="ready"><span class="plus">+</span><p><b>Ready when:</b> a project duplicated from the template shows Aktiv Grotesk headlines, JetBrains Mono eyebrows in the accent color, one color family, square corners, and the real LA.IO logo.</p></div>'''

TAB_OTHER = f'''<p class="for">For <b>ChatGPT, Gemini, Cursor, and anything else</b>, and for any one-off chat. If the tool can fetch a URL, one line sets it up. If it cannot, attach two files.</p>
<h3 class="subhead">Paste one line</h3>
{code(PROMPT, wrap=True)}
<p class="note">Making something visual in a plain chat? Attach CLAUDE.md and laio-fonts-inline.css so the AI has the font in hand.</p>
<ol class="steps">
  <li><div class="st">Paste the brand instruction</div><div class="sd">Paste this at the start of a chat, or into the tool's custom instructions, project instructions, or rules so it applies every time.</div>
{code(PROMPT, wrap=True)}
  </li>
  <li><div class="st">No web access? Attach the files</div><div class="sd">Download both files and attach them to the chat or to the tool's project knowledge. <code class="inline">laio-fonts-inline.css</code> lets any HTML the tool builds render in Aktiv Grotesk.</div>
{dlrow(dl("/ai/CLAUDE.md", "Download CLAUDE.md"), dl("/fonts/laio-fonts-inline.css", "Download laio-fonts-inline.css", True))}
  </li>
  <li><div class="st">Coding agents: keep it in the repo</div><div class="sd">Put <code class="inline">CLAUDE.md</code> in the project root. Cursor and other agents that look for <code class="inline">AGENTS.md</code> can use that name instead. It is the same file.</div>
{dlrow(dl("/ai/AGENTS.md", "Download AGENTS.md", True))}
  </li>
</ol>
<div class="ready"><span class="plus">+</span><p><b>Ready when:</b> asked "what bullet does LA.IO use, and what are the three pillars?", the tool answers with a plus sign and + Capital, + Coaching, + Connections, in that order. Asked for a one-slide artifact, it embeds the font and inlines the logo rather than linking them.</p></div>'''

TABS = [
    ("connector", "Connector",          TAB_CONNECTOR),
    ("claude",  "Claude Project",       TAB_CLAUDE),
    ("design",  "Claude Design",        TAB_DESIGN),
    ("code",    "Claude Code + Cowork", TAB_CODE),
    ("lovable", "Lovable",              TAB_LOVABLE),
    ("other",   "Other AI",             TAB_OTHER),
]
tabbuttons, panels = [], []
for i, (key, label, body) in enumerate(TABS):
    sel = "true" if i == 0 else "false"
    active = ' data-active="true"' if i == 0 else ""
    tabbuttons.append(f'          <button class="tab" role="tab" aria-selected="{sel}" data-tab="{key}">{label}</button>')
    panels.append(f'''
        <!-- {label.upper()} -->
        <div class="panel" data-tab="{key}"{active} role="tabpanel">
{body}
        </div>''')

SETUP = f'''
  <!-- ============ SETUP TABS ============ -->
  <section class="block">
    <div class="wrap">
      <span class="mono sec-eyebrow">01 &nbsp;Connect your AI</span>
      <h2>Pick how you work.</h2>
      <p class="lead">Six ways in, one kit behind all of them. Set up the ones you use. On claude.ai the connector is the best of them, so start there.</p>
      <p class="lead">The one-line paste is fine for copy and quick questions. For anything visual, use the connector, a Project, Claude Design, Cowork, or Claude Code. Those carry the font with them, so previews come out right.</p>

      <div class="tabs">
        <div class="tablist" role="tablist">
{chr(10).join(tabbuttons)}
        </div>
{"".join(panels)}
      </div>
    </div>
  </section>
'''

# ---- the brand in 30 seconds (unchanged from the original page) ----
SUMMARY = '''
  <!-- ============ BRAND IN 30 SECONDS ============ -->
  <section class="block">
    <div class="wrap">
      <span class="mono sec-eyebrow">02 &nbsp;The brand</span>
      <h2>If you read nothing else.</h2>

      <div class="families">
        <div class="fam"><div class="swatches"><span style="background:#101948"></span><span style="background:#E385FE"></span><span style="background:#F629CB"></span></div><div class="meta"><div class="fname">Magenta</div></div></div>
        <div class="fam"><div class="swatches"><span style="background:#172708"></span><span style="background:#C8ED5D"></span><span style="background:#96F90B"></span></div><div class="meta"><div class="fname">Green</div></div></div>
        <div class="fam"><div class="swatches"><span style="background:#01233C"></span><span style="background:#63DCDE"></span><span style="background:#00B9FE"></span></div><div class="meta"><div class="fname">Blue</div></div></div>
        <div class="fam"><div class="swatches"><span style="background:#302511"></span><span style="background:#F1DC43"></span><span style="background:#F5C124"></span></div><div class="meta"><div class="fname">Orange</div></div></div>
        <div class="fam"><div class="swatches"><span style="background:#231F20"></span><span style="background:#E3E6E7"></span><span style="background:#929497"></span></div><div class="meta"><div class="fname">Gray</div></div></div>
      </div>

      <div class="voice">
        <div class="col never">
          <h4>Never write</h4>
          <ul>
            <li><span class="m">+</span><span>"resilience" or "Silicon Bayou"</span></li>
            <li><span class="m">+</span><span>"innovative solutions", "cutting-edge", "disruptive"</span></li>
            <li><span class="m">+</span><span>"rethink" or "reimagine" Louisiana</span></li>
            <li><span class="m">+</span><span>jazz, Mardi Gras, Bourbon Street, crawfish</span></li>
            <li><span class="m">+</span><span>"it's not X, it's Y" constructions</span></li>
            <li><span class="m">+</span><span>em dashes, anywhere</span></li>
          </ul>
        </div>
        <div class="col always">
          <h4>Always do</h4>
          <ul>
            <li><span class="m">+</span><span>State the case, then stop</span></li>
            <li><span class="m">+</span><span>Lead with fact, not persuasion</span></li>
            <li><span class="m">+</span><span>Use + as the bullet, never a dot or hyphen</span></li>
            <li><span class="m">+</span><span>One color family per piece</span></li>
            <li><span class="m">+</span><span>Aktiv Grotesk, Light or Bold for headlines</span></li>
            <li><span class="m">+</span><span>Angular geometry, generous whitespace</span></li>
          </ul>
        </div>
      </div>

      <div class="pillars">
        <span class="pillar"><span class="m">+</span> Capital</span>
        <span class="pillar"><span class="m">+</span> Coaching</span>
        <span class="pillar"><span class="m">+</span> Connections</span>
      </div>
    </div>
  </section>
'''

ASSETS = f'''
  <!-- ============ THE ASSETS ============ -->
  <section class="block" id="assets">
    <div class="wrap">
      <span class="mono sec-eyebrow">03 &nbsp;The assets</span>
      <h2>Every file, at a permanent URL.</h2>
      <p class="lead">Every file is public, current, and served with open CORS, so it loads on any domain. Copy a URL into code, a prompt, or a tool's knowledge.</p>

      <div class="agroup">
        <div class="ahead"><h3 class="mono">Instructions and docs</h3><span class="anote">Markdown, fetchable, always current.</span></div>
        <div class="urows">
{docrows}        </div>
      </div>

      <div class="agroup">
        <div class="ahead"><h3 class="mono">Type</h3><span class="anote">Embedded CSS for sandboxes, hosted CSS for real sites. JetBrains Mono comes from Google Fonts.</span></div>
        <div class="urows">
{fontrows}        </div>
        <div class="tip"><b>Headlines use Light (300) or Bold (700).</b> Regular (400) for body. Never 500 or 600 as a headline weight. Family name is <code>'Aktiv Grotesk'</code>, never <code>'aktiv-grotesk'</code>. Stack: <code>'Aktiv Grotesk', 'Roboto', system-ui, sans-serif</code>. Roboto only when neither CSS file can load, and say so in the handoff.</div>
      </div>

      <div class="agroup">
        <div class="ahead"><h3 class="mono">Color</h3><span class="anote">Five families. One family per project. Do not mix them.</span></div>
        <div class="urows">
{datarows}        </div>
      </div>

      <div class="agroup">
        <div class="ahead"><h3 class="mono">Logos</h3></div>
        <div class="acards">
{logocards}        </div>
        <div class="tip"><b>Every file ships black (#231F20) on transparent, except the white LED files.</b> Recolor with CSS <code>fill</code>, or inline the SVG and set <code>fill: currentColor</code>. Do not edit the artwork.</div>
        <div class="tip"><b>LED logo.</b> {LED_NOTE}</div>
      </div>

      <div class="agroup">
        <div class="ahead"><h3 class="mono">Motifs</h3><span class="anote">Structural graphics. Same black artwork, recolor to the active family.</span></div>
        <div class="mcards">
{motifcards}        </div>
      </div>
    </div>
  </section>
'''

FOOTER = f'''
  <!-- ============ FOOTER ============ -->
  <footer>
    <div class="wrap">
      <div class="row">
        <div>
          {MARK}
          <div class="descriptor">A Division of Louisiana Economic Development</div>
          <div class="flinks"><a href="/">assets.la.io</a><a href="/llms.txt">llms.txt</a></div>
        </div>
        <div class="sign">
          <div class="made">Maintained by</div>
          <span class="mp-logo">MONDAY <span class="plus">+</span> PARTNERS</span>
          <a href="mailto:dylan@mondayandpartners.com">dylan@mondayandpartners.com</a>
        </div>
      </div>
    </div>
  </footer>

<script>
'''

ai_page = (AI_HEAD
           + _read(PAGE, "page.css") + _read(PAGE, "additions.css")
           + INTRO + HERO + SETUP + SUMMARY + ASSETS + FOOTER
           + _read(PAGE, "rings.js") + "\n" + _read(PAGE, "ui.js") + _read(PAGE, "inventory.js")
           + "</script>\n</body>\n</html>\n")

os.makedirs(AI, exist_ok=True)
open(os.path.join(AI, "index.html"), "w", encoding="utf-8").write(ai_page)
# AGENTS.md is the same file as CLAUDE.md under the name other agents look for.
shutil.copyfile(os.path.join(AI, "CLAUDE.md"), os.path.join(AI, "AGENTS.md"))

# ---------- llms.txt ----------
def _t(path, note):
    return f"- [{path}](https://assets.la.io/{path}): {note}"

llms = "\n".join([
"# assets.la.io",
"",
"> The LA.IO (Louisiana Innovation) brand system, served as public URLs with open CORS.",
"> Fetch what you need. Every file is current and permanent.",
"",
"If you are an AI assistant asked to produce LA.IO work, read ai/CLAUDE.md first. It carries",
"the voice rules, banned language, color families, type rules, and asset URLs. It is short.",
"",
"## Start here",
"",
"The whole kit is also served as an MCP connector at https://assets.la.io/mcp. A Claude",
"organization adds it once and every chat can pull the logo, colors, fonts and voice rules",
"as tools. Setup steps are at https://assets.la.io/ai#connector-admin.",
"",
_t("ai/CLAUDE.md", "Brand instructions for any AI. Read this before generating anything."),
_t("ai/AGENTS.md", "The same file, for tools that look for AGENTS.md."),
"",
"## Docs",
""] + [
_t(p, f"{n}. {d}") for p, n, d in DOCS if p not in ("ai/CLAUDE.md", "ai/AGENTS.md", "llms.txt")
] + [
"",
"## Color",
"",
_t("colors/laio-tokens.json", "All five color families as JSON. Hex, RGB, brand names."),
_t("colors/laio-colors.css", "The same values as CSS custom properties."),
_t("colors/laio-cmyk.json", "CMYK builds for print. GRACoL 2013 coated and SNAP 2007 newsprint, rich blacks, and the out-of-gamut notes."),
_t("colors/LA_IO_COLORS_RGB.ase", "The RGB swatch master for Adobe apps."),
"",
"## Type",
"",
"Aktiv Grotesk, family name 'Aktiv Grotesk' (title case, never 'aktiv-grotesk'). Headlines Light 300 or Bold 700, never a middle weight. Body Regular 400.",
"Three ways to load it, in this order of preference:",
""] + [
_t("fonts/" + f, f"{name}. {desc}") for f, name, desc in FONT_CSS
] + [
"",
"Fallback: Roboto from Google Fonts, only when neither of the above is possible. Say so in the handoff. Roboto is a stand-in, never the goal. Never Roboto inside an artifact; embed instead.",
"font-family stack: 'Aktiv Grotesk', 'Roboto', system-ui, sans-serif",
"",
"The individual woff2 files behind laio-fonts.css:",
""] + [
_t("fonts/" + f, f"Aktiv Grotesk {label}, weight {w}.") for f, label, w in FONTS
] + [
"",
"JetBrains Mono for eyebrows, labels, tags, metadata only. All caps, letter-spacing 0.08 to 0.12em, weights 400/700, always a brand accent color. Google Fonts:",
"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap",
"",
"## Logos",
"",
"All artwork ships black (#231F20) on transparent. Recolor with CSS. Do not edit the artwork.",
""] + [
_t("logos/" + f, desc) for f, name, desc in LOGOS
] + [
"",
"LED logo: " + LED_NOTE,
"",
"## Motifs",
"",
] + [
_t("motifs/" + f, name + " motif.") for f, name in MOTIFS
] + [
"",
"## Pages",
"",
_t("ai", "Brand Kit for AI. Setup for Claude, Claude Design, Claude Code, Cowork, Lovable, and any other AI, plus every asset with a copy button."),
_t("labs", "Louisiana Innovation Labs sub-brand identity assets."),
_t("illustrator", "Generates original illustration in the LA.IO system."),
"",
"## Rules that apply to all LA.IO work",
"",
"- Bullets are always `+`. Never a bullet character, hyphen, or asterisk. In markdown, escape it as `\\+ ` so it renders as a plus instead of becoming a list bullet.",
"- Never use em dashes.",
"- Never write \"resilient\", \"Silicon Bayou\", or \"it's not X, it's Y\".",
"- One color family per project. Do not mix families.",
"- Border radius is 0 on structural elements.",
""])

open(os.path.join(REPO, 'llms.txt'), 'w').write(llms)
open(os.path.join(REPO, 'robots.txt'), 'w').write(
    "User-agent: *\nAllow: /\n\n"
    "# Machine-readable index of the LA.IO brand system\n"
    "# https://assets.la.io/llms.txt\n")

print('ai/index.html + ai/AGENTS.md + llms.txt + robots.txt written')
