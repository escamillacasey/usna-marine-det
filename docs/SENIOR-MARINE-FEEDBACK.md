# Senior Marine feedback — checklist & schedule

**Captured:** Friday, 17 July 2026, 12:43 PM (UTC-4)  
**Source:** Senior Marine walkthrough / review  
**Live site:** `https://www.usna.edu/MarineCorps/`  
**Tracking:** Update checkboxes here as items ship; link commits or paste deploy dates inline.

---

## Summary

| Phase | Focus | Target window | Owner notes |
|-------|--------|---------------|-------------|
| **A** | Copy-only fixes (no new assets) | Week of 17 Jul 2026 | Dev + paste deploy |
| **B** | Verbiage alignment (Service Assignment, TBS, summer training) | Week of 17 Jul 2026 | Sync `MESSAGING-GUIDE.md` after |
| **C** | Role content + MOS order (incl. MARSOC 0370) | 21–28 Jul 2026 | PAO input for MAGTF / battles language |
| **D** | Image swaps (roles, PROTRAMID, mentors) | 28 Jul – Aug 2026 | PAO / photo pipeline |
| **E** | Structural (roles regroup, mentors bios, visual divider) | Aug 2026 | Requires design + content decisions |

---

## Phase A — Quick copy (no assets)

### Home
- [ ] Remove “regardless of commissioning intent” (`paste-home-marinecorps.html`, `index.html`)

### Midshipmen index
- [ ] Reorder hub header/card emphasis (chronological for mids):
  1. Learn more about **summer training**
  2. **Marine Mentor**
  3. **Path to Commission**
  4. **Leading Marines**
- [ ] Replace **“Marine Option”** → **Marine Corps Service Assignment** (site-wide pass)
- [ ] Remove **“Signed in on the Yard?”** callout — intranet access is implicit; link to mentor assignments without that framing (`paste-midshipmen-marinecorps.html`)

### Leatherneck / summer training copy
- [ ] Remove **“Marine Option”** and **“Selection”** → **Service Assignment** references (Leatherneck section + related callouts)

### Prospective Marines
- [ ] Add eligibility line: **“To be eligible for service assignment to the Marine Corps, you must go to Leatherneck.”**
- [ ] **MAGTF:** correct duration — **4 weeks** (not 2); clarify **with an FMF unit**
- [ ] **PROTRAMID:** clarify **with an FMF unit** (parallel to MAGTF note)

### TBS (Prospective Marines)
- [ ] **29-week curriculum** (not “6 months”)
- [ ] Keep page in **second person** (addressed to the reader)
- [ ] Remove **“Points to consider”** section
- [ ] Add **TBS official logo** (asset needed — placeholder OK until file received)
- [ ] Add **banger bar** for key TBS points:
  - Every Marine Officer is a **provisional Rifle Platoon Commander**
  - Common training / grounding themes (draft with PAO if needed)

### Support roles (summary line only)
- [ ] Add to roles support summary: **“…and other functions that provide vital capabilities to MAGTF success on the battlefield.”**

---

## Phase B — Verbiage & messaging alignment

- [ ] Global find/replace plan: **Marine Option** → **Marine Corps Service Assignment** (public pages only; don’t break official USNA forms/links)
- [ ] Update `docs/MESSAGING-GUIDE.md` approved phrases after copy lands
- [ ] Run `python3 scripts/apply-site-urls.py` before Cascade paste if URLs touched
- [ ] Re-paste affected pages on `MarineCorps/` (see deploy table at bottom)

**Pages likely touched:** Home, Midshipmen index, Prospective Marines, Summer Training (Leatherneck block), Roles intros (battles vs wars).

---

## Phase C — Roles content (Ground, Aviation, Support)

### All roles / hub
- [ ] Change **wars** → **battles** (“The Marine Corps wins our Nation’s battles”)
- [ ] Amplify **Role of the Marine Corps** + **MAGTF integration** — **await PAO input**
- [ ] **Contemplate regrouping** layout: **Air (pilots only) | Ground | Cyber** vs current Ground / Aviation / Support — decision needed before refactor

### Ground Combat
- [ ] Add **MARSOC 0370**
- [ ] **Re-order entries by MOS number**
- [ ] Intro: explain **combined arms**
- [ ] **Artillery** — three images: HIMARS, Ship Killers, M777
- [ ] **Combat Engineer** — mobility + counter-mobility (short, compelling copy)
- [ ] **LAR** — remove 1st sentence; use: *Infantry officers who specialize in reconnaissance, security, offensive, and defensive operations…*
- [ ] **Recon** — better photo
- [ ] **ACV** — splashing-off-ship photo
- [ ] **LAAD** — confirm **combat arms** classification in copy/tags

### Aviation
- [ ] **0207** — better picture
- [ ] **7220** — officer photo + fix narrative
- [ ] **7315** — improve title/description (**MQ-9 pilot**)
- [ ] **UH-1Y** — fast-rope photo
- [ ] **CH-53** *(note: “CH-153” in feedback likely CH-53)* — sling-load photo
- [ ] **C-130** — new narrative: versatile intra-theater lift, mid-air refueling, transportation, insertion; **Hellfire** capability

### Support
- [ ] **Intel** — remove **MAGTF Intel Officer** entry
- [ ] Better images: **Ground Intel, HUMINT, Comm Officer, Logistics Officer, MP, Ground Supply, Financial Management**

---

## Phase D — Images & assets

| Asset | Page / role | Status |
|-------|-------------|--------|
| HIMARS / Ship Killer / M777 | Artillery | [ ] Incoming |
| Recon, ACV splash, LAAD confirm | Ground | [ ] Incoming |
| 0207, 7220 officer, 7315 MQ-9, UH-1Y fast rope, CH-53 sling load | Aviation | [ ] Incoming |
| Intel, HUMINT, Comm, Logistics, MP, Supply, Fin Mgmt | Support | [ ] Incoming |
| Gas chamber / PROTRAMID highlights | Summer Training | [ ] Incoming |
| TBS official logo | Prospective Marines | [ ] Incoming |

**Pipeline:** drop files in `assets/images/incoming/` → manifest/import → regenerate role pastes (`scripts/build-roles-pages.py`).

---

## Phase E — Structural / larger lifts

### Prospective Marines — visual design
- [ ] **Visual divider after commissioning path** (EGA motif?) — design mockup first
- [ ] TBS banger bar component (may need `local.css` append)

### Mentors
- [ ] Add **“Schedule a meeting”** link (standard URL pattern TBD — Calendly, USNA form, or mailto?)
- [ ] **Standardize bios** across 36 mentors (source: sheet sync + PAO?)
- [ ] Deploy mentor roster on **`intranet.usna.edu/USMC/Midshipmen/company_mentors.php`** (paste `paste-intranet-company-mentors-marinecorps.html`)

### Roles IA (future)
- [ ] Decision: regroup to **Air (pilots) | Ground | Cyber** — impacts nav, three paste files, and `Midshipmen/roles/` tree

---

## Suggested schedule

| Date | Milestone |
|------|-----------|
| **17 Jul 2026, 12:43 PM** | Feedback captured (this doc) |
| **17–18 Jul 2026** | Phase A copy edits in repo; paste Home, Midshipmen, Prospective, Summer Training (Leatherneck) |
| **21 Jul 2026** | PAO delivers MAGTF / battles / Role of the Marine Corps language |
| **22–24 Jul 2026** | Phase C ground + aviation + support copy (MOS order, MARSOC, TBS banger bar text) |
| **25 Jul 2026** | Regenerate + paste all three `paste-roles-*` files |
| **28 Jul – 1 Aug 2026** | Phase D image swaps as assets arrive |
| **Aug 2026** | Phase E: EGA divider, mentor meeting links + bios, roles regroup decision |

---

## Cascade re-paste checklist (after repo changes)

| Paste file | Cascade path | Triggered by |
|------------|--------------|--------------|
| `paste-home-marinecorps.html` | `index.php` | Home copy |
| `paste-midshipmen-marinecorps.html` | `Midshipmen/index.php` | Order, Service Assignment, remove Yard callout |
| `paste-prospective-marines-marinecorps.html` | `Midshipmen/prospective-marines.php` | Leatherneck eligibility, MAGTF, TBS, divider |
| `paste-summer-training-marinecorps.html` | `Midshipmen/summer-training.php` | Leatherneck verbiage, PROTRAMID photos |
| `paste-roles-ground-marinecorps.html` | `Midshipmen/roles/index.php` | Ground MOS content/images |
| `paste-roles-aviation-marinecorps.html` | `Midshipmen/roles/aviation.php` | Aviation content/images |
| `paste-roles-support-marinecorps.html` | `Midshipmen/roles/support.php` | Support content/images |
| `paste-public-company-mentors-marinecorps.html` | `Midshipmen/company_mentors.php` | Meeting link, bios |
| `paste-intranet-company-mentors-marinecorps.html` | `Midshipmen/company_mentors.php` on **intranet.usna.edu/USMC/** | Full roster |

---

## Open decisions (blockers)

1. **Roles regroup** — Air / Ground / Cyber vs current three-page model?
2. **PAO copy** — official MAGTF integration paragraph for roles hub?
3. **Mentor “schedule a meeting”** — single detachment link or per-mentor?
4. **CH-153 vs CH-53** — confirm aircraft for sling-load photo request.
5. **TBS logo** — file from TBS PAO / USMC brand?

---

## Related docs

- `docs/MESSAGING-GUIDE.md` — update after Service Assignment sweep
- `cascade/DEPLOY.md` — paste workflow
- `cascade/LIVE-URLS.md` — active `MarineCorps/` URLs
