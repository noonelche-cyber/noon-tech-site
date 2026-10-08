import re, sys, json, wave, numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig
V = PiperVoice.load(sys.argv[1])
LINES = {
 "s1": "Si tu parles espagnol et que tu comprends toujours rien quand un Espagnol t'engueule... regarde ça.",
 "s2": "Un : {gilipollas}. Littéralement... pas traduisible poliment. Un Espagnol sur deux l'utilise avant même neuf heures du matin. C'est presque tendre.",
 "s3": "Deux : {a freír espárragos}. Littéralement, va frire des asperges. Oui, les Espagnols t'envoient bouler... en te donnant une recette.",
 "s4": "Et la troisième... celle-là, je peux même pas te la dire ici. Elle est dans l'appli.",
 "s5": "Mon appli t'apprend tout ça : trois cent quarante-cinq expressions, l'audio, le vrai langage de la rue. Bêta en cours, lien en bio. Les trente premiers ont l'accès à vie gratuit.",
}
cfg = SynthesisConfig(length_scale=float(sys.argv[2]) if len(sys.argv)>2 else 0.9, noise_scale=0.6, noise_w_scale=0.7)
def phon(text, lang):
    V.config.espeak_voice = lang
    out = []
    for sent in V.phonemize(text): out += sent
    return out
out = {}
for k, line in LINES.items():
    ph = []
    for i, part in enumerate(re.split(r"[{}]", line)):
        if not part.strip(): continue
        p = phon(part, "es" if i % 2 else "fr")
        if ph: ph += [" "]
        ph += p
    ph = [c for c in ph if c in V.config.phoneme_id_map]
    audio = V.phoneme_ids_to_audio(V.phonemes_to_ids(ph), cfg)
    a = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
    with wave.open(f"vo_{k}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(V.config.sample_rate); w.writeframes(a.tobytes())
    out[k] = len(a) / V.config.sample_rate
print(json.dumps(out)); print("total", sum(out.values()))
