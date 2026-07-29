#!/usr/bin/env python3
"""Import PAO photos from MARDET zip (Aviation Combat / Combat Support / Summer training)."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from role_photo_export import ROLE_CARD_SIZE, RolePhotoSpec, export_role_image

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "assets/images/incoming/mardet-drop"
SUMMER_INCOMING = ROOT / "assets/images/incoming/summer-training"
ROLES_PUBLIC = ROOT / "assets/images/public/roles"
MANIFEST = ROOT / "data/summer-training-photos.csv"
REPORT = ROOT / "data/mardet-photo-import-report.txt"

SUMMER_MAX_WIDTH = 1400
SUMMER_JPEG_QUALITY = 86

# Zip-relative path (under MARDET/) -> export spec
# Aviation/aircraft: contain (avoid cutting airframes). Portraits: cover_top.
ROLE_SPECS: list[RolePhotoSpec] = [
    RolePhotoSpec("Aviation Combat/0207.jpg", "aviation/air-intel.jpg", "cover_top"),
    RolePhotoSpec("Aviation Combat/7220.jpg", "aviation/atc.jpg", "contain"),
    RolePhotoSpec("Aviation Combat/7315.avif", "aviation/uas.jpg", "cover_top"),
    RolePhotoSpec("Aviation Combat/CH-53 Pilot.jpg", "aviation/ch53.jpg", "contain"),
    RolePhotoSpec("Aviation Combat/F-35 Pilot.avif", "aviation/f35.png", "contain"),
    RolePhotoSpec("Aviation Combat/MV-22 Pilot.jpg", "aviation/mv22.jpg", "contain"),
    RolePhotoSpec("Aviation Combat/UH-1Y Pilot.webp", "aviation/uh1y.png", "contain"),
    RolePhotoSpec("Combat Support/0102.jpg", "support/manpower.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/0203.jpg", "support/ground-intel.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/0204.webp", "support/ci-humint.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/0206.jpg", "support/sigint-ew.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/0602.avif", "support/communications.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/1706.webp", "support/space.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/1707.webp", "support/influence.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/3404.webp", "support/financial.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/4402.jpg", "support/judge-advocate.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/4502.jpg", "support/commstrat.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/5803.jpg", "support/military-police.jpg", "cover_top"),
    RolePhotoSpec("Combat Support/6602.webp", "support/aviation-supply.png", "cover_top"),
]

# Optional paths checked when PAO adds files later
OPTIONAL_ROLE_SPECS: list[RolePhotoSpec] = [
    RolePhotoSpec("Aviation Combat/AH-1 Pilot.jpg", "aviation/ah1.png", "contain"),
    RolePhotoSpec("Aviation Combat/AH-1Z Pilot.jpg", "aviation/ah1.png", "contain"),
]

SUMMER_PROGRAMS: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"^FFI\b", re.I), "ffi", "Force Fitness Instructor"),
    (re.compile(r"^Marine Secfor", re.I), "secfor", "Marine SECFOR"),
    (re.compile(r"^Marsoc and Recon", re.I), "marsoc", "MARSOC / Recon"),
    (re.compile(r"^Marsot Screener", re.I), "marsot", "MARSOT Screener"),
    (re.compile(r"^RTAP\b", re.I), "rtap", "RTAP"),
]

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}

SCRAPED_AH1 = (
    ROOT / "assets/images/scraped/MarineCorps/_files/images/roles/aviation/AH1.png"
)


def import_role_specs(src_root: Path, specs: list[RolePhotoSpec], log: list[str]) -> None:
    for spec in specs:
        src = src_root / spec.src_rel
        dest = ROLES_PUBLIC / spec.dest_rel
        if not src.exists():
            log.append(f"  SKIP missing: {spec.src_rel}")
            continue
        export_role_image(src, dest, spec)
        log.append(f"  OK {spec.src_rel} -> {spec.dest_rel} ({spec.mode})")


def import_ah1_fallback(log: list[str]) -> None:
    """AH-1Z was not in the PAO zip; use contain on legacy art so the airframe stays visible."""
    dest = ROLES_PUBLIC / "aviation/ah1.png"
    if not SCRAPED_AH1.exists():
        log.append("  SKIP ah1.png — no PAO file and no scraped fallback")
        return
    export_role_image(
        SCRAPED_AH1,
        dest,
        RolePhotoSpec("", "aviation/ah1.png", "contain"),
    )
    log.append(f"  OK fallback {SCRAPED_AH1.name} -> aviation/ah1.png (contain)")
    log.append("  NOTE: Request AH-1Z / AH-1W photo from PAO for aviation/ah1.png")


def extract_zip(zip_path: Path) -> Path:
    INCOMING.mkdir(parents=True, exist_ok=True)
    if INCOMING.exists():
        shutil.rmtree(INCOMING)
    INCOMING.mkdir(parents=True)

    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir() or info.filename.startswith("__MACOSX"):
                continue
            rel = Path(info.filename)
            if rel.parts and rel.parts[0] == "MARDET":
                rel = Path(*rel.parts[1:])
            dest = INCOMING / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(zf.read(info.filename))
    return INCOMING


def summer_program_for(stem: str) -> tuple[str, str] | None:
    for pattern, program, label in SUMMER_PROGRAMS:
        if pattern.search(stem):
            return program, label
    return None


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "photo"


def stage_summer_photos(src_root: Path) -> list[dict[str, str]]:
    summer_dir = src_root / "Summer training"
    if not summer_dir.exists():
        return []

    SUMMER_INCOMING.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    sort_counters: dict[str, int] = {}

    for src in sorted(summer_dir.iterdir()):
        if not src.is_file() or src.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        match = summer_program_for(src.stem)
        if not match:
            continue
        program, label = match
        sort_counters[program] = sort_counters.get(program, 0) + 1
        order = sort_counters[program]
        rel_name = f"{program}/{slugify(src.stem)}{src.suffix.lower()}"
        dest = SUMMER_INCOMING / rel_name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

        caption = re.sub(r"\s+\d+$", "", src.stem).strip()
        if caption.lower() == "ffi":
            caption = "Force Fitness Instructor training"
        rows.append(
            {
                "source_file": rel_name,
                "program": program,
                "caption": caption,
                "alt": f"{caption} — {label} summer training",
                "month": "Summer 2026",
                "sort_order": str(order),
                "featured": "y" if order == 1 else "n",
            }
        )
    return rows


def append_manifest_rows(new_rows: list[dict[str, str]]) -> int:
    if not new_rows:
        return 0

    existing_sources: set[str] = set()
    header = "source_file,program,caption,alt,month,sort_order,featured\n"
    body_lines: list[str] = []

    if MANIFEST.exists():
        text = MANIFEST.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.lstrip().startswith("#") or not line.strip():
                body_lines.append(line)
                continue
            source = line.split(",", 1)[0].strip()
            if source == "source_file":
                if not body_lines:
                    body_lines.append(line)
                continue
            existing_sources.add(source)
            body_lines.append(line)

    added = 0
    for row in new_rows:
        if row["source_file"] in existing_sources:
            continue
        body_lines.append(
            ",".join(
                [
                    row["source_file"],
                    row["program"],
                    row["caption"],
                    row["alt"],
                    row["month"],
                    row["sort_order"],
                    row["featured"],
                ]
            )
        )
        existing_sources.add(row["source_file"])
        added += 1

    if added:
        if not body_lines or body_lines[0].split(",")[0] != "source_file":
            MANIFEST.write_text(header + "\n".join(body_lines) + "\n", encoding="utf-8")
        else:
            MANIFEST.write_text("\n".join(body_lines) + "\n", encoding="utf-8")
    return added


def run_script(name: str) -> None:
    subprocess.run(["python3", str(ROOT / "scripts" / name)], check=True, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "zip_path",
        nargs="?",
        default="/Users/hellbentactual/Downloads/MARDET (2).zip",
        help="Path to MARDET photo zip",
    )
    parser.add_argument("--skip-build", action="store_true", help="Import only; do not regenerate pages")
    parser.add_argument(
        "--roles-only",
        choices=("all", "aviation", "support"),
        default="all",
        help="Re-import only selected role categories",
    )
    parser.add_argument(
        "--from-dir",
        type=Path,
        help="Use an extracted MARDET folder instead of unzipping (e.g. ~/Downloads/MARDET)",
    )
    args = parser.parse_args()

    zip_path = Path(args.zip_path).expanduser()
    if args.from_dir:
        src_root = Path(args.from_dir).expanduser()
        if not src_root.exists():
            raise SystemExit(f"Source folder not found: {src_root}")
        log: list[str] = [f"Source dir: {src_root}", ""]
    else:
        if not zip_path.exists():
            raise SystemExit(f"Zip not found: {zip_path}")
        log = [f"Source zip: {zip_path}", ""]
        src_root = extract_zip(zip_path)
        log.append(f"Extracted -> {src_root.relative_to(ROOT)}")

    specs = ROLE_SPECS
    if args.roles_only == "aviation":
        specs = [s for s in ROLE_SPECS if s.dest_rel.startswith("aviation/")]
    elif args.roles_only == "support":
        specs = [s for s in ROLE_SPECS if s.dest_rel.startswith("support/")]

    if specs:
        log.append("\nRole images:")
        import_role_specs(src_root, specs, log)
        if args.roles_only in ("all", "aviation"):
            import_role_specs(src_root, OPTIONAL_ROLE_SPECS, log)
            ah1_from_pao = any((src_root / s.src_rel).exists() for s in OPTIONAL_ROLE_SPECS)
            if not ah1_from_pao:
                import_ah1_fallback(log)

    if args.roles_only != "all":
        REPORT.write_text("\n".join(log) + "\n", encoding="utf-8")
        print(REPORT.read_text(encoding="utf-8"))
        if not args.skip_build and args.roles_only == "aviation":
            run_script("build-roles-pages.py")
        return 0

    unused_role_dirs = []
    for folder in ("Aviation Combat", "Combat Support"):
        folder_path = src_root / folder
        if not folder_path.exists():
            continue
        wired_names = {Path(s.src_rel).name for s in ROLE_SPECS if s.src_rel.startswith(folder)}
        for path in sorted(folder_path.iterdir()):
            if path.is_file() and path.name not in wired_names:
                unused_role_dirs.append(f"  unused: {folder}/{path.name}")

    summer_rows = stage_summer_photos(src_root)
    log.append(f"\nSummer training staged: {len(summer_rows)} files -> {SUMMER_INCOMING.relative_to(ROOT)}")
    for row in summer_rows:
        log.append(f"  {row['program']}: {row['source_file']}")

    added = append_manifest_rows(summer_rows)
    log.append(f"\nManifest rows added: {added}")

    if unused_role_dirs:
        log.append("\nUnused role files (not wired):")
        log.extend(unused_role_dirs)

    REPORT.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8"))

    if args.skip_build:
        return 0

    run_script("import-summer-training-photos.py")
    run_script("build-summer-training-pages.py")
    run_script("build-roles-pages.py")
    print("\nDone. Upload updated assets to Cascade, then re-paste roles + summer training pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
