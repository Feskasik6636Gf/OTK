"""Synthesizes the sound effects + music bed for the plane video (numpy) and converts the user's own SFX. python tools/make_sfx_plane.py <user_sfx_dir>"""
import numpy as np, wave, sys, os, subprocess
SR = 48000
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sfx")
rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(SR * d)) / SR
def save(name, x, peak=0.9):
    x = np.asarray(x, float); x = x / max(np.abs(x).max(), 1e-9) * peak
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype("<i2").tobytes())
def noise(d): return rng.standard_normal(int(SR * d))
def lp(x, fc):  # one-pole lowpass (applied twice)
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y
def lpf(x, fc): return lp(lp(x, fc), fc)
def hpf(x, fc): return x - lpf(x, fc)
def bp(x, lo, hi): return hpf(lpf(x, hi), lo)
def env(d, a=0.01, r=None, curve=3):
    n = int(SR * d); e = np.ones(n); na = max(1, int(SR * a)); e[:na] = np.linspace(0, 1, na)
    r = r if r is not None else d - a; nr = n - na
    e[na:] = np.exp(-curve * np.linspace(0, 1, nr) * (d - a) / max(r, 1e-3))
    return e
def sine(f, d): 
    t = t_(d); f = np.broadcast_to(f, t.shape) if np.ndim(f) else np.full_like(t, f)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def saw(f, d):
    t = t_(d); f = np.full_like(t, f) if not np.ndim(f) else f
    ph = np.cumsum(f) / SR % 1.0; return 2 * ph - 1
def sweep(a, b, d): return np.linspace(a, b, int(SR * d))

save("whoosh", bp(noise(0.7), 300, 5000) * np.sin(np.linspace(0, np.pi, int(SR * 0.7))) ** 2)
save("swoosh", bp(noise(1.2), 500, 7000) * np.sin(np.linspace(0, np.pi, int(SR * 1.2))) ** 1.5)
d = 0.45; save("thud", (sine(sweep(110, 45, d), d) * env(d, 0.003, curve=6) + 0.35 * lpf(noise(d), 600) * env(d, 0.002, curve=9)))
d = 0.3; save("stomp", sine(sweep(140, 60, d), d) * env(d, 0.002, curve=8) + 0.5 * lpf(noise(d), 1500) * env(d, 0.001, curve=14))
d = 1.6; save("boom_synth", sine(sweep(70, 28, d), d) * env(d, 0.004, curve=3.5) + 0.7 * lpf(noise(d), 500) * env(d, 0.003, curve=4))
d = 1.0; save("splash", (bp(noise(d), 800, 7000) * env(d, 0.01, curve=3.2)) + 0.3 * lpf(noise(d), 300) * env(d, 0.01, curve=4))
d = 0.35; c = hpf(noise(d), 1500) * env(d, 0.001, curve=14)
for k in range(6): i = int(rng.uniform(0, 0.2) * SR); c[i:i + 120] += rng.standard_normal(120) * 1.5
save("crack", c)
d = 0.9; m = (rng.random(int(SR * d) // 480 + 1) > 0.45).astype(float).repeat(480)[:int(SR * d)]
save("rip", hpf(noise(d), 700) * np.convolve(m, np.ones(200) / 200, "same") * env(d, 0.02, curve=1.5) * 1.5 + sine(sweep(120, 40, d), d) * 0.4 * env(d, 0.01, curve=2))
d = 3.0; save("rumble", lpf(noise(d), 90) * (1 + 0.4 * np.sin(2 * np.pi * 3 * t_(d))) + 0.4 * sine(48, d))
d = 2.2; save("riser", (bp(noise(d), 400, 6000) * np.linspace(0.05, 1, int(SR * d)) ** 2) * 0.7 + saw(sweep(80, 900, d), d) * 0.25 * np.linspace(0, 1, int(SR * d)))
d = 0.08; save("tick", (sine(2400, d) + 0.5 * sine(4800, d)) * env(d, 0.001, curve=9))
d = 1.2; save("ding", (sine(1175, d) + 0.5 * sine(1760, d) + 0.25 * sine(2349, d)) * env(d, 0.003, curve=4))
d = 0.1; save("pop", sine(sweep(900, 250, d), d) * env(d, 0.001, curve=8))
d = 0.35; save("paper", hpf(bp(noise(d), 1500, 9000) * (1 + 0.8 * np.sin(2 * np.pi * 32 * t_(d))), 1200) * env(d, 0.01, curve=3.5))
d = 3.0; save("jet", bp(noise(d), 200, 2200) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * t_(d))) + 0.3 * saw(110, d) * 0.3)
d = 1.1; save("horn", lpf(saw(98, d) + saw(147, d) * 0.8 + saw(99, d) * 0.7, 700) * env(d, 0.06, curve=1.4))
d = 3.0; save("wind", bp(noise(d), 150, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t_(d))))
d = 1.2; f = np.where((t_(d) // 0.3) % 2 == 0, 880, 660); save("alarm", np.sign(sine(f, d)) * 0.5 * np.where((t_(d) % 0.3) < 0.26, 1, 0))
d = 0.35; save("zap", (hpf(noise(d), 2000) * env(d, 0.001, curve=7)) + saw(sweep(3000, 200, d), d) * env(d, 0.001, curve=6) * 0.4)
d = 0.9; save("sting", lpf(saw(220, d) + saw(233, d) + saw(311, d), 1800) * env(d, 0.01, curve=3))
d = 4.0; save("waves", lpf(noise(d), 600) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.35 * t_(d) - 1.0)) ** 2)
d = 0.6; save("clink", (sine(2400, d) + 0.6 * sine(3720, d) + 0.4 * sine(5100, d)) * env(d, 0.001, curve=7))
d = 1.6; b = np.zeros(int(SR * d))
for k in range(26):
    i = int(rng.uniform(0, d - 0.1) * SR); p = sine(sweep(500 + rng.uniform(0, 600), 200, 0.06), 0.06) * env(0.06, 0.001, curve=6); b[i:i + len(p)] += p
save("bubbles", b)
d = 1.0; save("creak", lpf(saw(sweep(70, 140, d) * (1 + 0.15 * np.sin(2 * np.pi * 11 * t_(d))), d), 900) * env(d, 0.15, curve=1.2) + 0.2 * bp(noise(d), 300, 1500) * env(d, 0.1, curve=2))
d = 0.45; save("gasp", bp(noise(d), 900, 3800) * np.sin(np.linspace(0, np.pi, int(SR * d))) ** 1.5)
hb = np.zeros(int(SR * 0.9))
for st, a in ((0.0, 1.0), (0.22, 0.7)):
    i = int(st * SR); p = sine(sweep(80, 45, 0.2), 0.2) * env(0.2, 0.004, curve=6) * a; hb[i:i + len(p)] += p
save("heartbeat", hb)
d = 0.7; s_ = np.zeros(int(SR * d))
for k, f in enumerate((1568, 2093, 2637, 3136, 4186)):
    i = int(k * 0.07 * SR); p = sine(f, 0.4) * env(0.4, 0.002, curve=6); s_[i:i + len(p)] += p * 0.6
save("sparkle", s_)
d = 3.0; save("water", bp(noise(d), 500, 4500) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.7 * t_(d))))
d = 3.0; save("cabin", lpf(noise(d), 350) * 0.6 + 0.25 * sine(180, d))
d = 2.4; l = np.zeros(int(SR * d))
for k in range(9):
    i = int((0.1 + k * 0.23 + rng.uniform(-0.03, 0.03)) * SR); f0 = rng.uniform(250, 380)
    seg = bp(noise(0.16), 500, 1800) * sine(sweep(f0 * 1.3, f0, 0.16), 0.16) * env(0.16, 0.01, curve=5); l[i:i + len(seg)] += seg
save("laughs", l)
# ---- user's own sounds
U = sys.argv[1] if len(sys.argv) > 1 else ""
def conv(src, name, trim=None, peak=0.9):
    p = os.path.join(U, src)
    if not os.path.exists(p): return
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", str(SR)] + (["-t", str(trim)] if trim else []) + [os.path.join(OUT, name + ".wav")]
    subprocess.run(cmd, check=True)
conv("capcut-explosion-sound.mp3", "boom_1")
conv("slap-soundmaster13-49669815_4L20wGP.mp3", "slap")
conv("correct.mp3", "correct")
conv("applepay.mp3", "pay")
conv("discord-notification.mp3", "notif")
conv("mouse-click-sound.mp3", "click", trim=0.35)
conv("movie_1.mp3", "hit")
os.replace(os.path.join(OUT, "boom_synth.wav"), os.path.join(OUT, "boom.wav"))
# ---- music bed: A minor, 116 bpm, builds & releases with the story
def music():
    bpm = 116; beat = 60 / bpm; dur = 66.0; n = int(SR * dur); m = np.zeros(n)
    def add(x, at):
        i = int(at * SR); m[i:i + len(x)] += x[:max(0, n - i)]
    def tone(f, d, a=0.01, curve=3, wave="saw"):
        w = saw(f, d) if wave == "saw" else sine(f, d)
        return lpf(w, 2200) * env(d, a, curve=curve)
    prog = [55, 55, 43.65, 49]            # A1 A1 F1 G1
    ar = [220, 261.63, 329.63, 392, 329.63, 261.63]
    t = 0.0; bar = 0
    while t < dur - 1:
        sec = "intro" if t < 10 else "main" if t < 22.3 else "dark" if t < 36 else "build" if t < 49.3 else "bright"
        root = prog[bar % 4]
        if sec == "bright": root *= 1.0
        # bass
        for k in range(8):
            if sec in ("intro", "main", "build", "bright") or k % 2 == 0:
                add(tone(root, beat / 2, 0.005, 5, "sine") * (0.55 if sec != "dark" else 0.4), t + k * beat / 2)
        # pluck arp
        if sec in ("main", "build", "bright", "intro"):
            for k in range(8):
                f = ar[(k + bar) % 6] * (2 if sec == "bright" else 1) * (1.189 if (sec == "bright" and bar % 4 == 0) else 1)
                add(tone(f, beat * 0.5, 0.003, 6, "sine") * (0.22 if sec == "intro" else 0.3), t + k * beat / 2)
        # kick + hat
        if sec in ("main", "build", "bright"):
            for k in range(4):
                add(sine(sweep(120, 45, 0.2), 0.2) * env(0.2, 0.002, curve=7) * 0.7, t + k * beat)
            for k in range(8):
                add(hpf(noise(0.05), 6000) * env(0.05, 0.001, curve=9) * 0.15, t + k * beat / 2 + beat / 4)
        # pad
        pad = tone(root * 4, beat * 4, 0.4, 0.8) * 0.12 + tone(root * 4 * 1.5, beat * 4, 0.4, 0.8) * 0.08
        add(pad * (1.4 if sec in ("dark", "build") else 1.0), t)
        if sec == "dark":
            add(sine(sweep(80, 45, 0.2), 0.2) * env(0.2, 0.004, curve=6) * 0.5, t)
        t += beat * 4; bar += 1
    m = m / np.abs(m).max()
    # master automation: low intro, tension pull at the crashes, swell into the resolution
    g = np.interp(np.arange(n) / SR, [0, 3, 10, 22, 22.6, 36, 44, 49.2, 49.4, 56, 62, 66], [0.5, 0.7, 0.9, 1.0, 0.55, 0.65, 0.85, 1.0, 0.8, 0.9, 0.9, 0.0])
    m *= g
    with wave.open(os.path.join(os.path.dirname(OUT), "music", "bed.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m / np.abs(m).max() * 0.9 * 32767).astype("<i2").tobytes())
music()
import json
json.dump({"boom": {"gain": 0}, "rumble": {"gain": -4}, "wind": {"gain": -8}, "jet": {"gain": -8}, "waves": {"gain": -8},
           "water": {"gain": -6}, "cabin": {"gain": -12}, "laughs": {"gain": -8}, "alarm": {"gain": -8}, "bubbles": {"gain": -4},
           "riser": {"gain": -3}, "heartbeat": {"gain": -1}, "pop": {"gain": -4}, "tick": {"gain": -4}, "paper": {"gain": -3},
           "notif": {"gain": -4}, "pay": {"gain": -4}, "correct": {"gain": -3}, "click": {"gain": -3}, "swoosh": {"gain": -4},
           "sparkle": {"gain": -5}, "slap": {"gain": -2}}, open(os.path.join(OUT, "pack.json"), "w"), indent=1)
print("ok", sorted(f for f in os.listdir(OUT)))
