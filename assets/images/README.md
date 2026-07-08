# Image assets

## Folder layout

**`IMAGE-SPLIT.md`** — public vs intranet inventory and Cascade upload paths.

```
shared/     → header logo (all pages)
public/     → open internet (leadership + content imagery)
intranet/   → mentors, MARDET staff (never public deploy)
incoming/   → photo drop (gitignored)
scraped/    → live-site reference downloads
```

## Gap report

**`IMAGE-GAPS.md`** — checklist of images needed vs. on disk.

## Import workflow

```bash
python3 scripts/import-photos.py
python3 scripts/scrape-live-images.py   # optional: pull from live site
```

- Mentors → `intranet/mentors/company-NN.jpg`
- MARDET staff → `intranet/staff/staff-{slug}.jpg`
- Public leadership → `public/leadership/col-reid.jpg`, `ltcol-giraldi.jpg`

## Public content mapping (in `public/content/`)

| Local filename | Source (usna.edu) | Used on |
|----------------|-------------------|---------|
| `hero-masthead.jpg` | `Marines/_files/USNAMARINES.JPG` | Homepage hero |
| `prospective-marines.jpg` | `Marines/_files/rsz_2prospective_marines.jpg` | Prospective |
| `summer-training.jpg` | `Marines/_files/SummerTrainingResize2.jpg` | Summer training |
| `ground-combat.jpg` | `MarineCorps/_files/images/groundCombat.jpg` | Roles |
| `aviation-combat.jpg` | `MarineCorps/_files/images/aviationCombat.jpg` | Roles |
| `combat-support.jpg` | `MarineCorps/_files/images/combatSupport.jpg` | Roles |
| `col-reid.jpg` | `public/leadership/` | Leadership page |
| `ltcol-giraldi.jpg` | `public/leadership/` | Leadership page |

Mentor headshots live under **`intranet/mentors/`** only.
