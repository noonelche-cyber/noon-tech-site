"""¡JODER! TikTok — poster style (teal grunge, torn paper cards, yellow paint, stickers)."""
import math, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
TEAL = (11, 105, 116); TEAL_D = (6, 62, 70); INK = (15, 21, 28); CREAM = (246, 233, 212)
PINK = (247, 160, 160); RED = (226, 45, 82); YEL = (252, 213, 73); CYAN = (64, 185, 182)
ANTON = 'Anton-Regular.ttf'; MARK = 'PermanentMarker.ttf'; BANG = 'Bangers-Regular.ttf'; BRUSH = 'CaveatBrush-Regular.ttf'
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
POSTER = 'assets/poster_original.webp'
PAD = 0.3
import os
from lang import LANGS
LANG = os.environ['LANG_CODE']; VSET = os.environ['VSET']; L = LANGS[LANG]
AUD = f'out/{LANG}/{VSET}/'
OUT = f'out/joder_tiktok_{LANG}_voix{VSET}.mp4'

def dur(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
D = [dur(AUD + f's{i}t.wav') + PAD for i in range(1, 6)]
START = [sum(D[:i]) for i in range(5)]
TOTAL = sum(D)

from prims import *

# ---------- pre-built assets ----------
SPL1 = splash(1000, 520, YEL, 2)
HOOK_STRIP = strip(L['hook'][2], 74, seed=11)
JAMAIS = fit(L['hook'][3], MARK, 190, 760, fill=CREAM, stroke=8, emo='🤬', esize=150)
TAG = strip(L['tag'], 46, seed=21)

def word_card(lines, trans, col, size, seed):
    tl = [fit(l, ANTON, size, 700, fill=INK) for l in lines]
    tr = txt(trans, font(BRUSH, 92), RED)
    tw = max(max(l.width for l in tl), tr.width); th = sum(l.height - 10 for l in tl) + tr.height
    w, h = max(820, tw + 210), th + 90
    card = torn(w, h, col, seed)
    y = 24 + 35
    for l in tl: card.alpha_composite(l, (24 + 40, y)); y += l.height - 10
    card.alpha_composite(tr, (24 + 40, y))
    sp = speaker(); card.alpha_composite(sp, (24 + w - sp.width - 30, 24 + 40))
    return card

CARD1 = word_card(['GILIPOLLAS'], L['tr1'], PINK, 150, 31)
CARD2 = word_card(['¡VETE A FREÍR', 'ESPÁRRAGOS!'], L['tr2'], CREAM, 128, 32)
UNDER = [torn(820, 300, YEL, 41), torn(820, 300, CYAN, 42)]

def stack(c, t, card, cy, t0):
    if t < t0: return
    p = pop(t - t0)
    paste(c, UNDER[0], W / 2 + 10, cy + 20, p * 1.02, rot=7)
    paste(c, UNDER[1], W / 2 - 10, cy + 10, p * 1.0, rot=-5)
    paste(c, card, W / 2, cy, pop(t - t0 - 0.06), rot=-3)

def sticker(c, s, x, y, t, t0, rot=8, size=70, col=RED, fg=CREAM):
    if t < t0: return
    l = strip(s, size, col=col, fg=fg, seed=hash(s) % 100, p=BANG)
    paste(c, l, x, y, pop(t - t0, 0.22), rot=rot)

# ---------- scenes ----------
def s1(t):
    c = background(); d = ImageDraw.Draw(c)
    paste(c, SPL1, W / 2, 720, pop(t, 0.3), rot=-2)
    if t > 0.25: rays(d, W / 2, 720, 14, 560, 640, CREAM, 3, 12)
    paste(c, fit(L['hook'][0], ANTON, 210, 880, fill=INK), W / 2, 610, pop(t - 0.05, 0.25), rot=-3)
    paste(c, fit(L['hook'][1], ANTON, 200, 900, fill=RED), W / 2, 815, pop(t - 0.15, 0.25), rot=-3)
    if t > 0.45: paste(c, HOOK_STRIP, W / 2, 1090, pop(t - 0.45, 0.22), rot=2)
    if t > 0.75: paste(c, JAMAIS, W / 2, 1300, pop(t - 0.75, 0.22), rot=-6)
    paste(c, TAG, W / 2, 280, a=fade(t - 1.2, 0.3), rot=-2)
    c = shake(c, t, 10 * (1 - t / 0.3) if t < 0.3 else 0)
    return flash(zoom(c, 1 + 0.02 * t), 1 - t / 0.15 if t < 0.15 else 0)

def s2(t):
    c = background()
    sticker(c, '#1', 220, 520, t, 0.1, rot=-10, size=90)
    p = PT[1]
    stack(c, t, CARD1, 760, p[1])
    if t > p[3]: paste(c, LAB1, W / 2, 1150, pop(t - p[3], 0.22), rot=-2)
    if t > p[4]: paste(c, BUB1, W / 2 + 40, 1380, pop(t - p[4], 0.22), rot=3)
    return zoom(c, 1 + 0.012 * t)

def asparagus(c, t, cy):
    if t < PT[2][3]: return
    a = fade(t - PT[2][3], 0.25)
    layer = Image.new('RGBA', (520, 330)); d = ImageDraw.Draw(layer)
    d.ellipse((40, 150, 480, 300), fill=INK + (255,)); d.ellipse((60, 160, 460, 280), fill=(40, 44, 48, 255))
    d.rectangle((470, 205, 520, 235), fill=INK + (255,))
    for i in range(5):
        x = 120 + i * 62; tilt = (i - 2) * 9
        d.line((x, 240, x + tilt, 60), fill=(110, 170, 70, 255), width=22)
        d.ellipse((x + tilt - 16, 40, x + tilt + 16, 90), fill=(85, 135, 55, 255))
    for i in range(6):
        ph = (t * 3 + i * 0.37) % 1; x = 110 + i * 60; y = 140 - ph * 120
        d.arc((x, y, x + 30, y + 40), 200, 340, fill=CREAM + (int(220 * (1 - ph)),), width=6)
    paste(c, layer, W / 2 + 150, cy, 0.85 + 0.03 * math.sin(t * 12), a=a, rot=-4)

def s3(t):
    c = background()
    sticker(c, '#2', 220, 470, t, 0.1, rot=-10, size=90)
    p = PT[2]
    stack(c, t, CARD2, 760, p[1])
    if t > p[2]: paste(c, LAB2, W / 2, 1140, pop(t - p[2], 0.22), rot=2)
    asparagus(c, t, 1420)
    if t > p[4]: paste(c, bubble('¡VAYA!', 64), 260, 1390, pop(t - p[4], 0.22), rot=-8)
    if t < 0.22:
        off = int(W * (1 - eo(t / 0.22))); bg = background(); bg.alpha_composite(c.crop((0, 0, W - off, H)), (off, 0)); c = bg
    return zoom(c, 1 + 0.012 * t)

CENS_CARD = torn(820, 300, PINK, 71)
dc = ImageDraw.Draw(CENS_CARD)
for i, w in enumerate((560, 700, 430)): dc.rounded_rectangle((90, 70 + i * 80, 90 + w, 70 + i * 80 + 46), 12, fill=INK + (255,))
TAPE = torn(900, 150, YEL, 72, jag=5, shadow=True)
_ct = fit(L['cens'], ANTON, 110, 800, fill=INK); TAPE.alpha_composite(_ct, (24 + (900 - _ct.width) // 2, 24 + (150 - _ct.height) // 2))

def s4(t):
    c = background(dark=True)
    p = PT[3]; tt = max(0.9, p[1] - 0.2)
    paste(c, THIRD, W / 2, 520, pop(t - 0.1, 0.25), rot=-4)
    if t > 0.5: paste(c, CENS_CARD, W / 2, 860, pop(t - 0.5, 0.25), rot=3)
    if t > tt: paste(c, TAPE, W / 2, 860, pop(t - tt, 0.18), rot=-9)
    if t > p[1] + 0.3: paste(c, BUB3, W / 2, 1180, pop(t - p[1] - 0.3, 0.22), rot=-2)
    if t > p[2]: paste(c, INAPP, W / 2, 1390, pop(t - p[2], 0.22), rot=2)
    return zoom(c, 1 + 0.03 * t)

import poster as _poster
PFIT, BTN, CTA_Y = _poster.build(LANG, with_offer=True)
PW, PH = PFIT.size
PBG = PFIT.resize((int(H * PW / PH), H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
PBG = PBG.crop(((PBG.width - W) // 2, 0, (PBG.width - W) // 2 + W, H))
PBG.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 90)))

def offer_sticker():
    l1 = txt('APPLI COMPLÈTE GRATUITE', font(ANTON, 92), CREAM)
    l2 = txt('pour les 30 premiers inscrits !', font(BANG, 66), YEL)
    w, h = max(l1.width, l2.width) + 70, l1.height + l2.height + 30
    im = torn(w, h, RED, 91)
    im.alpha_composite(l1, (24 + (w - l1.width) // 2, 24 + 12)); im.alpha_composite(l2, (24 + (w - l2.width) // 2, 24 + 12 + l1.height))
    return im

def s5(t):
    T = D[4]; c = PBG.copy()
    # One continuous move, never reversing: the full poster eases in, then pushes slowly towards the CTA.
    u = max(0., min(1., t / T)); push = u * u * (3 - 2 * u)
    s = (0.94 + 0.06 * eo(t / 0.35)) * (1.0 + 0.14 * push)
    ax, ay = PW / 2, 1250                                  # zoom anchor on the poster (lower half, near the CTA)
    sx, sy = W / 2, (H - PH) / 2 + ay                      # where that anchor sits on screen
    pw, ph = int(PW * s), int(PH * s)
    img = PFIT.resize((pw, ph), Image.BICUBIC)
    x, y = int(sx - ax * s), int(sy - ay * s)
    c.paste(img, (x, y), img)
    if t > T * 0.55:                                       # pulse the CTA button, same scale as the poster
        p = 1 + 0.07 * abs(math.sin((t - T * 0.55) * 5))
        by = y + CTA_Y * s
        paste(c, BTN, x + pw / 2, by, s * p)
    return flash(c, 0.6 * (1 - t / 0.12) if t < 0.12 else 0)

SCENES = [s1, s2, s3, s4, s5]

import subs
PHR = [[p.lstrip('§') for p in sc] for sc in L['vo']]
SUBS = subs.build(AUD, START, phrases=PHR)
PT = [[a - START[i] for a, b, txt_, sp in SUBS if START[i] <= a < START[i] + D[i]] for i in range(5)]
LAB1 = strip(L['lab1'], 58, seed=51, emo='☕')
BUB1 = bubble(L['bub1'], 56, emo='🥰')
LAB2 = strip(L['lab2'], 52, seed=61)
THIRD = fit(L['third'], MARK, 150, 900, fill=CREAM, stroke=6)
BUB3 = bubble(L['bub3'], 54, emo='😳', col=CREAM)
INAPP = strip(L['inapp'], 64, col=YEL, seed=77, emo='📲')
SUB_FONT = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
_sc = {}
def sub_layer(text, spanish):
    if text in _sc: return _sc[text]
    f = font(SUB_FONT, 58); words = text.split(); lines = ['']
    for w in words:
        trial = (lines[-1] + ' ' + w).strip()
        if hfont(f, trial).getlength(trial) > 900 and lines[-1]: lines.append(w)
        else: lines[-1] = trial
    ls = [txt(l, f, YEL if spanish else (255, 255, 255), stroke=7, sf=(0, 0, 0)) for l in lines]
    im = Image.new('RGBA', (max(l.width for l in ls) + 48, sum(l.height - 8 for l in ls) + 8 + 28))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 26, fill=(0, 0, 0, 120))
    y = 14
    for l in ls: im.alpha_composite(l, ((im.width - l.width) // 2, y)); y += l.height - 8
    _sc[text] = im
    return im

def subtitles(c, t):
    for a, b, text, sp in SUBS:
        if a <= t < b:
            paste(c, sub_layer(text, sp), W / 2, 1585, 1 + 0.12 * (1 - eo((t - a) / 0.12)))
    return c

def mix():
    dl = lambda s: f'adelay={int(s * 1000)}|{int(s * 1000)}'
    ins = [AUD + f's{i}t.wav' for i in range(1, 6)] + ['boom.wav', 'ding.wav', 'whoosh.wav']
    f = ';'.join(f'[{i}]{dl(START[i] + 0.1)}[a{i}]' for i in range(5))
    f += f';[5]asplit=3[b0][b1][b2];[b1]{dl(START[3] + 1.3)}[b1d];[b2]{dl(START[4])}[b2d]'
    f += f';[6]asplit=2[d0][d1];[d0]{dl(START[1] + 0.45)}[d0d];[d1]{dl(START[2] + 0.45)}[d1d];[7]{dl(START[2] - 0.05)}[w]'
    f += ';' + ''.join(f'[a{i}]' for i in range(5)) + '[b0][b1d][b2d][d0d][d1d][w]amix=inputs=11:normalize=0,alimiter=limit=0.95,apad[mix]'
    cmd = ['ffmpeg', '-v', 'error', '-y'] + sum([['-i', x] for x in ins], []) + ['-filter_complex', f, '-map', '[mix]', '-t', f'{TOTAL:.2f}', '-ar', '48000', '-ac', '2', AUD + 'mix2.wav']
    subprocess.run(cmd, check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', AUD + 'video2.mp4', '-i', AUD + 'mix2.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                    '-movflags', '+faststart', OUT], check=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        i = int(sys.argv[1]); tt = float(sys.argv[2]); subtitles(SCENES[i](tt), START[i] + tt).convert('RGB').save(sys.argv[3]); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', AUD + 'video2.mp4'], stdin=subprocess.PIPE)
    for fr in range(int(TOTAL * FPS)):
        t = fr / FPS; i = max(k for k in range(5) if START[k] <= t)
        p.stdin.write(subtitles(SCENES[i](t - START[i]), t).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); mix()
    print('starts', [round(s, 2) for s in START], 'total', round(TOTAL, 2))
