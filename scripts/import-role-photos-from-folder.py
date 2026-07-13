#!/usr/bin/env python3
"""Import role photos from a source folder, format to 300x400, and copy to public paths."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "assets/images/public/roles"
INCOMING = ROOT / "assets/images/incoming/roles-found"
TARGET_SIZE = (300, 400)

# Source-relative path -> destination under public/roles
WIRED: dict[str, str] = {
    "ground/infantry.avif": "ground/infantry.jpg",
    "ground/engineer.avif": "ground/combat-engineer.jpg",
    "ground/acv.avif": "ground/acv.jpg",
    "ground/recon_in_the_rain.avif": "ground/egr.jpg",
    "aviation/ch53.avif": "aviation/ch53.jpg",
    "aviation/j35-2.avif": "aviation/f35.png",
    "aviation/UH1Y2.avif": "aviation/uh1y.png",
    "support/comm2.avif": "support/communications.jpg",
    "support/logistics.jpg": "support/logistics.jpg",
}

UNUSED_NOTES: dict[str, str] = {
    "ground/recon.avif": "Amphibious recon — alternate for EGR (0307)",
    "ground/acv2.avif": "Alternate ACV shot",
    "ground/us-marines-with-7th-engineers-support-battalion-a00146.jpg": "Alternate combat engineer / demolitions",
    "aviation/f35-1.avif": "Alternate F-35 in-flight shot",
    "aviation/UH1Y.avif": "Alternate UH-1Y runway hover",
    "support/comm.avif": "Alternate communications",
    "support/comm3.avif": "Tactical networking — possible Cyberspace (1702)",
    "support/logo.webp": "Duplicate logistics ship scene — skip",
}


def crop_portrait(img: Image.Image, size: tuple[int, int] = TARGET_SIZE) -> Image.Image:
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


def archive_sources(src_root: Path) -> None:
    INCOMING.mkdir(parents=True, exist_ok=True)
    for path in sorted(src_root.rglob("*")):
        if path.is_file() and path.name != ".DS_Store":
            rel = path.relative_to(src_root)
            target = INCOMING / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        default="/Users/hellbentactual/Downloads/images to add to website",
        help="Folder containing ground/, aviation/, support/ subfolders",
    )
    args = parser.parse_args()

    src_root = Path(args.source).expanduser()
    if not src_root.exists():
        raise SystemExit(f"Source folder not found: {src_root}")

    print(f"Source: {src_root}")
    archive_sources(src_root)
    print(f"Archived copies -> {INCOMING.relative_to(ROOT)}")

    print("\nWiring role images:")
    for src_rel, dest_rel in WIRED.items():
        src = src_root / src_rel
        dest = PUBLIC / dest_rel
        if not src.exists():
            raise SystemExit(f"Missing expected source file: {src}")
        export_role_image(src, dest)
        print(f"  {src_rel} -> {dest_rel}")

    print("\nUnused in source folder:")
    for src_rel, note in UNUSED_NOTES.items():
        src = src_root / src_rel
        status = "present" if src.exists() else "missing"
        print(f"  [{status}] {src_rel} — {note}")

    report = ROOT / "data/role-image-import-latest.txt"
    lines = [f"Source: {src_root}", "", "Wired:"]
    lines.extend(f"  {k} -> {v}" for k, v in WIRED.items())
    lines.extend(["", "Unused:"])
    lines.extend(f"  {k} — {v}" for k, v in UNUSED_NOTES.items())
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nReport -> {report.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
