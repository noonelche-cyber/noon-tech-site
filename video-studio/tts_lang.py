"""Generate voiceover for one language and voice set: out/<lang>/<A|B>/s1..s5t.wav"""
import json, os, subprocess, sys
from xml.sax.saxutils import escape
from lang import LANGS, ES_VOICE_A, VOICE_B

STYLES = {v['ShortName']: v.get('StyleList') or [] for v in json.load(open('voices.json'))}
def style_for(voice, prefs):
    return next((s for s in prefs if s in STYLES.get(voice, [])), None)

def seg(voice, lang, text, prefs, multilingual):
    t = escape(text)
    if multilingual: t = f'<lang xml:lang="{lang}">{t}</lang>'
    st = style_for(voice, prefs)
    if st: t = f'<mstts:express-as style="{st}">{t}</mstts:express-as>'
    return f'<voice name="{voice}">{t}</voice>'

def ssml(L, phrases, vset):
    groups = []
    for p in phrases:
        es = p.startswith('§'); p = p.lstrip('§')
        if groups and groups[-1][0] == es: groups[-1][1].append(p)
        else: groups.append((es, [p]))
    body = ''
    for es, ps in groups:
        text = ' '.join(ps)
        if vset == 'A':
            v = ES_VOICE_A if es else L['voiceA']
            body += seg(v, 'es-ES' if es else L['locale'], text, ['excited'] if es else ['joyful', 'friendlycheerful', 'cheerful'], False)
        else:
            body += seg(VOICE_B, 'es-ES' if es else L['locale'], text, [], True)
    return ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" '
            f'xml:lang="{L["locale"]}">{body}</speak>')

def run(code, vset):
    L = LANGS[code]; d = f'out/{code}/{vset}/'; os.makedirs(d, exist_ok=True)
    for i, phrases in enumerate(L['vo']):
        raw, out = f'{d}s{i+1}.wav', f'{d}s{i+1}t.wav'
        r = subprocess.run(['curl', '-sS', '-o', raw, '-w', '%{http_code}', '-X', 'POST',
            'https://francecentral.tts.speech.microsoft.com/cognitiveservices/v1',
            '-H', 'Content-Type: application/ssml+xml', '-H', 'X-Microsoft-OutputFormat: riff-48khz-16bit-mono-pcm',
            '-H', 'User-Agent: noon-tiktok', '--data-binary', ssml(L, phrases, vset).encode()], capture_output=True, text=True)
        if r.stdout != '200': sys.exit(f'{code} {vset} s{i+1}: HTTP {r.stdout} {open(raw, errors="replace").read()[:200]}')
        af = ('silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.28:stop_threshold=-42dB,'
              'areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse')
        if vset == 'A': af += ',atempo=1.12'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', af, out], check=True)
    durs = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{d}s{i}t.wav'],
            capture_output=True, text=True).stdout) for i in range(1, 6)]
    print(code, vset, ' '.join(f'{x:.1f}' for x in durs), f'= {sum(durs):.1f}s')

if __name__ == '__main__':
    for code in sys.argv[1].split(','):
        for vset in sys.argv[2].split(','):
            run(code, vset)
