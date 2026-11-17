import NextLink from 'next/link';
import type { ComponentProps } from 'react';
import type { Locale } from '@/i18n/config';
import { isExternal, localize } from '@/lib/utils';

type Props = Omit<ComponentProps<typeof NextLink>, 'href'> & {
  href: string;
  locale: Locale;
  externalLabel?: string;
};

/** A CMS link: locale-prefixed when internal, new tab with a spoken hint when external. */
export function SmartLink({ href, locale, externalLabel, children, ...rest }: Props) {
  if (isExternal(href)) {
    const newTab = href.startsWith('http');
    return (
      <a href={href} {...(newTab ? { target: '_blank', rel: 'noopener noreferrer' } : {})} {...rest}>
        {children}
        {newTab && externalLabel && <span className="sr-only"> ({externalLabel})</span>}
      </a>
    );
  }
  return (
    <NextLink href={localize(href, locale)} {...rest}>
      {children}
    </NextLink>
  );
}
