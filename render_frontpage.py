#!/usr/bin/env python3
"""Render the 19 November 2026 front page (1024x1024 PNG).

A newspaper front page for the make.fun news-image-20261119 bounty: six
stories verified against live reporting on 19 Nov 2026, each with a small
flat illustration drawn here with PIL primitives plus a headline and deck.
Everything is drawn in this script, so the output is deterministic.
Usage: python3 render_frontpage.py [out.png]
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
INK = (22, 22, 22)
RED = (176, 32, 32)
GREY = (98, 95, 86)
BODY = (56, 54, 48)
RULE = (22, 22, 22)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, width, limit=None):
    """Greedy word wrap; returns lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if limit is not None:
        lines = lines[:limit]
    return lines


def para(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def rule(self, y, thick=2):
        self.d.line([(30, y), (W - 30, y)], fill=RULE, width=thick)

    def kicker(self, x, y, text, size=19):
        f = font(SANS_B, size)
        self.d.text((x, y), text, font=f, fill=RED)
        return f

    def headline(self, x, y, text, width, size, max_lines, leading):
        f = font(SERIF_B, size)
        lines = wrap_lines(self.d, text, f, width, max_lines)
        return para(self.d, lines, x, y, f, INK, leading)

    def deck(self, x, y, text, width, size, max_lines, leading, fill=BODY):
        f = font(SERIF, size)
        lines = wrap_lines(self.d, text, f, width, max_lines)
        return para(self.d, lines, x, y, f, fill, leading)


def sky_bands(d, box, colors):
    """Horizontal gradient bands across box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    n = len(colors)
    band_h = (y1 - y0) / n
    for i, c in enumerate(colors):
        d.rectangle([x0, y0 + i * band_h, x1, y0 + (i + 1) * band_h + 1], fill=c)


def art_palace(p, box):
    """Peace Palace, The Hague: pediment, columns, steps, lawn."""
    d = p.d
    x0, y0, x1, y1 = box
    sky_bands(d, box, [(178, 196, 214), (196, 208, 220), (214, 220, 224)])
    d.rectangle([x0, y1 - 26, x1, y1], fill=(148, 164, 128))
    d.rectangle([x0, y1 - 44, x1, y1 - 26], fill=(206, 198, 180))
    d.rectangle([x0, y1 - 52, x1, y1 - 44], fill=(222, 214, 196))
    d.rectangle([x0 + 30, y0 + 118, x1 - 30, y1 - 52], fill=(196, 186, 164))
    d.rectangle([x0 + 30, y0 + 118, x1 - 30, y0 + 128], fill=(168, 156, 132))
    d.polygon([(x0 + 150, y0 + 118), (x1 - 150, y0 + 118),
               ((x0 + x1) // 2, y0 + 82)], fill=(176, 164, 140))
    cx = (x0 + x1) // 2
    d.rectangle([cx - 26, y0 + 44, cx + 26, y0 + 86], fill=(168, 156, 132))
    d.ellipse([cx - 34, y0 + 18, cx + 34, y0 + 52], fill=(96, 112, 128))
    d.rectangle([cx - 3, y0 + 6, cx + 3, y0 + 20], fill=(96, 112, 128))
    for i in range(6):
        cx0 = x0 + 78 + i * 58
        d.rectangle([cx0, y0 + 140, cx0 + 20, y1 - 52], fill=(228, 220, 202))
        d.rectangle([cx0 - 3, y0 + 136, cx0 + 23, y0 + 142], fill=(228, 220, 202))
    d.rectangle([cx - 18, y0 + 196, cx + 18, y1 - 52], fill=(74, 66, 58))
    d.ellipse([cx - 18, y0 + 178, cx + 18, y0 + 200], fill=(74, 66, 58))
    for fx in (x0 + 52, x1 - 52):
        d.line([(fx, y0 + 96), (fx, y0 + 150)], fill=INK, width=3)
        d.rectangle([fx, y0 + 96, fx + 26, y0 + 110], fill=(38, 80, 160))


def art_flags(p, box):
    """Three flags over a Shenzhen skyline: China, Russia, USA."""
    d = p.d
    x0, y0, x1, y1 = box
    sky_bands(d, box, [(52, 74, 108), (74, 96, 128), (110, 128, 148)])
    towers = [(8, 44, 34, 96), (40, 26, 62, 110), (68, 56, 88, 110),
              (216, 34, 240, 110), (246, 52, 268, 110), (274, 20, 300, 110)]
    for tx, ty, tx1, ty1 in towers:
        d.rectangle([x0 + tx, y0 + ty, x0 + tx1, y1], fill=(30, 42, 60))
        for wy in range(y0 + ty + 8, y1 - 6, 12):
            for wx in range(x0 + tx + 5, x0 + tx1 - 4, 10):
                if (wx + wy) % 23 < 9:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(240, 200, 90))
    poles = [x0 + 108, x0 + 156, x0 + 204]
    for px in poles:
        d.line([(px, y0 + 14), (px, y1 - 8)], fill=(230, 228, 220), width=3)
    d.rectangle([poles[0], y0 + 16, poles[0] + 36, y0 + 40], fill=(222, 40, 30))
    d.polygon(star_points(poles[0] + 10, y0 + 28, 7, 3), fill=(250, 220, 60))
    d.rectangle([poles[1], y0 + 16, poles[1] + 36, y0 + 24], fill=(240, 240, 238))
    d.rectangle([poles[1], y0 + 24, poles[1] + 36, y0 + 32], fill=(30, 70, 170))
    d.rectangle([poles[1], y0 + 32, poles[1] + 36, y0 + 40], fill=(210, 30, 30))
    for s in range(7):
        c = (200, 40, 44) if s % 2 == 0 else (240, 240, 238)
        d.rectangle([poles[2], y0 + 16 + s * 3, poles[2] + 36, y0 + 19 + s * 3], fill=c)
    d.rectangle([poles[2], y0 + 16, poles[2] + 15, y0 + 28], fill=(36, 56, 120))
    for sx in range(3):
        for sy in range(2):
            d.ellipse([poles[2] + 3 + sx * 5, y0 + 18 + sy * 5,
                       poles[2] + 5 + sx * 5, y0 + 20 + sy * 5], fill=(255, 255, 255))


def art_vice(p, box):
    """Vice City sunset: gradient sky, sun, palms, skyline, water."""
    d = p.d
    x0, y0, x1, y1 = box
    sky_bands(d, box, [(58, 32, 96), (122, 52, 110), (214, 96, 110),
                       (248, 158, 92), (252, 206, 130)])
    cx = (x0 + x1) // 2
    d.ellipse([cx - 34, y0 + 18, cx + 34, y0 + 86], fill=(255, 226, 150))
    for bx, bw, bh in [(6, 30, 34), (40, 22, 52), (66, 34, 28), (104, 26, 44),
                       (208, 30, 40), (242, 24, 58), (270, 34, 30)]:
        d.rectangle([x0 + bx, y1 - 34 - bh, x0 + bx + bw, y1 - 22], fill=(40, 24, 64))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(30, 60, 96))
    d.line([(x0 + 20, y1 - 12), (x1 - 20, y1 - 12)], fill=(255, 226, 150), width=2)
    for px, lean in [(x0 + 150, -14), (x0 + 176, 10)]:
        d.line([(px, y1 - 22), (px + lean, y0 + 52)], fill=(28, 16, 44), width=5)
        tx, ty = px + lean, y0 + 52
        for ang in (-70, -35, 0, 35, 70):
            a = math.radians(ang - 90)
            ex, ey = tx + 26 * math.cos(a), ty + 14 * math.sin(a) + 6
            d.line([(tx, ty), (ex, ey)], fill=(28, 16, 44), width=4)


def art_voyager(p, box):
    """Deep space: stars, gold probe with dish, distance arc."""
    d = p.d
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(8, 12, 30))
    rnd = random.Random(20261119)
    for _ in range(46):
        sx = rnd.randint(x0 + 4, x1 - 4)
        sy = rnd.randint(y0 + 4, y1 - 4)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 235, 225))
    # dotted trajectory from Earth toward the probe (stays inside the panel)
    for i in range(9):
        dx = x0 + 44 + i * 13
        dy = y0 + 82 - i * 3
        d.ellipse([dx - 1, dy - 1, dx + 1, dy + 1], fill=(140, 160, 200))
    cx, cy = x0 + 196, y0 + 56
    d.polygon([(cx - 26, cy - 8), (cx + 6, cy - 8), (cx + 6, cy + 10),
               (cx - 26, cy + 10)], fill=(212, 175, 90))
    d.line([(cx + 6, cy - 2), (cx + 34, cy - 12)], fill=(212, 175, 90), width=3)
    d.ellipse([cx + 26, cy - 30, cx + 62, cy + 6], fill=(238, 205, 120))
    d.ellipse([cx + 32, cy - 24, cx + 56, cy + 0], fill=(180, 140, 60))
    d.line([(cx - 26, cy + 2), (cx - 52, cy + 14)], fill=(180, 180, 170), width=3)
    d.rectangle([cx - 60, cy + 10, cx - 48, cy + 22], fill=(200, 200, 190))
    d.ellipse([x0 + 16, y0 + 74, x0 + 34, y0 + 92], fill=(70, 130, 200))
    d.arc([x0 + 16, y0 + 74, x0 + 34, y0 + 92], start=300, end=120,
          fill=(120, 200, 120), width=2)


def art_stamp(p, box):
    """A document stamped SANCTIONED in red."""
    d = p.d
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 220, 206))
    d.rectangle([x0 + 56, y0 + 12, x1 - 56, y1 - 12], fill=(252, 250, 244))
    d.rectangle([x0 + 56, y0 + 12, x1 - 56, y1 - 12], outline=(150, 146, 134))
    for i, ly in enumerate(range(y0 + 26, y0 + 62, 10)):
        ln = x1 - 96 if i % 2 else x1 - 76
        d.line([(x0 + 70, ly), (ln, ly)], fill=(170, 166, 152), width=2)
    layer = Image.new("RGBA", (180, 52), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([4, 4, 176, 48], outline=(176, 32, 32), width=4)
    ld.text((90, 26), "SANCTIONED", font=font(SANS_B, 20),
            fill=(176, 32, 32), anchor="mm")
    layer = layer.rotate(-11, expand=True, resample=Image.BICUBIC)
    p.img.paste(layer, (x0 + 64, y0 + 28), layer)


def art_storm(p, box):
    """Cyclone spiral over a dark sea, coast at the bottom."""
    d = p.d
    x0, y0, x1, y1 = box
    sky_bands(d, box, [(36, 64, 84), (52, 88, 104), (70, 110, 120)])
    cx, cy = x0 + 150, y0 + 52
    for r, a0, a1 in [(50, 20, 300), (40, 80, 340), (30, 140, 40),
                      (20, 200, 100), (11, 260, 160)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=a0, end=a1,
              fill=(235, 240, 240), width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(235, 240, 240))
    for rx in range(x0 + 14, x1 - 10, 26):
        d.line([(rx, y0 + 8), (rx - 8, y0 + 30)], fill=(200, 214, 220), width=2)
    d.polygon([(x0, y1), (x0, y1 - 18), (x0 + 90, y1 - 26), (x0 + 190, y1 - 16),
               (x1, y1 - 24), (x1, y1)], fill=(214, 196, 150))
    d.rectangle([x0, y1 - 4, x1, y1], fill=(150, 170, 190))


LEAD = {
    "kicker": "THE HAGUE  —  LEAD STORY",
    "headline": "World Court Rules on Rohingya Genocide",
    "deck": ("Judges in The Hague rule on whether Myanmar's 2017 campaign "
             "against the Rohingya was genocide."),
    "deck2": "The Gambia brought the case in 2019.",
    "art": art_palace,
}

CARDS = [
    {"kicker": "GEOPOLITICS", "art": art_flags,
     "headline": "Xi, Putin and Trump Meet in First Trilateral",
     "deck": "The three leaders meet in Shenzhen on APEC's sidelines."},
    {"kicker": "CULTURE", "art": art_vice,
     "headline": "Vice City Opens as GTA VI Rolls Out Worldwide",
     "deck": "Unlocks at midnight, New Zealand first."},
    {"kicker": "SPACE", "art": art_voyager,
     "headline": "Voyager 1, One Light-Day From Earth",
     "deck": "NASA confirms the 1977 probe is a full light-day out."},
    {"kicker": "DIPLOMACY", "art": art_stamp,
     "headline": "Australia Sanctions Israeli Settlers",
     "deck": "Canberra targets settlement growth in the West Bank."},
    {"kicker": "WEATHER", "art": art_storm,
     "headline": "Cyclone Akvan Bears Down on India",
     "deck": "Landfall expected between Machilipatnam and Puri."},
]

ALSO = [
    "US House Democrats order Trump allies to preserve records",
    "Saudi Arabia: danger passed in three southern cities",
    "Bacterial toxin tied to early bowel-cancer surge",
    "EU to pause long-term UK talks over Brexit",
]


def build():
    p = Page()
    d = p.d
    # masthead
    f_mast = font(SERIF_B, 92)
    d.text((W // 2, 14), "THE WORLD", font=f_mast, fill=INK, anchor="ma")
    f_date = font(SANS_B, 25)
    d.text((W // 2, 112), "THURSDAY, 19 NOVEMBER 2026  •  SIX STORIES, ONE DAY",
           font=f_date, fill=INK, anchor="ma")
    p.rule(142, 3)
    p.rule(147, 1)
    # lead story
    lx0, ly0, lx1, ly1 = 30, 158, 530, 446
    LEAD["art"](p, (lx0, ly0, lx1, ly1))
    d.rectangle([lx0, ly0, lx1, ly1], outline=RULE, width=2)
    tx = 552
    p.kicker(tx, 162, LEAD["kicker"], 21)
    y = p.headline(tx, 192, LEAD["headline"], 442, 42, 3, 48)
    y = p.deck(tx, y + 10, LEAD["deck"], 442, 22, 3, 26)
    p.deck(tx, y + 8, LEAD["deck2"], 442, 19, 1, 24, fill=GREY)
    p.rule(456, 2)
    # grid rows
    col_x = [30, 358, 686]
    col_w = 308
    row_y = [468, 732]
    img_h = 104
    for idx, card in enumerate(CARDS):
        r, c = divmod(idx, 3)
        x = col_x[c]
        y = row_y[r]
        box = (x, y, x + col_w, y + img_h)
        card["art"](p, box)
        d.rectangle(box, outline=RULE, width=1)
        y2 = y + img_h + 6
        p.kicker(x, y2, card["kicker"], 18)
        y2 = p.headline(x, y2 + 22, card["headline"], col_w, 24, 3, 28)
        p.deck(x, y2 + 4, card["deck"], col_w, 19, 2, 22)
    # ALSO box in the last grid cell
    ax, ay = col_x[2], row_y[1]
    d.rectangle([ax, ay, ax + col_w, ay + 256], outline=INK, width=2)
    d.text((ax + 14, ay + 12), "ALSO ON 19 NOV", font=font(SANS_B, 20), fill=RED)
    yy = ay + 46
    for item in ALSO:
        f = font(SANS, 17)
        lines = wrap_lines(d, item, f, col_w - 34, 2)
        d.text((ax + 14, yy), "—", font=f, fill=INK)
        yy = para(d, lines, ax + 34, yy, f, INK, 21)
        yy += 8
    # footer
    d.text((W // 2, 998),
           "Sources: Reuters, BBC, Le Monde, The West, NASA, Rockstar Games — all events Thursday 19 November 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")
    return p.img


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {img.size} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
