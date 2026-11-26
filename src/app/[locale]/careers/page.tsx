import { Blocks } from '@/components/content/Blocks';
import { PageHeader } from '@/components/content/PageHeader';
import { ApplicationForm } from '@/components/forms/ApplicationForm';
import { ArrowIcon } from '@/components/ui/Button';
import { EmptyState } from '@/components/ui/Feedback';
import { SectionHeading } from '@/components/ui/Heading';
import { Section } from '@/components/ui/Section';
import { SmartLink } from '@/components/ui/SmartLink';
import { PendingMarker, Tag } from '@/components/ui/Tag';
import { getDictionary } from '@/i18n/dictionaries';
import { getJobs, getSettings } from '@/lib/cms';
import { ButtonLink } from '@/components/ui/Button';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/careers'>;

const PATH = '/careers/';

export const generateMetadata = ({ params }: Props) => pageMetadata(params, 'careers', PATH, (l) => getDictionary(l).sections.careers);

export default async function CareersPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, jobs, settings] = await Promise.all([pageCopy(locale, 'careers', t.sections.careers), getJobs(locale), getSettings(locale)]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} image={page.image} gate={page}>
        {page.ctaLabel && (
          <ButtonLink href="#open-roles" locale={locale} arrow track="careers_view_opportunities">
            {page.ctaLabel}
          </ButtonLink>
        )}
      </PageHeader>
      <Blocks blocks={page.blocks} locale={locale} />
      <Section tone="surface" tight id="open-roles">
        <div className="container-wide">
          <SectionHeading title={t.sections.openRoles} />
          {jobs.length === 0 ? (
            <EmptyState>{t.sections.noRoles}</EmptyState>
          ) : (
            <ul className="divide-y divide-hairline border-y border-hairline">
              {jobs.map((job) => (
                <li key={job.slug} className="group relative flex flex-col gap-2 py-6 md:flex-row md:items-center md:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">
                      <SmartLink href={`/careers/${job.slug}/`} locale={locale} className="after:absolute after:inset-0 group-hover:text-blue">
                        {job.title}
                      </SmartLink>
                    </h3>
                    <p className="text-ink-muted">{job.summary}</p>
                    <PendingMarker pending={job.pending} fallbacks={job.fallbacks} locale={locale} className="mt-2" />
                  </div>
                  <div className="group/button flex items-center gap-3">
                    <Tag>{job.location}</Tag>
                    <Tag tone="blue">{job.employmentType}</Tag>
                    <ArrowIcon className="text-blue" />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </Section>
      <Section tight>
        <div className="container-content max-w-3xl">
          <SectionHeading title={t.forms.openApplication} />
          <ApplicationForm turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined} />
        </div>
      </Section>
    </>
  );
}
