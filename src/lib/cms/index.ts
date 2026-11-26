import 'server-only';
import { cache } from 'react';
import { fallbackHome, fallbackNavigation, fallbackSettings } from '@/content/fallback';
import type { Locale } from '@/i18n/config';
import { cmsGet, cmsGetOr } from './client';
import type {
  ApproachStep,
  Certification,
  Download,
  Home,
  Insight,
  InsightList,
  Job,
  JobCard,
  Navigation,
  Office,
  Page,
  Pillar,
  Project,
  ProjectList,
  Redirect,
  Sector,
  SectorCard,
  Service,
  ServiceCard,
  SiteSettings,
  SitemapEntry,
  TeamMember,
} from './types';

/*
 * Lists and site-wide data fall back to static content when the CMS is down.
 * Detail fetchers throw instead: during a background revalidation that keeps
 * the last good page in the cache, and on a cold cache the error page tells
 * the truth rather than a fake 404.
 */

export const getSettings = cache((locale: Locale) =>
  cmsGetOr<SiteSettings>('site-settings/', { tags: ['settings'], locale }, fallbackSettings(locale)),
);

export const getNavigation = cache((locale: Locale) =>
  cmsGetOr<Navigation>('navigation/', { tags: ['navigation'], locale }, fallbackNavigation(locale)),
);

export const getHome = (locale: Locale) => cmsGetOr<Home>('home/', { tags: ['home'], locale }, fallbackHome(locale));

export const getServices = (locale: Locale) => cmsGetOr<ServiceCard[]>('services/', { tags: ['services'], locale }, []);
export const getService = cache((locale: Locale, slug: string) =>
  cmsGet<Service>(`services/${slug}/`, { tags: ['services', 'projects'], locale }),
);

export const getSectors = (locale: Locale) => cmsGetOr<SectorCard[]>('sectors/', { tags: ['sectors'], locale }, []);
export const getSector = cache((locale: Locale, slug: string) =>
  cmsGet<Sector>(`sectors/${slug}/`, { tags: ['sectors', 'services', 'projects'], locale }),
);

export interface ProjectFilters {
  sector?: string;
  service?: string;
  role?: string;
  type?: string;
  page?: string;
}

const EMPTY_PROJECTS: ProjectList = {
  count: 0,
  next: null,
  previous: null,
  results: [],
  facets: { sectors: [], services: [], roles: [], types: [] },
};

export const getProjects = (locale: Locale, filters: ProjectFilters = {}) =>
  cmsGetOr<ProjectList>('projects/', { tags: ['projects'], locale, params: { ...filters } }, EMPTY_PROJECTS);
export const getProject = cache((locale: Locale, slug: string) =>
  cmsGet<Project>(`projects/${slug}/`, { tags: ['projects'], locale }),
);

export interface InsightFilters {
  category?: string;
  kind?: string;
  page?: string;
}

export const getInsights = (locale: Locale, params: InsightFilters = {}) =>
  cmsGetOr<InsightList>(
    'insights/',
    { tags: ['insights'], locale, params: { category__slug: params.category, kind: params.kind, page: params.page } },
    { count: 0, next: null, previous: null, results: [], categories: [], kinds: [] },
  );
export const getInsight = cache((locale: Locale, slug: string) =>
  cmsGet<Insight>(`insights/${slug}/`, { tags: ['insights'], locale }),
);

export const getPage = cache((locale: Locale, slug: string) =>
  cmsGet<Page>(`pages/${slug}/`, { tags: ['pages'], locale }),
);

export const getPillars = (locale: Locale) => cmsGetOr<Pillar[]>('pillars/', { tags: ['pillars'], locale }, []);
export const getApproachSteps = (locale: Locale) =>
  cmsGetOr<ApproachStep[]>('approach-steps/', { tags: ['approach'], locale }, []);

export const getTeam = (locale: Locale) => cmsGetOr<TeamMember[]>('team/', { tags: ['team'], locale }, []);
export const getOffices = (locale: Locale) => cmsGetOr<Office[]>('offices/', { tags: ['offices'], locale }, []);
export const getCertifications = (locale: Locale) =>
  cmsGetOr<Certification[]>('certifications/', { tags: ['certifications'], locale }, []);
export const getDownloads = (locale: Locale) => cmsGetOr<Download[]>('downloads/', { tags: ['downloads'], locale }, []);

export const getJobs = (locale: Locale) => cmsGetOr<JobCard[]>('jobs/', { tags: ['jobs'], locale }, []);
export const getJob = cache((locale: Locale, slug: string) => cmsGet<Job>(`jobs/${slug}/`, { tags: ['jobs'], locale }));

export const getRedirects = () => cmsGetOr<Redirect[]>('redirects/', { tags: ['redirects'] }, []);
export const getSitemap = () =>
  cmsGetOr<SitemapEntry[]>('sitemap/', { tags: ['pages', 'services', 'sectors', 'projects', 'insights', 'jobs'] }, []);
