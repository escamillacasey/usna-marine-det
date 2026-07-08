# USNA Marine Detachment Website

Local development for the USNA Marine Detachment site modernization. Content merges the current [USNA Marines](https://www.usna.edu/Marines) and [Marine Corps](https://www.usna.edu/MarineCorps) sites into a single, maintainable static site for Cascade CMS.

**Public vs intranet:** Detachment leadership is public; company mentors, roster, and collateral duties are **intranet only**. See `docs/PUBLISH-SPLIT.md`. GitHub Pages deploys the public subset via `scripts/build-public-site.sh`.

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
│   ├── intranet/           # MARDET hub (not public deploy)
│   ├── fleet-application.html
│   ├── leadership.html
│   └── …                   # Topic pages linked from hubs
├── css/
├── js/
└── assets/images/
    ├── shared/             # Site chrome (header logo)
    ├── public/
    │   ├── leadership/     # Public leadership headshots
    │   └── content/        # Heroes, roles, prospective art
    └── intranet/
        ├── mentors/        # Company mentor headshots
        └── staff/          # MARDET staff photos
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
3. Commit mentor data and add photos to `assets/images/intranet/mentors/company-XX.jpg`.

See `assets/images/intranet/mentors/README.md` for photo naming.

## Cascade CMS workflow

1. Develop and preview locally (`python3 -m http.server` from repo root)
2. Build the Cascade CSS bundle: `bash scripts/build-cascade-bundle.sh` → upload `cascade/marines.css` (do **not** use `css/main.css` — `@import` breaks in Cascade)
3. Upload `js/` and images under your site asset folder (see `cascade/README.md`)
4. Copy only the HTML between `<!-- CASCADE: page content start -->` and `<!-- CASCADE: page content end -->` into the page editor
5. Wire CSS/JS on the Format or page metadata using snippets in `cascade/snippets/` — full guide: **`docs/CASCADE-WIRING.md`**

## Images

Placeholder blocks are used until official assets are added. Replace files in `assets/images/` using the mapping in `assets/images/README.md`.
