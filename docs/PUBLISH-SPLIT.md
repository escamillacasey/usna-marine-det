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

## Cascade workflow (`usna.edu/Marines`)

**One Cascade site** at `https://www.usna.edu/Marines/` serves both audiences. Gated pages use **page/folder SSO** — not a separate host. Migration: **`cascade/MIGRATE-TO-MARINES.md`**.

1. Paste **public** HTML blocks to open pages on `Marines/`.
2. Paste **intranet** HTML blocks to the **same path tree** on pages Web Services marks authenticated.
3. After `sync-from-sheets.py`, update gated pages only unless leadership bios changed.
4. Run `python3 scripts/apply-site-urls.py` when the canonical base URL changes.

## Copy rules for public midshipmen pages

- Link to **`company_mentors.php`** for what a mentor is; link to **`company_mentor_assignments.php`** only where login is expected (or use generic “ask your mentor in Bancroft”).
- Do **not** put roster emails or mentor cards on ungated pages.
- Direct external audiences to **Detachment Leadership** for detachment-level questions.
