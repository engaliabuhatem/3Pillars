# Go-live: 3pillars-go.com (on the HS Investment server)

The site runs next to HS Investment on the same server, separately: its own Unix user (`pillars`), folders (`/srv/3pillars`, `/var/lib/3pillars`), ports (Next.js 3011, Django 8011) and nginx site file. Nothing in these steps changes HS Investment's nginx sites, services or firewall.

| Address | Serves |
|---|---|
| `https://3pillars-go.com` | the website |
| `https://www.3pillars-go.com` | redirects to `https://3pillars-go.com` |
| `https://admin.3pillars-go.com/admin/` | the CMS (and the API the website reads) |

---

## 1. DNS records (add these first)

`SERVER_IP` is the public IPv4 address of the HS Investment server: the same value as the `A` record of HS Investment's own domain. On the server, `curl -4 ifconfig.me` prints it.

| Type | Name / Host | Value | TTL |
|---|---|---|---|
| A | `@` | `SERVER_IP` | 300 |
| A | `www` | `SERVER_IP` | 300 |
| A | `admin` | `SERVER_IP` | 300 |
| CAA | `@` | `0 issue "letsencrypt.org"` | 3600 |

- **Delete** any records the registrar added for parking (a default `A` for `@` or `www`, a `www` CNAME to a parking page, any `AAAA` records). A leftover record splits visitors between two servers and makes the HTTPS certificate request fail.
- Add `AAAA` records only if the server has a public IPv6 address (`curl -6 ifconfig.me` on the server). Use the same three names.
- The CAA record is optional. It allows only Let's Encrypt to issue certificates for the domain. Skip it if the registrar doesn't offer CAA.
- After launch, raise the TTLs to 3600.

### Email records (only if 3 Pillars sends mail from this domain)

Enquiry notifications and auto-replies go out from `NOTIFY_FROM_EMAIL` (default `no-reply@3pillars-go.com`). To keep them out of spam folders, the mail provider that sends them needs these records. **Its own setup page gives the exact values:**

| Type | Name | Value |
|---|---|---|
| MX | `@` | the provider's mail servers (only if mailboxes are hosted on this domain) |
| TXT | `@` | SPF, e.g. `v=spf1 include:<provider> ~all`; one SPF record only |
| TXT / CNAME | `<selector>._domainkey` | DKIM, from the provider |
| TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:<a mailbox you read>` |

If the HS Investment SMTP account is reused instead, use a `NOTIFY_FROM_EMAIL` on HS Investment's domain. Otherwise the From domain won't match its SPF/DKIM.

Check that DNS has spread before step 3:

```bash
dig +short 3pillars-go.com www.3pillars-go.com admin.3pillars-go.com   # all three: SERVER_IP
```

---

## 2. Code on the server

All work must be pushed to `main` on GitHub first.

```bash
sudo -i
# first time only
git clone https://github.com/engaliabuhatem/3Pillars.git /srv/3pillars
# if /srv/3pillars already exists from an earlier test install, skip the clone:
#   step 3 is safe to re-run, and deploy.sh pulls the latest main
```

## 3. Install (once)

```bash
DOMAIN=3pillars-go.com EMAIL=<an inbox that reads certificate notices> bash /srv/3pillars/deploy/setup-server.sh
```

This script:
- installs packages only if they are missing (no system-wide upgrade)
- creates the `pillars` user and generates both env files with new secrets
- migrates the database and loads the content (`seed_content`)
- adds the `3pillars` nginx site and requests HTTPS certificates for all three names
- builds the website

It leaves HS Investment's nginx sites and the firewall state as they are. If `ufw` is active, it only adds the SSH and HTTP/HTTPS rules.

Check with `nginx -t` (it must say `ok`) and confirm HS Investment's site still loads.

## 4. Bring over the approved content

A fresh install starts with everything awaiting approval. The pages, services, sectors and sections already approved in the development CMS (`backend/db.sqlite3`, with its uploads in `backend/assets/`) can be moved across in one go.

From the development PC (PowerShell):

```powershell
scp D:\3Pillars\backend\db.sqlite3 root@SERVER_IP:/tmp/3p-db.sqlite3
scp -r D:\3Pillars\backend\assets root@SERVER_IP:/tmp/3p-assets
```

On the server:

```bash
systemctl stop 3pillars-backend
cp /var/lib/3pillars/db.sqlite3 /root/3p-db-fresh-$(date +%F).sqlite3   # keep the fresh one, just in case
mv /tmp/3p-db.sqlite3 /var/lib/3pillars/db.sqlite3
cp -r /tmp/3p-assets/. /var/lib/3pillars/assets/
chown -R pillars:pillars /var/lib/3pillars
chmod -R o+rX /var/lib/3pillars/assets
sudo -u pillars /srv/3pillars/backend/.venv/bin/python /srv/3pillars/backend/manage.py migrate --noinput
systemctl start 3pillars-backend
bash /srv/3pillars/deploy/deploy.sh --frontend-only   # rebuild the pages from the copied content
```

The copied database brings its staff accounts. Log in as `admin` with the development password, then change it straight away (top-right menu → Change password). Add each team member under Configuration → Staff users.

If you'd rather start from the fresh install, skip this step and approve the content in the live admin instead (§5, first line).

## 5. In the live admin (`https://admin.3pillars-go.com/admin/`)

In this order:

1. **Site settings → Switches → Site-wide wording: Approved.** This is the hero, the positioning statement and the home SEO. Approvers only. It's the one item still pending in the development CMS.
2. **Site settings → Forms:** the general notification list, a list per area of interest if wanted, and the **Consent wording** (approved legal text).
3. **Site settings → Contact:** the verified address, phone, email and hours. Tick **Contact details verified** only when they are correct.
4. **Site settings → Hero video:** upload a **Default page hero background** (at least 1600 × 900) so interior pages open on a photograph instead of navy.
5. **Site settings → SEO & analytics:** add analytics if wanted. Leave *Use the www address* **off**; the site's address is `3pillars-go.com`.
6. **Configuration → Launch readiness:** confirm the items that are done. Turning off coming-soon warns about any still open.
7. **Site settings → Switches:** *Show content awaiting approval* **OFF**, then *Show the coming-soon page* **OFF**. The site is live within ~10 seconds, and robots.txt then allows indexing.

## 6. Mail and two-factor sign-in

```bash
nano /srv/3pillars/backend/.env    # EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, NOTIFY_FROM_EMAIL
systemctl restart 3pillars-backend
```

Send a test enquiry from `https://3pillars-go.com/en/contact/` and check that it arrives.

Once every staff account has a TOTP device (Configuration → Staff users → TOTP devices), set `ADMIN_REQUIRE_2FA=True` in the same file and restart the backend.

## 7. Launch checks

```bash
curl -sI http://3pillars-go.com          | head -1   # 301 → https
curl -sI https://www.3pillars-go.com/en/ | head -3   # 308 → https://3pillars-go.com/en/
curl -s  https://3pillars-go.com/robots.txt          # Allow: /   (only after step 5.7)
curl -s  https://3pillars-go.com/sitemap.xml | head  # https://3pillars-go.com/en/... URLs
curl -s  -o /dev/null -w "%{http_code}\n" https://3pillars-go.com/api/revalidate/   # 403 (local only)
```

Then:
- In a browser: home, a service, a sector, Contact (submit a test), Arabic home.
- Google Search Console: add the `3pillars-go.com` domain property (it asks for one more TXT record) and submit `https://3pillars-go.com/sitemap.xml`.
- Arabic pages stay out of search until *Arabic reviewed* is ticked on each one, by design.

## Every later release

```bash
sudo bash /srv/3pillars/deploy/deploy.sh
```

Content edits in the admin never need a deploy.
