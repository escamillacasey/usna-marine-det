# Image layout — public vs intranet

```
assets/images/
├── shared/                 # Both audiences (site chrome)
├── public/                 # www / MarineCorps open internet
│   ├── leadership/         # Col Reid, LtCol Giraldi only
│   └── content/            # Heroes, roles, prospective, social icons
├── intranet/               # USNA internal only — never GitHub Pages
│   ├── mentors/            # company-01.jpg … company-36.jpg
│   ├── staff/              # OpsO, Adjutant, SNCO, etc.
│   └── marine-mentors.jpg  # Legacy hub art (intranet context)
├── incoming/               # Photo drop zone (gitignored)
└── scraped/                # Live-site reference downloads
```

## Public (`assets/images/public/`)

Deploy to **MarineCorps** Cascade `_files/images/public/` (mirror folder structure).

| Folder | Files | Used on |
|--------|-------|---------|
| `leadership/` | `col-reid.jpg`, `ltcol-giraldi.jpg` | Public leadership page only |
| `content/` | heroes, roles, prospective, summer, social, logos | Subpages as you wire images in |

**Not public:** mentor headshots, MARDET staff photos (OpsO, Adj, Prieto, etc.), roster imagery.

## Intranet (`assets/images/intranet/`)

Deploy to **intranet** Cascade only — separate site/folder from open internet.

| Folder | Files | Used on |
|--------|-------|---------|
| `mentors/` | `company-NN.jpg` | Company mentors page |
| `staff/` | `staff-*.jpg` | MARDET hub key contacts, yard directory |

## Shared (`assets/images/shared/`)

| File | Used on |
|------|---------|
| `eagle-globe-anchor.svg` | Header logo (all pages, local preview) |

## Cascade upload cheat sheet

| Repo path | Public MarineCorps assets |
|-----------|---------------------------|
| `public/leadership/*.jpg` | `_files/images/public/leadership/` |
| `public/content/*` | `_files/images/public/content/` |
| `shared/*` | `_files/images/shared/` |

| Repo path | Intranet assets |
|-----------|-----------------|
| `intranet/mentors/*` | `_files/images/intranet/mentors/` |
| `intranet/staff/*` | `_files/images/intranet/staff/` |

After `import-photos.py` or `sync-from-sheets.py`, re-upload changed files to the matching Cascade folder.

## Scripts

- `scripts/import-photos.py` — routes incoming photos to `intranet/mentors`, `intranet/staff`, or `public/leadership`
- `scripts/sync-from-sheets.py` — mentor JS photo paths point at `intranet/mentors/`
- `scripts/build-public-site.sh` — excludes entire `assets/images/intranet/`

See also: `docs/PUBLISH-SPLIT.md`, `assets/images/IMAGE-GAPS.md`
