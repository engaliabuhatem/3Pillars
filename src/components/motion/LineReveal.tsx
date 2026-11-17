import { Fragment, type CSSProperties } from 'react';

/**
 * Headline reveal: each word rises out of a mask. Words rather than measured
 * lines, because line breaks depend on font, width and language; per-word
 * staggering gives the same effect without measuring layout.
 *
 * Screen readers get the sentence once; the animated words are hidden.
 */
export function LineReveal({ text, delay = 0 }: { text: string; delay?: number }) {
  const words = text.split(/\s+/).filter(Boolean);
  return (
    <>
      <span className="sr-only">{text}</span>
      <span aria-hidden data-reveal="words">
        {words.map((word, i) => (
          <Fragment key={`${word}-${i}`}>
            <span className="reveal-word">
              <span style={{ '--word-delay': `${Math.round((delay + i * 0.05) * 1000)}ms` } as CSSProperties}>{word}</span>
            </span>
            {i < words.length - 1 && ' '}
          </Fragment>
        ))}
      </span>
    </>
  );
}
