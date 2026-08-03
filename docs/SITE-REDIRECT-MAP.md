# Site redirect map — USNA Marine Detachment

**Purpose:** Request **301 permanent redirects** from Web Services to consolidate legacy public URLs onto **`www.usna.edu/MarineCorps/`**.

**Prepared:** Jul 2026 · Source: live crawl + Cascade sitemaps (`/MarineCorps/sitemap.xml`, `/USMC/sitemap.xml`)

**Canonical public site:** `https://www.usna.edu/MarineCorps/`  
**Legacy public sites (retire):** `https://www.usna.edu/USMC/`, `https://www.usna.edu/Marines/`, `https://www.usna.edu/Marine/`  
**Intranet (separate — do not redirect to www):** `https://intranet.usna.edu/USMC/`

**Machine-readable:** [`docs/site-redirect-map.csv`](site-redirect-map.csv)

---

## Request summary for Web Services

1. Implement **301** redirects (preserve query strings if possible).
2. Apply the **same path rules** to both **`/USMC/`** and **`/Marines/`** (duplicate legacy sites).
3. Redirect **`/Marine/`** → **`/MarineCorps/`** (currently aliases to `/Marines/`).
4. Do **not** redirect **intranet** hosts to www.
5. Leave **`/MarineCorps/`** unchanged as the production tree.

---

## www.usna.edu — alias & site root

| From path | To path | Notes |
|-----------|---------|--------|
| `/Marine/` | `/MarineCorps/` | Short alias (currently → `/Marines/`) |
| `/Marine/index.php` | `/MarineCorps/` | |
| `/Marines/` | `/MarineCorps/` | Legacy site root |
| `/Marines/index.php` | `/MarineCorps/` | |
| `/Marines/Index.php` | `/MarineCorps/` | |
| `/Marines/Home.php` | `/MarineCorps/` | Legacy alternate home |
| `/USMC/` | `/MarineCorps/` | Legacy site root |
| `/USMC/index.php` | `/MarineCorps/` | |
| `/USMC/Index.php` | `/MarineCorps/` | |
| `/USMC/Home.php` | `/MarineCorps/` | Legacy alternate home |

---

## www.usna.edu — legacy pages → MarineCorps (apply to `/USMC/` and `/Marines/`)

| From path | To path | Confidence | Notes |
|-----------|---------|------------|--------|
| `Prospective_Marine.php` | `/MarineCorps/Midshipmen/prospective-marines.php` | **High** | Same content, modern URL |
| `Summer_Training.php` | `/MarineCorps/Midshipmen/summer-training.php` | **High** | Same content, modern URL |
| `staff.php` | `/MarineCorps/MARDET/leadership.php` | **High** | Detachment leadership bios |
| `FacultyStaffApp.php` | `/MarineCorps/Fleet_Marines.php` | **High** | Fleet / faculty-staff application info |
| `Marine-Company-Mentors-public.php` | `https://intranet.usna.edu/USMC/company_mentors.php` | **Medium** | Legacy public mentors; roster is intranet-only |
| `Midshipmen/company_mentors.php` (www) | `https://intranet.usna.edu/USMC/company_mentors.php` | **High** | Public page removed Jul 2026 |
| `Midshipmen/company_mentor_assignments.php` (www) | `https://intranet.usna.edu/USMC/company_mentors.php` | **High** | Legacy two-page split consolidated |
| `Selection.php` | `/MarineCorps/Midshipmen/prospective-marines.php` | **Medium** | Selection path — confirm with Senior Marine |
| `marine_corps.php` | `/MarineCorps/` | **Medium** | Generic legacy landing |
| `degree_update.php` | `/MarineCorps/Fleet_Marines.php` | **Low** | Internal fleet form — confirm destination |
| `Directives-Control-Point.php` | `/MarineCorps/MARDET/index.php` | **Low** | MARDET internal — confirm with MARDET |
| `MaRSATS External.php` | `/MarineCorps/MARDET/index.php` | **Low** | MaRSATS — confirm still needed or archive |

---

## www.usna.edu — legacy assets (optional)

| From path | To path | Notes |
|-----------|---------|--------|
| `/USMC/Application_FAC_STAFF/*` | `/MarineCorps/Fleet_Marines.php` | PDF/DOCX application templates — or keep assets at legacy path until migrated |
| `/USMC/_files/*` | *(no redirect)* | Legacy bios/PDFs — migrate assets to `/MarineCorps/assets/` or leave until decommission |

---

## www.usna.edu — wrong paths linked from legacy content

These return **404** today but may receive traffic from old bookmarks or bad links:

| From path | To path | Notes |
|-----------|---------|--------|
| `/MarineCorps/roles/aviation.php` | `/MarineCorps/Midshipmen/roles/aviation.php` | Linked from legacy USMC/Marines home |
| `/MarineCorps/roles/index.php` | `/MarineCorps/Midshipmen/roles/index.php` | |
| `/MarineCorps/roles/support.php` | `/MarineCorps/Midshipmen/roles/support.php` | |
| `/MarineCorps/leadership.php` | `/MarineCorps/MARDET/leadership.php` | Retired root path |

---

## www.usna.edu — modern paths that do NOT exist on legacy roots

Do **not** expect `/Marines/Midshipmen/...` or `/USMC/MARDET/...` to work. If needed, redirect:

| From pattern | To pattern |
|--------------|------------|
| `/Marines/Midshipmen/*` | `/MarineCorps/Midshipmen/*` |
| `/Marines/MARDET/*` | `/MarineCorps/MARDET/*` |
| `/Marines/Fleet_Marines.php` | `/MarineCorps/Fleet_Marines.php` |
| `/USMC/Midshipmen/*` | `/MarineCorps/Midshipmen/*` |
| `/USMC/MARDET/*` | `/MarineCorps/MARDET/*` |
| `/USMC/Fleet_Marines.php` | `/MarineCorps/Fleet_Marines.php` |

---

## intranet.usna.edu — separate redirect set

**Do not redirect intranet → www.**

| From path | To path | Notes |
|-----------|---------|--------|
| `/Marines/` | `/USMC/` | Stale alias (canonical tags reference `/Marines/`) |
| `/Marines/index.php` | `/USMC/` | |
| `/Marines/company_mentors.php` | `/USMC/company_mentors.php` | If page exists on both |
| `/MarineCorps/*` | *(404 today)* | No action unless site created |

**Roster (login required):** `https://intranet.usna.edu/USMC/company_mentors.php`

---

## Apache-style examples (for Web Services — not for editors)

```apache
# Site roots
RedirectMatch 301 ^/Marine/?$ /MarineCorps/
RedirectMatch 301 ^/Marines/?$ /MarineCorps/
RedirectMatch 301 ^/USMC/?$ /MarineCorps/

# Legacy flat filenames (USMC and Marines)
RedirectMatch 301 ^/(USMC|Marines)/Prospective_Marine\.php$ /MarineCorps/Midshipmen/prospective-marines.php
RedirectMatch 301 ^/(USMC|Marines)/Summer_Training\.php$ /MarineCorps/Midshipmen/summer-training.php
RedirectMatch 301 ^/(USMC|Marines)/staff\.php$ /MarineCorps/MARDET/leadership.php
RedirectMatch 301 ^/(USMC|Marines)/FacultyStaffApp\.php$ /MarineCorps/Fleet_Marines.php

# Wrong MarineCorps role paths
RedirectMatch 301 ^/MarineCorps/roles/(.*)$ /MarineCorps/Midshipmen/roles/$1
Redirect 301 /MarineCorps/leadership.php /MarineCorps/MARDET/leadership.php
```

Web Services may prefer IIS URL Rewrite or load-balancer rules — above is illustrative only.

---

## After redirects go live

- [ ] Spot-check 10 URLs from each legacy site (200 → 301 → MarineCorps 200).
- [ ] Republish **MarineCorps** pages so left nav no longer links to `/USMC/` or `/Marines/`.
- [ ] Unpublish or archive legacy **USMC/Marines** Cascade sites (after 30-day verification).
- [ ] Update external links (MARADMIN, email signatures, slides) to `/MarineCorps/…`.

---

## Future cutover (not now)

When `/Marines/` becomes the permanent public slug, **reverse** redirects: `/MarineCorps/*` → `/Marines/*`. See `cascade/MIGRATE-TO-MARINES.md`.
