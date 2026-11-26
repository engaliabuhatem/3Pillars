#!/usr/bin/env bash
# 3 Pillars — ship the latest `main` to the server.
#
#   sudo bash /srv/3pillars/deploy/deploy.sh
#
# Content edits in the CMS need NO deploy: the webhook refreshes the site in
# seconds. The coming-soon switch needs none either. After editing
# .env.production, `systemctl restart 3pillars-frontend` is enough.
set -euo pipefail

APP=/srv/3pillars
USER_NAME=pillars
BRANCH=${BRANCH:-main}
FRONTEND_PORT=3011
step() { printf '\n\033[1;33m==> %s\033[0m\n' "$*"; }
as_app() { sudo -u "$USER_NAME" bash -c "set -e; $*"; }

[ "$(id -u)" -eq 0 ] || { echo "Run with sudo."; exit 1; }

if [ "${1:-}" != "--frontend-only" ]; then
  step "Pulling $BRANCH"
  as_app "cd $APP && git fetch --quiet origin && git checkout --quiet $BRANCH && git reset --hard --quiet origin/$BRANCH"
  as_app "cd $APP && git log --oneline -1"

  step "Backend"
  as_app "cd $APP/backend && .venv/bin/pip install -r requirements.txt -q \
    && .venv/bin/python manage.py migrate --noinput \
    && .venv/bin/python manage.py collectstatic --noinput -v 0 \
    && .venv/bin/python manage.py check --deploy --fail-level WARNING"
  chmod -R o+rX "$APP/backend/staticfiles"
  install -m 644 "$APP/deploy/systemd/3pillars-backend.service" /etc/systemd/system/
  install -m 644 "$APP/deploy/systemd/3pillars-frontend.service" /etc/systemd/system/
  systemctl daemon-reload
  systemctl restart 3pillars-backend
fi

# Tripwire, carried over from HS Investment after injected code was found in
# config files there: refuse to build if any source line is absurdly long or
# matches a known obfuscation signature. Config files run during `next build`.
step "Scanning source for injected code"
SUSPECT=$(cd "$APP" && git ls-files -- '*.js' '*.mjs' '*.cjs' '*.ts' '*.tsx' '*.py' '*.sh' \
  | xargs -d '\n' awk 'length($0) > 1000 || /_\$jsoPow|global\.o=|_\$_[0-9a-f]{4}=\(function/ { print FILENAME ":" FNR; nextfile }')
if [ -n "$SUSPECT" ]; then
  echo "!! Refusing to build — suspicious code in:"; echo "$SUSPECT"
  exit 1
fi

# The build reads the CMS (with a static fallback if it can't); wait so the
# first build after a backend restart gets real content.
step "Waiting for the CMS API"
API=$(grep -E '^CMS_API_URL=' "$APP/.env.production" | cut -d= -f2-)
for i in $(seq 1 30); do
  curl -fsS -o /dev/null "$API/health/" && break
  [ "$i" = 30 ] && { echo "CMS API at $API/health/ is not answering — journalctl -u 3pillars-backend -n 50"; exit 1; }
  sleep 2
done

step "Frontend build"
# A build reuses the on-disk fetch cache; if a webhook was missed while the
# site was down, that cache could be stale. Build from fresh CMS data.
as_app "rm -rf $APP/.next/cache/fetch-cache"
as_app "cd $APP && npm ci --include=dev --no-audit --no-fund \
  && set -a && . ./.env.production && set +a && NODE_ENV=production npm run build"
systemctl restart 3pillars-frontend

step "Smoke test"
sleep 3
curl -fsS -o /dev/null -w "website  %{http_code}\n" "http://127.0.0.1:$FRONTEND_PORT/en/"
curl -fsS -o /dev/null -w "api      %{http_code}\n" "$API/health/"
echo "Deployed."
