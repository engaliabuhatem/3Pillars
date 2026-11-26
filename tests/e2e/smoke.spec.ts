import { expect, test } from '@playwright/test';
import { AWAITING_SEO, LOCALES, REMOVED, TEMPLATES, quietVisit } from './helpers';

/*
 * Run with "Show content awaiting approval" ON (staging) and the content
 * seeded (`manage.py seed_content`): every page then has its pending copy.
 */

test.beforeEach(async ({ page }) => quietVisit(page));

for (const locale of LOCALES) {
  test(`home renders in ${locale} with the right language and direction`, async ({ page }) => {
    await page.goto(`/${locale}/`);
    await expect(page.locator('html')).toHaveAttribute('lang', locale);
    await expect(page.locator('html')).toHaveAttribute('dir', locale === 'ar' ? 'rtl' : 'ltr');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.locator('footer')).toBeVisible();
  });

  test(`every route answers 200 in ${locale} with exactly one h1`, async ({ page }) => {
    for (const path of TEMPLATES) {
      const response = await page.goto(`/${locale}${path}`);
      expect(response?.status(), path).toBe(200);
      await expect(page.locator('h1'), path).toHaveCount(1);
      await expect(page.getByRole('heading', { level: 1 }), path).toBeVisible();
    }
  });

  test(`every page in ${locale} has its own title and meta description`, async ({ page }) => {
    const titles = new Map<string, string>();
    const descriptions = new Map<string, string>();
    for (const path of TEMPLATES.filter((p) => !AWAITING_SEO.includes(p))) {
      await page.goto(`/${locale}${path}`);
      const title = await page.title();
      const description = (await page.locator('meta[name="description"]').getAttribute('content')) ?? '';
      expect(title, path).not.toBe('');
      expect(description, path).not.toBe('');
      expect(titles.get(title), `${path} repeats the title of ${titles.get(title)}`).toBeUndefined();
      expect(descriptions.get(description), `${path} repeats the description of ${descriptions.get(description)}`).toBeUndefined();
      titles.set(title, path);
      descriptions.set(description, path);
    }
  });

  test(`removed pages are not reachable in ${locale}`, async ({ page }) => {
    for (const path of REMOVED) {
      const response = await page.goto(`/${locale}${path}`);
      expect(response?.status(), path).toBe(404);
    }
  });
}

test('page addresses end in a slash', async ({ page }) => {
  await page.goto('/en/services');
  await expect(page).toHaveURL(/\/en\/services\/$/);
  const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
  expect(canonical).toMatch(/\/en\/services\/$/);
});

test('robots and hreflang follow approval and Arabic review', async ({ page, request }) => {
  const api = process.env.NEXT_PUBLIC_CMS_API_URL ?? 'http://127.0.0.1:8000/api';
  const { seo } = (await (await request.get(`${api}/pages/services/`)).json()) as { seo: { indexable: { en: boolean; ar: boolean } } };
  for (const locale of ['en', 'ar'] as const) {
    await page.goto(`/${locale}/services/`);
    const robots = page.locator('meta[name="robots"]');
    await expect(robots, locale).toHaveAttribute('content', seo.indexable[locale] ? /(^|, )index/ : /noindex/);
    await expect(page.locator('link[rel="alternate"][hreflang="ar"]'), locale).toHaveCount(seo.indexable.ar ? 1 : 0);
  }
});

test('unknown paths get a real 404', async ({ page }) => {
  const response = await page.goto('/en/this/does/not/exist/');
  expect(response?.status()).toBe(404);
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Page not found');
});

test('a path without a locale redirects to one', async ({ page }) => {
  await page.goto('/services/');
  await expect(page).toHaveURL(/\/(en|ar)\/services\/$/);
});

test('navigation reaches a service page', async ({ page, isMobile }) => {
  await page.goto('/en/');
  if (isMobile) {
    await page.getByRole('button', { name: 'Menu' }).click();
    await page.locator('#mobile-menu').getByRole('link', { name: 'Services' }).click();
    await expect(page).toHaveURL(/\/en\/services\/$/);
  } else {
    await page.getByRole('navigation', { name: 'Main' }).getByRole('button', { name: 'Services' }).click();
    await page.getByRole('link', { name: 'Services →' }).click();
    await expect(page).toHaveURL(/\/en\/services\/$/);
  }
});

test('the header button requests a consultation', async ({ page, isMobile }) => {
  test.skip(isMobile, 'The header button is hidden on small screens; the mobile menu carries it.');
  await page.goto('/en/');
  await page.locator('header').getByRole('link', { name: 'Request a Consultation' }).click();
  await expect(page).toHaveURL(/\/en\/contact\/request-a-consultation\/$/);
});

test('services and sectors link to each other', async ({ page }) => {
  await page.goto('/en/sectors/infrastructure/');
  await page.getByRole('link', { name: 'PMO & Project Controls' }).first().click();
  await expect(page).toHaveURL(/\/en\/services\/pmo-project-controls\/$/);
  await expect(page.getByRole('link', { name: 'Infrastructure' }).first()).toBeVisible();
});

test('the language switch keeps the page and mirrors the layout', async ({ page, isMobile }) => {
  await page.goto('/en/services/');
  await page.getByRole('link', { name: /العربية/ }).click();
  await expect(page).toHaveURL(/\/ar\/services\/$/);
  await expect(page.locator('html')).toHaveAttribute('dir', 'rtl');

  // RTL mirroring: the logo moves to the right edge, the breadcrumb starts on the right.
  const width = page.viewportSize()!.width;
  const logo = await page.locator('header a[href="/ar/"]').first().boundingBox();
  expect(logo!.x).toBeGreaterThan(width / 2);
  if (!isMobile) {
    const crumb = await page.getByRole('navigation', { name: 'مسار التنقل' }).boundingBox();
    expect(crumb!.x + crumb!.width).toBeGreaterThan(width - 80);
  }
});

test('no horizontal overflow on any route, in either direction', async ({ page }) => {
  for (const locale of LOCALES) {
    for (const path of TEMPLATES) {
      await page.goto(`/${locale}${path}`);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, `${locale}${path}`).toBeLessThanOrEqual(0);
    }
  }
});
