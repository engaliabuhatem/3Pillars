import { PageHeader } from '@/components/content/PageHeader';
import { ProposalWizard } from '@/components/forms/ProposalWizard';
import { Section } from '@/components/ui/Section';
import { getDictionary } from '@/i18n/dictionaries';
import { getSectors, getServices, getSettings } from '@/lib/cms';
import { pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/request-a-proposal'>;

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'request-a-proposal', '/request-a-proposal', (l) => getDictionary(l).common.requestProposal);

export default async function RequestProposalPage({ params }: Props) {
  const locale = await resolveLocale(params);
  const t = getDictionary(locale);
  const [page, sectors, services, settings] = await Promise.all([
    pageCopy(locale, 'request-a-proposal', t.common.requestProposal),
    getSectors(locale),
    getServices(locale),
    getSettings(locale),
  ]);

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: '/request-a-proposal' }]} eyebrow={page.eyebrow} title={page.title} intro={page.intro} gate={page} />
      <Section tone="surface" tight>
        <div className="container-content max-w-4xl">
          <ProposalWizard
            sectors={sectors.map(({ slug, name }) => ({ slug, name }))}
            services={services.map(({ slug, name }) => ({ slug, name }))}
            turnstileKey={settings.turnstileEnabled ? settings.turnstileSiteKey : undefined}
          />
        </div>
      </Section>
    </>
  );
}
