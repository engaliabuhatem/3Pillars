'use client';

import { Download } from 'lucide-react';
import { useState, type FormEvent } from 'react';
import { Button, buttonClass } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Feedback';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import { isEmail, submitForm, type FieldErrors } from '@/lib/forms';
import { Honeypot, TextField } from './Field';
import { Turnstile } from './Turnstile';

/**
 * The capability statement (or any gated download). Ungated: a plain link.
 * Gated: name, email and company first; the API answers with the file URL.
 */
export function DownloadGate({
  downloadId,
  directUrl,
  turnstileKey,
}: {
  downloadId: number;
  directUrl: string | null;
  turnstileKey?: string;
}) {
  const locale = useLocale();
  const t = useDictionary().forms;
  const [values, setValues] = useState({ name: '', email: '', company: '' });
  const [honeypot, setHoneypot] = useState('');
  const [token, setToken] = useState('');
  const [errors, setErrors] = useState<FieldErrors>({});
  const [url, setUrl] = useState<string | null>(directUrl);
  const [sending, setSending] = useState(false);

  if (url) {
    return (
      <div className="grid gap-4">
        {!directUrl && <Alert tone="success">{t.downloadReady}</Alert>}
        <a
          href={url}
          download
          className={buttonClass('primary', 'lg', 'w-fit')}
          onClick={() => track('download', { id: downloadId })}
        >
          <Download aria-hidden className="size-5" />
          {t.download}
        </a>
      </div>
    );
  }

  const field = (name: keyof typeof values) => ({
    name,
    value: values[name],
    error: errors[name],
    onChange: (e: { target: { value: string } }) => setValues((v) => ({ ...v, [name]: e.target.value })),
  });

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const found: FieldErrors = {};
    if (!values.name.trim()) found.name = t.required;
    if (!isEmail(values.email)) found.email = t.invalidEmail;
    setErrors(found);
    if (Object.keys(found).length) return;
    setSending(true);
    const result = await submitForm<{ url: string }>(`downloads/${downloadId}/lead/`, {
      ...values,
      locale,
      sourcePage: window.location.pathname,
      website: honeypot,
      turnstileToken: token,
    });
    setSending(false);
    if (result.ok) {
      track('download_lead', { id: downloadId });
      setUrl(result.data.url);
    } else {
      setErrors(Object.keys(result.errors).length ? result.errors : { form: t.error });
    }
  };

  return (
    <form noValidate onSubmit={onSubmit} className="relative grid max-w-xl gap-6">
      {errors.form && <Alert tone="error">{errors.form}</Alert>}
      <TextField label={t.name} required autoComplete="name" {...field('name')} />
      <TextField label={t.email} required type="email" autoComplete="email" dir="ltr" {...field('email')} />
      <TextField label={t.company} autoComplete="organization" {...field('company')} />
      <Honeypot value={honeypot} onChange={setHoneypot} />
      {turnstileKey && <Turnstile siteKey={turnstileKey} onToken={setToken} />}
      <div>
        <Button type="submit" size="lg" disabled={sending}>
          {sending ? t.sending : t.getDocument}
        </Button>
      </div>
    </form>
  );
}
