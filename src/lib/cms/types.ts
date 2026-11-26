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

/** Which language versions search engines may index (approved; Arabic also reviewed). */
export interface Indexable {
  en: boolean;
  ar: boolean;
}

export interface Seo {
  title: string;
  description: string;
  /** The page's single <h1>; empty means "use the title". */
  h1: string;
  image: Media | null;
  indexable: Indexable;
}

export interface Link {
  label: string;
  href: string;
}

export interface Hero {
  /** The home page <h1>, set as the small line above the display headline. */
  h1: string;
  eyebrow: string;
  headline: string;
  subline: string;
  primary: Link;
  secondary: Link;
  video: { mp4: FileRef | null; webm: FileRef | null; mobile: FileRef | null };
  poster: Media | null;
  /** Portrait still for phones; falls back to `poster`. */
  posterMobile: Media | null;
}

export interface SiteSettings {
  companyName: string;
  shortName: string;
  /** The positioning statement. */
  tagline: string;
  groupRelationship: string;
  hero: Hero;
  logos: { light: FileRef | null; dark: FileRef | null; favicon: FileRef | null };
  /** Contact fields are empty until Site settings marks them verified. */
  phone: string;
  email: string;
  whatsapp: string;
  showWhatsapp: boolean;
  address: string;
  businessHours: string;
  socials: Array<{ network: 'linkedin' | 'x_twitter' | 'facebook' | 'instagram' | 'youtube'; href: string }>;
  seoTitle: string;
  seoDescription: string;
  homeSeo: Seo;
  preferWww: boolean;
  defaultOgImage: Media | null;
  analytics: { provider: 'plausible' | 'ga4'; id: string } | null;
  cookieNotice: string;
  consentText: string;
  turnstileEnabled: boolean;
  turnstileSiteKey: string;
  capabilityGate: boolean;
  capabilityStatement: { id: number; slug: string; gated: boolean } | null;
  comingSoon: boolean;
  showPendingContent: boolean;
  copyPending: boolean;
  fallbacks?: string[];
}

export interface NavItem {
  label: string;
  link: string;
  megaMenu: '' | 'services' | 'sectors';
  isCta: boolean;
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

export type PillarColor = 'green' | 'blue' | 'grey';

export interface Pillar extends Gated {
  id: number;
  number: number;
  name: string;
  roleOnSite: 'lead' | 'enabling';
  color: PillarColor;
  coreValue: string;
  summary: string;
  detail: string;
  coreOutcomes: string;
  covers: string;
  isProposed: boolean;
  service: Ref | null;
}

export interface ValuePoint extends Gated {
  id: number;
  title: string;
  body: string;
}

export interface CompanyValue extends Gated {
  id: number;
  value: string;
  inPractice: string;
}

export interface ApproachStep extends Gated {
  id: number;
  name: string;
  summary: string;
}

export interface KPI extends Gated {
  id: number;
  value: number;
  prefix: string;
  suffix: string;
  label: string;
  source: string;
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
  pillar: { number: number; color: PillarColor; isProposed: boolean } | null;
  image: Media | null;
}

export interface Faq {
  question: string;
  answer: string;
}

export interface Service extends ServiceCard {
  intro: string;
  capabilitiesTitle: string;
  capabilities: Array<{ title: string; description: string }>;
  bulletsTitle: string;
  bullets: Array<{ text: string }>;
  scopeCaveat: string;
  stepsTitle: string;
  steps: Array<{ title: string; body: string }>;
  contextTitle: string;
  contextBody: string;
  whoWeSupport: string;
  faqs: Faq[];
  relatedSectors: SectorCard[];
  projects: ProjectCard[];
  ctaHeadline: string;
  ctaLabel: string;
  seo: Seo;
  updatedAt: string;
}

export interface SectorCard extends Gated {
  slug: string;
  name: string;
  icon: string;
  focusSummary: string;
  image: Media | null;
}

export interface Sector extends SectorCard {
  intro: string;
  listTitle: string;
  listItems: Array<{ text: string }>;
  scopeCaveat: string;
  ourFocus: string;
  relatedServices: ServiceCard[];
  projects: ProjectCard[];
  insights: InsightCard[];
  faqs: Faq[];
  seo: Seo;
  updatedAt: string;
}

export type ProjectStatus = 'ongoing' | 'completed';
export type ProjectRole = 'project_manager' | 'pmo_support' | 'advisor' | 'bd_support' | 'other';

export interface ProjectCard extends Gated {
  slug: string;
  title: string;
  entryType: 'selected' | 'case_study';
  summary: string;
  location: string;
  country: string;
  status: ProjectStatus;
  sector: Ref | null;
  client: string | null;
  deliveryEntity: string;
  /** Display label of 3 Pillars' role. */
  ourRole: string;
  roleKey: ProjectRole;
  featured: boolean;
  image: Media | null;
}

export interface Project extends ProjectCard {
  ourRoleDetail: string;
  challenge: string;
  scopeOfServices: string;
  approach: string;
  results: string;
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

export interface Facet {
  value: string;
  label: string;
}

export interface ProjectList extends Paginated<ProjectCard> {
  facets: { sectors: Ref[]; services: Ref[]; roles: Facet[]; types: Facet[] };
}

export interface InsightCategory {
  slug: string;
  name: string;
}

export type InsightKind = 'article' | 'perspective' | 'delivery' | 'news';

export interface InsightCard extends Gated {
  slug: string;
  title: string;
  kind: InsightKind;
  excerpt: string;
  category: InsightCategory | null;
  author: string;
  publishedAt: string | null;
  readingMinutes: number;
  image: Media | null;
}

export interface Insight extends InsightCard {
  body: string;
  ourRoleStatement: string;
  seo: Seo;
  updatedAt: string;
}

export interface InsightList extends Paginated<InsightCard> {
  categories: InsightCategory[];
  kinds: Array<{ value: InsightKind; label: string }>;
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

export type BlockKind =
  | 'rich_text'
  | 'image_text'
  | 'stats'
  | 'quote'
  | 'gallery'
  | 'cta'
  | 'faq'
  | 'values'
  | 'approach_steps'
  | 'affiliation';

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
  /** Company values or approach steps, for blocks of those kinds. */
  entries: Array<CompanyValue | ApproachStep>;
}

export interface Page extends Gated {
  slug: string;
  path: string;
  title: string;
  eyebrow: string;
  intro: string;
  ctaLabel: string;
  image: Media | null;
  blocks: PageBlock[];
  seo: Seo;
  updatedAt: string;
}

export type HomeSectionKind =
  | 'hero'
  | 'intro'
  | 'pillars'
  | 'sectors'
  | 'value'
  | 'cta'
  | 'trust'
  | 'kpis'
  | 'projects'
  | 'testimonial'
  | 'insights';

interface SectionBase<K extends HomeSectionKind, D> extends Gated {
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
  | SectionBase<'intro', Record<string, never>>
  | SectionBase<'pillars', Pillar[]>
  | SectionBase<'sectors', SectorCard[]>
  | SectionBase<'value', ValuePoint[]>
  | SectionBase<'cta', { id?: number; slug?: string; gated?: boolean }>
  | SectionBase<'trust', Client[]>
  | SectionBase<'kpis', KPI[]>
  | SectionBase<'projects', ProjectCard[]>
  | SectionBase<'testimonial', Testimonial>
  | SectionBase<'insights', InsightCard[]>;

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
  /** Whether the Arabic version may be listed. */
  ar: boolean;
}
