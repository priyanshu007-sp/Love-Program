import math as m
import random as r
import turtle as t
import tkinter.font as tkf

# ------------------------------------------------------------------
#  100 WAYS TO SAY I LOVE YOU
#  A rotating wheel of loving notes in warm, romantic colours.
# ------------------------------------------------------------------

TICK = 16
INTERVAL = 9            # ticks between each loving note appearing
R0 = 182                # where the spokes start
R_MAX = 342             # where the longest spoke may end
SERIF = "Georgia"
SANS = "Helvetica"

BG_TOP = (0.12, 0.025, 0.09)
BG_BOT = (0.34, 0.07, 0.19)
BGC = (0.15, 0.035, 0.10)
CREAM = (1.0, 0.91, 0.87)
GOLD = (1.0, 0.67, 0.55)
FLASH = (1.0, 0.96, 0.92)

STOPS = [
    (0.88, 0.28, 0.48),   # rose
    (0.96, 0.34, 0.52),   # berry
    (1.00, 0.48, 0.50),   # blush
    (1.00, 0.63, 0.48),   # coral
    (1.00, 0.80, 0.56),   # peach
]

PHRASES = [
    "I love you", "You are my favorite person", "You make my heart smile",
    "I am so lucky to have you", "You make every day brighter",
    "I love your laugh", "You are beautiful inside and out",
    "You make everything feel better", "I believe in you",
    "You are my happy place", "I adore your kind heart",
    "You make ordinary days magical", "I am proud of you",
    "You are always on my mind", "I love being by your side",
    "You make me feel at home", "I cherish every moment with you",
    "You are one of a kind", "I love the way you see the world",
    "You make my world more colorful", "I will always cheer you on",
    "Your smile is my favorite", "I love how thoughtful you are",
    "You make me a better person", "I feel safe with you",
    "I love sharing life with you", "You are my sweetest adventure",
    "I appreciate all that you are", "You have the warmest heart",
    "I am happiest when we are together", "You make my heart feel full",
    "I love your little quirks", "You can always count on me",
    "You are wonderful just as you are", "I love making memories with you",
    "You bring out the best in me", "I will choose you every day",
    "You are my sunshine", "I love listening to your stories",
    "You make even quiet moments special", "I am grateful for your love",
    "You are my favorite hello", "I love your curious mind",
    "You inspire me every day", "My heart is happiest with you",
    "I love how you care for others", "You make life sweeter",
    "I am always here for you", "You are my favorite kind of magic",
    "I love growing together", "You deserve all the happiness",
    "You make me laugh like no one else", "I treasure your gentle heart",
    "Every day with you is a gift", "I love your brave spirit",
    "You make the world feel kinder", "I am thankful we found each other",
    "Your hugs make everything okay", "I love dreaming with you",
    "You are my best friend and my love", "I see so much good in you",
    "You make my heart glow", "I love the life we are building",
    "You are more than I ever hoped for", "I will always make time for you",
    "I love your wonderful imagination", "You make every place feel like home",
    "I am on your team, always", "You are my favorite person to talk to",
    "I love how genuine you are", "You make me feel understood",
    "I will hold your hand through anything", "You are a joy in my life",
    "I love your generous heart", "You make every day worth celebrating",
    "I am grateful for your hugs", "You are my sweetest thought",
    "I love discovering new things with you", "You make hope feel easy",
    "I am so glad you are you", "You are loved beyond words",
    "I love your beautiful soul", "You make every season better",
    "I will keep showing up for you", "You are my favorite part of today",
    "I love how we understand each other", "You make my dreams feel closer",
    "I am always rooting for you", "You are a bright light in my life",
    "I love every version of you", "You make my heart feel at peace",
    "I will never stop appreciating you", "You are my once-in-a-lifetime",
    "I love you more with every day", "Thank you for being you",
    "My heart will always find its way to you",
    "You make my favorite memories", "I love your beautiful laugh",
    "You are my sweetest forever", "There is no one quite like you",
]
N = len(PHRASES)
assert N == 100, N

s = t.Screen()
s.setup(800, 800)


def hx(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in c)


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def clamp(v):
    return max(0.0, min(1.0, v))


def palette(k):
    k = clamp(k) * (len(STOPS) - 1)
    i = min(int(k), len(STOPS) - 2)
    return mix(STOPS[i], STOPS[i + 1], k - i)


s.bgcolor(hx(BG_TOP))
s.title("100 Ways to Say I Love You")
s.tracer(0)
cv = s.getcanvas()
rng = r.Random(7)

# ---------------- background: warm gradient, stars, rings ----------------
BANDS = 80
for i in range(BANDS):
    y0 = -420 + 840 * i / BANDS
    c = mix(BG_TOP, BG_BOT, (i / (BANDS - 1)) ** 1.4)
    cv.create_rectangle(-430, y0, 430, y0 + 840 / BANDS + 1,
                        fill=hx(c), outline="")

stars = []
for _ in range(90):
    x, y = rng.uniform(-400, 400), rng.uniform(-400, 400)
    if m.hypot(x, y) < 372:
        continue
    b = rng.uniform(0.15, 0.5)
    sz = rng.choice((0.8, 1, 1, 1.4))
    stars.append((cv.create_oval(x - sz, y - sz, x + sz, y + sz,
                                 fill=hx(mix(BGC, CREAM, b)), outline=""), b))

hearts = []
for i in range(18):
    a = 2 * m.pi * i / 18 + rng.uniform(-0.12, 0.12)
    radius = rng.uniform(374, 389)
    size = rng.uniform(7, 12)
    x, y = radius * m.cos(a), -radius * m.sin(a)
    color = rng.choice(((1.0, 0.35, 0.55), (1.0, 0.55, 0.62), (1.0, 0.72, 0.68)))
    hearts.append(dict(
        id=cv.create_polygon(0, 0, 0, 0, 0, 0, fill=hx(color), outline=""),
        x=x, y=y, size=size, phase=rng.uniform(0, 2 * m.pi), color=color,
    ))

for rad, k in ((R0 - 14, 0.35), (R0 - 19, 0.12)):
    cv.create_oval(-rad, -rad, rad, rad, outline=hx(mix(BG_TOP, GOLD, k)),
                   width=1)
RING = 366
cv.create_oval(-RING, -RING, RING, RING,
               outline=hx(mix(BG_TOP, GOLD, 0.18)), width=1)

# ---------------- spokes ----------------
fs = 9
while fs > 6:
    f = tkf.Font(root=cv, family=SANS, size=fs)
    if max(f.measure(p) for p in PHRASES) <= R_MAX - R0:
        break
    fs -= 1

spokes = []
for i, text in enumerate(PHRASES):
    th = m.pi / 2 - 2 * m.pi * i / N          # start at 12 o'clock, go clockwise
    sid = cv.create_text(0, 0, text=text, font=(SANS, fs),
                         fill=hx(BGC), anchor="w")
    spokes.append(dict(id=sid, th=th, color=palette(i / (N - 1)),
                       born=None))

# ---------------- centre ----------------
title = cv.create_text(0, -72, text="1 0 0   W A Y S   T O   S A Y",
                       font=(SANS, 8, "bold"), fill=hx(BGC))
title2 = cv.create_text(0, -56, text="I   L O V E   Y O U",
                        font=(SANS, 8, "bold"), fill=hx(BGC))
phrase = cv.create_text(0, -2, text="", font=(SERIF, 19, "italic"),
                        fill=hx(BGC), width=250, justify="center")
rule = cv.create_line(-26, 52, 26, 52, fill=hx(BGC), width=1)
counter = cv.create_text(0, 72, text="", font=(SANS, 9, "bold"),
                         fill=hx(BGC))

arc = cv.create_arc(-RING, -RING, RING, RING, start=90, extent=-0.01,
                    style="arc", outline=hx(GOLD), width=2)

# ---------------- state ----------------
tick = 0
rot = 0.0
shown = 0
cur = None            # index of phrase in the centre
cur_t = 0             # tick it appeared
done_t = None


def show_center(i):
    global cur, cur_t
    cur, cur_t = i, tick
    cv.itemconfig(phrase, text=PHRASES[i])
    cv.itemconfig(counter, text="N° %03d" % (i + 1))


def place(p, slide):
    a = (p["th"] + rot) % (2 * m.pi)
    rr = R0 + slide
    x, y = rr * m.cos(a), -rr * m.sin(a)
    if m.pi / 2 < a < 3 * m.pi / 2:
        ang, anc = m.degrees(a) + 180, "e"
    else:
        ang, anc = m.degrees(a), "w"
    cv.coords(p["id"], x, y)
    cv.itemconfig(p["id"], angle=ang % 360, anchor=anc)


def heart_points(x, y, size):
    points = []
    for i in range(24):
        a = 2 * m.pi * i / 24
        px = 16 * m.sin(a) ** 3
        py = 13 * m.cos(a) - 5 * m.cos(2 * a) - 2 * m.cos(3 * a) - m.cos(4 * a)
        points.extend((x + px * size / 32, y - py * size / 32))
    return points


def step():
    global tick, rot, shown, done_t
    tick += 1
    rot -= 0.0006 + (0.0006 if shown >= N else 0)

    # reveal the next loving note
    if shown < N and tick % INTERVAL == 0:
        spokes[shown]["born"] = tick
        show_center(shown)
        shown += 1
        cv.itemconfig(arc, extent=-max(0.01, min(359.9, 360 * shown / N)))
        if shown == N:
            done_t = tick

    # when finished, keep the centre alive
    if done_t and (tick - done_t) > 150 and (tick - cur_t) > 170:
        show_center(rng.choice([k for k in range(N) if k != cur]))

    # spokes: fade in, slide out, sweeping highlight when complete
    sweep = (tick * 0.22) % N
    for i, p in enumerate(spokes):
        if p["born"] is None:
            continue
        u = clamp((tick - p["born"]) / 40)
        e = 1 - (1 - u) ** 3
        place(p, (1 - e) * 18)
        glow = 0.0
        if done_t:
            d = abs(i - sweep)
            d = min(d, N - d)
            glow = m.exp(-(d / 3.0) ** 2) * 0.65
        pop = 0.9 * m.sin(m.pi * clamp((u - 0.1) / 0.5)) if u < 0.6 else 0
        col = mix(mix(BGC, p["color"], 0.82 * e), FLASH, max(glow, pop))
        cv.itemconfig(p["id"], fill=hx(col))

    # centre text
    k = clamp((tick - 8) / 40)
    cv.itemconfig(title, fill=hx(mix(BGC, GOLD, 0.85 * k)))
    cv.itemconfig(title2, fill=hx(mix(BGC, GOLD, 0.85 * k)))
    cv.itemconfig(rule, fill=hx(mix(BGC, GOLD, 0.5 * k)))
    if cur is not None:
        fe = clamp((tick - cur_t) / 14)
        c = mix(BGC, mix(CREAM, spokes[cur]["color"], 0.18), fe)
        cv.itemconfig(phrase, fill=hx(c))
        cv.itemconfig(counter, fill=hx(mix(BGC, GOLD, 0.75 * fe)))

    # twinkle
    for _ in range(2):
        sid, b = rng.choice(stars)
        cv.itemconfig(sid, fill=hx(mix(BGC, CREAM, b * rng.uniform(0.4, 1.3))))

    for heart in hearts:
        shimmer = (1 + m.sin(tick * 0.16 + heart["phase"])) / 2
        size = heart["size"] * (0.78 + 0.32 * shimmer)
        cv.coords(heart["id"], *heart_points(heart["x"], heart["y"], size))
        color = mix(heart["color"], FLASH, shimmer ** 5 * 0.8)
        cv.itemconfig(heart["id"], fill=hx(color))

    cv.after(TICK, step)


try:
    cv.after(300, step)
    t.done()
except (t.Terminator, Exception):
    pass