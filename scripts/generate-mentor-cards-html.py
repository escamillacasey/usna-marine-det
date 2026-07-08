#!/usr/bin/env python3
"""Generate static mentor card HTML from company-mentors-data.js (no JavaScript)."""

from __future__ import annotations

import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_JS = ROOT / "js" / "intranet" / "company-mentors-data.js"
PHOTOS_DIR = ROOT / "assets" / "images" / "intranet" / "mentors"
OUT_LOCAL = ROOT / "cascade" / "includes" / "mentor-cards-local.html"
OUT_CASCADE = ROOT / "cascade" / "includes" / "mentor-cards-cascade.html"
# Photo prefix (MARDET/ pages). Live site serves from assets/, not _files/.
CASCADE_PHOTO_PREFIX = os.environ.get(
    "CASCADE_PHOTO_PREFIX",
    "../assets/images/public/mentors/",
)


def ordinal_suffix(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def parse_mentors() -> list[dict]:
    text = DATA_JS.read_text(encoding="utf-8")
    mentors = []
    for block in re.findall(r"\{[^}]+\}", text):
        row: dict = {}
        for key, value in re.findall(r'(\w+):\s*"([^"]*)"', block):
            row[key] = value
        for key, value in re.findall(r"(\w+):\s*(\d+)", block):
            row[key] = int(value)
        if row.get("company"):
            mentors.append(row)
    return sorted(mentors, key=lambda m: int(m["company"]))


def duties_html(mentor: dict) -> str:
    rows = [
        ("Primary Duty", mentor.get("primaryDuty", "")),
        ("Collateral Duty", mentor.get("collateralDuty", "")),
        ("2026 Summer Duty", mentor.get("summerDuty", "")),
    ]
    rows = [(label, value) for label, value in rows if value and str(value).strip()]
    if not rows:
        return '<p class="mentor-card__bio is-placeholder">Duty information coming soon.</p>'

    parts = ['<dl class="mentor-card__duties">']
    for label, value in rows:
        parts.append(f"<dt>{html.escape(label)}</dt>")
        parts.append(f"<dd>{html.escape(str(value))}</dd>")
    parts.append("</dl>")
    return "".join(parts)


def card_html(mentor: dict, photo_prefix: str) -> str:
    company = int(mentor["company"])
    battalion = int(mentor["battalion"])
    rank = str(mentor.get("rank", ""))
    name = str(mentor.get("name", ""))
    email = str(mentor.get("email", ""))
    photo_file = PHOTOS_DIR / f"company-{company:02d}.jpg"
    photo_src = f"{photo_prefix}company-{company:02d}.jpg"

    if name:
        alt = f"Portrait of {rank} {name}"
        display = f"{rank} {name}"
    else:
        alt = f"Company {company} Marine mentor"
        display = "Marine Company Mentor"

    if photo_file.exists():
        photo_html = (
            f'<img src="{html.escape(photo_src)}" alt="{html.escape(alt)}" '
            f'width="400" height="500"/>'
        )
    else:
        photo_html = (
            f'<span class="mentor-card__photo-placeholder">Photo pending<br/>'
            f"Company {company}</span>"
        )

    email_html = ""
    if email:
        email_html = (
            f'<p class="mentor-card__meta"><a href="mailto:{html.escape(email)}">'
            f"{html.escape(email)}</a></p>"
        )

    battalion_label = f"{battalion}{ordinal_suffix(battalion)} Battalion"

    return (
        f'<article class="mentor-card" id="company-{company}">\n'
        f'<div class="mentor-card__photo">{photo_html}</div>\n'
        f'<div class="mentor-card__body">\n'
        f'<p class="mentor-card__company">Company {company} · {battalion_label}</p>\n'
        f'<h3 class="mentor-card__name">{html.escape(display)}</h3>\n'
        f"{email_html}\n"
        f"{duties_html(mentor)}\n"
        f"</div>\n"
        f"</article>"
    )


def grouped_html(mentors: list[dict], photo_prefix: str) -> str:
    lines: list[str] = []
    current_bn = None
    for mentor in mentors:
        battalion = int(mentor["battalion"])
        if battalion != current_bn:
            if current_bn is not None:
                lines.append("</div>")
            current_bn = battalion
            lines.append(f'<h2 class="mentor-battalion-heading" id="battalion-{battalion}">')
            lines.append(f"{battalion}{ordinal_suffix(battalion)} Battalion</h2>")
            lines.append('<div class="mentor-grid">')
        lines.append(card_html(mentor, photo_prefix))
    if current_bn is not None:
        lines.append("</div>")
    return "\n".join(lines) + "\n"


def main() -> int:
    mentors = parse_mentors()
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.write_text(
        grouped_html(mentors, "../../assets/images/intranet/mentors/"),
        encoding="utf-8",
    )
    OUT_CASCADE.write_text(
        grouped_html(mentors, CASCADE_PHOTO_PREFIX),
        encoding="utf-8",
    )
    print(f"Wrote {len(mentors)} mentors → {OUT_CASCADE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
