# Migration plan — `usna.edu/Marines` (public + intranet, one site)

Target production host: **`https://www.usna.edu/Marines/`**  
Legacy test host: `https://www.usna.edu/MarineCorps/` (retire with redirects)

This is **one Cascade site** with two audiences — not two separate site roots.

| Audience | How it works on `Marines/` |
|----------|----------------------------|
| **Traditional (public)** | Open pages: home, Midshipmen resources, roles, summer training, fleet info, detachment leadership bios |
| **Intranet (authenticated)** | Same URL tree; Web Services enables **page- or folder-level SSO** on gated assets. Logged-in mids/Marines see roster, emails, MOTY directory, DCP links |

**Nav rule unchanged:** Cascade left nav comes from the **folder tree**. Do not rename `Midshipmen/`, `MARDET/`, or `company_mentors.php` during migration — only change the **site root slug** (`MarineCorps` → `Marines`) and paste bodies.

---

## Canonical structure at `Marines/`

```
Marines/                              ← Cascade site root (replaces MarineCorps/)
├── index.php
├── Fleet_Marines.php
├── _files/css/local.css
├── _files/js/…
├── assets/images/public/…            ← open web
├── assets/images/intranet/…          ← gated pages only
├── MARDET/
│   ├── index.php                     ← hub (may be gated or split public/internal)
│   ├── leadership.php                ← public bios
│   └── marines_on_the_yard.php       ← public cards; directory JS gated
└── Midshipmen/
    ├── index.php
    ├── prospective-marines.php
    ├── summer-training.php
    ├── company_mentors.php           ← public overview
    ├── company_mentor_assignments.php ← gated roster
    └── roles/…
```

Folder names stay identical to today. Only the **root folder name** changes.

Canonical URL map: **`cascade/LIVE-URLS.md`** (sourced from **`cascade/site-urls.json`**).

---

## Public vs intranet on one host (confirm with Web Services)

Ask Web Services which pattern they support on `Marines/`:

### Option A — Page-level auth (preferred)

| Page | Anonymous visitor | Logged-in USNA user |
|------|-------------------|---------------------|
| `Midshipmen/company_mentors.php` | USNA login prompt | Full 36-card roster paste |
| `MARDET/marines_on_the_yard.php` | Community cards only, or login for `#yard-directory` | Full directory |
| `MARDET/index.php` | Public teaser or login | MARDET Team hub + internal links |

- Paste: **`paste-intranet-company-mentors-marinecorps.html`** on the gated page.
- **No separate stub** required if anonymous users never receive roster HTML.
- Nav link stays; unauthenticated click → login → roster.

### Option B — Public stub + gated full page (same path not possible)

If Cascade **cannot** gate a single page, use:

- Public nav item → **`paste-public-company-mentors-stub-marinecorps.html`** (no PII)
- Authenticated users bookmark a **Web Services–provided** gated URL or secondary path (last resort)

Prefer Option A; stub paste exists as fallback (`DEPLOY-MENTORS-INTRANET-SPLIT.md`).

### Gated folders (recommended list for Web Services)

| Path | Content |
|------|---------|
| `Midshipmen/company_mentors.php` | Public program overview |
| `Midshipmen/company_mentor_assignments.php` | Full mentor roster |
| `MARDET/marines_on_the_yard.php` | Yard directory JS + roster data |
| `MARDET/index.php` | Internal quick links (Google Drive, DCP) when added |
| `assets/images/intranet/` | Mentor headshots, staff photos |
| `_files/js/intranet/` | Roster data JS |

Keep `assets/images/public/` for leadership, summer training, roles — safe on open web.

---

## Migration phases

### Phase 0 — Web Services kickoff

- [ ] Confirm site slug: **`Marines`** (not `MarineCorps`, not `USMC`)
- [ ] Confirm auth model (Option A vs B) and which folders get SSO
- [ ] Plan **301 redirects**: `/MarineCorps/*` → `/Marines/*`
- [ ] Confirm whether `Midshipmen/` and `MARDET/` casing stays the same

### Phase 1 — Repo URL sweep (before paste)

```bash
python3 scripts/apply-site-urls.py
```

Updates `MarineCorps` → `Marines` in `cascade/*.html`, includes, snippets, and build scripts.  
Config: `cascade/site-urls.json`. Re-run after any manual edit that reintroduces legacy URLs.

Regenerate dynamic pastes:

```bash
bash scripts/build-intranet-mentors-paste.sh
python3 scripts/build-summer-training-pages.py
```

### Phase 2 — Build `Marines/` tree in Cascade (copy, don’t move)

1. Create new site root **`Marines/`** (or let Web Services clone `MarineCorps/` → `Marines/`).
2. **Mirror folder tree** exactly (`SITE-STRUCTURE.md`).
3. Upload `_files/`, `assets/` to **`Marines/_files/`**, **`Marines/assets/`** — same relative paths as today.
4. Paste pages using updated paste files (URLs already say `…/Marines/…`).
5. **Configure → Include in Navigation** on each folder/page — match current MarineCorps site order.
6. Apply **page/folder auth** on gated list above.
7. Publish **`Marines/`** root and all contents.

### Phase 3 — Smoke test on `Marines/`

| Check | URL |
|-------|-----|
| Home | `https://www.usna.edu/Marines/` |
| Prospective Marines | `…/Marines/Midshipmen/prospective-marines.php` |
| Company mentors (logged out) | Login wall or stub — **no** `mailto:` in anonymous view source |
| Company mentors (logged in) | 36 cards, photos |
| Left nav | Home, Midshipmen, MARDET, Fleet — no 404s |

### Phase 4 — Cutover

1. Enable redirects `MarineCorps` → `Marines`.
2. Republish or unpublish old `MarineCorps/` site (Web Services).
3. Update external links (MARADMIN refs, emails, slides) to `…/Marines/…`.
4. GitHub Pages preview: optional; production of record is Cascade `Marines/`.

### Phase 5 — Decommission `MarineCorps/`

- Archive Cascade site folder (do not delete until redirects verified 30+ days).
- Remove legacy base from paste comments after cutover (optional cleanup).

---

## Nav safety during migration

| Do | Don’t |
|----|-------|
| Copy tree to `Marines/` with same child folder names | Rename `company_mentors.php` or move under `MARDET/` |
| Paste body HTML only in source mode | Drag pages between folders (breaks nav order) |
| Republish root + all contents after nav metadata changes | Run two competing roots (`MarineCorps` + `Marines`) in the same nav |
| Keep **Include in Navigation** settings when copying | Delete public mentor page — gate it instead |

See **`FIX-NAV.md`** if MARDET folder drops out of the menu after bulk publish.

---

## Paste file → audience matrix (`Marines/`)

| Paste file | Page path | Audience |
|------------|-----------|----------|
| `paste-home-marinecorps.html` | `index.php` | Public |
| `paste-midshipmen-marinecorps.html` | `Midshipmen/index.php` | Public |
| `paste-prospective-marines-marinecorps.html` | `Midshipmen/prospective-marines.php` | Public |
| `paste-summer-training-marinecorps.html` | `Midshipmen/summer-training.php` | Public |
| `paste-roles-*-marinecorps.html` | `Midshipmen/roles/*.php` | Public |
| `paste-fleet-application-marinecorps.html` | `Fleet_Marines.php` | Public |
| `paste-leadership-marinecorps.html` | `MARDET/leadership.php` | Public |
| `paste-intranet-mardet-marinecorps.html` | `MARDET/index.php` | Gated |
| `paste-intranet-company-mentors-marinecorps.html` | `Midshipmen/company_mentor_assignments.php` | Gated |
| `paste-public-company-mentors-marinecorps.html` | `Midshipmen/company_mentors.php` | Public |
| `paste-intranet-marines-on-the-yard-marinecorps.html` | `MARDET/marines_on_the_yard.php` | Mixed / gated for directory |

*(Paste filenames still say `marinecorps` — content URLs inside point at `Marines/` after `apply-site-urls.py`. Rename files later; not required for launch.)*

---

## Related docs

| Doc | Purpose |
|-----|---------|
| `SITE-STRUCTURE.md` | Folder tree + nav rules |
| `LIVE-URLS.md` | URL map for paste links |
| `site-urls.json` | Machine-readable bases + paths |
| `DEPLOY-MENTORS-INTRANET-SPLIT.md` | Mentor gating detail |
| `DEPLOY-INTRANET.md` | Asset upload + smoke tests |
| `docs/PUBLISH-SPLIT.md` | Repo public vs gated content rules |
