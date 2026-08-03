# Live URL map — `usna.edu/MarineCorps`

Use these in paste files and when fixing Cascade navigation.

| | URL |
|---|-----|
| **Production base (active)** | `https://www.usna.edu/MarineCorps/` |
| **Future cutover** | `https://www.usna.edu/Marines/` |
| **Intranet base** | `https://intranet.usna.edu/USMC/` |
| **Config source** | `cascade/site-urls.json` |
| **Migration plan** | `cascade/MIGRATE-TO-MARINES.md` |

Regenerate paste URLs after path changes:

```bash
python3 scripts/apply-site-urls.py          # active: Marines/ → MarineCorps/
python3 scripts/apply-site-urls.py --migrate  # cutover: MarineCorps/ → Marines/
```

---

## Page map

| Page | Cascade path | Audience |
|------|----------------|----------|
| Home | `index.php` | Public |
| Midshipmen hub | `Midshipmen/index.php` | Public |
| Prospective Marines | `Midshipmen/prospective-marines.php` | Public |
| Summer Training | `Midshipmen/summer-training.php` | Public |
| Fleet Assignments | `Fleet_Marines.php` | Public |
| MARDET hub | `MARDET/index.php` | Gated |
| Detachment Leadership | `MARDET/leadership.php` | Public |
| Company mentors (roster) | `company_mentors.php` on **intranet.usna.edu/USMC/** | Intranet only |
| Marines on the Yard | `MARDET/marines_on_the_yard.php` | **Coming soon** — use `paste-public-marines-on-the-yard-coming-soon-marinecorps.html` |
| Roles hub | `Midshipmen/roles/index.php` | Public |
| Roles aviation | `Midshipmen/roles/aviation.php` | Public |
| Roles support | `Midshipmen/roles/support.php` | Public |

**Retired:** `MarineCorps/leadership.php` at site root (404) — use `MARDET/leadership.php`.

---

## MARDET quick links (use in paste hub)

From `MARDET/index.php` body:

| Label | URL |
|-------|-----|
| Detachment Leadership | `https://www.usna.edu/MarineCorps/MARDET/leadership.php` |
| Company Mentors | `https://intranet.usna.edu/USMC/company_mentors.php` |
| Marines on the Yard | `https://www.usna.edu/MarineCorps/MARDET/marines_on_the_yard.php` |
| Midshipmen Resources | `https://www.usna.edu/MarineCorps/Midshipmen/index.php` |
| Fleet Assignment Info | `https://www.usna.edu/MarineCorps/Fleet_Marines.php` |

**Not:** `company-mentors.php`, `marines-on-the-yard.php`, `fleet-application.php`, or lowercase `midshipmen/`.

---

## Public www vs intranet

| Host | Cascade root | Audience |
|------|--------------|----------|
| `www.usna.edu/MarineCorps/` | Active public site | Open internet |
| `intranet.usna.edu/USMC/` | Separate Cascade site | USNA login |

Intranet pastes use **relative links** (resolve under `USMC/`). Public www pastes use `https://www.usna.edu/MarineCorps/…` until Marines cutover.

Update `cascade/site-urls.json` → `intranet_base` if the intranet slug changes.

---

## Public page linking rules

- **Home / Midshipmen:** link to `MARDET/index.php` for detachment-wide needs (gated — may prompt login).
- **Fleet Assignments:** may link to `MARDET/leadership.php` for Chief of Staff contact.
- **MARDET pages:** use relative `leadership.php` for leadership.
- **Do not** expose mentor emails or roster on **ungated** pages.

---

## Images on this site

Published photos resolve under **`assets/images/public/…`** or **`assets/images/intranet/…`** (gated).

Examples:
- `../assets/images/public/leadership/col-reid.jpg` (from `MARDET/leadership.php`)
- `assets/images/public/mentors/company-02.jpg` (from intranet `company_mentors.php`)
- `assets/images/public/roles/ground/infantry.jpg` (from `Midshipmen/roles/`)
