import { ARCS, PILLARS } from './logoPaths';

type Variant = 'full' | 'mark';
type Tone = 'color' | 'white' | 'navy';

const BRAND_INK = {
  green: 'var(--color-green)',
  blue: 'var(--color-blue)',
  grey: 'var(--color-grey)',
};
const MONO_INK = { green: 'currentColor', blue: 'currentColor', grey: 'currentColor' };

const TONE_CLASS: Record<Tone, string | undefined> = {
  color: undefined,
  white: 'text-white',
  navy: 'text-navy',
};

const VIEWBOX: Record<Variant, string> = { full: '0 0 595 842', mark: '40 10 520 760' };

interface LogoProps {
  variant?: Variant;
  tone?: Tone;
  title?: string;
  className?: string;
}

/**
 * The 3 Pillars logo as inline SVG. Every pillar and arc is its own path with a
 * `data-part`, which is what the draw-on intro animates. An empty `title` makes
 * it decorative, for when visible text beside it already names the company.
 */
export function Logo({
  variant = 'mark',
  tone = 'color',
  title = '3 Pillars Project Management Services',
  className,
}: LogoProps) {
  const ink = tone === 'color' ? BRAND_INK : MONO_INK;

  return (
    <svg
      viewBox={VIEWBOX[variant]}
      {...(title ? { role: 'img', 'aria-label': title } : { 'aria-hidden': true })}
      className={[TONE_CLASS[tone], className].filter(Boolean).join(' ')}
      data-logo
    >
      <g fill="none" strokeLinecap="round" strokeLinejoin="round">
        <path data-part="arc-outer" d={ARCS.outer} stroke={ink.grey} strokeWidth={13} pathLength={1} />
        <path data-part="arc-bowl" d={ARCS.bowl} stroke={ink.grey} strokeWidth={16} pathLength={1} />
        <path data-part="arc-grey" d={ARCS.grey} stroke={ink.grey} strokeWidth={7} pathLength={1} />
        <path data-part="arc-blue" d={ARCS.blue} stroke={ink.blue} strokeWidth={8} pathLength={1} />
        <path data-part="arc-green" d={ARCS.green} stroke={ink.green} strokeWidth={8} pathLength={1} />
      </g>
      <path data-part="pillar-green" d={PILLARS.green} fill={ink.green} />
      <path data-part="pillar-blue" d={PILLARS.blue} fill={ink.blue} />
      <path data-part="pillar-grey" d={PILLARS.grey} fill={ink.grey} />
      {variant === 'full' && (
        <g data-part="wordmark" fill={tone === 'color' ? ink.grey : 'currentColor'} aria-hidden>
          <text x={181} y={654} fontSize={100} fontWeight={600} textLength={362} lengthAdjust="spacingAndGlyphs">
            3 Pillars
          </text>
          <text x={181} y={744} fontSize={60} textLength={358} lengthAdjust="spacing">
            PROJECT
          </text>
          <rect x={51} y={759} width={491} height={2.5} />
          <text x={51} y={804} fontSize={34} textLength={489} lengthAdjust="spacingAndGlyphs">
            MANAGEMENT SERVICES
          </text>
        </g>
      )}
    </svg>
  );
}
