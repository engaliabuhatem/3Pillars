/**
 * Wire types for the Django API (the serializers in backend/apps). One file so
 * a serializer change has exactly one place to land on this side.
 */

export interface Media {
  src: string;
  alt: string;
  width: number | null;
  height: number | null;
  sources: Partial<Record<'webp' | 'avif', string>>;
}

export interface FileRef {
  src: string;
  size: number;
}

/** Present on every publishable row: whether it is awaiting approval. */
export interface Gated {
  pending?: boolean;
  /** Fields that fell back to English because the Arabic is empty. */
  fallbacks?: string[];
}

export interface Seo {
  title: string;
  description: string;
  image: Media | null;
}

export interface Link {
  label: string;
  href: string;
}

export interface Hero {
  eyebrow: string;
  headline: string;
  subline: string;
  primary: Link;
  secondary: Link;
  video: { mp4: FileRef | null; webm: FileRef | null; mobile: FileRef | null };
  poster: Media | null;
}

export interface SiteSettings {
  companyName: string;
  shortName: string;
  tagline: string;
  groupRelationship: string;
  hero: Hero;
  logos: { light: FileRef | null; dark: FileRef | null; favicon: FileRef | null };
  phone: string;
  email: string;
  whatsapp: string;
  showWhatsapp: boolean;
  address: string;
  socials: Array<{ network: 'linkedin' | 'x_twitter' | 'facebook' | 'instagram' | 'youtube'; href: string }>;
  seoTitle: string;
  seoDescription: string;
  defaultOgImage: Media | null;
  analytics: { provider: 'plausible' | 'ga4'; id: string } | null;
  cookieNotice: string;
  turnstileEnabled: boolean;
  turnstileSiteKey: string;
  capabilityGate: boolean;
  capabilityStatement: { id: number; slug: string; gated: boolean } | null;
  comingSoon: boolean;
  showPendingContent: boolean;
  fallbacks?: string[];
}

export interface NavItem {
  label: string;
  link: string;
  megaMenu: '' | 'services' | 'sectors';
  children: NavItem[];
}

export interface Navigation {
  header: NavItem[];
  footer: Array<{ title: string; items: NavItem[] }>;
  legal: NavItem[];
  mega: { services: ServiceCard[]; sectors: SectorCard[] };
}

export interface Ref {
  slug: string;
  name: string;
  icon?: string;
}

export interface Pillar extends Gated {
  id: number;
  name: string;
  color: 'green' | 'blue' | 'grey';
  icon: string;
  summary: string;
  detail: string;
}

export interface KPI extends Gated {
  id: number;
  value: number;
  prefix: string;
  suffix: string;
  label: string;
  source: string;
}

export interface LifecycleStage extends Gated {
  id: number;
  name: string;
  icon: string;
  summary: string;
  deliverables: string[];
}

export interface Client extends Gated {
  id: number;
  name: string;
  kind: 'client' | 'partner';
  website: string;
  logo: FileRef | null;
}

export interface Testimonial extends Gated {
  id: number;
  quote: string;
  person: string;
  role: string;
  company: string;
  photo: Media | null;
  project: { slug: string; title: string } | null;
}

export interface ServiceCard extends Gated {
  slug: string;
  name: string;
  icon: string;
  summary: string;
  featured: boolean;
  image: Media | null;
}

export interface Service extends ServiceCard {
  overview: string;
  deliverables: Array<{ text: string }>;
  steps: Array<{ title: string; body: string }>;
  faqs: Array<{ question: string; answer: string }>;
  sectors: Ref[];
  projects: ProjectCard[];
  seo: Seo;
  updatedAt: string;
}

export interface SectorCard extends Gated {
  slug: string;
  name: string;
  icon: string;
  summary: string;
  image: Media | null;
}

export interface Sector extends SectorCard {
  intro: string;
  services: ServiceCard[];
  projects: ProjectCard[];
  seo: Seo;
  updatedAt: string;
}

export type ProjectStatus = 'ongoing' | 'completed';

export interface ProjectCard extends Gated {
  slug: string;
  title: string;
  summary: string;
  location: string;
  country: string;
  status: ProjectStatus;
  sector: Ref | null;
  client: string | null;
  featured: boolean;
  image: Media | null;
}

export interface Project extends ProjectCard {
  role: string;
  challenge: string;
  approach: string;
  outcome: string;
  services: Ref[];
  metrics: Array<{ label: string; value: string; unit: string; delta: string }>;
  gallery: Array<{ caption: string; image: Media | null }>;
  facts: {
    value: { amount: number; currency: string } | null;
    start: string | null;
    end: string | null;
    durationMonths: number | null;
  };
  related: ProjectCard[];
  seo: Seo;
  updatedAt: string;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ProjectList extends Paginated<ProjectCard> {
  facets: { countries: string[]; sectors: Ref[]; services: Ref[] };
}

export interface InsightCategory {
  slug: string;
  name: string;
}

export interface InsightCard extends Gated {
  slug: string;
  title: string;
  excerpt: string;
  category: InsightCategory | null;
  author: string;
  publishedAt: string;
  readingMinutes: number;
  image: Media | null;
}

export interface Insight extends InsightCard {
  body: string;
  seo: Seo;
  updatedAt: string;
}

export interface InsightList extends Paginated<InsightCard> {
  categories: InsightCategory[];
}

export interface TeamMember extends Gated {
  id: number;
  name: string;
  role: string;
  bio: string;
  linkedin: string;
  leadership: boolean;
  photo: Media | null;
}

export interface Office extends Gated {
  id: number;
  city: string;
  country: string;
  address: string;
  phone: string;
  email: string;
  isHeadquarters: boolean;
  coordinates: { lat: number; lng: number } | null;
  mapImage: Media | null;
}

export interface Certification extends Gated {
  id: number;
  name: string;
  issuer: string;
  kind: 'certification' | 'membership';
  year: number | null;
  logo: FileRef | null;
}

export interface Download extends Gated {
  id: number;
  slug: string;
  title: string;
  description: string;
  gated: boolean;
  isCapabilityStatement: boolean;
  file: FileRef | null;
}

export interface JobCard extends Gated {
  slug: string;
  title: string;
  location: string;
  employmentType: string;
  summary: string;
  isOpen: boolean;
  postedAt: string;
  closesAt: string | null;
}

export interface Job extends JobCard {
  description: string;
  seo: Seo;
  updatedAt: string;
}

export type BlockKind = 'rich_text' | 'image_text' | 'stats' | 'quote' | 'gallery' | 'cta' | 'faq';

export interface PageBlock {
  id: number;
  kind: BlockKind;
  navy: boolean;
  eyebrow: string;
  title: string;
  body: string;
  attribution: string;
  imageOnEnd: boolean;
  ctaLabel: string;
  ctaLink: string;
  image: Media | null;
  items: Array<{ label: string; value: string; text: string; image: Media | null }>;
}

export interface Page extends Gated {
  slug: string;
  title: string;
  eyebrow: string;
  intro: string;
  image: Media | null;
  blocks: PageBlock[];
  seo: Seo;
  updatedAt: string;
}

export type HomeSectionKind =
  | 'hero'
  | 'trust'
  | 'pillars'
  | 'services'
  | 'kpis'
  | 'projects'
  | 'approach'
  | 'sectors'
  | 'testimonial'
  | 'insights'
  | 'cta';

interface SectionBase<K extends HomeSectionKind, D> {
  kind: K;
  eyebrow: string;
  title: string;
  intro: string;
  ctaLabel: string;
  ctaLink: string;
  secondaryLabel: string;
  secondaryLink: string;
  image: Media | null;
  data: D;
}

export type HomeSection =
  | SectionBase<'hero', Hero>
  | SectionBase<'trust', Client[]>
  | SectionBase<'pillars', Pillar[]>
  | SectionBase<'services', ServiceCard[]>
  | SectionBase<'kpis', KPI[]>
  | SectionBase<'projects', ProjectCard[]>
  | SectionBase<'approach', LifecycleStage[]>
  | SectionBase<'sectors', SectorCard[]>
  | SectionBase<'testimonial', Testimonial>
  | SectionBase<'insights', InsightCard[]>
  | SectionBase<'cta', { id?: number; slug?: string; gated?: boolean }>;

export interface Home {
  sections: HomeSection[];
}

export interface Redirect {
  oldPath: string;
  newPath: string;
  permanent: boolean;
}

export interface SitemapEntry {
  path: string;
  updatedAt: string;
}
