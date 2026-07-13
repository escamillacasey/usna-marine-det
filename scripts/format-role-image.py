#!/usr/bin/env python3
"""Convert and crop role images to site format (300x400 portrait JPG/PNG)."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "assets/images/public/roles"
TARGET_SIZE = (300, 400)


def open_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def crop_portrait(img: Image.Image, size: tuple[int, int] = TARGET_SIZE) -> Image.Image:
    target_w, target_h = size
    target_ratio = target_w / target_h
    src_w, src_h = img.size
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Too wide — crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # Too tall — crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    return img.resize(size, Image.Resampling.LANCZOS)


def export_role_image(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = crop_portrait(open_image(src))
    if dest.suffix.lower() == ".png":
        img.save(dest, "PNG", optimize=True)
    else:
        img.save(dest, "JPEG", quality=88, optimize=True)
    print(f"  {src.name} -> {dest.relative_to(ROOT)} ({dest.stat().st_size:,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", nargs="*", help="Pairs: source_path dest_rel_under_public/roles")
    args = parser.parse_args()

    if not args.mapping:
        parser.print_help()
        return 1

    if len(args.mapping) % 2:
        raise SystemExit("Provide source/destination pairs.")

    print("Formatting role images to 300x400...")
    for src_raw, dest_rel in zip(args.mapping[0::2], args.mapping[1::2]):
        src = Path(src_raw).expanduser()
        dest = PUBLIC / dest_rel
        if not src.exists():
            raise SystemExit(f"Missing source: {src}")
        export_role_image(src, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
