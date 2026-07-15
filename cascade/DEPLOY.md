# Cascade deploy order — MarineCorps test site

Live site map: **`cascade/LIVE-URLS.md`**  
Fix broken **Home** nav: **`cascade/FIX-NAV.md`** (Cascade navigation — not paste HTML)

Homepage (`index.php`) is live. Re-paste pages after URL or CSS changes; append updated `marines.css` to `_files/css/local.css`.

## Every page (same workflow)

1. **Add Content** → Page (match template used by home)
2. Set output path / filename (see table below)
3. Paste file contents in **HTML / source mode**
4. **Publish**
5. View source → confirm `local.css` link and page content

## Live paths (paste files updated)

| Paste file | Cascade path |
|------------|----------------|
| `paste-home-marinecorps.html` | `index.php` |
| `paste-leadership-marinecorps.html` | `MARDET/leadership.php` |
| `paste-fleet-application-marinecorps.html` | `Fleet_Marines.php` |
| `paste-midshipmen-marinecorps.html` | `Midshipmen/index.php` |
| `paste-prospective-marines-marinecorps.html` | `Midshipmen/prospective-marines.php` |
| `paste-summer-training-marinecorps.html` | `Midshipmen/summer-training.php` |
| `paste-roles-ground-marinecorps.html` | `Midshipmen/roles/index.php` |
| `paste-roles-aviation-marinecorps.html` | `Midshipmen/roles/aviation.php` |
| `paste-roles-support-marinecorps.html` | `Midshipmen/roles/support.php` |
| `paste-intranet-mardet-marinecorps.html` | `MARDET/index.php` |
| `paste-intranet-company-mentors-marinecorps.html` | `Midshipmen/company_mentors.php` |
| `paste-intranet-marines-on-the-yard-marinecorps.html` | `MARDET/marines_on_the_yard.php` *(when ready)* |

**Photos:** upload to `assets/images/public/leadership/` and `assets/images/public/mentors/` (see `LIVE-URLS.md`).

**Summer training gallery:** drop sitrep photos in `assets/images/incoming/summer-training/`, list them in `data/summer-training-photos.csv`, then run `python3 scripts/import-summer-training-photos.py` and `python3 scripts/build-summer-training-pages.py`. Upload `assets/images/public/summer-training/` to Cascade before re-pasting `paste-summer-training-marinecorps.html`.

**Roles** (`roles/index.php`, etc.): paste files still link here — pages return 404 until published.

## CSS reminder

First line of root paste files:

```html
<link href="_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>
```

Subfolder pages: `../_files/css/local.css`

After repo CSS changes:

```bash
bash scripts/print-local-css-append.sh > /dev/null
```

Copy **`cascade/paste-local-css-append.css`** → paste at the **bottom** of Cascade `_files/css/local.css` → publish. See **`cascade/APPEND-LOCAL-CSS.md`**.

**Banner fix:** Interior pages must use **`marines-page-header`** (not `page-header`). Re-paste updated HTML files after updating `local.css`.

## Fine-tune pass (deferred)

| Issue | Notes |
|-------|-------|
| **Site nav Home → 404** | Fix in Cascade navigation per `FIX-NAV.md` |
| **Fleet + MOTY outdated** | Re-paste per `DEPLOY-REMAINING.md` |
| Hero / content images | Wire `assets/images/public/content/` into pages |
| Marine Cyber | Static hub card until 2027 revamp |

**Intranet deploy:** see `cascade/DEPLOY-INTRANET.md`. **Remaining public pastes:** see `cascade/DEPLOY-REMAINING.md`.
