# Site structure — public www + intranet (`USMC`)

USNA Cascade builds the **left nav from the folder tree**, not from paste HTML. Renaming, moving, or deleting pages breaks nav until the whole site is reconfigured and republished.

| Host | Cascade root | Notes |
|------|--------------|-------|
| **Public (active)** | `https://www.usna.edu/MarineCorps/` | Open internet |
| **Public (cutover)** | `https://www.usna.edu/Marines/` | See `MIGRATE-TO-MARINES.md` |
| **Intranet** | `https://intranet.usna.edu/USMC/` | MARDET hub, mentor roster, MOTY — same folder tree as www |

**Folder names** (`Midshipmen/`, `MARDET/`, `company_mentors.php`) are identical on both hosts; only the site root slug differs (`MarineCorps` / `Marines` vs `USMC`).

---

## Canonical folder tree

```
Marines/                              ← Cascade site root
├── index.php                         ← Home
├── Fleet_Marines.php
├── _files/
│   ├── css/local.css
│   └── js/…
├── assets/images/…
├── MARDET/
│   ├── index.php                     ← MARDET Team hub (gated)
│   ├── leadership.php                ← public bios
│   └── marines_on_the_yard.php       ← cards public; directory gated
└── Midshipmen/                       ← capital M
    ├── index.php
    ├── prospective-marines.php
    ├── summer-training.php
    └── roles/
        ├── index.php
        ├── aviation.php
        └── support.php

USMC/ (intranet site root only)
└── company_mentors.php               ← full roster (intranet only)
```

**Never rename for intranet gate or Marines migration:**

| Wrong | Why |
|-------|-----|
| `company-mentors.php` (hyphen) | 404; nav and paste links use underscore |
| `midshipmen/` (lowercase) | Live URLs use `Midshipmen/` |
| Moving mentors under `MARDET/` | Breaks paste links and nav |
| Deleting intranet `company_mentors.php` | Nav 404 on mentor roster |
| Second root `MarineCorps/` after cutover | Split nav, duplicate content |

---

## What lives where (gated vs public on `Marines/`)

| Path | Public (anonymous) | Authenticated (USNA login) |
|------|-------------------|----------------------------|
| `company_mentors.php` (intranet root) | — | Full mentor roster paste |
| `MARDET/marines_on_the_yard.php` | Community overview | `#yard-directory` roster |
| `MARDET/index.php` | Optional public teaser | MARDET hub + internal links |
| `MARDET/leadership.php` | Reid + Giraldi bios | Same |
| Mentor photos | — | `assets/images/intranet/mentors/` |
| Summer / roles photos | `assets/images/public/…` | Same |

Same URL paths — Cascade auth controls HTML exposure, not folder names.

---

## Nav-safe checklist (`Marines/`)

### New site build (copy from `MarineCorps/`, do not drag-and-drop rename)

1. Create **`Marines/`** site root in Cascade (Web Services may clone the tree).
2. Copy **folder names and filenames** exactly as above.
3. Paste updated HTML (run `python3 scripts/apply-site-urls.py` first).
4. **Configure** each page: **Include in Navigation** matches legacy site order.
5. Apply **SSO / page auth** on gated paths (Web Services).
6. Publish **`Marines/`** root and all contents.
7. Enable **redirects** `MarineCorps/*` → `Marines/*`.
8. Verify left nav on `…/Marines/index.php` — all sections 200.

### Company mentors (intranet only)

1. Publish **`company_mentors.php`** on **intranet.usna.edu/USMC/** — paste `paste-intranet-company-mentors-marinecorps.html`.
2. **Include in Navigation → Yes** on the intranet site.
3. Do **not** publish a public www company mentors page — public pages link to the intranet URL.

---

## CSS depth (unchanged)

| Page folder | `local.css` link in paste |
|-------------|---------------------------|
| Site root | `_files/css/local.css` |
| `MARDET/`, `Midshipmen/` | `../_files/css/local.css` |
| `Midshipmen/roles/` | `../../_files/css/local.css` |

---

## Escalate to Web Services if

- Site slug is not `Marines` or redirects are not ready at cutover
- Page-level auth is unavailable — need Option B stub plan
- Left nav disappears — `FIX-NAV.md`
- Duplicate `Marines/` and `MarineCorps/` both indexed in nav

See: `MIGRATE-TO-MARINES.md`, `LIVE-URLS.md`, `site-urls.json`, `DEPLOY-MENTORS-INTRANET-SPLIT.md`.
