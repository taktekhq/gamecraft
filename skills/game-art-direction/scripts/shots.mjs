#!/usr/bin/env node
// Capture a web game at portal iframe sizes, before and after some clicks, and fail on console errors.
// Usage: node shots.mjs --url http://localhost:4173 --out shots/ [--clicks 40] [--selector "#scene"] [--wait 1500]
// Needs playwright or playwright-core and a Chromium (set CHROMIUM_PATH if playwright cannot find one).
import fs from "node:fs";
import path from "node:path";

const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, all) => (a.startsWith("--") ? [...acc, [a.slice(2), all[i + 1]]] : acc), [])
);
if (!args.url) {
  console.error("usage: node shots.mjs --url URL --out DIR [--clicks N] [--selector CSS] [--wait MS]");
  process.exit(2);
}
const out = args.out || "shots";
const clicks = Number(args.clicks ?? 40);
const wait = Number(args.wait ?? 1500);
const sizes = (args.sizes || "907x510,1366x768,1920x1080,800x450,390x844").split(",");

let chromium;
try { ({ chromium } = await import("playwright")); } catch { ({ chromium } = await import("playwright-core")); }

fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const errors = [];
for (const size of sizes) {
  const [width, height] = size.split("x").map(Number);
  const isPhone = width < height;
  const ctx = await browser.newContext({ viewport: { width, height }, hasTouch: isPhone, isMobile: isPhone, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on("console", (m) => { if (m.type() === "error") errors.push(`${size}: ${m.text()}`); });
  page.on("pageerror", (e) => errors.push(`${size}: ${e.message}`));
  page.on("request", (r) => {
    const u = new URL(r.url());
    const base = new URL(args.url);
    if (!["data:", "blob:"].includes(u.protocol) && u.host !== base.host) errors.push(`${size}: external request ${r.url()}`);
  });
  const t0 = Date.now();
  await page.goto(args.url, { waitUntil: "load" });
  const loadMs = Date.now() - t0;
  await page.waitForTimeout(wait);
  await page.screenshot({ path: path.join(out, `${size}-start.png`) });
  const target = args.selector ? page.locator(args.selector).first() : null;
  for (let i = 0; i < clicks; i++) {
    if (target) await target.click({ force: true }).catch(() => {});
    else await page.mouse.click(width * 0.35, height * 0.55);
    await page.waitForTimeout(60);
  }
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(out, `${size}-play.png`) });
  console.log(`${size}: load ${loadMs} ms`);
  await ctx.close();
}
await browser.close();
if (errors.length) {
  console.error(`FAIL: ${errors.length} problem(s)\n` + [...new Set(errors)].slice(0, 30).join("\n"));
  process.exit(1);
}
console.log(`ok: ${sizes.length * 2} screenshots in ${out}`);
