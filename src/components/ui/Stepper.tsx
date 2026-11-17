import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';

/**
 * Form progress as three-pillar bars: each step a bar that fills as it is
 * reached. The text "Step 2 of 4" is the accessible source of truth.
 */
export function Stepper({ steps, current, caption }: { steps: string[]; current: number; caption: string }) {
  return (
    <nav aria-label={caption} className="mb-10">
      <p className="mb-4 text-caption font-semibold text-ink-muted">{caption}</p>
      <ol className="grid gap-3" style={{ gridTemplateColumns: `repeat(${steps.length}, minmax(0, 1fr))` }}>
        {steps.map((step, i) => {
          const done = i < current;
          const active = i === current;
          return (
            <li key={step} aria-current={active ? 'step' : undefined} className="flex flex-col gap-2">
              <span className="h-1 overflow-hidden rounded-pill bg-navy-100">
                <span
                  className={cn(
                    'block h-full origin-left rounded-pill bg-blue transition-transform duration-slow ease-out-expo rtl:origin-right',
                    done || active ? 'scale-x-100' : 'scale-x-0',
                    done && 'bg-green',
                  )}
                />
              </span>
              <span className={cn('flex items-center gap-1.5 text-caption', active ? 'font-semibold text-navy' : 'text-ink-muted')}>
                {done && <Check aria-hidden className="size-3.5 text-green" />}
                <span className="max-sm:sr-only">{step}</span>
              </span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
