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

1. Paste **public** HTML blocks to the public Marines site.
2. Paste **intranet** HTML blocks to the intranet Marines section (separate folder/site in Cascade).
3. After `sync-from-sheets.py`, update intranet pages only unless leadership bios changed.

## Copy rules for public midshipmen pages

- Do **not** link to company mentor cards, roster emails, or collateral duties.
- Direct mids to their **company Marine mentor in Bancroft Hall** or to **Detachment Leadership** for detachment-level questions.
