"""plane / "Почему окна самолёта круглые": the Comet square-window story.
Engineer refuses square windows -> square-window jets crack and fall -> water tank test -> stress at corners -> round windows.
Shots keyed to script word indices (audio/words.json)."""
from shotkit import *
from rbx import story
from rbx.story import *
from rbx.core import _obj
import math, random
from mathutils import Vector

V = Video(__file__)
story.bind(V)
TEXD = os.path.join(rbx.ASSETS, "tex")


# ================================================================== small helpers
def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def EM(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


def TX(name, rough=0.5, emit=0.0, alpha=False):
    return img_mat("t_" + name + str(emit), os.path.join(TEXD, name), rough, emit, alpha)


def vis(ob, t, v):
    """show/hide an object from time t on (keyframed)."""
    f = F(t)
    ob.hide_render = not v
    ob.hide_viewport = not v
    ob.keyframe_insert("hide_render", frame=f)
    ob.keyframe_insert("hide_viewport", frame=f)


def show_at(ob, t, t_end=None):
    """hidden until t, visible from t (until t_end if given)."""
    vis(ob, t - 2.0 / 30, False)
    vis(ob, t, True)
    if t_end is not None:
        vis(ob, t_end, False)


def pop(ob, t, s=1.0, dur=0.22, over=1.25):
    """scale-pop appearance (0 -> overshoot -> s)."""
    ob.scale = (0.01,) * 3; ob.keyframe_insert("scale", frame=F(t - 0.03))
    ob.scale = (s * over,) * 3; ob.keyframe_insert("scale", frame=F(t + dur * 0.6))
    ob.scale = (s,) * 3; ob.keyframe_insert("scale", frame=F(t + dur))


def slide(ob, t0, t1, p0, p1, ease="EASE_OUT"):
    ob.location = p0; ob.keyframe_insert("location", frame=F(t0))
    ob.location = p1; ob.keyframe_insert("location", frame=F(t1))
    if ease == "LINEAR":
        set_interp(ob, "location", F(t1), "LINEAR")
    else:
        set_interp(ob, "location", F(t1), "BEZIER", ease)


def spinz(ob, t0, t1, turns=1.0, axis=2):
    ob.rotation_euler[axis] = 0; ob.keyframe_insert("rotation_euler", index=axis, frame=F(t0))
    ob.rotation_euler[axis] = math.tau * turns; ob.keyframe_insert("rotation_euler", index=axis, frame=F(t1))
    set_interp(ob, "rotation_euler", F(t1), "LINEAR")


def impact(cam, t, amp=0.4, dur=0.45, n=10):
    """Camera shake burst at t (camera parented to a keyframed rig)."""
    rnd = random.Random(int(t * 100) + 3)
    rig = getattr(cam, "_rig", None)
    if rig is None:
        rig = empty("camrig", (0, 0, 0))
        cam.ob.parent = rig
        cam._rig = rig
    rig.location = (0, 0, 0); rig.keyframe_insert("location", frame=F(t) - 1)
    for i in range(n):
        k = 1 - i / n
        rig.location = (rnd.uniform(-1, 1) * amp * k, rnd.uniform(-1, 1) * amp * k * 0.4, rnd.uniform(-1, 1) * amp * k)
        rig.keyframe_insert("location", frame=F(t + dur * i / n))
    rig.location = (0, 0, 0); rig.keyframe_insert("location", frame=F(t + dur))
    return cam


def cpush(t0, t1, tgt, d0, d1, yaw=0.0, pitch=6.0, lens=30, yaw1=None, pitch1=None, lens1=None, roll=0.0, shake=1.0,
          fstop=3.2, look=None, ease="EASE_IN_OUT"):
    cam = Cam()
    cam.push(t0, t1, tgt, d0, d1, yaw=yaw, pitch=pitch, lens=lens, yaw1=yaw1, pitch1=pitch1, lens1=lens1, roll=roll,
             fstop=fstop, look=look, ease=ease)
    if shake:
        cam.handheld(shake)
    return cam


def corbit(t0, t1, tgt, dist, yaw0, yaw1, pitch=8.0, lens=30, pitch1=None, shake=0.8, fstop=3.2):
    cam = Cam()
    cam.orbit(t0, t1, tgt, dist, yaw0, yaw1, pitch=pitch, lens=lens, fstop=fstop, pitch1=pitch1)
    if shake:
        cam.handheld(shake)
    return cam


def cfree(keys, shake=0.8, fstop=3.2):
    """keys = [(t, loc, target, lens)] free camera path."""
    cam = Cam()
    for i, (t, loc, tgt, lens) in enumerate(keys):
        cam.key(t, loc, tgt, lens=lens, focus=tgt, fstop=fstop, ease="EASE_IN_OUT" if i else None)
    if shake:
        cam.handheld(shake)
    return cam


def boom_fx(cam, t, amp=0.5, col=None):
    impact(cam, t, amp)
    fl = fx.white_flash(f"fl{F(t)}", cam.ob, t, t + 0.1)
    show_at(fl, t, t + 0.1)


def ring_plate(name, outer, inner_kind, inner, thick=0.5, mat_=None, loc=(0, 0, 0), n=72, coll=None, corner_r=0.0):
    """Plate (outer w,h) with a hole: inner_kind 'round' (radius) or 'square' (half-size). Faces -Y (like card).
    corner_r > 0 rounds the square hole slightly."""
    ow, oh = outer[0] / 2, outer[1] / 2

    def rect_pt(a, hw, hh):
        c, s = math.cos(a), math.sin(a)
        k = min(hw / abs(c) if abs(c) > 1e-6 else 1e9, hh / abs(s) if abs(s) > 1e-6 else 1e9)
        return (c * k, s * k)

    ins, outs = [], []
    for i in range(n):
        a = math.tau * i / n + 0.0001
        outs.append(rect_pt(a, ow, oh))
        if inner_kind == "round":
            ins.append((math.cos(a) * inner, math.sin(a) * inner))
        else:
            ins.append(rect_pt(a, inner, inner))
    hz = thick / 2
    verts = []
    for p in ins:
        verts.append((p[0], p[1], hz))      # 0..n-1  inner front
    for p in outs:
        verts.append((p[0], p[1], hz))      # n..2n-1 outer front
    for p in ins:
        verts.append((p[0], p[1], -hz))     # 2n..3n-1 inner back
    for p in outs:
        verts.append((p[0], p[1], -hz))     # 3n..4n-1 outer back
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, n + i, n + j, j))                                  # front
        faces.append((2 * n + j, 3 * n + j, 3 * n + i, 2 * n + i))          # back
        faces.append((2 * n + i, i, j, 2 * n + j))                          # hole wall
        faces.append((n + i, 3 * n + i, 3 * n + j, n + j))                  # outer wall
    me = D.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = _obj(name, me, coll, loc, (90, 0, 0), None)
    if mat_ is not None:
        me.materials.append(mat_)
    return ob


def corner_pts(inner, loc):
    """world positions of the 4 corners of a square hole centred at loc (card facing -Y)."""
    x, y, z = loc
    return [(x + sx * inner, y - 0.3, z + sz * inner) for sx in (-1, 1) for sz in (-1, 1)]


def glow_line(name, p0, p1, w, col, s=6.0, t_on=None, t_off=None):
    a, b = Vector(p0), Vector(p1)
    mid = (a + b) / 2
    d = b - a
    o = box(name, (w, d.length, w), tuple(mid), EM(col, s), 0.0)
    q = d.to_track_quat("Y", "Z")
    o.rotation_euler = q.to_euler()
    if t_on is not None:
        show_at(o, t_on, t_off)
    return o


def crack(name, start, direction, length, t0, t1, n=14, w=0.07, col="#120806", seed=0, glow="#ff5a20"):
    """zig-zag crack that propagates from start along direction over [t0,t1]."""
    rnd = random.Random(seed)
    d = Vector(direction).normalized()
    side = d.cross(Vector((0, -1, 0))).normalized()
    p = Vector(start)
    segs = []
    for i in range(n):
        step = length / n
        q = p + d * step + side * rnd.uniform(-0.45, 0.45) * step
        segs.append((p, q))
        p = q
    for i, (a, b) in enumerate(segs):
        ts = t0 + (t1 - t0) * i / n
        o = glow_line(f"{name}{i}", tuple(a), tuple(b), w, glow, 5.0)
        show_at(o, ts)
        o2 = glow_line(f"{name}d{i}", tuple(a + Vector((0, 0.01, 0))), tuple(b + Vector((0, 0.01, 0))), w * 0.5, col, 0.0)
        o2.data.materials.clear(); o2.data.materials.append(M(col, 0.9))
        show_at(o2, ts + 0.05)
    return segs[-1][1]


# ================================================================== cast
def eng(t0, t1, expr="neutral"):
    E = chars.Char("Eng", skin="#e6bf9a", shirt="#eceae2", pants="#343b52", hair="short", hair_color="#2a1d16",
                   face="hero", sleeves="long", extras=("glasses",), vneck="#7aa0d8")
    return story._live(E, t0, t1, expr, 0.6)


def boss(t0, t1, expr="neutral"):
    B = chars.Char("Boss", skin="#d9b48f", shirt="#22232a", pants="#22232a", hair="slick", hair_color="#16120f",
                   face="villain", sleeves="long", extras=("collar:#f4f4f4",), scale=1.15)
    box("Boss_tie", (0.36, 0.06, 1.3), (0, -0.57, 1.25), M("#c8261e", 0.4), 0.03, parent=B.hip, coll=B.coll)
    return story._live(B, t0, t1, expr, 0.6)


def invest(i, t0, t1, expr="neutral"):
    cols = [("#2f6fd0", "#222a3a"), ("#d9a02e", "#2a2a2a"), ("#3f9a5a", "#2a3444"), ("#c8261e", "#222222")]
    sh, pa = cols[i % 4]
    I = chars.Char(f"Inv{i}", skin=["#e9c7a6", "#c9926a", "#f1dfc6", "#a8714a"][i % 4], shirt=sh, pants=pa,
                   hair=["buzz", "short", "cap", "buzz"][i % 4], hair_color="#2a1d16", face="plain" if i % 2 else "mustache",
                   sleeves="long", extras=("collar:#f4f4f4",) if i % 2 == 0 else ())
    return story._live(I, t0, t1, expr, 0.6)


def folk(i, t0, t1, expr="neutral"):
    return townie(i, t0, t1, expr)


def pax(t0, t1, expr="neutral"):
    P = chars.Char("Pax", skin="#e9c7a6", shirt="#e8b520", pants="#2f3f6a", hair="messy", hair_color="#5a3a22",
                   face="kid", vneck="#ffe08a")
    return story._live(P, t0, t1, expr, 0.8)


# ================================================================== sets
def office(dim=False):
    c = collection("OFFICE")
    world((0.55, 0.6, 0.72), 0.55 if not dim else 0.3)
    box("of_floor", (50, 34, 0.4), (0, 4, -0.2), M("#8a6a4a", 0.55), 0, coll=c)
    box("of_wall", (50, 0.6, 18), (0, 10, 9), M("#7f9bbb", 0.7), 0, coll=c)
    box("of_wallL", (0.6, 34, 18), (-22, 4, 9), M("#7490b0", 0.7), 0, coll=c)
    box("of_wallR", (0.6, 34, 18), (22, 4, 9), M("#7490b0", 0.7), 0, coll=c)
    # window with a bright city/sky view
    card("of_sky", 10, 6, (-11, 9.6, 9.5), mat("of_skym", (0.6, 0.82, 1.0), emit=(0.6, 0.82, 1.0), estr=3.0), "-Y", coll=c)
    box("of_wf", (10.6, 0.3, 0.5), (-11, 9.5, 12.6), M("#f2f2f2", 0.5), 0.02, coll=c)
    box("of_wf2", (10.6, 0.3, 0.5), (-11, 9.5, 6.4), M("#f2f2f2", 0.5), 0.02, coll=c)
    # drafting board with the blueprint
    box("of_board", (11.2, 0.4, 6.2), (2.5, 9.2, 7.6), M("#2a2f3a", 0.6), 0.1, coll=c)
    card("of_bp", 10.4, 5.2, (2.5, 8.95, 7.6), TX("plane_bp_sq.png", 0.7, 0.35), "-Y", coll=c)
    # desk + plane model
    box("of_desk", (9, 3.6, 0.4), (-1.5, 6.2, 3.4), M("#6b4a30", 0.5), 0.05, coll=c)
    for sx in (-1, 1):
        box(f"of_leg{sx}", (0.4, 3.0, 3.3), (-1.5 + sx * 4.2, 6.2, 1.65), M("#4d3522", 0.6), 0.03, coll=c)
    box("of_lamp", (0.2, 0.2, 2.6), (-5, 6.8, 4.8), M("#2a2a2a", 0.4), 0.05, coll=c)
    sphere("of_bulb", 0.4, (-5, 6.3, 6.0), EM("#fff0c0", 6), coll=c, seg=12)
    light("of_key", "AREA", (0, -4, 13), 4200, (1.0, 0.96, 0.9), 9, coll=c, target=(0, 5, 3))
    light("of_fill", "AREA", (-10, -6, 7), 1100, (0.85, 0.92, 1.0), 8, coll=c, target=(0, 5, 3))
    light("of_rim", "AREA", (8, 12, 9), 1500, (1.0, 0.8, 0.6), 5, coll=c, target=(0, 4, 4))
    return c


def model_plane(name, loc, scale=0.16, rot=0, round_win=False):
    root = W2.airliner(name, loc, rot=rot, scale=scale, label="")
    if round_win:
        swap_windows(name)
    return root


def swap_windows(name):
    Mk = mat("plane_win", hexc("#1a2433"), 0.15)
    root = D.objects[name]
    for k in range(18):
        for sx in (-1, 1):
            o = D.objects.get(f"{name}_w{k}{sx}")
            if o is not None:
                loc = Vector(o.location)
                D.objects.remove(o, do_unlink=True)
                c = cyl(f"{name}_rw{k}{sx}", 0.36, 0.14, tuple(loc), Mk, 20, rot=(0, 90, 0), parent=root)


def sky_set(top=(0.03, 0.14, 0.72), bottom=(0.18, 0.42, 0.95), sun_s=4.0, clouds=18, seed=3, center=(0, 0, 40)):
    W.sky(1.0, top, bottom)
    W.sun(sun_s)
    W.cloud_field("sk", center, spread=(110, 110, 14), n=clouds, seed=seed)


def ground_runway(y0=-120, y1=80):
    c = collection("AIRFIELD")
    box("rw_grass", (400, 400, 0.4), (0, 0, -0.2), M("#5fae4a", 0.9), 0, coll=c)
    box("rw_strip", (16, y1 - y0, 0.2), (0, (y0 + y1) / 2, 0.02), M("#3a3d44", 0.8), 0, coll=c)
    for i in range(int((y1 - y0) / 14)):
        box(f"rw_d{i}", (0.6, 6, 0.05), (0, y0 + 5 + i * 14, 0.14), M("#f4f4f4", 0.7), 0, coll=c)
    return c


def ocean(col="#1f6fbf", size=700):
    box("sea", (size, size, 0.4), (0, 0, -0.2), mat("sea_m", hexc(col), 0.12, metal=0.1), 0, coll=None)
    for i in range(26):
        r = random.Random(i)
        o = box(f"foam{i}", (r.uniform(3, 7), 0.5, 0.06), (r.uniform(-60, 60), r.uniform(-30, 120), 0.22), M("#e8f4ff", 0.5), 0)
        noise(o, "location", 0, 0.8, 18)


def debris(prefix, n, center, spread, seed=0, sinks=True):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        p = (center[0] + rnd.uniform(-spread, spread), center[1] + rnd.uniform(-spread, spread), 0.15)
        o = box(f"{prefix}{i}", (rnd.uniform(0.8, 2.6), rnd.uniform(0.5, 1.6), 0.12), p,
                M(rnd.choice(["#e8ecf0", "#c0c8d0", "#2f6fd0", "#f4f6f8"]), 0.35, metal=0.5), 0.03,
                rot=(rnd.uniform(-12, 12), rnd.uniform(-12, 12), rnd.uniform(0, 360)))
        noise(o, "location", 2, 0.12, 14)
        noise(o, "rotation_euler", 0, 0.06, 18)
        out.append(o)
    return out


def boat(name, loc, rot=0):
    r = empty(name, loc, rot=(0, 0, rot))
    box(name + "_h", (5.4, 9, 1.4), (0, 0, 0.7), M("#f4f4f4", 0.45), 0.4, parent=r)
    box(name + "_s", (5.6, 2.0, 0.3), (0, -3.6, 1.35), M("#c8261e", 0.5), 0.1, parent=r)
    box(name + "_c", (3.0, 3.0, 2.2), (0, 1.8, 2.4), M("#d8dde4", 0.5), 0.2, parent=r)
    box(name + "_cw", (3.1, 0.1, 0.9), (0, 0.28, 2.7), M("#1a2433", 0.15), 0.05, parent=r)
    noise(r, "location", 2, 0.12, 22)
    noise(r, "rotation_euler", 0, 0.03, 26)
    noise(r, "rotation_euler", 1, 0.04, 30)
    return r


def ship(name, loc, rot=0, scale=1.0):
    """Old steamer with round portholes."""
    r = empty(name, loc, rot=(0, 0, rot)); r.scale = (scale,) * 3
    box(name + "_hull", (7, 24, 4), (0, 0, 2.0), M("#243a5a", 0.5), 0.8, parent=r)
    box(name + "_deck", (6.4, 20, 3.2), (0, 0, 5.6), M("#f4f4f4", 0.5), 0.5, parent=r)
    box(name + "_bridge", (4.6, 6, 3.0), (0, 2.5, 8.7), M("#f4f4f4", 0.5), 0.3, parent=r)
    cyl(name + "_fun", 1.2, 5, (0, -2.0, 9.5), M("#c8261e", 0.5), 20, parent=r)
    box(name + "_funt", (2.5, 2.5, 0.8), (0, -2.0, 12.2), M("#1a1a1a", 0.5), 0.1, parent=r)
    Mp = M("#e2b23a", 0.3, metal=0.9)
    Mg = mat("ship_glass", (0.5, 0.75, 1.0), emit=(0.5, 0.75, 1.0), estr=2.0)
    for k in range(8):
        for sx in (-1, 1):
            cyl(f"{name}_pf{k}{sx}", 0.62, 0.2, (sx * 3.22, -8 + k * 2.2, 5.6), Mp, 20, rot=(0, 90, 0), parent=r)
            cyl(f"{name}_pg{k}{sx}", 0.46, 0.22, (sx * 3.25, -8 + k * 2.2, 5.6), Mg, 20, rot=(0, 90, 0), parent=r)
    return r


def tank_set(water=True):
    c = collection("TANK")
    world((0.1, 0.14, 0.2), 0.35)
    box("tk_floor", (60, 40, 0.4), (0, 10, -0.2), M("#3a4048", 0.5), 0, coll=c)
    box("tk_wall", (60, 0.6, 24), (0, 24, 12), M("#2c3340", 0.7), 0, coll=c)
    # glass tank
    box("tk_water", (22, 12, 11), (0, 10, 6.0), mat("tk_wat", (0.15, 0.5, 0.95), 0.05, emit=(0.1, 0.4, 0.9), estr=0.5, alpha=0.4), 0.2, coll=c)
    for sx in (-1, 1):
        box(f"tk_post{sx}", (0.6, 0.6, 12.2), (sx * 11.2, 4, 6.1), M("#8a929e", 0.3, metal=0.9), 0.05, coll=c)
        box(f"tk_postb{sx}", (0.6, 0.6, 12.2), (sx * 11.2, 16, 6.1), M("#8a929e", 0.3, metal=0.9), 0.05, coll=c)
    box("tk_top", (23, 13, 0.6), (0, 10, 12.2), M("#8a929e", 0.3, metal=0.9), 0.05, coll=c)
    # fuselage section inside
    cyl("tk_fus", 3.4, 14, (0, 10, 5.4), M("#e8ecf0", 0.25, metal=0.6), 40, rot=(0, 90, 0), coll=c)
    for k in range(5):
        box(f"tk_fw{k}", (1.0, 0.1, 1.0), (-5 + k * 2.5, 6.62, 6.3), M("#1a2433", 0.15), 0.05, coll=c)
    # gauge on a pedestal
    box("tk_ped", (2.4, 2.4, 3.6), (-15, 0, 1.8), M("#2e343e", 0.5), 0.1, coll=c)
    cyl("tk_dial", 2.2, 0.4, (-15, -1.1, 4.6), M("#f4f4f4", 0.4), 40, rot=(90, 0, 0), coll=c)
    ndl = box("tk_needle", (0.14, 0.1, 1.8), (0, 0, 0), M("#c8261e", 0.3), 0.02, coll=c)
    ndl.parent = empty("tk_pivot", (-15, -1.4, 4.6), coll=c)
    ndl.location = (0, 0, 0.9)
    pivot = ndl.parent
    for i in range(7):
        a = math.radians(-120 + i * 40)
        box(f"tk_tick{i}", (0.1, 0.08, 0.4), (-15 + math.sin(a) * 1.8, -1.35, 4.6 + math.cos(a) * 1.8), M("#222222", 0.5), 0.0,
            rot=(0, math.degrees(a), 0), coll=c)
    light("tk_key", "AREA", (0, -8, 14), 4800, (0.8, 0.9, 1.0), 10, coll=c, target=(0, 10, 5))
    light("tk_fill", "AREA", (-14, -6, 6), 1600, (1.0, 0.92, 0.85), 6, coll=c, target=(-6, 6, 5))
    light("tk_rim", "AREA", (14, 20, 10), 1800, (0.4, 0.7, 1.0), 6, coll=c, target=(0, 10, 5))
    return dict(coll=c, pivot=pivot)


def bubbles(prefix, center, spread, t0, t1, n=28, seed=0, rise=7.0):
    rnd = random.Random(seed)
    Mb = mat("bubble", (0.85, 0.95, 1.0), 0.05, emit=(0.8, 0.9, 1.0), estr=1.2, alpha=0.6)
    for i in range(n):
        p = Vector(center) + Vector((rnd.uniform(-1, 1) * spread[0], rnd.uniform(-1, 1) * spread[1], rnd.uniform(-1, 0) * spread[2]))
        o = sphere(f"{prefix}{i}", rnd.uniform(0.1, 0.3), tuple(p), Mb, seg=8)
        ts = t0 + rnd.uniform(0, max(0.1, (t1 - t0) * 0.6))
        o.location = tuple(p); o.keyframe_insert("location", frame=F(ts))
        o.location = tuple(p + Vector((rnd.uniform(-0.6, 0.6), 0, rise)))
        o.keyframe_insert("location", frame=F(ts + rnd.uniform(0.5, 1.4)))
        show_at(o, ts)


def window_set(round_win, dark_sky=False, size=(15, 10), inner=3.0, thick=0.7, light_col=(1.0, 0.95, 0.9)):
    """Macro fuselage wall with ONE window, camera looks at it from -Y. Returns dict of key points."""
    c = collection("WIN")
    world((0.06, 0.07, 0.1), 0.3)
    metal = mat("fus_metal", hexc("#b9c2cc"), 0.28, metal=0.85)
    box("wn_back", (60, 0.4, 40), (0, 4.0, 5), M("#0b0d12", 0.9), 0, coll=c)
    card("wn_sky", 30, 20, (0, 2.5, 5), mat("wn_skym", (0.35, 0.6, 1.0) if not dark_sky else (0.1, 0.12, 0.2),
         emit=(0.35, 0.6, 1.0) if not dark_sky else (0.1, 0.12, 0.2), estr=2.2), "-Y", coll=c)
    card("wn_cloud", 6, 2.4, (3.0, 2.4, 3.5), mat("wn_cl", (1, 1, 1), emit=(1, 1, 1), estr=1.4), "-Y", coll=c)
    plate = ring_plate("wn_plate", size, "round" if round_win else "square", inner, thick, metal, loc=(0, 0, 5), coll=c)
    # frame bevel ring so the hole reads: dark inner edge
    light("wn_key", "AREA", (-6, -10, 12), 3800, light_col, 6, coll=c, target=(0, 0, 5))
    light("wn_rim", "AREA", (9, -6, 2), 1600, (0.5, 0.7, 1.0), 5, coll=c, target=(0, 0, 5))
    return dict(coll=c, plate=plate, ctr=(0, 0, 5), inner=inner, thick=thick, size=size)


def rivets(prefix, ctr, size, inner, n=14, coll=None):
    Mr = M("#d6dce2", 0.25, metal=0.9)
    for i in range(n):
        a = math.tau * i / n
        r = inner * 1.9
        sphere(f"{prefix}{i}", 0.18, (ctr[0] + math.cos(a) * r, ctr[1] - 0.38, ctr[2] + math.sin(a) * r), Mr, seg=10, coll=coll)


# ================================================================== SHOTS
# ---------------- act 1: engineer vs boss
@S(1, 0, 3, "HOOK: engineer in shock/refusal, crash zoom, shakes head (Он отказался)")
def s01(t0, t1):
    office()
    e = eng(t0, t1, "angry")
    e.pose(t0, loc=(0, 4, 0), rot=0)
    e.act(t0 + 0.05, "fists", expr="angry")
    e.shake(t0 + 0.5, n=3, amp=22, rate=6.0)
    lips(e, t0, t1)
    cam = Cam()
    cam.key(t0, (0.6, -1.0, 4.9), (0, 4, 4.8), lens=18, focus=5.0, fstop=3)
    cam.key(t1, (0.2, -0.4, 4.7), (0, 4, 4.7), lens=38, focus=4.4, fstop=3, ease="EASE_OUT")
    cam.crash(t0 + 0.1, 20, 36, 0.2)
    cam.handheld(1.6)
    sfx(t0 + 0.02, "whoosh", 0.8)
    sfx(t0 + 0.5, "thud", 0.7)


@S(2, 3, 5, "Square windows on the blueprint (квадратные окна)")
def s02(t0, t1):
    office()
    ring = EM("#ffd84a", 4)
    for i in range(9):
        o = box(f"hl{i}", (0.8, 0.12, 0.8), (-2.4 + i * 1.1 + 0.4, 8.7, 8.55), ring, 0.0)
        show_at(o, t0 + 0.08 * i)
    cam = cpush(t0, t1, (2.5, 8.9, 7.6), 9, 5.0, yaw=-18, pitch=2, lens=28, yaw1=6, shake=1.0)
    sfx(t0 + 0.02, "click", 0.6)
    sfx(t0 + 0.4, "tick", 0.5)


@S(3, 5, 7, "Plane model on the desk, whip (для самолёта)")
def s03(t0, t1):
    office()
    mp = model_plane("mdl", (-1.5, 6.2, 5.0), scale=0.2, rot=-35)
    mp.rotation_euler[0] = math.radians(-6)
    spinz(mp, t0, t1, 0.25, 2)
    e = eng(t0, t1, "neutral")
    e.pose(t0, loc=(2.8, 3.6, 0), rot=facing((2.8, 3.6), (-1.5, 6.2)) + 8)
    e.act(t0 + 0.3, "think", expr="sus")
    cam = Cam()
    cam.whip(t0, t0 + 0.28, (6, -4, 5), (3, 4, 5), (-4, -3.0, 6.5), (-1.5, 6.2, 5.2), lens=26)
    cam.key(t1, (-2.4, -1.6, 6.0), (-1.5, 6.2, 5.2), lens=34, focus=8.0, fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.0)


@S(4, 7, 9, "Boss storms in (Начальник сказал)")
def s04(t0, t1):
    office()
    e = eng(t0, t1, "worried")
    e.pose(t0, loc=(-1.5, 4.5, 0), rot=facing((-1.5, 4.5), (-14, 0)))
    b = boss(t0, t1, "angry")
    b.walk(t0, t0 + 0.8, (-17, -2, 0), (-5, -1, 0), rate=3.6, swing=45, arm=30, bob=0.22)
    b.pose(t0 + 0.8, rot=facing((-5, -1), (-1.5, 4.5)))
    b.act(t0 + 0.9, "point", expr="angry")
    lips(b, t0 + 0.9, t1)
    cam = cfree([(t0, (3.5, -8, 3.0), (-8, -1, 4.0), 24), (t1, (6, -7, 4.2), (-3, 1, 4.6), 28)], shake=1.2)
    sfx(t0 + 0.05, "stomp", 0.7)
    sfx(t0 + 0.4, "stomp", 0.7)
    sfx(t0 + 0.8, "whoosh", 0.5)


@S(5, 9, 12, "Boss: Квадрат дешевле — sign pops")
def s05(t0, t1):
    office()
    b = boss(t0, t1, "smug")
    b.pose(t0, loc=(0, 3.5, 0), rot=0)
    b.act(t0 + 0.05, "point", expr="smug")
    lips(b, t0, t1)
    sg = card("sqbad", 5.6, 2.0, (4.4, 3.0, 5.0), TX("plane_sq_bad.png", 0.5, 0.6), "-Y")
    pop(sg, t0 + 0.55, 1.0)
    sg.rotation_euler[1] = math.radians(8)
    cam = cpush(t0, t1, (1.6, 3.5, 4.6), 8.5, 6.4, yaw=-14, pitch=4, lens=30, yaw1=8, shake=1.1)
    sfx(t0 + 0.55, "pop", 0.8)
    sfx(t0 + 0.6, "sparkle", 0.4)


@S(6, 12, 14, "Boss smug low angle (выглядит современно)")
def s06(t0, t1):
    office()
    b = boss(t0, t1, "smug")
    b.pose(t0, loc=(0, 3.5, 0), rot=-14)
    b.act(t0, "cross", expr="smug")
    lips(b, t0, t1)
    cam = cpush(t0, t1, (0, 3.5, 5.2), 6.0, 4.4, yaw=-28, pitch=-8, lens=28, yaw1=-8, pitch1=-4, roll=4, shake=1.0)
    sfx(t0 + 0.2, "sparkle", 0.45)


@S(7, 14, 18, "Boss furious: Ты срываешь запуск! slams desk")
def s07(t0, t1):
    office()
    b = boss(t0, t1, "furious")
    b.pose(t0, loc=(0, 3.5, 0), rot=0)
    b.act(t0 + 0.05, "fists", expr="furious", strength=1.3)
    lips(b, t0, t1, "shout")
    b.act(t0 + 0.9, "push", expr="furious")
    b.panic(t0 + 1.0, t1, 8.0)
    cam = Cam()
    cam.key(t0, (0.5, -6.5, 4.4), (0, 3.5, 5.0), lens=32, focus=10.0, fstop=3)
    cam.key(t1, (0.1, -3.3, 5.0), (0, 3.5, 5.0), lens=44, focus=6.8, fstop=3, ease="EASE_IN")
    cam.crash(t0 + 0.88, 32, 22, 0.12)
    cam.handheld(2.2)
    impact(cam, t0 + 0.9, 0.5)
    impact(cam, t0 + 1.5, 0.35)
    sfx(t0 + 0.9, "thud", 1.0)
    sfx(t0 + 1.5, "stomp", 0.8)


@S(8, 18, 20, "Engineer calm reply (Инженер ответил)")
def s08(t0, t1):
    office(dim=True)
    e = eng(t0, t1, "neutral")
    e.pose(t0, loc=(0, 4, 0), rot=0)
    e.act(t0 + 0.2, "idle", expr="neutral")
    lips(e, t0 + 0.2, t1)
    cam = cpush(t0, t1, (0, 4, 4.7), 5.4, 3.9, yaw=10, pitch=0, lens=36, yaw1=2, shake=0.5, fstop=2.4)
    sfx(t0, "rumble", 0.5, dur=t1 - t0 + 0.4)


@S(9, 20, 22, "Углы убивают: eyes close-up, crash zoom, boom")
def s09(t0, t1):
    office(dim=True)
    e = eng(t0, t1, "determined")
    e.pose(t0, loc=(0, 4, 0), rot=0)
    lips(e, t0, t1)
    e.look(t0 + 0.3, 0, 0)
    cam = Cam()
    cam.key(t0, (0.1, -0.4, 4.9), (0, 4, 4.9), lens=70, focus=4.4, fstop=2.0)
    cam.key(t1, (0.0, 0.8, 4.95), (0, 4, 4.95), lens=95, focus=3.2, fstop=2.0, ease="EASE_IN")
    cam.crash(t0 + 0.4, 70, 120, 0.1)
    cam.handheld(1.2)
    boom_fx(cam, t0 + 0.4, 0.6)
    sfx(t0 + 0.38, "boom", 1.0)
    sfx(t0 + 0.38, "riser", 0.5)


# ---------------- act 2: success
@S(10, 22, 25, "Первый в мире: airliner on the runway, hero shot")
def s10(t0, t1):
    ground_runway()
    sky_set()
    pl = W2.airliner("jet", (0, 20, 4.2), rot=0, scale=1.0)
    cam = Cam()
    cam.key(t0, (-14, -26, 3.0), (0, 20, 6), lens=22, focus=40.0, fstop=4)
    cam.key(t1, (-9, -18, 5.0), (0, 14, 6), lens=30, focus=34.0, fstop=4, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "jet", 0.6, dur=t1 - t0 + 0.4)


@S(11, 25, 28, "реактивный лайнер взлетел: takeoff, tracking camera")
def s11(t0, t1):
    ground_runway()
    sky_set()
    pl = W2.airliner("jet", (0, 30, 4.2), rot=0, scale=1.0)
    pl.location = (0, 30, 4.2); pl.keyframe_insert("location", frame=F(t0))
    pl.rotation_euler[0] = 0; pl.keyframe_insert("rotation_euler", index=0, frame=F(t0))
    pl.location = (0, -70, 4.4); pl.keyframe_insert("location", frame=F(t0 + (t1 - t0) * 0.5))
    pl.rotation_euler[0] = math.radians(-14); pl.keyframe_insert("rotation_euler", index=0, frame=F(t0 + (t1 - t0) * 0.7))
    pl.location = (0, -120, 30); pl.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.key(t0, (24, 22, 4.0), (0, 28, 5), lens=26, focus=30.0, fstop=5)
    cam.key(t1, (30, -70, 10), (0, -100, 22), lens=22, focus=40.0, fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.1, "jet", 0.9, dur=t1 - t0)
    sfx(t0 + 0.6, "whoosh", 0.8)


@S(12, 28, 32, "с почти квадратными окнами: fly-by along the windows")
def s12(t0, t1):
    sky_set()
    pl = W2.airliner("jet", (0, 0, 20), rot=0, scale=1.6)
    cam = Cam()
    cam.key(t0, (-6, 18, 21.5), (-1, 14, 21), lens=34, focus=7.0, fstop=2.8)
    cam.key(t1, (-6, -22, 21.5), (-1, -26, 21), lens=34, focus=7.0, fstop=2.8, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "whoosh", 0.8)


@S(13, 32, 36, "Газеты назвали его будущим: newspapers fly in")
def s13(t0, t1):
    world((0.12, 0.12, 0.16), 0.3)
    box("bg", (60, 0.4, 40), (0, 14, 10), M("#1b1d26", 0.8), 0)
    for i in range(5):
        n = card(f"np{i}", 6.0, 8.0, (0, 6, 5), TX("plane_news.png", 0.6, 0.55), "-Y")
        ts = t0 + i * 0.28
        pos = [(-5, 6, 4), (4.2, 5.5, 6.2), (-1.5, 5, 7.5), (3.6, 4.8, 3.6), (0, 4.0, 5.4)][i]
        n.location = (pos[0] + 14, pos[1], pos[2] + 6)
        n.rotation_euler[1] = math.radians([-18, 14, -8, 20, 4][i])
        n.keyframe_insert("location", frame=F(ts)); n.keyframe_insert("rotation_euler", index=1, frame=F(ts))
        n.location = pos
        n.keyframe_insert("location", frame=F(ts + 0.3))
        set_interp(n, "location", F(ts + 0.3), "BEZIER", "EASE_OUT")
        spinz(n, ts, ts + 0.3, 1.0, 1)
        sfx(ts + 0.18, "paper", 0.7)
    light("nl", "AREA", (0, -6, 12), 3000, (1, 0.97, 0.9), 8, target=(0, 6, 5))
    cam = cpush(t0, t1, (0, 5, 5), 15, 11, yaw=0, pitch=0, lens=30, yaw1=-6, shake=1.2)
    sfx(t0 + 1.2, "notif", 0.5)


@S(14, 36, 37, "авиации.: front page slam")
def s14(t0, t1):
    world((0.12, 0.12, 0.16), 0.3)
    box("bg", (60, 0.4, 40), (0, 14, 10), M("#1b1d26", 0.8), 0)
    n = card("np", 7.4, 9.9, (0, 5, 5), TX("plane_news.png", 0.6, 0.6), "-Y")
    n.location = (0, -2, 5); n.keyframe_insert("location", frame=F(t0))
    n.location = (0, 5, 5); n.keyframe_insert("location", frame=F(t0 + 0.2))
    set_interp(n, "location", F(t0 + 0.2), "BEZIER", "EASE_OUT")
    light("nl", "AREA", (0, -6, 12), 3000, (1, 0.97, 0.9), 8, target=(0, 6, 5))
    cam = cpush(t0, t1, (0, 5, 5), 14, 10, lens=30, shake=1.0)
    impact(cam, t0 + 0.2, 0.4)
    sfx(t0 + 0.18, "slap", 0.9)


@S(15, 37, 40, "Билеты раскупили: queue at ticket office")
def s15(t0, t1):
    world((0.75, 0.82, 0.95), 0.6)
    box("fl", (60, 40, 0.4), (0, 4, -0.2), M("#c9c2b4", 0.6), 0)
    box("wall", (60, 0.6, 20), (0, 14, 10), M("#8fa6c2", 0.7), 0)
    box("counter", (14, 2.4, 3.6), (0, 11, 1.8), M("#6b4a30", 0.5), 0.1)
    card("cs", 8, 2.8, (0, 10.6, 7.5), mat("cs_m", hexc("#2f6fd0"), emit=hexc("#2f6fd0"), estr=1.5), "-Y")
    for i in range(7):
        k = folk(i, t0, t1, "happy")
        x = -1.5 + (i % 2) * 0.6
        k.pose(t0, loc=(x, 6.5 - i * 3.0, 0), rot=facing((x, 6.5 - i * 3.0), (0, 11)))
        if i % 2 == 0:
            k.act(t0 + 0.2 + i * 0.1, "cheer", expr="joy")
        else:
            k.act(t0 + 0.3, "phone", expr="happy")
        sfx(t0 + 0.15 + i * 0.14, "pay", 0.5)
    light("kl", "AREA", (0, -6, 14), 4000, (1, 0.97, 0.92), 9, target=(0, 6, 3))
    cam = cfree([(t0, (6, -16, 4.0), (0, 5, 3.5), 22), (t1, (-3, -9, 7.0), (0, 8, 3.5), 28)], shake=1.2)


@S(16, 40, 42, "за несколько дней: SOLD OUT board slams down")
def s16(t0, t1):
    world((0.75, 0.82, 0.95), 0.6)
    box("wall", (60, 0.6, 20), (0, 14, 10), M("#8fa6c2", 0.7), 0)
    sb = card("sold", 9.6, 4.2, (0, 8, 5.4), TX("plane_sold.png", 0.5, 0.6), "-Y")
    sb.location = (0, 8, 14); sb.keyframe_insert("location", frame=F(t0))
    sb.location = (0, 8, 5.4); sb.keyframe_insert("location", frame=F(t0 + 0.25))
    set_interp(sb, "location", F(t0 + 0.25), "BEZIER", "EASE_IN")
    light("kl", "AREA", (0, -6, 14), 4000, (1, 0.97, 0.92), 9, target=(0, 8, 5))
    cam = cpush(t0, t1, (0, 8, 5.4), 16, 10, lens=30, shake=1.2)
    impact(cam, t0 + 0.25, 0.8)
    sfx(t0 + 0.24, "thud", 1.0)
    sfx(t0 + 0.26, "ding", 0.6)


@S(17, 42, 46, "Круглые окна героя высмеивали: engineer surrounded by laughing crowd")
def s17(t0, t1):
    office()
    e = eng(t0, t1, "worried")
    e.pose(t0, loc=(0, 4, 0), rot=0)
    e.act(t0, "slump", expr="worried")
    for i, (x, y) in enumerate(((-6, 0), (6, 0.5), (-3.5, -3), (3.8, -2.5), (-9, -2), (9, -1.5))):
        k = folk(i + 3, t0, t1, "joy")
        k.pose(t0, loc=(x, y, 0), rot=facing((x, y), (0, 4)))
        laugh(k, t0 + 0.1 + i * 0.07, t1, rate=5 + i % 3)
        k.act(t0 + 0.1 + i * 0.07, "point", expr="joy")
        bub = card(f"hb{i}", 2.6, 1.45, (x, y - 0.5, 8.6 + (i % 2) * 0.8), TX("plane_laugh.png", 0.6, 0.5, True), "-Y")
        pop(bub, t0 + 0.3 + i * 0.12, 1.0)
        sfx(t0 + 0.3 + i * 0.12, "pop", 0.4)
    cam = corbit(t0, t1, (0, 3, 4.5), 15, -25, 25, pitch=5, lens=26, shake=1.0)
    sfx(t0, "laughs", 0.6, dur=t1 - t0)


@S(18, 46, 49, "Как на пароходе!: steamer with round portholes")
def s18(t0, t1):
    W.sky(1.0, (0.2, 0.45, 0.85), (0.7, 0.85, 1.0)); W.sun(4.0)
    ocean()
    sh = ship("ship", (0, 20, 0), rot=0, scale=1.0)
    slide(sh, t0, t1, (14, 20, 0), (-14, 20, 0), "LINEAR")
    cam = Cam()
    cam.key(t0, (8, -14, 3.5), (10, 20, 5.6), lens=28, focus=34.0, fstop=4)
    cam.key(t1, (-6, -14, 3.8), (-10, 20, 5.6), lens=28, focus=34.0, fstop=4, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0 + 0.1, "horn", 0.8)
    sfx(t0 + 0.05, "whoosh", 0.4)


# ---------------- act 3: planes fall
@S(19, 49, 51, "Потом самолёты: dark sky, plane flies, dutch angle")
def s19(t0, t1):
    W.sky(0.9, (0.04, 0.06, 0.18), (0.2, 0.26, 0.4)); W.sun(1.2, rot=(60, 0, 20))
    W.cloud_field("c", (0, 0, 25), spread=(60, 60, 10), n=10, seed=5)
    pl = W2.airliner("jet", (-30, 20, 24), rot=90, scale=0.9)
    slide(pl, t0, t1, (-30, 20, 24), (30, 20, 24), "LINEAR")
    cam = Cam()
    cam.key(t0, (0, -30, 12), (-12, 20, 24), lens=28, roll=-6, focus=50.0, fstop=4)
    cam.key(t1, (0, -30, 14), (12, 20, 24), lens=28, roll=-10, focus=50.0, fstop=4, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0, "wind", 0.5, dur=t1 - t0 + 0.4)
    sfx(t0, "riser", 0.4)


@S(20, 51, 53, "начали падать: plane tilts and plunges, alarm")
def s20(t0, t1):
    W.sky(0.9, (0.04, 0.06, 0.18), (0.2, 0.26, 0.4)); W.sun(1.2, rot=(60, 0, 20))
    W.cloud_field("c", (0, 0, 25), spread=(60, 60, 10), n=10, seed=5)
    pl = W2.airliner("jet", (6, 20, 28), rot=90, scale=0.9)
    pl.keyframe_insert("location", frame=F(t0))
    pl.rotation_euler = (0, 0, math.radians(90)); pl.keyframe_insert("rotation_euler", frame=F(t0))
    pl.location = (-6, 20, 4); pl.keyframe_insert("location", frame=F(t1))
    pl.rotation_euler = (math.radians(50), 0, math.radians(90)); pl.keyframe_insert("rotation_euler", frame=F(t1))
    set_interp(pl, "location", F(t1), "BEZIER", "EASE_IN")
    cam = Cam()
    cam.key(t0, (0, -26, 18), (4, 20, 26), lens=26, roll=8, focus=50.0, fstop=4)
    cam.key(t1, (0, -26, 10), (-4, 20, 8), lens=26, roll=-14, focus=50.0, fstop=4, ease="EASE_IN")
    cam.handheld(2.0)
    sfx(t0, "alarm", 0.6, dur=t1 - t0 + 0.2)
    sfx(t0 + 0.1, "whoosh", 0.6)
    impact(cam, t0 + 0.4, 0.3)


def crash_scene(t0, t1, hit_t, loc, side=1, seed=0):
    W.sky(1.0, (0.2, 0.4, 0.8), (0.6, 0.78, 0.95)); W.sun(3.2)
    ocean()
    pl = W2.airliner("jet", (loc[0] - 6 * side, loc[1], 40), rot=90 * side, scale=0.8)
    pl.keyframe_insert("location", frame=F(t0))
    pl.rotation_euler = (0, 0, math.radians(90 * side)); pl.keyframe_insert("rotation_euler", frame=F(t0))
    pl.location = (loc[0], loc[1], 1.5); pl.keyframe_insert("location", frame=F(hit_t))
    pl.rotation_euler = (math.radians(55), 0, math.radians(90 * side)); pl.keyframe_insert("rotation_euler", frame=F(hit_t))
    set_interp(pl, "location", F(hit_t), "BEZIER", "EASE_IN")
    show_at(pl, t0 - 0.1, hit_t + 0.1)
    W2.poof("splash", (loc[0], loc[1], 2.0), hit_t, s=6.0, n=9, seed=seed)
    W2.poof("splashb", (loc[0], loc[1] - 3, 4.0), hit_t + 0.08, s=4.0, n=7, seed=seed + 1)
    return pl


@S(21, 53, 56, "Один над морем: plane dives into the sea, big splash")
def s21(t0, t1):
    pl = crash_scene(t0, t1, t0 + 1.9, (0, 30, 0), 1, 1)
    cam = Cam()
    cam.key(t0, (-20, -10, 14), (-6, 30, 22), lens=24, focus=45.0, fstop=4)
    cam.key(t0 + 1.9, (-14, -6, 6), (0, 30, 6), lens=30, focus=42.0, fstop=4, ease="EASE_IN")
    cam.key(t1, (-12, -4, 7), (0, 30, 8), lens=30, focus=42.0, fstop=4)
    cam.handheld(1.1)
    boom_fx(cam, t0 + 1.9, 1.0)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 1.9, "boom", 1.0)
    sfx(t0 + 1.95, "splash", 1.0)


@S(22, 56, 58, "потом второй: second plane, other angle, splash")
def s22(t0, t1):
    pl = crash_scene(t0, t1, t0 + 1.0, (10, 34, 0), -1, 4)
    cam = Cam()
    cam.key(t0, (30, -6, 10), (14, 34, 18), lens=24, focus=45.0, fstop=4, roll=-5)
    cam.key(t1, (24, 0, 4), (10, 34, 5), lens=28, focus=40.0, fstop=4, roll=-8, ease="EASE_IN")
    cam.handheld(1.4)
    boom_fx(cam, t0 + 1.0, 1.0)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 1.0, "boom", 1.0)
    sfx(t0 + 1.05, "splash", 1.0)


@S(23, 58, 60, "Ни бури: storm cloud crossed out")
def s23(t0, t1):
    W.sky(0.8, (0.05, 0.07, 0.15), (0.25, 0.3, 0.4))
    W.sun(0.8)
    root = W.cloud("storm", (0, 10, 6), 1.6)
    for ob in root.children:
        ob.data.materials.clear(); ob.data.materials.append(M("#3a3f4c", 0.9))
    zap = box("zap", (0.5, 0.3, 7), (0, 7.5, 3.0), EM("#fff060", 8), 0.05, rot=(0, 18, 0))
    show_at(zap, t0 + 0.05, t0 + 0.35)
    x1 = box("x1", (0.9, 0.4, 7), (0, 5.0, 6.0), EM("#ff2a2a", 5), 0.05, rot=(0, 45, 0))
    x2 = box("x2", (0.9, 0.4, 7), (0, 5.0, 6.0), EM("#ff2a2a", 5), 0.05, rot=(0, -45, 0))
    for o in (x1, x2):
        pop(o, t0 + 0.55, 1.0)
    cam = cpush(t0, t1, (0, 8, 6), 24, 15, lens=26, shake=1.4)
    impact(cam, t0 + 0.55, 0.5)
    sfx(t0 + 0.05, "zap", 0.7)
    sfx(t0 + 0.55, "thud", 0.9)


@S(24, 60, 63, "ни ошибки пилота: calm pilot on the apron, red X")
def s24(t0, t1):
    ground_runway()
    sky_set(seed=11)
    W2.airliner("jet", (0, 44, 4.2), rot=0, scale=1.0)
    p = story.pilot(t0, t1, "smile")
    p.pose(t0, loc=(0, 0, 0), rot=0)
    p.act(t0 + 0.2, "cross", expr="smile")
    lips(p, t0, t0 + 0.8)
    p.act(t0 + 0.9, "shrug", expr="smile")
    cam = cfree([(t0, (3.5, -10, 3.4), (0, 0, 4.4), 30), (t1, (-2.5, -7.5, 5.0), (0, 0, 4.6), 36)], shake=1.0)
    x1 = box("x1", (0.8, 0.3, 4.6), (0, -1.6, 4.8), EM("#ff2a2a", 6), 0.05, rot=(0, 45, 0))
    x2 = box("x2", (0.8, 0.3, 4.6), (0, -1.6, 4.8), EM("#ff2a2a", 6), 0.05, rot=(0, -45, 0))
    for o in (x1, x2):
        pop(o, t0 + 1.3, 1.0)
    sfx(t0 + 1.3, "thud", 0.8)
    sfx(t0 + 1.3, "sting", 0.5)


# ---------------- act 4: investigation
@S(25, 63, 66, "Следователи доставали обломки: boat in debris field")
def s25(t0, t1):
    W.sky(1.0, (0.35, 0.55, 0.85), (0.8, 0.88, 0.95)); W.sun(2.6)
    ocean()
    debris("d", 22, (0, 12), 14, seed=2)
    b = boat("boat", (0, 10, 0), rot=15)
    for i in range(2):
        iv = invest(i, t0, t1, "worried")
        iv.pose(t0, loc=(-0.8 + i * 1.6, 6.5 + i * 2.5, 1.4), rot=15 + 150 + i * 40)
        iv.act(t0 + 0.2 + i * 0.2, "reach", expr="worried")
    cam = corbit(t0, t1, (0, 10, 2.5), 24, -40, 30, pitch=14, lens=26, shake=1.2)
    sfx(t0, "waves", 0.5, dur=t1 - t0 + 0.4)
    sfx(t0 + 0.8, "splash", 0.4)


@S(26, 66, 70, "из воды по кусочкам: pulling a fragment out, close")
def s26(t0, t1):
    W.sky(1.0, (0.35, 0.55, 0.85), (0.8, 0.88, 0.95)); W.sun(2.6)
    ocean()
    debris("d", 12, (0, 6), 6, seed=7)
    iv = invest(1, t0, t1, "worried")
    iv.pose(t0, loc=(0, 4, 0.9), rot=0, armL=(70, 6), armR=(70, 6))
    iv.pose(t0 + 0.6, armL=(80, 10), armR=(80, 10))
    iv.act(t0 + 0.6, "reach", expr="worried")
    frag = box("frag", (2.4, 0.15, 1.6), (0.8, 2.8, 0.5), M("#e8ecf0", 0.3, metal=0.7), 0.05)
    frag.keyframe_insert("location", frame=F(t0))
    frag.location = (0.6, 2.9, 3.6); frag.keyframe_insert("location", frame=F(t0 + 1.3))
    set_interp(frag, "location", F(t0 + 1.3), "BEZIER", "EASE_OUT")
    frag.rotation_euler = (0.3, 0.2, 0.4); frag.keyframe_insert("rotation_euler", frame=F(t0 + 1.3))
    cam = Cam()
    cam.key(t0, (4, -4, 0.8), (0.8, 3.0, 1.0), lens=30, focus=8.0, fstop=3)
    cam.key(t1, (-1, -3, 4.0), (0.6, 3.0, 3.4), lens=34, focus=7.0, fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.8, "splash", 0.7)
    sfx(t0 + 1.3, "clink", 0.7)


@S(27, 70, 74, "Они построили огромный бак: tilt up the huge tank")
def s27(t0, t1):
    T = tank_set()
    for i in range(2):
        iv = invest(i, t0, t1, "gasp")
        iv.pose(t0, loc=(-4 + i * 8, -4, 0), rot=0)
        iv.act(t0 + 0.3 + i * 0.2, "shock", expr="gasp")
    cam = Cam()
    cam.key(t0, (0, -12, 1.0), (0, 10, 2.0), lens=22, focus=24.0, fstop=4)
    cam.key(t1, (0, -16, 2.0), (0, 10, 10.0), lens=22, focus=28.0, fstop=4, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "rumble", 0.6, dur=t1 - t0)
    sfx(t0 + 0.2, "whoosh", 0.7)
    sfx(t0 + 1.2, "thud", 0.7)


@S(28, 74, 77, "И снова и: pressure gauge, needle swings")
def s28(t0, t1):
    T = tank_set()
    pv = T["pivot"]
    pv.rotation_euler[1] = math.radians(-110); pv.keyframe_insert("rotation_euler", index=1, frame=F(t0))
    pv.rotation_euler[1] = math.radians(60); pv.keyframe_insert("rotation_euler", index=1, frame=F(t0 + 0.5))
    pv.rotation_euler[1] = math.radians(-100); pv.keyframe_insert("rotation_euler", index=1, frame=F(t1))
    cam = cpush(t0, t1, (-15, -1.2, 4.6), 5.0, 3.4, yaw=10, pitch=2, lens=34, shake=1.2, fstop=2.4)
    sfx(t0, "tick", 0.6)
    sfx(t0 + 0.4, "tick", 0.6)


@S(29, 77, 80, "снова проверяли целый: fuselage section lowered/tested, bubbles")
def s29(t0, t1):
    T = tank_set()
    bubbles("bb", (0, 10, 2), (7, 3, 1), t0, t1, 30, seed=2)
    iv = invest(2, t0, t1, "determined")
    iv.pose(t0, loc=(8, -3, 0), rot=facing((8, -3), (0, 10)))
    iv.act(t0 + 0.3, "point", expr="determined")
    cam = cfree([(t0, (-8, -14, 3.0), (-2, 10, 5.0), 24), (t1, (6, -10, 8.5), (0, 10, 6.0), 24)], shake=1.2)
    sfx(t0, "bubbles", 0.7, dur=t1 - t0)
    sfx(t0 + 0.1, "whoosh", 0.5)


@S(30, 80, 83, "корпус давлением воды: hull flexes, gauge to red, creak")
def s30(t0, t1):
    T = tank_set()
    bubbles("bb", (0, 10, 2), (7, 3, 1), t0, t1, 36, seed=5)
    f = D.objects["tk_fus"]
    for k, s in enumerate((1.0, 0.94, 1.03, 0.92, 1.05)):
        f.scale = (1.0, s, s)
        f.keyframe_insert("scale", frame=F(t0 + k * (t1 - t0) / 5))
    pv = T["pivot"]
    pv.rotation_euler[1] = math.radians(-110); pv.keyframe_insert("rotation_euler", index=1, frame=F(t0))
    pv.rotation_euler[1] = math.radians(95); pv.keyframe_insert("rotation_euler", index=1, frame=F(t1))
    cam = Cam()
    cam.key(t0, (0, -9, 6.0), (0, 10, 5.4), lens=26, focus=19.0, fstop=3)
    cam.key(t1, (0, -3.5, 6.2), (0, 10, 5.6), lens=44, focus=13.5, fstop=3, ease="EASE_IN")
    cam.crash(t0 + 0.9, 26, 42, 0.16)
    cam.handheld(1.6)
    impact(cam, t0 + 0.9, 0.4)
    sfx(t0, "creak", 0.8)
    sfx(t0 + 0.9, "creak", 0.8)
    sfx(t0, "riser", 0.4)


@S(31, 83, 87, "В итоге нашли причину: investigator spots something, ding")
def s31(t0, t1):
    T = tank_set()
    iv = invest(0, t0, t1, "sus")
    iv.pose(t0, loc=(-2, -2, 0), rot=facing((-2, -2), (0, 10)))
    iv.act(t0 + 0.1, "lean", expr="sus")
    iv.act(t0 + 1.0, "shock", expr="gasp")
    lips(iv, t0 + 1.1, t1)
    lens_glass = EM("#fff4a0", 5)
    sp = sphere("alertbulb", 0.5, (-2, -2, 8.0), lens_glass, seg=12)
    show_at(sp, t0 + 1.0, t1)
    cam = cfree([(t0, (-9, -10, 3.5), (-2, -2, 4.0), 26), (t1, (-4, -5, 4.6), (-2, -2, 4.6), 38)], shake=1.1)
    sfx(t0 + 1.0, "correct", 0.9)
    sfx(t0 + 1.0, "gasp", 0.5)


@S(32, 87, 90, "Трещину, которая начиналась: macro crack grows from the corner")
def s32(t0, t1):
    Wn = window_set(False)
    rivets("rv", Wn["ctr"], Wn["size"], Wn["inner"], coll=Wn["coll"])
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    cor = cp[3]
    crack("ck", (cor[0], cor[1] - 0.35, cor[2]), (1, 0, 0.6), 5.0, t0 + 0.25, t1 - 0.1, n=14, seed=3)
    cam = Cam()
    cam.key(t0, (3.8, -8.0, 7.5), (cor[0], cor[1], cor[2]), lens=30, focus=8.0, fstop=2.8)
    cam.key(t1, (4.2, -3.2, 7.6), (cor[0] + 1.5, cor[1], cor[2] + 0.5), lens=46, focus=3.4, fstop=2.8, ease="EASE_IN")
    cam.crash(t0 + 0.25, 30, 46, 0.16)
    cam.handheld(1.4)
    sfx(t0 + 0.25, "crack", 1.0)
    sfx(t0 + 0.7, "crack", 0.8)
    impact(cam, t0 + 0.25, 0.25)


@S(33, 90, 93, "в углу окна: orbit square window, corner ring highlight")
def s33(t0, t1):
    Wn = window_set(False)
    rivets("rv", Wn["ctr"], Wn["size"], Wn["inner"], coll=Wn["coll"])
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    for i, c in enumerate(cp):
        r = cyl(f"hr{i}", 1.1, 0.06, (c[0], c[1] - 0.45, c[2]), EM("#ff4a1a", 6), 32, rot=(90, 0, 0))
        r2 = cyl(f"hr2{i}", 0.85, 0.07, (c[0], c[1] - 0.47, c[2]), M("#0b0d12", 0.9), 32, rot=(90, 0, 0))
        show_at(r, t0 + 0.2 + 0.12 * i); show_at(r2, t0 + 0.2 + 0.12 * i)
        sfx(t0 + 0.2 + 0.12 * i, "tick", 0.5)
    cam = Cam()
    cam.key(t0, (-9, -11, 9.0), (0, 0, 5), lens=28, focus=14.0, fstop=3, roll=-4)
    cam.key(t1, (9, -11, 1.5), (0, 0, 5), lens=28, focus=14.0, fstop=3, roll=4, ease="EASE_IN_OUT")
    cam.handheld(1.0)


@S(34, 93, 97, "В полёте корпус самолёта: airliner cruising, orbit")
def s34(t0, t1):
    sky_set(sun_s=4.5, seed=8)
    pl = W2.airliner("jet", (0, 0, 40), rot=0, scale=1.0)
    slide(pl, t0, t1, (0, 20, 40), (0, -20, 40), "LINEAR")
    cam = Cam()
    cam.orbit(t0, t1, (0, 0, 40), 38, -80, -20, pitch=8, lens=28, steps=4, fstop=4)
    cam.handheld(1.0)
    sfx(t0, "jet", 0.6, dur=t1 - t0)
    sfx(t0 + 0.1, "whoosh", 0.5)


@S(35, 97, 99, "тысячи раз: x1000 counter pops")
def s35(t0, t1):
    sky_set(sun_s=4.5, seed=8)
    pl = W2.airliner("jet", (0, 0, 40), rot=0, scale=1.0)
    pl.rotation_euler[0] = math.radians(2)
    for k in range(3):
        o = text(f"x{k}", "x1000", (0, -9 - k * 0.1, 46), 7.0 - k, EM("#ffe14a", 6), rot=(90, 0, 0), extrude=0.4)
        show_at(o, t0 + 0.12 + k * 0.1, t0 + 0.3 + k * 0.1 if k < 2 else None)
    cam = cpush(t0, t1, (0, 0, 42), 30, 18, yaw=-20, pitch=6, lens=30, yaw1=10, shake=1.4)
    sfx(t0 + 0.12, "pop", 0.8)
    sfx(t0 + 0.22, "pop", 0.8)
    sfx(t0 + 0.32, "pop", 0.8)


@S(36, 99, 102, "сжимается и растягивается: fuselage pulses, camera whips")
def s36(t0, t1):
    W.sky(1.0, (0.03, 0.1, 0.5), (0.2, 0.45, 0.95)); W.sun(3.5)
    pl = W2.airliner("jet", (0, 0, 30), rot=0, scale=1.0)
    for k in range(6):
        t = t0 + k * (t1 - t0) / 6
        sy = (1.0, 0.88, 1.12)[k % 3]
        pl.scale = (1.0 / sy ** 0.5, sy, 1.0 / sy ** 0.5)
        pl.keyframe_insert("scale", frame=F(t))
    cam = Cam()
    cam.whip(t0, t0 + 0.3, (-26, -34, 36), (0, 0, 30), (24, -30, 24), (0, 0, 30), lens=26, whoosh=False)
    cam.key(t1, (10, -34, 28), (0, 0, 30), lens=30, focus=34.0, fstop=4, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.1, "whoosh", 0.7)
    sfx(t0 + 0.3, "creak", 0.6)
    sfx(t0 + 1.0, "creak", 0.6)


@S(37, 102, 106, "И всё напряжение собирается: red stress lines converge to corners")
def s37(t0, t1):
    Wn = window_set(False)
    rivets("rv", Wn["ctr"], Wn["size"], Wn["inner"], coll=Wn["coll"])
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    rnd = random.Random(4)
    for i in range(18):
        a = math.tau * i / 18
        far = (Wn["ctr"][0] + math.cos(a) * 9.0, Wn["ctr"][1] - 0.4, Wn["ctr"][2] + math.sin(a) * 6.0)
        tgt = cp[min(range(4), key=lambda j: (cp[j][0] - far[0]) ** 2 + (cp[j][2] - far[2]) ** 2)]
        ln = glow_line(f"sl{i}", far, (tgt[0], tgt[1] - 0.1, tgt[2]), 0.06, "#ff5a20", 7.0, t_on=t0 + 0.04 * i)
    cam = Cam()
    cam.key(t0, (0, -16, 5.5), (0, 0, 5), lens=28, focus=16.0, fstop=3)
    cam.key(t1, (0, -9, 5.5), (0, 0, 5), lens=34, focus=9.0, fstop=3, ease="EASE_IN")
    cam.handheld(1.5)
    sfx(t0, "riser", 0.8, dur=t1 - t0)
    sfx(t0 + 0.4, "tick", 0.5)
    sfx(t0 + 0.9, "tick", 0.5)


@S(38, 106, 109, "в острых углах: corner extreme close-up, red pulse, crash zoom")
def s38(t0, t1):
    Wn = window_set(False)
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    cor = cp[1]
    g = sphere("cg", 0.9, (cor[0], cor[1] - 0.4, cor[2]), EM("#ff4a1a", 14), seg=16)
    g.scale = (0.6,) * 3; g.keyframe_insert("scale", frame=F(t0))
    g.scale = (1.4,) * 3; g.keyframe_insert("scale", frame=F(t0 + 0.4))
    g.scale = (0.7,) * 3; g.keyframe_insert("scale", frame=F(t0 + 0.8))
    g.scale = (1.6,) * 3; g.keyframe_insert("scale", frame=F(t1))
    for i in range(6):
        glow_line(f"sl{i}", (cor[0] + (i - 3) * 1.4, cor[1] - 0.4, cor[2] - 4.0 + i * 0.3), (cor[0], cor[1] - 0.4, cor[2]), 0.05, "#ff7a30", 6.0)
    cam = Cam()
    cam.key(t0, (cor[0] + 3.0, -5.5, cor[2] + 1.2), (cor[0], cor[1], cor[2]), lens=40, focus=6.0, fstop=2.0)
    cam.key(t1, (cor[0] + 0.6, -2.4, cor[2] + 0.3), (cor[0], cor[1], cor[2]), lens=70, focus=2.4, fstop=2.0, ease="EASE_IN")
    cam.crash(t0 + 0.35, 40, 62, 0.12)
    cam.handheld(1.8)
    sfx(t0 + 0.1, "heartbeat", 0.9)
    sfx(t0 + 0.8, "heartbeat", 1.0)


@S(39, 109, 112, "Оно копится там: glow builds, camera trembles")
def s39(t0, t1):
    Wn = window_set(False)
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    cor = cp[3]
    for k in range(5):
        sp = sphere(f"gl{k}", 0.4 + k * 0.1, (cor[0] + 0.3 * k, cor[1] - 0.4, cor[2] + 0.1 * k), EM("#ff4a1a", 8 + k * 3), seg=12)
        show_at(sp, t0 + k * 0.18)
    crack("hair", (cor[0], cor[1] - 0.35, cor[2]), (1, 0, 0.5), 2.4, t0 + 0.2, t1, n=8, seed=9)
    cam = Cam()
    cam.key(t0, (cor[0] + 2, -5.0, cor[2] + 1), (cor[0], cor[1], cor[2]), lens=44, focus=5.0, fstop=2.2)
    cam.key(t1, (cor[0] + 1, -3.0, cor[2] + 0.4), (cor[0] + 0.8, cor[1], cor[2] + 0.3), lens=58, focus=3.2, fstop=2.2, ease="EASE_IN")
    cam.handheld(2.4)
    sfx(t0, "riser", 0.9, dur=t1 - t0)
    sfx(t0 + 0.2, "creak", 0.7)


@S(40, 112, 116, "пока металл не порвётся: crack runs, plate rips, boom")
def s40(t0, t1):
    Wn = window_set(False)
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    cor = cp[3]
    end = crack("rip", (cor[0], cor[1] - 0.35, cor[2]), (1, 0, 0.4), 9.0, t0, t0 + 1.0, n=16, w=0.12, seed=6)
    spark = sphere("burst", 1.6, (end[0], end[1] - 0.6, end[2]), EM("#fff0a0", 20), seg=12)
    show_at(spark, t0 + 1.0, t0 + 1.16)
    cam = Cam()
    cam.key(t0, (cor[0] + 2, -7, cor[2] + 1), (cor[0] + 2, cor[1], cor[2]), lens=28, focus=7.0, fstop=3)
    cam.key(t0 + 1.0, (cor[0] + 6, -6.0, cor[2] + 2.5), (cor[0] + 5, cor[1], cor[2] + 1.0), lens=30, focus=6.0, fstop=3)
    cam.key(t1, (cor[0] + 7, -9, cor[2] + 3), (cor[0] + 5, cor[1], cor[2] + 1.0), lens=26, focus=9.0, fstop=3, ease="EASE_OUT")
    cam.handheld(1.8)
    boom_fx(cam, t0 + 1.0, 1.2)
    sfx(t0, "crack", 0.9, dur=0.9)
    sfx(t0 + 1.0, "rip", 1.0)
    sfx(t0 + 1.0, "boom", 1.0)


# ---------------- act 5: round window
@S(41, 116, 119, "В круглом окне: round window, calm light, ding")
def s41(t0, t1):
    Wn = window_set(True, light_col=(0.9, 0.97, 1.0))
    rivets("rv", Wn["ctr"], Wn["size"], Wn["inner"], coll=Wn["coll"])
    cam = Cam()
    cam.key(t0, (0, -3.0, 5), (0, 0, 5), lens=70, focus=5.5, fstop=3)
    cam.key(t1, (0, -11, 5), (0, 0, 5), lens=36, focus=13.0, fstop=3, ease="EASE_OUT")
    cam.handheld(0.6)
    sfx(t0 + 0.02, "ding", 0.9)
    sfx(t0, "whoosh", 0.7)


@S(42, 119, 121, "углов нет: orbit round window, no corners")
def s42(t0, t1):
    Wn = window_set(True, light_col=(0.9, 0.97, 1.0))
    rivets("rv", Wn["ctr"], Wn["size"], Wn["inner"], coll=Wn["coll"])
    ring = cyl("ringglow", Wn["inner"] + 0.15, 0.05, (0, -0.4, 5), EM("#6ad0ff", 4), 64, rot=(90, 0, 0))
    ring2 = cyl("ringglow2", Wn["inner"] - 0.1, 0.06, (0, -0.42, 5), mat("wn_skym2", (0.35, 0.6, 1.0), emit=(0.35, 0.6, 1.0), estr=2.2), 64, rot=(90, 0, 0))
    show_at(ring, t0 + 0.25); show_at(ring2, t0 + 0.25)
    cam = Cam()
    cam.orbit(t0, t1, (0, 0, 5), 11, -35, 35, pitch=4, lens=30, steps=3, fstop=3)
    cam.handheld(0.7)
    sfx(t0 + 0.25, "sparkle", 0.7)


def flow_particles(Wn, t0, t1, n_lines=11, seed=0):
    """cyan particles flowing left->right around the round window (potential flow around a cylinder)."""
    Rr = Wn["inner"] + 0.35
    rnd = random.Random(seed)
    Mc = EM("#7ae0ff", 9)
    cx, cz = 0.0, 5.0

    def streamline_y(x, h):
        y = h
        for _ in range(12):
            r2 = x * x + y * y
            f = y * (1 - Rr * Rr / r2) - h
            df = (1 - Rr * Rr / r2) + 2 * y * y * Rr * Rr / (r2 * r2)
            y -= f / df if abs(df) > 1e-6 else 0
        return y

    for i in range(n_lines):
        h = (i - (n_lines - 1) / 2) * 1.05
        if abs(h) < Rr * 0.18:
            h = Rr * 0.2 * (1 if h >= 0 else -1)
        for j in range(3):
            o = sphere(f"fl{i}_{j}", 0.17, (-10, -0.5, cz + h), Mc, (2.4, 0.6, 0.6), seg=8)
            ts = t0 + rnd.uniform(0, 0.4) + j * (t1 - t0) * 0.28
            steps = 18
            for k in range(steps + 1):
                x = -10 + 20 * k / steps
                y = streamline_y(x if abs(x) > 1e-3 else 1e-3, h)
                o.location = (cx + x, -0.5, cz + y)
                o.keyframe_insert("location", frame=F(ts + (t1 - t0) * 0.75 * k / steps))
                set_interp(o, "location", F(ts + (t1 - t0) * 0.75 * k / steps), "LINEAR")
            show_at(o, ts)


@S(43, 121, 125, "И напряжение обтекает его: stress flows smoothly around the round window")
def s43(t0, t1):
    Wn = window_set(True, light_col=(0.9, 0.97, 1.0))
    flow_particles(Wn, t0, t1, seed=2)
    cam = Cam()
    cam.key(t0, (-3, -11, 4.0), (0, 0, 5), lens=28, focus=12.0, fstop=3)
    cam.key(t1, (4, -9.5, 6.0), (0, 0, 5), lens=28, focus=10.0, fstop=3, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "swoosh", 0.7, dur=t1 - t0)
    sfx(t0 + 0.1, "sparkle", 0.5)


@S(44, 125, 128, "как вода камень: river water flows around a smooth rock")
def s44(t0, t1):
    W.sky(1.0, (0.2, 0.45, 0.85), (0.8, 0.9, 1.0)); W.sun(3.5)
    box("river", (60, 60, 0.4), (0, 10, -0.2), mat("riv_m", hexc("#2f93e0"), 0.1, emit=hexc("#2f93e0"), estr=0.25), 0)
    box("bankL", (14, 60, 1.6), (-20, 10, 0.4), M("#5a8a3a", 0.9), 0.2)
    box("bankR", (14, 60, 1.6), (20, 10, 0.4), M("#5a8a3a", 0.9), 0.2)
    rock = sphere("rock", 2.6, (0, 10, 0.2), M("#8c8f96", 0.9), (1.2, 1.0, 0.8), seg=24)
    Mc = EM("#d8f4ff", 3)
    rnd = random.Random(3)
    Rr = 3.2
    for i in range(14):
        h = (i - 6.5) * 1.15
        if abs(h) < 2.2 * 0.55:
            h = 1.3 * (1 if h >= 0 else -1)
        o = sphere(f"wp{i}", 0.3, (0, 0, 0.2), Mc, (1.0, 1.0, 0.4), seg=8)
        ts = t0 + rnd.uniform(0, 0.4)
        for k in range(15):
            y = -22 + 44 * k / 14
            x0 = h * (1 + Rr * Rr / (y * y + h * h + 0.01) * 0.0)
            yy = y
            xx = h
            # potential flow around a circle (flow along +Y)
            for _ in range(10):
                r2 = xx * xx + (yy) * (yy)
                f = xx * (1 - Rr * Rr / r2) - h
                df = (1 - Rr * Rr / r2) + 2 * xx * xx * Rr * Rr / (r2 * r2)
                xx -= f / df if abs(df) > 1e-6 else 0
            o.location = (xx, 10 + yy, 0.45)
            o.keyframe_insert("location", frame=F(ts + (t1 - t0) * 0.9 * k / 14))
        show_at(o, ts)
    cam = Cam()
    cam.key(t0, (-9, -6, 6.0), (0, 10, 0.8), lens=30, focus=18.0, fstop=3)
    cam.key(t1, (9, -3, 4.0), (0, 10, 0.8), lens=30, focus=18.0, fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "water", 0.8, dur=t1 - t0 + 0.2)


@S(45, 128, 131, "Поэтому окна на каждом: airliner with ROUND windows, fly-by")
def s45(t0, t1):
    sky_set(sun_s=4.5, seed=6)
    pl = W2.airliner("jet", (0, 0, 22), rot=0, scale=1.6)
    swap_windows("jet")
    cam = Cam()
    cam.key(t0, (-8, -24, 23.2), (-1, -18, 22), lens=34, focus=7.0, fstop=2.8)
    cam.key(t1, (-8, 20, 23.2), (-1, 14, 22), lens=34, focus=7.0, fstop=2.8, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "whoosh", 0.8)
    for k in range(5):
        sfx(t0 + 0.2 + k * 0.2, "pop", 0.3)


@S(46, 131, 134, "самолёте круглые: formation of planes, tilt up")
def s46(t0, t1):
    sky_set(sun_s=4.5, seed=9)
    for i, (x, y, z) in enumerate(((-30, 0, 38), (6, 14, 46), (36, -10, 34))):
        W2.airliner(f"jet{i}", (x, y, z), rot=90 - i * 6, scale=1.0)
        swap_windows(f"jet{i}")
        slide(D.objects[f"jet{i}"], t0, t1, (x, y, z), (x + 14, y, z), "LINEAR")
    cam = Cam()
    cam.key(t0, (0, -60, 20), (0, 10, 38), lens=24, focus=70.0, fstop=4)
    cam.key(t1, (6, -50, 34), (4, 10, 44), lens=24, focus=60.0, fstop=4, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "jet", 0.5, dur=t1 - t0)
    sfx(t0 + 0.2, "whoosh", 0.6)


@S(47, 134, 137, "В следующий раз, глядя: passenger by the window (cabin)")
def s47(t0, t1):
    c = collection("CAB")
    world((0.5, 0.55, 0.62), 0.4)
    box("cb_floor", (30, 40, 0.4), (0, 4, -0.2), M("#3a4a6a", 0.9), 0, coll=c)
    box("cb_ceil", (30, 40, 0.4), (0, 4, 14), M("#e9ebee", 0.6), 0, coll=c)
    box("cb_wallB", (40, 0.4, 20), (0, -14, 7), M("#d8dce2", 0.6), 0, coll=c)
    # side wall with round window at x=+6 (faces -X)
    plate = ring_plate("cb_wall", (22, 12), "round", 2.2, 0.6, M("#e9ebee", 0.45), loc=(6.0, 2.0, 6.0), coll=c)
    plate.rotation_euler = (math.radians(90), 0, math.radians(-90))   # normal toward -X
    card("cb_sky", 20, 14, (7.2, 2.0, 6.0), mat("cb_skym", (0.4, 0.7, 1.0), emit=(0.4, 0.7, 1.0), estr=3.0), "-X", coll=c)
    box("cb_seat", (2.4, 2.6, 0.7), (3.4, 2.0, 1.8), M("#2f5fb8", 0.6), 0.2, coll=c)
    box("cb_seatb", (0.6, 2.6, 3.8), (2.2, 2.0, 3.8), M("#2f5fb8", 0.6), 0.2, coll=c)
    p = pax(t0, t1, "neutral")
    p.pose(t0, loc=(3.4, 2.0, 1.8 - 1.96 + 0.2), rot=90, legL=(85, 3), legR=(85, -3), armL=(30, 6), armR=(30, 6))
    p.act(t0 + 0.2, "lean", expr="smile")
    p.look(t0 + 0.5, -35, 4)
    light("cb_k", "AREA", (-6, -6, 12), 3000, (1.0, 0.97, 0.92), 8, coll=c, target=(3, 2, 4))
    cam = cfree([(t0, (-1, -9, 6.4), (4.2, 2.0, 5.5), 28), (t1, (1.5, -5.5, 6.2), (5.0, 2.0, 5.8), 34)], shake=1.0)
    sfx(t0, "cabin", 0.4, dur=t1 - t0 + 0.5)
    sfx(t0 + 0.5, "ding", 0.4)


@S(48, 137, 140, "иллюминатор: push into the round window, clouds beyond")
def s48(t0, t1):
    Wn = window_set(True, light_col=(1.0, 0.95, 0.88))
    cam = Cam()
    cam.key(t0, (0, -9, 5), (0, 0, 5), lens=34, focus=10.0, fstop=3)
    cam.key(t1, (0, -2.6, 5), (0, 0, 5), lens=44, focus=3.6, fstop=3, ease="EASE_IN")
    cam.handheld(0.7)
    sfx(t0, "whoosh", 0.6)
    sfx(t0, "riser", 0.4, dur=t1 - t0)


@S(49, 140, 144, "помните, эта форма появилась: engineer proud at the blueprint, golden light")
def s49(t0, t1):
    office()
    e = eng(t0, t1, "smile")
    e.pose(t0, loc=(0, 4, 0), rot=0)
    e.act(t0 + 0.1, "cross", expr="smile")
    D.objects["of_bp"].data.materials.clear(); D.objects["of_bp"].data.materials.append(TX("plane_bp_round.png", 0.7, 0.45))
    light("gold", "SPOT", (-6, -6, 10), 9000, (1.0, 0.8, 0.5), 2, target=(0, 4, 4.5), spot=40)
    cam = corbit(t0, t1, (0, 4, 4.8), 8, -22, 18, pitch=-2, lens=34, pitch1=2, shake=0.8, fstop=2.6)
    sfx(t0, "sparkle", 0.5)


@S(50, 144, 148, "потому, что кто-то: square plate with crack, camera backs off")
def s50(t0, t1):
    Wn = window_set(False)
    cp = corner_pts(Wn["inner"], Wn["ctr"])
    cor = cp[3]
    crack("ck", (cor[0], cor[1] - 0.35, cor[2]), (1, 0, 0.6), 5.0, t0 - 0.0, t0 + 0.4, n=8, seed=3)
    cam = Cam()
    cam.key(t0, (cor[0] + 1.8, -4.0, cor[2] + 0.8), (cor[0] + 1.0, cor[1], cor[2] + 0.5), lens=44, focus=4.0, fstop=2.4)
    cam.key(t1, (-1, -13, 6), (0, 0, 5), lens=26, focus=13.0, fstop=2.4, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "heartbeat", 0.8)
    sfx(t0 + 0.9, "whoosh", 0.6)


@S(51, 148, None, "заплатил за углы: final pull-back from the round window, fade")
def s51(t0, t1):
    Wn = window_set(True, light_col=(1.0, 0.95, 0.9))
    rivets("rv", Wn["ctr"], Wn["size"], Wn["inner"], coll=Wn["coll"])
    cam = Cam()
    cam.key(t0, (0, -4.5, 5), (0, 0, 5), lens=42, focus=5.0, fstop=3)
    cam.key(t1, (0, -16, 5.5), (0, 0, 5), lens=30, focus=16.0, fstop=3, ease="EASE_OUT")
    cam.handheld(0.5)
    vs = bpy.context.scene.view_settings
    vs.exposure = 0.0; vs.keyframe_insert("exposure", frame=F(t1 - 0.9))
    vs.exposure = -9.0; vs.keyframe_insert("exposure", frame=F(t1 - 0.05))
    sfx(t0 + 0.1, "ding", 0.5)
    sfx(t0 + 0.8, "boom", 0.6)
