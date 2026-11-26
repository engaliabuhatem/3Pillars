# Gap report: repositioning to the three-pillar content

Phase 0 audit. Nothing has been changed or deleted yet. This report maps every existing page, model, route and seeded row to what happens to it, and lists the decisions that need a sign-off before Phase 1.

Audited: `main` at `20adc17` plus uncommitted admin restyle work (9 modified files and `backend/static/css/admin-apple.css`, see §8). Next.js 16.4.6, React 19.3, Django dev DB `backend/db.sqlite3`.

---

## 0. Blockers

| # | Blocker | Effect |
|---|---|---|
| B1 | **`docs/content/3pillars-content.md` does not exist.** It isn't in the repo, git history, `~/Downloads`, `~/Desktop`, `~/Documents` or the other likely folders on D:. The only 3 Pillars files on disk are the brand CI PDF, the logo and the hero videos. | Blocks Phase 2 (seed), the copy check (§9) and every content-dependent field. Phase 1 (models, migrations, admin) can mostly run without it, because the field list comes from the prompt. However, these structural values come from the document: the 8 draft article topics, the 6 company values, the 3 value points, the 5 approach steps, the LaunchReadiness item list, `list_title` per sector and the keyword clusters. |
| B2 | **`claude/3pillars-master-prompt.md` does not exist.** The prompt says to run "the master prompt's full §11 test suite" and keep its standards. | I can infer §11 from the existing tests (`backend/apps/*/tests.py`, `backend/adminkit/tests.py`, `tests/e2e/*.spec.ts`, `tests/unit/contrast.test.ts`), but cannot confirm it matches. |
| B3 | **`docs/content/glossary-en-ar.md` does not exist.** | Not blocking: I can create it in Phase 2 from the terms in the prompt (see decision D14). |

**Needed to continue past Phase 1:** put the content document at `docs/content/3pillars-content.md`. The master prompt is optional but useful.

---

## 1. Current state of the dev database (affects how the seed is written)

| Fact | Consequence |
|---|---|
| All 8 old services, 5 old sectors, 3 pillars, 5 lifecycle stages and all 13 pages are **approved**. | They are public right now. Deleting or replacing them makes the public site (with Show pending off) show only empty states until an Approver approves the new copy. That is the intended result, but it is a visible change. |
| `coming_soon = False`, `show_pending_content = True`. | The dev site is fully open. With pending on, the new pending copy shows immediately after seeding. |
| One `Office` row (Aden, Yemen, pending, address "Placeholder — …"). | This is a fact claim (office location) that the document is supposed to supply. It will be deleted (§2.9: do not seed any address). |
| 43 `Enquiry` and 26 `ProposalRequest` rows, all `e2e@example.com`. | Playwright residue. Deleting old services/sectors clears their `services` M2M and sets `sector` to NULL on these rows. That's harmless and they will be kept. |
| 0 projects, clients, testimonials, KPIs, team members, certifications, insights or downloads. | Nothing to migrate for the proof models. |
| 0 `Redirect` rows. | No existing redirects to clean up. |
| 18 `NavItem` rows (8 header, 7 footer, 3 legal) and 2 `InsightCategory` rows (News, Articles). | All header and footer rows are replaced. Legal rows are kept. |

---

## 2. Routes (`src/app/[locale]/…`)

| Existing route | Fate | New route |
|---|---|---|
| `page.tsx` (home) | **keep**, re-render per §5.1 | `/` |
| `about/page.tsx` | **rename** | `/about-us/` |
| none | **new** | `/about-us/leadership-team/` |
| none | **new** (page row hidden until affiliation wording approved) | `/about-us/hs-group/` |
| `approach/page.tsx` | **rename + rebuild** (3 pillar sections + 3-step flow) | `/our-approach/` |
| `services/page.tsx` | **keep**, new intro + service-line table | `/services/` |
| `services/[slug]/page.tsx` | **keep**, new template §5.3 | 4 service slugs |
| `sectors/page.tsx` | **keep** | `/sectors/` |
| `sectors/[slug]/page.tsx` | **keep**, new template §5.3 | 4 sector slugs |
| `projects/page.tsx`, `projects/[slug]/page.tsx` | **keep**, add role filters and case-study order | same, plus `?type=case-study` |
| `insights/page.tsx`, `insights/[slug]/page.tsx` | **keep**, add kind filter and reading time | same, plus `?category=` |
| `careers/page.tsx`, `careers/[slug]/page.tsx` | **keep**, new intro and "View Opportunities" anchor | same |
| `contact/page.tsx` | **keep**, new form §2.9 | `/contact/` |
| `request-a-proposal/page.tsx` | **rename** | `/contact/request-a-consultation/` |
| `capability-statement/page.tsx` | **keep** as is | same |
| `[slug]/page.tsx` (privacy, terms, cookies) | **keep** as is | same |
| `coming-soon`, `not-found`, `error`, `global-error`, `global-not-found`, `[...rest]` | **keep** as is | same |
| `%5Fstyleguide/` | **keep**, add pillar card, value point, capability card, case-study facts and breadcrumb demos | same |
| `opengraph-image.tsx` | **keep** | same |
| `src/app/sitemap.ts` | **rewrite**: the static list has the old paths; add trailing slashes and the Arabic indexing rule | |
| `src/app/robots.ts` | **keep** (settings-driven) | |
| `src/proxy.ts` | **change**: currently strips trailing slashes before matching. Add trailing-slash enforcement and the preferred-host redirect. | |
| `next.config.ts` | **change**: add `trailingSlash: true`, after reading the routing docs in `node_modules/next/dist/docs/` | |

Removed old paths (`/about`, `/approach`, `/request-a-proposal`, the 4 retired service slugs, `energy`, `industrial`, `government`) will **404**. There will be no redirect rows (rule 6: one version only, see D2).

---

## 3. Models

### 3.1 `apps.core`

| Model | Fate | Changes |
|---|---|---|
| `ApprovalStatus` | **keep** | No "archived" state (rule 6). |
| `Publishable` | **change** | Add `ar_reviewed` (bool, default False). Every publishable model carries Arabic, so it belongs on the base class. |
| `Seo` (abstract) | **change** | Rename `seo_description` → `meta_description` (and `_ar`). Add `h1`, `h1_ar`, `primary_keyword`, `supporting_keywords`. `seo_title` stays at max_length 70 at DB level; the admin counter warns above 60. Applies to Page, Service, Sector, Project, Insight and Job. |
| `Slugged` | **keep** | Its auto-redirect on slug change stays as an editor feature. The seed deletes and creates rows instead of renaming slugs, so it creates no redirect rows. |
| `SiteSettings` | **change** | Add `home_seo_title`, `home_meta_description`, `home_h1` (+ `_ar`) and keyword fields (D4). Add `contact_verified`, `preferred_host` (www/apex), and per-area recipient lists (5 text fields, one per Area of Interest). Add `consent_text`, `consent_text_ar` and `consent_version`. Change the hero defaults: `hero_primary_label`/`link` "Request a proposal" → document values, and `hero_eyebrow` default "Project Management Services" → blank (set by seed). Add `hero_h1` + `_ar` (§5.1). Clear seeded `tagline` and set it from the positioning sentence. |
| `NavItem` | **keep** | Add auto-hide (computed in `NavigationView`, not stored): hide when the target is a page, service, sector or listing with no visible content. Add `is_cta` (bool) for the header "Request a Consultation" button. |
| `FooterColumn` | **keep** | Rows replaced by seed. |
| `Redirect` | **keep** | Normalise `old_path`/`new_path` to trailing slash. No seeded rows. |
| `HomeSection` | **change** | Kinds: add `intro` and `value`. **Remove** `approach` and `services` (pillar cards replace the services grid, §2.7). Keep `trust`, `kpis`, `projects`, `testimonial` and `insights`, set `visible=False`. They already auto-hide when empty (`apps/core/home.py`). Data migration deletes the `approach` and `services` rows. |
| `Page` | **change** | Add a `path` override (D3) so nested pages (`/about-us/leadership-team/`, `/about-us/hs-group/`, `/contact/request-a-consultation/`) have correct canonicals and sitemap entries. |
| `PageBlock` | **change** | Add kinds `values` (renders CompanyValue), `approach_steps` (renders ApproachStep) and `affiliation` (hidden by default; help text quotes the document's approval note, from B1). |
| `PageBlockItem` | **keep** | |
| **`LaunchReadiness`** + **`LaunchReadinessItem`** | **new** | Singleton plus rows: `item`, `kind` (claim / checklist), `status` (open/confirmed), `owner`, `note`, `confirmed_by`, `confirmed_at`. Item list comes from the document (B1). The admin warning appears when Coming soon is turned off. |

### 3.2 `apps.content`

| Model | Fate | Changes |
|---|---|---|
| `Pillar` | **repurpose** | Add `number`, `role_on_site` (lead/enabling), `core_value`, `core_outcomes`, `is_proposed` and `service` FK (nullable, to Service). Keep `name`, `summary`, `color` and `order`. **Remove** `icon` and `detail` (replaced by `core_value`/`core_outcomes`). The 3 existing rows (Governance/Delivery/Assurance) are **deleted**, and 3 new rows are created by the seed. |
| `Sector` | **change** | Add `focus_summary`, `list_title`, `our_focus`, `scope_caveat` (+ `_ar`). Keep `intro` (rich), `summary`, `icon` and `image`. Relation to services: see D5. |
| **`SectorListItem`** | **new** | Inline: `text`, `text_ar`, `order`. |
| **`SectorFAQ`** | **new** | Same shape as `ServiceFAQ`. |
| `Service` | **change** | Add `pillar` FK, `intro` (rich; **replaces** `overview`, renamed by migration), `who_we_support`, `positioning_note` (admin-only), `cta_headline`, `cta_label` and `scope_caveat` (+ `_ar` except the positioning note). Rename `sectors` → `related_sectors` (D5). **Remove** `featured` (no flagship cell any more). |
| `ServiceDeliverable` | **rename** → `ServiceCapability` | Rename `text` → `title`, then add `description` (+ `_ar`). |
| `ServiceStep` | **keep** | |
| **`ServiceBullet`** | **new** | Inline with `group_title` (e.g. "What we can support"), `text` (+ `_ar`) and `order`. |
| `ServiceFAQ` | **keep** | Hidden when empty (already true in the template). |
| `Client` | **keep** | No rows. |
| `Project` | **change** | Add `entry_type`, `delivery_entity` (required), `our_role` (choices), `our_role_detail`, `scope_of_services` (rich), `client_name_approved`, `attribution_evidence` (private file), `attribution_notes` and `attribution_approved`. Rename `outcome` → `results`. **Remove** free-text `role` (replaced by `our_role` + `our_role_detail`; 0 rows, so no data to move). Add an attribution gate in `clean()` and in the approve action. |
| `ProjectMetric`, `ProjectImage` | **keep** | |
| `Testimonial`, `KPI`, `Certification`, `TeamMember` | **keep** | Model only; never seeded. Home sections hidden. |
| `LifecycleStage` | **rename** → `ApproachStep` | Keep fields. Move off Home to the About page's approach block and `/our-approach/`. API route `approach-stages/` → `approach-steps/`. The 5 existing rows are **deleted**; the seed creates 5 from the document. |
| `Office` | **keep** model | Delete the Aden row. The contact block now reads verified Site settings fields; Office stays for later use. |
| `InsightCategory` | **keep** | Delete "News" and "Articles" (they become `kind`); seed the 6 categories from §2.6. |
| `Insight` | **change** | Add `kind` (article / market perspective / project delivery insight / news), `is_draft_topic` and `our_role_statement` (+ `_ar`). Make `body` and `excerpt` blank-able. In `clean()`, require body for approval, and require `published_at`, summary (`excerpt`) and `our_role_statement` for news. The queryset `.public()` always excludes rows with an empty body, even with pending on. |
| `Download` | **keep** | |
| **`ValuePoint`** | **new** | Publishable: `title`, `body` (+ `_ar`) and `order`. 3 rows. |
| **`CompanyValue`** | **new** | Publishable: `value` and `in_practice` (+ `_ar`). 6 rows. |

### 3.3 `apps.bd`

| Model | Fate | Changes |
|---|---|---|
| `Lead` (abstract) | **change** | Add `area_of_interest` (5 choices), `consent_text`, `consent_version` and `consent_at` (snapshot of exactly what was agreed). |
| `Enquiry` | **change** | Contact Us form. Map fields: Full Name → `name`, Organisation → `organisation`, Business Email → `email`, Phone → `phone`, Country / Location → `country`, Project or Enquiry Summary → `message`. Remove `topic` and `subject` (not in the field list), which loses that data on 43 e2e rows. |
| `ProposalRequest` | **rename (display only)** → "Consultation request" | Keep the DB model name (D6). Add `area_of_interest` to step 2. **Remove** `ProjectStage.DESIGN` and `ProjectStage.CONSTRUCTION`? See D11. |
| `DownloadLead`, notes, attachments | **keep** | |

### 3.4 `apps.careers`

| Model | Fate | Changes |
|---|---|---|
| `Job` | **keep** | Gains the `Seo` and `ar_reviewed` changes. JobPosting JSON-LD only when required fields are present. |
| `Application` | **keep** | |

---

## 4. Seed

| Item | Fate |
|---|---|
| `backend/apps/core/seed_data.py` | **delete** (every row is old placeholder copy) |
| `backend/apps/core/management/commands/seed.py` | **delete**, replaced by `backend/apps/content/management/commands/seed_content.py` |
| `backend/apps/content/seed_data/content.py` | **new**: transcription of the document (B1) |
| `docs/content/glossary-en-ar.md` | **new** |
| `docs/seo/keyword-clusters.md` | **new**, from document §18 (B1) |
| Old seeded rows | **delete**: 8 services (and their 5 deliverables, 4 steps), 5 sectors, 3 pillars, 5 lifecycle stages, 1 office, 2 insight categories, 15 header/footer nav items and 2 footer columns. Pages `about`, `approach` and `request-a-proposal` are deleted and recreated under their new slugs. The other page rows are updated in place by slug. |
| `HomeSection` rows `approach`, `services` | **delete** |
| Seed rows that stay | Legal nav rows; the `privacy`, `terms`, `cookies` and `capability-statement` pages (content untouched); Site settings switches and analytics. |

---

## 5. Frontend components and libraries

| File | Fate |
|---|---|
| `components/home/HomeSections.tsx` | **change**: add `Intro` and `Value`; Pillars become 3 numbered cards that link to the service; remove `Services` and `Approach`; CTA from the section row. |
| `components/home/PillarsShowcase.tsx` | **repurpose** into numbered pillar cards with a "Proposed" tag. |
| `components/home/ApproachTimeline.tsx` | **move** to the `/our-approach/` and About approach block. |
| `components/home/VideoHero.tsx` | **change**: `h1` line above the display headline (`<p>`). |
| `components/home/TrustStrip.tsx` | **keep** (hidden section). |
| `components/brand/ThreeArcs.tsx` | **reuse** for the "How the pillars work together" flow. |
| `components/content/Cards.tsx` | **change**: `ServiceCard` loses `large`; add `CapabilityCard`, `ValuePoint`, `PillarCard` and `CaseStudyFacts`. |
| `components/content/PageHeader.tsx` | **change**: renders CMS `h1` when set; breadcrumbs already present, so check that JSON-LD is emitted on every detail page. |
| `components/content/ProjectFilters.tsx` | **change**: add our-role and type filters. |
| `components/content/OfficeCard.tsx` | **keep**, unused on Contact (verified Site settings fields replace it). |
| `components/layout/Header.tsx`, `MegaMenu.tsx` | **change**: dropdown children, CTA button, auto-hidden items. |
| `components/layout/Footer.tsx` | **keep** (data-driven). |
| `components/forms/ContactForm.tsx` | **rewrite** to the §2.9 fields, consent text from settings, and an Area-of-Interest analytics event. |
| `components/forms/ProposalWizard.tsx` | **rename** → `ConsultationWizard`, add Area of Interest to step 2 and step events. |
| `lib/cms/types.ts`, `lib/cms/index.ts` | **change** to match the API. |
| `lib/seo.tsx` | **change**: trailing-slash canonicals, Arabic noindex and hreflang rule, `WebSite`, `Article` and `JobPosting` JSON-LD, `meta_description`/`h1`. |
| `content/fallback.ts` | **audit in Phase 3**: offline fallback copy may contain old positioning. |
| `i18n/dictionaries.ts` | **change**: UI strings ("Request a proposal", "The outcome", etc.) → new labels. It has `group: 'HS Group'`, which stays as a UI label only. |
| `lib/analytics.ts` | **change**: add the 2 events. |

---

## 6. API (`backend/config/api_urls.py`)

| Endpoint | Fate |
|---|---|
| `services/`, `sectors/`, `projects/`, `insights/`, `pages/`, `jobs/`, `pillars/`, `team/`, `downloads/`, `certifications/`, `offices/` | **keep**, serializers updated |
| `approach-stages/` | **rename** → `approach-steps/` |
| `proposal-requests/` | **rename** → `consultation-requests/`; front and back deploy together |
| `enquiries/` | **keep**, new fields |
| **`value-points/`, `company-values/`** | **new** (or nested in `home/` and `pages/about-us/`) |
| `sitemap/` | **change**: per-locale entries for the Arabic rule; excludes draft topics |
| `navigation/` | **change**: auto-hide and CTA flag |

---

## 7. Tests

| Existing | Fate |
|---|---|
| `backend/apps/core/tests.py` (26) | **update**: lines 105 and 116 reference "Design Management". |
| `backend/apps/bd/tests.py` (13) | **update** for the new form fields and renamed endpoint. |
| `backend/adminkit/tests.py` (37) | **update** sidebar and dashboard expectations. |
| `tests/e2e/smoke.spec.ts`, `forms.spec.ts`, `a11y.spec.ts`, `motion.spec.ts` | **update** paths and forms. |
| `tests/unit/contrast.test.ts` | **keep** |
| **New** | Attribution gate, Arabic indexing rule, draft topics never public, nav auto-hide, consent stored, routes 200 in EN/AR, one `<h1>` and unique titles, copy check (needs B1), grep check, thin-content check, no-leak with pending off. |

Grep for banned terms in current code (to be zero after Phase 2): `seed_data.py` lines 67, 71, 74, 75, 89 and 110 ("Quantity Surveying", "Design Management", "Construction Supervision", "supervision", "contractor"), plus `core/tests.py`. No HS Group project names or figures exist anywhere in the code.

---

## 8. Uncommitted work in the tree

The working tree has an unfinished admin restyle (`admin-apple.css`, changes to 5 `admin.py` files, `admin_base.py`, `settings.py` and `admin-brand.css`). Phase 1 edits the same admin files. **I recommend committing or stashing it before Phase 1** so the two changes stay separate. I haven't touched it.

---

## 9. Decisions (need sign-off; my recommendation is first)

| # | Question | Decision | Rejected alternative |
|---|---|---|---|
| D1 | Replace old service/sector rows: update in place or delete? | **Delete and create.** Updating `project-management-consultancy` in place to `project-programme-management` would make `Slugged.save()` write a Redirect row, which keeps the old URL alive, against rule 6. | Update in place (keeps PKs and links on e2e leads, but creates redirects). |
| D2 | Old URLs: 404 or redirect? | **404**, as the revised prompt says. Risk: if any old URL was ever indexed or shared on a real host, it now breaks. The dev DB shows the site open (`coming_soon` off). If production was ever public, I'd add a short Redirect list instead. **Please confirm production was never public.** | 301s to the closest page. |
| D3 | Nested CMS pages (`/about-us/leadership-team/`, `/contact/request-a-consultation/`) | Add a `path` override field on `Page`, with a dedicated Next route for each. The `[slug]` catch-all ignores pages with a custom path. | Parent FK tree (overkill for 3 pages). |
| D4 | Where do Home SEO, H1 and keywords live? | **SiteSettings `home_*` fields.** | A `Page` row with slug `home`, which collides with the `[slug]` route (`/home/` would render). |
| D5 | Service ↔ sector relation | **One M2M** (`Service.related_sectors`), with the reverse exposed as `Sector.related_services` through an admin form field that writes the same table. Bidirectional links can never disagree. | Two independent M2Ms (they would drift). |
| D6 | Proposal → Consultation rename depth | Rename the **display name, admin, API path and frontend**, and keep the DB model `ProposalRequest`. This avoids renaming tables that hold private uploaded files. | `RenameModel` (cosmetic gain, migration risk on file paths and permissions). |
| D7 | `Seo.seo_title` limit 70 vs counter ≤ 60 | Keep DB 70; the admin counter warns above 60. | Shrink to 60 (would truncate existing values). |
| D8 | `ar_reviewed` placement | On `Publishable` (every Arabic-bearing content row). The indexing rule reads it on page-level models only. | Only on page-level models (Pillar, CompanyValue and others then can't be tracked for review). |
| D9 | Draft topics: never public even with pending on | A model-level `.public()` filter that excludes rows with `is_draft_topic=True` and an empty body, used by every Insight endpoint, sitemap and home section. | A view-level check (easy to miss in one place). |
| D10 | Thin-content "build-time" check | A Django test plus a `manage.py check_thin_content` command run in CI. The content lives in the CMS, and `next build` may run without CMS access. | A Next build step (fails when the CMS isn't reachable at build). |
| D11 | Consultation wizard `project_stage` choices include "Design" and "Construction" | **Keep.** They describe the *client's* project stage, not a 3 Pillars service, so they don't present 3 Pillars as a designer or contractor. | Remove them. Your call if you read rule 5 more strictly. |
| D12 | Redirect status codes | The proxy currently returns 308/307. Keep it for editor-created redirects. Trailing-slash and host redirects use 308 (permanent, method-preserving). | 301. |
| D13 | Nav auto-hide gate | Follows the same gate as content: an item shows when its target has visible content under the current "Show pending" setting. Projects hides at 0 approved projects regardless. | Hide on "not approved" even with pending on (staging nav would then hide everything being reviewed). |
| D14 | Market Intelligence in Arabic | **المعلومات السوقية**, used everywhere. | استخبارات السوق, which has security-service connotations in Arabic and reads poorly for a B2B advisory. |
| D15 | Old HomeSection kinds `services` and `approach` | **Delete** the rows and remove the kinds from the choices (rule 6). | Keep them hidden. |
| D16 | `Enquiry.topic`/`subject` | Remove (not in the §2.9 field list). Data loss is limited to e2e test rows. | Keep them hidden. |

---

## 10. Phase plan once B1 is resolved

1. **Models and migrations**: everything in §3, admin §3 of the prompt, new-rule tests. Can start now apart from item lists and help text quoting the document.
2. **Seed**: `seed_content`, glossary and keyword clusters. **Blocked on B1.**
3. **Routes and templates**: §2 and §5.
4. **SEO and quality**: sitemap, JSON-LD, Arabic rule, thin-content, copy check (B1), full suite.
5. **Final report.**
