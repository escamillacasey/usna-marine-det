# USNA Marine Detachment Website

Local development for the USNA Marine Detachment site modernization. Content merges the current [USNA Marines](https://www.usna.edu/Marines) and [Marine Corps](https://www.usna.edu/MarineCorps) sites into a single, maintainable static site for Cascade CMS.

## Quick start

Open `index.html` in a browser, or serve locally:

```bash
cd ~/Coding/usna-marine-det
python3 -m http.server 8080
```

Then visit http://localhost:8080

## GitHub

This project is tracked in Git and published to **GitHub Pages** on push to `main`.

| | |
|---|---|
| **Repository** | Create/link at `github.com/<you>/usna-marine-det` |
| **Live preview** | `https://<you>.github.io/usna-marine-det/` (after Pages is enabled) |

### First-time setup (if not already linked)

```bash
cd ~/Coding/usna-marine-det
gh auth login
gh repo create usna-marine-det --source=. --public --push
```

In the repo on GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

### Day-to-day workflow

```bash
git add -A
git commit -m "Describe your change"
git push
```

Pages redeploys automatically via `.github/workflows/pages.yml`.

### Data sync (mentor roster)

```bash
python3 scripts/sync-from-sheets.py
git add js/company-mentors-data.js js/marines-on-the-yard-data.js
git commit -m "Sync mentor roster from Ops workbook"
git push
```

Ops workbook and full roster CSV stay local (gitignored). `data/company-mentor-list.csv` is committed as the public assignment source.

## Structure

```
├── index.html              # Audience gateway (not a content dump)
├── pages/
│   ├── midshipmen/         # Hub for midshipman resources
│   ├── mardet/             # Hub for detachment members
│   ├── fleet-application.html
│   ├── leadership.html
│   └── …                   # Topic pages linked from hubs
├── css/
├── js/
└── assets/images/
```

## Audiences

The site is organized around three primary users:

1. **Midshipmen** — Marine option, training, mentors, roles
2. **MARDET Team** — detachment members and internal resources
3. **Fleet Marines** — applying for USNA billets

Faculty/staff looking for a POC → Leadership page.

## Updating company mentors

1. Update `data/company-mentor-list.csv` and/or export from the Ops workbook (see `data/README.md`).
2. Run `python3 scripts/sync-from-sheets.py`.
3. Commit the generated `js/company-mentors-data.js` and add photos to `assets/images/mentors/company-XX.jpg`.

See `assets/images/mentors/README.md` for photo naming.

## Cascade CMS workflow

1. Develop and preview locally
2. Copy the content between `<!-- CASCADE: page content start -->` and `<!-- CASCADE: page content end -->`
3. Paste into the Cascade page editor
4. Link CSS/JS via Cascade asset blocks or inline as required by your template

## Images

Placeholder blocks are used until official assets are added. Replace files in `assets/images/` using the mapping in `assets/images/README.md`.
