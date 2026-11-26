import { Blocks } from '@/components/content/Blocks';
import { CtaBand } from '@/components/content/CtaBand';
import { Linkedin } from '@/components/content/Linkedin';
import { PageHeader } from '@/components/content/PageHeader';
import { MediaFrame } from '@/components/ui/CmsImage';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { PendingMarker } from '@/components/ui/Tag';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getTeam } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

const PATH = '/about-us/leadership-team/';
type Props = PageProps<'/[locale]/about-us/leadership-team'>;

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'leadership-team', PATH, (l) => getDictionary(l).sections.team);

/** Leadership and team members, published only with each person's approval. */
export default async function LeadershipPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, about, team] = await Promise.all([
    pageCopy(locale, 'leadership-team', t.sections.team),
    pageCopy(locale, 'about-us', t.sections.about),
    getTeam(locale),
  ]);
  const ordered = [...team.filter((m) => m.leadership), ...team.filter((m) => !m.leadership)];

  return (
    <>
      <PageHeader
        background={page.heroImage}
        locale={locale}
        trail={[
          { name: about.title, path: '/about-us/' },
          { name: page.title, path: PATH },
        ]}
        eyebrow={page.eyebrow}
        title={heading(page)}
        intro={page.intro}
        gate={page}
      />
      <Section tone="surface" tight>
        <div className="container-wide">
          {ordered.length === 0 ? (
            <EmptyState>{t.empty.generic}</EmptyState>
          ) : (
            <ul className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {ordered.map((member, i) => (
                <Reveal as="li" key={member.id} index={i % 4}>
                  <MediaFrame media={member.photo} sizes="(min-width: 1024px) 25vw, 50vw" ratio="portrait" />
                  <h2 className="mt-5 text-xl font-semibold">{member.name}</h2>
                  <p className="text-ink-muted">{member.role}</p>
                  {member.bio && <p className="mt-3 text-[0.9375rem] text-ink-muted">{member.bio}</p>}
                  {member.linkedin && <Linkedin href={member.linkedin} name={member.name} locale={locale} />}
                  <PendingMarker pending={member.pending} fallbacks={member.fallbacks} locale={locale} className="mt-3" />
                </Reveal>
              ))}
            </ul>
          )}
        </div>
      </Section>
      <Blocks blocks={page.blocks} locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
