import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { LineReveal } from '../motion/LineReveal';
import { Reveal } from '../motion/Reveal';

/** The tracked-caps "PROJECT" treatment from the logo, used above titles. */
export function Eyebrow({ children, className }: { children: ReactNode; className?: string }) {
  return <p className={cn('eyebrow text-blue on-navy:text-blue-200', className)}>{children}</p>;
}

interface SectionHeadingProps {
  id?: string;
  eyebrow?: string;
  title: string;
  intro?: string;
  as?: 'h1' | 'h2';
  align?: 'start' | 'center';
  size?: 'display' | 'h1' | 'h2';
  action?: ReactNode;
  className?: string;
}

const SIZES = { display: 'text-display', h1: 'text-h1', h2: 'text-h2' } as const;

export function SectionHeading({
  id,
  eyebrow,
  title,
  intro,
  as: Tag = 'h2',
  align = 'start',
  size = Tag === 'h1' ? 'h1' : 'h2',
  action,
  className,
}: SectionHeadingProps) {
  return (
    <header
      className={cn(
        'mb-12 flex flex-col gap-6 md:mb-16 md:flex-row md:items-end md:justify-between',
        align === 'center' && 'items-center text-center md:flex-col md:items-center',
        className,
      )}
    >
      <div className={cn('max-w-3xl', align === 'center' && 'mx-auto')}>
        {eyebrow && (
          <Reveal>
            <Eyebrow className="mb-4">{eyebrow}</Eyebrow>
          </Reveal>
        )}
        <Tag id={id} className={cn(SIZES[size], 'font-semibold text-balance')}>
          <LineReveal text={title} />
        </Tag>
        {intro && (
          <Reveal delay={0.12}>
            <p className="mt-5 max-w-prose text-lead text-ink-muted on-navy:text-ink-inverse-muted">{intro}</p>
          </Reveal>
        )}
      </div>
      {action && <Reveal delay={0.18}>{action}</Reveal>}
    </header>
  );
}
