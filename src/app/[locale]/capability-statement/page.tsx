import { Blocks } from '@/components/content/Blocks';
import { PageHeader } from '@/components/content/PageHeader';
import { DownloadGate } from '@/components/forms/DownloadGate';
import { EmptyState } from '@/components/ui/Feedback';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getDownloads, getSettings } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/capability-statement'>;

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'capability-statement', '/capability-statement', (l) => getDictionary(l).common.capability);

export default async function CapabilityStatementPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, downloads, settings] = await Promise.all([
    pageCopy(locale, 'capability-statement', t.common.capability),
    getDownloads(locale),
    getSettings(locale),
  ]);
  const doc = downloads.find((d) => d.isCapabilityStatement);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/capability-statement' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} gate={page} />
      <Section tone="surface" tight>
        <div className="container-wide">
          {doc ? (
            <>
              <h2 className="mb-2 text-h3 font-semibold">{doc.title}</h2>
              {doc.description && <p className="mb-8 max-w-prose text-ink-muted">{doc.description}</p>}
              <DownloadGate
                downloadId={doc.id}
                directUrl={doc.file?.src ?? null}
                turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined}
              />
            </>
          ) : (
            <EmptyState>{t.empty.generic}</EmptyState>
          )}
        </div>
      </Section>
      <Blocks blocks={page.blocks} locale={locale} />
    </>
  );
}
