#!/usr/bin/env python3
"""Regenerate summer training page and Cascade paste from includes + gallery."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDES = ROOT / "cascade" / "includes"
PAGE = ROOT / "pages" / "summer-training.html"
PASTE = ROOT / "cascade" / "paste-summer-training-marinecorps.html"

BODY_INCLUDE = INCLUDES / "summer-training-body.html"
GALLERY_INCLUDE = INCLUDES / "summer-training-gallery.html"

INLINE_GALLERY_MARKERS = {
    "leatherneck": ("<!-- LEATHERNECK_GALLERY_INSERT -->", INCLUDES / "summer-training-leatherneck-gallery.html"),
    "magtf": ("<!-- MAGTF_GALLERY_INSERT -->", INCLUDES / "summer-training-magtf-gallery.html"),
    "protramid": ("<!-- PROTRAMID_GALLERY_INSERT -->", INCLUDES / "summer-training-protramid-gallery.html"),
    "mciws": ("<!-- MCIWS_GALLERY_INSERT -->", INCLUDES / "summer-training-mciws-gallery.html"),
    "mwtc": ("<!-- MWTC_GALLERY_INSERT -->", INCLUDES / "summer-training-mwtc-gallery.html"),
    "mcmap": ("<!-- MCMAP_GALLERY_INSERT -->", INCLUDES / "summer-training-mcmap-gallery.html"),
}

IMAGE_LOCAL_PREFIX = "../"

PASTE_HEADER = """<!-- CASCADE paste → https://www.usna.edu/MarineCorps/Midshipmen/summer-training.php -->
<!-- Upload gallery images to assets/images/public/summer-training/ before pasting. -->
<link href="../_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>

<div class="marines-page-header">
<div class="container">
<h1 class="marines-page-header__title">Summer Training</h1>
<p class="marines-page-header__subtitle">Shaping and decisive training evolutions &#8212; inform, influence, assess, select, and equip by class year.</p>
</div>
</div>

"""

PHOTOS_NAV_CASCADE = '<a href="#training-gallery">Photos</a>\n'
PHOTOS_NAV_LOCAL = '<a href="#training-gallery">Photos</a>\n'

LOCAL_LINKS = (
    (r'href="https://www\.usna\.edu/MarineCorps/Midshipmen/prospective-marines\.php"', 'href="prospective-marines.html"'),
    (r'href="https://www\.usna\.edu/MarineCorps/MARDET/index\.php"', 'href="intranet/index.html"'),
)


def load_include(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def load_gallery() -> str:
    return load_include(GALLERY_INCLUDE)


def stitch_inline_galleries(body: str, image_prefix: str = "") -> str:
    result = body
    for _program, (marker, include_path) in INLINE_GALLERY_MARKERS.items():
        gallery = load_include(include_path)
        if image_prefix:
            gallery = gallery.replace("assets/images/public/", f"{image_prefix}assets/images/public/")
        replacement = f"\n{gallery}\n" if gallery else ""
        result = result.replace(marker, replacement)
    return result


def stitch_body(body: str, gallery: str, photos_nav: str, image_prefix: str = "") -> str:
    result = stitch_inline_galleries(body, image_prefix=image_prefix)
    result = result.replace("<!-- PHOTOS_NAV -->", photos_nav if gallery else "")
    if image_prefix and gallery:
        gallery = gallery.replace("assets/images/public/", f"{image_prefix}assets/images/public/")
    result = result.replace("<!-- GALLERY_INSERT -->", f"\n{gallery}\n" if gallery else "")
    return result.strip() + "\n"


def to_local_html(cascade_body: str) -> str:
    html = cascade_body
    for pattern, replacement in LOCAL_LINKS:
        html = re.sub(pattern, replacement, html)
    return html


def indent_for_page(html: str) -> str:
    lines = html.splitlines()
    return "\n".join(f"    {line}" if line else "" for line in lines) + "\n"


def replace_cascade_block(page_text: str, inner_html: str) -> str:
    start = "    <!-- CASCADE: page content start -->"
    end = "    <!-- CASCADE: page content end -->"
    if start not in page_text or end not in page_text:
        raise SystemExit("Could not find CASCADE markers in pages/summer-training.html")

    header = """    <div class="marines-page-header">
      <div class="container">
        <h1 class="marines-page-header__title">Summer Training</h1>
        <p class="marines-page-header__subtitle">Shaping and decisive training evolutions — inform, influence, assess, select, and equip by class year.</p>
      </div>
    </div>

"""
    block = f"{start}\n\n{header}{inner_html}\n{end}"
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    return pattern.sub(block, page_text, count=1)


def main() -> int:
    body = BODY_INCLUDE.read_text(encoding="utf-8")
    gallery = load_gallery()

    cascade_body = stitch_body(body, gallery, PHOTOS_NAV_CASCADE)
    local_body = stitch_body(body, to_local_html(gallery), PHOTOS_NAV_LOCAL, image_prefix=IMAGE_LOCAL_PREFIX)
    local_body = to_local_html(local_body)

    PASTE.write_text(PASTE_HEADER + cascade_body, encoding="utf-8")
    print(f"Wrote {PASTE.relative_to(ROOT)}")

    page = PAGE.read_text(encoding="utf-8")
    PAGE.write_text(replace_cascade_block(page, indent_for_page(local_body)), encoding="utf-8")
    print(f"Wrote {PAGE.relative_to(ROOT)}")
    if gallery:
        print("Page-wide gallery section included (Photos nav link active).")
    elif any(load_include(path) for _, path in INLINE_GALLERY_MARKERS.values()):
        print("Inline program galleries included.")
    else:
        print("No gallery photos yet — run import-summer-training-photos.py after adding CSV rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
