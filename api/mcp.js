// The LA.IO brand connector. Streamable HTTP MCP server at /mcp.
//
// Tool descriptions carry the weight here. Nobody calls a tool by name, so each
// description has to say plainly when it applies.
import { createMcpHandler } from "mcp-handler";
import { z } from "zod";
import {
  brandBrief, voiceFor, colorsFor, assetList, logoFor, motifFor, fontsFor,
} from "../lib/tools.js";
import { LOGO_VARIANTS, motifNames } from "../lib/assets.js";

const LAIO = "LA.IO, Louisiana Innovation, or Louisiana Economic Development's innovation work";

const mcp = createMcpHandler(
  (server) => {
    server.registerTool("get_brand_brief", {
      title: "LA.IO brand brief",
      description:
        `Call this before writing, designing, or producing anything for ${LAIO}. ` +
        "Returns the current brand instructions: voice, banned language, color families, type rules, logo rules, " +
        "and the standing rules for AI work. Call it even when the request never mentions a brand system, " +
        "for example a social post, a press release, a deck, a page, an email, or an ad. Start here, then use the " +
        "other tools for voice detail, colors, logos, motifs and fonts.",
      inputSchema: z.object({}),
    }, async () => brandBrief());

    server.registerTool("get_voice", {
      title: "LA.IO voice guide",
      description:
        `Get the voice profile, naming rules, ban list and anti-AI rules before writing any copy for ${LAIO}. ` +
        "Use speaker 'brand' for anything in the organization's own voice, 'josh' for Josh Fleig, Chief Innovation " +
        "Officer, and 'susan' for Susan Bourgois, Secretary of Economic Development. Call this for posts, quotes, " +
        "remarks, releases, newsletters, op-eds, talking points and award submissions.",
      inputSchema: z.object({
        speaker: z.enum(["brand", "josh", "susan"]).default("brand")
          .describe("Whose voice the copy is in. Default brand."),
      }),
    }, async ({ speaker }) => voiceFor(speaker));

    server.registerTool("get_colors", {
      title: "LA.IO color values",
      description:
        "Get exact LA.IO color values for a job, plus a swatch file to download. Call this whenever you need a " +
        "color for a design, a deck, a page, a print piece or a video. Use format 'cmyk-coated' for anything " +
        "printed, including digital print. Use 'cmyk-newsprint' only when the job is a newspaper or the Advocate. " +
        "Use 'rec709' for video. Use 'hex' or 'rgb' for screen. One family per piece, never mixed.",
      inputSchema: z.object({
        family: z.enum(["magenta", "green", "blue", "orange", "gray", "all"]).default("all")
          .describe("Which of the five families. Default all."),
        format: z.enum(["hex", "rgb", "cmyk-coated", "cmyk-newsprint", "rec709", "all"]).default("hex")
          .describe("Which values to return. Default hex."),
      }),
    }, async ({ family, format }) => colorsFor(family, format));

    server.registerTool("list_assets", {
      title: "What is in the LA.IO kit",
      description:
        "See every logo lockup, motif, font and video asset in the LA.IO kit, with the rule for when each one " +
        "applies. Call this when you are not sure which lockup or shape a piece needs, or when someone asks what " +
        "is available.",
      inputSchema: z.object({
        kind: z.enum(["logos", "motifs", "fonts", "video", "all"]).default("all"),
      }),
    }, async ({ kind }) => assetList(kind));

    server.registerTool("get_logo", {
      title: "Get an LA.IO logo file",
      description:
        "Get an LA.IO or LED logo as a download link, in any brand color, size and format. Call this whenever " +
        "someone asks for the logo, a mark, a lockup, a transparent PNG, a vector file, artwork for print, or a " +
        "logo with alpha for video, and whenever you are building something that needs the real logo rather than " +
        "typed text. PNG is transparent unless you set a background. SVG also comes back as inline markup for " +
        `artifacts and sandboxed output. Variants: ${LOGO_VARIANTS.join(", ")}. 'complete' is the default everywhere.`,
      inputSchema: z.object({
        variant: z.enum(LOGO_VARIANTS).default("complete")
          .describe("Which lockup. complete is the default everywhere unless a rule says otherwise."),
        color: z.string().optional()
          .describe("A brand color name like 'easy green' or 'electric blue', or a hex value. Leave empty for the default."),
        format: z.enum(["svg", "png", "pdf"]).default("png")
          .describe("svg for web and artifacts, png for slides and video, pdf for print."),
        width: z.number().int().positive().max(6000).optional()
          .describe("Width in pixels for PNG. Default 2000."),
        background: z.string().optional()
          .describe("A brand color for the background, or leave empty for transparent."),
      }),
    }, async (args) => logoFor(args));

    server.registerTool("get_motif", {
      title: "Get an LA.IO motif file",
      description:
        "Get one of the LA.IO bracket and shape motifs as a download link, in any brand color and format. Call " +
        "this when a layout needs a graphic element, a corner, a bracket, a divider or a background pattern. " +
        `Available: ${motifNames().join(", ")}.`,
      inputSchema: z.object({
        name: z.string().describe("Motif name, for example plus, x, diamond, left-bracket, hatch."),
        color: z.string().optional().describe("A brand color name or hex value."),
        format: z.enum(["svg", "png", "pdf"]).default("svg"),
        size: z.number().int().positive().max(6000).optional().describe("Width in pixels for PNG. Default 1000."),
      }),
    }, async (args) => motifFor(args));

    server.registerTool("get_fonts", {
      title: "Get LA.IO fonts and how to load them",
      description:
        "Get Aktiv Grotesk and the right way to load it for what you are building. Call this before producing any " +
        "visual output for LA.IO. Use context 'artifact' for a claude.ai artifact, Claude Design, a Lovable " +
        "preview, an email, or anything else sandboxed. Use 'web' for a real site on a domain. Use 'desktop' for " +
        "Adobe apps. Use 'video' for Resolve, After Effects and Premiere. Use 'office' before building any " +
        "PowerPoint, Word, Google Slides or Google Docs file, because the font does not travel in those and there " +
        "is a specific fallback.",
      inputSchema: z.object({
        context: z.enum(["artifact", "web", "desktop", "video", "office"]).default("artifact"),
      }),
    }, async ({ context }) => fontsFor(context));
  },
  {
    serverInfo: { name: "laio-brand", version: "1.0.0" },
    capabilities: { tools: { listChanged: false } },
  }
);

// Vercel Node function to Web Request and back.
function readBody(req) {
  if (req.body !== undefined && req.body !== null) {
    return Promise.resolve(typeof req.body === "string" ? req.body : JSON.stringify(req.body));
  }
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

export default async function handler(req, res) {
  if (req.method === "OPTIONS") {
    res.statusCode = 204;
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "content-type, authorization, mcp-session-id, mcp-protocol-version");
    res.setHeader("Access-Control-Expose-Headers", "mcp-session-id");
    return res.end();
  }

  const proto = req.headers["x-forwarded-proto"] || "https";
  const host = req.headers["x-forwarded-host"] || req.headers.host || "assets.la.io";
  const url = new URL(req.url || "/mcp", `${proto}://${host}`);
  url.pathname = "/mcp";

  const headers = new Headers();
  for (const [k, v] of Object.entries(req.headers)) {
    if (v === undefined) continue;
    headers.set(k, Array.isArray(v) ? v.join(", ") : String(v));
  }

  const init = { method: req.method, headers };
  if (req.method !== "GET" && req.method !== "HEAD") init.body = await readBody(req);

  let response;
  try {
    response = await mcp(new Request(url, init));
  } catch (err) {
    console.error("mcp failed", err);
    res.statusCode = 500;
    res.setHeader("Content-Type", "application/json");
    return res.end(JSON.stringify({ jsonrpc: "2.0", error: { code: -32603, message: "Internal error" }, id: null }));
  }

  res.statusCode = response.status;
  response.headers.forEach((v, k) => res.setHeader(k, v));
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Expose-Headers", "mcp-session-id");
  res.setHeader("Cache-Control", "no-store");

  if (!response.body) return res.end();
  const reader = response.body.getReader();
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    res.write(Buffer.from(value));
  }
  res.end();
}
