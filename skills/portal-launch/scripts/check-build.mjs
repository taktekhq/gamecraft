#!/usr/bin/env node
// Pre-submit check for an HTML5 game build folder (CrazyGames / Poki style rules).
// Usage: node check-build.mjs DIST [--budget-mb 5] [--max-files 1500] [--allow host1,host2]
// Exits 1 on any failure. Checks: index.html exists, total size vs budget, file count, absolute asset paths
// in index.html, external URLs referenced in JS/CSS/HTML (portal SDK hosts allowed), source maps shipped.
import fs from "node:fs";
import path from "node:path";

const argv = process.argv.slice(2);
const dir = argv.find((a) => !a.startsWith("--") && !/^\d/.test(a));
const opt = (k, d) => { const i = argv.indexOf(`--${k}`); return i >= 0 ? argv[i + 1] : d; };
if (!dir) { console.error("usage: node check-build.mjs DIST [--budget-mb 5] [--max-files 1500] [--allow hosts]"); process.exit(2); }
const budget = Number(opt("budget-mb", 5)) * 1024 * 1024;
const maxFiles = Number(opt("max-files", 1500));
const allow = new Set(["sdk.crazygames.com", "game-cdn.poki.com", "www.w3.org", ...String(opt("allow", "")).split(",").filter(Boolean)]);

const files = [];
(function walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); e.isDirectory() ? walk(p) : files.push(p); } })(dir);

const fails = [], notes = [];
const total = files.reduce((s, f) => s + fs.statSync(f).size, 0);
const mb = (n) => (n / 1024 / 1024).toFixed(2) + " MB";
if (!fs.existsSync(path.join(dir, "index.html"))) fails.push("no index.html at the build root");
if (total > budget) fails.push(`total size ${mb(total)} is over the ${mb(budget)} budget`);
if (files.length > maxFiles) fails.push(`${files.length} files, over ${maxFiles}`);
const maps = files.filter((f) => f.endsWith(".map"));
if (maps.length) fails.push(`${maps.length} source map file(s) shipped (e.g. ${path.relative(dir, maps[0])})`);

const idx = path.join(dir, "index.html");
if (fs.existsSync(idx)) {
  const html = fs.readFileSync(idx, "utf8");
  const abs = [...html.matchAll(/(?:src|href)=["'](\/[^"'/][^"']*)["']/g)].map((m) => m[1]);
  if (abs.length) fails.push(`absolute paths in index.html (use ./): ${abs.slice(0, 5).join(", ")}`);
}

const ext = new Map();
for (const f of files.filter((f) => /\.(m?js|css|html)$/.test(f))) {
  const text = fs.readFileSync(f, "utf8");
  for (const m of text.matchAll(/https?:\/\/([a-z0-9.-]+\.[a-z]{2,})[^\s"'`)<>]*/gi)) {
    const host = m[1].toLowerCase();
    if (!allow.has(host)) ext.set(host, `${path.relative(dir, f)}: ${m[0].slice(0, 80)}`);
  }
}
if (ext.size) fails.push(`external URLs referenced (bundle them or allow with --allow):\n    ${[...ext.values()].slice(0, 12).join("\n    ")}`);

const biggest = files.map((f) => [fs.statSync(f).size, path.relative(dir, f)]).sort((a, b) => b[0] - a[0]).slice(0, 5);
notes.push(`total ${mb(total)} in ${files.length} files; largest: ${biggest.map(([s, n]) => `${n} ${mb(s)}`).join(", ")}`);

console.log(notes.join("\n"));
if (fails.length) { console.error("FAIL\n- " + fails.join("\n- ")); process.exit(1); }
console.log("ok");
