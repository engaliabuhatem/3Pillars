import { Source_Sans_3, Tajawal } from 'next/font/google';

// display: optional — preloaded fonts are ready for first paint on any normal
// connection; on a very slow first visit the metric-matched fallback stays
// rather than swapping late (which would re-trigger LCP and shift text).
//
// Source Sans 3 stands in for the CI's Myriad Pro (Adobe's open-source humanist
// sibling). Swap here, and only here, if an Adobe Fonts licence is added.
export const sourceSans = Source_Sans_3({
  subsets: ['latin'],
  variable: '--font-source-sans',
  display: 'optional',
});

export const tajawal = Tajawal({
  subsets: ['arabic'],
  weight: ['400', '700'],
  variable: '--font-tajawal',
  display: 'optional',
});
