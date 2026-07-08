#!/usr/bin/env python3
"""
Import Marine headshots from assets/images/incoming/ into site paths.

Drop photos with any filenames, or pass a zip:
  python3 scripts/import-photos.py
  python3 scripts/import-photos.py --zip ~/Downloads/mardet-photos.zip

Priority:
  1. Company mentor photos → assets/images/intranet/mentors/company-NN.jpg
  2. MARDET staff → assets/images/intranet/staff/staff-{slug}.jpg
  3. Public leadership → assets/images/public/leadership/col-reid.jpg, ltcol-giraldi.jpg

Optional manifest: data/photo-manifest.csv
  source_file,company
  Burke formal.jpg,16

Writes: data/photo-import-report.txt
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCOMING_DIR = ROOT / "assets" / "images" / "incoming"
MENTORS_DIR = ROOT / "assets" / "images" / "intranet" / "mentors"
STAFF_DIR = ROOT / "assets" / "images" / "intranet" / "staff"
PUBLIC_LEADERSHIP_DIR = ROOT / "assets" / "images" / "public" / "leadership"
REPORT_FILE = ROOT / "data" / "photo-import-report.txt"
MANIFEST_FILE = ROOT / "data" / "photo-manifest.csv"
MENTORS_JS = ROOT / "js" / "intranet" / "company-mentors-data.js"
MARINES_CSV = ROOT / "data" / "marines.csv"
MENTOR_LIST_CSV = ROOT / "data" / "company-mentor-list.csv"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif"}
RANK_TOKENS = {
    "col", "ltcol", "maj", "capt", "captain", "gysgt", "msgt", "sgtmaj", "sgtmaJ",
    "1stlt", "2ndlt", "lt", "cpt", "mr", "mrs", "ms", "dr",
}

LEADERSHIP_TARGETS = {
    "reid": PUBLIC_LEADERSHIP_DIR / "col-reid.jpg",
    "giraldi": PUBLIC_LEADERSHIP_DIR / "ltcol-giraldi.jpg",
}


def compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def parse_csv_name(name: str) -> dict[str, str]:
    name = name.strip().strip('"')
    if "," in name:
        last, first = name.split(",", 1)
        first_words = re.findall(r"[A-Za-z]+", first)
    else:
        parts = name.split()
        last = parts[-1] if parts else name
        first_words = parts[:-1] if len(parts) > 1 else re.findall(r"[A-Za-z]+", name)
    last_token = re.split(r"\s+", last.strip())[0]
    return {
        "last": last_token,
        "last_key": compact(last_token),
        "first_initial": first_words[0][0].upper() if first_words else "",
        "first_word": first_words[0].lower() if first_words else "",
        "first_key": compact(first_words[0]) if first_words else "",
        "display": name,
    }


def parse_js_mentors() -> list[dict]:
    text = MENTORS_JS.read_text(encoding="utf-8")
    mentors = []
    for block in re.finditer(
        r"company:\s*(\d+).*?name:\s*\"([^\"]*)\".*?rank:\s*\"([^\"]*)\"",
        text,
        re.S,
    ):
        company = int(block.group(1))
        name = block.group(2)
        rank = block.group(3)
        if not name:
            continue
        parts = parse_csv_name(name if "," in name else f"{name.split()[-1]}, {' '.join(name.split()[:-1])}")
        # name is "First M. Last" format from sync
        name_parts = name.split()
        if len(name_parts) >= 2:
            last = name_parts[-1].rstrip(".")
            first_words = [p for p in name_parts[:-1] if p.replace(".", "").isalpha()]
        else:
            last, first_words = name, []
        mentors.append(
            {
                "company": company,
                "battalion": (company - 1) // 6 + 1,
                "rank": rank,
                "name": name,
                "last_key": compact(last),
                "first_initial": first_words[0][0].upper() if first_words else "",
                "first_key": compact(first_words[0].rstrip(".")) if first_words else "",
                "last": last,
            }
        )
    return sorted(mentors, key=lambda m: m["company"])


def load_mardet_roster() -> list[dict]:
    if not MARINES_CSV.exists():
        return []
    people = []
    with MARINES_CSV.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            cost = (row.get("Cost / Staff Center") or "").strip().upper()
            if cost != "MARDET":
                continue
            name = row.get("LName/FName/MI") or row.get("name") or ""
            if not name:
                continue
            parsed = parse_csv_name(name)
            helper = (row.get("Helper") or "").strip()
            slug = helper.replace("|", "-").lower() if helper else f"{parsed['last_key']}-{parsed['first_key'] or parsed['first_initial'].lower()}"
            people.append(
                {
                    **parsed,
                    "rank": row.get("Rank", ""),
                    "billet": row.get("Billet / Primary Duty") or "",
                    "slug": slug,
                    "display": parsed["display"],
                }
            )
    return people


def normalize_stem(path: Path) -> str:
    stem = path.stem.lower()
    stem = re.sub(r"[_\-]+", " ", stem)
    stem = re.sub(r"\([^)]*\)", " ", stem)
    stem = re.sub(r"\b\d+\s*x\s*\d+\b", " ", stem)
    stem = re.sub(r"\b(photo|headshot|portrait|formal|official|copy|final|web|print)\b", " ", stem)
    for rank in sorted(RANK_TOKENS, key=len, reverse=True):
        stem = re.sub(rf"\b{re.escape(rank)}\b\.?", " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem


def tokens_from_stem(stem: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", stem.lower()) if t not in RANK_TOKENS and len(t) > 1]


def score_person_match(stem: str, person: dict) -> int:
    tokens = tokens_from_stem(stem)
    joined = " ".join(tokens)
    last_key = person["last_key"]
    first_key = person.get("first_key") or ""
    first_initial = person.get("first_initial", "").lower()

    if not last_key or last_key not in joined.replace(" ", ""):
        # also try last name as token
        if not any(last_key.startswith(t) or t.startswith(last_key[:4]) for t in tokens if len(t) >= 4):
            if last_key not in compact(stem):
                return 0

    score = 50

    if first_key and first_key in joined.replace(" ", ""):
        score += 40
    elif first_initial and re.search(rf"\b{first_initial}[a-z]*\b", stem):
        score += 25
    elif first_key and any(first_key.startswith(t) or t.startswith(first_key[:3]) for t in tokens):
        score += 20

    # Prefer longer last-name token matches
    if any(token == last_key for token in tokens):
        score += 15

    # Penalize very short/generic filenames
    if len(tokens) <= 1:
        score -= 10

    return score


def best_match(stem: str, candidates: list[dict], min_score: int = 55) -> tuple[dict | None, int, list[tuple[dict, int]]]:
    scored = [(c, score_person_match(stem, c)) for c in candidates]
    scored = [(c, s) for c, s in scored if s >= min_score]
    scored.sort(key=lambda x: x[1], reverse=True)
    if not scored:
        return None, 0, []
    if len(scored) >= 2 and scored[0][1] == scored[1][1]:
        return None, scored[0][1], scored[:3]
    return scored[0][0], scored[0][1], scored[:3]


def load_manifest() -> dict[str, int]:
    mapping: dict[str, int] = {}
    if not MANIFEST_FILE.exists():
        return mapping
    with MANIFEST_FILE.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            src = (row.get("source_file") or row.get("file") or "").strip()
            company = (row.get("company") or "").strip()
            if src and company.isdigit():
                mapping[src.lower()] = int(company)
                mapping[Path(src).stem.lower()] = int(company)
    return mapping


def unzip_to_incoming(zip_path: Path, incoming: Path) -> list[Path]:
    incoming.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            suffix = Path(info.filename).suffix.lower()
            if suffix not in IMAGE_EXTS:
                continue
            dest = incoming / Path(info.filename).name
            # handle duplicate basenames from subfolders
            if dest.exists():
                dest = incoming / f"{Path(info.filename).parent.name}_{dest.name}"
            with zf.open(info) as src, dest.open("wb") as out:
                shutil.copyfileobj(src, out)
            extracted.append(dest)
    return extracted


def collect_incoming(incoming: Path) -> list[Path]:
    if not incoming.exists():
        return []
    files = []
    for path in incoming.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            files.append(path)
    return sorted(files)


@dataclass
class ImportResult:
    mentor_copied: list[str] = field(default_factory=list)
    staff_copied: list[str] = field(default_factory=list)
    manifest_copied: list[str] = field(default_factory=list)
    ambiguous: list[str] = field(default_factory=list)
    unmatched: list[str] = field(default_factory=list)
    skipped_existing: list[str] = field(default_factory=list)


def copy_image(src: Path, dest: Path, force: bool) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        return
    shutil.copy2(src, dest)


def import_photos(incoming: Path, force: bool = False) -> ImportResult:
    result = ImportResult()
    mentors = parse_js_mentors()
    roster = load_mardet_roster()
    manifest = load_manifest()
    files = collect_incoming(incoming)

    mentor_by_company = {m["company"]: m for m in mentors}
    used_companies: set[int] = set()
    used_files: set[Path] = set()

    # Manifest overrides first
    for path in files:
        key = path.name.lower()
        if key not in manifest and path.stem.lower() not in manifest:
            continue
        company = manifest.get(key) or manifest.get(path.stem.lower())
        if not company:
            continue
        dest = MENTORS_DIR / f"company-{company:02d}.jpg"
        copy_image(path, dest, force)
        used_files.add(path)
        used_companies.add(company)
        mentor = mentor_by_company.get(company, {})
        result.manifest_copied.append(
            f"{path.name} → company-{company:02d}.jpg ({mentor.get('rank', '')} {mentor.get('name', '')})"
        )

    # Mentor auto-match
    for path in files:
        if path in used_files:
            continue
        stem = normalize_stem(path)
        person, score, ties = best_match(stem, mentors)
        if person is None and ties:
            tie_desc = ", ".join(f"Co {t[0]['company']} ({t[1]})" for t in ties)
            result.ambiguous.append(f"{path.name} — tied: {tie_desc}")
            continue
        if not person:
            continue
        if person["company"] in used_companies:
            if not force:
                result.skipped_existing.append(
                    f"{path.name} matched Co {person['company']} but slot already filled"
                )
            continue
        dest = MENTORS_DIR / f"company-{person['company']:02d}.jpg"
        copy_image(path, dest, force)
        used_files.add(path)
        used_companies.add(person["company"])
        result.mentor_copied.append(
            f"{path.name} → company-{person['company']:02d}.jpg ({person['rank']} {person['name']}, score {score})"
        )

    # Leadership + MARDET staff (non-mentor duplicates ok for staff files)
    for path in files:
        if path in used_files:
            continue
        stem = normalize_stem(path)
        stem_compact = compact(stem)

        leadership_matched = False
        for key, dest in LEADERSHIP_TARGETS.items():
            if key in stem_compact:
                if not dest.exists() or force:
                    copy_image(path, dest, force)
                    used_files.add(path)
                    result.staff_copied.append(f"{path.name} → {dest.name} (leadership)")
                leadership_matched = True
                break
        if leadership_matched:
            continue

        person, score, ties = best_match(stem, roster, min_score=60)
        if person is None and ties:
            continue
        if not person:
            continue
        slug = person["slug"]
        dest = STAFF_DIR / f"staff-{slug}.jpg"
        if dest.exists() and not force:
            continue
        copy_image(path, dest, force)
        used_files.add(path)
        result.staff_copied.append(
            f"{path.name} → {dest.name} ({person.get('rank', '')} {person['display']}, score {score})"
        )

    for path in files:
        if path not in used_files:
            result.unmatched.append(path.name)

    return result, mentors, used_companies


def write_report(result: ImportResult, mentors: list[dict], used_companies: set[int]) -> str:
    lines = ["# Photo import report", ""]
    lines.append(f"## Mentor photos copied ({len(result.mentor_copied) + len(result.manifest_copied)})")
    for row in result.manifest_copied + result.mentor_copied:
        lines.append(f"- {row}")
    if not result.manifest_copied and not result.mentor_copied:
        lines.append("- (none)")

    lines.append("")
    lines.append(f"## Staff / leadership copied ({len(result.staff_copied)})")
    for row in result.staff_copied:
        lines.append(f"- {row}")
    if not result.staff_copied:
        lines.append("- (none)")

    if result.ambiguous:
        lines.append("")
        lines.append("## Ambiguous — add to data/photo-manifest.csv")
        for row in result.ambiguous:
            lines.append(f"- {row}")

    if result.skipped_existing:
        lines.append("")
        lines.append("## Skipped (company slot already filled)")
        for row in result.skipped_existing:
            lines.append(f"- {row}")

    if result.unmatched:
        lines.append("")
        lines.append(f"## Unmatched files ({len(result.unmatched)})")
        for name in result.unmatched:
            lines.append(f"- {name}")

    lines.append("")
    lines.append("## Company mentor gaps")
    missing = []
    for m in mentors:
        dest = MENTORS_DIR / f"company-{m['company']:02d}.jpg"
        if not dest.exists():
            missing.append(m)
            lines.append(
                f"- Company {m['company']:2d} ({m['battalion']} Bn): {m['rank']} {m['name']} — missing"
            )
    if not missing:
        lines.append("- All 36 company mentor photos present.")

    lines.append("")
    lines.append("## MARDET roster without staff photo (non-mentor)")
    roster = load_mardet_roster()
    mentor_names = {compact(m["name"]) for m in mentors}
    staff_missing = []
    for person in roster:
        slug = person["slug"]
        staff_path = STAFF_DIR / f"staff-{slug}.jpg"
        leadership_hit = any(k in person["last_key"] for k in LEADERSHIP_TARGETS)
        if staff_path.exists() or leadership_hit:
            continue
        # if they're a company mentor, mentor path covers them
        if compact(person["display"]) in mentor_names:
            continue
        staff_missing.append(person)
        lines.append(f"- {person.get('rank', '')} {person['display']} ({person.get('billet', '')})")
    if not staff_missing:
        lines.append("- (none beyond mentor coverage)")

    text = "\n".join(lines) + "\n"
    REPORT_FILE.write_text(text, encoding="utf-8")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Import Marine headshots into site paths")
    parser.add_argument("--zip", type=Path, help="Unzip images into incoming/ before import")
    parser.add_argument("--incoming", type=Path, default=INCOMING_DIR)
    parser.add_argument("--force", action="store_true", help="Overwrite existing destination files")
    args = parser.parse_args()

    incoming = args.incoming
    incoming.mkdir(parents=True, exist_ok=True)
    MENTORS_DIR.mkdir(parents=True, exist_ok=True)

    if args.zip:
        if not args.zip.exists():
            print(f"Zip not found: {args.zip}")
            return 1
        extracted = unzip_to_incoming(args.zip, incoming)
        print(f"Extracted {len(extracted)} images to {incoming}")

    files = collect_incoming(incoming)
    if not files:
        print(f"No images in {incoming}. Drop photos there or pass --zip.")
        return 1

    result, mentors, used = import_photos(incoming, force=args.force)
    report = write_report(result, mentors, used)
    print(report)
    print(f"\nReport saved to {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
