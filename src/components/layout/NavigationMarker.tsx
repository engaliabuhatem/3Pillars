'use client';

import { usePathname } from 'next/navigation';
import { useEffect, useRef } from 'react';

/** Marks <html> once the visitor has navigated within the site, enabling the page fade. */
export function NavigationMarker() {
  const pathname = usePathname();
  const first = useRef(pathname);

  useEffect(() => {
    if (pathname !== first.current) document.documentElement.dataset.navigated = '';
  }, [pathname]);

  return null;
}
