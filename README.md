# 3 Pillars Project Management Services — website + CMS

Bilingual (English / Arabic-RTL) business-development website for Three Pillars
Project Management Services, with a Django admin from which every piece of public
content is edited. Editors: see [EDITING.md](EDITING.md). Servers: see
[deploy/README.md](deploy/README.md).

| Part | Stack |
|---|---|
| Website `/` | Next.js 16 (App Router), React 19, TypeScript strict, Tailwind CSS v4 tokens, GSAP ScrollTrigger (lazy), Lenis (lazy), lucide-react |
| CMS `/backend` | Django 5.2, django-unfold 0.104.1 + `adminkit`, DRF 3.15, django-filter, django-otp, Pillow, nh3 |

## Run it locally

```bash
# 1. CMS
cd backend
python -m venv .venv && .venv/Scripts/activate      # macOS/Linux: source .venv/bin/activate
cp .env.example .env                                 # then set SECRET_KEY and REVALIDATE_SECRET
python manage.py migrate
python manage.py seed_content                        # the content document's copy, all "awaiting approval"
python manage.py check_content                       # copy matches the document, no banned wording, no near-duplicate pages
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000

# 2. Website (second terminal, repo root)
npm install
cp .env.example .env.local                           # same REVALIDATE_SECRET as the backend
npm run dev                                          # http://localhost:3000
```

The seeded Site settings start with **coming-soon ON** (safe default). Turn it off in
the admin (Site settings → Switches) to see the site, or use `?preview=<PREVIEW_TOKEN>`.

## How content reaches the page

```
Admin save ──► Django signal ──► signed webhook (HMAC-SHA256) ──► /api/revalidate ──► revalidateTag
                                                                                         │
Browser ◄── Next page (cached with fetch tags, 5-min fallback) ◄── typed client src/lib/cms
```

- **One typed client** — `src/lib/cms/` (`types.ts` mirrors every serializer). Every
  fetch carries cache tags (`services`, `projects`, …); each Django model declares the
  tags its saves invalidate (`cache_tags`).
- **Approval gate** — every publishable model has `approval`. The API serves approved
  rows only, unless *Site settings → Show content awaiting approval* is on (staging),
  in which case pending rows come with `pending: true` and render with a marker.
  The gate lives in one place: `apps/core/api.py → GatedReadOnlyViewSet`.
- **Arabic** — every text field `x` has `x_ar`. `?locale=ar` returns Arabic with
  English fallback; fallen-back field names are listed in `fallbacks`.
- **Outages** — lists and site-wide data fall back to `src/content/fallback.ts`;
  detail pages keep serving their last good cached render.
- **Wire format** — camelCase JSON both ways (`apps/core/wire.py`).

## Layout

```
src/app/[locale]/…        routes (root layout per locale; proxy.ts adds the locale)
src/components/ui         primitives (Button, Card, Section, Carousel, Lightbox, Tabs…)
src/components/motion     Reveal / LineReveal (server-marked, one observer drives them)
src/components/home       VideoHero, PillarsShowcase (pinned), ApproachTimeline (scrubbed)
src/components/forms      fields + Contact, ProposalWizard, Application, DownloadGate
src/styles/palette.css    generated brand scales (node scripts/generate-palette.mjs)
src/app/globals.css       design tokens (@theme) — components use tokens only
backend/adminkit          copied verbatim from HS Investment — never edit
backend/apps/core         bases, settings, nav, pages, redirects, webhook, security
backend/apps/content      services, sectors, projects, insights, team, KPIs…
backend/apps/bd           enquiries, consultation requests, download leads, pipeline
backend/apps/careers      jobs, applications (private CV storage)
```

A component styleguide lives at `/en/_styleguide` and `/ar/_styleguide` (not linked,
not indexed, off in production unless `STYLEGUIDE=true`).

## Checks

```bash
npm run lint          # ESLint, zero warnings allowed
npm run typecheck     # next typegen + tsc --noEmit
npm test              # Vitest: token contrast (fails on any text pair < 4.5:1)
npm run build
npm run test:e2e      # Playwright, desktop + mobile, needs both servers running

cd backend
python manage.py test                 # adminkit's 37 + project tests
python manage.py check --deploy       # with DEBUG=False and production env
```

E2E covers: every template in both languages, 404s, locale redirect, navigation,
RTL mirroring, no horizontal overflow, every form (validation + submit + uploads),
hero video pause/resume, hero scrim contrast over a white frame, reduced motion,
and axe (WCAG 2.2 AA, zero serious/critical) on every template. Form tests create
records named "E2E" — run against development or staging only.

## Conventions

- No raw colour values in components; add a token in `globals.css` (and a contrast
  row in `tests/unit/contrast.test.ts` if it is used for text).
- Logical CSS only (`ms-`, `pe-`, `start-`…); ESLint rejects `ml-`/`left-` etc.
- Interface strings live in `src/i18n/dictionaries.ts`; content comes from the CMS.
- Every admin imports from `unfold.admin`. Missing it leaves that screen unstyled.
- `revalidateTag(tag, { expire: 0 })` in the webhook — Next 16's API (read
  `node_modules/next/dist/docs/` before touching caching).
