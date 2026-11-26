import { expect, test } from '@playwright/test';
import { quietVisit } from './helpers';

/*
 * These submit real records to the CMS from e2e@example.com, so they are easy
 * to find and delete. Run against development or staging only.
 */

test.beforeEach(async ({ page }) => quietVisit(page));

const PDF = { name: 'brief.pdf', mimeType: 'application/pdf', buffer: Buffer.from('%PDF-1.7\n%e2e\n') };

test('contact form: the document’s fields, validated, then submitted', async ({ page }) => {
  await page.goto('/en/contact/');
  const submit = page.getByRole('button', { name: 'Submit Enquiry' });
  await submit.click();
  await expect(page.getByRole('alert').filter({ hasText: 'check the highlighted fields' })).toBeVisible();
  for (const label of ['Full Name', 'Organisation', 'Business Email', 'Country / Location']) {
    await expect(page.getByLabel(label, { exact: false }).first(), label).toHaveAttribute('aria-invalid', 'true');
  }

  await page.getByLabel('Full Name').fill('E2E Contact');
  await page.getByLabel('Organisation').fill('E2E Authority');
  await page.getByLabel('Business Email').fill('e2e@example.com');
  await page.getByLabel('Country / Location').fill('Jordan');
  await page.getByLabel('Area of Interest').selectOption('pmo_controls');
  await page.getByLabel('Project or Enquiry Summary').fill('An end-to-end test message, please ignore.');
  await page.getByLabel(/I agree/).check();
  await submit.click();
  await expect(page.getByRole('status').filter({ hasText: 'Our team will review your enquiry' })).toBeVisible();
});

test('request a consultation: four steps, area of interest, autosave, review, submit', async ({ page }) => {
  await page.goto('/en/contact/request-a-consultation/');
  await expect(page.getByText('Step 1 of 4')).toBeVisible();

  await page.getByRole('button', { name: 'Continue' }).click();
  await expect(page.getByLabel('Full Name')).toHaveAttribute('aria-invalid', 'true');

  await page.getByLabel('Full Name').fill('E2E Consultation');
  await page.getByLabel('Email').fill('e2e@example.com');
  await page.getByLabel('Organisation', { exact: true }).fill('E2E Authority');
  await page.getByRole('button', { name: 'Continue' }).click();

  await expect(page.getByText('Step 2 of 4')).toBeVisible();
  await page.reload();
  // The draft survives a reload (sessionStorage autosave).
  await page.getByRole('button', { name: 'Continue' }).click();
  await expect(page.getByText('Step 2 of 4')).toBeVisible();

  await page.getByText('Business Development', { exact: true }).click();
  await page.getByLabel('Project type').fill('E2E port expansion');
  await page.getByLabel('Project location').fill('Aden');
  await page.getByText('Feasibility', { exact: true }).click();
  await page.getByText('Within 3 months', { exact: true }).click();
  await page.getByRole('button', { name: 'Continue' }).click();

  await page.getByLabel('Describe the scope').fill('End-to-end test: programme management support for a two-phase expansion.');
  await page.locator('input[type=file]').setInputFiles(PDF);
  await expect(page.getByText('brief.pdf')).toBeVisible();
  await page.getByRole('button', { name: 'Continue' }).click();

  await expect(page.getByText('E2E port expansion')).toBeVisible();
  await page.getByLabel(/I agree/).check();
  await page.getByRole('button', { name: 'Submit request' }).click();
  await expect(page.getByRole('heading', { name: 'Request received' })).toBeVisible();
});

test('open application with a CV', async ({ page }) => {
  await page.goto('/en/careers/');
  await page.getByLabel('Full Name').fill('E2E Applicant');
  await page.getByLabel('Email').fill('e2e@example.com');
  await page.locator('input[type=file]').setInputFiles({ ...PDF, name: 'cv.pdf' });
  await page.getByLabel(/I agree/).check();
  await page.getByRole('button', { name: 'Send' }).click();
  await expect(page.getByText('your application has been received')).toBeVisible();
});

test('arabic contact form submits', async ({ page }) => {
  await page.goto('/ar/contact/');
  await page.getByLabel('الاسم الكامل').fill('اختبار آلي');
  await page.getByLabel('الجهة').fill('جهة اختبار');
  await page.getByLabel('البريد الإلكتروني للعمل').fill('e2e@example.com');
  await page.getByLabel('الدولة / الموقع').fill('الأردن');
  await page.getByLabel('مجال الاهتمام').selectOption('other');
  await page.getByLabel('ملخص المشروع أو الاستفسار').fill('رسالة اختبار آلي، يُرجى تجاهلها.');
  await page.getByLabel(/أوافق/).check();
  await page.getByRole('button', { name: 'أرسل الاستفسار' }).click();
  await expect(page.getByRole('status').filter({ hasText: 'سيراجع فريقنا' })).toBeVisible();
});
