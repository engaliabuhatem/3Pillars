import type { ReactNode } from 'react';
import { Logo } from '@/components/brand/Logo';
import { ThreeArcs } from '@/components/brand/ThreeArcs';

/** The navy, three-arc screen behind 404, 500 and coming-soon. */
export function StatusScreen({ code, title, body, children }: { code?: string; title: string; body: string; children?: ReactNode }) {
  return (
    <section data-surface="navy" className="relative isolate flex min-h-svh items-center overflow-hidden bg-navy py-32 text-white">
      <ThreeArcs className="pointer-events-none absolute inset-0 -z-10 size-full" />
      <div className="container-wide">
        <Logo variant="mark" tone="white" className="mb-12 h-20 w-auto" title="" />
        {code && <p className="eyebrow mb-4 text-blue-200">{code}</p>}
        <h1 className="max-w-3xl text-h1 font-semibold text-balance">{title}</h1>
        <p className="mt-6 max-w-xl text-lead text-ink-inverse-muted">{body}</p>
        {children && <div className="mt-10 flex flex-wrap gap-3">{children}</div>}
      </div>
    </section>
  );
}
