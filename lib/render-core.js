// The render engine behind /render. Pure functions so the MCP server and the
// HTTP endpoint agree on every variant.
import { load, recolor, toPng, toPdf } from "./svg.js";
import { logoPath, motifPath, isLed } from "./assets.js";
import { resolve, hexToRgb, cmykFor, FAMILIES } from "./colors.js";
import { buildAse } from "./ase.js";
import { tokens, cmyk } from "./kit.js";

export const MAX_WIDTH = 6000;
export const DEFAULT_PNG_WIDTH = 2000;

export class RenderError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

function groundOf(bg) {
  if (!bg || bg === "transparent") return "dark";
  const c = resolve(bg);
  if (!c) return "dark";
  const [r, g, b] = hexToRgb(c.hex);
  // Rec. 601 luma. Light grounds take the black LED artwork.
  return (0.299 * r + 0.587 * g + 0.114 * b) > 150 ? "light" : "dark";
}

export function resolveArtwork(kind, id, { color, background } = {}) {
  const ground = groundOf(background);
  const rel = kind === "logo" ? logoPath(id, ground) : motifPath(id);
  if (!rel) throw new RenderError(404, `Unknown ${kind} "${id}".`);

  let hex = null;
  let note = null;
  if (color) {
    const c = resolve(color);
    if (!c) throw new RenderError(400, `Unknown color "${color}".`);
    hex = c.hex;
    if (kind === "logo" && isLed(id)) {
      // LED ships white and black only. White stays white on dark grounds;
      // anything else becomes the family dark, which is the rule in the kit.
      if (c.hex !== "#FFFFFF" && c.slot !== "dark") {
        const fam = c.family && tokens()[c.family] ? c.family : "gray";
        hex = tokens()[fam].dark.value.toUpperCase();
        note = `LED is white or black only. Recolored to ${tokens()[fam].dark.name} for a light ground.`;
      }
    }
  } else if (kind === "logo" && isLed(id)) {
    hex = ground === "light" ? null : "#FFFFFF";
  }
  return { rel, hex, ground, note };
}

export function renderAsset(kind, id, format, opts = {}) {
  const { rel, hex, note } = resolveArtwork(kind, id, opts);
  const raw = load(rel);
  if (!raw) throw new RenderError(404, `Artwork missing: ${rel}`);
  const svg = hex ? recolor(raw, hex) : raw;

  if (format === "svg") {
    return { body: Buffer.from(svg, "utf8"), type: "image/svg+xml; charset=utf-8", note };
  }
  if (format === "png") {
    let width = Number(opts.width) || DEFAULT_PNG_WIDTH;
    if (!Number.isFinite(width) || width < 16) width = DEFAULT_PNG_WIDTH;
    width = Math.min(Math.round(width), MAX_WIDTH);
    const bgHex = opts.background && opts.background !== "transparent"
      ? (resolve(opts.background) || {}).hex : null;
    return { body: toPng(svg, { width, background: bgHex || undefined }), type: "image/png", note };
  }
  if (format === "pdf") {
    return {
      body: toPdf(svg, { hex: hex || "#231F20", width: opts.width ? Number(opts.width) : undefined }),
      type: "application/pdf",
      note,
      async: true,
    };
  }
  throw new RenderError(400, `Unsupported format "${format}". Use svg, png or pdf.`);
}

const PROFILE_LABEL = {
  rgb: "RGB",
  coated: "GRACoL 2013 coated",
  newsprint: "SNAP 2007 newsprint",
};

export function renderSwatch(family, profile) {
  if (!PROFILE_LABEL[profile]) {
    throw new RenderError(400, `Unknown profile "${profile}". Use rgb, coated or newsprint.`);
  }
  const fams = family === "all" ? FAMILIES : [family];
  for (const f of fams) if (!tokens()[f]) throw new RenderError(404, `Unknown family "${f}".`);

  const groups = [];
  const missing = [];
  for (const f of fams) {
    const colors = [];
    for (const [slot, entry] of Object.entries(tokens()[f])) {
      if (profile === "rgb") {
        colors.push({ name: entry.name, model: "RGB", values: hexToRgb(entry.value).map((v) => v / 255) });
        continue;
      }
      if (slot === "white") {
        colors.push({ name: entry.name, model: "CMYK", values: [0, 0, 0, 0] });
        continue;
      }
      const c = cmykFor(f, slot, profile);
      if (!c || !c.values) { missing.push(`${f} ${slot}`); continue; }
      colors.push({ name: entry.name, model: "CMYK", values: c.values.map((v) => v / 100) });
      if (profile === "coated" && c.vivid) {
        colors.push({ name: entry.name + " VIVID", model: "CMYK", values: c.vivid.map((v) => v / 100) });
      }
    }
    if (profile !== "rgb") {
      const rb = cmyk().profiles[profile].richBlack;
      colors.push({ name: "LA.IO RICH BLACK", model: "CMYK", values: rb.map((v) => v / 100) });
    }
    if (colors.length) {
      groups.push({ name: `LA.IO ${f[0].toUpperCase() + f.slice(1)} (${PROFILE_LABEL[profile]})`, colors });
    }
  }
  if (!groups.length) throw new RenderError(404, "No swatches available for that combination.");
  return { body: buildAse(groups), type: "application/octet-stream", missing };
}
