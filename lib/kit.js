// Reads the brand kit off disk. Every rule the connector serves comes from these
// files, so the connector cannot drift from what assets.la.io publishes. Nothing
// here is hand-copied from a document.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const MARKER = path.join("colors", "laio-tokens.json");

function findRoot() {
  const seen = new Set();
  const candidates = [];
  for (const start of [HERE, process.cwd(), "/var/task"]) {
    let dir = start;
    for (let i = 0; i < 6; i++) {
      if (!seen.has(dir)) { seen.add(dir); candidates.push(dir); }
      const up = path.dirname(dir);
      if (up === dir) break;
      dir = up;
    }
  }
  for (const dir of candidates) {
    try { if (fs.existsSync(path.join(dir, MARKER))) return dir; } catch {}
  }
  throw new Error("laio kit not found. Looked in: " + candidates.join(", "));
}

export const ROOT = findRoot();
export const SITE = "https://assets.la.io";

const cache = new Map();

export function readText(rel) {
  if (!cache.has(rel)) cache.set(rel, fs.readFileSync(path.join(ROOT, rel), "utf8"));
  return cache.get(rel);
}

export function readJson(rel) {
  const key = "json:" + rel;
  if (!cache.has(key)) cache.set(key, JSON.parse(readText(rel)));
  return cache.get(key);
}

export function exists(rel) {
  try { return fs.existsSync(path.join(ROOT, rel)); } catch { return false; }
}

export function listDir(rel) {
  try { return fs.readdirSync(path.join(ROOT, rel)).sort(); } catch { return []; }
}

export const tokens = () => readJson("colors/laio-tokens.json").laio;
export const cmyk   = () => readJson("colors/laio-cmyk.json");
export const brief  = () => readText("ai/CLAUDE.md");
export const voice  = () => readText("ai/laio-brand/VOICE.md");

// Pull one "## Heading" section out of a markdown file, heading line included.
export function section(md, heading) {
  const lines = md.split("\n");
  const start = lines.findIndex(
    (l) => l.trim().toLowerCase() === "## " + heading.toLowerCase()
  );
  if (start === -1) return "";
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    if (/^## /.test(lines[i])) { end = i; break; }
  }
  return lines.slice(start, end).join("\n").replace(/\n*-{3,}\n*$/, "").trim();
}
