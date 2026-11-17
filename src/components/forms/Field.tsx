'use client';

import { Paperclip, X } from 'lucide-react';
import {
  useId,
  type ChangeEvent,
  type InputHTMLAttributes,
  type ReactNode,
  type SelectHTMLAttributes,
  type TextareaHTMLAttributes,
} from 'react';
import { useDictionary } from '@/i18n/LocaleProvider';
import { cn } from '@/lib/utils';

const CONTROL =
  'block w-full rounded-md bg-surface px-4 py-3 text-base text-ink ring-1 ring-hairline-strong ring-inset ' +
  'placeholder:text-grey-400 transition-shadow duration-fast ' +
  'hover:ring-grey-400 focus:ring-2 focus:ring-blue focus:outline-none ' +
  'aria-invalid:ring-2 aria-invalid:ring-danger disabled:cursor-not-allowed disabled:bg-grey-50 disabled:text-grey-500';

interface WrapperProps {
  id: string;
  label: string;
  hint?: string;
  error?: string;
  required?: boolean;
  children: ReactNode;
  className?: string;
}

/** Label, control, hint and error, wired together with ids for screen readers. */
function FieldWrapper({ id, label, hint, error, required, children, className }: WrapperProps) {
  const t = useDictionary().forms;
  return (
    <div className={cn('flex flex-col gap-2', className)}>
      <label htmlFor={id} className="text-[0.9375rem] font-semibold">
        {label}
        {!required && <span className="ms-1.5 font-normal text-ink-muted">({t.optional})</span>}
      </label>
      {children}
      {hint && (
        <p id={`${id}-hint`} className="text-caption text-ink-muted">
          {hint}
        </p>
      )}
      {error && (
        <p id={`${id}-error`} className="text-caption font-semibold text-danger">
          {error}
        </p>
      )}
    </div>
  );
}

function describedBy(id: string, hint?: string, error?: string) {
  return [hint && `${id}-hint`, error && `${id}-error`].filter(Boolean).join(' ') || undefined;
}

type Common = { label: string; hint?: string; error?: string; wrapperClassName?: string };

export function TextField({ label, hint, error, wrapperClassName, required, className, ...rest }: Common & InputHTMLAttributes<HTMLInputElement>) {
  const id = useId();
  return (
    <FieldWrapper id={id} label={label} hint={hint} error={error} required={required} className={wrapperClassName}>
      <input
        id={id}
        required={required}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy(id, hint, error)}
        className={cn(CONTROL, 'min-h-12', className)}
        {...rest}
      />
    </FieldWrapper>
  );
}

export function TextArea({ label, hint, error, wrapperClassName, required, className, ...rest }: Common & TextareaHTMLAttributes<HTMLTextAreaElement>) {
  const id = useId();
  return (
    <FieldWrapper id={id} label={label} hint={hint} error={error} required={required} className={wrapperClassName}>
      <textarea
        id={id}
        required={required}
        rows={5}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy(id, hint, error)}
        className={cn(CONTROL, 'resize-y', className)}
        {...rest}
      />
    </FieldWrapper>
  );
}

interface Option {
  value: string;
  label: string;
}

export function Select({
  label,
  hint,
  error,
  wrapperClassName,
  required,
  options,
  placeholder,
  className,
  ...rest
}: Common & SelectHTMLAttributes<HTMLSelectElement> & { options: Option[]; placeholder?: string }) {
  const id = useId();
  return (
    <FieldWrapper id={id} label={label} hint={hint} error={error} required={required} className={wrapperClassName}>
      <select
        id={id}
        required={required}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy(id, hint, error)}
        className={cn(
          CONTROL,
          'min-h-12 appearance-none bg-[length:1rem] bg-[position:right_1rem_center] bg-no-repeat pe-10 rtl:bg-[position:left_1rem_center]',
          "bg-[url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%235C5E60' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E\")]",
          className,
        )}
        {...rest}
      >
        {placeholder !== undefined && <option value="">{placeholder}</option>}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </FieldWrapper>
  );
}

export function Checkbox({ label, error, className, ...rest }: { label: ReactNode; error?: string } & InputHTMLAttributes<HTMLInputElement>) {
  const id = useId();
  return (
    <div className={cn('flex flex-col gap-2', className)}>
      <div className="flex items-start gap-3">
        <input
          id={id}
          type="checkbox"
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? `${id}-error` : undefined}
          className="mt-0.5 size-5 shrink-0 cursor-pointer rounded-sm accent-blue"
          {...rest}
        />
        <label htmlFor={id} className="cursor-pointer text-[0.9375rem]">
          {label}
        </label>
      </div>
      {error && (
        <p id={`${id}-error`} className="text-caption font-semibold text-danger">
          {error}
        </p>
      )}
    </div>
  );
}

/** Pill choices for small option sets (topic, stage). Radios underneath. */
export function ChoiceGroup({
  legend,
  name,
  options,
  value,
  onChange,
  error,
  multiple,
  required,
}: {
  legend: string;
  name: string;
  options: Option[];
  value: string | string[];
  onChange: (value: string | string[]) => void;
  error?: string;
  multiple?: boolean;
  required?: boolean;
}) {
  const id = useId();
  const t = useDictionary().forms;
  const selected = Array.isArray(value) ? value : [value];
  const toggle = (option: string) => {
    if (!multiple) return onChange(option);
    onChange(selected.includes(option) ? selected.filter((v) => v !== option) : [...selected, option]);
  };
  return (
    <fieldset aria-describedby={error ? `${id}-error` : undefined} className="flex flex-col gap-3">
      <legend className="mb-3 text-[0.9375rem] font-semibold">
        {legend}
        {!required && <span className="ms-1.5 font-normal text-ink-muted">({t.optional})</span>}
      </legend>
      <div className="flex flex-wrap gap-2">
        {options.map((option) => (
          <label
            key={option.value}
            className={cn(
              'inline-flex min-h-11 cursor-pointer items-center rounded-pill px-4 text-[0.9375rem] ring-1 ring-inset transition-colors duration-fast',
              'has-focus-visible:outline-2 has-focus-visible:outline-offset-2 has-focus-visible:outline-blue',
              selected.includes(option.value) ? 'bg-navy text-white ring-navy' : 'bg-surface ring-hairline-strong hover:ring-blue',
            )}
          >
            <input
              type={multiple ? 'checkbox' : 'radio'}
              name={name}
              value={option.value}
              checked={selected.includes(option.value)}
              onChange={() => toggle(option.value)}
              className="sr-only"
            />
            {option.label}
          </label>
        ))}
      </div>
      {error && (
        <p id={`${id}-error`} className="text-caption font-semibold text-danger">
          {error}
        </p>
      )}
    </fieldset>
  );
}

export function FileField({
  label,
  hint,
  error,
  files,
  onFiles,
  accept,
  multiple,
  required,
}: {
  label: string;
  hint?: string;
  error?: string;
  files: File[];
  onFiles: (files: File[]) => void;
  accept: string;
  multiple?: boolean;
  required?: boolean;
}) {
  const id = useId();
  const t = useDictionary().forms;
  const add = (event: ChangeEvent<HTMLInputElement>) => {
    const picked = Array.from(event.target.files ?? []);
    onFiles(multiple ? [...files, ...picked] : picked.slice(0, 1));
    event.target.value = '';
  };
  return (
    <FieldWrapper id={id} label={label} hint={hint} error={error} required={required}>
      <div className="flex flex-col gap-3">
        <label
          className={cn(
            'inline-flex min-h-12 w-fit cursor-pointer items-center gap-2 rounded-md bg-surface px-5 font-semibold text-navy ring-1 ring-hairline-strong ring-inset',
            'hover:ring-blue has-focus-visible:outline-2 has-focus-visible:outline-offset-2 has-focus-visible:outline-blue',
          )}
        >
          <Paperclip aria-hidden className="size-4" />
          {t.chooseFile}
          <input
            id={id}
            type="file"
            accept={accept}
            multiple={multiple}
            onChange={add}
            className="sr-only"
            aria-invalid={error ? true : undefined}
            aria-describedby={describedBy(id, hint, error)}
          />
        </label>
        {files.length === 0 ? (
          <span className="text-caption text-ink-muted">{t.noFile}</span>
        ) : (
          <ul className="flex flex-col gap-2">
            {files.map((file, i) => (
              <li key={`${file.name}-${i}`} className="flex items-center justify-between gap-3 rounded-md bg-navy-50 px-4 py-2 text-[0.9375rem]">
                <span className="truncate">
                  {file.name} <span className="text-ink-muted">({(file.size / 1048576).toFixed(1)} MB)</span>
                </span>
                <button
                  type="button"
                  onClick={() => onFiles(files.filter((_, j) => j !== i))}
                  className="grid size-11 place-items-center rounded-pill text-ink-muted hover:text-danger"
                  aria-label={`${t.remove} ${file.name}`}
                >
                  <X aria-hidden className="size-4" />
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </FieldWrapper>
  );
}

/** Off-screen honeypot: people never see or reach it; naive bots fill it in. */
export function Honeypot({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <div aria-hidden className="pointer-events-none absolute size-px overflow-hidden opacity-0 [clip-path:inset(50%)]">
      <label>
        Website
        <input type="text" name="website" tabIndex={-1} autoComplete="off" value={value} onChange={(e) => onChange(e.target.value)} />
      </label>
    </div>
  );
}
