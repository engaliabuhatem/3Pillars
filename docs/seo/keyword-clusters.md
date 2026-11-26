# Keyword clusters

From section 18 of `docs/content/3pillars-content.md`, verbatim. Keywords are editor guidance: each page's primary and supporting keywords are stored in its SEO tab and are never output as a `<meta name="keywords">` tag.

| Cluster | Primary themes | Target pages |
|---|---|---|
| Project Management | project management consultancy; project and programme management; construction project management | Home; Services; Project & Programme Management |
| PMO & Controls | PMO services; project controls; schedule management; cost control; project reporting | PMO & Project Controls |
| Business Development | business development consulting; market expansion; opportunity identification; tender strategy | Business Development |
| Market Intelligence | market research; country market study; sector analysis; opportunity assessment | Strategic Advisory; Research & Studies |
| Infrastructure | infrastructure project management; transport project management; water infrastructure | Infrastructure sector page |
| Built Environment | built environment project management; building project management; development management | Built Environment sector page |
| Urban Development | urban development programme management; master plan implementation; stakeholder coordination | Urban Development & Planning |
| Brand | 3 Pillars; 3 Pillars project management; 3 Pillars business development | Home; About Us; Contact |

## Where each page's keywords live

| Page | Admin location |
|---|---|
| Home | Site settings → Home SEO |
| About Us, Our Approach, Services, Sectors, Projects, Insights, Careers, Contact | Website — Content → Pages → (page) → SEO |
| Each service | Website — Content → Services → (service) → SEO |
| Each sector | Website — Content → Sectors → (sector) → SEO |

## On-page rules the site enforces

- One `<h1>` per page, from the page's H1 field (the title when it is empty).
- Unique SEO title and meta description: the admin's SEO tab lists any other page using the same text, and counts characters against 60 / 160.
- Image alt text must describe the image: the admin rejects alt text equal to the page's primary keyword.
- Breadcrumbs, with `BreadcrumbList` structured data, on service, sector, project and insight pages.
- An Arabic page is indexed and listed in `hreflang` and the sitemap only once its content is approved and its Arabic is marked reviewed.
