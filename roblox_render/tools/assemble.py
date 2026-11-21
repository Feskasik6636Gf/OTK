"""Final edit for a video whose frames were rendered in parts (CI).
python tools/assemble.py <slug> [--parts out/<slug>_part_*.mp4]

1. joins the rendered parts (720x1280) in frame order, checks nothing is missing
2. mixes voice + sfx cues + music (tools/mix.py)
3. dynamic edit in one ffmpeg pass: punch-in zoom on every cut and on every impact sound, camera shake and
   white flashes on the big hits, slight colour pop, upscale to 1080x1920
4. burns one-word captions in Titan One (white, black outline, pop-in), mutes nothing
Writes videos/<slug>/out/final.mp4 (+ final_phone.mp4 for sending to a phone)."""
import argparse, glob, json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("--no-fx", action="store_true")
ap.add_argument("--cap-size", type=int, default=112)
ap.add_argument("--cap-y", type=int, default=1560)
o = ap.parse_args()
slug = o.slug
vdir = os.path.join(ROOT, "videos", slug)
adir = os.path.join(vdir, "audio")
odir = os.path.join(vdir, "out")
os.makedirs(odir, exist_ok=True)
FPS = 30


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd)[:300], flush=True)
    subprocess.run(cmd, check=True, **kw)


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------------------------------------------------------- 1. join parts
parts = sorted(glob.glob(os.path.join(ROOT, "out", f"{slug}_part_*.mp4")))
if not parts:
    sys.exit("no rendered parts found in out/")
info = []
for p in parts:
    m = re.search(r"_part_(\d+)_(\d+)\.mp4$", p)
    info.append((int(m.group(1)), int(m.group(2)), p))
info.sort()
nxt = 1
missing = []
for first, n, p in info:
    if first > nxt:
        missing.append((nxt, first - 1))
    nxt = max(nxt, first + n)
print(f"parts: {len(info)}, frames 1..{nxt - 1}, missing ranges: {missing}")
if missing:
    sys.exit(f"missing frames {missing}: re-run the render for those shots (workflow input parts), then assemble again")
lst = os.path.join(vdir, "parts.txt")
with open(lst, "w") as f:
    for first, n, p in info:
        f.write(f"file '{p}'\n")
joined = os.path.join(vdir, "joined.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
nframes = int(round(dur(joined) * FPS))
print("joined frames:", nframes)

# ---------------------------------------------------------------- 2. audio
run([sys.executable, os.path.join(HERE, "mix.py"), "--video", slug])
mix = os.path.join(adir, "mix.m4a")
total = dur(mix)

# ---------------------------------------------------------------- 3. captions (ASS, Titan One, white)
words = json.load(open(os.path.join(adir, "words.json"), encoding="utf-8"))
LAG = 1.3 / FPS


def ts(t):
    cs = int(round(max(t, 0) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Titan One,{o.cap_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,1,0,1,8,4,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for i, w in enumerate(words):
    txt = re.sub(r"[^\w'$%,.!?-]", "", w["word"]).strip(",.!?-").upper()
    if not txt:
        continue
    s = 0.0 if i == 0 else w["start"] + LAG
    e = (words[i + 1]["start"] + LAG) if i + 1 < len(words) else w["end"] + 0.4
    pop = "\\fscx72\\fscy72\\t(0,70,\\fscx112\\fscy112)\\t(70,150,\\fscx100\\fscy100)"
    lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Word,,0,0,0,,{{\\pos(540,{o.cap_y}){pop}}}{txt}")
ass = os.path.join(vdir, "captions.ass")
open(ass, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")

# ---------------------------------------------------------------- 4. dynamic edit
HITS = {  # sound -> (zoom punch, shake, flash)
    "boom": (0.075, 1.0, 0.10), "blast": (0.09, 1.3, 0.14), "sting": (0.05, 0.5, 0.0), "slap": (0.05, 0.8, 0.0),
    "thud": (0.04, 0.6, 0.0), "stomp": (0.035, 0.5, 0.0), "fart": (0.04, 0.4, 0.0), "window": (0.04, 0.9, 0.0),
    "splat": (0.035, 0.4, 0.0), "confetti": (0.03, 0.0, 0.05), "chaching": (0.03, 0.0, 0.03), "ding": (0.025, 0.0, 0.0),
    "correct": (0.025, 0.0, 0.04), "pop": (0.025, 0.0, 0.0), "rimshot": (0.025, 0.0, 0.0), "poof": (0.04, 0.0, 0.05),
}
cues = json.load(open(os.path.join(adir, "cues.json")))
shots = json.load(open(os.path.join(adir, "shots.json"))) if os.path.exists(os.path.join(adir, "shots.json")) else []
zterms, sterms, fterms = [], [], []
last = {}
for s in shots:
    t = s["t0"]
    if t > 0.1:
        zterms.append(f"0.032*gte(t,{t:.3f})*exp(-9*max(t-{t:.3f},0))")
for c in cues:
    h = HITS.get(c["name"])
    if not h:
        continue
    t = c["t"]
    if last.get(c["name"], -9) > t - 0.25:
        continue
    last[c["name"]] = t
    z, sh, fl = h
    zterms.append(f"{z * c.get('vol', 1.0):.3f}*gte(t,{t:.3f})*exp(-8*max(t-{t:.3f},0))")
    if sh:
        sterms.append(f"{sh * c.get('vol', 1.0):.3f}*gte(t,{t:.3f})*exp(-6*max(t-{t:.3f},0))")
    if fl:
        fterms.append(f"{fl:.3f}*gte(t,{t:.3f})*exp(-14*max(t-{t:.3f},0))")
Z = "1+" + ("+".join(zterms) if zterms else "0")
SH = "+".join(sterms) if sterms else "0"
FL = "+".join(fterms) if fterms else "0"
fx = (f"scale=w='trunc(1080*({Z})/2)*2':h='trunc(1920*({Z})/2)*2':eval=frame:flags=bicubic,"
      f"crop=1080:1920:x='(iw-1080)/2+({SH})*16*sin(t*53)':y='(ih-1920)/2+({SH})*14*cos(t*61)',"
      f"eq=brightness='{FL}':saturation=1.10:contrast=1.04:eval=frame")
base = "scale=1080:1920:flags=lanczos"
vf = (base if o.no_fx else fx) + f",ass={ass}:fontsdir={os.path.join(ROOT, 'assets', 'fonts')}"
script = os.path.join(vdir, "fx_filter.txt")
open(script, "w").write(vf)
final = os.path.join(odir, "final.mp4")
run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-i", mix, "-filter_script:v", script,
     "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
     "-t", f"{total:.3f}", "-movflags", "+faststart", final])
vbr = max(900, int(24 * 8 * 1024 / total) - 160)
run(["ffmpeg", "-v", "error", "-y", "-i", final, "-vf", "scale=720:1280", "-c:v", "libx264", "-preset", "slow",
     "-b:v", f"{vbr}k", "-maxrate", f"{int(vbr * 1.2)}k", "-bufsize", f"{vbr * 2}k", "-c:a", "aac", "-b:a", "128k",
     "-movflags", "+faststart", os.path.join(odir, "final_phone.mp4")])
print("done:", final, f"{total:.1f}s, joined {nframes} frames, missing {missing}")
