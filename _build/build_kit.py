import os,re,shutil,subprocess,json,tempfile
import cairosvg
import sys, argparse
_p=argparse.ArgumentParser(description="Build the Louisiana Innovation Labs logo kit.")
_p.add_argument("source", help="Folder holding the LILabs-*.svg master art")
_p.add_argument("-o","--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"logos","labs"),
                help="Output folder (default: <repo>/logos/labs)")
_a=_p.parse_args()
SRC=_a.source
OUT=_a.out
RECOLOR={"#42b4e7":"#00B9FE","#03243c":"#01233C"}
# lockup type -> (source stem, output stem)
LOCKUPS=[
 ("Primary",        "LILabs-Primary",        "LILabs-Primary"),
 ("Primary-Reverse","LILabs-Reverse",        "LILabs-Primary-Reverse"),
 ("Stacked",        "LILabs-Stacked",        "LILabs-Stacked"),
 ("Stacked-Reverse","LILabs-Stacked-Reverse","LILabs-Stacked-Reverse"),
 ("LABS",           "LILabs-LABS",           "LILabs-LABS"),
 ("Icon",           "LILabs-Icon",           "LILabs-Icon"),
 ("Icon-Reverse",   "LILabs-Icon-Reverse",   "LILabs-Icon-Reverse"),
]
VARIANTS=["Color","White","Black"]
# source suffix overrides (the White_1 bug)
OVERRIDE={("LILabs-Reverse","Black"):"LILabs-Reverse-White_1"}

def srcfile(sstem,var):
    o=OVERRIDE.get((sstem,var))
    return os.path.join(SRC,(o or f"{sstem}-{var}")+".svg")

for d in ["svg","eps","png"]:
    os.makedirs(os.path.join(OUT,d),exist_ok=True)

manifest=[]
for typ,sstem,ostem in LOCKUPS:
    for var in VARIANTS:
        sp=srcfile(sstem,var)
        assert os.path.exists(sp), sp
        s=open(sp,encoding="utf-8").read()
        for a,b in RECOLOR.items():
            s=re.sub(a,b,s,flags=re.I)
        # strip Illustrator layer ids/comments, tidy
        s=re.sub(r'\s*<!--.*?-->','',s,flags=re.S)
        s=s.replace(' id="Layer_2" data-name="Layer 2"','').replace(' id="Layer_3" data-name="Layer 3"','')
        s=s.replace(' id="Layer_1" data-name="Layer 1"','')
        name=f"{ostem}-{var}"
        svgp=os.path.join(OUT,"svg",name+".svg")
        open(svgp,"w",encoding="utf-8").write(s)
        vb=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',s)
        w,h=float(vb.group(1)),float(vb.group(2))
        # PNG renditions
        base=round(w)
        for label,px in [("1x",base),("2x",base*2),("3x",base*3),("3000",3000)]:
            cairosvg.svg2png(url=svgp,write_to=os.path.join(OUT,"png",f"{name}@{label}.png"),
                             output_width=px,output_height=round(px*h/w),background_color=None)
        # EPS via pdf -> gs eps2write, CMYK
        pdfp=os.path.join(tempfile.gettempdir(),f"{name}.pdf")
        cairosvg.svg2pdf(url=svgp,write_to=pdfp)
        epsp=os.path.join(OUT,"eps",name+".eps")
        pw,ph=w*0.75,h*0.75
        subprocess.run(["gs","-q","-dNOPAUSE","-dBATCH","-dSAFER","-sDEVICE=eps2write",
                        "-dNOCACHE","-dFIXEDMEDIA",
                        f"-dDEVICEWIDTHPOINTS={pw:.4f}",f"-dDEVICEHEIGHTPOINTS={ph:.4f}",
                        "-sColorConversionStrategy=CMYK","-dProcessColorModel=/DeviceCMYK",
                        f"-sOutputFile={epsp}",pdfp],check=True)
        manifest.append({"type":typ,"variant":var,"name":name,"w":w,"h":h})
json.dump(manifest,open(os.path.join(OUT,"manifest.json"),"w"),indent=1)
print(len(manifest),"variants built")

# ---- download-all zip, organized by lockup type ----
ZPARENT=tempfile.mkdtemp()
ZROOT=os.path.join(ZPARENT,"LILabs-Logos")
for e in manifest:
    t,n=e["type"],e["name"]
    for sub,ext in (("SVG",".svg"),("EPS",".eps")):
        d=os.path.join(ZROOT,t,sub); os.makedirs(d,exist_ok=True)
        shutil.copy(os.path.join(OUT,sub.lower(),n+ext),d)
    d=os.path.join(ZROOT,t,"PNG"); os.makedirs(d,exist_ok=True)
    for lab in ("1x","2x","3x","3000"):
        shutil.copy(os.path.join(OUT,"png",f"{n}@{lab}.png"),d)
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"kit-README.txt"),
            os.path.join(ZROOT,"READ-ME.txt"))
zbase=os.path.join(OUT,"LILabs-Logos")
if os.path.exists(zbase+".zip"): os.remove(zbase+".zip")
shutil.make_archive(zbase,"zip",ZPARENT,"LILabs-Logos")
shutil.rmtree(ZPARENT)
print("zip:",zbase+".zip",round(os.path.getsize(zbase+".zip")/1e6,1),"MB")
