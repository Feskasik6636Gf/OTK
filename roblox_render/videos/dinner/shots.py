"""dinner / "What's for dinner?": every time someone asks, dinner is pushed back one hour.
Narrator asks it 500 times, the Table Eater under the town square starves. Shots keyed to script word indices."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from rbx.sets import wood

V = Video(__file__)
story.bind(V)

TABLE_Z = 2.8
CTOP = 3.2
TBL = (1.0, -5.0)           # kitchen table centre
SQ = (0.0, -20.0)           # town square centre


def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def emitm(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


def head(p, s=1.0):
    return (p[0], p[1], p[2] + 4.6 * s)


# ================================================================== cast
def dad_c(t0, t1, expr="neutral", s=1.0):
    d = chars.Char("Dad", skin="#e9c7a6", shirt="#3f7fd9", pants="#c8b48a", hair="short", hair_color="#3a2a1e",
                   face="mustache", vneck="#f4f4f4", scale=s)
    return story._live(d, t0, t1, expr, 0.6)


def mom_c(t0, t1, expr="neutral"):
    m = chars.Char("Mom", skin="#f1dfc6", shirt="#e8423a", pants="#2b2b3a", hair="bob", hair_color="#7a3a1e",
                   face="girl", sleeves="long", vneck="#f6c0a8")
    return story._live(m, t0, t1, expr)


def hero(t0, t1, expr="neutral"):
    return story.eddie(t0, t1, expr)


def bro(t0, t1, expr="neutral"):
    return story.leo(t0, t1, expr)


def at(ch, t, p, to=None, rot=None):
    ch.pose(t, loc=p, rot=facing(p, to) if rot is None else rot)
    return ch


def pop_text(name, body, loc, t, size=1.0, col="#ffe14a", yaw=0, dur=None, outline="#1a1a22"):
    root = empty(name, loc, rot=(0, 0, yaw))
    text(name + "_t", body, (0, 0, 0), size, emitm(col, 2.5), extrude=0.08 * size, parent=root)
    text(name + "_o", body, (0.04 * size, 0.06 * size, -0.04 * size), size, M(outline, 0.6), extrude=0.06 * size,
         parent=root)
    root.scale = (0.01,) * 3
    root.keyframe_insert("scale", frame=F(t - 0.04))
    root.scale = (1.3,) * 3
    root.keyframe_insert("scale", frame=F(t + 0.08))
    root.scale = (1.0,) * 3
    root.keyframe_insert("scale", frame=F(t + 0.16))
    if dur:
        root.keyframe_insert("scale", frame=F(t + dur - 0.1))
        root.scale = (0.01,) * 3
        root.keyframe_insert("scale", frame=F(t + dur))
    noise(root, "rotation_euler", 1, 0.05, 8)
    return root


def sparkle_on(name, loc, t, s=1.0, n=10, seed=0, col="#fff1a0"):
    rnd = random.Random(seed)
    Ms = mat("sp_" + col, hexc(col), 0.3, emit=hexc(col), estr=10)
    for i in range(n):
        p = Vector(loc) + Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.5, 1))) * s
        o = sphere(f"{name}{i}", 0.09 * s, tuple(p), Ms, seg=8)
        ts = t + rnd.uniform(0, 0.5)
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts - 0.05))
        o.scale = (1.6, 1.6, 1.6)
        o.keyframe_insert("scale", frame=F(ts + 0.08))
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts + 0.3))


def pop_in(ob, t, s=1.0, dur=0.18):
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.03))
    ob.scale = (s * 1.25,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur * 0.6))
    ob.scale = (s,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur))


def ding(t, loc, size=1.2, yaw=0, dur=0.9):
    r = pop_text(f"ding{F(t)}", "DING!", loc, t, size, "#ffd23a", yaw, dur)
    sfx(t, "ding", 1.0)
    return r


# ================================================================== props
def clock(name, loc, t0=None, t1=None, turns=1.0, yaw=0, r=1.3, coll=None):
    root = empty(name, loc, coll=coll, rot=(0, 0, yaw))
    cyl(name + "_b", r, 0.25, (0, 0, 0), M("#f6f0e0", 0.5), 32, rot=(90, 0, 0), parent=root, coll=coll)
    cyl(name + "_r", r * 1.1, 0.2, (0, 0.06, 0), M("#2a2a3a", 0.4), 32, rot=(90, 0, 0), parent=root, coll=coll)
    for k in range(12):
        a = math.radians(k * 30)
        box(f"{name}_t{k}", (0.07 * r, 0.04, 0.2 * r), (math.sin(a) * r * 0.82, -0.14, math.cos(a) * r * 0.82),
            M("#1a1a1a"), 0.01, parent=root, coll=coll, rot=(0, -k * 30, 0))
    pv = empty(name + "_pv", (0, -0.17, 0), parent=root, coll=coll)
    box(name + "_hand", (0.12 * r, 0.05, 0.75 * r), (0, 0, 0.32 * r), M("#c8261e"), 0.02, parent=pv, coll=coll)
    box(name + "_hand2", (0.08 * r, 0.05, 1.0 * r), (0, 0.01, 0.42 * r), M("#1a1a1a"), 0.02, parent=pv, coll=coll)
    if t0 is not None:
        pv.rotation_euler = (0, 0, 0)
        pv.keyframe_insert("rotation_euler", frame=F(t0))
        pv.rotation_euler = (0, math.radians(-360 * turns), 0)
        pv.keyframe_insert("rotation_euler", frame=F(t1))
        set_interp(pv, "rotation_euler", F(t0), "BEZIER", "EASE_OUT")
    return root


def plate(name, loc, coll=None, food="#f0c05a", s=1.0):
    cyl(name, 0.55 * s, 0.07, loc, M("#ffffff", 0.3), 20, coll=coll)
    sphere(name + "_f", 0.3 * s, (loc[0], loc[1], loc[2] + 0.12 * s), M(food, 0.7), (1, 1, 0.5), coll=coll, seg=10)


def pot(name, loc, coll=None, s=1.0, full=True, col="#6e7480"):
    cyl(name, 0.9 * s, 0.9 * s, (loc[0], loc[1], loc[2] + 0.45 * s), M(col, 0.3, metal=0.7), 24, coll=coll)
    if full:
        cyl(name + "_s", 0.8 * s, 0.05, (loc[0], loc[1], loc[2] + 0.86 * s), M("#d8532a", 0.5), 24, coll=coll)
    box(name + "_h1", (0.5 * s, 0.1, 0.1), (loc[0] + 1.05 * s, loc[1], loc[2] + 0.7 * s), M("#2a2a2a"), 0.02, coll=coll)
    box(name + "_h2", (0.5 * s, 0.1, 0.1), (loc[0] - 1.05 * s, loc[1], loc[2] + 0.7 * s), M("#2a2a2a"), 0.02, coll=coll)


def mic(name, loc, parent=None, coll=None):
    root = empty(name, loc, parent=parent, coll=coll)
    sphere(name + "_h", 0.32, (0, 0, 0.5), M("#3a3a42", 0.3, metal=0.6), parent=root, coll=coll, seg=14)
    cyl(name + "_s", 0.12, 0.8, (0, 0, 0), M("#1a1a22", 0.4), 10, parent=root, coll=coll)
    return root


def kitchen(night=False, table=True):
    world((0.9, 0.93, 1.0) if not night else (0.12, 0.15, 0.3), 0.45 if not night else 0.6)
    c = collection("KITCH")
    box("k_floor", (60, 50, 0.4), (0, 0, -0.2), sets.checker_mat("k_fl", "#f2ece0", "#d8cdb8", 0.18), 0, coll=c)
    box("k_back", (60, 0.5, 16), (0, 8.25, 8), M("#bfe0d0", 0.85), 0, coll=c)
    box("k_left", (0.5, 50, 16), (-16, 0, 8), M("#b0d4c4", 0.85), 0, coll=c)
    Mc = wood("k_cab", "#e8e2d4", "#f4efe4", 2.0)
    box("k_counter", (20, 3.2, CTOP - 0.2), (0, 6.5, (CTOP - 0.2) / 2), M("#4f86c6", 0.6), 0.06, coll=c)
    box("k_top", (20.4, 3.5, 0.2), (0, 6.4, CTOP - 0.1), M("#f4f1ea", 0.25), 0.04, coll=c)
    for i in range(5):
        box(f"k_door{i}", (3.4, 0.08, 2.2), (-8 + i * 4, 4.86, 1.6), M("#5f96d6", 0.55), 0.06, coll=c)
    for i in range(4):
        box(f"k_up{i}", (3.6, 1.6, 3.0), (-6 + i * 4, 7.4, 10.0), Mc, 0.08, coll=c)
    box("k_wfr", (5.0, 0.3, 4.0), (-5, 8.0, 7.0), M("#f4f4f4"), 0.04, coll=c)
    card("k_wsky", 4.4, 3.4, (-5, 7.85, 7.0), emitm("#bfe3ff", 2.5), "-Y", coll=c)
    box("k_fridge", (4, 3.6, 9), (-12.5, 6.2, 4.5), M("#e8eef4", 0.25, metal=0.3), 0.15, coll=c)
    clock("k_clk", (6.5, 7.7, 9.5), coll=c, r=1.4)
    if table:
        Mt = wood("k_tab", "#a0703f", "#c89260", 2.0)
        box("k_table", (9, 5, 0.3), (TBL[0], TBL[1], TABLE_Z - 0.15), Mt, 0.06, coll=c)
        for sx in (-1, 1):
            for sy in (-1, 1):
                box(f"k_tl{sx}{sy}", (0.35, 0.35, TABLE_Z - 0.3), (TBL[0] + sx * 4.0, TBL[1] + sy * 2.1, (TABLE_Z - 0.3) / 2),
                    M("#704a2a"), 0.02, coll=c)
    light("k_key", "AREA", (0, -8, 13), 5500, (1.0, 0.97, 0.92), 12, coll=c, target=(0, 0, 2))
    light("k_fill", "AREA", (-10, -10, 6), 1800, (0.9, 0.95, 1.0), 6, coll=c, target=(0, 0, 3))
    return c


def square(banner=True, tables=True, dusk=False, hall_clock=True):
    W.sky(1.0)
    W.sun(4.0, rot=(52, 0, 28))
    c = collection("SQ")
    box("sq_ground", (400, 400, 0.4), (0, 0, -0.3), mat("grass", hexc("#5fb04a"), 0.9), 0, coll=c)
    box("sq_plaza", (90, 70, 0.3), (0, -10, -0.05), sets.checker_mat("sq_pl", "#e8dcc0", "#d8c9a8", 0.3), 0, coll=c)
    # town hall at the back
    box("th_body", (34, 12, 14), (0, 32, 7), M("#d9453a", 0.6), 0.3, coll=c)
    box("th_roof", (36, 14, 2), (0, 32, 15), M("#4a3a30", 0.7), 0.3, coll=c)
    box("th_tower", (8, 8, 12), (0, 32, 22), M("#f2c14e", 0.6), 0.3, coll=c)
    box("th_tower_roof", (9.4, 9.4, 2), (0, 32, 29), M("#4a3a30", 0.7), 0.3, coll=c)
    box("th_door", (6, 0.6, 8), (0, 25.8, 4), M("#4a2e20", 0.6), 0.1, coll=c)
    text("th_sign", "TOWN HALL", (0, 25.6, 11.2), 1.8, emitm("#fff2c0", 1.8), extrude=0.1, coll=c)
    if hall_clock:
        clock("th_clock", (0, 27.5, 22), coll=c, r=3.0)
    for k in range(5):
        box(f"th_w{k}", (3, 0.4, 4), (-12 + k * 6 if k != 2 else 0, 25.7, 9.5 if k == 2 else 5), M("#bfe3ff", 0.2), 0.05, coll=c)
    # houses left and right
    for k in range(6):
        for sx in (-1, 1):
            hh = 8 + (k * 3) % 7
            box(f"h{sx}{k}", (12, 12, hh), (sx * 52, -30 + k * 22, hh / 2),
                M(["#e2725b", "#f2c14e", "#6fb3e0", "#9b8fd6", "#8fd18c", "#f59bb5"][(k + (sx > 0)) % 6], 0.7), 0.2, coll=c)
            box(f"hr{sx}{k}", (13, 13, 1.2), (sx * 52, -30 + k * 22, hh + 0.6), M("#a33b2f", 0.7), 0.2, coll=c)
    if banner:
        cyl("flag_pole1", 0.25, 12, (-26, 8, 6), M("#cccccc"), 8, coll=c)
        cyl("flag_pole2", 0.25, 12, (26, 8, 6), M("#cccccc"), 8, coll=c)
        box("flag_banner", (53, 0.3, 3.2), (0, 8, 11), emitm("#ffd23a", 1.2), 0.1, coll=c)
        text("flag_txt", "TOWN DINNER FESTIVAL", (0, 7.7, 11), 2.1, M("#c8261e", 0.5), extrude=0.1, coll=c)
    if tables:
        for r in range(7):
            for k in range(11):
                x, y = -34 + k * 6.8, -38 + r * 6.6
                if abs(x) < 3 and abs(y - 16) < 5:
                    continue
                box(f"tb{r}_{k}", (4.6, 2.6, 0.25), (x, y, 2.4), M("#a0703f", 0.7), 0.04, coll=c)
                box(f"tc{r}_{k}", (4.7, 2.7, 0.08), (x, y, 2.55), M("#ffffff" if (r + k) % 2 else "#e8423a", 0.8), 0.02, coll=c)
                box(f"tl{r}_{k}", (0.3, 0.3, 2.3), (x, y, 1.15), M("#704a2a"), 0.02, coll=c)
                if (r * 3 + k) % 2 == 0:
                    plate(f"pl{r}_{k}", (x, y, 2.65), c)
    light("sq_fill", "AREA", (0, -40, 30), 4000, (1, 1, 1), 40, coll=c, target=(0, 0, 0))
    return c


def monster(name="Eater", loc=(0, 8, 0), s=1.0, coll=None, mood="angry"):
    c = coll or collection("MON_" + name)
    root = empty(name, loc, coll=c, rot=(0, 0, 0))
    root.scale = (s,) * 3
    Mp, Md = M("#7a4fd0", 0.55), M("#4a2f90", 0.6)
    sphere(name + "_body", 7.0, (0, 0, 7.0), Mp, (1.0, 0.9, 1.0), parent=root, coll=c, seg=32)
    sphere(name + "_belly", 5.2, (0, -3.4, 5.5), M("#b99cf0", 0.6), (1.0, 0.6, 1.0), parent=root, coll=c, seg=24)
    sphere(name + "_head", 5.0, (0, -0.5, 15.2), Mp, (1.15, 1.0, 0.95), parent=root, coll=c, seg=32)
    for sx in (-1, 1):
        sphere(f"{name}_eyeW{sx}", 1.5, (sx * 2.2, -4.2, 16.6), M("#ffffff", 0.2), parent=root, coll=c, seg=16)
        sphere(f"{name}_eyeP{sx}", 0.7, (sx * 2.2, -5.5, 16.6), M("#101018", 0.2), parent=root, coll=c, seg=12)
        cone_h = box(f"{name}_horn{sx}", (1.2, 1.2, 3.2), (sx * 3.4, -0.5, 20.3), M("#f2e8c0", 0.4), 0.3, parent=root,
                     coll=c, rot=(0, sx * 18, 0))
        box(f"{name}_brow{sx}", (3.0, 0.7, 0.8), (sx * 2.2, -4.4, 18.4), Md, 0.2, parent=root, coll=c,
            rot=(0, sx * (-18 if mood == "angry" else 18), 0))
    jaw = empty(name + "_jaw", (0, -4.3, 13.0), parent=root, coll=c)
    box(name + "_mouth", (5.6, 1.0, 2.4), (0, 0.1, 0), M("#2a0a14", 0.9), 0.4, parent=jaw, coll=c)
    for k in range(6):
        box(f"{name}_tu{k}", (0.6, 0.5, 0.9), (-2.5 + k * 1.0, -0.4, 1.0), M("#ffffff", 0.3), 0.1, parent=jaw, coll=c)
    tong = box(name + "_tongue", (3.0, 0.6, 0.6), (0, -0.2, -0.9), M("#e8566a", 0.6), 0.2, parent=jaw, coll=c)
    # napkin round the neck
    box(name + "_napkin", (9.0, 3.0, 5.0), (0, -4.2, 9.8), M("#ffffff", 0.8), 0.3, parent=root, coll=c, rot=(-12, 0, 0))
    for k in range(5):
        box(f"{name}_nst{k}", (9.2, 3.1, 0.55), (0, -4.2, 8.0 + k * 1.1), M("#e8423a", 0.8), 0.1, parent=root, coll=c,
            rot=(-12, 0, 0))
    for sx in (-1, 1):
        arm = empty(f"{name}_arm{sx}", (sx * 7.4, 0, 9.0), parent=root, coll=c)
        cyl(f"{name}_ac{sx}", 1.5, 7, (0, 0, -3.0), Mp, 16, parent=arm, coll=c)
        sphere(f"{name}_ah{sx}", 2.1, (0, 0, -7.0), Md, parent=arm, coll=c, seg=14)
        cyl(f"{name}_leg{sx}", 2.4, 4.5, (sx * 3.4, -0.5, 2.0), Md, 16, parent=root, coll=c)
    
    return root, jaw


def mon_rise(root, t0, t1, z0=-26.0, z1=0.0):
    root.location = (root.location[0], root.location[1], z0)
    root.keyframe_insert("location", frame=F(t0))
    root.location = (root.location[0], root.location[1], z1)
    root.keyframe_insert("location", frame=F(t1))
    set_interp(root, "location", F(t0), "BEZIER", "EASE_OUT")


def jaw_chomp(jaw, t0, t1, rate=3.0, amp=-30):
    t = t0
    k = 0
    while t <= t1:
        jaw.rotation_euler = (math.radians(0 if k % 2 == 0 else amp), 0, 0)
        jaw.keyframe_insert("rotation_euler", frame=F(t))
        t += 0.5 / rate
        k += 1


def shake_obj(ob, t0, t1, amp=0.25, rate=14):
    t = t0
    k = 0
    base = Vector(ob.location)
    while t <= t1:
        ob.location = base + Vector((amp * (1 if k % 2 else -1), amp * 0.3 * (1 if k % 3 else -1), 0))
        ob.keyframe_insert("location", frame=F(t))
        t += 1.0 / rate
        k += 1
    ob.location = base
    ob.keyframe_insert("location", frame=F(t1))


def mover(t0, t1, k, tgt, d, pitch=4, lens=30, hh=0.6, yaw=0, fstop=2.6, wide=False):
    """Camera moves cycled by k so the cut feels alive: push, pull, orbit, dutch push, crash."""
    cam = Cam()
    m = k % 6
    if m == 0:
        cam.push(t0, t1, tgt, d * 1.35, d * 0.78, yaw=yaw, yaw1=yaw + 8, pitch=pitch, lens=lens, fstop=fstop)
    elif m == 1:
        cam.orbit(t0, t1, tgt, d, yaw - 22, yaw + 22, pitch=pitch, lens=lens, fstop=fstop)
    elif m == 2:
        cam.push(t0, t1, tgt, d * 0.8, d * 1.3, yaw=yaw + 14, yaw1=yaw - 6, pitch=pitch, lens=lens, fstop=fstop)
    elif m == 3:
        cam.push(t0, t1, tgt, d * 1.25, d * 0.72, yaw=yaw - 12, yaw1=yaw + 4, pitch=pitch + 4, lens=lens, fstop=fstop,
                 roll=0.07)
    elif m == 4:
        cam.orbit(t0, t1, tgt, d, yaw + 24, yaw - 18, pitch=pitch, lens=lens, fstop=fstop, pitch1=pitch + 6)
    else:
        cam.push(t0, t1, tgt, d * 1.1, d * 0.85, yaw=yaw, yaw1=yaw - 10, pitch=pitch - 2, lens=lens, fstop=fstop)
        cam.crash(t0 + 0.05, lens, lens * 1.3, 0.14)
    cam.handheld(hh)
    return cam


FAM = {"dad": (-2.6, -1.0), "mom": (1.0, -1.0), "bro": (4.6, -1.0), "me": (-4.6, -5.0)}


def family(t0, t1, ex="neutral", hungry=False, who=("dad", "mom", "bro", "me")):
    out = {}
    mk = {"dad": dad_c, "mom": mom_c, "bro": bro, "me": hero}
    for w_ in who:
        ch = mk[w_](t0, t1, ex)
        p = FAM[w_]
        at(ch, t0, (p[0], p[1], 0.0), to=(1.0, -5.0) if w_ == "me" else (p[0], -12.0))
        if w_ == "me":
            ch.root.rotation_euler[2] = math.radians(90)
            ch.pose(t0, rot=90)
        if hungry:
            ch.act(t0, "slump", expr="sleepy")
        out[w_] = ch
    return out


# ================================================================== HOOK
@S(1, 0, 5, "HOOK: narrator at the table slams hands, asks WHAT'S FOR DINNER")
def s01(t0, t1):
    kitchen()
    fm = family(t0, t1, "bored", who=("dad", "mom", "bro"))
    for ch in fm.values():
        ch.act(t0, "slump", expr="sleepy")
    me = hero(t0, t1, "shout")
    at(me, t0, (-3.2, -5.0, 0), rot=90)
    me.act(t0 + 0.2, "push", expr="shout")
    lips(me, t0, t1, "shout")
    tgt = (-1.6, -5, 5.2)
    cam = Cam()
    cam.whip(t0, t0 + 0.25, (6, -9, 4.5), (0, -2, 3.5), (-8.5, -9.0, 5.6), tgt, lens=26)
    cam.key(t1, (-5.2, -8.2, 5.6), (-3.0, -5, 5.3), lens=34, focus=tgt, fstop=2.2)
    cam.crash(t0 + 0.9, 28, 40, 0.1)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "slap", 0.7)
    sfx(t0, "whoosh", 0.7)


@S(2, 5, 9, "so many times: tally marks wall, narrator counting")
def s02(t0, t1):
    kitchen()
    me = hero(t0, t1, "sus")
    at(me, t0, (-1.0, 3.5, 0.0), rot=0)
    me.act(t0, "think", expr="sus")
    lips(me, t0, t1)
    # tally wall
    for i in range(30):
        box(f"tally{i}", (0.1, 0.05, 1.0), (-8 + (i % 10) * 0.6 + (i // 10) * 0.0, 7.95, 6.6 - (i // 10) * 1.3),
            M("#2a2a3a"), 0.02, rot=(0, (i % 5 == 4) * 60, 0))
    mover(t0, t1, 1, head((-1.0, 3.5, 0)), 7.0, pitch=2, lens=30, yaw=-8)


@S(3, 9, 15, "family hasn't eaten since Tuesday: starving slump, cobwebs, TUESDAY calendar")
def s03(t0, t1):
    kitchen()
    fm = family(t0, t1, "sleepy", hungry=True)
    for k in fm.values():
        k.face(w(12), "cry")
    pop_text("tue", "TUESDAY", (6, 7.5, 6.5), w(14), 1.6, "#ffffff", 0)
    box("cal", (4.4, 0.2, 3.6), (6, 7.9, 6.2), M("#fff8e0", 0.8), 0.1)
    cam = Cam()
    cam.key(t0, (-9, -14, 4.0), (-1, -2, 3.6), lens=24, focus=14, fstop=5)
    cam.key(t1, (4, -12, 5.4), (0, -2, 3.8), lens=24, focus=12, fstop=5)
    cam.handheld(0.8)
    sfx(w(14), "faaah", 0.6)


@S(4, 15, 21, "AND IT SAVED THE WHOLE TOWN: epic hero on roof, crane up")
def s04(t0, t1):
    square()
    me = hero(t0, t1, "grin")
    at(me, t0, (0, -6, 0), rot=0)
    me.act(t0, "fists", expr="grin")
    sparkle_on("hr", (0, -6, 5.2), w(18), 1.0, 14, seed=4)
    cam = Cam()
    cam.key(t0, (0, -12, 1.0), (0, -6, 4.2), lens=24, focus=6, fstop=3)
    cam.key(t1, (-6, -30, 15), (0, 5, 8), lens=28, focus=30, fstop=8)
    cam.handheld(0.5)
    sfx(t0, "rise", 0.7)
    sfx(w(18), "sparkle", 0.8)


@S(5, 21, 26, "You see, in this world: narrator to camera")
def s05(t0, t1):
    kitchen(table=False)
    me = hero(t0, t1, "smug")
    p = (0, -2, 0)
    at(me, t0, p, rot=0)
    me.act(t0, "cross", expr="smug")
    lips(me, t0, t1)
    cam = Cam()
    cam.push(t0, t1, head(p), 6.5, 3.4, yaw=-10, yaw1=0, pitch=-2, lens=34, fstop=2.0)
    cam.handheld(0.7)
    sfx(t0, "whoosh", 0.5)


@S(6, 26, 33, "every time someone asks: narrator, big speech-bubble words")
def s06(t0, t1):
    kitchen(table=False)
    me = hero(t0, t1, "talk")
    p = (0, -2, 0)
    at(me, t0, p, rot=0)
    me.act(t0, "point", expr="talk")
    lips(me, t0, t1)
    pop_text("q", "WHAT'S FOR DINNER?", (0, -4.5, 9.0), w(30), 1.0, "#ffffff", 0, dur=2.0)
    mover(t0, t1, 4, head(p), 5.5, pitch=2, lens=30, yaw=18)
    sfx(w(30), "pop", 0.8)


@S(7, 33, 39, "dinner pushed back one hour: clock spins, +1 HOUR")
def s07(t0, t1):
    kitchen(table=False)
    c = collection("CLK")
    clock("big", (0, 3.0, 5.0), w(35), w(38), turns=1 / 12, r=3.4, coll=c)
    pop_text("hr", "+1 HOUR", (0, 2.0, 9.4), w(37), 1.6, "#ff5a3c", 0, dur=2.0)
    cam = Cam()
    cam.push(t0, t1, (0, 3, 5.4), 12, 6.5, yaw=-6, yaw1=6, pitch=2, lens=32, fstop=4)
    cam.crash(w(37), 32, 46, 0.12)
    cam.handheld(0.5)
    sfx(w(35), "click", 0.8)
    sfx(w(37), "boom", 0.4)


@S(8, 39, 40, "DING!")
def s08(t0, t1):
    kitchen(table=False)
    ding(t0, (0, -2, 6.5), 2.4)
    me = hero(t0, t1, "shock")
    at(me, t0, (0, -2, 0), rot=0)
    me.act(t0, "recoil", expr="shock")
    cam = Cam()
    cam.key(t0, (0, -14, 5), (0, -2, 5), lens=26, focus=12, fstop=4)
    cam.key(t1, (0, -10, 5), (0, -2, 5), lens=26, focus=8, fstop=4)
    cam.crash(t0, 24, 38, 0.1)
    cam.shake(0.025, 3)


def street_bg():
    W.sky(1.0)
    W.sun(4.0, rot=(52, 0, 28))
    c = collection("ST")
    box("st_g", (300, 300, 0.4), (0, 0, -0.2), mat("grass2", hexc("#5fb04a"), 0.9), 0, coll=c)
    box("st_road", (300, 14, 0.1), (0, 0, 0.06), mat("asph", hexc("#55565e"), 0.8), 0, coll=c)
    for i in range(14):
        box(f"st_d{i}", (4, 0.4, 0.05), (-45 + i * 7, 0, 0.14), M("#f2c14e", 0.5), 0, coll=c)
    cols = ["#e2725b", "#f2c14e", "#6fb3e0", "#9b8fd6", "#8fd18c", "#f59bb5"]
    for i in range(10):
        hh = 8 + (i * 5) % 7
        box(f"st_h{i}", (11, 10, hh), (-50 + i * 11.5, 16, hh / 2), M(cols[i % 6], 0.7), 0.2, coll=c)
        box(f"st_r{i}", (12, 11, 1.2), (-50 + i * 11.5, 16, hh + 0.6), M("#a33b2f", 0.7), 0.2, coll=c)
    box("st_sw", (300, 6, 0.2), (0, 9, 0.1), M("#c9c5b8", 0.7), 0, coll=c)
    light("st_fill", "AREA", (0, -30, 25), 5000, (1, 1, 1), 40, coll=c, target=(0, 0, 0))
    return c


@S(9, 40, 44, "So everyone is careful: townsfolk tiptoe, hands over mouths")
def s09(t0, t1):
    street_bg()
    for i in range(7):
        a = story.townie(i * 3 + 1, t0, t1, "scared")
        x0 = -16 + i * 5.2
        a.pose(t0, loc=(x0, 3.0 - (i % 2) * 2.2, 0), rot=-90 + (i % 2) * 180)
        a.walk(t0, t1, (x0, 3.0 - (i % 2) * 2.2, 0), (x0 + (4 if i % 2 else -4), 3.0 - (i % 2) * 2.2, 0), rate=1.3, swing=14)
        a.act(t0, "hands_face", expr="scared")
    cam = Cam()
    cam.key(t0, (-6, -22, 4.0), (-2, 2, 3.0), lens=20, focus=24, fstop=7)
    cam.key(t1, (6, -20, 4.5), (2, 2, 3.0), lens=20, focus=22, fstop=7)
    cam.handheld(0.8)
    sfx(t0, "footsteps", 0.5)


@S(10, 44, 47, "Moms say Surprise!")
def s10(t0, t1):
    kitchen(table=False)
    mo = mom_c(t0, t1, "grin")
    p = (0, -2, 0)
    at(mo, t0, p, rot=0)
    mo.act(t0, "wave", expr="joy")
    lips(mo, t0, t1)
    confetti("cf", (0, -3, 7), (3, 2, 2), w(46), dur=1.4, n=60, seed=3)
    pop_text("sur", "SURPRISE!", (0, -3.5, 9.5), w(46), 1.2, "#ff8ad8", 0, dur=1.4)
    mover(t0, t1, 3, head(p, 0.8), 9.5, pitch=0, lens=28, yaw=-12)
    sfx(w(46), "confetti", 0.8)


@S(11, 47, 50, "Dads say Food.")
def s11(t0, t1):
    kitchen(table=False)
    da = dad_c(t0, t1, "bored")
    p = (0, -2, 0)
    at(da, t0, p, rot=0)
    da.act(t0, "point", expr="bored")
    lips(da, t0, t1)
    pop_text("fd", "FOOD.", (0, -3.5, 9.0), w(49), 1.3, "#ffffff", 0, dur=1.4)
    mover(t0, t1, 5, head(p), 5.4, pitch=0, lens=32, yaw=14)
    sfx(w(49), "pop", 0.8)


@S(12, 50, 53, "Grandma hands you a pickle")
def s12(t0, t1):
    kitchen(table=False)
    g = story.grandma(t0, t1, "smile")
    at(g, t0, (1.0, -2.0, 0), rot=-25)
    g.act(t0, "reach", expr="smile")
    pk = cyl("pickle", 0.38, 1.6, (-0.4, -3.8, 4.1), M("#4f9a2a", 0.5), 14, rot=(90, 0, 0))
    pop_in(pk, w(52))
    k = story.townie(4, t0, t1, "happy")
    at(k, t0, (-2.4, -5.5, 0), to=(1.0, -2.0))
    k.act(t0, "reach", expr="happy")
    tgt = (-0.5, -3.8, 4.0)
    mover(t0, t1, 1, (0, -3, 4.2), 11.0, pitch=0, lens=30, yaw=-8)
    sfx(w(52), "pop", 0.7)


@S(13, 53, 59, "pickle in hand, grandma walks away, kid stares")
def s13(t0, t1):
    street_bg()
    g = story.grandma(t0, t1, "smile")
    g.walk(t0, t1, (-2, 2, 0), (14, 2, 0), rate=1.6)
    k = story.townie(4, t0, t1, "shock")
    at(k, t0, (-6, 2, 0), rot=-90)
    k.act(t0, "hold", expr="confused")
    pk = cyl("pickle2", 0.38, 1.6, (-6.9, 1.2, 3.4), M("#4f9a2a", 0.5), 14, rot=(0, 20, 0))
    cam = Cam()
    cam.key(t0, (-4, -14, 3.0), (-3, 2, 3.4), lens=24, focus=16, fstop=5)
    cam.key(t1, (4, -16, 3.6), (4, 2, 3.4), lens=22, focus=18, fstop=5)
    cam.handheld(0.8)
    sfx(w(57), "footsteps", 0.5)


@S(14, 59, 63, "But I always ask: narrator sneaky smirk, orbit")
def s14(t0, t1):
    kitchen(table=False)
    me = hero(t0, t1, "smug")
    p = (0, -2, 0)
    at(me, t0, p, rot=0)
    me.act(t0, "lean", expr="smug")
    lips(me, t0, t1)
    mover(t0, t1, 4, head(p), 4.4, pitch=-2, lens=35, yaw=-20)


@S(15, 63, 66, "What's for dinner? (1) crash zoom")
def s15(t0, t1):
    kitchen(table=False)
    me = hero(t0, t1, "shout")
    p = (0, -2, 0)
    at(me, t0, p, rot=0)
    me.act(t0, "shrug", expr="shout")
    lips(me, t0, t1, "shout")
    cam = Cam()
    cam.key(t0, orbit_pos(head(p), 7, 18, 0), head(p), lens=28, focus=head(p), fstop=2.2)
    cam.key(t1, orbit_pos(head(p), 3.2, 4, 0), head(p), lens=34, focus=head(p), fstop=2.2, ease="EASE_IN")
    cam.crash(t0 + 0.5, 34, 48, 0.12)
    cam.handheld(1.0)
    sfx(t0, "pop", 0.6)


@S(16, 66, 69, "What's for dinner? (2) other side, bigger")
def s16(t0, t1):
    kitchen(table=False)
    me = hero(t0, t1, "shout")
    p = (0, -2, 0)
    at(me, t0, p, rot=0)
    me.act(t0, "point", expr="shout")
    lips(me, t0, t1, "shout")
    cam = Cam()
    cam.key(t0, orbit_pos(head(p), 6, -30, 6), head(p), lens=26, focus=head(p), fstop=2.2)
    cam.key(t1, orbit_pos(head(p), 2.6, -8, 2), head(p), lens=38, focus=head(p), fstop=2.2, ease="EASE_IN")
    cam.crash(t0 + 0.4, 36, 52, 0.1)
    cam.handheld(1.2)
    sfx(t0, "pop", 0.7)


@S(17, 69, 70, "DING!")
def s17(t0, t1):
    kitchen(table=False)
    c = collection("CLK2")
    clock("big", (0, 3.0, 5.0), t0, t1 + 0.4, turns=1 / 12, r=3.4, coll=c)
    ding(t0, (0, 1.8, 9.4), 2.0)
    cam = Cam()
    cam.key(t0, (0, -9, 5.6), (0, 3, 5.4), lens=28, focus=12, fstop=4)
    cam.key(t1, (0, -7, 5.6), (0, 3, 5.4), lens=28, focus=10, fstop=4)
    cam.crash(t0, 26, 40, 0.1)
    cam.shake(0.03, 3)


# ---- family chaos
@S(18, 70, 75, "brother chewed the remote")
def s18(t0, t1):
    kitchen(table=False)
    b = bro(t0, t1, "grin")
    p = (0, -2, 0)
    at(b, t0, p, rot=0)
    b.act(t0, "reach", expr="grin")
    remote = box("remote", (0.5, 0.25, 1.5), (0, -3.4, 3.8), M("#222428", 0.4), 0.06, rot=(0, 90, 20))
    box("remote_b", (0.12, 0.02, 0.12), (0.1, -3.55, 3.9), M("#e8423a"), 0.01, rot=(0, 90, 20))
    b.talk(t0, t1, open_m="laugh", wide_m="open_smile", rest="laugh")
    shake_obj(remote, w(72), w(74), 0.1, 16)
    mover(t0, t1, 2, (0, -3, 4.6), 4.8, pitch=0, lens=30, yaw=0)
    sfx(w(72), "snort", 0.5)
    sfx(w(72) + 0.1, "click", 0.7)


@S(19, 75, 79, "dad ate a candle")
def s19(t0, t1):
    kitchen(table=False)
    d = dad_c(t0, t1, "smile")
    p = (0, -2, 0)
    at(d, t0, p, rot=0)
    d.act(t0, "hold", expr="smile")
    candle = cyl("candle", 0.25, 1.6, (0, -3.4, 3.9), M("#f7ecd0", 0.5), 12)
    fl = sphere("flame", 0.16, (0, -3.4, 4.85), emitm("#ffb030", 6), (1, 1, 1.6), seg=8)
    pop_in(candle, t0 + 0.05)
    candle.scale = (1, 1, 1)
    d.talk(t0, t1, open_m="talk_wide", wide_m="talk", rest="flat")
    mover(t0, t1, 0, head(p), 4.6, pitch=0, lens=30, yaw=-14)
    sfx(w(77) + 0.1, "snort", 0.6)


def soup_scene(t0, t1, mom_ex, ice=0.0, hist=False, tgt=(0, -3, 3.8)):
    kitchen(table=False)
    mo = mom_c(t0, t1, mom_ex)
    at(mo, t0, (0, -1.5, 0), rot=0)
    mo.act(t0, "hold", expr=mom_ex)
    pot("pot", (0, -4.6, 3.3), s=1.6, col="#a0a8b4" if not hist else "#8a6a3a")
    return mo


@S(20, 79, 83, "Mom's soup went cold")
def s20(t0, t1):
    mo = soup_scene(t0, t1, "bored")
    pop_text("cold", "COLD", (0, -4.5, 8.0), w(82), 1.2, "#7ad0ff", 0, dur=1.2)
    mover(t0, t1, 1, (0, -4, 4.6), 6.0, pitch=2, lens=30, yaw=10)
    sfx(w(82), "pop", 0.6)


@S(21, 83, 85, "then frozen: ice blocks the pot")
def s21(t0, t1):
    mo = soup_scene(t0, t1, "shock")
    ice = box("ice", (2.6, 2.6, 2.0), (0, -4.6, 4.3), mat("ice", hexc("#9bdcff"), 0.1, alpha=0.5), 0.3)
    pop_in(ice, t0 + 0.1)
    for i in range(6):
        sparkle_on(f"fz{i}", (0, -4.6, 5), t0 + 0.1, 1.6, 6, seed=i, col="#d8f4ff")
    mover(t0, t1, 5, (0, -4.6, 4.2), 10.0, pitch=4, lens=30, yaw=-12)
    sfx(t0 + 0.1, "sparkle", 0.7)
    sfx(t0 + 0.12, "click", 0.6)


@S(22, 85, 87, "then historic: museum, soup in glass case")
def s22(t0, t1):
    kitchen(table=False)
    box("case", (4.4, 4.4, 3.6), (0, -4.6, 5.2), mat("glass", hexc("#cfe9ff"), 0.05, alpha=0.12), 0.1)
    box("plinth", (4.8, 4.8, 3.4), (0, -4.6, 1.7), M("#d8cdb8", 0.6), 0.1)
    pot("pot", (0, -4.6, 3.5), s=1.3, col="#8a6a3a")
    text("plaque", "HISTORIC SOUP", (0, -7.2, 1.8), 0.5, M("#ffffff", 0.5), extrude=0.03)
    mo = mom_c(t0, t1, "sad" if False else "cry")
    at(mo, t0, (3.2, -2, 0), to=(0, -4.6))
    mo.act(t0, "hands_face", expr="cry")
    cam = Cam()
    cam.push(t0, t1, (0, -4.6, 5.0), 11, 6.5, yaw=-18, yaw1=6, pitch=3, lens=28, fstop=3)
    cam.handheld(0.6)
    sfx(t0, "sparkle", 0.6)
    sfx(t0 + 0.15, "rimshot", 0.5)


# ================================================================== festival
@S(23, 87, 92, "Then the town festival started: wide crane over the square")
def s23(t0, t1):
    square()
    cam = Cam()
    cam.key(t0, (-30, -50, 8), (0, 10, 4), lens=22, focus=60, fstop=9)
    cam.key(t1, (30, -48, 22), (0, 8, 6), lens=22, focus=60, fstop=9)
    cam.handheld(0.5)
    sfx(t0, "whoosh", 0.7)
    sfx(w(90), "cheer", 0.6)


@S(24, 92, 97, "500 tables in the square: low angle racking along rows")
def s24(t0, t1):
    square()
    pop_text("n500", "500", (0, -24, 6.0), w(92), 3.0, "#ffe14a", 0, dur=2.0)
    cam = Cam()
    cam.key(t0, (-36, -44, 3.4), (-10, -10, 3.0), lens=22, focus=28, fstop=3.5)
    cam.key(t1, (30, -44, 4.0), (6, -8, 3.0), lens=22, focus=30, fstop=3.5)
    cam.handheld(0.6)
    sfx(w(92), "pop", 0.8)


@S(25, 97, 106, "mayor ready to ring the dinner bell: hero shot")
def s25(t0, t1):
    square()
    mj = story.mayor(t0, t1, "joy")
    at(mj, t0, (0, 6, 0), rot=0)
    mj.act(t0, "cheer", expr="joy")
    lips(mj, t0, t1)
    bell = empty("bell", (5, 6, 7.5))
    cyl("bell_post", 0.2, 7.5, (5, 6, 3.75), M("#4a2e20"), 8)
    sphere("bell_b", 1.4, (0, 0, 0), M("#e2b23a", 0.25, metal=0.9), (1, 1, 1.1), parent=bell, seg=20)
    box("bell_top", (2.4, 0.3, 0.3), (5, 6, 8.5), M("#4a2e20"), 0.02)
    bell.rotation_euler = (0, math.radians(25), 0)
    bell.keyframe_insert("rotation_euler", frame=F(w(100)))
    bell.rotation_euler = (0, math.radians(-25), 0)
    bell.keyframe_insert("rotation_euler", frame=F(w(100) + 0.4))
    cam = Cam()
    cam.key(t0, (-4, -2, 2.6), (0, 6, 5.0), lens=24, focus=9, fstop=3)
    cam.key(w(102), (2, -4, 4.0), (1.5, 6, 5.0), lens=28, focus=10, fstop=3)
    cam.key(t1, (4, 1, 4.4), (4, 6, 6.2), lens=30, focus=6, fstop=3)
    cam.handheld(0.7)
    sfx(w(102), "ding", 0.5)


@S(26, 106, 110, "But under the square: plaza cracks, rumble, camera shakes")
def s26(t0, t1):
    square(tables=False)
    for i in range(5):
        box(f"crack{i}", (0.25, 9 + i * 2, 0.06), (-2 + i * 1.3, 12 + i * 0.5, 0.08), M("#1a1410"), 0, rot=(0, 0, -20 + i * 11))
    cam = Cam()
    cam.key(t0, (0, -26, 2.5), (0, 12, 0.6), lens=22, focus=38, fstop=4)
    cam.key(t1, (0, -12, 1.2), (0, 12, 0.4), lens=20, focus=24, fstop=4)
    cam.shake(0.05, 2)
    cam.handheld(1.5)
    sfx(t0, "rumble", 0.9)


@S(27, 110, 114, "lived the Table Eater: monster silhouette rises in the ground")
def s27(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 12, 0), 0.9)
    mon_rise(root, t0, t1, -20, -4)
    cam = Cam()
    cam.key(t0, (-8, -16, 1.0), (0, 12, 6), lens=24, focus=28, fstop=3)
    cam.key(t1, (6, -12, 3.0), (0, 12, 9), lens=24, focus=24, fstop=3)
    cam.shake(0.04, 2)
    pop_text("te", "THE TABLE EATER", (0, -6, 12), w(112), 1.4, "#ff5a3c", 0, dur=1.8)
    sfx(t0, "rumble", 0.8)
    sfx(w(112), "boom", 0.6)


@S(28, 114, 123, "giant monster with a napkin around his neck: comedic close-up")
def s28(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 10, 0), 1.0, mood="happy")
    jaw_chomp(jaw, t0 + 0.5, t1, 2.0, -18)
    cam = Cam()
    cam.key(t0, (-12, -22, 12), (0, 10, 13), lens=30, focus=26, fstop=4)
    cam.key(w(119), (10, -22, 12), (0, 10, 12), lens=32, focus=26, fstop=4)
    cam.key(t1, (0, -18, 10), (0, 10, 11), lens=36, focus=20, fstop=4)
    cam.handheld(0.7)
    sfx(t0, "pop", 0.8)
    sfx(w(119), "rimshot", 0.5)


@S(29, 123, 128, "When a table gets served: server sets a table, plate lands")
def s29(t0, t1):
    square()
    for i in range(3):
        plate(f"serve{i}", (-3 + i * 3, -10 + i, 2.7))
    pk = story.townie(3, t0, t1, "happy")
    at(pk, t0, (-6, -12, 0), to=(0, -10))
    pk.act(t0, "reach", expr="happy")
    cam = Cam()
    cam.key(t0, (-4, -16, 4.0), (0, -10, 2.8), lens=30, focus=10, fstop=3)
    cam.key(t1, (2, -13, 3.4), (0, -10, 2.8), lens=34, focus=7, fstop=3)
    cam.handheld(0.8)
    sfx(w(125), "place", 0.8)


@S(30, 128, 134, "he wakes up and eats everything: monster bursts out huge")
def s30(t0, t1):
    square()
    root, jaw = monster("Eater", (0, 6, 0), 1.0)
    mon_rise(root, t0, w(130), -22, 0)
    jaw_chomp(jaw, w(130), t1, 4.0, -35)
    cam = Cam()
    cam.key(t0, (0, -30, 2.0), (0, 6, 8), lens=22, focus=36, fstop=4)
    cam.key(t1, (0, -22, 7), (0, 6, 12), lens=22, focus=28, fstop=4)
    cam.crash(w(130), 22, 14, 0.15)
    cam.shake(0.05, 2)
    cam.handheld(1.2)
    sfx(w(129), "roar" if False else "zombie", 0.8)
    sfx(w(130), "boom", 0.9)


@S(31, 134, 135, "Plates (eaten)")
def s31(t0, t1):
    kitchen()
    for i in range(6):
        plate(f"p{i}", (-4 + i * 1.6, -4, 2.8), s=1.3)
    root, jaw = monster("Eater", (0, 8, 0), 0.5)
    jaw_chomp(jaw, t0, t1, 6, -35)
    cam = Cam()
    cam.key(t0, (-6, -10, 4), (0, -4, 3), lens=28, focus=10, fstop=3)
    cam.key(t1, (4, -8, 4), (0, -4, 3), lens=28, focus=8, fstop=3)
    sfx(t0, "stomp", 0.6)


@S(32, 135, 136, "chairs (flying)")
def s32(t0, t1):
    square()
    for i in range(5):
        c = box(f"chair{i}", (1.4, 1.4, 2.2), (-6 + i * 3, -10, 1.1), M("#a0703f", 0.7), 0.1)
        c.location = (-6 + i * 3, -10, 1.1)
        c.keyframe_insert("location", frame=F(t0))
        c.location = (i * 0.6 - 1.2, 4, 12)
        c.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.key(t0, (0, -20, 3), (0, 0, 5), lens=26, focus=20, fstop=4)
    cam.key(t1, (0, -16, 3), (0, 2, 8), lens=26, focus=20, fstop=4)
    sfx(t0, "whoosh", 0.7)


@S(33, 136, 137, "people (scream, eaten)")
def s33(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 6, 0), 1.0)
    jaw.rotation_euler = (math.radians(-35), 0, 0)
    jaw.keyframe_insert("rotation_euler", frame=F(t0))
    for i in range(4):
        k = story.townie(i + 2, t0, t1, "panic")
        k.pose(t0, loc=(-6 + i * 4, -14, 0), rot=0)
        k.act(t0, "hands_head", expr="panic")
    cam = Cam()
    cam.key(t0, (0, -26, 3), (0, 0, 6), lens=22, focus=26, fstop=5)
    cam.key(t1, (0, -22, 4), (0, 2, 9), lens=22, focus=24, fstop=5)
    cam.crash(t0, 22, 30, 0.1)
    sfx(t0, "gasp", 0.8)


@S(34, 137, 140, "The bell rang: huge bell swings, shockwave")
def s34(t0, t1):
    square()
    mj = story.mayor(t0, t1, "joy")
    at(mj, t0, (0, 0, 0), rot=0)
    mj.act(t0, "cheer", expr="shout")
    bell = empty("bell", (0, 6, 9))
    sphere("bell_b", 2.2, (0, 0, 0), M("#e2b23a", 0.25, metal=0.9), (1, 1, 1.1), parent=bell, seg=20)
    box("bell_top", (4, 0.3, 0.3), (0, 6, 11), M("#4a2e20"), 0.02)
    for k in range(5):
        bell.rotation_euler = (0, math.radians(30 if k % 2 == 0 else -30), 0)
        bell.keyframe_insert("rotation_euler", frame=F(t0 + k * 0.25))
    ding(w(138), (4, -2, 9.5), 1.4, dur=1.0)
    cam = Cam()
    cam.key(t0, (-6, -10, 3.0), (0, 6, 9), lens=26, focus=16, fstop=3)
    cam.key(t1, (8, -6, 5), (0, 6, 9), lens=34, focus=14, fstop=3)
    cam.crash(w(138), 26, 40, 0.1)
    cam.handheld(1.0)
    sfx(w(138), "bell" if False else "ding", 0.9)


@S(35, 140, 143, "The ground shook: tables jitter, camera quake")
def s35(t0, t1):
    square()
    cam = Cam()
    cam.key(t0, (0, -48, 5.0), (0, -8, 3.0), lens=24, focus=40, fstop=5)
    cam.key(t1, (0, -42, 5.0), (0, -8, 3.0), lens=24, focus=34, fstop=5)
    cam.shake(0.08, 1.5)
    cam.handheld(2.0)
    sfx(t0, "rumble", 1.0)
    sfx(w(142), "stomp", 0.8)


@S(36, 143, 146, "He was coming: monster POV stomps toward camera")
def s36(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 20, 0), 1.0)
    root.location = (0, 24, 0)
    root.keyframe_insert("location", frame=F(t0))
    root.location = (0, -2, 0)
    root.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.key(t0, (0, -32, 1.4), (0, 8, 8), lens=20, focus=36, fstop=5)
    cam.key(t1, (0, -26, 1.2), (0, 8, 9), lens=20, focus=24, fstop=5)
    cam.shake(0.06, 2)
    cam.handheld(1.4)
    sfx(t0, "stomp", 1.0)
    sfx(t0 + 0.6, "stomp", 1.0)
    sfx(t0 + 1.2, "stomp", 1.0)


@S(37, 146, 150, "Then I noticed something: narrator close, eyes narrow")
def s37(t0, t1):
    kitchen(table=False)
    me = hero(t0, t1, "sus")
    p = (0, -2, 0)
    at(me, t0, p, rot=0)
    me.act(t0, "think", expr="sus")
    me.face(w(149), "smug")
    lips(me, t0, t1)
    cam = Cam()
    cam.push(t0, t1, head(p), 6.5, 2.6, yaw=0, yaw1=-6, pitch=-2, lens=36, fstop=1.8)
    cam.crash(w(149), 36, 48, 0.15)
    cam.handheld(0.5)
    sfx(t0, "rise", 0.5)
    sfx(w(149), "movie_1" if False else "ding", 0.5)


@S(38, 150, 155, "He can only eat a table: monster stares at a table")
def s38(t0, t1):
    square()
    root, jaw = monster("Eater", (0, 8, 0), 0.8)
    box("tab", (4.6, 2.6, 0.25), (0, -4, 2.4), M("#a0703f", 0.7), 0.04)
    plate("tp", (0, -4, 2.7))
    cam = Cam()
    cam.push(t0, t1, (0, -2, 6), 22, 14, yaw=-12, yaw1=10, pitch=6, lens=26, fstop=5)
    cam.handheld(0.8)
    sfx(t0, "stomp", 0.5)


@S(39, 155, 159, "that's been served: plate on table glows, empty table does nothing")
def s39(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 10, 0), 0.8)
    for i, x in enumerate((-8, 0, 8)):
        box(f"tb{i}", (4.6, 2.6, 0.25), (x, -6, 2.4), M("#a0703f", 0.7), 0.04)
        if i == 1:
            plate("pp", (x, -6, 2.7))
            light("glow", "POINT", (x, -6, 4.5), 500, (1, 0.9, 0.5), 1.0)
    cam = Cam()
    cam.key(t0, (-6, -22, 3.0), (-8, -6, 2.8), lens=30, focus=16, fstop=3)
    cam.key(t1, (4, -20, 3.0), (6, -6, 2.8), lens=30, focus=16, fstop=3)
    cam.handheld(0.8)
    sfx(w(157), "ding", 0.6)


@S(40, 159, 163, "I grabbed the microphone: narrator, determined hero shot, low angle")
def s40(t0, t1):
    square()
    me = hero(t0, t1, "determined")
    at(me, t0, (0, -12, 0), rot=0)
    me.act(t0, "reach", expr="determined")
    m_ = mic("mic", (0.9, 0.2, 2.4), parent=me.hip)
    cam = Cam()
    cam.key(t0, orbit_pos(head((0, -12, 0)), 5, -25, -8), head((0, -12, 0)), lens=26, focus=5, fstop=2.6)
    cam.key(t1, orbit_pos(head((0, -12, 0)), 3.2, 10, -4), head((0, -12, 0)), lens=32, focus=3.2, fstop=2.6)
    cam.handheld(1.0)
    sfx(t0, "click", 0.8)
    sfx(w(161), "whoosh", 0.6)


@S(41, 163, 166, "What's for dinner? narrator booming into the mic")
def s41(t0, t1):
    square()
    me = hero(t0, t1, "shout")
    at(me, t0, (0, -12, 0), rot=0)
    me.act(t0, "point", expr="shout")
    lips(me, t0, t1, "shout")
    mic("mic", (0.9, 0.2, 2.4), parent=me.hip)
    cam = Cam()
    cam.key(t0, orbit_pos(head((0, -12, 0)), 7, 14, 2), head((0, -12, 0)), lens=26, focus=7, fstop=2.4)
    cam.key(t1, orbit_pos(head((0, -12, 0)), 2.6, 2, 0), head((0, -12, 0)), lens=38, focus=2.6, fstop=2.4, ease="EASE_IN")
    cam.crash(t0 + 0.6, 38, 54, 0.1)
    cam.handheld(1.0)


@S(42, 166, 167, "DING: monster flinches")
def s42(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 10, 0), 0.9)
    root.rotation_euler = (math.radians(-8), 0, 0)
    root.keyframe_insert("rotation_euler", frame=F(t0))
    ding(t0, (0, -4, 10), 2.4, dur=1.0)
    cam = Cam()
    cam.key(t0, (0, -24, 6), (0, 10, 10), lens=24, focus=30, fstop=4)
    cam.key(t1, (0, -20, 6), (0, 10, 10), lens=24, focus=26, fstop=4)
    cam.crash(t0, 22, 34, 0.1)
    cam.shake(0.03, 3)


@S(43, 167, 171, "500 people joined in: crowd rushes the stage")
def s43(t0, t1):
    square(tables=False)
    src = crowd_src("CR1", t0, t1, [1, 2, 3, 4, 5, 6], mode="cheer", spread=1.5)
    crowd(src, t0, t1, 30, ((-22, 22), (-26, -6)), z0=(0, 0), z1=(0, 0.2), delay=(0, 0.3), seed=11)
    cam = Cam()
    cam.key(t0, (-14, -34, 10), (0, -12, 3), lens=24, focus=24, fstop=5)
    cam.key(t1, (12, -36, 6), (0, -12, 4), lens=24, focus=24, fstop=5)
    cam.handheld(1.0)
    pop_text("n500b", "500", (0, -22, 12), w(167), 3.0, "#ffe14a", 0, dur=2.0)
    sfx(t0, "crowd", 0.9)
    sfx(w(167), "cheer", 0.8)


@S(44, 171, 174, "What's for dinner? (everyone) crowd yelling")
def s44(t0, t1):
    square(tables=False)
    src = crowd_src("CR2", t0, t1, [7, 8, 9, 10], mode="cheer", spread=1.2)
    crowd(src, t0, t1, 24, ((-18, 18), (-26, -8)), z0=(0, 0.3), z1=(0.2, 0.9), delay=(0, 0.2), seed=5)
    me = hero(t0, t1, "shout")
    at(me, t0, (0, -12, 0), rot=0)
    me.act(t0, "cheer", expr="shout")
    lips(me, t0, t1, "shout")
    cam = Cam()
    cam.key(t0, (4, -22, 3), (0, -12, 5), lens=22, focus=12, fstop=4)
    cam.key(t1, (-6, -18, 5), (0, -12, 5.4), lens=26, focus=10, fstop=4)
    cam.handheld(1.2)
    sfx(t0, "chat", 0.5)


@S(45, 174, 175, "DING 1")
def s45(t0, t1):
    square(tables=False)
    ding(t0, (-6, -10, 9), 1.8, dur=0.7)
    cam = Cam()
    cam.key(t0, (-12, -20, 5), (-6, -10, 7), lens=26, focus=16, fstop=4)
    cam.key(t1, (-10, -18, 5), (-6, -10, 7), lens=26, focus=14, fstop=4)
    cam.crash(t0, 24, 36, 0.1)
    cam.shake(0.03, 3)


@S(46, 175, 176, "DING 2")
def s46(t0, t1):
    square(tables=False)
    ding(t0, (6, -10, 9), 1.8, dur=0.7)
    cam = Cam()
    cam.key(t0, (12, -20, 5), (6, -10, 7), lens=26, focus=16, fstop=4)
    cam.key(t1, (10, -18, 5), (6, -10, 7), lens=26, focus=14, fstop=4)
    cam.crash(t0, 24, 36, 0.1)
    cam.shake(0.03, 3)


@S(47, 176, 177, "DING 3")
def s47(t0, t1):
    square(tables=False)
    ding(t0, (0, -6, 10), 2.4, dur=0.9)
    cam = Cam()
    cam.key(t0, (0, -22, 4), (0, -6, 8), lens=22, focus=16, fstop=4)
    cam.key(t1, (0, -16, 4), (0, -6, 8), lens=22, focus=10, fstop=4)
    cam.crash(t0, 20, 34, 0.1)
    cam.shake(0.04, 3)


@S(48, 177, 183, "pushed back 500 hours: giant clock spins crazy fast")
def s48(t0, t1):
    kitchen(table=False)
    c = collection("CLK3")
    clock("big", (0, 3.0, 6.0), t0, t1, turns=40, r=4.6, coll=c)
    pop_text("h500", "+500 HOURS", (0, 1.5, 12.5), w(181), 1.7, "#ff5a3c", 0, dur=2.5)
    cam = Cam()
    cam.push(t0, t1, (0, 3, 6.4), 16, 9, yaw=0, yaw1=10, pitch=0, lens=30, fstop=5, roll=0.05)
    cam.crash(w(181), 30, 44, 0.12)
    cam.handheld(0.8)
    sfx(t0, "rise", 0.9)
    sfx(w(181), "boom", 0.6)


@S(49, 183, 192, "monster stares at the empty tables: drool")
def s49(t0, t1):
    square(tables=False)
    for r in range(3):
        for k in range(5):
            box(f"et{r}{k}", (4.6, 2.6, 0.25), (-12 + k * 6, -10 - r * 6, 2.4), M("#a0703f", 0.7), 0.04)
    root, jaw = monster("Eater", (0, 12, 0), 1.0, mood="happy")
    jaw.rotation_euler = (math.radians(-12), 0, 0)
    jaw.keyframe_insert("rotation_euler", frame=F(t0))
    cam = Cam()
    cam.key(t0, (-10, -26, 4), (0, 8, 10), lens=28, focus=36, fstop=4)
    cam.key(w(188), (6, -22, 6), (0, 8, 12), lens=30, focus=30, fstop=4)
    cam.key(t1, (0, -18, 8), (0, 8, 13), lens=36, focus=26, fstop=4)
    cam.handheld(0.6)
    sfx(t0, "crickets", 0.7)


@S(50, 192, 198, "so hungry he cried: monster tears")
def s50(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 14, 0), 0.9, mood="happy")
    jaw.rotation_euler = (math.radians(-22), 0, 0)
    jaw.keyframe_insert("rotation_euler", frame=F(t0))
    for sx in (-1, 1):
        for k in range(8):
            tt = t0 + 0.3 + k * 0.35
            tr = sphere(f"tear{sx}{k}", 0.6, (sx * 2.0, 8.0, 14.5), M("#7ad0ff", 0.1), (1, 1, 1.5))
            tr.scale = (0.01,) * 3
            tr.keyframe_insert("scale", frame=F(tt - 0.02))
            tr.scale = (1, 1, 1)
            tr.keyframe_insert("scale", frame=F(tt))
            tr.location = (sx * 2.2, 8.0, 14.5)
            tr.keyframe_insert("location", frame=F(tt))
            tr.location = (sx * 2.4, 8.0, 6.0)
            tr.keyframe_insert("location", frame=F(tt + 0.5))
    cam = Cam()
    cam.push(t0, t1, (0, 8, 14), 24, 12, yaw=0, yaw1=-8, pitch=0, lens=32, fstop=4)
    cam.handheld(0.7)
    sfx(w(196), "faaah", 0.6)
    sfx(w(195), "aww", 0.6)


@S(51, 198, 206, "fell asleep on the town hall: zzz, camera slow drift")
def s51(t0, t1):
    square(tables=False)
    root, jaw = monster("Eater", (0, 14, 0), 1.0, mood="happy")
    root.rotation_euler = (math.radians(-70), 0, 0)
    root.location = (0, 22, 8)
    root.keyframe_insert("rotation_euler", frame=F(t0))
    root.keyframe_insert("location", frame=F(t0))
    for i in range(3):
        pop_text(f"zz{i}", "Z", (6 + i * 2.4, 0, 18 + i * 3), t0 + 0.4 + i * 0.5, 2.2 - i * 0.4, "#9ec8ff", 0, dur=2.4)
    cam = Cam()
    cam.key(t0, (-20, -34, 8), (0, 22, 10), lens=24, focus=56, fstop=6)
    cam.key(t1, (20, -34, 12), (0, 22, 10), lens=24, focus=56, fstop=6)
    cam.handheld(0.4)
    sfx(t0, "snort", 0.7)
    sfx(w(203), "snort", 0.6)


@S(52, 206, 213, "Three weeks later the clocks hit zero: clock hands spin and stop")
def s52(t0, t1):
    square(tables=False, hall_clock=False)
    clock("hallclk", (0, 24, 11), t0 + 0.3, t1 - 0.3, turns=6, r=6.0)
    pop_text("3w", "3 WEEKS LATER", (0, -6, 6), t0 + 0.1, 1.6, "#ffffff", 0, dur=1.8)
    cam = Cam()
    cam.push(t0, t1, (0, 24, 11), 36, 16, yaw=-8, yaw1=6, pitch=-4, lens=28, fstop=5)
    cam.handheld(0.6)
    sfx(t0, "click", 0.8)
    sfx(w(212), "ding", 0.9)


@S(53, 213, 219, "We served spaghetti for 3,000 people: pans along a huge feast")
def s53(t0, t1):
    square()
    src = crowd_src("CR3", t0, t1, [11, 12, 13, 14], mode="cheer", spread=1.2)
    crowd(src, t0, t1, 18, ((-22, 22), (-30, -14)), z0=(0, 0.2), z1=(0, 0.4), delay=(0, 0.3), seed=8)
    for i in range(7):
        sphere(f"sp{i}", 0.7, (-12 + i * 4, -22, 2.9), M("#f0c05a", 0.7), (1.3, 1, 0.6))
    pop_text("3k", "3,000", (0, -26, 8), w(217), 2.6, "#ffe14a", 0, dur=1.8)
    cam = Cam()
    cam.key(t0, (-30, -50, 5), (-10, -18, 3), lens=24, focus=40, fstop=5)
    cam.key(t1, (30, -48, 8), (10, -18, 3), lens=24, focus=40, fstop=5)
    cam.handheld(0.8)
    sfx(w(217), "cheer", 0.7)
    sfx(w(216), "whoosh", 0.5)


@S(54, 219, 222, "Very, very quietly: finger on lips, everyone tiptoes, quiet")
def s54(t0, t1):
    square(tables=True)
    for i in range(5):
        k = story.townie(i + 3, t0, t1, "smile")
        k.pose(t0, loc=(-8 + i * 4, -8 - (i % 2) * 2, 0), rot=0)
        k.act(t0, "think", expr="sus")
    root, jaw = monster("Eater", (0, 30, 0), 0.6)
    pop_text("shh", "SHHH", (0, -12, 8), w(219), 1.6, "#ffffff", 0, dur=2.0)
    cam = Cam()
    cam.push(t0, t1, (0, -9, 4), 18, 10, yaw=0, yaw1=-12, pitch=2, lens=26, fstop=4)
    cam.handheld(0.4)
    sfx(t0, "crickets", 0.6)


@S(55, 222, 230, "best meal of my life: narrator eats spaghetti, tears of joy")
def s55(t0, t1):
    kitchen()
    me = hero(t0, t1, "joy")
    at(me, t0, (-4.6, -5.0, 0), rot=90)
    me.act(t0, "cheer", expr="joy")
    lips(me, t0, t1, "laugh")
    plate("spag", (-2.0, -5.0, 2.95), s=1.5, food="#f0c05a")
    confetti("cf2", (-3, -5, 8), (3, 2, 2), w(226), dur=1.5, n=50, seed=9)
    cam = Cam()
    cam.key(t0, (-10.0, -12.0, 6.0), (-4.6, -5, 5.2), lens=32, focus=9, fstop=2.4)
    cam.key(t1, (-11.0, -8.0, 6.4), (-4.6, -5, 5.2), lens=36, focus=8, fstop=2.4)
    cam.handheld(0.8)
    sfx(w(226), "sparkle", 0.8)
    sfx(w(225), "aww", 0.7)


@S(56, 230, 236, "Mom looks at the empty pot")
def s56(t0, t1):
    mo = soup_scene(t0, t1, "bored")
    mo.act(t0, "lean", expr="sus")
    lips(mo, t0, t1)
    cam = Cam()
    cam.push(t0, t1, (0, -3.0, 4.4), 14, 9, yaw=50, yaw1=38, pitch=14, lens=30, fstop=3.0)
    cam.handheld(0.5)
    sfx(w(233), "crickets", 0.5)


@S(57, 236, 241, "Honey, what's for dinner tomorrow? Mom to camera, big")
def s57(t0, t1):
    kitchen(table=False)
    mo = mom_c(t0, t1, "talk")
    p = (0, -2, 0)
    at(mo, t0, p, rot=0)
    mo.act(t0, "shrug", expr="talk")
    lips(mo, t0, t1)
    cam = Cam()
    cam.push(t0, t1, head(p), 6.0, 2.8, yaw=0, yaw1=-8, pitch=-2, lens=34, fstop=1.8)
    cam.crash(w(239), 34, 46, 0.15)
    cam.handheld(0.7)
    sfx(w(240), "gasp", 0.6)


@S(58, 241, 242, "DING! (callback)")
def s58(t0, t1):
    kitchen(table=False)
    c = collection("CLK4")
    clock("big", (0, 3.0, 5.0), t0, t1, turns=1 / 12, r=3.4, coll=c)
    ding(t0, (0, 1.8, 9.4), 2.2)
    cam = Cam()
    cam.key(t0, (0, -8, 5.6), (0, 3, 5.4), lens=28, focus=10, fstop=4)
    cam.key(t1, (0, -6, 5.6), (0, 3, 5.4), lens=28, focus=8, fstop=4)
    cam.crash(t0, 26, 42, 0.1)
    cam.shake(0.04, 3)


@S(59, 242, None, "One more hour: family groans, button on final hit")
def s59(t0, t1):
    kitchen()
    fm = family(t0, t1, "cry", hungry=True)
    for k in fm.values():
        k.face(t0, "cry")
    pop_text("omh", "+1 HOUR", (0, -6, 8), w(243), 1.8, "#ff5a3c", 0, dur=None)
    cam = Cam()
    cam.key(t0, (0, -12, 4.5), (0, -2, 4), lens=26, focus=12, fstop=4)
    cam.key(t1, (0, -9, 4.5), (0, -2, 4), lens=26, focus=9, fstop=4)
    cam.crash(w(243), 26, 38, 0.15)
    cam.handheld(0.6)
    sfx(w(243), "faaah", 0.7)
    sfx(w(244) + 0.2, "rimshot", 0.7)
