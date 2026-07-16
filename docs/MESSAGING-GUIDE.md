# Site messaging guide

Public copy on this site should reflect **commander's intent** and detachment priorities without publishing the annual campaign plan (ACO) or operational taskings.

**Source of truth (internal):** `docs/internal/campaign-order-source.md` (from `Campaign Plan 2025-2026.pdf`, gitignored).  
**When the ACO updates:** revise the internal source, then update the page snippets in the table below.

---

## Principles

1. **Intent, not the order** — Echo themes, tone, and priority outcomes. Never reproduce taskings, timelines, internal-only initiatives, or quota pressure language.
2. **One canonical phrase per idea** — Pick one formulation for mission/tagline and reuse it site-wide (see Approved phrases).
3. **Audience-first** — Same intent, different emphasis:
   - **Midshipmen:** inform → influence → assess → select → equip; summer training; mentors; TBS readiness
   - **MARDET Team:** nest in USNA mission; engagement model; visible example on the Yard
   - **Fleet:** billets that extend inform/influence through summer training and mentorship
4. **Homepage stays a router** — Hero + two-sentence about block only; no LOE lists or event calendars (see `AGENTS.md`).
5. **All midshipmen** — Public copy reflects developing *all* mids regardless of service assignment intent (per CO).

---

## Approved phrases (aligned to AY 2025-2026 campaign plan)

| Role | Copy | Where used |
|------|------|------------|
| **Primary tagline** | Inform, influence, and develop midshipmen for service as Marine Corps officers. | `index.html` hero |
| **Engagement model (short)** | Shaping engagements inform, influence, and assess; decisive engagements select and equip. | Reference only — use plain language on public pages |
| **Detachment mission** | The detachment embodies the Naval Academy mission to develop midshipmen morally, mentally, and physically — attracting, identifying, screening, and selecting high-quality midshipmen for Marine Corps commissions. | `pages/intranet/index.html` (intranet) |
| **About (para 1)** | The Marine Detachment supports the Naval Academy mission to develop midshipmen morally, mentally, and physically. Marine cadre inform and influence all midshipmen on the Marine Corps — its mission, culture, and opportunities for service — regardless of commissioning intent. | `index.html` |
| **About (para 2)** | Through four years of engagement, the detachment assesses suitability, selects those best qualified to commission, and equips Marine-selects for success at The Basic School. | `index.html` |
| **Midshipmen hub subtitle** | Learn more about leading Marines, Summer Training Opportunities, and get connected with your Marine Mentor. | `paste-midshipmen-marinecorps.html`, home audience card |
| **Fleet card / page subtitle** | Apply for a USNA Billet and learn more about USNA as an Enlisted to Officer pathway. Requirements, billet types, deadlines and how to submit a package. | `paste-home-marinecorps.html`, `paste-fleet-application-marinecorps.html` |
| **Why Marines?** | Fight and win; character, judgment, warfighting mindset; earn the title Marine Officer. Second graf ties to Superintendent strategic vision (leaders of character, warfighters of consequence, leading sailors and Marines). | `paste-midshipmen-marinecorps.html` |

---

## Superintendent strategic vision (alignment)

**Source phrase:** *Developing leaders of character and warfighters of consequence — preparing the next generation of officers for the privilege of leading sailors and Marines.*

**Where reflected publicly:**
- **Why Marines?** (`paste-midshipmen-marinecorps.html`) — character, judgment, warfighting mindset; explicit alignment sentence in second paragraph
- **About the Detachment** (home) — morally, mentally, physically; developing midshipmen (nested in USNA mission)
- **Detachment mission** (MARDET hub) — morally, mentally, physically; high-quality commissions

**Alignment check:** Public copy emphasizes **character + warfighting + leading Marines/sailors** without quoting the Superintendent verbatim except in the Why Marines alignment graf. Do not dilute with generic recruiting language ("tip of the spear" removed AY27).

---

| Page | Audience | Snippet target | Location |
|------|----------|----------------|----------|
| Home | All | Hero lead + about (2 sentences max) | `index.html` |
| Midshipmen hub | Mids | Page subtitle + Why Marines? | `paste-midshipmen-marinecorps.html` |
| Prospective Marines | Mids | Intro under "Becoming a Marine at USNA" | `pages/prospective-marines.html` |
| Summer Training | Mids | Intro paragraph | `pages/summer-training.html` |
| Company Mentors | Mids + MARDET | First content paragraph | `pages/intranet/company-mentors.html` (intranet) |
| Marines on the Yard | Mids | **Deferred** — coming soon paste | `paste-public-marines-on-the-yard-coming-soon-marinecorps.html` |
| MARDET Team hub | MARDET | Mission section (2 paragraphs) | `pages/intranet/index.html` (intranet) |
| Leadership | All | Page subtitle | `pages/leadership.html` |
| Fleet Assignments | Fleet | Overview opening | `pages/fleet-application.html` |

**Do not add:** ACO PDFs, internal event calendars, MARSATs, SNCE criteria, or "read the campaign plan" links.

---

## Tone

- Direct, professional, institutional — not recruiting poster hype
- Active voice; engagement-model verbs (inform, influence, assess, select, equip) on detail pages; softer "develop" on the homepage hero
- Standards and selection are matter-of-fact, not punitive
- Emphasize proactive Marine presence and mentorship of all midshipmen

---

## Agent workflow

1. Read `docs/internal/campaign-order-source.md`.
2. Update **Approved phrases** in this file, then edit HTML snippets in the mapping table.
3. Diff-check tagline and mission language across home and MARDET hub.
4. Do not commit internal source files or OCR output.

---

## Status

**Last alignment pass:** AY 2025-2026 campaign plan ingested (22 Aug 2025). Public pages updated to reflect commander's intent and inform/influence/assess/select/equip model without publishing the order.
