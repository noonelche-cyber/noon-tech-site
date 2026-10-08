import wave, json, numpy as np
SR = 44100
def load(p):
    with wave.open(p) as w:
        sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
    # resample to SR
    n = int(len(a)*SR/sr); a = np.interp(np.linspace(0, len(a)-1, n), np.arange(len(a)), a)
    idx = np.where(np.abs(a) > 0.02)[0]
    return a[max(idx[0]-400,0): idx[-1]+2000]
vo = {k: load(f"vo_{k}_f.wav") for k in ["s1","s2","s3","s4","s5"]}
L = {k: len(v)/SR for k, v in vo.items()}
T = {}; at = {}
at["s1"] = 0.15; T["s1"] = {"start": 0}
s2 = at["s1"]+L["s1"]+0.15; at["s2"] = s2+0.1
T["s2"] = {"start": s2, "word": at["s2"]+0.4, "c1": at["s2"]+1.5, "c2": at["s2"]+0.55*L["s2"], "c3": at["s2"]+L["s2"]-1.1}
s3 = at["s2"]+L["s2"]+0.2; at["s3"] = s3+0.3
T["s3"] = {"start": s3, "word": at["s3"]+0.4, "pan": at["s3"]+1.0, "c1": at["s3"]+1.6, "c2": at["s3"]+0.3*L["s3"]+0.6}
s4 = at["s3"]+L["s3"]+0.2; at["s4"] = s4+0.7
T["s4"] = {"start": s4, "cens": s4+0.55, "t": at["s4"]+0.2, "app": at["s4"]+L["s4"]-1.3}
s5 = at["s4"]+L["s4"]+0.25; at["s5"] = s5+0.2
T["s5"] = {"start": s5, "stamp": s5+0.6, "t1": at["s5"]+0.22*L["s5"], "t2": at["s5"]+0.6*L["s5"], "t3": at["s5"]+0.76*L["s5"]}
total = at["s5"]+L["s5"]+0.35
for a, b in [("s1","s2"),("s2","s3"),("s3","s4"),("s4","s5")]: T[a]["end"] = T[b]["start"]
T["s5"]["end"] = total; T["total"] = total
open("timeline.js","w").write("window.TL="+json.dumps(T, indent=1)+";")
json.dump({"T": T, "at": at}, open("timeline.json","w"), indent=1)

# ---- SFX
rng = np.random.default_rng(3)
def tt(d): return np.arange(int(d*SR))/SR
def env(d, a=0.005, r=None):
    t = tt(d); e = np.minimum(t/a, 1); return e*np.exp(-t/(r or d/4))
def ding():
    t = tt(1.2); return sum(np.sin(2*np.pi*f*t)*g for f, g in [(1318,1),(2637,.35),(3951,.15)])*np.exp(-t*4)*.5
def boom():
    t = tt(0.9); f = 120*np.exp(-t*6)+40; ph = 2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)*np.exp(-t*4)*1.0 + rng.normal(0,1,len(t))*np.exp(-t*30)*.25)
def whoosh(d=0.45):
    n = rng.normal(0,1,int(d*SR)); t = tt(d)
    # moving one-pole lowpass
    out = np.zeros_like(n); y = 0
    for i in range(len(n)):
        c = 0.02+0.5*(t[i]/d); y += c*(n[i]-y); out[i] = y
    return out*np.sin(np.pi*t/d)**2*1.2
def click():
    t = tt(0.06); return np.sin(2*np.pi*900*t)*np.exp(-t*80)*.5
def sizzle(d):
    n = rng.normal(0,1,int(d*SR)); n = n - np.convolve(n, np.ones(8)/8, "same")
    crack = (rng.random(len(n)) > .9993)*rng.normal(0,3,len(n))
    t = tt(d); e = np.minimum(t/0.3,1)*np.minimum((d-t)/0.3,1)
    return (n*.35+crack)*e*.35
def heartbeat():
    t = tt(0.25); b = np.sin(2*np.pi*55*t)*np.exp(-t*18)
    out = np.zeros(int(0.6*SR)); out[:len(b)] += b; out[int(.18*SR):int(.18*SR)+len(b)] += b*.7; return out
def stamp():
    return boom()*.7 + np.concatenate([rng.normal(0,1,int(.05*SR))*np.exp(-tt(.05)*60), np.zeros(int(.85*SR))])[:int(.9*SR)]*.6

def build(with_vo=True):
    mix = np.zeros(int((total+1)*SR))
    def put(sig, t, g=1.0):
        i = int(t*SR); j = min(len(mix), i+len(sig)); mix[i:j] += sig[:j-i]*g
    put(whoosh(.35), 0, .5); put(boom(), 0.0, .6)
    put(boom(), T["s1"]["start"]+0.75, .8)
    put(boom(), T["s2"]["start"], .9)       # "beat drop" à l'entrée de la 1re insulte
    put(ding(), T["s2"]["word"], .55)
    for k in ["c1","c2","c3"]: put(click(), T["s2"][k], .5)
    put(whoosh(), T["s3"]["start"]-0.15, .7)
    put(ding(), T["s3"]["word"], .55)
    put(sizzle(T["s4"]["start"]-T["s3"]["pan"]), T["s3"]["pan"], .5)
    for k in ["c1","c2"]: put(click(), T["s3"][k], .5)
    put(boom(), T["s4"]["cens"], .9)
    for i in range(int((T["s4"]["end"]-T["s4"]["start"]-0.9)/0.75)): put(heartbeat(), T["s4"]["start"]+0.9+i*0.75, .7)
    put(whoosh(.3), T["s5"]["start"]-0.1, .6)
    put(stamp(), T["s5"]["stamp"], .8)
    for k in ["t1","t3"]: put(click(), T["s5"][k], .5)
    put(boom(), T["s5"]["t2"], .6)
    sfx_gain = 0.42 if with_vo else 0.6
    mix *= sfx_gain
    if with_vo:
        for k, v in vo.items(): put(v, at[k], 1.0)
    mix = mix[:int(total*SR)]
    mix /= max(1e-6, np.abs(mix).max()/0.95)
    return mix
for name, wv in [("mix_vo", True), ("mix_sfx", False)]:
    m = (build(wv)*32767).astype(np.int16)
    with wave.open(name+".wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(m.tobytes())
print(json.dumps(L)); print("total", round(total,2))
