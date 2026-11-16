"""gary: "In this world every kid is born with a guardian monster under the bed." Shots keyed to script word indices."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, os, random
from mathutils import Vector

V = Video(__file__)
story.bind(V)
WY = sets.WALL_Y
BED = (-7.6, 0.3)            # front edge of the bed (x, y)
GAP = (-7.6, 0.28, 0.95)     # the dark gap "under" the bed
FONT = os.environ.get("TITAN_FONT", "/root/.fonts/TitanOne-Regular.ttf")


def rad(a):
    return math.radians(a)


# ------------------------------------------------------------------ cast
def mom(t0, t1, expr="smile"):
    return story._live(chars.Char("Mom", skin="#efd2b8", shirt="#e8788f", pants="#5a4a7a", hair="bob", hair_color="#6b3f27",
                                  face="girl", sleeves="long"), t0, t1, expr)


def sis(t0, t1, expr="neutral"):
    return story._live(chars.Char("Sis", skin="#f2dbc6", shirt="#ffd36b", pants="#e58fc0", hair="bun", hair_color="#c0793a",
                                  face="girl", sleeves="short", scale=0.78), t0, t1, expr)


def bully(t0, t1, expr="angry"):
    return story._live(chars.Char("Bully", skin="#d9b48f", shirt="#c23a3a", pants="#2a2d36", hair="buzz", hair_color="#2a1a10",
                                  face="villain", sleeves="short"), t0, t1, expr)


def eddie_pj(t0, t1, expr="neutral"):
    return story._live(chars.eddie(shirt="#f4a6c8", pants="#6f7fd8", vneck="#ffd0e4", bolt="#f2c14e"), t0, t1, expr)


def lie_in_bed(ch, t=0.0):
    ch.root.rotation_euler[0] = rad(-90)
    ch.pose(t, loc=(BED[0], 3.2, 3.2), rot=0, armL=(0, 8), armR=(0, 8))


# ------------------------------------------------------------------ monsters
def _eye(name, c, x, z, r, glow, parent):
    Mw = mat("eye_w" + ("g" if glow else ""), hexc("#fffbe0") if glow else hexc("#ffffff"), 0.3,
             emit=hexc("#fff0a0") if glow else None, estr=5.0 if glow else 0.0)
    y = -math.sqrt(max(1.0 - (x * x + z * z) / (2.3 * 2.3), 0.05)) * 1.75
    sphere(name, r, (x, y, z), Mw, parent=parent, coll=c, seg=20)
    sphere(name + "_p", r * 0.5, (x * 0.96, y - r * 0.82, z - 0.02), mat("pupil", hexc("#15101a"), 0.2),
           parent=parent, coll=c, seg=12)
    sphere(name + "_h", r * 0.16, (x * 0.96 + 0.1, y - r * 1.2, z + 0.12), mat("pupil_hl", (1, 1, 1), 0.2, emit=(1, 1, 1), estr=3),
           parent=parent, coll=c, seg=8)


def gary(name="Gary", loc=(0, 0, 0), rot=0, scale=1.0, glow=False, hat=False, tears=False, bag=False):
    c = collection("MO_" + name)
    fur = mat("gfur", hexc("#8a5cc4"), 0.95)
    fur2 = mat("gbelly", hexc("#d6b8f4"), 0.95)
    dark = mat("gdark", hexc("#4a2a78"), 0.9)
    root = empty(name + "_root", loc, None, c, (0, 0, rot), 0.8)
    root.scale = (scale,) * 3
    sphere(name + "_body", 2.0, (0, 0, 3.0), fur, (1.2, 0.95, 1.3), parent=root, coll=c)
    sphere(name + "_belly", 1.3, (0, -1.25, 2.8), fur2, (1.0, 0.45, 1.15), parent=root, coll=c)
    rnd = random.Random(5)
    for i in range(16):
        a = rnd.uniform(0, math.tau)
        z = rnd.uniform(1.6, 4.6)
        cyl(f"{name}_tuft{i}", 0.28, 0.9, (math.cos(a) * 2.25, math.sin(a) * 1.85, z), dark, 6, parent=root, coll=c, r2=0.02,
            rot=(rnd.uniform(-30, 30), rnd.uniform(-30, 30), 0))
    head = empty(name + "_head", (0, 0, 5.9), root, c)
    sphere(name + "_skull", 1.75, (0, 0, 0), fur, (1.15, 1.0, 0.95), parent=head, coll=c, seg=32)
    for sx in (-1, 1):
        cyl(f"{name}_horn{sx}", 0.38, 1.4, (sx * 1.05, 0.0, 1.75), mat("ghorn", hexc("#f4e4b8"), 0.4), 12, parent=head, coll=c,
            r2=0.03, rot=(0, sx * 22, 0))
        sphere(f"{name}_ear{sx}", 0.5, (sx * 1.85, 0.2, 0.2), fur, (0.5, 0.8, 1.0), parent=head, coll=c, seg=12)
    pos = [(-0.62, 0.0), (0.0, 0.0), (0.62, 0.0), (-0.34, 0.55), (0.34, 0.55), (-0.34, -0.55), (0.34, -0.55)]
    for i, (x, z) in enumerate(pos):
        _eye(f"{name}_eye{i}", c, x * 1.5, z * 1.5 + 0.35, 0.33, glow, head)
    sphere(name + "_nose", 0.28, (0, -1.72, -0.55), mat("gnose", hexc("#2a1a40"), 0.4), (1.2, 0.8, 0.8), parent=head, coll=c)
    sphere(name + "_mouth", 0.7, (0, -1.35, -0.95), mat("gmouth", hexc("#2a0e28"), 0.5), (1.1, 0.35, 0.5), parent=head, coll=c)
    for sx in (-1, 1):
        cyl(f"{name}_tusk{sx}", 0.1, 0.5, (sx * 0.55, -1.52, -0.8), mat("gtusk", hexc("#fffbe8"), 0.3), 8, parent=head, coll=c,
            r2=0.01)
    arms = []
    for sx in (-1, 1):
        sh = empty(f"{name}_sh{sx}", (sx * 2.45, 0, 4.2), root, c)
        cyl(f"{name}_arm{sx}", 0.6, 2.8, (0, 0, -1.4), fur, 14, parent=sh, coll=c)
        sphere(f"{name}_hand{sx}", 0.75, (0, 0, -2.9), fur, parent=sh, coll=c, seg=16)
        arms.append(sh)
    for sx in (-1, 1):
        cyl(f"{name}_leg{sx}", 0.85, 1.9, (sx * 1.0, 0, 0.95), fur, 14, parent=root, coll=c)
        box(f"{name}_foot{sx}", (1.5, 1.9, 0.55), (sx * 1.0, -0.4, 0.28), dark, 0.2, parent=root, coll=c)
    if hat:
        Mh = mat("hardhat", hexc("#f5c518"), 0.4)
        cyl(name + "_hat", 1.5, 0.5, (0, 0, 1.55), Mh, 24, parent=head, coll=c)
        sphere(name + "_hat2", 1.4, (0, 0, 1.6), Mh, (1, 1, 0.6), parent=head, coll=c)
    if bag:
        sh = arms[0]
        box(name + "_suit", (1.7, 0.6, 1.3), (0, -0.2, -3.3), mat("suitcase", hexc("#b8473a"), 0.5), 0.1, parent=sh, coll=c)
        box(name + "_suith", (0.6, 0.15, 0.2), (0, -0.2, -2.55), mat("suitcase_h", hexc("#222222"), 0.4), 0.04, parent=sh, coll=c)
    if tears:
        Mt = mat("tear", hexc("#7fc8ff"), 0.1, emit=hexc("#7fc8ff"), estr=1.5)
        for i, (x, z) in enumerate(pos):
            sphere(f"{name}_tear{i}", 0.17, (x * 1.5, -1.5, z * 1.5 + 0.0), Mt, (1, 1, 1.6), parent=head, coll=c, seg=8)
    return dict(root=root, head=head, arms=arms, coll=c)


def nm(name="Nm", loc=(0, 0, 0), rot=0, scale=1.0):
    """the new monster: black-teal, red eyes, THREE rows of teeth."""
    c = collection("MO_" + name)
    body = mat("nbody", hexc("#1b2a3c"), 0.6)
    rim = mat("nrim", hexc("#2f6f7a"), 0.5)
    root = empty(name + "_root", loc, None, c, (0, 0, rot), 0.8)
    root.scale = (scale,) * 3
    sphere(name + "_body", 1.7, (0, 0.2, 2.7), body, (1.0, 0.9, 1.4), parent=root, coll=c)
    head = empty(name + "_head", (0, -0.2, 5.5), root, c)
    sphere(name + "_skull", 1.7, (0, 0, 0), body, (1.35, 1.0, 1.0), parent=head, coll=c, seg=32)
    Me = mat("nredeye", hexc("#ff2a2a"), 0.2, emit=hexc("#ff2020"), estr=9.0)
    for sx in (-1, 1):
        sphere(f"{name}_eye{sx}", 0.5, (sx * 0.8, -1.45, 0.55), Me, (1.0, 0.7, 0.9), parent=head, coll=c, seg=16)
        cyl(f"{name}_spike{sx}", 0.3, 1.3, (sx * 1.2, 0, 1.55), rim, 8, parent=head, coll=c, r2=0.02, rot=(0, sx * 25, 0))
    sphere(name + "_mouth", 1.0, (0, -1.25, -0.55), mat("nmouth", hexc("#14040a"), 0.5), (1.5, 0.4, 0.62), parent=head, coll=c)
    Mt = mat("nteeth", hexc("#fffff0"), 0.3)
    for row, (yy, zz, up) in enumerate(((-1.62, -0.28, -1), (-1.62, -0.88, 1), (-1.38, -0.58, -1))):
        n = 11 if row < 2 else 9
        for i in range(n):
            x = (i / (n - 1) - 0.5) * 2.5
            cyl(f"{name}_t{row}_{i}", 0.12, 0.42, (x, yy - abs(x) * 0.06, zz), Mt, 6, parent=head, coll=c, r2=0.01,
                rot=(0, 0, 180 if up < 0 else 0))
    arms = []
    for sx in (-1, 1):
        sh = empty(f"{name}_sh{sx}", (sx * 2.1, 0.1, 4.0), root, c)
        cyl(f"{name}_arm{sx}", 0.4, 3.4, (0, 0, -1.7), body, 12, parent=sh, coll=c)
        for k in (-1, 0, 1):
            cyl(f"{name}_claw{sx}{k}", 0.1, 0.9, (k * 0.25, -0.1, -3.6), mat("nclaw", hexc("#e8e8e0"), 0.3), 6, parent=sh, coll=c,
                r2=0.01, rot=(180, 0, 0))
        arms.append(sh)
    for sx in (-1, 1):
        cyl(f"{name}_leg{sx}", 0.6, 2.0, (sx * 0.9, 0, 1.0), body, 12, parent=root, coll=c)
    tail = empty(name + "_tail", (0, 1.7, 1.3), root, c)
    cyl(name + "_tailc", 0.35, 3.2, (0, 1.4, 0), body, 12, parent=tail, coll=c, r2=0.1, rot=(-90, 0, 0))
    sphere(name + "_tailtip", 0.45, (0, 3.1, 0), rim, parent=tail, coll=c)
    return dict(root=root, head=head, arms=arms, tail=tail, coll=c)


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


def stink(prefix, loc, t0, t1, n=9, seed=1):
    rnd = random.Random(seed)
    M = mat("stink", hexc("#7fd24a"), 0.9, emit=hexc("#6fc83a"), estr=0.7, alpha=0.55)
    for i in range(n):
        p = Vector(loc) + Vector((rnd.uniform(-1.5, 1.5), rnd.uniform(-1.2, 0.2), rnd.uniform(-0.4, 0.8)))
        ob = sphere(f"{prefix}{i}", rnd.uniform(0.45, 0.8), tuple(p), M, seg=12)
        ob.scale = (0.05,) * 3
        d = rnd.uniform(0, 0.4)
        ob.keyframe_insert("scale", frame=F(t0 + d))
        ob.keyframe_insert("location", frame=F(t0 + d))
        ob.scale = (1.1,) * 3
        ob.keyframe_insert("scale", frame=F(t0 + d + 0.6))
        ob.location = tuple(p + Vector((rnd.uniform(-0.6, 0.6), 0, 3.0)))
        ob.keyframe_insert("location", frame=F(t1))
        ob.scale = (0.05,) * 3
        ob.keyframe_insert("scale", frame=F(t1))


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


# ------------------------------------------------------------------ sets
def night_room():
    world((0.08, 0.1, 0.24), 0.5)
    A = sets.bedroom(night=True)
    light("nfill", "AREA", (0, -12.5, 12), 9000, (0.8, 0.82, 1.0), 14, target=(0, 0, 3))
    m = sets.MIRROR
    box("hole_cover", (m["w"] + 0.5, 0.2, m["h"] + 0.5), (m["x"], WY - 0.1, m["z"]), mat("hole_cov", hexc("#5a6a96"), 0.35), 0.02)
    locs.window("win", 10.8, -3.0, 7.8, 4.6, 5.0, A["static"], facing="-X", sky=(0.10, 0.16, 0.42), estr=1.4)
    box("bed_gap", (5.2, 0.1, 1.15), (GAP[0], 0.42, GAP[2]), mat("gapblack", (0.0, 0.0, 0.0), 1.0), 0.0)
    return A


def day_house():
    W.sky(1.0)
    W.sun(4.0, rot=(52, 0, 30))
    box("ground", (240, 240, 0.4), (0, 0, -0.2), mat("lawn", hexc("#6fc050"), 0.9), 0)
    box("path", (4.4, 14, 0.06), (0, -2, 0.04), mat("pathc", hexc("#d9cfba"), 0.8), 0.02)
    box("house", (22, 12, 13), (0, 14, 6.5), mat("house_wall", hexc("#f2c14e"), 0.7), 0.2)
    box("roof", (24.6, 14.6, 2.0), (0, 14, 14.2), mat("house_roof", hexc("#a33b2f"), 0.7), 0.3)
    box("door", (4.0, 0.3, 7.2), (0, 7.85, 3.6), mat("door_c", hexc("#b8312a"), 0.5), 0.1)
    box("step", (6.0, 2.2, 0.6), (0, 6.6, 0.3), mat("step_c", hexc("#c8c2b4"), 0.8), 0.1)
    for sx in (-1, 1):
        box(f"hwin{sx}", (4.0, 0.2, 3.4), (sx * 7.2, 7.9, 6.8), mat("hwin", hexc("#9fd0ff"), 0.2, emit=hexc("#9fd0ff"), estr=0.6), 0.1)
        sphere(f"bush{sx}", 1.9, (sx * 4.8, 6.0, 1.4), mat("bushg", hexc("#3f9f3a"), 0.9), (1.3, 1, 1), seg=16)
    for i, (x, y) in enumerate(((-16, -2), (17, 1), (-24, 9), (25, 6))):
        cyl(f"trunk{i}", 0.7, 5, (x, y, 2.5), mat("trunk", hexc("#7a4a2a"), 0.8), 10)
        sphere(f"crown{i}", 4.2, (x, y, 7.5), mat("crown", hexc("#4aa83a"), 0.9), (1, 1, 1.1), seg=16)


def dump_scene():
    world((0.06, 0.09, 0.22), 0.55)
    light("dfill", "AREA", (0, -26, 22), 16000, (0.7, 0.78, 1.0), 20, target=(0, 6, 3))
    box("dground", (260, 260, 0.4), (0, 0, -0.2), mat("dgrass", hexc("#2f4a2e"), 0.95), 0)
    box("dstreet", (260, 7.5, 0.06), (0, -26, 0.04), mat("dstreet_m", hexc("#2e2f38"), 0.8), 0)
    box("dyard", (60, 40, 0.07), (0, 8, 0.05), mat("dmud", hexc("#5a4a3a"), 0.95), 0)
    rnd = random.Random(3)
    cols = ["#6a6a72", "#8a5a3a", "#4a6a7a", "#7a7a52", "#5a3a4a"]
    for i in range(46):
        x, y = rnd.uniform(-24, 24), rnd.uniform(-6, 26)
        if abs(x) < 7 and 2 < y < 14:
            continue
        sphere(f"junk{i}", rnd.uniform(0.7, 2.0), (x, y, 0.5), mat("junk" + str(i % 5), hexc(cols[i % 5]), 0.8),
               (1, 1, rnd.uniform(0.5, 1.0)), seg=10)
    for i in range(10):
        box(f"fence{i}", (3.4, 0.4, 7 + rnd.uniform(0, 2)), (-22 + i * 5, 30, 3.8), mat("fence", hexc("#6a4a32"), 0.8), 0.05)
    Mc = mat("couch", hexc("#a8503c"), 0.8)
    box("couch_seat", (7.5, 3.2, 1.6), (0, 8.5, 1.1), Mc, 0.25)
    box("couch_back", (7.5, 1.1, 3.6), (0, 10.0, 3.0), Mc, 0.25, rot=(-10, 0, 0))
    box("couch_armL", (1.2, 3.4, 2.6), (-4.1, 8.5, 1.5), Mc, 0.25)
    box("couch_armR", (1.2, 3.4, 2.6), (4.1, 8.5, 1.0), Mc, 0.25, rot=(0, 28, 0))
    box("couch_stuff", (1.6, 1.0, 0.9), (1.8, 8.6, 2.2), mat("stuffing", hexc("#f4efe0"), 0.95), 0.4)
    for i in range(3):
        for s in (-1, 1):
            cyl(f"can{i}{s}", 1.3, 3.4, (s * (11 + i * 3.4), 12 + i * 2, 1.7), mat("canm", hexc("#7a7f8a"), 0.4, metal=0.5), 18)
    big = empty("bigcan", (10.5, 6.5, 0))
    cyl("bigcan_b", 3.0, 7.0, (0, 0, 3.5), mat("canbig", hexc("#4f6a8a"), 0.45, metal=0.5), 28, parent=big)
    for k in range(4):
        cyl(f"bigcan_r{k}", 3.08, 0.25, (0, 0, 1.2 + k * 1.6), mat("canrib", hexc("#3a4f68"), 0.5, metal=0.5), 28, parent=big)
    lid = empty("bigcan_lid", (0, 0, 7.0), big)
    cyl("bigcan_lidc", 3.25, 0.35, (0, 0, 0.18), mat("canlid", hexc("#6a86a8"), 0.4, metal=0.5), 28, parent=lid)
    cyl("bigcan_knob", 0.5, 0.5, (0, 0, 0.55), mat("canlid", hexc("#6a86a8"), 0.4), 12, parent=lid)
    light("moon", "AREA", (-12, -20, 38), 16000, (0.55, 0.65, 1.0), 14, target=(0, 8, 2))
    light("lamp", "SPOT", (0, 2, 16), 20000, (1.0, 0.8, 0.5), 1.2, target=(0, 8.5, 2), spot=70)
    sphere("moonball", 7, (-60, 140, 90), mat("moonm", hexc("#f4f0d8"), 0.5, emit=hexc("#f4f0d8"), estr=4), seg=24)
    Mg = mat("footglow", hexc("#7dff9a"), 0.3, emit=hexc("#6dff8a"), estr=5.0)
    feet = []
    for i in range(18):
        t = i / 17
        x, y = -3 + 2.0 * math.sin(t * 5), -30 + t * 33
        side = -1 if i % 2 else 1
        feet.append(sphere(f"foot{i}", 0.75, (x + side * 0.9, y, 0.15), Mg, (0.55, 1.0, 0.08), seg=10))
    return dict(big=big, lid=lid, feet=feet)


def sandwich(loc):
    r = empty("sandwich", loc)
    box("sw_b1", (1.6, 1.4, 0.28), (0, 0, 0), mat("bread", hexc("#e8c58a"), 0.7), 0.1, parent=r)
    box("sw_l", (1.7, 1.5, 0.12), (0, 0, 0.2), mat("lettuce", hexc("#7fc050"), 0.7), 0.05, parent=r)
    box("sw_m", (1.4, 1.2, 0.18), (0, 0, 0.35), mat("ham", hexc("#e89aa0"), 0.7), 0.05, parent=r)
    box("sw_b2", (1.6, 1.4, 0.28), (0, 0, 0.58), mat("bread", hexc("#e8c58a"), 0.7), 0.1, parent=r, rot=(0, 0, 8))
    return r


def warm_room():
    world((0.9, 0.75, 0.6), 0.5)
    box("lfloor", (40, 40, 0.4), (0, 0, -0.2), mat("lrug", hexc("#d8a070"), 0.8), 0)
    box("lwall", (40, 0.5, 20), (0, 9, 10), mat("lwallm", hexc("#f2d8b0"), 0.8), 0)
    light("ll", "AREA", (0, -6, 12), 12000, (1.0, 0.85, 0.65), 12, target=(0, 0, 3))


# ================================================================== SHOTS
@S(1, 0, 4, "HOOK: Eddie kicks Gary out of the door")
def s01(t0, t1):
    day_house()
    G = gary("Gary", (1.5, 5.3, 0.2), rot=-8, scale=0.55)
    E = eddie(t0, t1, "furious")
    E.pose(t0, loc=(-1.6, 5.2, 0.6), rot=-20, legR=(70, 0), armL=(70, 30), armR=(50, -30))
    E.pose(t0 + 0.25, legR=(-10, 0), armL=(20, 20), armR=(20, -20))
    E.act(t0 + 0.28, "point", expr="furious")
    move(G["root"], t0, loc=(1.5, 5.3, 0.2), rot=(0, 0, -8))
    move(G["root"], t0 + 0.28, loc=(2.2, 4.4, 1.2), rot=(10, 0, -20), ease="EASE_IN")
    move(G["root"], t1, loc=(11, -6, 7.5), rot=(-40, 0, 200))
    swing(G["arms"][0], t0, t1, 1, 50, 8, 100)
    cam = C(t0, t1, (1.0, 5.0, 3.2), 11, 8, yaw=18, pitch=4, lens=24, yaw1=40, drop=0.0, hh=1.6)
    cam.crash(t0 + 0.28, 24, 34, 0.1)
    sfx(t0 + 0.28, "u_slap", 0.9)
    sfx(t0 + 0.3, "whoosh", 0.8)


@S(2, 4, 9, "Gary lands, tumbling across the lawn")
def s02(t0, t1):
    day_house()
    G = gary("Gary", (14, -8, 0), scale=0.55)
    move(G["root"], t0, loc=(9, 3, 9.0), rot=(0, 0, 160), interp="LINEAR")
    move(G["root"], t0 + 0.45, loc=(-4, -6, 0.3), rot=(80, 0, 360), interp="LINEAR")
    move(G["root"], t0 + 0.6, loc=(-6, -7, 1.6), rot=(90, 0, 420))
    move(G["root"], t1 - 0.1, loc=(-9, -8.5, 0.2), rot=(160, 0, 560))
    move(G["root"], t1, loc=(-9.5, -8.5, 0.2), rot=(190, 0, 600))
    stars_pop("dust", (-4, -6, 0.6), t0 + 0.45, 6, 1.8, 3, 0.3, "#e8e0cc")
    cam = Cam()
    cam.whip(t0, t0 + 0.4, (14, -26, 7), (9, 3, 9), (-3, -26, 3), (-5, -6, 1.5), lens=24, whoosh=False)
    cam.key(t1, (-6, -22, 2.6), (-9.5, -8.5, 1.0), lens=28, ease="EASE_OUT")
    cam.handheld(1.4)
    sfx(t0 + 0.45, "thud", 1.0)
    sfx(t0 + 1.0, "boing", 0.8)


@S(3, 9, 12, "ONE WEEK LATER card")
def s03(t0, t1):
    world((0.95, 0.85, 0.5), 0.9)
    box("card_bg", (60, 1, 40), (0, 4, 0), mat("cardbg", hexc("#ffcf3f"), 0.8), 0)
    for i in range(7):
        sphere(f"cardstar{i}", 0.5, (-12 + i * 4, 3.4, 8 - (i % 2) * 14), mat("cardstarm", hexc("#fff0a0"), 0.5), (1, 0.2, 1), seg=8)
    light("cardlight", "AREA", (0, -14, 6), 4000, (1, 1, 1), 18, target=(0, 0, 0))
    ob = text("wk", "ONE WEEK\nLATER", (0, 0, 0), 1.5, mat("wktxt", hexc("#5a2a9a"), 0.4), rot=(90, 0, 0), extrude=0.25, font=FONT)
    move(ob, t0, rot=(90, 0, -4), scale=0.2)
    move(ob, t0 + 0.2, scale=1.15)
    move(ob, t0 + 0.32, scale=1.0)
    move(ob, t1, rot=(90, 0, 4), scale=1.12)
    cam = Cam()
    cam.key(t0, (0, -16, 0), (0, 0, 0), lens=26)
    cam.key(t1, (0, -11, 0.3), (0, 0, 0), lens=26, ease="EASE_OUT")
    cam.handheld(0.6)
    sfx(t0, "pop", 0.9)
    sfx(t0 + 0.05, "whoosh", 0.7)


@S(4, 12, 17, "A different monster moves in: climbs through the window")
def s04(t0, t1):
    night_room()
    N = nm("Nm", (15.5, -3, 5.0), rot=-90, scale=0.9)
    move(N["root"], t0, loc=(15.5, -3, 5.0), rot=(0, 0, -90))
    move(N["root"], t0 + 0.9, loc=(11.5, -3, 4.5), rot=(0, 0, -90))
    move(N["root"], t1 - 0.2, loc=(8.0, -3.5, 0.3), rot=(0, 0, -70), ease="EASE_IN")
    move(N["root"], t1, loc=(7.0, -3.6, 0.2), rot=(0, 0, -60))
    swing(N["arms"][0], t0, t1, 0, 35, 3)
    swing(N["arms"][1], t0, t1, 0, -35, 3)
    cam = Cam()
    cam.key(t0, (0, -11, 8.5), (11, -3, 4.5), lens=26)
    cam.key(t1, (1.5, -11, 7.5), (8, -3.5, 3.0), lens=28, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    cam.crash(t0 + 0.9, 28, 34, 0.2)
    sfx(t0 + 0.05, "window", 0.8)
    sfx(t0 + 1.1, "zombie", 0.7)
    sfx(t0 + 0.9, "thud", 0.5)


@S(5, 17, 22, "Eddie to camera: You see, in this world")
def s05(t0, t1):
    night_room()
    E = eddie(t0, t1, "talk")
    E.pose(t0, loc=(-1.0, -4, 0), rot=0)
    E.act(t0 + 0.2, "think")
    E.act(t0 + 0.9, "point", expr="smug")
    lips(E, t0, t1)
    cam = C(t0, t1, (-1.0, -4, 4.5), 7.5, 4.6, yaw=-12, pitch=2, lens=30, yaw1=8, hh=1.0)
    cam.crash(t0, 24, 32, 0.15)
    sfx(t0, "whoosh", 0.6)


@S(6, 22, 28, "every kid is born: lineup of kids, monsters pop up behind them")
def s06(t0, t1):
    W.sky(1.0)
    W.sun(4.0, rot=(52, 0, 30))
    box("ground", (200, 200, 0.4), (0, 0, -0.2), mat("lawn", hexc("#6fc050"), 0.9), 0)
    for i in range(3):
        k = townie(3 + i * 4, t0, t1, "smile")
        k.pose(t0, loc=(-6 + i * 6, 0, 0), rot=0)
        k.act(t0 + 0.2 + i * 0.25, "cheer")
        m = gary(f"Gm{i}", (-6 + i * 6, 3.2, 0), rot=0, scale=0.5 + 0.1 * i)
        move(m["root"], t0, scale=0.01)
        move(m["root"], t0 + 0.15 + i * 0.3, scale=0.05)
        move(m["root"], t0 + 0.4 + i * 0.3, scale=0.62 + 0.1 * i)
        sfx(t0 + 0.15 + i * 0.3, "pop", 0.7)
    cam = Cam()
    cam.key(t0, (-12, -16, 4), (-5, 1, 3.4), lens=26)
    cam.key(t1, (12, -16, 4), (5, 1, 3.4), lens=26, ease="EASE_IN_OUT")
    cam.handheld(0.8)


@S(7, 28, 33, "...a guardian monster under the bed (eyes in the dark gap)")
def s07(t0, t1):
    night_room()
    E = eddie_pj(t0, t1, "relief")
    lie_in_bed(E, t0)
    Me = mat("gapeye", hexc("#fff3a0"), 0.2, emit=hexc("#fff3a0"), estr=8.0)
    for i in range(7):
        x = GAP[0] - 1.4 + i * 0.47
        z = GAP[2] + (0.18 if i % 2 else -0.1)
        e = sphere(f"geye{i}", 0.17, (x, 0.3, z), Me, (1, 0.4, 1.2), seg=12)
        e.scale = (0.01,) * 3
        e.keyframe_insert("scale", frame=F(t0 + 0.55))
        e.scale = (1, 0.4, 1.2)
        e.keyframe_insert("scale", frame=F(t0 + 0.7 + i * 0.05))
    cam = Cam()
    cam.key(t0, (-1, -9, 1.5), (-7.6, 1.5, 2.2), lens=24, focus=10, fstop=5)
    cam.key(t1, (-5.2, -6.5, 1.2), (-7.6, 0.5, 1.6), lens=24, focus=7, fstop=5, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0 + 0.6, "rise", 0.6)


@S(8, 33, 36, "Mine, Gary: reveal")
def s08(t0, t1):
    night_room()
    G = gary("Gary", (-3.0, -3.0, 0), rot=15, scale=0.78)
    G["arms"][1].rotation_euler = (rad(160), 0, 0)
    G["arms"][1].keyframe_insert("rotation_euler", frame=F(t0))
    swing(G["arms"][1], t0 + 0.2, t1, 0, 25, 5, 160)
    bounce(G["root"], t0, t1, 0.08, 4.0)
    cam = C(t0, t1, (-3.0, -3.0, 4.2), 10, 7, yaw=-10, pitch=-2, lens=26, yaw1=10, drop=0.0, hh=1.2)
    cam.crash(t0, 22, 30, 0.14)
    sfx(t0, "u_1-108", 0.7)
    sfx(t0 + 0.05, "whoosh", 0.6)


@S(9, 36, 39, "seven eyes: extreme close-up")
def s09(t0, t1):
    night_room()
    G = gary("Gary", (-2.0, -2.0, 0), rot=0, scale=0.8)
    cam = C(t0, t1, (-2.0, -3.4, 5.0), 7.0, 4.2, yaw=2, pitch=0, lens=36, yaw1=-3, drop=0, hh=0.8, fstop=4.0)
    cam.crash(t0, 30, 44, 0.3)
    sfx(t0, "click", 0.8)
    sfx(t0 + 0.55, "click", 0.7)


@S(10, 39, 43, "smelled like old socks: stink cloud, Eddie holds nose")
def s10(t0, t1):
    night_room()
    G = gary("Gary", (-3.2, -3.2, 0), rot=10, scale=0.75)
    E = eddie_pj(t0, t1, "scared")
    E.pose(t0, loc=(1.6, -3.4, 0), rot=-15)
    look_at(E, t0 + 0.2, (-3.2, -3.2, 3))
    E.act(t0 + 0.4, "recoil", expr="scream")
    E.pose(t0 + 0.5, armL=(60, 0), armR=(140, -30))
    stink("stk", (-1.0, -3.8, 2.0), t0 + 0.1, t1, 11, 4)
    cam = C(t0, t1, (-0.8, -3.4, 3.6), 9.5, 7.5, yaw=-5, pitch=2, lens=26, yaw1=12, hh=1.3)
    sfx(t0 + 0.3, "u_dry-fart", 1.0)


@S(11, 43, 48, "Errrrr! So, monsters have jobs: hard hat Gary")
def s11(t0, t1):
    night_room()
    G = gary("Gary", (-3.0, -3.5, 0), rot=0, scale=0.8, hat=True)
    bounce(G["root"], t0, t0 + 0.6, 0.18, 14)
    swing(G["arms"][0], t0 + 0.6, t1, 0, 18, 3, 60)
    swing(G["arms"][1], t0 + 0.6, t1, 0, -18, 3, 60)
    cam = Cam()
    cam.orbit(t0, t1, (-3.0, -3.5, 4.6), 8.5, -35, 30, pitch=3, lens=26, fstop=6)
    cam.handheld(2.4)
    sfx(t0, "u_faaah", 0.8)
    sfx(t0 + 0.1, "zombie", 0.6)


@S(12, 48, 52, "Bullies get a growl")
def s12(t0, t1):
    night_room()
    B = bully(t0, t1, "angry")
    B.pose(t0, loc=(1.5, -4.2, 0), rot=-10)
    B.act(t0 + 0.1, "fists")
    G = gary("Gary", (-5.5, -1.0, -3.0), rot=-20, scale=0.85)
    move(G["root"], t0, loc=(-5.5, -1.0, -3.0))
    move(G["root"], t0 + 0.8, loc=(-5.5, -1.0, -3.0))
    move(G["root"], t0 + 1.0, loc=(-4.5, -2.2, 0.0), scale=0.9)
    B.act(t0 + 1.1, "recoil", expr="terror")
    B.pose(t0 + 1.35, loc=(3.2, -8.0, 0))
    cam = C(t0, t1, (0, -3.3, 3.6), 9, 7, yaw=-8, pitch=3, lens=26, yaw1=8, hh=1.6)
    cam.crash(t0 + 1.0, 26, 34, 0.12)
    sfx(t0 + 0.9, "zombie", 1.0)


@S(13, 52, 56, "Bad dreams get eaten")
def s13(t0, t1):
    night_room()
    E = eddie_pj(t0, t1, "sleepy")
    lie_in_bed(E, t0)
    Mn = mat("dreamcloud", hexc("#3a2050"), 0.8, emit=hexc("#6a30a0"), estr=0.8)
    Mr = mat("dremit", hexc("#ff3030"), 0.3, emit=hexc("#ff2020"), estr=8)
    cl = empty("dream", (-7.6, 3.0, 9.5))
    for i, (x, z, r) in enumerate(((0, 0, 1.6), (1.4, 0.3, 1.2), (-1.4, 0.2, 1.2), (0.6, 1.0, 1.0))):
        sphere(f"dr{i}", r, (x, 0, z), Mn, parent=cl, seg=14)
    sphere("dr_e1", 0.3, (-0.5, -1.5, 0.1), Mr, (1, 0.4, 1), parent=cl)
    sphere("dr_e2", 0.3, (0.5, -1.5, 0.1), Mr, (1, 0.4, 1), parent=cl)
    G = gary("Gary", (-2.8, 3.6, 0), rot=30, scale=0.8)
    move(cl, t0, loc=(-7.6, 3.0, 9.5), scale=1.0)
    move(cl, t0 + 0.55, loc=(-7.6, 3.0, 9.5), scale=1.0)
    move(cl, t0 + 0.75, loc=(-4.0, 3.2, 6.8), scale=0.7)
    move(cl, t0 + 0.9, loc=(-3.0, 3.4, 6.7), scale=0.05)
    for dt, a in ((0.0, 0), (0.55, -20), (0.8, 15), (1.1, 0)):
        G["head"].rotation_euler = (rad(a), 0, 0)
        G["head"].keyframe_insert("rotation_euler", frame=F(t0 + dt))
    stars_pop("nom", (-3.0, 3.0, 6.5), t0 + 0.85, 7, 2.0, 5, 0.2, "#c070ff")
    cam = Cam()
    cam.key(t0, (-1.5, -9, 5.5), (-6, 3.4, 6.4), lens=24)
    cam.key(t1, (-2.5, -6, 6.2), (-4.2, 3.4, 6.5), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.8, "snort", 0.9)
    sfx(t0 + 0.85, "u_duck-toy-sound", 0.5)


@S(14, 56, 63, "A kid falls out of bed")
def s14(t0, t1):
    night_room()
    K = townie(9, t0, t1, "sleepy")
    ob = K.root
    for dt, (x, z, ry) in ((0.0, (BED[0] + 1.0, 3.2, 0)), (0.4, (BED[0] + 2.9, 3.4, 0)), (0.7, (BED[0] + 4.6, 3.0, 35)),
                           (1.05, (BED[0] + 5.8, 0.6, 80))):
        ob.location = (x, 3.2 - dt * 0.4, z)
        ob.rotation_euler = (rad(-90 + ry), rad(dt * 90), 0)
        ob.keyframe_insert("location", frame=F(t0 + dt))
        ob.keyframe_insert("rotation_euler", frame=F(t0 + dt))
    K.face(t0 + 0.5, "scream")
    cam = Cam()
    cam.key(t0, (-1.8, -8, 6), (-5.6, 3.2, 3.2), lens=24)
    cam.key(t1 - 0.3, (-1.0, -7.4, 4.0), (-2.4, 3.0, 2.4), lens=26)
    cam.key(t1, (-1.0, -7.2, 3.2), (-2.2, 2.6, 1.0), lens=28, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.4, "rope", 0.5)
    sfx(t0 + 0.75, "gasp", 0.9)
    sfx(t0 + 1.05, "whoosh", 0.7)


@S(15, 63, 68, "...a hairy arm catches them (arm shoots out of the gap)")
def s15(t0, t1):
    night_room()
    K = townie(9, t0, t1, "scream")
    ob = K.root
    ob.rotation_euler = (rad(-20), 0, 0)
    ob.location = (-3.0, 1.6, 6.5)
    ob.keyframe_insert("location", frame=F(t0))
    ob.location = (-3.0, 1.2, 2.0)
    ob.keyframe_insert("location", frame=F(t0 + 0.7))
    Mf = mat("hairyarm", hexc("#8a5cc4"), 0.95)
    root = empty("hairyarm", (GAP[0] + 4.0, 0.3, 1.0))
    cyl("harm", 0.7, 7.0, (0, -3.5, 0), Mf, 14, parent=root, rot=(90, 0, 0))
    sphere("hhand", 1.0, (0, -7.2, 0), Mf, parent=root)
    for i in range(8):
        cyl(f"htuft{i}", 0.18, 0.8, (math.cos(i) * 0.7, -0.8 - i * 0.75, math.sin(i) * 0.7), mat("gdark", hexc("#4a2a78"), 0.9), 6,
            parent=root, r2=0.02, rot=(math.cos(i) * 40, 0, math.sin(i) * 40))
    move(root, t0 + 0.35, scale=(1, 0.03, 1))
    move(root, t0 + 0.6, scale=(1, 1.15, 1))
    move(root, t0 + 0.75, scale=(1, 1.0, 1))
    root.rotation_euler = (0, 0, rad(20))
    root.keyframe_insert("rotation_euler", frame=F(t0))
    cam = C(t0, t1, (-3.5, 1.5, 3.2), 13, 8.5, yaw=-18, pitch=8, lens=26, yaw1=0, hh=1.5)
    cam.crash(t0 + 0.72, 26, 36, 0.1)
    sfx(t0 + 0.4, "whoosh", 0.9)


@S(16, 68, 69, "FWOOMP: kid safe in the arm, stars")
def s16(t0, t1):
    night_room()
    K = townie(9, t0, t1, "gasp")
    K.pose(t0, loc=(-5.0, 1.0, 2.2), rot=0)
    K.act(t0, "hands_face")
    gary("Gary", (-7.4, 1.4, 0), rot=0, scale=0.9)
    stars_pop("fw", (-5.0, 0.4, 5.0), t0, 10, 3.0, 4, 0.25)
    pop_text("fwoomp", "FWOOMP!", (-4.5, -1.5, 8.0), t0, 0.7, 1.0, "#ffe066")
    cam = C(t0, t1, (-5.0, 1.0, 4.0), 9, 6.0, yaw=0, pitch=2, lens=24, hh=2.0)
    cam.crash(t0, 22, 30, 0.1)
    sfx(t0, "u_capcut-explosion-sound", 0.7)
    sfx(t0, "boing", 0.6)


@S(17, 69, 75, "But I was ten and embarrassed")
def s17(t0, t1):
    night_room()
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(0.5, -3.5, 0), rot=0)
    E.act(t0 + 0.2, "slump")
    E.act(t0 + 1.0, "hands_face", expr="worried")
    for sx in (-1, 1):
        sphere(f"blush{sx}", 0.2, (sx * 0.5, -0.64, -0.2), mat("blush", hexc("#ff7a8a"), 0.5, emit=hexc("#ff7a8a"), estr=1.2),
               (1.4, 0.2, 0.8), parent=E.head)
    cam = C(t0, t1, (0.5, -3.5, 4.5), 9, 4.5, yaw=10, pitch=3, lens=30, yaw1=-8, hh=1.0)
    sfx(t0 + 0.9, "u_mac-quack", 0.4)


@S(18, 75, 79, "Gary was huge (low angle)")
def s18(t0, t1):
    night_room()
    gary("Gary", (-1.0, -1.0, 0), rot=0, scale=1.25)
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(3.6, -6.5, 0), rot=-10)
    E.act(t0 + 0.1, "recoil")
    cam = C(t0, t1, (-1.0, -1.0, 6.5), 10, 6.5, yaw=-8, pitch=-14, lens=22, yaw1=8, drop=0.0, hh=1.4)
    sfx(t0, "stomp", 0.9)


@S(19, 79, 83, "drooled on the carpet")
def s19(t0, t1):
    night_room()
    gary("Gary", (-1.0, -1.0, 0), rot=0, scale=1.0)
    Md = mat("drool", hexc("#bfe8ff"), 0.05, emit=hexc("#8fc8ff"), estr=0.5, alpha=0.8)
    for i in range(5):
        x = -1.0 + (i - 2) * 0.12
        d = sphere(f"drip{i}", 0.2, (x, -3.2, 4.0), Md, (1, 1, 1.5), seg=8)
        t = t0 + 0.05 + i * 0.22
        d.scale = (0.2,) * 3
        d.keyframe_insert("scale", frame=F(t))
        d.keyframe_insert("location", frame=F(t))
        d.scale = (1, 1, 1.5)
        d.keyframe_insert("scale", frame=F(t + 0.2))
        d.location = (x, -3.2, 0.12)
        d.keyframe_insert("location", frame=F(t + 0.5))
        d.scale = (0.01,) * 3
        d.keyframe_insert("scale", frame=F(t + 0.55))
    sphere("puddle", 1.5, (-1.0, -3.1, 0.07), Md, (1, 1, 0.03), seg=12)
    cam = Cam()
    cam.key(t0, (-1.4, -7.8, 3.2), (-1.0, -3.2, 3.8), lens=30, focus=6, fstop=3)
    cam.key(t1, (-1.2, -6.2, 0.8), (-1.0, -3.2, 1.0), lens=30, focus=3, fstop=3, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0 + 0.3, "splat", 0.5)
    sfx(t0 + 0.75, "splat", 0.5)


@S(20, 83, 88, "So one night I yelled,")
def s20(t0, t1):
    night_room()
    E = eddie(t0, t1, "shout")
    E.pose(t0, loc=(0.5, -3.2, 0), rot=0)
    E.act(t0 + 0.1, "fists", expr="shout")
    lips(E, t0, t1, "shout")
    cam = C(t0, t1, (0.5, -3.2, 4.5), 7.5, 4.8, yaw=-14, pitch=2, lens=30, yaw1=6, hh=1.6, roll=1.5)
    sfx(t0 + 0.05, "wind", 0.4)


@S(21, 88, 91, "Gary, get out! (point, shake)")
def s21(t0, t1):
    night_room()
    E = eddie(t0, t1, "furious")
    E.pose(t0, loc=(0, -3.2, 0), rot=-60)
    E.act(t0 + 0.05, "point", expr="furious", strength=1.1)
    cam = C(t0, t1, (0, -3.2, 4.6), 8.0, 5.2, yaw=-30, pitch=2, lens=26, yaw1=-10, hh=3.0)
    cam.crash(t0 + 0.1, 24, 34, 0.1)
    sfx(t0, "u_slap", 0.6)


@S(22, 91, 96, "I'm too old for you!")
def s22(t0, t1):
    night_room()
    E = eddie(t0, t1, "shout")
    E.pose(t0, loc=(0, -3.2, 0), rot=0)
    E.act(t0 + 0.1, "cross", expr="furious")
    lips(E, t0, t1, "shout")
    cam = C(t0, t1, (0, -3.2, 4.8), 6.0, 3.8, yaw=8, pitch=0, lens=32, yaw1=-8, hh=2.2)
    sfx(t0, "boom", 0.4)


@S(23, 96, 102, "His seven eyes filled with tears")
def s23(t0, t1):
    night_room()
    gary("Gary", (-1.5, -1.5, 0), rot=0, scale=0.9, tears=True)
    cam = C(t0, t1, (-1.5, -2.8, 6.0), 9, 4.6, yaw=0, pitch=0, lens=34, drop=0.0, hh=0.9, fstop=3.5)
    sfx(t0 + 0.2, "aww", 0.6)
    sfx(t0 + 1.3, "u_duck-toy-sound", 0.5)


@S(24, 102, 108, "He packed a tiny suitcase")
def s24(t0, t1):
    night_room()
    G = gary("Gary", (-4.0, -1.0, 0), rot=0, scale=0.85, bag=True)
    swing(G["arms"][1], t0, t1, 0, 10, 2, 20)
    move(G["head"], t0, rot=(10, 0, 0))
    move(G["head"], t1, rot=(28, 0, 0))
    cam = C(t0, t1, (-4.0, -1.0, 3.4), 11, 8.0, yaw=-25, pitch=2, lens=26, yaw1=-5, hh=1.0)
    sfx(t0 + 0.8, "click", 0.7)
    sfx(t0 + 1.2, "paper", 0.6)


@S(25, 108, 112, "...and left through the window")
def s25(t0, t1):
    night_room()
    G = gary("Gary", (4.0, -3.0, 0), rot=-90, scale=0.8, bag=True)
    move(G["root"], t0, loc=(4.0, -3.0, 0), rot=(0, 0, -90))
    move(G["root"], t0 + 0.65, loc=(8.5, -3.0, 0.8), rot=(0, 0, -90), ease="EASE_IN")
    move(G["root"], t1 - 0.05, loc=(14.0, -3.0, 4.5), rot=(0, 0, -90))
    move(G["root"], t1, loc=(16.0, -3.0, 4.5), rot=(0, 0, -90))
    swing(G["arms"][1], t0, t1, 0, 20, 4, 0)
    cam = Cam()
    cam.key(t0, (-2.0, -12, 5.5), (5.0, -3.0, 3.5), lens=24)
    cam.key(t1, (3.0, -11, 6.0), (10.5, -3.0, 4.5), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0, "footsteps", 0.8)
    sfx(t0 + 0.9, "window", 0.7)


@S(26, 112, 117, "Next night, my bed creaked")
def s26(t0, t1):
    night_room()
    E = eddie_pj(t0, t1, "worried")
    lie_in_bed(E, t0)
    E.face(t0 + 0.5, "gasp")
    for i in range(6):
        E.pose(t0 + 0.3 + i * 0.12, loc=(BED[0] + (0.08 if i % 2 else -0.08), 3.2, 3.2 + (0.1 if i % 2 else 0)))
    cam = Cam()
    cam.key(t0, (-4.5, -5, 6.5), (-7.6, 4.0, 3.5), lens=26)
    cam.key(t1, (-5.6, -3, 5.5), (-7.6, 4.2, 3.4), lens=26, ease="EASE_IN_OUT")
    cam.handheld(2.4)
    sfx(t0 + 0.2, "door", 0.7)
    sfx(t0 + 0.7, "door", 0.7)


@S(27, 117, 122, "Something new was under there: red eyes in the gap")
def s27(t0, t1):
    night_room()
    Me = mat("nredeye", hexc("#ff2a2a"), 0.2, emit=hexc("#ff2020"), estr=9.0)
    for sx in (-1, 1):
        e = sphere(f"redeye{sx}", 0.34, (GAP[0] + sx * 0.8, 0.32, GAP[2] + 0.1), Me, (1, 0.5, 0.8))
        e.scale = (0.01,) * 3
        e.keyframe_insert("scale", frame=F(t0 + 0.4))
        e.scale = (1, 0.5, 0.8)
        e.keyframe_insert("scale", frame=F(t0 + 0.55))
    cam = Cam()
    cam.key(t0, (-4.0, -7, 1.1), (-7.6, 0.4, 1.0), lens=26, focus=8, fstop=4)
    cam.key(t1, (-6.6, -3.2, 1.0), (-7.6, 0.4, 1.0), lens=26, focus=3.6, fstop=4, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.4, "zombie", 0.9)
    sfx(t0 + 0.4, "rise", 0.7)


@S(28, 122, 126, "with too many teeth: extreme close-up grin")
def s28(t0, t1):
    night_room()
    nm("Nm", (-7.6, -3.0, 0), rot=0, scale=1.0)
    cam = C(t0, t1, (-7.6, -4.7, 5.0), 5.5, 3.2, yaw=0, pitch=0, lens=34, drop=0, hh=1.6, fstop=3.5)
    cam.crash(t0, 28, 44, 0.12)
    sfx(t0, "u_capcut-explosion-sound", 0.5)
    sfx(t0 + 0.2, "zombie", 1.0)


@S(29, 126, 128, "Gary's gone (empty gap)")
def s29(t0, t1):
    night_room()
    sphere("dustb", 0.6, (GAP[0], 0.0, 0.5), mat("dust", hexc("#b8b0a0"), 0.9, alpha=0.7), (1.5, 1, 0.5))
    cam = Cam()
    cam.key(t0, (-6.8, -6, 2.0), (-7.6, 0.4, 1.0), lens=28)
    cam.key(t1, (-7.2, -4.8, 1.8), (-7.6, 0.4, 1.0), lens=28)
    cam.handheld(0.8)
    sfx(t0, "crickets", 0.8)


@S(30, 128, 131, "Now you're mine (claw reaches the camera)")
def s30(t0, t1):
    night_room()
    N = nm("Nm", (-7.0, -1.8, 0), rot=0, scale=1.05)
    swing(N["arms"][0], t0, t1, 0, 15, 4, 70)
    N["arms"][1].rotation_euler = (rad(95), 0, 0)
    N["arms"][1].keyframe_insert("rotation_euler", frame=F(t0))
    move(N["arms"][1], t1, rot=(115, 0, 0))
    move(N["root"], t0, loc=(-7.0, -1.8, 0))
    move(N["root"], t1, loc=(-6.6, -2.6, 0))
    E = eddie_pj(t0, t1, "terror")
    E.pose(t0, loc=(-4.0, -8.5, 0), rot=0)
    E.act(t0 + 0.1, "recoil")
    cam = C(t0, t1, (-6.6, -3.0, 4.8), 10, 7.0, yaw=0, pitch=-4, lens=24, hh=2.4)
    cam.crash(t0 + 0.5, 24, 36, 0.12)
    sfx(t0 + 0.1, "zombie", 0.8)
    sfx(t0 + 0.5, "boom", 0.6)


@S(31, 131, 135, "I ran to mom (run down the hallway)")
def s31(t0, t1):
    world((0.35, 0.3, 0.5), 0.6)
    box("hfloor", (14, 90, 0.4), (0, 20, -0.2), mat("hwood", hexc("#a57850"), 0.5), 0)
    for sx in (-1, 1):
        box(f"hwall{sx}", (0.6, 90, 14), (sx * 5, 20, 7), mat("hwallm", hexc("#c4b8e0"), 0.8), 0)
    for i in range(7):
        box(f"hframe{i}", (0.2, 2.0, 2.4), (-4.6 if i % 2 else 4.6, i * 5 + 2, 6.5), mat("hfr", hexc("#e8c66a"), 0.5), 0.05)
    light("hl", "AREA", (0, 10, 12), 9000, (1, 0.9, 0.8), 12, target=(0, 12, 0))
    E = eddie_pj(t0, t1, "terror")
    acting.run(E, t0, t1, (0, -2, 0), (0, 12, 0))
    E.pose(t0, rot=180)
    E.pose(t1, rot=180)
    cam = Cam()
    cam.track(E, t0, t1, offset=(2.2, -7.5, 3.4), look_up=3.6, lens=24)
    cam.handheld(2.4)
    sfx(t0, "footsteps", 1.0)
    sfx(t0 + 0.1, "whoosh", 0.6)


@S(32, 135, 138, "She hugged me")
def s32(t0, t1):
    warm_room()
    M = mom(t0, t1, "smile")
    M.pose(t0, loc=(0.4, 0, 0), rot=0)
    M.act(t0, "hold")
    E = eddie_pj(t0, t1, "relief")
    E.pose(t0, loc=(-0.5, -1.2, 0), rot=0)
    E.act(t0 + 0.1, "hold")
    cam = C(t0, t1, (0, -0.6, 4.2), 9, 6.2, yaw=-20, pitch=3, lens=28, yaw1=15, hh=0.9)
    sfx(t0 + 0.1, "aww", 0.6)


@S(33, 138, 143, "Your monster protects you")
def s33(t0, t1):
    warm_room()
    M = mom(t0, t1, "talk")
    M.pose(t0, loc=(0, 0, 0), rot=0)
    lips(M, t0, t1)
    M.act(t0 + 0.1, "think")
    M.act(t0 + 0.9, "point", expr="smile")
    cam = C(t0, t1, (0, 0, 4.4), 8.0, 5.0, yaw=14, pitch=2, lens=30, yaw1=-8, hh=0.9)


@S(34, 143, 147, "from the other monsters, honey")
def s34(t0, t1):
    warm_room()
    M = mom(t0, t1, "talk")
    M.pose(t0, loc=(0, 0, 0), rot=0)
    lips(M, t0, t1)
    M.act(t0, "wave")
    M.act(t0 + 1.0, "shrug", expr="smile")
    E = eddie_pj(t0, t1, "worried")
    E.pose(t0, loc=(-3.2, -2.5, 0), rot=-20)
    E.act(t0 + 0.2, "think", expr="sus")
    cam = C(t0, t1, (-1.2, -1.0, 4.2), 10, 7.0, yaw=-6, pitch=3, lens=26, yaw1=14, hh=1.0)
    sfx(t0 + 0.9, "ding", 0.3)


@S(35, 147, 151, "Then I noticed something")
def s35(t0, t1):
    world((0.07, 0.09, 0.2), 0.4)
    box("lfloor", (40, 40, 0.4), (0, 0, -0.2), mat("lrug2", hexc("#8a6a50"), 0.8), 0)
    box("lwall", (40, 0.5, 20), (0, 9, 10), mat("lwall2", hexc("#9a8ab0"), 0.8), 0)
    locs.window("lwin", 0, 8.6, 7, 6, 5, collection("WIN"), facing="-Y", sky=(0.1, 0.5, 0.3), estr=1.5)
    light("greenlight", "AREA", (0, 4, 6), 2500, (0.4, 1.0, 0.5), 5, target=(0, -2, 3))
    light("roomfill", "AREA", (0, -8, 10), 4000, (0.6, 0.6, 0.9), 12, target=(0, 0, 4))
    E = eddie_pj(t0, t1, "sus")
    E.pose(t0, loc=(0, 0.4, 0), rot=0)
    E.act(t0 + 0.2, "lean")
    cam = Cam()
    cam.key(t0, (-2.0, -9, 6.0), (0, 2, 5), lens=26)
    cam.key(t1, (0, -3.0, 5.4), (0, 8.6, 6.4), lens=32, ease="EASE_IN")
    cam.handheld(0.9)
    cam.crash(t0 + 0.9, 26, 38, 0.2)
    sfx(t0, "u_correct", 0.5)
    sfx(t0 + 0.35, "rise", 0.8)


@S(36, 151, 155, "Glowing footprints led across (track along)")
def s36(t0, t1):
    D_ = dump_scene()
    cam = Cam()
    cam.key(t0, (-2.6, -34, 2.2), (-2, -22, 0.2), lens=24)
    cam.key(t1, (-1.5, -16, 2.0), (-0.5, -2, 0.2), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    for i, f in enumerate(D_["feet"]):
        f.scale = (0.01,) * 3
        f.keyframe_insert("scale", frame=F(t0 + i * 0.045))
        f.scale = (0.55, 1.0, 0.08)
        f.keyframe_insert("scale", frame=F(t0 + 0.12 + i * 0.045))
    sfx(t0, "sparkle", 0.6)
    sfx(t0 + 0.2, "footsteps", 0.5)


@S(37, 155, 160, "...across the street to the dump (wide reveal)")
def s37(t0, t1):
    dump_scene()
    pop_text("dumpsign", "DUMP", (0, 29.4, 11.0), t0 + 0.7, 1.6, 3.2, "#ffe066")
    cam = Cam()
    cam.key(t0, (14, -34, 3.0), (-2, 6, 3), lens=22)
    cam.key(t1, (3, -20, 9.0), (0, 12, 4), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.7, "pop", 0.7)


@S(38, 160, 163, "I ran there (Eddie sprinting at the camera)")
def s38(t0, t1):
    dump_scene()
    E = eddie_pj(t0, t1, "terror")
    acting.run(E, t0, t1, (-1.0, -3.0, 0), (0.5, -19.0, 0))
    E.pose(t0, rot=0)
    E.pose(t1, rot=0)
    cam = Cam()
    cam.key(t0, (-4.0, -26, 2.0), (-1, -6, 3.0), lens=26)
    cam.key(t1, (-6.0, -24, 2.4), (0.5, -19.0, 3.0), lens=28, ease="EASE_OUT")
    cam.handheld(2.4)
    sfx(t0, "footsteps", 1.0)
    sfx(t0, "whoosh", 0.5)


@S(39, 163, 169, "Gary sat on a broken couch")
def s39(t0, t1):
    dump_scene()
    G = gary("Gary", (0, 8.4, 1.2), rot=0, scale=0.85, bag=True)
    move(G["head"], t0, rot=(20, 0, 0))
    move(G["head"], t1, rot=(32, 0, 0))
    G["arms"][1].rotation_euler = (rad(20), 0, 0)
    cam = Cam()
    cam.orbit(t0, t1, (0, 8.4, 4.0), 17, -25, 10, pitch=4, lens=26, fstop=6)
    cam.handheld(1.0)
    sfx(t0, "crickets", 0.7)
    sfx(t0 + 0.7, "aww", 0.5)


@S(40, 169, 173, "eating a sad sandwich")
def s40(t0, t1):
    dump_scene()
    G = gary("Gary", (0, 8.4, 1.2), rot=0, scale=0.85)
    G["arms"][1].rotation_euler = (rad(95), 0, rad(-10))
    G["arms"][1].keyframe_insert("rotation_euler", frame=F(t0))
    s = sandwich((-0.8, 5.0, 4.9))
    move(s, t0, loc=(-0.8, 5.0, 4.9), rot=(-20, 0, 0))
    move(s, t1, loc=(-0.3, 5.5, 5.5), rot=(-20, 0, 0))
    move(G["head"], t0, rot=(25, 0, 0))
    move(G["head"], t0 + 0.6, rot=(10, 0, 0))
    move(G["head"], t1, rot=(30, 0, 0))
    cam = C(t0, t1, (0, 5.0, 5.4), 8.5, 5.4, yaw=-8, pitch=0, lens=30, hh=0.8, drop=0.0, fstop=4)
    sfx(t0 + 0.4, "u_mac-quack", 0.5)
    sfx(t0 + 0.7, "snort", 0.6)


@S(41, 173, 178, "Behind me, the new monster...")
def s41(t0, t1):
    dump_scene()
    E = eddie_pj(t0, t1, "worried")
    E.pose(t0, loc=(2.0, -1.0, 0), rot=0)
    N = nm("Nm", (8.0, 4.0, -7.0), rot=180, scale=1.4)
    move(N["root"], t0, loc=(6.0, 6.0, -8.0), rot=(0, 0, 0))
    move(N["root"], t1 - 0.3, loc=(6.0, 6.0, 0), rot=(0, 0, 0), ease="EASE_OUT")
    cam = Cam()
    cam.key(t0, (3.2, -9, 4.2), (1.0, 2.5, 4.0), lens=26)
    cam.key(t1, (2.6, -2.4, 4.6), (4.2, 6.0, 5.6), lens=28, ease="EASE_IN")
    cam.handheld(1.4)
    sfx(t0 + 0.4, "rise", 0.9)
    sfx(t0 + 1.0, "zombie", 0.8)


@S(42, 178, 182, "crawled out and grinned")
def s42(t0, t1):
    dump_scene()
    N = nm("Nm", (10.0, 20.0, 0), rot=0, scale=1.1)
    swing(N["arms"][0], t0, t1, 0, 30, 3, 40)
    move(N["root"], t0, loc=(10.0, 20.0, 0))
    move(N["root"], t1, loc=(4.0, 6.0, 0))
    cam = C(t0, t1, (4.0, 5.0, 6.0), 12, 4.8, yaw=0, pitch=-2, lens=28, drop=0, hh=1.8, fstop=4)
    cam.crash(t0 + 1.0, 28, 40, 0.15)
    sfx(t0, "zombie", 1.0)
    sfx(t0 + 0.9, "u_movie_1", 0.4)


@S(43, 182, 184, "Too late. (terror close-up)")
def s43(t0, t1):
    dump_scene()
    E = eddie_pj(t0, t1, "terror")
    E.pose(t0, loc=(0, -4, 0), rot=0)
    E.act(t0 + 0.05, "hands_head", expr="terror")
    nm("Nm", (0, 8.0, 0), rot=0, scale=1.6)
    cam = C(t0, t1, (0, -4, 4.8), 7.0, 4.0, yaw=0, pitch=2, lens=30, hh=1.6)
    cam.crash(t0, 24, 36, 0.1)
    sfx(t0, "gasp", 0.9)


@S(44, 184, 185, "RAWR! monster lunges")
def s44(t0, t1):
    dump_scene()
    N = nm("Nm", (0, 6.0, 0), rot=0, scale=1.3)
    move(N["root"], t0, loc=(0, 8.0, 0), scale=1.3)
    move(N["root"], t1, loc=(0, 1.0, 0), scale=1.6)
    cam = C(t0, t1, (0, 3.0, 6.6), 9.0, 5.0, yaw=0, pitch=0, lens=22, drop=0, hh=3.2)
    cam.crash(t0, 22, 40, 0.14)
    pop_text("rawr", "RAWR!", (0, -1.5, 11.0), t0 + 0.02, 0.6, 1.4, "#ff4a4a")
    sfx(t0, "u_capcut-explosion-sound", 0.9)
    sfx(t0, "zombie", 1.0)


@S(45, 185, 190, "Gary's seven eyes lit up (glow)")
def s45(t0, t1):
    dump_scene()
    G = gary("Gary", (0, 7.4, 1.2), rot=0, scale=0.9, glow=True)
    G["head"].rotation_euler = (rad(28), 0, 0)
    G["head"].keyframe_insert("rotation_euler", frame=F(t0))
    move(G["head"], t0 + 0.7, rot=(-8, 0, 0))
    bounce(G["root"], t0 + 0.7, t1, 0.12, 8)
    light("eyeglow", "POINT", (0, 3, 6.5), 6000, (1.0, 0.95, 0.5), 1.5)
    cam = C(t0, t1, (0, 7.4, 7.0), 11, 5.5, yaw=0, pitch=-6, lens=28, drop=0, hh=1.2, fstop=4)
    cam.crash(t0 + 1.5, 28, 40, 0.2)
    sfx(t0 + 0.7, "rise", 1.0)
    sfx(t0 + 1.7, "sparkle", 0.8)


@S(46, 190, 197, "He grabbed the monster by the tail")
def s46(t0, t1):
    dump_scene()
    G = gary("Gary", (-5.5, 6.0, 0), rot=-25, scale=1.0, glow=True)
    nm("Nm", (2.0, 2.0, 0), rot=180, scale=0.95)
    move(G["root"], t0, loc=(-5.5, 6.0, 0))
    move(G["root"], t0 + 0.7, loc=(-1.0, 3.0, 0), ease="EASE_OUT")
    move(G["arms"][0], t0 + 0.7, rot=(110, 0, -20))
    cam = C(t0, t1, (1.0, 3.2, 3.8), 14, 8.5, yaw=-10, pitch=2, lens=26, yaw1=-35, hh=1.5)
    cam.crash(t0 + 0.9, 26, 36, 0.12)
    sfx(t0, "stomp", 0.8)
    sfx(t0 + 0.9, "rope", 0.9)


@S(47, 197, 203, "...and swung it like a lasso (orbit spin)")
def s47(t0, t1):
    dump_scene()
    G = gary("Gary", (0, 4.0, 0), rot=0, scale=1.0, glow=True)
    N = nm("Nm", (0, 0, 3.0), rot=0, scale=0.9)
    cx, cy = 0.0, 4.0
    n = int((t1 - t0) * 30 / 2)
    for k in range(n + 1):
        tt = t0 + (t1 - t0) * k / n
        ang = (k / n) * math.tau * 3.0
        r = 3.0 + 6.0 * min(1.0, k / (n * 0.4))
        move(N["root"], tt, loc=(cx + math.cos(ang) * r, cy + math.sin(ang) * r, 2.2 + 0.5 * math.sin(ang * 2)),
             rot=(70, 0, math.degrees(ang) + 90), interp="LINEAR")
        move(G["root"], tt, rot=(0, 0, math.degrees(ang) * 0.9 - 180), interp="LINEAR")
    cam = Cam()
    cam.orbit(t0, t1, (0, 4.0, 3.5), 24, -40, 50, pitch=8, lens=24, steps=6, fstop=8)
    cam.handheld(1.6)
    sfx(t0 + 0.1, "rope", 0.8)
    sfx(t0 + 0.5, "wind", 0.9)
    sfx(t0 + 1.2, "wind", 0.9)


@S(48, 203, 208, "Whoosh! It flew into the biggest")
def s48(t0, t1):
    dump_scene()
    N = nm("Nm", (-3.0, 4.0, 2.5), rot=0, scale=0.9)
    move(N["root"], t0, loc=(-3.0, 4.0, 2.5), rot=(70, 0, 90), interp="LINEAR")
    move(N["root"], t0 + 0.45, loc=(2.0, 6.0, 11.0), rot=(160, 0, 300), interp="LINEAR")
    move(N["root"], t1 - 0.2, loc=(8.0, 6.5, 9.5), rot=(260, 0, 400))
    move(N["root"], t1, loc=(10.0, 6.5, 8.0), rot=(300, 0, 440))
    cam = Cam()
    cam.key(t0, (-8, -4, 3.0), (-3, 4, 3), lens=24)
    cam.key(t0 + 0.4, (-2, -6, 6.0), (2, 6, 11), lens=24)
    cam.key(t1, (7.5, -10, 6.5), (9.5, 6.5, 9.0), lens=28, ease="EASE_IN_OUT")
    cam.handheld(1.8)
    pop_text("whsh", "WHOOSH!", (1, -2.0, 10.0), t0 + 0.05, 0.9, 1.1, "#aef0ff")
    sfx(t0, "whoosh", 1.0)
    sfx(t0 + 0.3, "jet", 0.4)


@S(49, 208, 211, "trash can (monster dropping in)")
def s49(t0, t1):
    d = dump_scene()
    N = nm("Nm", (10.5, 6.5, 14.0), rot=0, scale=0.7)
    move(N["root"], t0, loc=(10.5, 6.5, 14.0), rot=(180, 0, 40), interp="LINEAR")
    move(N["root"], t1 - 0.3, loc=(10.5, 6.5, 6.8), rot=(190, 0, 120), interp="LINEAR")
    move(N["root"], t1, loc=(10.5, 6.5, 3.0), rot=(190, 0, 150))
    move(d["lid"], t0, loc=(-2.5, 0, 8.0))
    cam = Cam()
    cam.key(t0, (5, -8, 10.5), (10.5, 6.5, 8), lens=24)
    cam.key(t1, (9, -5, 9.0), (10.5, 6.5, 5.5), lens=24, ease="EASE_IN")
    cam.handheld(1.4)
    sfx(t0 + 0.7, "thud", 0.8)


@S(50, 211, 212, "CLANG! lid slams")
def s50(t0, t1):
    d = dump_scene()
    lid = d["lid"]
    move(lid, t0 - 0.02, loc=(0, 0, 11.0))
    move(lid, t0 + 0.12, loc=(0, 0, 7.0), ease="EASE_IN")
    move(lid, t0 + 0.2, loc=(0, 0, 7.5))
    move(lid, t0 + 0.3, loc=(0, 0, 7.0))
    for i in range(6):
        move(d["big"], t0 + 0.12 + i * 0.05, loc=(10.5 + (0.12 if i % 2 else -0.12), 6.5, 0))
    pop_text("clang", "CLANG!", (10.5, -1.5, 11.5), t0 + 0.1, 0.65, 1.3, "#ffe066")
    stars_pop("cl", (10.5, 3.5, 7.4), t0 + 0.12, 8, 3.0, 2)
    cam = C(t0, t1, (10.5, 6.5, 7.0), 12, 8.5, yaw=-12, pitch=2, lens=26, hh=3.4)
    cam.crash(t0 + 0.12, 24, 32, 0.1)
    sfx(t0 + 0.12, "u_slap", 1.0)
    sfx(t0 + 0.12, "hammer", 0.8)


@S(51, 212, 216, "Nobody touches my kid! (hero low angle)")
def s51(t0, t1):
    dump_scene()
    G = gary("Gary", (0, 5.0, 0), rot=0, scale=1.05, glow=True)
    G["arms"][0].rotation_euler = (rad(60), 0, rad(-20))
    G["arms"][1].rotation_euler = (rad(60), 0, rad(20))
    bounce(G["root"], t0, t1, 0.06, 6)
    light("herolight", "SPOT", (-6, -6, 3), 9000, (1.0, 0.9, 0.7), 1.5, target=(0, 5, 6), spot=60)
    cam = C(t0, t1, (0, 5.0, 6.8), 11, 7.0, yaw=-6, pitch=-16, lens=22, yaw1=8, drop=0, hh=1.6)
    cam.crash(t0 + 0.2, 22, 30, 0.12)
    sfx(t0 + 0.1, "u_rizz-sound-effect", 0.5)
    sfx(t0, "boom", 0.6)


@S(52, 216, 221, "I hugged his hairy leg")
def s52(t0, t1):
    dump_scene()
    gary("Gary", (0, 5.0, 0), rot=0, scale=1.05)
    E = eddie_pj(t0, t1, "relief")
    E.pose(t0, loc=(0.0, 1.0, 0), rot=0)
    E.pose(t0 + 0.4, loc=(0.9, 3.9, 0), rot=10)
    E.pose(t0 + 0.5, armL=(120, 0), armR=(120, 0))
    cam = C(t0, t1, (0.5, 3.0, 3.0), 10, 6.6, yaw=-30, pitch=6, lens=26, yaw1=-10, hh=1.0)
    sfx(t0 + 0.4, "aww", 0.7)
    sfx(t0 + 0.5, "pop", 0.5)


@S(53, 221, 225, "Sorry. I'm never too")
def s53(t0, t1):
    dump_scene()
    E = eddie_pj(t0, t1, "cry")
    E.pose(t0, loc=(0, 2.0, 0), rot=0)
    E.act(t0 + 0.2, "slump", expr="cry")
    cam = C(t0, t1, (0, 2.0, 4.6), 8.0, 4.4, yaw=-10, pitch=2, lens=32, yaw1=6, hh=0.9, fstop=3.5)
    sfx(t0, "sparkle", 0.4)


@S(54, 225, 228, "old for you. (Gary tearing up, smiling)")
def s54(t0, t1):
    dump_scene()
    G = gary("Gary", (0, 4.0, 0), rot=0, scale=1.0, tears=True)
    bounce(G["root"], t0, t1, 0.08, 5)
    cam = C(t0, t1, (0, 4.0, 6.0), 9, 5.0, yaw=0, pitch=0, lens=32, drop=0, hh=0.9, fstop=3.5)
    sfx(t0, "aww", 0.7)
    sfx(t0 + 0.4, "u_applepay", 0.4)


@S(55, 228, 233, "That night, he went back (Gary walks home)")
def s55(t0, t1):
    night_room()
    G = gary("Gary", (13.0, -3.0, 4.5), rot=90, scale=0.78)
    E = eddie_pj(t0, t1, "smile")
    E.pose(t0, loc=(10.5, -3.0, 0), rot=90)
    move(G["root"], t0, loc=(13.0, -3.0, 4.5), rot=(0, 0, 90))
    move(G["root"], t0 + 0.7, loc=(9.0, -3.0, 0.0), rot=(0, 0, 90), ease="EASE_OUT")
    move(G["root"], t1, loc=(-1.0, -3.0, 0.0), rot=(0, 0, 90))
    E.pose(t1, loc=(-3.0, -3.0, 0), rot=90)
    cam = Cam()
    cam.key(t0, (4.0, -13, 5.0), (8, -3, 3.5), lens=24)
    cam.key(t1, (-2, -12, 4.5), (-2, -3, 3.5), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.5, "footsteps", 0.9)
    sfx(t0 + 0.7, "window", 0.5)


@S(56, 233, 236, "under the bed (Gary slides into the gap)")
def s56(t0, t1):
    night_room()
    E = eddie_pj(t0, t1, "smile")
    lie_in_bed(E, t0)
    G = gary("Gary", (GAP[0] + 0.5, -3.6, 0), rot=0, scale=0.55)
    move(G["root"], t0, loc=(GAP[0] + 0.5, -3.6, 0.0))
    move(G["root"], t0 + 0.5, loc=(GAP[0], -0.2, 0.0), ease="EASE_IN")
    move(G["root"], t1 - 0.06, loc=(GAP[0], 1.6, -0.2))
    hide(G, t0, True)
    hide(G, t1 - 0.03, False)
    cam = Cam()
    cam.key(t0, (-4.0, -10, 4.0), (-7.6, 0, 1.6), lens=24)
    cam.key(t1, (-5.5, -7.5, 2.8), (-7.6, 1.5, 2.2), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.1, "footsteps", 0.7)
    sfx(t0 + 0.55, "thud", 0.5)


@S(57, 236, 237, "Rawr! eyes in the dark")
def s57(t0, t1):
    night_room()
    Me = mat("gapeye", hexc("#fff3a0"), 0.2, emit=hexc("#fff3a0"), estr=8.0)
    for i in range(7):
        sphere(f"geye{i}", 0.17, (GAP[0] - 1.4 + i * 0.47, 0.3, GAP[2] + (0.18 if i % 2 else -0.1)), Me, (1, 0.4, 1.2), seg=12)
    cam = C(t0, t1, (GAP[0], 0.3, GAP[2]), 8.5, 5.0, yaw=0, pitch=2, lens=26, drop=0, hh=2.2, fstop=4)
    cam.crash(t0, 26, 36, 0.1)
    pop_text("rawr2", "RAWR!", (-7.6, -4.5, 3.6), t0 + 0.02, 0.6, 1.2, "#ffe066")
    sfx(t0, "zombie", 0.9)
    sfx(t0, "u_capcut-explosion-sound", 0.5)


@S(58, 237, 243, "But yesterday, my little sister said...")
def s58(t0, t1):
    warm_room()
    S_ = sis(t0, t1, "talk")
    S_.pose(t0, loc=(1.0, 0.0, 0), rot=0)
    lips(S_, t0, t1)
    S_.act(t0 + 0.3, "point")
    S_.act(t0 + 1.2, "shrug", expr="talk")
    E = eddie_pj(t0, t1, "sus")
    E.pose(t0, loc=(-2.4, -1.0, 0), rot=15)
    E.act(t0 + 0.3, "think")
    cam = C(t0, t1, (-0.2, -0.5, 3.8), 10, 6.6, yaw=-10, pitch=3, lens=26, yaw1=10, hh=1.0)
    sfx(t0 + 0.4, "rimshot", 0.2)


@S(59, 243, None, "her monster is scared of Gary (tiny monster, giant Gary)")
def s59(t0, t1):
    world((0.08, 0.06, 0.16), 0.3)
    box("sfloor", (60, 60, 0.4), (0, 0, -0.2), mat("srug2", hexc("#7a5a8a"), 0.8), 0)
    box("swall", (60, 0.5, 30), (0, 22, 15), mat("swallm2", hexc("#8a7aa8"), 0.8), 0)
    light("moon", "AREA", (4, -14, 16), 7000, (0.5, 0.6, 1.0), 12, target=(0, 4, 2))
    light("back", "SPOT", (0, -2, 30), 60000, (1.0, 0.9, 0.7), 2.0, target=(0, 6, 0), spot=40)
    tiny = nm("Tiny", (0, 4.0, 0), rot=0, scale=0.32)
    swing(tiny["root"], t0, t1, 2, 4, 14, 0)
    swing(tiny["arms"][0], t0, t1, 0, 12, 10, 120)
    swing(tiny["arms"][1], t0, t1, 0, -12, 10, 120)
    G = gary("Gary", (0, 16.0, 0), rot=0, scale=1.9)
    move(G["root"], t0, loc=(0, 16.0, 0))
    move(G["root"], t1, loc=(0, 13.0, 0))
    cam = Cam()
    cam.key(t0, (0, -6, 2.4), (0, 4, 2.0), lens=30)
    cam.key(t1, (0, -2.0, 1.8), (0, 4, 1.8), lens=30, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0 + 0.5, "u_duck-toy-sound", 0.6)
    sfx(t0 + 1.4, "u_faaah", 0.5)
