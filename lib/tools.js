// Tool bodies for the LA.IO brand connector. Every rule served here is read from
// the kit at request time. Nothing is restated in this file.
import { brief, voice, section, tokens, cmyk, readText, SITE } from "./kit.js";
import { FAMILIES, resolve, hexToRgb, toRec709, cmykFor, fmtCmyk } from "./colors.js";
import { LOGO_VARIANTS, motifNames, isLed, logoPath, renderUrl, cdn } from "./assets.js";
import { load } from "./svg.js";
import { resolveArtwork } from "./render-core.js";

const text = (s) => ({ content: [{ type: "text", text: s }] });
const list = (a) => a.filter(Boolean).join("\n");

export function brandBrief() {
  return text(list([
    brief().trim(),
    "",
    "---",
    "",
    section(voice(), "Standing rules"),
    "",
    "The full voice guide, speaker profiles and ban list: call get_voice.",
    "Assets and download links: call get_logo, get_motif, get_colors, get_fonts, list_assets.",
  ]));
}

const SPEAKER_HEADING = {
  brand: "Brand",
  josh: "Josh Fleig, Chief Innovation Officer",
  susan: "Susan Bourgois, Secretary of Economic Development",
};

export function voiceFor(speaker = "brand") {
  const v = voice();
  const key = String(speaker).toLowerCase();
  const heading = SPEAKER_HEADING[key] || SPEAKER_HEADING.brand;
  return text(list([
    "# LA.IO voice: " + heading,
    "",
    section(v, "Standing rules"),
    "",
    section(v, "Naming"),
    "",
    section(v, heading),
    key === "brand" ? null : "\n" + section(v, "Brand") + "\n\nThe brand voice above is the floor. The speaker profile sits on top of it.",
    "",
    section(v, "Banned, all speakers"),
    "",
    "The short ban list these extend, quoted from the brand instructions:",
    (brief().split("\n").find((l) => /^\+ Never:/.test(l)) || "").trim(),
    "",
    section(v, "The anti-AI rule"),
    "",
    section(v, "Calibration lines"),
  ]));
}

export function colorsFor(family, format = "hex") {
  const t = tokens();
  const fams = !family || family === "all" ? FAMILIES : [String(family).toLowerCase()];
  for (const f of fams) if (!t[f]) return text(`No family called "${family}". The five families are ${FAMILIES.join(", ")}.`);

  const wantAll = format === "all";
  const want = (k) => wantAll || format === k;
  const out = [];

  for (const f of fams) {
    out.push(`## ${f[0].toUpperCase() + f.slice(1)}`);
    for (const [slot, entry] of Object.entries(t[f])) {
      const rgb = hexToRgb(entry.value);
      const bits = [`${entry.name}`];
      if (want("hex") || (!want("rgb") && !want("cmyk-coated") && !want("cmyk-newsprint") && !want("rec709"))) {
        bits.push(entry.value.toUpperCase());
      }
      if (want("rgb")) bits.push(`rgb(${rgb.join(", ")})`);
      if (want("rec709")) bits.push(`Rec.709 legal ${toRec709(rgb).join("/")}`);
      for (const [key, prof] of [["cmyk-coated", "coated"], ["cmyk-newsprint", "newsprint"]]) {
        if (!want(key)) continue;
        const c = cmykFor(f, slot, prof);
        if (slot === "white") { bits.push(`CMYK ${prof} 0/0/0/0`); continue; }
        if (!c?.values) { bits.push(`CMYK ${prof} not built, ask before quoting one`); continue; }
        let s = `CMYK ${prof} ${fmtCmyk(c.values)}`;
        if (c.vivid) s += ` (VIVID ${fmtCmyk(c.vivid)})`;
        if (c.outOfGamut) s += c.pantone ? ` [out of gamut, Pantone ${c.pantone}]` : " [out of gamut]";
        bits.push(s);
      }
      out.push("+ " + bits.join(" · "));
    }
    out.push("");
  }

  const printed = want("cmyk-coated") || want("cmyk-newsprint");
  if (printed) {
    const p = cmyk().profiles;
    out.push("## Print profiles");
    if (want("cmyk-coated")) out.push(`+ Coated: ${p.coated.icc}. Rich black ${fmtCmyk(p.coated.richBlack)}. ${p.coated.use}`);
    if (want("cmyk-newsprint")) out.push(`+ Newsprint: ${p.newsprint.icc}. Rich black ${fmtCmyk(p.newsprint.richBlack)}. ${p.newsprint.use}`);
    out.push("");
    out.push("## Notes");
    for (const n of cmyk().notes) out.push("+ " + n);
    if (want("cmyk-coated")) { out.push(""); out.push("Export: " + cmyk().profiles.coated.export); }
    out.push("");
  }

  out.push("## Swatch files");
  const profs = printed
    ? [["coated", "GRACoL 2013 coated"], ["newsprint", "SNAP 2007 newsprint"]].filter(([k]) => want("cmyk-" + k))
    : [["rgb", "RGB"]];
  for (const f of fams) {
    for (const [pid, plabel] of profs) out.push(`+ ${f} ${plabel}: ${SITE}/render/swatch/${f}-${pid}.ase`);
  }
  out.push(`+ Every family in one file: ${SITE}/render/swatch/all-${profs[0][0]}.ase`);
  out.push("");
  out.push("Body copy is white on dark, or the family dark on light. Never an accent color. One family per piece.");
  return text(out.join("\n"));
}

export function assetList(kind = "all") {
  const k = String(kind).toLowerCase();
  const out = [];
  const logoRules = section(brief(), "Logo & motifs");

  if (k === "all" || k === "logos") {
    out.push("## Logos");
    for (const v of LOGO_VARIANTS) out.push(`+ ${v} · ${cdn(logoPath(v, "dark"))}`);
    out.push("");
    out.push("Usage rules, quoted from the brand instructions:");
    out.push(logoRules);
    out.push("");
    out.push("Any variant in any color, size and format: call get_logo.");
    out.push("");
  }
  if (k === "all" || k === "motifs") {
    out.push("## Motifs");
    out.push(motifNames().map((n) => "+ " + n).join("\n"));
    out.push("");
    out.push("Recolored motifs in any format: call get_motif.");
    out.push("");
  }
  if (k === "all" || k === "fonts") {
    out.push("## Fonts");
    out.push("+ Aktiv Grotesk. Headlines Light 300 or Bold 700, body Regular 400. Never a middle weight as a headline.");
    out.push("+ JetBrains Mono. Eyebrows, labels, tags and metadata only. All caps, always a brand accent color.");
    out.push("Loading instructions for your situation: call get_fonts.");
    out.push("");
  }
  if (k === "all" || k === "video") {
    out.push("## Video");
    out.push("+ Alpha logo renders: get_logo with format png and no background gives a transparent file at any size.");
    out.push("+ Color values for grading: get_colors with format rec709.");
    out.push("+ Fonts for Resolve, After Effects and Premiere: get_fonts with context video.");
    out.push("+ The shared video library (intros, outros, lower thirds, sound beds) is not in the connector yet.");
    out.push("");
  }
  return text(out.join("\n"));
}

function lockupNote(variant, width) {
  const w = Number(width);
  if (["louisiana-innovation-a", "louisiana-innovation-b", "division-line"].includes(variant)) {
    return "This is a secondary mark. It sits under or beside the primary mark, never alone on a page.";
  }
  if (variant === "complete" && w && w < 120) {
    return "Under about 120px the LOUISIANA INNOVATION subtext stops being legible. base is the lockup for that size.";
  }
  if (variant === "base" && w && w >= 400) {
    return "base is for small sizes. At this width complete is the default lockup.";
  }
  if (variant === "horz") return "horz belongs in a header or nav bar. Everywhere else, complete is the default.";
  return null;
}

export function logoFor({ variant = "complete", color, format = "png", width, background } = {}) {
  const v = String(variant).toLowerCase();
  if (!LOGO_VARIANTS.includes(v)) {
    return text(`No lockup called "${variant}". Available: ${LOGO_VARIANTS.join(", ")}.`);
  }
  const fmt = String(format).toLowerCase();
  if (!["svg", "png", "pdf"].includes(fmt)) return text(`Format must be svg, png or pdf.`);

  // Never refuse. A color that is not in the kit gets named, then the closest
  // thing that does exist comes back anyway.
  let useColor = color;
  let colorNote = null;
  if (color && !resolve(color)) {
    useColor = undefined;
    colorNote = isLed(v)
      ? `LED's ${color} mark belongs to LED's own communications. In LA.IO work the mark is white or black. Here is white, the default on dark grounds. Black for light grounds is below. If LED's team has asked for their own version, that request goes to them, not through this kit.`
      : `"${color}" is not an LA.IO color, so this is the default artwork. The five families are magenta, green, blue, orange and gray, each with a dark, an easy and an electric. Name one and it comes back in that color.`;
  }

  let info;
  try { info = resolveArtwork("logo", v, { color: useColor, background }); }
  catch (e) { return text(e.message); }

  const w = fmt === "png" ? Number(width) || 2000 : width ? Number(width) : undefined;
  const url = renderUrl("logo", v, fmt, { color: useColor, width: w, background });

  const out = [`${v} · ${fmt.toUpperCase()}${w ? ` · ${w}px wide` : ""}`, url, ""];
  if (colorNote) { out.push(colorNote); out.push(""); }
  if (colorNote && isLed(v)) {
    out.push(`Black LED, for light grounds: ${renderUrl("logo", v, fmt, { color: "black", width: w })}`);
    out.push("");
  }
  if (fmt === "png") out.push(background && background !== "transparent"
    ? `Background: ${background}.`
    : "Transparent background.");
  if (info.note) out.push(info.note);
  const ln = lockupNote(v, w);
  if (ln) out.push(ln);
  if (isLed(v)) out.push("LED sits under or beside the LA.IO mark, never above it, never as the only logo on a page.");
  out.push("");
  out.push("Other formats of the same file:");
  for (const f of ["svg", "png", "pdf"]) {
    if (f === fmt) continue;
    out.push(`+ ${f}: ${renderUrl("logo", v, f, { color: useColor, width: f === "png" ? w || 2000 : undefined, background })}`);
  }

  if (fmt === "svg") {
    const raw = load(info.rel);
    if (raw) {
      out.push("");
      out.push("Inline markup, for anything sandboxed. Paste this in place of an <img> tag:");
      out.push("");
      out.push(info.hex ? raw.replace(/fill\s*:\s*#[0-9a-fA-F]{3,6}/g, "fill:" + info.hex) : raw);
    }
  }
  out.push("");
  out.push("Anything here can be overruled. Say the word and you get the file you asked for.");
  return text(out.join("\n"));
}

export function motifFor({ name, color, format = "svg", size } = {}) {
  const names = motifNames();
  const n = String(name || "").toLowerCase().replace(/^laio-/, "");
  if (!names.includes(n)) return text(`No motif called "${name}". Available: ${names.join(", ")}.`);
  const fmt = String(format).toLowerCase();
  if (!["svg", "png", "pdf"].includes(fmt)) return text("Format must be svg, png or pdf.");
  let useColor = color;
  let colorNote = null;
  if (color && !resolve(color)) {
    useColor = undefined;
    colorNote = `"${color}" is not an LA.IO color, so this is the default artwork. Name a family color and it comes back in that color.`;
  }
  const w = fmt === "png" ? Number(size) || 1000 : size ? Number(size) : undefined;
  const url = renderUrl("motif", n, fmt, { color: useColor, width: w });
  const out = [`${n} · ${fmt.toUpperCase()}${w ? ` · ${w}px` : ""}`, url, ""];
  if (colorNote) { out.push(colorNote); out.push(""); }
  out.push("Shape grammar: every shape comes from the logo's bracket, at 0, 45 or 90 degrees. Two shapes per composition.");
  out.push("");
  for (const f of ["svg", "png", "pdf"]) {
    if (f === fmt) continue;
    out.push(`+ ${f}: ${renderUrl("motif", n, f, { color: useColor, width: f === "png" ? w || 1000 : undefined })}`);
  }
  if (fmt === "svg") {
    const rel = "motifs/LAIO-" + n.toUpperCase() + ".svg";
    const raw = load(rel);
    const c = useColor ? resolve(useColor) : null;
    if (raw) {
      out.push("");
      out.push("Inline markup:");
      out.push("");
      out.push(c ? raw.replace(/fill\s*:\s*#[0-9a-fA-F]{3,6}/g, "fill:" + c.hex) : raw);
    }
  }
  return text(out.join("\n"));
}

const FONT_STACK = "'Aktiv Grotesk', 'Roboto', system-ui, sans-serif";
const JETBRAINS = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap";

export function fontsFor(context = "artifact") {
  const c = String(context).toLowerCase();
  const rules = section(brief(), "Type");
  const head = ["# Aktiv Grotesk: " + c, ""];
  const tail = ["", "## The type rules, quoted from the brand instructions", rules];

  if (c === "web") {
    return text(list([...head,
      `Hosted stylesheet, for a real site or app on a domain. Never inside an artifact or a preview.`,
      "",
      `    <link rel="stylesheet" href="${SITE}/fonts/laio-fonts.css">`,
      `    font-family: ${FONT_STACK};`,
      "",
      `JetBrains Mono for eyebrows and labels: ${JETBRAINS}`,
      ...tail]));
  }
  if (c === "desktop" || c === "video") {
    return text(list([...head,
      `Licensed desktop font files, all nine weights as TTF: ${SITE}/fonts/desktop/AktivGrotesk-Desktop.zip`,
      "",
      "Install on Mac: unzip, select every .ttf, double-click, then Install Font. Or drop them into ~/Library/Fonts.",
      "Install on Windows: unzip, select every .ttf, right-click, then Install for all users.",
      "Quit and reopen the app after installing.",
      "",
      c === "video"
        ? list([
            "After Effects and Premiere:",
            "+ Install the fonts before opening the project, or text layers fall back and reflow.",
            "+ Collect the project with Reduce Project and hand the fonts to anyone opening it. Adobe does not embed them.",
            "+ Resolve reads system fonts, so the same install covers it. Restart Resolve after installing.",
            "+ Grading values: call get_colors with format rec709.",
          ])
        : "The license covers the team. Do not repost the zip outside LA.IO.",
      ...tail]));
  }
  if (c === "office") {
    return text(list([...head,
      "Read this before you build a PowerPoint, Word or Google file.",
      "",
      "+ A PowerPoint or Word file renders Aktiv Grotesk only if the person opening it has the font installed. Do not try to embed it in a PPTX. It does not travel.",
      "+ Google Slides and Google Docs cannot use Aktiv Grotesk at all. There is no upload path.",
      "",
      "What to do:",
      `+ Staying inside the team: install the desktop fonts first. ${SITE}/fonts/desktop/AktivGrotesk-Desktop.zip`,
      "+ Going to anyone outside the team as an Office file: set the type in Roboto, or Arial if Roboto is not installed.",
      "+ Working in Google Workspace: use Roboto. It is the closest thing Google has.",
      "+ Going out as a PDF: use Aktiv Grotesk. The PDF carries the font with it.",
      "",
      "Say which fallback you used in the handoff. Roboto is a stand-in, never the goal.",
      ...tail]));
  }
  return text(list([...head,
    "Sandboxed output has no network. A claude.ai artifact, a Claude Design canvas, a Lovable preview and an email all fail to reach assets.la.io.",
    "",
    `Fetch ${SITE}/fonts/laio-fonts-inline.css and paste the whole file into a <style> tag. It is about 150KB of @font-face rules with data: URIs, so the type works with zero network requests.`,
    "",
    `    font-family: ${FONT_STACK};`,
    "",
    "In the same file, paste every logo as inline <svg> markup. Call get_logo with format svg to get it.",
    "Never <link> a stylesheet, never <img src>, never background-image a URL, never load Roboto from Google.",
    "",
    `JetBrains Mono is the one exception when the target allows a network request: ${JETBRAINS}`,
    ...tail]));
}
