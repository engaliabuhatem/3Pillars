import type { Locale } from '@/i18n/config';
import type { InsightCard, LifecycleStage, Pillar, ProjectCard, SectorCard, ServiceCard } from '@/lib/cms/types';

/**
 * Specimen text for the styleguide only. Deliberately generic and never
 * served by the CMS, so nothing here can be mistaken for company content.
 */
const specimen = {
  en: {
    title: 'Components',
    intro: 'Every primitive in one place, in both languages, with every state.',
    display: 'Clarity on every project',
    heading: 'Specimen heading',
    body: 'Body copy sits at a comfortable measure of about sixty-eight characters, with a generous line height for long reading.',
    caption: 'Specimen caption',
    faq: ['Specimen question one?', 'Specimen question two?'],
    answer: 'Specimen answer text.',
  },
  ar: {
    title: 'المكونات',
    intro: 'جميع العناصر الأساسية في مكان واحد، باللغتين وبكل حالاتها.',
    display: 'وضوح في كل مشروع',
    heading: 'عنوان تجريبي',
    body: 'يُعرض النص الأساسي بعرض مريح يقارب ثمانية وستين حرفاً، مع تباعد أسطر سخي للقراءة الطويلة.',
    caption: 'تعليق تجريبي',
    faq: ['سؤال تجريبي أول؟', 'سؤال تجريبي ثانٍ؟'],
    answer: 'نص إجابة تجريبي.',
  },
};

function build(locale: Locale) {
  const s = specimen[locale];
  const service: ServiceCard = { slug: 'specimen', name: s.heading, icon: 'ClipboardCheck', summary: s.body, featured: false, image: null, pending: true };
  const sector: SectorCard = { slug: 'specimen', name: s.heading, icon: 'Building', summary: s.caption, image: null };
  const project: ProjectCard = {
    slug: 'specimen',
    title: s.heading,
    summary: s.body,
    location: s.caption,
    country: s.caption,
    status: 'ongoing',
    sector: { slug: 'specimen', name: s.caption },
    client: null,
    featured: false,
    image: null,
  };
  const insight: InsightCard = {
    slug: 'specimen',
    title: s.heading,
    excerpt: s.body,
    category: { slug: 'specimen', name: s.caption },
    author: '',
    publishedAt: '2026-01-15',
    readingMinutes: 4,
    image: null,
  };
  const pillars: Pillar[] = (['green', 'blue', 'grey'] as const).map((color, i) => ({
    id: i,
    name: `${s.heading} ${i + 1}`,
    color,
    icon: 'Layers',
    summary: s.caption,
    detail: s.body,
  }));
  const stages: LifecycleStage[] = [1, 2, 3].map((n) => ({ id: n, name: `${s.heading} ${n}`, icon: 'Flag', summary: s.body, deliverables: [s.caption] }));
  return {
    ...s,
    service,
    sector,
    project,
    insight,
    pillars,
    stages,
    faqs: s.faq.map((question) => ({ question, answer: s.answer })),
  };
}

export const FIXTURES = { en: build('en'), ar: build('ar') };
