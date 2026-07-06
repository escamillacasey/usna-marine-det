#!/usr/bin/env python3
"""
Download images from the active usna.edu/USMC and usna.edu/MarineCorps sites.

Usage:
  python3 scripts/scrape-live-images.py
  python3 scripts/scrape-live-images.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
SCRAPED_DIR = ROOT / "assets" / "images" / "scraped"
IMAGES_DIR = ROOT / "assets" / "images"
MANIFEST_PATH = SCRAPED_DIR / "manifest.json"
GAPS_PATH = ROOT / "assets" / "images" / "IMAGE-GAPS.md"

PAGES = [
    "https://www.usna.edu/USMC/index.php",
    "https://www.usna.edu/USMC/staff.php",
    "https://www.usna.edu/USMC/Marine-Company-Mentors-public.php",
    "https://www.usna.edu/USMC/Prospective_Marine.php",
    "https://www.usna.edu/USMC/Summer_Training.php",
    "https://www.usna.edu/MarineCorps/index.php",
    "https://www.usna.edu/MarineCorps/roles/index.php",
    "https://www.usna.edu/MarineCorps/roles/aviation.php",
    "https://www.usna.edu/MarineCorps/roles/support.php",
]

IMG_RE = re.compile(
    r'(?:src|href|data-src)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|svg))["\']',
    re.I,
)

# Public site content only — skip USNA global chrome.
SKIP_PATH_PARTS = (
    "/CMS/_standard3.0/_files/img/",
    "/CMS/_standard3.0/_files/img/favicon/",
)

CANONICAL_MAP = {
    "USMC/_files/USNAMARINES.JPG": "hero-masthead.jpg",
    "USMC/_files/images/MardetLogo.jpg": "mardet-logo.jpg",
    "USMC/_files/images/OFFICIAL_trident-Flat-Blue-Gold-01.png": "trident-logo.png",
    "USMC/_files/rsz_2prospective_marines.jpg": "prospective-marines.jpg",
    "USMC/_files/SummerTrainingResize2.jpg": "summer-training.jpg",
    "USMC/_files/MarineMentorsResize2.jpg": "marine-mentors.jpg",
    "USMC/_files/rsz_graded.jpg": "marine-officers.jpg",
    "USMC/_files/images/MarineAviationF35.jpg": "marine-aviation.jpg",
    "USMC/_files/MarineCyber.png": "marine-cyber.png",
    "USMC/_files/instagram.png": "social-instagram.png",
    "USMC/_files/facebook.png": "social-facebook.png",
    "USMC/_files/images/Col_Reid,_5x72.jpg": "col-reid.jpg",
    "USMC/_files/Giraldi_Tom.jpg": "ltcol-giraldi.jpg",
    "USMC/_files/images/Lt_Swartz.jpg": "staff-lt-swartz.jpg",
    "USMC/_files/images/MSgt_Prieto.jpg": "staff-msgt-prieto.jpg",
    "USMC/_files/images/Maj._Snelgrove,_M._4x5_1.jpg": "staff-maj-snelgrove.jpg",
    "USMC/_files/images/mastheads/IMG_6850.JPG": "summer-training-masthead.jpg",
    "USMC/_files/images/protramid.PNG": "protramid.png",
    "USMC/_files/images/CH53.jpg": "prospective-ch53.jpg",
    "USMC/_files/images/Cyber2.jpg": "prospective-cyber.jpg",
    "USMC/_files/images/FA-18.jpg": "prospective-fa18.jpg",
    "USMC/_files/images/MarineGround.jpg": "prospective-ground.jpg",
    "USMC/_files/images/ProspectiveAAV.jpg": "prospective-aav.jpg",
    "MarineCorps/_files/images/mastheads/hero1.jpg": "hero-marinecorps.jpg",
    "MarineCorps/_files/images/tank.jpg": "tank.jpg",
    "MarineCorps/_files/images/jump.jpg": "jump.jpg",
    "MarineCorps/_files/images/groundCombat.jpg": "ground-combat.jpg",
    "MarineCorps/_files/images/aviationCombat.jpg": "aviation-combat.jpg",
    "MarineCorps/_files/images/combatSupport.jpg": "combat-support.jpg",
}

PROJECT_IMAGE_NEEDS = [
    ("hero-masthead.jpg", "Homepage / hero", "scraped or canonical"),
    ("prospective-marines.jpg", "Midshipmen hub / prospective card", "canonical"),
    ("summer-training.jpg", "Midshipmen hub / summer training", "canonical"),
    ("marine-mentors.jpg", "Midshipmen hub / mentors card", "canonical"),
    ("marine-aviation.jpg", "Roles / aviation", "canonical"),
    ("marine-cyber.png", "Marine Cyber page", "canonical"),
    ("ground-combat.jpg", "Roles / ground", "canonical"),
    ("aviation-combat.jpg", "Roles / aviation", "canonical"),
    ("combat-support.jpg", "Roles / support", "canonical"),
    ("col-reid.jpg", "Leadership", "canonical"),
    ("ltcol-giraldi.jpg", "Leadership", "canonical"),
    ("trident-logo.png", "Optional leadership strip", "canonical"),
    ("mardet-logo.jpg", "Optional leadership strip", "canonical"),
    ("social-instagram.png", "Social bar", "canonical"),
    ("social-facebook.png", "Social bar", "canonical"),
    *[(f"mentors/company-{n:02d}.jpg", f"Company {n} mentor headshot", "not on public site") for n in range(1, 37)],
]


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "usna-marine-det-scraper/1.0"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_images(html: str, page_url: str) -> list[str]:
    urls: list[str] = []
    for match in IMG_RE.finditer(html):
        full = urljoin(page_url, match.group(1))
        if full.startswith("/"):
            full = "https://www.usna.edu" + full
        urls.append(full)
    return urls


def is_site_content(url: str) -> bool:
    if "intranet.usna.edu" in url:
        return False
    if any(part in url for part in SKIP_PATH_PARTS):
        return False
    return "/USMC/" in url or "/MarineCorps/" in url


def local_scraped_path(url: str) -> Path:
    parsed = urlparse(url)
    rel = parsed.path.lstrip("/")
    return SCRAPED_DIR / rel


def site_key_from_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path.lstrip("/")


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "usna-marine-det-scraper/1.0"})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
            dest.write_bytes(resp.read())
        return True
    except urllib.error.URLError as exc:
        print(f"  skip {url}: {exc}")
        return False


def copy_canonical(scraped_path: Path, canonical_name: str) -> None:
    dest = IMAGES_DIR / canonical_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if scraped_path.exists():
        dest.write_bytes(scraped_path.read_bytes())


def write_gaps_report(manifest: dict) -> None:
    canonical_on_disk = {p.name for p in IMAGES_DIR.glob("*") if p.is_file()}
    mentor_on_disk = {p.name for p in (IMAGES_DIR / "mentors").glob("company-*.jpg")}

    lines = [
        "# Image inventory & gaps",
        "",
        f"Generated: {manifest['scraped_at']}",
        "",
        "Run `python3 scripts/scrape-live-images.py` to refresh downloads from the live site.",
        "",
        "## Canonical site images",
        "",
        "| File | Used for | Status |",
        "|------|----------|--------|",
    ]

    for filename, purpose, source in PROJECT_IMAGE_NEEDS:
        if filename.startswith("mentors/"):
            name = Path(filename).name
            status = "✅ local" if name in mentor_on_disk else "❌ missing — not published on live mentor page"
        elif (IMAGES_DIR / filename).exists() or filename in canonical_on_disk:
            status = "✅ local"
        else:
            status = f"❌ missing — expected from {source}"
        lines.append(f"| `{filename}` | {purpose} | {status} |")

    lines.extend(
        [
            "",
            "## Scraped from live site",
            "",
            f"- **Pages crawled:** {len(manifest['pages'])}",
            f"- **Images downloaded:** {manifest['downloaded_count']}",
            f"- **Stored under:** `assets/images/scraped/`",
            "",
            "### By page",
            "",
        ]
    )

    for page, info in manifest["pages"].items():
        lines.append(f"- `{page}` — {info['count']} content images")
        for url in info["images"]:
            key = site_key_from_url(url)
            lines.append(f"  - `{key}`")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- The live **Marine Company Mentors** page has no public headshots — mentor photos must come from MARDET or individual Marines.",
            "- One prospective-marine image (`Maj_MathiesonJ.jpg`) is on `intranet.usna.edu` and was skipped.",
            "- Role-specific images live under `assets/images/scraped/MarineCorps/_files/images/roles/`.",
            "",
        ]
    )

    GAPS_PATH.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape images from live USNA Marine sites")
    parser.add_argument("--dry-run", action="store_true", help="List URLs only; do not download")
    args = parser.parse_args()

    discovered: dict[str, list[str]] = {}
    all_urls: set[str] = set()

    for page in PAGES:
        html = fetch_html(page)
        imgs = sorted({u for u in extract_images(html, page) if is_site_content(u)})
        discovered[page] = imgs
        all_urls.update(imgs)
        print(f"{page}: {len(imgs)} content images")

    print(f"\nUnique content images: {len(all_urls)}")

    downloaded: list[str] = []
    if not args.dry_run:
        for url in sorted(all_urls):
            dest = local_scraped_path(url)
            print(f"download {url}")
            if download(url, dest):
                downloaded.append(url)

        for site_key, canonical in CANONICAL_MAP.items():
            scraped = SCRAPED_DIR / site_key
            if scraped.exists():
                copy_canonical(scraped, canonical)
                print(f"canonical {canonical} <- {site_key}")

    manifest = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "pages": {page: {"count": len(imgs), "images": imgs} for page, imgs in discovered.items()},
        "downloaded_count": len(downloaded),
        "canonical_map": CANONICAL_MAP,
    }
    SCRAPED_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n")
    write_gaps_report(manifest)

    print(f"\nManifest: {MANIFEST_PATH}")
    print(f"Gap report: {GAPS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
