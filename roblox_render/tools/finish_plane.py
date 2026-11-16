"""Finish the plane video locally: concat rendered parts + mix (voice, sfx, music) + captions.
python tools/finish_plane.py [--no-captions]  -> videos/plane/out/final.mp4"""
import glob, json, os, re, subprocess, sys, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(R, "videos", "plane"); A = os.path.join(V, "audio"); O = os.path.join(V, "out"); os.makedirs(O, exist_ok=True)
FONTS = os.path.join(R, "assets", "fonts")
parts = sorted(glob.glob(os.path.join(R, "out", "plane_part_*.mp4")))
print(len(parts), "parts")
shutil.copy(os.path.join(R, "music", "bed.wav"), os.path.join(A, "music.wav"))
subprocess.run([sys.executable, os.path.join(R, "tools", "mix.py"), "--video", "plane", "--music-db", "-17", "--sfx-db", "-11", "--duck-db", "-6"], check=True)
lst = os.path.join(O, "parts.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
words = json.load(open(os.path.join(A, "words.json"), encoding="utf-8"))
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
Style: Word,Rubik Black Static,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,8,3,5,20,20,20,1
Style: Lat,Titan One,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,8,3,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
LAG = 0.03
lines = []
for i, w in enumerate(words):
    txt = re.sub(r"[^\w!?]", "", w["word"]).upper()
    if not txt: continue
    s = 0.0 if i == 0 else w["start"] + LAG
    nxt = words[i + 1]["start"] + LAG if i + 1 < len(words) else w["end"] + 0.5
    e = min(nxt, w["end"] + 0.55) if i + 1 < len(words) else nxt
    if e <= s: e = s + 0.2
    style = "Word" if re.search("[А-ЯЁ]", txt) else "Lat"
    pop = r"{\pos(540,1560)\fscx82\fscy82\t(0,90,\fscx108\fscy108)\t(90,170,\fscx100\fscy100)}"
    lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},{style},,0,0,0,,{pop}{txt}")
open(os.path.join(O, "captions.ass"), "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
mix = os.path.join(A, "mix.m4a")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mix], capture_output=True, text=True).stdout)
base = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", mix]
enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart"]
subprocess.run(base + ["-vf", "scale=1080:1920:flags=lanczos"] + enc + [os.path.join(O, "final_nocaptions.mp4")], check=True)
if "--no-captions" not in sys.argv:
    vf = f"scale=1080:1920:flags=lanczos,ass={os.path.join(O, 'captions.ass')}:fontsdir={FONTS}"
    subprocess.run(base + ["-vf", vf] + enc + [os.path.join(O, "final.mp4")], check=True)
print("done", dur)
