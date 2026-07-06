# Image assets

Placeholder SVGs are included for local development. Official images can be pulled from the live site with:

```bash
python3 scripts/scrape-live-images.py
```

That downloads **65 content images** into `scraped/` (mirroring the live paths), copies key files to canonical names in this folder, and regenerates **`IMAGE-GAPS.md`** — use that file to see what's still missing.

## Gap report

See **`IMAGE-GAPS.md`** for a checklist of every image the new site needs vs. what is on disk.

## Mapping from live sites

| Local filename | Source (usna.edu) | Used on |
|----------------|-------------------|---------|
| `hero-masthead.jpg` | `Marines/_files/USNAMARINES.JPG` | Homepage hero |
| `mardet-logo.jpg` | `Marines/_files/images/MardetLogo.jpg` | Leadership strip |
| `trident-logo.png` | `Marines/_files/images/OFFICIAL_trident-Flat-Blue-Gold-01.png` | Leadership strip |
| `prospective-marines.jpg` | `Marines/_files/rsz_2prospective_marines.jpg` | Card grid |
| `summer-training.jpg` | `Marines/_files/SummerTrainingResize2.jpg` | Card grid |
| `marine-mentors.jpg` | `Marines/_files/MarineMentorsResize2.jpg` | Card grid |
| `marine-officers.jpg` | `Marines/_files/rsz_graded.jpg` | Card grid |
| `marine-aviation.jpg` | `Marines/_files/images/MarineAviationF35.jpg` | Card grid |
| `marine-cyber.png` | `Marines/_files/MarineCyber.png` | Card grid |
| `hero-marinecorps.jpg` | `MarineCorps/_files/images/mastheads/hero1.jpg` | Optional alt hero |
| `tank.jpg` | `MarineCorps/_files/images/tank.jpg` | Tools section |
| `jump.jpg` | `MarineCorps/_files/images/jump.jpg` | Battle section |
| `ground-combat.jpg` | `MarineCorps/_files/images/groundCombat.jpg` | Roles |
| `aviation-combat.jpg` | `MarineCorps/_files/images/aviationCombat.jpg` | Roles |
| `combat-support.jpg` | `MarineCorps/_files/images/combatSupport.jpg` | Roles |

| `col-reid.jpg` | `USMC/_files/images/Col_Reid,_5x72.jpg` | Leadership page |
| `ltcol-giraldi.jpg` | `USMC/_files/Giraldi_Tom.jpg` | Leadership page |
