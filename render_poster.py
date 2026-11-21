#!/usr/bin/env python3
"""Render VELMARA, a vintage travel poster for a place that isn't there.

A sunset coast where the sea falls upward into the sky. Drawn with Pillow
only; run once locally to produce entry.png (1024x1024, under 1 MiB).
The graded program (main.ts) only copies the finished image.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
SKY_TOP = (26, 32, 66)
SKY_MID = (94, 74, 120)
HORIZON = (242, 166, 90)
SEA_TOP = (16, 96, 104)
SEA_BOT = (7, 46, 62)
SUN = (247, 201, 72)
SUN_CORE = (255, 228, 150)
CREAM = (247, 232, 200)
CORAL = (232, 106, 74)
CLIFF_DARK = (30, 24, 46)
CLIFF_MID = (56, 42, 74)
CLIFF_LIT = (146, 90, 104)
FALL = (178, 226, 222)
FALL_DEEP = (120, 196, 198)
FOAM = (240, 248, 244)
BIRD = (24, 26, 54)

DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, x0, y0, x1, y1, top, bot):
    """Vertical gradient band, one horizontal line per row."""
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bot, (y - y0) / span))


def tracked_width(font, text, tracking):
    w = 0
    for ch in text:
        w += font.getlength(ch) + tracking
    return w - tracking


def draw_tracked(draw, cx, y, text, font, fill, tracking):
    """Draw letterspaced text centred on cx."""
    total = tracked_width(font, text, tracking)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + tracking


def bird(draw, cx, cy, s, fill):
    """A tiny two-arc gull."""
    draw.arc([cx - s, cy - s // 2, cx, cy + s // 2], 200, 340, fill=fill, width=3)
    draw.arc([cx, cy - s // 2, cx + s, cy + s // 2], 200, 340, fill=fill, width=3)


def main():
    img = Image.new("RGB", (W, H), SKY_TOP)
    d = ImageDraw.Draw(img)

    # --- sky: indigo dusk melting into a peach horizon --------------------
    vgrad(d, 0, 0, W, 430, SKY_TOP, SKY_MID)
    vgrad(d, 0, 430, W, 640, SKY_MID, HORIZON)

    # --- stars fading in near the top -------------------------------------
    rng = random.Random(20261121)
    for _ in range(90):
        x = rng.randint(20, W - 20)
        y = rng.randint(16, 300)
        r = rng.choice([1, 1, 2])
        a = 200 - y // 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=(240, 235, 220))

    # --- sun: big low gold disc with a soft halo --------------------------
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    sx, sy, sr = 712, 298, 108
    for i, (rad, alpha) in enumerate([(210, 26), (175, 40), (145, 60)]):
        g.ellipse([sx - rad, sy - rad, sx + rad, sy + rad],
                  fill=SUN + (alpha,))
    g.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SUN + (255,))
    g.ellipse([sx - sr + 26, sy - sr + 26, sx + sr - 26, sy + sr - 26],
              fill=SUN_CORE + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)

    # --- distant headland, a dark roll along the horizon ------------------
    d.polygon([(0, 640), (0, 596), (120, 580), (260, 604), (420, 586),
               (600, 606), (760, 588), (900, 602), (1024, 590), (1024, 640)],
              fill=(52, 40, 72))

    # --- sea: teal darkening toward the viewer ----------------------------
    vgrad(d, 0, 640, W, H, SEA_TOP, SEA_BOT)

    # --- wave strokes ------------------------------------------------------
    for row, yy in enumerate(range(690, 1000, 42)):
        tone = lerp(SEA_TOP, (150, 210, 205), 0.25 + 0.05 * (row % 3))
        for k in range(3):
            x0 = 60 + k * 340 + (row % 2) * 90
            d.arc([x0, yy, x0 + 190, yy + 26], 180, 360, fill=tone, width=3)

    # --- the rising fall: sea water climbing back into the sky ------------
    # A tapering ribbon, S-curved, from the sea (wide) to the sky (narrow).
    left, right = [], []
    for t in range(0, 101):
        y = 700 - t * 5.1
        drift = 26 * math.sin(t / 100 * math.pi * 0.9)
        half = 78 - t * 0.55
        left.append((512 + drift - half, y))
        right.append((512 + drift + half, y))
    d.polygon(left + right[::-1], fill=FALL_DEEP)
    # Bright core of the falling-up water.
    left2, right2 = [], []
    for t in range(0, 101):
        y = 700 - t * 5.1
        drift = 26 * math.sin(t / 100 * math.pi * 0.9)
        half = (78 - t * 0.55) * 0.55
        left2.append((512 + drift - half, y))
        right2.append((512 + drift + half, y))
    d.polygon(left2 + right2[::-1], fill=FALL)
    # Streaks inside the ribbon.
    for off in (-34, -12, 10, 30):
        pts = []
        for t in range(0, 101, 4):
            y = 700 - t * 5.1
            drift = 26 * math.sin(t / 100 * math.pi * 0.9)
            pts.append((512 + drift + off, y))
        d.line(pts, fill=FOAM, width=4)
    # Droplets breaking free as the water climbs.
    for t in range(55, 101, 4):
        y = 700 - t * 5.1
        drift = 26 * math.sin(t / 100 * math.pi * 0.9)
        r = max(2, 9 - t // 14)
        dx = rng.randint(-46, 46)
        d.ellipse([512 + drift + dx - r, y - r, 512 + drift + dx + r,
                   y + r], fill=FOAM)
    # A pointed tip where the rising water dissolves into the sky.
    tip_x = 512 + 26 * math.sin(math.pi * 0.9)
    d.polygon([(tip_x - 23, 192), (tip_x + 23, 192), (tip_x, 148)], fill=FALL)
    d.polygon([(tip_x - 12, 192), (tip_x + 12, 192), (tip_x, 158)], fill=FOAM)
    for k in range(14):
        dx = rng.randint(-70, 70)
        dy = rng.randint(120, 185)
        r = rng.randint(2, 5)
        d.ellipse([tip_x + dx - r, dy - r, tip_x + dx + r, dy + r], fill=FOAM)
    # Foam where the fall leaves the sea.
    for k in range(9):
        fx = 430 + k * 20 + rng.randint(-6, 6)
        fr = rng.randint(10, 20)
        d.ellipse([fx - fr, 690 - fr // 2, fx + fr, 690 + fr // 2], fill=FOAM)

    # --- cliffs: layered headlands left and right -------------------------
    def cliff(points, strata):
        d.polygon(points, fill=CLIFF_DARK)
        for i, (y0, y1, tone) in enumerate(strata):
            band = [(x, y) for (x, y) in points if y0 <= y <= y1]
            if len(band) >= 2:
                d.polygon(band + [(points[-1][0], y1), (points[0][0], y1)],
                          fill=tone)

    left_pts = [(0, 1024), (0, 470), (90, 430), (170, 470), (230, 520),
                (300, 560), (330, 640), (300, 760), (210, 900), (120, 1024)]
    d.polygon(left_pts, fill=CLIFF_DARK)
    d.polygon([(0, 470), (90, 430), (170, 470), (230, 520), (300, 560),
               (330, 640), (330, 600), (250, 520), (160, 460), (60, 440)],
              fill=CLIFF_MID)
    d.line([(0, 470), (90, 430), (170, 470), (230, 520), (300, 560)],
           fill=CLIFF_LIT, width=5)

    right_pts = [(1024, 1024), (1024, 500), (950, 460), (880, 500),
                 (820, 560), (790, 660), (830, 780), (900, 900),
                 (960, 1024)]
    d.polygon(right_pts, fill=CLIFF_DARK)
    d.polygon([(1024, 500), (950, 460), (880, 500), (820, 560), (790, 660),
               (800, 620), (860, 540), (930, 490), (1024, 470)],
              fill=CLIFF_MID)
    d.line([(1024, 500), (950, 460), (880, 500), (820, 560), (790, 660)],
           fill=CLIFF_LIT, width=5)
    # A lone pine on the right cliff.
    px, py = 905, 512
    d.polygon([(px, py - 64), (px - 26, py), (px + 26, py)], fill=(20, 40, 30))
    d.polygon([(px, py - 92), (px - 18, py - 38), (px + 18, py - 38)],
              fill=(26, 52, 36))
    d.rectangle([px - 3, py, px + 3, py + 14], fill=(40, 26, 20))

    # --- birds -------------------------------------------------------------
    for (bx, by, bs) in [(180, 220, 16), (260, 170, 12), (330, 250, 14),
                         (620, 150, 13), (820, 200, 15), (880, 130, 11),
                         (430, 120, 12), (150, 330, 13)]:
        bird(d, bx, by, bs, BIRD)

    # --- type: the name carries the poster --------------------------------
    title_font = ImageFont.truetype(DEJAVU_BOLD, 148)
    tag_font = ImageFont.truetype(DEJAVU_BOLD, 30)
    small_font = ImageFont.truetype(DEJAVU, 24)

    # Soft dark panel so the name reads over the sea.
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = ImageDraw.Draw(panel)
    p.rectangle([0, 800, W, 1000], fill=(10, 16, 34, 110))
    img.paste(Image.alpha_composite(img.convert("RGBA"), panel).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)

    draw_tracked(d, W // 2 + 3, 815, "VELMARA", title_font, (24, 20, 40), 10)
    draw_tracked(d, W // 2, 812, "VELMARA", title_font, CREAM, 10)
    draw_tracked(d, W // 2, 946, "WHERE THE SEA FALLS UPWARD",
                 tag_font, CREAM, 6)

    # --- double cream frame -------------------------------------------------
    d.rectangle([24, 24, W - 24, H - 24], outline=CREAM, width=5)
    d.rectangle([38, 38, W - 38, H - 38], outline=CREAM, width=2)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
