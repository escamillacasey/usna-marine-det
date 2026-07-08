#!/usr/bin/env bash
# Concatenate site CSS into one file for Cascade (avoids broken @import in asset library).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/cascade/marines.css"
mkdir -p "$(dirname "$OUT")"
{
  echo "/* USNA Marines — Cascade bundle. Generated — do not edit by hand. */"
  echo "/* Run: bash scripts/build-cascade-bundle.sh */"
  cat "$ROOT/css/variables.css"
  echo ""
  cat "$ROOT/css/base.css"
  echo ""
  cat "$ROOT/css/layout.css"
  echo ""
  cat "$ROOT/css/components.css"
} > "$OUT"
echo "Wrote $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"
