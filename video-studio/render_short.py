"""Short "insult of the day" episodes (~13 s): word on screen from the first frame, literal, meaning, context, CTA.
usage: python render_short.py <lang> <n>   →  out/short/joder_short_<lang>_<n>.mp4"""
import math, os, subprocess, sys, wave
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw
from prims import *
import subs
from episodes import EPISODES, SERIES, SUB, LOCALE

LANG, N = sys.argv[1], int(sys.argv[2])
EP = next(e for e in EPISODES[LANG] if e['n'] == N)
D = f'out/short/{LANG}{N}/'; os.makedirs(D, exist_ok=True)
VOICE = 'es-ES-Ximena:DragonHDLatestNeural'

# ---------- voice ----------
def synth(text, loc, out, voice=VOICE):
    ssml = (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{loc}">' +
            (f'<voice name="{voice}">{escape(text)}</voice></speak>' if voice != VOICE else
             f'<voice name="{voice}"><lang xml:lang="{loc}">{escape(text)}</lang></voice></speak>'))
    r = subprocess.run(['curl', '-sS', '-o', out, '-w', '%{http_code}', '-X', 'POST',
        'https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1', '-H', 'Content-Type: application/ssml+xml',
        '-H', 'X-Microsoft-OutputFormat: riff-48khz-16bit-mono-pcm', '-H', 'User-Agent: noon-tiktok', '--data-binary', ssml.encode()],
        capture_output=True, text=True)
    assert r.stdout == '200', r.stdout

def tts():
    # Split into same-language runs; "¡Joder!" is always its own Spanish request, so it never gets a French/English accent.
    runs = []
    for p in EP['lines']:
        if p.startswith('§'): parts = [('es-ES', p[1:])]
        else:
            parts = []
            for i, chunk in enumerate(p.split('¡Joder!')):
                if i: parts.append(('es-ES', '¡Joder!'))
                if chunk.strip(' :'): parts.append((LOCALE[LANG], chunk.strip(' :')))
        for loc, t in parts:
            if runs and runs[-1][0] == loc and t != '¡Joder!' and runs[-1][1] != '¡Joder!': runs[-1][1] += ' ' + t
            else: runs.append([loc, t])
    files = []
    for i, (loc, t) in enumerate(runs):
        f = f'{D}part{i}.wav'
        # app name: Spanish-only voice (same Ximena persona), so it can never pick up a foreign accent
        synth(t, loc, f, 'es-ES-XimenaNeural' if t == '¡Joder!' else VOICE); files.append(f)
    inputs = sum([['-i', f] for f in files], [])
    chain = ''.join(f'[{i}]apad=pad_dur=0.12[p{i}];' for i in range(len(files))) + ''.join(f'[p{i}]' for i in range(len(files)))
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', chain + f'concat=n={len(files)}:v=0:a=1[a]', '-map', '[a]', D + 'raw.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'raw.wav', '-af',
        'silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.25:stop_threshold=-42dB,'
        'areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse', D + 'vo.wav'], check=True)
    print('runs:', runs)

if not os.path.exists(D + 'vo.wav'): tts()
with wave.open(D + 'vo.wav') as w: VO = w.getnframes() / w.getframerate()
LEAD = 0.15
PH = [(a + LEAD, b + LEAD, t) for a, b, t in subs.timings(D + 'vo.wav', [p.lstrip('§') for p in EP['lines']])]
TOTAL = VO + LEAD + 0.6
T = [p[0] for p in PH]                       # start time of each phrase

# ---------- assets ----------
L = EP['lines']; word = L[1].lstrip('§')
HEAD = strip(f"{SERIES[LANG]} #{N}", 56, col=RED, fg=CREAM, seed=5)
SUBT = txt(SUB[LANG], font(BANG, 48), CREAM)
HOOK = strip(L[0], 58, seed=11)
def word_card():
    t = fit(word.upper(), ANTON, 150, 760, fill=INK)
    card = torn(max(t.width + 160, 760), t.height + 70, PINK, 31)
    card.alpha_composite(t, (24 + 40, 24 + 30)); sp = speaker(52); card.alpha_composite(sp, (card.width - sp.width - 40, 24 + 28))
    return card
CARD = word_card(); UNDER = [torn(760, 260, YEL, 41), torn(760, 260, CYAN, 42)]
LIT = strip(L[2], 60, seed=61, emo=EP['emo'])
MEAN_T = fit(L[3], BRUSH, 96, 900, fill=RED)
MEAN = torn(MEAN_T.width + 60, MEAN_T.height + 20, CREAM, 71); MEAN.alpha_composite(MEAN_T, (24 + 30, 24 + 10))
CTX = bubble(L[4], 50, emo='😅')
LOGO = Image.open('assets/joder.png').convert('RGBA').resize((300, 300), Image.LANCZOS)
m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 299, 299), 64, fill=255); LOGO.putalpha(m)
CTA = strip(L[5], 58, col=YEL, seed=77, emo='📩')

def frame(t):
    c = background(); d = ImageDraw.Draw(c)
    # series header: there from frame 1
    paste(c, HEAD, W / 2, 300, pop(t, 0.25), rot=-3); paste(c, SUBT, W / 2, 395, a=fade(t - 0.2, 0.3), rot=-3)
    if t < T[5]:
        paste(c, HOOK, W / 2, 560, pop(t - 0.05, 0.22), rot=2)
        # the Spanish word is on screen from the very start; it punches again when it is spoken
        paste(c, UNDER[0], W / 2 + 10, 830, pop(t - 0.1) * 1.02, rot=6); paste(c, UNDER[1], W / 2 - 10, 820, pop(t - 0.1), rot=-4)
        pulse = 1 + 0.12 * max(0, 1 - abs(t - T[1] - 0.1) / 0.18)
        paste(c, CARD, W / 2, 810, pop(t - 0.15) * pulse, rot=-3)
        if t > T[2]: paste(c, LIT, W / 2, 1090, pop(t - T[2], 0.22), rot=-2)
        if t > T[3]: paste(c, MEAN, W / 2, 1260, pop(t - T[3], 0.22), rot=2)
        if t > T[4]: paste(c, CTX, W / 2 + 30, 1460, pop(t - T[4], 0.22), rot=-3)
    else:
        u = t - T[5]
        paste(c, LOGO, W / 2, 840, pop(u, 0.3), rot=-4)
        rays(d, W / 2, 840, 12, 230, 290, CREAM, 3, 10)
        paste(c, CTA, W / 2, 1140, pop(u - 0.15, 0.22), rot=2)
    return zoom(c, 1 + 0.015 * t)

if __name__ == '__main__':
    if len(sys.argv) > 3: frame(float(sys.argv[3])).convert('RGB').save(sys.argv[4]); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', D + 'video.mp4'], stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)): p.stdin.write(frame(f / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    ms = lambda s: int(s * 1000)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'vo.wav', '-i', 'ding.wav', '-i', 'boom.wav', '-filter_complex',
        f'[0]adelay={ms(LEAD)}|{ms(LEAD)}[v];[1]adelay={ms(T[1])}|{ms(T[1])}[d];[2]adelay={ms(T[5])}|{ms(T[5])}[b];'
        f'[v][d][b]amix=inputs=3:normalize=0,alimiter=limit=0.95,apad[m]', '-map', '[m]', '-t', f'{TOTAL:.2f}', '-ac', '2', D + 'mix.wav'], check=True)
    out = f'out/short/joder_short_{LANG}_{N}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'video.mp4', '-i', D + 'mix.wav', '-c:v', 'libx264', '-b:v', '5M', '-maxrate', '6M',
                    '-bufsize', '10M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    print(out, f'{TOTAL:.1f}s')
