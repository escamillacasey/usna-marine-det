# Fix left nav “Home” link (USNA Cascade)

There is **no separate “Navigation” menu** in Administration on USNA’s Cascade setup. The left nav and sitemap are both **auto-generated** from your **site folder tree** via **Index Blocks** in the USNA page **Format/Configuration** (Standard 3.0 template).

That matches what you saw: moving `indexOldOld.php` to Archive updated the **sitemap**, but interior pages can still show the old Home URL until they are **republished**.

---

## Why Home still points at `indexOldOld.php`

Each published page embeds a snapshot of the left nav HTML. Example from live source:

```html
<li><a href="https://www.usna.edu/MarineCorps/indexOldOld.php">Home</a></li>
```

The nav block still thinks the site “home” asset is `indexOldOld.php`, **or** those pages have not been republished since you archived it.

---

## Fix (try in this order)

### 1. Set the real home page at site root

In **Site Content** (open the **Marine Corps - Public** site — not Administration):

1. At the **site root**, confirm **`index.php`** exists and is your new homepage content.
2. Open **`index.php`** → **Configure** tab (or **More → Configure**).
3. Look for:
   - **Include in Navigation** — should be **Yes**
   - **Display Name** — e.g. “Home” or “USNA Marines”
   - Any **Index** / **Default page for folder** option — this page should be the root index.
4. Open the archived **`indexOldOld`** (in Archive folder) → **Configure**:
   - **Include in Navigation** → **No** (if available)
   - Or **Unpublish** it so it is not the site index candidate.

### 2. Republish so nav regenerates

Index Blocks refresh when relevant content changes, but **each page must be republished** to push new nav HTML live.

1. In Site Content, go to the **Marine Corps root folder**.
2. **Publish** → publish **this folder and all contents** (or use your site’s bulk publish).
3. Hard-refresh a test page (Cmd+Shift+R) and click **Home** — should go to `index.php` or `/MarineCorps/`.

If only the sitemap updated before, you likely republished the sitemap page but not the rest of the site.

### 3. Check folder order (nav order)

Nav order follows **Order** column in Site Content, not alphabetical name.

1. Open the site root folder in Site Content.
2. Click the **Order** column header to sort by order number.
3. Put **`index.php`** first (drag or edit order values).
4. Republish the root folder and descendants again.

### 4. Search for a nav Index Block asset (optional)

Some USNA sites keep shared blocks under a `_blocks`, `_cascade`, or `formats` folder:

1. Site Content → search asset name: `nav`, `navigation`, `side`, `left`
2. If you find an **Index Block** used for left nav, open it and check **Start Folder** / indexed folder — should be site root, not Archive.

You usually **do not edit the Format** (webmaster-owned). Focus on which pages are published, indexed, and included in navigation.

### 5. Site Settings (gear icon on the site)

**Manage Site → Site Settings** (wording varies):

- **Index page** / **Default page** / **Live URL** — should match `index.php`, not `indexOldOld.php`.

---

## If Home is still wrong after full republish

The Standard 3.0 **Format** may hard-code “Home” to a specific asset path. That requires **USNA Webmaster** (`websupport@usna.edu`):

> “Marine Corps - Public left nav Home link still outputs `indexOldOld.php` after archiving that page and republishing. Please point the nav Index Block / site index to `index.php`.”

---

## What you cannot fix from paste HTML

The left nav is **outside** your page body paste. Updating `paste-home-marinecorps.html` does not change **Home** in the sidebar.

---

## Quick verify

| Check | Expected |
|-------|----------|
| `https://www.usna.edu/MarineCorps/` | 200, new homepage |
| `https://www.usna.edu/MarineCorps/indexOldOld.php` | 404 |
| Left nav **Home** on `leadership.php` | `index.php` or `/MarineCorps/` |

See also **`LIVE-URLS.md`** for in-content link paths (fleet, Midshipmen subpages, etc.).

---

## MARDET / “Marine Detachment” folder missing from left nav

**Symptom:** `MARDET/index.php` loads at  
`https://www.usna.edu/MarineCorps/MARDET/index.php`, but the left nav only shows Home, MARDET Leadership, Midshipmen, Fleet Marines — **no Marine Detachment / MARDET section** (no dropdown for Company Mentors, Marines on the Yard).

Same root cause as Home: nav is **auto-generated from the site folder tree**. The folder or its index page is not indexed for navigation, or pages were not republished after a change.

### Fix (Cascade Site Content)

1. Open **Marine Corps - Public** → site root.
2. Open the **`MARDET`** folder (display name may be **Marine Detachment**).
3. On the **folder** and on **`MARDET/index.php`** → **Configure**:
   - **Include in Navigation** → **Yes**
   - **Display Name** → e.g. **Marine Detachment** or **MARDET** (what you want in the menu)
4. On child pages that should appear under it:
   - `company_mentors.php` → **Include in Navigation → Yes** (public overview)
   - `company_mentor_assignments.php` → gated roster; optional in nav
   - `marines_on_the_yard.php` → **Include in Navigation → Yes** (when published)
5. In the **root folder**, sort by **Order** and place **MARDET** where you want it (typically after Midshipmen, before Fleet Marines).
6. Confirm **`MARDET/index.php`** is **Published** (not draft only).
7. **Publish the site root folder and all contents** so every page gets fresh nav HTML.

### Verify

| Check | Expected |
|-------|----------|
| Left nav on `index.php` | **Marine Detachment** (or MARDET) with sub-links |
| Hover / mobile | Company Mentors, Marines on the Yard |
| Direct URL still works | `…/MARDET/index.php` → 200 |

### If it keeps disappearing

Something is resetting nav metadata when you publish or move assets:

- Re-check **Include in Navigation** on the **MARDET folder** after each bulk publish.
- Do not move `MARDET/` under Archive or a non-indexed parent.
- Avoid duplicating the folder (two MARDET copies — only one should be in nav).
