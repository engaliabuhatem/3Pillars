// usage: node _shots.mjs outDir width url1 name1 [url2 name2 ...]  (env FULL=1 for full page)
import { chromium } from '@playwright/test';
const [out, width, ...pairs] = process.argv.slice(2);
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: Number(width), height: 900 }, reducedMotion: process.env.REDUCED ? 'reduce' : 'no-preference' });
await ctx.addInitScript(() => sessionStorage.setItem('3p-intro', '1'));
const p = await ctx.newPage();
const logs = [];
p.on('console', (m) => (m.type() === 'error' || m.type() === 'warning') && logs.push(`${m.type()}: ${m.text()}`));
p.on('pageerror', (e) => logs.push(`pageerror: ${e.message}`));
for (let i = 0; i < pairs.length; i += 2) {
  const res = await p.goto(pairs[i], { waitUntil: 'networkidle' });
  if (process.env.FULL) { await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); }); await p.waitForTimeout(800); }
  await p.screenshot({ path: `${out}/${pairs[i + 1]}.png`, fullPage: Boolean(process.env.FULL) });
  console.log(pairs[i], res?.status());
}
console.log(logs.slice(0, 15).join('\n'));
await b.close();
