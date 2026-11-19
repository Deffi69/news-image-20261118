#!/usr/bin/env python3
"""news-image-20261118: 'The World on One Page' - Wednesday 18 November 2026.

v3: 12-biggest-stories edition. Big roomy cards, a picture on every card
(leader busts for person stories, scene drawings for the rest) and a proper
hand-drawn world map with numbered dots. Cream newspaper front page,
1024x1024 PNG. Fixed data, no network, no randomness: running it twice
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


ACCENTS = [(178, 34, 24), (217, 119, 6), (31, 122, 77), (30, 80, 160),
           (122, 60, 160), (0, 130, 140), (200, 60, 110), (90, 110, 30)]


def draw_glasses(d, cx, cy, r):
    d.ellipse([cx - r - r * 0.9, cy - r * 0.62, cx - r + r * 0.9,
               cy + r * 0.62], outline=INK, width=1)
    d.ellipse([cx + r - r * 0.9, cy - r * 0.62, cx + r + r * 0.9,
               cy + r * 0.62], outline=INK, width=1)
    d.line([cx - r * 0.1, cy - r * 0.2, cx + r * 0.1, cy - r * 0.2],
           fill=INK, width=1)


def draw_bust(d, cx, top, w, hgt, skin, hair, style, suit, tie=None,
              glasses=False, beard=None, shirt=True):
    """Stylized cartoon bust: head, hair, shoulders/suit, simple cues."""
    hr = w * 0.30
    cy = top + hr + 1
    sh_top = top + 2 * hr - 3
    if style == "hasina":  # long dark hair behind the face
        d.ellipse([cx - hr - 5, cy - hr - 3, cx + hr + 5, cy + hr + 13],
                  fill=hair)
    # neck
    d.rectangle([cx - hr * 0.28, cy + hr - 5, cx + hr * 0.28, sh_top + 3],
                fill=skin)
    # shoulders / suit
    d.polygon([(cx - w / 2, top + hgt), (cx - w / 2 + 3, sh_top + 8),
               (cx - 5, sh_top), (cx + 5, sh_top),
               (cx + w / 2 - 3, sh_top + 8), (cx + w / 2, top + hgt)],
              fill=suit)
    if shirt:
        d.polygon([(cx - 5, sh_top), (cx + 5, sh_top),
                   (cx, top + hgt - 4)], fill=(245, 245, 240))
    if tie:
        d.polygon([(cx - 2.5, sh_top + 2), (cx + 2.5, sh_top + 2),
                   (cx + 1.2, top + hgt - 8), (cx - 1.2, top + hgt - 8)],
                  fill=tie)
    # head
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=skin)
    # hair / head cues per style
    if style in ("trump", "xi", "huang", "harry"):
        d.pieslice([cx - hr, cy - hr, cx + hr, cy + hr], 180, 360, fill=hair)
        if style == "trump":  # blond sweep across the forehead
            d.polygon([(cx - hr, cy - hr * 0.30), (cx + hr, cy - hr * 0.52),
                       (cx + hr, cy - hr * 0.02), (cx - hr, cy + hr * 0.10)],
                      fill=hair)
    elif style == "putin":  # balding: side hair only
        d.ellipse([cx - hr - 2, cy - 3, cx - hr + 3, cy + 6], fill=hair)
        d.ellipse([cx + hr - 3, cy - 3, cx + hr + 2, cy + 6], fill=hair)
        d.arc([cx - hr, cy - hr, cx + hr, cy + hr], 185, 355, fill=hair,
              width=2)
    elif style == "pope":  # white zucchetto cap
        d.pieslice([cx - hr, cy - hr, cx + hr, cy + hr], 180, 360,
                   fill=(250, 250, 248), outline=INK, width=1)
        d.ellipse([cx - hr - 1, cy - 2, cx - hr + 4, cy + 6], fill=hair)
        d.ellipse([cx + hr - 4, cy - 2, cx + hr + 1, cy + 6], fill=hair)
    elif style in ("hasina", "modi"):
        d.pieslice([cx - hr, cy - hr, cx + hr, cy + hr], 180, 360, fill=hair)
    if beard:
        d.chord([cx - hr, cy - hr + 3, cx + hr, cy + hr + 5], 15, 165,
                fill=beard)
    if glasses:
        draw_glasses(d, cx, cy + 1, hr * 0.52)


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
    elif code == "PE":  # red/white/red vertical
        d.rectangle([x + 1, y + 1, x + 9, y + h - 1], fill=(206, 17, 38))
        d.rectangle([x + w - 9, y + 1, x + w - 1, y + h - 1], fill=(206, 17, 38))
    elif code == "RU":  # white/blue/red
        d.rectangle([x + 1, y + 1, x + w - 1, y + 1 + h / 3], fill=(255, 255, 255))
        d.rectangle([x + 1, y + 1 + h / 3, x + w - 1, y + 1 + 2 * h / 3],
                    fill=(0, 57, 166))
        d.rectangle([x + 1, y + 1 + 2 * h / 3, x + w - 1, y + h - 1],
                    fill=(213, 0, 50))


# ---------------------------------------------------------------- scenes
def scene_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 244, 233))
    cx, cy = x + w / 2, y + h / 2
    for a_deg in range(0, 360, 45):
        a = math.radians(a_deg)
        x1, y1 = cx + 15 * math.cos(a), cy + 15 * math.sin(a)
        x2, y2 = cx + 22 * math.cos(a), cy + 22 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(150, 40, 30), width=2)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(200, 60, 40))
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(214, 84, 60))
    for dx, dy, r in [(-6, -4, 3), (5, -7, 2), (2, 5, 3), (-7, 6, 2)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=(245, 200, 180))


def scene_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 242, 225))
    brass = (168, 128, 40)
    cx = x + w / 2 - 6
    top = y + 12
    d.line([cx - 32, top, cx + 32, top], fill=brass, width=3)
    d.ellipse([cx - 3, top - 4, cx + 3, top + 2], fill=brass)
    d.line([cx, top, cx, y + 46], fill=brass, width=3)
    for sgn in (-1, 1):
        px = cx + sgn * 32
        d.line([px, top, px - 8, y + 32], fill=INK, width=1)
        d.line([px, top, px + 8, y + 32], fill=INK, width=1)
        d.pieslice([px - 11, y + 26, px + 11, y + 40], 0, 180, fill=brass)
        d.line([px - 11, y + 33, px + 11, y + 33], fill=brass, width=2)
    d.line([cx - 14, y + 48, cx + 14, y + 48], fill=INK, width=3)
    # small gavel, bottom right
    gx, gy = x + w - 20, y + h - 14
    d.line([gx, gy + 8, gx + 10, gy - 2], fill=(120, 72, 20), width=3)
    d.line([gx + 6, gy - 6, gx + 14, gy + 2], fill=(120, 72, 20), width=4)
    d.line([gx - 4, gy + 11, gx + 12, gy + 11], fill=INK, width=2)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 218, 234))
    d.ellipse([x + w - 26, y + 6, x + w - 12, y + 20], fill=(255, 176, 32))
    for bx, bw, bh in [(4, 15, 26), (21, 13, 34), (36, 17, 22),
                       (55, 13, 30), (70, 16, 24)]:
        d.rectangle([x + bx, y + h - 8 - bh, x + bx + bw, y + h - 8],
                    fill=(66, 70, 82))
    for sx, sy, sr in [(30, 16, 7), (38, 12, 9), (48, 15, 6)]:
        d.ellipse([x + sx - sr, y + sy - sr / 2, x + sx + sr, y + sy + sr / 2],
                  fill=(168, 168, 168))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(122, 110, 88))


def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 32, 56))
    for sx, sy in [(10, 10), (30, 6), (68, 10), (84, 24), (14, 42), (86, 46)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 255))
    cx = x + w / 2
    d.polygon([(cx, y + 5), (cx + 9, y + 19), (cx + 9, y + 40),
               (cx - 9, y + 40), (cx - 9, y + 19)], fill=(240, 240, 240))
    d.polygon([(cx, y + 5), (cx + 9, y + 19), (cx - 9, y + 19)],
              fill=(200, 40, 40))
    d.ellipse([cx - 4, y + 22, cx + 4, y + 30], fill=(90, 160, 220),
              outline=INK, width=1)
    d.polygon([(cx - 9, y + 32), (cx - 16, y + 44), (cx - 9, y + 42)],
              fill=(200, 40, 40))
    d.polygon([(cx + 9, y + 32), (cx + 16, y + 44), (cx + 9, y + 42)],
              fill=(200, 40, 40))
    d.polygon([(cx - 5, y + 40), (cx + 5, y + 40), (cx, y + 55)],
              fill=(255, 160, 20))
    d.rectangle([x + 8, y + h - 13, x + 13, y + h - 8], fill=(80, 200, 120))
    d.rectangle([x + 16, y + h - 9, x + 20, y + h - 5], fill=(80, 200, 120))


# figure cards: num -> (style, skin, hair, suit, tie, label, glasses, beard, shirt)
FIGS = {
    4: ("huang", (246, 205, 164), (20, 20, 20), (32, 38, 52),
        (178, 34, 24), "HUANG", True, None, True),
    8: ("hasina", (198, 140, 96), (15, 12, 10), (128, 20, 60),
        None, "HASINA", True, None, False),
    10: ("harry", (246, 200, 168), (196, 96, 44), (40, 48, 66),
         (30, 60, 120), "HARRY", False, (196, 96, 44), True),
    12: ("pope", (240, 190, 150), (220, 220, 220), (226, 221, 208),
         (198, 158, 44), "POPE", False, None, True),
}

SCENES = {5: scene_virus, 6: scene_scales, 7: scene_gaza, 9: scene_rocket}


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
    (5, "USA", "US", "US loses measles-free status after 26 years", 31.5, -101.0),
    (6, "NETHERLANDS", "NL", "UN court set for historic genocide verdict on Myanmar", 52.1, 4.3),
    (7, "GAZA", "PS", "Israel launches rare ground raid in Gaza", 31.5, 34.5),
    (8, "BANGLADESH", "BD", "Bangladesh sends in troops as Hasina unrest grows", 23.8, 90.4),
    (9, "NEW ZEALAND", "NZ", "GTA 6 unlocks first in New Zealand after 13-year wait", -41.8, 172.6),
    (10, "UK", "GB", "Prince Harry: I'd rejoin the army, warns of Russia", 53.5, -2.2),
    (11, "INDIA", "IN", "William and Kate meet Modi to end India tour", 28.6, 77.2),
    (12, "PERU", "PE", "Pope bids farewell to Peru after 12-day tour", -12.0, -77.0),
]

NUMBERS = [
    ("$83", "ANTHROPIC IPO PRICE"),
    ("5,412", "US MEASLES CASES IN 2026"),
    ("3.6%", "UK INFLATION, 1-YEAR HIGH"),
]

ALSO_LINE1 = ("Waymo pulls driverless cars off all US freeways  \u00b7  "
              "Fed minutes point to faster rate hikes")
ALSO_LINE2 = ("UK inflation jumps to 3.6%, a one-year high  \u00b7  "
              "TfL data breach exposes 265,000 customers  \u00b7  "
              "Peltola wins Alaska; Democrats take 56-44 Senate")

# manual nudges (dx, dy px) so close dots do not overlap
DOT_NUDGE = {6: (12, 8), 10: (-12, -8)}


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
    y0, y1 = 154, 186
    d.rectangle([MX, y0, W - MX, y1], fill=INK)
    f_lab = font(SANS_B, 11)
    tracked(d, (MX + 12, y0 + 10), "THE DAY IN NUMBERS", f_lab, (246, 239, 224), 2)
    f_num = font(SANS_B, 20)
    f_nlab = font(SANS_B, 10)
    xs = [212, 500, 762]
    for (fig, lab), gx in zip(NUMBERS, xs):
        d.text((gx, y0 + 6), fig, font=f_num, fill=(255, 208, 92))
        fw = d.textlength(fig, font=f_num)
        d.text((gx + fw + 9, y0 + 12), lab, font=f_nlab, fill=(190, 184, 168))

    # ---- heroes
    hy, scene_h = 194, 74
    col_w, gap = 317, 12
    for i, (num, country, flag, head, deck, _lat, _lon) in enumerate(HEROES):
        x = MX + i * (col_w + gap)
        sx, sy = x, hy
        if i == 0:  # summit: sky, flags, skyline, three leaders in front
            d.rectangle([sx, sy, sx + col_w, sy + scene_h], fill=(216, 228, 238))
            d.rectangle([sx, sy + 56, sx + col_w, sy + scene_h], fill=(52, 58, 70))
            for bx, bw, bh in [(8, 34, 24), (48, 26, 36), (80, 40, 20),
                               (128, 30, 42), (164, 36, 28), (206, 28, 38),
                               (240, 34, 22), (276, 24, 32)]:
                d.rectangle([sx + bx, sy + 56 - bh, sx + bx + bw, sy + 56],
                            fill=(40, 46, 60))
            for fx, fc in [(30, "US"), (146, "CN"), (262, "RU")]:
                d.line([sx + fx, sy + 3, sx + fx, sy + 17], fill=INK, width=2)
                draw_flag(d, sx + fx + 2, sy + 3, 24, 13, fc)
            leaders = [
                (56, "trump", (247, 203, 164), (232, 197, 90), (35, 42, 66),
                 (178, 34, 24), "TRUMP"),
                (158, "xi", (243, 200, 158), (18, 18, 18), (40, 40, 48),
                 (160, 20, 30), "XI JINPING"),
                (260, "putin", (244, 198, 160), (205, 195, 165), (45, 50, 64),
                 (40, 60, 130), "PUTIN"),
            ]
            f_lab8 = font(SANS_B, 8)
            for cxo, style, skin, hairc, suit, tie, name in leaders:
                draw_bust(d, sx + cxo, sy + 10, 54, 50, skin, hairc, style,
                          suit, tie=tie)
                nw = d.textlength(name, font=f_lab8)
                d.text((sx + cxo - nw / 2, sy + 62), name, font=f_lab8,
                       fill=(255, 255, 255))
        elif i == 1:  # IPO: rising office towers + arrow
            d.rectangle([sx, sy, sx + col_w, sy + scene_h], fill=(233, 240, 232))
            bars = [(28, 22, GREEN), (92, 36, (43, 140, 90)),
                    (156, 50, (27, 94, 32)), (220, 62, (21, 71, 46))]
            for bx, bh, col in bars:
                d.rectangle([sx + bx, sy + 64 - bh, sx + bx + 46, sy + 64],
                            fill=col)
                for wy in range(sy + 68 - bh, sy + 58, 10):
                    for wx in (sx + bx + 8, sx + bx + 24):
                        d.rectangle([wx, wy, wx + 6, wy + 5],
                                    fill=(255, 244, 180))
            d.line([sx + 24, sy + 48, sx + 104, sy + 34, sx + 184, sy + 20,
                    sx + 262, sy + 8], fill=RED, width=4)
            d.polygon([(sx + 262, sy + 2), (sx + 274, sy + 14), (sx + 256, sy + 16)],
                      fill=RED)
            d.text((sx + 10, sy + 6), "$", font=font(SERIF_B, 24), fill=GREEN)
            d.rectangle([sx, sy + 64, sx + col_w, sy + scene_h], fill=(52, 58, 70))
        else:  # gulf: sea, island, explosion, jet
            d.rectangle([sx, sy, sx + col_w, sy + scene_h], fill=(191, 217, 232))
            d.rectangle([sx, sy + 46, sx + col_w, sy + scene_h], fill=(127, 179, 213))
            d.polygon([(sx + 128, sy + 46), (sx + 156, sy + 34),
                       (sx + 188, sy + 46)], fill=(214, 196, 150))
            d.line([sx + 20, sy + 26, sx + 92, sy + 38], fill=RED, width=2)
            d.ellipse([sx + 18, sy + 24, sx + 24, sy + 30], fill=RED)
            d.line([sx + 297, sy + 22, sx + 226, sy + 36], fill=RED, width=2)
            d.ellipse([sx + 293, sy + 20, sx + 299, sy + 26], fill=RED)
            star(d, sx + 158, sy + 26, 21, 9, 8, (255, 176, 32))
            star(d, sx + 158, sy + 26, 11, 5, 8, (230, 60, 20))
            jx, jy = sx + 24, sy + 8
            d.polygon([(jx, jy + 5), (jx + 18, jy), (jx + 34, jy + 5),
                       (jx + 18, jy + 9)], fill=(40, 46, 60))
            d.polygon([(jx + 4, jy + 5), (jx, jy - 3), (jx + 8, jy + 2)],
                      fill=(40, 46, 60))
            d.polygon([(jx + 14, jy + 7), (jx + 10, jy + 14), (jx + 20, jy + 9)],
                      fill=(40, 46, 60))
        d.rectangle([sx, sy, sx + col_w, sy + scene_h], outline=INK, width=1)
        # kicker + headline + deck
        ky = hy + scene_h + 6
        tracked(d, (x, ky), country + "  \u00b7  " + ("DIPLOMACY" if i == 0 else
                "MARKETS" if i == 1 else "CONFLICT"),
                font(SANS_B, 11), RED, 1)
        f_h = font(SERIF_B, 19)
        lines = wrap(d, head, f_h, col_w)
        ly = ky + 18
        for ln in lines[:2]:
            d.text((x, ly), ln, font=f_h, fill=INK)
            ly += 22
        d.text((x, ly + 4), deck, font=font(SANS, 11), fill=GRAY)

    # ---- card grid: 3 x 3 big cards
    gy, row_h, col_w2, gap2 = 362, 100, 317, 12
    f_num_c = font(SANS_B, 15)
    f_ctry = font(SANS_B, 9)
    f_lab8 = font(SANS_B, 8)
    for idx, (num, country, flag, head, _lat, _lon) in enumerate(CARDS):
        r, c = divmod(idx, 3)
        x = MX + c * (col_w2 + gap2)
        y = gy + r * (row_h + 8)
        d.rectangle([x, y, x + col_w2, y + row_h], fill=PAPER, outline=INK, width=1)
        d.rectangle([x, y, x + col_w2, y + 3], fill=ACCENTS[idx % len(ACCENTS)])
        d.text((x + 8, y + 6), str(num), font=f_num_c, fill=RED)
        draw_flag(d, x + 32, y + 7, 26, 17, flag)
        d.text((x + 63, y + 10), country, font=f_ctry, fill=GRAY)
        # picture box
        px, py, pw, ph = x + 8, y + 30, 94, 62
        if num in FIGS:
            d.rectangle([px, py, px + pw, py + ph], fill=(250, 246, 235),
                        outline=INK, width=1)
            style, skin, hairc, suit, tie, label, gls, brd, shrt = FIGS[num]
            draw_bust(d, px + pw / 2, py + 3, 46, 46, skin, hairc, style,
                      suit, tie=tie, glasses=gls, beard=brd, shirt=shrt)
            lw8 = d.textlength(label, font=f_lab8)
            d.text((px + pw / 2 - lw8 / 2, py + 51), label, font=f_lab8,
                   fill=GRAY)
        elif num == 11:  # three mini busts: William, Kate, Modi
            d.rectangle([px, py, px + pw, py + ph], fill=(250, 246, 235),
                        outline=INK, width=1)
            minis = [
                (px + 17, "xi", (246, 205, 164), (30, 30, 30), (35, 42, 66),
                 None, "WILL", False, None, True),
                (px + 47, "hasina", (243, 198, 158), (110, 70, 40),
                 (0, 110, 120), None, "KATE", False, None, False),
                (px + 77, "modi", (206, 148, 100), (215, 215, 215),
                 (60, 70, 90), None, "MODI", True, (228, 228, 228), True),
            ]
            f_lab7 = font(SANS_B, 7)
            for cxo, style, skin, hairc, suit, tie, label, gls, brd, shrt in minis:
                draw_bust(d, cxo, py + 5, 26, 36, skin, hairc, style, suit,
                          tie=tie, glasses=gls, beard=brd, shirt=shrt)
                lw7 = d.textlength(label, font=f_lab7)
                d.text((cxo - lw7 / 2, py + 46), label, font=f_lab7, fill=GRAY)
        else:
            SCENES[num](d, px, py, pw, ph)
            d.rectangle([px, py, px + pw, py + ph], outline=INK, width=1)
        # headline, auto-fit to at most 3 lines
        tx, tw2 = x + 110, col_w2 - 118
        for size in (15, 14, 13, 12):
            f_head = font(SANS_B, size)
            lines = wrap(d, head, f_head, tw2)
            if len(lines) <= 3:
                break
        ly = y + 34
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += size + 4

    # ---- ALSO THAT DAY strip
    ay0, ay1 = 686, 730
    d.rectangle([MX, ay0, W - MX, ay1], fill=PAPER, outline=INK, width=1)
    d.text((MX + 12, ay0 + 7), "ALSO THAT DAY", font=font(SANS_B, 11), fill=RED)
    f_also = font(SANS, 10)
    d.text((MX + 118, ay0 + 8), ALSO_LINE1, font=f_also, fill=INK)
    d.text((MX + 12, ay0 + 25), ALSO_LINE2, font=f_also, fill=INK)

    # ---- map band: a proper, readable world map
    my0, my1 = 738, 974
    d.rectangle([MX, my0, W - MX, my1], fill=DARK)
    d.text((MX + 12, my0 + 8), "THE DAY AROUND THE WORLD",
           font=font(SANS_B, 15), fill=(246, 239, 224))
    d.text((MX + 12, my0 + 30), "RED DOTS MARK WHERE EACH STORY HAPPENED",
           font=font(SANS, 10), fill=(170, 164, 150))
    MAP_X0, MAP_X1, MAP_Y0, MAP_Y1 = 40, 984, 788, 964

    def proj(lat, lon):
        px = MAP_X0 + (lon + 180) / 360.0 * (MAP_X1 - MAP_X0)
        py = MAP_Y0 + (82 - lat) / 142.0 * (MAP_Y1 - MAP_Y0)
        return px, py

    # faint graticule
    for lon in range(-150, 151, 30):
        gx, _ = proj(0, lon)
        d.line([gx, MAP_Y0, gx, MAP_Y1], fill=(58, 58, 58), width=1)
    for lat in range(-60, 61, 30):
        _, gy2 = proj(lat, 0)
        d.line([MAP_X0, gy2, MAP_X1, gy2], fill=(58, 58, 58), width=1)

    # continent polygons, points are (lon, lat), hand-simplified coastlines
    LAND = [
        # North America
        [(-168, 66), (-158, 71), (-140, 70), (-128, 70), (-118, 72),
         (-108, 73), (-98, 73), (-94, 79), (-88, 79), (-82, 77), (-86, 72),
         (-93, 71), (-94, 68), (-88, 68), (-82, 66), (-78, 62), (-76, 59),
         (-70, 57), (-65, 54), (-64, 49), (-70, 46), (-68, 44), (-70, 41),
         (-74, 39), (-76, 35), (-79, 33), (-80, 31), (-81, 27), (-80, 25),
         (-82, 23), (-84, 20), (-87, 18), (-88, 15), (-91, 14), (-94, 16),
         (-97, 17), (-100, 18), (-104, 20), (-107, 23), (-110, 24),
         (-113, 28), (-117, 33), (-121, 35), (-124, 40), (-124, 46),
         (-128, 50), (-133, 55), (-141, 60), (-152, 58), (-158, 56),
         (-163, 58), (-166, 60)],
        # Central America (thin strip to Panama)
        [(-104, 20), (-97, 16), (-92, 15), (-88, 14), (-84, 12), (-80, 9),
         (-78, 8), (-79, 10), (-83, 13), (-87, 15), (-92, 17), (-97, 19),
         (-101, 21)],
        # Greenland
        [(-46, 60), (-52, 64), (-55, 68), (-57, 72), (-53, 75), (-47, 77),
         (-39, 79), (-31, 78), (-24, 76), (-20, 72), (-22, 68), (-27, 65),
         (-33, 62), (-40, 60)],
        # South America
        [(-79, 9), (-75, 11), (-70, 12), (-64, 11), (-60, 9), (-55, 6),
         (-52, 4), (-50, 1), (-44, -3), (-38, -5), (-35, -8), (-37, -12),
         (-39, -15), (-40, -20), (-42, -23), (-48, -27), (-52, -32),
         (-57, -34), (-62, -37), (-62, -40), (-65, -43), (-67, -47),
         (-68, -50), (-69, -52), (-68, -54), (-70, -53), (-72, -48),
         (-73, -42), (-73, -36), (-71, -28), (-70, -20), (-72, -15),
         (-76, -10), (-79, -6), (-81, -3), (-80, 1), (-79, 5)],
        # Europe
        [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (-2, 50),
         (0, 51), (3, 52), (6, 54), (8, 56), (8, 57), (10, 58), (6, 59),
         (5, 61), (8, 62), (12, 65), (16, 68), (21, 70), (27, 71),
         (33, 70), (39, 68), (45, 67), (46, 65), (42, 62), (40, 58),
         (36, 54), (34, 52), (33, 50), (36, 47), (39, 47), (38, 44),
         (35, 42), (32, 42), (29, 41), (27, 40), (24, 40), (23, 38),
         (22, 37), (20, 38), (19, 40), (16, 40), (14, 42), (12, 44),
         (9, 44), (7, 44), (3, 43), (2, 41), (0, 39), (-1, 38), (-3, 37),
         (-6, 36)],
        # Britain (slightly exaggerated so it reads at this scale)
        [(-6, 49), (-2, 51), (-1, 53), (-2, 55), (-4, 58), (-8, 59),
         (-9, 56), (-7, 53), (-5, 50)],
        # Ireland
        [(-10, 52), (-8, 52), (-6, 53), (-6, 55), (-8, 55), (-10, 54)],
        # Africa
        [(-6, 35), (-2, 35), (3, 37), (9, 37), (10, 34), (12, 34),
         (16, 32), (21, 32), (26, 32), (30, 31), (32, 31), (34, 28),
         (35, 25), (37, 22), (38, 21), (39, 17), (40, 15), (42, 12),
         (44, 11), (48, 11), (51, 12), (50, 14), (46, 10), (44, 6),
         (42, 2), (41, -2), (40, -6), (39, -10), (38, -14), (36, -18),
         (35, -21), (33, -25), (31, -28), (29, -31), (27, -33), (22, -34),
         (19, -34), (18, -33), (17, -30), (16, -26), (14, -22), (13, -17),
         (12, -12), (11, -8), (10, -4), (9, 0), (9, 3), (6, 4), (2, 6),
         (-3, 5), (-7, 4), (-11, 7), (-13, 8), (-16, 12), (-17, 15),
         (-17, 19), (-16, 22), (-15, 26), (-13, 29), (-10, 31), (-8, 33)],
        # Madagascar
        [(44, -16), (47, -15), (49, -16), (50, -18), (48, -21), (47, -24),
         (45, -25), (44, -23), (43, -20), (44, -17)],
        # Asia (Siberia, China, India triangle, SE Asia)
        [(36, 36), (33, 36), (30, 36), (27, 37), (30, 39), (33, 41),
         (36, 42), (39, 44), (41, 46), (44, 48), (46, 50), (48, 52),
         (50, 55), (53, 58), (56, 60), (59, 62), (61, 65), (60, 68),
         (65, 69), (70, 71), (76, 72), (82, 73), (88, 74), (94, 76),
         (100, 77), (106, 77), (112, 76), (118, 74), (124, 73), (130, 72),
         (136, 72), (142, 71), (148, 70), (154, 69), (160, 68), (166, 67),
         (172, 66), (178, 64), (178, 62), (171, 62), (167, 64), (164, 60),
         (161, 58), (159, 53), (156, 51), (153, 55), (149, 59), (145, 56),
         (142, 53), (142, 50), (140, 46), (138, 44), (135, 43), (132, 43),
         (129, 41), (127, 40), (124, 39), (122, 38), (121, 35), (122, 32),
         (121, 29), (120, 26), (118, 24), (114, 22), (110, 20), (108, 17),
         (107, 13), (106, 9), (104, 6), (103, 3), (101, 6), (99, 9),
         (98, 12), (96, 15), (94, 17), (92, 20), (91, 22), (89, 22),
         (88, 21), (86, 20), (84, 19), (82, 16), (80, 13), (79, 10),
         (77, 8), (76, 10), (75, 13), (73, 16), (72, 19), (70, 21),
         (67, 23), (66, 25), (62, 25), (58, 26), (56, 27), (53, 28),
         (50, 30), (48, 30), (47, 29), (44, 30), (42, 33), (40, 35),
         (38, 36)],
        # Arabia
        [(43, 12), (45, 12), (48, 14), (50, 16), (52, 19), (54, 22),
         (55, 24), (56, 26), (54, 26), (52, 25), (50, 27), (48, 29),
         (47, 30), (44, 29), (42, 28), (40, 26), (39, 23), (38, 20),
         (37, 17), (36, 15), (38, 13), (41, 12)],
        # Sumatra
        [(95, 5), (99, 2), (102, -1), (104, -3), (106, -5), (104, -4),
         (101, 0), (98, 2), (95, 4)],
        # Borneo
        [(109, 1), (111, 3), (114, 4), (117, 6), (119, 3), (118, 0),
         (116, -2), (113, -3), (110, -2), (109, 0)],
        # Java
        [(106, -6), (109, -7), (112, -7), (114, -8), (114, -9), (110, -8),
         (107, -7)],
        # Sulawesi
        [(119, 0), (120, 1), (121, 0), (120, -2), (119, -1)],
        # New Guinea
        [(131, -1), (134, -2), (137, -2), (140, -3), (143, -4), (146, -6),
         (148, -8), (146, -8), (142, -6), (138, -4), (134, -3), (131, -2)],
        # Japan (Honshu arc)
        [(130, 31), (132, 33), (134, 34), (136, 35), (138, 36), (140, 37),
         (141, 39), (141, 41), (142, 43), (144, 44), (143, 42), (141, 40),
         (140, 38), (138, 36), (135, 34), (132, 32)],
        # Philippines
        [(120, 13), (121, 14), (122, 13), (121, 12)],
        [(121, 16), (122, 17), (122, 18), (121, 17)],
        # Australia
        [(113, -22), (114, -26), (114, -30), (115, -33), (117, -35),
         (120, -34), (124, -33), (128, -32), (131, -32), (134, -33),
         (136, -35), (138, -35), (139, -37), (141, -38), (144, -38),
         (147, -38), (150, -37), (152, -34), (153, -30), (153, -26),
         (151, -22), (149, -20), (146, -19), (144, -16), (143, -13),
         (142, -11), (141, -13), (140, -16), (139, -18), (136, -16),
         (136, -12), (134, -12), (132, -11), (130, -13), (127, -14),
         (124, -16), (122, -17), (120, -19), (117, -20), (114, -21)],
        # New Zealand (North + South Island, exaggerated ~2x to be visible)
        [(170, -34), (174, -36), (178, -37), (177, -40), (174, -42),
         (171, -40), (169, -37)],
        [(164, -46), (167, -44), (170, -42), (173, -41), (171, -40),
         (168, -42), (165, -44)],
    ]
    for poly in LAND:
        d.polygon([proj(lat, lon) for lon, lat in poly],
                  fill=(232, 224, 200), outline=(168, 158, 130))

    f_dot = font(SANS_B, 9)
    for story in HEROES + CARDS:
        num, lat, lon = story[0], story[-2], story[-1]
        px, py = proj(lat, lon)
        dx, dy = DOT_NUDGE.get(num, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=(232, 224, 200), width=1)
        cx, cy = px + dx, py + dy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        lw = d.textlength(label, font=f_dot)
        d.text((cx - lw / 2, cy - 5), label, font=f_dot, fill=(255, 255, 255))

    # footer
    f_f = font(SANS, 10)
    foot = ("SOURCES: REUTERS \u00b7 AP \u00b7 BBC \u00b7 AFP \u00b7 PAHO \u00b7 CDC  "
            "\u2014  ALL STORIES FROM WEDNESDAY 18 NOVEMBER 2026")
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, 984), foot, font=f_f, fill=GRAY)

    out = os.environ.get("OUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
