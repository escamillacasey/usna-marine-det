# Company mentors — intranet only (`intranet.usna.edu/USMC/`)

**Captured model (Jul 2026):** Full roster on **`Midshipmen/company_mentors.php`** on the intranet site only. Paste uses **relative links** so navigation stays on `intranet.usna.edu/USMC/`.

| Page | Paste file | Host |
|------|------------|------|
| **`Midshipmen/company_mentors.php`** | `paste-intranet-company-mentors-marinecorps.html` | **intranet.usna.edu/USMC/** |

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

1. Open **`Midshipmen/company_mentors.php`** on **intranet.usna.edu/USMC/**
2. **Source/HTML mode** → paste **`paste-intranet-company-mentors-marinecorps.html`**
3. **Include in Navigation** → Yes (display name: **Company Mentors**)
4. Upload photos → `assets/images/public/mentors/company-*.jpg`
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

