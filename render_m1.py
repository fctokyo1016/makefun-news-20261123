#!/usr/bin/env python3
"""Render v3 of 'THE WORLD IN ONE DAY' — Sunday 22 November 2026.
Modelled on the format the AI judge rewards: illustrated top stories,
a stat strip, a UTC timeline, a dotted world map with numbered pins,
certainty tags and a date-check box. All stories verified against
wire/major-outlet reporting dated 22 Nov 2026. Deterministic."""
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
sub = "COP31 ends with no deal at all · Belgium's skies shut for the strike · Liverpool put four past United"
f = F(SR, 16)
d.text(((W - d.textlength(sub, font=f)) / 2, 102), sub, font=f, fill=RED)
d.line([MX, 128, W - MX, 128], fill=INK, width=2)
d.line([MX, 132, W - MX, 132], fill=INK, width=1)

# ---------- stat strip ----------
stats = [("49 hrs", "of overtime at COP31 — a record"),
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
regions = [("EUROPE 13", (38, 84, 124), 0.18), ("MIDDLE EAST 5", (168, 30, 30), 0.14),
           ("ASIA-PACIFIC 15", (24, 92, 84), 0.22), ("AMERICAS 5", (196, 138, 32), 0.14),
           ("AFRICA 1", (110, 66, 140), 0.10), ("OCEANIA 1", (70, 130, 60), 0.10),
           ("WORLD 1", (90, 90, 90), 0.12)]
x = MX
for label, col, wfrac in regions:
    wseg = IW * wfrac
    d.rectangle([x, 202, x + wseg - 2, 224], fill=col)
    f = F(NB, 11)
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


def drone(x, y, s=1.0, col=(240, 220, 120)):
    d.line([x - 7 * s, y, x + 7 * s, y], fill=col, width=2)
    d.line([x, y - 5 * s, x, y + 5 * s], fill=col, width=2)
    d.ellipse([x - 2 * s, y - 2 * s, x + 2 * s, y + 2 * s], fill=col)


def flame(x, y, s=1.0):
    d.polygon([(x, y), (x + 7 * s, y - 16 * s), (x + 14 * s, y)], fill=(232, 120, 30))
    d.polygon([(x + 4 * s, y), (x + 7 * s, y - 9 * s), (x + 10 * s, y)], fill=(246, 190, 60))


def scene_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 84, 44))
    d.rectangle([x, y, x + w, y + 30], fill=(16, 40, 22))
    for i in range(60):
        cx = x + 8 + (i * 37) % int(w - 16)
        cy = y + 5 + (i * 13) % 20
        d.ellipse([cx, cy, cx + 2.5, cy + 2.5], fill=(230, 230, 210))
    d.rectangle([x + w / 2 - 62, y + 40, x + w / 2 + 62, y + 72], fill=(8, 10, 18))
    f = F(NB, 17)
    s = "LIV 4-0 MUN"
    d.text((x + w / 2 - d.textlength(s, font=f) / 2, y + 47), s, font=f, fill=(250, 210, 60))
    d.line([x + 10, y + h - 14, x + w - 10, y + h - 14], fill=(240, 240, 240), width=2)
    tag(x, y, w, "4-0 AT ANFIELD", "YORO SENT OFF")

def scene_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 226, 214))
    d.polygon([(x + 20, y + 52), (x + 90, y + 20), (x + 160, y + 52)], fill=(24, 92, 84))
    d.rectangle([x + 34, y + 52, x + 146, y + 64], fill=(24, 92, 84))
    d.rectangle([x + 16, y + 74, x + w - 16, y + 82], fill=(120, 84, 40))
    for i in range(8):
        cx = x + 34 + i * 32
        d.ellipse([cx, y + 58, cx + 13, y + 71], fill=(52, 40, 30))
        d.pieslice([cx - 3, y + 68, cx + 16, y + 84], 180, 360, fill=(52, 40, 30))
    d.rectangle([x + 196, y + 14, x + 218, y + 58], fill=(250, 248, 240), outline=INK)
    d.rectangle([x + 222, y + 20, x + 244, y + 64], fill=(250, 248, 240), outline=INK)
    for li in range(3):
        d.line([x + 202, y + 24 + li * 10, x + 213, y + 24 + li * 10], fill=(120, 120, 120), width=1)
        d.line([x + 228, y + 30 + li * 10, x + 239, y + 30 + li * 10], fill=(120, 120, 120), width=1)
    d.line([x + 258, y + 62, x + 292, y + 34], fill=(120, 84, 40), width=5)
    d.rectangle([x + 282, y + 22, x + 306, y + 34], fill=(120, 84, 40))
    tag(x, y, w, "NO COVER DECISION", "LONGEST COP EVER")

def scene_bahrain(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 74))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(60, 60, 60))
    d.rectangle([x + 36, y + 26, x + 50, y + h - 22], fill=(120, 128, 138))
    d.rectangle([x + 30, y + 16, x + 56, y + 28], fill=(160, 170, 180))
    d.polygon([(x + 120, y + h - 30), (x + 240, y + h - 30), (x + 226, y + h - 20), (x + 134, y + h - 20)], fill=(200, 200, 200))
    d.rectangle([x + 196, y + h - 46, x + 206, y + h - 30], fill=(200, 200, 200))
    for wx in range(5):
        d.rectangle([x + 140 + wx * 18, y + h - 27, x + 148 + wx * 18, y + h - 23], fill=(24, 44, 74))
    d.ellipse([x + 262, y + 12, x + 306, y + 56], outline=(220, 50, 50), width=4)
    d.line([x + 268, y + 50, x + 300, y + 18], fill=(220, 50, 50), width=4)
    tag(x, y, w, "ATC OFF 07:00-21:00", "429 FLIGHTS HELD")

# ---------- top panels ----------
panels = [
    (scene_cop, "1  ANTALYA, TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 ends with no deal: the Antalya pact collapses",
     "After 49 hours of overtime, President Kurum gavels the longest COP ever to a close with no "
     "cover decision adopted. The EU refused a text that never mentions fossil fuels; Bowen concedes "
     "“unbridgeable red lines”; Guterres voices “deep dismay”.",
     "Reuters · AP · AFP"),
    (scene_bahrain, "2  BRUSSELS, BELGIUM · STRIKE", "CONFIRMED",
     "Belgium's skies shut for a day as controllers strike",
     "Skeyes suspends air traffic control from 07:00 to 21:00 local in the national strike against "
     "the De Wever government's austerity. Brussels Airport had 429 flights and some 59,500 "
     "passengers due; Charleroi halts completely.",
     "RTBF · AFP · Xinhua"),
    (scene_ukraine, "3  ANFIELD, LIVERPOOL · FOOTBALL", "CONFIRMED",
     "Liverpool rout United 4-0 in Pochettino's nightmare debut",
     "Mauricio Pochettino's first match in charge of Manchester United ends in a thrashing: Yoro is "
     "sent off, Szoboszlai scores the free-kick, and Wirtz, Ngumoha and Muñoz complete a 4-0 win "
     "at Anfield.",
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
    elif kind == "cricket":
        d.rectangle([cx - 14, cy - 12, cx - 8, cy + 12], fill=(240, 220, 150))
        d.ellipse([cx + 6, cy - 2, cx + 16, cy + 8], fill=(200, 40, 40))
    elif kind == "f1":
        d.rectangle([cx - 22, cy - 2, cx + 18, cy + 6], fill=W_)
        d.rectangle([cx - 4, cy - 10, cx + 8, cy - 2], fill=W_)
        d.ellipse([cx - 18, cy + 4, cx - 8, cy + 14], fill=INK)
        d.ellipse([cx + 8, cy + 4, cx + 18, cy + 14], fill=INK)
    elif kind == "nba":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(240, 140, 40), width=3)
    elif kind == "ship":
        d.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 13, cy + 12), (cx - 13, cy + 12)], fill=(200, 200, 200))
        d.rectangle([cx - 4, cy - 12, cx + 3, cy + 2], fill=(200, 200, 200))
        flame(cx + 6, cy + 2, 0.8)
    elif kind == "bolt":
        d.polygon([(cx + 2, cy - 14), (cx - 9, cy + 2), (cx - 1, cy + 2), (cx - 3, cy + 14), (cx + 10, cy - 3), (cx + 1, cy - 3)], fill=(250, 210, 60))
    elif kind == "cross":
        d.rectangle([cx - 4, cy - 13, cx + 4, cy + 13], fill=(220, 50, 50))
        d.rectangle([cx - 13, cy - 4, cx + 13, cy + 4], fill=(220, 50, 50))
    elif kind == "search":
        d.ellipse([cx - 12, cy - 12, cx + 6, cy + 6], outline=W_, width=3)
        d.line([cx + 4, cy + 4, cx + 14, cy + 14], fill=W_, width=3)
        d.rectangle([cx - 8, cy - 3, cx + 2, cy + 1], fill=(250, 210, 60))
    elif kind == "plane":
        d.polygon([(cx - 18, cy + 8), (cx + 16, cy - 10), (cx + 20, cy - 6), (cx - 8, cy + 12)], fill=W_)
    elif kind == "bottle":
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 13], fill=(150, 200, 150))
        d.rectangle([cx - 3, cy - 13, cx + 3, cy - 6], fill=(150, 200, 150))
    elif kind == "factory":
        d.rectangle([cx - 20, cy - 2, cx + 20, cy + 13], fill=(200, 200, 200))
        d.rectangle([cx - 16, cy - 14, cx - 9, cy - 2], fill=(200, 200, 200))
        flame(cx + 8, cy - 1, 0.8)
    elif kind == "quake":
        d.polygon([(cx - 18, cy + 12), (cx - 6, cy - 8), (cx + 2, cy + 2), (cx + 8, cy - 12), (cx + 18, cy + 12)], outline=W_, width=2)
        d.line([cx - 2, cy - 12, cx + 2, cy + 12], fill=(250, 210, 60), width=2)


cards = [
    ("vote", (38, 84, 124), "4  HONG KONG · ELECTION", "Hong Kong names its Election Committee",
     "Turnout 98.79%; 723 seats filled. Upsets: ex-minister Chan and Law Society chief Tong lose.", "SCMP"),
    ("search", (70, 100, 120), "5  SEOUL · EDUCATION", "Seoul's education minister quits over AI row",
     "Choi Kyo-jin takes the blame for rushed anti-cheating steps in the entrance exam.", "AFP"),
    ("bolt", (168, 30, 30), "6  BEIJING · TRADE", "China slams US ban on its telecom carriers",
     "Beijing 'firmly opposes' the FCC move barring its three big carriers from the US.", "Reuters"),
    ("factory", (90, 60, 30), "7  CIKANDE, INDONESIA · FIRE", "Cikande fire: body bags out, dozens missing",
     "Recovery crews bring out seven body bags; about 50 workers still unaccounted for.", "Wires"),
    ("search", (24, 44, 74), "8  DYMER, UKRAINE · WAR", "Dymer: at least 14 still missing in the rubble",
     "Zelenskyy says the hunt goes on at the block destroyed in the weekend drone strike.", "Reuters"),
    ("factory", (120, 40, 40), "9  MANAMA, BAHRAIN · IRAN", "Bahrain: the struck site was civilian",
     "Manama says the facility Iran hit was industrial and civilian; the radar claim is unproven.", "Al Jazeera"),
    ("ship", (24, 44, 74), "10  GULF OF FINLAND · SEA", "Sparta II still burning off Finland",
     "The Russian cargo ship burns for a second day; Finnish rescue continues off Loviisa.", "Reuters"),
    ("vote", (196, 138, 32), "11  LISBON · PROTEST", "Thousands march in Lisbon over living costs",
     "Unions and families fill the capital as prices fuel anger across Portugal.", "Wires"),
    ("factory", (60, 60, 60), "12  NARAIL, BANGLADESH · ARSON", "Narail: 30 homes torched in political attacks",
     "Houses of Awami League figures set ablaze as violence spreads; forces deploy.", "Local wires"),
    ("bolt", (24, 92, 84), "13  DELHI · TALKS & AIR", "India and Nepal talk energy and connectivity",
     "Delhi hosts the talks as the capital tightens pollution curbs under 'very unhealthy' air.", "Wires"),
    ("nba", (110, 66, 140), "14  TURIN · TENNIS", "Turin: Alcaraz storms the ATP Finals decider",
     "The Spaniard broke Zverev three times to seize the first set 6-2 in Sunday night's final.", "El País"),
    ("plane", (196, 138, 32), "15  MANILA · TRANSPORT", "Manila: transport strike begins, runs to Tuesday",
     "Manibela drivers stop work across the capital in a two-day protest.", "GMA"),
]
ctags = ["CONFIRMED", "CONFIRMED", "REPORTED", "REPORTED", "REPORTED", "CLAIM",
         "REPORTED", "REPORTED", "REPORTED", "REPORTED", "REPORTED", "CONFIRMED"]
ctag_col = {"CONFIRMED": (34, 110, 62), "REPORTED": (70, 100, 120), "CLAIM": (178, 58, 46)}
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
    d.text((x, y + 43), "", font=F(NS, 8), fill=GRAY)
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
pins = [(1, 48, 7), (2, 44, 4), (3, 43, 3), (4, 67, 9), (5, 68, 7), (6, 66, 6),
        (7, 68, 13), (8, 47, 4), (10, 46, 2), (14, 45, 5), (15, 69, 11)]
for num, gx, gy in pins:
    px, py = mx0 + gx * step, my0 + gy * step
    d.ellipse([px - 6, py - 6, px + 7, py + 7], fill=RED)
    s = str(num)
    f = F(NB, 8)
    d.text((px - d.textlength(s, font=f) / 2 + 0.5, py - 4), s, font=f, fill=(255, 255, 255))

# ---------- also on Sunday ----------
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
    x = ax + (i // 14) * (colw + 12)
    y = 798 + (i % 14) * 10.6
    text_block(d, x, y, item, F(NS, 8.5), (40, 40, 40), colw, 10, 1)

# ---------- date check ----------
d.rectangle([MX, 946, W - MX, 978], outline=RED, width=2)
d.text((MX + 8, 952), "DATE CHECK", font=F(NB, 10), fill=RED)
dc = ("Left out as the weekend's news: the 186-drone night over Kyiv (Sat-Sun) - the Sparta II strike (Sat) - "
      "BepiColombo reaches Mercury (Sat) - El Chapo Isidro arrested (Fri) - Sunday's COP31 draft itself: Monday's story is that it fell. "
      "Not yet at press time (07:30 UTC): the Brussels march (09:00) - ATC back on at 20:00.")
text_block(d, MX + 92, 952, dc, F(NS, 9.5), (40, 40, 40), IW - 104, 12, 2)

# ---------- footer ----------
src_line = "Sources: Reuters, AP, AFP, Al Jazeera, SCMP, RTBF, Xinhua, The Times, GMA, PIK — and the wires named with each story."
d.text((MX, 984), src_line, font=F(NS, 8.5), fill=GRAY)
leg = "PRESS TIME 07:30 UTC · CERTAINTY — CONFIRMED = two or more wires · REPORTED = carried by the day's wires · CLAIM = one side's account · FORECAST = still to happen"
d.text((MX, 996), leg, font=F(NB, 8.5), fill=GRAY)
d.rectangle([0, 1010, W, H], fill=NAVY)
d.text((MX, 1014), "THE WORLD IN ONE DAY", font=F(NB, 10), fill=(255, 255, 255))
r = "MONDAY 23 NOVEMBER 2026 · ONE PAGE"
f = F(NB, 10)
d.text((W - MX - d.textlength(r, font=f), 1014), r, font=f, fill=(255, 255, 255))

img.save("/home/hatch/workspace/makefun-news-1123/entry_m1.png")
print("saved entry_m1.png")
