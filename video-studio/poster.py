"""Localized rebuild of the ¡JODER! beta-tester poster (1080x1620), in the style of the original artwork."""
import math, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from prims import (hfont, font, txt, fit, paste, torn, splash, bubble, speaker, rays,
                   TEAL, INK, CREAM, PINK, RED, YEL, CYAN, ANTON, MARK, BANG, BRUSH)
from lang import LANGS

PW, PH = 1080, 1620
SCREEN = (250, 196, 190)

def wrap(s, f, maxw):
    lines = ['']
    for w in s.split():
        t = (lines[-1] + ' ' + w).strip()
        if hfont(f, t).getlength(t) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = t
    return lines

def block(lines, f, fill, gap=-6, align='center'):
    ls = [txt(l, f, fill) for l in lines]
    im = Image.new('RGBA', (max(l.width for l in ls), sum(l.height + gap for l in ls) - gap))
    y = 0
    for l in ls:
        x = (im.width - l.width) // 2 if align == 'center' else 0
        im.alpha_composite(l, (x, y)); y += l.height + gap
    return im

def poster_bg():
    rng = np.random.default_rng(14)
    blot = Image.fromarray((rng.random((PH // 8, PW // 8)) * 255).astype(np.uint8)).resize((PW, PH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    b = np.array(blot, float)[..., None] / 255
    arr = np.clip(np.array(TEAL, float) * (0.7 + 0.55 * b) + rng.normal(0, 10, (PH, PW, 1)), 0, 255).astype(np.uint8)
    im = Image.fromarray(arr, 'RGB').convert('RGBA')
    sp = Image.new('RGBA', (PW, PH)); d = ImageDraw.Draw(sp); rnd = random.Random(19)
    for _ in range(40):
        x, y = rnd.randint(0, PW), rnd.randint(0, PH); col = rnd.choice([CREAM, YEL, RED, INK])
        for _ in range(rnd.randint(4, 16)):
            s = rnd.uniform(2, 10); dx, dy = rnd.gauss(0, 28), rnd.gauss(0, 28)
            d.ellipse((x + dx - s, y + dy - s, x + dx + s, y + dy + s), fill=col + (160,))
    im.alpha_composite(sp)
    return im

def brush_strokes(d, pts, col, w=10):
    for (x0, y0, x1, y1) in pts: d.line((x0, y0, x1, y1), fill=col + (255,), width=w)

# ---------- icons ----------
def icon(kind, r=64, col=PINK):
    im = Image.new('RGBA', (2 * r + 10, 2 * r + 10)); d = ImageDraw.Draw(im); c = r + 5
    d.ellipse((5, 5, 2 * r + 5, 2 * r + 5), fill=col + (255,))
    k = INK + (255,); w = 6
    if kind == 'game':
        d.rounded_rectangle((c - 40, c - 20, c + 40, c + 22), 18, outline=k, width=w)
        d.line((c - 26, c, c - 12, c), fill=k, width=w); d.line((c - 19, c - 7, c - 19, c + 7), fill=k, width=w)
        d.ellipse((c + 12, c - 8, c + 20, c), fill=k); d.ellipse((c + 22, c, c + 30, c + 8), fill=k)
    elif kind == 'book':
        d.polygon([(c - 42, c - 26), (c - 4, c - 18), (c - 4, c + 30), (c - 42, c + 22)], outline=k, width=w)
        d.polygon([(c + 42, c - 26), (c + 4, c - 18), (c + 4, c + 30), (c + 42, c + 22)], outline=k, width=w)
    elif kind == 'globe':
        d.ellipse((c - 38, c - 38, c + 38, c + 38), outline=k, width=w); d.ellipse((c - 16, c - 38, c + 16, c + 38), outline=k, width=5)
        d.line((c - 38, c, c + 38, c), fill=k, width=5); d.arc((c - 36, c - 52, c + 36, c - 10), 30, 150, fill=k, width=4); d.arc((c - 36, c + 10, c + 36, c + 52), 210, 330, fill=k, width=4)
    elif kind == 'audio':
        d.polygon([(c - 34, c - 12), (c - 18, c - 12), (c, c - 30), (c, c + 30), (c - 18, c + 12), (c - 34, c + 12)], outline=k, width=w)
        for q in (1, 2): d.arc((c - 8 - 14 * q, c - 14 * q - 6, c + 12 + 14 * q, c + 14 * q + 6), -50, 50, fill=k, width=w)
    elif kind == 'phone':
        d.rounded_rectangle((c - 22, c - 40, c + 22, c + 40), 8, outline=k, width=w); d.line((c - 6, c + 30, c + 6, c + 30), fill=k, width=4)
    return im

def plane(size=56):
    im = Image.new('RGBA', (size + 8, size + 8)); d = ImageDraw.Draw(im); s = size
    d.polygon([(4, s * 0.45), (s, 4), (s * 0.6, s), (s * 0.45, s * 0.6)], outline=INK + (255,), width=5)
    d.line((s * 0.45, s * 0.6, s, 4), fill=INK + (255,), width=5)
    return im

# ---------- phone mockup ----------
def phone(L):
    w, h = 430, 860
    im = Image.new('RGBA', (w + 30, h + 30)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 18, w + 14, h + 18), 70, fill=(0, 0, 0, 120))
    d.rounded_rectangle((0, 0, w, h), 70, fill=(40, 44, 50, 255)); d.rounded_rectangle((6, 6, w - 6, h - 6), 64, fill=(200, 205, 212, 255))
    d.rounded_rectangle((16, 16, w - 16, h - 16), 56, fill=SCREEN + (255,))
    d.rounded_rectangle((w / 2 - 70, 16, w / 2 + 70, 46), 15, fill=(20, 22, 26, 255))
    d.text((48, 30), '17:49', font=font(BANG, 26), fill=INK)
    paste(im, txt('joder!', font(MARK, 66), INK, stroke=3, sf=CREAM), 150, 110, rot=4)
    d.rounded_rectangle((44, 160, 250, 182), 11, fill=(255, 255, 255, 200)); d.rounded_rectangle((44, 160, 210, 182), 11, fill=CYAN + (255,))
    d.rounded_rectangle((300, 140, 395, 192), 10, outline=INK + (255,), width=3)
    l = txt('345/345', font(BANG, 26), INK); im.alpha_composite(l, (348 - l.width // 2, 152))
    im.alpha_composite(txt('GILIPOLLAS', font(ANTON, 52), INK), (36, 205))
    im.alpha_composite(fit(L['tr1'], BRUSH, 34, 230, fill=RED), (36, 280))
    for i in range(3):
        x = 285 + i * 46; d.ellipse((x, 222, x + 40, 262), fill=CREAM + (255,), outline=CYAN + (255,), width=3)
    y = 336
    for i, row in enumerate(L['p_rows']):
        last = i == len(L['p_rows']) - 1
        d.rounded_rectangle((34, y, w - 34, y + 62), 10, fill=((255, 205, 205, 255) if last else (255, 240, 236, 255)), outline=(RED if last else CYAN) + (255,), width=3)
        rs = 26
        while hfont(font(BANG, rs), row).getlength(row) > w - 150 and rs > 16: rs -= 1
        t = txt(row, font(BANG, rs), RED if last else INK); im.alpha_composite(t, (48, y + (62 - t.height) // 2))
        d.line((w - 70, y + 26, w - 60, y + 36, w - 50, y + 26), fill=INK + (255,), width=3)
        y += 72
    d.rounded_rectangle((16, h - 112, w - 16, h - 16), 0, fill=(52, 40, 46, 255)); d.rounded_rectangle((16, h - 70, w - 16, h - 16), 56, fill=(52, 40, 46, 255))
    for i in range(5):
        x = 62 + i * 77; yy = h - 72
        col = YEL if i == 1 else (240, 220, 220)
        d.rounded_rectangle((x - 16, yy - 18, x + 16, yy + 16), 6, outline=col + (255,), width=3)
    return im

# ---------- poster ----------
def build(code, with_offer=True):
    L = LANGS[code]; c = poster_bg(); d = ImageDraw.Draw(c)
    # logo + rays
    brush_strokes(d, [(40, 60, 70, 110), (620, 40, 650, 90), (660, 120, 710, 130), (60, 300, 100, 320)], CREAM, 9)
    paste(c, fit('¡JODER!', MARK, 230, 600, fill=CREAM, stroke=12, sf=INK), 320, 180, rot=-6)
    # pink splash
    sp = splash(370, 300, RED, 7); paste(c, sp, 885, 175, rot=-6)
    if with_offer:
        o1 = block(wrap(L['offer'][0], font(ANTON, 44), 300), font(ANTON, 44), CREAM, gap=-4)
        o2 = block(wrap(L['offer'][1], font(BANG, 32), 280), font(BANG, 32), YEL, gap=-6)
        ob = Image.new('RGBA', (max(o1.width, o2.width), o1.height + o2.height + 4)); ob.alpha_composite(o1, ((ob.width - o1.width) // 2, 0)); ob.alpha_composite(o2, ((ob.width - o2.width) // 2, o1.height + 4))
        paste(c, ob, 885, 178, rot=-8)
    else:
        paste(c, block(wrap(L['p_splash'], font(BANG, 40), 270), font(BANG, 40), INK, gap=-4), 895, 170, rot=-8)
    # tagline strip (last part in red)
    a, b, red = L['p_tag']; f = font(BANG, 42)
    l1 = txt(a, f, INK); l2a = txt(b, f, INK) if b else None; l2b = txt(red, f, RED)
    w2 = (l2a.width - 14 if l2a else 0) + l2b.width
    st = torn(max(l1.width, w2) + 40, l1.height + l2b.height + 6, CREAM, 81, jag=5)
    st.alpha_composite(l1, (44, 34)); x = 44
    if l2a: st.alpha_composite(l2a, (x, 34 + l1.height - 6)); x += l2a.width - 14
    st.alpha_composite(l2b, (x, 34 + l1.height - 6))
    paste(c, st, 300, 390, rot=-4)
    # insult cards
    for col, cx, cy, rot, seed in ((YEL, 270, 600, 6, 1), (CYAN, 262, 630, -5, 2), (CYAN, 255, 835, 4, 3)):
        paste(c, torn(470, 200, col, seed), cx, cy, rot=rot)
    def card(lines, tr, col, seed, size):
        tl = [fit(x, ANTON, size, 330, fill=INK) for x in lines]
        trl = fit(tr, BRUSH, 48, 340, fill=RED)
        h = sum(x.height - 8 for x in tl) + trl.height + 30
        cd = torn(450, h, col, seed); y = 40
        for x in tl: cd.alpha_composite(x, (50, y)); y += x.height - 8
        cd.alpha_composite(trl, (50, y))
        spk = speaker(36); cd.alpha_composite(spk, (450 - 30, 44))
        return cd
    paste(c, card(['GILIPOLLAS'], L['tr1'], PINK, 11, 76), 285, 600, rot=-3)
    paste(c, card(['A FREÍR', 'ESPÁRRAGOS'], L['tr2'], CREAM, 12, 60), 275, 830, rot=-4)
    # phone
    paste(c, phone(L), 805, 700, 0.95, rot=-7)
    # bubbles
    paste(c, bubble('¡VAYA!', 40), 90, 1010, 0.85, rot=8)
    paste(c, bubble('¡MÁS QUE UN DICCIO!', 30), 960, 1075, 0.8, rot=-6)
    # beta testers splash
    paste(c, splash(720, 250, YEL, 5), 400, 1175, rot=-3)
    b0 = fit(L['p_big'][0], BANG, 128, 660, fill=INK); b1 = fit(L['p_big'][1], BANG, 140, 680, fill=RED, stroke=4, sf=INK)
    paste(c, b0, 400, 1115, rot=-5); paste(c, b1, 410, 1225, rot=-5)
    d.line((170, 1300, 640, 1280), fill=INK + (255,), width=7)
    rays(d, 400, 1175, 8, 420, 470, CREAM, 8, 9)
    # icons row
    kinds = ['game', 'book', 'globe', 'audio', 'phone']; cols = [PINK, CYAN, YEL, PINK, CYAN]
    for i, (k, col, lab) in enumerate(zip(kinds, cols, L['p_icons'])):
        x = 108 + i * 216
        paste(c, icon(k, 60, col), x, 1375)
        f = font(BANG, 25); bl = block(wrap(lab, f, 180), f, INK, gap=-6)
        stp = torn(bl.width + 24, bl.height + 10, CREAM, 30 + i, jag=4, shadow=False)
        stp.alpha_composite(bl, (36, 29)); paste(c, stp, x, 1478, rot=(-2 if i % 2 else 2))
    # CTA pill
    f = font(BANG, 58); t = txt(L['p_cta'], f, INK); pl = plane(54)
    bw, bh = t.width + pl.width + 90, 96
    btn = Image.new('RGBA', (bw + 10, bh + 10)); bd = ImageDraw.Draw(btn)
    bd.rounded_rectangle((6, 8, bw + 6, bh + 8), 48, fill=(0, 0, 0, 110)); bd.rounded_rectangle((0, 0, bw, bh), 48, fill=CREAM + (255,))
    btn.alpha_composite(pl, (34, (bh - pl.height) // 2)); btn.alpha_composite(t, (34 + pl.width + 20, (bh - t.height) // 2))
    cta_y = 1565
    for s in (-1, 1):
        for k in range(3):
            x0 = PW / 2 + s * (bw / 2 + 20); a = math.radians(-30 + k * 30)
            d.line((x0, cta_y + math.sin(a) * 10, x0 + s * 40 * math.cos(a), cta_y + math.sin(a) * 40), fill=RED + (255,), width=7)
    paste(c, btn, PW / 2, cta_y)
    return c, btn, cta_y

def offer(L):
    l1 = txt(L['offer'][0], font(ANTON, 92), CREAM)
    l2 = txt(L['offer'][1], font(BANG, 66), YEL)
    w, h = max(l1.width, l2.width) + 70, l1.height + l2.height + 30
    im = torn(w, h, RED, 91)
    im.alpha_composite(l1, (24 + (w - l1.width) // 2, 24 + 12)); im.alpha_composite(l2, (24 + (w - l2.width) // 2, 24 + 12 + l1.height))
    return im

if __name__ == '__main__':
    import os; os.makedirs('out/posters', exist_ok=True)
    for code in (sys.argv[1].split(',') if len(sys.argv) > 1 else LANGS):
        im, _, _ = build(code)
        im.convert('RGB').save(f'out/posters/joder_poster_{code}.png'); print(code)
