import { ArrowRight } from 'lucide-react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';
import type { Locale } from '@/i18n/config';
import { cn } from '@/lib/utils';
import { SmartLink } from './SmartLink';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'inverse' | 'inverse-outline';
type Size = 'md' | 'lg';

const BASE =
  'group/button inline-flex min-h-11 items-center justify-center gap-2 rounded-md font-semibold whitespace-nowrap ' +
  'transition-[background-color,color,box-shadow,transform] duration-fast ease-out-expo active:scale-[0.98] ' +
  'disabled:pointer-events-none disabled:opacity-50';

const VARIANTS: Record<ButtonVariant, string> = {
  primary: 'bg-blue text-white shadow-1 hover:bg-blue-700 hover:shadow-2',
  secondary: 'bg-surface text-navy ring-1 ring-hairline-strong ring-inset hover:ring-blue hover:text-blue',
  ghost: 'text-blue hover:bg-blue-50',
  inverse: 'bg-white text-navy hover:bg-blue-50',
  'inverse-outline': 'text-white ring-1 ring-white/40 ring-inset hover:bg-white/10 hover:ring-white',
};

const SIZES: Record<Size, string> = {
  md: 'px-5 py-2.5 text-[0.9375rem]',
  lg: 'px-7 py-3.5 text-base',
};

export function buttonClass(variant: ButtonVariant = 'primary', size: Size = 'md', className?: string) {
  return cn(BASE, VARIANTS[variant], SIZES[size], className);
}

/** Directional arrow that mirrors in RTL and nudges toward the reading direction on hover. */
export function ArrowIcon({ className }: { className?: string }) {
  return (
    <ArrowRight
      aria-hidden
      className={cn(
        'size-4 shrink-0 transition-transform duration-base ease-out-expo rtl:-scale-x-100',
        'group-hover/button:translate-x-0.5 rtl:group-hover/button:-translate-x-0.5',
        className,
      )}
    />
  );
}

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: Size;
}

export function Button({ variant = 'primary', size = 'md', className, type = 'button', ...rest }: ButtonProps) {
  return <button type={type} className={buttonClass(variant, size, className)} {...rest} />;
}

interface ButtonLinkProps {
  href: string;
  locale: Locale;
  children: ReactNode;
  variant?: ButtonVariant;
  size?: Size;
  arrow?: boolean;
  className?: string;
  /** Analytics event name, read by the analytics click listener. */
  track?: string;
}

export function ButtonLink({ href, locale, children, variant = 'primary', size = 'md', arrow, className, track }: ButtonLinkProps) {
  return (
    <SmartLink href={href} locale={locale} className={buttonClass(variant, size, className)} data-track={track}>
      {children}
      {arrow && <ArrowIcon />}
    </SmartLink>
  );
}
