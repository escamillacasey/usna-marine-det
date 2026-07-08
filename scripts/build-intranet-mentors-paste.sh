#!/usr/bin/env bash
# Regenerate static mentor cards + full Cascade paste file.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/generate-mentor-cards-html.py"

HEADER='<!-- CASCADE paste → https://www.usna.edu/MarineCorps/MARDET/company_mentors.php -->
<!-- USNA intranet only. Static HTML — no JavaScript. Regenerate: bash scripts/build-intranet-mentors-paste.sh -->
<link href="../_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>

<header class="marines-page-header">
<div class="container">
<h1 class="marines-page-header__title">Marine Company Mentors</h1>
<p class="marines-page-header__subtitle">One Marine officer dedicated to each of the Brigade'\''s 36 companies.</p>
</div>
</header>

<section class="content-section">
<div class="container">
<p>Company Marine mentors are the detachment'\''s primary link to midshipmen in Bancroft Hall. Each mentor informs and influences mids in their company on Marine Corps culture, customs, courtesies, career opportunities, summer training, and the path to selection &#8212; developing moral, mental, and physical leadership regardless of service assignment intent.</p>
<p>Not sure how mentors fit among other Marines on the Yard? See <a href="marines_on_the_yard.php">Marines on the Yard</a> for the full picture.</p>

<nav aria-label="Jump to battalion" class="page-subnav">
<a href="#battalion-1">1st Battalion</a>
<a href="#battalion-2">2nd Battalion</a>
<a href="#battalion-3">3rd Battalion</a>
<a href="#battalion-4">4th Battalion</a>
<a href="#battalion-5">5th Battalion</a>
<a href="#battalion-6">6th Battalion</a>
</nav>

'

FOOTER='
</div>
</section>
'

{
  printf '%s' "$HEADER"
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
