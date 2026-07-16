# Site structure — `usna.edu/Marines` (public + intranet, one site)

USNA Cascade builds the **left nav from the folder tree**, not from paste HTML. Renaming, moving, or deleting pages breaks nav until the whole site is reconfigured and republished.

**Production root:** `https://www.usna.edu/Marines/` (replaces legacy `…/MarineCorps/`).  
**One site, two audiences:** open web pages + SSO-gated pages on the **same path tree** — see `MIGRATE-TO-MARINES.md`.

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
    ├── company_mentors.php           ← public: what a mentor is
    ├── company_mentor_assignments.php ← gated: full roster
    └── roles/
        ├── index.php
        ├── aviation.php
        └── support.php
```

**Never rename for intranet gate or Marines migration:**

| Wrong | Why |
|-------|-----|
| `company-mentors.php` (hyphen) | 404; nav and paste links use underscore |
| `midshipmen/` (lowercase) | Live URLs use `Midshipmen/` |
| Moving mentors under `MARDET/` | Breaks paste links and nav |
| Deleting `company_mentors.php` | Nav 404 — **gate** the page instead |
| Second root `MarineCorps/` after cutover | Split nav, duplicate content |

---

## What lives where (gated vs public on `Marines/`)

| Path | Public (anonymous) | Authenticated (USNA login) |
|------|-------------------|----------------------------|
| `Midshipmen/company_mentors.php` | Program overview (what, role, how to find) | Same |
| `Midshipmen/company_mentor_assignments.php` | Login wall | Full roster paste |
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

### Company mentors (no nav breakage)

1. Keep **`Midshipmen/company_mentors.php`** in nav — public overview paste.
2. Add **`Midshipmen/company_mentor_assignments.php`** — gated roster; optional in nav.

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
