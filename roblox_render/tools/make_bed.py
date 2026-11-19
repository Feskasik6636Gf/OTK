"""Synthesizes a light upbeat background bed (music/bed.wav, 90 s) because the licensed track could not be downloaded."""
import os, subprocess
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SR = 44100
BPM = 124
beat = 60 / BPM
dur = 90
n = int(dur * SR)
out = np.zeros(n)
rng = np.random.default_rng(3)


def add(t, x, g=1.0):
    a = int(t * SR)
    if a >= n: return
    b = min(n, a + len(x)); out[a:b] += x[:b - a] * g


def tone(f, d, kind='pluck'):
    t = np.arange(int(d * SR)) / SR
    w = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t)
    return w * np.exp(-t * (6 if kind == 'pluck' else 3))


def kick():
    t = np.arange(int(0.25 * SR)) / SR
    f = 120 * np.exp(-t * 18) + 40
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def hat():
    t = np.arange(int(0.05 * SR)) / SR
    return rng.standard_normal(len(t)) * np.exp(-t * 90) * 0.25


prog = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66), (164.81, 207.65, 246.94)]
bar = beat * 4
for b in range(int(dur / bar) + 1):
    ch = prog[b % 4]
    for k in range(16):
        add(b * bar + k * beat / 4, tone(ch[k % 3] * 2, 0.3), 0.18)
    add(b * bar, tone(ch[0] / 2, bar * 0.95, 'pad'), 0.35)
    for q in range(4):
        add(b * bar + q * beat, kick(), 0.5)
        add(b * bar + q * beat + beat / 2, hat(), 0.6)
out /= np.abs(out).max() / 0.8
st = np.stack([out, out], 1).astype('<f4')
os.makedirs(os.path.join(ROOT, 'music'), exist_ok=True)
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                      os.path.join(ROOT, 'music', 'bed.wav')], stdin=subprocess.PIPE)
p.communicate(st.tobytes())
