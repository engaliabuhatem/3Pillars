import type { ReactNode } from 'react';

/**
 * Remounts on every navigation, so each new page fades in (≤ 300ms, CSS only).
 * The fade only runs after an in-site navigation (see NavigationMarker), never
 * on the first page load, so it can't hold back the first paint.
 */
export default function PageTransition({ children }: { children: ReactNode }) {
  return <div className="page-in">{children}</div>;
}
