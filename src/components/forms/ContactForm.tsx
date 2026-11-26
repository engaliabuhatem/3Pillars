'use client';

import { useState, type FormEvent } from 'react';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Feedback';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import { AREAS_OF_INTEREST, isEmail, submitForm, trackingFields, type FieldErrors } from '@/lib/forms';
import { Checkbox, Honeypot, Select, TextArea, TextField } from './Field';
import { Turnstile } from './Turnstile';

const EMPTY = { name: '', organisation: '', email: '', phone: '', country: '', areaOfInterest: '', message: '' };
type Values = typeof EMPTY;

/**
 * Contact Us, with exactly the fields the content document lists, in its
 * order. The consent wording is editable in Site settings; the version agreed
 * to is stored with the enquiry.
 */
export function ContactForm({ turnstileKey, consentText, submitLabel }: { turnstileKey?: string; consentText?: string; submitLabel?: string }) {
  const locale = useLocale();
  const t = useDictionary().forms;
  const [values, setValues] = useState<Values>(EMPTY);
  const [consent, setConsent] = useState(false);
  const [honeypot, setHoneypot] = useState('');
  const [token, setToken] = useState('');
  const [errors, setErrors] = useState<FieldErrors>({});
  const [state, setState] = useState<'idle' | 'sending' | 'sent'>('idle');

  const field = (name: keyof Values) => ({
    name,
    value: values[name],
    error: errors[name],
    onChange: (e: { target: { value: string } }) => setValues((v) => ({ ...v, [name]: e.target.value })),
  });

  const validate = (): FieldErrors => {
    const found: FieldErrors = {};
    for (const key of ['name', 'organisation', 'country', 'areaOfInterest'] as const) if (!values[key].trim()) found[key] = t.required;
    if (!isEmail(values.email)) found.email = t.invalidEmail;
    if (values.message.trim().length < 10) found.message = t.tooShort(10);
    if (!consent) found.consent = t.required;
    return found;
  };

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const found = validate();
    setErrors(found);
    if (Object.keys(found).length) {
      event.currentTarget.querySelector<HTMLElement>('[aria-invalid="true"]')?.focus();
      return;
    }
    setState('sending');
    const result = await submitForm('enquiries/', { ...values, consent, website: honeypot, turnstileToken: token, ...trackingFields(locale) });
    if (result.ok) {
      track('form_submit', { form: 'enquiry', area: values.areaOfInterest });
      setState('sent');
      return;
    }
    setErrors(Object.keys(result.errors).length ? result.errors : { form: t.error });
    setState('idle');
  };

  if (state === 'sent') return <Alert tone="success">{t.sent}</Alert>;

  return (
    <form noValidate onSubmit={onSubmit} className="relative grid gap-6">
      {Object.keys(errors).length > 0 && <Alert tone="error">{errors.form ?? t.fixErrors}</Alert>}
      <div className="grid gap-6 sm:grid-cols-2">
        <TextField label={t.name} required autoComplete="name" {...field('name')} />
        <TextField label={t.organisation} required autoComplete="organization" {...field('organisation')} />
        <TextField label={t.businessEmail} required type="email" autoComplete="email" dir="ltr" {...field('email')} />
        <TextField label={t.phoneNumber} type="tel" autoComplete="tel" dir="ltr" {...field('phone')} />
        <TextField label={t.country} required autoComplete="country-name" {...field('country')} />
        <Select
          label={t.area}
          required
          placeholder="—"
          options={AREAS_OF_INTEREST.map((value) => ({ value, label: t.areas[value] ?? value }))}
          {...field('areaOfInterest')}
          onChange={(e) => {
            setValues((v) => ({ ...v, areaOfInterest: e.target.value }));
            if (e.target.value) track('area_of_interest', { form: 'enquiry', area: e.target.value });
          }}
        />
      </div>
      <TextArea label={t.message} required {...field('message')} />
      <Checkbox label={consentText || t.consent} required checked={consent} onChange={(e) => setConsent(e.target.checked)} error={errors.consent} />
      <Honeypot value={honeypot} onChange={setHoneypot} />
      {turnstileKey && <Turnstile siteKey={turnstileKey} onToken={setToken} />}
      <div>
        <Button type="submit" size="lg" disabled={state === 'sending'}>
          {state === 'sending' ? t.sending : submitLabel || t.submit}
        </Button>
      </div>
    </form>
  );
}
