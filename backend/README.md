# 3 Pillars CMS (Django)

See the root [README.md](../README.md) for setup, architecture and checks, and
[EDITING.md](../EDITING.md) for editors. `adminkit/` is copied verbatim from HS
Investment — brand it only through `build_unfold()` and `static/css/admin-brand.css`.
The Unfold chrome (system type, surfaces, sidebar, segmented tabs, badges) follows
Apple's HIG via `static/css/admin-apple.css` and the Apple grey/label colours in
`config/settings.py`.

Apps: `core` (bases, settings, navigation, pages, redirects, webhook, security),
`content` (public content), `bd` (leads + pipeline), `careers` (jobs + applications).
