'use client';

import { StatusScreen } from '@/components/content/StatusScreen';
import { sourceSans, tajawal } from './fonts';
import './globals.css';

/** Errors in the root layout itself. Bilingual, because the locale is not known here. */
export default function GlobalError({ reset }: { error: Error; reset: () => void }) {
  return (
    <html lang="en" className={`${sourceSans.variable} ${tajawal.variable}`}>
      <body>
        <StatusScreen code="500" title="Something went wrong · حدث خطأ" body="Please try again in a moment. · يُرجى المحاولة بعد قليل.">
          <button type="button" onClick={reset} className="min-h-11 rounded-md bg-white px-6 font-semibold text-navy">
            Try again · حاول مجدداً
          </button>
        </StatusScreen>
      </body>
    </html>
  );
}
