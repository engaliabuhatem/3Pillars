import type { CSSProperties, ReactNode } from 'react';

interface RevealProps {
  children: ReactNode;
  delay?: number;
  /** Stagger index for lists: each step adds 60ms. */
  index?: number;
  className?: string;
  as?: 'div' | 'li' | 'article' | 'span';
}

/**
 * Fade + rise + blur-to-sharp, once, when the element scrolls into view.
 *
 * A server component: it only marks the element. RevealController (one client
 * component for the whole page) hides marked elements that start below the
 * fold and shows them on entry. Anything already on screen, any visitor
 * without JS, and anyone preferring reduced motion simply sees the content.
 */
export function Reveal({ children, delay = 0, index = 0, className, as: Tag = 'div' }: RevealProps) {
  const style = { '--reveal-delay': `${Math.round((delay + index * 0.06) * 1000)}ms` } as CSSProperties;
  return (
    <Tag data-reveal="" className={className} style={style}>
      {children}
    </Tag>
  );
}
