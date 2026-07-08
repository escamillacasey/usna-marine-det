# No Default CSS region? Wire `local.css` another way

Content authors on USNA Marine Corps often **do not** see a **Default CSS** region on the Configure tab. That region only appears if the Template defines something like `<system-region name="DEFAULT_CSS"/>` in the `<head>`. Your template probably only has **DEFAULT** (page body).

`index.php` loads `local.css` because its **Configuration** includes that link — not because you attached it on the page.

---

## Option A — Use the same Configuration as `index.php` (try first)

1. Open **`index.php`** in Cascade (the one that loads `local.css` on publish).
2. Note its **Configuration** name:
   - **Edit → Configure**, or
   - **Edit → Outputs →** (HTML output) **Configuration** field, or
   - asset details / Info panel on the right.
3. Open **`working.php`** → same screen → set the **same Configuration**.
4. **Submit** and **Publish** `working.php`.
5. View source — search for `local.css`.

If the Configuration is inherited and grayed out, check for **Override** / **Unlock** on the page before changing it.

---

## Option B — Manage Site → Configurations

1. **Manage Site → Configurations**
2. Open the Configuration used by **`roles/index.php`** or **`index.php`** (ask a colleague if unsure).
3. **Edit → Outputs →** your HTML output (often named like `page` or `html`).
4. Under **Regions**, look for anything head-related (`CSS`, `HEAD`, `DEFAULT_CSS`, `METADATA`, etc.) with a block that contains the `local.css` link.
5. Either:
   - Assign **`working.php`** to this Configuration (Option A), or
   - Create a **new Configuration** copied from this one for test pages.

Publish the Configuration, then publish `working.php`.

---

## Option C — Paste the stylesheet link in page content (no Configure access)

If you only edit the **Content** tab, add this as the **first line** of your HTML (source mode):

```html
<link href="_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>
```

Included at the top of `cascade/paste-home-marinecorps.html`.

Cascade sometimes strips `<link>` from WYSIWYG; **source/HTML mode** usually keeps it. A `<link>` in the body is valid HTML5 and browsers will load it.

Publish the page and confirm `local.css` appears in view-source.

---

## Option D — Ask USNA Webmaster (one-time)

Request a single line in the Marine Corps Template `<head>` (affects all pages):

```html
<link href="_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>
```

You already maintain Marines styles inside `local.css` — they only need to wire the link once.

---

## How to see what regions you actually have

1. **Preview** the page → **More** menu → **Show Regions** (if available).
2. Or **Edit → Configure** — list every region name shown (often just **DEFAULT**).
3. Or **Edit → Outputs** — expand the HTML output and read the **Regions** list.

If the only region is **DEFAULT**, you cannot attach head CSS via Configure without webmaster help — use **Option A** or **Option C**.

---

## After `local.css` loads

Replace the full page HTML on `working.php` with **`cascade/paste-home-marinecorps.html`** (source/HTML mode only — not WYSIWYG).

Changes from the broken version:
- Cards use `<div class="audience-card">` with a link only on the CTA line (Cascade won't tear them apart)
- MARDET card removed (public site); middle card is **Detachment Leadership**
- Links use `https://www.usna.edu/MarineCorps/...` paths, not `pages/...html`
- `<link href="_files/css/local.css">` stays as the first line

After editing `css/components.css`, re-run `bash scripts/print-local-css-append.sh` and update `local.css` in Cascade.
