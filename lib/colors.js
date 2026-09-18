// Color resolution. Values come from colors/laio-tokens.json and
// colors/laio-cmyk.json. Nothing is written twice.
import { tokens, cmyk } from "./kit.js";

export const FAMILIES = ["magenta", "green", "blue", "orange", "gray"];

export function slotsFor(family) {
  return Object.keys(tokens()[family] || {});
}

// "easy green", "Electric Blue", "green.electric", "#96F90B", "white", "black"
export function resolve(input) {
  if (!input) return null;
  const raw = String(input).trim();

  if (/^#?[0-9a-f]{6}$/i.test(raw)) {
    const hex = "#" + raw.replace("#", "").toUpperCase();
    return { hex, family: null, slot: null, name: hex };
  }
  if (/^#?[0-9a-f]{3}$/i.test(raw)) {
    const s = raw.replace("#", "");
    const hex = "#" + s.split("").map((c) => c + c).join("").toUpperCase();
    return { hex, family: null, slot: null, name: hex };
  }

  const t = tokens();
  const norm = raw.toLowerCase().replace(/[^a-z]+/g, " ").trim();

  if (norm === "white") return { hex: "#FFFFFF", family: "gray", slot: "white", name: "White" };
  if (norm === "black") {
    return { hex: t.gray.dark.value, family: "gray", slot: "dark", name: t.gray.dark.name };
  }

  const words = norm.split(" ");
  const family = FAMILIES.find((f) => words.includes(f))
    || (words.includes("purple") ? "magenta" : null)
    || (words.includes("grey") ? "gray" : null);
  if (!family) return null;

  const slots = t[family];
  let slot = Object.keys(slots).find((s) => words.includes(s));
  if (!slot) slot = family === "gray" ? "mid" : "electric";
  const entry = slots[slot];
  if (!entry) return null;
  return { hex: entry.value.toUpperCase(), family, slot, name: entry.name };
}

export const hexToRgb = (hex) => {
  const s = hex.replace("#", "");
  return [0, 2, 4].map((i) => parseInt(s.slice(i, i + 2), 16));
};

// Rec.709 studio swing. Same primaries as sRGB, broadcast-legal 16 to 235.
export const toRec709 = (rgb) => rgb.map((v) => Math.round(16 + (v * 219) / 255));

export function cmykFor(family, slot, profile) {
  const v = cmyk().values?.[family]?.[slot];
  if (!v) return null;
  const out = { values: v[profile] || null, profile };
  if (profile === "coated" && v.coatedVivid) out.vivid = v.coatedVivid;
  if (v.outOfGamut) out.outOfGamut = true;
  if (v.pantone) out.pantone = v.pantone;
  return out;
}

export const fmtCmyk = (a) => (a ? a.map((n) => Math.round(n)).join("/") : null);
