"""vo3: "Are we there yet?" - every time someone asks, the road gets one mile longer. Shots keyed to script word indices."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from helpers import rad, hide, move, bounce, swing, stars_pop, FONT
from rbx.core import _bsdf

V = Video(__file__)
story.bind(V)
RED = "#e8503a"
VY = -560


# ------------------------------------------------------------------ cast
def dad(t0, t1, expr="determined"):
    return story._live(chars.Char("Dad", skin="#e9c7a6", shirt="#5aa05a", pants="#3b3f4a", hair="short", hair_color="#4a3020",
                                  face="mustache", sleeves="short", extras=("beard:#6b4a2c",)), t0, t1, expr)


def mom(t0, t1, expr="smile"):
    return story._live(chars.Char("Mom", skin="#efd2b8", shirt="#e8788f", pants="#5a4a7a", hair="bob", hair_color="#6b3f27",
                                  face="girl", sleeves="long"), t0, t1, expr)


def kid(t0, t1, expr="talk"):
    return story._live(chars.eddie(), t0, t1, expr)


def sis(t0, t1, expr="sleepy"):
    return story._live(chars.Char("Sis", skin="#f2dbc6", shirt="#ffd36b", pants="#e58fc0", hair="bun", hair_color="#c0793a",
                                  face="girl", sleeves="short", scale=0.78), t0, t1, expr)


SEAT = dict(d=(-1.5, -1.0, 0.1), m=(1.5, -1.0, 0.1), k=(-1.5, 2.8, 1.0), s=(1.5, 2.8, 1.0))


def sit(ch, who, t0=0.0, arms=((70, -12), (70, -12))):
    ch.root.parent = CAR["root"]
    ch.pose(t0, loc=SEAT[who], rot=0, legL=(85, 3), legR=(85, -3), armL=arms[0], armR=arms[1])
    return ch


CAR = {}


def car(y=0.0, color=RED):
    root = empty("car", (0, y, 0))
    Mb = mat("carbody", hexc(color), 0.3, metal=0.3)
    Md = mat("cardark", hexc("#2a2a30"), 0.6)
    box("c_floor", (6, 12, 0.5), (0, 0, 0.6), Md, 0.05, parent=root)
    for sx in (-1, 1):
        box(f"c_side{sx}", (0.5, 12, 2.4), (sx * 2.85, 0, 1.8), Mb, 0.2, parent=root)
        sphere(f"c_head{sx}", 0.5, (sx * 2.0, -6.0, 2.0), mat("headl", hexc("#fff6c0"), 0.2, emit=hexc("#fff6c0"), estr=4), (1, 0.5, 1),
               parent=root, seg=12)
        box(f"c_tail{sx}", (0.9, 0.3, 0.5), (sx * 2.2, 6.1, 2.4), mat("taill", hexc("#ff3030"), 0.3, emit=hexc("#ff2020"), estr=2), 0.05,
            parent=root)
    box("c_hood", (6, 3.8, 2.4), (0, -4.1, 1.8), Mb, 0.3, parent=root)
    box("c_trunk", (6, 2.6, 2.6), (0, 4.7, 1.9), Mb, 0.3, parent=root)
    box("c_dash", (5.6, 0.7, 1.2), (0, -2.45, 2.7), Md, 0.1, parent=root)
    Ms = mat("cseat", hexc("#3a3f58"), 0.7)
    for sx in (-1, 1):
        box(f"c_fseat{sx}", (2.2, 1.8, 1.3), (sx * 1.5, -0.9, 1.2), Ms, 0.15, parent=root)
        box(f"c_fback{sx}", (2.2, 0.5, 2.0), (sx * 1.5, 0.5, 2.4), Ms, 0.15, parent=root)
    box("c_bseat", (5.6, 2.2, 2.1), (0, 2.8, 1.5), Ms, 0.15, parent=root)
    box("c_bback", (5.6, 0.6, 2.4), (0, 4.2, 3.3), Ms, 0.15, parent=root)
    wheels = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = empty(f"c_wp{sx}{sy}", (sx * 3.05, sy * 3.7, 1.5), root)
            cyl(f"c_tire{sx}{sy}", 1.5, 0.9, (0, 0, 0), mat("tire", hexc("#141414"), 0.8), 20, parent=p, rot=(0, 90, 0))
            cyl(f"c_hub{sx}{sy}", 0.8, 0.95, (0, 0, 0), mat("hub", hexc("#d8d8e0"), 0.3, metal=0.6), 14, parent=p, rot=(0, 90, 0))
            wheels.append(p)
    CAR.clear()
    CAR.update(root=root, wheels=wheels)
    return CAR


def drive(c, t0, t1, y0, y1):
    move(c["root"], t0, loc=(0, y0, 0), interp="LINEAR")
    move(c["root"], t1, loc=(0, y1, 0), interp="LINEAR")
    ang = abs(y1 - y0) / 1.5
    for w in c["wheels"]:
        w.rotation_euler = (0, 0, 0)
        w.keyframe_insert("rotation_euler", frame=F(t0))
        set_interp(w, "rotation_euler", F(t0), "LINEAR")
        w.rotation_euler = (-ang, 0, 0)
        w.keyframe_insert("rotation_euler", frame=F(t1))
        set_interp(w, "rotation_euler", F(t1), "LINEAR")
    noise(c["root"], "location", 2, 0.05, 3)
    sfx(t0, "wind", 0.25)


def fam(t0, t1, who="dmks", dog=False, d="determined", m="smile", k="talk", s="sleepy"):
    out = {}
    if "d" in who:
        out["d"] = sit(dad(t0, t1, d), "d", t0)
    if "m" in who:
        out["m"] = sit(mom(t0, t1, m), "m", t0)
    if "k" in who:
        out["k"] = sit(kid(t0, t1, k), "k", t0, arms=((20, 15), (20, 15)))
    if "s" in who:
        out["s"] = sit(sis(t0, t1, s), "s", t0, arms=((20, 15), (20, 15)))
    if dog:
        dg = W.dog("dog", (0, 2.6, 2.6))
        dg.parent = CAR["root"]
        dg.location = (0, 2.7, 1.9)
        dg.scale = (0.8,) * 3
        out["dog"] = dg
    return out


# ------------------------------------------------------------------ world
def env(volcano=True, dashes=True, y0=60, trees=True):
    W.sky(1.0)
    W.sun(3.4, rot=(50, 0, 25))
    light("sun2", "SUN", (0, 0, 50), 2.4, (1.0, 0.97, 0.92), 2, rot=(50, 0, 205))
    box("ground", (1800, 1800, 0.4), (0, -300, -0.28), mat("fgrass", hexc("#6fc050"), 0.9), 0)
    box("road", (14, 900, 0.1), (0, -300, 0.0), mat("asph", hexc("#4c4d56"), 0.8), 0)
    for sx in (-1, 1):
        box(f"edge{sx}", (0.35, 900, 0.12), (sx * 6.4, -300, 0.01), mat("edgew", hexc("#f4f4f4"), 0.6), 0)
    dl = []
    if dashes:
        Md = mat("dashy", hexc("#ffd23a"), 0.5)
        for i in range(110):
            dl.append(box(f"dash{i}", (0.5, 3.2, 0.06), (0, y0 - i * 8, 0.08), Md, 0.0))
    if trees:
        rnd = random.Random(7)
        Mt, Mc = mat("trunk", hexc("#7a4a2a"), 0.8), mat("crown", hexc("#4aa83a"), 0.9)
        for i in range(60):
            x = rnd.choice((-1, 1)) * rnd.uniform(14, 46)
            y = rnd.uniform(-380, 70)
            cyl(f"tr{i}", 0.8, 5, (x, y, 2.5), Mt, 8)
            sphere(f"cr{i}", rnd.uniform(3.2, 4.6), (x, y, 7.2), Mc, (1, 1, 1.15), seg=10)
    for i in range(7):
        if abs(-170 + i * 58) < 110:
            continue
        sphere(f"hill{i}", 1, (-170 + i * 58, -430 + (i % 2) * 40, 0), mat("hillg", hexc("#58a844"), 0.9), (70, 50, 24 + (i % 3) * 8), seg=12)
    out = dict(dashes=dl)
    if volcano:
        out.update(volcano_build())
    return out


def volcano_build():
    c = cyl("volcano", 78, 120, (0, VY, 60), mat("volc", hexc("#6a4636"), 0.95), 28, r2=14)
    Ml = mat("lavamat", hexc("#ff5a14"), 0.4, emit=hexc("#ff4a00"), estr=3.5)
    cr = sphere("crater", 15, (0, VY, 118), Ml, (1, 1, 0.35), seg=16)
    light("lavalight", "POINT", (0, VY + 25, 125), 90000, (1.0, 0.45, 0.12), 6)
    pv = empty("lavapiv", (0, VY, 0))
    box("lavaflow", (22, 330, 0.6), (0, 165, 0.35), Ml, 0.05, parent=pv)
    pv.scale = (1, 0.001, 1)
    smoke = []
    Ms = mat("smokeg", hexc("#3a3836"), 0.95)
    for i in range(9):
        s = sphere(f"smoke{i}", 15 + (i % 3) * 5, (-10 + i * 3, VY, 138 + i * 12), Ms, seg=10)
        smoke.append(s)
    return dict(lava=pv, lavamat=Ml, crater=cr, smoke=smoke)


def eruption(t, n=14, seed=3):
    rnd = random.Random(seed)
    Mb = mat("lavabomb", hexc("#ff7a20"), 0.3, emit=hexc("#ff6000"), estr=9)
    for i in range(n):
        b = sphere(f"bomb{i}", rnd.uniform(1.2, 2.6), (0, VY, 118), Mb, seg=8)
        b.scale = (0.01,) * 3
        d = rnd.uniform(0, 0.25)
        b.keyframe_insert("scale", frame=F(t + d - 0.02))
        b.keyframe_insert("location", frame=F(t + d - 0.02))
        b.scale = (1,) * 3
        b.keyframe_insert("scale", frame=F(t + d))
        a = rnd.uniform(0, math.tau)
        r = rnd.uniform(20, 70)
        b.location = (math.cos(a) * r * 0.6, VY + math.sin(a) * r * 0.6, 118 + rnd.uniform(40, 90))
        b.keyframe_insert("location", frame=F(t + d + 0.6))
        b.location = (math.cos(a) * r, VY + math.sin(a) * r, 40)
        b.keyframe_insert("location", frame=F(t + d + 1.4))
        b.scale = (0.01,) * 3
        b.keyframe_insert("scale", frame=F(t + d + 1.5))


def lava_run(E, t0, t1, s0=0.02, s1=1.0):
    move(E["lava"], t0, scale=(1, s0, 1))
    move(E["lava"], t1, scale=(1, s1, 1), ease="EASE_IN")


def cool_lava(E, t0, t1):
    b = _bsdf(E["lavamat"])
    for k, (c, es) in enumerate((((1.0, 0.35, 0.08), 6.0), ((0.05, 0.04, 0.04), 0.0))):
        t = t0 if k == 0 else t1
        b.inputs["Base Color"].default_value = (*c, 1)
        b.inputs["Emission Color"].default_value = (*c, 1)
        b.inputs["Emission Strength"].default_value = es
        for nm in ("Base Color", "Emission Color", "Emission Strength"):
            b.inputs[nm].keyframe_insert("default_value", frame=F(t))


def road_stretch(E, t, f=1.8, dur=0.55):
    for d in E["dashes"]:
        y = d.location[1]
        d.location = (0, y, 0.08)
        d.keyframe_insert("location", frame=F(t))
        d.location = (0, y * f if y < 0 else y + (y) * 0.0, 0.08)
        d.keyframe_insert("location", frame=F(t + dur))
        set_interp(d, "location", F(t + dur), "BEZIER", "EASE_OUT")
    sfx(t, "boing", 0.9)
    sfx(t + 0.05, "whoosh", 0.8)


def sign(loc, txt, size=1.1):
    post = cyl("sgn_post", 0.25, 6, (loc[0], loc[1], 3), mat("post", hexc("#8a8a90"), 0.5), 8)
    box("sgn_board", (6.2, 0.3, 3.2), (loc[0], loc[1], 7.2), mat("sgnb", hexc("#1f8a4a"), 0.5), 0.1)
    text("sgn_txt", txt, (loc[0], loc[1] + 0.25, 7.2), size, mat("sgnt", hexc("#ffffff"), 0.4), rot=(90, 0, 180), extrude=0.05, font=FONT)


def house(x=-26.0, y=-60.0):
    box("gh_wall", (14, 16, 10), (x, y, 5), mat("ghw", hexc("#f2d27a"), 0.7), 0.2)
    box("gh_roof", (16.4, 18.4, 2.2), (x, y, 11.1), mat("ghr", hexc("#a33b2f"), 0.7), 0.3)
    box("gh_door", (0.3, 3.4, 6.6), (x + 7.1, y, 3.3), mat("ghd", hexc("#7a4a2a"), 0.6), 0.1)
    for sy in (-5, 5):
        box(f"gh_win{sy}", (0.3, 3.2, 3.2), (x + 7.1, y + sy, 6.4), mat("ghwin", hexc("#9fd0ff"), 0.2, emit=hexc("#9fd0ff"), estr=0.6), 0.1)
    box("gh_porch", (7, 12, 0.6), (x + 10.4, y, 0.3), mat("ghp", hexc("#b88a5a"), 0.7), 0.1)
    for sy in (-4.6, 4.6):
        cyl(f"gh_post{sy}", 0.3, 7, (x + 13, y + sy, 3.5), mat("ghpost", hexc("#f4f4f4"), 0.5), 10)
    box("gh_proof", (7, 12.4, 0.5), (x + 10.4, y, 7.2), mat("ghr", hexc("#a33b2f"), 0.7), 0.1)
    for sy in (-7.5, 7.5):
        sphere(f"gh_bush{sy}", 2.0, (x + 8.2, y + sy, 1.4), mat("bushg", hexc("#3f9f3a"), 0.9), (1, 1.2, 1), seg=12)


# ------------------------------------------------------------------ cameras
def lerp3(a, b, e):
    return tuple(a[i] + (b[i] - a[i]) * e for i in range(3))


def tcam(t0, t1, off0, off1=None, tgt0=(0, 0, 3.5), tgt1=None, lens0=28, lens1=None, hh=1.0, fstop=6.0, ease=True, dy=0.0):
    """Camera that rides along with the car (offset relative to its root) and moves between two framings."""
    off1 = off1 or off0
    tgt1 = tgt1 or tgt0
    lens1 = lens1 or lens0
    cam = Cam()
    n = max(2, int((t1 - t0) / 0.1))
    sc = bpy.context.scene
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if ease else u
        t = t0 + (t1 - t0) * u
        sc.frame_set(F(t))
        p = Vector(CAR["root"].matrix_world.translation)
        loc = p + Vector(lerp3(off0, off1, e))
        tg = p + Vector(lerp3(tgt0, tgt1, e))
        cam.key(t, tuple(loc), tuple(tg), lens=lens0 + (lens1 - lens0) * e, focus=tuple(tg), fstop=fstop, interp="LINEAR")
    cam.handheld(hh)
    return cam


def ctext(cam, body, t, dur=0.9, size=0.7, color="#ffe066", loc=(0, 1.8, -10.0), rot=(0, 0, 0), emit=2.0):
    M = mat("ct_" + color, hexc(color), 0.4, emit=hexc(color), estr=emit)
    ob = text("ct_" + body[:6], body, loc, size, M, rot=rot, extrude=0.08, font=FONT, parent=cam.ob)
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.02))
    for dt, k in ((0.07, 1.25), (0.15, 0.95), (0.22, 1.0)):
        ob.scale = (k,) * 3
        ob.keyframe_insert("scale", frame=F(t + dt))
    ob.keyframe_insert("scale", frame=F(t + dur))
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur + 0.1))
    return ob


def scene(t0, t1, y0=0.0, y1=None, who="dmks", dog=False, volcano=True, **ex):
    E = env(volcano=volcano)
    c = car(y0)
    if y1 is not None and y1 != y0:
        drive(c, t0, t1, y0, y1)
    F_ = fam(t0, t1, who, dog, **ex)
    return E, c, F_


def shout(ch, t0, t1, mode="shout"):
    lips(ch, t0, t1, mode)


# ================================================================== SHOTS
@S(1, 0, 6, "HOOK: kid asks 'are we there yet' - crash zoom")
def s01(t0, t1):
    E, c, P = scene(t0, t1, 0, -30)
    P["k"].act(t0 + 0.1, "point", expr="shout")
    lips(P["k"], t0, t1, "shout")
    P["d"].act(t0 + 1.0, "facepalm")
    cam = tcam(t0, t1, (-2.5, -9.5, 7.6), (-1.0, -6.5, 7.2), (-1.5, 2.8, 5.4), (-1.5, 2.8, 5.4), 26, 30, hh=1.8)
    cam.crash(t0, 22, 34, 0.15)
    sfx(t0, "whoosh", 0.7)


@S(2, 6, 8, "4,000 times: giant number slam")
def s02(t0, t1):
    E, c, P = scene(t0, t1, -30, -60)
    P["d"].act(t0 + 0.1, "hands_head", expr="terror")
    cam = tcam(t0, t1, (0, -9.5, 5.5), (0, -7, 5.0), (0, 0, 4.4), None, 26, 28, hh=2.2)
    ctext(cam, "4,000x", t0 + 0.15, 1.3, 1.0, "#ff4a4a", (0, 2.2, -9))
    sfx(t0 + 0.15, "u_slap", 0.8)
    sfx(t0 + 0.2, "boom", 0.4)


@S(3, 8, 14, "That's why the trip to Grandma's: signpost")
def s03(t0, t1):
    E, c, P = scene(t0, t1, 40, -8, who="dm")
    sign((11, -4, 0), "GRANDMA'S\n5 MI")
    cam = tcam(t0, t1, (8, 12, 5), (-9, -9, 4.2), (0, -2, 3.5), (0, -2, 3.8), 24, 28, hh=1.2)
    sfx(t0 + 0.2, "whoosh", 0.7)


@S(4, 14, 17, "took three years")
def s04(t0, t1):
    E, c, P = scene(t0, t1, -8, -60, who="dmks", k="sleepy")
    for who in P.values():
        pass
    P["d"].act(t0 + 0.2, "slump", expr="bored")
    cam = tcam(t0, t1, (-11, 8, 4.4), (-11, -9, 4.8), (0, 0, 3.4), None, 26, 30, hh=1.4)
    ctext(cam, "3 YEARS", t0 + 0.2, 1.5, 0.9, "#ffe066", (0, 3.0, -9))
    sfx(t0 + 0.2, "pop", 0.8)
    sfx(t0 + 0.3, "u_faaah", 0.35)


@S(5, 17, 22, "You see, in this world (kid to camera)")
def s05(t0, t1):
    E, c, P = scene(t0, t1, -60, -90, who="dmks", k="talk")
    P["k"].act(t0 + 0.2, "point", expr="smug")
    lips(P["k"], t0, t1)
    cam = tcam(t0, t1, (-3.5, -8.5, 7.8), (-2.2, -5.8, 7.2), (-1.5, 2.8, 5.4), None, 30, 34, hh=1.2)
    cam.crash(t0, 24, 32, 0.15)
    sfx(t0, "whoosh", 0.6)


@S(6, 22, 30, "every time someone asks: bubble ARE WE THERE YET?")
def s06(t0, t1):
    E, c, P = scene(t0, t1, -90, -150, who="dmks", k="shout")
    lips(P["k"], t0 + 0.6, t1, "shout")
    P["k"].act(t0 + 1.2, "cheer", expr="shout")
    cam = tcam(t0, t1, (10, -2, 5.0), (7, -9, 4.4), (0, 0, 3.4), None, 26, 26, hh=1.3)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 1.3, 1.5, 0.8, "#ffffff", (0, 2.2, -9.5))
    sfx(t0 + 1.3, "pop", 0.8)


@S(7, 30, 36, "the road gets one mile longer: milestone sign + dashes spread")
def s07(t0, t1):
    E, c, P = scene(t0, t1, -150, -230, who="dmks")
    sign((10, -170, 0), "GRANDMA'S\n5 MI")
    road_stretch(E, t0 + 1.2, 1.7)
    cam = tcam(t0, t1, (0, 13, 4.5), (4, 24, 9), (0, -12, 3), (0, -40, 5), 26, 22, hh=1.2)
    ctext(cam, "+1 MILE", t0 + 1.5, 1.4, 0.85, "#ff8a3a", (0, 2.5, -10))
    sfx(t0 + 1.5, "rise", 0.7)


@S(8, 36, 37, "Stretch! (elastic road)")
def s08(t0, t1):
    E, c, P = scene(t0, t1, -230, -250, who="dmks")
    road_stretch(E, t0 + 0.0, 2.2, 0.5)
    cam = tcam(t0, t1, (0, 6, 3.0), (0, 26, 12), (0, -10, 3), (0, -40, 3), 22, 30, hh=2.4, ease=False)
    ctext(cam, "STRETCH!", t0 + 0.0, 0.9, 0.85, "#7affc8", (0, 2.2, -9))
    cam.crash(t0, 22, 36, 0.2)
    sfx(t0, "u_1-108", 0.5)


@S(9, 37, 41, "So families are careful")
def s09(t0, t1):
    E, c, P = scene(t0, t1, 0, -25, who="dmks", k="neutral", d="worried", m="worried")
    P["m"].act(t0 + 0.2, "think")
    P["d"].face(t0 + 0.1, "worried")
    cam = tcam(t0, t1, (-6, -7, 6), (6, -9, 5.2), (0, 0, 4), None, 24, 26, hh=1.0)
    sfx(t0 + 0.4, "crickets", 0.5)


@S(10, 41, 45, "Dads drive in silence")
def s10(t0, t1):
    E, c, P = scene(t0, t1, -25, -55, who="d", d="determined")
    P["d"].act(t0 + 0.2, "hold")
    cam = tcam(t0, t1, (-0.5, -5.6, 5.0), (-2.6, -4.6, 4.8), (-1.5, -1.0, 4.6), None, 32, 38, hh=0.7)
    sfx(t0, "crickets", 0.6)


@S(11, 45, 51, "Moms hand out snacks like medicine")
def s11(t0, t1):
    E, c, P = scene(t0, t1, -55, -90, who="mk", m="smile", k="sleepy")
    P["m"].root.rotation_euler[2] = rad(180)
    P["m"].pose(t0, loc=(1.5, -1.0, 0.1), rot=180, armL=(90, 20), armR=(90, -20))
    bottle = cyl("pillbottle", 0.45, 1.1, (0.0, -0.9, -0.5), mat("pill", hexc("#e8892a"), 0.4), 14, parent=P["m"].hip)
    cyl("pillcap", 0.5, 0.25, (0.0, -0.9, 0.2), mat("pillcap", hexc("#f4f4f4"), 0.4), 14, parent=P["m"].hip)
    P["k"].act(t0 + 1.0, "cross", expr="worried")
    cam = tcam(t0, t1, (0.5, 8.0, 6.4), (3.4, 5.6, 5.4), (0.2, 1.0, 4.0), None, 28, 32, hh=1.0)
    sfx(t0 + 0.3, "click", 0.6)
    sfx(t0 + 1.3, "u_correct", 0.2)


@S(12, 51, 58, "Some kids even tape their mouths shut")
def s12(t0, t1):
    E, c, P = scene(t0, t1, -90, -125, who="ks", k="worried")
    k = P["k"]
    tape = box("tape", (1.15, 0.06, 0.38), (0, -0.63, -0.32), mat("tape", hexc("#e8e2d2"), 0.6), 0.02, parent=k.head)
    move(tape, t0, scale=(0.01, 1, 1))
    move(tape, t0 + 0.4, scale=(1.1, 1, 1))
    move(tape, t0 + 0.5, scale=(1, 1, 1))
    noise(k.head, "rotation_euler", 2, 0.08, 6)
    k.act(t0 + 0.6, "hands_face", expr="worried")
    cam = tcam(t0, t1, (-1.5, -6.6, 7.6), (-1.5, -4.6, 7.2), (-1.5, 2.8, 5.6), None, 34, 40, hh=0.9)
    sfx(t0 + 0.35, "paper", 0.8)
    sfx(t0 + 0.4, "u_slap", 0.4)


@S(13, 58, 63, "But I can't help it (tape rips, vibration)")
def s13(t0, t1):
    E, c, P = scene(t0, t1, -125, -150, who="ks", k="scream")
    k = P["k"]
    k.act(t0 + 0.2, "hands_head", expr="scream")
    noise(k.hip, "location", 0, 0.12, 2)
    cam = tcam(t0, t1, (-1.5, -5.6, 7.4), (-1.5, -4.0, 7.0), (-1.5, 2.8, 5.6), None, 36, 46, hh=3.0)
    cam.crash(t0 + 0.8, 36, 48, 0.2)
    sfx(t0 + 0.3, "zombie", 0.4)
    sfx(t0 + 0.9, "gasp", 0.8)


@S(14, 63, 67, "Are we there yet? (shout)")
def s14(t0, t1):
    E, c, P = scene(t0, t1, -150, -178, who="dmks", k="shout")
    lips(P["k"], t0, t1, "shout")
    P["k"].act(t0 + 0.1, "cheer", expr="shout")
    P["d"].act(t0 + 0.6, "facepalm")
    cam = tcam(t0, t1, (3, -9.5, 8.0), (-0.5, -6.6, 7.4), (-0.5, 1, 4.4), None, 26, 30, hh=2.0)
    cam.crash(t0, 24, 34, 0.15)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.1, 1.0, 0.7, "#ffffff", (0, 2.4, -9.5))
    sfx(t0, "whoosh", 0.5)


@S(15, 67, 68, "Stretch! #1")
def s15(t0, t1):
    E, c, P = scene(t0, t1, -178, -190, who="dmks")
    road_stretch(E, t0, 1.9, 0.5)
    cam = tcam(t0, t1, (0, 9, 4), (0, 28, 10), (0, -14, 3), (0, -50, 3), 22, 28, hh=2.4, ease=False)
    ctext(cam, "STRETCH!", t0, 0.8, 0.85, "#7affc8", (0, 2.2, -9))


@S(16, 68, 72, "Are we there yet? (side view)")
def s16(t0, t1):
    E, c, P = scene(t0, t1, -190, -215, who="dmks", k="shout")
    lips(P["k"], t0, t1, "shout")
    P["s"].act(t0 + 0.1, "cheer", expr="shout")
    cam = tcam(t0, t1, (-11, 0, 4.5), (-8, -6, 4.8), (0, 0, 3.6), None, 24, 30, hh=1.6)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.1, 1.0, 0.7, "#ffffff", (0, 2.4, -9.5))
    sfx(t0, "whoosh", 0.5)


@S(17, 72, 73, "Stretch! #2")
def s17(t0, t1):
    E, c, P = scene(t0, t1, -215, -225, who="dmks")
    road_stretch(E, t0, 2.0, 0.5)
    cam = tcam(t0, t1, (6, 4, 3), (14, 24, 14), (0, -20, 3), (0, -60, 4), 22, 26, hh=2.4, ease=False)
    ctext(cam, "STRETCH!", t0, 0.8, 0.85, "#7affc8", (0, 2.2, -9))


@S(18, 73, 78, "Dad's beard reached his knees")
def s18(t0, t1):
    E, c, P = scene(t0, t1, -225, -245, who="d", d="worried")
    d = P["d"]
    pivb = empty("beardpiv", (0, -0.5, -0.5), d.head)
    bd = box("longbeard", (1.0, 0.35, 1.0), (0, -0.05, -0.5), mat("bd_long", hexc("#6b4a2c"), 0.9), 0.15, parent=pivb)
    move(pivb, t0, scale=(1, 1, 0.2))
    move(pivb, t0 + 1.1, scale=(1, 1, 5.5), ease="EASE_IN_OUT")
    d.act(t0 + 1.2, "shock", expr="gasp")
    cam = tcam(t0, t1, (-1.5, -7.5, 5.0), (-1.5, -6.5, 3.2), (-1.5, -1.0, 4.6), (-1.5, -1.0, 2.6), 28, 28, hh=1.0)
    sfx(t0 + 0.3, "rise", 0.8)
    sfx(t0 + 1.3, "boing", 0.7)


@S(19, 78, 84, "Mom learned French from the radio")
def s19(t0, t1):
    E, c, P = scene(t0, t1, -245, -265, who="m", m="talk")
    box("radio", (1.8, 0.6, 1.0), (0.9, -2.3, 3.2), mat("radiom", hexc("#c8a060"), 0.5), 0.1, parent=CAR["root"])
    cyl("antenna", 0.04, 2.4, (1.6, -2.3, 4.5), mat("antm", hexc("#aaaaaa"), 0.3, metal=0.8), 6, parent=CAR["root"], rot=(0, 20, 0))
    lips(P["m"], t0, t1)
    P["m"].act(t0 + 0.4, "point", expr="talk")
    cam = tcam(t0, t1, (3.4, -6.0, 5.2), (0.4, -4.8, 5.0), (1.5, -1.0, 4.4), None, 30, 34, hh=0.9)
    ctext(cam, "BONJOUR!", t0 + 1.0, 1.3, 0.7, "#6ab0ff", (0, 2.4, -9))
    sfx(t0 + 0.3, "click", 0.7)
    sfx(t0 + 1.0, "u_mac-quack", 0.4)


@S(20, 84, 89, "Then one morning, Grandma called (phone ringing)")
def s20(t0, t1):
    E, c, P = scene(t0, t1, -265, -285, who="dmks", k="sleepy")
    ph = box("phone", (0.7, 0.15, 1.3), (1.5, -2.5, 3.6), mat("phonem", hexc("#222222"), 0.3), 0.08, parent=CAR["root"])
    noise(ph, "rotation_euler", 1, 0.5, 2)
    P["m"].face(t0 + 0.4, "gasp")
    cam = tcam(t0, t1, (0, -7.5, 5.8), (1.0, -5.0, 5.0), (0.8, -1.5, 3.8), None, 26, 32, hh=1.4)
    ctext(cam, "GRANDMA\nCALLING", t0 + 0.3, 1.8, 0.7, "#ffe066", (0, 2.4, -9))
    sfx(t0 + 0.2, "alarm", 0.5)
    sfx(t0 + 0.2, "u_discord-notification", 0.6)


@S(21, 89, 91, "Don't come! (Grandma shouting on the phone)")
def s21(t0, t1):
    world((0.95, 0.7, 0.45), 0.8)
    box("gwall", (60, 0.5, 40), (0, 12, 15), mat("gwall", hexc("#f2d8b0"), 0.8), 0)
    box("gfloor", (60, 40, 0.4), (0, 0, -0.2), mat("gfl", hexc("#b88a5a"), 0.8), 0)
    light("gl", "AREA", (0, -8, 12), 12000, (1.0, 0.85, 0.7), 12, target=(0, 0, 4))
    G = grandma(t0, t1, "scream")
    G.pose(t0, loc=(0, 4, 0), rot=0)
    G.act(t0 + 0.05, "phone", expr="scream")
    lips(G, t0, t1, "shout")
    cam = Cam()
    cam.key(t0, (-0.5, -3.5, 4.8), (0, 4, 4.8), lens=34)
    cam.key(t1, (-0.2, -1.6, 4.9), (0, 4, 4.9), lens=34, ease="EASE_IN")
    cam.handheld(3.0)
    cam.crash(t0, 30, 44, 0.12)
    sfx(t0, "u_slap", 0.6)
    sfx(t0 + 0.1, "gasp", 0.7)


@S(22, 91, 96, "The volcano just woke up! (eruption)")
def s22(t0, t1):
    E = env(volcano=True)
    c = car(-250)
    fam(t0, t1, who="dmks", d="terror", m="scream", k="scream", s="gasp")
    eruption(t0 + 0.4, 18, 4)
    move(E["lava"], t0, scale=(1, 0.001, 1))
    move(E["lava"], t1, scale=(1, 0.2, 1))
    cam = Cam()
    cam.key(t0, (9, -240, 12), (0, VY, 85), lens=24)
    cam.key(t1, (6, -262, 9), (0, VY, 100), lens=28, ease="EASE_OUT")
    cam.handheld(3.2)
    cam.crash(t0 + 0.4, 22, 30, 0.2)
    ctext(cam, "ERUPTION!", t0 + 0.6, 1.2, 0.8, "#ff6a2a", (0, 2.4, -9))
    sfx(t0 + 0.4, "u_capcut-explosion-sound", 0.9)
    sfx(t0 + 0.4, "boom", 0.9)
    sfx(t0 + 0.5, "rise", 0.5)


@S(23, 96, 102, "Lava was pouring down her street (lava between houses)")
def s23(t0, t1):
    E = env(volcano=True, y0=-200)
    house(-26, -330)
    lava_run(E, t0, t1, 0.5, 0.68)
    cam = Cam()
    cam.key(t0, (-8, -300, 14), (0, -380, 5), lens=22)
    cam.key(t1, (-2, -308, 6), (0, -372, 4), lens=26, ease="EASE_IN_OUT")
    cam.handheld(2.4)
    sfx(t0 + 0.3, "wind", 0.6)
    sfx(t0 + 0.5, "splat", 0.4)


@S(24, 102, 107, "We were five miles away (car + sign 5 MI, volcano behind)")
def s24(t0, t1):
    E, c, P = scene(t0, t1, -300, -315, who="dmks", d="terror", m="gasp", k="scream", s="scream")
    sign((-10, -250, 0), "5 MI")
    lava_run(E, t0, t1, 0.25, 0.3)
    cam = tcam(t0, t1, (-9, 8, 4.8), (-3, 12, 6.5), (0, -20, 5), (0, -40, 9), 26, 22, hh=1.8)
    sfx(t0 + 0.3, "gasp", 0.8)


@S(25, 107, 112, "Dad stomped on the gas")
def s25(t0, t1):
    E, c, P = scene(t0, t1, -315, -380, who="d", d="furious")
    lava_run(E, t0, t1, 0.3, 0.3)
    P["d"].act(t0 + 0.1, "fists", expr="furious")
    c2 = c
    cam = tcam(t0, t1, (-4.5, -7.5, 4.0), (-2.5, -10.5, 5.0), (-1.5, -1.0, 3.6), (-1.5, -1.0, 4.4), 28, 24, hh=2.8)
    cam.crash(t0 + 0.3, 30, 20, 0.2)
    sfx(t0 + 0.2, "stomp", 0.9)
    sfx(t0 + 0.3, "rocket", 0.6)


@S(26, 112, 120, "But the lava was racing toward the road")
def s26(t0, t1):
    E, c, P = scene(t0, t1, -300, -306, who="dmks", d="scared", m="scared", k="scared", s="scared")
    lava_run(E, t0, t1, 0.3, 0.55)
    cam = tcam(t0, t1, (-3, 9, 4.5), (4, 16, 6.5), (0, -30, 4), (0, -70, 5), 24, 20, hh=2.0)
    sfx(t0 + 0.2, "rise", 0.7)
    sfx(t0 + 1.0, "wind", 0.7)


@S(27, 120, 122, "Five miles.")
def s27(t0, t1):
    E, c, P = scene(t0, t1, -306, -318, who="dmks", d="scared", m="scared", k="scared", s="scared")
    lava_run(E, t0, t1, 0.55, 0.6)
    cam = tcam(t0, t1, (0, 11, 5), (0, 8, 4.6), (0, -25, 5), None, 26, 28, hh=2.0)
    ctext(cam, "5 MILES", t0, 0.7, 0.8, "#ff4a4a", (0, 2.4, -9))
    sfx(t0, "u_slap", 0.6)


@S(28, 122, 123, "Four.")
def s28(t0, t1):
    E, c, P = scene(t0, t1, -318, -326, who="dmks", d="scared", m="scared", k="scared", s="scared")
    lava_run(E, t0, t1, 0.6, 0.66)
    cam = tcam(t0, t1, (-9, 11, 5.6), (9, 11, 5.6), (0, -25, 5), None, 22, 26, hh=2.4)
    ctext(cam, "4", t0, 0.6, 2.4, "#ff6a2a", (0, 2.4, -9))
    sfx(t0, "u_slap", 0.6)


@S(29, 123, 124, "Three.")
def s29(t0, t1):
    E, c, P = scene(t0, t1, -326, -330, who="dmks", d="terror", m="scream", k="scream", s="scream")
    lava_run(E, t0, t1, 0.66, 0.72)
    cam = tcam(t0, t1, (0, -8, 4.4), (0, -6, 4.4), (0, 0, 4.2), None, 26, 30, hh=2.8)
    ctext(cam, "3", t0, 0.6, 2.6, "#ff3a2a", (0, 2.4, -9))
    sfx(t0, "u_slap", 0.7)


@S(30, 124, 131, "We were driving straight into the fire (lava wall ahead)")
def s30(t0, t1):
    E, c, P = scene(t0, t1, -330, -360, who="dmks", d="terror", m="scream", k="scream", s="scream")
    lava_run(E, t0, t1, 0.72, 0.8)
    for ch in P.values():
        noise(ch.hip, "location", 0, 0.12, 2)
    cam = tcam(t0, t1, (0, -10, 5.0), (0, -7, 4.8), (0, 0, 4.4), None, 24, 30, hh=3.2)
    cam.crash(t0 + 1.2, 24, 38, 0.3)
    sfx(t0, "rise", 0.9)
    sfx(t0 + 1.0, "zombie", 0.5)


@S(31, 131, 135, "Then I noticed something (kid thinks, lightbulb)")
def s31(t0, t1):
    E, c, P = scene(t0, t1, -200, -200, who="k", k="sus")
    P["k"].act(t0 + 0.2, "think", expr="sus")
    bulb = sphere("bulb", 0.5, (-1.5, 2.8, 8.4), mat("bulbm", hexc("#fff4a0"), 0.2, emit=hexc("#fff4a0"), estr=12), parent=CAR["root"])
    move(bulb, t0, scale=0.01)
    move(bulb, t1 - 0.6, scale=0.01)
    move(bulb, t1 - 0.4, scale=1.3)
    move(bulb, t1 - 0.3, scale=1.0)
    cam = tcam(t0, t1, (-1.5, -6.4, 7.6), (-1.5, -4.4, 7.2), (-1.5, 2.8, 5.6), (-1.5, 2.8, 6.0), 34, 44, hh=0.9)
    sfx(t0 + 0.2, "u_correct", 0.5)
    sfx(t1 - 0.4, "ding", 0.8)
    sfx(t0 + 0.1, "rise", 0.6)


@S(32, 135, 139, "If we never arrived: endless road")
def s32(t0, t1):
    E, c, P = scene(t0, t1, -200, -230, who="dmks", d="neutral", m="neutral", k="smug", s="sleepy")
    lava_run(E, t0, t1, 0.3, 0.3)
    cam = tcam(t0, t1, (10, -8, 4.4), (11, 8, 4.8), (0, 0, 3.6), None, 24, 28, hh=1.4)
    sfx(t0 + 0.2, "wind", 0.5)


@S(33, 139, 144, "we'd never reach the lava (lava far ahead at end of road)")
def s33(t0, t1):
    E, c, P = scene(t0, t1, -230, -242, who="dmks", d="neutral", m="neutral", k="smug", s="sleepy")
    lava_run(E, t0, t1, 0.25, 0.25)
    cam = tcam(t0, t1, (0, 14, 6), (0, 30, 14), (0, -60, 4), (0, -200, 20), 24, 20, hh=1.2)
    sfx(t0 + 0.2, "sparkle", 0.6)


@S(34, 144, 149, "I took a deep breath")
def s34(t0, t1):
    E, c, P = scene(t0, t1, -242, -260, who="k", k="neutral")
    k = P["k"]
    move(k.head, t0, scale=1.0)
    move(k.head, t0 + 0.9, scale=1.35, ease="EASE_IN_OUT")
    move(k.head, t1, scale=1.0)
    k.act(t0 + 0.8, "cheer", expr="grin")
    cam = tcam(t0, t1, (-1.5, -7.0, 7.6), (-1.5, -4.2, 7.2), (-1.5, 2.8, 5.6), None, 34, 40, hh=0.8)
    sfx(t0 + 0.3, "wind", 0.9)
    sfx(t0 + 0.8, "gasp", 0.8)


@S(35, 149, 153, "Are we there yet? (kid)")
def s35(t0, t1):
    E, c, P = scene(t0, t1, -280, -305, who="dmks", k="shout")
    lips(P["k"], t0, t1, "shout")
    P["k"].act(t0 + 0.1, "cheer", expr="shout")
    cam = tcam(t0, t1, (-3.5, -9, 7.8), (-1.5, -6.2, 7.2), (-1.5, 2.4, 4.6), None, 28, 34, hh=2.0)
    cam.crash(t0, 24, 34, 0.15)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.1, 1.0, 0.7, "#ffffff", (0, 2.4, -9.5))
    sfx(t0, "whoosh", 0.5)


@S(36, 153, 155, "Mom joined")
def s36(t0, t1):
    E, c, P = scene(t0, t1, -305, -318, who="m", m="shout")
    lips(P["m"], t0, t1, "shout")
    P["m"].act(t0 + 0.1, "cheer", expr="shout")
    cam = tcam(t0, t1, (3.2, -5.8, 5.2), (1.8, -4.0, 5.0), (1.5, -1.0, 4.6), None, 30, 36, hh=2.0)
    cam.crash(t0, 24, 32, 0.12)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.05, 0.7, 0.7, "#ff8ac0", (0, 2.4, -9.5))
    sfx(t0, "whoosh", 0.5)


@S(37, 155, 157, "Dad joined")
def s37(t0, t1):
    E, c, P = scene(t0, t1, -318, -332, who="d", d="shout")
    lips(P["d"], t0, t1, "shout")
    P["d"].act(t0 + 0.1, "cheer", expr="shout")
    cam = tcam(t0, t1, (-3.2, -5.8, 5.2), (-1.8, -4.0, 5.0), (-1.5, -1.0, 4.6), None, 30, 36, hh=2.0)
    cam.crash(t0, 24, 32, 0.12)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.05, 0.6, 0.7, "#8ae0ff", (0, 2.4, -9.5))
    sfx(t0, "whoosh", 0.5)


@S(38, 157, 162, "Even the dog barked it")
def s38(t0, t1):
    E, c, P = scene(t0, t1, -332, -350, who="ks", dog=True, k="grin", s="grin")
    dg = P["dog"]
    swing(dg, t0, t1, 0, 5, 6, 0)
    bounce(dg, t0 + 0.3, t1, 0.15, 7)
    cam = tcam(t0, t1, (0, -7.0, 7.4), (0, -5.0, 6.8), (0, 2.7, 4.4), None, 30, 36, hh=1.2)
    ctext(cam, "WOOF!", t0 + 0.6, 1.0, 1.2, "#ffd36b", (0, 2.4, -9.5))
    sfx(t0 + 0.6, "u_mac-quack", 0.6)
    sfx(t0 + 0.7, "u_duck-toy-sound", 0.5)


@S(39, 162, 166, "Are we there yet? (everybody)")
def s39(t0, t1):
    E, c, P = scene(t0, t1, -350, -378, who="dmks", dog=True, d="shout", m="shout", k="shout", s="shout")
    for ch in (P["d"], P["m"], P["k"], P["s"]):
        lips(ch, t0, t1, "shout")
        ch.act(t0 + 0.1, "cheer", expr="shout")
    cam = tcam(t0, t1, (0, -9.5, 6.5), (0, -6.5, 5.2), (0, 0.5, 4.2), None, 24, 26, hh=2.4)
    cam.crash(t0, 22, 28, 0.15)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.1, 1.2, 0.8, "#ffffff", (0, 2.6, -9.5))
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 0.2, "cheer", 0.4)


@S(40, 166, 167, "Stretch! #1 (big)")
def s40(t0, t1):
    E, c, P = scene(t0, t1, -378, -388, who="dmks")
    road_stretch(E, t0, 1.8, 0.7)
    lava_run(E, t0, t1, 0.3, 0.26)
    cam = tcam(t0, t1, (0, 8, 4), (0, 26, 10), (0, -14, 3), (0, -50, 3), 22, 28, hh=2.4, ease=False)
    ctext(cam, "STRETCH!", t0, 0.8, 0.85, "#7affc8", (0, 2.2, -9))


@S(41, 167, 168, "Stretch! #2 (lava pushed back)")
def s41(t0, t1):
    E, c, P = scene(t0, t1, -388, -396, who="dmks")
    road_stretch(E, t0, 1.9, 0.7)
    lava_run(E, t0, t1, 0.26, 0.2)
    cam = tcam(t0, t1, (7, 6, 3), (16, 22, 10), (0, -14, 3), (0, -50, 4), 22, 26, hh=2.4, ease=False)
    ctext(cam, "STRETCH!", t0, 0.8, 0.85, "#8aff8a", (0, 2.2, -9))


@S(42, 168, 169, "Stretch! #3 (huge)")
def s42(t0, t1):
    E, c, P = scene(t0, t1, -396, -402, who="dmks")
    road_stretch(E, t0, 2.2, 0.9)
    lava_run(E, t0, t1, 0.2, 0.1)
    cam = tcam(t0, t1, (0, 5, 3), (0, 40, 16), (0, -10, 3), (0, -90, 4), 20, 32, hh=3.0, ease=False)
    ctext(cam, "STRETCH!", t0, 1.0, 1.0, "#c8ff7a", (0, 2.2, -9))
    cam.crash(t0, 20, 32, 0.2)
    sfx(t0 + 0.5, "rise", 0.9)


@S(43, 169, 174, "The road stretched like gum")
def s43(t0, t1):
    E, c, P = scene(t0, t1, -300, -330, who="dmks", d="neutral", m="happy", k="grin", s="smile")
    for i, d in enumerate(E["dashes"][:40]):
        pass
    road_stretch(E, t0 + 0.2, 1.6, 1.0)
    cam = tcam(t0, t1, (-9, 1, 2.2), (-14, -9, 4.0), (0, 0, 2.6), None, 20, 26, hh=1.5)
    ctext(cam, "LIKE GUM", t0 + 0.6, 1.0, 1.0, "#ff8ac0", (0, 2.4, -9))
    sfx(t0 + 0.4, "boing", 0.8)


@S(44, 174, 177, "mile after mile (aerial)")
def s44(t0, t1):
    E, c, P = scene(t0, t1, -330, -420, who="dmks")
    cam = tcam(t0, t1, (0, 12, 40), (0, -10, 70), (0, -40, 0), (0, -120, 0), 24, 28, hh=1.0)
    sfx(t0 + 0.1, "whoosh", 0.6)
    sfx(t0 + 0.8, "wind", 0.5)


@S(45, 177, 182, "We drove for four days: sun sweeps")
def s45(t0, t1):
    E, c, P = scene(t0, t1, -300, -360, who="dmks", d="bored", m="bored", k="sleepy", s="sleepy")
    sun = sphere("sunball", 14, (-120, -200, 20), mat("sunm", hexc("#fff0a0"), 0.3, emit=hexc("#ffe070"), estr=8), seg=14)
    move(sun, t0, loc=(-140, -330, 15))
    move(sun, (t0 + t1) / 2, loc=(0, -380, 120))
    move(sun, t1, loc=(140, -330, 15))
    cam = tcam(t0, t1, (-9, 12, 5), (9, 12, 5.4), (0, -4, 4), None, 24, 26, hh=1.2)
    ctext(cam, "4 DAYS", t0 + 0.4, 1.5, 1.0, "#ffe066", (0, 3.0, -9))
    sfx(t0 + 0.4, "pop", 0.7)
    sfx(t0 + 0.5, "crickets", 0.4)


@S(46, 182, 190, "...while the lava slowly cooled into black rock")
def s46(t0, t1):
    E = env(volcano=True)
    c = car(-330)
    drive(c, t0, t1, -330, -345)
    fam(t0, t1, who="dmks", d="bored", m="bored", k="smug", s="sleepy")
    lava_run(E, t0, t0 + 0.1, 0.45, 0.45)
    cool_lava(E, t0, t1 - 0.2)
    cam = tcam(t0, t1, (0, 16, 6), (4, 28, 9), (0, -50, 6), (0, -80, 6), 24, 22, hh=1.2)
    ctext(cam, "COOLING...", t0 + 1.0, 1.6, 0.9, "#8aa0ff", (0, 3.0, -9))
    sfx(t0 + 0.5, "wind", 0.6)
    sfx(t0 + 1.6, "u_correct", 0.3)


@S(47, 190, 193, "Three months later: card")
def s47(t0, t1):
    world((0.4, 0.6, 1.0), 0.9)
    box("card_bg", (80, 1, 50), (0, 4, 0), mat("cardbg2", hexc("#3a7ae0"), 0.8), 0)
    light("cardlight", "AREA", (0, -14, 6), 4000, (1, 1, 1), 18, target=(0, 0, 0))
    ob = text("m3", "3 MONTHS\nLATER", (0, 0, 0), 1.1, mat("m3txt", hexc("#ffffff"), 0.4), rot=(90, 0, 0), extrude=0.25, font=FONT)
    move(ob, t0, rot=(90, 0, 4), scale=0.2)
    move(ob, t0 + 0.2, scale=1.15)
    move(ob, t0 + 0.32, scale=1.0)
    move(ob, t1, rot=(90, 0, -4), scale=1.12)
    cam = Cam()
    cam.key(t0, (0, -16, 0), (0, 0, 0), lens=26)
    cam.key(t1, (0, -11, 0.3), (0, 0, 0), lens=26, ease="EASE_OUT")
    cam.handheld(0.6)
    sfx(t0, "pop", 0.9)
    sfx(t0 + 0.05, "whoosh", 0.7)


@S(48, 193, 197, "we finally pulled up (car stops at Grandma's)")
def s48(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(40)
    drive(c, t0, t0 + 0.9, 40, -52)
    move(c["root"], t1, loc=(0, -60, 0))
    fam(t0, t1, who="dmks", dog=True, d="relief", m="happy", k="happy", s="sleepy")
    cam = Cam()
    cam.key(t0, (14, 20, 5), (0, 10, 3), lens=24)
    cam.key(t1, (12, -36, 4.5), (-1, -56, 3.0), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0, "wind", 0.6)
    sfx(t0 + 0.9, "thud", 0.5)
    sfx(t0 + 0.95, "u_mac-quack", 0.5)


@S(49, 197, 205, "Grandma was on the porch with a pie")
def s49(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    fam(t0, t1, who="dmks", d="relief", m="happy", k="happy", s="sleepy")
    G = grandma(t0, t1, "joy")
    G.pose(t0, loc=(-12.0, -60, 0.6), rot=facing((-12, -60), (0, -60)), armL=(85, -10), armR=(85, -10))
    pie = cyl("pie", 0.8, 0.45, (0, -1.5, 3.2), mat("piem", hexc("#d8a050"), 0.6), 18, parent=G.hip)
    cyl("piec", 0.65, 0.2, (0, -1.5, 3.5), mat("piec", hexc("#8a4a2a"), 0.7), 14, parent=G.hip)
    cam = Cam()
    cam.key(t0, (-1, -48, 5), (-12, -60, 4.0), lens=26)
    cam.key(t1, (-6, -53, 5.0), (-12.4, -60, 4.4), lens=34, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.6, "sparkle", 0.6)
    sfx(t0 + 1.3, "aww", 0.6)


@S(50, 205, 207, "You're late. (Grandma side-eye)")
def s50(t0, t1):
    world((0.95, 0.8, 0.55), 0.8)
    box("gwall", (60, 0.5, 40), (0, 12, 15), mat("gwall2", hexc("#f2d8b0"), 0.8), 0)
    box("gfloor", (60, 40, 0.4), (0, 0, -0.2), mat("gfl2", hexc("#b88a5a"), 0.8), 0)
    light("gl", "AREA", (0, -8, 12), 12000, (1.0, 0.85, 0.7), 12, target=(0, 0, 4))
    G = grandma(t0, t1, "sus")
    G.pose(t0, loc=(0, 4, 0), rot=0)
    G.act(t0 + 0.1, "cross", expr="sus")
    lips(G, t0, t1)
    cam = Cam()
    cam.key(t0, (-1.5, -4.2, 4.6), (0, 4, 4.8), lens=34)
    cam.key(t1, (-0.4, -2.2, 4.8), (0, 4, 4.8), lens=36, ease="EASE_IN")
    cam.handheld(1.0)
    cam.crash(t0, 30, 40, 0.15)
    sfx(t0, "u_slap", 0.4)
    sfx(t0 + 0.5, "rimshot", 0.5)


@S(51, 207, 210, "Dad hugged me")
def s51(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    d = dad(t0, t1, "happy")
    d.pose(t0, loc=(8, -52, 0), rot=facing((8, -52), (9, -52)) + 180)
    k = kid(t0, t1, "happy")
    k.pose(t0, loc=(8, -55, 0), rot=0)
    d.pose(t0, loc=(8, -53.2, 0), rot=180)
    d.act(t0 + 0.2, "hold", expr="smile")
    k.act(t0 + 0.2, "hold", expr="relief")
    cam = Cam()
    cam.key(t0, (14, -62, 5), (8, -54, 4), lens=28)
    cam.key(t1, (11, -58, 5), (8, -54, 4.4), lens=32, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.3, "aww", 0.8)


@S(52, 210, 216, "Best question you ever asked, kiddo")
def s52(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    d = dad(t0, t1, "talk")
    d.pose(t0, loc=(6, -56, 0), rot=0)
    lips(d, t0, t1)
    d.act(t0 + 0.3, "point", expr="smile")
    cam = Cam()
    cam.key(t0, (4, -62, 5.2), (6, -56, 4.8), lens=34)
    cam.key(t1, (5.2, -60, 5.0), (6, -56, 4.8), lens=40, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0 + 1.5, "u_applepay", 0.3)


@S(53, 216, 218, "I smiled")
def s53(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    k = kid(t0, t1, "grin")
    k.pose(t0, loc=(8, -56, 0), rot=0)
    k.act(t0 + 0.1, "cheer", expr="grin")
    cam = Cam()
    cam.key(t0, (8, -63, 5), (8, -56, 4.8), lens=34)
    cam.key(t1, (8, -61, 5), (8, -56, 4.8), lens=40, ease="EASE_OUT")
    cam.handheld(0.8)
    sfx(t0, "sparkle", 0.6)


@S(54, 218, 224, "Then my little sister woke up")
def s54(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    P = fam(t0, t1, who="s", s="sleepy")
    P["s"].face(t0 + 0.9, "gasp")
    P["s"].act(t0 + 0.9, "cheer", expr="gasp")
    cam = tcam(t0, t1, (6, 7, 6.5), (2.2, 4.6, 5.0), (1.5, 2.8, 5.0), None, 30, 38, hh=0.9)
    sfx(t0 + 0.5, "rise", 0.6)
    sfx(t0 + 0.9, "gasp", 0.8)


@S(55, 224, 228, "in the back seat")
def s55(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    P = fam(t0, t1, who="dmks", dog=True, d="smile", m="smile", k="smile", s="smug")
    cam = tcam(t0, t1, (-8, 12, 7.0), (-2.4, 7.6, 5.4), (0, 0, 3.8), (1.5, 2.8, 5.2), 26, 30, hh=1.0)
    sfx(t0 + 0.3, "crickets", 0.5)


@S(56, 228, 232, "Are we there yet? (sister)")
def s56(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    P = fam(t0, t1, who="dmks", d="gasp", m="gasp", k="gasp", s="shout")
    lips(P["s"], t0, t1, "shout")
    P["s"].act(t0 + 0.1, "cheer", expr="shout")
    cam = tcam(t0, t1, (4, -8, 5.8), (2.2, -5.2, 5.0), (1.5, 2.8, 5.2), None, 26, 34, hh=2.2)
    cam.crash(t0, 24, 36, 0.15)
    ctext(cam, "ARE WE\nTHERE YET?", t0 + 0.1, 1.0, 0.7, "#ffffff", (0, 2.4, -9.5))
    sfx(t0, "whoosh", 0.5)
    sfx(t0 + 0.1, "u_slap", 0.4)


@S(57, 232, 233, "Stretch! (house flies away)")
def s57(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    fam(t0, t1, who="dmks", d="terror", m="scream", k="scream", s="shout")
    road_stretch(E, t0, 2.0, 0.6)
    cam = tcam(t0, t1, (0, 8, 4), (0, 34, 12), (0, -14, 3), (0, -60, 3), 22, 28, hh=2.4, ease=False)
    ctext(cam, "STRETCH!", t0, 0.8, 0.85, "#7affc8", (0, 2.2, -9))
    sfx(t0, "u_faaah", 0.5)


@S(58, 233, None, "We're still driving (car drives off to the horizon)")
def s58(t0, t1):
    E = env(volcano=False)
    house(-26, -60)
    c = car(-60)
    drive(c, t0, t1, -60, -330)
    fam(t0, t1, who="dmks", dog=True, d="bored", m="bored", k="sleepy", s="shout")
    cam = tcam(t0, t1, (0, 12, 5), (0, 30, 12), (0, -20, 3.5), (0, -80, 5), 26, 22, hh=1.2)
    ctext(cam, "STILL\nDRIVING...", t0 + 0.7, 2.0, 0.85, "#ffe066", (0, 3.0, -9.5))
    sfx(t0 + 0.2, "wind", 0.7)
    sfx(t0 + 1.2, "u_faaaa", 0.4)
