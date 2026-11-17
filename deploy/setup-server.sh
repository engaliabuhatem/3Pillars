#!/usr/bin/env bash
# 3 Pillars — ONE-TIME setup of an Ubuntu 24.04 VPS (fresh, or already
# running HS Investment: ports, user and paths are separate).
#
# Run as root, from a checkout of this repo at /srv/3pillars:
#
#   DOMAIN=example.com EMAIL=you@example.com bash deploy/setup-server.sh
#
# Safe to re-run: every step checks before it changes anything.
# Prerequisites (deploy/README.md): DNS A records for DOMAIN, www.DOMAIN and
# admin.DOMAIN point at this server.
set -euo pipefail

: "${DOMAIN:?Set DOMAIN, e.g. DOMAIN=example.com}"
: "${EMAIL:?Set EMAIL for Let's Encrypt expiry notices}"

APP=/srv/3pillars
DATA=/var/lib/3pillars
USER_NAME=pillars
HERE="$(cd "$(dirname "$0")" && pwd)"

step() { printf '\n\033[1;33m==> %s\033[0m\n' "$*"; }
[ "$(id -u)" -eq 0 ] || { echo "Run as root (sudo -i)."; exit 1; }
[ -d "$APP/.git" ] || { echo "Clone the repo to $APP first (deploy/README.md)."; exit 1; }

# ── 1. Packages ──────────────────────────────────────────────────────────
step "System packages"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get -y upgrade
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  nginx certbot python3-certbot-nginx python3-venv python3-pip git ufw curl sqlite3

if ! command -v node >/dev/null || [ "$(node -v | cut -d. -f1 | tr -d v)" -lt 22 ]; then
  step "Node.js 22"
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
fi

# ── 2. Swap (next build is memory-hungry) ────────────────────────────────
if ! swapon --show | grep -q .; then
  step "2G swap"
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# ── 3. User + directories ────────────────────────────────────────────────
step "App user and directories"
id "$USER_NAME" >/dev/null 2>&1 || useradd --system --create-home --shell /bin/bash "$USER_NAME"
mkdir -p "$DATA/assets" "$DATA/private" "$DATA/cache"
chown -R "$USER_NAME:$USER_NAME" "$APP" "$DATA"
chmod 700 "$DATA/private"

# ── 4. Env files (generated once, never overwritten) ─────────────────────
step "Environment files"
REVALIDATE=$(python3 -c "import secrets; print(secrets.token_hex(32))")
if [ ! -f "$APP/backend/.env" ]; then
  SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
  sed -e "s/example\.com/$DOMAIN/g" -e "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET|" \
      -e "s|^REVALIDATE_SECRET=.*|REVALIDATE_SECRET=$REVALIDATE|" \
    "$HERE/backend.env.production.example" > "$APP/backend/.env"
  echo "   created backend/.env"
fi
if [ ! -f "$APP/.env.production" ]; then
  SHARED=$(grep -E '^REVALIDATE_SECRET=' "$APP/backend/.env" | cut -d= -f2-)
  PREVIEW=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")
  sed -e "s/example\.com/$DOMAIN/g" -e "s|^PREVIEW_TOKEN=.*|PREVIEW_TOKEN=$PREVIEW|" \
      -e "s|^REVALIDATE_SECRET=.*|REVALIDATE_SECRET=$SHARED|" \
    "$HERE/frontend.env.production.example" > "$APP/.env.production"
  echo "   created .env.production (new PREVIEW_TOKEN, shared REVALIDATE_SECRET)"
fi
chown "$USER_NAME:$USER_NAME" "$APP/backend/.env" "$APP/.env.production"
chmod 600 "$APP/backend/.env" "$APP/.env.production"

# ── 5. Backend ───────────────────────────────────────────────────────────
step "Backend: venv, migrate, collectstatic, checks"
sudo -u "$USER_NAME" bash -c "
  set -e
  cd $APP/backend
  [ -d .venv ] || python3 -m venv .venv
  .venv/bin/pip install --upgrade pip -q
  .venv/bin/pip install -r requirements.txt -q
  .venv/bin/python manage.py migrate --noinput
  .venv/bin/python manage.py seed
  .venv/bin/python manage.py collectstatic --noinput -v 0
  .venv/bin/python manage.py check --deploy --fail-level WARNING
"
install -m 644 "$HERE/systemd/3pillars-backend.service" /etc/systemd/system/
install -m 644 "$HERE/systemd/3pillars-frontend.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now 3pillars-backend
systemctl restart 3pillars-backend

# nginx must traverse to staticfiles and public assets — and nothing else.
chmod o+x /srv "$APP" "$APP/backend" "$DATA"
chmod -R o+rX "$APP/backend/staticfiles" "$DATA/assets"

# ── 6. nginx ─────────────────────────────────────────────────────────────
step "nginx"
install -m 644 "$HERE/nginx/3pillars-proxy.conf" /etc/nginx/snippets/3pillars-proxy.conf
if [ ! -f /etc/nginx/sites-available/3pillars ]; then
  sed "s/__DOMAIN__/$DOMAIN/g" "$HERE/nginx/3pillars.conf" > /etc/nginx/sites-available/3pillars
fi
ln -sf /etc/nginx/sites-available/3pillars /etc/nginx/sites-enabled/3pillars
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# ── 7. Firewall ──────────────────────────────────────────────────────────
step "Firewall (SSH + HTTP/HTTPS only)"
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# ── 8. HTTPS ─────────────────────────────────────────────────────────────
step "Let's Encrypt certificates"
certbot --nginx --non-interactive --agree-tos --redirect -m "$EMAIL" \
  -d "$DOMAIN" -d "www.$DOMAIN" -d "admin.$DOMAIN"

# ── 9. Frontend (needs the CMS reachable over HTTPS, so it goes last) ────
step "Frontend build"
bash "$HERE/deploy.sh" --frontend-only
systemctl enable 3pillars-frontend

step "Done"
PREVIEW=$(grep -E '^PREVIEW_TOKEN=' "$APP/.env.production" | cut -d= -f2-)
echo "  Website:          https://$DOMAIN"
echo "  CMS:              https://admin.$DOMAIN/admin/"
echo "  Private preview:  https://$DOMAIN/?preview=$PREVIEW   (keep this secret)"
echo "  First admin login:"
echo "    sudo -u $USER_NAME $APP/backend/.venv/bin/python $APP/backend/manage.py createsuperuser"
