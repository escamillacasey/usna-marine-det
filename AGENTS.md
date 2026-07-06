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

## Primary audiences (in priority order)

1. **Midshipmen** — exploring or pursuing a Marine Corps commission → `pages/midshipmen/index.html`
2. **MARDET Team** — Marines assigned to the detachment → `pages/mardet/index.html`
3. **Fleet Marines** — applying for a USNA billet → `pages/fleet-application.html`
4. **Faculty/Staff POCs** (secondary) — need a contact → `pages/leadership.html` (linked subtly from homepage)

## Site map

| Page | Audience | Path |
|------|----------|------|
| Home (audience gateway) | All | `index.html` |
| Midshipmen hub | Midshipmen | `pages/midshipmen/index.html` |
| MARDET Team hub | Det members | `pages/mardet/index.html` |
| Fleet Assignments | Fleet applicants | `pages/fleet-application.html` |
| Leadership | MARDET + POCs | `pages/leadership.html` |
| Prospective Marines | Midshipmen | `pages/prospective-marines.html` |
| Summer Training | Midshipmen | `pages/summer-training.html` |
| Marines on the Yard | Midshipmen | `pages/marines-on-the-yard.html` |
| Company Mentors | Midshipmen + MARDET | `pages/marine-company-mentors.html` |
| Roles (ground / aviation / support) | Midshipmen | `pages/roles/` |
| Marine Cyber | Midshipmen | `pages/marine-cyber.html` — **outdated; full revamp required for 2027 cycle before publish** |

## Navigation (top-level only — 5 items)

Home · Midshipmen · MARDET Team · Fleet Assignments · Leadership

Sub-pages are reached through hub pages, not the main nav. Keeps navigation scannable.

## Homepage rules

The homepage is a **router**, not a content dump. It contains:
- Compact hero + one-line mission
- Three audience gateway cards
- Brief about-the-detachment (2 sentences max)
- POC strip for faculty/staff
- Social links

Do **not** put generic USMC recruiting copy, roles grids, mission/benefits blocks, or image-card grids on the homepage — that content belongs under the Midshipmen path.

## Data source (Google Sheets / AppSheet)

Operational data lives in Google Sheets (AppSheet backend). Workflow:

1. **POA&M** tab — internal ops; not synced to the public site
2. **Marines** tab — export to `data/marines.csv` → run `python3 scripts/sync-from-sheets.py`
3. Sync generates `js/marines-on-the-yard-data.js` and mentor data when applicable

See `data/README.md` for column mapping. When the user exports their Marines sheet, run sync and update pages from the generated JS.

## When editing

Preserve consistency with existing patterns. Recommend usability, accessibility, and maintainability improvements proactively.
