"""vo / shoe swap: "In this world, if you put on someone else's shoes, you swap bodies with them."
Leo (11) steps into grumpy Mr. Pruitt's boots. Shots keyed to script word indices."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from rbx.sets import wood, planks
from rbx.acting import wiggle

V = Video(__file__)
story.bind(V)

LEO_C, PRU_C = "#5af07a", "#ffb03a"        # soul colours
PORCH_Z = 0.8
CHAIR = (10.0, 13.6, PORCH_Z)              # Pruitt's rocking chair on the porch
BOOTS = (4.2, 12.4, PORCH_Z)               # where the boots sit
DOOR = (6.0, 15.9, PORCH_Z)
FENCE_Y = -12.0


# ================================================================== props
def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def shoe_prop(name, loc, color="#e8423a", rot=0, boot=False, s=1.0, coll=None):
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    if boot:
        Mb = M("#6b4326", 0.65)
        box(name + "_up", (1.08, 1.12, 1.25), (0, 0.15, 0.68), Mb, 0.14, parent=root, coll=coll)
        box(name + "_toe", (1.08, 1.0, 0.6), (0, -0.62, 0.35), Mb, 0.2, parent=root, coll=coll)
        box(name + "_sole", (1.14, 2.2, 0.16), (0, -0.2, 0.08), M("#3a2516", 0.8), 0.04, parent=root, coll=coll)
        box(name + "_cuff", (1.14, 1.18, 0.18), (0, 0.15, 1.3), M("#4e2f1a", 0.7), 0.06, parent=root, coll=coll)
    else:
        Mu = M(color, 0.35)
        box(name + "_up", (1.06, 1.9, 0.62), (0, -0.15, 0.42), Mu, 0.22, parent=root, coll=coll)
        box(name + "_sole", (1.12, 2.0, 0.2), (0, -0.15, 0.1), M("#f4f4f4", 0.5), 0.06, parent=root, coll=coll)
        box(name + "_stripe", (1.1, 0.5, 0.2), (0, 0.1, 0.5), M("#f4f4f4", 0.5), 0.05, parent=root, coll=coll)
    return root


def wear(ch, kind="sneaker", color="#e8423a"):
    """Shoes / boots / socks on a character's feet (parented to the leg pivots)."""
    for piv in (ch.hpL, ch.hpR):
        n = ch.name + piv.name
        if kind == "boots":
            box(n + "_boot", (1.12, 1.5, 0.95), (0, -0.2, -1.6), M("#6b4326", 0.65), 0.14, parent=piv, coll=ch.coll)
            box(n + "_bsole", (1.16, 1.56, 0.16), (0, -0.2, -2.04), M("#3a2516", 0.8), 0.04, parent=piv, coll=ch.coll)
        elif kind == "socks":
            box(n + "_sock", (1.04, 1.06, 0.7), (0, -0.05, -1.68), M("#f2f2f2", 0.8), 0.1, parent=piv, coll=ch.coll)
            box(n + "_sockb", (1.06, 1.08, 0.16), (0, -0.05, -1.4), M("#d9453a", 0.8), 0.03, parent=piv, coll=ch.coll)
        else:
            box(n + "_shoe", (1.1, 1.55, 0.5), (0, -0.25, -1.8), M(color, 0.35), 0.16, parent=piv, coll=ch.coll)
            box(n + "_ssole", (1.14, 1.6, 0.16), (0, -0.25, -2.03), M("#f4f4f4", 0.5), 0.04, parent=piv, coll=ch.coll)
    return ch


def soccer_ball(name, loc, r=0.6, coll=None):
    root = empty(name, loc, coll=coll)
    sphere(name + "_b", r, (0, 0, 0), M("#f6f6f6", 0.35), parent=root, coll=coll, seg=20)
    for i, (a, b) in enumerate(((0, 0), (72, 60), (144, 60), (216, 60), (288, 60), (36, 120), (108, 120),
                                (180, 120), (252, 120), (324, 120), (0, 180))):
        d = Vector((math.sin(math.radians(b)) * math.cos(math.radians(a)),
                    math.sin(math.radians(b)) * math.sin(math.radians(a)), math.cos(math.radians(b))))
        p = sphere(f"{name}_p{i}", r * 0.33, tuple(d * r * 0.93), M("#1a1a1e", 0.4), (1, 1, 0.35), parent=root,
                   coll=coll, seg=10)
        p.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return root


def ball_fly(ob, t0, t1, p0, p1, h=4.0, spin=2.0, n=6):
    for i in range(n + 1):
        k = i / n
        p = Vector(p0).lerp(Vector(p1), k) + Vector((0, 0, 4 * h * k * (1 - k)))
        ob.location = p
        ob.keyframe_insert("location", frame=F(t0 + (t1 - t0) * k))
        set_interp(ob, "location", F(t0 + (t1 - t0) * k), "LINEAR")
    ob.rotation_euler = (0, 0, 0)
    ob.keyframe_insert("rotation_euler", frame=F(t0))
    ob.rotation_euler = (spin * math.tau, spin * 0.6 * math.tau, 0)
    ob.keyframe_insert("rotation_euler", frame=F(t1))
    set_interp(ob, "rotation_euler", F(t0), "LINEAR")


def bounce(ob, t0, p0, p1, hops=(2.0, 0.8, 0.25), dt=(0.35, 0.22, 0.14)):
    p0, p1 = Vector(p0), Vector(p1)
    t = t0
    seg = len(hops)
    for i, (h, d) in enumerate(zip(hops, dt)):
        a = p0.lerp(p1, i / seg); b = p0.lerp(p1, (i + 1) / seg)
        ob.location = a; ob.keyframe_insert("location", frame=F(t))
        ob.location = (a + b) / 2 + Vector((0, 0, h)); ob.keyframe_insert("location", frame=F(t + d / 2))
        t += d
    ob.location = p1; ob.keyframe_insert("location", frame=F(t))


def swap_fx(name, pa, pb, t, dur=0.4, s=1.0, ca=LEO_C, cb=PRU_C, snd=True):
    """Body swap: two glowing souls leave the heads, spiral past each other and dive into the other body."""
    pa, pb = Vector(pa), Vector(pb)
    side = (pb - pa).cross(Vector((0, 0, 1)))
    side = side.normalized() if side.length > 1e-3 else Vector((1, 0, 0))
    for k, (p0, p1, c) in enumerate(((pa, pb, ca), (pb, pa, cb))):
        Ms = mat("soul" + c, hexc(c), 0.3, emit=hexc(c), estr=14)
        mid = (p0 + p1) / 2 + Vector((0, 0, 2.2 * s)) + side * (1.6 * s if k == 0 else -1.6 * s)
        for j in range(5):
            r = (0.42 if j == 0 else 0.3 - j * 0.045) * s
            o = sphere(f"{name}_soul{k}_{j}", r, tuple(p0), Ms, seg=14)
            lag = j * 0.035
            sets.set_obj_visible(o, t - 1.0 / 30, False)
            sets.set_obj_visible(o, t + lag, True)
            for kk, (tt, pp) in enumerate(((t + lag, p0), (t + lag + dur * 0.5, mid), (t + lag + dur, p1))):
                o.location = pp
                o.keyframe_insert("location", frame=F(tt))
            sets.set_obj_visible(o, t + lag + dur + 1.0 / 30, False)
        lt = light(f"{name}_fl{k}", "POINT", tuple(p1 + Vector((0, -1.2, 0.4))), 0, hexc(c), 1.5)
        lt.data.keyframe_insert("energy", frame=F(t + dur - 0.05))
        lt.data.energy = 6000 * s
        lt.data.keyframe_insert("energy", frame=F(t + dur + 0.02))
        lt.data.energy = 0
        lt.data.keyframe_insert("energy", frame=F(t + dur + 0.35))
        W2.poof(f"{name}_pf{k}", tuple(p1), t + dur, 0.35 * s, n=4, seed=k)
    if snd:
        sfx(t, "teleport", 0.9)
        sfx(t + dur, "glitch", 0.7)


def sparkle_on(name, loc, t, s=1.0, n=10, seed=0):
    rnd = random.Random(seed)
    Ms = mat("sp_gold", hexc("#fff1a0"), 0.3, emit=hexc("#fff1a0"), estr=10)
    for i in range(n):
        p = Vector(loc) + Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.5, 1))) * s
        o = sphere(f"{name}{i}", 0.09 * s, tuple(p), Ms, seg=8)
        ts = t + rnd.uniform(0, 0.6)
        o.scale = (0.01,) * 3; o.keyframe_insert("scale", frame=F(ts - 0.05))
        o.scale = (1.6, 1.6, 1.6); o.keyframe_insert("scale", frame=F(ts + 0.08))
        o.scale = (0.01,) * 3; o.keyframe_insert("scale", frame=F(ts + 0.3))


def zzz(ch, t0, t1):
    Mz = mat("zzz", hexc("#ffffff"), 0.4, emit=hexc("#cfe3ff"), estr=2)
    for i in range(3):
        z = text(f"{ch.name}_z{i}", "Z", (0, 0, 0), 0.7 + 0.25 * i, Mz, extrude=0.05)
        z.parent = ch.root
        ts = t0 + i * 0.35
        p0 = Vector((0.8, -0.6, 5.6)); p1 = p0 + Vector((1.0 + i * 0.3, 0, 2.2))
        z.location = p0; z.scale = (0.01,) * 3
        z.keyframe_insert("location", frame=F(ts)); z.keyframe_insert("scale", frame=F(ts))
        z.location = p1; z.scale = (1, 1, 1)
        z.keyframe_insert("location", frame=F(min(t1, ts + 1.0))); z.keyframe_insert("scale", frame=F(min(t1, ts + 1.0)))


def popcorn(name, loc, t, n=8, seed=0):
    """Little white puffs popping off a knee."""
    rnd = random.Random(seed)
    Mp = mat("popc", hexc("#fff6dc"), 0.7, emit=hexc("#fff0c0"), estr=1.5)
    for i in range(n):
        ts = t + i * 0.09
        p = Vector(loc)
        o = sphere(f"{name}{i}", 0.2, tuple(p), Mp, (1, 0.8, 0.9), seg=10)
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(ts - 0.04)); o.keyframe_insert("location", frame=F(ts - 0.04))
        o.scale = (1, 1, 1); o.keyframe_insert("scale", frame=F(ts + 0.03))
        o.location = tuple(p + Vector((rnd.uniform(-1.2, 1.2), rnd.uniform(-1.5, -0.3), rnd.uniform(0.8, 2.0))))
        o.keyframe_insert("location", frame=F(ts + 0.3))
        o.location = tuple(Vector(o.location) + Vector((0, 0, -1.5)))
        o.keyframe_insert("location", frame=F(ts + 0.55))
        sfx(ts, "pop", 0.55)


def hunch(ch, t):
    ch.pose(t, torso=(0, 16, 0), head=(0, -12, 0), armL=(18, 6), armR=(18, 6), hipz=-0.25)


def lemonade(loc, coll=None):
    root = empty("lemo", loc, coll=coll)
    box("lemo_tab", (3.0, 2.0, 0.2), (0, 0, 2.4), wood("lemo_w", "#c8955f", "#dcae78", 2.0), 0.05, parent=root, coll=coll)
    for sx in (-1, 1):
        box(f"lemo_leg{sx}", (0.2, 1.6, 2.3), (sx * 1.3, 0, 1.15), M("#8a5a32"), 0.02, parent=root, coll=coll)
    Mg = mat("lemon_juice", hexc("#ffe14a"), 0.1, emit=hexc("#ffd23a"), estr=0.4, alpha=0.85)
    cyl("lemo_pitch", 0.5, 1.3, (-0.6, 0, 3.15), Mg, 20, parent=root, coll=coll)
    for i in range(3):
        cyl(f"lemo_g{i}", 0.22, 0.6, (0.3 + i * 0.5, -0.2 + (i % 2) * 0.4, 2.8), Mg, 14, parent=root, coll=coll)
    sphere("lemo_lemon", 0.25, (-0.6, -0.55, 2.7), M("#f7d21e", 0.4), (1.3, 1, 1), parent=root, coll=coll)
    return root


# ================================================================== cast
def leo_c(t0, t1, expr="neutral", feet="sneaker", name=None):
    L = leo(t0, t1, expr) if name is None else story._live(chars.Char(name, skin="#d9b48f", shirt="#4fbf5a",
            pants="#2f3f6a", hair="messy", hair_color="#1d1714", face="kid", vneck="#8fe39a"), t0, t1, expr)
    return wear(L, feet, "#e8423a")


def pruitt(t0, t1, expr="angry", feet="boots"):
    P = chars.Char("Pruitt", skin="#ecd2b8", shirt="#8a6a48", pants="#55565e", hair="short", hair_color="#e4e4e4",
                   face="mustache", sleeves="long", extras=("glasses",), vneck="#efe6d6")
    story._live(P, t0, t1, expr, 0.5)
    return wear(P, feet)


def big_kid(t0, t1, expr="smug"):
    K = chars.Char("BigKid", skin="#c9926a", shirt="#d9453a", pants="#2b2b2b", hair="buzz", hair_color="#2a1d16",
                   face="villain", scale=1.3)
    return wear(story._live(K, t0, t1, expr), "sneaker", "#2b2b2b")


def guard(t0, t1, expr="determined"):
    G = chars.Char("Guard", skin="#a8714a", shirt="#1e2230", pants="#1e2230", hair="cap", hair_color="#1e2230",
                   face="villain", sleeves="long", extras=("glasses", "collar:#f2c14e"), scale=1.15)
    return story._live(G, t0, t1, expr)


def bride(t0, t1, expr="happy"):
    B = chars.Char("Bride", skin="#f1dfc6", shirt="#ffffff", pants="#ffffff", hair="bun", hair_color="#c87a3a",
                   face="girl", sleeves="long")
    box("Bride_veil", (1.9, 0.08, 2.6), (0, 0.75, 0.0), mat("veil", (1, 1, 1), 0.3, alpha=0.55), 0.04, parent=B.head,
        coll=B.coll, rot=(12, 0, 0))
    return story._live(B, t0, t1, expr)


def groom(t0, t1, expr="happy"):
    G = chars.Char("Groom", skin="#d9b48f", shirt="#22232a", pants="#22232a", hair="slick", hair_color="#151212",
                   face="hero", sleeves="long", extras=("collar:#f4f4f4",))
    return story._live(G, t0, t1, expr)


def uncle(t0, t1, expr="neutral"):
    return story._live(chars.Char("Uncle", skin="#e9c7a6", shirt="#e8b520", shirt_kind="checker", shirt_c2="#c8761e",
                                  pants="#3b3f4a", hair="short", hair_color="#5a3a22", face="mustache"), t0, t1, expr)


def on_all_fours(ch, t, loc, rot=0):
    ch.pose(t, loc=loc, rot=rot, torso=(0, 78, 0), legL=(80, 4), legR=(80, -4), armL=(80, 4), armR=(80, 4),
            head=(0, -68, 0), hipz=-0.55)


def sit_on(ch, t, seat_top, rot=0, **kw):
    x, y, z = seat_top
    ch.pose(t, loc=(x, y, z - 1.96), rot=rot, legL=(85, 3), legR=(85, -3), armL=(30, 6), armR=(30, 6), **kw)


# ================================================================== sets
def day(sun_rot=(50, 0, 32)):
    W.sky(1.0)
    W.sun(4.0, rot=sun_rot)


def rocking_chair(loc, coll=None, rot=0):
    root = empty("rock", loc, coll=coll, rot=(0, 0, rot))
    Mw = wood("rock_w", "#7a4a2a", "#9a6238", 2.0)
    box("rock_seat", (2.4, 2.2, 0.25), (0, 0, 1.3), Mw, 0.06, parent=root, coll=coll)
    box("rock_back", (2.4, 0.25, 3.4), (0, 1.1, 3.0), Mw, 0.06, parent=root, coll=coll, rot=(-8, 0, 0))
    for sx in (-1, 1):
        box(f"rock_arm{sx}", (0.22, 2.2, 0.2), (sx * 1.2, 0, 2.3), Mw, 0.04, parent=root, coll=coll)
        box(f"rock_run{sx}", (0.2, 3.2, 0.25), (sx * 1.0, 0.2, 0.15), Mw, 0.06, parent=root, coll=coll)
        for sy in (-1, 1):
            box(f"rock_leg{sx}{sy}", (0.2, 0.2, 1.2), (sx * 1.0, sy * 0.9, 0.7), Mw, 0.02, parent=root, coll=coll)
    return root


def hood(boots=True, chair=True, sun_rot=(50, 0, 32), lemon=False):
    """The street: Pruitt's grey house with porch + picket fence, Leo's blue house, sidewalk, road at y=-30."""
    day(sun_rot)
    W.town(school=False)
    c = collection("HOOD")
    # Pruitt house (front face y=16)
    box("ph_body", (18, 12, 10), (6, 22, 5), M("#8c948c", 0.85), 0.1, coll=c)
    box("ph_roof", (19.5, 13.5, 1.4), (6, 22, 10.7), M("#3f3a38", 0.75), 0.25, coll=c)
    box("ph_roof2", (14, 9, 3.0), (6, 22, 12.6), M("#3f3a38", 0.75), 0.25, coll=c)
    box("ph_door", (2.8, 0.3, 5.4), (6, 15.9, 3.5), M("#4a2e1c", 0.6), 0.06, coll=c)
    sphere("ph_knob", 0.18, (7.0, 15.7, 3.4), M("#e2b23a", 0.3, metal=0.8), coll=c)
    for k, x in enumerate((0.0, 12.0)):
        box(f"ph_win{k}", (3.6, 0.3, 3.2), (x, 15.9, 5.0), mat("ph_glass", hexc("#2a3440"), 0.15, metal=0.3), 0.04, coll=c)
        box(f"ph_wfr{k}", (4.1, 0.25, 3.7), (x, 16.0, 5.0), M("#e8e4da"), 0.04, coll=c)
    # porch
    box("ph_porch", (18, 5, PORCH_Z), (6, 13.5, PORCH_Z / 2), wood("porch_w", "#8a6a4e", "#9c7a5a", 1.5), 0.04, coll=c)
    box("ph_step", (4, 1.4, 0.4), (6, 10.4, 0.2), M("#7a5c42", 0.8), 0.03, coll=c)
    box("ph_proof", (19, 6, 0.4), (6, 13.5, 8.2), M("#6a6f6a", 0.8), 0.06, coll=c)
    for x in (-2.7, 14.7):
        box(f"ph_col{x}", (0.5, 0.5, 7.4), (x, 11.3, 4.5), M("#e8e4da"), 0.04, coll=c)
    light("porch_fill", "AREA", (6, 5, 7.5), 4000, (1.0, 0.93, 0.82), 12, coll=c, target=(6, 13, 2))
    if chair:
        rocking_chair(CHAIR, c, rot=0)
    if boots:
        shoe_prop("bootL", (BOOTS[0] - 0.65, BOOTS[1], BOOTS[2]), boot=True, rot=8, coll=c)
        shoe_prop("bootR", (BOOTS[0] + 0.65, BOOTS[1], BOOTS[2]), boot=True, rot=-4, coll=c)
    if lemon:
        lemonade((1.0, 12.6, PORCH_Z), c)
    # yard + picket fence
    box("ph_yard", (18, 22, 0.1), (6, -1, 0.05), M("#4f9a3c", 0.9), 0, coll=c)
    Mf = M("#f2f0ea", 0.6)
    for i in range(19):
        x = -3 + i * 1.0
        if abs(x - 6) < 1.4:
            continue
        box(f"pk{i}", (0.45, 0.2, 2.2), (x, FENCE_Y, 1.1), Mf, 0.04, coll=c)
    box("pk_rail", (18.4, 0.15, 0.3), (6, FENCE_Y + 0.15, 1.4), Mf, 0.02, coll=c)
    box("ph_path", (2.6, 22, 0.12), (6, -1, 0.07), M("#c9c3b5", 0.9), 0, coll=c)
    # Leo's house
    box("lh_body", (16, 12, 9), (-20, 22, 4.5), M("#6fb3e0", 0.75), 0.1, coll=c)
    box("lh_roof", (17.5, 13.5, 1.4), (-20, 22, 9.7), M("#a33b2f", 0.7), 0.25, coll=c)
    box("lh_door", (2.8, 0.3, 5.4), (-20, 15.9, 2.7), M("#f2c14e", 0.5), 0.06, coll=c)
    box("lh_win", (3.6, 0.3, 3.2), (-25, 15.9, 4.6), mat("lh_glass", hexc("#cfe8ff"), 0.1, emit=hexc("#cfe8ff"), estr=0.3), 0.04, coll=c)
    # sidewalk + trees
    box("sidewalk", (120, 5, 0.18), (0, -19, 0.09), M("#d6d2c8", 0.9), 0, coll=c)
    for k, (x, y) in enumerate(((-34, 6), (24, 4), (-8, -8), (30, -6))):
        cyl(f"tr_t{k}", 0.45, 5, (x, y, 2.5), M("#6a4a2a"), 10, coll=c)
        sphere(f"tr_c{k}", 3.0, (x, y, 6.5), M("#3f8f3a", 0.9), (1, 1, 1.15), coll=c, seg=14)
    return c


def shoe_store():
    world((0.95, 0.93, 0.9), 0.5)
    c = collection("SHOP")
    box("ss_floor", (30, 30, 0.4), (0, 2, -0.2), sets.checker_mat("ss_fl", "#f4f1ea", "#d8d2c6", 0.25), 0, coll=c)
    box("ss_back", (30, 0.5, 14), (0, 10.25, 7), M("#f6d3a8", 0.85), 0, coll=c)
    for sx in (-1, 1):
        box(f"ss_side{sx}", (0.5, 30, 14), (sx * 13, 2, 7), M("#f0c896", 0.85), 0, coll=c)
    rnd = random.Random(2)
    cols = ["#e8423a", "#3f7fd9", "#f2c14e", "#63c06a", "#f09ac2", "#ffffff", "#2b2b2b", "#ff9a3c"]
    for r, z in enumerate((1.2, 3.4, 5.6, 7.8)):
        box(f"ss_shelf{r}", (24, 1.8, 0.25), (0, 9.2, z), wood("ss_wood", "#b07a52", "#c89260", 2.0), 0.03, coll=c)
        for i in range(11):
            x = -10.5 + i * 2.1 + rnd.uniform(-0.15, 0.15)
            shoe_prop(f"ss_sh{r}_{i}", (x, 9.2, z + 0.12), cols[(i + r * 3) % len(cols)], rot=rnd.uniform(60, 120),
                      s=0.75, coll=c)
    t = text("ss_sign", "SHOES", (0, 10.0, 11.2), 2.4, mat("ss_neon", hexc("#ff4a6a"), 0.3, emit=hexc("#ff4a6a"), estr=6),
             extrude=0.1, coll=c)
    # velvet rope + stanchions in front of the shelves
    Mg = M("#e2b23a", 0.25, metal=0.8)
    for x in (-6, -2, 2, 6):
        cyl(f"ss_post{x}", 0.18, 3.0, (x, 4.0, 1.5), Mg, 12, coll=c)
        sphere(f"ss_postk{x}", 0.3, (x, 4.0, 3.1), Mg, coll=c, seg=12)
    box("ss_rope", (12, 0.2, 0.2), (0, 4.0, 2.5), M("#b0122a", 0.5), 0.08, coll=c)
    box("ss_bench", (6, 2, 1.6), (-8, 0, 0.8), M("#3f7fd9", 0.5), 0.2, coll=c)
    light("ss_key", "AREA", (0, -4, 12), 5000, (1.0, 0.96, 0.9), 12, coll=c, target=(0, 6, 2))
    light("ss_fill", "AREA", (8, -6, 5), 1500, (0.9, 0.95, 1.0), 6, coll=c, target=(0, 6, 3))
    return c


def bowling():
    world((0.15, 0.1, 0.25), 0.4)
    c = collection("BOWL")
    box("bw_floor", (40, 60, 0.4), (0, 14, -0.2), M("#2a2340", 0.7), 0, coll=c)
    Mlane = wood("bw_lane", "#d9a86a", "#e8bd84", 1.0, 0.15)
    for k in range(4):
        x = -9 + k * 6
        box(f"bw_lane{k}", (3.6, 40, 0.2), (x, 18, 0.1), Mlane, 0.02, coll=c)
        for sx in (-1, 1):
            box(f"bw_gut{k}{sx}", (0.6, 40, 0.12), (x + sx * 2.1, 18, 0.06), M("#555566", 0.4, metal=0.4), 0.02, coll=c)
        for r in range(4):
            for j in range(r + 1):
                px = x + (j - r / 2) * 0.75
                cyl(f"bw_pin{k}{r}{j}", 0.22, 1.3, (px, 34 + r * 0.7, 0.85), M("#f6f6f6", 0.3), 12, coll=c)
    box("bw_back", (40, 0.5, 14), (0, 38, 7), M("#1a1430", 0.8), 0, coll=c)
    Mn = [mat("neon_p", hexc("#ff4adf"), 0.3, emit=hexc("#ff4adf"), estr=8),
          mat("neon_c", hexc("#3ae8ff"), 0.3, emit=hexc("#3ae8ff"), estr=8)]
    for k in range(6):
        box(f"bw_neon{k}", (40, 0.2, 0.25), (0, 37.7, 4 + k * 1.6), Mn[k % 2], 0.02, coll=c)
    for k in range(5):
        sphere(f"bw_ball{k}", 0.75, (-14 + k * 1.7, 1.5, 3.4), M(["#3f7fd9", "#e8423a", "#9b6ad6", "#63c06a", "#f2c14e"][k], 0.15), coll=c, seg=16)
    box("bw_rack", (9, 1.4, 0.4), (-10.6, 1.5, 2.5), M("#555566", 0.4, metal=0.5), 0.05, coll=c)
    box("bw_rackleg", (0.4, 0.4, 2.4), (-10.6, 1.5, 1.2), M("#555566", 0.4, metal=0.5), 0.05, coll=c)
    light("bw_key", "AREA", (0, 4, 12), 6000, (1.0, 0.85, 1.0), 14, coll=c, target=(0, 8, 0), size_y=10)
    light("bw_p", "POINT", (-8, 20, 6), 3000, hexc("#ff4adf"), 2, coll=c)
    light("bw_c", "POINT", (8, 20, 6), 3000, hexc("#3ae8ff"), 2, coll=c)
    return c


def banned_sign(loc=(0, 8, 7.5), rot=0):
    root = empty("ban", loc, rot=(0, 0, rot))
    box("ban_board", (8.0, 0.3, 3.4), (0, 0, 0), M("#d0262a", 0.4), 0.15, parent=root)
    box("ban_rim", (8.4, 0.25, 3.8), (0, 0.08, 0), M("#f4f4f4", 0.4), 0.15, parent=root)
    Mt = mat("ban_txt", hexc("#ffffff"), 0.3, emit=hexc("#ffffff"), estr=1.5)
    text("ban_t1", "BANNED", (0, -0.2, 0.55), 1.5, Mt, extrude=0.04, parent=root)
    text("ban_t2", "SINCE 2003", (0, -0.2, -0.95), 0.95, Mt, extrude=0.04, parent=root)
    return root


def wedding():
    day((55, 0, 20))
    c = collection("WED")
    box("wd_lawn", (200, 200, 0.4), (0, 0, -0.2), M("#5fb04a", 0.9), 0, coll=c)
    box("wd_aisle", (3.2, 30, 0.06), (0, -6, 0.03), M("#f4f4f4", 0.8), 0, coll=c)
    Mw = M("#ffffff", 0.5)
    for sx in (-1, 1):
        cyl(f"wd_col{sx}", 0.35, 8, (sx * 3.5, 9, 4), Mw, 16, coll=c)
    box("wd_top", (8.2, 0.8, 0.8), (0, 9, 8.2), Mw, 0.3, coll=c)
    rnd = random.Random(5)
    for i in range(26):
        a = i / 25
        x = -3.9 + a * 7.8
        z = 8.2 + math.sin(a * math.pi) * 0.9
        col = ["#f09ac2", "#ffffff", "#f6c0d8", "#ffd6e8"][i % 4]
        sphere(f"wd_fl{i}", rnd.uniform(0.4, 0.6), (x, 8.6, z), M(col, 0.5), coll=c, seg=10)
    for i in range(10):
        col = ["#f09ac2", "#ffffff"][i % 2]
        for sx in (-1, 1):
            sphere(f"wd_cf{i}{sx}", 0.4, (sx * 3.5 + rnd.uniform(-0.3, 0.3), 8.6, 1 + i * 0.7), M(col, 0.5), coll=c, seg=10)
    for r in range(4):
        for sx in (-1, 1):
            for j in range(3):
                x = sx * (3.2 + j * 2.4)
                y = 0 - r * 3.4
                box(f"wd_ch{r}{sx}{j}", (1.8, 1.8, 0.2), (x, y, 1.9), Mw, 0.05, coll=c)
                box(f"wd_chb{r}{sx}{j}", (1.8, 0.2, 2.0), (x, y - 0.9, 3.0), Mw, 0.05, coll=c)
    for k in range(6):
        cyl(f"wd_tr{k}", 0.5, 6, (-26 + k * 10, 34, 3), M("#6a4a2a"), 10, coll=c)
        sphere(f"wd_tc{k}", 4.5, (-26 + k * 10, 34, 8), M("#3f8f3a", 0.9), coll=c, seg=14)
    return c


def guests(t0, t1, mode="smile", n=8):
    ks = []
    for i in range(n):
        r, j = i // 4, i % 4
        sx = -1 if j < 2 else 1
        x = sx * (3.2 + (j % 2) * 2.4)
        y = 0 - r * 3.4
        k = townie(10 + i, t0, t1, mode)
        sit_on(k, t0, (x, y + 0.05, 2.0), rot=180)
        ks.append(k)
    return ks


def ball_room(window_light=True):
    """Pruitt's dim living room: hundreds of balls on shelves, a chair by the window."""
    world((0.45, 0.4, 0.38), 0.25)
    c = collection("BALLS")
    box("br_floor", (30, 30, 0.4), (0, 2, -0.2), planks("br_fl", "#7a5a40", "#6e5038", "#3f2a1c"), 0, coll=c)
    box("br_back", (30, 0.5, 14), (0, 10.25, 7), M("#b8a88a", 0.9), 0, coll=c)
    box("br_left", (0.5, 30, 14), (-13, 2, 7), M("#a8987a", 0.9), 0, coll=c)
    box("br_right", (0.5, 30, 14), (13, 2, 7), M("#a8987a", 0.9), 0, coll=c)
    box("br_door", (0.3, 2.8, 5.4), (12.7, -4, 2.7), M("#4a2e1c", 0.6), 0.06, coll=c)
    # window on the left wall, looking at the yard
    box("br_wframe", (0.3, 5.4, 4.6), (-12.8, -2, 5.0), M("#e8e4da"), 0.04, coll=c)
    card("br_wsky", 4.8, 4.0, (-12.6, -2, 5.0), mat("br_out", hexc("#bfe3ff"), 0.5, emit=hexc("#bfe3ff"), estr=3.0), "+X", coll=c)
    rnd = random.Random(11)
    cols = ["#e8423a", "#3f7fd9", "#f2c14e", "#63c06a", "#f09ac2", "#ff9a3c", "#ffffff", "#9b6ad6"]
    Ml = M("#f4efe0", 0.8)
    for r, z in enumerate((0.9, 2.9, 4.9, 6.9, 8.9, 10.9)):
        box(f"br_shelf{r}", (24, 1.8, 0.22), (0, 9.3, z), wood("br_wood", "#6a4426", "#7d5230", 2.0), 0.03, coll=c)
        for i in range(17):
            x = -11.2 + i * 1.4 + rnd.uniform(-0.08, 0.08)
            rr = rnd.uniform(0.45, 0.6)
            sphere(f"br_b{r}_{i}", rr, (x, 9.3, z + 0.11 + rr), M(cols[rnd.randrange(len(cols))], 0.35), coll=c, seg=12)
            box(f"br_l{r}_{i}", (0.6, 0.04, 0.3), (x, 8.38, z - 0.05), Ml, 0.01, coll=c)
    # armchair by the window, facing it
    Mc = M("#6a3a3a", 0.75)
    ch = empty("br_chair", (-9.0, -2.0, 0), coll=c, rot=(0, 0, -90))
    box("br_cseat", (2.8, 2.6, 1.6), (0, 0, 0.8), Mc, 0.3, parent=ch, coll=c)
    box("br_cback", (2.8, 0.8, 3.6), (0, 1.4, 1.8), Mc, 0.3, parent=ch, coll=c)
    for sx in (-1, 1):
        box(f"br_carm{sx}", (0.6, 2.6, 2.4), (sx * 1.5, 0, 1.2), Mc, 0.25, parent=ch, coll=c)
    light("br_win", "AREA", (-12.2, -2, 6), 3500 if window_light else 800, (1.0, 0.9, 0.75), 4, coll=c, target=(-4, 2, 1))
    light("br_fill", "AREA", (4, -8, 9), 900, (1.0, 0.85, 0.65), 10, coll=c, target=(0, 8, 4))
    light("br_shelfl", "AREA", (0, 3, 12), 1500, (1.0, 0.92, 0.8), 12, coll=c, target=(0, 9, 4), size_y=3)
    Md = mat("dust", hexc("#fff4d6"), 0.5, emit=hexc("#fff4d6"), estr=2.0)
    for i in range(40):
        s = sphere(f"dust{i}", 0.03, (rnd.uniform(-12, -4), rnd.uniform(-5, 1), rnd.uniform(1, 8)), Md, seg=6, coll=c)
        for ax in range(3):
            noise(s, "location", ax, 0.4, 40)
    return c


def label_card(name, body, loc, rot=(90, 0, 0), s=1.0, parent=None):
    root = empty(name, loc, rot=rot, parent=parent)
    box(name + "_c", (2.2 * s, 1.1 * s, 0.04), (0, 0, 0), M("#f6efdc", 0.8), 0.01, parent=root)
    text(name + "_t", body, (0, 0, 0.04), 0.36 * s, mat("ink", hexc("#2a2a3a"), 0.6), extrude=0.005, parent=root, rot=(0, 0, 0))
    return root


def living():
    world((0.85, 0.9, 1.0), 0.4)
    return locs.living_room()


# ================================================================== HOOK (rule)
A0, B0 = (-1.9, -18.2, 0.0), (1.9, -18.2, 0.0)


def hook_pair(t0, t1, ea="neutral", eb="neutral"):
    a = townie(2, t0, t1, ea)
    b = townie(1, t0, t1, eb)
    wear(a, "socks"); wear(b, "socks")
    a.pose(t0, loc=A0, rot=-10)
    b.pose(t0, loc=B0, rot=10)
    return a, b


@S(1, 0, 5, "HOOK: two kids stomp into each other's sneakers")
def s01(t0, t1):
    hood()
    a, b = hook_pair(t0, t1, "grin", "grin")
    shoe_prop("shA", (A0[0] - 0.5, A0[1] - 0.2, 0), "#3f7fd9", rot=-10)
    shoe_prop("shA2", (A0[0] + 0.5, A0[1] - 0.1, 0), "#3f7fd9", rot=-10)
    shoe_prop("shB", (B0[0] - 0.5, B0[1] - 0.1, 0), "#e8423a", rot=10)
    shoe_prop("shB2", (B0[0] + 0.5, B0[1] - 0.2, 0), "#e8423a", rot=10)
    for ch in (a, b):
        ch.pose(t0, legL=(45, 0), hipz=0.4, armL=(30, 20), armR=(30, 20))
        ch.pose(t1 - 0.12, legL=(0, 0), hipz=-0.15)
        ch.pose(t1, hipz=0.0)
    cam = Cam()
    cam.push(t0, t1, (0, -18.2, 2.2), 13, 9, yaw=-28, pitch=12, lens=24, yaw1=-8)
    cam.handheld(1.6)
    sfx(t1 - 0.12, "stomp", 0.8)


@S(2, 5, 10, "Insert: feet slide into the other's shoes")
def s02(t0, t1):
    hood()
    a, b = hook_pair(t0, t1, "grin", "grin")
    shoe_prop("shA", (A0[0] - 0.5, A0[1] - 0.2, 0), "#e8423a", rot=-10)
    shoe_prop("shA2", (A0[0] + 0.5, A0[1] - 0.1, 0), "#e8423a", rot=-10)
    shoe_prop("shB", (B0[0] - 0.5, B0[1] - 0.1, 0), "#3f7fd9", rot=10)
    shoe_prop("shB2", (B0[0] + 0.5, B0[1] - 0.2, 0), "#3f7fd9", rot=10)
    for ch in (a, b):
        ch.pose(t0, legR=(40, 0), hipz=0.5)
        ch.pose(t0 + 0.5, legR=(0, 0), hipz=0.0)
    cam = Cam()
    cam.key(t0, (-4.5, -29, 1.0), (0, -18.4, 0.6), lens=22, focus=11.5, fstop=3.5)
    cam.key(t1, (3.0, -28, 1.4), (0, -18.4, 0.9), lens=24, focus=10.0, fstop=3.5)
    cam.handheld(1.2)
    sfx(t0 + 0.45, "place", 0.8)
    sparkle_on("spk", (0, -18.6, 0.6), t0 + 0.5, 2.5)


@S(3, 10, 15, "SWAP: souls fly between their heads")
def s03(t0, t1):
    hood()
    a, b = hook_pair(t0, t1, "neutral", "neutral")
    for ch in (a, b):
        wear(ch, "sneaker", "#e8423a" if ch is a else "#3f7fd9")
    ts = t0 + 0.05
    swap_fx("sw", up(A0, 4.6), up(B0, 4.6), ts, 0.45, 1.0)
    for ch in (a, b):
        ch.face(ts, eyes="closed", mouth="o")
        ch.pose(ts, torso=(0, -10, 0), armL=(40, 50), armR=(40, 50))
        ch.face(ts + 0.5, "shock")
        ch.act(ts + 0.5, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, -18.2, 4.6), 12, 8.5, yaw=0, pitch=8, lens=22)
    cam.crash(ts + 0.45, 22, 30, 0.1)
    cam.handheld(2.0)


@S(4, 15, 21, "Swapped: each stares at their new hands")
def s04(t0, t1):
    hood()
    a, b = hook_pair(t0, t1, "terror", "shock")
    wear(a, "sneaker", "#e8423a"); wear(b, "sneaker", "#3f7fd9")
    a.act(t0, "hands_head", expr="terror")
    b.pose(t0, armL=(70, -20), armR=(70, -20), head=(0, 30, 0))
    b.face(t0, eyes="wide", mouth="scream")
    look_at(a, t0 + 0.5, up(B0, 4.6))
    a.act(t0 + 0.5, "point", expr="shout")
    cam = Cam()
    cam.whip(t0, t0 + 0.18, orbit_pos(up(A0, 4.4), 6.5, -20, 6), up(A0, 4.4), orbit_pos(up(A0, 4.4), 6.0, -10, 6),
             up(A0, 4.4), lens=28)
    cam.key(t0 + 0.55, orbit_pos(up(A0, 4.4), 6.0, -10, 6), up(A0, 4.4), lens=28)
    cam.key(t1, orbit_pos(up(B0, 4.4), 6.3, 12, 4), up(B0, 4.4), lens=28)
    cam.handheld(1.4)


@S(5, 21, 27, "Both kick the shoes off at the same instant")
def s05(t0, t1):
    hood()
    a, b = hook_pair(t0, t1, "determined", "determined")
    tk = w(24) - 0.05
    shoes = []
    for i, (ch, col, p) in enumerate(((a, "#e8423a", A0), (b, "#3f7fd9", B0))):
        for j, dx in enumerate((-0.5, 0.5)):
            sh = shoe_prop(f"fly{i}{j}", (p[0] + dx, p[1] - 0.15, 0), col)
            sh.keyframe_insert("location", frame=F(tk))
            sh.keyframe_insert("rotation_euler", frame=F(tk))
            sh.location = (p[0] + dx * 4 + (i - 0.5) * 3, p[1] - 4, 7 + j)
            sh.rotation_euler = (math.tau * 1.2, 0.8, math.tau * (j - 0.5))
            sh.keyframe_insert("location", frame=F(t1 + 0.4))
            sh.keyframe_insert("rotation_euler", frame=F(t1 + 0.4))
            shoes.append(sh)
        ch.pose(tk - 0.15, legL=(-20, 0), legR=(-20, 0), hipz=-0.3)
        ch.pose(tk + 0.08, legL=(70, 0), legR=(55, 0), hipz=0.6, armL=(150, 30), armR=(150, 30))
        ch.pose(tk + 0.4, legL=(0, 0), legR=(0, 0), hipz=0.0)
        ch.face(tk, "shout")
    cam = Cam()
    cam.push(t0, t1, (0, -18.2, 3.0), 13, 10, yaw=18, pitch=6, lens=22, yaw1=-6)
    cam.crash(tk, 22, 18, 0.12)
    cam.handheld(1.5)
    sfx(tk, "whoosh")


@S(6, 27, 30, "Same second: souls snap back, flash")
def s06(t0, t1):
    hood()
    a, b = hook_pair(t0, t1, "shock", "shock")
    ts = t0 + 0.02
    swap_fx("sb", up(A0, 4.6), up(B0, 4.6), ts, 0.35, 1.0)
    for ch in (a, b):
        ch.face(ts + 0.45, "joy")
        ch.act(ts + 0.4, "cheer")
    cam = Cam()
    cam.orbit(t0, t1, (0, -18.2, 4.0), 10, -25, 20, pitch=10, lens=22, fstop=5)
    cam.handheld(1.5)
    sfx(ts + 0.35, "ding", 0.8)


# ================================================================== SOCIETY
@S(7, 30, 34, "Shoe store: wall of sneakers behind a velvet rope")
def s07(t0, t1):
    shoe_store()
    k = townie(4, t0, t1, "sus")
    wear(k, "socks")
    k.walk(t0, t1, (-6, -2, 0), (-3, 1.5, 0), rate=2.2)
    cam = Cam()
    cam.push(t0, t1, (0, 6, 4.5), 22, 15, yaw=-6, pitch=8, lens=20, yaw1=6, fstop=8)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "cashier", 0.5)


@S(8, 34, 36, "SECURITY GUARD crash zoom, arms crossed")
def s08(t0, t1):
    shoe_store()
    G = guard(t0, t1)
    G.pose(t0, loc=(0, 2.0, 0), rot=0)
    G.act(t0, "cross")
    G.look(t0 + 0.2, -20, 0)
    G.look(t0 + 0.45, 15, 0)
    cam = Cam()
    cam.push(t0, t1, (0, 2.0, 5.4), 9, 6.0, yaw=8, pitch=-4, lens=26)
    cam.crash(t0, 18, 30, 0.12)
    cam.handheld(1.2)
    sfx(t0, "whoosh", 0.7)
    sfx(t0 + 0.1, "bonk", 0.5)


@S(9, 36, 39, "Bowling alley, neon lanes")
def s09(t0, t1):
    bowling()
    k = townie(5, t0, t1, "happy")
    k.pose(t0, loc=(-6.5, 3, 0), rot=150)
    k.act(t0, "reach")
    b = sphere("rollball", 0.75, (-3, 6, 0.75), M("#3f7fd9", 0.15), seg=16)
    b.keyframe_insert("location", frame=F(t0 + 0.2))
    b.location = (-3, 30, 0.75)
    b.keyframe_insert("location", frame=F(t1 + 0.3))
    cam = Cam()
    cam.key(t0, (-3, -6, 2.5), (-3, 20, 1.5), lens=22, focus=12.0, fstop=4)
    cam.key(t1, (-3, 0, 2.0), (-3, 24, 1.0), lens=22, focus=12.0, fstop=4)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "rise", 0.5)


@S(10, 39, 42, "BANNED 2003 sign slams down")
def s10(t0, t1):
    bowling()
    sg = banned_sign((0, 8, 14))
    sg.keyframe_insert("location", frame=F(t0))
    sg.location = (0, 8, 6.2)
    sg.keyframe_insert("location", frame=F(t0 + 0.2))
    set_interp(sg, "location", F(t0), "BEZIER", "EASE_IN")
    sg.location = (0, 8, 6.6)
    sg.keyframe_insert("location", frame=F(t0 + 0.32))
    sg.location = (0, 8, 6.4)
    sg.keyframe_insert("location", frame=F(t0 + 0.45))
    cam = Cam()
    cam.push(t0, t1, (0, 8, 6.4), 14, 11, yaw=0, pitch=2, lens=26)
    cam.crash(t0 + 0.2, 26, 32, 0.08)
    cam.handheld(1.2)
    sfx(t0 + 0.2, "hammer")


@S(11, 42, 49, "The whole town swapped at once: souls everywhere")
def s11(t0, t1):
    bowling()
    rnd = random.Random(3)
    pts = []
    for i in range(8):
        k = townie(20 + i, t0, t1, "shock")
        p = (-12 + (i % 4) * 7 + rnd.uniform(-1, 1), 2 + (i // 4) * 6, 0)
        k.pose(t0, loc=p, rot=rnd.uniform(-40, 40) + 180 * (i // 4 == 0) * 0)
        k.act(t0 + rnd.uniform(0.3, 0.8), "hands_head", expr="terror")
        k.face(t0 + 0.9, "panic")
        pts.append(up(p, 4.6))
    for i in range(4):
        swap_fx(f"tw{i}", pts[i], pts[7 - i], t0 + 0.1 + i * 0.18, 0.45, 0.9, snd=(i % 2 == 0))
    cam = Cam()
    cam.orbit(t0, t1, (-1.5, 5, 3.5), 20, -30, 25, pitch=22, lens=20, fstop=8)
    cam.handheld(1.5)
    sfx(t0 + 0.4, "crowd", 0.8)


@S(12, 49, 52, "Nobody owns shoelaces: laces crossed out")
def s12(t0, t1):
    shoe_store()
    root = empty("lace_root", (0, 2, 3.6))
    Ml = M("#f4f4f4", 0.6)
    for i in range(5):
        box(f"lace{i}", (2.6, 0.12, 0.12), (0, 0, -0.9 + i * 0.45), Ml, 0.05, parent=root, rot=(0, 25 * (1 if i % 2 else -1), 0))
    box("lace_box", (3.4, 0.4, 3.2), (0, 0.3, 0), M("#5a4a9a"), 0.08, parent=root)
    Mx = mat("redx", hexc("#ff2a2a"), 0.3, emit=hexc("#ff2a2a"), estr=3)
    for sgn in (-1, 1):
        x = box(f"xbar{sgn}", (5.0, 0.2, 0.55), (0, -0.4, 0), Mx, 0.1, parent=root, rot=(0, 45 * sgn, 0))
        x.scale = (0.01, 1, 1)
        x.keyframe_insert("scale", frame=F(t0 + 0.15 + (sgn + 1) * 0.08))
        x.scale = (1, 1, 1)
        x.keyframe_insert("scale", frame=F(t0 + 0.3 + (sgn + 1) * 0.08))
    cam = Cam()
    cam.push(t0, t1, (0, 2, 3.6), 9, 7, yaw=-12, pitch=4, lens=30, yaw1=10)
    cam.handheld(1.0)
    sfx(t0 + 0.15, "buzzer", 0.6)


@S(13, 52, 55, "Velcro strap RIP close-up")
def s13(t0, t1):
    hood()
    k = townie(6, t0, t1, "determined")
    p = (-6, -24, 0)
    k.pose(t0, loc=p, rot=-30)
    wear(k, "sneaker", "#63c06a")
    straps = []
    for piv in (k.hpL, k.hpR):
        s = box(k.name + piv.name + "_strap", (1.2, 0.5, 0.15), (0, -0.55, -1.5), M("#2b2b2b", 0.8), 0.05, parent=piv, coll=k.coll)
        straps.append(s)
    tr = w(54)
    for s in straps:
        s.rotation_euler = (0, 0, 0); s.keyframe_insert("rotation_euler", frame=F(tr))
        s.rotation_euler = (math.radians(-80), 0, 0); s.keyframe_insert("rotation_euler", frame=F(tr + 0.1))
    cam = Cam()
    cam.key(t0, orbit_pos((p[0], p[1], 0.8), 7.5, -55, 16), (p[0], p[1], 0.8), lens=30, focus=7.5, fstop=3.5)
    cam.key(t1, orbit_pos((p[0], p[1], 0.9), 6.0, -15, 22), (p[0], p[1], 0.9), lens=30, focus=6.0, fstop=3.5)
    cam.handheld(1.5)
    sfx(tr, "rip")


@S(14, 55, 59, "Fast escape: kid jumps out of the shoes and sprints off in socks")
def s14(t0, t1):
    hood()
    k = townie(6, t0, t1, "terror")
    wear(k, "socks")
    p = (-6, -24, 0)
    shoe_prop("es1", (p[0] - 0.5, p[1], 0), "#63c06a", rot=-30)
    shoe_prop("es2", (p[0] + 0.5, p[1] + 0.2, 0), "#63c06a", rot=-30)
    sn = townie(3, t0, t1, "sus")
    sn.pose(t0, loc=(-11, -22, 0), rot=facing((-11, -22), p))
    sn.act(t0, "reach")
    sn.walk(t0, t1, (-11, -22, 0), (-8, -23, 0), rate=1.6)
    k.pose(t0, loc=p, rot=-30)
    tj = t0 + 0.15
    k.jump(tj, 1.8, 0.4, loc=p)
    k.run(tj + 0.4, t1, (p[0], p[1], 0), (14, -27, 0), rate=4.2)
    k.face(tj + 0.4, "scream")
    cam = Cam()
    cam.key(t0, (-11, -32, 3.5), (-6, -24, 3.0), lens=24, focus=9.0, fstop=5)
    cam.key(t1, (4, -35, 3.5), (8, -26, 3.0), lens=24, focus=9.0, fstop=5)
    cam.handheld(1.4)
    sfx(tj, "boing", 0.7)
    sfx(tj + 0.45, "whoosh", 0.8)


@S(15, 59, 62, "Wedding: crane down onto the white arch")
def s15(t0, t1):
    wedding()
    B = bride(t0, t1); G = groom(t0, t1)
    B.pose(t0, loc=(1.6, 8, 0), rot=facing((1.6, 8), (-1.6, 8)))
    G.pose(t0, loc=(-1.6, 8, 0), rot=facing((-1.6, 8), (1.6, 8)))
    guests(t0, t1)
    cam = Cam()
    cam.key(t0, (0, -26, 16), (0, 6, 4), lens=22, focus=30.0, fstop=8)
    cam.key(t1, (0, -16, 7), (0, 8, 4.5), lens=22, focus=24.0, fstop=8)
    cam.handheld(0.8)
    sfx(t0, "rise", 0.4)


@S(16, 62, 65, "Bride and groom, hands held, smiling")
def s16(t0, t1):
    wedding()
    B = bride(t0, t1, "happy"); G = groom(t0, t1, "happy")
    B.pose(t0, loc=(1.6, 8, 0), rot=facing((1.6, 8), (-1.6, 8)), armR=(55, -20))
    G.pose(t0, loc=(-1.6, 8, 0), rot=facing((-1.6, 8), (1.6, 8)), armL=(55, -20))
    B.face(t0 + 0.3, "smile")
    cam = Cam()
    cam.orbit(t0, t1, (0, 8, 4.4), 9.5, -30, -5, pitch=4, lens=24, fstop=3.5)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "aww", 0.5)


@S(17, 65, 70, "They swap shoes: souls cross under the arch, petals")
def s17(t0, t1):
    wedding()
    B = bride(t0, t1, "happy"); G = groom(t0, t1, "happy")
    pb, pg = (1.6, 8, 0), (-1.6, 8, 0)
    B.pose(t0, loc=pb, rot=facing(pb, pg))
    G.pose(t0, loc=pg, rot=facing(pg, pb))
    ts = w(67)
    swap_fx("wsw", up(pg, 4.6), up(pb, 4.6), ts, 0.45, 1.0)
    for ch in (B, G):
        ch.face(ts + 0.5, "shock")
        ch.act(ts + 0.5, "shock")
    confetti("petal", (0, 8, 9), (5, 3, 2), ts + 0.45, 1.6, 60, seed=4, fall=9)
    cam = Cam()
    cam.push(t0, t1, (0, 8, 4.4), 12, 8, yaw=8, pitch=6, lens=22, yaw1=-8)
    cam.crash(ts + 0.45, 22, 28, 0.1)
    cam.handheld(1.2)
    sfx(ts + 0.45, "confetti", 0.6)


@S(18, 70, 73, "That's the vow: groom (in the bride's body) blushes, bride flexes")
def s18(t0, t1):
    wedding()
    B = bride(t0, t1, "smug"); G = groom(t0, t1, "smile")
    pb, pg = (1.6, 8, 0), (-1.6, 8, 0)
    B.pose(t0, loc=pb, rot=facing(pb, (0, -10)))
    G.pose(t0, loc=pg, rot=facing(pg, (0, -10)))
    B.act(t0 + 0.1, "fists", expr="determined")
    G.act(t0 + 0.1, "hands_face")
    G.face(t0 + 0.1, eyes="happy", mouth="smile")
    cam = Cam()
    cam.push(t0, t1, (0, 8, 4.5), 9, 7.0, yaw=0, pitch=2, lens=24)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "rimshot", 0.5)


@S(19, 73, 78, "I've walked in your shoes: guests go aww")
def s19(t0, t1):
    wedding()
    B = bride(t0, t1, "happy"); G = groom(t0, t1, "happy")
    pb, pg = (1.6, 8, 0), (-1.6, 8, 0)
    B.pose(t0, loc=pb, rot=facing(pb, pg))
    G.pose(t0, loc=pg, rot=facing(pg, pb))
    lips(G, t0, t1)
    ks = guests(t0, t1, "smile")
    for k in ks:
        k.face(t0 + 0.6, eyes="happy", mouth="open_smile")
    cam = Cam()
    cam.push(t0, t1, up(pg, 4.6), 6.5, 5.0, yaw=60, pitch=2, lens=30, yaw1=48)
    cam.handheld(0.8)
    sfx(t0 + 0.6, "aww", 0.6)


@S(20, 78, 81, "My uncle: on the couch with his dog")
def s20(t0, t1):
    living()
    U = uncle(t0, t1, "happy")
    sit_on(U, t0, (-2.5, 6.4, 2.2), rot=0)
    U.act(t0 + 0.1, "wave")
    d = W.dog("dog", (3.0, 1.0, 0))
    d.rotation_euler[2] = math.radians(-30)
    cam = Cam()
    cam.push(t0, t1, (0, 5, 3.5), 15, 12, yaw=-12, pitch=10, lens=22, yaw1=6, fstop=6)
    cam.handheld(1.0)


@S(21, 81, 86, "...squeezing on the dog's tiny booties, swap!")
def s21(t0, t1):
    living()
    U = uncle(t0, t1, "grin")
    p = (0, 0.5, 0)
    U.pose(t0, loc=p, rot=0, hipz=-0.7, legL=(60, 10), legR=(60, -10), torso=(0, 20, 0), armL=(70, -10), armR=(70, -10))
    for piv in (U.hpL, U.hpR):
        b = box(U.name + piv.name + "_bootie", (1.1, 1.3, 0.7), (0, -0.2, -1.7), M("#f09ac2", 0.6), 0.25, parent=piv, coll=U.coll)
        b.scale = (0.4, 0.4, 0.4)
        b.keyframe_insert("scale", frame=F(t0 + 0.2))
        b.scale = (1, 1, 1)
        b.keyframe_insert("scale", frame=F(t0 + 0.6))
    d = W.dog("dog", (4.0, 0.0, 0))
    d.rotation_euler[2] = math.radians(-80)
    ts = w(85)
    swap_fx("dsw", up(p, 3.8), (4.0, -1.5, 2.2), ts, 0.4, 0.8)
    U.face(ts + 0.45, "shock")
    cam = Cam()
    cam.push(t0, t1, (1.6, 0.3, 2.4), 11, 8, yaw=-10, pitch=12, lens=24, yaw1=8)
    cam.crash(ts + 0.4, 24, 30, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.3, "rip", 0.4)


@S(22, 86, 91, "He barked for a week: uncle on all fours, dog in the armchair")
def s22(t0, t1):
    living()
    U = uncle(t0, t1, "happy")
    on_all_fours(U, t0, (-1.5, -1.0, 0), rot=20)
    U.face(t0, eyes="happy", mouth="open_smile")
    for i in range(4):
        tb = t0 + 0.12 + i * 0.32
        U.face(tb, eyes="wide", mouth="scream")
        U.face(tb + 0.14, eyes="happy", mouth="open_smile")
        U.pose(tb, head=(0, -80, 0))
        U.pose(tb + 0.14, head=(0, -66, 0))
        sfx(tb, "bark", 0.8)
    d = W.dog("dog", (2.5, 6.0, 1.4))
    d.rotation_euler[2] = math.radians(0)
    noise(U.root, "rotation_euler", 2, 0.15, 6)
    cam = Cam()
    cam.key(t0, (-4, -11, 2.0), (0, 2, 2.2), lens=22, focus=10.0, fstop=5)
    cam.key(t1, (1.5, -10, 1.6), (0, 2, 2.0), lens=22, focus=9.0, fstop=5)
    cam.handheld(1.2)


# ================================================================== LEO + PRUITT
LEO_P = (-14.0, -22.0, 0.0)


@S(23, 91, 93, "I'm Leo: crash zoom, wave")
def s23(t0, t1):
    hood()
    L = leo_c(t0, t1, "grin")
    L.pose(t0, loc=LEO_P, rot=-15)
    L.act(t0, "wave")
    cam = Cam()
    cam.whip(t0, t0 + 0.12, orbit_pos(up(LEO_P, 4.0), 9, 40, 6), up(LEO_P, 8), orbit_pos(up(LEO_P, 4.2), 7.5, -10, 4),
             up(LEO_P, 4.2), lens=26)
    cam.key(t1, orbit_pos(up(LEO_P, 4.4), 6.0, -15, 4), up(LEO_P, 4.4), lens=28)
    cam.handheld(1.0)


@S(24, 93, 96, "I'm 11: grin, thumbs up")
def s24(t0, t1):
    hood()
    L = leo_c(t0, t1, "grin")
    L.pose(t0, loc=LEO_P, rot=-15)
    L.act(t0, "fists")
    L.face(t0, eyes="happy", mouth="grin")
    L.jump(t0 + 0.2, 1.0, 0.4)
    cam = Cam()
    cam.orbit(t0, t1, up(LEO_P, 4.0), 6.8, -40, -5, pitch=4, lens=26, fstop=3)
    cam.handheld(0.8)
    sfx(t0 + 0.3, "boing", 0.4)


@S(25, 96, 102, "Nobody has ever touched my sneakers: glowing sneakers insert")
def s25(t0, t1):
    hood()
    L = leo_c(t0, t1, "smug")
    L.pose(t0, loc=LEO_P, rot=-15)
    L.pose(t0 + 0.3, legR=(25, 0))
    L.pose(t0 + 0.6, legR=(0, 0))
    sparkle_on("snk", (LEO_P[0], LEO_P[1] - 0.5, 0.6), t0 + 0.4, 1.6, 14)
    lt = light("snk_glow", "POINT", (LEO_P[0], LEO_P[1] - 2.5, 1.5), 500, (1.0, 0.85, 0.85), 1.0)
    cam = Cam()
    cam.key(t0, (LEO_P[0] - 4.0, LEO_P[1] - 9.5, 0.9), (LEO_P[0], LEO_P[1] - 0.4, 0.6), lens=32, focus=10.0, fstop=3)
    cam.key(w(99), (LEO_P[0] + 2.0, LEO_P[1] - 8.0, 1.0), (LEO_P[0], LEO_P[1] - 0.4, 0.7), lens=32, focus=8.2, fstop=3)
    cam.key(t1, (LEO_P[0] + 2.5, LEO_P[1] - 7.5, 4.2), (LEO_P[0], LEO_P[1], 4.0), lens=30, focus=7.8, fstop=3)
    cam.handheld(0.9)
    sfx(t0 + 0.4, "sparkle", 0.8)


@S(26, 102, 105, "Next door: whip to the grey house over the fence")
def s26(t0, t1):
    hood()
    L = leo_c(t0, t1, "worried")
    L.pose(t0, loc=LEO_P, rot=facing(LEO_P, (6, 14)))
    cam = Cam()
    cam.whip(t0 + 0.1, t0 + 0.32, orbit_pos(up(LEO_P, 4.2), 7, -30, 4), up(LEO_P, 4.2), (-6, -30, 5), (6, 14, 5), lens=22)
    cam.key(t1, (-4, -26, 4.5), (6, 14, 5.2), lens=22, focus=40.0, fstop=8)
    cam.handheld(1.0)
    sfx(t0 + 0.5, "crickets", 0.4)


@S(27, 105, 107, "MR. PRUITT: crash zoom on the porch")
def s27(t0, t1):
    hood(chair=True, boots=False)
    P = pruitt(t0, t1, "angry")
    p = (8.0, 12.6, PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    P.act(t0, "cross")
    cam = Cam()
    cam.push(t0, t1, up(p, 4.4), 16, 7, yaw=-6, pitch=-6, lens=26)
    cam.crash(t0 + 0.05, 20, 30, 0.1)
    cam.handheld(1.4)
    sfx(t0 + 0.05, "whoosh")
    sfx(t0 + 0.15, "thud", 0.6)


@S(28, 107, 111, "Grumpiest man alive: fist shake, storm face")
def s28(t0, t1):
    hood(chair=True, boots=False)
    P = pruitt(t0, t1, "furious")
    p = (8.0, 12.6, PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    wiggle(P, t0, t1, "armR", (12, 8), 8.0, (120, 10))
    P.pose(t0, armL=(10, 4))
    lips(P, t0, t1, "shout")
    cam = Cam()
    cam.push(t0, t1, up(p, 4.6), 5.6, 4.6, yaw=10, pitch=-10, lens=28, yaw1=-6)
    cam.handheld(2.2)
    sfx(t0 + 0.1, "zombie", 0.5)


@S(29, 111, 116, "He's worn the same: Pruitt stomping down the steps")
def s29(t0, t1):
    hood(chair=True, boots=False)
    P = pruitt(t0, t1, "angry")
    P.walk(t0, t1, (6, 12.6, PORCH_Z), (6, 8.0, 0), rate=1.8)
    cam = Cam()
    cam.key(t0, (14, 2, 3.0), (6, 12, 3.5), lens=24, focus=11.0, fstop=4)
    cam.key(t1, (11, 0, 2.2), (6, 8, 2.5), lens=24, focus=9.0, fstop=4)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "footsteps", 0.6)


@S(30, 116, 120, "Brown boots, 40 years: dusty boot close-up, flies")
def s30(t0, t1):
    hood(chair=True, boots=False)
    P = pruitt(t0, t1, "angry")
    p = (6, 8.5, 0)
    P.pose(t0, loc=p, rot=0)
    P.pose(t0 + 0.2, legL=(20, 0)); P.pose(t0 + 0.4, legL=(0, 0))
    Mf = M("#151515", 0.5)
    for i in range(3):
        f = sphere(f"fly{i}", 0.08, (p[0] + 0.5 * i - 0.5, p[1] - 1.2, 1.8 + 0.3 * i), Mf, seg=8)
        for ax in range(3):
            noise(f, "location", ax, 0.6, 4)
    Md = mat("bootdust", hexc("#c8b89a"), 0.9, alpha=0.6)
    for i in range(8):
        d = sphere(f"bdust{i}", 0.3, (p[0] + random.uniform(-1, 1), p[1] - 0.5, 0.3), Md, seg=8)
        d.scale = (0.01,) * 3
        d.keyframe_insert("scale", frame=F(t0 + 0.38))
        d.scale = (1.2,) * 3
        d.location = (d.location[0] * 1.0 + random.uniform(-1.5, 1.5), d.location[1] - 0.8, 0.8)
        d.keyframe_insert("scale", frame=F(t0 + 0.8)); d.keyframe_insert("location", frame=F(t0 + 0.8))
    cam = Cam()
    cam.key(t0, (p[0] - 3, p[1] - 5.5, 0.6), (p[0], p[1], 0.8), lens=32, focus=6.2, fstop=2.4)
    cam.key(t1, (p[0] + 2, p[1] - 4.0, 0.9), (p[0], p[1], 0.9), lens=32, focus=4.5, fstop=2.4)
    cam.handheld(1.0)
    sfx(t0 + 0.4, "stomp", 0.8)


@S(31, 120, 123, "Every ball: a ball sails over the fence")
def s31(t0, t1):
    hood()
    b = soccer_ball("ball", (0, -26, 0.6))
    ball_fly(b, t0, t1 + 0.4, (-2, -27, 0.6), (5, -2, 0.6), h=7)
    k = townie(7, t0, t1, "happy")
    k.pose(t0, loc=(-1, -30, 0), rot=facing((-1, -30), (5, -2)))
    k.pose(t0, legR=(-30, 0)); k.pose(t0 + 0.12, legR=(60, 0)); k.pose(t0 + 0.4, legR=(0, 0))
    k.face(t0 + 0.4, "gasp")
    cam = Cam()
    cam.key(t0, (-12, -37, 3), (-1, -27, 2.5), lens=24, focus=14.0, fstop=6)
    cam.key(t1, (-13, -33, 6), (3, -10, 6), lens=24, focus=24.0, fstop=6)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "bonk", 0.6)
    sfx(t0 + 0.12, "whoosh", 0.7)


@S(32, 123, 127, "Lands in his yard: bounce bounce")
def s32(t0, t1):
    hood()
    b = soccer_ball("ball", (5, -2, 0.6))
    ball_fly(b, t0 - 0.4, t0, (0, -16, 6.0), (5, -2, 0.6), h=1.5)
    bounce(b, t0, (5, -2, 0.6), (6, 4, 0.6))
    cam = Cam()
    cam.key(t0, (10, -10, 2.5), (5, -2, 1.2), lens=26, focus=9.0, fstop=3.5)
    cam.key(t1, (11, -6, 2.0), (6, 3, 1.0), lens=26, focus=9.0, fstop=3.5)
    cam.handheld(1.0)
    sfx(t0, "thud", 0.7)
    sfx(t0 + 0.35, "thud", 0.4)


@S(33, 127, 129, "Disappears forever: the door snatches it, slam")
def s33(t0, t1):
    hood(boots=False)
    P = pruitt(t0, t1, "angry")
    b = soccer_ball("ball", (6, 9.5, 0.6))
    P.pose(t0, loc=(6, 13.0, PORCH_Z), rot=0)
    P.act(t0, "reach")
    b.keyframe_insert("location", frame=F(t0 + 0.1))
    b.location = (6, 14.0, 3.0)
    b.keyframe_insert("location", frame=F(t0 + 0.35))
    W2.vanish(P, t0 + 0.42, extra=[b] + list(b.children))
    W2.poof("pf", (6, 14.5, 3.2), t0 + 0.42, 0.7)
    cam = Cam()
    cam.push(t0, t1, (6, 12, 3.4), 12, 9, yaw=12, pitch=6, lens=24)
    cam.crash(t0 + 0.42, 24, 30, 0.08)
    cam.handheld(1.3)
    sfx(t0 + 0.42, "door")


@S(34, 129, 134, "Last Tuesday: Leo with his shiny new ball on the street")
def s34(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy")
    p = (-6, -27, 0)
    L.pose(t0, loc=p, rot=facing(p, (5, -2)))
    b = soccer_ball("ball", (p[0] + 0.6, p[1] - 1.5, 0.6))
    bounce(b, t0, (p[0] + 0.6, p[1] - 1.5, 0.6), (p[0] + 0.6, p[1] - 1.5, 0.6), hops=(1.4, 1.4, 1.4), dt=(0.4, 0.4, 0.4))
    sparkle_on("nb", (p[0] + 0.6, p[1] - 1.5, 1.2), t0 + 0.1, 1.2, 10)
    L.pose(t0 + 0.2, legR=(35, 0)); L.pose(t0 + 0.4, legR=(0, 0))
    L.pose(t0 + 0.6, legL=(35, 0)); L.pose(t0 + 0.8, legL=(0, 0))
    cam = Cam()
    cam.orbit(t0, t1, up(p, 2.6), 9, 200, 160, pitch=8, lens=24, fstop=4)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "sparkle", 0.6)


@S(35, 134, 138, "Brand new soccer ball: Leo kicks, it sails over the fence, his face drops")
def s35(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy")
    p = (-6, -27, 0)
    L.pose(t0, loc=p, rot=facing(p, (5, -2)))
    tk = t0 + 0.2
    L.pose(tk - 0.15, legR=(-40, 0)); L.pose(tk + 0.08, legR=(80, 0), armL=(60, 20)); L.pose(tk + 0.5, legR=(0, 0))
    b = soccer_ball("ball", (p[0] + 0.5, p[1] + 1.0, 0.6))
    ball_fly(b, tk, tk + 1.1, (p[0] + 0.5, p[1] + 1.0, 0.6), (5, -2, 0.6), h=8)
    L.face(tk + 0.7, "shock")
    L.act(tk + 0.7, "hands_head")
    cam = Cam()
    fy = facing(p, (5, -2))
    cam.key(t0, orbit_pos(up(p, 3.0), 8, fy + 160, 8), (0, -14, 4), lens=24, focus=10.0, fstop=6)
    cam.key(tk + 0.75, orbit_pos(up(p, 3.0), 8.5, fy + 170, 10), (2, -8, 5), lens=24, focus=14.0, fstop=6)
    cam.key(t1, orbit_pos(up(p, 4.4), 5.5, fy + 10, 2), up(p, 4.4), lens=28, focus=5.5, fstop=3)
    cam.handheld(1.3)
    sfx(tk, "bonk", 0.7)
    sfx(tk + 0.7, "gasp", 0.6)


@S(36, 138, 142, "The big kid: towering, smirking")
def s36(t0, t1):
    hood()
    K = big_kid(t0, t1, "smug")
    p = (-3, -29, 0)
    K.pose(t0, loc=p, rot=facing(p, (-8, -27)))
    K.act(t0, "cross")
    for i in (7, 8):
        k = townie(i, t0, t1, "smug")
        q = (p[0] + (i - 7.5) * 6, p[1] - 3, 0)
        k.pose(t0, loc=q, rot=facing(q, (-8, -27)))
    cam = Cam()
    cam.push(t0, t1, up(p, 5.8), 10, 8, yaw=-120, pitch=-14, lens=24, yaw1=-100)
    cam.handheld(1.0)


@S(37, 142, 145, "Wear Pruitt's boots: points at the porch")
def s37(t0, t1):
    hood()
    K = big_kid(t0, t1, "smug")
    p = (-3, -29, 0)
    K.pose(t0, loc=p, rot=facing(p, (-8, -27)))
    lips(K, t0, t1)
    K.pose(t0 + 0.15, rot=facing(p, (6, 12)))
    K.act(t0 + 0.15, "point")
    cam = Cam()
    cam.whip(t0 + 0.4, t0 + 0.6, orbit_pos(up(p, 5.8), 8, -105, -6), up(p, 5.8), (2, -6, 3.0), (BOOTS[0], BOOTS[1], 1.6), lens=26)
    cam.key(t1, (3, -1, 2.6), (BOOTS[0], BOOTS[1], 1.4), lens=30, focus=13.0, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.7, "zombie", 0.4)


@S(38, 145, 149, "Get it back yourself: Leo gulps")
def s38(t0, t1):
    hood()
    L = leo_c(t0, t1, "scared")
    p = (-8, -27, 0)
    L.pose(t0, loc=p, rot=facing(p, (-3, -29)))
    L.act(t0, "shrug")
    L.face(t0 + 0.4, eyes="worried", mouth="wavy")
    L.look(t0 + 0.5, 30, -10)
    cam = Cam()
    cam.push(t0, t1, up(p, 4.4), 6.5, 4.4, yaw=facing(p, (-3, -29)) + 10, pitch=4, lens=30)
    cam.handheld(1.2)
    sfx(t0 + 0.5, "gasp", 0.5)


# ================================================================== THE SWAP
@S(39, 149, 155, "His boots sat on the porch: hero push on the boots")
def s39(t0, t1):
    hood()
    sparkle_on("bt", (BOOTS[0], BOOTS[1], 1.5), t0 + 0.2, 1.4, 8)
    lt = light("bt_spot", "SPOT", (BOOTS[0], BOOTS[1] - 2, 7.5), 2500, (1.0, 0.92, 0.75), 0.4, target=BOOTS, spot=35)
    cam = Cam()
    cam.key(t0, (BOOTS[0] - 3.5, BOOTS[1] - 9, 1.6), (BOOTS[0], BOOTS[1], 1.3), lens=28, focus=9.6, fstop=2.4)
    cam.key(t1, (BOOTS[0] - 0.5, BOOTS[1] - 4.2, 1.5), (BOOTS[0], BOOTS[1], 1.0), lens=30, focus=4.3, fstop=2.4)
    cam.handheld(0.8)
    sfx(t0 + 0.2, "rise", 0.6)


@S(40, 155, 161, "Asleep in his chair, rocking, Zzz")
def s40(t0, t1):
    hood()
    P = pruitt(t0, t1, "sleepy", feet="socks")
    sit_on(P, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0, head=(0, 18, 8))
    P.face(t0, eyes="closed", mouth="wavy")
    rk = D.objects["rock"]
    for i in range(5):
        tt = t0 + i * 0.45
        for ob in (rk, P.root):
            ob.rotation_euler[0] = math.radians(5 if i % 2 else -5)
            ob.keyframe_insert("rotation_euler", index=0, frame=F(tt))
    zzz(P, t0, t1)
    cam = Cam()
    cam.orbit(t0, t1, (CHAIR[0], CHAIR[1], 4.6), 9, -35, -10, pitch=6, lens=26, fstop=3.5)
    cam.handheld(0.8)
    sfx(t0 + 0.2, "snort", 0.7)


@S(41, 161, 163, "In socks: toes wiggle")
def s41(t0, t1):
    hood()
    P = pruitt(t0, t1, "sleepy", feet="socks")
    sit_on(P, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0)
    for i in range(4):
        P.pose(t0 + i * 0.15, legL=(85 + (8 if i % 2 else -8), 3), legR=(85 + (-8 if i % 2 else 8), -3))
    f = (CHAIR[0], CHAIR[1] - 2.0, 2.4)
    cam = Cam()
    cam.key(t0, (f[0] - 3.5, f[1] - 7.0, 2.0), f, lens=30, focus=7.8, fstop=3)
    cam.key(t1, (f[0] + 2.0, f[1] - 6.5, 2.2), f, lens=32, focus=6.8, fstop=3)
    cam.handheld(0.9)
    sfx(t0 + 0.1, "snort", 0.5)


@S(42, 163, 166, "I stepped in: Leo tiptoes into the boots")
def s42(t0, t1):
    hood(boots=True)
    P = pruitt(t0, t1, "sleepy", feet="socks")
    sit_on(P, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0, head=(0, 18, 8))
    P.face(t0, eyes="closed", mouth="wavy")
    L = leo_c(t0, t1, "determined", feet="socks")
    L.walk(t0, t0 + 0.5, (BOOTS[0] - 2.5, BOOTS[1] - 1.2, PORCH_Z), (BOOTS[0], BOOTS[1], PORCH_Z), rate=2.0)
    L.pose(t0 + 0.5, rot=0, legL=(40, 0), hipz=0.5)
    L.pose(t0 + 0.8, legL=(0, 0), hipz=0.0)
    L.face(t0 + 0.8, eyes="closed", mouth="grimace")
    cam = Cam()
    cam.key(t0, (BOOTS[0] - 7, BOOTS[1] - 10, 2.0), (BOOTS[0] - 1, BOOTS[1], 2.0), lens=24, focus=11.5, fstop=4)
    cam.key(t1, (BOOTS[0] - 3, BOOTS[1] - 8.5, 1.6), (BOOTS[0], BOOTS[1], 1.6), lens=26, focus=9.0, fstop=4)
    cam.handheld(1.0)
    sfx(t0 + 0.8, "place", 0.8)


@S(43, 166, 167, "CRACK! souls swap porch-wide, white flash")
def s43(t0, t1):
    hood(boots=False)
    P = pruitt(t0, t1, "sleepy", feet="socks")
    sit_on(P, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0, head=(0, 18, 8))
    L = leo_c(t0, t1, "terror", feet="boots")
    L.pose(t0, loc=(BOOTS[0], BOOTS[1], PORCH_Z), rot=0)
    L.act(t0, "brace")
    swap_fx("cr", up(BOOTS, 4.6), (CHAIR[0], CHAIR[1] - 0.3, CHAIR[2] + 4.2), t0 - 0.05, 0.35, 1.3, snd=False)
    cam = Cam()
    cam.key(t0, (7, 1, 4.5), (7, 13, 4.0), lens=22, roll=-8)
    cam.key(t1, (7, 4, 4.6), (7, 13, 4.2), lens=22, roll=6)
    cam.crash(t0, 18, 28, 0.1)
    cam.handheld(3.0)
    sfx(t0, "crack")
    sfx(t0 + 0.02, "glitch", 0.8)
    sfx(t0 + 0.05, "boom", 0.5)


@S(44, 167, 172, "Knees popping like popcorn: old body, hunched")
def s44(t0, t1):
    hood(boots=False)
    P = pruitt(t0, t1, "terror")
    p = (BOOTS[0], BOOTS[1], PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    hunch(P, t0)
    P.face(t0, eyes="terror", mouth="grimace_wide")
    for i in range(3):
        tt = w(169) + i * 0.3
        P.pose(tt, legL=(25 if i % 2 == 0 else 0, 0), legR=(0 if i % 2 == 0 else 25, 0), hipz=-0.4)
        P.pose(tt + 0.15, legL=(0, 0), legR=(0, 0), hipz=-0.2)
        popcorn(f"pc{i}", (p[0] + (0.5 if i % 2 else -0.5), p[1] - 0.8, p[2] + 1.6), tt, 3, seed=i)
    cam = Cam()
    cam.key(t0, (p[0] + 3.5, p[1] - 6, 2.2), (p[0], p[1], 2.2), lens=26, focus=7.0, fstop=3)
    cam.key(t1, (p[0] - 1.5, p[1] - 6.5, 2.8), (p[0], p[1], 2.8), lens=26, focus=6.7, fstop=3)
    cam.handheld(1.4)


@S(45, 172, 175, "I was 78: stares at wrinkly hands, crash zoom")
def s45(t0, t1):
    hood(boots=False)
    P = pruitt(t0, t1, "shock")
    p = (BOOTS[0], BOOTS[1], PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    hunch(P, t0)
    P.pose(t0 + 0.1, armL=(85, -25), armR=(85, -25), head=(0, 26, 0))
    P.face(t0 + 0.1, eyes="down", mouth="o")
    P.face(w(174), "terror")
    P.look(w(174), 0, -6)
    cam = Cam()
    cam.push(t0, t1, up(p, 4.0), 6, 4.6, yaw=15, pitch=-2, lens=28)
    cam.crash(w(174), 28, 38, 0.08)
    cam.handheld(1.6)
    sfx(w(174), "buzzer", 0.4)


@S(46, 175, 182, "On his chair, rubbing his eyes...")
def s46(t0, t1):
    hood(boots=False)
    L = leo_c(t0, t1, "sleepy", feet="socks")
    sit_on(L, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0)
    wiggle(L, t0 + 0.4, t1, "armL", (8, 6), 6.0, (140, -25))
    wiggle(L, t0 + 0.45, t1, "armR", (8, 6), 6.0, (140, -25))
    L.face(t0 + 0.4, eyes="closed", mouth="yawn")
    cam = Cam()
    cam.push(t0, t1, (CHAIR[0], CHAIR[1], 3.6), 12, 7, yaw=-30, pitch=8, lens=24, yaw1=-15)
    cam.handheld(1.0)
    sfx(t0 + 0.4, "snort", 0.5)


@S(47, 182, 184, "...was ME: crash zoom on Leo's body opening its eyes")
def s47(t0, t1):
    hood(boots=False)
    L = leo_c(t0, t1, "smug", feet="socks")
    sit_on(L, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0)
    L.face(t0, eyes="half", mouth="smirk")
    L.face(t0 + 0.2, eyes="wide", mouth="smirk")
    q = (CHAIR[0], CHAIR[1], CHAIR[2] + 4.2)
    cam = Cam()
    cam.push(t0, t1, q, 6.5, 4.5, yaw=0, pitch=2, lens=26)
    cam.crash(t0 + 0.05, 20, 32, 0.08)
    cam.handheld(1.5)
    sfx(t0 + 0.05, "whoosh", 0.8)
    sfx(t0 + 0.12, "ding", 0.5)


@S(48, 184, 190, "'Well,' said me, in my voice: Leo-body stands, cocky")
def s48(t0, t1):
    hood(boots=False)
    L = leo_c(t0, t1, "smug", feet="socks")
    sit_on(L, t0, (CHAIR[0], CHAIR[1], CHAIR[2] + 1.42), rot=0)
    L.pose(t0 + 0.6, loc=(CHAIR[0] - 0.5, CHAIR[1] - 2.2, PORCH_Z), legL=(0, 0), legR=(0, 0), armL=(5, 6), armR=(5, 6),
           rot=facing((CHAIR[0], CHAIR[1] - 2.2), BOOTS))
    lips(L, t0, t1)
    L.act(t0 + 0.9, "cross")
    P = pruitt(t0, t1, "shock")
    P.pose(t0, loc=(BOOTS[0], BOOTS[1], PORCH_Z), rot=facing(BOOTS, CHAIR))
    hunch(P, t0)
    cam = Cam()
    cam.key(t0, (CHAIR[0] - 11, CHAIR[1] - 7, 4.0), (CHAIR[0] - 1, CHAIR[1] - 1, 4.0), lens=24, focus=11.0, fstop=4)
    cam.key(t1, (CHAIR[0] - 9, CHAIR[1] - 8, 4.6), (CHAIR[0] - 1.5, CHAIR[1] - 1.5, 4.4), lens=26, focus=10.0, fstop=4)
    cam.handheld(1.0)


@S(49, 190, 191, "'Finally.' huge grin, close")
def s49(t0, t1):
    hood(boots=False)
    L = leo_c(t0, t1, "grin", feet="socks")
    p = (CHAIR[0] - 0.5, CHAIR[1] - 2.2, PORCH_Z)
    L.pose(t0, loc=p, rot=-10)
    L.face(t0, eyes="happy", mouth="grin")
    L.act(t0, "fists")
    cam = Cam()
    cam.push(t0, t1, up(p, 4.6), 5.0, 4.0, yaw=-10, pitch=0, lens=30)
    cam.crash(t0, 30, 36, 0.1)
    cam.handheld(1.2)
    sfx(t0, "sparkle", 0.5)


@S(50, 191, 197, "Then me ran out the door: Leo-body sprints off the porch, old me reaches")
def s50(t0, t1):
    hood(boots=False)
    L = leo_c(t0, t1, "joy", feet="socks")
    p0 = (CHAIR[0] - 0.5, CHAIR[1] - 2.2, PORCH_Z)
    L.pose(t0, loc=p0)
    L.run(t0 + 0.1, t1, p0, (-6, -24, 0), rate=4.4)
    P = pruitt(t0, t1, "terror")
    P.pose(t0, loc=(BOOTS[0], BOOTS[1], PORCH_Z), rot=180 + 30)
    hunch(P, t0)
    P.act(t0 + 0.6, "reach")
    lips(P, t0 + 0.6, t1, "shout")
    cam = Cam()
    cam.track(L, t0, t1, offset=(5.0, -7.0, 2.5), look_up=3.5, lens=22, step=0.3, fstop=5)
    cam.handheld(1.5)
    sfx(t0 + 0.1, "whoosh", 0.8)
    sfx(t0 + 0.2, "footsteps", 0.6)


# ================================================================== INSIDE
@S(51, 197, 200, "I limped inside: old body hobbles in the doorway")
def s51(t0, t1):
    ball_room(window_light=False)
    P = pruitt(t0, t1, "worried")
    P.walk(t0, t1, (11.5, -4, 0), (8.5, -3, 0), rate=1.2, swing=14, arm=8)
    hunch(P, t0)
    hunch(P, t1)
    cam = Cam()
    cam.key(t0, (3, -11, 4.5), (10, -3.5, 3.8), lens=24, focus=10.0, fstop=3)
    cam.key(t1, (3.5, -9.5, 4.2), (8.5, -3, 3.8), lens=24, focus=8.0, fstop=3)
    cam.handheld(1.0)
    sfx(t0, "door", 0.5)
    sfx(t0 + 0.3, "crack", 0.3)


@S(52, 200, 204, "...to find my ball: peering into the dark room")
def s52(t0, t1):
    ball_room(window_light=False)
    P = pruitt(t0, t1, "sus")
    p = (8.0, -3, 0)
    P.pose(t0, loc=p, rot=facing(p, (0, 8)))
    hunch(P, t0)
    P.look(t0 + 0.2, -40, 0)
    P.look(t0 + 0.7, 30, 0)
    cam = Cam()
    cam.push(t0, t1, up(p, 4.0), 6.0, 5.0, yaw=facing(p, (0, 8)) - 10, pitch=4, lens=28, yaw1=facing(p, (0, 8)) + 20)
    cam.handheld(1.0)


@S(53, 204, 209, "I found all of them: shelves REVEAL, lights up")
def s53(t0, t1):
    ball_room()
    P = pruitt(t0, t1, "gasp")
    p = (3, -4, 0)
    P.pose(t0, loc=p, rot=facing(p, (0, 9)))
    hunch(P, t0)
    P.act(t0 + 0.3, "recoil", expr="shock")
    cam = Cam()
    cam.key(t0, (6, -12, 4.0), (3, -2, 4.4), lens=24, focus=10.0, fstop=4)
    cam.key(t1, (2, -12, 7.0), (0, 9, 5.5), lens=20, focus=20.0, fstop=8)
    cam.handheld(0.9)
    sfx(t0 + 0.3, "rise", 0.8)
    sfx(t0 + 0.6, "sparkle", 0.5)


@S(54, 209, 214, "Hundreds of balls on shelves: tracking along the wall")
def s54(t0, t1):
    ball_room()
    cam = Cam()
    cam.key(t0, (-9, 3.5, 3.0), (-6, 9.3, 4.0), lens=24, focus=6.5, fstop=3, interp="LINEAR")
    cam.key(t1, (6, 3.0, 7.5), (9, 9.3, 7.0), lens=24, focus=6.5, fstop=3)
    cam.handheld(0.6)


@S(55, 214, 219, "Each with a little label: macro on a label")
def s55(t0, t1):
    ball_room()
    lc = label_card("lab0", "GREEN\n1987", (-0.5, 8.3, 4.35), rot=(90, 0, 0), s=0.45)
    cam = Cam()
    cam.key(t0, (-1.6, 5.8, 5.2), (-0.5, 8.4, 4.9), lens=32, focus=3.0, fstop=2.0)
    cam.key(t1, (0.6, 6.4, 5.0), (-0.5, 8.4, 4.7), lens=34, focus=2.2, fstop=2.0)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "paper", 0.5)


def ball_insert(t0, t1, col, label, yaw=-15, seed=0):
    world((0.45, 0.4, 0.38), 0.25)
    ball_room()
    b = sphere("hero_ball", 0.9, (0, 4.0, 1.3), M(col, 0.3), seg=24)
    box("hero_shelf", (4, 2.4, 0.3), (0, 4.0, 0.25), wood("br_wood", "#6a4426", "#7d5230", 2.0), 0.03)
    label_card("lab", label, (0, 2.8, 0.5), rot=(70, 0, 0), s=0.75)
    light("hero_l", "SPOT", (2, 1, 6), 1500, (1.0, 0.92, 0.8), 0.5, target=(0, 4, 1), spot=40)
    cam = Cam()
    cam.key(t0, orbit_pos((0, 3.6, 1.0), 6.0, yaw, 22), (0, 3.6, 1.0), lens=30, focus=6.0, fstop=2.8)
    cam.key(t1, orbit_pos((0, 3.6, 1.0), 4.6, -yaw, 26), (0, 3.6, 1.0), lens=30, focus=4.6, fstop=2.8)
    cam.handheld(0.7)
    return b


@S(56, 219, 222, "RED BALL, 1994")
def s56(t0, t1):
    ball_insert(t0, t1, "#e8423a", "RED BALL\n1994", -18)
    sfx(t0, "whoosh", 0.5)


@S(57, 222, 225, "BLUE BALL, 2008")
def s57(t0, t1):
    ball_insert(t0, t1, "#3f7fd9", "BLUE BALL\n2008", 18)
    sfx(t0, "whoosh", 0.5)


@S(58, 225, 228, "LEO'S BALL, TUESDAY: my soccer ball, warm light")
def s58(t0, t1):
    world((0.45, 0.4, 0.38), 0.25)
    ball_room()
    soccer_ball("hero_ball", (0, 4.0, 1.3), 0.9)
    box("hero_shelf", (4, 2.4, 0.3), (0, 4.0, 0.25), wood("br_wood", "#6a4426", "#7d5230", 2.0), 0.03)
    label_card("lab", "LEO'S BALL\nTUESDAY", (0, 2.8, 0.5), rot=(70, 0, 0), s=0.75)
    light("hero_l", "SPOT", (2, 1, 6), 2200, (1.0, 0.88, 0.7), 0.5, target=(0, 4, 1), spot=40)
    sparkle_on("lb", (0, 3.8, 1.6), t0 + 0.1, 1.4, 10)
    cam = Cam()
    cam.key(t0, orbit_pos((0, 3.6, 1.0), 7.0, 0, 20), (0, 3.6, 1.0), lens=30, focus=7.0, fstop=2.8)
    cam.key(t1, orbit_pos((0, 3.6, 1.0), 4.2, 0, 24), (0, 3.6, 1.0), lens=30, focus=4.2, fstop=2.8)
    cam.handheld(0.7)
    sfx(t0 + 0.1, "sparkle", 0.6)


@S(59, 228, 235, "Beside them: a lonely armchair by the window, dust in the light")
def s59(t0, t1):
    ball_room()
    cam = Cam()
    cam.key(t0, (-2, 5, 6.5), (-9.5, -2, 2.4), lens=24, focus=10.0, fstop=3)
    cam.key(t1, (-3.5, 2.5, 5.0), (-9.5, -2, 2.4), lens=26, focus=7.0, fstop=3)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "wind", 0.4)


@S(60, 235, 238, "Facing the yard: through the window frame, kids playing outside")
def s60(t0, t1):
    hood()
    for i in range(4):
        k = townie(30 + i, t0, t1, "joy")
        q = (-4 + i * 4.5, -26 - (i % 2) * 2, 0)
        k.pose(t0, loc=q, rot=facing(q, (0, 16)))
        k.jump(t0 + 0.1 + i * 0.15, 1.2, 0.45)
    b = soccer_ball("ball", (2, -27, 0.6))
    ball_fly(b, t0, t1, (-2, -26, 0.6), (8, -28, 0.6), h=3)
    Mf = M("#3a2a20", 0.7)
    fc = (0.0, 15.2, 5.0)
    for k2, (sz, off) in enumerate((((5.0, 0.3, 0.35), (0, 0, 2.0)), ((5.0, 0.3, 0.35), (0, 0, -2.0)),
                                     ((0.35, 0.3, 4.4), (-2.4, 0, 0)), ((0.35, 0.3, 4.4), (2.4, 0, 0)),
                                     ((0.2, 0.3, 4.2), (0, 0, 0)), ((4.8, 0.3, 0.2), (0, 0, 0.3)))):
        box(f"wf{k2}", sz, (fc[0] + off[0], fc[1] + off[1], fc[2] + off[2]), Mf, 0.02)
    for nm in ("ph_body", "ph_roof", "ph_roof2", "ph_win0", "ph_wfr0", "ph_door", "ph_knob", "ph_win1", "ph_wfr1"):
        D.objects[nm].hide_render = True
    Mw = M("#5a4a3e", 0.85)
    box("iw_top", (30, 0.3, 10), (0, 15.4, 12.2), Mw, 0)
    box("iw_bot", (30, 0.3, 2.7), (0, 15.4, 1.35), Mw, 0)
    box("iw_l", (12, 0.3, 4.6), (-8.4, 15.4, 5.0), Mw, 0)
    box("iw_r", (12, 0.3, 4.6), (8.4, 15.4, 5.0), Mw, 0)
    cam = Cam()
    cam.key(t0, (1.3, 17.6, 5.0), (1.0, -20, 3.2), lens=20, focus=36.0, fstop=8)
    cam.key(t1, (1.1, 17.0, 4.9), (1.5, -20, 3.0), lens=21, focus=36.0, fstop=8)
    cam.handheld(0.5)
    sfx(t0 + 0.1, "kids_laugh", 0.4)


@S(61, 238, 242, "He wasn't stealing them: realization close-up")
def s61(t0, t1):
    ball_room()
    P = pruitt(t0, t1, "worried")
    p = (-5, 1, 0)
    P.pose(t0, loc=p, rot=facing(p, (-9, -2)))
    hunch(P, t0)
    P.face(t0 + 0.4, eyes="cry", mouth="frown")
    P.pose(t0 + 0.4, head=(0, 8, 0))
    cam = Cam()
    cam.push(t0, t1, up(p, 4.2), 5.6, 4.2, yaw=facing(p, (-9, -2)), pitch=0, lens=30)
    cam.handheld(0.7)
    sfx(t0 + 0.3, "aww", 0.4)


@S(62, 242, 251, "Waiting for someone to knock: the front door, nobody comes")
def s62(t0, t1):
    ball_room()
    lt = light("door_l", "SPOT", (6, -4, 11), 2000, (1.0, 0.9, 0.75), 0.5, target=(12.7, -4, 2.7), spot=30)
    cam = Cam()
    cam.key(t0, (2, -2, 5.0), (12.7, -4, 3.2), lens=22, focus=11.0, fstop=3)
    cam.key(t1, (7.5, -3.5, 3.8), (12.7, -4, 3.0), lens=26, focus=5.5, fstop=3)
    cam.handheld(0.5)
    sfx(t0 + 0.3, "crickets", 0.5)


# ================================================================== OUTSIDE
@S(63, 251, 258, "Outside, Mr. Pruitt was in my body: Leo-body dribbling on the street")
def s63(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy", feet="socks")
    L.run(t0, t1, (-14, -27, 0), (4, -29, 0), rate=3.6)
    b = soccer_ball("ball", (0, 0, 0))
    b.parent = L.root
    b.location = (0, -1.8, 0.6)
    noise(b, "location", 1, 0.4, 6)
    noise(b, "rotation_euler", 0, 3, 8)
    cam = Cam()
    cam.track(L, t0, t1, offset=(-2.0, -10.0, 3.0), look_up=3.0, lens=24, step=0.3, fstop=5)
    cam.handheld(1.2)
    sfx(t0, "kids_laugh", 0.6)


@S(64, 258, 264, "Playing soccer with the big kids: wide game, ball zipping")
def s64(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy", feet="socks")
    L.run(t0, t1, (-4, -26, 0), (6, -31, 0), rate=3.8)
    K = big_kid(t0, t1, "joy")
    K.run(t0, t1, (8, -33, 0), (2, -28, 0), rate=3.4)
    for i, (a, b2) in enumerate((((-10, -32, 0), (-3, -29, 0)), ((14, -27, 0), (8, -30, 0)))):
        k = townie(7 + i, t0, t1, "joy")
        k.run(t0, t1, a, b2, rate=3.6)
    ba = soccer_ball("ball", (0, -28, 0.6))
    ball_fly(ba, t0, t0 + 0.7, (-2, -27, 0.6), (6, -32, 0.6), h=2)
    ball_fly(ba, t0 + 0.7, t1, (6, -32, 0.6), (-4, -29, 0.6), h=3)
    cam = Cam()
    cam.orbit(t0, t1, (1, -29, 2.5), 17, -40, 10, pitch=24, lens=22, fstop=8)
    cam.handheld(1.0)
    sfx(t0 + 0.05, "bonk", 0.5)
    sfx(t0 + 0.75, "bonk", 0.5)


@S(65, 264, 265, "Running: low fast tracking sprint")
def s65(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy", feet="socks")
    L.run(t0, t1, (-10, -27, 0), (0, -27, 0), rate=5.0)
    cam = Cam()
    cam.track(L, t0, t1, offset=(3.0, -4.5, 1.0), look_up=3.0, lens=20, step=0.15, fstop=4)
    cam.handheld(2.0)
    sfx(t0, "whoosh", 0.7)


@S(66, 265, 266, "Laughing: big laugh close-up")
def s66(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy", feet="socks")
    p = (0, -27, 0)
    L.pose(t0, loc=p, rot=-20)
    laugh(L, t0, t1, flail=False)
    L.act(t0, "cheer")
    cam = Cam()
    cam.push(t0, t1, up(p, 4.6), 5.2, 4.2, yaw=-20, pitch=-6, lens=28, yaw1=-5)
    cam.handheld(1.4)
    sfx(t0, "kids_laugh", 0.7)


@S(67, 266, 272, "Hadn't run in 50 years: slow orbit, leaping goal celebration")
def s67(t0, t1):
    hood()
    L = leo_c(t0, t1, "joy", feet="socks")
    p = (0, -28, 0)
    L.pose(t0, loc=p, rot=0)
    L.jump(t0 + 0.2, 2.2, 0.6)
    L.jump(t0 + 1.0, 1.6, 0.5)
    laugh(L, t0, t1)
    for i in range(3):
        k = townie(7 + i, t0, t1, "joy")
        q = (p[0] - 5 + i * 5, p[1] - 4 - (i % 2) * 2, 0)
        k.pose(t0, loc=q, rot=facing(q, p))
        k.act(t0 + 0.3 + i * 0.1, "cheer")
    confetti("cf", (0, -28, 8), (6, 4, 2), t0 + 0.4, 1.6, 50, seed=2, fall=9)
    cam = Cam()
    cam.orbit(t0, t1, up(p, 4.0), 12, -60, 30, pitch=6, lens=22, fstop=4, pitch1=14)
    cam.handheld(0.8)
    sfx(t0 + 0.4, "cheer", 0.7)


@S(68, 272, 281, "I told him we had to swap back: old body confronts Leo-body")
def s68(t0, t1):
    hood()
    P = pruitt(t0, t1, "determined")
    L = leo_c(t0, t1, "happy", feet="socks")
    pp, pl = (-3, -24, 0), (1, -25.5, 0)
    P.pose(t0, loc=pp, rot=facing(pp, pl))
    L.pose(t0, loc=pl, rot=facing(pl, pp))
    hunch(P, t0)
    lips(P, t0, t1)
    P.act(t0 + 0.4, "point")
    L.face(t0 + 1.0, "worried")
    cam = Cam()
    mid = (-1, -24.75, 4.0)
    cam.push(t0, t1, mid, 11, 8.5, yaw=facing(pp, pl) - 95, pitch=4, lens=24, yaw1=facing(pp, pl) - 80, fstop=4)
    cam.handheld(0.9)


@S(69, 281, 288, "He looked at my legs: Leo-body looks down, wiggles them")
def s69(t0, t1):
    hood()
    L = leo_c(t0, t1, "worried", feet="socks")
    p = (1, -25.5, 0)
    L.pose(t0, loc=p, rot=facing(p, (-3, -24)))
    L.pose(t0 + 0.2, head=(0, 34, 0))
    L.face(t0 + 0.2, eyes="down", mouth="frown")
    for i in range(4):
        L.pose(t0 + 0.4 + i * 0.25, legL=(25 if i % 2 else 0, 0), legR=(0 if i % 2 else 25, 0))
    L.pose(t1 - 0.3, head=(0, 0, 0))
    cam = Cam()
    cam.key(t0, orbit_pos((p[0], p[1], 1.5), 6.0, facing(p, (-3, -24)) - 30, 10), (p[0], p[1], 1.5), lens=26, focus=6.0, fstop=3)
    cam.key(t1, orbit_pos((p[0], p[1], 3.8), 6.0, facing(p, (-3, -24)) + 10, 4), (p[0], p[1], 3.8), lens=26, focus=6.0, fstop=3)
    cam.handheld(0.9)


@S(70, 288, 291, "'Five more minutes?' puppy eyes crash zoom")
def s70(t0, t1):
    hood()
    L = leo_c(t0, t1, "worried", feet="socks")
    p = (1, -25.5, 0)
    yaw = facing(p, (-3, -24))
    L.pose(t0, loc=p, rot=yaw)
    L.act(t0, "hold", armL=(60, -30), armR=(60, -30))
    L.face(t0, eyes="worried", mouth="smile")
    lips(L, t0, t1)
    L.pose(t0, head=(0, 0, 14))
    cam = Cam()
    cam.push(t0, t1, up(p, 4.6), 5.0, 3.8, yaw=yaw, pitch=0, lens=30)
    cam.crash(t0 + 0.05, 26, 36, 0.1)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "aww", 0.6)


# ================================================================== PAYOFF
@S(71, 291, 299, "So I did the only thing I could: old body marches to the porch")
def s71(t0, t1):
    hood(boots=False, lemon=True)
    P = pruitt(t0, t1, "determined")
    P.walk(t0, t1, (6, -6, 0), (6, 9.5, 0), rate=2.2)
    cam = Cam()
    cam.track(P, t0, t1, offset=(-3.5, -7.0, 1.0), look_up=4.0, lens=22, step=0.35, fstop=5)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "footsteps", 0.6)


@S(72, 299, 304, "I stood on the porch: low hero angle")
def s72(t0, t1):
    hood(boots=False, lemon=True)
    P = pruitt(t0, t1, "determined")
    p = (6, 11.5, PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    P.act(t0 + 0.2, "fists")
    cam = Cam()
    cam.push(t0, t1, up(p, 3.8), 9, 6.5, yaw=-15, pitch=-22, lens=22, yaw1=10)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "stomp", 0.6)


@S(73, 304, 309, "In his body and yelled: hands cupped, crash zoom")
def s73(t0, t1):
    hood(boots=False, lemon=True)
    P = pruitt(t0, t1, "shout")
    p = (6, 11.5, PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    P.act(t0 + 0.1, "hands_face")
    P.face(w(308), eyes="angry", mouth="scream")
    cam = Cam()
    cam.push(t0, t1, up(p, 4.6), 7, 5.0, yaw=8, pitch=-4, lens=26)
    cam.crash(w(308), 24, 34, 0.08)
    cam.handheld(1.8)
    sfx(w(308), "whoosh", 0.7)


@S(74, 309, 314, "Anyone want their balls back?: holds up a ball, kids on the street turn")
def s74(t0, t1):
    hood(boots=False, lemon=True)
    P = pruitt(t0, t1, "shout")
    p = (6, 11.5, PORCH_Z)
    P.pose(t0, loc=p, rot=0)
    P.act(t0, "cheer")
    b = soccer_ball("ball", (0, 0, 0))
    b.parent = P.shR
    b.location = (0, 0, -2.4)
    lips(P, t0, t1, "shout")
    for i in range(4):
        k = townie(7 + i, t0, t1, "neutral")
        q = (-10 + i * 5, -24 - (i % 2) * 2, 0)
        k.pose(t0, loc=q, rot=180 + 20)
        k.pose(t0 + 0.3 + i * 0.08, rot=facing(q, p))
        k.face(t0 + 0.35 + i * 0.08, "gasp")
    cam = Cam()
    cam.key(t0, (14, -30, 4.0), (6, 6, 5), lens=22, focus=36.0, fstop=8)
    cam.key(t1, (10, -28, 3.0), (6, 4, 5.5), lens=24, focus=33.0, fstop=8)
    cam.handheld(1.0)
    sfx(t0 + 0.4, "gasp", 0.5)


@S(75, 314, 318, "Knock on the door: insert, door knocker")
def s75(t0, t1):
    hood(boots=False, lemon=True)
    k = townie(9, t0, t1, "happy")
    k.pose(t0, loc=(4.8, 13.4, PORCH_Z), rot=160)
    for i in range(3):
        k.pose(t0 + 0.1 + i * 0.18, armR=(110, 0))
        k.pose(t0 + 0.19 + i * 0.18, armR=(80, 0))
    cam = Cam()
    cam.key(t0, (11.0, 11.0, 4.4), (5.5, 15.5, 3.8), lens=24, focus=7.5, fstop=3)
    cam.key(t1, (10.0, 12.2, 4.2), (5.5, 15.5, 3.8), lens=26, focus=6.0, fstop=3)
    cam.handheld(0.9)
    sfx(t0 + 0.1, "knock")


@S(76, 318, 325, "Stay for lemonade: pitcher pour, ice clink")
def s76(t0, t1):
    hood(boots=False, lemon=True)
    lt = (1.0, 12.6, PORCH_Z)
    P = pruitt(t0, t1, "smile")
    P.pose(t0, loc=(lt[0] - 2.6, lt[1] + 0.2, PORCH_Z), rot=-90)
    P.act(t0 + 0.2, "hold")
    sparkle_on("lem", (lt[0], lt[1], 3.4), t0 + 0.3, 1.2, 8)
    cam = Cam()
    cam.orbit(t0, t1, (lt[0], lt[1], 3.0), 6.0, -35, 15, pitch=14, lens=28, fstop=3)
    cam.handheld(0.7)
    sfx(t0 + 0.3, "clink")
    sfx(t0 + 0.6, "clink", 0.6)


@S(77, 325, 329, "30 kids lined up: high crane over the queue to the porch")
def s77(t0, t1):
    hood(boots=False, lemon=True)
    src = crowd_src("Q", t0, t1, [40, 41, 42, 43], mode="cheer", spread=0.0)
    for i in range(30):
        x = 6 + (0.6 if i % 2 else -0.6)
        y = 9.0 - i * 2.4
        if y < -12:
            x = 6 - (y + 12) * 0.0 + ((i % 3) - 1) * 0.6
        ob = instance(f"q{i}", src, (x, y, 0), rot=(0, 0, 180))
        noise(ob, "location", 2, 0.15, 4)
    P = pruitt(t0, t1, "joy")
    P.pose(t0, loc=(6, 12.5, PORCH_Z), rot=0)
    P.act(t0, "wave")
    cam = Cam()
    cam.key(t0, (24, -40, 14), (6, -12, 2), lens=20, focus=36.0, fstop=11)
    cam.key(t1, (22, -30, 28), (6, -10, 0), lens=20, focus=40.0, fstop=11)
    cam.handheld(0.6)
    sfx(t0, "crowd", 0.7)
    sfx(t0 + 0.2, "cheer", 0.5)


@S(78, 329, 334, "We took off the shoes: both kick on the porch")
def s78(t0, t1):
    hood(boots=False, lemon=True)
    pp, pl = (4.0, 12.0, PORCH_Z), (8.0, 12.0, PORCH_Z)
    P = pruitt(t0, t1, "determined", feet="socks")
    L = leo_c(t0, t1, "determined", feet="socks")
    P.pose(t0, loc=pp, rot=-15)
    L.pose(t0, loc=pl, rot=15)
    tk = w(331)
    for i, (ch, p, boot) in enumerate(((P, pp, True), (L, pl, False))):
        for j, dx in enumerate((-0.5, 0.5)):
            sh = shoe_prop(f"ks{i}{j}", (p[0] + dx, p[1] - 0.15, PORCH_Z), "#e8423a", boot=not boot)
            sh.keyframe_insert("location", frame=F(tk)); sh.keyframe_insert("rotation_euler", frame=F(tk))
            sh.location = (p[0] + dx * 5 + (i - 0.5) * 4, p[1] - 5, 7.5 + j)
            sh.rotation_euler = (math.tau * 1.3, 0.6, math.tau * (j - 0.5))
            sh.keyframe_insert("location", frame=F(t1 + 0.3)); sh.keyframe_insert("rotation_euler", frame=F(t1 + 0.3))
        ch.pose(tk - 0.15, legL=(-20, 0), legR=(-20, 0), hipz=-0.3)
        ch.pose(tk + 0.08, legL=(70, 0), legR=(55, 0), hipz=0.6, armL=(150, 30), armR=(150, 30))
        ch.pose(tk + 0.4, legL=(0, 0), legR=(0, 0), hipz=0.0)
    cam = Cam()
    cam.push(t0, t1, (6, 12, 3.5), 13, 9.5, yaw=-10, pitch=4, lens=22, yaw1=6)
    cam.crash(tk, 22, 18, 0.1)
    cam.handheld(1.3)
    sfx(tk, "whoosh")


@S(79, 334, 339, "Exact same second: souls swap back, flash, boots spin in the air")
def s79(t0, t1):
    hood(boots=False, lemon=True)
    pp, pl = (4.0, 12.0, PORCH_Z), (8.0, 12.0, PORCH_Z)
    P = pruitt(t0, t1, "shock", feet="socks")
    L = leo_c(t0, t1, "shock", feet="socks")
    P.pose(t0, loc=pp, rot=-15)
    L.pose(t0, loc=pl, rot=15)
    ts = w(336)
    swap_fx("back", up(pp, 4.6), up(pl, 4.6), ts, 0.45, 1.2)
    P.face(ts + 0.55, "smile")
    L.face(ts + 0.55, "joy")
    L.act(ts + 0.55, "cheer")
    P.act(ts + 0.55, "shrug")
    cam = Cam()
    cam.orbit(t0, t1, (6, 12, 4.4), 10, 20, -25, pitch=8, lens=22, fstop=5)
    cam.crash(ts + 0.45, 22, 28, 0.1)
    cam.handheld(1.4)
    sfx(ts + 0.5, "ding", 0.8)


@S(80, 339, 344, "Now I knock every day: Leo knocks, Pruitt opens with lemonade")
def s80(t0, t1):
    hood(boots=False, lemon=True)
    L = leo_c(t0, t1, "happy")
    L.pose(t0, loc=(4.6, 13.2, PORCH_Z), rot=160)
    for i in range(3):
        L.pose(t0 + 0.1 + i * 0.18, armR=(110, 0))
        L.pose(t0 + 0.19 + i * 0.18, armR=(80, 0))
    dr = D.objects["ph_door"]
    dr.hide_render = False
    to = t0 + 0.8
    dr.keyframe_insert("location", frame=F(to))
    dr.location = (8.6, 15.9, 3.5)
    dr.keyframe_insert("location", frame=F(to + 0.25))
    P = pruitt(t0, t1, "smile")
    P.pose(t0, loc=(6, 17.5, PORCH_Z), rot=0)
    P.pose(to + 0.3, loc=(6, 15.6, PORCH_Z))
    P.act(to + 0.4, "wave", expr="happy")
    cam = Cam()
    cam.key(t0, (11.5, 9.5, 4.4), (5.5, 15, 4.3), lens=22, focus=8.5, fstop=3.5)
    cam.key(t1, (10.5, 11.0, 4.6), (5.5, 15.5, 4.6), lens=24, focus=7.0, fstop=3.5)
    cam.handheld(0.9)
    sfx(t0 + 0.1, "knock")
    sfx(to, "door", 0.6)


@S(81, 344, 347, "And Mr. Pruitt? in the yard with a ball, sneaky look")
def s81(t0, t1):
    hood(lemon=True)
    P = pruitt(t0, t1, "sus")
    p = (6, -14.5, 0)
    P.pose(t0, loc=p, rot=180 + 20)
    b = soccer_ball("ball", (p[0] - 0.3, p[1] + 1.6, 0.6))
    P.look(t0 + 0.2, -40, 0)
    P.look(t0 + 0.6, 40, 0)
    cam = Cam()
    cam.push(t0, t1, up(p, 3.6), 9, 7, yaw=200, pitch=6, lens=24, yaw1=170)
    cam.handheld(1.0)


@S(82, 347, None, "He kicks balls into his own yard on purpose: kick, wink, end")
def s82(t0, t1):
    hood(lemon=True)
    P = pruitt(t0, t1, "grin")
    p = (6, -15.5, 0)
    P.pose(t0, loc=p, rot=180)
    tk = t0 + 0.2
    P.pose(tk - 0.15, legR=(-40, 0)); P.pose(tk + 0.08, legR=(75, 0), armL=(50, 20)); P.pose(tk + 0.5, legR=(0, 0))
    b = soccer_ball("ball", (p[0], p[1] + 1.4, 0.6))
    ball_fly(b, tk, tk + 0.9, (p[0], p[1] + 1.4, 0.6), (8, 2, 0.6), h=6)
    bounce(b, tk + 0.9, (8, 2, 0.6), (9, 6, 0.6))
    tw = t1 - 0.75
    P.pose(tw, rot=0)
    P.face(tw + 0.1, "wink")
    P.act(tw + 0.1, "point")
    cam = Cam()
    cam.key(t0, (p[0] + 4, p[1] + 9, 3.0), (p[0], p[1], 3.0), lens=24, focus=10.0, fstop=4)
    cam.key(tk + 0.8, (p[0] + 6, p[1] + 1, 6.0), (8, 4, 1.0), lens=24, focus=10.0, fstop=4)
    cam.key(tw, orbit_pos(up(p, 4.6), 7.0, 0, 2), up(p, 4.6), lens=26, focus=7.0, fstop=3)
    cam.key(t1, orbit_pos(up(p, 4.6), 4.6, 0, 2), up(p, 4.6), lens=30, focus=4.6, fstop=3)
    cam.handheld(1.0)
    sfx(tk, "bonk", 0.7)
    sfx(tw + 0.1, "ding", 0.7)
