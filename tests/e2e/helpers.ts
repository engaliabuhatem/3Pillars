import type { Page } from '@playwright/test';

export const LOCALES = ['en', 'ar'] as const;

/** Every page template, by a path that exists with the seeded content. */
export const TEMPLATES = [
  '',
  '/services',
  '/services/project-management-consultancy',
  '/sectors',
  '/sectors/energy',
  '/projects',
  '/insights',
  '/about',
  '/approach',
  '/careers',
  '/contact',
  '/request-a-proposal',
  '/capability-statement',
  '/privacy',
];

/** Skip the once-per-session logo intro and pre-answer the cookie banner. */
export async function quietVisit(page: Page) {
  await page.addInitScript(() => {
    sessionStorage.setItem('3p-intro', '1');
    localStorage.setItem('3p-consent', 'essential');
  });
}
