# Company mentors — public overview + gated roster (`Marines/`)

Two pages, same `Midshipmen/` folder — nav stays on the public overview.

| Page | Paste file | Audience |
|------|------------|----------|
| **`Midshipmen/company_mentors.php`** | `paste-public-company-mentors-marinecorps.html` | **Public** — what a company Marine mentor is |
| **`Midshipmen/company_mentor_assignments.php`** | `paste-intranet-company-mentors-marinecorps.html` | **Gated** — full 36-card roster |

**Read first:** `SITE-STRUCTURE.md`, `MIGRATE-TO-MARINES.md`

---

## Why two pages

- **Public** visitors (prospective students, parents, internet) learn the mentor program without PII.
- **Authenticated** mids and MARDET Marines get photos, email, duties, and battalion jump links.
- Left nav **Company Mentors** stays on `company_mentors.php` — do not move or rename.

`company_mentor_assignments.php` is linked from the overview, Midshipmen hub, MARDET hub, and MOTY. **Include in Navigation** on assignments is optional (omit from public nav if you prefer login-only discovery).

---

## Deploy

### 1. Public overview (`company_mentors.php`)

1. Paste `paste-public-company-mentors-marinecorps.html` (source mode).
2. **Configure:** Include in Navigation → **Yes**; Display name → **Company Mentors**.
3. **No** authentication on this page.
4. Publish.

### 2. Gated roster (`company_mentor_assignments.php`)

1. Create page at `Midshipmen/company_mentor_assignments.php` if missing.
2. Regenerate:
   ```bash
   CASCADE_PHOTO_PREFIX="assets/images/intranet/mentors/" \
     bash scripts/build-intranet-mentors-paste.sh
   ```
3. Paste `paste-intranet-company-mentors-marinecorps.html`.
4. Web Services: enable **authentication** on this page.
5. Upload `assets/images/intranet/mentors/`.
6. Publish.

### Smoke tests

| Page | Logged out | Logged in |
|------|------------|-----------|
| `company_mentors.php` | Program description, no `mailto:` | Same |
| `company_mentor_assignments.php` | Login wall | 36 cards, photos 200 |

---

## AY rollover

1. `python3 scripts/sync-from-sheets.py`
2. `CASCADE_PHOTO_PREFIX="assets/images/intranet/mentors/" bash scripts/build-intranet-mentors-paste.sh`
3. Re-paste **`company_mentor_assignments.php` only** — public overview unchanged unless copy edits

---

## Nav troubleshooting

| Symptom | Fix |
|---------|-----|
| Company Mentors missing from nav | `company_mentors.php` → Include in Navigation **Yes** |
| Roster visible when logged out | `company_mentor_assignments.php` not gated — escalate Web Services |
| 404 on assignments | Create `company_mentor_assignments.php` under `Midshipmen/` |
