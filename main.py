#!/usr/bin/env python3
"""Draw one infographic image summing up the world news of Thursday
19 November 2026, and write it to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set).

Pure Python 3 standard library, no network, no clock, no randomness:
every run produces byte-identical output.

The six stories, all of Thursday 19 November 2026 (researched and
verified against the day's reporting):
  1. Trump, Xi and Putin hold their first trilateral summit in
     Shenzhen, China; Ukraine tops the talks. (NYT live updates)
  2. Bitcoin falls to a four-month low near $62K, down ~15% in a
     week; the Fear & Greed index reads 10, "extreme fear".
     (CoinGabbar, market briefs of 19 Nov 2026)
  3. The International Court of Justice delivers its genocide
     judgment in The Gambia v. Myanmar over the Rohingya, at The
     Hague. (Muslim Network TV, 19 Nov 2026)
  4. COP31 climate talks in Antalya, Turkiye: ministers try to
     unblock the negotiations as a deal stays elusive.
     (Guardian live blog, 19 Nov 2026)
  5. Cyclone Akvan bears down on Odisha, India: more than 100,000
     people evacuated, red alert for landfall near Gopalpur.
     (The Hindu live updates, 19 Nov 2026)
  6. Van Gogh's "Blossoming Chestnut Trees" (1890) sells for
     $190.4M at Sotheby's New York, an auction record for the
     artist. (Reuters, 19 Nov 2026)
"""

import os
import struct
import zlib

W = 1024
H = 1024

# Palette: a newspaper front page -- cream paper, dark ink, red accent.
PAPER = (246, 241, 231)
PANEL_BG = (255, 253, 247)
INK = (22, 26, 38)
RED = (179, 0, 27)
GREY = (96, 100, 112)
WHITE = (255, 255, 255)

# The canvas: one RGB bytearray, row-major, no alpha.
px = bytearray(W * H * 3)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i] = color[0]
        px[i + 1] = color[1]
        px[i + 2] = color[2]


def fill_rect(x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, color)


def rect_outline(x, y, w, h, color, t=2):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def line(x0, y0, x1, y1, color, t=1):
    """Thick line: Bresenham path stamped with small filled discs."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        disc(x, y, max(1, t // 2), color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def disc(cx, cy, r, color):
    r2 = r * r
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r2:
                set_px(xx, yy, color)


def ring(cx, cy, r, color, t=3):
    r2o = r * r
    ri = max(0, r - t)
    r2i = ri * ri
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
            if r2i < d2 <= r2o:
                set_px(xx, yy, color)


def triangle(x0, y0, x1, y1, x2, y2, color):
    """Filled triangle via scanline over its bounding box."""
    minx = max(0, min(x0, x1, x2))
    maxx = min(W - 1, max(x0, x1, x2))
    miny = max(0, min(y0, y1, y2))
    maxy = min(H - 1, max(y0, y1, y2))

    def edge(ax, ay, bx, by, px_, py_):
        return (px_ - ax) * (by - ay) - (py_ - ay) * (bx - ax)

    for yy in range(miny, maxy + 1):
        for xx in range(minx, maxx + 1):
            d0 = edge(x0, y0, x1, y1, xx, yy)
            d1 = edge(x1, y1, x2, y2, xx, yy)
            d2 = edge(x2, y2, x0, y0, xx, yy)
            if (d0 >= 0 and d1 >= 0 and d2 >= 0) or (d0 <= 0 and d1 <= 0 and d2 <= 0):
                set_px(xx, yy, color)


def write_png(path):
    """Encode the canvas as a PNG with zlib + struct only."""

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter type 0 for every row
        raw += px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# A 5x7 bitmap font, one glyph per character, rows top to bottom.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": (".##..", ".##..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    "$": ("..#..", ".####", "##.#.", ".###.", ".#..#", "####.", "..#.."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, color):
    """Draw s with its top-left corner at (x, y); returns the width."""
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "#":
                    fill_rect(x + col * scale, y + row * scale, scale, scale, color)
        x += 6 * scale
    return len(s) * 6 * scale - scale


def draw_text_centered(cx, y, s, scale, color):
    w = text_width(s, scale)
    draw_text(cx - w // 2, y, s, scale, color)
    return w


import math

GOLD = (232, 176, 32)
ORANGE = (247, 147, 26)
TEAL = (3, 105, 161)
GREEN = (4, 120, 87)
BROWN = (121, 85, 52)
PINK = (244, 164, 196)
SKY = (186, 225, 245)


def icon_flags(x, y):
    """Three flags on poles: the Shenzhen trilateral summit."""
    for i, col in enumerate(((200, 30, 40), GOLD, (30, 80, 200))):
        px_ = x + 10 + i * 29
        line(px_, y + 10, px_, y + 78, INK, 3)
        fill_rect(px_ + 2, y + 10, 25, 18, col)
    line(x + 4, y + 80, x + 88, y + 80, INK, 3)


def icon_bitcoin(x, y):
    """An orange coin with the Bitcoin B and its two strokes."""
    cx, cy = x + 46, y + 46
    disc(cx, cy, 41, ORANGE)
    ring(cx, cy, 41, (214, 116, 10), 3)
    bw = text_width("B", 9)
    draw_text(cx - bw // 2 - 4, cy - 31, "B", 9, WHITE)
    fill_rect(cx - 12, cy - 37, 4, 74, WHITE)
    fill_rect(cx - 3, cy - 37, 4, 74, WHITE)


def icon_court(x, y):
    """A courthouse: pediment, three columns, steps."""
    triangle(x + 4, y + 32, x + 88, y + 32, x + 46, y + 8, INK)
    disc(x + 46, y + 22, 4, PAPER)
    for i in range(3):
        fill_rect(x + 16 + i * 26, y + 40, 9, 30, INK)
    fill_rect(x + 8, y + 72, 76, 6, INK)
    fill_rect(x + 4, y + 81, 84, 5, INK)


def icon_globe(x, y):
    """A globe with meridians and green continents: climate."""
    cx, cy, r = x + 46, y + 44, 37
    ring(cx, cy, r, TEAL, 4)
    for t in range(0, 360, 3):
        a = math.radians(t)
        ex = int(cx + 15 * math.sin(a))
        ey = int(cy - r * math.cos(a))
        disc(ex, ey, 2, TEAL)
    for dy in (-15, 15):
        hw = int(math.sqrt(r * r - dy * dy)) - 3
        line(cx - hw, cy + dy, cx + hw, cy + dy, TEAL, 3)
    disc(cx - 16, cy - 12, 9, GREEN)
    disc(cx + 10, cy - 18, 7, GREEN)
    disc(cx + 4, cy + 14, 10, GREEN)
    disc(cx - 22, cy + 8, 6, GREEN)


def icon_cyclone(x, y):
    """A spiral storm with rain streaks."""
    cx, cy = x + 48, y + 38
    for t in range(0, 560, 3):
        a = math.radians(t)
        r = 3 + t / 560.0 * 31
        disc(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), 5, TEAL)
    disc(cx, cy, 5, PAPER)
    for i in range(3):
        line(x + 18 + i * 22, y + 76, x + 10 + i * 22, y + 88, TEAL, 3)


def icon_art(x, y):
    """A framed painting of a blossoming tree: the Van Gogh."""
    rect_outline(x + 4, y + 6, 84, 72, (201, 162, 39), 6)
    fill_rect(x + 10, y + 12, 72, 60, SKY)
    fill_rect(x + 10, y + 60, 72, 12, GREEN)
    line(x + 46, y + 70, x + 46, y + 44, BROWN, 5)
    line(x + 46, y + 54, x + 34, y + 40, BROWN, 4)
    line(x + 46, y + 52, x + 58, y + 38, BROWN, 4)
    disc(x + 46, y + 32, 15, (34, 139, 34))
    disc(x + 33, y + 38, 10, (34, 139, 34))
    disc(x + 59, y + 38, 10, (34, 139, 34))
    for dx, dy in ((40, 26), (52, 24), (34, 34), (58, 32), (46, 38), (50, 42), (38, 44)):
        disc(x + dx, y + dy, 3, PINK)


BLUE = (29, 78, 216)
AMBER = (180, 83, 9)
PURPLE = (109, 40, 217)
PINKD = (190, 24, 93)

# (header, header colour, icon, headline lines, sub lines)
STORIES = [
    ("DIPLOMACY - CHINA", BLUE, icon_flags,
     ("TRUMP XI PUTIN", "SUMMIT MEETING"),
     ("UKRAINE TOPS TALKS", "IN SHENZHEN CHINA")),
    ("MARKETS - CRYPTO", AMBER, icon_bitcoin,
     ("BITCOIN FALLS", "TO 4-MONTH LOW"),
     ("NEAR $62K DOWN 15%", "FEAR INDEX AT 10")),
    ("JUSTICE - THE HAGUE", PURPLE, icon_court,
     ("UN COURT RULES", "ON GENOCIDE"),
     ("GAMBIA V MYANMAR", "ROHINGYA AT HAGUE")),
    ("CLIMATE - TURKIYE", GREEN, icon_globe,
     ("COP31 CLIMATE", "TALKS STALL"),
     ("TALKS GO ON BUT", "DEAL STAYS ELUSIVE")),
    ("WEATHER - INDIA", TEAL, icon_cyclone,
     ("CYCLONE AKVAN", "NEARS ODISHA"),
     ("100000 EVACUATED", "RED ALERT LANDFALL")),
    ("ARTS - NEW YORK", PINKD, icon_art,
     ("VAN GOGH SELLS", "FOR $190.4M"),
     ("SOTHEBYS AUCTION", "RECORD FOR ARTIST")),
]


def draw_panel(x, y, story):
    header, hcol, icon, headline, subs = story
    fill_rect(x, y, 468, 224, PANEL_BG)
    rect_outline(x, y, 468, 224, INK, 2)
    fill_rect(x, y, 468, 36, hcol)
    draw_text(x + 14, y + 8, header, 3, WHITE)
    icon(x + 12, y + 52)
    draw_text(x + 120, y + 52, headline[0], 4, INK)
    draw_text(x + 120, y + 90, headline[1], 4, INK)
    draw_text(x + 120, y + 142, subs[0], 3, GREY)
    draw_text(x + 120, y + 171, subs[1], 3, GREY)


def draw_image():
    fill_rect(0, 0, W, H, PAPER)
    rect_outline(10, 10, W - 20, H - 20, INK, 3)
    rect_outline(20, 20, W - 40, H - 40, INK, 1)

    # Masthead: the day, named as large as the page allows.
    draw_text_centered(W // 2, 44, "WORLD NEWS IN ONE PICTURE", 3, RED)
    fill_rect(60, 84, W - 120, 4, INK)
    draw_text_centered(W // 2, 100, "THURSDAY", 12, INK)
    draw_text_centered(W // 2, 196, "19 NOVEMBER 2026", 8, RED)
    fill_rect(60, 264, W - 120, 4, INK)

    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        draw_panel(36 + col * 484, 284 + row * 236, story)


def main():
    draw_image()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    write_png(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()



