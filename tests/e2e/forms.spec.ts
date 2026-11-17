import { expect, test } from '@playwright/test';
import { quietVisit } from './helpers';

/*
 * These submit real records to the CMS, marked "E2E" so they are easy to find
 * and delete. Run against development or staging only.
 */

test.beforeEach(async ({ page }) => quietVisit(page));

const PDF = { name: 'brief.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.7\n%e2e\n') };

test('contact form validates, then submits', async ({ page }) => {
  await page.goto('/en/contact');
  await page.getByRole('button', { name: 'Send' }).click();
  await expect(page.getByRole('alert').filter({ hasText: 'check the highlighted fields' })).toBeVisible();
  await expect(page.getByLabel('Full name')).toHaveAttribute('aria-invalid', 'true');

  await page.getByLabel('Full name').fill('E2E Contact');
  await page.getByLabel('Email').fill('e2e@example.com');
  await page.getByLabel('Message').fill('An end-to-end test message, please ignore.');
  await page.getByLabel(/I agree/).check();
  await page.getByRole('button', { name: 'Send' }).click();
  await expect(page.getByRole('status').filter({ hasText: 'received your message' })).toBeVisible();
});

test('proposal request: four steps, autosave, review, submit', async ({ page }) => {
  await page.goto('/en/request-a-proposal');
  await expect(page.getByText('Step 1 of 4')).toBeVisible();

  await page.getByRole('button', { name: 'Continue' }).click();
  await expect(page.getByLabel('Full name')).toHaveAttribute('aria-invalid', 'true');

  await page.getByLabel('Full name').fill('E2E Proposal');
  await page.getByLabel('Email').fill('e2e@example.com');
  await page.getByLabel('Organisation', { exact: true }).fill('E2E Authority');
  await page.getByRole('button', { name: 'Continue' }).click();

  await expect(page.getByText('Step 2 of 4')).toBeVisible();
  await page.reload();
  // The draft survives a reload (sessionStorage autosave).
  await page.getByRole('button', { name: 'Continue' }).click();
  await expect(page.getByText('Step 2 of 4')).toBeVisible();

  await page.getByLabel('Project type').fill('E2E terminal expansion');
  await page.getByLabel('Project location').fill('Aden');
  await page.getByText('Feasibility', { exact: true }).click();
  await page.getByText('Within 3 months', { exact: true }).click();
  await page.getByRole('button', { name: 'Continue' }).click();

  await page.getByLabel('Describe the scope').fill('End-to-end test: project management consultancy for a two-phase expansion.');
  await page.locator('input[type=file]').setInputFiles(PDF);
  await expect(page.getByText('brief.pdf')).toBeVisible();
  await page.getByRole('button', { name: 'Continue' }).click();

  await expect(page.getByText('E2E terminal expansion')).toBeVisible();
  await page.getByLabel(/I agree/).check();
  await page.getByRole('button', { name: 'Submit request' }).click();
  await expect(page.getByRole('heading', { name: 'Request received' })).toBeVisible();
});

test('open application with a CV', async ({ page }) => {
  await page.goto('/en/careers');
  await page.getByLabel('Full name').fill('E2E Applicant');
  await page.getByLabel('Email').fill('e2e@example.com');
  await page.locator('input[type=file]').setInputFiles({ ...PDF, name: 'cv.pdf' });
  await page.getByLabel(/I agree/).check();
  await page.getByRole('button', { name: 'Send' }).click();
  await expect(page.getByText('your application has been received')).toBeVisible();
});

test('arabic contact form submits', async ({ page }) => {
  await page.goto('/ar/contact');
  await page.getByLabel('الاسم الكامل').fill('اختبار آلي');
  await page.getByLabel('البريد الإلكتروني').fill('e2e@example.com');
  await page.getByLabel('الرسالة').fill('رسالة اختبار آلي، يُرجى تجاهلها.');
  await page.getByLabel(/أوافق/).check();
  await page.getByRole('button', { name: 'إرسال' }).click();
  await expect(page.getByRole('status').filter({ hasText: 'استلمنا رسالتك' })).toBeVisible();
});
