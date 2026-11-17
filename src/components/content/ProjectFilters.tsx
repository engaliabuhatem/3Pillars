'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { useTransition } from 'react';
import { Select } from '@/components/forms/Field';
import { Button } from '@/components/ui/Button';
import { useDictionary } from '@/i18n/LocaleProvider';
import type { ProjectList } from '@/lib/cms/types';

const KEYS = ['sector', 'service', 'country', 'status'] as const;

/**
 * Filters live in the URL, so a filtered list can be shared, bookmarked and
 * rendered on the server. Changing one replaces the query and drops paging.
 */
export function ProjectFilters({ facets, count }: { facets: ProjectList['facets']; count: number }) {
  const t = useDictionary();
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const [pending, startTransition] = useTransition();

  const set = (key: (typeof KEYS)[number], value: string) => {
    const next = new URLSearchParams(params.toString());
    if (value) next.set(key, value);
    else next.delete(key);
    next.delete('page');
    startTransition(() => router.replace(`${pathname}${next.size ? `?${next}` : ''}`, { scroll: false }));
  };
  const active = KEYS.some((key) => params.get(key));

  return (
    <div className="tile mb-10 p-5 md:p-7" aria-busy={pending}>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Select
          label={t.filters.sector}
          required
          placeholder={t.filters.all}
          value={params.get('sector') ?? ''}
          onChange={(e) => set('sector', e.target.value)}
          options={facets.sectors.map((s) => ({ value: s.slug, label: s.name }))}
        />
        <Select
          label={t.filters.service}
          required
          placeholder={t.filters.all}
          value={params.get('service') ?? ''}
          onChange={(e) => set('service', e.target.value)}
          options={facets.services.map((s) => ({ value: s.slug, label: s.name }))}
        />
        <Select
          label={t.filters.country}
          required
          placeholder={t.filters.all}
          value={params.get('country') ?? ''}
          onChange={(e) => set('country', e.target.value)}
          options={facets.countries.map((c) => ({ value: c, label: c }))}
        />
        <Select
          label={t.filters.status}
          required
          placeholder={t.filters.all}
          value={params.get('status') ?? ''}
          onChange={(e) => set('status', e.target.value)}
          options={[
            { value: 'ongoing', label: t.project.ongoing },
            { value: 'completed', label: t.project.completed },
          ]}
        />
      </div>
      <div className="mt-5 flex items-center justify-between gap-4">
        <p role="status" className="text-caption font-semibold text-ink-muted">
          {t.filters.results(count)}
        </p>
        {active && (
          <Button variant="ghost" onClick={() => startTransition(() => router.replace(pathname, { scroll: false }))}>
            {t.filters.clear}
          </Button>
        )}
      </div>
    </div>
  );
}
