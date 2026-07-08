# MARDET data (Google Sheets → website)

Your workbook has two layers:

| Source | Purpose | Synced to website? |
|--------|---------|-------------------|
| **POA&M** (predecessor) | Internal ops, milestones, tracking | **No** — stays in the sheet |
| **MARDET Marines tab** (Ops workbook) | Roster, billets, communities, contacts | **Yes** — curated public data |
| **POA&M / other tabs** | Internal ops, events, tasks | **No** — stays in the workbook |

Place `MARDET_Ops_Master_Working_2026.xlsx` in `data/` (gitignored). Sync exports the **MARDET Marines** tab to `data/marines.csv` automatically if the CSV is missing.

## Phase 1 — Export from Ops workbook

**Option A — drop the workbook (easiest)**

1. Save/download the workbook as `data/MARDET_Ops_Master_Working_2026.xlsx`
2. Run sync — it exports **MARDET Marines** → `data/marines.csv` and generates JS:

```bash
cd /Users/hellbentactual/Coding/usna-marine-det
python3 scripts/sync-from-sheets.py
```

**Option B — CSV only**

Export the **MARDET Marines** tab → `data/marines.csv`, then run sync as above.

## Marines tab → website mapping

The sync script recognizes flexible column names (case-insensitive). Your **MARDET Marines** tab maps like this:

| Concept | Column in Ops workbook |
|---------|------------------------|
| Rank | `Rank` |
| Name | `LName/FName/MI` |
| Billet | `Billet / Primary Duty` |
| Department | `Cost / Staff Center` |
| Email / Phone | `Email`, `Phone` |
| Company (mentors) | `Company Mentor` — number 1–36 |
| Collateral / clubs | `Collateral Duty '26`, `O/E Rep` → notes when public |

Community groups are **inferred** from department, billet, mentor assignment, and O/E Rep when no explicit `Community` column exists. Rows marked `(DEPARTED)` in billet are excluded.

## What gets generated

| Output | Used on |
|--------|---------|
| `js/intranet/marines-on-the-yard-data.js` | Marines on the Yard directory (by community) — **intranet only** |
| `js/intranet/company-mentors-data.js` | Company Mentors page — **intranet only** |

## Company mentor assignments

**Source of truth:** `data/company-mentor-list.csv` — the **Company Mentor List** with AY26/AY27 columns.

Sync matches AY27 mentor names to the MARDET Marines roster for rank, email, and billet. All **36 companies** get a card even when the `Company Mentor` column in the ops sheet is blank (e.g. Reading, Swartz, Flynn, Hartmann).

Set `MENTOR_ACADEMIC_YEAR=ay26` in `scripts/config.env` to use AY26 assignments instead.

Optional legacy export: `data/company-mentors.csv` if you prefer full rows per mentor instead of the assignment list.

## POA&M columns

Keep POA&M-only fields in the sheet — they are ignored by sync unless you later add mappings. Do not put POA&M internal notes in columns mapped to `notes` / `Public Notes` unless they should appear on the website.

## Phase 2 — Live Google Sheets

See `scripts/config.example.env` — set `SHEET_TAB_MARINES=Marines`.

## Sample header row

See `marines.csv.example` for a starter template. Your real export can have extra columns; sync ignores unmapped fields.
