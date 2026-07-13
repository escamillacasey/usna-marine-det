#!/usr/bin/env python3
"""Regenerate roles pages and Cascade paste files from cascade/includes/roles-*-body.html."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDES = ROOT / "cascade" / "includes"
PAGES = ROOT / "pages" / "roles"
CASCADE = ROOT / "cascade"

NAV_CASCADE = """<nav aria-label="Roles in the Corps" class="page-subnav">
<a href="https://www.usna.edu/MarineCorps/Midshipmen/roles/index.php">Ground Combat</a>
<a href="https://www.usna.edu/MarineCorps/Midshipmen/roles/aviation.php">Aviation Combat</a>
<a href="https://www.usna.edu/MarineCorps/Midshipmen/roles/support.php">Combat Support</a>
</nav>"""

NAV_LOCAL = """<nav class="page-subnav" aria-label="Roles in the Corps">
          <a href="index.html">Ground Combat</a>
          <a href="aviation.html">Aviation Combat</a>
          <a href="support.html">Combat Support</a>
        </nav>"""

PASTE_HEADERS = {
    "ground": """<!-- CASCADE paste → https://www.usna.edu/MarineCorps/Midshipmen/roles/index.php -->
<!-- Upload role images to assets/images/public/roles/ground/ first. -->
<link href="../../_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>

<div class="marines-page-header">
<div class="container">
<h1 class="marines-page-header__title">Ground Combat Roles</h1>
<p class="marines-page-header__subtitle">Lead Marines in the fight on land — infantry, artillery, engineers, reconnaissance, amphibious vehicles, and air defense.</p>
</div>
</div>

<section class="content-section">
<div class="container leadership-list">
""",
    "aviation": """<!-- CASCADE paste → https://www.usna.edu/MarineCorps/Midshipmen/roles/aviation.php -->
<!-- Upload role images to assets/images/public/roles/aviation/ first. -->
<link href="../../_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>

<div class="marines-page-header">
<div class="container">
<h1 class="marines-page-header__title">Aviation Combat Roles</h1>
<p class="marines-page-header__subtitle">Pilots and aviation Marines who support the fight from the air.</p>
</div>
</div>

<section class="content-section">
<div class="container leadership-list">
""",
    "support": """<!-- CASCADE paste → https://www.usna.edu/MarineCorps/Midshipmen/roles/support.php -->
<!-- Upload role images to assets/images/public/roles/support/ first. -->
<link href="../../_files/css/local.css" media="all" rel="stylesheet" type="text/css"/>

<div class="marines-page-header">
<div class="container">
<h1 class="marines-page-header__title">Combat Support Roles</h1>
<p class="marines-page-header__subtitle">Intelligence, logistics, communications, and other functions that enable the MAGTF.</p>
</div>
</div>

<section class="content-section">
<div class="container leadership-list">
""",
}

PASTE_FOOTER = """
</div>
</section>
"""

PAGE_FILES = {
    "ground": PAGES / "index.html",
    "aviation": PAGES / "aviation.html",
    "support": PAGES / "support.html",
}

PASTE_FILES = {
    "ground": CASCADE / "paste-roles-ground-marinecorps.html",
    "aviation": CASCADE / "paste-roles-aviation-marinecorps.html",
    "support": CASCADE / "paste-roles-support-marinecorps.html",
}


def local_body(body: str) -> str:
    return body.replace(NAV_CASCADE, NAV_LOCAL)


def inject_page(page: Path, inner: str) -> None:
    text = page.read_text(encoding="utf-8")
    start = "    <!-- CASCADE: page content start -->"
    end = "    <!-- CASCADE: page content end -->"
    if start not in text or end not in text:
        raise SystemExit(f"{page} missing CASCADE markers")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    page.write_text(
        before
        + start
        + "\n\n    "
        + inner.replace("\n", "\n    ")
        + "\n\n    "
        + end
        + after,
        encoding="utf-8",
    )


def main() -> int:
    for key in ("ground", "aviation", "support"):
        body = (INCLUDES / f"roles-{key}-body.html").read_text(encoding="utf-8")
        paste = PASTE_HEADERS[key] + body + PASTE_FOOTER
        PASTE_FILES[key].write_text(paste, encoding="utf-8")
        print(f"Wrote {PASTE_FILES[key].name}")

        local_inner = f"""<div class="marines-page-header">
      <div class="container">
        <h1 class="marines-page-header__title">{_title(key)}</h1>
        <p class="marines-page-header__subtitle">{_subtitle(key)}</p>
      </div>
    </div>

    <section class="content-section">
      <div class="container leadership-list">

        {local_body(body)}

      </div>
    </section>"""
        inject_page(PAGE_FILES[key], local_inner)
        print(f"Updated {PAGE_FILES[key].relative_to(ROOT)}")
    return 0


def _title(key: str) -> str:
    return {
        "ground": "Ground Combat Roles",
        "aviation": "Aviation Combat Roles",
        "support": "Combat Support Roles",
    }[key]


def _subtitle(key: str) -> str:
    return {
        "ground": "Lead Marines in the fight on land — infantry, artillery, engineers, reconnaissance, amphibious vehicles, and air defense.",
        "aviation": "Pilots and aviation Marines who support the fight from the air.",
        "support": "Intelligence, logistics, communications, and other functions that enable the MAGTF.",
    }[key]


if __name__ == "__main__":
    raise SystemExit(main())
