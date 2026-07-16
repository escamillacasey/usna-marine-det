#!/usr/bin/env python3
"""Rewrite legacy MarineCorps absolute URLs to canonical Marines URLs in Cascade pastes."""

from __future__ import annotations

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

# Also patch build-script headers that embed URLs
TARGET_FILES = [
    ROOT / "scripts" / "build-intranet-mentors-paste.sh",
    ROOT / "scripts" / "build-summer-training-pages.py",
]


def load_config() -> dict:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    for key in ("public_base", "legacy_public_base"):
        if not data.get(key, "").endswith("/"):
            data[key] = data[key].rstrip("/") + "/"
    return data


def replace_in_text(text: str, legacy: str, public: str) -> tuple[str, int]:
    count = text.count(legacy)
    if count:
        text = text.replace(legacy, public)
    # Host-only comments sometimes omit trailing path
    legacy_host = legacy.rstrip("/")
    public_host = public.rstrip("/")
    if legacy_host != legacy:
        extra = text.count(legacy_host)
        if extra:
            text = text.replace(legacy_host, public_host)
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
    cfg = load_config()
    legacy = cfg["legacy_public_base"]
    public = cfg["public_base"]
    intranet = cfg.get("intranet_base", public)
    if not intranet.endswith("/"):
        intranet += "/"

    total = 0
    for path in iter_html_files() + [p for p in TARGET_FILES if p.exists()]:
        original = path.read_text(encoding="utf-8")
        updated, n = replace_in_text(original, legacy, public)
        # intranet.usna.edu/MarineCorps → www Marines (same-host auth model)
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

    print(f"\nDone. {total} URL replacements. Config: cascade/site-urls.json")
    print(f"  {legacy} → {public}")
    if intranet != public:
        print(f"  intranet base → {intranet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
