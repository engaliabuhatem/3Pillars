'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { useTransition } from 'react';
import { Select } from '@/components/forms/Field';
import { Button } from '@/components/ui/Button';
import { useDictionary } from '@/i18n/LocaleProvider';
import type { ProjectList } from '@/lib/cms/types';

const KEYS = ['sector', 'service', 'role', 'type'] as const;

/**
 * Filters live in the URL, so a filtered list can be shared, bookmarked and
 * rendered on the server. Changing one replaces the query and drops paging.
 * Each filter offers only values that at least one visible project has.
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
          label={t.filters.role}
          required
          placeholder={t.filters.all}
          value={params.get('role') ?? ''}
          onChange={(e) => set('role', e.target.value)}
          options={facets.roles.map((r) => ({ value: r.value, label: t.project.roles[r.value] ?? r.label }))}
        />
        <Select
          label={t.filters.type}
          required
          placeholder={t.filters.all}
          value={params.get('type') ?? ''}
          onChange={(e) => set('type', e.target.value)}
          options={facets.types.map((r) => ({ value: r.value, label: t.filters.types[r.value] ?? r.label }))}
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
