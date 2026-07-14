#!/usr/bin/env python3
"""Import summer training photos and regenerate the gallery include."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "assets/images/incoming/summer-training"
PUBLIC = ROOT / "assets/images/public/summer-training"
MANIFEST = ROOT / "data/summer-training-photos.csv"
INCLUDES = ROOT / "cascade/includes"
GALLERY_INCLUDE = INCLUDES / "summer-training-gallery.html"
INLINE_PROGRAMS = ("leatherneck", "magtf", "protramid", "mciws", "mwtc")
REPORT = ROOT / "data/summer-training-photo-import-report.txt"

PROGRAM_LABELS = {
    "leatherneck": "Leatherneck",
    "magtf": "MAGTF Summer Training",
    "protramid": "PROTRAMID Marine Week",
    "selective": "Selective programs",
    "marsot": "MARSOT Screener",
    "mciws": "MCIWS",
    "mwtc": "MWTC",
    "general": "Summer training",
}

MAX_WIDTH = 1400
JPEG_QUALITY = 86


@dataclass
class PhotoRow:
    source_file: str
    program: str
    caption: str
    alt: str
    month: str
    sort_order: int
    featured: bool
    published_path: str = ""


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "photo"


def read_manifest() -> list[PhotoRow]:
    if not MANIFEST.exists():
        return []
    rows: list[PhotoRow] = []
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        lines = [line for line in handle if not line.lstrip().startswith("#")]
    for raw in csv.DictReader(lines):
        source = (raw.get("source_file") or "").strip()
        if not source:
            continue
        rows.append(
            PhotoRow(
                source_file=source,
                program=raw.get("program", "general").strip().lower() or "general",
                caption=raw.get("caption", "").strip(),
                alt=(raw.get("alt") or raw.get("caption", "")).strip() or "Summer training photo",
                month=raw.get("month", "").strip(),
                sort_order=int(raw.get("sort_order") or 999),
                featured=str(raw.get("featured", "")).strip().lower() in {"y", "yes", "true", "1"},
            )
        )
    rows.sort(key=lambda r: (r.program, r.sort_order, r.source_file))
    return rows


def find_source(name: str) -> Path | None:
    direct = INCOMING / name
    if direct.exists():
        return direct
    matches = list(INCOMING.rglob(name))
    return matches[0] if matches else None


def publish_image(src: Path, program: str, stem: str) -> tuple[Path, str]:
    dest_dir = PUBLIC / program
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{stem}.jpg"

    img = Image.open(src)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    elif img.mode == "L":
        img = img.convert("RGB")

    w, h = img.size
    if w > MAX_WIDTH:
        new_h = int(h * (MAX_WIDTH / w))
        img = img.resize((MAX_WIDTH, new_h), Image.Resampling.LANCZOS)

    img.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)
    rel = f"assets/images/public/summer-training/{program}/{dest.name}"
    return dest, rel


def render_program_gallery(program: str, rows: list[PhotoRow]) -> str:
    items = [r for r in rows if r.program == program and r.published_path]
    if not items:
        return ""
    items.sort(key=lambda r: (r.sort_order, r.source_file))
    parts = [
        '<div class="program-block__gallery">',
        '<h3 class="program-block__gallery-heading">Training in action</h3>',
        '<ul class="training-gallery__grid training-gallery__grid--inline">',
    ]
    for row in items:
        parts.append(_render_item(row, featured=row.featured))
    parts.extend(["</ul>", "</div>"])
    return "\n".join(parts) + "\n"


def render_gallery(rows: list[PhotoRow]) -> str:
    if not rows:
        return ""

    inline = set(INLINE_PROGRAMS)
    page_rows = [r for r in rows if r.program not in inline]
    if not page_rows:
        return ""

    featured = [r for r in page_rows if r.featured]
    by_program: dict[str, list[PhotoRow]] = {}
    for row in page_rows:
        by_program.setdefault(row.program, []).append(row)

    parts = [
        '<section class="content-section section--alt" id="training-gallery">',
        '<div class="container">',
        '<h2>Training in action</h2>',
        '<p>Recent photos from Leatherneck, MAGTF, PROTRAMID, and selective Marine Corps summer programs.</p>',
    ]

    if featured:
        parts.append('<ul class="training-gallery__hero" aria-label="Featured training photos">')
        for row in featured:
            parts.append(_render_item(row, featured=True))
        parts.append("</ul>")

    for program in (
        "leatherneck",
        "magtf",
        "protramid",
        "selective",
        "marsot",
        "general",
    ):
        items = by_program.get(program, [])
        if not items:
            continue
        label = PROGRAM_LABELS[program]
        parts.append(f'<div class="training-gallery" id="gallery-{program}">')
        parts.append(f'<h3 class="training-gallery__heading">{label}</h3>')
        parts.append('<ul class="training-gallery__grid">')
        for row in items:
            if row in featured:
                continue
            parts.append(_render_item(row))
        parts.append("</ul></div>")

    parts.extend(["</div>", "</section>"])
    return "\n".join(parts) + "\n"


def _render_item(row: PhotoRow, featured: bool = False) -> str:
    classes = "training-gallery__item"
    if featured:
        classes += " training-gallery__item--featured"
    meta = f'<span class="training-gallery__month">{row.month}</span>' if row.month else ""
    caption = (
        f'<figcaption class="training-gallery__caption">{row.caption}{meta}</figcaption>'
        if row.caption or row.month
        else ""
    )
    return (
        f'<li class="{classes}">'
        f'<figure class="training-gallery__figure">'
        f'<img alt="{_escape(row.alt)}" height="900" loading="lazy" '
        f'src="{row.published_path}" width="1400"/>'
        f"{caption}"
        f"</figure></li>"
    )


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = read_manifest()
    if not rows:
        print("No photo rows in data/summer-training-photos.csv — gallery will be omitted.")
        GALLERY_INCLUDE.write_text("", encoding="utf-8")
        REPORT.write_text("No manifest rows.\n", encoding="utf-8")
        return 0

    INCOMING.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    used_names: set[str] = set()

    for index, row in enumerate(rows, start=1):
        src = find_source(row.source_file)
        if not src:
            log.append(f"MISSING source: {row.source_file}")
            continue
        stem = slugify(Path(row.source_file).stem)
        if stem in used_names:
            stem = f"{stem}-{index:02d}"
        used_names.add(stem)
        if args.dry_run:
            rel = f"assets/images/public/summer-training/{row.program}/{stem}.jpg"
            row.published_path = rel
            log.append(f"DRY-RUN {src.name} -> {rel}")
            continue
        dest, rel = publish_image(src, row.program, stem)
        row.published_path = rel
        archive = INCOMING / "_imported" / row.source_file
        archive.parent.mkdir(parents=True, exist_ok=True)
        if not archive.exists():
            shutil.copy2(src, archive)
        log.append(f"OK {src.name} -> {dest.relative_to(ROOT)}")

    published = [r for r in rows if r.published_path]
    gallery_html = render_gallery(published)
    if not args.dry_run:
        GALLERY_INCLUDE.write_text(gallery_html, encoding="utf-8")
        for program in INLINE_PROGRAMS:
            include = INCLUDES / f"summer-training-{program}-gallery.html"
            include.write_text(render_program_gallery(program, published), encoding="utf-8")
            count = len([r for r in published if r.program == program])
            print(f"Wrote {include.relative_to(ROOT)} ({count} photos)")
        if gallery_html:
            print(f"Wrote {GALLERY_INCLUDE.relative_to(ROOT)} (page-wide gallery)")
        elif not any(r.program in INLINE_PROGRAMS for r in published):
            print(f"Wrote {GALLERY_INCLUDE.relative_to(ROOT)} ({len(published)} photos)")

    REPORT.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"Report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
