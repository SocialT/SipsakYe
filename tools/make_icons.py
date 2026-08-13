#!/usr/bin/env python3
"""
Marka ikonlarını üretir: favicon, apple-touch-icon, PWA ikonları ve OG görseli.
Harici bağımlılık yok — PNG kodlayıcı standart kütüphane (zlib) ile yazıldı.

Kullanım:  python3 tools/make_icons.py
Çıktı:     assets/img/
"""

import os
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")

BRAND_A = (0xFF, 0x4D, 0x2D)   # turuncu-kırmızı
BRAND_B = (0xFF, 0x8A, 0x3D)   # turuncu
WHITE = (0xFF, 0xFF, 0xFF)

# 24x24 viewBox'taki şimşek işareti — style.css ve HTML'deki logo ile aynı.
BOLT = [(13, 2), (4.5, 13.5), (11, 13.5), (10, 22), (18.5, 10.5), (12, 10.5)]

SS = 3  # kenar yumuşatma için süper örnekleme katsayısı


def write_png(path, width, height, rows):
    """rows: her biri (r,g,b) üçlülerinden oluşan satır listesi."""
    raw = bytearray()
    for row in rows:
        raw.append(0)  # filtre tipi: none
        for r, g, b in row:
            raw += bytes((r, g, b))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def point_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            xint = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < xint:
                inside = not inside
    return inside


def rounded_rect_contains(px, py, w, h, r):
    if px < 0 or py < 0 or px > w or py > h:
        return False
    cx = min(max(px, r), w - r)
    cy = min(max(py, r), h - r)
    dx, dy = px - cx, py - cy
    return dx * dx + dy * dy <= r * r


def render_icon(size):
    """Yuvarlatılmış kare + degrade zemin + beyaz şimşek."""
    r = size * 0.22
    scale = size / 24.0
    bolt = [(x * scale, y * scale) for x, y in BOLT]
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            acc = [0, 0, 0]
            hits = 0
            for sy in range(SS):
                for sx in range(SS):
                    px = x + (sx + 0.5) / SS
                    py = y + (sy + 0.5) / SS
                    if not rounded_rect_contains(px, py, size, size, r):
                        continue
                    hits += 1
                    if point_in_poly(px, py, bolt):
                        c = WHITE
                    else:
                        t = (px / size * 0.55) + (py / size * 0.45)
                        c = lerp(BRAND_A, BRAND_B, min(max(t, 0.0), 1.0))
                    for i in range(3):
                        acc[i] += c[i]
            total = SS * SS
            miss = total - hits
            # zemin dışı: beyaz (şeffaflık yerine düz beyaz, RGB PNG)
            for i in range(3):
                acc[i] += 255 * miss
            row.append(tuple(v // total for v in acc))
        rows.append(row)
    return rows


def render_og(width=1200, height=630):
    """Sosyal paylaşım görseli: degrade zemin + büyük şimşek."""
    bolt_h = height * 0.52
    scale = bolt_h / 24.0
    ox = width * 0.5 - 11.5 * scale
    oy = height * 0.5 - 12 * scale
    bolt = [(x * scale + ox, y * scale + oy) for x, y in BOLT]
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            acc = [0, 0, 0]
            for sy in range(2):
                for sx in range(2):
                    px = x + (sx + 0.5) / 2
                    py = y + (sy + 0.5) / 2
                    if point_in_poly(px, py, bolt):
                        c = WHITE
                    else:
                        t = (px / width * 0.6) + (py / height * 0.4)
                        c = lerp(BRAND_A, BRAND_B, min(max(t, 0.0), 1.0))
                    for i in range(3):
                        acc[i] += c[i]
            row.append(tuple(v // 4 for v in acc))
        rows.append(row)
    return rows


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF4D2D"/>
      <stop offset="1" stop-color="#FF8A3D"/>
    </linearGradient>
  </defs>
  <rect width="24" height="24" rx="5.3" fill="url(#g)"/>
  <path d="M13 2 4.5 13.5H11l-1 8.5 8.5-11.5H12l1-8.5Z" fill="#fff"/>
</svg>
"""


def main():
    os.makedirs(OUT, exist_ok=True)

    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(FAVICON_SVG)
    print("yazıldı: favicon.svg")

    for name, size in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)]:
        write_png(os.path.join(OUT, name), size, size, render_icon(size))
        print("yazıldı: %s (%dx%d)" % (name, size, size))

    write_png(os.path.join(OUT, "og-image.png"), 1200, 630, render_og())
    print("yazıldı: og-image.png (1200x630)")


if __name__ == "__main__":
    main()
