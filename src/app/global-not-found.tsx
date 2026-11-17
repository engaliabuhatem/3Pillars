import type { Metadata } from 'next';
import Link from 'next/link';
import { StatusScreen } from '@/components/content/StatusScreen';
import { sourceSans, tajawal } from './fonts';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL(process.env.SITE_URL ?? 'http://localhost:3000'),
  title: 'Page not found · 3 Pillars',
  robots: { index: false },
};

/** URLs outside any locale (the proxy redirects nearly all of these). */
export default function GlobalNotFound() {
  return (
    <html lang="en" className={`${sourceSans.variable} ${tajawal.variable}`}>
      <body>
        <StatusScreen code="404" title="Page not found · الصفحة غير موجودة" body="The page you are looking for does not exist.">
          <Link href="/en" className="inline-flex min-h-11 items-center rounded-md bg-white px-6 font-semibold text-navy">
            Home
          </Link>
          <Link href="/ar" lang="ar" className="inline-flex min-h-11 items-center rounded-md px-6 font-semibold text-white ring-1 ring-white/40 ring-inset">
            الرئيسية
          </Link>
        </StatusScreen>
      </body>
    </html>
  );
}
