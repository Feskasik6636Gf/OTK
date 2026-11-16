"""Shared helpers (camera, keyframe moves, pop-up text) for the vo3 video."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, os, random
from mathutils import Vector
FONT = os.environ.get("TITAN_FONT", "/root/.fonts/TitanOne-Regular.ttf")


def rad(a):
    return math.radians(a)


# ------------------------------------------------------------------ cast


def hide(m, t, vis):
    sets.set_coll_visible(m["coll"], t, vis)


def move(ob, t, loc=None, rot=None, scale=None, interp="BEZIER", ease=None):
    f = F(t)
    if loc is not None:
        ob.location = loc
        ob.keyframe_insert("location", frame=f)
        set_interp(ob, "location", f, interp, ease)
    if rot is not None:
        ob.rotation_euler = [rad(a) for a in rot]
        ob.keyframe_insert("rotation_euler", frame=f)
        set_interp(ob, "rotation_euler", f, interp, ease)
    if scale is not None:
        ob.scale = scale if isinstance(scale, tuple) else (scale,) * 3
        ob.keyframe_insert("scale", frame=f)
        set_interp(ob, "scale", f, interp, ease)


def bounce(ob, t0, t1, amp=0.25, rate=5.0):
    """Squash-and-stretch pulse on scale so monsters feel alive."""
    b = Vector(ob.scale)
    t = t0
    k = 0
    while t <= t1:
        s = 1 + amp * (1 if k % 2 == 0 else -0.6)
        ob.scale = (b.x * (2 - s) ** 0.5, b.y * (2 - s) ** 0.5, b.z * s)
        ob.keyframe_insert("scale", frame=F(t))
        t += 1.0 / rate
        k += 1


def swing(piv, t0, t1, axis=0, amp=30, rate=4.0, base=0.0):
    t = t0
    k = 0
    while t <= t1:
        v = [0, 0, 0]
        v[axis] = rad(base + amp * (1 if k % 2 == 0 else -1))
        piv.rotation_euler = v
        piv.keyframe_insert("rotation_euler", frame=F(t))
        t += 0.5 / rate
        k += 1


def stars_pop(prefix, loc, t, n=8, r=2.2, seed=2, size=0.22, color="#ffe066"):
    rnd = random.Random(seed)
    M = mat("starpop_" + color, hexc(color), 0.3, emit=hexc(color), estr=6.0)
    for i in range(n):
        a = i / n * math.tau
        ob = sphere(f"{prefix}{i}", size, tuple(loc), M, seg=8)
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(t - 0.02))
        ob.keyframe_insert("location", frame=F(t - 0.02))
        ob.scale = (1,) * 3
        ob.keyframe_insert("scale", frame=F(t + 0.05))
        ob.location = (loc[0] + math.cos(a) * r * rnd.uniform(0.7, 1.2), loc[1] - rnd.uniform(0.2, 0.8), loc[2] + math.sin(a) * r)
        ob.keyframe_insert("location", frame=F(t + 0.35))
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(t + 0.45))


def pop_text(name, body, loc, t, dur=0.8, size=1.6, color="#ffe066", rot=(90, 0, 0)):
    M = mat("txt_" + color, hexc(color), 0.4, emit=hexc(color), estr=1.0)
    ob = text(name, body, loc, size, M, rot=rot, extrude=0.12, font=FONT)
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.02))
    for dt, k in ((0.07, 1.25), (0.15, 0.95), (0.22, 1.0)):
        ob.scale = (k,) * 3
        ob.keyframe_insert("scale", frame=F(t + dt))
    ob.keyframe_insert("scale", frame=F(t + dur))
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur + 0.12))
    return ob


def C(t0, t1, tgt, d0, d1, yaw, pitch=5, lens=28, yaw1=None, pitch1=None, lens1=None, drop=0.6, hh=1.0, fstop=6.0, roll=0.0):
    cam = Cam()
    cam.push(t0, t1, (tgt[0], tgt[1], tgt[2] - drop), d0, d1, yaw=yaw, pitch=pitch, lens=lens, yaw1=yaw1, pitch1=pitch1,
             lens1=lens1, fstop=fstop, roll=roll)
    cam.handheld(hh)
    return cam


