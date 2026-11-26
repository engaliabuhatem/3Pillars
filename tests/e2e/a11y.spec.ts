import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { LOCALES, TEMPLATES, quietVisit } from './helpers';

test.beforeEach(async ({ page }) => quietVisit(page));
test.use({ reducedMotion: 'reduce' });

for (const locale of LOCALES) {
  for (const path of [...TEMPLATES, '/_styleguide/', '/nope/']) {
    test(`axe: /${locale}${path} has no serious or critical issues`, async ({ page }) => {
      await page.goto(`/${locale}${path}`);
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
      const blocking = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
      expect(
        blocking.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).slice(0, 3).join(' | ')}`),
      ).toEqual([]);
    });
  }
}
