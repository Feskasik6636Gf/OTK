"""Original upbeat bed (plucks + bass + soft beat), 112 BPM, 32 s loop -> videos/<slug>/audio/music.wav
python tools/make_music.py <slug>"""
import os, sys, wave
import numpy as np
SR = 48000
slug = sys.argv[1]
BPM = 112
beat = 60 / BPM
bars = 16
n = int(SR * beat * 4 * bars)
mix = np.zeros(n)
rng = np.random.default_rng(3)


def add(t, x, g=1.0):
    a = int(t * SR)
    if a >= n:
        return
    b = min(n, a + len(x))
    mix[a:b] += x[:b - a] * g


def pluck(f, d=0.5):
    t = np.arange(int(SR * d)) / SR
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t))
    return x * np.exp(-t * 7.0) * np.minimum(1, t * 300)


def bass(f, d=0.45):
    t = np.arange(int(SR * d)) / SR
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 4.5) * np.minimum(1, t * 200)


def kick():
    t = np.arange(int(SR * 0.22)) / SR
    f = 120 * np.exp(-t * 22) + 42
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def hat():
    t = np.arange(int(SR * 0.05)) / SR
    x = rng.standard_normal(len(t))
    x = np.diff(x, prepend=0)
    return x * np.exp(-t * 90)


mid = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [(48, [60, 64, 67, 72]), (45, [57, 60, 64, 69]), (41, [60, 65, 69, 72]), (43, [59, 62, 67, 71])]
for bar in range(bars):
    root, notes = chords[(bar // 2) % 4]
    t0 = bar * 4 * beat
    for q in range(8):
        tt = t0 + q * beat / 2
        add(tt, bass(mid(root), 0.4), 0.55 if q % 2 == 0 else 0.0)
        m = notes[(q * 3 + bar) % 4] + (12 if q % 4 == 3 else 0)
        add(tt + (beat / 6 if q % 2 else 0), pluck(mid(m), 0.45), 0.28)
        add(tt, hat(), 0.10 if q % 2 else 0.05)
    for q in range(4):
        if q in (0, 2):
            add(t0 + q * beat, kick(), 0.5)
mix /= np.abs(mix).max()
mix *= 0.8
st = np.stack([mix, np.roll(mix, int(0.012 * SR))], 1)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos", slug, "audio", "music.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
print("music ->", out, f"{n / SR:.1f}s")
