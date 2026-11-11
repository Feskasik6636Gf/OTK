# Roblox-style story render (shoe swap)

Engine (rbx/, tools/, assets/) + videos/vo/shots.py (82 shots).
.github/workflows/render-roblox.yml renders the shots in 20 parallel jobs (Blender 5.2 EEVEE on CPU, 720x1280, 12 samples)
and pushes each part as an mp4 to roblox_render/out/. Voice, music and captions are mixed afterwards.
