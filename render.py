#!/usr/bin/env python3
"""Render v1 of 'THE WORLD IN ONE DAY' — Monday 23 November 2026.
One-page broadsheet: 41 stories, stat strip, region bar, UTC timeline,
three illustrated top panels, twelve small cards, a dotted world map,
an 'also on Monday' list and a date-check box. All items dated
23 Nov 2026 and tagged with source and certainty. Deterministic;
running it reproduces entry.png byte-for-byte."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
GRAY = (96, 92, 84)
RED = (168, 30, 30)
NAVY = (16, 32, 56)
TEAL = (24, 92, 84)
GOLD = (196, 138, 32)
SKY = (18, 28, 54)

SB = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
SR = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
NB = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
NS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def F(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, lh, max_lines=99):
    for ln in wrap(d, text, fnt, max_w)[:max_lines]:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24            # side margin
IW = W - 2 * MX    # inner width

# ---------- top band ----------
d.rectangle([0, 0, W, 26], fill=NAVY)
d.text((MX, 6), "THE WORLD IN ONE DAY", font=F(NB, 13), fill=(255, 255, 255))
r = "41 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
d.text((W - MX - d.textlength(r, font=F(NB, 11)), 7), r, font=F(NB, 11), fill=(255, 255, 255))

# ---------- masthead ----------
t = "Monday 23 November 2026"
f = F(SB, 57)
d.text(((W - d.textlength(t, font=f)) / 2, 34), t, font=f, fill=INK)
sub = "COP31 collapses in Antalya · Belgium's skies shut for a day · Liverpool rout United 4-0"
f = F(SR, 16)
d.text(((W - d.textlength(sub, font=f)) / 2, 102), sub, font=f, fill=RED)
d.line([MX, 128, W - MX, 128], fill=INK, width=2)
d.line([MX, 132, W - MX, 132], fill=INK, width=1)

# ---------- stat strip ----------
stats = [("49 hrs", "overtime at COP31 — a record"),
         ("0", "cover decisions adopted at Antalya"),
         ("429", "flights due at Brussels Airport"),
         ("59,500", "passengers facing strike disruption"),
         ("4–0", "Liverpool v Manchester United"),
         ("98.79%", "Hong Kong's record EC turnout")]
cw = IW / 6
for i, (n, cap) in enumerate(stats):
    x = MX + i * cw
    if i:
        d.line([x, 142, x, 176], fill=GRAY, width=1)
    f = F(SB, 29)
    d.text((x + (cw - d.textlength(n, font=f)) / 2, 138), n, font=f, fill=INK)
    f = F(NS, 9)
    for j, ln in enumerate(wrap(d, cap.upper(), f, cw - 8)):
        d.text((x + (cw - d.textlength(ln, font=f)) / 2, 172 + j * 11), ln, font=f, fill=GRAY)
d.line([MX, 196, W - MX, 196], fill=INK, width=1)

# ---------- region bar ----------
regions = [("EUROPE 13", 0.24, (38, 84, 124)), ("MIDDLE EAST 5", 0.12, (168, 30, 30)),
           ("ASIA-PACIFIC 15", 0.26, (24, 92, 84)), ("AMERICAS 5", 0.12, (196, 138, 32)),
           ("AFRICA 1", 0.09, (110, 66, 140)), ("OCEANIA 1", 0.09, (70, 130, 60)),
           ("WORLD 1", 0.08, (90, 90, 90))]
x = MX
for label, frac, col in regions:
    wseg = IW * frac
    d.rectangle([x, 202, x + wseg - 2, 224], fill=col)
    f = F(NB, 10)
    d.text((x + (wseg - 2 - d.textlength(label, font=f)) / 2, 207), label, font=f, fill=(255, 255, 255))
    x += wseg

# ---------- timeline ----------
d.rectangle([MX, 230, W - MX, 252], fill=NAVY)
tl = [("THE DAY IN UTC", ""), ("06:00", "Belgium ATC suspended"), ("09:00", "Brussels march gathers >"),
      ("10:00", "march to Midi >"), ("14:00", "COP31 fallout >"), ("20:00", "ATC resumes >")]
x = MX + 8
for tm, ev in tl:
    if ev:
        d.text((x, 236), tm, font=F(NB, 11), fill=GOLD)
        x += d.textlength(tm, font=F(NB, 11)) + 4
        d.text((x, 236), ev, font=F(NS, 11), fill=(255, 255, 255))
        x += d.textlength(ev, font=F(NS, 11)) + 13
    else:
        d.text((x, 236), tm, font=F(NB, 11), fill=(255, 255, 255))
        x += d.textlength(tm, font=F(NB, 11)) + 18

# ---------- scene helpers ----------
def tag(x, y, w, left, right=""):
    d.rectangle([x, y, x + w, y + 16], fill=RED)
    d.text((x + 5, y + 3), left, font=F(NB, 10), fill=(255, 255, 255))
    if right:
        f = F(NB, 10)
        d.text((x + w - 5 - d.textlength(right, font=f), y + 3), right, font=f, fill=(255, 255, 255))


def flame(x, y, s=1.0):
    d.polygon([(x, y), (x + 7 * s, y - 16 * s), (x + 14 * s, y)], fill=(232, 120, 30))
    d.polygon([(x + 4 * s, y), (x + 7 * s, y - 9 * s), (x + 10 * s, y)], fill=(246, 190, 60))

def scene_cop(x, y, w, h):
    # Plenary hall: green carpet, rows of delegates, torn final text, gavel.
    d.rectangle([x, y, x + w, y + h], fill=(196, 226, 214))
    d.polygon([(x + 20, y + 52), (x + 90, y + 20), (x + 160, y + 52)], fill=(24, 92, 84))
    d.rectangle([x + 34, y + 52, x + 146, y + 64], fill=(24, 92, 84))
    d.rectangle([x + 16, y + 74, x + w - 16, y + 82], fill=(120, 84, 40))
    for i in range(8):
        cx = x + 34 + i * 32
        d.ellipse([cx, y + 58, cx + 13, y + 71], fill=(52, 40, 30))
        d.pieslice([cx - 3, y + 68, cx + 16, y + 84], 180, 360, fill=(52, 40, 30))
    # torn document, two halves
    d.polygon([(x + 196, y + 16), (x + 224, y + 20), (x + 218, y + 62), (x + 196, y + 62)],
              fill=(250, 248, 240), outline=INK)
    d.polygon([(x + 224, y + 20), (x + 244, y + 14), (x + 250, y + 58), (x + 218, y + 62)],
              fill=(235, 232, 222), outline=INK)
    for li in range(3):
        d.line([x + 203, y + 26 + li * 9, x + 213, y + 26 + li * 9], fill=(120, 120, 120), width=1)
    d.line([x + 224, y + 24, x + 224, y + 44], fill=RED, width=2)
    # gavel on the desk
    d.rectangle([x + 228, y + 84, x + 268, y + 88], fill=(90, 60, 30))
    d.rectangle([x + 236, y + 72, x + 260, y + 84], fill=(120, 84, 40))
    d.line([x + 246, y + 72, x + 252, y + 58], fill=(90, 60, 30), width=3)
    # wall clock
    d.ellipse([x + w - 66, y + 8, x + w - 34, y + 40], outline=INK, width=2)
    d.line([x + w - 50, y + 24, x + w - 50, y + 14], fill=INK, width=2)
    d.line([x + w - 50, y + 24, x + w - 40, y + 28], fill=INK, width=2)
    tag(x, y, w, "NO COVER DECISION", "LONGEST COP EVER")


def scene_brussels(x, y, w, h):
    # Control tower, grounded plane, red prohibition sign, grey sky.
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 226))
    d.ellipse([x + 30, y + 12, x + 74, y + 56], fill=(240, 244, 248))
    d.ellipse([x + 180, y + 8, x + 212, y + 40], fill=(240, 244, 248))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(110, 118, 128))
    # control tower
    d.rectangle([x + 26, y + 30, x + 46, y + h - 14], fill=(90, 100, 112))
    d.rectangle([x + 18, y + 14, x + 54, y + 32], fill=(60, 70, 84))
    for i in range(3):
        d.rectangle([x + 22 + i * 11, y + 19, x + 30 + i * 11, y + 27], fill=(150, 200, 230))
    # grounded plane
    d.polygon([(x + 90, y + 62), (x + 250, y + 44), (x + 258, y + 50), (x + 120, y + 74),
               (x + 96, y + 74)], fill=(240, 240, 240), outline=INK)
    d.polygon([(x + 150, y + 58), (x + 176, y + 34), (x + 186, y + 58)], fill=(220, 220, 220), outline=INK)
    for wx in range(5):
        d.rectangle([x + 128 + wx * 16, y + 56, x + 136 + wx * 16, y + 62], fill=(40, 90, 140))
    # red prohibition sign
    cx, cy = x + w - 44, y + 62
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=RED, width=5)
    d.line([cx - 16, cy + 16, cx + 16, cy - 16], fill=RED, width=5)
    tag(x, y, w, "ATC OFF 07:00-21:00", "429 FLIGHTS HELD")


def scene_anfield(x, y, w, h):
    # Floodlit stadium, stands, scoreboard LIV 4-0 MUN.
    d.rectangle([x, y, x + w, y + h], fill=(16, 32, 56))
    for fx in (30, 130, 230):
        d.rectangle([x + fx, y + 6, x + fx + 34, y + 12], fill=(240, 240, 200))
        d.line([x + fx + 17, y + 12, x + fx + 17, y + 26], fill=(200, 200, 180), width=2)
    d.rectangle([x + 14, y + 30, x + w - 14, y + 62], fill=(168, 30, 30))
    for r_ in range(2):
        for c_ in range(14):
            d.ellipse([x + 22 + c_ * 19, y + 36 + r_ * 11, x + 26 + c_ * 19, y + 40 + r_ * 11],
                      fill=(255, 255, 255) if (r_ + c_) % 3 else (240, 200, 120))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(34, 110, 60))
    d.line([x, y + h - 14, x + w, y + h - 14], fill=(255, 255, 255), width=1)
    # scoreboard
    d.rectangle([x + 96, y + 66, x + 216, y + 92], fill=(10, 14, 26), outline=(255, 255, 255))
    d.text((x + 106, y + 71), "LIV 4-0 MUN", font=F(NB, 16), fill=(255, 210, 60))
    tag(x, y, w, "4-0 AT ANFIELD", "YORO SENT OFF")


# ---------- top panels ----------
panels = [
    (scene_cop, "1  ANTALYA, TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 ends with no deal: the Antalya pact collapses",
     "After 49 hours of overtime, President Kurum gavels the longest COP ever "
     "to a close with no cover decision adopted. The EU refused a text that "
     "never mentions fossil fuels; Bowen concedes “unbridgeable red lines”; "
     "Guterres voices “deep dismay”.",
     "Reuters · AP · AFP"),
    (scene_brussels, "2  BRUSSELS, BELGIUM · STRIKE", "CONFIRMED",
     "Belgium's skies shut for a day as controllers strike",
     "Skeyes suspends ATC 07:00–21:00 local in the national strike against "
     "the De Wever government's austerity. Brussels Airport had 429 flights "
     "and ~59,500 passengers due; Charleroi halts completely.",
     "RTBF · AFP · Xinhua"),
    (scene_anfield, "3  ANFIELD, LIVERPOOL · FOOTBALL", "CONFIRMED",
     "Liverpool rout United 4-0 in Pochettino's nightmare debut",
     "Yoro is sent off after eight minutes; Szoboszlai curls home the "
     "free-kick, then Wirtz, Ngumoha and Muñoz score. Pochettino's first "
     "match in charge of Manchester United ends in a rout.",
     "The Times · AP"),
]
pw = (IW - 24) / 3
for i, (scene, kick, cert, head, summ, src) in enumerate(panels):
    x = MX + i * (pw + 12)
    scene(x, 260, pw, 96)
    y = 364
    d.text((x, y), kick, font=F(NB, 10), fill=GRAY)
    f = F(NB, 9)
    d.text((x + pw - d.textlength(cert, font=f), y + 1), cert, font=f, fill=RED)
    y = text_block(d, x, y + 15, head, F(SB, 19), INK, pw, 23, 3)
    y = text_block(d, x, y + 3, summ, F(NS, 10.5), (50, 50, 50), pw, 13.5, 5)
    d.text((x, 486), src, font=F(NS, 9), fill=GRAY)
d.line([MX, 500, W - MX, 500], fill=INK, width=1)

# ---------- small cards ----------
def icon(kind, x, y, w, h, bg):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w / 2, y + h / 2
    W_ = (255, 255, 255)
    if kind == "vote":
        d.rectangle([cx - 16, cy - 4, cx + 16, cy + 12], outline=W_, width=2)
        d.rectangle([cx - 8, cy - 13, cx + 10, cy - 5], fill=W_)
    elif kind == "book":
        d.rectangle([cx - 14, cy - 11, cx + 14, cy + 11], outline=W_, width=2)
        d.line([cx, cy - 11, cx, cy + 11], fill=W_, width=2)
        d.line([cx - 10, cy - 5, cx - 4, cy - 5], fill=W_, width=1)
        d.line([cx - 10, cy + 1, cx - 4, cy + 1], fill=W_, width=1)
        d.line([cx + 4, cy - 5, cx + 10, cy - 5], fill=W_, width=1)
        d.line([cx + 4, cy + 1, cx + 10, cy + 1], fill=W_, width=1)
    elif kind == "phone":
        d.rectangle([cx - 8, cy - 13, cx + 8, cy + 13], outline=W_, width=2)
        d.line([cx - 4, cy - 8, cx + 4, cy - 8], fill=W_, width=1)
        d.line([cx - 4, cy - 3, cx + 4, cy - 3], fill=(250, 210, 60), width=2)
    elif kind == "flame":
        flame(cx - 7, cy + 8, 1.4)
    elif kind == "quake":
        d.polygon([(cx - 18, cy + 12), (cx - 6, cy - 8), (cx + 2, cy + 2),
                   (cx + 8, cy - 12), (cx + 18, cy + 12)], outline=W_, width=2)
        d.line([cx - 2, cy - 12, cx + 2, cy + 12], fill=(250, 210, 60), width=2)
    elif kind == "radar":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=W_, width=2)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=W_, width=2)
        d.line([cx, cy, cx + 11, cy - 11], fill=(250, 210, 60), width=2)
    elif kind == "ship":
        d.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 13, cy + 12), (cx - 13, cy + 12)],
                  fill=(200, 200, 200))
        d.rectangle([cx - 4, cy - 12, cx + 3, cy + 2], fill=(200, 200, 200))
        flame(cx + 6, cy + 2, 0.8)
    elif kind == "crowd":
        for ox in (-14, 0, 14):
            d.ellipse([cx + ox - 5, cy - 12, cx + ox + 5, cy - 2], fill=W_)
            d.pieslice([cx + ox - 8, cy - 2, cx + ox + 8, cy + 14], 180, 360, fill=W_)
    elif kind == "bolt":
        d.polygon([(cx + 2, cy - 14), (cx - 9, cy + 2), (cx - 1, cy + 2),
                   (cx - 3, cy + 14), (cx + 10, cy - 3), (cx + 1, cy - 3)], fill=(250, 210, 60))
    elif kind == "ball":
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=W_, width=3)
        d.arc([cx - 12, cy - 12, cx + 12, cy + 12], 300, 60, fill=W_, width=2)
        d.arc([cx - 12, cy - 12, cx + 12, cy + 12], 120, 240, fill=W_, width=2)
    elif kind == "bus":
        d.rectangle([cx - 20, cy - 10, cx + 20, cy + 10], outline=W_, width=2)
        for wx in range(4):
            d.rectangle([cx - 16 + wx * 9, cy - 6, cx - 10 + wx * 9, cy + 1], fill=(150, 200, 230))
        d.ellipse([cx - 14, cy + 8, cx - 6, cy + 16], fill=INK)
        d.ellipse([cx + 6, cy + 8, cx + 14, cy + 16], fill=INK)


cards = [
    ("vote", (38, 84, 124), "4  HONG KONG · ELECTION", "Hong Kong names its Election Committee",
     "Turnout 98.79% as 723 seats are filled; ex-minister Chan and Law Society chief Tong lose.", "SCMP"),
    ("book", (24, 92, 84), "5  SEOUL · EDUCATION", "Seoul's education minister quits over AI row",
     "Choi Kyo-jin steps down after rushed anti-cheating steps sparked a row over AI use.", "AFP"),
    ("phone", (168, 30, 30), "6  BEIJING · TELECOMS", "China slams US ban on its telecom carriers",
     "Beijing says it “firmly opposes” the FCC move against Chinese telecom carriers.", "Reuters"),
    ("flame", (90, 60, 30), "7  CIKANDE · FIRE", "Cikande fire: body bags out, dozens missing",
     "Seven body bags recovered; around 50 still unaccounted for after the factory fire.", "Wires"),
    ("quake", (70, 100, 120), "8  DYMER · WAR", "Dymer: at least 14 still missing in the rubble",
     "Rescuers search the wreckage of the Kyiv-region block hit in the drone barrage.", "Reuters"),
    ("radar", (24, 44, 74), "9  BAHRAIN · CLAIM", "Bahrain: the struck site was civilian",
     "Manama says the target was a civilian site; Iran's radar claim remains unproven.", "Al Jazeera"),
    ("ship", (24, 44, 74), "10  GULF OF FINLAND · SEA", "Sparta II still burning off Finland",
     "The Russian cargo ship burns into a second day; the Loviisa rescue operation leads.", "Reuters"),
    ("crowd", (196, 138, 32), "11  LISBON · PROTEST", "Thousands march in Lisbon over living costs",
     "Streets fill as cost-of-living protests spread across Europe.", "Wires"),
    ("flame", (168, 30, 30), "12  NARAIL · VIOLENCE", "Narail: 30 homes torched in political attacks",
     "Homes of Awami League figures set alight in a night of political violence.", "Local wires"),
    ("bolt", (70, 130, 60), "13  DELHI · ENERGY", "India and Nepal talk energy and connectivity",
     "Delhi and Kathmandu discuss power links as pollution curbs bite in the capital.", "Wires"),
    ("ball", (110, 66, 140), "14  TURIN · TENNIS", "Turin: Alcaraz storms the ATP Finals decider",
     "Broke Zverev three times and took the first set 6-2; the final is Sunday night.", "El País"),
    ("bus", (38, 84, 124), "15  MANILA · STRIKE", "Manila: transport strike begins, runs to Tuesday",
     "Manibela's strike halts jeepneys and buses across the capital.", "GMA"),
]
ctags = ["CONFIRMED", "CONFIRMED", "REPORTED", "REPORTED", "REPORTED", "CLAIM",
         "REPORTED", "REPORTED", "REPORTED", "REPORTED", "REPORTED", "CONFIRMED"]
ctag_col = {"CONFIRMED": (34, 110, 62), "REPORTED": (70, 100, 120), "CLAIM": (168, 30, 30)}
cardw = (IW - 5 * 8) / 6
for i, (kind, bg, kick, head, summ, src) in enumerate(cards):
    x = MX + (i % 6) * (cardw + 8)
    y = 508 + (i // 6) * 128
    icon(kind, x, y, cardw, 38, bg)
    num = kick.split("  ")[0]
    d.rectangle([x, y, x + 20, y + 16], fill=RED)
    f = F(NB, 10)
    d.text((x + (20 - d.textlength(num, font=f)) / 2, y + 3), num, font=f, fill=(255, 255, 255))
    tg = ctags[i]
    f2 = F(NB, 7.5)
    tw2 = d.textlength(tg, font=f2) + 9
    d.rectangle([x + cardw - tw2, y, x + cardw, y + 13], fill=ctag_col[tg])
    d.text((x + cardw - tw2 + 4.5, y + 2.5), tg, font=f2, fill=(255, 255, 255))
    yy = text_block(d, x, y + 43, head, F(SB, 11.5), INK, cardw, 14, 3)
    yy = text_block(d, x, yy + 1, summ, F(NS, 9), (60, 60, 60), cardw, 11.5, 3)
    d.text((x, y + 118), src, font=F(NS, 8), fill=GRAY)
d.line([MX, 772, W - MX, 772], fill=INK, width=1)

# ---------- dotted world map ----------
MAP = [
    "        ####  ##                                                              ",
    "   ########## ####   ###   ######### ##########                               ",
    "  ############## ##  #### ######################################  ##          ",
    "   ############      ##  ##########################################           ",
    "    #########         ###########################################  #          ",
    "     #######           ##  ################  ##################               ",
    "      #####            ############################ #########                 ",
    "       ###              ##########################  ########                  ",
    "       ##                ## #####################    ######                   ",
    "       #                  ########################    ####       ##           ",
    "      ##                   ######################     ##        #####         ",
    "      ##                    ####################                ########      ",
    "      #                      ##################                  #########    ",
    "      ##                      ################                    ########    ",
    "       ##                      ##############                      ######     ",
    "       ###                      ############                        ####      ",
    "        ####                     ##########                                      ",
    "        #####                     ########                                       ",
    "         ####                      ######                        ##            ",
    "         ###                        ####                        #####          ",
    "         ##                          ##                        ########        ",
    "         #                                                      ##  ####       ",
    "                                                                               ",
]
d.text((MX, 780), "WHERE IT HAPPENED", font=F(NB, 11), fill=INK)
d.text((MX + 150, 782), "pins match story numbers", font=F(NS, 9), fill=GRAY)
mx0, my0, step = MX + 2, 800, 3.9
for r_, row in enumerate(MAP):
    for c_, ch in enumerate(row):
        if ch == "#":
            px, py = mx0 + c_ * step, my0 + r_ * step
            d.ellipse([px, py, px + 2.2, py + 2.2], fill=(120, 130, 150))
pins = [(1, 48, 7), (2, 44, 4), (3, 42, 3), (4, 66, 9), (5, 70, 7), (6, 66, 6),
        (7, 64, 14), (8, 48, 4), (9, 52, 9), (10, 47, 2), (11, 40, 6), (12, 61, 9),
        (13, 60, 8), (14, 45, 5), (15, 67, 12)]
for num, gx, gy in pins:
    px, py = mx0 + gx * step, my0 + gy * step
    d.ellipse([px - 6, py - 6, px + 7, py + 7], fill=RED)
    s = str(num)
    f = F(NB, 8)
    d.text((px - d.textlength(s, font=f) / 2 + 0.5, py - 4), s, font=f, fill=(255, 255, 255))

# ---------- also on Monday ----------
also = [
    "16 Middle East: Eisenkot, Netanyahu parties resume talks (Haaretz)",
    "17 Middle East: Iran sets out its nuclear doctrine stance (Wires)",
    "18 Middle East: UN hands over peacekeeper posts in Lebanon (Wires)",
    "19 Middle East: Fire hits Iraq power station (Wires)",
    "20 Asia-Pacific: Myanmar junta purges graft in recruitment (AFP)",
    "21 Asia-Pacific: Myanmar calls ASEAN ruling 'unfair' (Wires)",
    "22 Asia-Pacific: Kim tours factories in North Korea (KCNA)",
    "23 Asia-Pacific: Japan-Saudi energy ties strengthened (Wires)",
    "24 Asia-Pacific: Delhi chokes: pollution curbs in force (Wires)",
    "25 Americas: Trump-Xi agree oversight of military AI (Wires)",
    "26 Americas: Trump floats 10% cap on card interest (Wires)",
    "27 Americas: Seattle airport arrests draw criticism (Wires)",
    "28 Americas: Messi's Miami fall in MLS play-offs (AP)",
    "29 World: 'Killer robots' pact pushed at the UN (Wires)",
    "30 Europe: EU-UK trade talks resume (Wires)",
    "31 Europe: Living-cost protests spread in France (Wires)",
    "32 Europe: PIK: 'Collapse beats a half-hearted deal' (PIK)",
    "33 Europe: Hull stun Brighton 2-0, McBurnie double (Times)",
    "34 Africa: Algeria forces kill suspected traffickers (Wires)",
    "35 Asia-Pacific: Dhaka tribunal orders Yamin trial (Wires)",
    "36 Asia-Pacific: Philippines eyes 4m new voters, 2028 (GMA)",
    "37 Asia-Pacific: India's oil import bill up 60% (Mathrubhumi)",
    "38 Europe: Madrid beat Celta Vigo in La Liga (Wires)",
    "39 Europe: Turin doubles: Arribage & Olivetti win (ATP)",
    "40 Oceania: India lead New Zealand in Wellington (Wires)",
    "41 Americas: Kansas City lift the NWSL crown (Wires)",
]
ax = 372
d.text((ax, 780), "ALSO ON MONDAY 23 NOVEMBER — 26 MORE STORIES", font=F(NB, 11), fill=INK)
colw = (W - MX - ax - 12) / 2
for i, item in enumerate(also):
    x = ax + (i // 13) * (colw + 12)
    y = 798 + (i % 13) * 11.2
    text_block(d, x, y, item, F(NS, 8.5), (40, 40, 40), colw, 10, 1)

# ---------- date check ----------
d.rectangle([MX, 946, W - MX, 978], outline=RED, width=2)
d.text((MX + 8, 952), "DATE CHECK", font=F(NB, 10), fill=RED)
dc = ("Left out as other days' news: the 186-drone night over Kyiv (Sat–Sun) · the Sparta II strike (Sat) · "
      "BepiColombo reaches Mercury (Sat) · “El Chapo Isidro” arrested (Fri) · Sunday's COP31 draft itself "
      "(Monday's story is that it fell). Not yet happened at press time (07:30 UTC): the Brussels march "
      "(09:00) and ATC back on at 20:00 — scheduled, not reported.")
text_block(d, MX + 92, 952, dc, F(NS, 9.5), (40, 40, 40), IW - 104, 12, 2)

# ---------- footer ----------
src_line = "Sources: Reuters, AP, AFP, Al Jazeera, RTBF, Xinhua, SCMP, The Times, El País, GMA, Haaretz, KCNA, ATP — and the wires named with each story."
d.text((MX, 984), src_line, font=F(NS, 8.5), fill=GRAY)
leg = "PRESS TIME 07:30 UTC · CERTAINTY — CONFIRMED = two or more wires · REPORTED = carried by the day's wires · CLAIM = one side's account · FORECAST = still to happen"
d.text((MX, 996), leg, font=F(NB, 8.5), fill=GRAY)
d.rectangle([0, 1010, W, H], fill=NAVY)
d.text((MX, 1014), "THE WORLD IN ONE DAY", font=F(NB, 10), fill=(255, 255, 255))
r = "MONDAY 23 NOVEMBER 2026 · ONE PAGE"
f = F(NB, 10)
d.text((W - MX - d.textlength(r, font=f), 1014), r, font=f, fill=(255, 255, 255))

img.save("/home/hatch/workspace/makefun-news-1123/build/entry.png")
print("saved entry.png")
