#!/usr/bin/env python3
"""Download top DVIDS role image candidates and copy legacy scraped images."""

from __future__ import annotations

import re
import shutil
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRAPED = ROOT / "assets/images/scraped/MarineCorps/_files/images/roles"
PUBLIC = ROOT / "assets/images/public/roles"

DVIDS_DOWNLOADS: list[tuple[int, str, str]] = [
    # (image_id, category subdir, filename)
    (9092926, "ground", "lar.jpg"),
    (9166566, "ground", "egr.jpg"),
    (9132989, "ground", "acv.jpg"),
    (9058332, "aviation", "flight-student.jpg"),
    (7737144, "aviation", "air-defense-control.jpg"),
    (8291474, "aviation", "atc.jpg"),
    (8765465, "aviation", "uas.jpg"),
    (5877109, "support", "magtf-intel.jpg"),
    (8025301, "support", "logistics.jpg"),
    (168167, "support", "military-police.jpg"),  # fresher than legacy mpo.jpg
    (8961399, "support", "influence.jpg"),  # MAGTF design wargame — interim for 1707
    (9507026, "support", "ground-intel.jpg"),  # fresher than legacy groundintel.jpg
    (8132214, "support", "communications.jpg"),  # fresher than legacy commo.jpg
    (6252836, "support", "ci-humint.jpg"),
    (6086782, "support", "cyberspace.jpg"),
    (7292231, "support", "space.jpg"),
    (8301306, "support", "judge-advocate.jpg"),
]

LEGACY_COPIES: list[tuple[Path, Path]] = [
    (SCRAPED / "support/manpower.jpg", PUBLIC / "support/manpower.jpg"),
    (SCRAPED / "support/gsupply1.jpg", PUBLIC / "support/ground-supply.jpg"),
    (SCRAPED / "support/finance.jpg", PUBLIC / "support/financial.jpg"),
    (SCRAPED / "support/pao.jpg", PUBLIC / "support/commstrat.jpg"),
    (SCRAPED / "support/amo.jpg", PUBLIC / "support/aircraft-maintenance.jpg"),
    (SCRAPED / "support/aviationsupply.png", PUBLIC / "support/aviation-supply.png"),
    (SCRAPED / "aviation/airIntellsignalIntell.jpg", PUBLIC / "support/sigint-ew.jpg"),
]


def fetch_dvids_image_url(image_id: int) -> str | None:
    url = f"https://www.dvidshub.net/image/{image_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "usna-marine-det/1.0"})
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        print(f"  fetch failed for {image_id}: {exc}")
        return None

    for pattern in (
        r'property="twitter:image"\s+content="([^"]+)"',
        r'property="og:image"\s+content="([^"]+)"',
        r'content="(https://d1ldvf68ux039x\.cloudfront\.net/[^"]+)"',
    ):
        match = re.search(pattern, html)
        if match:
            img_url = match.group(1)
            # Prefer largest thumb available
            return img_url.replace("/1000w_", "/2000w_")
    return None


def download_file(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "usna-marine-det/1.0"})
    try:
        with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=60) as resp:
            data = resp.read()
    except urllib.error.URLError as exc:
        print(f"  download failed: {exc}")
        return False
    dest.write_bytes(data)
    print(f"  saved {dest.relative_to(ROOT)} ({len(data):,} bytes)")
    return True


def main() -> int:
    print("=== DVIDS downloads ===")
    for image_id, category, filename in DVIDS_DOWNLOADS:
        dest = PUBLIC / category / filename
        print(f"{image_id} -> {dest.relative_to(ROOT)}")
        img_url = fetch_dvids_image_url(image_id)
        if not img_url:
            print("  no image URL found")
            continue
        print(f"  {img_url}")
        download_file(img_url, dest)

    print("\n=== Legacy copies ===")
    for src, dest in LEGACY_COPIES:
        if not src.exists():
            print(f"  missing source: {src.relative_to(ROOT)}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f"  skip (exists): {dest.relative_to(ROOT)}")
            continue
        shutil.copy2(src, dest)
        print(f"  copied {src.name} -> {dest.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
