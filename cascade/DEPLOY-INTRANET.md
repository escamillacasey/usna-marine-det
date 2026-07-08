# Cascade deploy — intranet (MARDET)

**Host on USNA intranet only** (`intranet.usna.edu` or equivalent). Do **not** publish these pages to the open `www.usna.edu/MarineCorps` site.

Same CSS workflow as public pages: `local.css` with Marines bundle appended at the bottom.

## Assets to upload first

| Local | Cascade path |
|-------|----------------|
| `js/main.js` | `_files/js/main.js` |
| `js/company-mentors.js` | `_files/js/company-mentors.js` |
| `js/marines-on-the-yard.js` | `_files/js/marines-on-the-yard.js` |
| `js/intranet/company-mentors-data.js` | `_files/js/intranet/company-mentors-data.js` |
| `js/intranet/marines-on-the-yard-data.js` | `_files/js/intranet/marines-on-the-yard-data.js` |
| `assets/images/intranet/mentors/company-*.jpg` | See **Photo upload** below |

### Photo upload (pick one)

| Where you publish | Cascade folder | HTML `src` (page under `mardet/`) |
|-------------------|----------------|-------------------------------------|
| **Marine Corps - Public** (`www.usna.edu/MarineCorps`) | `_files/images/public/mentors/` | `../_files/images/public/mentors/company-02.jpg` |
| **USNA intranet** (`intranet.usna.edu`) | `_files/images/intranet/mentors/` | `../_files/images/intranet/mentors/company-02.jpg` |

**Important:** `intranet/` assets return WAF HTML (not JPEG) on the public www site. Copy photos to `public/mentors/` for Marine Corps - Public testing.

Regenerate: `bash scripts/build-intranet-mentors-paste.sh`

### Photos missing on live site?

**Symptom:** Network shows **200** but `Content-Type: text/html` and ~281 bytes — broken image icons. That is the USNA WAF returning “Request Rejected” for `intranet/` asset URLs on the **public** www site. The path is correct; the folder name is blocked.

**Fix on Marine Corps - Public:** move photos in Cascade to `_files/images/public/mentors/`, re-paste the default paste file (`public/mentors` paths), publish.

1. On the **live** page: DevTools → **Network** → filter **Img** → confirm `Content-Type` is `image/jpeg` (not `text/html`).
2. Compare to working **leadership.php** photos (`_files/images/public/leadership/`).
3. Confirm photos are **uploaded and published** in the matching Cascade folder (not draft only).
4. On real intranet host, use `intranet/mentors` paths and regenerate with `CASCADE_PHOTO_PREFIX` above.
5. If still blocked, email **websupport@usna.edu** with the support ID from the rejection page.

## Recommended order

### 1. MARDET hub (`paste-intranet-mardet-marinecorps.html`)

**Page path:** `mardet/index.php` (create `mardet/` folder — adjust name to match your intranet URL plan)

**JS:** standard — `main.js` only (paste link in page HTML or metadata).

---

### 2. Company mentors (`paste-intranet-company-mentors-marinecorps.html`)

**Page path:** `mardet/company-mentors.php`

**Static HTML (no JavaScript):** paste file includes all 36 mentor cards, grouped by battalion. Battalion jump links replace the JS filter toolbar.

**Before paste:** upload mentor photos to `_files/images/public/mentors/` (Marine Corps - Public on www) or `_files/images/intranet/mentors/` (real intranet host).

**After roster changes:** run `python3 scripts/sync-from-sheets.py` then `python3 scripts/generate-mentor-cards-html.py` and re-paste.

**No page-metadata JavaScript required.**

---

### 3. Marines on the Yard (`paste-intranet-marines-on-the-yard-marinecorps.html`)

**Page path:** `mardet/marines-on-the-yard.php`

**JS metadata:**

```html
<script src="_files/js/intranet/company-mentors-data.js"></script>
<script src="_files/js/intranet/marines-on-the-yard-data.js"></script>
<script src="_files/js/marines-on-the-yard.js"></script>
<script src="_files/js/main.js"></script>
```

Snippets: `cascade/snippets/foot-marines-on-the-yard.html`.

---

## CSS link by folder depth

| Page | First line of paste |
|------|---------------------|
| `mardet/index.php` | `<link href="../_files/css/local.css" …/>` |
| `mardet/company-mentors.php` | `<link href="../_files/css/local.css" …/>` |
| `mardet/marines-on-the-yard.php` | `<link href="../_files/css/local.css" …/>` |

Adjust `../` if your intranet folder depth differs.

---

## Cascade JS smoke test

Run after each intranet page is **published**. Use Chrome or Edge DevTools (F12).

### A. Asset URLs (once, before data pages)

Open each URL directly in the browser (replace host/path if your intranet base differs):

| URL | Expect |
|-----|--------|
| `…/_files/js/main.js` | 200, ~1.5 KB |
| `…/_files/js/company-mentors.js` | 200, ~3 KB |
| `…/_files/js/marines-on-the-yard.js` | 200 |
| `…/_files/js/intranet/company-mentors-data.js` | 200, starts with `window.COMPANY_MENTORS` |
| `…/_files/js/intranet/marines-on-the-yard-data.js` | 200, starts with `window.MARINES_ON_THE_YARD` |
| `…/MarineCorps/_files/images/public/mentors/company-02.jpg` | 200 + `Content-Type: image/jpeg` |

Any **404** → fix upload path before testing pages.

### B. MARDET hub (`mardet/index.php`)

- [ ] View page source → `local.css` link present (`../_files/css/local.css`)
- [ ] Hub cards styled (gold left border)
- [ ] **Console** (F12 → Console): no red errors *(optional `main.js` only if wired in metadata)*

### C. Company mentors (`mardet/company-mentors.php`) — static HTML

**Page source**

- [ ] Battalion jump nav (`#battalion-1` … `#battalion-6`) present
- [ ] `.mentor-grid` contains **36** `.mentor-card` articles
- [ ] Cards visible in page source (not an empty grid waiting for JS)

**Photos** (Network tab, hard refresh)

- [ ] Spot-check `company-02.jpg` → 200
- [ ] Companies **1** and **20** show “Photo pending” placeholder until photos uploaded

**Behavior**

- [ ] Battalion jump links scroll to the right section
- [ ] Cards show name, duties, and email where applicable

### D. Marines on the Yard (`mardet/marines-on-the-yard.php`)

**Network**

- [ ] `company-mentors-data.js` → 200 (first)
- [ ] `marines-on-the-yard-data.js` → 200 (second)
- [ ] `marines-on-the-yard.js` → 200 (third)

**Console**

- [ ] No errors on load

**Page behavior**

- [ ] `#yard-directory` contains multiple `.yard-group` sections
- [ ] **Company Marine Mentors** section lists mentors
- [ ] Other communities appear (MARDET, instructors, etc.) if present in data
- [ ] Community cards above directory still styled

### E. Editor discipline

- [ ] Re-open page in **source/HTML mode** only after publish — avoid visual editor on mentors/yard pages
- [ ] After any re-paste, re-run sections C or D

### F. Escalate to webmaster if

- Configure tab has **no JavaScript** field
- Scripts in metadata do not appear in published HTML source
- Cascade strips `id="mentor-grid"` or filter buttons from paste

---

## Fine-tune (deferred)

- Same **site nav** issue as public pages — see `DEPLOY.md` fine-tune table.
- Staff headshots on key contacts (optional).
- Remove dev callout on yard page once roster is live in Cascade data JS.
