#!/usr/bin/env bash
# Output marines.css wrapped for pasting at the END of Cascade local.css.
# @import only works at the top of a stylesheet — do not use @import mid-file.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/cascade/paste-local-css-append.css"
bash "$ROOT/scripts/build-cascade-bundle.sh" >/dev/null
{
  echo "/* --- USNA Marines site styles (paste below existing local.css rules) --- */"
  cat "$ROOT/cascade/marines.css"
} > "$OUT"
cat "$OUT"
