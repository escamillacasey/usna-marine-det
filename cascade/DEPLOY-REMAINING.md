# Remaining Cascade deploys (site scrub — Jul 2026)

Live audit vs repo. Most public pages are current; these three pastes fix **404 leadership links** and a **broken Marine directory** on Marines on the Yard.

**Already live (no action):** Home, Midshipmen hub, Prospective Marines, Summer Training, MARDET hub, Company mentors, Ground/Aviation/Support roles, `local.css` (galleries + commissioning path).

---

## Deployment order

### Step 1 — Fleet Assignments (fixes 404 links)

| Item | Value |
|------|--------|
| **Paste file** | `cascade/paste-fleet-application-marinecorps.html` |
| **Cascade path** | `Fleet_Marines.php` (site root) |
| **Mode** | HTML / source only |
| **JS** | None |

**What this fixes:**
- Replaces broken `https://www.usna.edu/MarineCorps/leadership.php` (404) with `MARDET/leadership.php`
- Swaps old `page-header` for `marines-page-header`

**Smoke test after publish:**
- Open [Fleet Assignments](https://www.usna.edu/MarineCorps/Fleet_Marines.php)
- Click **detachment leadership** in FAQ → should land on `MARDET/leadership.php`

---

### Step 2 — Marines on the Yard (fixes directory + links)

| Item | Value |
|------|--------|
| **Paste file** | `cascade/paste-intranet-marines-on-the-yard-marinecorps.html` |
| **Cascade path** | `MARDET/marines_on_the_yard.php` |
| **Mode** | HTML / source only |
| **JS metadata** | `cascade/snippets/foot-marines-on-the-yard.html` |

**Paste workflow:**
1. Open page → **source/HTML mode**
2. Replace body with full paste file contents
3. Open **Page Metadata → JavaScript**
4. Paste contents of `cascade/snippets/foot-marines-on-the-yard.html`
5. **Publish**

**What this fixes:**
- Adds `<div id="yard-directory">` so the roster JS can render
- Replaces broken root `leadership.php` links with full `MARDET/leadership.php` URLs
- Keeps community cards + quick-reference table in sync with repo

**Prerequisites (should already be on live):**
- `_files/js/intranet/company-mentors-data.js` → 200
- `_files/js/intranet/marines-on-the-yard-data.js` → 200
- `_files/js/marines-on-the-yard.js` → 200

**Smoke test after publish:**
- [Marines on the Yard](https://www.usna.edu/MarineCorps/MARDET/marines_on_the_yard.php) shows **Marine directory** section with roster groups
- **Detachment leadership** links → `MARDET/leadership.php` (not 404)
- Browser console: no red errors on load

---

### Step 3 — Detachment Leadership (optional polish)

| Item | Value |
|------|--------|
| **Paste file** | `cascade/paste-leadership-marinecorps.html` |
| **Cascade path** | `MARDET/leadership.php` |
| **Mode** | HTML / source only |
| **JS** | None |

**What this fixes:**
- `marines-page-header` + breadcrumb back to MARDET hub (cosmetic; bios/images already correct)

**Smoke test:** Reid and Giraldi photos load from `assets/images/public/leadership/`

---

### Step 4 — Cascade navigation (admin, not a paste)

| Issue | Doc |
|-------|-----|
| Left nav **Home** still points at archived `indexOldOld.php` | `cascade/FIX-NAV.md` |

Republish interior pages after fixing site index so nav HTML refreshes.

---

## Do not re-paste (already current)

- `paste-prospective-marines-marinecorps.html`
- `paste-summer-training-marinecorps.html`
- `paste-intranet-company-mentors-marinecorps.html`
- `paste-roles-ground-marinecorps.html`
- `paste-roles-aviation-marinecorps.html`
- `paste-roles-support-marinecorps.html`

## CSS

No new CSS append needed unless you add components not already on live `MarineCorps/_files/css/local.css`.

---

## Intentionally deferred

- **Marine Cyber** hub card — static “coming in a future update”
- **Hero/content images** — `assets/images/public/content/` not wired into page heroes yet
