#!/usr/bin/env bash
# Sunucuda siteyi güncelle. Kullanım: ./deploy/update.sh
set -euo pipefail

BRANCH="${1:-claude/mobile-app-promo-site-yecg4a}"
cd "$(dirname "$0")/.."

echo "→ $BRANCH dalından çekiliyor…"
git fetch origin "$BRANCH"
git checkout "$BRANCH"
git reset --hard "origin/$BRANCH"

echo "→ Doldurulmamış alanlar kontrol ediliyor…"
python3 tools/check_placeholders.py || echo "  (uyarı: doldurulmamış alan var)"

echo "→ Nginx yapılandırması test ediliyor…"
sudo nginx -t && sudo systemctl reload nginx

echo "✓ Güncelleme tamam."
