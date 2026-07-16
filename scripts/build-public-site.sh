#!/usr/bin/env bash
# Build a public-only site artifact for GitHub Pages (excludes intranet content).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/_site"
rm -rf "$OUT"
mkdir -p "$OUT"
rsync -a \
  --exclude '_site' \
  --exclude '.git' \
  --exclude '.tmp' \
  --exclude 'pages/intranet' \
  --exclude 'js/intranet' \
  --exclude 'js/company-mentors.js' \
  --exclude 'js/marines-on-the-yard.js' \
  --exclude 'assets/images/intranet' \
  --exclude 'assets/images/incoming' \
  --exclude 'assets/images/scraped' \
  --exclude 'docs/internal' \
  --exclude 'templates' \
  --exclude 'data' \
  --exclude 'scripts' \
  "$ROOT/" "$OUT/"
echo "Public site built at _site/ ($(find "$OUT" -type f | wc -l | tr -d ' ') files)"
