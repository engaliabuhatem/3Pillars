import { Accordion } from '@/components/ui/Accordion';
import { ButtonLink } from '@/components/ui/Button';
import { MediaFrame } from '@/components/ui/CmsImage';
import { Eyebrow } from '@/components/ui/Heading';
import { KPICounter } from '@/components/ui/KPICounter';
import { Lightbox } from '@/components/ui/Lightbox';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import type { Locale } from '@/i18n/config';
import type { ApproachStep, CompanyValue, PageBlock } from '@/lib/cms/types';
import { cn } from '@/lib/utils';
import { ApproachTimeline } from './ApproachTimeline';
import { CtaBand } from './CtaBand';

function BlockTitle({ block }: { block: PageBlock }) {
  if (!block.eyebrow && !block.title) return null;
  return (
    <div className="mb-10 max-w-3xl">
      {block.eyebrow && <Eyebrow className="mb-4">{block.eyebrow}</Eyebrow>}
      {block.title && <h2 className="text-h2 font-semibold text-balance">{block.title}</h2>}
    </div>
  );
}

function Block({ block, locale }: { block: PageBlock; locale: Locale }) {
  switch (block.kind) {
    case 'rich_text':
      return (
        <>
          <BlockTitle block={block} />
          <Reveal>
            <RichText html={block.body} />
          </Reveal>
        </>
      );
    case 'image_text':
      return (
        <div className="grid items-center gap-10 lg:grid-cols-2 lg:gap-20">
          <Reveal className={cn(block.imageOnEnd && 'lg:order-last')}>
            <MediaFrame media={block.image} sizes="(min-width: 1024px) 50vw, 100vw" ratio="portrait" />
          </Reveal>
          <div>
            <BlockTitle block={block} />
            <RichText html={block.body} />
            {block.ctaLabel && (
              <ButtonLink href={block.ctaLink} locale={locale} variant="secondary" arrow className="mt-8">
                {block.ctaLabel}
              </ButtonLink>
            )}
          </div>
        </div>
      );
    case 'stats':
      return (
        <>
          <BlockTitle block={block} />
          <ul className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
            {block.items.map((item) => (
              <li key={item.label} className="border-t border-hairline pt-6 on-navy:border-hairline-inverse">
                <StatValue value={item.value} label={item.label} source={item.text} />
              </li>
            ))}
          </ul>
        </>
      );
    case 'quote':
      return (
        <figure className="max-w-4xl">
          <blockquote className="text-h2 font-medium text-balance [&_p]:inline">
            “<RichText html={block.body} className="inline max-w-none text-h2" />”
          </blockquote>
          {block.attribution && <figcaption className="mt-6 text-lead text-ink-muted on-navy:text-ink-inverse-muted">— {block.attribution}</figcaption>}
        </figure>
      );
    case 'gallery':
      return (
        <>
          <BlockTitle block={block} />
          <Lightbox items={block.items.map((item) => ({ image: item.image, caption: item.label }))} />
        </>
      );
    case 'faq':
      return (
        <div className="grid gap-10 lg:grid-cols-[1fr_2fr]">
          <BlockTitle block={block} />
          <Accordion name={`faq-${block.id}`} items={block.items.map((item) => ({ question: item.label, answer: item.text }))} />
        </div>
      );
    case 'values': {
      const values = block.entries as CompanyValue[];
      return (
        <>
          <BlockTitle block={block} />
          <dl className="grid gap-x-10 gap-y-8 md:grid-cols-2 lg:grid-cols-3">
            {values.map((value, i) => (
              <Reveal key={value.id} index={i % 3} className="border-t border-hairline pt-6 on-navy:border-hairline-inverse">
                <dt className="text-h3 font-semibold">{value.value}</dt>
                <dd className="mt-3 text-ink-muted on-navy:text-ink-inverse-muted">{value.inPractice}</dd>
              </Reveal>
            ))}
          </dl>
        </>
      );
    }
    case 'approach_steps':
      return (
        <>
          <BlockTitle block={block} />
          {block.body && <RichText html={block.body} className="mb-14 text-lead" />}
          <ApproachTimeline stages={block.entries as ApproachStep[]} />
        </>
      );
    case 'affiliation':
      return block.body ? (
        <>
          <BlockTitle block={block} />
          <RichText html={block.body} />
        </>
      ) : null;
    case 'cta':
      return null;
  }
}

/** A numeric figure counts up; anything else (e.g. "ISO 9001") is shown as written. */
function StatValue({ value, label, source }: { value: string; label: string; source: string }) {
  const match = value.match(/^([^\d-]*)(-?\d+(?:\.\d+)?)(.*)$/);
  if (match) {
    return <KPICounter prefix={match[1]} value={Number(match[2])} suffix={match[3]} label={label} source={source || undefined} />;
  }
  return (
    <div className="flex flex-col gap-2">
      <span className="text-h2 font-semibold">{value}</span>
      <span className="text-lg text-ink-muted">{label}</span>
    </div>
  );
}

/** Blocks with nothing to show (an empty affiliation statement, a list with no entries) are skipped. */
const isEmpty = (block: PageBlock) =>
  (block.kind === 'affiliation' && !block.body) || ((block.kind === 'values' || block.kind === 'approach_steps') && block.entries.length === 0 && !block.body);

/** Renders a CMS page's ordered blocks, alternating canvas/white unless a block asks for navy. */
export function Blocks({ blocks, locale }: { blocks: PageBlock[]; locale: Locale }) {
  return blocks.filter((block) => !isEmpty(block)).map((block, i) =>
    block.kind === 'cta' ? (
      <CtaBand
        key={block.id}
        locale={locale}
        eyebrow={block.eyebrow}
        title={block.title}
        primary={{ label: block.ctaLabel, href: block.ctaLink }}
      />
    ) : (
      <Section key={block.id} tone={block.navy ? 'navy' : i % 2 ? 'surface' : 'canvas'} arcs={block.navy} tight>
        <div className="container-wide">
          <Block block={block} locale={locale} />
        </div>
      </Section>
    ),
  );
}
