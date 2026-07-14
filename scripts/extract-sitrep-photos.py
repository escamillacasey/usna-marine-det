#!/usr/bin/env python3
"""Extract photos from summer sitrep .docx files into program subfolders."""

from __future__ import annotations

import argparse
import re
import shutil
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "assets/images/incoming/summer-training"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

PROGRAM_LABELS = {
    "leatherneck": "Leatherneck",
    "magtf": "MAGTF",
    "magtf-aviation": "Aviation MAGTF",
    "protramid": "PROTRAMID",
    "mciws": "MCIWS",
    "mwtc": "MWTC",
    "mcmap": "MCMAP",
    "ffi": "FFI",
    "rtap": "RTAP",
    "marsoc": "MARSOC / Recon",
    "secfor": "Marine SECFOR",
    "selective": "Selective programs",
    "general": "General",
}


def slugify(name: str) -> str:
    stem = Path(name).stem
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-").lower()
    return value or "sitrep"


def detect_section(text: str, current: str) -> str:
    t = text.strip()
    if not t:
        return current
    low = t.lower()

    if re.match(r"^leatherneck\s*\(", low):
        return "leatherneck"
    if re.match(r"^mciws\s*\(", low):
        return "mciws"
    if re.match(r"^mwtc\s*\(", low):
        return "mwtc"
    if re.match(r"^mcmap\s*\(", low):
        return "mcmap"
    if re.match(r"^ffi\s*\(", low):
        return "ffi"
    if re.match(r"^rtap\s*\(", low):
        return "rtap"
    if re.match(r"^marsoc", low):
        return "marsoc"
    if re.match(r"^secfor", low):
        return "secfor"
    if low.startswith("protramid/"):
        return "protramid"
    if re.match(r"^protramid\s*[\(:]", low) or low in {"protramid", "protramid:"}:
        return "protramid"
    if re.match(r"^aviation\s+magtf", low):
        return "magtf-aviation"
    if re.match(r"^magtf\s", low) or low == "magtf":
        return "magtf"

    if len(t) < 100:
        if "mcmap" in low and "course" in low:
            return "mcmap"
        if low.startswith("protramid"):
            return "protramid"
        if low.startswith("magtf"):
            return "magtf"
        if "aviation magtf" in low:
            return "magtf-aviation"

    return current


def paragraph_text(element: ET.Element) -> str:
    return "".join(t.text or "" for t in element.iter(f"{W}t")).strip()


def process_element(
    element: ET.Element,
    current: str,
    extracted: list[tuple[str, str, str]],
    rid_map: dict[str, str],
) -> str:
    tag = element.tag.split("}")[-1]
    if tag == "p":
        text = paragraph_text(element)
        current = detect_section(text, current)
        for blip in element.findall(f".//{A}blip"):
            rid = blip.get(f"{R}embed")
            target = rid_map.get(rid)
            if target:
                section = detect_section(text, current)
                extracted.append((section, target, text))
        return current
    if tag == "tbl":
        for blip in element.findall(f".//{A}blip"):
            rid = blip.get(f"{R}embed")
            target = rid_map.get(rid)
            if target:
                extracted.append((current, target, ""))
        return current
    for child in element:
        current = process_element(child, current, extracted, rid_map)
    return current


def extract_images(docx: Path) -> list[tuple[str, str, str]]:
    """Return list of (program, media_path, nearby_text)."""
    with zipfile.ZipFile(docx) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
        rels = ET.fromstring(zf.read("word/_rels/document.xml.rels"))
        rid_map = {rel.get("Id"): rel.get("Target") for rel in rels}

        body = root.find(f"{W}body")
        extracted: list[tuple[str, str, str]] = []
        current = "leatherneck"
        for child in body:
            current = process_element(child, current, extracted, rid_map)

    results = []
    with zipfile.ZipFile(docx) as zf:
        names = set(zf.namelist())
        for program, target, text in extracted:
            media_key = f"word/{target}" if not target.startswith("word/") else target
            if media_key in names:
                results.append((program, media_key, text))
    return results


def copy_image(docx: Path, media_key: str, program: str, out_dir: Path, index: int) -> Path:
    sitrep_slug = slugify(docx.name)
    ext = Path(media_key).suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff"}:
        ext = ".jpg"
    dest_name = f"{sitrep_slug}__{index:02d}{ext}"
    dest = out_dir / program / dest_name
    dest.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx) as zf:
        data = zf.read(media_key)
    dest.write_bytes(data)
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="Zip archive and/or .docx sitrep files")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--clean", action="store_true", help="Remove existing extracted photos first")
    args = parser.parse_args()

    docx_files: list[Path] = []
    for source in args.sources:
        path = Path(source).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"Not found: {path}")
        if path.suffix.lower() == ".zip":
            tmp = path.parent / f".{path.stem}-extracted"
            tmp.mkdir(exist_ok=True)
            with zipfile.ZipFile(path) as zf:
                zf.extractall(tmp)
            docx_files.extend(sorted(tmp.glob("*.docx")))
        elif path.suffix.lower() == ".docx":
            docx_files.append(path)
        elif path.is_dir():
            docx_files.extend(sorted(path.glob("*.docx")))
        else:
            raise SystemExit(f"Unsupported source: {path}")

    if not docx_files:
        raise SystemExit("No .docx sitrep files found.")

    out_dir = args.out.resolve()
    if args.clean and out_dir.exists():
        for child in out_dir.iterdir():
            if child.is_dir() and child.name != "_imported":
                shutil.rmtree(child)

    counts: Counter[str] = Counter()
    manifest_lines = ["program,source_sitrep,filename,nearby_text"]

    for docx in docx_files:
        images = extract_images(docx)
        for idx, (program, media_key, text) in enumerate(images, start=1):
            dest = copy_image(docx, media_key, program, out_dir, idx)
            counts[program] += 1
            nearby = text.replace('"', "'").replace("\n", " ")[:120]
            manifest_lines.append(
                f'{program},{docx.name},{dest.name},"{nearby}"'
            )
        print(f"{docx.name}: {len(images)} photos")

    report = ROOT / "data/summer-training-sitrep-import-report.txt"
    lines = [
        f"Extracted {sum(counts.values())} photos from {len(docx_files)} sitreps.",
        f"Output: {out_dir}",
        "",
        "By program:",
    ]
    for program, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        label = PROGRAM_LABELS.get(program, program)
        lines.append(f"  {count:3d}  {program}/  ({label})")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = ROOT / "data/summer-training-sitrep-manifest.csv"
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print(f"\nTotal: {sum(counts.values())} photos -> {out_dir}")
    for program, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {program}: {count}")
    print(f"Report: {report.relative_to(ROOT)}")
    print(f"Manifest: {manifest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
