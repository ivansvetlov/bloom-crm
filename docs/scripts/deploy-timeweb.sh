#!/usr/bin/env bash
# Запускать в WebConsole Timeweb на vh* (под вашим cs*).
# Кладёт хаб + все КП в public_html сайта flowww.webtm.ru
set -euo pipefail

WEB="${1:-}"
if [[ -z "$WEB" ]]; then
  WEB=$(find "$HOME" -maxdepth 4 -type d -path '*flowww*' -name public_html 2>/dev/null | head -1 || true)
fi
if [[ -z "$WEB" || ! -d "$WEB" ]]; then
  echo "Не нашли public_html для flowww. Передайте путь:"
  echo "  bash deploy-timeweb.sh /home/c/USER/flowww.webtm.ru/public_html"
  echo "Доступные public_html:"
  find "$HOME" -maxdepth 4 -type d -name public_html 2>/dev/null || true
  exit 1
fi

echo "TARGET: $WEB"
cd /tmp
rm -rf flowwow-crm-master crm.zip
curl -fsSL -o crm.zip https://github.com/ivansvetlov/flowwow-crm/archive/refs/heads/master.zip
unzip -qo crm.zip
SRC=flowwow-crm-master/docs

mkdir -p "$WEB/kp"
cp -f "$SRC/index.html" "$WEB/"
# redirects (optional, handy)
for f in demo.html questions.html landing.html security.html test-dynamic.html; do
  [[ -f "$SRC/$f" ]] && cp -f "$SRC/$f" "$WEB/"
done
cp -rf "$SRC/kp/." "$WEB/kp/"
# readable by web server
chmod -R a+rX "$WEB/index.html" "$WEB/kp" 2>/dev/null || true
find "$WEB" -maxdepth 2 -name '*.html' -exec chmod a+r {} \; 2>/dev/null || true

echo "=== hub ==="
ls -la "$WEB/index.html"
echo "=== kp ==="
ls -la "$WEB/kp"
echo "OK: https://flowww.webtm.ru/"
echo "OK: https://flowww.webtm.ru/kp/flowwow/"
