#!/usr/bin/env python3
"""news-image-20261118: 'The World on One Page' - Wednesday 18 November 2026.

Draws a cream newspaper front page (1024x1024 PNG) summing up the day's
verified world news. Fixed data, no network, no randomness: running it twice
produces byte-identical output. Writes to /output/entry.png (or $OUT).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 224)
PAPER = (255, 253, 246)
INK = (20, 20, 20)
RED = (178, 34, 24)
DARK = (25, 25, 25)
GRAY = (90, 86, 76)
GREEN = (31, 122, 77)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, spacing=3):
    """Draw text with letter tracking; returns total width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x - xy[0] - spacing


def star(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- flags
def draw_flag(d, x, y, w, h, code):
    """Simplified flag badge drawn from code (no external images)."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if code == "US":  # stripes + blue canton
        for i in range(7):
            if i % 2 == 0:
                d.rectangle([x + 1, y + 1 + i * h / 7, x + w - 1,
                             y + (i + 1) * h / 7], fill=(178, 34, 52))
        d.rectangle([x + 1, y + 1, x + w * 0.45, y + h * 0.55], fill=(30, 50, 110))
        for r in range(3):
            for c in range(4):
                d.ellipse([x + 4 + c * 5, y + 3 + r * 4, x + 6 + c * 5,
                           y + 5 + r * 4], fill=(255, 255, 255))
    elif code == "CN":  # red + yellow star
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(222, 41, 16))
        star(d, x + 8, y + 8, 5, 2, 5, (255, 222, 0))
    elif code == "KW":  # green/white/red + black triangle
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 3], fill=(0, 122, 61))
        d.rectangle([x + 1, y + 1 + 2 * h / 3, x + w - 1, y + h - 1],
                    fill=(206, 17, 38))
        d.polygon([(x + 1, y + 1), (x + 1, y + h - 1), (x + 9, y + h / 2)],
                  fill=(0, 0, 0))
    elif code == "NZ":  # dark blue + 4 red stars
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(0, 20, 60))
        for sx, sy in [(17, 4), (21, 9), (13, 11), (18, 14)]:
            star(d, x + sx, y + sy, 2.6, 1.1, 4, (200, 30, 40))
    elif code == "BD":  # green + red disc
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(0, 106, 78))
        d.ellipse([x + 8, y + 3, x + 18, y + h - 3], fill=(244, 42, 65))
    elif code == "NL":  # red/white/blue
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 3], fill=(174, 28, 40))
        d.rectangle([x + 1, y + 1 + 2 * h / 3, x + w - 1, y + h - 1],
                    fill=(33, 70, 139))
    elif code == "PS":  # black/white/green + red triangle
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 3], fill=(0, 0, 0))
        d.rectangle([x + 1, y + 1 + 2 * h / 3, x + w - 1, y + h - 1],
                    fill=(0, 122, 61))
        d.polygon([(x + 1, y + 1), (x + 1, y + h - 1), (x + 9, y + h / 2)],
                  fill=(238, 42, 34))
    elif code == "GB":  # simplified Union Jack
        d.rectangle([x + 1, y + 1, x + w - 1, y + h - 1], fill=(0, 36, 125))
        d.line([x + 1, y + 1, x + w - 1, y + h - 1], fill=(255, 255, 255), width=3)
        d.line([x + w - 1, y + 1, x + 1, y + h - 1], fill=(255, 255, 255), width=3)
        d.rectangle([x + w / 2 - 2, y + 1, x + w / 2 + 2, y + h - 1],
                    fill=(200, 16, 46))
        d.rectangle([x + 1, y + h / 2 - 2, x + w - 1, y + h / 2 + 2],
                    fill=(200, 16, 46))
    elif code == "IN":  # saffron/white/green + navy wheel
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 3], fill=(255, 153, 51))
        d.rectangle([x + 1, y + 1 + 2 * h / 3, x + w - 1, y + h - 1],
                    fill=(19, 136, 8))
        d.ellipse([x + 10, y + 5, x + 16, y + h - 5], outline=(0, 0, 128), width=1)
    elif code == "PH":  # blue/red + white triangle
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 2], fill=(0, 56, 168))
        d.rectangle([x + 1, y + 1 + h / 2, x + w - 1, y + h - 1],
                    fill=(206, 17, 38))
        d.polygon([(x + 1, y + 1), (x + 1, y + h - 1), (x + 10, y + h / 2)],
                  fill=(255, 255, 255))
        d.ellipse([x + 3, y + 6, x + 6, y + 9], fill=(252, 209, 22))
    elif code == "CR":  # blue/white/red/white/blue
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 5], fill=(0, 43, 127))
        d.rectangle([x + 1, y + 1 + 2 * h / 5, x + w - 1, y + 1 + 3 * h / 5],
                    fill=(206, 17, 38))
        d.rectangle([x + 1, y + 1 + 4 * h / 5, x + w - 1, y + h - 1],
                    fill=(0, 43, 127))
    elif code == "PE":  # red/white/red vertical
        d.rectangle([x + 1, y + 1, x + 9, y + h - 1], fill=(206, 17, 38))
        d.rectangle([x + w - 9, y + 1, x + w - 1, y + h - 1], fill=(206, 17, 38))
    elif code == "RU":  # white/blue/red
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 3], fill=(255, 255, 255))
        d.rectangle([x + 1, y + 1 + h / 3, x + w - 1, y + 1 + 2 * h / 3],
                    fill=(0, 57, 166))
        d.rectangle([x + 1, y + 1 + 2 * h / 3, x + w - 1, y + h - 1],
                    fill=(213, 0, 50))


# ---------------------------------------------------------------- data
# (number, country, flag, headline, lat, lon) - all verified 18 Nov 2026
HEROES = [
    (1, "CHINA", "CN",
     "Trump, Xi and Putin meet in China for historic summit",
     "Shenzhen summit: Ukraine, Iran and trade", 22.5, 114.1),
    (2, "USA", "US",
     "Anthropic prices record IPO at $83 a share",
     "Claude maker valued above $1.4 trillion", 40.7, -74.0),
    (3, "GULF", "KW",
     "Iran fires on Kuwait and Bahrain after US strike",
     "First attack on Kuwait since September", 29.4, 47.9),
]

CARDS = [
    (4, "USA", "US", "Nvidia beats forecasts in first report since Huang exit", 37.4, -122.0),
    (5, "NEW ZEALAND", "NZ", "GTA 6 unlocks first in New Zealand after 13-year wait", -41.8, 172.6),
    (6, "USA", "US", "Waymo pulls driverless cars off all US freeways", 34.1, -118.2),
    (7, "USA", "US", "US loses measles-free status after 26 years", 31.5, -101.0),
    (8, "BANGLADESH", "BD", "Bangladesh sends in troops as Hasina unrest grows", 23.8, 90.4),
    (9, "NETHERLANDS", "NL", "UN court set for historic genocide verdict on Myanmar", 52.1, 4.3),
    (10, "USA", "US", "Peltola wins Alaska; Democrats take 56-44 Senate", 61.2, -149.9),
    (11, "GAZA", "PS", "Israel launches rare ground raid in Gaza", 31.5, 34.5),
    (12, "USA", "US", "Fed minutes point to faster rate hikes", 38.9, -77.0),
    (13, "UK", "GB", "UK inflation jumps to 3.6%, a one-year high", 51.5, -0.1),
    (14, "UK", "GB", "Prince Harry: I'd rejoin the army, warns of Russia", 53.5, -2.2),
    (15, "INDIA", "IN", "William and Kate meet Modi to end India tour", 28.6, 77.2),
    (16, "UK", "GB", "TfL data breach exposes 265,000 customers", 50.8, -2.5),
    (17, "PHILIPPINES", "PH", "Philippines seeks charges in Thomas Markle case", 14.6, 121.0),
    (18, "COSTA RICA", "CR", "Costa Rica journalist shot dead, first in 25 years", 9.9, -84.1),
    (19, "PERU", "PE", "Pope bids farewell to Peru after 12-day tour", -12.0, -77.0),
]

NUMBERS = [
    ("$83", "ANTHROPIC IPO PRICE"),
    ("5,412", "US MEASLES CASES IN 2026"),
    ("3.6%", "UK INFLATION, 1-YEAR HIGH"),
]

BRIEF = [
    "Java security flaw found in a top programming language",
    "Crimea Bridge: new video shows blasts before collapse",
    "Ukraine fights Russia inside an old gas pipeline",
    "South Korea seals exam buttons, checks every pair of glasses",
    "UK energy bills forecast to rise \u00a3443 a year",
    "Hakeem Jeffries nominated as next US House Speaker",
]

# manual nudges (dx, dy px) so close dots do not overlap
DOT_NUDGE = {6: (14, 8), 9: (12, 10), 12: (26, 6), 14: (16, -12),
             16: (-14, 10), 17: (12, 8)}


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 24  # margin

    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    # ---- masthead
    f_mast = font(SERIF_B, 57)
    title = "THE WORLD ON ONE PAGE"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 26), title, font=f_mast, fill=INK)
    f_tag = font(SANS_B, 15)
    tag = "EVERY STORY THAT MATTERED"
    tag_w = sum(d.textlength(c, font=f_tag) + 4 for c in tag) - 4
    tracked(d, ((W - tag_w) / 2, 92), tag, f_tag, GRAY, 4)
    f_date = font(SERIF_B, 19)
    d.text((MX + 150, 116), "Wednesday", font=f_date, fill=RED)
    w_wed = d.textlength("Wednesday", font=f_date)
    d.text((MX + 150 + w_wed + 8, 116), "18 November 2026",
           font=f_date, fill=INK)
    d.text((W - MX - 150, 118), "WEDNESDAY EDITION",
           font=font(SANS_B, 12), fill=GRAY)
    d.line([MX, 142, W - MX, 142], fill=INK, width=2)
    d.line([MX, 146, W - MX, 146], fill=INK, width=1)

    # ---- numbers strip
    y0, y1 = 156, 190
    d.rectangle([MX, y0, W - MX, y1], fill=INK)
    f_lab = font(SANS_B, 11)
    tracked(d, (MX + 12, y0 + 11), "THE DAY IN NUMBERS", f_lab, (246, 239, 224), 2)
    f_num = font(SANS_B, 20)
    f_nlab = font(SANS_B, 10)
    xs = [212, 500, 762]
    for (fig, lab), gx in zip(NUMBERS, xs):
        d.text((gx, y0 + 7), fig, font=f_num, fill=(246, 239, 224))
        fw = d.textlength(fig, font=f_num)
        d.text((gx + fw + 9, y0 + 13), lab, font=f_nlab, fill=(190, 184, 168))

    # ---- heroes
    hy, scene_h = 200, 84
    col_w, gap = 304, 16
    for i, (num, country, flag, head, deck, _lat, _lon) in enumerate(HEROES):
        x = MX + i * (col_w + gap)
        # scene
        sx, sy = x, hy
        if i == 0:  # summit: sky, three flags, skyline
            d.rectangle([sx, sy, sx + col_w, sy + scene_h], fill=(216, 228, 238))
            d.rectangle([sx, sy + 74, sx + col_w, sy + scene_h], fill=(70, 80, 95))
            for bx, bw, bh in [(8, 34, 30), (48, 26, 44), (80, 40, 24),
                               (128, 30, 52), (164, 36, 34), (206, 28, 46),
                               (240, 34, 28), (276, 24, 40)]:
                d.rectangle([sx + bx, sy + 74 - bh, sx + bx + bw, sy + 74],
                            fill=(40, 46, 60))
            for fx, fc in [(48, "US"), (140, "CN"), (232, "RU")]:
                d.line([sx + fx, sy + 12, sx + fx, sy + 74], fill=INK, width=2)
                draw_flag(d, sx + fx + 2, sy + 12, 34, 20, fc)
        elif i == 1:  # IPO: rising bars + arrow
            d.rectangle([sx, sy, sx + col_w, sy + scene_h], fill=(233, 240, 232))
            bars = [(30, 26, GREEN), (95, 46, (43, 140, 90)),
                    (160, 66, (27, 94, 32)), (225, 84, (21, 71, 46))]
            for bx, bh, col in bars:
                d.rectangle([sx + bx, sy + scene_h - 12 - bh,
                             sx + bx + 46, sy + scene_h - 12], fill=col)
            d.line([sx + 30, sy + 62, sx + 110, sy + 44, sx + 190, sy + 26,
                    sx + 268, sy + 10], fill=RED, width=4)
            d.polygon([(sx + 268, sy + 4), (sx + 280, sy + 16), (sx + 262, sy + 18)],
                      fill=RED)
            d.text((sx + 12, sy + 8), "$", font=font(SERIF_B, 26), fill=GREEN)
        else:  # gulf: sea, island, explosion
            d.rectangle([sx, sy, sx + col_w, sy + scene_h], fill=(191, 217, 232))
            d.rectangle([sx, sy + 58, sx + col_w, sy + scene_h], fill=(127, 179, 213))
            d.polygon([(sx + 120, sy + 58), (sx + 150, sy + 44),
                       (sx + 185, sy + 58)], fill=(214, 196, 150))
            d.line([sx + 20, sy + 30, sx + 90, sy + 44], fill=RED, width=2)
            d.ellipse([sx + 18, sy + 28, sx + 24, sy + 34], fill=RED)
            d.line([sx + 285, sy + 26, sx + 220, sy + 42], fill=RED, width=2)
            d.ellipse([sx + 281, sy + 24, sx + 287, sy + 30], fill=RED)
            star(d, sx + 152, sy + 34, 26, 11, 8, (255, 176, 32))
            star(d, sx + 152, sy + 34, 14, 6, 8, (230, 60, 20))
        d.rectangle([sx, sy, sx + col_w, sy + scene_h], outline=INK, width=1)
        # kicker + headline + deck
        ky = hy + scene_h + 8
        tracked(d, (x, ky), country + "  \u00b7  " + ("DIPLOMACY" if i == 0 else
                "MARKETS" if i == 1 else "CONFLICT"),
                font(SANS_B, 11), RED, 1)
        f_h = font(SERIF_B, 19)
        lines = wrap(d, head, f_h, col_w)
        ly = ky + 18
        for ln in lines[:2]:
            d.text((x, ly), ln, font=f_h, fill=INK)
            ly += 23
        d.text((x, ly + 2), deck, font=font(SANS, 12), fill=GRAY)

    # ---- card grid: 4 x 4
    gy, row_h, col_w2, gap2 = 382, 82, 235, 12
    f_num_c = font(SANS_B, 15)
    f_ctry = font(SANS_B, 9)
    f_head = font(SANS_B, 13)
    for idx, (num, country, flag, head, _lat, _lon) in enumerate(CARDS):
        r, c = divmod(idx, 4)
        x = MX + c * (col_w2 + gap2)
        y = gy + r * (row_h + 10)
        d.rectangle([x, y, x + col_w2, y + row_h], fill=PAPER, outline=INK, width=1)
        d.text((x + 8, y + 6), str(num), font=f_num_c, fill=RED)
        draw_flag(d, x + 30, y + 7, 26, 17, flag)
        d.text((x + 61, y + 9), country, font=f_ctry, fill=GRAY)
        lines = wrap(d, head, f_head, col_w2 - 16)
        ly = y + 30
        for ln in lines[:2]:
            d.text((x + 8, ly), ln, font=f_head, fill=INK)
            ly += 17
        # thin red rule under the number column
        d.line([x + 8, y + row_h - 6, x + 22, y + row_h - 6], fill=RED, width=2)

    # ---- map band
    my0, my1 = 748, 866
    d.rectangle([MX, my0, W - MX, my1], fill=DARK)
    d.text((MX + 12, my0 + 8), "THE DAY AROUND THE WORLD",
           font=font(SANS_B, 15), fill=(246, 239, 224))
    d.text((MX + 12, my0 + 28), "RED DOTS MARK WHERE EACH STORY HAPPENED",
           font=font(SANS, 10), fill=(170, 164, 150))

    def proj(lat, lon):
        px = 40 + (lon + 170) / 360.0 * 944
        py = 792 + (75 - lat) / 130.0 * 56
        return px, py

    LAND = {
        "N America": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                      (-85, 80), (-75, 72), (-65, 60), (-55, 52), (-60, 45),
                      (-70, 42), (-75, 35), (-80, 32), (-81, 26), (-90, 21),
                      (-95, 18), (-97, 16), (-105, 20), (-110, 24), (-115, 30),
                      (-125, 40), (-125, 48), (-135, 58), (-155, 60), (-165, 60)],
        "S America": [(-80, 10), (-75, 10), (-70, 12), (-62, 10), (-52, 5),
                      (-50, 0), (-45, -5), (-35, -8), (-40, -20), (-48, -28),
                      (-58, -35), (-65, -40), (-68, -50), (-70, -55), (-73, -45),
                      (-73, -35), (-70, -20), (-80, -5), (-81, 0), (-80, 8)],
        "Europe": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53),
                   (8, 57), (10, 59), (5, 60), (12, 56), (18, 56), (21, 55),
                   (24, 58), (21, 60), (18, 65), (12, 68), (18, 70), (25, 71),
                   (30, 70), (40, 68), (45, 66), (40, 60), (35, 55), (30, 50),
                   (28, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 42),
                   (0, 39), (-2, 37), (-6, 36)],
        "Africa": [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31),
                   (32, 31), (35, 28), (37, 22), (40, 15), (43, 12), (48, 11),
                   (51, 10), (46, 5), (42, 0), (40, -5), (40, -12), (36, -18),
                   (32, -26), (28, -33), (20, -35), (17, -32), (14, -22),
                   (12, -15), (9, -2), (9, 4), (4, 6), (-8, 5), (-13, 8),
                   (-17, 15), (-17, 20), (-15, 25), (-10, 30)],
        "Asia": [(40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
                 (100, 77), (110, 76), (120, 73), (130, 72), (140, 72),
                 (150, 70), (160, 68), (170, 66), (178, 65), (170, 60),
                 (162, 58), (158, 52), (150, 60), (142, 55), (140, 45),
                 (135, 43), (130, 42), (127, 40), (122, 38), (120, 35),
                 (122, 30), (120, 25), (115, 22), (108, 18), (105, 10),
                 (103, 5), (100, 8), (98, 12), (95, 16), (92, 21), (90, 22),
                 (88, 22), (85, 20), (80, 15), (77, 8), (75, 12), (72, 20),
                 (68, 23), (66, 25), (62, 25), (58, 26), (56, 27), (52, 28),
                 (50, 30), (48, 30), (44, 29), (42, 30), (40, 35), (38, 36),
                 (36, 36), (33, 36), (30, 36), (27, 37), (26, 38), (30, 40),
                 (35, 42), (40, 45), (42, 48), (45, 50), (48, 52), (50, 55),
                 (55, 58), (60, 60), (65, 65)],
        "Australia": [(114, -22), (114, -30), (115, -35), (120, -34),
                      (125, -33), (130, -32), (135, -35), (138, -35),
                      (140, -38), (145, -38), (150, -37), (153, -32),
                      (153, -27), (150, -22), (146, -19), (142, -15),
                      (142, -11), (137, -12), (135, -15), (132, -12),
                      (130, -13), (126, -14), (122, -17), (118, -20)],
        "Greenland": [(-45, 60), (-55, 70), (-60, 74), (-50, 76), (-40, 78),
                      (-30, 76), (-22, 70), (-25, 65), (-32, 60), (-40, 60)],
    }
    for poly in LAND.values():
        d.polygon([proj(lat, lon) for lon, lat in poly], fill=(239, 231, 211))

    f_dot = font(SANS_B, 9)
    for story in HEROES + CARDS:
        num, lat, lon = story[0], story[-2], story[-1]
        px, py = proj(lat, lon)
        dx, dy = DOT_NUDGE.get(num, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=(239, 231, 211), width=1)
        cx, cy = px + dx, py + dy
        d.ellipse([cx - 7.5, cy - 7.5, cx + 7.5, cy + 7.5], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        lw = d.textlength(label, font=f_dot)
        d.text((cx - lw / 2, cy - 5), label, font=f_dot, fill=(255, 255, 255))

    # ---- IN BRIEF panel
    by0, by1 = 874, 986
    d.rectangle([MX, by0, W - MX, by1], fill=PAPER, outline=INK, width=1)
    d.text((MX + 12, by0 + 8), "IN BRIEF", font=font(SANS_B, 15), fill=RED)
    f_b = font(SANS, 12)
    col_x = [MX + 12, MX + 500]
    for i, item in enumerate(BRIEF):
        x = col_x[i % 2]
        y = by0 + 32 + (i // 2) * 24
        d.text((x, y), "\u2022  " + item, font=f_b, fill=INK)
    # footer
    f_f = font(SANS, 10)
    foot = ("SOURCES: REUTERS \u00b7 AP \u00b7 BBC \u00b7 AFP \u00b7 PAHO \u00b7 CDC  "
            "\u2014  ALL STORIES FROM WEDNESDAY 18 NOVEMBER 2026")
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, 994), foot, font=f_f, fill=GRAY)

    out = os.environ.get("OUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
