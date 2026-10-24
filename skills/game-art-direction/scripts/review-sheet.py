#!/usr/bin/env python3
"""Build a review sheet for one game screenshot or cover: original, grayscale, blurred,
and thumbnails at 200 px and 94 px wide (portal grid sizes), side by side.

Usage: python3 review-sheet.py IMAGE [IMAGE ...]   -> writes IMAGE-review.png next to each
Needs Pillow (pip install pillow, or: uv run --with pillow python3 review-sheet.py ...).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

PANEL_H = 360
BG = (40, 40, 48)
LABEL = (230, 230, 230)


def fit(img, h):
    w = max(1, round(img.width * h / img.height))
    return img.resize((w, h), Image.LANCZOS)


def thumb(img, w):
    h = max(1, round(img.height * w / img.width))
    small = img.resize((w, h), Image.LANCZOS)
    # show it at real size on a tile so it reads like a portal grid
    tile = Image.new("RGB", (max(w + 20, 120), h + 20), (25, 25, 30))
    tile.paste(small, (10, 10))
    return tile


def sheet(path):
    src = Image.open(path).convert("RGB")
    big = fit(src, PANEL_H)
    panels = [
        ("original", big),
        ("grayscale (do shapes still separate?)", ImageOps.grayscale(big).convert("RGB")),
        ("blurred (is there one focal point?)", big.filter(ImageFilter.GaussianBlur(6))),
        ("200 px", thumb(src, 200)),
        ("94 px", thumb(src, 94)),
    ]
    width = sum(p.width for _, p in panels) + 20 * (len(panels) + 1)
    out = Image.new("RGB", (width, PANEL_H + 60), BG)
    d = ImageDraw.Draw(out)
    x = 20
    for label, p in panels:
        out.paste(p, (x, 40))
        d.text((x, 14), label, fill=LABEL)
        x += p.width + 20
    dest = Path(path).with_name(Path(path).stem + "-review.png")
    out.save(dest)
    print(dest)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    for p in sys.argv[1:]:
        sheet(p)
