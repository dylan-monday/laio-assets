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
 ("Brand Assets for AI","/ai",False,"The core brand system as fetchable URLs. Fonts, color, logos, motifs, and drop-in instructions for any AI or build tool."),
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

# ---------- /ai — brand assets for AI ----------
PROMPT = ("Fetch https://assets.la.io/claude/CLAUDE.md and follow it as the "
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

DATA = [
    ("colors/laio-tokens.json", "All five color families as JSON. Hex, RGB, and the brand name for each."),
    ("colors/laio-colors.css",  "The same values as CSS custom properties. Link it or paste it."),
]

LOGOS = [
    ("LAIO-COMPLETE.svg",           "Complete lockup",        "Primary mark. Use this unless there is a reason not to."),
    ("LAIO-BASE.svg",               "Base mark",              "The LA.IO mark alone."),
    ("LAIO-HORZ.svg",               "Horizontal lockup",      "For wide spaces and headers."),
    ("LOUISIANA-INNOVATION-A.svg",  "Louisiana Innovation A", "Full name lockup, stacked."),
    ("LOUISIANA-INNOVATION-B.svg",  "Louisiana Innovation B", "Full name lockup, condensed."),
    ("DIVISION-LINE.svg",           "Division line",          "The LED division line. Sits under the mark."),
]

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
]

DOCS = [
    ("claude/CLAUDE.md",                 "Drop-in instructions",  "Voice, banned language, color, type, and asset URLs. The one file to hand an AI."),
    ("claude/laio-brand/BRAND.md",       "Full brand system",     "The long form. Load when the work needs depth."),
    ("claude/laio-brand/COMPONENTS.md",  "Component code",        "Buttons, cards, eyebrows, and layout patterns as code."),
    ("claude/laio-brand.zip",            "Packaged skill",        "The whole kit as a Claude skill. Unzip into .claude/skills/."),
    ("llms.txt",                         "Machine-readable index","A plain list of everything above. Point a crawler or an agent at this."),
]

def urlrow(path, name, desc):
    url = "https://assets.la.io/" + path
    return f'''<div class="urow">
  <span class="uplus">+</span>
  <div class="ubody">
    <div class="uname">{name}</div>
    <div class="udesc">{desc}</div>
  </div>
  <button class="ucopy mono" data-copy="{url}"><span class="upath">/{path}</span><span class="uci">COPY</span></button>
</div>'''

fontrows = "".join(
    urlrow("fonts/" + f, f"{label} <span class=\"uw mono\">{w}</span>",
           "woff2. Self-hosted, open CORS.")
    for f, label, w in FONTS)

datarows = "".join(urlrow(p, p.split("/")[-1], d) for p, d in DATA)

logorows = "".join(f'''<div class="acard">
  <div class="astage"><img src="/logos/{f}" alt="{name}" loading="lazy"></div>
  <div class="aname">{name}</div>
  <div class="adesc">{desc}</div>
  <button class="ucopy mono" data-copy="https://assets.la.io/logos/{f}"><span class="upath">/logos/{f}</span><span class="uci">COPY</span></button>
</div>''' for f, name, desc in LOGOS)

motifrows = "".join(f'''<div class="mcard">
  <div class="mstage"><img src="/motifs/{f}" alt="{name}" loading="lazy"></div>
  <div class="mname">{name}</div>
  <button class="ucopy mono" data-copy="https://assets.la.io/motifs/{f}"><span class="upath">/motifs/{f}</span><span class="uci">COPY</span></button>
</div>''' for f, name in MOTIFS)

docrows = "".join(urlrow(p, n, d) for p, n, d in DOCS)

AI_CSS = CSS + '''
header{padding:80px 0 0}
.eyebrow{font-size:11.5px;color:var(--electric);margin:0 0 26px;letter-spacing:.16em;font-weight:700}
h1{font-weight:300;font-size:clamp(34px,5.2vw,58px);line-height:1.04;margin:0;letter-spacing:-.02em}
h1 b{font-weight:700;display:block}
.lede{margin:24px 0 0;max-width:52ch;font-size:17px;line-height:1.5;color:var(--body)}

.step{padding:66px 0 0}
.shead{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;
  border-bottom:1px solid var(--rule-soft);padding-bottom:14px;margin-bottom:26px}
.snum{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;
  color:rgba(255,255,255,.34)}
h2{font-size:13px;color:var(--electric);margin:0;font-weight:700;
  font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:.1em}
.snote{font-size:14.5px;color:var(--body);margin-left:auto;max-width:40ch}
@media(max-width:760px){.snote{margin-left:0;flex-basis:100%}}

.prompt{border:1px solid var(--electric);background:rgba(0,185,254,.06)}
.plabel{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.12em;
  color:var(--easy);padding:15px 20px 0;text-transform:uppercase}
.ptext{padding:11px 20px 20px;font-size:clamp(15px,2vw,19px);line-height:1.45;
  font-family:'JetBrains Mono',monospace;color:#fff;word-break:break-word;letter-spacing:0}
.pbtn{display:block;width:100%;text-align:left;background:var(--electric);color:var(--dark);
  border:0;padding:14px 20px;cursor:pointer;font-family:'JetBrains Mono',monospace;
  font-size:11px;letter-spacing:.12em;font-weight:700;text-transform:uppercase;transition:.15s}
.pbtn:hover{background:var(--easy)}

.ways{margin:26px 0 0;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:860px){.ways{grid-template-columns:1fr}}
.way{border:1px solid var(--rule-soft);padding:20px}
.wlabel{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.1em;
  color:var(--easy);text-transform:uppercase;margin-bottom:10px}
.way p{margin:0;font-size:14.5px;line-height:1.5;color:var(--body)}
.way a{color:var(--electric);text-decoration:none;border-bottom:1px solid rgba(0,185,254,.35)}
.way a:hover{border-bottom-color:var(--electric)}

.urow{display:grid;grid-template-columns:20px minmax(0,1fr) auto;gap:4px 6px;
  align-items:center;padding:15px 0;border-bottom:1px solid var(--rule-soft)}
.urow:first-child{border-top:1px solid var(--rule-soft)}
.uplus{color:var(--electric);font-size:16px;line-height:1}
.uname{font-size:16px;font-weight:400}
.uw{font-size:10px;color:rgba(255,255,255,.36);padding-left:7px}
.udesc{font-size:13.5px;color:var(--body);margin-top:3px;line-height:1.45}
.ubody{min-width:0}
.ucopy{display:flex;align-items:center;gap:12px;justify-content:space-between;
  background:transparent;border:1px solid var(--rule);color:rgba(255,255,255,.55);
  padding:9px 12px;cursor:pointer;font-family:'JetBrains Mono',monospace;
  font-size:9.5px;letter-spacing:.04em;text-transform:none;transition:.15s;white-space:nowrap}
.ucopy:hover{color:var(--dark);background:var(--electric);border-color:var(--electric)}
.uci{letter-spacing:.1em;color:var(--easy);font-weight:700}
.ucopy:hover .uci{color:var(--dark)}
.ucopy.done{background:var(--easy);border-color:var(--easy);color:var(--dark)}
.ucopy.done .uci{color:var(--dark)}
@media(max-width:760px){
  .urow{grid-template-columns:20px minmax(0,1fr);grid-template-areas:"p b" ". c"}
  .uplus{grid-area:p} .ubody{grid-area:b} .ucopy{grid-area:c;margin-top:9px;width:100%}
}

.acards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:860px){.acards{grid-template-columns:1fr}}
.acard{border:1px solid var(--rule-soft)}
.astage{background:#fff;height:150px;display:flex;align-items:center;justify-content:center;padding:26px}
.astage img{max-width:100%;max-height:100%}
.aname{font-size:15px;padding:15px 15px 0}
.adesc{font-size:13px;color:var(--body);padding:5px 15px 13px;line-height:1.45}
.acard .ucopy{width:100%;border:0;border-top:1px solid var(--rule-soft)}

.mcards{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
@media(max-width:980px){.mcards{grid-template-columns:repeat(3,1fr)}}
@media(max-width:600px){.mcards{grid-template-columns:repeat(2,1fr)}}
.mcard{border:1px solid var(--rule-soft)}
.mstage{background:#fff;height:96px;display:flex;align-items:center;justify-content:center;padding:24px}
.mstage img{max-width:100%;max-height:100%}
.mname{font-size:13px;padding:11px 12px 9px}
.mcard .ucopy{width:100%;border:0;border-top:1px solid var(--rule-soft);font-size:9px;padding:8px 10px}

.tip{margin:24px 0 0;padding:16px 18px;border-left:2px solid var(--easy);
  background:rgba(99,220,222,.05);font-size:14px;line-height:1.55;color:var(--body)}
.tip b{color:#fff;font-weight:400}
.tip code{font-family:'JetBrains Mono',monospace;font-size:12.5px;color:var(--easy)}
footer{margin:96px 0 0;padding:26px 0 60px;border-top:1px solid var(--rule-soft);
  font-size:11px;color:rgba(255,255,255,.34);letter-spacing:.1em;
  display:flex;gap:18px;flex-wrap:wrap}
footer a{color:var(--easy);text-decoration:none}
footer a:hover{color:var(--electric)}
'''

ai = f'''<!doctype html>
<html lang="en"><head>{HEAD}
<title>Brand Assets for AI — assets.la.io</title>
<meta name="description" content="The LA.IO brand system as URLs an AI can fetch. Instructions, fonts, colors, logos, and motifs.">
<style>{AI_CSS}</style></head>
<body><div class="wrap">

<header>
{LOGO}
<p class="eyebrow mono">Brand Assets for AI</p>
<h1>Point your AI<b>at these URLs.</b></h1>
<p class="lede">Every core LA.IO asset lives at a permanent, public URL. Any AI, tool, or
site that can fetch a URL can pull the real fonts, colors, logos, and rules. No downloads,
no attachments, no stale copies.</p>
</header>

<section class="step">
  <div class="shead"><span class="snum">01</span><h2>Start here</h2>
  <span class="snote">Works in Claude, ChatGPT, Lovable, Cursor, or anything else that can read a link.</span></div>
  <div class="prompt">
    <div class="plabel">Paste this into your AI</div>
    <div class="ptext">{PROMPT}</div>
    <button class="pbtn" data-copy="{PROMPT}">Copy the instruction</button>
  </div>
  <div class="tip"><b>That one file carries the whole system.</b> Voice rules, banned
  language, the five color families, type rules, and every asset URL on this page. One
  fetch and the AI is on brand.</div>
</section>

<section class="step">
  <div class="shead"><span class="snum">02</span><h2>Three ways to use it</h2></div>
  <div class="ways">
    <div class="way">
      <div class="wlabel">Any AI chat</div>
      <p>Paste the line above. The AI fetches the file and works to the brand from there.</p>
    </div>
    <div class="way">
      <div class="wlabel">Claude project or Claude Code</div>
      <p>Install the packaged skill instead. Setup steps are at
      <a href="/claude">assets.la.io/claude</a>.</p>
    </div>
    <div class="way">
      <div class="wlabel">Lovable, Framer, a web build</div>
      <p>Use the raw URLs below directly in code. Every file is served with open CORS,
      so it loads on any domain.</p>
    </div>
  </div>
</section>

<section class="step">
  <div class="shead"><span class="snum">03</span><h2>Instructions and docs</h2>
  <span class="snote">Markdown, fetchable, always current.</span></div>
  {docrows}
</section>

<section class="step">
  <div class="shead"><span class="snum">04</span><h2>Type</h2>
  <span class="snote">Aktiv Grotesk, self-hosted. JetBrains Mono comes from Google Fonts.</span></div>
  {fontrows}
  <div class="tip"><b>Headlines use Light (300) or Bold (700).</b> Regular (400) for body.
  Never 500 or 600 as a headline weight.</div>
</section>

<section class="step">
  <div class="shead"><span class="snum">05</span><h2>Color</h2>
  <span class="snote">Five families. One family per project. Do not mix them.</span></div>
  {datarows}
</section>

<section class="step">
  <div class="shead"><span class="snum">06</span><h2>Logos</h2></div>
  <div class="acards">{logorows}</div>
  <div class="tip"><b>Every file ships black (#231F20) on transparent.</b> Recolor with
  CSS <code>fill</code> or inline the SVG and set <code>fill:currentColor</code>. Do not
  edit the artwork.</div>
</section>

<section class="step">
  <div class="shead"><span class="snum">07</span><h2>Motifs</h2>
  <span class="snote">Structural graphics. Same black artwork, recolor to the active family.</span></div>
  <div class="mcards">{motifrows}</div>
</section>

<footer>
  <span class="mono">assets.la.io</span>
  <a class="mono" href="/">All tools</a>
  <a class="mono" href="/llms.txt">llms.txt</a>
  <a class="mono" href="/claude">Claude kit</a>
</footer>

</div>
<script>
document.addEventListener('click',function(e){{
  var b=e.target.closest('[data-copy]'); if(!b) return;
  navigator.clipboard.writeText(b.getAttribute('data-copy'));
  var t=b.querySelector('.uci'), o;
  if(t){{o=t.textContent;t.textContent='COPIED';b.classList.add('done');
    setTimeout(function(){{t.textContent=o;b.classList.remove('done')}},1200);}}
  else {{o=b.textContent;b.textContent='Copied';
    setTimeout(function(){{b.textContent=o}},1200);}}
}});
</script>
</body></html>'''

os.makedirs(os.path.join(REPO, 'ai'), exist_ok=True)
open(os.path.join(REPO, 'ai', 'index.html'), 'w').write(ai)

# ---------- llms.txt ----------
def _t(path, note):
    return f"- [{path}](https://assets.la.io/{path}): {note}"

llms = "\n".join([
"# assets.la.io",
"",
"> The LA.IO (Louisiana Innovation) brand system, served as public URLs with open CORS.",
"> Fetch what you need. Every file is current and permanent.",
"",
"If you are an AI assistant asked to produce LA.IO work, read CLAUDE.md first. It carries",
"the voice rules, banned language, color families, type rules, and asset URLs. It is short.",
"",
"## Start here",
"",
_t("claude/CLAUDE.md", "Drop-in brand instructions. Read this before generating anything."),
"",
"## Depth",
"",
_t("claude/laio-brand/BRAND.md", "The full brand system."),
_t("claude/laio-brand/COMPONENTS.md", "Component patterns as code."),
_t("claude/laio-brand.zip", "The whole kit packaged as a Claude skill."),
"",
"## Color",
"",
_t("colors/laio-tokens.json", "All five color families as JSON. Hex, RGB, brand names."),
_t("colors/laio-colors.css", "The same values as CSS custom properties."),
"",
"## Type",
"",
"Aktiv Grotesk, self-hosted woff2. Light (300) or Bold (700) for headlines, Regular (400) for body.",
""] + [
_t("fonts/" + f, f"Aktiv Grotesk {label}, weight {w}.") for f, label, w in FONTS
] + [
"",
"JetBrains Mono for eyebrows, labels, and metadata only. Always caps. Load from Google Fonts:",
"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap",
"",
"## Logos",
"",
"All artwork ships black (#231F20) on transparent. Recolor with CSS. Do not edit the artwork.",
""] + [
_t("logos/" + f, desc) for f, name, desc in LOGOS
] + [
"",
"## Motifs",
"",
] + [
_t("motifs/" + f, name + " motif.") for f, name in MOTIFS
] + [
"",
"## Pages",
"",
_t("ai", "Human-readable version of this file, with previews and copy buttons."),
_t("claude", "Setup steps for Claude projects and Claude Code."),
_t("labs", "Louisiana Innovation Labs sub-brand identity assets."),
_t("illustrator", "Generates original illustration in the LA.IO system."),
"",
"## Rules that apply to all LA.IO work",
"",
"- Bullets are always `+`. Never a bullet character, hyphen, or asterisk.",
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

print('ai + llms.txt + robots.txt written')
