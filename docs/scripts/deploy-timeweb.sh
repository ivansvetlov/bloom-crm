#!/usr/bin/env bash
# WebConsole Timeweb → public_html сайта crmbloom.ru
set -euo pipefail

WEB="${1:-}"
if [[ -z "$WEB" ]]; then
  WEB=$(find "$HOME" -maxdepth 4 -type d \( -path '*crmbloom*' -o -path '*crm_bloom*' \) -name public_html 2>/dev/null | head -1 || true)
fi
if [[ -z "$WEB" || ! -d "$WEB" ]]; then
  echo "Не нашли public_html для crmbloom.ru. Передайте путь:"
  echo "  bash deploy-timeweb.sh /home/c/USER/crmbloom.ru/public_html"
  find "$HOME" -maxdepth 4 -type d -name public_html 2>/dev/null || true
  exit 1
fi

echo "TARGET: $WEB"
cd /tmp
rm -rf bloom-crm-master flowwow-crm-master crm.zip
# предпочитаем bloom-crm; fallback на старое имя репо
if ! curl -fsSL -o crm.zip https://github.com/ivansvetlov/bloom-crm/archive/refs/heads/master.zip; then
  curl -fsSL -o crm.zip https://github.com/ivansvetlov/flowwow-crm/archive/refs/heads/master.zip
fi
unzip -qo crm.zip
SRC=$(ls -d /tmp/bloom-crm-master/docs /tmp/flowwow-crm-master/docs 2>/dev/null | head -1)
[[ -n "$SRC" ]] || { echo "docs not found in zip"; exit 1; }

mkdir -p "$WEB/kp"
cp -f "$SRC/index.html" "$WEB/"
for f in demo.html questions.html landing.html security.html test-dynamic.html; do
  [[ -f "$SRC/$f" ]] && cp -f "$SRC/$f" "$WEB/"
done
cp -rf "$SRC/kp/." "$WEB/kp/"
chmod -R a+rX "$WEB/kp" "$WEB/index.html" 2>/dev/null || true
find "$WEB" -maxdepth 2 -name '*.html' -exec chmod a+r {} \; 2>/dev/null || true

echo "=== hub ==="
ls -la "$WEB/index.html"
echo "=== kp ==="
ls -la "$WEB/kp"
echo "OK: https://crmbloom.ru/"
echo "OK: https://crmbloom.ru/kp/demo/"
