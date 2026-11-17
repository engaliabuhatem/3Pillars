import { expect, test } from '@playwright/test';
import { contrast } from '../../src/lib/color.mjs';
import { quietVisit } from './helpers';

test.beforeEach(async ({ page }) => quietVisit(page));

test('hero video can be paused and resumed with the button', async ({ page }) => {
  await page.goto('/en');
  const toggle = page.getByTestId('hero-video-toggle');
  // The video mounts after hydration (it is never server-rendered, so reduced-motion visitors never download it).
  const hasVideo = await toggle.waitFor({ timeout: 8000 }).then(() => true, () => false);
  test.skip(!hasVideo, 'No hero video uploaded in this CMS.');

  const video = page.locator('section video');
  await expect.poll(() => video.evaluate((v: HTMLVideoElement) => !v.paused)).toBe(true);
  await toggle.click();
  await expect.poll(() => video.evaluate((v: HTMLVideoElement) => v.paused)).toBe(true);
  await expect(toggle).toHaveAccessibleName('Play background video');
  await toggle.click();
  await expect.poll(() => video.evaluate((v: HTMLVideoElement) => !v.paused)).toBe(true);
});

test('hero scrim keeps white text ≥ 4.5:1 over the brightest possible frame', async ({ page }) => {
  await page.goto('/en');
  // Worst case: replace the footage with pure white and hide the text, then
  // sample the brightest pixel behind where the headline and subline sit.
  await page.addStyleTag({
    content: `section[aria-labelledby=hero-title] img, section[aria-labelledby=hero-title] video { visibility: hidden !important }
      section[aria-labelledby=hero-title] { background: #fff !important }
      section[aria-labelledby=hero-title] h1, section[aria-labelledby=hero-title] p { color: transparent !important }`,
  });
  for (const selector of ['#hero-title', '#hero-title + p']) {
    const box = await page.locator(selector).boundingBox();
    if (!box) continue;
    const shot = await page.screenshot({ clip: box });
    const brightest = await page.evaluate(async (b64) => {
      const img = new Image();
      img.src = `data:image/png;base64,${b64}`;
      await img.decode();
      const canvas = Object.assign(document.createElement('canvas'), { width: img.width, height: img.height });
      const ctx = canvas.getContext('2d')!;
      ctx.drawImage(img, 0, 0);
      const data = ctx.getImageData(0, 0, img.width, img.height).data;
      let best = [0, 0, 0];
      let bestSum = -1;
      for (let i = 0; i < data.length; i += 4) {
        const sum = data[i]! + data[i + 1]! + data[i + 2]!;
        if (sum > bestSum) [bestSum, best] = [sum, [data[i]!, data[i + 1]!, data[i + 2]!]];
      }
      return `#${best.map((c) => c.toString(16).padStart(2, '0')).join('')}`;
    }, shot.toString('base64'));
    expect(contrast('#FFFFFF', brightest), `${selector} over ${brightest}`).toBeGreaterThanOrEqual(4.5);
  }
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });

  test('no video, no smooth scroll, nothing hidden for reveal, no running animations', async ({ page }) => {
    await page.goto('/en');
    await expect(page.locator('section video')).toHaveCount(0);
    await expect(page.locator('html.lenis')).toHaveCount(0);
    await expect(page.locator('[data-intro]')).toHaveCount(0);
    for (let y = 0; y < 6000; y += 800) await page.mouse.wheel(0, 800);
    await expect(page.locator('.reveal-pending')).toHaveCount(0);
    const running = await page.evaluate(() =>
      document.getAnimations().filter((a) => a.playState === 'running' && (a.effect?.getComputedTiming().duration as number) > 1).length,
    );
    expect(running).toBe(0);
  });
});
