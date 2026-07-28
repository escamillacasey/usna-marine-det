#!/usr/bin/env bash
# Regenerate static mentor cards + Cascade paste for intranet company mentors.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Live intranet paths (from view-source audit Jul 2026)
export CASCADE_PHOTO_PREFIX="${CASCADE_PHOTO_PREFIX:-/USMC/_files/images/mentors/}"
python3 "$ROOT/scripts/generate-mentor-cards-html.py"

STYLE_FILE="$ROOT/cascade/paste-local-css-mentor-cards-delta.css"
STYLE_INNER=$(sed '/^\/\*/d' "$STYLE_FILE")

read -r -d '' HEADER <<'HEADER_EOF' || true
<!-- CASCADE paste → intranet.usna.edu/USMC/company_mentors.php -->
<!-- INTRANET ONLY — full roster. Styles embedded below (USNA loads intranet-root _files/css/local.css). -->
<!-- Regenerate: bash scripts/build-intranet-mentors-paste.sh -->
<style>
HEADER_EOF

read -r -d '' HEADER2 <<'HEADER2_EOF' || true
</style>

<div class="marines-page-header">
<div class="container">
<h1 class="marines-page-header__title">Marine Company Mentors</h1>
<p class="marines-page-header__subtitle">Current Marine officer assigned to each of the Brigade's 36 companies.</p>
</div>
</div>

<section class="content-section">
<div class="container">
<p>Company Marine mentors are the detachment's primary link to midshipmen in Bancroft Hall. Below: photos, contact information, primary duty, collateral assignments, and summer duty. For the commissioning path and summer programs, see <a href="prospective-marines.php">Prospective Marines</a> and <a href="summer-training.php">Summer Training</a>.</p>

<nav aria-label="Jump to battalion" class="page-subnav">
<a href="#battalion-1">1st Battalion</a>
<a href="#battalion-2">2nd Battalion</a>
<a href="#battalion-3">3rd Battalion</a>
<a href="#battalion-4">4th Battalion</a>
<a href="#battalion-5">5th Battalion</a>
<a href="#battalion-6">6th Battalion</a>
</nav>

HEADER2_EOF

FOOTER='
<p class="info-callout">Detachment-level questions: <a href="../MARDET/leadership.php">Detachment Leadership</a> · <a href="../MARDET/index.php">MARDET Team</a></p>
</div>
</section>
'

{
  printf '%s\n' "$HEADER"
  printf '%s\n' "$STYLE_INNER"
  printf '%s' "$HEADER2"
  cat "$ROOT/cascade/includes/mentor-cards-cascade.html"
  printf '%s' "$FOOTER"
} > "$ROOT/cascade/paste-intranet-company-mentors-marinecorps.html"

python3 <<PY
from pathlib import Path

root = Path("$ROOT")
page = root / "pages/intranet/company-mentors.html"
cards = (root / "cascade/includes/mentor-cards-local.html").read_text(encoding="utf-8")
text = page.read_text(encoding="utf-8")
start_marker = "<!-- mentor-cards:start -->"
end_marker = "<!-- mentor-cards:end -->"
if start_marker not in text or end_marker not in text:
    raise SystemExit("company-mentors.html missing mentor-cards markers")
before, rest = text.split(start_marker, 1)
_, after = rest.split(end_marker, 1)
page.write_text(
    before + start_marker + "\n" + cards + end_marker + after,
    encoding="utf-8",
)
print("Updated pages/intranet/company-mentors.html")
PY

echo "Wrote cascade/paste-intranet-company-mentors-marinecorps.html"
