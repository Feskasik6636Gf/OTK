"""Builds sfx/*.wav: the user's meme sounds (trimmed) + synthesized whoosh/pop/rumble/etc.
usage: python tools/build_sfx.py <dir with the user's mp3 files>"""
import json, os, subprocess, sys
import numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(ROOT, 'sfx'); os.makedirs(OUT, exist_ok=True)
SR = 44100
rng = np.random.default_rng(7)


def save(name, x):
    x = np.asarray(x, dtype=np.float64)
    x = x / max(1e-9, np.abs(x).max()) * 0.9
    st = np.stack([x, x], 1)
    p = os.path.join(OUT, name + '.wav')
    pr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', p],
                          stdin=subprocess.PIPE)
    pr.communicate(st.astype('<f4').tobytes())


def t(d): return np.arange(int(d * SR)) / SR


def env(x, a=0.005, r=0.1):
    x = x.copy(); n = len(x); na = int(a * SR); nr = int(r * SR)
    x[:na] *= np.linspace(0, 1, na); x[-nr:] *= np.linspace(1, 0, nr)
    return x


def lp(x, k):
    c = np.cumsum(np.insert(x, 0, 0))
    y = (c[k:] - c[:-k]) / k
    return np.pad(y, (0, len(x) - len(y)))


def noise(d): return rng.standard_normal(int(d * SR))


def sweep(d, f0, f1):
    tt = t(d); f = f0 * (f1 / f0) ** (tt / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def from_zip(src, name, start=0.0, dur=None):
    p = os.path.join(sys.argv[1], src)
    cmd = ['ffmpeg', '-y', '-v', 'error', '-ss', str(start)] + (['-t', str(dur)] if dur else []) + \
          ['-i', p, '-ac', '2', '-ar', str(SR), os.path.join(OUT, name + '.wav')]
    subprocess.run(cmd, check=True)


# the user's sounds
from_zip('discord-notification.mp3', 'ding')
from_zip('slap-soundmaster13-49669815_4L20wGP.mp3', 'slap')
from_zip('faaah.mp3', 'faaah')
from_zip('capcut-explosion-sound.mp3', 'boom', 0, 2.2)
from_zip('applepay.mp3', 'sparkle')
from_zip('duck-toy-sound.mp3', 'snort')
from_zip('mac-quack.mp3', 'aww')
from_zip('mouse-click-sound.mp3', 'click', 0, 0.25)
from_zip('rizz-sound-effect.mp3', 'rimshot', 0, 1.3)
from_zip('correct.mp3', 'correct')
from_zip('dry-fart.mp3', 'gasp')
# synthesized
d = 0.55; save('whoosh', lp(noise(d), 25) * np.sin(np.pi * t(d) / d) ** 2)
d = 0.12; save('pop', env(sweep(d, 900, 250) * np.exp(-t(d) * 25), 0.001, 0.03))
d = 2.0; save('rumble', env(lp(noise(d), 120) * (1 + 0.5 * np.sin(2 * np.pi * 9 * t(d))) + sweep(d, 45, 30) * 0.8, 0.1, 0.5))
d = 0.45; save('stomp', env(sweep(d, 110, 40) * np.exp(-t(d) * 8) + lp(noise(d), 30) * np.exp(-t(d) * 18), 0.002, 0.1))
d = 0.25; save('place', env(sweep(d, 500, 180) * np.exp(-t(d) * 22) + 0.3 * lp(noise(d), 4) * np.exp(-t(d) * 40), 0.001, 0.05))
d = 1.2; save('rise', env(sweep(d, 220, 1400) * np.linspace(0.2, 1, int(d * SR)), 0.05, 0.1))
d = 1.3; save('confetti', env(noise(d) * np.exp(-t(d) * 3) * (rng.random(int(d * SR)) > 0.5), 0.002, 0.2))
d = 1.4; save('footsteps', env(lp(noise(d), 40) * np.exp(-((t(d) % 0.35) * 40)), 0.01, 0.1))
d = 1.6; save('crowd', env(lp(noise(d), 12) * (1 + 0.6 * np.sin(2 * np.pi * 7 * t(d))), 0.1, 0.3))
d = 1.4; save('chat', env(lp(noise(d), 10) * (1 + 0.8 * np.sin(2 * np.pi * 11 * t(d))), 0.1, 0.3))
d = 1.6; save('cheer', env(lp(noise(d), 8) * (1 + 0.4 * np.sin(2 * np.pi * 5 * t(d))), 0.15, 0.4))
d = 2.0; save('crickets', env(np.sin(2 * np.pi * 4300 * t(d)) * (np.sin(2 * np.pi * 14 * t(d)) > 0.3) * 0.5, 0.05, 0.2))
d = 1.2; save('zombie', env(sweep(d, 140, 60) * (1 + 0.3 * np.sin(2 * np.pi * 30 * t(d))) + lp(noise(d), 20) * 0.5, 0.05, 0.3))
json.dump({'ding': {'gain': 3}, 'sparkle': {'gain': 3}, 'rumble': {'gain': -2}, 'whoosh': {'gain': 1}},
          open(os.path.join(OUT, 'pack.json'), 'w'))
print('sfx:', sorted(f[:-4] for f in os.listdir(OUT) if f.endswith('.wav')))
