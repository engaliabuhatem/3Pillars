import type { PillarColor } from '@/lib/cms/types';

/** The logo's three pillar colours, in order: green, blue, grey. */
export const PILLAR_BAR: Record<PillarColor, string> = {
  green: 'bg-green',
  blue: 'bg-blue',
  grey: 'bg-grey-300',
};

export const pillarNumber = (n: number) => String(n).padStart(2, '0');
