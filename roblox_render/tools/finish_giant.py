"""Assemble the giant video: concat rendered parts + mix + Titan One white captions.
python tools/finish_giant.py [--font-dir DIR] [--size 112]"""
import argparse, glob, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser(); ap.add_argument("--slug", default="giant"); ap.add_argument("--font-dir", default=os.path.join(ROOT, "fonts"))
ap.add_argument("--size", type=int, default=112); ap.add_argument("--music-db", default="-17"); ap.add_argument("--sfx-db", default="-11")
o = ap.parse_args()
vdir = os.path.join(ROOT, "videos", o.slug); adir = os.path.join(vdir, "audio"); os.makedirs(os.path.join(vdir, "out"), exist_ok=True)
subprocess.run([sys.executable, os.path.join(HERE, "mix.py"), "--video", o.slug, "--music-db", o.music_db, "--sfx-db", o.sfx_db], check=True)
words = json.load(open(os.path.join(adir, "words.json"), encoding="utf-8"))
LAG = 0.04
def ts(t):
    cs = int(round(max(t, 0) * 100)); return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"
head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Titan One,{o.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,9,4,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for i, w in enumerate(words):
    txt = re.sub(r"[^\w'$%,.!?:]", "", w["word"]).strip(",.!?:").upper()
    if not txt: continue
    s = 0.0 if i == 0 else w["start"] + LAG
    e = (words[i + 1]["start"] + LAG) if i + 1 < len(words) else w["end"] + 0.4
    lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Word,,0,0,0,,{{\\pos(540,1560)\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)}}{txt}")
open(os.path.join(vdir, "captions.ass"), "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
parts = sorted(glob.glob(os.path.join(ROOT, "out", f"{o.slug}_part_*.mp4")), key=lambda p: int(re.findall(r"_part_(\d+)_", p)[0]))
tot = sum(int(re.findall(r"_part_\d+_(\d+)", p)[0]) for p in parts); print(len(parts), "parts,", tot, "frames")
lst = os.path.join(vdir, "parts.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
raw = os.path.join(vdir, "out", "video_raw.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw], check=True)
fd = o.font_dir
sub = f"ass={os.path.join(vdir, 'captions.ass')}:fontsdir={fd}"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(adir, "mix.m4a")], capture_output=True, text=True).stdout)
enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-i", os.path.join(adir, "mix.m4a"), "-vf", f"scale=1080:1920:flags=lanczos,{sub}"] + enc + [os.path.join(vdir, "out", "final.mp4")], check=True)
print("done", os.path.join(vdir, "out", "final.mp4"), dur)
