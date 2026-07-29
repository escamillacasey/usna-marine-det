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

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "assets/images/incoming/mardet-drop"
SUMMER_INCOMING = ROOT / "assets/images/incoming/summer-training"
ROLES_PUBLIC = ROOT / "assets/images/public/roles"
MANIFEST = ROOT / "data/summer-training-photos.csv"
REPORT = ROOT / "data/mardet-photo-import-report.txt"

ROLE_TARGET_SIZE = (300, 400)
SUMMER_MAX_WIDTH = 1400
SUMMER_JPEG_QUALITY = 86

# Zip-relative path (under MARDET/) -> public/roles destination
ROLE_WIRED: dict[str, str] = {
    "Aviation Combat/0207.jpg": "aviation/air-intel.jpg",
    "Aviation Combat/7220.jpg": "aviation/atc.jpg",
    "Aviation Combat/7315.avif": "aviation/uas.jpg",
    "Aviation Combat/CH-53 Pilot.jpg": "aviation/ch53.jpg",
    "Aviation Combat/F-35 Pilot.avif": "aviation/f35.png",
    "Aviation Combat/MV-22 Pilot.jpg": "aviation/mv22.jpg",
    "Aviation Combat/UH-1Y Pilot.webp": "aviation/uh1y.png",
    "Combat Support/0102.jpg": "support/manpower.jpg",
    "Combat Support/0203.jpg": "support/ground-intel.jpg",
    "Combat Support/0204.webp": "support/ci-humint.jpg",
    "Combat Support/0206.jpg": "support/sigint-ew.jpg",
    "Combat Support/0602.avif": "support/communications.jpg",
    "Combat Support/1706.webp": "support/space.jpg",
    "Combat Support/1707.webp": "support/influence.jpg",
    "Combat Support/3404.webp": "support/financial.jpg",
    "Combat Support/4402.jpg": "support/judge-advocate.jpg",
    "Combat Support/4502.jpg": "support/commstrat.jpg",
    "Combat Support/5803.jpg": "support/military-police.jpg",
    "Combat Support/6602.webp": "support/aviation-supply.png",
}

SUMMER_PROGRAMS: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"^FFI\b", re.I), "ffi", "Force Fitness Instructor"),
    (re.compile(r"^Marine Secfor", re.I), "secfor", "Marine SECFOR"),
    (re.compile(r"^Marsoc and Recon", re.I), "marsoc", "MARSOC / Recon"),
    (re.compile(r"^Marsot Screener", re.I), "marsot", "MARSOT Screener"),
    (re.compile(r"^RTAP\b", re.I), "rtap", "RTAP"),
]

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}


def crop_portrait(img: Image.Image, size: tuple[int, int] = ROLE_TARGET_SIZE) -> Image.Image:
    target_w, target_h = size
    target_ratio = target_w / target_h
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    return img.resize(size, Image.Resampling.LANCZOS)


def export_role_image(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = crop_portrait(Image.open(src).convert("RGB"))
    if dest.suffix.lower() == ".png":
        img.save(dest, "PNG", optimize=True)
    else:
        img.save(dest, "JPEG", quality=88, optimize=True)


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
    args = parser.parse_args()

    zip_path = Path(args.zip_path).expanduser()
    if not zip_path.exists():
        raise SystemExit(f"Zip not found: {zip_path}")

    log: list[str] = [f"Source zip: {zip_path}", ""]
    src_root = extract_zip(zip_path)
    log.append(f"Extracted -> {src_root.relative_to(ROOT)}")

    log.append("\nRole images:")
    for src_rel, dest_rel in ROLE_WIRED.items():
        src = src_root / src_rel
        dest = ROLES_PUBLIC / dest_rel
        if not src.exists():
            raise SystemExit(f"Missing expected file in zip: {src_rel}")
        export_role_image(src, dest)
        log.append(f"  OK {src_rel} -> {dest_rel}")

    unused_role_dirs = []
    for folder in ("Aviation Combat", "Combat Support"):
        folder_path = src_root / folder
        if not folder_path.exists():
            continue
        wired_names = {Path(k).name for k in ROLE_WIRED if k.startswith(folder)}
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
