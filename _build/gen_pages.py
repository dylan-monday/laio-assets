#!/usr/bin/env python3
"""Regenerate index.html, 404.html and labs/index.html.

    python3 _build/gen_pages.py

Reads logos/labs/manifest.json (written by build_kit.py) for lockup
dimensions, so run build_kit.py first if the master art changed.
"""
import json, datetime, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSS  = open(os.path.join(HERE, "shared.css")).read()
LOGO = open(os.path.join(HERE, "laio-complete.inline.svg")).read().strip()
M    = json.load(open(os.path.join(REPO, "logos", "labs", "manifest.json")))
BASE="/logos/labs"
ABS="https://assets.la.io/logos/labs"
PANEL=65.3  # LABS panel box width in source units

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
<title>Louisiana Innovation Labs — Identity Assets</title>
<meta name="description" content="Logo files and color values for the Louisiana Innovation Labs identity.">
<link rel="icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
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
  <p class="fmeta">LAST UPDATED {updated.upper()}</p>
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
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">'''

ENTRIES=[
 ("Illustration Machine","/illustrator",False,"Generates original illustration and background graphics in the LA.IO system."),
 ("Badge Builder","https://badgebuilder.la.io",True,"Builds embeddable, trackable LA.IO badges for partner sites."),
 ("Claude Design System","/claude",False,"Instructions for building LA.IO work in Claude."),
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

ROOT_CSS=f'''{CSS}
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
<body><div class="wrap">
{LOGO}
<p class="lede">Brand assets, tools, and documentation for LA.IO and the Louisiana Innovation ecosystem.</p>
<nav class="rows">{rows}</nav>
</div></body></html>'''
open(os.path.join(REPO,'index.html'),'w').write(index)

nf=f'''<!doctype html>
<html lang="en"><head>{HEAD}
<title>404 — assets.la.io</title>
<meta name="robots" content="noindex">
<style>{CSS}
body{{min-height:100vh;display:flex;align-items:center}}
.wrap{{width:100%;max-width:880px}}
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
</div></body></html>'''
open(os.path.join(REPO,'404.html'),'w').write(nf)
print('index + 404 written')
