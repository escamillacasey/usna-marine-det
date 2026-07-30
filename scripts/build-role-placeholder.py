#!/usr/bin/env python3
"""Generate the shared role photo placeholder (5:7 card ratio)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets/images/public/roles"
SVG_OUT = OUT_DIR / "image-coming-soon.svg"
JPG_OUT = OUT_DIR / "image-coming-soon.jpg"

SIZE = (300, 420)
NAVY = (0, 48, 87)  # #003057
MAROON = (128, 0, 0)  # #800000
GOLD = (197, 165, 114)  # #c5a572
MUTED = (180, 190, 200)


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/Supplemental Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    )
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def build_raster() -> Image.Image:
    img = Image.new("RGB", SIZE, NAVY)
    draw = ImageDraw.Draw(img)

    # Top maroon accent bar (matches staff-profile card)
    draw.rectangle((0, 0, SIZE[0], 8), fill=MAROON)

    # Gold frame
    inset = 18
    draw.rounded_rectangle(
        (inset, 28, SIZE[0] - inset, SIZE[1] - inset),
        radius=12,
        outline=GOLD,
        width=2,
    )

    # Simple camera / photo icon
    cx, cy = SIZE[0] // 2, 148
    draw.rounded_rectangle((cx - 44, cy - 28, cx + 44, cy + 28), radius=8, outline=GOLD, width=2)
    draw.ellipse((cx - 18, cy - 14, cx + 18, cy + 14), outline=GOLD, width=2)
    draw.rectangle((cx - 16, cy - 36, cx + 6, cy - 28), fill=GOLD)

    title_font = _load_font(22, bold=True)
    sub_font = _load_font(14)
    small_font = _load_font(11)

    title = "Image coming soon"
    sub = "Official photo pending"

    tw = draw.textlength(title, font=title_font)
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((SIZE[0] - tw) / 2, 228), title, fill=(255, 255, 255), font=title_font)
    draw.text(((SIZE[0] - sw) / 2, 262), sub, fill=MUTED, font=sub_font)

    note = "U.S. Marine Corps"
    nw = draw.textlength(note, font=small_font)
    draw.text(((SIZE[0] - nw) / 2, SIZE[1] - 42), note, fill=GOLD, font=small_font)

    return img


def build_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 420" role="img" aria-label="Image coming soon">
  <rect width="300" height="420" fill="#003057"/>
  <rect width="300" height="8" fill="#800000"/>
  <rect x="18" y="28" width="264" height="374" rx="12" fill="none" stroke="#c5a572" stroke-width="2"/>
  <rect x="118" y="120" width="64" height="48" rx="8" fill="none" stroke="#c5a572" stroke-width="2"/>
  <circle cx="150" cy="144" r="18" fill="none" stroke="#c5a572" stroke-width="2"/>
  <rect x="134" y="108" width="22" height="8" fill="#c5a572"/>
  <text x="150" y="240" text-anchor="middle" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="700">Image coming soon</text>
  <text x="150" y="268" text-anchor="middle" fill="#b4bec8" font-family="Arial, Helvetica, sans-serif" font-size="14">Official photo pending</text>
  <text x="150" y="390" text-anchor="middle" fill="#c5a572" font-family="Arial, Helvetica, sans-serif" font-size="11">U.S. Marine Corps</text>
</svg>
"""


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text(build_svg(), encoding="utf-8")
    build_raster().save(JPG_OUT, "JPEG", quality=90, optimize=True)
    print(f"Wrote {SVG_OUT.relative_to(ROOT)}")
    print(f"Wrote {JPG_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
