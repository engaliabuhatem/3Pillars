import { chromium } from '@playwright/test';
const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
await ctx.addInitScript(() => sessionStorage.setItem('3p-intro', '1'));
const p = await ctx.newPage(); await p.goto('http://localhost:3000/en', { waitUntil: 'networkidle' });
for (let i = 0; i < 40; i++) { await p.mouse.wheel(0, 500); await p.waitForTimeout(150); }
await p.waitForTimeout(1200);
console.log('pending left:', await p.locator('.reveal-pending').count(), 'done:', await p.locator('.reveal-done').count(), 'scrollY', await p.evaluate(() => scrollY));
await p.screenshot({ path: 'C:/Users/abuha/AppData/Local/Temp/claude/7a70f5e40637c9bc/674eb5c7-7fb6-4df7-b8b5-d11bb8ff0947/scratchpad/wheel.png' }); await b.close();
