import { ImageResponse } from 'next/og';
import { ARCS, PILLARS } from '@/components/brand/logoPaths';
import { isLocale } from '@/i18n/config';
import { getSettings } from '@/lib/cms';

export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';
export const alt = '3 Pillars Project Management Services';

/*
 * The generated share image used when a page has no CMS image: navy, the
 * white mark, the three arcs, and the company name. Colours are literal here
 * because ImageResponse renders outside the CSS token pipeline; they are the
 * CI values from palette.css.
 */
const NAVY = '#191747';
const ARC_TINTS = ['#9D9EA0', '#6D9ECD', '#71A083'];

export default async function OpenGraphImage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  const settings = await getSettings(isLocale(locale) ? locale : 'en');

  return new ImageResponse(
    (
      <div style={{ display: 'flex', width: '100%', height: '100%', background: NAVY, color: 'white', padding: 80, position: 'relative' }}>
        <svg width="1200" height="630" viewBox="0 0 1200 630" style={{ position: 'absolute', inset: 0 }}>
          {ARC_TINTS.map((stroke, i) => (
            <path key={stroke} d={`M-40 ${560 + i * 30}C300 ${500 + i * 30} 760 ${360 + i * 30} 1040 ${80 + i * 20}`} stroke={stroke} strokeWidth="2" fill="none" />
          ))}
        </svg>
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '100%' }}>
          <svg width="150" height="219" viewBox="40 10 520 760">
            <g fill="none" stroke="white" strokeLinecap="round">
              <path d={ARCS.outer} strokeWidth="13" />
              <path d={ARCS.bowl} strokeWidth="16" />
              <path d={ARCS.grey} strokeWidth="7" />
              <path d={ARCS.blue} strokeWidth="8" />
              <path d={ARCS.green} strokeWidth="8" />
            </g>
            <path d={PILLARS.green} fill="white" />
            <path d={PILLARS.blue} fill="white" />
            <path d={PILLARS.grey} fill="white" />
          </svg>
          <div style={{ display: 'flex', fontSize: 60, fontWeight: 600, maxWidth: 900, lineHeight: 1.1 }}>{settings.companyName}</div>
        </div>
      </div>
    ),
    size,
  );
}
