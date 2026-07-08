# Cascade deploy order — MarineCorps test site

Homepage (`working.php`) is done. Deploy the three pages it links to next.

## Every page (same workflow as home)

1. **Add Content** → Page (match template used by `working.php`)
2. Set output path / filename (see table below)
3. Paste file contents in **HTML / source mode**
4. **Publish**
5. View source → confirm `local.css` link and page content

## Recommended order

### 1. Leadership (`paste-leadership-marinecorps.html`)

**Before paste:** upload photos to `_files/images/public/leadership/`:

| Local file | Cascade path |
|------------|----------------|
| `assets/images/public/leadership/col-reid.jpg` | `_files/images/public/leadership/col-reid.jpg` |
| `assets/images/public/leadership/ltcol-giraldi.jpg` | `_files/images/public/leadership/ltcol-giraldi.jpg` |

**Page path:** `leadership.php`

Unblocks home card + fleet FAQ links.

---

### 2. Fleet assignments (`paste-fleet-application-marinecorps.html`)

**Page path:** `fleet-application.php`

No extra assets.

---

### 3. Midshipmen hub (`paste-midshipmen-marinecorps.html`)

**Page path:** `midshipmen/index.php` (create `midshipmen` folder in Cascade)

Note: CSS link uses `../_files/css/local.css` (one level down from site root).

Links to subpages that don't exist yet — deploy those next when ready.

---

## After these three

| Paste file | Repo source | Cascade path |
|------------|-------------|--------------|
| `paste-prospective-marines-marinecorps.html` | `pages/prospective-marines.html` | `prospective-marines.php` |
| `paste-summer-training-marinecorps.html` | `pages/summer-training.html` | `summer-training.php` |

Roles pages (`roles/index.php`, etc.) already exist on the live site — update later if needed.

---

## Go live

When `working.php` is ready to replace the public home:

1. Paste home content into `index.php`
2. Or rename outputs per webmaster guidance
3. Republish

---

## CSS reminder

First line of every paste file:

```html
<link href="_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>
```

Subfolder pages use `../_files/css/local.css`.

After editing repo CSS, run `bash scripts/print-local-css-append.sh` and update `local.css` in Cascade assets.

---

## Fine-tune pass (deferred)

Track these when circling back after the 70% publish:

| Issue | Notes |
|-------|-------|
| **Site nav intermittent** | Header/nav (`site-header`, `nav-toggle`, `site-nav`) is not in paste files — relies on USNA template or is missing entirely. Nav only works when that DOM is present; inconsistent across pages. **Fix:** include header block in paste content (or Marines Format) on every page; verify `main.js` nav toggle on Cascade output. |
| Roles pages | Repo stubs only; live `roles/*.php` may still be legacy content |
| Hero / content images | Wire `assets/images/public/content/` into pages |
| Marine Cyber | Static hub card until 2027 revamp |

**Intranet deploy:** see `cascade/DEPLOY-INTRANET.md`.
