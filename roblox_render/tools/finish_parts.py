"""Assemble rendered part mp4s (out/<slug>_part_*.mp4), mix audio, burn Titan One captions.
python tools/finish_parts.py <slug>"""
import glob, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STUDIO = os.path.dirname(HERE)
slug = sys.argv[1]
vdir = os.path.join(STUDIO, "videos", slug); adir = os.path.join(vdir, "audio"); odir = os.path.join(vdir, "out")
os.makedirs(odir, exist_ok=True)
parts = []
for f in glob.glob(os.path.join(STUDIO, "out", f"{slug}_part_*.mp4")):
    m = re.search(r"_part_(\d+)_(\d+)\.mp4$", f)
    parts.append((int(m.group(1)), int(m.group(2)), f))
parts.sort()
tot = sum(p[1] for p in parts)
exp = 0
for a, n, f in parts:
    if a != exp: print(f"WARNING: gap/overlap at frame {exp} (part starts {a})")
    exp = a + n
print(f"{len(parts)} parts, {tot} frames ({tot/30:.1f}s)")
lst = os.path.join(vdir, "parts.txt")
open(lst, "w").write("".join(f"file '{p[2]}'\n" for p in parts))
silent = os.path.join(odir, "video_silent.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
# music bed
shutil.copyfile(os.path.join(STUDIO, "music", "dark_drone.wav"), os.path.join(adir, "music.wav"))
subprocess.run([sys.executable, os.path.join(HERE, "mix.py"), "--video", slug, "--music-db", "-17", "--sfx-db", "-11"], check=True)
# captions: Titan One, white, smaller than before, quick pop-in per word
words = json.load(open(os.path.join(adir, "words.json"), encoding="utf-8"))
LAG = 1.3 / 30
def ts(t):
    cs = int(round(max(t, 0) * 100)); return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Titan One,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,8,3,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for i, w in enumerate(words):
    txt = re.sub(r"[^\w'$%,.?!]", "", w["word"]).strip(",.").upper()
    if not txt: continue
    s = 0.0 if i == 0 else w["start"] + LAG
    e = (words[i + 1]["start"] + LAG) if i + 1 < len(words) else w["end"] + 0.4
    lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Word,,0,0,0,,{{\\pos(540,1600)\\fscx70\\fscy70\\t(0,110,\\fscx100\\fscy100)}}{txt}")
open(os.path.join(vdir, "captions.ass"), "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
fonts = os.path.join(STUDIO, "assets", "fonts")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(adir, "mix.m4a")], capture_output=True, text=True).stdout)
os.chdir(vdir)
enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart"]
base = ["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", os.path.join("audio", "mix.m4a")]
vf = f"scale=1080:1920:flags=lanczos,ass=captions.ass:fontsdir={fonts}"
subprocess.run(base + ["-vf", vf] + enc + [os.path.join("out", "final.mp4")], check=True)
subprocess.run(base + ["-vf", "scale=1080:1920:flags=lanczos"] + enc + [os.path.join("out", "final_nocaptions.mp4")], check=True)
print("done", os.path.join(vdir, "out", "final.mp4"), f"{dur:.1f}s")
