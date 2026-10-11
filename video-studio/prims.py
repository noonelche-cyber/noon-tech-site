"""Shared drawing primitives for the ¡JODER! TikTok (poster style)."""
import math, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
TEAL = (11, 105, 116); TEAL_D = (6, 62, 70); INK = (15, 21, 28); CREAM = (246, 233, 212)
PINK = (247, 160, 160); RED = (226, 45, 82); YEL = (252, 213, 73); CYAN = (64, 185, 182)
ANTON = 'Anton-Regular.ttf'; MARK = 'PermanentMarker.ttf'; BANG = 'Bangers-Regular.ttf'; BRUSH = 'CaveatBrush-Regular.ttf'
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
POSTER = 'assets/poster_original.webp'
_fc = {}
# Hebrew: swap to fonts that have Hebrew glyphs (same role, size-adjusted)
HE_MAP = {ANTON: ('fonts/Karantina-Bold.ttf', 1.2), MARK: ('fonts/Karantina-Bold.ttf', 1.25), BANG: ('fonts/SecularOne-Regular.ttf', 0.82),
          BRUSH: ('fonts/AmaticSC-Bold.ttf', 1.3), '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf': ('fonts/SecularOne-Regular.ttf', 0.92)}
def is_he(s): return any('\u0590' <= ch <= '\u05ff' for ch in s)
def hfont(f, s):
    if not is_he(s): return f
    path, k = HE_MAP.get(f.path, ('fonts/SecularOne-Regular.ttf', 1.0))
    return font(path, max(8, int(f.size * k)))
def font(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]

_ec = {}
def emoji(ch, size):
    if (ch, size) not in _ec:
        im = Image.new('RGBA', (160, 160)); ImageDraw.Draw(im).text((10, 10), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True)
        _ec[(ch, size)] = im.crop(im.getbbox()).resize((size, size), Image.LANCZOS)
    return _ec[(ch, size)]

def txt(s, f, fill, stroke=0, sf=INK, emo=None, esize=None):
    rtl = is_he(s); f = hfont(f, s); kw = {'direction': 'rtl'} if rtl else {}
    b = f.getbbox(s, stroke_width=stroke, **kw)
    im = Image.new('RGBA', (b[2] - b[0] + 20, b[3] - b[1] + 20))
    ImageDraw.Draw(im).text((10 - b[0], 10 - b[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sf, **kw)
    if emo:
        e = emoji(emo, esize or int(im.height * 0.9))
        n = Image.new('RGBA', (im.width + e.width + 12, max(im.height, e.height)))
        tx, ex = (e.width + 12, 0) if rtl else (0, im.width + 12)      # emoji goes after the text: on the left in RTL
        n.alpha_composite(im, (tx, (n.height - im.height) // 2)); n.alpha_composite(e, (ex, (n.height - e.height) // 2)); im = n
    return im

def fit(s, p, size, maxw, **kw):
    while True:
        l = txt(s, font(p, size), **kw)
        if l.width <= maxw or size < 30: return l
        size -= 4

def paste(c, l, cx, cy, sc=1.0, a=1.0, rot=0):
    if a <= 0: return
    if sc != 1.0: l = l.resize((max(1, int(l.width * sc)), max(1, int(l.height * sc))), Image.BICUBIC)
    if rot: l = l.rotate(rot, Image.BICUBIC, expand=True)
    if a < 1: l = l.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * a)))
    c.alpha_composite(l, (int(cx - l.width / 2), int(cy - l.height / 2)))

def eo(x): x = max(0., min(1., x)); return 1 - (1 - x) ** 3
def back(x): x = max(0., min(1., x)); s = 1.7; return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2
def pop(t, d=0.28): return max(0.0, back(t / d)) if t >= 0 else 0
def fade(t, d=0.18): return max(0., min(1., t / d))

# ---------- paper / paint primitives ----------
def torn(w, h, col, seed, jag=9, shadow=True):
    rnd = random.Random(seed); pts = []
    def edge(x0, y0, x1, y1, n):
        for i in range(n):
            f = i / n; pts.append((x0 + (x1 - x0) * f + rnd.uniform(-jag, jag) * (y0 == y1 and 0 or 1),
                                   y0 + (y1 - y0) * f + rnd.uniform(-jag, jag) * (x0 == x1 and 0 or 1)))
    m = 24; edge(m, m, w + m, m, w // 14); edge(w + m, m, w + m, h + m, h // 14); edge(w + m, h + m, m, h + m, w // 14); edge(m, h + m, m, m, h // 14)
    im = Image.new('RGBA', (w + 2 * m + 14, h + 2 * m + 14))
    d = ImageDraw.Draw(im)
    if shadow: d.polygon([(x + 12, y + 12) for x, y in pts], fill=(0, 0, 0, 110))
    d.polygon(pts, fill=col + (255,))
    # paper grain
    g = (np.random.default_rng(seed).random((im.height, im.width)) * 26).astype(np.uint8)
    grain = Image.fromarray(g, 'L'); a = im.getchannel('A')
    dark = Image.new('RGBA', im.size, (60, 40, 20, 0)); dark.putalpha(Image.fromarray(np.minimum(np.array(grain), np.array(a)), 'L'))
    im.alpha_composite(dark)
    return im

def splash(w, h, col, seed):
    rnd = random.Random(seed); im = Image.new('RGBA', (w + 200, h + 200)); d = ImageDraw.Draw(im)
    cx, cy = (w + 200) / 2, (h + 200) / 2; pts = []
    for i in range(90):
        a = i / 90 * 2 * math.pi; r = 1 + 0.10 * math.sin(a * 5 + seed) + rnd.uniform(-0.06, 0.06)
        if rnd.random() < 0.12: r += rnd.uniform(0.1, 0.25)
        pts.append((cx + math.cos(a) * w / 2 * r, cy + math.sin(a) * h / 2 * r))
    d.polygon(pts, fill=col + (255,))
    for _ in range(70):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(1.05, 1.35); s = rnd.uniform(3, 16)
        x, y = cx + math.cos(a) * w / 2 * rr, cy + math.sin(a) * h / 2 * rr
        d.ellipse((x - s, y - s, x + s, y + s), fill=col + (255,))
    return im

def bubble(s, size=60, seed=1, emo=None, col=CREAM):
    t = txt(s, font(BANG, size), INK, emo=emo)
    w, h = t.width + 90, t.height + 70
    im = Image.new('RGBA', (w + 40, h + 80)); d = ImageDraw.Draw(im)
    d.polygon([(w * 0.25, h - 10), (w * 0.12, h + 60), (w * 0.42, h - 6)], fill=INK)
    d.ellipse((6, 6, w + 6, h + 6), fill=INK); d.ellipse((0, 0, w, h), fill=INK)
    d.ellipse((7, 7, w - 7, h - 7), fill=col + (255,))
    d.polygon([(w * 0.27, h - 18), (w * 0.17, h + 46), (w * 0.39, h - 14)], fill=col + (255,))
    im.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2))
    return im

def strip(s, size=62, col=CREAM, fg=INK, seed=3, p=BANG, emo=None, maxw=920):
    t = fit(s, p, size, maxw - 70, fill=fg, emo=emo)
    im = torn(t.width + 50, t.height + 26, col, seed, jag=6)
    im.alpha_composite(t, (24 + 25, 24 + 13)); return im

def speaker(r=58):
    im = Image.new('RGBA', (2 * r + 8, 2 * r + 8)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=CREAM + (255,), outline=CYAN, width=7)
    c = r + 4; s = r / 58
    d.polygon([(c - 26 * s, c - 12 * s), (c - 12 * s, c - 12 * s), (c + 4 * s, c - 28 * s), (c + 4 * s, c + 28 * s), (c - 12 * s, c + 12 * s), (c - 26 * s, c + 12 * s)], fill=CYAN)
    for k in (1, 2): d.arc((c - 6 * s - 14 * k * s, c - 14 * k * s - 6 * s, c + 14 * s + 14 * k * s, c + 14 * k * s + 6 * s), -50, 50, fill=CYAN, width=int(6 * s))
    return im

def rays(d, cx, cy, n, r0, r1, col, seed, width=10):
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi); a0 = rnd.uniform(r0, r0 * 1.2)
        d.line((cx + math.cos(a) * a0, cy + math.sin(a) * a0, cx + math.cos(a) * r1, cy + math.sin(a) * r1), fill=col + (255,), width=width)

# ---------- background ----------
_bg = {}
def background(dark=False):
    if dark in _bg: return _bg[dark].copy()
    rng = np.random.default_rng(5 if dark else 4)
    base = np.array(TEAL_D if dark else TEAL, float)
    blot = Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    b = np.array(blot, float)[..., None] / 255
    n = rng.normal(0, 10, (H, W, 1))
    arr = np.clip(base * (0.72 + 0.5 * b) + n, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr, 'RGB').convert('RGBA')
    # vignette
    v = Image.new('L', (W, H), 0); ImageDraw.Draw(v).ellipse((-250, -150, W + 250, H + 150), fill=255); v = v.filter(ImageFilter.GaussianBlur(170))
    shade = Image.new('RGBA', (W, H), (0, 10, 14, 0)); shade.putalpha(Image.eval(v, lambda x: int(170 * (1 - x / 255)))); im.alpha_composite(shade)
    # splatters
    sp = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(sp); rnd = random.Random(9)
    for _ in range(45):
        x, y = rnd.randint(0, W), rnd.randint(0, H); col = rnd.choice([CREAM, YEL, RED, INK])
        for _ in range(rnd.randint(4, 18)):
            s = rnd.uniform(2, 11); dx, dy = rnd.gauss(0, 30), rnd.gauss(0, 30)
            d.ellipse((x + dx - s, y + dy - s, x + dx + s, y + dy + s), fill=col + (170,))
    im.alpha_composite(sp)
    _bg[dark] = im
    return im.copy()

def shake(c, t, amp):
    if amp <= 0: return c
    dx, dy = int(math.sin(t * 90) * amp), int(math.cos(t * 77) * amp)
    o = background(); o.alpha_composite(c, (dx, dy)); return o

def zoom(im, s):
    if s == 1.0: return im
    w, h = int(W * s), int(H * s); big = im.resize((w, h), Image.BICUBIC)
    return big.crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))

def flash(im, a):
    if a <= 0: return im
    return Image.alpha_composite(im, Image.new('RGBA', (W, H), (255, 255, 255, int(255 * min(1, a)))))

