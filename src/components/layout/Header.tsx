'use client';

import { ChevronDown, Menu, X } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Suspense, useEffect, useRef, useState } from 'react';
import { Logo } from '@/components/brand/Logo';
import { buttonClass } from '@/components/ui/Button';
import { SmartLink } from '@/components/ui/SmartLink';
import { useDictionary, useLocale } from '@/i18n/LocaleProvider';
import type { Navigation, NavItem } from '@/lib/cms/types';
import { cn, localize } from '@/lib/utils';
import { LanguageSwitch } from './LanguageSwitch';
import { MegaMenu } from './MegaMenu';

/**
 * A slim translucent bar that recedes while reading (hides on scroll down)
 * and returns the moment you scroll up. Over a dark hero it switches to its
 * inverse look until the page scrolls past the hero.
 */
export function Header({
  navigation,
  shortName,
  ctaLabel,
  homeStartsDark,
}: {
  navigation: Navigation;
  shortName: string;
  ctaLabel: string;
  /** The home page opens on the navy video hero, so the bar starts in its inverse look there. */
  homeStartsDark: boolean;
}) {
  const locale = useLocale();
  const t = useDictionary();
  const pathname = usePathname();
  const [hidden, setHidden] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const lastY = useRef(0);

  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY;
      setScrolled(y > window.innerHeight * 0.6);
      setHidden(y > 160 && y > lastY.current + 4);
      if (y < lastY.current - 4) setHidden(false);
      lastY.current = y;
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Close menus on navigation: adjust state during render rather than in an effect.
  const [lastPath, setLastPath] = useState(pathname);
  if (lastPath !== pathname) {
    setLastPath(pathname);
    setMobileOpen(false);
    setOpenMenu(null);
  }

  useEffect(() => {
    document.documentElement.style.overflow = mobileOpen ? 'hidden' : '';
  }, [mobileOpen]);

  const overDark = homeStartsDark && pathname === `/${locale}`;
  const dark = overDark && !scrolled && !mobileOpen;
  const isCurrent = (item: NavItem) => pathname.startsWith(localize(item.link, locale));

  return (
    <header
      onKeyDown={(event) => event.key === 'Escape' && (setOpenMenu(null), setMobileOpen(false))}
      className={cn(
        'glass fixed inset-x-0 top-0 z-40 transition-[transform,background-color,color] duration-base ease-out-expo',
        hidden && !mobileOpen && !openMenu ? '-translate-y-full' : 'translate-y-0',
        dark ? 'bg-navy/40 text-white' : 'bg-white/72 text-navy shadow-[0_1px_0_var(--color-hairline)]',
      )}
      data-surface={dark ? 'navy' : undefined}
    >
      <div className="container-wide flex h-(--spacing-nav) items-center gap-6">
        <Link href={`/${locale}`} className="-ms-1 flex min-h-11 items-center gap-3 rounded-md p-1">
          <span data-intro-logo>
            <Logo variant="mark" tone={dark ? 'white' : 'color'} className="h-9 w-auto" title="" />
          </span>
          <span data-intro-name className="text-lg font-semibold tracking-tight">{shortName}</span>
        </Link>

        <nav aria-label={t.a11y.mainNav} className="ms-auto hidden lg:block">
          <ul className="flex items-center gap-1">
            {navigation.header.map((item) => {
              const panel = item.megaMenu || item.children.length > 0;
              const key = item.link;
              return (
                <li key={key} className="relative" onMouseLeave={() => panel && setOpenMenu(null)}>
                  {panel ? (
                    <button
                      type="button"
                      aria-expanded={openMenu === key}
                      onClick={() => setOpenMenu(openMenu === key ? null : key)}
                      onMouseEnter={() => setOpenMenu(key)}
                      className={cn(navItemClass(dark), isCurrent(item) && 'font-semibold')}
                    >
                      {item.label}
                      <ChevronDown aria-hidden className={cn('size-4 transition-transform duration-fast', openMenu === key && 'rotate-180')} />
                    </button>
                  ) : (
                    <SmartLink
                      href={item.link}
                      locale={locale}
                      aria-current={isCurrent(item) ? 'page' : undefined}
                      className={cn(navItemClass(dark), isCurrent(item) && 'font-semibold')}
                    >
                      {item.label}
                    </SmartLink>
                  )}
                  {panel && openMenu === key && <MegaMenu item={item} mega={navigation.mega} locale={locale} />}
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="ms-auto flex items-center gap-2 lg:ms-0">
          <Suspense>
            <LanguageSwitch className={dark ? 'hover:bg-white/10' : 'hover:bg-navy-50'} />
          </Suspense>
          <SmartLink
            href="/request-a-proposal"
            locale={locale}
            data-track="cta_header_proposal"
            className={buttonClass(dark ? 'inverse' : 'primary', 'md', 'hidden sm:inline-flex')}
          >
            {ctaLabel}
          </SmartLink>
          <button
            type="button"
            className="grid size-11 place-items-center rounded-pill lg:hidden"
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
            aria-label={mobileOpen ? t.a11y.closeMenu : t.a11y.menu}
            onClick={() => setMobileOpen((open) => !open)}
          >
            {mobileOpen ? <X aria-hidden className="size-6" /> : <Menu aria-hidden className="size-6" />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav id="mobile-menu" aria-label={t.a11y.mainNav} className="h-[calc(100dvh-var(--spacing-nav))] overflow-y-auto bg-surface lg:hidden">
          <ul className="container-wide flex flex-col py-6">
            {navigation.header.map((item) => (
              <li key={item.link} className="border-b border-hairline">
                <SmartLink href={item.link} locale={locale} className="flex min-h-14 items-center text-h3 font-semibold">
                  {item.label}
                </SmartLink>
                {item.children.length > 0 && (
                  <ul className="pb-4">
                    {item.children.map((child) => (
                      <li key={child.link}>
                        <SmartLink href={child.link} locale={locale} className="flex min-h-11 items-center text-ink-muted">
                          {child.label}
                        </SmartLink>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
            <li className="pt-8">
              <SmartLink href="/request-a-proposal" locale={locale} className={buttonClass('primary', 'lg', 'w-full')}>
                {ctaLabel}
              </SmartLink>
            </li>
          </ul>
        </nav>
      )}
    </header>
  );
}

function navItemClass(dark: boolean) {
  return cn(
    'inline-flex min-h-11 items-center gap-1 rounded-pill px-3.5 text-[0.9375rem] transition-colors duration-fast',
    dark ? 'hover:bg-white/10' : 'hover:bg-navy-50',
  );
}
