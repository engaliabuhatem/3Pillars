'use client';

import { useState, type FormEvent } from 'react';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Feedback';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import { isEmail, submitForm, trackingFields, type FieldErrors } from '@/lib/forms';
import { Checkbox, ChoiceGroup, Honeypot, TextArea, TextField } from './Field';
import { Turnstile } from './Turnstile';

const TOPICS = ['general', 'consultation', 'partnership', 'media'] as const;

export function ContactForm({ turnstileKey, initialTopic = 'general' }: { turnstileKey?: string; initialTopic?: string }) {
  const locale = useLocale();
  const t = useDictionary().forms;
  const [values, setValues] = useState({ name: '', email: '', organisation: '', phone: '', subject: '', message: '' });
  const [topic, setTopic] = useState(TOPICS.includes(initialTopic as (typeof TOPICS)[number]) ? initialTopic : 'general');
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

  const validate = (): FieldErrors => {
    const found: FieldErrors = {};
    if (!values.name.trim()) found.name = t.required;
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
    const result = await submitForm('enquiries/', {
      ...values,
      topic,
      consent,
      website: honeypot,
      turnstileToken: token,
      ...trackingFields(locale),
    });
    if (result.ok) {
      track('form_submit', { form: 'enquiry', topic });
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
      <ChoiceGroup
        legend={t.topic}
        name="topic"
        required
        value={topic}
        onChange={(v) => setTopic(v as string)}
        options={TOPICS.map((value) => ({ value, label: t.topics[value] }))}
      />
      <div className="grid gap-6 sm:grid-cols-2">
        <TextField label={t.name} required autoComplete="name" {...field('name')} />
        <TextField label={t.email} required type="email" autoComplete="email" dir="ltr" {...field('email')} />
        <TextField label={t.organisation} autoComplete="organization" {...field('organisation')} />
        <TextField label={t.phone} type="tel" autoComplete="tel" dir="ltr" {...field('phone')} />
      </div>
      <TextField label={t.subject} {...field('subject')} />
      <TextArea label={t.message} required {...field('message')} />
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
