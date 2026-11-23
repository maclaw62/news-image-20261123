#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: a one-page front page summing up
Monday 23 November 2026 world news. Run on the build machine (PIL is NOT
available in the grading sandbox); the entry program main.py only copies
the finished entry.png to /output. Output: 1024x1024 PNG, <= 1 MiB."""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 233)      # warm newsprint
INK = (26, 26, 26)
RULE = (26, 26, 26)
RED = (178, 34, 34)
GREY = (105, 105, 105)
TEAL = (14, 124, 123)
GREEN = (30, 132, 73)
NAVY = (31, 56, 100)
BLUE = (36, 86, 166)
DARKRED = (176, 58, 46)
PANEL = (232, 226, 212)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
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


def draw_text_block(draw, x, y, text, fnt, max_w, fill, leading=1.22):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------------------------------------------------------- icons
def icon_globe_crack(draw, x, y, s, color=TEAL):
    """A globe with a crack through it (climate talks collapse)."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=7)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(223, 238, 235))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=7)
    # meridians / parallels
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=color, width=3)
    # crack: jagged line top-right to bottom-left
    pts = [(cx + r * 0.55, cy - r * 0.95), (cx + r * 0.25, cy - r * 0.45),
           (cx + r * 0.55, cy - r * 0.05), (cx + r * 0.1, cy + r * 0.4),
           (cx + r * 0.35, cy + r * 0.75), (cx - r * 0.1, cy + r * 0.95)]
    draw.line(pts, fill=RED, width=7, joint="curve")
    # small sun
    sx, sy, sr = x + s - 34, y + 18, 16
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(232, 168, 32))
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
        draw.line([sx + dx * (sr + 3), sy + dy * (sr + 3),
                   sx + dx * (sr + 11), sy + dy * (sr + 11)],
                  fill=(232, 168, 32), width=4)


def icon_chip_arrow(draw, x, y, s, color=GREEN):
    """A microchip with a rising arrow (Nvidia CEO back, shares +30%)."""
    m = 14
    draw.rounded_rectangle([x + m, y + m + 18, x + s - m, y + s - m - 6],
                           radius=10, fill=INK)
    # pins
    for i in range(4):
        px = x + m + 14 + i * ((s - 2 * m - 28) // 3)
        draw.line([px, y + m + 18, px, y + m + 6], fill=INK, width=5)
        draw.line([px, y + s - m - 6, px, y + s - m + 6], fill=INK, width=5)
    for i in range(3):
        py = y + m + 18 + 18 + i * ((s - m - 6 - (m + 18) - 36) // 2)
        draw.line([x + m, py, x + m - 12, py], fill=INK, width=5)
        draw.line([x + s - m, py, x + s - m + 12, py], fill=INK, width=5)
    draw.rectangle([x + s // 2 - 16, y + s // 2 - 6, x + s // 2 + 16, y + s // 2 + 26],
                   fill=(232, 168, 32))
    # rising arrow
    ax0, ay0 = x + 16, y + s - 34
    ax1, ay1 = x + s - 18, y + 8
    draw.line([ax0, ay0, x + s // 2, y + s // 2 + 6, ax1, ay1], fill=color, width=9, joint="curve")
    draw.polygon([(ax1, ay1), (ax1 - 22, ay1 + 2), (ax1 - 2, ay1 + 22)], fill=color)


def icon_ship_drone(draw, x, y, s, color=NAVY):
    """A warship with a drone above and a blast star (sea-drone strike)."""
    # sea
    draw.line([x + 8, y + s - 26, x + s - 8, y + s - 26], fill=color, width=4)
    draw.line([x + 24, y + s - 16, x + s - 24, y + s - 16], fill=color, width=3)
    # hull
    hull = [(x + 18, y + s - 52), (x + s - 22, y + s - 52),
            (x + s - 40, y + s - 28), (x + 34, y + s - 28)]
    draw.polygon(hull, fill=color)
    # superstructure + mast
    draw.rectangle([x + s // 2 - 8, y + s - 84, x + s // 2 + 26, y + s - 52], fill=color)
    draw.rectangle([x + s // 2 - 34, y + s - 70, x + s // 2 + 2, y + s - 52], fill=color)
    draw.line([x + s // 2 + 9, y + s - 84, x + s // 2 + 9, y + s - 104], fill=color, width=5)
    # drone (quadcopter)
    dx, dy = x + s - 40, y + 22
    draw.ellipse([dx - 10, dy - 7, dx + 10, dy + 7], fill=INK)
    for ox, oy in [(-18, -10), (18, -10), (-18, 10), (18, 10)]:
        draw.line([dx, dy, dx + ox, dy + oy], fill=INK, width=3)
        draw.line([dx + ox - 8, dy + oy, dx + ox + 8, dy + oy], fill=INK, width=3)
    # blast starburst at the bow
    bx, by = x + 30, y + s - 66
    star = []
    import math
    for i in range(12):
        ang = math.pi * i / 6
        rr = 20 if i % 2 == 0 else 8
        star.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    draw.polygon(star, fill=(232, 120, 32))
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 220, 90))


def icon_capitol(draw, x, y, s, color=BLUE):
    """A capitol dome with a ballot check (US House majority)."""
    cx = x + s // 2
    # dome: top half of an ellipse + drum
    draw.pieslice([cx - 30, y + 8, cx + 30, y + 52], 180, 360, fill=color)
    draw.rectangle([cx - 30, y + 30, cx + 30, y + 44], fill=color)
    # finial
    draw.line([cx, y + 8, cx, y + 1], fill=color, width=4)
    draw.ellipse([cx - 4, y - 2, cx + 4, y + 6], fill=color)
    # architrave
    draw.rectangle([x + 18, y + 44, x + s - 18, y + 56], fill=color)
    # columns
    for i in range(5):
        ccx = x + 30 + i * ((s - 60) // 4)
        draw.rectangle([ccx - 5, y + 56, ccx + 5, y + 92], fill=color)
    # steps
    draw.rectangle([x + 14, y + 92, x + s - 14, y + 102], fill=color)
    draw.rectangle([x + 22, y + 102, x + s - 22, y + 110], fill=color)
    # checkmark badge
    bx, by, br = x + s - 24, y + s - 22, 15
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=GREEN)
    draw.line([(bx - 8, by), (bx - 2, by + 7), (bx + 9, by - 7)], fill=(255, 255, 255),
              width=5, joint="curve")


def icon_chart_down(draw, x, y, s, color=DARKRED):
    """A falling line chart (Asian chip stocks slide)."""
    # axes
    draw.line([x + 16, y + 14, x + 16, y + s - 20], fill=INK, width=5)
    draw.line([x + 16, y + s - 20, x + s - 12, y + s - 20], fill=INK, width=5)
    # falling line
    pts = [(x + 24, y + 26), (x + s * 0.38, y + s * 0.34),
           (x + s * 0.55, y + s * 0.30), (x + s * 0.72, y + s * 0.62),
           (x + s - 20, y + s - 34)]
    draw.line(pts, fill=color, width=8, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=color)
    # arrowhead at the end
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 20, ey - 2), (ex - 2, ey - 20)], fill=color)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead
    d.text((M, 26), "THE WORLD IN ONE IMAGE", font=font(SANS_BOLD, 22), fill=GREY)
    tag = "MONDAY"
    d.text((W - M - d.textlength(tag, font=font(SANS_BOLD, 22)), 26), tag,
           font=font(SANS_BOLD, 22), fill=GREY)
    d.line([M, 58, W - M, 58], fill=RULE, width=2)
    date_f = font(SERIF_BOLD, 62)
    date = "23 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 66), date, font=date_f, fill=INK)
    d.line([M, 142, W - M, 142], fill=RULE, width=5)
    d.line([M, 150, W - M, 150], fill=RED, width=2)

    # ---- lead story: COP31
    lx, ly = M, 172
    lw = 600
    d.text((lx, ly), "CLIMATE  ·  ANTALYA, TURKEY", font=font(SANS_BOLD, 23), fill=RED)
    y = ly + 34
    head_f = font(SERIF_BOLD, 64)
    for ln in ["COP31 ENDS", "WITH NO DEAL"]:
        d.text((lx, y), ln, font=head_f, fill=INK)
        y += 72
    y += 6
    y = draw_text_block(d, lx, y,
                        "The longest UN climate summit in history collapses. "
                        "Nations split over fossil fuels and finance, with no "
                        "new deal to cut emissions.",
                        font(SANS, 26), lw, INK)
    # lead illustration panel
    px0, py0, px1, py1 = 672, 172, W - M, 440
    d.rounded_rectangle([px0, py0, px1, py1], radius=14, fill=PANEL)
    icon_globe_crack(d, px0 + 63, py0 + 12, 190)
    cap_f = font(SANS_BOLD, 21)
    cap = "TALKS COLLAPSE"
    d.text((px0 + (px1 - px0 - d.textlength(cap, font=cap_f)) / 2, py1 - 38),
           cap, font=cap_f, fill=TEAL)

    # ---- divider
    d.line([M, 466, W - M, 466], fill=RULE, width=3)

    # ---- secondary grid 2x2
    cells = [
        ("TECH  ·  NVIDIA", "Huang returns as Nvidia CEO",
         "Back 11 days after resigning; shares jump 30%.",
         icon_chip_arrow, GREEN),
        ("WAR  ·  LIBYA", "Ukraine drones hit Russian warship",
         "Sea drones hit Russian ships at Benghazi and in the Baltic.",
         icon_ship_drone, NAVY),
        ("USA  ·  POLITICS", "Democrats win House majority",
         "Recount win in North Carolina; largest majority since 1992.",
         icon_capitol, BLUE),
        ("MARKETS  ·  ASIA", "Asian chip stocks slide on AI fears",
         "Seoul's Kospi falls 3.3% as the AI sell-off spreads.",
         icon_chart_down, DARKRED),
    ]
    gx, gy = M, 482
    cw, chh, gap = 468, 164, 10
    for i, (kicker, head, summ, icon, color) in enumerate(cells):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (chh + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + chh], radius=12,
                            outline=(210, 203, 186), width=2)
        icon(d, cx + 12, cy + 20, 124, color)
        tx = cx + 150
        d.text((tx, cy + 12), kicker, font=font(SANS_BOLD, 19), fill=color)
        y = draw_text_block(d, tx, cy + 36, head, font(SANS_BOLD, 24), cw - 162, INK,
                            leading=1.12)
        draw_text_block(d, tx, y + 4, summ, font(SANS, 20), cw - 162, (60, 60, 60),
                        leading=1.18)

    # ---- also today strip
    ay = 832
    d.line([M, ay, W - M, ay], fill=RULE, width=3)
    d.text((M, ay + 12), "ALSO TODAY", font=font(SANS_BOLD, 21), fill=RED)
    also = [
        "Trump warns Iran strikes could resume after New Year",
        "CrowdStrike to buy Zscaler in a $44bn stock deal",
        "Indonesia factory fire toll reaches 24",
        "Mexico captures \u201cEl Chapo Isidro,\u201d an FBI most-wanted fugitive",
    ]
    ayy = ay + 44
    for i, item in enumerate(also):
        ix = M + (i % 2) * 476
        iy = ayy + (i // 2) * 56
        d.ellipse([ix, iy + 8, ix + 9, iy + 17], fill=RED)
        draw_text_block(d, ix + 18, iy, item, font(SANS, 21), 440, INK, leading=1.1)

    # ---- footer
    d.line([M, 986, W - M, 986], fill=(210, 203, 186), width=2)
    foot = "All stories reported on Monday 23 November 2026  ·  Sources: Reuters, AP, Dow Jones, Al Jazeera"
    ff = font(SANS, 19)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 992), foot, font=ff, fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {img.size} {size} bytes (limit 1048576)")


if __name__ == "__main__":
    main()
