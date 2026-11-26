import { Icon } from '@/components/ui/Icon';
import { SmartLink } from '@/components/ui/SmartLink';
import type { Locale } from '@/i18n/config';
import type { Navigation, NavItem } from '@/lib/cms/types';

/**
 * The dropdown under a header item: the full list of services or sectors when
 * the item is set as a mega menu in the admin, otherwise its child links.
 */
export function MegaMenu({ item, mega, locale }: { item: NavItem; mega: Navigation['mega']; locale: Locale }) {
  const base = item.megaMenu === 'services' ? '/services' : '/sectors';
  const entries =
    item.megaMenu === ''
      ? item.children.map((child) => ({ key: child.link, href: child.link, name: child.label, summary: '', icon: '' }))
      : mega[item.megaMenu].map((entry) => ({
          key: entry.slug,
          href: `${base}/${entry.slug}/`,
          name: entry.name,
          summary: 'focusSummary' in entry ? entry.focusSummary : entry.summary,
          icon: entry.icon,
        }));

  return (
    <div className="absolute start-1/2 top-full z-50 w-[min(44rem,90vw)] -translate-x-1/2 pt-3 rtl:translate-x-1/2">
      <div className="rounded-lg bg-surface p-3 text-navy shadow-3 ring-1 ring-hairline ring-inset">
        <ul className="grid grid-cols-2 gap-1">
          {entries.map((entry) => (
            <li key={entry.key}>
              <SmartLink href={entry.href} locale={locale} className="flex gap-3 rounded-md p-3 transition-colors duration-fast hover:bg-navy-50">
                {entry.icon && <Icon name={entry.icon} className="mt-0.5 size-5 shrink-0 text-blue" />}
                <span>
                  <span className="block font-semibold">{entry.name}</span>
                  {entry.summary && <span className="mt-0.5 line-clamp-2 block text-caption text-ink-muted">{entry.summary}</span>}
                </span>
              </SmartLink>
            </li>
          ))}
        </ul>
        {item.megaMenu && (
          <SmartLink href={item.link} locale={locale} className="mt-2 flex min-h-11 items-center rounded-md px-3 font-semibold text-blue hover:bg-blue-50">
            {item.label} →
          </SmartLink>
        )}
      </div>
    </div>
  );
}
