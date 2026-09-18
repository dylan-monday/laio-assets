// Mimics the Vercel rewrites locally: /render/* -> api/render, /mcp -> api/mcp
import http from "node:http";
import render from "../api/render.js";
let mcp = null;
try { mcp = (await import("../api/mcp.js")).default; } catch {}

http.createServer(async (req, res) => {
  const u = new URL(req.url, "http://localhost");
  if (u.pathname.startsWith("/render/")) {
    req.url = "/api/render?path=" + encodeURIComponent(u.pathname.slice("/render/".length)) + "&" + u.searchParams.toString();
    return render(req, res);
  }
  if (u.pathname === "/mcp" && mcp) return mcp(req, res);
  res.statusCode = 404; res.end("no route\n");
}).listen(5199, () => console.log("dev server on 5199"));
