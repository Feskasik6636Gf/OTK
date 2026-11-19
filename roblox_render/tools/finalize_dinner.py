"""Final assembly for the dinner video: concat rendered parts + mix (voice, sfx, music) + Titan One captions.
usage: python tools/finalize_dinner.py [slug]
needs roblox_render/out/<slug>_part_*.mp4, videos/<slug>/audio/{voice.wav,words.json,cues.json}, music/bed.wav (optional)"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
slug = sys.argv[1] if len(sys.argv) > 1 else 'dinner'
vdir = os.path.join(ROOT, 'videos', slug)
adir = os.path.join(vdir, 'audio')
odir = os.path.join(vdir, 'out'); os.makedirs(odir, exist_ok=True)

# 1. audio mix
music = os.path.join(ROOT, 'music', 'bed.wav')
cmd = [sys.executable, os.path.join(HERE, 'mix.py'), '--video', slug, '--music-db', '-17', '--sfx-db', '-10']
if os.path.exists(music):
    cmd += ['--music', music]
subprocess.run(cmd, check=True)

# 2. captions: one word at a time, white Titan One, pop-in
words = json.load(open(os.path.join(adir, 'words.json'), encoding='utf-8'))
LAG = 1.3 / 30


def ts(t):
    cs = int(round(max(t, 0) * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,Titan One,108,&H00FFFFFF,&H00FFFFFF,&H00101018,&H80000000,0,0,0,0,100,100,1,0,1,8,4,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = []
for i, w in enumerate(words):
    txt = re.sub(r"[^\w'$%,.!?]", "", w['word']).strip(',.!?"').upper()
    if not txt:
        continue
    s = 0.0 if i == 0 else w['start'] + LAG
    e = (words[i + 1]['start'] + LAG) if i + 1 < len(words) else w['end'] + 0.5
    lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Word,,0,0,0,,{{\\pos(540,1480)\\fscx70\\fscy70\\t(0,110,\\fscx104\\fscy104)\\t(110,190,\\fscx100\\fscy100)}}{txt}")
ass = os.path.join(vdir, 'captions.ass')
open(ass, 'w', encoding='utf-8').write(head + '\n'.join(lines) + '\n')

# 3. concat parts (sorted by first frame number)
parts = sorted(glob.glob(os.path.join(ROOT, 'out', f'{slug}_part_*.mp4')), key=lambda p: int(re.search(r'_part_(\d+)_', p).group(1)))
if not parts:
    sys.exit('no rendered parts found')
lst = os.path.join(vdir, 'parts.txt')
open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
silent = os.path.join(vdir, 'silent.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', silent], check=True)

# 4. mux + captions
mix = os.path.join(adir, 'mix.m4a')
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mix],
                           capture_output=True, text=True).stdout)
fonts = os.path.join(ROOT, 'fonts')
vf = f"scale=1080:1920:flags=lanczos,ass=captions.ass:fontsdir={fonts}"
os.chdir(vdir)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', mix, '-vf', vf, '-c:v', 'libx264', '-preset', 'slow',
                '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-t', f'{dur:.3f}', '-movflags', '+faststart',
                os.path.join('out', 'final.mp4')], check=True)
print('done', os.path.join(vdir, 'out', 'final.mp4'), f'{dur:.1f}s')
