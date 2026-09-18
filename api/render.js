// GET /render/logo/{variant}.{svg|png|pdf}
// GET /render/motif/{name}.{svg|png|pdf}
// GET /render/swatch/{family}-{profile}.ase
//
// Every variant is a deterministic URL, so the CDN caches it and the same
// request always returns the same bytes.
import { renderAsset, renderSwatch, RenderError } from "../lib/render-core.js";

const IMMUTABLE = "public, max-age=31536000, s-maxage=31536000, immutable";

function fail(res, status, message) {
  res.statusCode = status;
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=0, must-revalidate");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.end(message + "\n");
}

export default async function handler(req, res) {
  const url = new URL(req.url, "https://assets.la.io");
  const q = url.searchParams;
  const raw = (q.get("path") || url.pathname.replace(/^\/(api\/)?render\/?/, "")).replace(/^\/+/, "");

  if (req.method === "OPTIONS") {
    res.statusCode = 204;
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS");
    return res.end();
  }
  if (req.method !== "GET" && req.method !== "HEAD") return fail(res, 405, "Use GET.");

  const m = raw.match(/^(logo|motif|swatch)\/([A-Za-z0-9._-]+)$/);
  if (!m) {
    return fail(res, 404, [
      "LA.IO render endpoint.",
      "",
      "  /render/logo/{variant}.{svg|png|pdf}?color=&width=&background=",
      "  /render/motif/{name}.{svg|png|pdf}?color=&width=&background=",
      "  /render/swatch/{family}-{profile}.ase   profile: rgb, coated, newsprint",
    ].join("\n"));
  }

  const [, kind, tail] = m;
  const dot = tail.lastIndexOf(".");
  if (dot < 1) return fail(res, 400, "Missing a file extension.");
  const id = tail.slice(0, dot).toLowerCase();
  const format = tail.slice(dot + 1).toLowerCase();

  try {
    let out;
    let filename;

    if (kind === "swatch") {
      if (format !== "ase") return fail(res, 400, "Swatches are .ase only.");
      const cut = id.lastIndexOf("-");
      if (cut < 1) return fail(res, 400, "Use {family}-{profile}.ase, for example blue-coated.ase.");
      const family = id.slice(0, cut);
      const profile = id.slice(cut + 1);
      out = renderSwatch(family, profile);
      filename = `LA.IO-${family}-${profile}.ase`;
      if (out.missing?.length) res.setHeader("X-Laio-Missing", out.missing.join(", "));
    } else {
      out = renderAsset(kind, id, format, {
        color: q.get("color"),
        width: q.get("width"),
        background: q.get("background") || q.get("bg"),
      });
      const colorTag = (q.get("color") || "default").replace(/[^a-z0-9]+/gi, "-");
      filename = `LAIO-${id}-${colorTag}.${format}`;
    }

    const body = out.async ? await out.body : out.body;
    res.statusCode = 200;
    res.setHeader("Content-Type", out.type);
    res.setHeader("Cache-Control", IMMUTABLE);
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Content-Length", String(body.length));
    res.setHeader("Content-Disposition", `inline; filename="${filename}"`);
    if (out.note) res.setHeader("X-Laio-Note", out.note);
    if (req.method === "HEAD") return res.end();
    return res.end(body);
  } catch (err) {
    if (err instanceof RenderError) return fail(res, err.status, err.message);
    console.error("render failed", err);
    return fail(res, 500, "Render failed.");
  }
}
