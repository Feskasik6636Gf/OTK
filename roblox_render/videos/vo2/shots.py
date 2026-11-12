"""vo2 / ask your mom: "Every time a dad says 'Ask your mom,' he shrinks one inch."
A two-inch dad rescues the baby sister from a hot locked car. Shots keyed to script word indices."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from rbx.sets import wood, planks

V = Video(__file__)
story.bind(V)

S2 = 0.2          # "two inches" dad
SP = 0.07         # peanut dad
SBIG = 1.25       # six foot three
CTOP = 3.2        # kitchen counter top
DAD_K = (1.0, 5.4, CTOP)
BOX_K = (3.6, 6.2, CTOP)
KID_K = (-2.6, 2.6, 0.0)
CAR = (0.0, 2.0, 0.0)
HINGE = (-4.1, -1.75, 0.0)        # driver door hinge (front edge)
GAP_Z = 5.45                       # top of the lowered window glass
HANDLE = (-1.0, -1.9, 3.25)       # outside door handle (world, door closed)
BUTTON = (-1.4, -1.35, 3.45)      # unlock button on the inner armrest (world, door closed)
KEYS = (-1.2, 1.4, 3.2)           # keys on the driver seat
SEAT = (-1.6, 0.4, 3.1)           # driver seat top
KID_D = (-6.5, -6.5, 0.0)
MUG = (-4.6, 5.8, CTOP)
TABLE_Z = 2.8
DOOR_X = 14.0                      # kitchen doorway (wall at y=-3)


def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def emitm(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


# ================================================================== cast
def kid_c(t0, t1, expr="neutral"):
    K = chars.Char("Kid", skin="#e8c39e", shirt="#ff8a3d", pants="#2f3f6a", hair="spiky", hair_color="#5a3a22",
                   face="kid", vneck="#ffc08a")
    return story._live(K, t0, t1, expr)


def dad_c(t0, t1, expr="neutral", s=S2, cape=False):
    D_ = chars.Char("Dad", skin="#e9c7a6", shirt="#3f7fd9", pants="#c8b48a", hair="short", hair_color="#3a2a1e",
                    face="mustache", vneck="#f4f4f4", scale=s)
    story._live(D_, t0, t1, expr, 0.6)
    for piv in (D_.hpL, D_.hpR):          # shiny new white sneakers
        box(D_.name + piv.name + "_shoe", (1.1, 1.55, 0.5), (0, -0.25, -1.8), M("#ffffff", 0.3), 0.16, parent=piv, coll=D_.coll)
        box(D_.name + piv.name + "_sw", (1.14, 0.3, 0.2), (0, 0.05, -1.62), M("#e8423a", 0.4), 0.04, parent=piv, coll=D_.coll)
    if cape:
        cp = box("Dad_cape", (2.0, 0.12, 2.8), (0, 0.62, -0.3), M("#e8423a", 0.5), 0.05, parent=D_.torso, coll=D_.coll,
                 rot=(-12, 0, 0))
        noise(cp, "rotation_euler", 0, 0.25, 6)
    return D_


def mom_c(t0, t1, expr="neutral", necklace=False, s_dad=S2, dad_expr="happy"):
    Mo = chars.Char("Mom", skin="#f1dfc6", shirt="#e8423a", pants="#2b2b3a", hair="bob", hair_color="#7a3a1e",
                    face="girl", sleeves="long", vneck="#f6c0a8")
    story._live(Mo, t0, t1, expr)
    d = None
    if necklace:
        Mc = M("#e2b23a", 0.25, metal=0.9)
        for i in range(9):
            a = math.radians(-60 + i * 15)
            sphere(f"neck{i}", 0.06, (math.sin(a) * 0.75, -0.52, 0.95 - math.cos(a) * 0.75), Mc, parent=Mo.torso,
                   coll=Mo.coll, seg=8)
        cyl("neck_ring", 0.16, 0.05, (0, -0.56, 0.18), Mc, 16, rot=(90, 0, 0), parent=Mo.torso, coll=Mo.coll)
        d = dad_c(t0, t1, dad_expr, s_dad)
        d.root.parent = Mo.torso
        d.root.location = (0, -0.7, 0.12 - 4.9 * s_dad)
        d.pose(t0, armL=(170, 12), armR=(170, 12))
        noise(d.root, "rotation_euler", 1, 0.3, 10)
    return Mo, d


def sis_c(t0, t1, expr="happy"):
    Si = chars.Char("Sis", skin="#f1dfc6", shirt="#f09ac2", pants="#f6c0d8", hair="bun", hair_color="#c87a3a",
                    face="girl", scale=0.62)
    return story._live(Si, t0, t1, expr)


ADULTS = [("#3f7fd9", "#c8b48a", "short", "#3a2a1e"), ("#63c06a", "#2b2b3a", "slick", "#151212"),
          ("#9b6ad6", "#55565e", "buzz", "#2a1d16"), ("#e8b520", "#3b3f4a", "short", "#6b3a1e"),
          ("#e8423a", "#2b2b2b", "slick", "#5a3a22"), ("#4fb3b8", "#3d5fb8", "buzz", "#1d1714")]
SKINS = ["#e9c7a6", "#c9926a", "#f1dfc6", "#a8714a", "#d9b48f", "#ecd2b8"]


def adult(i, t0, t1, expr="neutral", s=1.0):
    sh, pa, hr, hc = ADULTS[i % len(ADULTS)]
    A = chars.Char(f"Ad{i}", skin=SKINS[i % len(SKINS)], shirt=sh, pants=pa, hair=hr, hair_color=hc,
                   face="mustache" if i % 2 == 0 else "hero", scale=s)
    return story._live(A, t0, t1, expr, 0.6)


def head(p, s=1.0):
    return (p[0], p[1], p[2] + 4.6 * s)


def sit_on(ch, t, seat_top, rot=0, s=1.0, **kw):
    x, y, z = seat_top
    ch.pose(t, loc=(x, y, z - 1.96 * s), rot=rot, legL=(85, 3), legR=(85, -3), armL=(30, 6), armR=(30, 6), **kw)


# ================================================================== fx
def resize(ch, t, s0, s1, dur=0.32, snd=True, sparkle=True, loc=None):
    r = ch.root
    r.scale = (s0,) * 3
    r.keyframe_insert("scale", frame=F(t))
    over = s1 + (s1 - s0) * 0.22
    r.scale = (over,) * 3
    r.keyframe_insert("scale", frame=F(t + dur * 0.7))
    r.scale = (s1,) * 3
    r.keyframe_insert("scale", frame=F(t + dur))
    p = Vector(loc) if loc else Vector(r.location)
    if sparkle:
        sparkle_on(f"rs{ch.name}{F(t)}", tuple(p + Vector((0, 0, 2.4 * max(s0, s1)))), t, 2.2 * max(s0, s1), 10, seed=F(t))
    if snd:
        sfx(t, "shrink" if s1 < s0 else "grow", 0.9)


def sparkle_on(name, loc, t, s=1.0, n=10, seed=0, col="#fff1a0"):
    rnd = random.Random(seed)
    Ms = mat("sp_" + col, hexc(col), 0.3, emit=hexc(col), estr=10)
    for i in range(n):
        p = Vector(loc) + Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.5, 1))) * s
        o = sphere(f"{name}{i}", 0.09 * s, tuple(p), Ms, seg=8)
        ts = t + rnd.uniform(0, 0.5)
        o.scale = (0.01,) * 3; o.keyframe_insert("scale", frame=F(ts - 0.05))
        o.scale = (1.6, 1.6, 1.6); o.keyframe_insert("scale", frame=F(ts + 0.08))
        o.scale = (0.01,) * 3; o.keyframe_insert("scale", frame=F(ts + 0.3))


def pop_text(name, body, loc, t, size=1.0, col="#ffe14a", yaw=0, dur=None, outline="#1a1a22"):
    root = empty(name, loc, rot=(0, 0, yaw))
    text(name + "_t", body, (0, 0, 0), size, emitm(col, 2.5), extrude=0.08 * size, parent=root)
    text(name + "_o", body, (0.04 * size, 0.06 * size, -0.04 * size), size, M(outline, 0.6), extrude=0.06 * size, parent=root)
    root.scale = (0.01,) * 3; root.keyframe_insert("scale", frame=F(t - 0.04))
    root.scale = (1.25,) * 3; root.keyframe_insert("scale", frame=F(t + 0.08))
    root.scale = (1.0,) * 3; root.keyframe_insert("scale", frame=F(t + 0.16))
    if dur:
        root.keyframe_insert("scale", frame=F(t + dur - 0.1))
        root.scale = (0.01,) * 3; root.keyframe_insert("scale", frame=F(t + dur))
    noise(root, "rotation_euler", 1, 0.04, 8)
    return root


def ask_mom(ch, t0, t1, s0=None, s1=None, ts=None, loc=None):
    """Dad shrugs, says it, and shrinks on 'mom'."""
    ch.act(t0, "shrug", expr="smile")
    lips(ch, t0, t1)
    if s0 is not None:
        resize(ch, ts if ts is not None else t1 - 0.25, s0, s1, loc=loc)
        ch.face((ts if ts is not None else t1 - 0.25) + 0.3, "shock")


def heat(name, center, size, n=14, seed=0):
    rnd = random.Random(seed)
    Mh = mat("heatw", hexc("#fff3c0"), 0.2, emit=hexc("#fff3c0"), estr=0.6, alpha=0.18)
    for i in range(n):
        p = Vector(center) + Vector((rnd.uniform(-1, 1) * size[0], rnd.uniform(-1, 1) * size[1], rnd.uniform(0, size[2])))
        o = sphere(f"{name}{i}", rnd.uniform(0.6, 1.4), tuple(p), Mh, (1, 1, 0.25), seg=10)
        noise(o, "location", 2, 0.6, 12)
        noise(o, "location", 0, 0.4, 16)


# ================================================================== props
def shoebox(loc, coll=None, dad_bed=True):
    root = empty("sbox", loc, coll=coll)
    Mb = M("#d9a86a", 0.7)
    box("sb_bot", (2.4, 1.6, 0.08), (0, 0, 0.04), Mb, 0.01, parent=root, coll=coll)
    for sx in (-1, 1):
        box(f"sb_s{sx}", (0.08, 1.6, 0.9), (sx * 1.2, 0, 0.45), Mb, 0.01, parent=root, coll=coll)
    for sy in (-1, 1):
        box(f"sb_e{sy}", (2.4, 0.08, 0.9), (0, sy * 0.8, 0.45), Mb, 0.01, parent=root, coll=coll)
    box("sb_lid", (2.5, 1.7, 0.1), (0, 1.2, 0.6), M("#c8955f", 0.7), 0.01, parent=root, coll=coll, rot=(70, 0, 0))
    text("sb_txt", "DAD", (0, -0.86, 0.45), 0.36, M("#2a2a3a", 0.6), extrude=0.01, parent=root, coll=coll)
    if dad_bed:
        box("sb_bed", (1.4, 0.9, 0.18), (-0.3, 0.1, 0.17), M("#3f7fd9", 0.8), 0.06, parent=root, coll=coll)
        box("sb_pil", (0.4, 0.6, 0.12), (-0.82, 0.1, 0.3), M("#ffffff", 0.8), 0.05, parent=root, coll=coll)
        cyl("sb_lamp", 0.07, 0.4, (0.8, 0.4, 0.28), M("#e2b23a", 0.3, metal=0.8), 10, parent=root, coll=coll)
        sphere("sb_bulb", 0.11, (0.8, 0.4, 0.52), emitm("#ffd890", 4), parent=root, coll=coll, seg=10)
    return root


def mug_big(loc, coll=None, col="#e8423a"):
    root = empty("mugb", loc, coll=coll)
    cyl("mug_b", 0.75, 1.7, (0, 0, 0.85), M(col, 0.3), 24, parent=root, coll=coll)
    cyl("mug_c", 0.66, 0.05, (0, 0, 1.68), M("#4a2a16", 0.2), 24, parent=root, coll=coll)
    box("mug_h", (0.2, 0.25, 1.0), (0.85, 0, 0.9), M(col, 0.3), 0.1, parent=root, coll=coll)
    text("mug_t", "#1 DAD", (0, -0.78, 0.9), 0.3, M("#ffffff", 0.5), extrude=0.01, parent=root, coll=coll)
    return root


def phone_prop(name, loc, rot=(0, 0, 0), coll=None, s=1.0):
    root = empty(name, loc, coll=coll, rot=rot)
    root.scale = (s,) * 3
    box(name + "_b", (1.2, 0.12, 2.2), (0, 0, 0), M("#18181c", 0.2), 0.08, parent=root, coll=coll)
    box(name + "_s", (1.05, 0.02, 2.0), (0, -0.07, 0), emitm("#2a3a5a", 1.2), 0.02, parent=root, coll=coll)
    text(name + "_t1", "FAMILY", (0, -0.1, 0.55), 0.2, emitm("#ffffff", 2), extrude=0.005, parent=root, coll=coll)
    text(name + "_t2", "CHAT", (0, -0.1, 0.3), 0.2, emitm("#ffffff", 2), extrude=0.005, parent=root, coll=coll)
    sphere(name + "_bd", 0.28, (0.48, -0.12, 0.98), emitm("#ff3a3a", 2), (1, 0.4, 1), parent=root, coll=coll, seg=12)
    text(name + "_n", "99+", (0.48, -0.25, 0.92), 0.16, emitm("#ffffff", 3), extrude=0.005, parent=root, coll=coll)
    for i in range(3):
        box(f"{name}_m{i}", (0.8, 0.02, 0.24), (-0.05 + (i % 2) * 0.1, -0.09, -0.15 - i * 0.38),
            emitm(["#63c06a", "#3f7fd9", "#63c06a"][i], 1.5), 0.08, parent=root, coll=coll)
    return root


def skateboard(name, loc, coll=None, s=1.0, rot=0, col="#e8423a"):
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    box(name + "_d", (1.2, 3.2, 0.14), (0, 0, 0.55), M(col, 0.4), 0.06, parent=root, coll=coll)
    for sy in (-1, 1):
        for sx in (-1, 1):
            cyl(f"{name}_w{sx}{sy}", 0.2, 0.18, (sx * 0.45, sy * 1.05, 0.22), M("#f4f4f4", 0.4), 12, rot=(0, 90, 0),
                parent=root, coll=coll)
    return root


def peanut(name, loc, s=1.0, coll=None, rot=0):
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    Mp = M("#d9a86a", 0.75)
    sphere(name + "_a", 0.22, (0, -0.2, 0.2), Mp, (1, 1.15, 1), parent=root, coll=coll, seg=14)
    sphere(name + "_b", 0.2, (0, 0.18, 0.19), Mp, (1, 1.1, 1), parent=root, coll=coll, seg=14)
    sphere(name + "_c", 0.15, (0, 0.0, 0.17), Mp, (1, 1, 1), parent=root, coll=coll, seg=12)
    return root


def keys_prop(name, loc, coll=None, s=1.0, rot=0):
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    Mk = M("#d8d8de", 0.2, metal=0.95)
    cyl(name + "_ring", 0.22, 0.04, (0, 0, 0.03), Mk, 18, parent=root, coll=coll)
    box(name + "_k1", (0.12, 0.7, 0.04), (0.08, -0.5, 0.03), Mk, 0.02, parent=root, coll=coll, rot=(0, 0, 18))
    box(name + "_k1h", (0.34, 0.3, 0.05), (0.0, -0.18, 0.03), M("#222226", 0.4), 0.06, parent=root, coll=coll)
    box(name + "_k2", (0.12, 0.6, 0.04), (-0.25, -0.35, 0.03), M("#e2b23a", 0.2, metal=0.9), 0.02, parent=root, coll=coll,
        rot=(0, 0, -35))
    return root


def horse(name, loc, rot=0, coll=None):
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    Mh = M("#8a5a32", 0.6); Md = M("#3a2516", 0.7)
    box(name + "_body", (2.2, 5.0, 2.2), (0, 0, 4.0), Mh, 0.4, parent=root, coll=coll)
    box(name + "_neck", (1.2, 1.4, 2.6), (0, -2.6, 5.4), Mh, 0.3, parent=root, coll=coll, rot=(-25, 0, 0))
    hd = box(name + "_head", (1.2, 2.4, 1.2), (0, -3.6, 6.6), Mh, 0.3, parent=root, coll=coll)
    box(name + "_mane", (0.4, 1.6, 2.4), (0, -2.2, 5.9), Md, 0.1, parent=root, coll=coll, rot=(-25, 0, 0))
    for sx in (-1, 1):
        sphere(f"{name}_eye{sx}", 0.14, (sx * 0.6, -3.9, 6.9), M("#151515", 0.2), parent=root, coll=coll, seg=8)
        box(f"{name}_ear{sx}", (0.25, 0.25, 0.6), (sx * 0.35, -3.0, 7.4), Mh, 0.06, parent=root, coll=coll)
        for sy in (-1, 1):
            box(f"{name}_leg{sx}{sy}", (0.6, 0.6, 3.0), (sx * 0.7, sy * 1.8, 1.5), Mh, 0.1, parent=root, coll=coll)
            box(f"{name}_hoof{sx}{sy}", (0.66, 0.66, 0.4), (sx * 0.7, sy * 1.8, 0.2), Md, 0.06, parent=root, coll=coll)
    tl = box(name + "_tail", (0.4, 0.4, 2.2), (0, 2.6, 3.8), Md, 0.1, parent=root, coll=coll, rot=(30, 0, 0))
    noise(tl, "rotation_euler", 1, 0.3, 6)
    noise(hd, "rotation_euler", 0, 0.08, 10)
    return root


def thermometer(loc, t, coll=None):
    root = empty("therm", loc, coll=coll)
    box("th_board", (1.6, 0.15, 6.0), (0, 0.1, 3.0), M("#f4f4f4", 0.5), 0.3, parent=root, coll=coll)
    cyl("th_tube", 0.28, 4.4, (0, -0.05, 3.4), mat("th_glass", hexc("#e8f4ff"), 0.1, alpha=0.5), 16, parent=root, coll=coll)
    sphere("th_bulb", 0.55, (0, -0.05, 0.9), emitm("#ff2a2a", 1.5), parent=root, coll=coll, seg=16)
    col = cyl("th_red", 0.17, 4.2, (0, -0.06, 1.1 + 2.1), emitm("#ff2a2a", 1.5), 12, parent=root, coll=coll)
    col.scale = (1, 1, 0.15); col.location = (0, -0.06, 1.1 + 2.1 * 0.15); col.keyframe_insert("scale", frame=F(t))
    col.keyframe_insert("location", frame=F(t))
    col.scale = (1, 1, 1.0); col.location = (0, -0.06, 3.2); col.keyframe_insert("scale", frame=F(t + 0.8))
    col.keyframe_insert("location", frame=F(t + 0.8))
    for i in range(5):
        box(f"th_tick{i}", (0.4, 0.05, 0.06), (0.45, -0.05, 1.6 + i * 0.85), M("#2a2a3a"), 0.0, parent=root, coll=coll)
    return root


def clock9(loc, coll=None, yaw=0):
    root = empty("clk", loc, coll=coll, rot=(0, 0, yaw))
    cyl("clk_b", 1.3, 0.25, (0, 0, 0), M("#f6f0e0", 0.5), 32, rot=(90, 0, 0), parent=root, coll=coll)
    cyl("clk_r", 1.42, 0.2, (0, 0.06, 0), M("#2a2a3a", 0.4), 32, rot=(90, 0, 0), parent=root, coll=coll)
    box("clk_h", (0.12, 0.05, 0.8), (-0.4, -0.16, 0), M("#1a1a1a"), 0.02, parent=root, coll=coll, rot=(0, 90, 0))
    box("clk_m", (0.08, 0.05, 1.1), (0, -0.18, 0.45), M("#1a1a1a"), 0.02, parent=root, coll=coll)
    text("clk_9", "9", (-0.95, -0.15, -0.15), 0.38, M("#1a1a1a"), extrude=0.01, parent=root, coll=coll)
    text("clk_12", "12", (0, -0.15, 0.8), 0.32, M("#1a1a1a"), extrude=0.01, parent=root, coll=coll)
    return root


# ================================================================== sets
def day(strength=4.0, rot=(50, 0, 32)):
    W.sky(1.0)
    W.sun(strength, rot=rot)


def kitchen(night=False, door=False, table=None):
    if night:
        world((0.12, 0.15, 0.3), 0.6)
    else:
        world((0.9, 0.93, 1.0), 0.45)
    c = collection("KITCH")
    box("k_floor", (60, 50, 0.4), (0, 0, -0.2), sets.checker_mat("k_fl", "#f2ece0", "#d8cdb8", 0.18), 0, coll=c)
    box("k_back", (60, 0.5, 16), (0, 8.25, 8), M("#bfe0d0" if not night else "#7a8fa0", 0.85), 0, coll=c)
    box("k_left", (0.5, 50, 16), (-16, 0, 8), M("#b0d4c4" if not night else "#6a7d8e", 0.85), 0, coll=c)
    Mc = wood("k_cab", "#e8e2d4", "#f4efe4", 2.0)
    box("k_counter", (20, 3.2, CTOP - 0.2), (0, 6.5, (CTOP - 0.2) / 2), M("#4f86c6", 0.6), 0.06, coll=c)
    box("k_top", (20.4, 3.5, 0.2), (0, 6.4, CTOP - 0.1), M("#f4f1ea", 0.25), 0.04, coll=c)
    for i in range(5):
        box(f"k_door{i}", (3.4, 0.08, 2.2), (-8 + i * 4, 4.86, 1.6), M("#5f96d6", 0.55), 0.06, coll=c)
        sphere(f"k_knob{i}", 0.12, (-8 + i * 4 + 1.2, 4.8, 2.3), M("#e2b23a", 0.3, metal=0.8), coll=c, seg=8)
    for i in range(4):
        box(f"k_up{i}", (3.6, 1.6, 3.0), (-6 + i * 4, 7.4, 10.0), Mc, 0.08, coll=c)
    # sink + faucet
    box("k_sink", (3.4, 2.2, 0.15), (-5, 6.2, CTOP + 0.02), M("#b8bcc4", 0.2, metal=0.8), 0.05, coll=c)
    cyl("k_fau", 0.14, 1.6, (-5, 7.3, CTOP + 0.8), M("#c8ccd4", 0.15, metal=0.9), 10, coll=c)
    box("k_spout", (0.24, 1.1, 0.24), (-5, 6.85, CTOP + 1.55), M("#c8ccd4", 0.15, metal=0.9), 0.08, coll=c)
    # window over the sink
    box("k_wfr", (5.0, 0.3, 4.0), (-5, 8.0, 7.0), M("#f4f4f4"), 0.04, coll=c)
    card("k_wsky", 4.4, 3.4, (-5, 7.85, 7.0), emitm("#bfe3ff" if not night else "#1a2a5a", 2.5 if not night else 1.0),
         "-Y", coll=c)
    # fridge
    box("k_fridge", (4, 3.6, 9), (-12.5, 6.2, 4.5), M("#e8eef4", 0.25, metal=0.3), 0.15, coll=c)
    box("k_fh", (0.25, 0.3, 2.4), (-11.0, 4.3, 5.5), M("#c8ccd4", 0.2, metal=0.8), 0.06, coll=c)
    mug_big(MUG, c)
    if table if table is not None else night:
        Mt = wood("k_tab", "#a0703f", "#c89260", 2.0)
        box("k_table", (8, 5, 0.3), (1, -5, TABLE_Z - 0.15), Mt, 0.06, coll=c)
        for sx in (-1, 1):
            for sy in (-1, 1):
                box(f"k_tl{sx}{sy}", (0.35, 0.35, TABLE_Z - 0.3), (1 + sx * 3.5, -5 + sy * 2.1, (TABLE_Z - 0.3) / 2),
                    M("#704a2a"), 0.02, coll=c)
    if door:
        Mw = M("#bfe0d0" if not night else "#7a8fa0", 0.85)
        box("k_dw1", (6, 0.5, 16), (DOOR_X - 4.6, -3, 8), Mw, 0, coll=c)
        box("k_dw2", (6, 0.5, 16), (DOOR_X + 4.6, -3, 8), Mw, 0, coll=c)
        box("k_dw3", (3.2, 0.5, 9.6), (DOOR_X, -3, 6.2 + 4.8), Mw, 0, coll=c)
        Mf = M("#f4f4f4", 0.5)
        for sx in (-1, 1):
            box(f"k_df{sx}", (0.3, 0.7, 6.2), (DOOR_X + sx * 1.6, -3, 3.1), Mf, 0.04, coll=c)
        box("k_dft", (3.5, 0.7, 0.3), (DOOR_X, -3, 6.2), Mf, 0.04, coll=c)
        box("k_hall", (6, 0.5, 8), (DOOR_X, 3, 4), M("#e8d8b8", 0.85), 0, coll=c)
    if night:
        cyl("k_pend", 0.05, 4, (1, -5, 11), M("#2a2a2a"), 6, coll=c)
        sphere("k_shade", 1.0, (1, -5, 8.6), emitm("#ffd890", 3.0), (1, 1, 0.5), coll=c, seg=16)
        light("k_lamp", "POINT", (1, -5, 7.8), 6000, (1.0, 0.82, 0.55), 2.0, coll=c)
        light("k_fill", "AREA", (0, -16, 10), 2500, (0.6, 0.7, 1.0), 14, coll=c, target=(0, 0, 3))
        light("k_fill2", "AREA", (9, -15, 10), 3500, (1.0, 0.85, 0.7), 10, coll=c, target=(9, -5, 3))
    else:
        light("k_key", "AREA", (0, -6, 13), 5000, (1.0, 0.97, 0.92), 12, coll=c, target=(0, 4, 2))
        light("k_fill", "AREA", (-10, -4, 6), 1500, (0.9, 0.95, 1.0), 6, coll=c, target=(0, 4, 3))
    return c


def car_set(open_t=None, pane_up=None, door_open=False):
    """Family car on the driveway. The driver door is a hinged root with the window, handle and unlock button."""
    c = collection("CAR")
    root = empty("car", CAR, coll=c)
    Mb = M("#3fa7d9", 0.25, metal=0.35)
    Mg = mat("carglass", hexc("#9fd0ee"), 0.05, metal=0.2, alpha=0.28)
    Mi = M("#3a3a44", 0.8)
    x0, y0 = CAR[0], CAR[1]
    box("car_body_f", (4.0, 7.5, 2.6), (x0 - 6.0, y0, 2.3), Mb, 0.5, coll=c)
    box("car_body_r", (7.6, 7.5, 2.6), (x0 + 4.2, y0, 2.3), Mb, 0.5, coll=c)
    box("car_floor", (16, 7.3, 0.4), (x0, y0, 1.2), Mi, 0.05, coll=c)
    box("car_pside", (16, 0.3, 2.6), (x0, y0 + 3.6, 2.3), Mb, 0.1, coll=c)
    box("car_roof", (9.2, 7.3, 0.35), (x0 + 0.5, y0, 6.1), Mb, 0.15, coll=c)
    for x in (-4.0, 4.9):
        for sy in (-1, 1):
            box(f"car_pil{x}{sy}", (0.35, 0.35, 2.5), (x0 + x, y0 + sy * 3.55, 4.85), Mb, 0.05, coll=c)
    box("car_bpil", (0.4, 0.35, 2.5), (x0 + 0.5, y0 - 3.55, 4.85), Mb, 0.05, coll=c)
    box("car_wsh", (0.08, 7.0, 2.6), (x0 - 4.5, y0, 4.8), Mg, 0.02, coll=c, rot=(0, -28, 0))
    box("car_rear", (0.08, 7.0, 2.5), (x0 + 5.2, y0, 4.8), Mg, 0.02, coll=c, rot=(0, 20, 0))
    box("car_backwin", (4.0, 0.08, 2.3), (x0 + 2.7, y0 - 3.6, 4.85), Mg, 0.02, coll=c)
    box("car_pwin", (8.6, 0.08, 2.3), (x0 + 0.4, y0 + 3.6, 4.85), Mg, 0.02, coll=c)
    box("car_rdoor", (4.3, 0.3, 2.6), (x0 + 2.7, y0 - 3.6, 2.3), Mb, 0.1, coll=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(f"car_wh{sx}{sy}", 1.3, 0.8, (x0 + sx * 5.4, y0 + sy * 3.5, 1.3), M("#151515", 0.7), 22, rot=(90, 0, 0), coll=c)
            cyl(f"car_hub{sx}{sy}", 0.6, 0.85, (x0 + sx * 5.4, y0 + sy * 3.5, 1.3), M("#c8ccd4", 0.2, metal=0.9), 16,
                rot=(90, 0, 0), coll=c)
    for sy in (-1, 1):
        sphere(f"car_hl{sy}", 0.45, (x0 - 8.0, y0 + sy * 2.6, 2.8), emitm("#fff6d0", 1.5), (0.4, 1, 1), coll=c, seg=12)
        sphere(f"car_tl{sy}", 0.4, (x0 + 8.0, y0 + sy * 2.6, 2.8), emitm("#ff3a3a", 1.2), (0.4, 1, 1), coll=c, seg=12)
    # interior
    Ms = M("#5a4a3a", 0.8)
    for y, nm in ((y0 - 1.6, "d"), (y0 + 1.7, "p")):
        box(f"seat_{nm}", (2.6, 2.6, 0.8), (x0 - 1.6, y, 2.7), Ms, 0.25, coll=c)
        box(f"seatb_{nm}", (0.7, 2.6, 2.8), (x0 - 0.1, y, 3.9), Ms, 0.3, coll=c, rot=(0, 10, 0))
    box("seat_back", (2.6, 6.6, 0.8), (x0 + 3.2, y0, 2.7), Ms, 0.25, coll=c)
    box("dash", (1.4, 7.0, 1.2), (x0 - 3.7, y0, 3.9), M("#2a2a32", 0.6), 0.2, coll=c)
    cyl("wheel", 0.85, 0.15, (x0 - 2.9, y0 - 1.6, 4.5), M("#18181c", 0.5), 24, rot=(0, 65, 0), coll=c)
    keys_prop("keys", KEYS, c, 1.0, rot=30)
    light("car_in", "POINT", (x0 - 1.0, y0, 5.4), 1500, (1.0, 0.95, 0.85), 1.0, coll=c)
    # driver door on a hinge
    door = empty("ddoor", HINGE, coll=c)
    lx, ly = -HINGE[0], -HINGE[1]

    def dl(p):
        return (p[0] - HINGE[0], p[1] - HINGE[1], p[2] - HINGE[2])
    box("dd_panel", (4.4, 0.3, 2.6), dl((x0 - 1.85, y0 - 3.6, 2.3)), Mb, 0.1, parent=door, coll=c)
    box("dd_inner", (4.2, 0.3, 2.4), dl((x0 - 1.85, y0 - 3.3, 2.4)), M("#4a4a54", 0.8), 0.08, parent=door, coll=c)
    box("dd_arm", (2.4, 0.6, 0.3), dl((x0 - 1.6, y0 - 3.15, 3.25)), M("#3a3a44", 0.8), 0.1, parent=door, coll=c)
    btn = box("dd_btn", (0.6, 0.4, 0.22), dl(BUTTON), emitm("#ff3a3a", 1.5), 0.08, parent=door, coll=c)
    box("dd_handle", (1.0, 0.3, 0.28), dl(HANDLE), M("#d8d8de", 0.2, metal=0.9), 0.1, parent=door, coll=c)
    for z in (3.6, 6.0):
        box(f"dd_fr{z}", (4.4, 0.25, 0.22), dl((x0 - 1.85, y0 - 3.55, z)), Mb, 0.05, parent=door, coll=c)
    box("dd_frb", (0.22, 0.25, 2.4), dl((x0 + 0.3, y0 - 3.55, 4.8)), Mb, 0.05, parent=door, coll=c)
    pane = box("dd_glass", (4.1, 0.08, 1.85), dl((x0 - 1.85, y0 - 3.55, GAP_Z - 0.93)), Mg, 0.02, parent=door, coll=c)
    pin = cyl("dd_pin", 0.08, 0.45, dl((x0 + 0.0, y0 - 3.35, 3.75)), M("#c8ccd4", 0.3, metal=0.8), 8, parent=door, coll=c)
    if pane_up is not None:
        t0, t1 = pane_up
        z = pane.location[2]
        pane.location[2] = z - 1.6; pane.keyframe_insert("location", index=2, frame=F(t0))
        pane.location[2] = z; pane.keyframe_insert("location", index=2, frame=F(t1))
    if open_t is not None:
        door.rotation_euler = (0, 0, 0); door.keyframe_insert("rotation_euler", frame=F(open_t))
        door.rotation_euler = (0, 0, math.radians(-68)); door.keyframe_insert("rotation_euler", frame=F(open_t + 0.45))
        set_interp(door, "rotation_euler", F(open_t), "BEZIER", "EASE_OUT")
    if door_open:
        door.rotation_euler = (0, 0, math.radians(-68))
    return dict(coll=c, door=door, pane=pane, btn=btn, pin=pin)


def driveway(hot=True, night=False):
    if night:
        world((0.05, 0.07, 0.18), 0.3)
    else:
        day(5.5 if hot else 4.0, rot=(40, 0, 28))
    c = collection("DRIVE")
    box("dw_lawn", (200, 200, 0.2), (0, 0, -0.1), M("#5fb04a" if not hot else "#8fb04a", 0.9), 0, coll=c)
    box("dw_conc", (14, 40, 0.12), (0, 2, 0.06), M("#cfcac0", 0.85), 0, coll=c)
    box("hs_body", (26, 12, 11), (0, 22, 5.5), M("#f2d7a8", 0.85), 0.1, coll=c)
    box("hs_roof", (28, 13.5, 1.4), (0, 22, 11.7), M("#a33b2f", 0.7), 0.25, coll=c)
    box("hs_gar", (10, 0.3, 7), (0, 15.9, 3.5), M("#f4f4f4", 0.6), 0.06, coll=c)
    for i in range(5):
        box(f"hs_gl{i}", (10, 0.32, 0.08), (0, 15.85, 0.8 + i * 1.4), M("#d8d8d8", 0.6), 0, coll=c)
    box("hs_door", (2.8, 0.3, 5.4), (-9, 15.9, 2.7), M("#3f7fd9", 0.5), 0.06, coll=c)
    for k, (x, y) in enumerate(((-22, 8), (20, 6), (-26, -16), (26, -20))):
        cyl(f"dw_tt{k}", 0.5, 6, (x, y, 3), M("#6a4a2a"), 10, coll=c)
        sphere(f"dw_tc{k}", 3.6, (x, y, 8), M("#3f8f3a", 0.9), (1, 1, 1.1), coll=c, seg=14)
    if hot:
        light("dw_hot", "AREA", (0, -20, 25), 9000, (1.0, 0.85, 0.6), 30, coll=c, target=(0, 2, 2))
    return c


def office():
    world((0.85, 0.9, 1.0), 0.4)
    c = collection("OFF")
    box("of_floor", (40, 40, 0.4), (0, 0, -0.2), M("#8a8f9a", 0.9), 0, coll=c)
    box("of_back", (40, 0.5, 14), (0, 8.25, 7), M("#e8ecf0", 0.85), 0, coll=c)
    for i in range(3):
        box(f"of_win{i}", (5, 0.3, 5), (-8 + i * 8, 8.0, 7), M("#f4f4f4"), 0.04, coll=c)
        card(f"of_sky{i}", 4.4, 4.4, (-8 + i * 8, 7.85, 7), emitm("#bfe3ff", 2.5), "-Y", coll=c)
    box("of_desk", (8, 4, 0.3), (0, 3.5, 2.6), M("#f4f1ea", 0.5), 0.05, coll=c)
    box("of_dleg", (7.6, 3.6, 2.4), (0, 3.7, 1.2), M("#b8bcc4", 0.4), 0.05, coll=c)
    box("of_mon", (4, 0.3, 2.4), (0, 4.6, 4.3), M("#18181c", 0.3), 0.1, coll=c)
    card("of_scr", 3.7, 2.1, (0, 4.42, 4.3), emitm("#5aa0ff", 1.6), "-Y", coll=c)
    box("of_kb", (2.6, 1.0, 0.1), (0, 2.6, 2.8), M("#2a2a32", 0.5), 0.03, coll=c)
    light("of_key", "AREA", (0, -6, 12), 4500, (1.0, 0.97, 0.92), 12, coll=c, target=(0, 4, 2))
    return c


def playground():
    day(4.0, rot=(52, 0, 40))
    c = collection("PLAY")
    box("pg_grass", (200, 200, 0.2), (0, 0, -0.1), M("#5fb04a", 0.9), 0, coll=c)
    box("pg_path", (80, 8, 0.12), (0, 0, 0.06), M("#d6d2c8", 0.85), 0, coll=c)
    box("pg_sand", (10, 8, 0.3), (-8, 14, 0.15), M("#f2d898", 0.9), 0.1, coll=c)
    Mr = M("#e8423a", 0.4); My = M("#f2c14e", 0.4)
    box("pg_slide", (2.4, 9, 0.3), (8, 14, 3.0), My, 0.1, coll=c, rot=(-30, 0, 0))
    box("pg_tower", (4, 4, 6), (8, 19.5, 3), Mr, 0.1, coll=c)
    for sx in (-1, 1):
        cyl(f"pg_sw{sx}", 0.25, 9, (-20 + sx * 4, 16, 4.5), M("#3f7fd9", 0.4), 10, coll=c)
    box("pg_swt", (8.5, 0.5, 0.5), (-20, 16, 9), M("#3f7fd9", 0.4), 0.1, coll=c)
    for k, (x, y) in enumerate(((-34, 24), (28, 26), (36, 10))):
        cyl(f"pg_tt{k}", 0.5, 6, (x, y, 3), M("#6a4a2a"), 10, coll=c)
        sphere(f"pg_tc{k}", 4.0, (x, y, 8), M("#3f8f3a", 0.9), coll=c, seg=14)
    return c


def dollhouse_room():
    world((0.95, 0.9, 0.95), 0.45)
    c = collection("DOLL")
    box("dr_floor", (40, 40, 0.4), (0, 0, -0.2), planks("dr_fl", "#c9a27a", "#bd966e", "#7a5a40"), 0, coll=c)
    box("dr_back", (40, 0.5, 14), (0, 8.25, 7), M("#f6d3e0", 0.85), 0, coll=c)
    Mp = M("#f09ac2", 0.6); Mw = M("#ffffff", 0.5)
    box("dh_body", (6, 4, 6.4), (0, 3, 3.2), Mp, 0.08, coll=c)
    for sx in (-1, 1):
        box(f"dh_roof{sx}", (4.4, 4.4, 0.3), (sx * 1.6, 3, 7.4), M("#9b6ad6", 0.5), 0.05, coll=c, rot=(0, sx * 40, 0))
    box("dh_door", (1.2, 0.1, 2.0), (0, 0.96, 1.0), M("#ffffff", 0.5), 0.04, coll=c)
    for k, (x, z) in enumerate(((-1.6, 4.4), (1.6, 4.4), (-1.6, 1.8), (1.6, 1.8))):
        box(f"dh_wf{k}", (1.2, 0.1, 1.2), (x, 0.96, z), Mw, 0.03, coll=c)
        card(f"dh_wl{k}", 1.0, 1.0, (x, 0.9, z), emitm("#ffd890", 2.5), "-Y", coll=c)
    box("dh_porch", (3, 1.4, 0.3), (0, 0.3, 0.15), Mw, 0.04, coll=c)
    light("dr_key", "AREA", (0, -8, 10), 4000, (1.0, 0.95, 0.9), 10, coll=c, target=(0, 2, 2))
    return c


def lineup_wall():
    day(4.0, rot=(50, 0, 25))
    c = collection("LINE")
    box("ln_ground", (200, 200, 0.2), (0, 0, -0.1), M("#d6d2c8", 0.9), 0, coll=c)
    box("ln_wall", (40, 0.4, 12), (0, 4, 6), M("#cfd8e8", 0.8), 0, coll=c)
    Ml = M("#2a2a3a", 0.6)
    for i in range(10):
        box(f"ln_l{i}", (40, 0.1, 0.06), (0, 3.78, 1 + i), Ml, 0, coll=c)
        text(f"ln_t{i}", f"{i + 1}'", (-15, 3.76, 1 + i + 0.12), 0.4, Ml, extrude=0.01, coll=c)
    return c


def restaurant():
    world((0.95, 0.88, 0.8), 0.45)
    c = collection("REST")
    box("rs_floor", (40, 40, 0.4), (0, 0, -0.2), sets.checker_mat("rs_fl", "#e8423a", "#f4f1ea", 0.25), 0, coll=c)
    box("rs_back", (40, 0.5, 16), (0, 8.25, 8), M("#f6d3a8", 0.85), 0, coll=c)
    box("rs_board", (9, 0.3, 4.4), (0, 7.9, 9.5), M("#2a2a32", 0.6), 0.1, coll=c)
    text("rs_t1", "MENU", (0, 7.7, 10.6), 0.9, emitm("#ffe14a", 2), extrude=0.04, coll=c)
    text("rs_t2", "PIZZA  TACOS", (0, 7.7, 9.2), 0.65, emitm("#ffffff", 1.5), extrude=0.03, coll=c)
    text("rs_t3", "BURGERS", (0, 7.7, 8.2), 0.65, emitm("#ffffff", 1.5), extrude=0.03, coll=c)
    box("rs_table", (6, 3.4, 0.3), (0, 1, 2.6), M("#f4f4f4", 0.4), 0.05, coll=c)
    box("rs_tleg", (0.6, 0.6, 2.5), (0, 1, 1.25), M("#c8ccd4", 0.2, metal=0.8), 0.05, coll=c)
    light("rs_key", "AREA", (0, -6, 13), 5000, (1.0, 0.93, 0.85), 12, coll=c, target=(0, 4, 3))
    return c


# ================================================================== helpers for the kitchen ask beats
def kitchen_dad(t0, t1, expr="smile", s=S2, loc=DAD_K, rot=None):
    d = dad_c(t0, t1, expr, s)
    d.pose(t0, loc=loc, rot=facing(loc, KID_K) if rot is None else rot)
    return d


def kitchen_kid(t0, t1, expr="happy"):
    k = kid_c(t0, t1, expr)
    k.pose(t0, loc=KID_K, rot=facing(KID_K, DAD_K))
    return k


def cam_on_dad(cam, t0, t1, d0=3.2, d1=2.4, yaw=-40, yaw1=-55, pitch=6, lens=32, s=S2, loc=DAD_K):
    tgt = (loc[0], loc[1], loc[2] + 3.6 * s)
    cam.push(t0, t1, tgt, d0, d1, yaw=yaw, yaw1=yaw1, pitch=pitch, lens=lens, fstop=1.6)
    cam.handheld(0.25)
    return tgt


def cam_on_kid(cam, t0, t1, d0=6.0, d1=4.6, yaw=150, yaw1=135, pitch=-6, lens=30):
    tgt = head(KID_K)
    cam.push(t0, t1, tgt, d0, d1, yaw=yaw, yaw1=yaw1, pitch=pitch, lens=lens, fstop=2.4)
    cam.handheld(0.7)
    return tgt


# ================================================================== HOOK
@S(1, 0, 6, "HOOK: two-inch dad flexes on the counter next to a giant #1 DAD mug")
def s01(t0, t1):
    kitchen()
    shoebox(BOX_K)
    d = kitchen_dad(t0, t1, "grin", rot=-20)
    d.act(t0, "fists", expr="grin")
    d.pose(t0 + 0.45, armL=(160, 40), armR=(160, 40), torso=(0, -8, 0))
    d.pose(t0 + 0.8, armL=(95, 70), armR=(95, 70), torso=(0, -4, 0))
    tgt = up(DAD_K, 0.6)
    cam = Cam()
    cam.whip(t0, t0 + 0.2, orbit_pos(up(MUG, 1.2), 4.0, 10, 4), up(MUG, 1.2),
             orbit_pos(tgt, 3.0, -15, 4), tgt, lens=32)
    cam.key(t1, orbit_pos(tgt, 2.2, -28, 8), tgt, lens=32, focus=tgt, fstop=1.6)
    cam.crash(t0 + 0.45, 32, 40, 0.1)
    cam.handheld(0.3)
    sfx(t0 + 0.45, "boing", 0.5)


@S(2, 6, 13, "Biggest hero: low heroic angle, cape, sparkles")
def s02(t0, t1):
    kitchen()
    d = dad_c(t0, t1, "smug", cape=True)
    d.pose(t0, loc=DAD_K, rot=-10)
    d.act(t0, "cross", expr="smug")
    d.pose(w(9), armL=(10, 30), armR=(10, 30), torso=(0, -6, 0))
    d.face(w(9), "grin")
    sparkle_on("hero", up(DAD_K, 0.6), w(9), 0.7, 14, seed=2)
    tgt = up(DAD_K, 0.55)
    cam = Cam()
    cam.orbit(t0, t1, tgt, 2.4, -40, 20, pitch=-5, lens=28, fstop=1.8)
    cam.handheld(0.25)
    light("hero_rim", "POINT", (DAD_K[0] + 1.5, DAD_K[1] + 2, CTOP + 3), 300, (1.0, 0.9, 0.6), 0.3, target=tgt)
    sfx(w(9), "sparkle", 0.8)
    sfx(w(9) - 0.2, "rise", 0.5)


@S(3, 13, 18, "In this world: street of dads of every size")
def s03(t0, t1):
    lineup_wall()
    sizes = [1.4, 0.35, 1.0, 0.6, 1.2, 0.2]
    for i, s in enumerate(sizes):
        a = adult(i, t0, t1, "happy", s)
        x0 = -16 + i * 6.0
        a.walk(t0, t1, (x0, -2 - (i % 2) * 1.5, 0), (x0 + 5, -2 - (i % 2) * 1.5, 0), rate=2.2, bob=0.12)
    cam = Cam()
    cam.key(t0, (-10, -17, 4.0), (-4, 0, 3.0), lens=24, focus=17.0, fstop=6)
    cam.key(t1, (0, -15, 3.5), (5, 0, 2.6), lens=24, focus=15.0, fstop=6)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "footsteps", 0.6)


@S(4, 18, 23, "Every time a dad says: kid tugs dad's shirt in a store aisle")
def s04(t0, t1):
    restaurant()
    a = adult(3, t0, t1, "neutral", 1.0)
    a.pose(t0, loc=(1.5, -2, 0), rot=-20)
    k = townie(4, t0, t1, "happy")
    k.pose(t0, loc=(-1.2, -3.2, 0), rot=facing((-1.2, -3.2), (1.5, -2)))
    k.act(t0, "reach", expr="happy")
    lips(k, t0, t1)
    look_at(a, t0 + 0.4, head((-1.2, -3.2, 0)))
    cam = Cam()
    cam.push(t0, t1, (0.3, -2.5, 3.8), 11, 8, yaw=-20, pitch=4, lens=24, yaw1=-6, fstop=3.5)
    cam.handheld(1.0)


@S(5, 23, 26, "Ask your mom: dad shrugs")
def s05(t0, t1):
    restaurant()
    a = adult(3, t0, t1, "smile", 1.0)
    p = (1.5, -2, 0)
    a.pose(t0, loc=p, rot=-20)
    ask_mom(a, t0, t1)
    cam = Cam()
    cam.push(t0, t1, head(p), 6.5, 4.8, yaw=-25, pitch=2, lens=28, yaw1=-12, fstop=2.4)
    cam.handheld(0.8)


@S(6, 26, 30, "He shrinks one inch: -1 INCH pops")
def s06(t0, t1):
    restaurant()
    p = (1.5, -2, 0)
    a = adult(3, t0, t1, "shock", 1.0)
    a.pose(t0, loc=p, rot=-20)
    ts = w(27)
    resize(a, ts, 1.0, 0.86, loc=p)
    a.face(ts + 0.2, "shock")
    a.act(ts + 0.2, "shock")
    pop_text("m1", "-1 INCH", (p[0] - 1.2, p[1] - 1, 5.9), ts + 0.1, 0.7, "#ff5a5a", yaw=-15)
    cam = Cam()
    cam.push(t0, t1, (p[0] - 1, p[1], 3.8), 10, 8, yaw=-18, pitch=4, lens=24, fstop=4)
    cam.crash(ts + 0.25, 24, 30, 0.1)
    cam.handheld(1.2)


@S(7, 30, 39, "Only way to grow back: dad thinks hard, kid waits")
def s07(t0, t1):
    restaurant()
    p = (1.5, -2, 0)
    a = adult(3, t0, t1, "worried", 0.86)
    a.pose(t0, loc=p, rot=-30)
    a.act(t0 + 0.1, "think", expr="worried")
    a.look(t0 + 0.8, 25, -10)
    a.look(t0 + 1.4, -25, -10)
    k = townie(4, t0, t1, "bored")
    k.pose(t0, loc=(-1.2, -3.2, 0), rot=facing((-1.2, -3.2), p))
    k.act(t0 + 0.5, "cross", expr="bored")
    cam = Cam()
    cam.orbit(t0, t1, (0.3, -2.5, 3.4), 9.0, -40, 5, pitch=6, lens=24, fstop=3.5)
    cam.handheld(1.0)
    sfx(t0 + 0.6, "crickets", 0.35)


@S(8, 39, 42, "Make a decision: fist slam, +1 INCH, grows")
def s08(t0, t1):
    restaurant()
    p = (1.5, -2, 0)
    a = adult(3, t0, t1, "determined", 0.86)
    a.pose(t0, loc=p, rot=-20)
    a.act(t0, "fists", expr="determined")
    tg = w(41)
    a.pose(tg, armR=(150, -10))
    a.face(tg, "shout")
    resize(a, tg, 0.86, 1.0, loc=p)
    pop_text("p1", "+1 INCH", (p[0] - 0.8, p[1] - 1, 6.0), tg + 0.1, 0.6, "#63e07a", yaw=-15)
    cam = Cam()
    cam.push(t0, t1, head(p, 0.95), 7, 5.5, yaw=-25, pitch=-8, lens=26, fstop=2.8)
    cam.crash(tg, 26, 34, 0.1)
    cam.handheld(1.3)
    sfx(tg, "bonk", 0.4)


@S(9, 42, 44, "By himself: proud hands on hips")
def s09(t0, t1):
    restaurant()
    p = (1.5, -2, 0)
    a = adult(3, t0, t1, "smug", 1.0)
    a.pose(t0, loc=p, rot=-10)
    a.pose(t0, armL=(30, 60), armR=(30, 60), torso=(0, -8, 0))
    sparkle_on("bh", head(p), t0 + 0.05, 1.6, 12, seed=3)
    cam = Cam()
    cam.orbit(t0, t1, head(p, 0.9), 6.0, 20, -10, pitch=-10, lens=28, fstop=2.8)
    cam.handheld(0.8)
    sfx(t0 + 0.05, "ding", 0.6)


@S(10, 44, 51, "Tell everything about a dad: lineup of dads against the height wall")
def s10(t0, t1):
    lineup_wall()
    sizes = [0.25, 0.5, 0.8, 1.0, 1.2, 1.4]
    exprs = ["worried", "sus", "neutral", "smile", "smug", "grin"]
    for i, s in enumerate(sizes):
        a = adult(i, t0, t1, exprs[i], s)
        a.pose(t0, loc=(-10 + i * 4.0, 1.5, 0), rot=0)
        if i == 5:
            a.act(t0 + 0.6, "cross", expr="smug")
    cam = Cam()
    cam.key(t0, (-10, -9, 2.0), (-9, 1.5, 1.4), lens=24, focus=10.0, fstop=4)
    cam.key(t1, (9, -10, 4.5), (10, 1.5, 4.0), lens=24, focus=11.0, fstop=4)
    cam.handheld(0.9)
    sfx(t0 + 0.1, "whoosh", 0.4)


@S(11, 51, 55, "By his height: tilt up the measuring wall")
def s11(t0, t1):
    lineup_wall()
    a = adult(5, t0, t1, "smug", 1.4)
    a.pose(t0, loc=(0, 1.5, 0), rot=0)
    b = adult(0, t0, t1, "worried", 0.25)
    b.pose(t0, loc=(-3, 1.5, 0), rot=15)
    b.look(t0 + 0.4, 0, -40)
    cam = Cam()
    cam.key(t0, (-2.5, -8, 0.6), (-2.5, 1.5, 0.8), lens=26, focus=9.0, fstop=3)
    cam.key(t1, (0, -11, 3.0), (0, 1.5, 6.2), lens=26, focus=12.0, fstop=3)
    cam.handheld(0.9)


@S(12, 55, 58, "Seven foot dads? Crash zoom up a giant dad")
def s12(t0, t1):
    lineup_wall()
    a = adult(5, t0, t1, "smug", 1.45)
    p = (0, 0, 0)
    a.pose(t0, loc=p, rot=0)
    a.act(t0 + 0.05, "cross", expr="smug")
    pop_text("7ft", "7 FT", (1.6, -1, 8.4), t0 + 0.2, 0.9, "#ffe14a", yaw=8)
    cam = Cam()
    cam.key(t0, (0, -9, 1.0), (0, 0, 4.0), lens=20, focus=9.0, fstop=4)
    cam.key(t1, (1.5, -10, 0.6), (0.5, 0, 6.4), lens=24, focus=10.0, fstop=4)
    cam.crash(t0 + 0.1, 18, 24, 0.12)
    cam.handheld(1.2)
    sfx(t0 + 0.1, "stomp", 0.8)


@S(13, 58, 62, "They pick the restaurant: points at the menu, family cheers")
def s13(t0, t1):
    restaurant()
    a = adult(5, t0, t1, "grin", 1.4)
    a.pose(t0, loc=(4.5, -1.5, 0), rot=facing((4.5, -1.5), (0, 8)) + 30)
    a.act(t0 + 0.1, "point", expr="grin")
    for i, (x, y) in enumerate(((-2.0, -1.4), (-0.4, -2.2))):
        k = townie(5 + i, t0, t1, "happy")
        k.pose(t0, loc=(x, y, 0), rot=facing((x, y), (4.5, -1.5)))
        k.act(t0 + 0.5 + i * 0.1, "cheer", expr="joy")
    cam = Cam()
    cam.push(t0, t1, (1, 2, 6), 18, 14, yaw=-15, pitch=8, lens=22, yaw1=0, fstop=6)
    cam.handheld(1.0)
    sfx(t0 + 0.55, "cheer", 0.5)


@S(14, 62, 65, "Fix the sink: wrench, water spray stops, ding")
def s14(t0, t1):
    kitchen(table=False)
    a = adult(5, t0, t1, "determined", 1.4)
    p = (-5, 2.2, 0)
    a.pose(t0, loc=p, rot=180)
    a.act(t0, "reach", expr="determined")
    wr = box("wrench", (0.3, 1.6, 0.18), (0, 0, 0), M("#c8ccd4", 0.2, metal=0.9), 0.05)
    locs.hand_prop(a, "R", wr, offset=(0, -0.6, -1.9))
    noise(a.shR, "rotation_euler", 0, 0.25, 4)
    Mw = mat("water", hexc("#7fc8ff"), 0.05, emit=hexc("#9fd8ff"), estr=0.8, alpha=0.7)
    rnd = random.Random(1)
    ts = t0 + 0.7
    for i in range(14):
        o = sphere(f"spray{i}", 0.12, (-5, 6.3, CTOP + 1.4), Mw, seg=8)
        o.keyframe_insert("location", frame=F(t0))
        o.location = (-5 + rnd.uniform(-3, 3), 6.3 + rnd.uniform(-4, -1), CTOP + rnd.uniform(0.5, 4))
        o.keyframe_insert("location", frame=F(t0 + 0.5))
        sets.set_obj_visible(o, ts, False)
    sparkle_on("fixd", (-5, 6.5, CTOP + 1.6), ts, 1.0, 10, seed=5)
    cam = Cam()
    cam.push(t0, t1, (-5, 4.0, 5.0), 11, 9, yaw=-50, pitch=6, lens=22, yaw1=-35, fstop=5)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "splat", 0.4)
    sfx(ts, "ding", 0.7)


@S(15, 65, 71, "Never check the group chat: giant dad flicks the buzzing phone away")
def s15(t0, t1):
    restaurant()
    a = adult(5, t0, t1, "bored", 1.4)
    p = (1.5, 0, 0)
    a.pose(t0, loc=p, rot=-15)
    ph = phone_prop("ph", (-1.6, -1.0, 4.4), rot=(0, 0, 15), s=1.3)
    noise(ph, "rotation_euler", 1, 0.08, 1.5)
    tf = w(67)
    ph.keyframe_insert("location", frame=F(tf))
    ph.location = (-12, 6, 12); ph.keyframe_insert("location", frame=F(tf + 0.5))
    a.pose(tf - 0.2, armR=(80, -60))
    a.pose(tf + 0.1, armR=(110, 40))
    a.face(tf + 0.1, "smug")
    for i in range(4):
        sfx(t0 + 0.05 + i * 0.25, "chat", 0.35)
    cam = Cam()
    cam.push(t0, t1, (-1.0, -1.0, 4.8), 7.5, 6.0, yaw=-10, pitch=0, lens=26, yaw1=5, fstop=3)
    cam.handheld(1.0)
    sfx(tf, "whoosh", 0.6)


@S(16, 71, 75, "Playground dads: tiny dads cruising on skateboards")
def s16(t0, t1):
    playground()
    for i in range(3):
        s = 0.3
        y = -1.5 + i * 1.6
        x0 = -12 - i * 2.5
        a = adult(i + 1, t0, t1, "joy", s)
        sb = skateboard(f"sk{i}", (x0, y, 0), s=s * 1.4, rot=90, col=["#e8423a", "#63c06a", "#f2c14e"][i])
        for ob, z in ((a.root, 0.82 * s * 1.4), (sb, 0)):
            ob.location = (x0, y, z); ob.keyframe_insert("location", frame=F(t0))
            ob.location = (x0 + 18, y, z); ob.keyframe_insert("location", frame=F(t1 + 0.3))
            set_interp(ob, "location", F(t0), "LINEAR")
        a.pose(t0, rot=0, legL=(20, 10), legR=(-20, 10), armL=(60, 70), armR=(60, 70), torso=(0, 10, 0))
        noise(a.hip, "rotation_euler", 1, 0.15, 6)
    k = townie(7, t0, t1, "joy")
    k.pose(t0, loc=(-3, 8, 0), rot=10)
    k.act(t0 + 0.4, "cheer", expr="joy")
    cam = Cam()
    cam.key(t0, (-14, -9, 3.0), (-8, 0, 0.6), lens=24, focus=10.0, fstop=4)
    cam.key(t1, (0, -10, 2.5), (2, 0, 0.6), lens=24, focus=10.0, fstop=4)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "whoosh", 0.6)
    sfx(t0 + 0.6, "kids_laugh", 0.4)


@S(17, 75, 81, "Like little surfers: low tracking close-up, arms out")
def s17(t0, t1):
    playground()
    s = 0.3
    a = adult(2, t0, t1, "joy", s)
    sb = skateboard("skc", (0, 0, 0), s=s * 1.4, rot=90, col="#63c06a")
    x0, x1 = -8, 6
    for ob, z in ((a.root, 0.82 * s * 1.4), (sb, 0)):
        for k in range(4):
            tt = t0 + (t1 + 0.2 - t0) * k / 3
            ob.location = (x0 + (x1 - x0) * k / 3, 0, z)
            ob.keyframe_insert("location", frame=F(tt))
            set_interp(ob, "location", F(tt), "LINEAR")
    a.pose(t0, rot=0, legL=(25, 12), legR=(-25, 12), armL=(80, 85), armR=(80, 85), torso=(0, 8, 0))
    noise(a.hip, "rotation_euler", 0, 0.2, 5)
    noise(sb, "rotation_euler", 1, 0.1, 5)
    cam = Cam()
    cam.key(t0, (x0 - 1.2, -3.0, 0.5), (x0, 0, 0.75), lens=30, focus=3.2, fstop=2.0, interp="LINEAR")
    cam.key(t1 + 0.2, (x1 + 1.2, -3.0, 0.6), (x1, 0, 0.75), lens=30, focus=3.2, fstop=2.0, interp="LINEAR")
    cam.handheld(0.5)
    sfx(t0 + 0.2, "wind", 0.4)


@S(18, 81, 87, "Some dads live in dollhouses: tiny dad waves from the porch")
def s18(t0, t1):
    dollhouse_room()
    s = 0.25
    a = adult(4, t0, t1, "happy", s)
    p = (0.4, 0.3, 0.3)
    a.pose(t0, loc=p, rot=-10)
    a.act(t0 + 0.3, "wave", expr="happy")
    cam = Cam()
    cam.push(t0, t1, (0, 1, 3.0), 12, 7, yaw=-20, pitch=6, lens=24, yaw1=5, fstop=3)
    cam.handheld(0.8)
    sfx(t0 + 0.3, "sparkle", 0.4)


@S(19, 87, 94, "Carried to work in lunchboxes: lunchbox swings, tiny dad with briefcase pops out")
def s19(t0, t1):
    W.sky(1.0); W.sun(4.0)
    W.town(school=False)
    Mo, _ = mom_c(t0, t1, "happy")
    Mo.walk(t0, t1 + 0.5, (-10, -30, 0), (4, -30, 0), rate=2.0)
    lb = empty("lunch", (0, 0, 0))
    box("lb_box", (1.6, 1.0, 1.1), (0, 0, -0.55), M("#e8423a", 0.4), 0.12, parent=lb)
    box("lb_hand", (0.8, 0.12, 0.5), (0, 0, 0.1), M("#2b2b2b", 0.5), 0.06, parent=lb)
    lid = box("lb_lid", (1.6, 1.0, 0.12), (0, 0.5, 0.02), M("#d0262a", 0.4), 0.05, parent=lb, rot=(-60, 0, 0))
    locs.hand_prop(Mo, "R", lb, offset=(0, 0, -2.05))
    a = adult(0, t0, t1, "happy", 0.17)
    a.root.parent = lb
    a.root.location = (0, -0.1, -0.6)
    a.pose(t0 + 0.3, armR=(165, 25))
    noise(lb, "rotation_euler", 0, 0.2, 2.5)
    cam = Cam()
    cam.track(Mo, t0, t1, offset=(2.5, -6.5, 0.4), look_up=2.0, lens=28, fstop=2.8)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "footsteps", 0.5)


# ================================================================== MY DAD
@S(20, 94, 96, "My dad? Whip into the kitchen counter")
def s20(t0, t1):
    kitchen()
    shoebox(BOX_K)
    d = dad_c(t0, t1, "smile")
    d.pose(t0, loc=(BOX_K[0] - 0.3, BOX_K[1] + 0.1, BOX_K[2] + 0.3), rot=-20)
    sit_on(d, t0, (BOX_K[0] - 0.3, BOX_K[1] + 0.1, BOX_K[2] + 0.35), rot=-20, s=S2)
    d.act(t0 + 0.2, "wave")
    tgt = up(BOX_K, 0.8)
    cam = Cam()
    cam.whip(t0, t0 + 0.2, (-8, -8, 6), (-6, 4, 4), orbit_pos(tgt, 3.4, -10, 14), tgt, lens=30)
    cam.key(t1, orbit_pos(tgt, 2.8, -4, 12), tgt, lens=30, focus=tgt, fstop=1.8)
    cam.handheld(0.3)


@S(21, 96, 100, "He lives in a shoebox: little bed, lamp, dad reads")
def s21(t0, t1):
    kitchen()
    shoebox(BOX_K)
    d = dad_c(t0, t1, "happy")
    sit_on(d, t0, (BOX_K[0] - 0.3, BOX_K[1] + 0.1, BOX_K[2] + 0.35), rot=-20, s=S2)
    d.act(t0, "hold")
    pg = box("tinybook", (0.4, 0.05, 0.3), (0, 0, 0), M("#f4f4f4", 0.7), 0.01)
    locs.hand_prop(d, "R", pg, offset=(0, -0.6, -1.9))
    d.look(t0 + 0.8, 25, -10)
    tgt = up(BOX_K, 0.55)
    cam = Cam()
    cam.orbit(t0, t1, tgt, 2.6, -35, 5, pitch=24, lens=30, fstop=1.6)
    cam.handheld(0.25)


@S(22, 100, 105, "On the kitchen counter: pull back to reveal kitchen + kid")
def s22(t0, t1):
    kitchen()
    shoebox(BOX_K)
    d = dad_c(t0, t1, "happy")
    d.pose(t0, loc=(BOX_K[0] - 1.6, BOX_K[1] - 0.6, CTOP), rot=-30)
    d.act(t0 + 0.2, "wave")
    k = kid_c(t0, t1, "happy")
    k.pose(t0, loc=(-1.0, 1.8, 0), rot=facing((-1.0, 1.8), BOX_K))
    tgt = up(BOX_K, 0.5)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 3.0, -10, 10), tgt, lens=30, focus=tgt, fstop=2)
    cam.key(t1, (2.5, -12, 6.5), (1.0, 4, 3.6), lens=24, focus=14.0, fstop=4)
    cam.handheld(0.6)
    sfx(t0 + 0.1, "whoosh", 0.4)


# ================================================================== ASKS in the kitchen
@S(23, 105, 111, "Dad, can I go to Tyler's? Kid leans on the counter")
def s23(t0, t1):
    kitchen()
    k = kitchen_kid(t0, t1, "happy")
    k.act(t0, "lean", expr="happy")
    lips(k, t0, t1)
    d = kitchen_dad(t0, t1, "smile")
    cam = Cam()
    cam_on_kid(cam, t0, t1)


@S(24, 111, 114, "Ask your mom (tiny dad shrugs, shrinks a hair)")
def s24(t0, t1):
    kitchen()
    d = kitchen_dad(t0, t1, "smile")
    ask_mom(d, t0, t1, 0.22, 0.2, loc=DAD_K)
    k = kitchen_kid(t0, t1, "bored")
    cam = Cam()
    cam_on_dad(cam, t0, t1, yaw=-30, yaw1=-45)


@S(25, 114, 118, "Pizza or tacos? Kid holds up a slice and a taco")
def s25(t0, t1):
    kitchen()
    k = kitchen_kid(t0, t1, "grin")
    k.pose(t0, armL=(100, 20), armR=(100, 20))
    pz = empty("pz", (0, 0, 0))
    box("pz_s", (1.0, 1.2, 0.1), (0, 0, 0), M("#f2c14e", 0.6), 0.05, parent=pz, rot=(0, 0, 0))
    for i in range(3):
        sphere(f"pz_p{i}", 0.12, (-0.25 + i * 0.25, -0.1 + (i % 2) * 0.3, 0.07), M("#d0262a", 0.5), (1, 1, 0.4), parent=pz, seg=8)
    locs.hand_prop(k, "L", pz, offset=(0, -0.9, -2.0), rot=(70, 0, 0))
    tc = empty("tc", (0, 0, 0))
    cyl("tc_s", 0.6, 0.35, (0, 0, 0), M("#f2c86a", 0.6), 16, parent=tc, rot=(0, 90, 0))
    box("tc_f", (0.36, 0.9, 0.3), (0, 0, 0.3), M("#63c06a", 0.6), 0.1, parent=tc)
    locs.hand_prop(k, "R", tc, offset=(0, -0.9, -2.0))
    lips(k, t0, t1)
    kitchen_dad(t0, t1, "smile")
    cam = Cam()
    cam_on_kid(cam, t0, t1, 5.2, 4.4, yaw=140, yaw1=125)
    sfx(t0 + 0.1, "pop", 0.4)


@S(26, 118, 121, "Ask your mom (shrug, shrink)")
def s26(t0, t1):
    kitchen()
    d = kitchen_dad(t0, t1, "smile", s=0.2)
    ask_mom(d, t0, t1, 0.2, 0.185, loc=DAD_K)
    kitchen_kid(t0, t1, "bored")
    cam = Cam()
    cam_on_dad(cam, t0, t1, 3.0, 2.3, yaw=-65, yaw1=-50, s=0.19)


@S(27, 121, 128, "Do you like your new shoes? Macro on tiny white sneakers, kid points")
def s27(t0, t1):
    kitchen()
    d = kitchen_dad(t0, t1, "smile", s=0.185)
    d.pose(t0 + 0.5, legR=(25, 0))
    d.pose(t0 + 0.9, legR=(0, 0))
    k = kitchen_kid(t0, t1, "happy")
    k.act(t0, "point", expr="happy")
    lips(k, t0, t1)
    sparkle_on("shoes", up(DAD_K, 0.05), t0 + 0.5, 0.4, 10, seed=8)
    cam = Cam()
    feet = up(DAD_K, 0.15)
    cam.key(t0, orbit_pos(feet, 2.0, -30, 4), feet, lens=36, focus=feet, fstop=1.4)
    cam.key(t1, orbit_pos(up(DAD_K, 0.6), 2.6, -55, 6), up(DAD_K, 0.55), lens=34, focus=feet, fstop=1.6)
    cam.handheld(0.2)
    sfx(t0 + 0.5, "sparkle", 0.5)


@S(28, 128, 131, "Ask your mom (shrink), kid facepalms behind")
def s28(t0, t1):
    kitchen()
    d = kitchen_dad(t0, t1, "smile", s=0.185)
    ask_mom(d, t0, t1, 0.185, 0.17, loc=DAD_K)
    k = kitchen_kid(t0, t1, "bored")
    k.act(t1 - 0.4, "facepalm")
    cam = Cam()
    tgt = up(DAD_K, 0.6)
    cam.push(t0, t1, tgt, 3.6, 2.8, yaw=-25, yaw1=-40, pitch=4, lens=26, fstop=2.6)
    cam.handheld(0.3)


@S(29, 131, 138, "Mom wears him on a necklace: mom walks into the kitchen")
def s29(t0, t1):
    kitchen()
    Mo, d = mom_c(t0, t1, "happy", necklace=True, s_dad=0.17)
    Mo.walk(t0, t1, (-8, -4, 0), (-1, -1.5, 0), rate=2.0)
    cam = Cam()
    cam.track(Mo, t0, t1, offset=(3.5, -8.0, 1.0), look_up=3.4, lens=26, fstop=3)
    cam.handheld(0.7)
    sfx(t0 + 0.1, "footsteps", 0.4)


@S(30, 138, 144, "So she doesn't lose him: necklace close-up, dad dangling and waving")
def s30(t0, t1):
    kitchen()
    Mo, d = mom_c(t0, t1, "smile", necklace=True, s_dad=0.17, dad_expr="grin")
    Mo.pose(t0, loc=(-1, -1.5, 0), rot=-10)
    Mo.look(t0 + 0.5, 0, 25)
    d.pose(t0 + 0.4, armL=(170, 12), armR=(165, 40))
    d.pose(t0 + 0.7, armR=(165, 0))
    d.pose(t0 + 1.0, armR=(165, 40))
    cam = Cam()
    tgt = (-1, -2.1, 2.9)
    cam.push(t0, t1, tgt, 3.6, 2.4, yaw=-20, yaw1=-5, pitch=4, lens=34, fstop=1.6)
    cam.handheld(0.35)
    sfx(t0 + 0.5, "aww", 0.5)


# ================================================================== THE CAR
@S(31, 144, 148, "But one summer day: blazing sun, crane down to the car on the driveway")
def s31(t0, t1):
    driveway()
    car_set()
    heat("hz", (0, -2, 0.5), (14, 10, 6))
    cam = Cam()
    cam.key(t0, (-6, -30, 26), (0, 2, 14), lens=22, focus=40.0, fstop=8)
    cam.key(t1, (-10, -24, 5), (0, 2, 3), lens=22, focus=26.0, fstop=8)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "rise", 0.4)


@S(32, 148, 155, "Baby sister grabs the car keys and giggles")
def s32(t0, t1):
    driveway()
    car_set()
    Si = sis_c(t0, t1, "grin")
    p = (-6, -6, 0)
    Si.pose(t0, loc=p, rot=-20)
    ky = keys_prop("skeys", (0, 0, 0), s=1.2)
    tg = w(151)
    Si.act(tg - 0.2, "reach", expr="grin")
    locs.hand_prop(Si, "R", ky, offset=(0, -0.7, -2.05))
    Si.pose(tg + 0.2, armR=(160, 20))
    Si.face(tg + 0.2, "joy")
    noise(ky, "rotation_euler", 0, 0.5, 6)
    cam = Cam()
    cam.push(t0, t1, head(p, 0.62), 5.0, 3.6, yaw=-25, pitch=8, lens=28, yaw1=-5, fstop=2)
    cam.crash(tg + 0.2, 28, 34, 0.1)
    cam.handheld(0.8)
    sfx(tg + 0.2, "clink", 0.9)
    sfx(tg + 0.5, "kids_laugh", 0.35)


@S(33, 155, 159, "Climbed into the car: sister hops into the driver seat, door swings shut")
def s33(t0, t1):
    driveway()
    cs = car_set(door_open=True)
    door = cs["door"]
    door.keyframe_insert("rotation_euler", frame=F(t0 + 0.6))
    door.rotation_euler = (0, 0, 0)
    door.keyframe_insert("rotation_euler", frame=F(t1 - 0.05))
    Si = sis_c(t0, t1, "grin")
    Si.pose(t0, loc=(-2.2, -5.5, 0), rot=150)
    Si.pose(t0 + 0.35, loc=(-1.9, -2.6, 1.6))
    sit_on(Si, t0 + 0.7, SEAT, rot=180, s=0.62)
    cam = Cam()
    cam.push(t0, t1, (-1.5, -1, 3.2), 14, 11, yaw=-30, pitch=8, lens=24, yaw1=-15, fstop=5)
    cam.handheld(0.9)
    sfx(t1 - 0.1, "door", 0.8)


@S(34, 159, 161, "Click! Lock pin drops: crash zoom")
def s34(t0, t1):
    driveway()
    cs = car_set()
    pin = cs["pin"]
    tc = w(160)
    pin.keyframe_insert("location", frame=F(tc - 0.03))
    pin.location[2] -= 0.35
    pin.keyframe_insert("location", frame=F(tc + 0.04))
    Si = sis_c(t0, t1, "grin")
    sit_on(Si, t0, SEAT, rot=180, s=0.62)
    Si.act(t0, "reach", expr="grin")
    tgt = (0.0, -1.4, 3.95)
    cam = Cam()
    tgt = (-0.8, -1.5, 4.2)
    cam.key(t0, orbit_pos(tgt, 4.6, -12, 6), tgt, lens=26, focus=tgt, fstop=2.4)
    cam.key(t1, orbit_pos(tgt, 3.6, 0, 6), tgt, lens=28, focus=tgt, fstop=2.4)
    cam.crash(tc, 30, 42, 0.08)
    cam.handheld(0.6)
    sfx(tc, "click", 1.0)


@S(35, 161, 165, "She locked herself in: sister giggles behind the glass, kid gasps outside")
def s35(t0, t1):
    driveway()
    car_set()
    Si = sis_c(t0, t1, "joy")
    sit_on(Si, t0, SEAT, rot=150, s=0.62)
    laugh(Si, t0, t1, rate=6)
    k = kid_c(t0, t1, "shock")
    p = (-3.0, -6.0, 0)
    k.pose(t0, loc=p, rot=facing(p, (-1.6, 0.4)))
    k.act(t0 + 0.3, "hands_head", expr="terror")
    cam = Cam()
    cam.push(t0, t1, (-2.0, -2.0, 4.2), 8, 6.5, yaw=-60, pitch=4, lens=24, yaw1=-48, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "gasp", 0.7)


@S(36, 165, 167, "Engine off: dark dashboard, key icon")
def s36(t0, t1):
    driveway()
    car_set()
    Si = sis_c(t0, t1, "happy")
    sit_on(Si, t0, SEAT, rot=180, s=0.62)
    tgt = (-3.0, 1.0, 4.4)
    cam = Cam()
    cam.key(t0, (-15, -1.0, 5.5), tgt, lens=26, focus=tgt, fstop=3)
    cam.key(t1, (-13, 0.5, 5.2), tgt, lens=28, focus=tgt, fstop=3)
    cam.handheld(0.5)
    pop_text("off", "ENGINE OFF", (-9.0, 0.3, 5.7), t0 + 0.1, 0.32, "#ff5a5a", yaw=-90)
    sfx(t0 + 0.1, "thud", 0.5)


@S(37, 167, 169, "Windows up: the glass rises to a sliver")
def s37(t0, t1):
    driveway()
    car_set(pane_up=(t0, t0 + 0.6))
    Si = sis_c(t0, t1, "happy")
    sit_on(Si, t0, SEAT, rot=150, s=0.62)
    tgt = (-1.85, -1.75, 5.2)
    cam = Cam()
    cam.push(t0, t1, tgt, 6.0, 4.6, yaw=-12, pitch=2, lens=26, fstop=2.6)
    cam.handheld(0.6)
    sfx(t0 + 0.05, "window", 0.7)


@S(38, 169, 175, "A hundred degrees: thermometer shoots up to 100, heat waves")
def s38(t0, t1):
    driveway()
    car_set()
    heat("hz2", (-6, -6, 0.5), (6, 4, 6), seed=2)
    thermometer((-8, -8, 0), w(172))
    pop_text("deg", "100°", (-7.2, -8.4, 6.6), w(173), 0.9, "#ff5a3a", yaw=-15)
    cam = Cam()
    cam.push(t0, t1, (-7.5, -8, 4), 10, 7, yaw=-18, pitch=6, lens=26, yaw1=-6, fstop=3)
    cam.handheld(1.0)
    sfx(w(172), "rise", 0.6)
    sfx(w(173), "boom", 0.4)


@S(39, 175, 179, "Mom was at work: typing, phone face-down")
def s39(t0, t1):
    office()
    Mo, _ = mom_c(t0, t1, "bored")
    Mo.pose(t0, loc=(0, 0.6, 0), rot=0, legL=(85, 3), legR=(85, -3), hipz=-1.1)
    box("of_chair", (2.4, 2.4, 0.3), (0, 0.9, 1.0), M("#2a2a32", 0.6), 0.1)
    Mo.pose(t0, armL=(75, -10), armR=(75, -10))
    noise(Mo.shL, "rotation_euler", 0, 0.12, 10)
    noise(Mo.shR, "rotation_euler", 0, 0.12, 11)
    cam = Cam()
    cam.orbit(t0, t1, (0, 1.5, 3.4), 9, -30, -10, pitch=8, lens=26, fstop=3.5)
    cam.handheld(0.6)
    sfx(t0 + 0.1, "click", 0.4)


@S(40, 179, 185, "The only opening: slow push toward the top of the window")
def s40(t0, t1):
    driveway()
    car_set()
    Si = sis_c(t0, t1, "worried")
    sit_on(Si, t0, SEAT, rot=150, s=0.62)
    Si.face(t0 + 0.6, "cry")
    tgt = (-1.85, -1.75, 5.5)
    cam = Cam()
    cam.push(t0, t1, tgt, 8, 4.5, yaw=-5, pitch=6, lens=26, fstop=2.8)
    cam.handheld(0.7)


@S(41, 185, 192, "A tiny gap at the top of the window: macro on the sliver")
def s41(t0, t1):
    driveway()
    car_set()
    Si = sis_c(t0, t1, "cry")
    sit_on(Si, t0, SEAT, rot=150, s=0.62)
    tgt = (-1.85, -1.75, GAP_Z + 0.25)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 2.2, -40, 6), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.key(t1, orbit_pos(tgt, 1.6, -18, 4), tgt, lens=32, focus=tgt, fstop=1.6)
    cam.handheld(0.3)
    sfx(t0 + 0.2, "wind", 0.3)


@S(42, 192, 194, "One inch: 1 INCH pops beside the gap")
def s42(t0, t1):
    driveway()
    car_set()
    tgt = (-1.85, -1.75, GAP_Z + 0.25)
    Mr = emitm("#ffe14a", 3)
    for z in (GAP_Z + 0.02, GAP_Z + 0.44):
        box(f"gapl{z}", (0.9, 0.04, 0.04), (-2.6, -1.9, z), Mr, 0.0)
    pop_text("inch1", "1 INCH", (-2.8, -2.0, GAP_Z - 0.45), t0 + 0.05, 0.2, "#ffe14a")
    cam = Cam()
    cam.key(t0, orbit_pos((-2.7, -1.75, GAP_Z), 3.2, -8, 4), (-2.7, -1.75, GAP_Z), lens=30,
            focus=tgt, fstop=2)
    cam.key(t1, orbit_pos((-2.7, -1.75, GAP_Z), 2.8, 4, 4), (-2.7, -1.75, GAP_Z), lens=32,
            focus=tgt, fstop=2)
    cam.crash(t0 + 0.05, 30, 36, 0.08)
    cam.handheld(0.3)
    sfx(t0 + 0.05, "ding", 0.6)


@S(43, 194, 200, "Dad ran up the door handle: tiny dad sprints and climbs")
def s43(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "determined", s=S2)
    hp = (HANDLE[0], HANDLE[1] - 0.1, HANDLE[2] + 0.14)
    d.walk(t0, t0 + 0.6, (hp[0] - 1.6, hp[1] - 0.1, hp[2] - 0.4), (hp[0] - 0.5, hp[1], hp[2] - 0.2), rate=5, swing=48,
           arm=55, bob=0.3)
    d.pose(t0 + 0.75, loc=(hp[0] - 0.3, hp[1], hp[2] + 0.02), armL=(160, 10), armR=(160, 10), legL=(60, 0))
    d.pose(t0 + 1.05, loc=hp, armL=(20, 10), armR=(20, 10), legL=(0, 0), rot=0)
    d.act(t0 + 1.2, "fists", expr="determined")
    tgt = (hp[0] - 0.4, hp[1], hp[2] + 0.5)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 2.6, -40, 6), tgt, lens=30, focus=tgt, fstop=1.8)
    cam.key(t1, orbit_pos(tgt, 2.2, -5, 12), tgt, lens=32, focus=tgt, fstop=1.8)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "footsteps", 0.5)


@S(44, 200, 204, "He was too big: dad stuck at the gap, legs kicking")
def s44(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "terror", s=S2)
    gp = (-2.0, -1.95, GAP_Z - 0.1)
    d.pose(t0, loc=(gp[0], gp[1] - 0.35, gp[2] - 0.6), rot=180, torso=(0, 70, 0), head=(0, 10, 0), armL=(170, 10),
           armR=(170, 10))
    noise(d.hpL, "rotation_euler", 0, 0.6, 4)
    noise(d.hpR, "rotation_euler", 0, 0.6, 4)
    noise(d.root, "location", 0, 0.03, 8)
    tgt = (gp[0], gp[1], gp[2] - 0.2)
    cam = Cam()
    cam.push(t0, t1, tgt, 2.6, 2.0, yaw=-30, pitch=-6, lens=30, yaw1=-12, fstop=1.8)
    cam.handheld(0.35)
    sfx(t0 + 0.2, "bonk", 0.5)
    sfx(t0 + 0.6, "thud", 0.4)


@S(45, 204, 207, "Two whole inches: 2 INCHES label next to dad on the handle")
def s45(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "worried", s=S2)
    hp = (HANDLE[0], HANDLE[1] - 0.1, HANDLE[2] + 0.14)
    d.pose(t0, loc=hp, rot=-15)
    d.act(t0 + 0.2, "shrug", expr="worried")
    Mr = emitm("#ff5a5a", 3)
    for z in (hp[2], hp[2] + 1.06):
        box(f"dl{z}", (0.5, 0.04, 0.04), (hp[0] + 0.55, hp[1] - 0.05, z), Mr, 0.0)
    pop_text("inch2", "2 INCHES", (hp[0] + 0.3, hp[1] - 0.1, hp[2] + 1.25), t0 + 0.1, 0.14, "#ff5a5a")
    tgt = (hp[0] + 0.4, hp[1], hp[2] + 0.55)
    cam = Cam()
    cam.push(t0, t1, tgt, 2.8, 2.3, yaw=-8, pitch=2, lens=32, fstop=2)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "buzzer", 0.5)


# ================================================================== THE PLAN
@S(46, 207, 211, "Then I noticed something: kid close-up, eyes go wide, crash zoom")
def s46(t0, t1):
    driveway()
    car_set()
    k = kid_c(t0, t1, "worried")
    k.pose(t0, loc=KID_D, rot=facing(KID_D, HANDLE))
    tn = w(209)
    k.face(tn, "gasp")
    k.act(tn, "think", expr="gasp")
    sparkle_on("idea", head(KID_D), tn, 1.4, 12, seed=11)
    cam = Cam()
    cam.push(t0, t1, head(KID_D), 6, 4.2, yaw=115, yaw1=135, pitch=2, lens=28, fstop=2.4)
    cam.crash(tn, 28, 38, 0.1)
    cam.handheld(0.8)
    sfx(tn, "ding", 0.8)


@S(47, 211, 216, "If he couldn't shrink himself: OTS kid looks at tiny dad on the handle")
def s47(t0, t1):
    driveway()
    car_set()
    k = kid_c(t0, t1, "sus")
    kp = (-3.0, -5.0, 0)
    k.pose(t0, loc=kp, rot=facing(kp, HANDLE))
    d = dad_c(t0, t1, "worried", s=S2)
    hp = (HANDLE[0], HANDLE[1] - 0.1, HANDLE[2] + 0.14)
    d.pose(t0, loc=hp, rot=facing(hp, kp))
    tgt = (hp[0], hp[1], hp[2] + 0.5)
    cam = Cam()
    cam.key(t0, (-1.8, -5.8, 5.4), tgt, lens=34, focus=tgt, fstop=2)
    cam.key(t1, (-1.6, -5.3, 5.1), tgt, lens=38, focus=tgt, fstop=2)
    cam.handheld(0.5)


@S(48, 216, 220, "I could make him: kid smirks, rubs hands")
def s48(t0, t1):
    driveway()
    car_set()
    k = kid_c(t0, t1, "smug")
    kp = (-3.0, -5.0, 0)
    k.pose(t0, loc=kp, rot=facing(kp, HANDLE) - 20)
    k.pose(t0, armL=(70, -30), armR=(70, -30))
    noise(k.shL, "rotation_euler", 2, 0.3, 6)
    k.face(t0 + 0.5, "wink")
    cam = Cam()
    cam.push(t0, t1, head(kp), 5.0, 3.8, yaw=140, pitch=-4, lens=30, yaw1=120, fstop=2.2)
    cam.handheld(0.6)
    sfx(t0 + 0.5, "sparkle", 0.4)


def handle_dad(t0, t1, s0, s1, expr="smile"):
    d = dad_c(t0, t1, expr, s=s0)
    hp = (HANDLE[0], HANDLE[1] - 0.1, HANDLE[2] + 0.14)
    d.pose(t0, loc=hp, rot=facing(hp, (-3.0, -5.0)))
    ask_mom(d, t0, t1, s0, s1, loc=hp)
    tgt = (hp[0], hp[1], hp[2] + 3.6 * s0)
    return d, tgt


@S(49, 220, 226, "Dad, can I get a tattoo? Kid flashes a skull sticker on his arm")
def s49(t0, t1):
    driveway()
    car_set()
    k = kid_c(t0, t1, "grin")
    kp = (-3.0, -5.0, 0)
    k.pose(t0, loc=kp, rot=facing(kp, HANDLE))
    k.pose(t0 + 0.2, armR=(95, 40))
    lips(k, t0, t1)
    tt = box("tattoo", (0.06, 0.6, 0.6), (-0.62, 0, -1.1), M("#2a2a3a", 0.5), 0.05, parent=k.shR, coll=k.coll)
    sphere("tattoo_h", 0.2, (-0.66, 0, -1.05), emitm("#ff3a3a", 1), parent=k.shR, coll=k.coll, seg=10)
    cam = Cam()
    cam.push(t0, t1, (kp[0] - 0.3, kp[1], 4.0), 6.0, 4.6, yaw=165, pitch=4, lens=28, yaw1=140, fstop=2.4)
    cam.handheld(0.7)


@S(50, 226, 229, "Ask your mom: shrink")
def s50(t0, t1):
    driveway()
    car_set()
    d, tgt = handle_dad(t0, t1, 0.2, 0.15)
    cam = Cam()
    cam.push(t0, t1, tgt, 2.4, 1.8, yaw=-30, yaw1=-15, pitch=6, lens=32, fstop=1.6)
    cam.handheld(0.25)


@S(51, 229, 234, "Can I drive the car? Kid mimes steering, vroom")
def s51(t0, t1):
    driveway()
    car_set()
    k = kid_c(t0, t1, "grin")
    kp = (-3.0, -5.0, 0)
    k.pose(t0, loc=kp, rot=facing(kp, HANDLE) + 20)
    k.pose(t0 + 0.1, armL=(85, 15), armR=(85, 15))
    noise(k.hip, "rotation_euler", 1, 0.25, 4)
    lips(k, t0, t1)
    cam = Cam()
    cam.orbit(t0, t1, head(kp), 5.2, 175, 125, pitch=0, lens=28, fstop=2.4)
    cam.handheld(0.8)


@S(52, 234, 237, "Ask your mom: shrink again")
def s52(t0, t1):
    driveway()
    car_set()
    d, tgt = handle_dad(t0, t1, 0.15, 0.11)
    cam = Cam()
    cam.push(t0, t1, tgt, 1.9, 1.4, yaw=15, yaw1=0, pitch=6, lens=32, fstop=1.4)
    cam.handheld(0.2)


@S(53, 237, 242, "Can I adopt a horse? A horse is standing right there")
def s53(t0, t1):
    driveway()
    car_set()
    k = kid_c(t0, t1, "grin")
    kp = (-3.0, -5.0, 0)
    k.pose(t0, loc=kp, rot=-15)
    k.act(t0 + 0.3, "point", expr="grin")
    lips(k, t0, t1)
    horse("horse", (-10, -7, 0), rot=-70)
    cam = Cam()
    cam.push(t0, t1, (-6.5, -6, 4.2), 14, 11, yaw=-12, pitch=6, lens=24, yaw1=4, fstop=5)
    cam.handheld(0.9)
    sfx(t0 + 0.4, "boing", 0.5)


@S(54, 242, 245, "Ask your mom: big shrink, poof")
def s54(t0, t1):
    driveway()
    car_set()
    d, tgt = handle_dad(t0, t1, 0.11, SP)
    W2.poof("bigp", (HANDLE[0], HANDLE[1] - 0.2, HANDLE[2] + 0.3), t1 - 0.25, 0.25, n=5)
    cam = Cam()
    cam.push(t0, t1, tgt, 1.5, 1.1, yaw=-10, yaw1=5, pitch=6, lens=34, fstop=1.4)
    cam.crash(t1 - 0.2, 34, 40, 0.08)
    cam.handheld(0.15)


@S(55, 245, 252, "Size of a peanut: dad next to a peanut on the handle")
def s55(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "grin", s=SP)
    hp = (HANDLE[0] - 0.1, HANDLE[1] - 0.1, HANDLE[2] + 0.14)
    d.pose(t0, loc=hp, rot=-20)
    d.act(t0 + 0.3, "point_l", expr="grin")
    peanut("pnut", (hp[0] + 0.28, hp[1], hp[2]), s=0.7, rot=20)
    pop_text("pn", "PEANUT SIZE", (hp[0] + 0.05, hp[1] - 0.2, hp[2] + 0.55), w(251), 0.08, "#ffe14a")
    tgt = (hp[0] + 0.12, hp[1], hp[2] + 0.18)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.2, -30, 8), tgt, lens=34, focus=tgt, fstop=1.4)
    cam.key(t1, orbit_pos(tgt, 0.9, 10, 10), tgt, lens=36, focus=tgt, fstop=1.4)
    cam.handheld(0.12)
    sfx(w(251), "pop", 0.6)


# ================================================================== THE RESCUE
@S(56, 252, 257, "Squeezed through the gap: tiny dad wriggles over the glass edge")
def s56(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "determined", s=SP)
    gx = -2.2
    d.pose(t0, loc=(gx, -1.95, GAP_Z - 0.05), rot=180, torso=(0, 60, 0), armL=(170, 10), armR=(170, 10))
    d.pose(t0 + 0.7, loc=(gx, -1.6, GAP_Z + 0.08), rot=180, torso=(0, 85, 0))
    d.pose(t0 + 1.2, loc=(gx, -1.4, GAP_Z - 0.2), rot=180, torso=(0, 30, 0), legL=(-30, 0), legR=(-30, 0))
    noise(d.hpL, "rotation_euler", 0, 0.5, 5)
    tgt = (gx, -1.75, GAP_Z + 0.05)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.3, -35, 12), tgt, lens=34, focus=tgt, fstop=1.4)
    cam.key(t1, orbit_pos(tgt, 1.0, -10, 22), tgt, lens=36, focus=tgt, fstop=1.4)
    cam.handheld(0.12)
    sfx(t0 + 0.4, "rip", 0.3)
    sfx(t0 + 1.0, "pop", 0.5)


@S(57, 257, 261, "Slid down the seat: wheee down the seat back")
def s57(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "joy", s=SP)
    p0 = (-0.05, -0.4, 5.2)
    p1 = (-1.6, -0.4, 3.12)
    d.pose(t0, loc=p0, rot=90, legL=(80, 0), legR=(80, 0), armL=(160, 30), armR=(160, 30), torso=(0, -30, 0))
    d.pose(t1 - 0.2, loc=p1, rot=90)
    set_interp(d.root, "location", F(t0), "BEZIER", "EASE_IN")
    Si = sis_c(t0, t1, "gasp")
    sit_on(Si, t0, (SEAT[0], SEAT[1] + 0.8, SEAT[2]), rot=150, s=0.62)
    cam = Cam()
    cam.key(t0, (-2.7, -0.9, 5.2), p0, lens=28, focus=p0, fstop=1.8)
    cam.key(t1, (-2.7, -0.9, 4.0), p1, lens=28, focus=p1, fstop=1.8)
    cam.handheld(0.2)
    sfx(t0 + 0.1, "whoosh", 0.6)


@S(58, 261, 265, "Ran across the keys: tiny dad sprints over the key ring")
def s58(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "determined", s=SP)
    k = KEYS
    d.walk(t0, t1, (k[0] - 0.9, k[1] + 0.5, k[2] + 0.05), (k[0] + 0.6, k[1] - 1.8, k[2] + 0.05), rate=6, swing=50,
           arm=60, bob=0.3)
    tgt = (k[0], k[1] - 0.6, k[2] + 0.2)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.6, -40, 14), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.key(t1, orbit_pos(tgt, 1.3, -10, 10), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.handheld(0.15)
    sfx(t0 + 0.3, "clink", 0.7)


@S(59, 265, 270, "And jumped: big leap toward the glowing button")
def s59(t0, t1):
    driveway()
    car_set()
    d = dad_c(t0, t1, "shout", s=SP)
    b = BUTTON
    p0 = (b[0] + 0.5, b[1] + 0.9, 3.25)
    top = (b[0] + 0.25, b[1] + 0.45, b[2] + 0.6)
    d.pose(t0, loc=p0, rot=180, hipz=-0.4)
    d.pose(t0 + 0.25, hipz=0.0)
    d.pose(t0 + 0.7, loc=top, armL=(170, 30), armR=(170, 30), legL=(40, 0), legR=(-30, 0))
    lt = light("btn_glow", "POINT", (b[0], b[1] + 0.3, b[2] + 0.4), 30, (1.0, 0.3, 0.3), 0.2)
    tgt = (b[0] + 0.25, b[1] + 0.5, b[2] + 0.3)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.6, 160, 4), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.key(t1, orbit_pos(tgt, 1.2, 135, -6), tgt, lens=32, focus=tgt, fstop=1.6)
    cam.handheld(0.15)
    sfx(t0 + 0.2, "boing", 0.6)


@S(60, 270, 274, "With both feet: lands on UNLOCK, button clicks, flash")
def s60(t0, t1):
    driveway()
    cs = car_set()
    btn = cs["btn"]
    d = dad_c(t0, t1, "shout", s=SP)
    b = BUTTON
    tl = t0 + 0.25
    d.pose(t0, loc=(b[0] + 0.1, b[1] + 0.2, b[2] + 0.4), rot=180, armL=(170, 30), armR=(170, 30), legL=(30, 0), legR=(30, 0))
    d.pose(tl, loc=(b[0], b[1], b[2] + 0.11), hipz=-0.4, armL=(60, 40), armR=(60, 40), legL=(0, 0), legR=(0, 0))
    d.pose(tl + 0.2, hipz=0.0, armL=(170, 30), armR=(170, 30))
    d.face(tl + 0.2, "joy")
    btn.keyframe_insert("location", frame=F(tl - 0.03))
    btn.location[2] -= 0.08
    btn.keyframe_insert("location", frame=F(tl + 0.03))
    lt = light("btn_flash", "POINT", (b[0], b[1] + 0.3, b[2] + 0.4), 0, (1.0, 0.4, 0.4), 0.3)
    lt.data.keyframe_insert("energy", frame=F(tl - 0.02))
    lt.data.energy = 400; lt.data.keyframe_insert("energy", frame=F(tl + 0.03))
    lt.data.energy = 0; lt.data.keyframe_insert("energy", frame=F(tl + 0.4))
    pop_text("unl", "UNLOCK!", (b[0] + 0.05, b[1] + 0.35, b[2] + 0.7), tl + 0.05, 0.14, "#63e07a", yaw=180)
    tgt = (b[0], b[1] + 0.1, b[2] + 0.2)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.2, 160, 22), tgt, lens=32, focus=tgt, fstop=1.6)
    cam.key(t1, orbit_pos(tgt, 1.0, 175, 30), tgt, lens=32, focus=tgt, fstop=1.6)
    cam.crash(tl, 32, 44, 0.08)
    cam.handheld(0.15)
    sfx(tl, "click", 1.0)
    sfx(tl + 0.05, "stomp", 0.5)


@S(61, 274, 278, "The door swung open: wide, door flies open, cool air")
def s61(t0, t1):
    driveway()
    cs = car_set(open_t=w(276))
    Si = sis_c(t0, t1, "cry")
    sit_on(Si, t0, SEAT, rot=150, s=0.62)
    Si.face(w(276) + 0.3, "joy")
    k = kid_c(t0, t1, "shock")
    kp = (-6.5, -6.5, 0)
    k.pose(t0, loc=kp, rot=facing(kp, SEAT))
    k.act(w(276) + 0.2, "cheer", expr="joy")
    cam = Cam()
    cam.push(t0, t1, (-2.5, -2.5, 3.6), 15, 12, yaw=-35, pitch=10, lens=22, yaw1=-20, fstop=5)
    cam.handheld(1.0)
    sfx(w(276), "door", 0.9)
    sfx(w(276) + 0.2, "whoosh", 0.5)


@S(62, 278, 282, "My sister was safe: kid hugs sister, tiny dad cheers on kid's shoulder")
def s62(t0, t1):
    driveway()
    car_set(door_open=True)
    k = kid_c(t0, t1, "joy")
    kp = (-4.5, -6.0, 0)
    k.pose(t0, loc=kp, rot=-15, armL=(75, -30), armR=(75, -30))
    Si = sis_c(t0, t1, "joy")
    Si.root.parent = k.torso
    Si.root.location = (0, -0.9, -1.8)
    Si.pose(t0, armL=(80, -40), armR=(80, -40))
    d = dad_c(t0, t1, "joy", s=SP)
    d.root.parent = k.torso
    d.root.location = (1.1, -0.1, 1.02)
    d.act(t0 + 0.3, "cheer", expr="joy")
    confetti("saf", (kp[0], kp[1], 9), (4, 3, 2), t0 + 0.3, 1.4, 40, seed=6, fall=8)
    cam = Cam()
    cam.orbit(t0, t1, head(kp, 0.85), 6.5, -25, 15, pitch=2, lens=26, fstop=2.6)
    cam.handheld(0.7)
    sfx(t0 + 0.25, "cheer", 0.6)
    sfx(t0 + 0.3, "confetti", 0.5)


# ================================================================== THAT NIGHT
@S(63, 282, 286, "That night: warm kitchen, push in on the dinner table")
def s63(t0, t1):
    kitchen(night=True, door=True)
    k = kid_c(t0, t1, "happy")
    sit_on(k, t0, (1, -8.2, 2.0), rot=180, s=1.0)
    box("chair_k", (2.2, 2.2, 0.25), (1, -8.2, 1.9), M("#704a2a"), 0.05)
    d = dad_c(t0, t1, "determined", s=SP)
    d.pose(t0, loc=(1.6, -3.2, 0.0), rot=180)
    cam = Cam()
    cam.key(t0, (-9, 6, 9), (1, -5, 2.5), lens=22, focus=14.0, fstop=4)
    cam.key(t1, (-6, 2, 6.5), (1, -5, 2.8), lens=22, focus=10.0, fstop=4)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "crickets", 0.3)


@S(64, 286, 290, "Climbed onto the table: tiny dad hauls himself up over the edge")
def s64(t0, t1):
    kitchen(night=True)
    d = dad_c(t0, t1, "determined", s=SP)
    e = (1.6, -2.55, TABLE_Z)
    d.pose(t0, loc=(e[0], e[1] + 0.12, e[2] - 0.33), rot=0, armL=(170, 5), armR=(170, 5), legL=(20, 0))
    d.pose(t0 + 0.6, loc=(e[0], e[1] + 0.05, e[2] - 0.15), armL=(150, 5), armR=(150, 5), legL=(70, 0))
    d.pose(t0 + 1.0, loc=(e[0], e[1] - 0.15, e[2]), armL=(10, 10), armR=(10, 10), legL=(0, 0))
    d.act(t0 + 1.1, "fists", expr="determined")
    tgt = (e[0], e[1], e[2] + 0.1)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.3, -20, 14), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.key(t1, orbit_pos(tgt, 1.1, 10, 8), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.handheld(0.15)
    sfx(t0 + 1.0, "thud", 0.4)


def table_dad(t0, t1, expr="determined", s=SP):
    d = dad_c(t0, t1, expr, s=s)
    p = (1.0, -6.6, TABLE_Z)
    d.pose(t0, loc=p, rot=0)
    return d, p


def table_kid(t0, t1, expr="gasp"):
    k = kid_c(t0, t1, expr)
    sit_on(k, t0, (1, -9.0, 2.0), rot=180, s=1.0)
    k.pose(t0, torso=(0, 18, 0))
    box("chair_t", (2.2, 2.2, 0.25), (1, -9.0, 1.9), M("#704a2a"), 0.05)
    return k


@S(65, 290, 297, "Looked me in the eye: kid's huge face behind, tiny dad stares up")
def s65(t0, t1):
    kitchen(night=True)
    d, p = table_dad(t0, t1, "determined")
    d.look(t0 + 0.2, 0, -30)
    table_kid(t0, t1, "gasp")
    tgt = (p[0], p[1], p[2] + 0.2)
    cam = Cam()
    cam.key(t0, (p[0] + 0.3, p[1] + 1.4, p[2] + 0.25), (p[0], p[1] - 2.0, p[2] + 1.0), lens=24, focus=tgt, fstop=2.0)
    cam.key(t1, (p[0] + 0.1, p[1] + 1.0, p[2] + 0.2), (p[0], p[1] - 2.0, p[2] + 1.2), lens=26, focus=tgt, fstop=2.0)
    cam.handheld(0.2)
    sfx(w(294), "whoosh", 0.3)


@S(66, 297, 301, "PIZZA. Dad points, shouting, grows a bit")
def s66(t0, t1):
    kitchen(night=True)
    d, p = table_dad(t0, t1, "shout")
    d.act(t0, "point", expr="shout")
    lips(d, t0, t1, "shout")
    resize(d, w(299), SP, 0.1, loc=p)
    pop_text("pzz", "PIZZA!", (p[0] + 0.05, p[1] + 0.2, p[2] + 0.75), t0 + 0.05, 0.14, "#ffb03a", yaw=0)
    tgt = (p[0], p[1], p[2] + 0.3)
    cam = Cam()
    cam.key(t0, orbit_pos(tgt, 1.4, -15, 4), tgt, lens=30, focus=tgt, fstop=1.6)
    cam.key(t1, orbit_pos(tgt, 1.8, -5, 8), (p[0], p[1], p[2] + 0.4), lens=30, focus=tgt, fstop=1.6)
    cam.crash(t0 + 0.05, 30, 38, 0.1)
    cam.handheld(0.2)


@S(67, 301, 308, "Bed at nine: dad points at the clock, kid gasps")
def s67(t0, t1):
    kitchen(night=True)
    clock9((-15.6, 0.0, 9.0), yaw=90)
    d, p = table_dad(t0, t1, "determined", s=0.1)
    d.act(t0, "point", expr="determined")
    lips(d, t0, t1, "shout")
    resize(d, w(305), 0.1, 0.13, loc=p)
    k = table_kid(t0, t1, "shock")
    k.act(w(305), "hands_head", expr="terror")
    cam = Cam()
    cam.key(t0, (3.5, -2.0, 4.6), (-15.6, 0, 9.0), lens=26, focus=19.0, fstop=3)
    cam.key(w(305), (3.5, -2.0, 4.6), (-15.6, 0, 9.0), lens=30, focus=12.0, fstop=3)
    cam.key(t1, (3.8, -4.0, 4.4), (1, -9, 4.4), lens=28, focus=6.0, fstop=2.4)
    cam.handheld(0.6)
    sfx(w(305), "ding", 0.6)


@S(68, 308, 311, "And these shoes? Dad looks down at his sneakers")
def s68(t0, t1):
    kitchen(night=True)
    d, p = table_dad(t0, t1, "confused", s=0.13)
    d.look(t0 + 0.1, 0, 35)
    d.pose(t0 + 0.4, legR=(30, 0))
    lips(d, t0, t1)
    feet = (p[0], p[1], p[2] + 0.06)
    cam = Cam()
    cam.key(t0, orbit_pos(feet, 1.2, -20, 10), feet, lens=34, focus=feet, fstop=1.4)
    cam.key(t1, orbit_pos((p[0], p[1], p[2] + 0.4), 1.6, -5, 4), (p[0], p[1], p[2] + 0.4), lens=32, focus=feet, fstop=1.4)
    cam.handheld(0.15)


@S(69, 311, 315, "I love these shoes! Dad jumps, cheering, grows")
def s69(t0, t1):
    kitchen(night=True)
    d, p = table_dad(t0, t1, "joy", s=0.13)
    d.act(t0, "cheer", expr="joy")
    lips(d, t0, t1, "laugh")
    d.jump(t0 + 0.2, 0.15, 0.4, loc=p)
    resize(d, w(314), 0.13, 0.2, loc=p)
    sparkle_on("love", (p[0], p[1], p[2] + 0.6), t0 + 0.3, 0.5, 12, seed=13, col="#ff9ad0")
    tgt = (p[0], p[1], p[2] + 0.45)
    cam = Cam()
    cam.orbit(t0, t1, tgt, 2.0, -30, 20, pitch=-6, lens=30, fstop=1.6)
    cam.handheld(0.2)
    sfx(t0 + 0.2, "boing", 0.5)


@S(70, 315, 321, "He grew back taller than ever: on the floor, scale up with a glow")
def s70(t0, t1):
    kitchen(night=True, door=True)
    p = (6.0, -7.0, 0)
    d = dad_c(t0, t1, "joy", s=0.2)
    d.pose(t0, loc=p, rot=-20)
    tg = w(316)
    resize(d, tg, 0.2, SBIG, dur=1.0, loc=p)
    d.act(tg + 0.6, "cheer", expr="joy")
    lt = light("grow_glow", "POINT", (p[0], p[1] - 2, 3), 0, (1.0, 0.9, 0.6), 2)
    lt.data.keyframe_insert("energy", frame=F(tg))
    lt.data.energy = 3000; lt.data.keyframe_insert("energy", frame=F(tg + 0.5))
    lt.data.energy = 0; lt.data.keyframe_insert("energy", frame=F(tg + 1.4))
    sparkle_on("grw", (p[0], p[1], 3), tg + 0.4, 3.0, 20, seed=14)
    cam = Cam()
    cam.key(t0, (p[0] - 3, p[1] - 9, 1.2), (p[0], p[1], 0.8), lens=24, focus=9.0, fstop=3)
    cam.key(t1, (p[0] - 4, p[1] - 12, 2.0), (p[0], p[1], 5.5), lens=24, focus=12.0, fstop=3)
    cam.handheld(1.0)


@S(71, 321, 324, "Six foot three: height marks on the wall")
def s71(t0, t1):
    kitchen(night=True)
    p = (-8.0, 3.4, 0)
    d = dad_c(t0, t1, "smug", s=SBIG)
    d.pose(t0, loc=p, rot=0)
    d.act(t0, "cross", expr="smug")
    Ml = M("#2a2a3a", 0.6)
    box("hm_board", (2.4, 0.12, 9.0), (-5.6, 4.6, 4.5), M("#ffffff", 0.6), 0.05)
    for i in range(8):
        box(f"hm{i}", (1.2, 0.05, 0.05), (-5.6, 4.52, 1 + i), Ml, 0.0)
    htop = 5.3 * SBIG
    box("hm_top", (2.6, 0.05, 0.1), (-5.6, 4.5, htop), emitm("#ff5a5a", 2), 0.0)
    pop_text("63", "6'3\"", (-4.2, 4.3, htop + 0.3), t0 + 0.1, 0.8, "#ffe14a")
    cam = Cam()
    cam.key(t0, (-7, -6, 2.0), (-7, 4, 3.0), lens=24, focus=10.0, fstop=3.5)
    cam.key(t1, (-6.5, -7, 3.5), (-7, 4, 6.0), lens=24, focus=11.0, fstop=3.5)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "rimshot", 0.5)


@S(72, 324, 332, "Had to duck under the door frame")
def s72(t0, t1):
    kitchen(night=True, door=True)
    d = dad_c(t0, t1, "happy", s=SBIG)
    p0, p1 = (DOOR_X, -0.5, 0), (DOOR_X, -6.5, 0)
    d.walk(t0, t1, p0, p1, rate=1.8)
    td = t0 + 0.5
    d.pose(td - 0.3, torso=(0, 0, 0), head=(0, 0, 0))
    d.pose(td, torso=(0, 38, 0), head=(0, -20, 0), hipz=-0.6)
    d.pose(td + 0.9, torso=(0, 0, 0), head=(0, 0, 0), hipz=0.0)
    d.face(td, "grin")
    cam = Cam()
    cam.key(t0, (DOOR_X + 6, -14, 5.0), (DOOR_X, -3, 5.0), lens=24, focus=14.0, fstop=4)
    cam.key(t1, (DOOR_X + 3, -17, 5.5), (DOOR_X, -6, 5.5), lens=24, focus=12.0, fstop=4)
    cam.handheld(0.8)
    sfx(td, "whoosh", 0.4)


# ================================================================== BUTTON
@S(73, 332, 339, "Then I asked: kid with a giant ice cream bowl, puppy eyes")
def s73(t0, t1):
    kitchen(night=True, door=True)
    k = kid_c(t0, t1, "happy")
    kp = (2, -8, 0)
    k.pose(t0, loc=kp, rot=-30)
    k.act(t0, "hold", expr="happy")
    bw = empty("bowl", (0, 0, 0))
    cyl("bw_b", 0.7, 0.5, (0, 0, 0), M("#f4f4f4", 0.3), 20, parent=bw)
    for i, c in enumerate(("#ffd6e8", "#8a5a32", "#fff2c8")):
        sphere(f"bw_s{i}", 0.42, (-0.3 + i * 0.3, 0, 0.4 + (i % 2) * 0.2), M(c, 0.5), parent=bw, seg=14)
    sphere("bw_cherry", 0.14, (0, 0, 0.9), M("#d0262a", 0.2), parent=bw, seg=10)
    locs.hand_prop(k, "R", bw, offset=(0.9, -0.9, -2.0))
    lips(k, w(335), t1)
    k.face(w(335), eyes="cry", mouth="smile")
    cam = Cam()
    cam.push(t0, t1, head(kp, 0.9), 6.0, 4.4, yaw=-35, yaw1=-15, pitch=-4, lens=28, fstop=2.4)
    cam.handheld(0.7)


@S(74, 339, 343, "Ice cream for dinner? Macro on the sundae, sprinkles")
def s74(t0, t1):
    kitchen(night=True)
    bw = empty("bowl", (1, -4.5, TABLE_Z))
    cyl("bw_b", 1.0, 0.7, (0, 0, 0.35), M("#f4f4f4", 0.3), 24, parent=bw)
    for i, c in enumerate(("#ffd6e8", "#8a5a32", "#fff2c8")):
        sphere(f"bw_s{i}", 0.6, (-0.45 + i * 0.45, 0, 1.0 + (i % 2) * 0.3), M(c, 0.5), parent=bw, seg=16)
    sphere("bw_cherry", 0.2, (0, 0, 1.75), M("#d0262a", 0.2), parent=bw, seg=12)
    rnd = random.Random(3)
    for i in range(24):
        box(f"spr{i}", (0.05, 0.18, 0.05), (rnd.uniform(-0.9, 0.9), rnd.uniform(-0.4, 0.4), rnd.uniform(1.2, 1.6)),
            M(["#ff3a6a", "#3a8aff", "#ffe14a", "#63e07a"][i % 4], 0.4), 0.02, parent=bw,
            rot=(rnd.uniform(0, 90), 0, rnd.uniform(0, 180)))
    tgt = (1, -4.5, TABLE_Z + 1.1)
    cam = Cam()
    cam.orbit(t0, t1, tgt, 4.8, -40, 20, pitch=22, lens=30, fstop=2.2)
    cam.handheld(0.3)
    sfx(t0 + 0.2, "sparkle", 0.5)


@S(75, 343, 344, "YES. Dad thumbs up, grin, crash zoom")
def s75(t0, t1):
    kitchen(night=True, door=True)
    p = (5, -6, 0)
    d = dad_c(t0, t1, "grin", s=SBIG)
    d.pose(t0, loc=p, rot=-20)
    d.act(t0, "fists", expr="grin")
    d.pose(t0 + 0.1, armR=(150, -10))
    lips(d, t0, t1, "shout")
    cam = Cam()
    cam.push(t0, t1 + 0.1, head(p, SBIG), 6, 4.6, yaw=-20, pitch=-4, lens=28, fstop=2.4)
    cam.crash(t0, 24, 34, 0.08)
    cam.handheld(1.0)
    sfx(t0, "ding", 0.6)


@S(76, 344, 348, "And Mom walked in: through the doorway, arms crossed")
def s76(t0, t1):
    kitchen(night=True, door=True)
    Mo, _ = mom_c(t0, t1, "angry")
    Mo.walk(t0, t0 + 0.9, (DOOR_X, 1.0, 0), (DOOR_X, -5.0, 0), rate=2.0)
    Mo.act(t0 + 1.0, "cross", expr="angry")
    cam = Cam()
    cam.push(t0, t1, (DOOR_X, -4, 4.2), 12, 9, yaw=10, pitch=6, lens=24, yaw1=-5, fstop=4)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "door", 0.6)
    sfx(t0 + 0.3, "footsteps", 0.4)


@S(77, 348, 351, "WHO SAID YES? Mom shouts, crash zoom")
def s77(t0, t1):
    kitchen(night=True, door=True)
    Mo, _ = mom_c(t0, t1, "furious")
    p = (DOOR_X, -5.0, 0)
    Mo.pose(t0, loc=p, rot=-60)
    Mo.act(t0, "point", expr="furious")
    lips(Mo, t0, t1, "shout")
    cam = Cam()
    cam.push(t0, t1, head(p), 5.0, 3.6, yaw=-60, pitch=-6, lens=28, fstop=2.2)
    cam.crash(t0 + 0.05, 24, 36, 0.1)
    cam.handheld(1.4)
    sfx(t0 + 0.05, "boom", 0.4)


@S(78, 351, 353, "Dad froze: grimace, slow push, crickets")
def s78(t0, t1):
    kitchen(night=True, door=True)
    p = (5, -6, 0)
    d = dad_c(t0, t1, "shock", s=SBIG)
    d.pose(t0, loc=p, rot=-30, armL=(35, 55), armR=(35, 55), torso=(0, -8, 0))
    sweat = sphere("sweat", 0.18, (0, 0, 0), mat("sweat", hexc("#9fd8ff"), 0.05, emit=hexc("#9fd8ff"), estr=1, alpha=0.8),
                   (0.8, 0.8, 1.2), seg=10)
    sweat.parent = d.head
    sweat.location = (0.75, -0.6, 0.5)
    sweat.keyframe_insert("location", frame=F(t0 + 0.2))
    sweat.location = (0.75, -0.6, -0.1)
    sweat.keyframe_insert("location", frame=F(t1))
    cam = Cam()
    cam.push(t0, t1, head(p, SBIG), 5.0, 4.2, yaw=-30, pitch=0, lens=30, fstop=2.2)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "crickets", 0.6)


@S(79, 353, 356, "Ask your mom (tiny voice, sheepish shrug)")
def s79(t0, t1):
    kitchen(night=True, door=True)
    p = (5, -6, 0)
    d = dad_c(t0, t1, "smile", s=SBIG)
    d.pose(t0, loc=p, rot=-30)
    d.act(t0, "shrug", expr="smile")
    lips(d, t0, t1)
    Mo, _ = mom_c(t0, t1, "angry")
    Mo.pose(t0, loc=(DOOR_X - 4, -5.0, 0), rot=-90)
    Mo.act(t0, "cross", expr="angry")
    cam = Cam()
    cam.push(t0, t1, (7.5, -6, 5.0), 13, 11, yaw=-25, pitch=4, lens=24, yaw1=-10, fstop=3.5)
    cam.handheld(0.6)


@S(80, 356, None, "FWOOP! Giant shrink to peanut size, poof, mom and kid look down")
def s80(t0, t1):
    kitchen(night=True, door=True)
    p = (5, -6, 0)
    d = dad_c(t0, t1, "shock", s=SBIG)
    d.pose(t0, loc=p, rot=-30)
    tf = t0 + 0.02
    resize(d, tf, SBIG, SP, dur=0.3, loc=p)
    W2.poof("fw", (p[0], p[1], 0.6), tf + 0.25, 0.6, n=7)
    d.face(tf + 0.35, "shock")
    d.act(tf + 0.5, "shrug", expr="smile")
    Mo, _ = mom_c(t0, t1, "angry")
    Mo.pose(t0, loc=(DOOR_X - 4, -5.0, 0), rot=-90)
    Mo.look(tf + 0.35, 0, 35)
    Mo.face(tf + 0.4, "gasp")
    k = kid_c(t0, t1, "shock")
    k.pose(t0, loc=(1.5, -8.0, 0), rot=facing((1.5, -8.0), p))
    k.look(tf + 0.4, 0, 30)
    k.face(tf + 0.4, "gasp")
    cam = Cam()
    cam.key(t0, orbit_pos(head(p, SBIG), 7.0, -30, 4), head(p, SBIG), lens=24, focus=head(p, SBIG), fstop=3)
    cam.key(tf + 0.4, orbit_pos((p[0], p[1], 1.5), 5.5, -25, 22), (p[0], p[1], 0.4), lens=26, focus=(p[0], p[1], 0.3),
            fstop=2.5)
    cam.key(t1 + 0.5, orbit_pos((p[0], p[1], 0.8), 3.6, -15, 18), (p[0], p[1], 0.2), lens=28, focus=(p[0], p[1], 0.2),
            fstop=2.0)
    cam.handheld(0.6)
    sfx(tf, "whoosh", 0.7)
    sfx(tf + 0.25, "poof", 0.8)
    sfx(tf + 0.9, "rimshot", 0.6)
