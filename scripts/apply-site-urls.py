#!/usr/bin/env python3
"""Rewrite absolute site URLs in Cascade pastes per cascade/site-urls.json.

Default (--active): future_public_base → public_base (Marines/ → MarineCorps/).
Use --migrate when cutting over: public_base → future_public_base.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "cascade" / "site-urls.json"
TARGET_DIRS = [
    ROOT / "cascade",
    ROOT / "cascade" / "includes",
    ROOT / "cascade" / "snippets",
]

TARGET_FILES = [
    ROOT / "scripts" / "build-intranet-mentors-paste.sh",
    ROOT / "scripts" / "build-summer-training-pages.py",
    ROOT / "scripts" / "build-roles-pages.py",
]


def load_config() -> dict:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    for key in ("public_base", "future_public_base", "legacy_public_base"):
        if key in data and data[key] and not data[key].endswith("/"):
            data[key] = data[key].rstrip("/") + "/"
    if "future_public_base" not in data and data.get("legacy_public_base"):
        data["future_public_base"] = data["legacy_public_base"]
    return data


def replace_in_text(text: str, source: str, target: str) -> tuple[str, int]:
    count = text.count(source)
    if count:
        text = text.replace(source, target)
    source_host = source.rstrip("/")
    target_host = target.rstrip("/")
    if source_host != source:
        extra = text.count(source_host)
        if extra:
            text = text.replace(source_host, target_host)
            count += extra
    return text, count


def iter_html_files() -> list[Path]:
    files: list[Path] = []
    for directory in TARGET_DIRS:
        if not directory.is_dir():
            continue
        files.extend(sorted(directory.glob("*.html")))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Rewrite site URLs in Cascade pastes.")
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Cutover mode: public_base → future_public_base (MarineCorps/ → Marines/).",
    )
    args = parser.parse_args()

    cfg = load_config()
    public = cfg["public_base"]
    future = cfg.get("future_public_base", "https://www.usna.edu/Marines/")
    intranet = cfg.get("intranet_base", public)
    if not intranet.endswith("/"):
        intranet += "/"

    if args.migrate:
        source, target = public, future
        mode = "migrate (cutover)"
    else:
        source, target = future, public
        mode = "active (MarineCorps)"

    total = 0
    for path in iter_html_files() + [p for p in TARGET_FILES if p.exists()]:
        original = path.read_text(encoding="utf-8")
        updated, n = replace_in_text(original, source, target)
        if not args.migrate:
            updated, n2 = replace_in_text(
                updated,
                "https://intranet.usna.edu/MarineCorps/",
                intranet,
            )
            n += n2
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"  {path.relative_to(ROOT)} ({n} replacements)")
            total += n

    print(f"\nDone. {total} URL replacements ({mode}). Config: cascade/site-urls.json")
    print(f"  {source} → {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
