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
