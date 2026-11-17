import { Linkedin } from '@/components/content/Linkedin';
import { Blocks } from '@/components/content/Blocks';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { PillarsShowcase } from '@/components/home/PillarsShowcase';
import { MediaFrame } from '@/components/ui/CmsImage';
import { SectionHeading } from '@/components/ui/Heading';
import { Section } from '@/components/ui/Section';
import { PendingMarker } from '@/components/ui/Tag';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getCertifications, getOffices, getPillars, getSettings, getTeam } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

export const generateMetadata = ({ params }: PageProps<'/[locale]/about'>) =>
  pageMetadata(params, 'about', '/about', (l) => getDictionary(l).sections.about);

export default async function AboutPage({ params }: PageProps<'/[locale]/about'>) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, pillars, team, certifications, offices, settings] = await Promise.all([
    pageCopy(locale, 'about', t.sections.about),
    getPillars(locale),
    getTeam(locale),
    getCertifications(locale),
    getOffices(locale),
    getSettings(locale),
  ]);
  const leaders = team.filter((member) => member.leadership);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/about' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} image={page.image} gate={page} />
      <Blocks blocks={page.blocks} locale={locale} />

      {pillars.length > 0 && (
        <Section tone="surface">
          <div className="container-wide">
            <SectionHeading title={t.sections.pillarsMeaning} />
            <PillarsShowcase pillars={pillars} />
          </div>
        </Section>
      )}

      {settings.groupRelationship && (
        <Section tight>
          <div className="container-wide max-w-4xl">
            <p className="eyebrow mb-4 text-blue">{t.sections.group}</p>
            <p className="text-h3 font-medium text-balance">{settings.groupRelationship}</p>
          </div>
        </Section>
      )}

      {leaders.length > 0 && (
        <Section tone="surface">
          <div className="container-wide">
            <SectionHeading title={t.sections.team} />
            <ul className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {leaders.map((member, i) => (
                <Reveal as="li" key={member.id} index={i % 4}>
                  <MediaFrame media={member.photo} sizes="(min-width: 1024px) 25vw, 50vw" ratio="portrait" />
                  <h3 className="mt-5 text-xl font-semibold">{member.name}</h3>
                  <p className="text-ink-muted">{member.role}</p>
                  {member.bio && <p className="mt-3 text-[0.9375rem] text-ink-muted">{member.bio}</p>}
                  {member.linkedin && <Linkedin href={member.linkedin} name={member.name} locale={locale} />}
                  <PendingMarker pending={member.pending} fallbacks={member.fallbacks} locale={locale} className="mt-3" />
                </Reveal>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {certifications.length > 0 && (
        <Section tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.certifications} />
            <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {certifications.map((cert) => (
                <li key={cert.id} className="tile p-7 md:p-8">
                  <p className="text-lg font-semibold">{cert.name}</p>
                  <p className="text-ink-muted">
                    {cert.issuer}
                    {cert.year ? ` · ${cert.year}` : ''}
                  </p>
                  <PendingMarker pending={cert.pending} locale={locale} className="mt-3" />
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      {offices.length > 0 && (
        <Section tone="surface" tight>
          <div className="container-wide">
            <SectionHeading title={t.sections.offices} />
            <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {offices.map((office) => (
                <li key={office.id} className="tile p-7 md:p-8">
                  <p className="text-xl font-semibold">
                    {office.city}, {office.country}
                  </p>
                  {office.address && <p className="mt-2 whitespace-pre-line text-ink-muted">{office.address}</p>}
                </li>
              ))}
            </ul>
          </div>
        </Section>
      )}

      <CtaBand locale={locale} />
    </>
  );
}
