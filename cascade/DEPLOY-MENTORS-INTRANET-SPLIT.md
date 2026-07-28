# Company mentors — intranet only (`intranet.usna.edu/USMC/`)

**Captured model (Jul 2026):** Full roster on **`company_mentors.php`** on the intranet site only.

| Page | Paste file | Host |
|------|------------|------|
| **`company_mentors.php`** | `paste-intranet-company-mentors-marinecorps.html` | **intranet.usna.edu/USMC/** |

**Live path (Jul 2026):** `https://intranet.usna.edu/USMC/company_mentors.php` (USMC site root — not `Midshipmen/`).

Paste includes an embedded **`<style>`** block for mentor cards. USNA Standard 3.0 loads **`intranet.usna.edu/_files/css/local.css`** (intranet root), not `USMC/_files/css/local.css` — editing the wrong `local.css` will not style this page.

Public `www` no longer hosts the roster. Optional public stub: `paste-public-company-mentors-marinecorps.html` (overview only, no PII).

**Read first:** `SITE-STRUCTURE.md`, `cascade/site-urls.json`

---

## Legacy two-page split (www + SSO)

Previously: public overview at `company_mentors.php` + gated roster at `company_mentor_assignments.php` on **www**. Superseded by intranet-only roster on `company_mentors.php`.

<details>
<summary>Legacy deploy steps (www same-host SSO)</summary>

| Page | Paste file | Audience |
|------|------------|----------|
| **`Midshipmen/company_mentors.php`** | `paste-public-company-mentors-marinecorps.html` | **Public** — what a company Marine mentor is |
| **`Midshipmen/company_mentor_assignments.php`** | `paste-intranet-company-mentors-marinecorps.html` | **Gated** — full 36-card roster |

</details>

---

## Deploy (intranet)

### 1. Regenerate paste

```bash
bash scripts/build-intranet-mentors-paste.sh
```

### 2. Publish on intranet Cascade

1. Open **`company_mentors.php`** on **intranet.usna.edu/USMC/**
2. **Source/HTML mode** → paste **`paste-intranet-company-mentors-marinecorps.html`** (includes embedded mentor card CSS)
3. **Include in Navigation** → Yes (display name: **Company Mentors**)
4. Upload photos → `USMC/_files/images/mentors/company-*.jpg`
5. **Publish**

### Relative links in paste (no edit needed)

| Link in paste | Resolves to |
|---------------|-------------|
| `../_files/css/local.css` | Site CSS |
| `assets/images/public/mentors/company-NN.jpg` | Mentor photos |
| `prospective-marines.php` | Same folder (`Midshipmen/`) |
| `summer-training.php` | Same folder |
| `../MARDET/leadership.php` | MARDET leadership |
| `#battalion-N` | In-page jump |

### Smoke test (intranet)

- [ ] 36 `.mentor-card` elements in page source
- [ ] Photos → 200, `Content-Type: image/jpeg`
- [ ] Click **Summer Training** → stays on `intranet.usna.edu/USMC/…`
- [ ] No `mailto:` on public www copy (if public stub remains)

---

## AY rollover

1. `python3 scripts/sync-from-sheets.py`
2. `bash scripts/build-intranet-mentors-paste.sh`
3. Re-paste **`Midshipmen/company_mentors.php`** on intranet only

---

## Nav troubleshooting

| Symptom | Fix |
|---------|-----|
| Company Mentors missing from nav | `company_mentors.php` → Include in Navigation **Yes** |
| Photos broken | Confirm `assets/images/public/mentors/` uploaded on intranet site |
| Links jump to www | Re-paste — paste must use relative hrefs, not `https://www.usna.edu/…` |
| Cards unstyled (stacked list, huge photos) | Re-paste latest paste file — it embeds `<style>` for `.mentor-grid` / `.mentor-card`. Do not rely on `USMC/_files/css/local.css` alone. |
| Edited wrong CSS file | Template loads **`intranet.usna.edu/_files/css/local.css`** (root). Optional upload: `cascade/marines-mentors.css` → `USMC/_files/css/marines-mentors.css`. |

