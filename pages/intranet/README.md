# Intranet-only pages

Publish these to **USNA intranet** (Cascade on `intranet.usna.edu` or equivalent). **Do not** deploy to the public `www.usna.edu` site or GitHub Pages.

| Page | File |
|------|------|
| MARDET Team hub | `index.html` |
| Company mentors (photos, emails, collateral duties) | `company-mentors.html` |
| Marines on the Yard (full roster) | `marines-on-the-yard.html` |

Data: `js/intranet/company-mentors-data.js`, `js/intranet/marines-on-the-yard-data.js`  
Photos: `assets/images/intranet/mentors/` and `assets/images/intranet/staff/`

Run `python3 scripts/sync-from-sheets.py` after roster exports to refresh intranet data.

**Static Cascade paste (no JS):** after sync, run `bash scripts/build-intranet-mentors-paste.sh` and re-paste `cascade/paste-intranet-company-mentors-marinecorps.html` into `Midshipmen/company_mentor_assignments.php` (gated). Public overview: `paste-public-company-mentors-marinecorps.html` → `Midshipmen/company_mentors.php`.

**Adding mentor photos:** drop files in `assets/images/incoming/`, then `python3 scripts/import-photos.py` (copies to intranet + public mentor folders). Rebuild paste and re-publish. Currently missing: **1st Company** (`company-01.jpg`) and **20th Company** (`company-20.jpg`).
