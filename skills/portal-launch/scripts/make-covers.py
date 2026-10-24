#!/usr/bin/env python3
"""Make the three CrazyGames covers (1920x1080, 800x1200, 800x800) from one piece of cover art,
with the game title set in code (image models garble lettering).

Usage:
  python3 make-covers.py ART.png "Game Title" --font Font.ttf --focus 0.7,0.5 --out covers/
     [--title-pos left|top|bottom] [--fill "#FFFFFF"] [--stroke "#3B2A1A"] [--max-lines 2]

--focus is the subject's centre as fractions of the art's width and height; the 2:3 and 1:1 crops keep it in
frame. The art is cover-scaled (never stretched) and upscaled with Lanczos when smaller than the target.
Title placement: 16:9 uses --title-pos (default left: the left 45 percent of the frame); 2:3 puts the title on
top; 1:1 puts it at the bottom. Needs Pillow.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZES = {"cover-16x9": (1920, 1080), "cover-2x3": (800, 1200), "cover-1x1": (800, 800)}


def crop_to(img, w, h, fx, fy):
    scale = max(w / img.width, h / img.height)
    rw, rh = round(img.width * scale), round(img.height * scale)
    big = img.resize((rw, rh), Image.LANCZOS)
    cx, cy = fx * rw, fy * rh
    left = min(max(0, round(cx - w / 2)), rw - w)
    top = min(max(0, round(cy - h / 2)), rh - h)
    return big.crop((left, top, left + w, top + h))


def wrap(draw, text, font, max_w, max_lines):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)
    return lines if len(lines) <= max_lines else None


def fit_title(draw, text, font_path, box_w, box_h, max_lines):
    for size in range(240, 20, -4):
        font = ImageFont.truetype(font_path, size)
        lines = wrap(draw, text, font, box_w, max_lines)
        if lines and len(lines) * size * 1.1 <= box_h:
            return font, lines, size
    raise SystemExit("title does not fit; shorten it or allow more lines")


def draw_title(img, text, font_path, box, fill, stroke, max_lines):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    font, lines, size = fit_title(d, text, font_path, x1 - x0, y1 - y0, max_lines)
    sw = max(4, size // 9)
    line_h = size * 1.1
    total = line_h * len(lines)
    y = y0 + ((y1 - y0) - total) / 2
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for ln in lines:
        w = d.textlength(ln, font=font)
        x = x0 + ((x1 - x0) - w) / 2
        sd.text((x + sw * 0.6, y + sw * 0.9), ln, font=font, fill=(0, 0, 0, 110), stroke_width=sw, stroke_fill=(0, 0, 0, 110))
        y += line_h
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(sw / 3)))
    y = y0 + ((y1 - y0) - total) / 2
    d = ImageDraw.Draw(img)
    for ln in lines:
        w = d.textlength(ln, font=font)
        x = x0 + ((x1 - x0) - w) / 2
        d.text((x, y), ln, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)
        y += line_h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("art")
    ap.add_argument("title")
    ap.add_argument("--font", required=True)
    ap.add_argument("--focus", default="0.5,0.5")
    ap.add_argument("--out", default="covers")
    ap.add_argument("--title-pos", default="left", choices=["left", "top", "bottom"])
    ap.add_argument("--fill", default="#FFFFFF")
    ap.add_argument("--stroke", default="#3B2A1A")
    ap.add_argument("--max-lines", type=int, default=3)
    a = ap.parse_args()
    fx, fy = (float(v) for v in a.focus.split(","))
    art = Image.open(a.art).convert("RGBA")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, (w, h) in SIZES.items():
        if name == "cover-16x9":
            img = crop_to(art, w, h, 0.5, fy)
            pos = a.title_pos
        elif name == "cover-2x3":
            img = crop_to(art, w, h, fx, fy)
            pos = "top"
        else:
            img = crop_to(art, w, h, fx, fy)
            pos = "bottom"
        m = round(min(w, h) * 0.06)
        box = {
            "left": (m, m, round(w * 0.47), h - m),
            "top": (m, m, w - m, round(h * 0.30)),
            "bottom": (m, round(h * 0.70), w - m, h - m),
        }[pos]
        draw_title(img, a.title, a.font, box, a.fill, a.stroke, a.max_lines)
        dest = out / f"{name}.png"
        img.convert("RGB").save(dest)
        print(dest, f"{w}x{h}")


if __name__ == "__main__":
    main()
