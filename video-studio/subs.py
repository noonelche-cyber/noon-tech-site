"""Subtitle timing: split each scene's voiceover into phrases and snap phrase boundaries to pauses in the audio."""
import re, subprocess, wave

PHRASES = {
    's1': ["Tu parles espagnol,", "mais quand un Espagnol t'engueule,", "tu captes rien ?", "Regarde."],
    's2': ["Un :", "¡Gilipollas!", "Pas traduisible poliment.", "En Espagne, tu l'entends avant même le premier café.", "C'est presque affectueux."],
    's3': ["Deux :", "¡Vete a freír espárragos!", "Littéralement :", "va faire frire des asperges.", "Oui… on t'envoie balader,", "avec une recette."],
    's4': ["Et la troisième…", "celle-là, je peux pas te la dire ici.", "Elle est dans l'appli."],
    's5': ["¡Joder!", "345 expressions, l'audio, des exemples et des jeux.", "Je cherche des bêta-testeurs :",
           "les 30 premiers inscrits ont l'appli complète gratuite !", "Écris-moi en privé."],
}
SPANISH = {"¡Gilipollas!", "¡Vete a freír espárragos!", "¡Joder!"}

def duration(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()

def pauses(p):
    out = subprocess.run(['ffmpeg', '-i', p, '-af', 'silencedetect=n=-38dB:d=0.09', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    return [(a + b) / 2 for a, b in zip(st, en)]

def timings(path, phrases):
    d = duration(path); ps = pauses(path)
    weights = [max(len(re.sub(r'\W', '', p)), 3) for p in phrases]
    tot = sum(weights); est = []; acc = 0
    for w in weights[:-1]:
        acc += w; est.append(acc / tot * d)
    cuts, last = [], 0.0
    for i, e in enumerate(est):
        cands = [p for p in ps if p > last + 0.25 and p < d - 0.25 and abs(p - e) < 0.9]
        c = min(cands, key=lambda p: abs(p - e)) if cands else max(e, last + 0.3)
        cuts.append(c); last = c
    b = [0.0] + cuts + [d]
    return [(b[i], b[i + 1], phrases[i]) for i in range(len(phrases))]

def build(aud, starts, delay=0.1, phrases=None):
    """Absolute (start, end, text, is_spanish) list for the whole video."""
    out = []
    for i in range(5):
        k = f's{i + 1}'
        for a, b, t in timings(f'{aud}{k}t.wav', phrases[i] if phrases else PHRASES[k]):
            out.append((starts[i] + delay + a, starts[i] + delay + b, t, t in SPANISH))
    return out

if __name__ == '__main__':
    import sys
    for a, b, t, s in build(sys.argv[1], [0] * 5):
        print(f'{a:6.2f} {b:6.2f} {"ES" if s else "  "} {t}')
