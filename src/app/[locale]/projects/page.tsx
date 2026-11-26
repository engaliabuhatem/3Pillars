import { Suspense } from 'react';
import { Blocks } from '@/components/content/Blocks';
import { ProjectCard } from '@/components/content/Cards';
import { CtaBand } from '@/components/content/CtaBand';
import { PageHeader } from '@/components/content/PageHeader';
import { ProjectFilters } from '@/components/content/ProjectFilters';
import { Pagination } from '@/components/content/Pagination';
import { EmptyState } from '@/components/ui/Feedback';
import { RichText } from '@/components/ui/RichText';
import { Section } from '@/components/ui/Section';
import { Reveal } from '@/components/motion/Reveal';
import { getDictionary } from '@/i18n/dictionaries';
import { getProjects } from '@/lib/cms';
import { heading, pageCopy, pageMetadata, resolveLocale } from '@/lib/page';

type Props = PageProps<'/[locale]/projects'>;

const PATH = '/projects/';

export const generateMetadata = ({ params }: Props) =>
  pageMetadata(params, 'projects', PATH, (l) => getDictionary(l).sections.projects);

const one = (value: string | string[] | undefined) => (Array.isArray(value) ? value[0] : value);

export default async function ProjectsPage({ params, searchParams }: Props) {
  const locale = await resolveLocale(params);
  const query = await searchParams;
  const t = getDictionary(locale);
  const filters = {
    sector: one(query.sector),
    service: one(query.service),
    role: one(query.role),
    type: one(query.type),
    page: one(query.page),
  };
  const [page, projects] = await Promise.all([pageCopy(locale, 'projects', t.sections.projects), getProjects(locale, filters)]);
  const filtered = Boolean(filters.sector || filters.service || filters.role || filters.type);
  // With nothing published, the page's first block (when an editor has written one) is the empty state.
  const emptyBlock = projects.count === 0 && !filtered ? page.blocks[0] : undefined;
  const blocks = emptyBlock ? page.blocks.slice(1) : page.blocks;

  return (
    <>
      <PageHeader locale={locale} trail={[{ name: page.title, path: PATH }]} eyebrow={page.eyebrow} title={heading(page)} intro={page.intro} gate={page} />
      <Section tight>
        <div className="container-wide">
          {(projects.count > 0 || filtered) && (
            <Suspense>
              <ProjectFilters facets={projects.facets} count={projects.count} />
            </Suspense>
          )}
          {projects.results.length === 0 ? (
            <EmptyState>
              {filtered ? t.filters.empty : emptyBlock?.body ? <RichText html={emptyBlock.body} /> : t.empty.projects}
            </EmptyState>
          ) : (
            <ul className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {projects.results.map((project, i) => (
                <Reveal as="li" key={project.slug} index={i % 3}>
                  <ProjectCard project={project} locale={locale} />
                </Reveal>
              ))}
            </ul>
          )}
          <Pagination locale={locale} basePath={PATH} query={query} hasPrevious={Boolean(projects.previous)} hasNext={Boolean(projects.next)} />
        </div>
      </Section>
      <Blocks blocks={blocks} locale={locale} />
      <CtaBand locale={locale} />
    </>
  );
}
