"""sky: "My grandpa's snoring is the only thing keeping the sky from falling." Shots keyed to script word indices.
Original story, original characters. Voice supplied by the user."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector, Euler
from rbx.sets import wood, planks, checker_mat

V = Video(__file__)
story.bind(V)

HOUSE = (0.0, -48.0, 0.0)          # grandpa's blue house, front faces -Y
ROOM_BACK = 10.0                   # bedroom back wall y
BED_TOP = 2.2


# ================================================================== materials
def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def emitm(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


PENDING = []


# ================================================================== camera helpers
def bump(cam, t, amp=0.5, n=6):
    """Impact shake: kicks location + rotation of the camera for n frames after t."""
    sc = bpy.context.scene
    ob = cam.ob
    for k in range(n):
        f = F(t) + k
        sc.frame_set(f)
        loc = Vector(ob.matrix_world.translation)
        rot = ob.rotation_euler.copy()
        s = amp * (1 - k / n) * (1 if k % 2 == 0 else -1)
        ob.location = loc + Vector((s * 0.5, s * 0.2, s * 0.6))
        ob.keyframe_insert("location", frame=f)
        ob.rotation_euler = (rot[0] + s * 0.025, rot[1] + s * 0.04, rot[2] + s * 0.02)
        ob.keyframe_insert("rotation_euler", frame=f)
    return cam


def mv(kind, t0, t1, tgt, d=7.0, yaw=0, pitch=6, lens=28, hh=1.0, fstop=4.0, roll=0.0):
    """One camera move. kind: in, out, orb, orbr, rise, fall, dutch, slide, still(drift only)."""
    cam = Cam()
    if kind == "in":
        cam.push(t0, t1, tgt, d * 1.5, d * 0.75, yaw=yaw, pitch=pitch, lens=lens, fstop=fstop)
    elif kind == "out":
        cam.push(t0, t1, tgt, d * 0.7, d * 1.5, yaw=yaw, pitch=pitch, lens=lens, fstop=fstop)
    elif kind == "orb":
        cam.orbit(t0, t1, tgt, d, yaw - 28, yaw + 28, pitch=pitch, lens=lens, fstop=fstop)
    elif kind == "orbr":
        cam.orbit(t0, t1, tgt, d, yaw + 28, yaw - 28, pitch=pitch, lens=lens, fstop=fstop)
    elif kind == "rise":
        cam.push(t0, t1, tgt, d * 1.3, d * 0.9, yaw=yaw, pitch=pitch - 8, pitch1=pitch + 26, lens=lens, fstop=fstop)
    elif kind == "fall":
        cam.push(t0, t1, tgt, d * 1.2, d * 0.9, yaw=yaw, pitch=pitch + 26, pitch1=pitch - 6, lens=lens, fstop=fstop)
    elif kind == "dutch":
        cam.push(t0, t1, tgt, d * 1.4, d * 0.8, yaw=yaw, pitch=pitch, yaw1=yaw + 14, lens=lens, fstop=fstop,
                 roll=roll or 9)
    elif kind == "slide":
        cam.push(t0, t1, tgt, d, d * 0.9, yaw=yaw - 24, yaw1=yaw + 24, pitch=pitch, lens=lens, fstop=fstop)
    else:
        cam.push(t0, t1, tgt, d, d * 0.93, yaw=yaw, pitch=pitch, lens=lens, fstop=fstop)
    cam._hh = hh
    return cam


def fin(cam, hh=1.0):
    cam.handheld(hh)
    sc = bpy.context.scene
    for fit, body, size, t, loc, rx in PENDING:
        sc.frame_set(F(t) + 3)
        cl = Vector(cam.ob.matrix_world.translation)
        d = max(0.5, (cl - Vector(loc)).length)
        if rx == 90:
            q = cam.ob.matrix_world.to_quaternion()
            fwd = q @ Vector((0, 0, -1))
            upv = q @ Vector((0, 1, 0))
            vh = 24.0 * d / max(10.0, cam.cd.lens)
            fit.location = cl + fwd * d + upv * (0.18 * vh)
            fit.rotation_euler = (q @ Euler((-math.pi / 2, 0, 0)).to_quaternion()).to_euler()
        vis_w = 24.0 * d / max(10.0, cam.cd.lens) * 0.5625
        tw = 0.62 * size * max(len(x) for x in body.split("\n"))
        k = max(0.12, min(1.0, 0.58 * vis_w / tw))
        fit.scale = (k, k, k)
    del PENDING[:]
    return cam


# ================================================================== cast
def eddie_c(t0, t1, expr="neutral"):
    return story.eddie(t0, t1, expr)


def grandpa(t0, t1, expr="sleepy", cap=True):
    G = chars.Char("Grandpa", skin="#ecd0b4", shirt="#7aa6e0", pants="#7aa6e0", hair="short", hair_color="#f2f2f2",
                   face="mustache", shirt_kind="stripes", shirt_c2="#ffffff", sleeves="long",
                   extras=("glasses", "beard"))
    story._live(G, t0, t1, expr, 0.5)
    if cap:
        Mc = M("#d9453a", 0.7)
        cyl("Grandpa_cap", 0.72, 0.9, (0, 0.06, 0.88), Mc, 20, parent=G.head, coll=G.coll, r2=0.22, rot=(-10, 0, 0))
        sphere("Grandpa_pom", 0.2, (0, 0.28, 1.4), M("#ffffff", 0.8), parent=G.head, coll=G.coll, seg=10)
    return G


def mayor_c(t0, t1, expr="joy"):
    return story.mayor(t0, t1, expr)


def baker_c(t0, t1, expr="joy"):
    B = chars.Char("Baker", skin="#e4b896", shirt="#ffffff", pants="#2b2b3a", hair="tophat", hair_color="#fbfbfb",
                   face="mustache", sleeves="long", extras=("collar:#ffffff",))
    return story._live(B, t0, t1, expr)


def grandma_c(t0, t1, expr="smile"):
    G = chars.Char("Grandma", skin="#f2dcc8", shirt="#9a6ad6", pants="#6a5a8a", hair="bun", hair_color="#dcdcdc",
                   face="girl", sleeves="long", extras=("glasses",))
    return story._live(G, t0, t1, expr, 0.5)


def mom_c(t0, t1, expr="smile"):
    G = chars.Char("Mom", skin="#f1dfc6", shirt="#e8423a", pants="#2b2b3a", hair="bob", hair_color="#7a3a1e",
                   face="girl", sleeves="long")
    return story._live(G, t0, t1, expr)


# ================================================================== fx
def pop_text(name, body, loc, t, size=1.0, col="#ffe14a", yaw=0, dur=None, outline="#1a1a22", rot_x=90):
    fit = empty(name + "_fit", loc, rot=(0, 0, yaw))
    root = empty(name, (0, 0, 0), parent=fit)
    PENDING.append((fit, body, size, t, tuple(loc), rot_x))
    text(name + "_t", body, (0, 0, 0), size, emitm(col, 2.5), rot=(rot_x, 0, 0), extrude=0.08 * size, parent=root)
    text(name + "_o", body, (0.04 * size, 0.06 * size, -0.04 * size), size, M(outline, 0.6), rot=(rot_x, 0, 0),
         extrude=0.06 * size, parent=root)
    root.scale = (0.01,) * 3
    root.keyframe_insert("scale", frame=F(t - 0.04))
    root.scale = (1.25,) * 3
    root.keyframe_insert("scale", frame=F(t + 0.08))
    root.scale = (1.0,) * 3
    root.keyframe_insert("scale", frame=F(t + 0.16))
    if dur:
        root.keyframe_insert("scale", frame=F(t + dur - 0.1))
        root.scale = (0.01,) * 3
        root.keyframe_insert("scale", frame=F(t + dur))
    noise(root, "rotation_euler", 1, 0.04, 8)
    return root


def wave(name, loc, t, r1=16.0, dur=0.7, col="#ffffff", rot=(0, 0, 0)):
    """Expanding translucent shock disc."""
    Mw = mat("wave_" + col, hexc(col), 0.3, emit=hexc(col), estr=2.5, alpha=0.32)
    o = cyl(name, 1.0, 0.08, loc, Mw, 40, rot=rot)
    o.scale = (0.01, 0.01, 1)
    o.keyframe_insert("scale", frame=F(t - 0.03))
    o.scale = (r1, r1, 1)
    o.keyframe_insert("scale", frame=F(t + dur))
    o.scale = (0.01, 0.01, 1)
    o.keyframe_insert("scale", frame=F(t + dur + 0.04))
    return o


def zzz(loc, t0, t1, n=5, size=1.0, yaw=0, col="#ffffff"):
    for i in range(n):
        ts = t0 + i * (t1 - t0) / n
        o = empty(f"z{i}_{F(t0)}", loc, rot=(0, 0, yaw))
        text(f"zt{i}_{F(t0)}", "Z", (0, 0, 0), size * (0.7 + 0.18 * i), emitm(col, 2.0), extrude=0.05, parent=o)
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts))
        o.scale = (1, 1, 1)
        o.keyframe_insert("scale", frame=F(ts + 0.12))
        o.keyframe_insert("location", frame=F(ts))
        o.location = (loc[0] + 0.6 + 0.4 * i, loc[1], loc[2] + 1.0 + 0.9 * i)
        o.keyframe_insert("location", frame=F(ts + 0.9))
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts + 0.9))


def sparkle(name, loc, t, s=1.0, n=10, seed=0, col="#fff1a0"):
    rnd = random.Random(seed)
    Ms = mat("sp_" + col, hexc(col), 0.3, emit=hexc(col), estr=10)
    for i in range(n):
        p = Vector(loc) + Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.5, 1))) * s
        o = sphere(f"{name}{i}", 0.09 * s, tuple(p), Ms, seg=8)
        ts = t + rnd.uniform(0, 0.4)
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts - 0.05))
        o.scale = (1.6, 1.6, 1.6)
        o.keyframe_insert("scale", frame=F(ts + 0.08))
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts + 0.3))


def snore(ch, t0, t1, rate=0.7, mouth="ah"):
    """Sleeping face cycle: closed eyes, mouth opens on each snore, chest heaves."""
    t = t0
    k = 0
    while t < t1:
        ch.face(t, eyes="closed", mouth=mouth if k % 2 == 0 else "flat")
        ch.pose(t, torso=(0, 3 if k % 2 == 0 else 0, 0))
        t += rate / 2
        k += 1


def shake_obj(ob, t0, t1, amp=0.25, rate=9.0):
    t = t0
    k = 0
    base = Vector(ob.location)
    while t < t1:
        s = 1 if k % 2 == 0 else -1
        ob.location = base + Vector((s * amp, 0, s * amp * 0.5))
        ob.keyframe_insert("location", frame=F(t))
        t += 1.0 / rate
        k += 1
    ob.location = base
    ob.keyframe_insert("location", frame=F(t1))


# ================================================================== props
def cow(name, loc, rot=0, s=1.0):
    r = empty(name, loc, rot=(0, 0, rot))
    Mw, Mb, Mp = M("#f7f7f2", 0.7), M("#262626", 0.7), M("#f2a6b0", 0.6)
    box(name + "_b", (3.0, 5.0, 2.6), (0, 0, 3.4), Mw, 0.3, parent=r)
    for i, (x, y, z) in enumerate([(1.0, 0.8, 4.4), (-1.1, -0.8, 4.2), (0.9, -1.6, 3.2), (-0.6, 1.8, 3.0)]):
        box(f"{name}_sp{i}", (1.1, 1.1, 1.1), (x, y, z), Mb, 0.3, parent=r)
    box(name + "_h", (1.9, 1.8, 1.8), (0, -3.2, 4.0), Mw, 0.3, parent=r)
    box(name + "_sn", (1.3, 0.8, 0.9), (0, -4.1, 3.6), Mp, 0.2, parent=r)
    for sx in (-1, 1):
        sphere(f"{name}_e{sx}", 0.17, (sx * 0.62, -4.0, 4.5), M("#101010", 0.3), parent=r, seg=8)
        box(f"{name}_ho{sx}", (0.25, 0.25, 0.7), (sx * 0.9, -3.0, 5.2), M("#e8d8a0", 0.6), 0.05, parent=r)
        box(f"{name}_ea{sx}", (0.9, 0.4, 0.3), (sx * 1.3, -3.2, 4.6), Mw, 0.08, parent=r)
        for sy in (-1, 1):
            box(f"{name}_l{sx}{sy}", (0.7, 0.7, 2.3), (sx * 0.95, sy * 1.7, 1.15), Mw, 0.1, parent=r)
    box(name + "_ud", (1.0, 1.0, 0.5), (0, 1.5, 2.1), Mp, 0.2, parent=r)
    box(name + "_tail", (0.18, 0.18, 1.8), (0, 2.6, 3.8), Mw, 0.04, parent=r, rot=(-25, 0, 0))
    r.scale = (s,) * 3
    return r


def seagull(name, loc, rot=0, s=1.0):
    r = empty(name, loc, rot=(0, 0, rot))
    Mw, Mg, Mo = M("#fafafa", 0.6), M("#a9b0bb", 0.6), M("#f5a623", 0.5)
    sphere(name + "_b", 0.7, (0, 0, 0), Mw, (0.85, 1.4, 0.8), parent=r, seg=16)
    sphere(name + "_h", 0.4, (0, -1.1, 0.4), Mw, parent=r, seg=12)
    cyl(name + "_bk", 0.12, 0.55, (0, -1.5, 0.35), Mo, 8, parent=r, rot=(90, 0, 0), r2=0.02)
    for sx in (-1, 1):
        sphere(f"{name}_e{sx}", 0.07, (sx * 0.2, -1.35, 0.55), M("#101010", 0.3), parent=r, seg=6)
        w = box(f"{name}_w{sx}", (1.9, 0.9, 0.12), (sx * 1.2, 0.1, 0.15), Mg, 0.05, parent=r)
        w.rotation_euler = (0, math.radians(sx * 18), 0)
        noise(w, "rotation_euler", 1, 0.9, 3)
    box(name + "_t", (0.7, 0.8, 0.1), (0, 1.1, 0.0), Mw, 0.04, parent=r)
    r.scale = (s,) * 3
    return r


def rooster(name, loc, rot=0, s=1.0):
    r = empty(name, loc, rot=(0, 0, rot))
    Mr, Mo, My = M("#c93a2a", 0.6), M("#e8872a", 0.6), M("#f5c030", 0.5)
    sphere(name + "_b", 0.9, (0, 0, 1.3), Mr, (0.9, 1.3, 1.0), parent=r, seg=16)
    sphere(name + "_h", 0.5, (0, -1.0, 2.5), Mr, parent=r, seg=12)
    box(name + "_c", (0.15, 0.7, 0.7), (0, -1.0, 3.1), M("#e01818", 0.4), 0.05, parent=r)
    cyl(name + "_bk", 0.14, 0.5, (0, -1.5, 2.5), My, 8, parent=r, rot=(90, 0, 0), r2=0.02)
    for sx in (-1, 1):
        sphere(f"{name}_e{sx}", 0.09, (sx * 0.3, -1.3, 2.65), M("#101010", 0.3), parent=r, seg=6)
        box(f"{name}_lg{sx}", (0.12, 0.12, 0.9), (sx * 0.35, 0, 0.45), My, 0.02, parent=r)
    for i in range(3):
        box(f"{name}_tf{i}", (0.2, 0.9, 1.6), ((i - 1) * 0.5, 1.4, 2.2), [Mo, M("#2f8f4a", 0.5), Mr][i], 0.06,
            parent=r, rot=(-30, (i - 1) * 18, 0))
    r.scale = (s,) * 3
    return r


def moon_ball(name, loc, r=12.0):
    root = empty(name, loc)
    sphere(name + "_m", r, (0, 0, 0), mat("moonmat", hexc("#f4f1dc"), 0.9, emit=hexc("#f4f1dc"), estr=1.2), parent=root,
           seg=40)
    Mc = M("#cfcab0", 0.9)
    for i, (x, z, rr) in enumerate([(-0.3, 0.25, 0.22), (0.35, -0.1, 0.16), (-0.1, -0.4, 0.13), (0.15, 0.45, 0.1)]):
        sphere(f"{name}_cr{i}", r * rr, (x * r, -r * 0.93, z * r), Mc, (1, 0.25, 1), parent=root, seg=16)
    return root


def haystack(name, loc, s=1.0):
    r = empty(name, loc)
    My, Md = M("#e8c04a", 0.9), M("#c9962e", 0.9)
    cyl(name + "_b", 3.4 * s, 3.2 * s, (0, 0, 1.6 * s), My, 24, parent=r)
    sphere(name + "_t", 3.4 * s, (0, 0, 3.2 * s), Md, (1, 1, 0.7), parent=r, seg=20)
    return r


def antenna(name, loc, h=8.0):
    r = empty(name, loc)
    Mg = M("#aab0ba", 0.4, metal=0.6)
    cyl(name + "_p", 0.15, h, (0, 0, h / 2), Mg, 8, parent=r)
    for i, (z, w) in enumerate([(h * 0.45, 3.4), (h * 0.65, 2.6), (h * 0.85, 1.8)]):
        box(f"{name}_c{i}", (w, 0.1, 0.1), (0, 0, z), Mg, 0.0, parent=r)
    return r


def book(name, loc, rot=(0, 0, 0), parent=None, s=1.0, label="VACUUM\nMANUAL"):
    r = empty(name, loc, parent=parent, rot=rot)
    box(name + "_c", (1.5 * s, 0.28 * s, 2.0 * s), (0, 0, 0), M("#2f6fd0", 0.5), 0.04, parent=r)
    box(name + "_pg", (1.4 * s, 0.22 * s, 1.9 * s), (0.04 * s, 0.02 * s, 0), M("#f6f1e2", 0.8), 0.02, parent=r)
    text(name + "_tx", label, (0, -0.16 * s, 0.1 * s), 0.3 * s, emitm("#ffffff", 1.2), parent=r, extrude=0.005)
    # little vacuum icon
    box(name + "_ic", (0.5 * s, 0.02, 0.28 * s), (0, -0.15 * s, -0.55 * s), M("#e8423a", 0.5), 0.02, parent=r)
    return r


def pillow_box(name, loc, parent=None, s=1.0):
    return box(name, (1.4 * s, 0.8 * s, 0.7 * s), loc, M("#ffffff", 0.9), 0.3, parent=parent)


# ================================================================== scenes
def ceiling(t0, t1, z0, z1, seed=2, n=7, ex=135, sc=(5.5, 8.5), extra=None, tag=""):
    """Cloud layer = the sky. Root moves from z0 (t0) to z1 (t1); extra = [(t, z), ...] more keys."""
    root = empty(f"ceil{seed}{tag}", (0, 0, z0))
    rnd = random.Random(seed)
    for i in range(n):
        for j in range(n):
            x = (i / (n - 1) - 0.5) * 2 * ex + rnd.uniform(-10, 10)
            y = (j / (n - 1) - 0.5) * 2 * ex + rnd.uniform(-10, 10) - 30
            c = W.cloud(f"ce{seed}{tag}_{i}_{j}", (x, y, rnd.uniform(-2.5, 3.0)), rnd.uniform(*sc), None,
                        seed * 100 + i * 10 + j)
            c.parent = root
    keys = [(t0, z0), (t1, z1)] + (extra or [])
    for t, z in sorted(keys):
        root.location = (0, 0, z)
        root.keyframe_insert("location", frame=F(t))
    return root


def blue_house(loc=HOUSE, lit=False, door_open=False):
    r = empty("bhouse", loc)
    Mb = M("#3a78d8", 0.6)
    box("bh_body", (15, 11, 9), (0, 0, 4.5), Mb, 0.15, parent=r)
    # roof: triangular prism
    poly_extrude("bh_roof", [(-8.4, 0), (8.4, 0), (0, 4.2)], 12.4, (0, 6.2, 9.0), M("#8a2f2f", 0.7), rot=(90, 0, 0), parent=r)
    box("bh_door", (2.6, 0.3, 5.4), (-3.2, -5.6, 2.7), M("#f0f0f0", 0.5), 0.05, parent=r)
    sphere("bh_knob", 0.2, (-2.4, -5.8, 2.6), M("#e2b23a", 0.3, metal=0.9), parent=r, seg=8)
    box("bh_chim", (1.6, 1.6, 4.0), (5.0, 2.0, 11.0), M("#a8553c", 0.7), 0.05, parent=r)
    glow = emitm("#ffd27a", 2.5) if lit else mat("bh_win", hexc("#bfe0ff"), 0.1, emit=hexc("#bfe0ff"), estr=0.8)
    box("bh_wfr", (3.6, 0.25, 3.4), (3.6, -5.6, 5.2), M("#ffffff", 0.5), 0.05, parent=r)
    box("bh_wg", (3.0, 0.3, 2.8), (3.6, -5.62, 5.2), glow, 0.03, parent=r)
    box("bh_step", (4.0, 1.6, 0.4), (-3.2, -6.4, 0.2), M("#c9c6bf", 0.8), 0.05, parent=r)
    antenna("bh_ant", (-3.5, 3.0, 9.4), 6.5).parent = r
    return r


TOWN_DY = -50.0


def town_ground():
    res = W.town(school=False)
    for ob in res["coll"].all_objects:
        if ob.parent is None:
            ob.location.y += TOWN_DY
    box("main_road", (260, 8, 0.06), (0, -68, 0.05), M("#55565e", 0.8), 0)
    return res


def town_day(t0, t1, z0=64, z1=64, extra=None, house=True, lit=False, seed=2, sun=True):
    W.sky(1.0)
    if sun:
        W.sun(4.0, rot=(52, 0, 30))
    town_ground()
    if house:
        blue_house(lit=lit)
    c = ceiling(t0, t1, z0, z1, seed=seed, extra=extra)
    return c


def town_night(t0, t1, z0=64, z1=64, lit=True, seed=2, house=True):
    W.sky(0.7, top=(0.02, 0.04, 0.2), bottom=(0.1, 0.16, 0.42))
    light("nsun", "SUN", (0, 0, 50), 2.4, (0.6, 0.7, 1.0), 2, rot=(50, 0, 30))
    town_ground()
    if house:
        blue_house(lit=lit)
    return ceiling(t0, t1, z0, z1, seed=seed)


def room(night=True, lamp=True, window_x=-6.0, bright=1.0):
    """Grandpa's bedroom. Camera lives at y < -6. Back wall y=10. Returns anchors."""
    wcol = "#b9c8ea" if night else "#e8dcc8"
    Mw = M(wcol, 0.85)
    box("r_floor", (26, 30, 0.4), (0, 0, -0.2), planks("rfloor"), 0)
    box("r_back", (26, 0.6, 14), (0, ROOM_BACK + 0.3, 7), Mw, 0)
    box("r_left", (0.6, 30, 14), (-13, 0, 7), Mw, 0)
    box("r_right", (0.6, 30, 14), (13, 0, 7), Mw, 0)
    box("r_ceil", (26, 30, 0.4), (0, 0, 14.2), M("#dfe6f3", 0.9), 0)
    # window on the back wall
    wx = window_x
    sky = mat("r_sky", (0.1, 0.16, 0.4) if night else (0.6, 0.8, 1.0), 0.2, emit=(0.15, 0.22, 0.55) if night else (0.7, 0.85, 1.0),
              estr=1.0 if night else 2.0)
    box("w_glass", (4.0, 0.2, 4.4), (wx, ROOM_BACK - 0.1, 7.2), sky, 0.0)
    hinge = empty("w_hingeL", (wx - 2.2, ROOM_BACK - 0.45, 7.2))
    box("w_sashL", (2.2, 0.2, 4.6), (1.1, 0.0, 0), M("#ffffff", 0.5), 0.04, parent=hinge)
    box("w_sashL_g", (1.8, 0.22, 4.1), (1.1, 0.0, 0), mat("w_gl", (0.7, 0.85, 1.0), 0.05, alpha=0.25, spec=1.0), 0.0, parent=hinge)
    hingeR = empty("w_hingeR", (wx + 2.2, ROOM_BACK - 0.45, 7.2))
    box("w_sashR", (2.2, 0.2, 4.6), (-1.1, 0.0, 0), M("#ffffff", 0.5), 0.04, parent=hingeR)
    box("w_sashR_g", (1.8, 0.22, 4.1), (-1.1, 0.0, 0), mat("w_gl", (0.7, 0.85, 1.0), 0.05, alpha=0.25, spec=1.0), 0.0, parent=hingeR)
    box("w_sill", (4.8, 0.7, 0.3), (wx, ROOM_BACK - 0.5, 4.8), M("#ffffff", 0.5), 0.05)
    # bed against back wall, centre
    box("bed_frame", (7.4, 9.0, 1.2), (0, 5.5, 0.6), M("#ffffff", 0.45), 0.1)
    box("bed_head", (7.4, 0.6, 4.4), (0, ROOM_BACK - 0.3, 2.2), M("#8a5a3a", 0.5), 0.1)
    box("mattress", (7.0, 8.4, 1.0), (0, 5.4, 1.7), M("#f2f4f8", 0.7), 0.25)
    box("pillow", (3.6, 2.0, 0.8), (0, 8.9, 2.45), M("#f7f8fb", 0.7), 0.35)
    bl = checker_mat("rblanket", "#2c4fae", "#5b84dc", 1.4)
    blanket = box("blanket", (7.3, 5.6, 1.1), (0, 4.0, 2.75), bl, 0.3)
    # nightstand + lamp
    box("nstand", (2.6, 2.4, 3.0), (-5.6, ROOM_BACK - 1.4, 1.5), wood("wd", "#6e4229", "#a06a45", 2.5), 0.06)
    cyl("lamp_base", 0.3, 0.9, (-5.6, ROOM_BACK - 1.4, 3.45), M("#ffffff", 0.4), 16)
    cyl("lamp_shade", 0.7, 0.9, (-5.6, ROOM_BACK - 1.4, 4.3), mat("shade", hexc("#f4efe4"), 0.6, emit=hexc("#ffd9a0"),
        estr=3.0 if lamp else 0.0), 24, r2=0.5)
    box("clock_b", (1.1, 0.5, 0.6), (-4.6, ROOM_BACK - 1.0, 3.3), M("#b8221e", 0.4), 0.08)
    # rug + chair + shelf
    cyl("rug", 5.5, 0.06, (0, -1.0, 0.03), M("#3aa3b8", 0.95), 48)
    box("chair_seat", (2.4, 2.4, 0.4), (8.0, 1.5, 2.2), M("#b5764e", 0.6), 0.06)
    box("chair_back", (2.4, 0.3, 3.0), (8.0, 2.8, 3.7), M("#b5764e", 0.6), 0.06)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"chair_l{sx}{sy}", (0.25, 0.25, 2.2), (8.0 + sx * 1.0, 1.5 + sy * 1.0, 1.1), M("#8a5634", 0.6), 0.02)
    box("wshelf", (5.0, 0.9, 0.3), (7.5, ROOM_BACK - 0.6, 8.0), M("#8a5634", 0.6), 0.03)
    for i in range(5):
        box(f"wbk{i}", (0.5, 0.7, 1.2), (5.6 + i * 0.6, ROOM_BACK - 0.7, 8.7), M(["#d4423a", "#3e6fd0", "#4fae5a", "#f0c040", "#9b6ad6"][i], 0.6), 0.03)
    # lights
    if night:
        light("room_moon", "AREA", (window_x, 4, 11), 2200 * bright, (0.5, 0.65, 1.0), 9, target=(0, 4, 2))
        light("room_fill", "AREA", (4, -9, 9), 1100 * bright, (0.6, 0.65, 1.0), 12, target=(0, 4, 3))
        if lamp:
            light("room_lamp", "POINT", (-5.6, ROOM_BACK - 1.9, 4.4), 90, (1.0, 0.75, 0.45), 0.6)
    else:
        light("room_sun", "AREA", (window_x, 2, 11), 6500 * bright, (1.0, 0.96, 0.88), 9, target=(0, 4, 2))
        light("room_fill", "AREA", (4, -9, 9), 3200 * bright, (1.0, 0.98, 0.95), 14, target=(0, 4, 3))
    return dict(hingeL=hinge, hingeR=hingeR, blanket=blanket, wx=wx)


def lie_in_bed(ch, t, y=3.9):
    """Grandpa on his back, head on the pillow (face up, head toward the wall)."""
    ch.root.rotation_euler[0] = math.radians(-90)
    ch.pose(t, loc=(0, y, BED_TOP + 0.62), rot=0, armL=(8, 6), armR=(8, 6))
    ch.root.rotation_euler[2] = 0.0


def sit_in_bed(ch, t, x=0.0, y=7.6):
    ch.pose(t, loc=(x, y, BED_TOP - 1.96 + 0.1), rot=0, legL=(88, 4), legR=(88, -4), armL=(25, 6), armR=(25, 6))


def open_window(R, t, dur=0.35):
    for k, h in enumerate((R["hingeL"], R["hingeR"])):
        sgn = 1 if k == 0 else -1
        h.rotation_euler[2] = 0
        h.keyframe_insert("rotation_euler", index=2, frame=F(t))
        h.rotation_euler[2] = math.radians(-100 * sgn)
        h.keyframe_insert("rotation_euler", index=2, frame=F(t + dur))


def tiptoe(ch, t0, t1, p0, p1, rate=1.4):
    ch.walk(t0, t1, p0, p1, rate=rate, swing=14, arm=10, bob=0.05)
    ch.pose(t0, torso=(0, 6, 0))
    return ch


def crawl_pose(ch, t, loc, rot=0):
    ch.pose(t, loc=loc, rot=rot, torso=(0, 78, 0), head=(0, -55, 0), armL=(-70, 8), armR=(-70, 8), legL=(30, 6),
            legR=(30, -6), hipz=-1.0)


def sfx_snore(t, vol=0.9):
    sfx(t, "snort", vol)


def clock(name, loc, t0, t1, r=1.6, turns=8.0, rot=(90, 0, 0)):
    root = empty(name, loc, rot=(0, 0, 0))
    cyl(name + "_f", r, 0.3, (0, 0, 0), M("#f6f6f0", 0.4), 40, rot=rot, parent=root)
    cyl(name + "_r", r * 1.08, 0.2, (0, 0.06, 0), M("#d9453a", 0.4), 40, rot=rot, parent=root)
    hand = empty(name + "_hand", (0, -0.2, 0), parent=root)
    box(name + "_hb", (0.1, 0.06, r * 0.8), (0, 0, r * 0.4), M("#1a1a22", 0.4), 0.0, parent=hand)
    hand.rotation_euler = (0, 0, 0)
    hand.keyframe_insert("rotation_euler", frame=F(t0))
    hand.rotation_euler = (0, math.radians(360 * turns), 0)
    hand.keyframe_insert("rotation_euler", frame=F(t1))
    set_interp(hand, "rotation_euler", F(t0), "LINEAR")
    return root


def vacuum(name, loc, rot=0, s=1.0):
    r = empty(name, loc, rot=(0, 0, rot))
    cyl(name + "_b", 1.2 * s, 1.6 * s, (0, 0, 1.0 * s), M("#e8423a", 0.35), 28, parent=r, rot=(90, 0, 0))
    for sx in (-1, 1):
        cyl(f"{name}_w{sx}", 0.45 * s, 0.3 * s, (sx * 1.15 * s, 0.3 * s, 0.45 * s), M("#222222", 0.6), 16, parent=r, rot=(0, 90, 0))
    cyl(name + "_hose", 0.22 * s, 4.0 * s, (0, -1.4 * s, 2.4 * s), M("#555a66", 0.5), 12, parent=r, rot=(-35, 0, 0))
    box(name + "_nz", (1.2 * s, 1.2 * s, 0.3 * s), (0, -2.8 * s, 0.25 * s), M("#2a2d36", 0.5), 0.05, parent=r)
    return r


def mug(name, loc, steam_t0=None, steam_t1=None, parent=None):
    r = empty(name, loc, parent=parent)
    cyl(name + "_c", 0.45, 0.8, (0, 0, 0.4), M("#f5f5f0", 0.4), 20, parent=r)
    cyl(name + "_m", 0.4, 0.05, (0, 0, 0.76), M("#fffbe8", 0.5), 20, parent=r)
    box(name + "_hd", (0.5, 0.1, 0.5), (0.55, 0, 0.4), M("#f5f5f0", 0.4), 0.04, parent=r)
    if steam_t0 is not None:
        Ms = mat("steam", (1, 1, 1), 0.9, emit=(1, 1, 1), estr=0.6, alpha=0.5)
        for i in range(4):
            o = sphere(f"{name}_st{i}", 0.18, (0.0, 0.0, 1.0), Ms, parent=r, seg=8)
            ts = steam_t0 + i * 0.25
            o.scale = (0.01,) * 3
            o.keyframe_insert("scale", frame=F(ts))
            o.keyframe_insert("location", frame=F(ts))
            o.scale = (1.4, 1.4, 1.4)
            o.keyframe_insert("scale", frame=F(ts + 0.3))
            o.location = (0.08 * (i - 1.5), 0, 2.4)
            o.keyframe_insert("location", frame=F(ts + 0.9))
            o.scale = (0.01,) * 3
            o.keyframe_insert("scale", frame=F(ts + 0.9))
    return r


def no_sign(name, loc, s=1.0):
    r = empty(name, loc)
    cyl(name + "_o", 1.6 * s, 0.2, (0, 0, 0), emitm("#e02020", 1.5), 40, rot=(90, 0, 0), parent=r)
    cyl(name + "_i", 1.25 * s, 0.24, (0, -0.02, 0), M("#ffffff", 0.5), 40, rot=(90, 0, 0), parent=r)
    box(name + "_bar", (2.9 * s, 0.26, 0.38 * s), (0, -0.05, 0), emitm("#e02020", 1.5), 0.02, parent=r, rot=(0, 45, 0))
    return r


# =========================================================================================== SHOTS
@S(1, 0, 3, "HOOK: grandpa snoring in bed, mid-snore crash zoom")
def s01(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    snore(G, t0, t1, 0.6)
    zzz((0.8, 8.0, 5.0), t0 + 0.2, t1, n=5, size=1.2)
    tgt = (0, 8.4, 3.2)
    cam = mv("in", t0, t1, tgt, d=6.5, yaw=-12, pitch=34, lens=30)
    cam.crash(w(2), 30, 46, 0.12)
    bump(cam, w(2), 0.5)
    fin(cam, 1.0)
    sfx(w(2) - 0.05, "snort", 1.0)
    sfx(t0 + 0.02, "whoosh", 0.7)


@S(2, 3, 9, "wide: ripples from the house hold up the sky")
def s02(t0, t1):
    town_day(t0, t1, 56, 56, extra=[(t0 + 0.9, 60), (t1, 56)])
    for i in range(3):
        wave(f"wv{i}", (HOUSE[0], HOUSE[1], 12 + i * 5), t0 + 0.2 + i * 0.45, 14 + i * 4, 0.9)
    cam = mv("rise", t0, t1, (0, -48, 24), d=62, yaw=8, pitch=12, lens=24, fstop=11)
    fin(cam, 0.8)
    sfx(t0 + 0.1, "rise", 0.6)


@S(3, 9, 15, "low angle: clouds sag over the heads of townsfolk")
def s03(t0, t1):
    town_day(t0, t1, 36, 20)
    for i, x in enumerate((-4.5, 0.5, 5.0)):
        k = townie(i + 2, t0, t1, "lookup")
        k.pose(t0, loc=(x, -74 + (i % 2), 0), rot=0, armL=(15, 12), armR=(15, 12))
        k.pose(t0, head=(0, -32, 0))
        k.face(w(12), "scared")
    cam = Cam()
    cam.key(t0, (0.5, -82, 1.4), (0, -68, 15), lens=22, fstop=8, focus=12.0)
    cam.key(t1, (-1.5, -80, 1.6), (0, -66, 19), lens=20, fstop=8, focus=12.0)
    cam.crash(w(12), 22, 17, 0.2)
    bump(cam, w(13), 0.25)
    fin(cam, 1.2)
    sfx(t0 + 0.4, "wind", 0.5)
    sfx(w(12), "rise", 0.7)


@S(4, 15, 18, "night: grandpa's window glows")
def s04(t0, t1):
    town_night(t0, t1, 64, 60)
    cam = Cam()
    cam.key(t0, (14, -80, 2.0), (2, -48, 5.0), lens=26, fstop=6, focus=34.0)
    cam.key(t1, (7, -68, 6.5), (3.6, -53, 5.4), lens=26, fstop=6, focus=18.0)
    fin(cam, 1.0)
    sfx(t0, "crickets", 0.6)


@S(5, 18, 21, "he woke up: eyes snap open")
def s05(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    G.face(t0, eyes="closed", mouth="flat")
    tw = w(19) - 0.05
    G.face(tw, eyes="wide", mouth="o")
    cam = Cam()
    cam.key(t0, (1.2, 5.6, 7.4), (0, 8.6, 3.1), lens=38, focus=4.5, fstop=2.2)
    cam.key(t1, (0.5, 6.4, 6.2), (0, 8.6, 3.1), lens=38, focus=3.4, fstop=2.2)
    cam.crash(tw, 38, 60, 0.1)
    bump(cam, tw, 0.4)
    fin(cam, 1.0)
    sfx(tw, "gasp", 0.9)
    sfx(tw, "ding", 0.5)


@S(6, 21, 26, "narrator: 'You see, in this world,'")
def s06(t0, t1):
    town_day(t0, t1, 60, 60, house=True)
    E = eddie_c(t0, t1, "talk")
    E.pose(t0, loc=(-3, -72, 0), rot=-8)
    E.act(t0, "hold")
    lips(E, t0, t1)
    cam = mv("dutch", t0, t1, (-3, -72, 4.6), d=8.5, yaw=-8, pitch=3, lens=30)
    cam.crash(w(23), 30, 38, 0.1)
    fin(cam, 1.0)
    sfx(t0, "whoosh", 0.6)


@S(7, 26, 31, "the sky is held up: cloud layer, ripples")
def s07(t0, t1):
    town_day(t0, t1, 52, 54)
    for i in range(4):
        wave(f"wv{i}", (HOUSE[0], HOUSE[1], 14 + i * 7), t0 + 0.15 + i * 0.35, 18 + i * 5, 0.8)
    cam = Cam()
    cam.key(t0, (-30, -90, 3.0), (0, -48, 30), lens=22, fstop=11, focus=70.0)
    cam.key(t1, (-18, -76, 3.0), (0, -48, 34), lens=22, fstop=11, focus=60.0)
    fin(cam, 0.8)
    sfx(t0, "rise", 0.5)


@S(8, 31, 38, "by the snores of one old man: roof-level zzz, pull up")
def s08(t0, t1):
    town_day(t0, t1, 52, 56, lit=True)
    zzz((3.6, -53.5, 9.5), t0 + 0.1, t1, n=6, size=1.6)
    for i in range(2):
        wave(f"wv{i}", (HOUSE[0], HOUSE[1], 14 + i * 8), t0 + 0.9 + i * 0.5, 16 + i * 6, 0.9)
    cam = mv("rise", t0, t1, (3, -50, 9.5), d=26, yaw=-12, pitch=2, lens=26)
    fin(cam, 0.9)
    sfx(t0 + 0.2, "snort", 0.8)


@S(9, 38, 42, "every country has one: globe with tiny grandpas")
def s09(t0, t1):
    W.space_world(1.0)
    W.sun(5.0, rot=(55, 0, 25))
    W2.earth("globe", (0, 0, 0), 18)
    for i, deg in enumerate((0, 55, -50, 100, -105)):
        G = grandpa(t0, t1, "sleepy")
        a = math.radians(deg)
        G.pose(t0, loc=(math.sin(a) * 18.4, -1.0, math.cos(a) * 18.4), rot=0)
        G.root.rotation_euler[1] = a
        G.root.scale = (1.6,) * 3
        zzz((math.sin(a) * 21, -2.0, math.cos(a) * 21 + 2), t0 + 0.1 * i, t1, n=3, size=1.5)
    cam = Cam()
    cam.key(t0, (-24, -58, 8), (0, 0, 8), lens=30, fstop=11, focus=50.0)
    cam.key(t1, (22, -50, 12), (0, 0, 8), lens=30, fstop=11, focus=50.0)
    fin(cam, 0.6)
    sfx(t0, "whoosh", 0.6)
    sfx(w(41), "pop", 0.6)


@S(10, 42, 48, "ours lives in a blue house: hero reveal")
def s10(t0, t1):
    town_day(t0, t1, 62, 62)
    cam = Cam()
    cam.key(t0, (16, -86, 2.5), (0, -48, 6), lens=26, fstop=8, focus=44.0)
    cam.key(t1, (6, -68, 9.5), (0, -48, 7), lens=26, fstop=8, focus=24.0)
    cam.crash(w(46), 26, 34, 0.15)
    fin(cam, 1.0)
    sfx(w(46), "pop", 0.6)


@S(11, 48, 54, "at the end of my street: Eddie walks to the house")
def s11(t0, t1):
    town_day(t0, t1, 62, 62)
    E = eddie_c(t0, t1, "smile")
    E.walk(t0, t1, (-10, -100, 0), (-6, -66, 0), rate=2.6)
    cam = Cam()
    cam.track(E, t0, t1, offset=(5, 6, 1.0), look_up=4.0, lens=26, step=0.25, fstop=6.0)
    fin(cam, 1.0)
    sfx(t0, "footsteps", 0.7)


@S(12, 54, 56, "HONG SHU! 1: house shakes, shock waves")
def s12(t0, t1):
    town_day(t0, t1, 56, 56, extra=[(t0 + 0.15, 66), (t0 + 0.7, 60), (t1, 58)], lit=True)
    ts = t0 + 0.05
    pop_text("hs", "HONG\nSHU!", (-1, -62, 13), ts, size=4.2, col="#ffe14a")
    for i in range(3):
        wave(f"wv{i}", (HOUSE[0], HOUSE[1], 10 + i * 4), ts + i * 0.12, 22, 0.8)
    cam = Cam()
    cam.key(t0, (0, -78, 6), (0, -48, 9), lens=22, fstop=8, focus=30.0)
    cam.key(t1, (0, -72, 9), (0, -48, 11), lens=22, fstop=8, focus=24.0)
    cam.crash(ts, 22, 30, 0.1)
    bump(cam, ts, 0.9, 8)
    fin(cam, 1.0)
    sfx(ts, "snort", 1.0)
    sfx(ts, "boom", 0.9)


@S(13, 56, 60, "every snore pushes: grandpa's mouth, blanket heaves")
def s13(t0, t1):
    R = room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    snore(G, t0, t1, 0.5)
    tgt = (0, 8.0, 3.4)
    cam = mv("orb", t0, t1, tgt, d=7.5, yaw=20, pitch=30, lens=28)
    bump(cam, t0 + 0.1, 0.3)
    fin(cam, 1.0)
    sfx(t0 + 0.1, "snort", 0.8)


@S(14, 60, 66, "the clouds pushed back up where they belong")
def s14(t0, t1):
    town_day(t0, t1, 24, 62, extra=[(t0 + 0.5, 40), (t0 + 1.0, 46)])
    for i in range(3):
        wave(f"wv{i}", (HOUSE[0], HOUSE[1], 10 + i * 6), t0 + 0.2 + i * 0.5, 22, 0.9)
    cam = Cam()
    cam.key(t0, (0, -90, 2.0), (0, -50, 16), lens=22, fstop=11, focus=60.0)
    cam.key(t1, (4, -84, 2.5), (0, -50, 42), lens=22, fstop=11, focus=60.0)
    cam.crash(t0 + 1.0, 22, 18, 0.5)
    fin(cam, 0.9)
    sfx(t0 + 0.2, "rise", 0.9)
    sfx(t0 + 0.2, "whoosh", 0.7)


@S(15, 66, 70, "so the whole town: townies tiptoe in a line")
def s15(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    for i in range(6):
        k = townie(i + 1, t0, t1, "worried")
        tiptoe(k, t0, t1, (-22 + i * 2.6, -64 - (i % 2) * 2, 0), (-8 + i * 2.6, -64 - (i % 2) * 2, 0))
    cam = mv("slide", t0, t1, (-6, -64, 4), d=22, yaw=-6, pitch=4, lens=28)
    fin(cam, 1.0)
    sfx(t0, "footsteps", 0.5)


@S(16, 70, 73, "works around him: SHHH sign + baker tiptoeing")
def s16(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    b = baker_c(t0, t1, "worried")
    tiptoe(b, t0, t1, (-6, -66, 0), (-1, -66, 0))
    b.act(t0, "point", expr="worried")
    pop_text("shh", "SHHH!", (4, -63, 7), t0 + 0.15, size=2.2, col="#9be8ff", dur=t1 - t0)
    cam = mv("orbr", t0, t1, (-1, -66, 4), d=11, yaw=-14, pitch=5, lens=30)
    fin(cam, 1.0)
    sfx(t0 + 0.15, "pop", 0.7)


@S(17, 73, 76, "cars drive...: car creeping on the street")
def s17(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    c = W.car("tcar", (-14, -70, 0), "#e2725b", rot=90)
    c.keyframe_insert("location", frame=F(t0))
    c.location = (6, -70, 0)
    c.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, (-4, -70, 2.2), 20, 14, yaw=-62, pitch=6, yaw1=-35, lens=28)
    fin(cam, 1.2)
    sfx(t0, "whoosh", 0.4)


@S(18, 76, 80, "mufflers made of pillows: pillow on the exhaust")
def s18(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    c = W.car("tcar2", (0, -70, 0), "#4aa5e8", rot=0)
    pillow_box("muf", (0, 4.9, 1.0), parent=c, s=1.3)
    Ms = mat("smoke_w", (1, 1, 1), 0.9, emit=(1, 1, 1), estr=0.5, alpha=0.55)
    for i in range(5):
        o = sphere(f"pf{i}", 0.4, (0, -65.0, 1.2), Ms, seg=8)
        ts = t0 + 0.25 + i * 0.3
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts))
        o.keyframe_insert("location", frame=F(ts))
        o.scale = (1.5, 1.5, 1.5)
        o.keyframe_insert("scale", frame=F(ts + 0.25))
        o.location = (0.4 * (i % 3 - 1), -62.5, 2.0)
        o.keyframe_insert("location", frame=F(ts + 0.8))
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts + 0.8))
    cam = mv("in", t0, t1, (0, -65.2, 1.4), d=7, yaw=180, pitch=8, lens=34, fstop=3.0)
    cam.crash(t0 + 0.25, 34, 42, 0.2)
    fin(cam, 1.0)
    sfx(t0 + 0.25, "pop", 0.6)
    sfx(t0 + 0.55, "pop", 0.5)
    sfx(t0 + 0.85, "pop", 0.5)


@S(19, 80, 83, "roosters are banned: rooster + red NO sign")
def s19(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    r = rooster("rst", (-1.0, -68, 0), rot=10, s=1.2)
    r.rotation_euler[2] = math.radians(10)
    r.keyframe_insert("rotation_euler", index=2, frame=F(t0))
    r.rotation_euler[2] = math.radians(-8)
    r.keyframe_insert("rotation_euler", index=2, frame=F(t1))
    s = no_sign("ns", (1.8, -64.5, 3.2), 1.0)
    s.scale = (0.01,) * 3
    s.keyframe_insert("scale", frame=F(t0 + 0.35))
    s.scale = (1.15, 1.15, 1.15)
    s.keyframe_insert("scale", frame=F(t0 + 0.5))
    s.scale = (1, 1, 1)
    s.keyframe_insert("scale", frame=F(t0 + 0.6))
    cam = mv("in", t0, t1, (0.4, -66.5, 3.0), d=9, yaw=-10, pitch=4, lens=30)
    cam.crash(t0 + 0.4, 30, 40, 0.1)
    bump(cam, t0 + 0.4, 0.3)
    fin(cam, 1.0)
    sfx(t0 + 0.05, "duck", 0.8)
    sfx(t0 + 0.4, "buzzer", 0.6)


@S(20, 83, 86, "birthday party: kids with hats, cake, candles")
def s20(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    box("tbl", (7, 2.6, 0.4), (0, -66, 2.6), M("#f2c14e", 0.6), 0.05)
    for sx in (-1, 1):
        box(f"tl{sx}", (0.4, 0.4, 2.6), (sx * 3.2, -66, 1.3), M("#a86a44", 0.6), 0.02)
    cyl("cake", 1.2, 1.0, (0, -66, 3.3), M("#ffb6d2", 0.5), 28)
    for i in range(4):
        cyl(f"cd{i}", 0.06, 0.5, (-0.6 + i * 0.4, -66, 4.0), M("#5ac8fa", 0.5), 8)
        sphere(f"fl{i}", 0.12, (-0.6 + i * 0.4, -66, 4.35), emitm("#ffb020", 6), seg=8)
    for i, x in enumerate((-4.5, -2.0, 2.0, 4.5)):
        k = townie(i + 10, t0, t1, "happy")
        k.pose(t0, loc=(x, -62.5, 0), rot=random.uniform(-12, 12), armL=(20, 10), armR=(20, 10))
        cyl(f"hat{i}", 0.5, 0.9, (0, 0.05, 0.9), M(["#ff5a5a", "#5ac8fa", "#ffd23a", "#7ee07a"][i], 0.5), 12,
            parent=k.head, coll=k.coll, r2=0.05)
    cam = mv("in", t0, t1, (0, -66, 3.6), d=12, yaw=0, pitch=14, lens=30)
    fin(cam, 1.0)
    sfx(t0, "kids_laugh", 0.5)


@S(21, 86, 89, "held in whispers: everyone goes SHHH")
def s21(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    for i, x in enumerate((-5, -1.7, 1.7, 5)):
        k = townie(i + 10, t0, t1, "worried")
        k.pose(t0, loc=(x, -66, 0), rot=0)
        k.act(t0 + 0.1 * i, "point", expr="worried")
        k.pose(t0 + 0.2 + 0.1 * i, armR=(150, -20), head=(0, 2, 0))
    pop_text("w1", "shh...", (-3, -66.5, 6.5), t0 + 0.2, size=1.4, col="#cfe8ff", dur=1.0)
    pop_text("w2", "psst", (3, -66.5, 7.0), t0 + 0.7, size=1.2, col="#cfe8ff", dur=1.0)
    cam = mv("slide", t0, t1, (0, -66, 4.0), d=11, yaw=0, pitch=5, lens=30)
    fin(cam, 1.0)
    sfx(t0 + 0.2, "chat", 0.5)


@S(22, 89, 95, "and the mayor pays my family")
def s22(t0, t1):
    town_day(t0, t1, 60, 60, house=False)
    My = mayor_c(t0, t1, "smile")
    My.pose(t0, loc=(-3, -66, 0), rot=facing((-3, -66), (3, -66)) )
    My.act(t0, "reach", expr="smile")
    Mo = mom_c(t0, t1, "smile")
    Mo.pose(t0, loc=(3, -66, 0), rot=facing((3, -66), (-3, -66)))
    cam = mv("orb", t0, t1, (0, -66, 4.2), d=13, yaw=0, pitch=4, lens=30)
    fin(cam, 1.0)
    sfx(t0 + 0.4, "chat", 0.5)


@S(23, 95, 101, "a tiny salary: one tiny coin on a palm")
def s23(t0, t1):
    W.sky(1.0)
    W.sun(4.0, rot=(52, 0, 30))
    box("pm", (30, 30, 0.4), (0, 0, -0.2), M("#d9c8a8", 0.9), 0)
    cyl("hand", 1.6, 0.4, (0, 0, 0.2), M("#e9c7a6", 0.45), 24)
    c = cyl("coin", 0.22, 0.05, (0, 0, 0.5), M("#e2b23a", 0.25, metal=0.9), 20)
    c.scale = (0.01,) * 3
    c.keyframe_insert("scale", frame=F(t0 + 0.2))
    c.scale = (1.3, 1.3, 1.3)
    c.keyframe_insert("scale", frame=F(t0 + 0.4))
    c.scale = (1, 1, 1)
    c.keyframe_insert("scale", frame=F(t0 + 0.55))
    sparkle("cs", (0, 0, 0.8), t0 + 0.4, 0.5, seed=3)
    pop_text("tiny", "$1", (0, -3.0, 1.2), t0 + 0.9, size=0.7, col="#ffe14a", rot_x=60)
    cam = Cam()
    cam.key(t0, (0, -7, 6), (0, 0, 0.5), lens=34, fstop=2.0, focus=8.0)
    cam.key(t1, (0.4, -2.8, 1.8), (0, 0, 0.5), lens=34, fstop=2.0, focus=3.0)
    fin(cam, 0.6)
    sfx(t0 + 0.3, "applepay", 0.9)
    sfx(t0 + 0.3, "coin", 0.7)


@S(24, 101, 105, "keep his bedroom nice and cozy")
def s24(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    snore(G, t0, t1, 0.8, mouth="flat")
    cam = Cam()
    cam.key(t0, (-9, -6, 5), (0, 5, 3), lens=24, fstop=6, focus=14.0)
    cam.key(t1, (9, -5, 6), (0, 5, 3), lens=24, fstop=6, focus=14.0)
    fin(cam, 0.9)
    sfx(t0 + 0.3, "sparkle", 0.5)


@S(25, 105, 109, "I'm his grandson: Eddie points at himself")
def s25(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    snore(G, t0, t1, 0.8, mouth="flat")
    E = eddie_c(t0, t1, "smile")
    E.pose(t0, loc=(-5.5, 0.5, 0), rot=-10)
    E.act(t0 + 0.2, "point", expr="smile")
    E.pose(t0 + 0.2, armR=(110, 60))
    lips(E, t0, t1)
    cam = mv("in", t0, t1, (-5.5, 0.5, 4.2), d=9, yaw=-12, pitch=4, lens=30)
    fin(cam, 1.0)
    sfx(t0 + 0.15, "pop", 0.5)


@S(26, 109, 114, "official sleep assistant: label pops over Eddie")
def s26(t0, t1):
    room(night=True)
    E = eddie_c(t0, t1, "grin")
    E.pose(t0, loc=(-2, 0.5, 0), rot=6)
    E.act(t0 + 0.2, "cheer", expr="grin")
    lips(E, t0, t1)
    pop_text("sa", "SLEEP ASSISTANT", (-2, -0.6, 7.6), w(111) - 0.05, size=1.0, col="#ffe14a")
    sparkle("sas", (-2, -0.6, 6.5), w(111), 1.6, seed=4)
    cam = mv("rise", t0, t1, (-2, 0.5, 4.4), d=10, yaw=8, pitch=4, lens=28)
    cam.crash(w(111), 28, 36, 0.12)
    fin(cam, 1.0)
    sfx(w(111), "ding", 0.8)
    sfx(w(111), "sparkle", 0.6)


@S(27, 114, 118, "I fluff the pillows")
def s27(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    snore(G, t0, t1, 0.8, mouth="flat")
    E = eddie_c(t0, t1, "smile")
    E.pose(t0, loc=(-4.4, 8.2, 0), rot=60)
    E.act(t0, "reach", expr="smile")
    E.wiggle(t0, t1, part="armR", amp=(30, 10), rate=8.0, base=(100, 4))
    pl = pillow_box("fpil", (-4.6, 9.2, 4.0), s=1.5)
    for i in range(8):
        pl.scale = (1.0, 1.0 - 0.3 * (i % 2), 1.0 + 0.25 * (i % 2))
        pl.keyframe_insert("scale", frame=F(t0 + i * 0.13))
    cam = mv("orbr", t0, t1, (-3.6, 8.4, 4.0), d=8, yaw=-30, pitch=12, lens=30)
    fin(cam, 1.0)
    sfx(t0 + 0.1, "paper", 0.6)
    sfx(t0 + 0.45, "paper", 0.6)


@S(28, 118, 122, "I warm the milk: mug steams, ding")
def s28(t0, t1):
    room(night=True)
    mug("milk", (-5.6, ROOM_BACK - 1.4, 3.15), t0 + 0.1, t1)
    E = eddie_c(t0, t1, "smile")
    E.pose(t0, loc=(-6.2, 6.2, 0), rot=0, armR=(60, 10))
    cam = Cam()
    cam.key(t0, (-9.5, 2.0, 5.2), (-5.6, ROOM_BACK - 1.4, 3.7), lens=36, fstop=2.4, focus=9.0)
    cam.key(t1, (-7.2, 5.6, 4.4), (-5.6, ROOM_BACK - 1.4, 3.7), lens=36, fstop=2.4, focus=5.0)
    fin(cam, 0.9)
    sfx(t0 + 0.9, "ding", 0.7)
    sfx(t0 + 0.1, "pop", 0.4)


_n = [28]


def SS(a, b, desc=""):
    _n[0] += 1
    return S(_n[0], a, b, desc)


def eddie_bed(t0, t1, expr="neutral", pos=(-5.5, 0.5), rot=-10):
    E = eddie_c(t0, t1, expr)
    E.pose(t0, loc=(pos[0], pos[1], 0), rot=rot)
    return E


def grandpa_lying(t0, t1, snore_rate=0.8, mouth="flat"):
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    snore(G, t0, t1, snore_rate, mouth=mouth)
    return G


def grandpa_sitting(t0, t1, expr="neutral", y=7.6):
    G = grandpa(t0, t1, expr)
    sit_in_bed(G, t0, y=y)
    return G


def hold_book(ch, side="R", t0=0.0):
    b = book("hb" + ch.name + side, (0, 0, 0), s=0.9)
    locs.hand_prop(ch, side, b, offset=(0, -0.8, -1.9), rot=(0, 0, 0))
    return b


@SS(122, 127, "I read him the dullest book: Eddie reading in chair")
def s29(t0, t1):
    room(night=True)
    grandpa_lying(t0, t1)
    E = eddie_c(t0, t1, "bored")
    E.pose(t0, loc=(8.0, 1.5, 0.2), rot=facing((8, 1.5), (0, 5)), legL=(85, 3), legR=(85, -3))
    E.pose(t0, loc=(8.0, 1.5, 2.4 - 1.96), armL=(70, -12), armR=(70, 12))
    b = hold_book(E, "R")
    E.face(t0, "bored")
    lips(E, t0, t1)
    cam = mv("orbr", t0, t1, (6, 3, 4.4), d=10, yaw=35, pitch=8, lens=30)
    fin(cam, 1.0)
    sfx(t0, "paper", 0.5)


@SS(127, 131, "the dullest book in the world: close-up on the book, yawns")
def s30(t0, t1):
    room(night=True)
    b = book("bk", (0, 3.0, 4.2), rot=(0, 0, 8), s=2.2)
    for i in range(3):
        pop_text(f"yw{i}", "ZZZ", (-1.8 + i * 1.8, 2.0, 6.0 + i * 0.5), t0 + 0.3 + i * 0.25, size=0.7, col="#9bb8ff", dur=1.0)
    b.rotation_euler[2] = math.radians(8)
    b.keyframe_insert("rotation_euler", index=2, frame=F(t0))
    b.rotation_euler[2] = math.radians(-6)
    b.keyframe_insert("rotation_euler", index=2, frame=F(t1))
    cam = Cam()
    cam.key(t0, (0.6, -3.5, 5.0), (0, 3.0, 4.2), lens=32, fstop=2.4, focus=6.5)
    cam.key(t1, (-0.2, -0.5, 4.6), (0, 3.0, 4.2), lens=32, fstop=2.4, focus=3.5)
    cam.crash(t0 + 0.05, 32, 40, 0.15)
    fin(cam, 0.8)
    sfx(t0 + 0.05, "paper", 0.6)


@SS(131, 137, "a manual for a vacuum cleaner: manual + vacuum reveal")
def s31(t0, t1):
    room(night=True)
    book("bk", (-1.8, 1.6, 3.4), rot=(0, 0, 14), s=1.8)
    v = vacuum("vac", (2.2, 1.4, 0), rot=-25, s=1.3)
    v.scale = (0.01,) * 3
    v.keyframe_insert("scale", frame=F(t0 + 0.7))
    v.scale = (1.3, 1.3, 1.3)
    v.keyframe_insert("scale", frame=F(t0 + 0.95))
    v.scale = (1.0, 1.0, 1.0)
    v.keyframe_insert("scale", frame=F(t0 + 1.1))
    pop_text("vm", "VACUUM MANUAL", (0, 3.5, 7.0), t0 + 0.55, size=1.1, col="#ffe14a")
    cam = mv("orb", t0, t1, (0.2, 1.6, 3.2), d=9, yaw=0, pitch=14, lens=30)
    cam.crash(t0 + 0.7, 30, 38, 0.12)
    fin(cam, 1.0)
    sfx(t0 + 0.7, "pop", 0.7)
    sfx(t0 + 0.7, "rimshot", 0.5)


@SS(137, 142, "asleep in four minutes: clock sprints, grandpa out cold")
def s32(t0, t1):
    room(night=True)
    G = grandpa_lying(t0, t1, 0.5, "ah")
    clock("clk", (-1.4, 2.0, 5.2), t0, t1 - 0.2, r=1.3, turns=4.0)
    pop_text("fm", "4 MIN", (1.6, 1.8, 6.0), t0 + 0.9, size=1.0, col="#7ee07a")
    zzz((0.8, 8.0, 5.0), t0 + 0.8, t1, n=4, size=1.1)
    cam = Cam()
    cam.key(t0, (-4.5, -2.5, 5.0), (-0.4, 2.0, 5.0), lens=32, fstop=2.8, focus=5.0)
    cam.key(t1, (4.5, -4.5, 6.0), (0.0, 6.0, 3.0), lens=26, fstop=6.0, focus=10.0)
    fin(cam, 1.0)
    sfx(t0, "click", 0.6)
    sfx(t0 + 0.9, "ding", 0.7)
    sfx(t0 + 1.0, "snort", 0.7)


@SS(142, 146, "But I hated it: Eddie fed up")
def s33(t0, t1):
    room(night=True)
    E = eddie_bed(t0, t1, "angry", (0, 0), 0)
    E.act(t0 + 0.2, "facepalm", expr="angry")
    E.face(w(144), "furious")
    cam = mv("in", t0, t1, (0, 0, 4.4), d=7, yaw=0, pitch=2, lens=34, fstop=2.8)
    cam.crash(w(143), 34, 44, 0.12)
    bump(cam, w(144), 0.25)
    fin(cam, 1.0)
    sfx(t0 + 0.1, "buzzer", 0.5)


@SS(146, 151, "other kids played outside: playground")
def s34(t0, t1):
    W.sky(1.0)
    W.sun(4.0, rot=(52, 0, 30))
    town_ground()
    px, py = 34, -64
    for i in range(5):
        k = townie(i + 20, t0, t1, "joy")
        a = i * 1.3
        k.pose(t0, loc=(px - 7 + i * 3.4, py - 3 + (i % 2) * 5, 0), rot=170 + i * 10)
        k.run(t0, t1, (px - 7 + i * 3.4, py - 3 + (i % 2) * 5, 0), (px - 1 + i * 2.2, py + 4 - (i % 2) * 7, 0), rate=3.2)
    cam = Cam()
    cam.push(t0, t1, (px - 2, py, 3), 26, 16, yaw=-20, pitch=8, yaw1=15, lens=28)
    fin(cam, 1.2)
    sfx(t0, "kids_laugh", 0.8)


@SS(151, 155, "I sat in a dark room: tiny Eddie in a dark bedroom")
def s35(t0, t1):
    room(night=True, lamp=False, bright=0.5)
    E = eddie_c(t0, t1, "sleepy")
    E.pose(t0, loc=(8.0, 1.5, 2.4 - 1.96), rot=facing((8, 1.5), (0, 5)), legL=(85, 3), legR=(85, -3), armL=(60, -6),
           armR=(60, 6))
    E.act(t0, "slump", expr="sleepy")
    G = grandpa_lying(t0, t1, 0.9, "flat")
    cam = Cam()
    cam.push(t0, t1, (6, 2, 3.6), 7, 20, yaw=-30, pitch=6, yaw1=-10, lens=22, fstop=6.0)
    fin(cam, 1.0)
    sfx(t0, "wind", 0.4)


@SS(155, 159, "for hours: clock hands spin")
def s36(t0, t1):
    room(night=True, lamp=False, bright=0.6)
    clock("clk", (-0.4, 4.0, 6.2), t0, t1, r=2.2, turns=14.0)
    pop_text("hrs", "HOURS...", (0.5, 3.5, 9.4), t0 + 0.3, size=1.1, col="#9bb8ff", dur=t1 - t0)
    cam = Cam()
    cam.key(t0, (-1.5, -4.0, 6.0), (-0.4, 4.0, 6.2), lens=36, fstop=2.2, focus=8.2)
    cam.key(t1, (0.5, -0.5, 6.2), (-0.4, 4.0, 6.2), lens=36, fstop=2.2, focus=4.6)
    fin(cam, 0.8)
    sfx(t0, "click", 0.5)
    sfx(t0 + 0.5, "click", 0.4)
    sfx(t0 + 0.9, "click", 0.4)


@SS(159, 162, "Grandpa, why you?")
def s37(t0, t1):
    room(night=True)
    grandpa_lying(t0, t1, 1.2, "flat")
    E = eddie_bed(t0, t1, "worried", (-4.2, 3.0), -50)
    E.act(t0, "lean", expr="worried")
    lips(E, t0, t1)
    cam = mv("in", t0, t1, (-4.2, 3.0, 4.2), d=8, yaw=-30, pitch=6, lens=32, fstop=3.0)
    fin(cam, 1.0)


@SS(162, 165, "I asked once: grandpa stirs")
def s38(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    G.face(t0, eyes="closed", mouth="flat")
    G.face(t0 + 0.7, eyes="half", mouth="flat")
    cam = Cam()
    cam.key(t0, (3.0, 4.5, 7.0), (0, 8.6, 3.1), lens=40, fstop=2.2, focus=5.0)
    cam.key(t1, (1.0, 5.6, 6.0), (0, 8.6, 3.1), lens=40, fstop=2.2, focus=3.6)
    fin(cam, 1.0)
    sfx(t0 + 0.7, "pop", 0.3)


@SS(165, 168, "He just smiled")
def s39(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    G.face(t0, eyes="half", mouth="flat")
    G.face(t0 + 0.3, eyes="happy", mouth="smile")
    sparkle("sm", (0, 8.4, 5.0), t0 + 0.35, 1.2, seed=5)
    cam = Cam()
    cam.key(t0, (-2.0, 5.5, 6.4), (0, 8.6, 3.1), lens=40, fstop=2.2, focus=4.6)
    cam.key(t1, (-0.6, 6.2, 5.6), (0, 8.6, 3.1), lens=40, fstop=2.2, focus=3.4)
    cam.crash(t0 + 0.3, 40, 48, 0.2)
    fin(cam, 1.0)
    sfx(t0 + 0.3, "sparkle", 0.5)
    sfx(t0 + 0.3, "aww", 0.4)


@SS(168, 173, "Somebody has to snore, kiddo")
def s40(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    G.face(t0, eyes="happy", mouth="smile")
    lips(G, t0, t1)
    E = eddie_bed(t0, t1, "worried", (-4.4, 3.4), -50)
    cam = mv("orb", t0, t1, (0, 7.6, 3.4), d=7.5, yaw=-8, pitch=24, lens=30)
    fin(cam, 1.0)


@SS(173, 175, "HONG SHU! 2")
def s41(t0, t1):
    room(night=True)
    G = grandpa_lying(t0, t1, 0.5, "ah")
    ts = t0 + 0.05
    G.face(ts, eyes="closed", mouth="ah")
    pop_text("hs", "HONG\nSHU!", (0, 0.5, 8.5), ts, size=2.6, col="#ffe14a")
    cam = Cam()
    cam.key(t0, (0, -3.0, 6.5), (0, 6, 4.0), lens=24, fstop=5.0, focus=10.0)
    cam.key(t1, (0, -2.0, 6.8), (0, 6, 4.2), lens=24, fstop=5.0, focus=9.0)
    cam.crash(ts, 24, 32, 0.1)
    bump(cam, ts, 0.7)
    fin(cam, 1.0)
    sfx(ts, "snort", 1.0)
    sfx(ts, "boom", 0.7)


@SS(175, 179, "Then, one night: moonlit town")
def s42(t0, t1):
    town_night(t0, t1, 64, 64)
    moon_ball("moon", (-30, 140, 54), 12)
    cam = Cam()
    cam.key(t0, (-6, -92, 3), (0, -50, 12), lens=24, fstop=9, focus=45.0)
    cam.key(t1, (8, -80, 8), (0, -50, 12), lens=24, fstop=9, focus=34.0)
    fin(cam, 1.0)
    sfx(t0, "crickets", 0.6)


@SS(179, 182, "I got really mad: Eddie fumes")
def s43(t0, t1):
    room(night=True)
    E = eddie_bed(t0, t1, "angry", (-2, 0), 0)
    E.act(t0, "fists", expr="furious")
    cam = mv("dutch", t0, t1, (-2, 0, 4.6), d=8, yaw=0, pitch=2, lens=32, fstop=3.0)
    cam.crash(w(181), 32, 44, 0.1)
    bump(cam, w(181), 0.4)
    fin(cam, 1.0)
    sfx(w(180), "stomp", 0.6)
    sfx(w(181), "buzzer", 0.5)


@SS(182, 190, "I wanted to go to the school dance: flyer + disco lights")
def s44(t0, t1):
    room(night=True)
    E = eddie_bed(t0, t1, "sleepy", (-2, 0), 0)
    E.act(t0, "think", expr="sleepy")
    fl = box("flyer", (2.6, 0.06, 3.4), (0.4, -3.6, 5.6), M("#fff5c8", 0.7), 0.02)
    text("fl_t", "SCHOOL\nDANCE", (0.4, -3.66, 5.9), 0.46, emitm("#ff4fa0", 2.0), extrude=0.01)
    for i, c in enumerate(("#ff4fa0", "#4fd0ff", "#ffe14a", "#7ee07a")):
        sphere(f"disco{i}", 0.35, (-2.6 + i * 1.8, -3.7, 8.4 - (i % 2) * 0.8), emitm(c, 4.0), seg=10)
    light("disco_l", "POINT", (0.4, -5, 7), 200, (1, 0.3, 0.7), 0.8)
    fl.rotation_euler[1] = math.radians(-6)
    fl.keyframe_insert("rotation_euler", index=1, frame=F(t0))
    fl.rotation_euler[1] = math.radians(6)
    fl.keyframe_insert("rotation_euler", index=1, frame=F(t1))
    cam = mv("slide", t0, t1, (-0.8, -1, 5.0), d=9, yaw=0, pitch=3, lens=30)
    fin(cam, 1.0)
    sfx(t0 + 0.2, "sparkle", 0.5)
    sfx(t0 + 1.2, "cheer", 0.3)


@SS(190, 195, "so I opened the window")
def s45(t0, t1):
    R = room(night=True)
    E = eddie_c(t0, t1, "determined")
    wx = R["wx"]
    E.pose(t0, loc=(wx, ROOM_BACK - 2.6, 0), rot=180)
    E.act(t0, "reach", expr="determined")
    open_window(R, w(192) + 0.1, 0.4)
    cam = Cam()
    cam.key(t0, (wx + 4.0, 1.5, 6.2), (wx, ROOM_BACK - 1.0, 6.2), lens=28, fstop=4.0, focus=9.0)
    cam.key(t1, (wx + 1.8, 3.8, 6.6), (wx, ROOM_BACK - 1.0, 6.6), lens=28, fstop=4.0, focus=6.0)
    fin(cam, 1.0)
    sfx(w(192) + 0.1, "window", 0.8)


@SS(195, 197, "and yelled: deep breath")
def s46(t0, t1):
    R = room(night=True)
    open_window(R, t0 - 1.0, 0.1)
    E = eddie_c(t0, t1, "determined")
    wx = R["wx"]
    E.pose(t0, loc=(wx, ROOM_BACK - 2.6, 0), rot=180)
    E.act(t0, "recoil", expr="determined")
    E.pose(t1 - 0.2, torso=(0, -14, 0), head=(0, -12, 0))
    cam = Cam()
    cam.key(t0, (wx + 1.0, 3.0, 6.0), (wx, ROOM_BACK - 2.6, 5.4), lens=26, fstop=3.0, focus=5.0)
    cam.key(t1, (wx + 0.5, 4.0, 5.6), (wx, ROOM_BACK - 2.6, 5.4), lens=30, fstop=3.0, focus=4.0)
    cam.crash(t1 - 0.25, 30, 44, 0.2)
    fin(cam, 1.0)
    sfx(t0 + 0.2, "gasp", 0.7)


@SS(197, 200, "WAKE UP, GRAMPA! shouted into the night")
def s47(t0, t1):
    R = room(night=True)
    open_window(R, t0 - 1.0, 0.1)
    E = eddie_c(t0, t1, "furious")
    wx = R["wx"]
    E.pose(t0, loc=(wx, ROOM_BACK - 2.6, 0), rot=180)
    E.face(t0, eyes="angry", mouth="scream")
    E.act(t0, "hands_face", expr="furious")
    pop_text("wu", "WAKE UP,\nGRAMPA!", (wx, 1.5, 9.0), t0 + 0.05, size=1.6, col="#ff5a4a")
    cam = Cam()
    cam.key(t0, (wx + 1.0, 4.0, 5.6), (wx, ROOM_BACK - 2.6, 5.4), lens=30, fstop=3.0, focus=4.0)
    cam.key(t1, (wx - 0.6, 3.0, 6.0), (wx, ROOM_BACK - 2.6, 5.6), lens=24, fstop=3.0, focus=5.0)
    cam.crash(t0, 30, 20, 0.12)
    bump(cam, t0 + 0.05, 0.8, 8)
    fin(cam, 1.2)
    sfx(t0, "boom", 0.6)
    sfx(t0 + 0.05, "wind", 0.6)


@SS(200, 204, "He opened one eye: extreme close-up")
def s48(t0, t1):
    room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    G.face(t0, eyes="closed", mouth="flat")
    G.face(t0 + 1.0, eyes="wink", mouth="flat")
    cam = Cam()
    cam.key(t0, (1.8, 6.2, 6.6), (0, 8.6, 3.2), lens=44, fstop=2.0, focus=4.5)
    cam.key(t1, (0.6, 7.0, 5.4), (0, 8.7, 3.3), lens=44, fstop=2.0, focus=2.4)
    cam.crash(t0 + 1.0, 44, 62, 0.15)
    bump(cam, t0 + 1.0, 0.3)
    fin(cam, 1.0)
    sfx(t0 + 1.0, "pop", 0.5)
    sfx(t0 + 1.0, "gasp", 0.5)


@SS(204, 205, "Silence.")
def s49(t0, t1):
    town_night(t0, t1, 64, 64)
    pop_text("sil", "...", (0, -75, 12), t0 + 0.05, size=5.0, col="#cfe8ff", dur=t1 - t0)
    cam = Cam()
    cam.key(t0, (0, -96, 4), (0, -50, 10), lens=24, fstop=9, focus=46.0)
    cam.key(t1, (0, -90, 4), (0, -50, 10), lens=24, fstop=9, focus=40.0)
    fin(cam, 0.5)
    sfx(t0, "crickets", 0.9)


@SS(205, 208, "Then, the sky: clouds tremble")
def s50(t0, t1):
    c = town_night(t0, t1, 64, 62)
    shake_obj(c, t0, t1, 0.35, 12.0)
    cam = Cam()
    cam.key(t0, (0, -86, 1.6), (0, -50, 30), lens=20, fstop=9, focus=50.0)
    cam.key(t1, (0, -84, 1.8), (0, -50, 36), lens=20, fstop=9, focus=50.0)
    bump(cam, t0 + 0.2, 0.3)
    fin(cam, 1.5)
    sfx(t0, "rise", 0.5)


@SS(208, 209, "creaked: the sky cracks, slow zoom")
def s51(t0, t1):
    c = town_night(t0, t1, 62, 56)
    shake_obj(c, t0, t1, 0.4, 14.0)
    for i in range(5):
        cr = box(f"crack{i}", (0.5, 0.5, 18), (-10 + i * 5, -48 + (i % 2) * 6, 52), M("#0c0c18", 0.5), 0.0,
                 rot=(0, 0, 0))
        cr.scale = (0.01, 1, 0.01)
        cr.keyframe_insert("scale", frame=F(t0 + 0.1 * i))
        cr.scale = (1, 1, 1)
        cr.keyframe_insert("scale", frame=F(t0 + 0.1 * i + 0.4))
        cr.rotation_euler = (math.radians(70), math.radians(i * 33), 0)
    pop_text("crk", "CREEEEAK...", (0, -72, 16), t0 + 0.1, size=3.0, col="#c8d4ff", dur=t1 - t0 - 0.1)
    cam = Cam()
    cam.key(t0, (0, -88, 2.0), (0, -50, 22), lens=20, fstop=9, focus=50.0)
    cam.key(t1, (0, -80, 2.4), (0, -52, 24), lens=34, fstop=9, focus=40.0)
    bump(cam, t0 + 0.5, 0.35)
    bump(cam, t0 + 1.3, 0.45)
    fin(cam, 1.4)
    sfx(t0, "zombie", 0.5)
    sfx(t0 + 0.9, "hammer", 0.3)


@SS(209, 213, "The clouds dropped lower")
def s52(t0, t1):
    town_night(t0, t1, 56, 34)
    for i, x in enumerate((-9, -3, 4, 10)):
        k = townie(i + 3, t0, t1, "scared")
        k.pose(t0, loc=(x, -74, 0), rot=0, armL=(40, 40), armR=(40, 40), head=(0, -30, 0))
    cam = Cam()
    cam.key(t0, (0, -86, 2.0), (0, -66, 26), lens=20, fstop=9, focus=40.0)
    cam.key(t1, (3, -82, 2.2), (0, -66, 18), lens=20, fstop=9, focus=30.0)
    cam.crash(t0 + 0.2, 20, 15, 0.3)
    bump(cam, t0 + 0.2, 0.5)
    fin(cam, 1.2)
    sfx(t0, "whoosh", 0.8)
    sfx(t0 + 0.1, "rise", 0.7)


@SS(213, 216, "A seagull bonked: seagull flies up")
def s53(t0, t1):
    town_night(t0, t1, 34, 34)
    g = seagull("gull", (-20, -62, 14), rot=-90)
    g.keyframe_insert("location", frame=F(t0))
    g.location = (4, -62, 26)
    g.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.key(t0, (-6, -92, 6), (-16, -62, 16), lens=28, fstop=5.0, focus=34.0)
    cam.key(t1, (6, -92, 10), (4, -62, 27), lens=28, fstop=5.0, focus=34.0)
    fin(cam, 1.2)
    sfx(t0, "whoosh", 0.5)
    sfx(t0 + 0.1, "quack", 0.6)


@SS(216, 222, "into the ceiling of the world: BONK")
def s54(t0, t1):
    town_night(t0, t1, 34, 34)
    g = seagull("gull", (4, -62, 26), rot=-90)
    g.keyframe_insert("location", frame=F(t0))
    g.keyframe_insert("rotation_euler", frame=F(t0))
    tb = t0 + 0.25
    g.location = (6, -62, 30.5)
    g.keyframe_insert("location", frame=F(tb))
    g.location = (12, -62, 2.0)
    g.rotation_euler = (math.radians(540), 0, math.radians(-90))
    g.keyframe_insert("location", frame=F(t1))
    g.keyframe_insert("rotation_euler", frame=F(t1))
    pop_text("bonk", "BONK!", (5, -66, 36), tb, size=3.6, col="#ffe14a")
    sparkle("stars", (6, -62, 31), tb, 2.5, n=12, seed=7)
    cam = Cam()
    cam.key(t0, (0, -88, 14), (5, -62, 28), lens=30, fstop=5.0, focus=30.0)
    cam.key(t1, (2, -86, 12), (8, -62, 20), lens=26, fstop=5.0, focus=26.0)
    cam.crash(tb, 30, 44, 0.1)
    bump(cam, tb, 0.8)
    fin(cam, 1.0)
    sfx(tb, "duck", 0.9)
    sfx(tb, "bonk", 0.9)


@SS(222, 225, "The moon started: big moon in a low sky")
def s55(t0, t1):
    town_night(t0, t1, 38, 38)
    m = moon_ball("moon", (20, 70, 22), 11)
    cam = Cam()
    cam.key(t0, (2, -88, 4), (20, 70, 22), lens=30, fstop=11, focus=150.0)
    cam.key(t1, (4, -80, 6), (22, 70, 22), lens=36, fstop=11, focus=150.0)
    fin(cam, 1.0)
    sfx(t0, "rise", 0.5)


@SS(225, 227, "sliding sideways: the moon slides across")
def s56(t0, t1):
    town_night(t0, t1, 38, 38)
    m = moon_ball("moon", (20, 70, 22), 11)
    m.keyframe_insert("location", frame=F(t0))
    m.location = (95, 70, 22)
    m.keyframe_insert("location", frame=F(t1))
    set_interp(m, "location", F(t0), "BEZIER", "EASE_IN")
    cam = Cam()
    cam.key(t0, (6, -84, 6), (30, 70, 22), lens=34, fstop=11, focus=150.0)
    cam.key(t1, (6, -84, 6), (70, 70, 22), lens=34, fstop=11, focus=150.0)
    fin(cam, 1.0)
    sfx(t0, "whoosh", 0.8)
    sfx(t0 + 0.2, "glitch", 0.4)


@SS(227, 232, "People screamed in the streets")
def s57(t0, t1):
    town_night(t0, t1, 30, 28)
    for i in range(9):
        k = townie(i + 30, t0, t1, "scream")
        x = -14 + i * 3.6
        k.run(t0, t1, (x, -70 - (i % 3) * 3, 0), (x + (-6 if i % 2 else 6), -62 - (i % 3) * 3, 0), rate=4.0)
        k.act(t0, "hands_head", expr="scream")
        k.panic(t0, t1, rate=6.0)
    cam = Cam()
    cam.push(t0, t1, (0, -66, 3.5), 24, 14, yaw=-10, pitch=6, yaw1=12, lens=26)
    bump(cam, t0 + 0.2, 0.2)
    fin(cam, 1.6)
    sfx(t0, "crowd", 0.9)
    sfx(t0 + 0.2, "gasp", 0.6)


@SS(232, 236, "A cow floated up")
def s58(t0, t1):
    town_night(t0, t1, 30, 30)
    c = cow("cow", (-4, -64, 0), rot=15, s=1.0)
    c.keyframe_insert("location", frame=F(t0))
    c.location = (-4, -64, 21)
    c.keyframe_insert("location", frame=F(t1))
    c.rotation_euler = (0, 0, math.radians(15))
    noise(c, "rotation_euler", 0, 0.25, 8)
    noise(c, "rotation_euler", 1, 0.3, 9)
    cam = Cam()
    cam.key(t0, (6, -86, 3), (-4, -64, 4), lens=26, fstop=5.0, focus=24.0)
    cam.key(t1, (6, -86, 4), (-4, -64, 20), lens=26, fstop=5.0, focus=24.0)
    fin(cam, 1.0)
    sfx(t0, "boing", 0.7)
    sfx(t0 + 0.4, "rise", 0.7)


@SS(236, 240, "and then slammed down: cow crash")
def s59(t0, t1):
    town_night(t0, t1, 30, 30)
    c = cow("cow", (-4, -64, 21), rot=15, s=1.0)
    c.keyframe_insert("location", frame=F(t0))
    c.keyframe_insert("rotation_euler", frame=F(t0))
    ts = t0 + 0.55
    c.location = (-4, -64, 0)
    c.keyframe_insert("location", frame=F(ts))
    set_interp(c, "location", F(t0), "BEZIER", "EASE_IN")
    c.rotation_euler = (math.radians(14), 0, math.radians(15))
    c.keyframe_insert("rotation_euler", frame=F(ts))
    W2.poof("dust", (-4, -64, 1.5), ts, 2.5)
    pop_text("slam", "SLAM!", (-4, -68, 12), ts, size=3.6, col="#ff5a4a")
    cam = Cam()
    cam.key(t0, (4, -88, 12), (-4, -64, 12), lens=26, fstop=5.0, focus=26.0)
    cam.key(t1, (3, -84, 6), (-4, -64, 3), lens=28, fstop=5.0, focus=22.0)
    cam.crash(ts, 28, 40, 0.1)
    bump(cam, ts, 1.0, 9)
    fin(cam, 1.0)
    sfx(t0, "whoosh", 0.8)
    sfx(ts, "thud", 1.0)
    sfx(ts, "slap", 0.8)


@SS(240, 245, "Grandpa, go back to sleep!")
def s60(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "gasp")
    E = eddie_bed(t0, t1, "panic", (-4.4, 2.2), -60)
    E.face(t0, eyes="terror", mouth="scream")
    E.act(t0, "hands_head", expr="panic")
    E.panic(t0, t1, rate=5.0)
    lips(E, t0, t1, "shout")
    cam = mv("dutch", t0, t1, (-1.6, 4.0, 4.6), d=11, yaw=-18, pitch=6, lens=26, fstop=4.0)
    bump(cam, t0 + 0.1, 0.3)
    fin(cam, 1.8)
    sfx(t0, "gasp", 0.5)


@SS(245, 247, "Can't, kiddo.")
def s61(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "sus")
    G.act(t0, "shrug", expr="sus")
    lips(G, t0, t1)
    cam = mv("in", t0, t1, (0, 7.6, 4.6), d=8, yaw=0, pitch=2, lens=34, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0, "faaah", 0.7)


@SS(247, 251, "I'm wide awake now")
def s62(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "gasp")
    G.face(t0, eyes="wide", mouth="talk")
    lips(G, t0, t1)
    cam = mv("orb", t0, t1, (0, 7.6, 4.8), d=5.5, yaw=0, pitch=4, lens=34, fstop=2.6)
    cam.crash(w(248), 34, 46, 0.12)
    fin(cam, 1.0)
    sfx(w(248), "pop", 0.5)


@SS(251, 255, "He tried to snore: inhales, puffs up")
def s63(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "neutral")
    G.face(t0 + 0.2, eyes="closed", mouth="o")
    G.face(t0 + 0.9, eyes="squint", mouth="grimace_wide")
    G.pose(t0 + 0.9, torso=(0, -10, 0))
    cam = mv("in", t0, t1, (0, 7.6, 4.6), d=7, yaw=6, pitch=2, lens=34, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0 + 0.1, "gasp", 0.6)
    sfx(t0 + 0.9, "rise", 0.5)


@SS(255, 257, "Nothing.")
def s64(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "worried")
    pop_text("nth", "...", (0, 0, 7.8), t0 + 0.1, size=3.5, col="#cfe8ff", dur=t1 - t0)
    cam = Cam()
    cam.key(t0, (0, -3.0, 5.0), (0, 7.6, 4.4), lens=30, fstop=3.0, focus=11.0)
    cam.key(t1, (0, -1.5, 5.0), (0, 7.6, 4.4), lens=30, fstop=3.0, focus=9.5)
    fin(cam, 0.6)
    sfx(t0, "crickets", 0.8)


@SS(257, 260, "Only a tiny whistle")
def s65(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "worried")
    G.face(t0 + 0.4, eyes="squint", mouth="o")
    tw = t0 + 0.5
    pop_text("wh", "fffft", (0.5, 4.2, 6.6), tw, size=0.6, col="#ffffff", dur=1.2)
    cam = Cam()
    cam.key(t0, (0.8, 1.6, 6.0), (0, 7.8, 4.6), lens=40, fstop=2.2, focus=6.2)
    cam.key(t1, (0.3, 3.8, 5.4), (0, 7.8, 4.7), lens=40, fstop=2.2, focus=4.0)
    cam.crash(tw, 40, 52, 0.2)
    fin(cam, 1.0)
    sfx(tw, "dry_fart", 0.7)


@SS(260, 264, "The sky was now as: clouds nearly touching")
def s66(t0, t1):
    town_night(t0, t1, 30, 24)
    cam = Cam()
    cam.key(t0, (0, -92, 2.0), (0, -50, 12), lens=22, fstop=9, focus=50.0)
    cam.key(t1, (3, -84, 2.2), (0, -50, 11), lens=22, fstop=9, focus=40.0)
    bump(cam, t0 + 0.2, 0.3)
    fin(cam, 1.2)
    sfx(t0, "rise", 0.7)


@SS(264, 269, "low as the rooftops: clouds scrape the roofs")
def s67(t0, t1):
    town_night(t0, t1, 24, 23)
    cam = Cam()
    cam.key(t0, (-14, -80, 5.0), (0, -50, 11), lens=28, fstop=7.0, focus=30.0)
    cam.key(t1, (10, -80, 5.4), (0, -50, 11), lens=28, fstop=7.0, focus=30.0)
    bump(cam, t0 + 0.3, 0.3)
    fin(cam, 1.3)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 0.2, "thud", 0.6)


@SS(269, 273, "Everyone had to crawl")
def s68(t0, t1):
    town_night(t0, t1, 23, 23)
    for i in range(6):
        k = townie(i + 40, t0, t1, "scared")
        x0 = -16 + i * 5
        crawl_pose(k, t0, (x0, -68 - (i % 2) * 3, 0), 20)
        crawl_pose(k, t1, (x0 + 10, -68 - (i % 2) * 3, 0), 20)
        k.pose(t0, rot=-70)
    cam = Cam()
    cam.push(t0, t1, (0, -68, 2.0), 16, 11, yaw=-10, pitch=3, yaw1=15, lens=28)
    fin(cam, 1.3)
    sfx(t0, "footsteps", 0.6)


def spring(name, loc, t0=None, h=8.0, turns=5, r=1.6):
    """Coil spring made of beads; returns root (scale z to squash/stretch)."""
    root = empty(name, loc)
    Mg = M("#c9ced8", 0.3, metal=0.9)
    n = turns * 10
    for i in range(n):
        a = i / 10 * math.tau
        sphere(f"{name}_b{i}", 0.32, (math.cos(a) * r, math.sin(a) * r, i / n * h), Mg, parent=root, seg=8)
    return root


def eddie_roof(t0, t1, expr="determined"):
    return eddie_c(t0, t1, expr)


@SS(273, 277, "Then, I noticed something: lightbulb")
def s69(t0, t1):
    town_night(t0, t1, 23, 23)
    E = eddie_c(t0, t1, "worried")
    E.pose(t0, loc=(0, -70, 0), rot=0, hipz=-0.8, torso=(0, 25, 0))
    E.face(w(275), "lookup")
    pop_text("idea", "!", (1.8, -71.2, 6.4), w(275), size=3.6, col="#ffe14a")
    sparkle("ids", (1.8, -71.2, 6.8), w(275), 1.6, seed=9)
    cam = mv("in", t0, t1, (0, -70, 3.6), d=9, yaw=-6, pitch=4, lens=32, fstop=2.8)
    cam.crash(w(275), 32, 44, 0.12)
    fin(cam, 1.0)
    sfx(w(275), "correct", 0.8)


@SS(277, 281, "Grandpa couldn't sleep: tossing in bed")
def s70(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "neutral")
    G.face(t0, eyes="wide", mouth="frown")
    G.pose(t0, head=(-18, 0, -6))
    G.pose(t0 + 1.0, head=(20, 0, 6))
    G.pose(t1 - 0.1, head=(-12, 0, -4))
    cam = mv("orbr", t0, t1, (0, 7.6, 4.6), d=8.5, yaw=10, pitch=6, lens=30, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0, "wind", 0.3)


@SS(281, 286, "too quiet: empty room, tick tock")
def s71(t0, t1):
    room(night=True, lamp=False, bright=0.6)
    G = grandpa_sitting(t0, t1, "bored")
    clock("clk2", (-0.5, -2.0, 3.0), t0, t1, r=1.0, turns=5.0)
    for i in range(4):
        pop_text(f"tk{i}", "TICK" if i % 2 == 0 else "TOCK", (-5 + i * 3.4, -3.0, 9.0 - (i % 2)), t0 + 0.3 + i * 0.6,
                 size=1.0, col="#cfe8ff", dur=0.9)
        sfx(t0 + 0.3 + i * 0.6, "click", 0.5)
    cam = Cam()
    cam.key(t0, (0, -9, 6.0), (0, 6, 4.0), lens=22, fstop=6.0, focus=15.0)
    cam.key(t1, (0, -5.5, 5.6), (0, 7, 4.0), lens=26, fstop=6.0, focus=12.0)
    fin(cam, 0.7)
    sfx(t0, "crickets", 0.5)


@SS(286, 292, "for the first time in: clock spins")
def s72(t0, t1):
    room(night=True, lamp=False, bright=0.6)
    clock("clk3", (0, 3.0, 6.4), t0, t1, r=2.6, turns=10.0)
    cam = Cam()
    cam.key(t0, (-2, -3.0, 6.0), (0, 3.0, 6.4), lens=34, fstop=2.4, focus=6.5)
    cam.key(t1, (1, -0.5, 6.6), (0, 3.0, 6.4), lens=34, fstop=2.4, focus=3.6)
    fin(cam, 0.8)
    sfx(t0, "rise", 0.6)
    sfx(t0 + 0.3, "click", 0.5)


@SS(292, 294, "60 years: big number")
def s73(t0, t1):
    room(night=True, lamp=False, bright=0.6)
    pop_text("sx", "60 YEARS", (0, 0, 7.4), t0 + 0.05, size=2.4, col="#ffe14a")
    sparkle("sxs", (0, 0, 7.6), t0 + 0.05, 3.0, n=14, seed=2)
    cam = Cam()
    cam.key(t0, (0, -6.5, 7.0), (0, 0, 7.4), lens=28, fstop=6.0, focus=6.5)
    cam.key(t1, (0, -4.6, 7.2), (0, 0, 7.4), lens=28, fstop=6.0, focus=4.6)
    cam.crash(t0 + 0.05, 28, 38, 0.1)
    bump(cam, t0 + 0.05, 0.4)
    fin(cam, 1.0)
    sfx(t0 + 0.05, "boom", 0.7)
    sfx(t0 + 0.05, "ding", 0.6)


@SS(294, 300, "nobody was reading him the manual: empty chair")
def s74(t0, t1):
    room(night=True, lamp=False, bright=0.5)
    book("lonely", (8.0, 1.2, 3.1), rot=(0, 0, 20), s=1.2)
    pop_text("qm", "?", (8.0, 0.6, 7.5), t0 + 0.4, size=3.0, col="#9bb8ff", dur=t1 - t0 - 0.4)
    cam = Cam()
    cam.key(t0, (2.5, -6.0, 4.6), (8.0, 1.8, 3.4), lens=30, fstop=2.8, focus=11.0)
    cam.key(t1, (5.5, -2.0, 4.8), (8.0, 1.8, 3.4), lens=30, fstop=2.8, focus=6.0)
    cam.crash(t0 + 0.4, 30, 38, 0.15)
    fin(cam, 0.9)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.4, "pop", 0.4)


@SS(300, 305, "I grabbed the vacuum manual")
def s75(t0, t1):
    room(night=True)
    b = book("bk", (5.0, 2.2, 3.3), rot=(0, 0, 10), s=1.3)
    E = eddie_c(t0, t1, "determined")
    E.pose(t0, loc=(1.0, 0.0, 0), rot=-70)
    E.run(t0, t0 + 0.55, (1.0, 0.0, 0), (6.4, 0.6, 0), rate=3.6)
    E.pose(t0 + 0.55, rot=-20)
    E.act(t0 + 0.55, "reach", expr="determined")
    tg = t0 + 0.7
    b.keyframe_insert("location", frame=F(t0))
    b.keyframe_insert("location", frame=F(tg))
    b.location = (5.6, 0.2, 5.0)
    b.rotation_euler = (math.radians(-20), 0, math.radians(-20))
    b.keyframe_insert("location", frame=F(tg + 0.3))
    b.keyframe_insert("rotation_euler", frame=F(tg + 0.3))
    E.act(tg + 0.3, "cheer", expr="grin")
    cam = Cam()
    cam.key(t0, (-1.0, -5.0, 4.6), (4.0, 1.0, 4.0), lens=28, fstop=4.0, focus=7.0)
    cam.key(t1, (5.0, -3.0, 5.4), (5.6, 0.6, 5.0), lens=34, fstop=3.0, focus=3.6)
    cam.crash(tg, 28, 40, 0.1)
    bump(cam, tg, 0.4)
    fin(cam, 1.2)
    sfx(t0, "footsteps", 0.6)
    sfx(tg, "paper", 0.8)
    sfx(tg + 0.1, "whoosh", 0.5)


@SS(305, 310, "I ran to the roof: Eddie sprints up the roof")
def s76(t0, t1):
    town_night(t0, t1, 30, 30, lit=True)
    E = eddie_c(t0, t1, "determined")
    r0, r1 = (-9.0, -48.0, 9.2), (-3.6, -48.0, 11.6)
    E.pose(t0, loc=r0, rot=facing(r0, r1))
    E.run(t0, t1 - 0.2, r0, r1, rate=4.0)
    cam = Cam()
    cam.track(E, t0, t1, offset=(2, -14, 1.5), look_up=3.0, lens=28, step=0.25, fstop=6.0)
    fin(cam, 1.3)
    sfx(t0, "footsteps", 0.8)
    sfx(t0 + 0.1, "whoosh", 0.5)


@SS(310, 314, "climbed up the antenna")
def s77(t0, t1):
    town_night(t0, t1, 30, 30, lit=True)
    E = eddie_c(t0, t1, "determined")
    E.pose(t0, loc=(-3.5, -46.0, 11.6), rot=0, armL=(170, 8), armR=(170, 8))
    E.pose(t0 + 0.9, loc=(-3.5, -46.0, 12.8), legL=(30, 4), legR=(-20, -4))
    E.pose(t1, loc=(-3.5, -46.0, 14.0), legL=(-20, 4), legR=(30, -4))
    cam = Cam()
    cam.key(t0, (-9, -58, 9.5), (-3.5, -46, 12.4), lens=28, fstop=4.0, focus=14.0)
    cam.key(t1, (-6, -54, 13.2), (-3.5, -46, 15.2), lens=28, fstop=4.0, focus=9.0)
    fin(cam, 1.2)
    sfx(t0, "rope", 0.6)
    sfx(t0 + 0.8, "clink", 0.5)


@SS(314, 319, "and shouted into the sky")
def s78(t0, t1):
    town_night(t0, t1, 30, 30, lit=True)
    E = eddie_c(t0, t1, "scream")
    E.pose(t0, loc=(-3.5, -46.0, 14.0), rot=0, armL=(170, 8), armR=(170, 8), legL=(-20, 4), legR=(30, -4))
    E.face(t0, eyes="angry", mouth="scream")
    lips(E, t0, t1, "shout")
    cam = mv("fall", t0, t1, (-3.5, -46, 17.0), d=14, yaw=-12, pitch=6, lens=26, fstop=4.0)
    fin(cam, 1.2)
    sfx(t0, "wind", 0.7)


@SS(319, 321, "CHAPTER ONE!")
def s79(t0, t1):
    town_night(t0, t1, 30, 30, lit=True)
    E = eddie_c(t0, t1, "scream")
    E.pose(t0, loc=(-3.5, -46.0, 14.0), rot=0, armL=(170, 8), armR=(170, 8), legL=(-20, 4), legR=(30, -4))
    E.face(t0, eyes="angry", mouth="scream")
    pop_text("ch1", "CHAPTER\nONE!", (-3.5, -58, 22), t0 + 0.05, size=3.4, col="#ffe14a")
    cam = Cam()
    cam.key(t0, (-3.5, -66, 12.0), (-3.5, -46, 17.0), lens=26, fstop=6.0, focus=20.0)
    cam.key(t1, (-3.5, -63, 14.0), (-3.5, -46, 18.0), lens=24, fstop=6.0, focus=17.0)
    cam.crash(t0 + 0.05, 26, 34, 0.1)
    bump(cam, t0 + 0.05, 0.8, 8)
    fin(cam, 1.0)
    sfx(t0 + 0.05, "boom", 0.7)
    sfx(t0 + 0.05, "wind", 0.5)


@SS(321, 326, "HOW TO ATTACH THE HOES!")
def s80(t0, t1):
    town_night(t0, t1, 30, 30, lit=True)
    E = eddie_c(t0, t1, "scream")
    E.pose(t0, loc=(-3.5, -46.0, 14.0), rot=0, armL=(170, 8), armR=(170, 8), legL=(-20, 4), legR=(30, -4))
    E.face(t0, eyes="angry", mouth="scream")
    pop_text("ch2", "HOW TO ATTACH\nTHE HOES!", (-3.5, -58, 22), t0 + 0.1, size=2.6, col="#ff9a3c")
    cam = Cam()
    cam.key(t0, (-12, -66, 15.0), (-3.5, -46, 17.0), lens=26, fstop=6.0, focus=22.0)
    cam.key(t1, (6, -64, 16.0), (-3.5, -46, 17.5), lens=26, fstop=6.0, focus=20.0)
    bump(cam, t0 + 0.1, 0.5)
    fin(cam, 1.0)
    sfx(t0 + 0.1, "boom", 0.6)


@SS(326, 330, "His eyes got heavy")
def s81(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "yawn")
    G.face(t0, eyes="wide", mouth="flat")
    G.face(t0 + 0.6, eyes="half", mouth="flat")
    G.face(t0 + 1.2, eyes="closed", mouth="yawn")
    cam = Cam()
    cam.key(t0, (0.5, 2.5, 5.8), (0, 7.6, 5.0), lens=44, fstop=2.2, focus=5.6)
    cam.key(t1, (0.2, 3.5, 5.4), (0, 7.6, 5.0), lens=44, fstop=2.2, focus=4.4)
    fin(cam, 0.9)
    sfx(t0 + 1.2, "aww", 0.4)


@SS(330, 332, "Hoes. Attachments.: grandpa nods off")
def s82(t0, t1):
    room(night=True)
    G = grandpa_sitting(t0, t1, "sleepy")
    G.pose(t0, head=(0, 0, 0))
    G.pose(t0 + 0.5, head=(0, 16, 0))
    G.pose(t0 + 0.9, head=(0, 2, 0))
    G.pose(t1 - 0.1, head=(0, 22, 0))
    G.face(t0, eyes="half", mouth="wavy")
    G.face(t0 + 1.2, eyes="closed", mouth="smile")
    zzz((1.2, 7.0, 5.6), t0 + 0.3, t1, n=3, size=1.0)
    cam = mv("orb", t0, t1, (0, 7.6, 5.0), d=7, yaw=0, pitch=4, lens=34, fstop=2.6)
    fin(cam, 0.9)
    sfx(t0 + 0.5, "snort", 0.4)


@SS(332, 336, "I kept reading louder: Eddie on the antenna with the book")
def s83(t0, t1):
    town_night(t0, t1, 30, 30, lit=True)
    E = eddie_c(t0, t1, "scream")
    E.pose(t0, loc=(-3.5, -46.0, 14.0), rot=0, legL=(-20, 4), legR=(30, -4), armL=(90, 20), armR=(90, 20))
    hold_book(E, "R")
    E.face(t0, eyes="angry", mouth="scream")
    lips(E, t0, t1, "shout")
    cam = mv("in", t0, t1, (-3.5, -46, 16.4), d=14, yaw=-18, pitch=4, lens=26, fstop=4.0)
    cam.crash(w(334), 26, 36, 0.12)
    bump(cam, w(334), 0.3)
    fin(cam, 1.2)
    sfx(w(334), "whoosh", 0.4)


def crowd_book(ids, y, t0, t1, x0=-20, step=3.8, rows=1, expr="scream"):
    out = []
    for r in range(rows):
        for i, kid_i in enumerate(ids):
            k = townie(kid_i, t0, t1, expr)
            x = x0 + i * step + (r % 2) * 1.6
            k.pose(t0, loc=(x, y - r * 4.0, 0), rot=random.uniform(-14, 14))
            b = book(f"cb{kid_i}{r}", (0, 0, 0), s=0.8)
            locs.hand_prop(k, "R", b, offset=(0, -0.8, -1.9), rot=(0, 0, 0))
            k.act(t0 + random.uniform(0, 0.3), "hold", expr=expr)
            lips(k, t0, t1, "shout")
            out.append(k)
    return out


@SS(336, 341, "The whole town joined in: townsfolk run to the street")
def s84(t0, t1):
    town_night(t0, t1, 30, 30)
    ks = []
    for i in range(10):
        k = townie(i + 50, t0, t1, "happy")
        x = -22 + i * 4.8
        k.run(t0, t1 - 0.6, (x + (14 if i % 2 else -14), -64 - (i % 3) * 3, 0), (x, -66 - (i % 3) * 3, 0), rate=3.4)
        b = book(f"rb{i}", (0, 0, 0), s=0.8)
        locs.hand_prop(k, "R", b, offset=(0, -0.8, -1.9))
        k.act(t1 - 0.6, "hold", expr="joy")
    cam = Cam()
    cam.push(t0, t1, (0, -66, 3.0), 30, 18, yaw=-25, pitch=18, yaw1=18, lens=26)
    fin(cam, 1.2)
    sfx(t0, "crowd", 0.9)
    sfx(t0 + 0.3, "footsteps", 0.6)


@SS(341, 345, "Every single person reading: crowd low angle")
def s85(t0, t1):
    town_night(t0, t1, 30, 30)
    crowd_book([60, 61, 62, 63, 64, 65], -68, t0, t1, x0=-9.5, step=3.8, rows=2)
    cam = Cam()
    cam.key(t0, (-16, -84, 1.4), (0, -66, 5.0), lens=24, fstop=5.0, focus=20.0)
    cam.key(t1, (12, -82, 1.8), (0, -66, 5.0), lens=24, fstop=5.0, focus=18.0)
    fin(cam, 1.2)
    sfx(t0, "chat", 0.8)


@SS(345, 349, "the vacuum manual together: pull-out over the crowd")
def s86(t0, t1):
    town_night(t0, t1, 30, 30)
    crowd_book([70, 71, 72, 73, 74, 75, 76], -68, t0, t1, x0=-12, step=4.0, rows=2)
    cam = Cam()
    cam.push(t0, t1, (0, -66, 4.0), 12, 30, yaw=0, pitch=22, pitch1=34, lens=26)
    fin(cam, 1.0)
    sfx(t0, "crowd", 0.7)
    sfx(t0 + 1.0, "chat", 0.6)


@SS(349, 354, "The mayor read the warranty")
def s87(t0, t1):
    town_night(t0, t1, 30, 30, house=False)
    My = mayor_c(t0, t1, "smile")
    My.pose(t0, loc=(0, -68, 0), rot=6)
    My.act(t0, "hold", expr="smile")
    pp = box("warr", (1.7, 0.05, 2.1), (0, 0, 0), M("#fffdf2", 0.8), 0.02)
    locs.hand_prop(My, "R", pp, offset=(0, -0.9, -1.4))
    pp.parent = My.shR
    text("warr_t", "WARRANTY", (0, -0.05, 0.1), 0.22, M("#1a1a22", 0.5), parent=pp, extrude=0.005)
    lips(My, t0, t1)
    cam = mv("in", t0, t1, (0, -68, 4.6), d=11, yaw=-12, pitch=3, lens=32, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0, "paper", 0.6)


@SS(354, 358, "The baker read the: baker with a booklet")
def s88(t0, t1):
    town_night(t0, t1, 30, 30, house=False)
    B = baker_c(t0, t1, "smile")
    B.pose(t0, loc=(0, -68, 0), rot=-6)
    B.act(t0, "hold", expr="smile")
    pp = box("tsb", (1.7, 0.1, 2.1), (0, 0, 0), M("#e8423a", 0.6), 0.02)
    locs.hand_prop(B, "R", pp, offset=(0, -0.9, -1.4))
    lips(B, t0, t1)
    cam = mv("orb", t0, t1, (0, -68, 4.8), d=10, yaw=14, pitch=4, lens=30, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0, "paper", 0.5)


@SS(358, 359, "troubleshooting.: baker, giant word")
def s89(t0, t1):
    town_night(t0, t1, 30, 30, house=False)
    B = baker_c(t0, t1, "sleepy")
    B.pose(t0, loc=(0, -68, 0), rot=0)
    B.face(t0 + 0.4, eyes="half", mouth="yawn")
    pop_text("tr", "TROUBLE-\nSHOOTING", (0, -72, 8.5), t0 + 0.05, size=1.7, col="#ffffff", dur=t1 - t0)
    cam = Cam()
    cam.key(t0, (0, -78, 5.0), (0, -68, 5.0), lens=34, fstop=3.0, focus=10.0)
    cam.key(t1, (0, -76, 5.2), (0, -68, 5.0), lens=40, fstop=3.0, focus=8.0)
    fin(cam, 1.0)
    sfx(t0 + 0.4, "aww", 0.4)


@SS(359, 362, "Zzzzzzz... HONG SHU! the sky is about to leap")
def s90(t0, t1):
    R = room(night=True)
    G = grandpa(t0, t1)
    lie_in_bed(G, t0)
    G.face(t0, eyes="closed", mouth="smile")
    th = w(360)
    G.face(th, eyes="closed", mouth="ah")
    zzz((0.8, 8.0, 5.0), t0 + 0.05, th, n=3, size=1.2)
    pop_text("hs", "HONG\nSHU!", (0, 0.5, 8.8), th, size=2.8, col="#ffe14a")
    cam = Cam()
    cam.key(t0, (0, 0.5, 8.0), (0, 8.2, 3.6), lens=36, fstop=3.0, focus=8.0)
    cam.key(t1, (0, -3.0, 7.0), (0, 6.0, 4.0), lens=24, fstop=5.0, focus=10.0)
    cam.crash(th, 36, 28, 0.1)
    bump(cam, th, 0.9, 8)
    fin(cam, 1.0)
    sfx(th, "snort", 1.0)
    sfx(th, "capcut_boom", 0.8)


@SS(362, 367, "The sky shot back up: clouds rocket away")
def s91(t0, t1):
    town_night(t0, t1, 14, 66, ) if False else None
    W.sky(0.7, top=(0.02, 0.04, 0.2), bottom=(0.1, 0.16, 0.42))
    light("nsun", "SUN", (0, 0, 50), 2.4, (0.6, 0.7, 1.0), 2, rot=(50, 0, 30))
    town_ground()
    blue_house(lit=True)
    ceiling(t0, t1, 26, 70, extra=[(t0 + 0.6, 50), (t0 + 1.0, 74)])
    for i, x in enumerate((-8, -2, 5, 11)):
        k = townie(i + 80, t0, t1, "joy")
        k.pose(t0, loc=(x, -70, 0), rot=0)
        k.act(t0 + 0.5, "cheer", expr="joy")
    cam = Cam()
    cam.key(t0, (0, -84, 1.6), (0, -60, 20), lens=20, fstop=9, focus=40.0)
    cam.key(t1, (2, -82, 1.8), (0, -60, 60), lens=20, fstop=9, focus=60.0)
    cam.crash(t0 + 0.2, 20, 28, 0.4)
    bump(cam, t0 + 0.2, 0.5, 8)
    fin(cam, 1.2)
    sfx(t0, "rocket", 0.8)
    sfx(t0 + 0.05, "whoosh", 0.9)
    sfx(t0 + 0.9, "boing", 0.6)


@SS(367, 370, "like a spring: giant spring pushes the sky")
def s92(t0, t1):
    W.sky(0.7, top=(0.02, 0.04, 0.2), bottom=(0.1, 0.16, 0.42))
    light("nsun", "SUN", (0, 0, 50), 2.4, (0.6, 0.7, 1.0), 2, rot=(50, 0, 30))
    town_ground()
    blue_house(lit=True)
    c = ceiling(t0, t1, 62, 62, extra=[(t0 + 0.25, 70), (t0 + 0.55, 58), (t0 + 0.85, 66)])
    sp = spring("spr", (-3.5, -48, 12.0), h=8.0)
    sp.scale = (1, 1, 1)
    for t, s in ((t0, 1.0), (t0 + 0.25, 3.2), (t0 + 0.55, 0.8), (t0 + 0.85, 2.0), (t1, 1.6)):
        sp.scale = (1, 1, s)
        sp.keyframe_insert("scale", frame=F(t))
    pop_text("bng", "BOING!", (6, -66, 30), t0 + 0.2, size=3.4, col="#7ee07a")
    cam = Cam()
    cam.key(t0, (-6, -80, 3), (0, -48, 22), lens=22, fstop=9, focus=40.0)
    cam.key(t1, (4, -76, 6), (0, -48, 30), lens=22, fstop=9, focus=40.0)
    bump(cam, t0 + 0.25, 0.5)
    fin(cam, 1.0)
    sfx(t0 + 0.2, "boing", 1.0)
    sfx(t0 + 0.55, "boing", 0.7)


@SS(370, 374, "The moon slid home")
def s93(t0, t1):
    town_night(t0, t1, 62, 62)
    m = moon_ball("moon", (95, 140, 54), 12)
    m.keyframe_insert("location", frame=F(t0))
    m.location = (-30, 140, 54)
    m.keyframe_insert("location", frame=F(t1 - 0.2))
    set_interp(m, "location", F(t0), "BEZIER", "EASE_OUT")
    cam = Cam()
    cam.key(t0, (4, -90, 3), (60, 140, 54), lens=26, fstop=11, focus=160.0)
    cam.key(t1, (4, -90, 5), (-20, 140, 54), lens=26, fstop=11, focus=160.0)
    fin(cam, 1.0)
    sfx(t0, "whoosh", 0.8)
    sfx(t1 - 0.3, "thud", 0.5)


@SS(374, 378, "The cow landed gently: floating down")
def s94(t0, t1):
    town_night(t0, t1, 62, 62)
    haystack("hay", (-6, -64, 0), 1.2)
    c = cow("cow", (-6, -64, 26), rot=15)
    c.keyframe_insert("location", frame=F(t0))
    c.location = (-6, -64, 9)
    c.keyframe_insert("location", frame=F(t1))
    noise(c, "rotation_euler", 0, 0.12, 8)
    cam = Cam()
    cam.key(t0, (6, -88, 12), (-6, -64, 22), lens=28, fstop=5.0, focus=26.0)
    cam.key(t1, (4, -84, 8), (-6, -64, 9), lens=28, fstop=5.0, focus=22.0)
    fin(cam, 1.0)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.4, "aww", 0.5)


@SS(378, 381, "in a haystack: soft landing, hay puffs")
def s95(t0, t1):
    town_night(t0, t1, 62, 62)
    haystack("hay", (-6, -64, 0), 1.2)
    c = cow("cow", (-6, -64, 9), rot=15)
    c.keyframe_insert("location", frame=F(t0))
    tl = t0 + 0.45
    c.location = (-6, -64, 3.4)
    c.keyframe_insert("location", frame=F(tl))
    set_interp(c, "location", F(t0), "BEZIER", "EASE_OUT")
    W2.poof("hp", (-6, -64, 4.0), tl, 2.2, seed=3)
    pop_text("mu", "moo~", (-6, -72, 10), tl + 0.2, size=2.4, col="#ffffff", dur=1.2)
    cam = Cam()
    cam.key(t0, (6, -86, 8), (-6, -64, 6), lens=30, fstop=4.0, focus=24.0)
    cam.key(t1, (2, -80, 6), (-6, -64, 4), lens=34, fstop=4.0, focus=18.0)
    bump(cam, tl, 0.3)
    fin(cam, 1.0)
    sfx(tl, "poof", 0.8)
    sfx(tl + 0.2, "aww", 0.5)


@SS(381, 384, "The next day: sunrise over the town")
def s96(t0, t1):
    W.sky(1.0, top=(0.28, 0.5, 0.95), bottom=(1.0, 0.8, 0.55))
    W.sun(4.5, rot=(70, 0, 40))
    town_ground()
    blue_house(lit=False)
    ceiling(t0, t1, 64, 64, seed=3)
    cam = Cam()
    cam.key(t0, (14, -90, 2.2), (0, -48, 8), lens=24, fstop=8, focus=46.0)
    cam.key(t1, (6, -72, 6.0), (0, -48, 8), lens=24, fstop=8, focus=26.0)
    fin(cam, 1.0)
    sfx(t0, "sparkle", 0.5)
    sfx(t0 + 0.2, "pigeon", 0.4)


@SS(384, 389, "I made grandpa a promise: Eddie by the bed")
def s97(t0, t1):
    room(night=False)
    G = grandpa_sitting(t0, t1, "smile")
    E = eddie_bed(t0, t1, "smile", (-4.6, 3.4), -55)
    E.act(t0, "lean", expr="smile")
    lips(E, t0, t1)
    cam = mv("orb", t0, t1, (-2.0, 5.5, 4.2), d=10, yaw=-12, pitch=6, lens=28, fstop=4.0)
    fin(cam, 1.0)
    sfx(t0, "chat", 0.3)


@SS(389, 395, "I'll read to you every night: manual held high")
def s98(t0, t1):
    room(night=False)
    G = grandpa_sitting(t0, t1, "happy")
    E = eddie_bed(t0, t1, "grin", (-4.6, 3.4), -55)
    E.act(t0, "cheer", expr="grin")
    hold_book(E, "R")
    sparkle("pm", (-4.6, 2.4, 7.5), t0 + 0.5, 2.0, seed=3)
    cam = mv("rise", t0, t1, (-4.6, 3.4, 5.0), d=10, yaw=-20, pitch=4, lens=28, fstop=4.0)
    fin(cam, 1.0)
    sfx(t0 + 0.5, "sparkle", 0.6)
    sfx(t0 + 0.5, "correct", 0.6)


@SS(395, 400, "And I'll skip the dance: flyer crumples")
def s99(t0, t1):
    room(night=False)
    E = eddie_bed(t0, t1, "smile", (-2, 1), 0)
    E.act(t0, "hold", expr="smile")
    fl = box("flyer", (2.4, 0.06, 3.1), (0.2, -2.4, 5.4), M("#fff5c8", 0.7), 0.02)
    text("fl_t", "SCHOOL\nDANCE", (0.2, -2.46, 5.7), 0.42, emitm("#ff4fa0", 2.0), extrude=0.01)
    tc = w(397)
    for ob in list(bpy.data.objects):
        if ob.name in ("flyer", "fl_t"):
            ob.scale = (1, 1, 1)
            ob.keyframe_insert("scale", frame=F(tc))
            ob.keyframe_insert("rotation_euler", frame=F(tc))
            ob.scale = (0.2, 0.2, 0.2) if ob.name == "flyer" else (0.01, 0.01, 0.01)
            ob.rotation_euler = (math.radians(200), math.radians(140), 0)
            ob.keyframe_insert("scale", frame=F(tc + 0.4))
            ob.keyframe_insert("rotation_euler", frame=F(tc + 0.4))
    cam = mv("in", t0, t1, (0, -2, 5.0), d=9, yaw=0, pitch=4, lens=30, fstop=3.0)
    fin(cam, 1.0)
    sfx(tc, "paper", 0.9)
    sfx(tc + 0.1, "pop", 0.5)


@SS(400, 402, "He winked")
def s100(t0, t1):
    room(night=False)
    G = grandpa_sitting(t0, t1, "smile")
    G.face(t0 + 0.25, eyes="wink", mouth="smirk")
    sparkle("wk", (0.9, 6.0, 5.6), t0 + 0.3, 1.2, seed=11)
    cam = Cam()
    cam.key(t0, (0.4, 2.4, 5.6), (0, 7.6, 5.0), lens=46, fstop=2.2, focus=5.5)
    cam.key(t1, (0.2, 3.4, 5.4), (0, 7.6, 5.0), lens=46, fstop=2.2, focus=4.5)
    cam.crash(t0 + 0.25, 46, 60, 0.12)
    fin(cam, 1.0)
    sfx(t0 + 0.25, "rizz", 0.9)
    sfx(t0 + 0.25, "sparkle", 0.6)


@SS(402, 407, "Go to the dance, kiddo")
def s101(t0, t1):
    room(night=False)
    G = grandpa_sitting(t0, t1, "happy")
    G.act(t0, "point", expr="happy")
    lips(G, t0, t1)
    cam = mv("orbr", t0, t1, (0, 7.6, 4.8), d=7.5, yaw=-10, pitch=4, lens=32, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0 + 0.4, "cheer", 0.3)


@SS(407, 412, "Your grandma will read tonight")
def s102(t0, t1):
    room(night=False)
    G = grandpa_sitting(t0, t1, "smile")
    Gm = grandma_c(t0, t1, "smile")
    Gm.pose(t0, loc=(10.0, -4.0, 0), rot=facing((10, -4), (0, 4)))
    Gm.walk(t0, t1, (11.0, -6.0, 0), (6.0, -1.0, 0), rate=2.2)
    cam = Cam()
    cam.push(t0, t1, (7, -2, 4.2), 14, 9, yaw=-25, pitch=4, yaw1=-5, lens=28, fstop=5.0)
    fin(cam, 1.0)
    sfx(t0 + 0.3, "door", 0.5)
    sfx(t0 + 0.5, "footsteps", 0.4)


@SS(412, 415, "I looked over: whip pan")
def s103(t0, t1):
    room(night=False)
    E = eddie_bed(t0, t1, "confused", (-3, 2), 0)
    E.face(t0 + 0.3, "lookup")
    E.look(t0 + 0.2, -60, 0)
    cam = Cam()
    cam.whip(t0, t1 - 0.1, (-9, -4, 5.0), (-3, 3, 4.4), (4, -5, 5.0), (8, 1.5, 3.6), lens=28)
    fin(cam, 1.0)


@SS(415, 420, "Grandma was holding the manual")
def s104(t0, t1):
    room(night=False)
    Gm = grandma_c(t0, t1, "smile")
    Gm.pose(t0, loc=(8.0, 1.5, 2.4 - 1.96), rot=facing((8, 1.5), (0, -6)) , legL=(85, 3), legR=(85, -3),
            armL=(70, -12), armR=(70, 12))
    hold_book(Gm, "R")
    lips(Gm, t0, t1)
    cam = mv("in", t0, t1, (8, 1.5, 4.0), d=10, yaw=0, pitch=5, lens=30, fstop=3.0)
    fin(cam, 1.0)
    sfx(t0, "paper", 0.5)


@SS(420, 425, "and she was already asleep")
def s105(t0, t1):
    room(night=False)
    Gm = grandma_c(t0, t1, "smile")
    Gm.pose(t0, loc=(8.0, 1.5, 2.4 - 1.96), rot=0, legL=(85, 3), legR=(85, -3), armL=(70, -12), armR=(70, 12))
    hold_book(Gm, "R")
    Gm.face(w(421), eyes="closed", mouth="smile")
    Gm.pose(w(421), head=(0, 22, 4))
    Gm.pose(t1 - 0.2, head=(0, 30, 8), torso=(0, 8, 0))
    zzz((7.2, 0.5, 6.0), w(422), t1, n=4, size=1.0)
    cam = Cam()
    cam.key(t0, (4.0, -5.0, 5.0), (8, 1.5, 4.0), lens=34, fstop=3.0, focus=8.0)
    cam.key(t1, (6.5, -2.0, 4.6), (8, 1.5, 4.0), lens=40, fstop=3.0, focus=4.5)
    cam.crash(w(421), 34, 44, 0.15)
    fin(cam, 1.0)
    sfx(w(421), "aww", 0.4)
    sfx(w(423), "snort", 0.4)


@SS(425, 427, "HONG SHU! (grandma)")
def s106(t0, t1):
    room(night=False)
    Gm = grandma_c(t0, t1, "smile")
    Gm.pose(t0, loc=(8.0, 1.5, 2.4 - 1.96), rot=0, legL=(85, 3), legR=(85, -3), armL=(70, -12), armR=(70, 12))
    hold_book(Gm, "R")
    ts = t0 + 0.05
    Gm.face(ts, eyes="closed", mouth="ah")
    pop_text("hs", "HONG\nSHU!", (8, -4.5, 8.8), ts, size=2.5, col="#ffe14a")
    cam = Cam()
    cam.key(t0, (7.5, -6.0, 5.4), (8, 1.5, 4.6), lens=28, fstop=4.0, focus=7.5)
    cam.key(t1, (7.5, -3.6, 5.2), (8, 1.5, 4.6), lens=24, fstop=4.0, focus=5.5)
    cam.crash(ts, 28, 36, 0.1)
    bump(cam, ts, 0.8, 8)
    fin(cam, 1.0)
    sfx(ts, "snort", 1.0)
    sfx(ts, "boom", 0.8)


@SS(427, None, "Now, there are two: both snoring, sky bounces")
def s107(t0, t1):
    room(night=True)
    G = grandpa_lying(t0, t1, 0.6, "ah")
    Gm = grandma_c(t0, t1, "smile")
    Gm.root.rotation_euler[0] = math.radians(-90)
    Gm.pose(t0, loc=(8.0, 3.9, 2.2 + 0.62), rot=0, armL=(8, 6), armR=(8, 6))
    box("bed2", (7.4, 9.0, 1.2), (8, 5.5, 0.6), M("#ffffff", 0.45), 0.1)
    box("mat2", (7.0, 8.4, 1.0), (8, 5.4, 1.7), M("#f2f4f8", 0.7), 0.25)
    box("pil2", (3.6, 2.0, 0.8), (8, 8.9, 2.45), M("#f7f8fb", 0.7), 0.35)
    snore(Gm, t0 + 0.3, t1, 0.6)
    pop_text("two", "x2", (4, -1.0, 8.2), t0 + 0.9, size=3.6, col="#ffe14a")
    sparkle("tw", (4, -1.0, 8.4), t0 + 0.9, 3.0, n=16, seed=5)
    cam = Cam()
    cam.key(t0, (0, -2.0, 6.0), (0, 6, 4.0), lens=24, fstop=6.0, focus=9.0)
    cam.key(t1, (4, -16.0, 9.0), (4, 6, 4.0), lens=24, fstop=8.0, focus=22.0)
    cam.crash(t0 + 0.9, 24, 20, 0.2)
    bump(cam, t0 + 0.9, 0.4)
    fin(cam, 1.0)
    sfx(t0 + 0.3, "snort", 0.9)
    sfx(t0 + 0.6, "snort", 0.9)
    sfx(t0 + 0.9, "confetti", 0.6)
    sfx(t0 + 0.9, "cheer", 0.4)
