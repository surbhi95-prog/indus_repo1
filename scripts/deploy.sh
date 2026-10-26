#!/usr/bin/env bash
# Repo path: scripts/deploy.sh   (run: chmod +x scripts/deploy.sh)
# Runs on the VPS as root, called by the GitHub Actions workflow.
set -euo pipefail

# ================== EDIT THESE ==================
APP_DIR="/var/www/myproject"
VENV_DIR="$APP_DIR/venv"
GUNICORN_SERVICE="gunicorn"            # systemd service name
HEALTH_URL="http://127.0.0.1:8000/"    # gunicorn port, or your site URL via nginx
# ================================================

cd "$APP_DIR"

LAST_GOOD_FILE="$APP_DIR/.last_good_commit"
NEW_COMMIT="$(git rev-parse HEAD)"
PREV_COMMIT="$(cat "$LAST_GOOD_FILE" 2>/dev/null || echo "")"

echo "==> Deploying commit: $NEW_COMMIT"
echo "==> Last good commit: ${PREV_COMMIT:-none}"

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Running migrations"
python manage.py migrate --noinput

echo "==> Collecting static files"
python manage.py collectstatic --noinput

echo "==> Restarting gunicorn"
systemctl restart "$GUNICORN_SERVICE"

echo "==> Validating and reloading nginx"
nginx -t
systemctl reload nginx

echo "==> Health check: $HEALTH_URL"
ok=0
for i in $(seq 1 10); do
  code="$(curl -s -o /dev/null -w '%{http_code}' "$HEALTH_URL" || true)"
  if [[ "$code" =~ ^(200|301|302)$ ]]; then
    ok=1
    break
  fi
  echo "    attempt $i: HTTP $code, retrying in 2s..."
  sleep 2
done

if [[ "$ok" -eq 1 ]]; then
  echo "$NEW_COMMIT" > "$LAST_GOOD_FILE"
  echo "==> Deployment successful"
  exit 0
fi

echo "!! Health check failed"
systemctl status "$GUNICORN_SERVICE" --no-pager -n 20 || true

if [[ -n "$PREV_COMMIT" ]]; then
  echo "!! Rolling back to $PREV_COMMIT"
  git reset --hard "$PREV_COMMIT"
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
  systemctl restart "$GUNICORN_SERVICE"
  echo "!! Rolled back code. Database migrations were NOT reverted."
fi

exit 1
