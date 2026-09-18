// SVG handling: read, recolor, measure, rasterize, and convert to vector PDF.
// The artwork itself is never edited on disk. Every variant is produced here.
import { Resvg } from "@resvg/resvg-js";
import { PDFDocument, rgb } from "pdf-lib";
import { readText, exists } from "./kit.js";
import { hexToRgb } from "./colors.js";

const FILL_STYLE = /fill\s*:\s*#[0-9a-fA-F]{3,6}/g;
const FILL_ATTR  = /fill\s*=\s*"#[0-9a-fA-F]{3,6}"/g;

export function load(rel) {
  if (!exists(rel)) return null;
  return readText(rel);
}

export function recolor(svg, hex) {
  if (!hex) return svg;
  const c = hex.toUpperCase();
  let out = svg;
  let touched = false;
  if (FILL_STYLE.test(out)) { out = out.replace(FILL_STYLE, "fill:" + c); touched = true; }
  FILL_STYLE.lastIndex = 0;
  if (FILL_ATTR.test(out)) { out = out.replace(FILL_ATTR, 'fill="' + c + '"'); touched = true; }
  FILL_ATTR.lastIndex = 0;
  if (!touched) out = out.replace(/<svg\b/, '<svg fill="' + c + '"');
  return out;
}

export function dimensions(svg) {
  const vb = svg.match(/viewBox\s*=\s*"([^"]+)"/);
  if (vb) {
    const p = vb[1].trim().split(/[\s,]+/).map(Number);
    if (p.length === 4 && p[2] > 0 && p[3] > 0) return { width: p[2], height: p[3], minX: p[0], minY: p[1] };
  }
  const w = Number((svg.match(/\swidth\s*=\s*"([\d.]+)/) || [])[1]);
  const h = Number((svg.match(/\sheight\s*=\s*"([\d.]+)/) || [])[1]);
  if (w && h) return { width: w, height: h, minX: 0, minY: 0 };
  return { width: 1000, height: 1000, minX: 0, minY: 0 };
}

export function toPng(svg, { width, background } = {}) {
  const opts = { font: { loadSystemFonts: false } };
  if (width) opts.fitTo = { mode: "width", value: Math.round(width) };
  if (background) opts.background = background;
  return new Resvg(svg, opts).render().asPng();
}

// Vector PDF. The marks are outlined artwork in one color, so every shape is
// drawn with the same fill. Paths and polygons cover every file in the kit.
export async function toPdf(svg, { hex = "#231F20", width } = {}) {
  const dim = dimensions(svg);
  const scale = width ? width / dim.width : 1;
  const pageW = dim.width * scale;
  const pageH = dim.height * scale;

  const doc = await PDFDocument.create();
  doc.setTitle("LA.IO brand asset");
  doc.setProducer("assets.la.io");
  const page = doc.addPage([pageW, pageH]);
  const [r, g, b] = hexToRgb(hex).map((v) => v / 255);
  const color = rgb(r, g, b);

  const shapes = [];
  for (const m of svg.matchAll(/<path\b[^>]*\bd\s*=\s*"([^"]+)"/g)) shapes.push(m[1]);
  for (const m of svg.matchAll(/<polygon\b[^>]*\bpoints\s*=\s*"([^"]+)"/g)) {
    const n = m[1].trim().split(/[\s,]+/).map(Number);
    if (n.length < 6) continue;
    let d = `M ${n[0]} ${n[1]}`;
    for (let i = 2; i + 1 < n.length; i += 2) d += ` L ${n[i]} ${n[i + 1]}`;
    shapes.push(d + " Z");
  }
  for (const m of svg.matchAll(/<rect\b[^>]*>/g)) {
    const tag = m[0];
    const num = (k) => Number((tag.match(new RegExp(k + '\\s*=\\s*"([\\d.\\-]+)"')) || [])[1] || 0);
    const x = num("x"), y = num("y"), w = num("width"), h = num("height");
    if (w > 0 && h > 0) shapes.push(`M ${x} ${y} L ${x + w} ${y} L ${x + w} ${y + h} L ${x} ${y + h} Z`);
  }
  if (!shapes.length) throw new Error("No drawable shapes found in this SVG.");

  for (const d of shapes) {
    page.drawSvgPath(d, {
      x: -dim.minX * scale,
      y: pageH + dim.minY * scale,
      scale,
      color,
      borderWidth: 0,
    });
  }
  return Buffer.from(await doc.save());
}
