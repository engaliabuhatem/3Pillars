'use client';

import { CircleCheck } from 'lucide-react';
import { useEffect, useRef, useState, type FormEvent } from 'react';
import { Button, ButtonLink } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Feedback';
import { Stepper } from '@/components/ui/Stepper';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import { track } from '@/lib/analytics';
import type { Ref } from '@/lib/cms/types';
import { isEmail, submitForm, trackingFields, type FieldErrors } from '@/lib/forms';
import { Checkbox, ChoiceGroup, FileField, Honeypot, Select, TextArea, TextField } from './Field';
import { Turnstile } from './Turnstile';

const STORAGE_KEY = '3p-proposal-draft';
const MAX_FILE_MB = 10;
const MAX_FILES = 5;
const ACCEPT = '.pdf,.docx,.xlsx,.png,.jpg,.jpeg,.zip';

const EMPTY = {
  name: '',
  email: '',
  phone: '',
  organisation: '',
  organisationType: '',
  role: '',
  country: '',
  projectType: '',
  sector: '',
  services: [] as string[],
  location: '',
  projectStage: '',
  budget: 'undisclosed',
  timeline: '',
  scope: '',
};
type Values = typeof EMPTY;

/** Which fields each step owns, so "Continue" validates only what is on screen. */
const STEP_FIELDS: Array<Array<keyof Values | 'consent'>> = [
  ['name', 'email', 'organisation'],
  ['projectType', 'location', 'projectStage', 'timeline'],
  ['scope'],
  ['consent'],
];

function loadDraft(): Values {
  try {
    const saved = sessionStorage.getItem(STORAGE_KEY);
    return saved ? { ...EMPTY, ...(JSON.parse(saved) as Partial<Values>) } : EMPTY;
  } catch {
    return EMPTY;
  }
}

export function ProposalWizard({ sectors, services, turnstileKey }: { sectors: Ref[]; services: Ref[]; turnstileKey?: string }) {
  const locale = useLocale();
  const t = useDictionary();
  const p = t.proposal;
  const f = t.forms;
  const [step, setStep] = useState(0);
  const [values, setValues] = useState<Values>(EMPTY);
  const [files, setFiles] = useState<File[]>([]);
  const [consent, setConsent] = useState(false);
  const [honeypot, setHoneypot] = useState('');
  const [token, setToken] = useState('');
  const [errors, setErrors] = useState<FieldErrors>({});
  const [status, setStatus] = useState<'editing' | 'sending' | 'sent'>('editing');
  const heading = useRef<HTMLHeadingElement>(null);
  const restored = useRef(false);

  // Restore the draft once, after mount (sessionStorage does not exist on the server).
  useEffect(() => {
    if (restored.current) return;
    restored.current = true;
    const draft = loadDraft();
    if (draft !== EMPTY) queueMicrotask(() => setValues(draft));
  }, []);

  useEffect(() => {
    if (!restored.current) return;
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(values));
    } catch {
      // Storage full or blocked: the form still works, it just won't survive a reload.
    }
  }, [values]);

  const set = <K extends keyof Values>(key: K, value: Values[K]) => setValues((v) => ({ ...v, [key]: value }));
  const text = (key: Exclude<keyof Values, 'services'>) => ({
    name: key,
    value: values[key],
    error: errors[key],
    onChange: (e: { target: { value: string } }) => set(key, e.target.value),
  });

  const validate = (fields: Array<keyof Values | 'consent'>): FieldErrors => {
    const found: FieldErrors = {};
    for (const key of fields) {
      if (key === 'consent') {
        if (!consent) found.consent = f.required;
      } else if (key === 'email') {
        if (!isEmail(values.email)) found.email = f.invalidEmail;
      } else if (key === 'scope') {
        if (values.scope.trim().length < 30) found.scope = f.tooShort(30);
      } else if (!String(values[key]).trim()) {
        found[key] = f.required;
      }
    }
    for (const file of files) if (file.size > MAX_FILE_MB * 1048576) found.attachments = f.fileTooLarge(MAX_FILE_MB);
    return found;
  };

  const goTo = (next: number) => {
    setStep(next);
    setErrors({});
    track('form_step', { form: 'proposal', step: next + 1 });
    requestAnimationFrame(() => heading.current?.focus());
  };

  const next = () => {
    const found = validate(STEP_FIELDS[step] ?? []);
    setErrors(found);
    if (Object.keys(found).length === 0) goTo(step + 1);
  };

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (step < 3) return next();
    const found = validate(STEP_FIELDS.flat());
    setErrors(found);
    if (Object.keys(found).length) return;

    setStatus('sending');
    const body = new FormData();
    for (const [key, value] of Object.entries({ ...values, ...trackingFields(locale) })) {
      if (Array.isArray(value)) value.forEach((v) => body.append(key, v));
      else if (value) body.append(key, value);
    }
    body.append('consent', 'true');
    body.append('website', honeypot);
    if (token) body.append('turnstileToken', token);
    files.forEach((file) => body.append('attachments', file));

    const result = await submitForm('proposal-requests/', body);
    if (result.ok) {
      track('form_submit', { form: 'proposal' });
      try {
        sessionStorage.removeItem(STORAGE_KEY);
      } catch {
        // Nothing to clean up.
      }
      setStatus('sent');
      window.scrollTo({ top: 0 });
      return;
    }
    setErrors(Object.keys(result.errors).length ? result.errors : { form: f.error });
    const firstStep = STEP_FIELDS.findIndex((fields) => fields.some((key) => key in result.errors));
    if (firstStep >= 0) setStep(firstStep);
    setStatus('editing');
  };

  if (status === 'sent') {
    return (
      <div className="tile p-8 md:p-12" role="status">
        <CircleCheck aria-hidden className="size-12 text-green" />
        <h2 className="mt-6 text-h2 font-semibold">{p.successTitle}</h2>
        <p className="mt-4 text-lead text-ink-muted">{p.successBody}</p>
        <ol className="mt-8 grid gap-4">
          {p.next.map((line, i) => (
            <li key={line} className="flex gap-4">
              <span className="grid size-8 shrink-0 place-items-center rounded-pill bg-blue-50 font-semibold text-blue">{i + 1}</span>
              <span className="pt-1">{line}</span>
            </li>
          ))}
        </ol>
        <ButtonLink href="/projects" locale={locale} variant="secondary" arrow className="mt-10">
          {t.common.allProjects}
        </ButtonLink>
      </div>
    );
  }

  const options = <T extends Record<string, string>>(labels: T) => Object.entries(labels).map(([value, label]) => ({ value, label }));

  return (
    <form noValidate onSubmit={submit} className="relative">
      <Stepper steps={p.steps} current={step} caption={p.stepOf(step + 1, p.steps.length)} />
      <h2 ref={heading} tabIndex={-1} className="mb-8 text-h3 font-semibold outline-none">
        {p.steps[step]}
      </h2>
      {Object.keys(errors).length > 0 && (
        <Alert tone="error" className="mb-6">
          {errors.form ?? f.fixErrors}
        </Alert>
      )}

      {step === 0 && (
        <div className="grid gap-6 sm:grid-cols-2">
          <TextField label={f.name} required autoComplete="name" {...text('name')} />
          <TextField label={f.email} required type="email" autoComplete="email" dir="ltr" {...text('email')} />
          <TextField label={f.organisation} required autoComplete="organization" {...text('organisation')} />
          <TextField label={f.organisationType} {...text('organisationType')} />
          <TextField label={f.role} autoComplete="organization-title" {...text('role')} />
          <TextField label={f.phone} type="tel" autoComplete="tel" dir="ltr" {...text('phone')} />
          <TextField label={f.country} autoComplete="country-name" {...text('country')} wrapperClassName="sm:col-span-2" />
        </div>
      )}

      {step === 1 && (
        <div className="grid gap-8">
          <div className="grid gap-6 sm:grid-cols-2">
            <TextField label={p.projectType} hint={p.projectTypeHint} required {...text('projectType')} />
            <TextField label={p.location} required {...text('location')} />
            <Select label={p.sector} placeholder="—" options={sectors.map((s) => ({ value: s.slug, label: s.name }))} {...text('sector')} />
            <Select label={p.budget} required options={options(p.budgets)} {...text('budget')} />
          </div>
          {services.length > 0 && (
            <ChoiceGroup
              legend={p.services}
              name="services"
              multiple
              value={values.services}
              onChange={(v) => set('services', v as string[])}
              options={services.map((s) => ({ value: s.slug, label: s.name }))}
            />
          )}
          <ChoiceGroup legend={p.stage} name="projectStage" required value={values.projectStage} error={errors.projectStage} onChange={(v) => set('projectStage', v as string)} options={options(p.stages)} />
          <ChoiceGroup legend={p.timeline} name="timeline" required value={values.timeline} error={errors.timeline} onChange={(v) => set('timeline', v as string)} options={options(p.timelines)} />
        </div>
      )}

      {step === 2 && (
        <div className="grid gap-8">
          <TextArea label={p.scope} hint={p.scopeHint} required rows={8} {...text('scope')} />
          <FileField
            label={p.attachments}
            hint={f.fileType('PDF, DOCX, XLSX, PNG, JPG, ZIP')}
            files={files}
            onFiles={(picked) => setFiles(picked.slice(0, MAX_FILES))}
            accept={ACCEPT}
            multiple
            error={errors.attachments}
          />
        </div>
      )}

      {step === 3 && (
        <div className="grid gap-8">
          <Review values={values} files={files} sectors={sectors} services={services} onEdit={goTo} />
          <Checkbox label={f.consent} checked={consent} onChange={(e) => setConsent(e.target.checked)} error={errors.consent} />
          {turnstileKey && <Turnstile siteKey={turnstileKey} onToken={setToken} />}
        </div>
      )}

      <Honeypot value={honeypot} onChange={setHoneypot} />
      <p className="mt-8 text-caption text-ink-muted">{p.saved}</p>
      <div className="mt-6 flex flex-wrap justify-between gap-3 border-t border-hairline pt-6">
        {step > 0 ? (
          <Button variant="secondary" onClick={() => goTo(step - 1)}>
            {p.back}
          </Button>
        ) : (
          <span />
        )}
        <Button type="submit" size="lg" disabled={status === 'sending'}>
          {status === 'sending' ? f.sending : step < 3 ? p.continue : p.submit}
        </Button>
      </div>
    </form>
  );
}

function Review({
  values,
  files,
  sectors,
  services,
  onEdit,
}: {
  values: Values;
  files: File[];
  sectors: Ref[];
  services: Ref[];
  onEdit: (step: number) => void;
}) {
  const t = useDictionary();
  const p = t.proposal;
  const f = t.forms;
  const nameOf = (list: Ref[], slug: string) => list.find((item) => item.slug === slug)?.name ?? slug;
  const groups: Array<{ step: number; rows: Array<[string, string]> }> = [
    { step: 0, rows: [[f.name, values.name], [f.email, values.email], [f.organisation, values.organisation], [f.phone, values.phone], [f.country, values.country]] },
    {
      step: 1,
      rows: [
        [p.projectType, values.projectType],
        [p.location, values.location],
        [p.sector, values.sector ? nameOf(sectors, values.sector) : ''],
        [p.services, values.services.map((s) => nameOf(services, s)).join(', ')],
        [p.stage, p.stages[values.projectStage as keyof typeof p.stages] ?? ''],
        [p.budget, p.budgets[values.budget as keyof typeof p.budgets] ?? ''],
        [p.timeline, p.timelines[values.timeline as keyof typeof p.timelines] ?? ''],
      ],
    },
    { step: 2, rows: [[p.scope, values.scope], [p.attachments, files.map((file) => file.name).join(', ')]] },
  ];

  return (
    <div className="grid gap-4">
      {groups.map((group) => (
        <section key={group.step} className="tile p-6 md:p-8">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="font-semibold">{p.steps[group.step]}</h3>
            <Button variant="ghost" onClick={() => onEdit(group.step)}>
              {p.edit}
            </Button>
          </div>
          <dl className="grid gap-3 text-[0.9375rem] sm:grid-cols-[12rem_1fr]">
            {group.rows
              .filter(([, value]) => value)
              .map(([label, value]) => (
                <div key={label} className="contents">
                  <dt className="text-ink-muted">{label}</dt>
                  <dd className="whitespace-pre-line">{value}</dd>
                </div>
              ))}
          </dl>
        </section>
      ))}
    </div>
  );
}
