# Cascade paste-in assets

Generated and hand-maintained files for Hannon Hill Cascade CMS.

## Deploy next

**`cascade/DEPLOY.md`** — order and steps for publishing subpages after the homepage.

| Paste file | Cascade page |
|------------|----------------|
| `paste-home-marinecorps.html` | `working.php` (done) |
| `paste-leadership-marinecorps.html` | `leadership.php` |
| `paste-fleet-application-marinecorps.html` | `fleet-application.php` |
| `paste-midshipmen-marinecorps.html` | `midshipmen/index.php` |
| `paste-prospective-marines-marinecorps.html` | `prospective-marines.php` |
| `paste-summer-training-marinecorps.html` | `summer-training.php` |

### Intranet (USNA internal only)

See **`cascade/DEPLOY-INTRANET.md`**.

| Paste file | Cascade path (example) |
|------------|------------------------|
| `paste-intranet-mardet-marinecorps.html` | `mardet/index.php` |
| `paste-intranet-company-mentors-marinecorps.html` | `mardet/company-mentors.php` |
| `paste-intranet-marines-on-the-yard-marinecorps.html` | `mardet/marines-on-the-yard.php` |

## Other files

| File | Purpose |
|------|---------|
| `marines.css` | Single CSS bundle (run `scripts/build-cascade-bundle.sh` after editing `css/*.css`) |
| `snippets/` | Template/metadata snippets if you gain Configure access later |

Guides: **`docs/CASCADE-WIRING.md`**, **`docs/CASCADE-NO-DEFAULT-CSS.md`**
