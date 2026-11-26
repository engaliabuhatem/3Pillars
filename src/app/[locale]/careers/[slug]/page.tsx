import { notFound } from 'next/navigation';
import { PageHeader } from '@/components/content/PageHeader';
import { ApplicationForm } from '@/components/forms/ApplicationForm';
import { SectionHeading } from '@/components/ui/Heading';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Tag } from '@/components/ui/Tag';
import { getDictionary } from '@/i18n/dictionaries';
import { getJob, getSettings } from '@/lib/cms';
import { heading, resolveLocale } from '@/lib/page';
import { buildMetadata, JsonLd, jobPostingJsonLd } from '@/lib/seo';

type Props = PageProps<'/[locale]/careers/[slug]'>;

// Rendered on first request, then cached until the CMS webhook expires it (ISR).
export const generateStaticParams = () => [];

export async function generateMetadata({ params }: Props) {
  const locale = await resolveLocale(params);
  const job = await getJob(locale, (await params).slug);
  if (!job) return {};
  return buildMetadata({ locale, path: `/careers/${job.slug}/`, title: job.title, description: job.summary, seo: job.seo });
}

export default async function JobPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const [job, settings] = await Promise.all([getJob(locale, (await params).slug), getSettings(locale)]);
  if (!job) notFound();
  const t = getDictionary(locale);

  return (
    <>
      <PageHeader
        background={job.heroImage}
        locale={locale}
        trail={[
          { name: t.sections.careers, path: '/careers/' },
          { name: job.title, path: `/careers/${job.slug}/` },
        ]}
        eyebrow={t.sections.careers}
        title={heading({ title: job.title, seo: job.seo })}
        intro={job.summary}
        gate={job}
      >
        <div className="flex flex-wrap gap-2">
          <Tag>{job.location}</Tag>
          <Tag tone="blue">{job.employmentType}</Tag>
        </div>
      </PageHeader>
      <Section tone="surface" tight>
        <div className="container-content">
          <RichText html={job.description} />
        </div>
      </Section>
      {job.isOpen && (
        <Section tight>
          <div className="container-content max-w-3xl">
            <SectionHeading title={t.forms.applyFor} />
            <ApplicationForm jobSlug={job.slug} turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined} />
          </div>
        </Section>
      )}
      {job.isOpen && <JsonLd data={jobPostingJsonLd(job, settings.companyName)} />}
    </>
  );
}
