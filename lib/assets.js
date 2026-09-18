// The asset map. File names are read from disk so the connector can never offer
// something the CDN does not have. Usage rules are quoted from ai/CLAUDE.md.
import { listDir, exists, SITE } from "./kit.js";

export const LOGO_FILES = {
  complete: "LAIO-COMPLETE.svg",
  base: "LAIO-BASE.svg",
  horz: "LAIO-HORZ.svg",
  "louisiana-innovation-a": "LOUISIANA-INNOVATION-A.svg",
  "louisiana-innovation-b": "LOUISIANA-INNOVATION-B.svg",
  "division-line": "DIVISION-LINE.svg",
};

export const LED_FILES = {
  led: { dark: "LED-WHITE.svg", light: "LED-BLACK.svg" },
  "led-small": { dark: "LED-SMALL-WHITE.svg", light: "LED-SMALL-BLACK.svg" },
};

export const LOGO_VARIANTS = [...Object.keys(LOGO_FILES), ...Object.keys(LED_FILES)];

export const isLed = (v) => Object.hasOwn(LED_FILES, v);

// ground is "dark" or "light"; LED ships white and black only.
export function logoPath(variant, ground = "dark") {
  if (isLed(variant)) return "logos/" + LED_FILES[variant][ground === "light" ? "light" : "dark"];
  const f = LOGO_FILES[variant];
  return f ? "logos/" + f : null;
}

export function motifNames() {
  return listDir("motifs")
    .filter((f) => /^LAIO-.*\.svg$/.test(f))
    .map((f) => f.replace(/^LAIO-/, "").replace(/\.svg$/, "").toLowerCase());
}

export function motifPath(name) {
  const file = "LAIO-" + String(name).replace(/^laio-/i, "").toUpperCase().replace(/\.SVG$/, "") + ".svg";
  return exists("motifs/" + file) ? "motifs/" + file : null;
}

export const cdn = (rel) => SITE + "/" + rel;

export function renderUrl(kind, id, format, params = {}) {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== null && v !== "") q.set(k, String(v));
  const qs = q.toString();
  return `${SITE}/render/${kind}/${id}.${format}` + (qs ? "?" + qs : "");
}
