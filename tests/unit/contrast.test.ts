import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { contrast } from '../../src/lib/color.mjs';

const css = ['src/styles/palette.css', 'src/app/globals.css']
  .map((file) => readFileSync(file, 'utf8'))
  .join('\n');

function token(name: string): string {
  const match = css.match(new RegExp(`--color-${name}:\\s*(#[0-9a-fA-F]{6})`));
  if (!match?.[1]) throw new Error(`token --color-${name} is not a hex value`);
  return match[1];
}

/**
 * Every foreground/background pair the UI uses for text or meaningful UI
 * strokes. A new pair in a component means a new row here, or the build fails.
 */
const TEXT_PAIRS: Array<[fg: string, bg: string, min: number]> = [
  ['navy', 'canvas', 4.5],
  ['navy', 'surface', 4.5],
  ['grey', 'surface', 4.5],
  ['grey', 'canvas', 4.5],
  ['blue', 'surface', 4.5],
  ['blue', 'canvas', 4.5],
  ['green', 'surface', 4.5],
  ['green', 'canvas', 4.5],
  ['surface', 'navy', 4.5],
  ['surface', 'blue', 4.5],
  ['surface', 'green', 4.5],
  ['surface', 'grey', 4.5],
  ['blue-200', 'navy', 4.5],
  ['blue-300', 'navy', 4.5],
  ['green-200', 'navy', 4.5],
  ['green-300', 'navy', 4.5],
  ['grey-200', 'navy', 4.5],
  ['grey-300', 'navy', 4.5],
  ['navy', 'blue-50', 4.5],
  ['blue-700', 'blue-50', 4.5],
  ['green-700', 'green-50', 4.5],
  ['navy', 'grey-100', 4.5],
  ['danger', 'surface', 4.5],
  ['danger', 'danger-50', 4.5],
  ['warning', 'warning-50', 4.5],
  ['blue', 'navy-50', 4.5],
];

describe('token contrast (WCAG 2.2 AA)', () => {
  it.each(TEXT_PAIRS)('%s on %s ≥ %s:1', (fg, bg, min) => {
    expect(contrast(token(fg), token(bg))).toBeGreaterThanOrEqual(min);
  });

  it('keeps the CI values at step 600', () => {
    expect(token('navy-600')).toBe('#191747');
    expect(token('blue-600')).toBe('#0B5EAC');
    expect(token('green-600')).toBe('#136131');
    expect(token('grey-600')).toBe('#5C5E60');
  });

  it.each([
    ['blue', 'navy'],
    ['green', 'navy'],
    ['grey', 'navy'],
  ])('flags %s on %s as unreadable, so it must never be used for text', (fg, bg) => {
    expect(contrast(token(fg), token(bg))).toBeLessThan(4.5);
  });
});
