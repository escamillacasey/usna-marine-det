# Agent instructions — USNA Marine Detachment site

Act as a senior front-end developer and technical advisor for this project.

## Always follow

- HTML5, CSS3, vanilla JS only — no SPA frameworks
- Cascade CMS compatibility: static, paste-in ready, minimal dependencies
- **No attachments or downloads** — convert PDF, Word, and other document content into inline HTML on the page; do not link to downloadable bio files
- **Audience-first information architecture** — organize content by who is visiting, not by legacy site structure
- Semantic HTML, responsive-first, accessible (WCAG-minded)
- Reusable components in `css/components.css` and consistent class naming (BEM-style)
- Complete, working code — not partial snippets
- Brief explanations of major design decisions
- **Avoid duplicate content** — each fact lives in one place; hub pages link outward, they don't repeat body copy

## Public vs intranet (critical)

See `docs/PUBLISH-SPLIT.md`. **Never publish intranet content to the open internet.**

| Tier | Who | MARDET people data |
|------|-----|-------------------|
| **Public** | Internet, GitHub Pages, www.usna.edu | **Leadership only** (`pages/leadership.html` — Senior Marine, Chief of Staff) |
| **Intranet** | USNA internal | MARDET hub, company mentors, roster, collateral duties, OpsO/Adj contacts |

Public pages must **not** link to `pages/intranet/`, roster JS, or mentor headshots. Direct midshipmen to their company mentor in Bancroft Hall or to detachment leadership.

GitHub Pages deploy uses `scripts/build-public-site.sh` (excludes intranet paths).

## Primary audiences (in priority order)

1. **Midshipmen** — exploring or pursuing a Marine Corps commission → `pages/midshipmen/index.html` (public)
2. **MARDET Team** — Marines assigned to the detachment → `pages/intranet/index.html` (**intranet only**)
3. **Fleet Marines** — applying for a USNA billet → `pages/fleet-application.html` (public)
4. **Faculty/Staff POCs** (secondary) — need a contact → `pages/leadership.html` (public)

## Site map

### Public

| Page | Path |
|------|------|
| Home (audience gateway) | `index.html` |
| Midshipmen hub | `pages/midshipmen/index.html` |
| Fleet Assignments | `pages/fleet-application.html` |
| Leadership | `pages/leadership.html` |
| Prospective Marines | `pages/prospective-marines.html` |
| Summer Training | `pages/summer-training.html` |
| Roles (ground / aviation / support) | `pages/roles/` |

### Intranet only

| Page | Path |
|------|------|
| MARDET Team hub | `pages/intranet/index.html` |
| Company Mentors | `pages/intranet/company-mentors.html` |
| Marines on the Yard | `pages/intranet/marines-on-the-yard.html` |
| Roster data | `js/intranet/*.js` |
| Mentor photos | `assets/images/intranet/mentors/` |
| Public leadership photos | `assets/images/public/leadership/` |
| MARDET staff photos (intranet) | `assets/images/intranet/staff/` |

## Navigation (top-level — public: 4 items)

Home · Midshipmen · Fleet Assignments · Leadership

Intranet pages add **MARDET Team** to nav. Sub-pages are reached through hub pages, not the main nav.

## Homepage rules

The homepage is a **router**, not a content dump. It contains:
- Compact hero + one-line mission
- Audience gateway cards (Midshipmen, Fleet, Leadership — **not** MARDET Team)
- Brief about-the-detachment (2 sentences max)
- POC strip for faculty/staff
- Social links

Do **not** put generic USMC recruiting copy, roles grids, mission/benefits blocks, or image-card grids on the homepage — that content belongs under the Midshipmen path.

## Data source (Google Sheets / AppSheet)

Operational data lives in Google Sheets (AppSheet backend). Workflow:

1. **POA&M** tab — internal ops; not synced to the public site
2. **Marines** tab — export to `data/marines.csv` → run `python3 scripts/sync-from-sheets.py`
3. Sync generates `js/intranet/marines-on-the-yard-data.js` and `js/intranet/company-mentors-data.js` (**intranet only**)

See `data/README.md` for column mapping.

## Messaging and commander's intent

- The **annual campaign order is internal only** — never link to it, attach it, or paste it on the public site.
- Public copy should reflect CO intent and priority themes using `docs/MESSAGING-GUIDE.md` (approved phrases + page mapping).
- Source material lives in gitignored `docs/internal/campaign-order-source.*` — see `docs/internal/README.md`.
- On a messaging pass: update the guide's approved phrases first, then edit the HTML snippets listed in the mapping table. Keep the homepage a router (tagline + two about sentences, not LOE lists).

## When editing

Preserve consistency with existing patterns. Recommend usability, accessibility, and maintainability improvements proactively.
