# Live URL map — Marine Corps - Public

Use these in paste files and when fixing Cascade navigation. Base: `https://www.usna.edu/MarineCorps/`

| Page | Cascade output | Notes |
|------|----------------|-------|
| Home | `index.php` | **Not** `indexOldOld.php`, `working.php` |
| Midshipmen hub | `Midshipmen/index.php` | Capital **M** |
| Prospective Marines | `Midshipmen/prospective-marines.php` | Under Midshipmen folder |
| Summer Training | `Midshipmen/summer-training.php` | Under Midshipmen folder |
| Fleet Assignments | `Fleet_Marines.php` | **Not** `fleet-application.php` |
| MARDET hub | `MARDET/index.php` | Top-level nav + home audience card |
| Detachment Leadership | `MARDET/leadership.php` | **Only** under MARDET — not site root |
| Company mentors | `MARDET/company_mentors.php` | Underscore, not hyphen |
| Marines on the Yard | `MARDET/marines_on_the_yard.php` | Underscore, not hyphen |
| Roles hub | `Midshipmen/roles/index.php` | Two levels under Midshipmen |
| Roles aviation | `Midshipmen/roles/aviation.php` | |
| Roles support | `Midshipmen/roles/support.php` | |

**Retired:** `leadership.php` at site root (404) — use `MARDET/leadership.php`.

## MARDET quick links (use in paste hub)

From `MARDET/index.php` body, link to sibling pages with relative paths:

| Label | URL (from `MARDET/`) |
|-------|----------------------|
| Detachment Leadership | `leadership.php` |
| Company Mentors | `company_mentors.php` |
| Marines on the Yard | `marines_on_the_yard.php` |
| Midshipmen Resources | `https://www.usna.edu/MarineCorps/Midshipmen/index.php` |
| Fleet Assignment Info | `https://www.usna.edu/MarineCorps/Fleet_Marines.php` |

**Not:** `company-mentors.php`, `marines-on-the-yard.php`, `fleet-application.php`, or lowercase `midshipmen/`.

## Public page linking rules

- **Home / Midshipmen:** link to `MARDET/index.php` for detachment-wide needs — not directly to leadership.
- **Fleet Assignments:** may link to `MARDET/leadership.php` for Chief of Staff contact (under MARDET).
- **MARDET pages:** use relative `leadership.php` for leadership.

## Images on this site

Published photos resolve under **`assets/images/public/…`** (not `_files/images/…`).

Examples:
- `../assets/images/public/leadership/col-reid.jpg` (from `MARDET/leadership.php`)
- `../assets/images/public/mentors/company-02.jpg` (from `MARDET/` pages)
- `../../assets/images/public/roles/ground/infantry.jpg` (from `Midshipmen/roles/`)
