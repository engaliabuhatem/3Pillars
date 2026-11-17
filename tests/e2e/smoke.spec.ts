import { expect, test } from '@playwright/test';
import { LOCALES, TEMPLATES, quietVisit } from './helpers';

test.beforeEach(async ({ page }) => quietVisit(page));

for (const locale of LOCALES) {
  test(`home renders in ${locale} with the right language and direction`, async ({ page }) => {
    await page.goto(`/${locale}`);
    await expect(page.locator('html')).toHaveAttribute('lang', locale);
    await expect(page.locator('html')).toHaveAttribute('dir', locale === 'ar' ? 'rtl' : 'ltr');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.locator('footer')).toBeVisible();
  });

  test(`every template answers 200 in ${locale}`, async ({ page }) => {
    for (const path of TEMPLATES) {
      const response = await page.goto(`/${locale}${path}`);
      expect(response?.status(), path).toBe(200);
      await expect(page.getByRole('heading', { level: 1 }), path).toBeVisible();
    }
  });
}

test('unknown paths get a real 404', async ({ page }) => {
  const response = await page.goto('/en/this/does/not/exist');
  expect(response?.status()).toBe(404);
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Page not found');
});

test('a path without a locale redirects to one', async ({ page }) => {
  await page.goto('/services');
  await expect(page).toHaveURL(/\/(en|ar)\/services$/);
});

test('navigation reaches the services page', async ({ page, isMobile }) => {
  await page.goto('/en');
  if (isMobile) {
    await page.getByRole('button', { name: 'Menu' }).click();
    await page.locator('#mobile-menu').getByRole('link', { name: 'Services' }).click();
  } else {
    await page.getByRole('navigation', { name: 'Main' }).getByRole('link', { name: 'Projects' }).click();
    await expect(page).toHaveURL(/\/en\/projects$/);
    await page.getByRole('navigation', { name: 'Main' }).getByRole('button', { name: 'Services' }).click();
    await page.getByRole('link', { name: 'Services →' }).click();
  }
  await expect(page).toHaveURL(/\/en\/services$/);
});

test('the language switch keeps the page and mirrors the layout', async ({ page, isMobile }) => {
  await page.goto('/en/services');
  await page.getByRole('link', { name: /العربية/ }).click();
  await expect(page).toHaveURL(/\/ar\/services$/);
  await expect(page.locator('html')).toHaveAttribute('dir', 'rtl');

  // RTL mirroring: the logo moves to the right edge, the breadcrumb starts on the right.
  const width = page.viewportSize()!.width;
  const logo = await page.locator('header a[href="/ar"]').first().boundingBox();
  expect(logo!.x).toBeGreaterThan(width / 2);
  if (!isMobile) {
    const crumb = await page.getByRole('navigation', { name: 'مسار التنقل' }).boundingBox();
    expect(crumb!.x + crumb!.width).toBeGreaterThan(width - 80);
  }
});

test('no horizontal overflow on any template, in either direction', async ({ page }) => {
  for (const locale of LOCALES) {
    for (const path of TEMPLATES) {
      await page.goto(`/${locale}${path}`);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, `${locale}${path}`).toBeLessThanOrEqual(0);
    }
  }
});
