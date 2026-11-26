import type { Page } from '@playwright/test';

export const LOCALES = ['en', 'ar'] as const;

export const SERVICES = [
  '/services/project-programme-management/',
  '/services/pmo-project-controls/',
  '/services/business-development/',
  '/services/strategic-advisory-market-intelligence/',
];

export const SECTORS = [
  '/sectors/built-environment/',
  '/sectors/infrastructure/',
  '/sectors/urban-development-planning/',
  '/sectors/research-studies/',
];

/** Every route in the site map (content document section 01), with `manage.py seed_content` loaded. */
export const TEMPLATES = [
  '/',
  '/about-us/',
  '/our-approach/',
  '/about-us/leadership-team/',
  '/about-us/hs-group/',
  '/services/',
  ...SERVICES,
  '/sectors/',
  ...SECTORS,
  '/projects/',
  '/insights/',
  '/careers/',
  '/contact/',
  '/contact/request-a-consultation/',
  '/capability-statement/',
  '/privacy/',
];

/**
 * Pages the content document gives no SEO title or description for. They fall
 * back to the site defaults until an editor writes their own, so they are left
 * out of the uniqueness check; the final report lists them as open.
 */
export const AWAITING_SEO = ['/about-us/leadership-team/', '/about-us/hs-group/', '/contact/request-a-consultation/'];

/** Pages the repositioning removed: they must not be reachable any more. */
export const REMOVED = [
  '/about/',
  '/approach/',
  '/request-a-proposal/',
  '/services/project-management-consultancy/',
  '/services/cost-management-quantity-surveying/',
  '/services/contract-administration-claims/',
  '/services/design-management/',
  '/services/construction-supervision/',
  '/services/project-controls/',
  '/services/pmo-setup/',
  '/services/feasibility-tender-management/',
  '/sectors/buildings/',
  '/sectors/energy/',
  '/sectors/industrial/',
  '/sectors/government/',
];

/** Skip the once-per-session logo intro and pre-answer the cookie banner. */
export async function quietVisit(page: Page) {
  await page.addInitScript(() => {
    sessionStorage.setItem('3p-intro', '1');
    localStorage.setItem('3p-consent', 'essential');
  });
}
