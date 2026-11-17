# Deploying 3 Pillars

One Ubuntu 24.04 VPS: nginx in front, gunicorn (Django, port 8011) and `next start`
(port 3011) behind it, both under systemd. Ports, Unix user (`pillars`) and paths
(`/srv/3pillars`, `/var/lib/3pillars`) are separate from HS Investment's, so both
can run on the same server.

```
example.com, www.example.com  → nginx → Next.js 127.0.0.1:3011
admin.example.com             → nginx → Django  127.0.0.1:8011   (/admin, /api)
                                       + /static/  from /srv/3pillars/backend/staticfiles
                                       + /assets/  from /var/lib/3pillars/assets
/var/lib/3pillars/private     CVs and RFP attachments — no nginx location, never public
```

## First install

1. **DNS** — A records for `example.com`, `www.example.com`, `admin.example.com`.
2. **Clone** — `sudo git clone <repo> /srv/3pillars`
3. **Run** — `sudo DOMAIN=example.com EMAIL=ops@example.com bash /srv/3pillars/deploy/setup-server.sh`
   It installs packages, creates the `pillars` user, generates both env files (secret
   key, shared webhook secret, preview token), migrates, seeds the placeholder
   structure, configures nginx + HTTPS + firewall, and builds the site.
4. **Admin user** — `sudo -u pillars /srv/3pillars/backend/.venv/bin/python /srv/3pillars/backend/manage.py createsuperuser`
5. **Mail** — fill `EMAIL_*` in `/srv/3pillars/backend/.env`, then `systemctl restart 3pillars-backend`.

## Every release

```bash
sudo bash /srv/3pillars/deploy/deploy.sh
```

Pulls `main`, installs, migrates, runs `check --deploy`, scans the source for injected
code (the tripwire carried over from HS Investment), builds and restarts.
**Content changes never need a deploy** — the admin's webhook refreshes pages in seconds.

## Going live checklist

- Site settings → **Show content awaiting approval: OFF** (otherwise pending content is
  public and robots.txt blocks indexing).
- Site settings → **Show the coming-soon page: OFF**.
- Every staff user has a TOTP device → set `ADMIN_REQUIRE_2FA=True`, restart backend.
- Optional: Turnstile — add `TURNSTILE_SECRET_KEY` to backend `.env`, then switch it on
  and paste the site key in Site settings → Forms.

## Operations

| Task | Command |
|---|---|
| Logs | `journalctl -u 3pillars-backend -f` / `journalctl -u 3pillars-frontend -f` |
| Restart | `systemctl restart 3pillars-backend 3pillars-frontend` |
| Backup | `sqlite3 /var/lib/3pillars/db.sqlite3 ".backup '/root/3p-$(date +%F).sqlite3'"` and copy `/var/lib/3pillars/{assets,private}` |
| Revoke previews | change `PREVIEW_TOKEN` in `/srv/3pillars/.env.production`, restart frontend |
| Postgres later | install psycopg, set `DATABASE_URL=postgres://…`, `manage.py migrate`, load a `dumpdata` export |
