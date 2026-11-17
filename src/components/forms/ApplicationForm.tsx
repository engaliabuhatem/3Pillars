'use client';

import { useState, type FormEvent } from 'react';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Feedback';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import { isEmail, submitForm, type FieldErrors } from '@/lib/forms';
import { Checkbox, FileField, Honeypot, TextArea, TextField } from './Field';
import { Turnstile } from './Turnstile';

const MAX_CV_MB = 5;

export function ApplicationForm({ jobSlug, turnstileKey }: { jobSlug?: string; turnstileKey?: string }) {
  const locale = useLocale();
  const t = useDictionary().forms;
  const [values, setValues] = useState({ name: '', email: '', phone: '', linkedin: '', coverNote: '' });
  const [cv, setCv] = useState<File[]>([]);
  const [consent, setConsent] = useState(false);
  const [honeypot, setHoneypot] = useState('');
  const [token, setToken] = useState('');
  const [errors, setErrors] = useState<FieldErrors>({});
  const [state, setState] = useState<'idle' | 'sending' | 'sent'>('idle');

  const field = (name: keyof typeof values) => ({
    name,
    value: values[name],
    error: errors[name],
    onChange: (e: { target: { value: string } }) => setValues((v) => ({ ...v, [name]: e.target.value })),
  });

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const found: FieldErrors = {};
    if (!values.name.trim()) found.name = t.required;
    if (!isEmail(values.email)) found.email = t.invalidEmail;
    const file = cv[0];
    if (!file) found.cv = t.required;
    else if (file.size > MAX_CV_MB * 1048576) found.cv = t.fileTooLarge(MAX_CV_MB);
    else if (!/\.(pdf|docx)$/i.test(file.name)) found.cv = t.fileType('PDF, DOCX');
    if (!consent) found.consent = t.required;
    setErrors(found);
    if (Object.keys(found).length || !file) return;

    setState('sending');
    const body = new FormData();
    Object.entries(values).forEach(([key, value]) => value && body.append(key, value));
    if (jobSlug) body.append('job', jobSlug);
    body.append('cv', file);
    body.append('consent', 'true');
    body.append('locale', locale);
    body.append('website', honeypot);
    if (token) body.append('turnstileToken', token);

    const result = await submitForm('applications/', body);
    if (result.ok) {
      track('form_submit', { form: 'application', job: jobSlug ?? 'open' });
      setState('sent');
      return;
    }
    setErrors(Object.keys(result.errors).length ? result.errors : { form: t.error });
    setState('idle');
  };

  if (state === 'sent') return <Alert tone="success">{t.applicationSent}</Alert>;

  return (
    <form noValidate onSubmit={onSubmit} className="relative grid gap-6">
      {Object.keys(errors).length > 0 && <Alert tone="error">{errors.form ?? t.fixErrors}</Alert>}
      <div className="grid gap-6 sm:grid-cols-2">
        <TextField label={t.name} required autoComplete="name" {...field('name')} />
        <TextField label={t.email} required type="email" autoComplete="email" dir="ltr" {...field('email')} />
        <TextField label={t.phone} type="tel" autoComplete="tel" dir="ltr" {...field('phone')} />
        <TextField label={t.linkedin} type="url" dir="ltr" {...field('linkedin')} />
      </div>
      <FileField label={t.cv} required files={cv} onFiles={setCv} accept=".pdf,.docx" error={errors.cv} />
      <TextArea label={t.coverNote} rows={4} {...field('coverNote')} />
      <Checkbox label={t.consent} checked={consent} onChange={(e) => setConsent(e.target.checked)} error={errors.consent} />
      <Honeypot value={honeypot} onChange={setHoneypot} />
      {turnstileKey && <Turnstile siteKey={turnstileKey} onToken={setToken} />}
      <div>
        <Button type="submit" size="lg" disabled={state === 'sending'}>
          {state === 'sending' ? t.sending : t.submit}
        </Button>
      </div>
    </form>
  );
}
