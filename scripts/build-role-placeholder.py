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
NAVY = (0, 48, 87)
NAVY_DARK = (0, 26, 51)
MAROON = (128, 0, 0)
GOLD = (197, 165, 114)
GOLD_DARK = (168, 134, 79)
WHITE = (255, 255, 255)
MUTED = (138, 154, 171)
PANEL = (255, 255, 255, 18)  # used conceptually; raster uses blend


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    )
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def _draw_vertical_gradient(img: Image.Image, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> None:
    base = Image.new("RGB", (1, SIZE[1]))
    pixels = base.load()
    for y in range(SIZE[1]):
        t = y / (SIZE[1] - 1)
        pixels[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    gradient = base.resize(SIZE)
    img.paste(gradient, (0, 0))


def _draw_landscape_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int) -> None:
    """Minimal photo-frame icon with landscape silhouette."""
    w, h = 112, 84
    x0, y0 = cx - w // 2, cy - h // 2
    x1, y1 = x0 + w, y0 + h
    draw.rounded_rectangle((x0, y0, x1, y1), radius=10, outline=GOLD, width=2)

    inner = (x0 + 10, y0 + 10, x1 - 10, y1 - 10)
    draw.rounded_rectangle(inner, radius=4, fill=(0, 36, 68))

    ix0, iy0, ix1, iy1 = inner
    draw.ellipse((ix1 - 34, iy0 + 14, ix1 - 14, iy0 + 34), fill=(120, 100, 70))
    draw.polygon([(ix0 + 8, iy1 - 12), (ix0 + 46, iy0 + 38), (ix0 + 78, iy1 - 12)], fill=(0, 58, 96))
    draw.polygon([(ix0 + 34, iy1 - 12), (ix0 + 72, iy0 + 48), (ix1 - 8, iy1 - 12)], fill=(0, 48, 87))


def build_raster() -> Image.Image:
    img = Image.new("RGB", SIZE, NAVY)
    _draw_vertical_gradient(img, NAVY_DARK, NAVY)
    draw = ImageDraw.Draw(img)

    # Top accent — matches staff-profile card
    draw.rectangle((0, 0, SIZE[0], 4), fill=MAROON)

    # Subtle inner panel
    draw.rounded_rectangle((20, 36, SIZE[0] - 20, SIZE[1] - 36), radius=14, fill=(0, 38, 72), outline=(40, 58, 78))

    # Gold rules
    draw.line((48, 318, SIZE[0] - 48, 318), fill=GOLD_DARK, width=1)

    _draw_landscape_icon(draw, SIZE[0] // 2, 156)

    title_font = _load_font(18, bold=True)
    caps_font = _load_font(11, bold=True)
    sub_font = _load_font(12)
    footer_font = _load_font(10, bold=True)

    title = "Image Coming Soon"
    caps = "OFFICIAL PHOTOGRAPH PENDING"
    footer = "U.S. MARINE CORPS"

    tw = draw.textlength(title, font=title_font)
    cw = draw.textlength(caps, font=caps_font)
    fw = draw.textlength(footer, font=footer_font)

    draw.text(((SIZE[0] - tw) / 2, 228), title, fill=WHITE, font=title_font)
    draw.text(((SIZE[0] - cw) / 2, 254), caps, fill=GOLD, font=caps_font)
    sub = "Awaiting final imagery from PAO"
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((SIZE[0] - sw) / 2, 278), sub, fill=MUTED, font=sub_font)
    draw.text(((SIZE[0] - fw) / 2, 336), footer, fill=GOLD_DARK, font=footer_font)

    return img


def build_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 420" role="img" aria-label="Image coming soon">
  <defs>
    <linearGradient id="bg" x1="150" y1="0" x2="150" y2="420" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#001a33"/>
      <stop offset="100%" stop-color="#003057"/>
    </linearGradient>
    <linearGradient id="panel" x1="150" y1="36" x2="150" y2="384" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#002640"/>
      <stop offset="100%" stop-color="#002a4a"/>
    </linearGradient>
    <linearGradient id="hill-back" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#003a60"/>
      <stop offset="100%" stop-color="#003057"/>
    </linearGradient>
    <linearGradient id="hill-front" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#004875"/>
      <stop offset="100%" stop-color="#003057"/>
    </linearGradient>
  </defs>

  <rect width="300" height="420" fill="url(#bg)"/>
  <rect width="300" height="4" fill="#800000"/>

  <rect x="20" y="36" width="260" height="348" rx="14" fill="url(#panel)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>

  <!-- Photo frame icon -->
  <g transform="translate(150 156)">
    <rect x="-56" y="-42" width="112" height="84" rx="10" fill="none" stroke="#c5a572" stroke-width="1.75"/>
    <rect x="-48" y="-34" width="96" height="68" rx="6" fill="#002444"/>
    <circle cx="28" cy="-16" r="10" fill="#c5a572" opacity="0.35"/>
    <path d="M-38 22 L-8 -18 L22 22 Z" fill="url(#hill-back)"/>
    <path d="M-14 22 L24 -8 L48 22 Z" fill="url(#hill-front)"/>
  </g>

  <!-- Typography -->
  <text x="150" y="232" text-anchor="middle" fill="#ffffff" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="18" font-weight="600" letter-spacing="0.02em">Image Coming Soon</text>
  <text x="150" y="258" text-anchor="middle" fill="#c5a572" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10.5" font-weight="700" letter-spacing="0.14em">OFFICIAL PHOTOGRAPH PENDING</text>
  <text x="150" y="282" text-anchor="middle" fill="#8a9aab" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11.5" font-weight="400">Awaiting final imagery from PAO</text>

  <line x1="52" y1="312" x2="248" y2="312" stroke="#a8864f" stroke-width="1" opacity="0.65"/>
  <text x="150" y="334" text-anchor="middle" fill="#a8864f" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="9.5" font-weight="700" letter-spacing="0.16em">U.S. MARINE CORPS</text>
</svg>
"""


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_OUT.write_text(build_svg(), encoding="utf-8")
    build_raster().save(JPG_OUT, "JPEG", quality=92, optimize=True)
    print(f"Wrote {SVG_OUT.relative_to(ROOT)}")
    print(f"Wrote {JPG_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
