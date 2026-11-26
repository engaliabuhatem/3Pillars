import type { Locale } from '@/i18n/config';
import type { ApproachStep, InsightCard, Pillar, Project, ProjectCard, SectorCard, ServiceCard, ValuePoint } from '@/lib/cms/types';

/**
 * Specimen text for the styleguide only. Deliberately generic and never
 * served by the CMS, so nothing here can be mistaken for company content.
 */
const specimen = {
  en: {
    title: 'Components',
    intro: 'Every primitive in one place, in both languages, with every state.',
    display: 'Specimen display line',
    heading: 'Specimen heading',
    body: 'Body copy sits at a comfortable measure of about sixty-eight characters, with a generous line height for long reading.',
    caption: 'Specimen caption',
    faq: ['Specimen question one?', 'Specimen question two?'],
    answer: 'Specimen answer text.',
  },
  ar: {
    title: 'المكونات',
    intro: 'جميع العناصر الأساسية في مكان واحد، باللغتين وبكل حالاتها.',
    display: 'سطر عرض تجريبي',
    heading: 'عنوان تجريبي',
    body: 'يُعرض النص الأساسي بعرض مريح يقارب ثمانية وستين حرفاً، مع تباعد أسطر سخي للقراءة الطويلة.',
    caption: 'تعليق تجريبي',
    faq: ['سؤال تجريبي أول؟', 'سؤال تجريبي ثانٍ؟'],
    answer: 'نص إجابة تجريبي.',
  },
};

const NO_SEO = { title: '', description: '', h1: '', image: null, indexable: { en: false, ar: false } };

function build(locale: Locale) {
  const s = specimen[locale];
  const service: ServiceCard = {
    slug: 'specimen',
    name: s.heading,
    icon: 'ClipboardList',
    summary: s.body,
    pillar: { number: 1, color: 'green', isProposed: false },
    image: null,
    pending: true,
  };
  const sector: SectorCard = { slug: 'specimen', name: s.heading, icon: 'Building2', focusSummary: s.caption, image: null };
  const project: ProjectCard = {
    slug: 'specimen',
    title: s.heading,
    entryType: 'case_study',
    summary: s.body,
    location: s.caption,
    country: s.caption,
    status: 'ongoing',
    sector: { slug: 'specimen', name: s.caption },
    client: null,
    deliveryEntity: s.caption,
    ourRole: 'PMO support',
    roleKey: 'pmo_support',
    featured: false,
    image: null,
  };
  const caseStudy: Project = {
    ...project,
    ourRoleDetail: s.caption,
    challenge: '',
    scopeOfServices: '',
    approach: '',
    results: '',
    services: [],
    metrics: [],
    gallery: [],
    facts: { value: null, start: '2026-01-15', end: null, durationMonths: null },
    related: [],
    seo: NO_SEO,
    updatedAt: '2026-01-15',
  };
  const insight: InsightCard = {
    slug: 'specimen',
    title: s.heading,
    kind: 'article',
    excerpt: s.body,
    category: { slug: 'specimen', name: s.caption },
    author: '',
    publishedAt: '2026-01-15',
    readingMinutes: 4,
    image: null,
  };
  const pillars: Pillar[] = (['green', 'blue', 'grey'] as const).map((color, i) => ({
    id: i,
    number: i + 1,
    name: `${s.heading} ${i + 1}`,
    roleOnSite: i < 2 ? 'lead' : 'enabling',
    color,
    coreValue: s.caption,
    summary: s.body,
    detail: s.body,
    coreOutcomes: s.caption,
    covers: s.caption,
    isProposed: i === 2,
    service: null,
  }));
  const values: ValuePoint[] = [1, 2, 3].map((n) => ({ id: n, title: `${s.heading} ${n}`, body: s.caption }));
  const steps: ApproachStep[] = [1, 2, 3].map((n) => ({ id: n, name: `${s.heading} ${n}`, summary: s.body }));
  return {
    ...s,
    service,
    sector,
    project,
    caseStudy,
    insight,
    pillars,
    values,
    steps,
    capabilities: [1, 2, 3].map((n) => ({ title: `${s.heading} ${n}`, description: s.caption })),
    faqs: s.faq.map((question) => ({ question, answer: s.answer })),
  };
}

export const FIXTURES = { en: build('en'), ar: build('ar') };
