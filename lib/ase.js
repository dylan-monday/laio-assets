// Adobe Swatch Exchange writer. Produces .ase files on demand so a designer can
// load the exact family and profile they need into Illustrator, InDesign or
// Photoshop. Values come from the kit, never from this file.
const MODELS = { RGB: "RGB ", CMYK: "CMYK", LAB: "LAB ", GRAY: "Gray" };

function nameBlock(name) {
  const units = name.length + 1; // UTF-16 code units, trailing null included
  const buf = Buffer.alloc(2 + units * 2);
  buf.writeUInt16BE(units, 0);
  buf.write(name, 2, "utf16le");
  // swap to big endian
  for (let i = 2; i < 2 + name.length * 2; i += 2) {
    const a = buf[i]; buf[i] = buf[i + 1]; buf[i + 1] = a;
  }
  return buf;
}

function colorBlock({ name, model, values, spot }) {
  const head = nameBlock(name);
  const body = Buffer.alloc(4 + values.length * 4 + 2);
  body.write(MODELS[model], 0, "ascii");
  values.forEach((v, i) => body.writeFloatBE(v, 4 + i * 4));
  body.writeUInt16BE(spot ? 1 : 2, 4 + values.length * 4);
  const data = Buffer.concat([head, body]);
  const out = Buffer.alloc(6 + data.length);
  out.writeUInt16BE(0x0001, 0);
  out.writeUInt32BE(data.length, 2);
  data.copy(out, 6);
  return out;
}

function groupStart(name) {
  const data = nameBlock(name);
  const out = Buffer.alloc(6 + data.length);
  out.writeUInt16BE(0xc001, 0);
  out.writeUInt32BE(data.length, 2);
  data.copy(out, 6);
  return out;
}

function groupEnd() {
  const out = Buffer.alloc(6);
  out.writeUInt16BE(0xc002, 0);
  out.writeUInt32BE(0, 2);
  return out;
}

export function buildAse(groups) {
  const blocks = [];
  for (const g of groups) {
    if (g.name) blocks.push(groupStart(g.name));
    for (const c of g.colors) blocks.push(colorBlock(c));
    if (g.name) blocks.push(groupEnd());
  }
  const head = Buffer.alloc(12);
  head.write("ASEF", 0, "ascii");
  head.writeUInt16BE(1, 4);
  head.writeUInt16BE(0, 6);
  head.writeUInt32BE(blocks.length, 8);
  return Buffer.concat([head, ...blocks]);
}

// Round-trip reader, used by the build check. Not served.
export function readAse(buf) {
  if (buf.slice(0, 4).toString("ascii") !== "ASEF") throw new Error("not an ASE file");
  const count = buf.readUInt32BE(8);
  const out = [];
  let o = 12;
  for (let i = 0; i < count; i++) {
    const type = buf.readUInt16BE(o);
    const len = buf.readUInt32BE(o + 2);
    const data = buf.slice(o + 6, o + 6 + len);
    o += 6 + len;
    if (type === 0xc002) { out.push({ type: "groupEnd" }); continue; }
    const units = data.readUInt16BE(0);
    const raw = Buffer.from(data.slice(2, 2 + units * 2));
    for (let j = 0; j < raw.length; j += 2) { const a = raw[j]; raw[j] = raw[j + 1]; raw[j + 1] = a; }
    const name = raw.toString("utf16le").replace(/\0+$/, "");
    if (type === 0xc001) { out.push({ type: "group", name }); continue; }
    const rest = data.slice(2 + units * 2);
    const model = rest.slice(0, 4).toString("ascii");
    const n = model === "CMYK" ? 4 : model === "Gray" ? 1 : 3;
    const values = [];
    for (let k = 0; k < n; k++) values.push(Number(rest.readFloatBE(4 + k * 4).toFixed(4)));
    out.push({ type: "color", name, model, values });
  }
  return out;
}
