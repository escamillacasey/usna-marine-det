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

**Static Cascade paste (no JS):** after sync, run `python3 scripts/generate-mentor-cards-html.py` and re-paste `cascade/paste-intranet-company-mentors-marinecorps.html`.
