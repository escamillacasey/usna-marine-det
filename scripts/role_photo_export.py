#!/usr/bin/env python3
"""Shared helpers for role photo export (portrait cards on site)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

# Matches .staff-profile__photo img { aspect-ratio: 5 / 7; object-fit: contain; }
ROLE_CARD_SIZE = (300, 420)
LETTERBOX_RGB = (32, 32, 32)


@dataclass(frozen=True)
class RolePhotoSpec:
    src_rel: str
    dest_rel: str
    mode: str = "cover_top"
    focal: tuple[float, float] = (0.5, 0.0)


def cover_crop(
    img: Image.Image,
    size: tuple[int, int] = ROLE_CARD_SIZE,
    focal: tuple[float, float] = (0.5, 0.0),
) -> Image.Image:
    """Cover-crop to size. focal=(x, y) in 0..1; y=0 keeps top (matches site CSS)."""
    target_w, target_h = size
    target_ratio = target_w / target_h
    src_w, src_h = img.size
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = int((src_w - new_w) * focal[0])
        box = (left, 0, left + new_w, src_h)
    else:
        new_h = int(src_w / target_ratio)
        top = int((src_h - new_h) * focal[1])
        box = (0, top, src_w, top + new_h)

    return img.crop(box).resize(size, Image.Resampling.LANCZOS)


def fit_contain(
    img: Image.Image,
    size: tuple[int, int] = ROLE_CARD_SIZE,
    background: tuple[int, int, int] = LETTERBOX_RGB,
) -> Image.Image:
    """Scale to fit inside size without cropping; letterbox the rest."""
    target_w, target_h = size
    src_w, src_h = img.size
    scale = min(target_w / src_w, target_h / src_h)
    new_w = max(1, int(src_w * scale))
    new_h = max(1, int(src_h * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, background)
    canvas.paste(resized, ((target_w - new_w) // 2, (target_h - new_h) // 2))
    return canvas


def export_role_image(src: Path, dest: Path, spec: RolePhotoSpec) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(src).convert("RGB")
    if spec.mode == "contain":
        out = fit_contain(img)
    elif spec.mode == "cover_focal":
        out = cover_crop(img, focal=spec.focal)
    else:
        out = cover_crop(img, focal=(0.5, 0.0))

    if dest.suffix.lower() == ".png":
        out.save(dest, "PNG", optimize=True)
    else:
        out.save(dest, "JPEG", quality=88, optimize=True)
