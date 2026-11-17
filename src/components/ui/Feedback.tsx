import { CircleExclamationPoint, Info } from 'lucide-react';
import type { ReactNode } from 'react';
import { cn } from '@/lib/utils';

export function Skeleton({ className }: { className?: string }) {
  return <div aria-hidden className={cn('animate-pulse rounded-md bg-navy-100/70', className)} />;
}

export function EmptyState({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div className={cn('flex items-start gap-3 rounded-lg bg-surface p-8 text-ink-muted ring-1 ring-hairline ring-inset', className)}>
      <Info aria-hidden className="mt-1 size-5 shrink-0 text-blue" />
      <p>{children}</p>
    </div>
  );
}

export function Alert({ tone, children, className }: { tone: 'error' | 'success'; children: ReactNode; className?: string }) {
  return (
    <div
      role={tone === 'error' ? 'alert' : 'status'}
      className={cn(
        'flex items-start gap-3 rounded-md p-4 text-[0.9375rem]',
        tone === 'error' ? 'bg-danger-50 text-danger' : 'bg-green-50 text-green-700',
        className,
      )}
    >
      {tone === 'error' ? <CircleExclamationPoint aria-hidden className="mt-0.5 size-5 shrink-0" /> : <Info aria-hidden className="mt-0.5 size-5 shrink-0" />}
      <div>{children}</div>
    </div>
  );
}
