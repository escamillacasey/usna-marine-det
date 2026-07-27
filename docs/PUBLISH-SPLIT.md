# Public vs intranet publishing

The repo holds **both** audiences. Only a subset may go on the open internet.

## Public (www / GitHub Pages)

**Detachment people info:** Senior Marine and Chief of Staff on `pages/leadership.html` only.

| Include | Path |
|---------|------|
| Homepage router | `index.html` |
| Midshipmen resources (no roster) | `pages/midshipmen/`, `prospective-marines.html`, `summer-training.html`, `roles/` |
| Fleet assignment info | `pages/fleet-application.html` |
| Detachment leadership | `pages/leadership.html` |

**Exclude from public deploy:** `pages/intranet/`, `js/intranet/`, `js/company-mentors.js`, `js/marines-on-the-yard.js`, `assets/images/intranet/`, `data/`, `docs/internal/`.

GitHub Actions builds the public artifact via `scripts/build-public-site.sh` (see `.github/workflows/pages.yml`).

## Intranet (USNA internal)

| Include | Path |
|---------|------|
| MARDET Team hub, key contacts (OpsO, Adj, etc.) | `pages/intranet/index.html` |
| Company mentors + collateral duties | `pages/intranet/company-mentors.html` |
| Marines on the Yard directory | `pages/intranet/marines-on-the-yard.html` |
| Roster JS + mentor headshots | `js/intranet/`, `assets/images/intranet/mentors/`, `assets/images/intranet/staff/` |

Midshipmen on the Yard reach mentor pages through the **intranet**, not the public site.

## Cascade workflow

| Host | Cascade root | Content |
|------|--------------|---------|
| `www.usna.edu/MarineCorps/` | Public site (active) | Open internet pages |
| `intranet.usna.edu/USMC/` | Intranet site | MARDET hub, mentor roster, Marines on the Yard |

Public cutover to `www.usna.edu/Marines/`: **`cascade/MIGRATE-TO-MARINES.md`**.

1. Paste **public** HTML to **www** Cascade pages.
2. Paste **intranet** HTML to **`intranet.usna.edu/USMC/`** (same folder tree: `Midshipmen/`, `MARDET/`, etc.).
3. After `sync-from-sheets.py`, update intranet roster pages; public pages only if copy changed.
4. Run `python3 scripts/apply-site-urls.py` when the canonical base URL changes (`cascade/site-urls.json`).

## Copy rules for public midshipmen pages

- Link to **`https://intranet.usna.edu/USMC/Midshipmen/company_mentors.php`** for current mentor assignments (or generic “ask your company Marine mentor in Bancroft”).
- Do **not** put roster emails or mentor cards on ungated **www** pages.
- Direct external audiences to **Detachment Leadership** for detachment-level questions.
