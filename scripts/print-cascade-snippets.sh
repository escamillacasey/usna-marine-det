#!/usr/bin/env bash
# Print Cascade snippets with ASSET_BASE substituted.
# Usage: bash scripts/print-cascade-snippets.sh /USMC/_files/marines
set -euo pipefail
BASE="${1:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SNIP="$ROOT/cascade/snippets"

echo "=== USNA USMC Format (recommended) ==="
cat "$SNIP/head-css-usna-usmc.html"
echo ""
cat "$SNIP/foot-standard-usna-usmc.html"
echo ""

if [[ -z "$BASE" ]]; then
  BASE="/USMC/_files/marines"
else
  BASE="${BASE%/}"
fi

echo "=== Alternate absolute paths (ASSET_BASE=$BASE) ==="
echo "=== CSS (all pages) ==="
sed "s|ASSET_BASE|$BASE|g" "$SNIP/head-css.html"
echo ""
echo "=== JS: standard pages ==="
sed "s|ASSET_BASE|$BASE|g" "$SNIP/foot-standard.html"
echo ""
echo "=== JS: company mentors ==="
sed "s|ASSET_BASE|$BASE|g" "$SNIP/foot-company-mentors.html"
echo ""
echo "=== JS: marines on the yard ==="
sed "s|ASSET_BASE|$BASE|g" "$SNIP/foot-marines-on-the-yard.html"
