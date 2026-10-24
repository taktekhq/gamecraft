#!/usr/bin/env python3
"""Cut sprites out of an image-model sheet drawn on a flat chroma background.

- Samples the real background colour from the image border (models never hit the exact hex you ask for).
- Keys it out with a soft edge, removes colour spill on the outline, splits the sheet into one sprite per
  separate object (no grid needed), trims each, and writes a check sheet on light and dark backgrounds.

Usage:
  python3 cutout.py SHEET.png --out sprites/ [--names a,b,c] [--tol 60] [--soft 40] [--min-area 2000] [--pad 4]
       [--height 256]
Sprites are numbered in reading order (top row left to right, then the next row) and named from --names when given.
--height scales every sprite to that height (Lanczos) for a consistent set. Needs Pillow and numpy.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def border_colour(a):
    b = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    return np.median(b, axis=0)


def key(rgb, bg, tol, soft):
    d = np.sqrt(((rgb.astype(np.float32) - bg) ** 2).sum(axis=2))
    alpha = np.clip((d - tol) / max(soft, 1), 0, 1)
    # despill: on semi-transparent edge pixels, pull the chroma colour back out
    out = rgb.astype(np.float32)
    edge = (alpha > 0) & (alpha < 1)
    if edge.any():
        a = alpha[edge][:, None]
        out[edge] = np.clip((out[edge] - (1 - a) * bg) / np.maximum(a, 0.15), 0, 255)
    return out.astype(np.uint8), (alpha * 255).astype(np.uint8)


def components(mask, min_area):
    """Label 8-connected regions of a boolean mask without scipy. Returns list of bounding boxes."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    boxes = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack = [(y0, x0)]
        seen[y0, x0] = True
        minx = maxx = x0
        miny = maxy = y0
        n = 0
        while stack:
            y, x = stack.pop()
            n += 1
            minx, maxx, miny, maxy = min(minx, x), max(maxx, x), min(miny, y), max(maxy, y)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        stack.append((yy, xx))
        if n >= min_area:
            boxes.append((minx, miny, maxx + 1, maxy + 1))
    return boxes


def merge_close(boxes, gap):
    """Merge boxes that overlap or sit within gap px (catches detached bits like steam or a falling leaf)."""
    merged = True
    while merged:
        merged = False
        out = []
        while boxes:
            a = boxes.pop()
            for i, b in enumerate(out):
                if a[0] - gap < b[2] and b[0] - gap < a[2] and a[1] - gap < b[3] and b[1] - gap < a[3]:
                    out[i] = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
                    merged = True
                    break
            else:
                out.append(a)
        boxes = out
    return boxes


def reading_order(boxes):
    boxes = sorted(boxes, key=lambda b: b[1])
    rows, row = [], []
    for b in boxes:
        if row and b[1] > max(r[3] for r in row) - (b[3] - b[1]) * 0.5:
            rows.append(row)
            row = []
        row.append(b)
    if row:
        rows.append(row)
    return [b for r in rows for b in sorted(r, key=lambda b: b[0])]


def check_sheet(sprites, dest):
    cell = 220
    sheet = Image.new("RGB", (cell * len(sprites), cell * 2), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(sprites):
        for row, bgc in enumerate([(245, 240, 225), (35, 35, 45)]):
            d.rectangle([i * cell, row * cell, (i + 1) * cell - 1, (row + 1) * cell - 1], fill=bgc)
            t = im.copy()
            t.thumbnail((cell - 30, cell - 40))
            sheet.paste(t, (i * cell + (cell - t.width) // 2, row * cell + 10 + (cell - 30 - t.height) // 2), t)
        d.text((i * cell + 8, cell - 18), name, fill=(60, 60, 60))
    sheet.save(dest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("--out", default="sprites")
    ap.add_argument("--names", default="")
    ap.add_argument("--tol", type=float, default=60, help="colour distance treated as fully background")
    ap.add_argument("--soft", type=float, default=40, help="distance over which alpha ramps to opaque")
    ap.add_argument("--min-area", type=int, default=2000)
    ap.add_argument("--gap", type=int, default=12)
    ap.add_argument("--pad", type=int, default=4)
    ap.add_argument("--height", type=int, default=0)
    a = ap.parse_args()

    rgb = np.array(Image.open(a.sheet).convert("RGB"))
    bg = border_colour(rgb)
    print("background", "#%02X%02X%02X" % tuple(int(v) for v in bg))
    col, alpha = key(rgb, bg, a.tol, a.soft)
    rgba = Image.fromarray(np.dstack([col, alpha]), "RGBA")
    boxes = reading_order(merge_close(components(alpha > 128, a.min_area), a.gap))
    names = [n.strip() for n in a.names.split(",") if n.strip()]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    sprites = []
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        p = a.pad
        im = rgba.crop((max(0, x0 - p), max(0, y0 - p), min(rgba.width, x1 + p), min(rgba.height, y1 + p)))
        if a.height:
            im = im.resize((max(1, round(im.width * a.height / im.height)), a.height), Image.LANCZOS)
        name = names[i] if i < len(names) else f"sprite_{i:02d}"
        im.save(out / f"{name}.png")
        sprites.append((name, im))
        print(out / f"{name}.png", f"{im.width}x{im.height}")
    if names and len(names) != len(boxes):
        print(f"WARNING: {len(boxes)} objects found, {len(names)} names given; check the sheet")
    check_sheet(sprites, out / "_check.png")
    print(out / "_check.png")


if __name__ == "__main__":
    main()
