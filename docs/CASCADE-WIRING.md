# Cascade CSS & JS wiring

How to attach Marines site assets in Hannon Hill Cascade CMS. Local preview uses `css/main.css` with `@import`; **Cascade should use the single bundled file** instead.

## USNA USMC site — fix unstyled pages (start here)

If pasted HTML shows plain text / no hero cards / no navy+gold styling, the page is missing **`marines.css`**. The live USMC template only loads USNA Foundation CSS plus `_files/css/local.css` — not your repo’s `css/main.css`.

**Do not put `<link>` tags inside the page body.** Cascade strips or ignores them in the WYSIWYG/HTML block. CSS belongs in the **Template `<head>`** (or via `local.css` — see below), same place as `local.css`.

### Step 1 — Upload the bundle

1. Run locally: `bash scripts/build-cascade-bundle.sh`
2. In Cascade **Administration → Assets**, open the **USMC** site folder `_files/css/`
3. Upload **`cascade/marines.css`** as **`marines.css`** (sibling to `local.css`)

Verify in a browser (must return **200**, not 404):

`https://www.usna.edu/USMC/_files/css/marines.css`

### Step 2 — Link it in the Format (not the page content)

Edit the **USMC page Format** (the template that outputs `<head>`). Find the existing line:

```html
<link href="_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>
```

Add **immediately after it** (snippet: `cascade/snippets/head-css-usna-usmc.html`):

```html
<link href="_files/css/marines.css" media="all" rel="stylesheet" type="text/css"/>
```

Publish the **Format**, then publish the **page**.

### Step 3 — JavaScript (mobile nav)

Upload `js/main.js` to `_files/js/main.js`. In the Format **footer** (after jQuery/Foundation), add:

```html
<script src="_files/js/main.js" type="text/javascript"></script>
```

(Snippet: `cascade/snippets/foot-standard-usna-usmc.html`.)

### Step 4 — Paste content only

In the page editor, paste **only** what is between:

`<!-- CASCADE: page content start -->` … `<!-- CASCADE: page content end -->`

Do **not** paste `<html>`, `<head>`, `<link>`, or `<script>` from the repo files — the USNA wrapper already provides those regions.

### No Template access? Use `local.css` instead

**→ Full walkthrough: [`docs/CASCADE-NO-TEMPLATE-ACCESS.md`](CASCADE-NO-TEMPLATE-ACCESS.md)**

1. Upload `cascade/marines.css` to `_files/css/marines.css`
2. Edit existing **`local.css`** in the same folder
3. Add at the bottom: `@import url("marines.css");`
4. Publish `local.css` and republish your page

Also try **Edit page → Configure** tab for a CSS/HEAD region. If neither works, ask the USNA webmaster to add one `<link>` to the USMC Template.

---

## Quick fix (most common problem)

**Do not upload only `main.css`.** Cascade serves each asset by URL; `@import url("variables.css")` resolves relative to the CSS file’s folder in the asset library. If sibling files are missing or paths differ, **nothing loads**.

**Use:** `cascade/marines.css` (one file, no imports).

Regenerate after CSS changes:

```bash
bash scripts/build-cascade-bundle.sh
```

---

## 1. Upload assets once

In Cascade **Administration → Assets**, create a folder (example: `marines` under your USMC site). Upload:

| Local path | Cascade (example) |
|------------|-------------------|
| `cascade/marines.css` | `marines/marines.css` |
| `js/main.js` | `marines/js/main.js` |
| `js/company-mentors.js` | `marines/js/company-mentors.js` |
| `js/marines-on-the-yard.js` | `marines/js/marines-on-the-yard.js` |
| `js/intranet/company-mentors-data.js` | `marines/js/intranet/company-mentors-data.js` |
| `js/intranet/marines-on-the-yard-data.js` | `marines/js/intranet/marines-on-the-yard-data.js` |
| `assets/images/**` | `marines/images/**` (keep folder structure) |

On USNA, published URLs often look like:

`https://www.usna.edu/USMC/_files/marines/marines.css`

Use that path (or your site’s equivalent) as **ASSET_BASE** in the snippets below — **without** a trailing slash.

Copy-paste snippets live in `cascade/snippets/` (replace `ASSET_BASE`).

---

## 2. Page template mapping

Each HTML file in the repo has markers:

```html
<!-- CASCADE: page content start -->
…paste this block only…
<!-- CASCADE: page content end -->
```

Wire **CSS once per Format** (or site metadata). Wire **JS per page type** — script order matters.

| Page | Repo file | JS snippet |
|------|-----------|------------|
| Home | `index.html` | `foot-standard.html` |
| Midshipmen hub | `pages/midshipmen/index.html` | `foot-standard.html` |
| Prospective Marines | `pages/prospective-marines.html` | `foot-standard.html` |
| Summer training | `pages/summer-training.html` | `foot-standard.html` |
| Fleet application | `pages/fleet-application.html` | `foot-standard.html` |
| Leadership | `pages/leadership.html` | `foot-standard.html` |
| Roles (index + subpages) | `pages/roles/*.html` | `foot-standard.html` |
| MARDET intranet hub | `pages/intranet/index.html` | `foot-standard.html` |
| Company mentors | `pages/intranet/company-mentors.html` | `foot-company-mentors.html` |
| Marines on the Yard | `pages/intranet/marines-on-the-yard.html` | `foot-marines-on-the-yard.html` |

**CSS for all pages:** `head-css.html` → one `<link>` to `marines.css`.

---

## 3. Where to paste in Cascade

USNA setups vary; use whichever your site exposes:

### Option A — Page Metadata (recommended)

1. Edit the **Format** or **Page** → **Metadata**.
2. **CSS** field: paste `cascade/snippets/head-css.html` (with real ASSET_BASE).
3. **JavaScript** field: paste the matching foot snippet for that page type.
4. **Main content** WYSIWYG / HTML block: only the region between the CASCADE comments.

### Option B — Format blocks

If Marines pages share a custom Format:

- Put the CSS `<link>` in the Format’s `<head>` block.
- Put JS in the Format’s footer block **or** override per page in metadata.
- Use **two Formats** if needed: `Marines Standard` vs `Marines Data` (mentors/yard foot scripts).

### Option C — System Default / site-wide CSS

Some sites allow one site CSS include — only do this if Marines styles must apply site-wide. Prefer a Marines-only Format so `.site-header` and nav styles don’t leak elsewhere.

---

## 4. Header, nav, and mobile menu

`main.js` toggles `.site-nav` and `.nav-toggle`. Those elements must exist in the **published HTML**, not only in local preview files.

**If the USNA global template wraps your content** and does **not** include our nav:

- Include the header block from any repo page **inside** the pasted content (between CASCADE comments), **or**
- Extend your Marines Format to output that header above `$content`.

If you paste **content only** and omit the header, CSS will still apply to cards and typography, but **mobile nav won’t work** (no matching DOM).

---

## 5. Images in pasted HTML

Local files use relative paths (`../assets/images/...`). In Cascade content, switch to asset URLs:

```html
<!-- Local preview -->
<img src="../assets/images/public/leadership/col-reid.jpg" alt="…">

<!-- Cascade (example) -->
<img src="/USMC/_files/marines/images/public/leadership/col-reid.jpg" alt="…">
```

Keep the `public/`, `intranet/`, and `shared/` folder names when uploading — do not flatten into a single `images/` directory.

Mentor and yard pages load photos via JS from paths inside the data files (`js/intranet/*-data.js`). After upload, update `photo` fields to Cascade paths such as `_files/marines/images/intranet/mentors/company-01.jpg`.

---

## 6. Intranet-only pages

Do not publish intranet HTML to the open USMC site. Host on USNA intranet with the same asset wiring; use `foot-company-mentors.html` or `foot-marines-on-the-yard.html` as appropriate.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Unstyled page | Only `main.css` linked, imports 404 | Link `marines.css` bundle |
| Nav doesn’t toggle | No `.site-nav` / `.nav-toggle` in page | Add header HTML or Format block |
| Empty mentor grid | Data script missing or wrong order | Load `company-mentors-data.js` **before** `company-mentors.js` |
| `COMPANY_MENTORS is undefined` | Script order or blocked JS | Check foot snippet order; avoid async/defer on data files |
| Broken photos | Relative paths in data JS | Update paths to `_files/marines/...` |
| Styles clash with USNA | Global CSS load order | Scope Marines Format; load `marines.css` after USNA base if needed |

---

## 8. Checklist per new page

1. Copy content between CASCADE comments into Cascade editor.
2. Confirm Format/metadata includes `marines.css`.
3. Add correct foot snippet (standard vs mentors vs yard).
4. Replace image `src` with `_files` URLs.
5. Publish → verify CSS, nav, and any dynamic grids in browser devtools (Network tab for 404s).
