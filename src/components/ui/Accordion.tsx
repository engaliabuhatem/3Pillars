import { Plus } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AccordionItem {
  question: string;
  answer: string;
}

/**
 * Native <details>: keyboard, screen reader and find-in-page support come
 * free, and it works before (or without) JavaScript. `name` makes the group
 * exclusive in browsers that support it.
 */
export function Accordion({ items, name, className }: { items: AccordionItem[]; name: string; className?: string }) {
  return (
    <div className={cn('divide-y divide-hairline border-y border-hairline on-navy:divide-hairline-inverse on-navy:border-hairline-inverse', className)}>
      {items.map((item) => (
        <details key={item.question} name={name} className="group">
          <summary className="flex min-h-14 cursor-pointer list-none items-center justify-between gap-6 py-5 text-lg font-semibold [&::-webkit-details-marker]:hidden">
            {item.question}
            <Plus
              aria-hidden
              className="size-5 shrink-0 text-blue transition-transform duration-base ease-out-expo group-open:rotate-45 on-navy:text-blue-200"
            />
          </summary>
          <div className="max-w-prose pb-6 text-ink-muted on-navy:text-ink-inverse-muted">
            {item.answer.split(/\n+/).map((p) => (
              <p key={p} className="mb-3 last:mb-0">
                {p}
              </p>
            ))}
          </div>
        </details>
      ))}
    </div>
  );
}
