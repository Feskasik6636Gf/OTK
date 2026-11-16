"""vo4: "When the Wi-Fi dies, the whole family turns into cavemen." Shots keyed to script word indices."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from helpers import rad, move, bounce, swing, stars_pop, C, FONT
from rbx import locs

V = Video(__file__)
story.bind(V)
FURC = "#8a5a32"


# ------------------------------------------------------------------ cast
def dad(t0, t1, expr="neutral"):
    return story._live(chars.Char("Dad", skin="#e9c7a6", shirt="#5aa05a", pants="#3b3f4a", hair="short", hair_color="#4a3020",
                                  face="mustache", sleeves="short", extras=("beard:#6b4a2c",)), t0, t1, expr)


def mom(t0, t1, expr="smile"):
    return story._live(chars.Char("Mom", skin="#efd2b8", shirt="#e8788f", pants="#5a4a7a", hair="bob", hair_color="#6b3f27",
                                  face="girl", sleeves="long"), t0, t1, expr)


def gpa(t0, t1, expr="neutral"):
    return story._live(chars.Char("Grandpa", skin="#ecd0b4", shirt="#7a88c8", pants="#4a4a5a", hair="bald", face="mustache",
                                  sleeves="long", extras=("beard:#e8e8e8", "glasses")), t0, t1, expr)


def gma(t0, t1, expr="smile"):
    return story.grandma(t0, t1, expr)


def sis(t0, t1, expr="neutral"):
    return story._live(chars.Char("Sis", skin="#f2dbc6", shirt="#ffd36b", pants="#e58fc0", hair="bun", hair_color="#c0793a",
                                  face="girl", sleeves="short", scale=0.78), t0, t1, expr)


def kid(t0, t1, expr="neutral"):
    return story._live(chars.eddie(), t0, t1, expr)


def neighbor(i, t0, t1, expr="neutral"):
    return story.townie(i, t0, t1, expr)


def cavefy(ch, t_on=None, t_off=None):
    """Fur tunic + loincloth + bone in the hair + a club in the hand. Visible only between t_on and t_off."""
    Mf = mat("fur", hexc(FURC), 0.95)
    Mp = mat("furspot", hexc("#f0e2c0"), 0.95)
    objs = []
    objs.append(box(ch.name + "_ftun", (2.25, 1.25, 1.5), (0, 0, 0.85), Mf, 0.2, parent=ch.hip, coll=ch.coll))
    objs.append(box(ch.name + "_fskirt", (2.3, 1.3, 0.7), (0, 0, -0.15), Mf, 0.2, parent=ch.hip, coll=ch.coll))
    for i, (x, z) in enumerate(((-0.6, 1.2), (0.5, 0.7), (-0.2, 0.3), (0.7, 1.3))):
        objs.append(sphere(f"{ch.name}_sp{i}", 0.2, (x, -0.65, z), Mp, (1, 0.3, 1), parent=ch.hip, coll=ch.coll, seg=8))
    objs.append(cyl(ch.name + "_bone", 0.1, 0.9, (0.3, 0, 0.9), mat("bone", hexc("#f4efe0"), 0.5), 8, parent=ch.head, coll=ch.coll,
                    rot=(0, 70, 0)))
    objs.append(cyl(ch.name + "_club", 0.3, 3.2, (0, -1.3, -2.0), mat("club", hexc("#6a4228"), 0.8), 10, parent=ch.shR, coll=ch.coll,
                    rot=(90, 0, 0), r2=0.5))
    if t_on is not None:
        for ob in objs:
            sets.set_obj_visible(ob, max(0.0, t_on - 1 / 15), False)
            sets.set_obj_visible(ob, t_on, True)
            if t_off is not None:
                sets.set_obj_visible(ob, t_off, False)
    ch.cave_objs = objs
    return objs


def fire(loc, t_on, t_off=None, s=1.0, intensity=9000):
    Mo = mat("flame_o", hexc("#ff6a10"), 0.4, emit=hexc("#ff5a00"), estr=8.0)
    My = mat("flame_y", hexc("#ffd23a"), 0.4, emit=hexc("#ffc010"), estr=10.0)
    objs = []
    for i, (x, h, c) in enumerate(((0, 2.4, Mo), (-0.5, 1.7, My), (0.5, 1.9, Mo), (0, 1.2, My))):
        f = cyl(f"flame{i}", 0.55 * s, h * s, (loc[0] + x * s, loc[1], loc[2] + h * s / 2), c, 8, r2=0.02)
        noise(f, "scale", 2, 0.35, 5 + i)
        noise(f, "rotation_euler", 1, 0.2, 7 + i)
        objs.append(f)
    for i in range(3):
        objs.append(cyl(f"log{i}", 0.3 * s, 2.4 * s, (loc[0], loc[1], loc[2] + 0.2), mat("log", hexc("#4a2a18"), 0.9), 8,
                        rot=(90, 0, 60 * i - 60)))
    lt = light("firelight", "POINT", (loc[0], loc[1] - 1.0, loc[2] + 1.5 * s), 0, (1.0, 0.55, 0.2), 1.0)
    lt.data.energy = 0
    lt.data.keyframe_insert("energy", frame=F(max(0.0, t_on - 1 / 15)))
    lt.data.energy = intensity * s
    lt.data.keyframe_insert("energy", frame=F(t_on))
    noise(lt.data, "energy", 0, intensity * 0.15 * s, 4) if False else None
    for ob in objs[:4]:
        sets.set_obj_visible(ob, max(0.0, t_on - 1 / 15), False)
        sets.set_obj_visible(ob, t_on, True)
        if t_off:
            sets.set_obj_visible(ob, t_off, False)
    return objs


def poof_at(name, loc, t, s=1.1):
    W2.poof(name, loc, t, s)
    sfx(t, "poof", 0.9)


# ------------------------------------------------------------------ sets
def room(dark=False, snowwin=False, warm=False, burnt=False):
    world((0.06, 0.08, 0.18) if dark else (0.8, 0.78, 0.9), 0.4 if dark else 0.3)
    Mw = mat("rw", hexc("#d8c8e8") if not dark else hexc("#5a5a7a"), 0.85)
    box("rfloor", (26, 28, 0.4), (0, -2, -0.2), sets.planks("rfloor_w"), 0)
    box("rback", (26, 0.6, 14), (0, 10, 7), Mw, 0)
    box("rleft", (0.6, 28, 14), (-12.5, -2, 7), Mw, 0)
    box("rright", (0.6, 28, 14), (12.5, -2, 7), Mw, 0)
    box("rceil", (26, 28, 0.4), (0, -2, 14.2), Mw, 0)
    box("rrug", (9, 7, 0.08), (0, 2, 0.05), mat("rrug", hexc("#c8503a"), 0.95), 0.02)
    # window on the back wall
    locs.window("win", 0, 9.6, 8.0, 6.0, 5.0, collection("WINC"), facing="-Y" if False else "+Y",
                sky=(0.9, 0.95, 1.0) if snowwin else (0.7, 0.88, 1.0), estr=0.9 if not dark else 1.6)
    if snowwin:
        box("snowsill", (6.6, 1.4, 1.6), (0, 9.0, 4.9), mat("snowm", hexc("#f4f8ff"), 0.9), 0.5)
    # couch
    Mc = mat("rcouch", hexc("#3f6fa0") if not burnt else hexc("#1a1a1a"), 0.8)
    box("rc_seat", (8.0, 3.0, 1.6), (0, 6.0, 1.1), Mc, 0.3)
    box("rc_back", (8.0, 1.0, 3.2), (0, 7.4, 2.7), Mc, 0.3)
    for sx in (-1, 1):
        box(f"rc_arm{sx}", (1.2, 3.2, 2.6), (sx * 4.5, 6.0, 1.5), Mc, 0.3)
    # tv + stand
    box("tv_stand", (5.0, 2.0, 2.4), (-7.5, 8.4, 1.2), mat("tvstand", hexc("#7a4a2a"), 0.7), 0.1)
    box("tv_body", (4.8, 0.6, 3.2), (-7.5, 8.4, 4.0), mat("tvb", hexc("#1a1a1e"), 0.4), 0.15)
    box("tv_screen", (4.3, 0.1, 2.7), (-7.5, 8.05, 4.0), mat("tvs", hexc("#0a0a10") if dark else hexc("#2a4a8a"), 0.2,
                                                           emit=hexc("#2a4a8a") if not dark else None, estr=0.8 if not dark else 0), 0.05)
    # shelf + router
    box("shelf", (4.6, 1.4, 0.35), (7.5, 9.1, 6.6), mat("shelfm", hexc("#7a4a2a"), 0.7), 0.05)
    # fireplace on the right wall
    Mb = mat("brick", hexc("#a04a3a"), 0.9)
    box("fp_body", (2.6, 7.5, 8.0), (11.0, 2.0, 4.0), Mb, 0.1)
    box("fp_hole", (0.4, 3.6, 3.4), (9.75, 2.0, 1.9), mat("fphole", hexc("#0a0806"), 1.0), 0.05)
    box("fp_mantel", (3.0, 8.5, 0.5), (10.8, 2.0, 8.2), mat("mantel", hexc("#5a3a22"), 0.7), 0.05)
    if dark:
        light("rfill", "AREA", (0, -10, 12), 5000, (0.5, 0.6, 1.0), 14, target=(0, 3, 3))
    else:
        light("rkey", "AREA", (0, -10, 12), 5500, (1.0, 0.95, 0.9), 14, target=(0, 3, 3))
        light("rkey2", "AREA", (-6, 0, 13), 2200, (1.0, 0.95, 0.9), 10, target=(0, 4, 2))


def router(blink_red=None, green_from=None, off=False, red_steady=False):
    """Router on the shelf; returns its root. LED: blink_red=(t0, t1) alternates red/dark; green_from = time it turns green."""
    r = empty("router", (7.5, 9.1, 6.8))
    box("rt_body", (2.4, 1.0, 0.5), (0, 0, 0.25), mat("rtm", hexc("#e8e8ee"), 0.4), 0.1, parent=r)
    for sx in (-1, 0, 1):
        cyl(f"rt_ant{sx}", 0.06, 1.8, (sx * 0.8, 0.3, 1.2), mat("rtant", hexc("#222222"), 0.4), 6, parent=r, rot=(0, sx * 18, 0))
    Mr = mat("ledred", hexc("#ff2020"), 0.2, emit=hexc("#ff2020"), estr=14)
    Mg = mat("ledgrn", hexc("#30ff50"), 0.2, emit=hexc("#30ff50"), estr=14)
    led_r = sphere("led_r", 0.14, (0.7, -0.52, 0.3), Mr, seg=8, parent=r)
    led_g = sphere("led_g", 0.14, (0.7, -0.52, 0.3), Mg, seg=8, parent=r)
    sets.set_obj_visible(led_g, 0.0, False)
    sets.set_obj_visible(led_r, 0.0, bool(red_steady) or blink_red is not None)
    if off:
        sets.set_obj_visible(led_r, 0.0, False)
    if blink_red:
        t = blink_red[0]
        k = 0
        while t < blink_red[1]:
            sets.set_obj_visible(led_r, t, k % 2 == 0)
            t += 0.22
            k += 1
    if green_from is not None:
        sets.set_obj_visible(led_r, green_from - 1 / 30, False)
        sets.set_obj_visible(led_g, green_from, True)
    return r


def snow(t0, t1, area=((-14, 14), (-14, 6), (3, 15)), n=70, wind=-6.0, seed=2):
    rnd = random.Random(seed)
    M = mat("snowflake", hexc("#ffffff"), 0.8, emit=hexc("#ffffff"), estr=1.0)
    for i in range(n):
        x, y, z = rnd.uniform(*area[0]), rnd.uniform(*area[1]), rnd.uniform(*area[2])
        s = sphere(f"fl{i}", rnd.uniform(0.08, 0.16), (x, y, z), M, seg=6)
        s.keyframe_insert("location", frame=F(t0))
        s.location = (x + wind * (t1 - t0), y, z - 9.0 * (t1 - t0))
        s.keyframe_insert("location", frame=F(t1))
        set_interp(s, "location", F(t1), "LINEAR")


def yard(snowy=False):
    W.sky(1.0)
    W.sun(4.0, rot=(50, 0, 25))
    box("yground", (400, 400, 0.4), (0, 0, -0.25), mat("ysnow" if snowy else "ygrass", hexc("#f0f4ff") if snowy else hexc("#6fc050"), 0.9), 0)
    box("yroad", (400, 9, 0.06), (0, -26, 0.03), mat("yroadm", hexc("#4c4d56"), 0.8), 0)
    box("yhouse", (24, 12, 12), (0, 16, 6), mat("yhw", hexc("#f2c14e"), 0.7), 0.2)
    box("yroof", (26.6, 14.6, 2.2), (0, 16, 13.1), mat("yhr", hexc("#a33b2f"), 0.7), 0.3)
    box("ydoor", (4.0, 0.3, 7.2), (0, 9.85, 3.6), mat("ydoor", hexc("#b8312a"), 0.5), 0.1)
    rnd = random.Random(4)
    for i in range(10):
        x = -90 + i * 20
        if abs(x) < 20:
            continue
        box(f"nh{i}", (14, 11, rnd.uniform(9, 13)), (x, 28, 6), mat(f"nhm{i % 3}", hexc(["#e2725b", "#6fb3e0", "#9b8fd6"][i % 3]), 0.7), 0.2)
    for i in range(6):
        x = rnd.choice((-1, 1)) * rnd.uniform(18, 40)
        cyl(f"yt{i}", 0.7, 5, (x, rnd.uniform(0, 14), 2.5), mat("trunk", hexc("#7a4a2a"), 0.8), 8)
        sphere(f"yc{i}", 3.6, (x, rnd.uniform(0, 14), 7), mat("crown", hexc("#4aa83a") if not snowy else hexc("#dfe8f4"), 0.9), (1, 1, 1.1), seg=10)


def mailbox(x=6.0, y=-10.0):
    cyl("mb_post", 0.25, 4.2, (x, y, 2.1), mat("mbpost", hexc("#6a4a2a"), 0.8), 8)
    mb = box("mb_box", (1.6, 2.4, 1.3), (x, y, 4.6), mat("mbbox", hexc("#2a5ab8"), 0.5), 0.2)
    flag = box("mb_flag", (0.1, 0.1, 1.2), (x + 0.9, y + 0.3, 5.4), mat("mbflag", hexc("#e03a2a"), 0.5), 0.02)
    return mb, flag


def sticks_scene():
    return None


# ------------------------------------------------------------------ cameras
def pc(t0, t1, tgt, d0, d1, yaw, pitch=4, lens=28, yaw1=None, **kw):
    return C(t0, t1, tgt, d0 * 1.35, d1 * 1.3, yaw, pitch, lens, yaw1=yaw1, **kw)


def ctext(cam, body, t, dur=0.9, size=0.8, color="#ffe066", loc=(0, 2.0, -10.0), emit=2.0):
    M = mat("ct_" + color, hexc(color), 0.4, emit=hexc(color), estr=emit)
    ob = text("ct_" + body[:6], body, loc, size, M, rot=(0, 0, 0), extrude=0.08, font=FONT, parent=cam.ob)
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.02))
    for dt, k in ((0.07, 1.25), (0.15, 0.95), (0.22, 1.0)):
        ob.scale = (k,) * 3
        ob.keyframe_insert("scale", frame=F(t + dt))
    ob.keyframe_insert("scale", frame=F(t + dur))
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur + 0.1))
    return ob


POS = dict(d=(-5.5, 2.0), m=(-1.8, 2.5), g=(1.8, 2.5), a=(5.3, 2.0), s=(-3.6, -2.5), k=(3.4, -2.5))


def crew(t0, t1, who="dmgaks", cave=("d", "m", "g", "a", "s"), t_on=0.0, expr=None):
    """Family standing in the living room; cave = who wears the fur; t_on = when the fur appears (0 = from the start)."""
    out = {}
    mk = dict(d=dad, m=mom, g=gpa, a=gma, s=sis, k=kid)
    for w_ in who:
        ch = mk[w_](t0, t1, (expr or {}).get(w_, "neutral") if isinstance(expr, dict) else "neutral")
        x, y = POS[w_]
        ch.pose(t0, loc=(x, y, 0), rot=0)
        if w_ in cave:
            cavefy(ch, t_on if t_on > 0 else None)
        out[w_] = ch
    return out


# ================================================================== SHOTS
@S(1, 0, 5, "HOOK: The router dies (red blink), crash zoom")
def s01(t0, t1):
    room()
    r = router(blink_red=(t0 + 0.3, t1))
    ob = text("wifi", "WI-FI", (7.5, 8.2, 8.9), 0.9, mat("wifit", hexc("#ffffff"), 0.4, emit=hexc("#ffffff"), estr=2), rot=(90, 0, 0), extrude=0.1, font=FONT)
    for sgn in (-1, 1):
        box(f"wx{sgn}", (3.2, 0.12, 0.35), (7.5, 8.1, 8.9), mat("wifix", hexc("#ff2020"), 0.3, emit=hexc("#ff2020"), estr=5), 0.03, rot=(0, sgn * 40, 0))
    cam = Cam()
    cam.key(t0, (4.0, -3.0, 8.0), (7.0, 9.1, 7.2), lens=26)
    cam.key(t1, (7.0, 3.0, 7.4), (7.5, 9.1, 7.0), lens=28, ease="EASE_IN")
    cam.handheld(2.0)
    cam.crash(t0, 22, 34, 0.15)
    sfx(t0 + 0.05, "glitch", 0.9)
    sfx(t0 + 0.3, "buzzer", 0.4)
    sfx(t0 + 0.6, "crickets", 0.3)


@S(2, 5, 9, "my dad tried to hunt: caveman Dad sneaking through the yard")
def s02(t0, t1):
    yard()
    mb, fl = mailbox()
    d = dad(t0, t1, "angry")
    cavefy(d)
    d.pose(t0, loc=(-10, -22, 0), rot=facing((-10, -22), (6, -10)))
    d.pose(t1, loc=(-3, -16, 0))
    d.walk(t0, t1, (-10, -22, 0), (-3, -16, 0), rate=3.0)
    d.pose(t0, armR=(110, -10), torso=(0, 18, 0))
    sp = cyl("spear", 0.12, 5.5, (0, -1.2, -2.0), mat("spear", hexc("#7a5a3a"), 0.7), 8, parent=d.shR, rot=(100, 0, 0))
    cyl("spear_tip", 0.3, 0.9, (0, -1.2, -2.0 - 0.0), mat("speartip", hexc("#d8d8e0"), 0.3, metal=0.5), 8, parent=sp, r2=0.01, rot=(0, 0, 0)).location = (0, 0, 3.1)
    cam = Cam()
    cam.key(t0, (-14, -16, 3.0), (-8, -20, 4.0), lens=26)
    cam.key(t1, (-8, -8, 4.0), (-3, -16, 4.0), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.8)
    sfx(t0, "footsteps", 0.8)
    sfx(t0 + 0.4, "u_mac-quack", 0.3)


@S(3, 9, 12, "hunt our mailbox (the target)")
def s03(t0, t1):
    yard()
    mb, fl = mailbox()
    d = dad(t0, t1, "furious")
    cavefy(d)
    d.pose(t0, loc=(0, -17, 0), rot=facing((0, -17), (6, -10)))
    d.act(t0 + 0.1, "point", expr="furious")
    cam = Cam()
    cam.key(t0, (2.5, 1.0, 5.2), (6, -10, 4.4), lens=30)
    cam.key(t1, (3.4, -1.5, 5.0), (6, -10, 4.4), lens=34, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.1, "rise", 0.6)


@S(4, 12, 15, "with a spear: it flies and sticks in the mailbox")
def s04(t0, t1):
    yard()
    mb, fl = mailbox()
    sp = cyl("spear", 0.12, 5.5, (-4, -17, 4.8), mat("spear", hexc("#7a5a3a"), 0.7), 8, rot=(90, 0, 55))
    tip = cyl("spear_tip", 0.3, 0.9, (0, 0, 3.0), mat("speartip", hexc("#d8d8e0"), 0.3, metal=0.5), 8, parent=sp, r2=0.01)
    move(sp, t0, loc=(-4, -17, 5.5), rot=(90, 0, 55), interp="LINEAR")
    move(sp, t0 + 0.35, loc=(4.5, -10.8, 5.0), rot=(90, 0, 55), interp="LINEAR")
    for i in range(6):
        move(sp, t0 + 0.4 + i * 0.07, loc=(4.5, -10.8, 5.0), rot=(90, 0 if False else (4 if i % 2 else -4), 55))
    move(fl, t0 + 0.35, rot=(0, 0, 0))
    move(fl, t0 + 0.5, rot=(0, 80, 0))
    stars_pop("hit", (5.5, -10.6, 4.8), t0 + 0.35, 8, 1.8, 3, 0.2)
    cam = Cam()
    cam.key(t0, (-8, -9, 5.5), (-4, -15, 5.0), lens=24)
    cam.key(t0 + 0.3, (-2, -4, 6.0), (4, -10.8, 5.0), lens=26)
    cam.key(t1, (-1.5, -2.5, 6.0), (5.5, -10.6, 4.8), lens=30, ease="EASE_OUT")
    cam.handheld(1.4)
    cam.crash(t0 + 0.35, 30, 40, 0.1)
    sfx(t0, "whoosh", 0.8)
    sfx(t0 + 0.35, "u_slap", 0.8)
    sfx(t0 + 0.4, "boing", 0.5)


@S(5, 15, 20, "You see, in this world: kid to camera in the living room")
def s05(t0, t1):
    room()
    router()
    k = kid(t0, t1, "talk")
    k.pose(t0, loc=(0, -2.5, 0), rot=0)
    k.act(t0 + 0.2, "point", expr="smug")
    lips(k, t0, t1)
    cam = pc(t0, t1, (0, -2.5, 4.5), 8.0, 5.0, yaw=-12, lens=30, yaw1=10, hh=1.0)
    cam.crash(t0, 24, 32, 0.15)
    sfx(t0, "whoosh", 0.6)


@S(6, 20, 24, "when the Wi-Fi dies: router goes red, wifi cracks")
def s06(t0, t1):
    room()
    router(blink_red=(t0 + 0.4, t1))
    for sgn in (-1, 1):
        box(f"wx{sgn}", (3.2, 0.12, 0.35), (7.5, 8.1, 8.6), mat("wifix", hexc("#ff2020"), 0.3, emit=hexc("#ff2020"), estr=5), 0.03, rot=(0, sgn * 40, 0))
    cam = Cam()
    cam.key(t0, (2.0, -2.0, 7.6), (7.5, 9.1, 7.0), lens=26)
    cam.key(t1, (6.4, 3.5, 7.2), (7.5, 9.1, 7.0), lens=30, ease="EASE_IN")
    cam.handheld(1.5)
    sfx(t0 + 0.4, "buzzer", 0.5)
    sfx(t0 + 0.5, "glitch", 0.8)


@S(7, 24, 30, "the whole family turns into cavemen: family freezes, wind-up")
def s07(t0, t1):
    room()
    router(blink_red=(t0, t1))
    P = crew(t0, t1, who="dmgas", cave=(), expr=dict(d="neutral", m="neutral", g="neutral", a="neutral", s="neutral"))
    for w_, ch in P.items():
        ch.face(t0 + 0.8, "shock")
        ch.act(t0 + 0.8, "shock", expr="shock")
        noise(ch.hip, "location", 0, 0.1, 2) if t1 - t0 > 1 else None
    cam = pc(t0, t1, (0, 2.5, 4.5), 16, 11, yaw=0, lens=24, yaw1=8, hh=1.5)
    sfx(t0 + 0.7, "rise", 0.8)
    sfx(t1 - 0.3, "zombie", 0.5)


@S(8, 30, 31, "Poof! everyone turns into cavemen")
def s08(t0, t1):
    room()
    router(blink_red=(t0, t1))
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"), t_on=t0 + 0.12)
    for w_, ch in P.items():
        x, y = POS[w_]
        poof_at("poof" + w_, (x, y, 3.5), t0 + 0.1, 1.2)
        ch.act(t0 + 0.2, "cheer", expr="furious")
    cam = pc(t0, t1, (0, 2.5, 4.5), 15, 11, yaw=0, lens=24, hh=2.6)
    cam.crash(t0 + 0.1, 24, 30, 0.15)
    pop = ctext(cam, "POOF!", t0 + 0.1, 0.55, 1.4, "#ffffff", (0, 2.4, -9))
    sfx(t0 + 0.1, "u_capcut-explosion-sound", 0.6)


@S(9, 31, 33, "Fur, clubs: close-up fur + club")
def s09(t0, t1):
    room()
    d = dad(t0, t1, "angry")
    cavefy(d)
    d.pose(t0, loc=(0, 2.0, 0), rot=0)
    d.act(t0 + 0.1, "fists", expr="furious")
    cam = Cam()
    cam.key(t0, (-1.2, -2.5, 4.5), (0, 2.0, 3.2), lens=36)
    cam.key(t1, (1.0, -3.2, 4.0), (0, 2.0, 3.0), lens=36, ease="EASE_IN_OUT")
    cam.handheld(1.5)
    sfx(t0, "whoosh", 0.5)
    sfx(t0 + 0.5, "stomp", 0.6)


@S(10, 33, 35, "the works: whole family posing with clubs")
def s10(t0, t1):
    room()
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"))
    for w_, ch in P.items():
        ch.act(t0 + 0.1, "fists", expr="grin")
    cam = pc(t0, t1, (0, 2.5, 4.0), 13, 10, yaw=-6, lens=24, yaw1=8, hh=1.5)
    sfx(t0 + 0.1, "cheer", 0.5)
    sfx(t0 + 0.2, "u_faaah", 0.3)


@S(11, 35, 43, "everyone panics when the router blinks red")
def s11(t0, t1):
    room()
    router(blink_red=(t0, t1))
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"))
    for w_, ch in P.items():
        ch.act(t0 + 0.3, "hands_head", expr="scream")
        ch.face(t0 + 0.3, "scream")
    for i, (w_, ch) in enumerate(P.items()):
        x, y = POS[w_]
        move(ch.root, t0 + 0.3, loc=(x, y, 0))
        move(ch.root, t0 + 0.55 + i * 0.1, loc=(x + (0.8 if i % 2 else -0.8), y - 0.5, 0.6))
        move(ch.root, t0 + 0.8 + i * 0.1, loc=(x, y, 0))
    cam = Cam()
    cam.key(t0, (6.5, -3.5, 6.5), (7.5, 9.1, 6.8), lens=24)
    cam.key(t1, (1.0, -8.0, 6.0), (0, 3.0, 4.0), lens=26, ease="EASE_IN_OUT")
    cam.handheld(2.6)
    sfx(t0 + 0.3, "alarm", 0.5)
    sfx(t0 + 0.4, "gasp", 0.7)


@S(12, 43, 48, "Moms guard couches like caves")
def s12(t0, t1):
    room()
    m = mom(t0, t1, "furious")
    cavefy(m)
    m.pose(t0, loc=(0, 3.4, 0), rot=0)
    m.act(t0 + 0.1, "fists", expr="furious")
    swing(m.shR, t0 + 0.3, t1, 0, 18, 3, 70)
    cam = pc(t0, t1, (0, 4.5, 3.8), 12, 9, yaw=14, lens=26, yaw1=-10, hh=1.4)
    sfx(t0 + 0.2, "zombie", 0.6)
    sfx(t0 + 0.4, "u_faaah", 0.4)


@S(13, 48, 55, "Grandpas drag the TV by the cord")
def s13(t0, t1):
    room()
    g = gpa(t0, t1, "angry")
    cavefy(g)
    tv = box("tv_drag", (3.6, 1.0, 2.6), (3.0, -2.0, 1.6), mat("tvb2", hexc("#1a1a1e"), 0.4), 0.15)
    box("tv_drag_s", (3.1, 0.1, 2.1), (0, -0.55, 0), mat("tvs2", hexc("#2a4a8a"), 0.2, emit=hexc("#2a4a8a"), estr=0.8), 0.03, parent=tv)
    cord = cyl("cord", 0.08, 3.0, (-1, -2, 0.4), mat("cordm", hexc("#222222"), 0.6), 6, rot=(0, 90, 0))
    move(g.root, t0, loc=(-6, -2, 0), rot=(0, 0, -90))
    g.walk(t0, t1, (-6, -2, 0), (4, -2, 0), rate=2.0)
    g.pose(t0, rot=-90)
    g.pose(t1, rot=-90)
    move(tv, t0, loc=(-9.8, -2, 1.6), interp="LINEAR")
    move(tv, t1, loc=(0.5, -2, 1.6), interp="LINEAR")
    move(cord, t0, loc=(-8.0, -2, 0.4), interp="LINEAR")
    move(cord, t1, loc=(2.0, -2, 0.4), interp="LINEAR")
    cam = Cam()
    cam.key(t0, (-10, -12, 3.5), (-6, -2, 3.0), lens=24)
    cam.key(t1, (2, -12, 3.5), (3, -2, 2.6), lens=28, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0 + 0.2, "footsteps", 0.8)
    sfx(t0 + 0.5, "u_faaaa", 0.2)
    sfx(t0 + 1.4, "stomp", 0.5)


@S(14, 55, 58, "Kids just scream")
def s14(t0, t1):
    room()
    a = neighbor(5, t0, t1, "scream")
    b = neighbor(8, t0, t1, "scream")
    for ch, x in ((a, -1.6), (b, 1.6)):
        ch.pose(t0, loc=(x, 1.0, 0), rot=0)
        ch.act(t0 + 0.1, "hands_head", expr="scream")
        cavefy(ch)
        lips(ch, t0, t1, "shout")
    cam = pc(t0, t1, (0, 1.0, 4.5), 9, 6.5, yaw=0, lens=26, hh=2.0)
    sfx(t0 + 0.1, "gasp", 0.6)


@S(15, 58, 59, "UGGAH!")
def s15(t0, t1):
    room()
    a = neighbor(5, t0, t1, "scream")
    a.pose(t0, loc=(0, 1.0, 0), rot=0)
    cavefy(a)
    a.act(t0, "cheer", expr="furious")
    lips(a, t0, t1, "shout")
    cam = pc(t0, t1, (0, 1.0, 5.2), 6.0, 3.6, yaw=0, lens=34, drop=0.0, hh=3.0)
    cam.crash(t0, 30, 48, 0.12)
    ctext(cam, "UGGAH!", t0, 0.5, 1.2, "#ffd36b", (0, 2.4, -9))
    sfx(t0, "u_slap", 0.6)
    sfx(t0 + 0.05, "boom", 0.4)


@S(16, 59, 67, "I'm the only one who stays human")
def s16(t0, t1):
    room()
    P = crew(t0, t1, who="dmgaks", cave=("d", "m", "g", "a", "s"))
    P["k"].face(t0, "smug")
    P["k"].act(t0 + 0.3, "cross", expr="smug")
    for w_ in "dmgas":
        P[w_].act(t0 + 0.2, "fists", expr="furious")
    cam = Cam()
    cam.key(t0, (-8, -9, 5.0), (0, 1, 4.0), lens=26)
    cam.key(t1, (3.4, -7, 5.0), (3.4, -2.5, 4.6), lens=34, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.6, "rimshot", 0.5)


@S(17, 67, 72, "...because I secretly read paper books")
def s17(t0, t1):
    room()
    k = kid(t0, t1, "smile")
    k.pose(t0, loc=(0, 7.8, 0), rot=0)
    k.act(t0 + 0.1, "hold", expr="smug")
    book = box("book", (1.6, 0.25, 2.0), (0, -1.4, 1.4), mat("bookm", hexc("#d84a3a"), 0.6), 0.05, parent=k.hip, rot=(-30, 0, 0))
    box("book_pg", (1.4, 0.22, 1.8), (0, 0.0, 0.0), mat("bookp", hexc("#f4efe0"), 0.8), 0.02, parent=book)
    for i, (x, s_) in enumerate(((-5, 1.0), (5, 1.2))):
        pass
    cam = pc(t0, t1, (0, 7.2, 4.5), 9, 5.5, yaw=-10, lens=28, yaw1=8, hh=0.8)
    sfx(t0 + 0.6, "paper", 0.7)
    sfx(t0 + 1.2, "sparkle", 0.4)


@S(18, 72, 76, "Then a blizzard hit")
def s18(t0, t1):
    yard(snowy=True)
    snow(t0, t1, ((-30, 30), (-30, 6), (2, 22)), 110, -14.0, 3)
    sfx(t0, "wind", 0.8)
    cam = Cam()
    cam.key(t0, (-6, -40, 10), (0, 14, 6), lens=24)
    cam.key(t1, (4, -30, 8), (0, 14, 6), lens=22, ease="EASE_IN_OUT")
    cam.handheld(3.0)
    ctext(cam, "BLIZZARD", t0 + 0.4, 1.4, 1.1, "#bfe8ff", (0, 2.6, -9))
    sfx(t0 + 0.4, "rise", 0.6)


@S(19, 76, 80, "Power out, internet out: lights die")
def s19(t0, t1):
    room(dark=False)
    router(blink_red=(t0, t0 + 1.0))
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"))
    cam = pc(t0, t1, (0, 3.0, 4.5), 15, 11, yaw=0, lens=24, hh=1.5)
    # lights die: everything goes dark by dimming the key lights
    for ob in list(D.objects):
        if ob.type == "LIGHT" and ob.name.startswith("rkey"):
            ob.data.keyframe_insert("energy", frame=F(t0 + 0.9))
            ob.data.energy = 0
            ob.data.keyframe_insert("energy", frame=F(t0 + 1.0))
    for w_, ch in P.items():
        ch.act(t0 + 1.0, "recoil", expr="gasp")
    sfx(t0 + 0.95, "u_slap", 0.5)
    sfx(t0 + 1.0, "boom", 0.4)
    sfx(t0 + 1.0, "wind", 0.7)


@S(20, 80, 85, "snow up to the windows")
def s20(t0, t1):
    room(dark=True, snowwin=True)
    snow(t0, t1, ((-8, 8), (4, 9), (3, 14)), 50, -3.0, 5)
    cam = Cam()
    cam.key(t0, (-5, -4, 7.2), (0, 9.5, 7.5), lens=26)
    cam.key(t1, (3, 2, 6.5), (0, 9.5, 6.5), lens=34, ease="EASE_IN_OUT")
    cam.handheld(1.8)
    sfx(t0, "wind", 0.8)


@S(21, 85, 91, "The whole street turned into cavemen")
def s21(t0, t1):
    yard(snowy=True)
    snow(t0, t1, ((-30, 30), (-40, 6), (2, 22)), 90, -8.0, 4)
    for i in range(6):
        n = neighbor(2 + i * 3, t0, t1, "angry")
        n.pose(t0, loc=(-12 + i * 5, -14 - (i % 2) * 3, 0), rot=0)
        cavefy(n, t0 + 0.2 + i * 0.12)
        poof_at(f"pf{i}", (-12 + i * 5, -14 - (i % 2) * 3, 3.0), t0 + 0.2 + i * 0.12, 0.9)
        n.act(t0 + 0.3 + i * 0.12, "fists", expr="furious")
    cam = Cam()
    cam.key(t0, (-14, -34, 6), (-6, -15, 3.5), lens=24)
    cam.key(t1, (10, -34, 8), (6, -15, 3.5), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    sfx(t0 + 0.2, "wind", 0.7)


@S(22, 91, 95, "shivering in the dark")
def s22(t0, t1):
    room(dark=True)
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"))
    for w_, ch in P.items():
        noise(ch.hip, "location", 0, 0.16, 1.6)
        ch.act(t0 + 0.1, "cross", expr="worried")
    cam = pc(t0, t1, (0, 2.5, 4.5), 16, 11, yaw=-6, lens=24, yaw1=8, hh=2.4)
    sfx(t0, "wind", 0.6)
    sfx(t0 + 0.3, "crickets", 0.5)


@S(23, 95, 100, "Dad grunted at the fireplace")
def s23(t0, t1):
    room(dark=True)
    d = dad(t0, t1, "angry")
    cavefy(d)
    d.pose(t0, loc=(6.5, 2.0, 0), rot=facing((6.5, 2.0), (10, 2.0)))
    d.act(t0 + 0.2, "point", expr="angry")
    lips(d, t0 + 0.2, t1)
    cam = Cam()
    cam.key(t0, (3.0, -6.0, 5.0), (7.5, 2.0, 3.6), lens=26)
    cam.key(t1, (5.0, -3.5, 4.6), (8.2, 2.0, 3.6), lens=30, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.2, "zombie", 0.5)


@S(24, 100, 102, "Fire... bad?")
def s24(t0, t1):
    room(dark=True)
    d = dad(t0, t1, "confused")
    cavefy(d)
    d.pose(t0, loc=(0, 2.0, 0), rot=0)
    d.act(t0 + 0.1, "think", expr="confused")
    cam = pc(t0, t1, (0, 2.0, 4.8), 7.0, 4.2, yaw=-8, lens=32, yaw1=6, hh=1.0)
    ctext(cam, "FIRE...", t0 + 0.1, 0.7, 0.9, "#ff9a3a", (0, 2.6, -9))
    ctext(cam, "BAD?", t0 + 0.85, 0.9, 1.1, "#ff5a3a", (0, 1.6, -9))
    sfx(t0 + 0.1, "u_mac-quack", 0.4)
    sfx(t0 + 0.9, "u_correct", 0.2)


@S(25, 102, 107, "Mom hid under a blanket")
def s25(t0, t1):
    room(dark=True)
    m = mom(t0, t1, "scared")
    cavefy(m)
    m.pose(t0, loc=(-2.0, 2.5, 0), rot=0)
    bl = box("blanket", (3.6, 2.6, 5.4), (-2.0, 2.2, 2.7), mat("blanketm", hexc("#c84a8a"), 0.9), 0.5)
    move(bl, t0, scale=(1, 1, 0.01))
    move(bl, t0 + 0.4, scale=(1, 1, 1.1))
    move(bl, t0 + 0.55, scale=(1, 1, 1.0))
    noise(bl, "rotation_euler", 1, 0.06, 4)
    cam = pc(t0, t1, (-2.0, 2.4, 3.4), 12, 9, yaw=10, lens=26, yaw1=-8, hh=1.2)
    sfx(t0 + 0.3, "paper", 0.7)
    sfx(t0 + 0.4, "boing", 0.5)


@S(26, 107, 113, "Grandma tried to eat a candle")
def s26(t0, t1):
    room(dark=True)
    g = gma(t0, t1, "grin")
    cavefy(g)
    g.pose(t0, loc=(0, 2.5, 0), rot=0)
    g.act(t0 + 0.1, "hold", expr="grin")
    can = cyl("candle", 0.28, 1.6, (0, -1.5, 3.2), mat("candlem", hexc("#f4efe0"), 0.6), 10, parent=g.hip)
    sphere("candle_fl", 0.22, (0, 0, 0.95), mat("candfl", hexc("#ffd23a"), 0.3, emit=hexc("#ffc010"), estr=8), (1, 1, 1.5), parent=can, seg=8)
    cam = pc(t0, t1, (0, 2.5, 4.6), 8, 4.6, yaw=-8, lens=30, yaw1=10, hh=1.0)
    sfx(t0 + 0.5, "snort", 0.6)
    sfx(t0 + 1.2, "u_duck-toy-sound", 0.5)


@S(27, 113, 117, "Then I noticed something (kid thinks, lightbulb)")
def s27(t0, t1):
    room(dark=True)
    k = kid(t0, t1, "sus")
    k.pose(t0, loc=(0, 3.0, 0), rot=0)
    k.act(t0 + 0.2, "think", expr="sus")
    bulb = sphere("bulb", 0.6, (0, 2.2, 7.2), mat("bulbm", hexc("#fff4a0"), 0.2, emit=hexc("#fff4a0"), estr=12))
    move(bulb, t0, scale=0.01)
    move(bulb, t1 - 0.6, scale=0.01)
    move(bulb, t1 - 0.4, scale=1.3)
    move(bulb, t1 - 0.3, scale=1.0)
    cam = pc(t0, t1, (0, 3.0, 5.0), 8, 4.6, yaw=-8, lens=30, yaw1=6, hh=0.9)
    sfx(t0 + 0.2, "u_correct", 0.5)
    sfx(t1 - 0.4, "ding", 0.8)


@S(28, 117, 122, "Cavemen survived the Ice Age (ice landscape + cavemen)")
def s28(t0, t1):
    world((0.7, 0.85, 1.0), 0.9)
    W.sun(3.6, rot=(45, 0, 30))
    box("iceg", (300, 300, 0.4), (0, 0, -0.2), mat("iceg", hexc("#e8f2ff"), 0.4), 0)
    rnd = random.Random(6)
    for i in range(14):
        sphere(f"ice{i}", rnd.uniform(3, 9), (rnd.uniform(-60, 60), rnd.uniform(14, 70), 1), mat("icem", hexc("#bfe0ff"), 0.2), (1, 1, rnd.uniform(0.6, 1.4)), seg=10)
    for i in range(4):
        n = neighbor(3 + i * 5, t0, t1, "grin")
        n.pose(t0, loc=(-6 + i * 4, 4 + (i % 2) * 2, 0), rot=180)
        cavefy(n)
        n.act(t0 + 0.2 + i * 0.1, "cheer", expr="grin")
    cam = Cam()
    cam.key(t0, (-12, -18, 6), (0, 6, 3.5), lens=24)
    cam.key(t1, (10, -14, 5), (0, 6, 3.5), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    ctext(cam, "ICE AGE", t0 + 0.3, 1.5, 1.0, "#ffffff", (0, 2.8, -9))
    sfx(t0 + 0.3, "wind", 0.7)
    sfx(t0 + 0.4, "pop", 0.7)


@S(29, 122, 128, "They just needed to remember how")
def s29(t0, t1):
    room(dark=True)
    k = kid(t0, t1, "determined")
    k.pose(t0, loc=(0, 3.0, 0), rot=0)
    k.act(t0 + 0.3, "fists", expr="determined")
    cam = pc(t0, t1, (0, 3.0, 4.6), 9, 5.0, yaw=8, lens=28, yaw1=-8, hh=1.0)
    sfx(t0 + 0.2, "rise", 0.6)


@S(30, 128, 132, "I grabbed two sticks")
def s30(t0, t1):
    room(dark=True)
    k = kid(t0, t1, "smug")
    k.pose(t0, loc=(0, 3.0, 0), rot=0)
    k.act(t0 + 0.1, "hold", expr="smug")
    Ms = mat("stickm", hexc("#7a5a3a"), 0.8)
    for sx in (-1, 1):
        cyl(f"stick{sx}", 0.14, 3.0, (sx * 0.5, -1.5, 1.8), Ms, 8, parent=k.hip, rot=(90, 0, sx * 25))
    cam = Cam()
    cam.key(t0, (-1.5, -2.0, 4.2), (0, 2.0, 3.2), lens=34)
    cam.key(t1, (0.6, -2.4, 3.6), (0, 2.0, 3.2), lens=40, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0 + 0.2, "click", 0.7)
    sfx(t0 + 0.4, "paper", 0.5)


@S(31, 132, 135, "Dad, fire, make")
def s31(t0, t1):
    room(dark=True)
    d = dad(t0, t1, "confused")
    cavefy(d)
    d.pose(t0, loc=(2.2, 2.5, 0), rot=0)
    k = kid(t0, t1, "talk")
    k.pose(t0, loc=(-2.2, 2.5, 0), rot=0)
    k.act(t0 + 0.1, "point", expr="talk")
    lips(k, t0, t1)
    cam = Cam()
    cam.key(t0, (0, -8, 5.0), (0, 2.5, 4.0), lens=28)
    cam.key(t1, (0.4, -6.2, 4.8), (0.4, 2.5, 4.2), lens=32, ease="EASE_IN")
    cam.handheld(1.0)
    ctext(cam, "DAD, FIRE,\nMAKE!", t0 + 0.2, 1.1, 0.7, "#ffe066", (0, 2.5, -9))
    sfx(t0 + 0.2, "pop", 0.6)


@S(32, 135, 139, "His eyes lit up")
def s32(t0, t1):
    room(dark=True)
    d = dad(t0, t1, "gasp")
    cavefy(d)
    d.pose(t0, loc=(0, 2.5, 0), rot=0)
    d.act(t0 + 0.3, "cheer", expr="grin")
    for sx in (-1, 1):
        sphere(f"glow{sx}", 0.28, (sx * 0.34, -0.66, 0.12), mat("eyeglow", hexc("#fff4a0"), 0.2, emit=hexc("#fff4a0"), estr=9), (1, 0.4, 1), parent=d.head, seg=10)
    cam = pc(t0, t1, (0, 2.5, 4.9), 7, 3.8, yaw=0, lens=34, drop=0.0, hh=1.0)
    cam.crash(t0 + 0.4, 34, 48, 0.2)
    sfx(t0 + 0.3, "sparkle", 0.8)
    sfx(t0 + 0.4, "u_correct", 0.4)


@S(33, 139, 142, "Rub, rub, rub (sticks, sparks)")
def s33(t0, t1):
    room(dark=True)
    d = dad(t0, t1, "angry")
    cavefy(d)
    d.pose(t0, loc=(8.0, 2.0, 0), rot=facing((8.0, 2.0), (10, 2.0)))
    d.pose(t0, torso=(0, 22, 0))
    wig = cyl("rubstick", 0.14, 2.6, (0, -1.5, -2.6), mat("stickm", hexc("#7a5a3a"), 0.8), 8, parent=d.hip, rot=(90, 0, 0))
    swing(d.shR, t0, t1, 0, 22, 8, 60)
    swing(d.shL, t0, t1, 0, -22, 8, 60)
    for i in range(10):
        stars_pop(f"sp{i}", (9.4, 2.0 + (i % 3 - 1) * 0.3, 2.2), t0 + 0.1 + i * 0.1, 3, 0.8 + (i % 3) * 0.2, i, 0.12, "#ffb030")
    cam = Cam()
    cam.key(t0, (4.5, -2.0, 4.2), (8.6, 2.0, 2.6), lens=34)
    cam.key(t1, (6.2, -0.4, 3.4), (9.0, 2.0, 2.4), lens=42, ease="EASE_IN")
    cam.handheld(3.2)
    sfx(t0, "wind", 0.2)
    sfx(t0 + 0.1, "paper", 0.5)
    sfx(t0 + 0.4, "paper", 0.5)
    sfx(t0 + 0.7, "paper", 0.5)


@S(34, 142, 143, "FOOSH! the fireplace ignites")
def s34(t0, t1):
    room(dark=False)
    fire((10.0, 2.0, 0.6), t0, None, 1.6, 12000)
    cam = Cam()
    cam.key(t0, (4.0, -3.5, 4.0), (10, 2.0, 2.8), lens=28)
    cam.key(t1, (5.6, -1.2, 3.6), (10, 2.0, 2.8), lens=22, ease="EASE_OUT")
    cam.handheld(3.4)
    cam.crash(t0, 28, 20, 0.15)
    ctext(cam, "FOOSH!", t0, 0.6, 1.3, "#ffb030", (0, 2.6, -9))
    sfx(t0, "u_capcut-explosion-sound", 0.7)
    sfx(t0 + 0.02, "whoosh", 0.9)


@S(35, 143, 150, "Mom dragged fur coats from the closet")
def s35(t0, t1):
    room(dark=False)
    fire((10.0, 2.0, 0.6), 0.0, None, 1.3, 7000)
    m = mom(t0, t1, "happy")
    cavefy(m)
    m.root.rotation_euler[2] = rad(90)
    cols = ["#8a5a32", "#b87a42", "#e8d8b8", "#6a4228", "#a8683a"]
    pile = empty("pile", (-10.0, -4.0, 0))
    for i in range(5):
        box(f"fur{i}", (2.6 - i * 0.2, 2.0, 0.7), (0, 0, 0.4 + i * 0.62), mat("furc" + str(i), hexc(cols[i]), 0.95), 0.3, parent=pile, rot=(0, 0, i * 15))
    move(pile, t0, loc=(-10.0, -4.0, 0), interp="LINEAR")
    move(pile, t1, loc=(2.0, -4.0, 0), interp="LINEAR")
    m.walk(t0, t1, (-8.0, -4.0, 0), (4.0, -4.0, 0), rate=2.2)
    m.pose(t0, rot=90)
    m.pose(t1, rot=90)
    cam = Cam()
    cam.key(t0, (-8, -14, 4.0), (-6, -4, 3.0), lens=24)
    cam.key(t1, (4, -14, 4.5), (3, -4, 3.0), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0 + 0.2, "footsteps", 0.8)
    sfx(t0 + 0.5, "u_mac-quack", 0.3)


@S(36, 150, 158, "Grandma roasted a frozen turkey like a mammoth")
def s36(t0, t1):
    room(dark=False)
    fire((10.0, 2.0, 0.6), 0.0, None, 1.3, 7000)
    g = gma(t0, t1, "joy")
    cavefy(g)
    g.pose(t0, loc=(6.8, 2.0, 0), rot=facing((6.8, 2.0), (10, 2.0)))
    g.act(t0 + 0.2, "hold", expr="joy")
    tk = sphere("turkey", 1.4, (9.0, 2.0, 3.4), mat("turkeym", hexc("#d8a060"), 0.6), (1.1, 0.8, 0.8), seg=14)
    for sy in (-1, 1):
        cyl(f"tleg{sy}", 0.3, 1.2, (9.0, 2.0 + sy * 1.4, 3.1), mat("turkeym", hexc("#d8a060"), 0.6), 8, rot=(sy * 40, 0, 0))
    cyl("spit", 0.1, 5, (9.0, 2.0, 3.4), mat("spitm", hexc("#aaaaaa"), 0.3, metal=0.8), 8, rot=(90, 0, 0))
    ice = sphere("ice_c", 1.55, (9.0, 2.0, 3.4), mat("icetk", hexc("#bfe8ff"), 0.15, alpha=0.5), (1.15, 0.85, 0.85), seg=12)
    move(ice, t0 + 1.6, scale=1.0)
    move(ice, t0 + 2.2, scale=0.01)
    swing(tk, t0, t1, 0, 12, 3, 0)
    cam = Cam()
    cam.key(t0, (2.0, -6.0, 5.0), (8, 2.0, 3.4), lens=24)
    cam.key(t1, (6.0, -4.0, 4.4), (9, 2.0, 3.4), lens=30, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    ctext(cam, "MAMMOTH!", t0 + 1.5, 1.4, 1.0, "#ffd36b", (0, 2.6, -9))
    sfx(t0 + 0.2, "sparkle", 0.4)
    sfx(t0 + 1.6, "u_duck-toy-sound", 0.5)
    sfx(t0 + 1.6, "pop", 0.7)


@S(37, 158, 168, "Soon the whole street was packed in our living room")
def s37(t0, t1):
    room(dark=False)
    fire((10.0, 2.0, 0.6), 0.0, None, 1.3, 7000)
    n_ = 0
    for r in range(3):
        for c in range(6):
            n = neighbor(1 + n_ * 2, t0, t1, "happy")
            n.pose(t0, loc=(-8.5 + c * 3.4 + (r % 2) * 1.2, -4 + r * 3.0, 0), rot=0)
            cavefy(n)
            n.act(t0 + 0.2 + (n_ % 5) * 0.12, "cheer", expr="grin")
            n_ += 1
    cam = Cam()
    cam.key(t0, (0, -16, 10), (0, 0, 3.6), lens=24)
    cam.key(t1, (2, -11, 6), (0, 0, 3.6), lens=28, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0 + 0.2, "crowd", 0.6)
    sfx(t0 + 0.6, "cheer", 0.5)


@S(38, 168, 172, "warm and grunting happily")
def s38(t0, t1):
    room(dark=False)
    fire((10.0, 2.0, 0.6), 0.0, None, 1.3, 7000)
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"))
    for w_, ch in P.items():
        ch.act(t0 + 0.2, "cheer", expr="grin")
        bounce(ch.root, t0 + 0.3, t1, 0.06, 5)
    cam = pc(t0, t1, (1, 2.5, 4.2), 12, 8.5, yaw=-14, lens=26, yaw1=4, hh=1.0)
    sfx(t0 + 0.1, "u_faaah", 0.3)
    sfx(t0 + 0.3, "snort", 0.5)
    sfx(t0 + 0.8, "aww", 0.6)


@S(39, 172, 175, "In the morning (sunrise through the window)")
def s39(t0, t1):
    room(dark=False, snowwin=True)
    cam = Cam()
    cam.key(t0, (-3, -6, 6.5), (0, 9.5, 7.8), lens=26)
    cam.key(t1, (2, 0, 7.4), (0, 9.5, 7.8), lens=32, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    ctext(cam, "MORNING", t0 + 0.1, 1.3, 0.9, "#ffe066", (0, 2.8, -9))
    sfx(t0 + 0.1, "sparkle", 0.7)
    sfx(t0 + 0.2, "ding", 0.4)


@S(40, 175, 179, "the router blinked green")
def s40(t0, t1):
    room()
    router(green_from=t0 + 0.7, off=True)
    cam = Cam()
    cam.key(t0, (4.0, 0.0, 7.4), (7.5, 9.1, 7.0), lens=30)
    cam.key(t1, (6.6, 4.5, 7.1), (7.5, 9.1, 7.0), lens=34, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.7, "u_applepay", 0.5)
    sfx(t0 + 0.7, "ding", 0.7)


@S(41, 179, 180, "Poof! back to normal")
def s41(t0, t1):
    room()
    router(green_from=0.0)
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"), t_on=0.0)
    for w_, ch in P.items():
        for ob in ch.cave_objs:
            sets.set_obj_visible(ob, 0.0, True)
            sets.set_obj_visible(ob, t0 + 0.12, False)
        x, y = POS[w_]
        poof_at("poof" + w_, (x, y, 3.5), t0 + 0.1, 1.2)
        ch.act(t0 + 0.25, "shrug", expr="confused")
    cam = pc(t0, t1, (0, 2.5, 4.5), 15, 11, yaw=0, lens=24, hh=2.4)
    cam.crash(t0 + 0.1, 24, 30, 0.15)
    sfx(t0 + 0.1, "u_capcut-explosion-sound", 0.5)


@S(42, 180, 184, "Everyone was normal again")
def s42(t0, t1):
    room()
    router(green_from=0.0)
    P = crew(t0, t1, who="dmgas", cave=())
    for w_, ch in P.items():
        ch.act(t0 + 0.2, "shrug", expr="happy")
    cam = pc(t0, t1, (0, 2.5, 4.5), 11, 8, yaw=-10, lens=26, yaw1=6, hh=1.0)
    sfx(t0 + 0.3, "sparkle", 0.5)


@S(43, 184, 190, "Dad looked at the burnt couch")
def s43(t0, t1):
    room(burnt=True)
    d = dad(t0, t1, "confused")
    d.pose(t0, loc=(0, 3.0, 0), rot=0)
    d.act(t0 + 0.3, "think", expr="confused")
    smoke = sphere("smk", 0.9, (0, 6.0, 4.4), mat("smkm", hexc("#555555"), 1.0, alpha=0.6), seg=10)
    move(smoke, t0, loc=(0, 6.0, 4.4), scale=0.4)
    move(smoke, t1, loc=(0.4, 6.0, 8.0), scale=1.6)
    cam = Cam()
    cam.key(t0, (-4, -8, 5.0), (0, 5, 3.4), lens=26)
    cam.key(t1, (3, -6, 4.4), (0, 5, 3.4), lens=30, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.3, "crickets", 0.6)


@S(44, 190, 194, "Did I... hunt something?")
def s44(t0, t1):
    room(burnt=True)
    d = dad(t0, t1, "confused")
    d.pose(t0, loc=(0, 3.0, 0), rot=0)
    d.act(t0 + 0.1, "shrug", expr="confused")
    cam = pc(t0, t1, (0, 3.0, 4.8), 7, 4.4, yaw=0, lens=32, yaw1=-6, hh=0.9)
    ctext(cam, "?", t0 + 0.9, 1.0, 2.0, "#ffe066", (1.8, 2.2, -9))
    sfx(t0 + 1.0, "u_correct", 0.3)


@S(45, 194, 197, "Mom hugged him")
def s45(t0, t1):
    room(burnt=True)
    d = dad(t0, t1, "smile")
    d.pose(t0, loc=(-0.8, 3.0, 0), rot=0)
    m = mom(t0, t1, "happy")
    m.pose(t0, loc=(1.0, 2.0, 0), rot=0)
    m.act(t0 + 0.2, "hold", expr="relief")
    d.act(t0 + 0.4, "hold", expr="relief")
    cam = pc(t0, t1, (0, 2.5, 4.6), 9, 6, yaw=-12, lens=28, yaw1=8, hh=0.9)
    sfx(t0 + 0.2, "aww", 0.8)


@S(46, 197, 202, "You saved the whole street (cheering neighbors)")
def s46(t0, t1):
    room(burnt=True)
    n_ = 0
    for r in range(3):
        for c in range(6):
            n = neighbor(2 + n_ * 2, t0, t1, "joy")
            n.pose(t0, loc=(-8.5 + c * 3.4 + (r % 2) * 1.2, -4 + r * 3.0, 0), rot=0)
            n.act(t0 + 0.2 + (n_ % 5) * 0.1, "cheer", expr="joy")
            n_ += 1
    d = dad(t0, t1, "grin")
    d.pose(t0, loc=(0, -8, 0), rot=0)
    d.act(t0 + 0.3, "cheer", expr="grin")
    cam = Cam()
    cam.key(t0, (0, -18, 9), (0, 0, 3.6), lens=24)
    cam.key(t1, (3, -13, 6), (0, -1, 3.8), lens=28, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0 + 0.1, "cheer", 0.8)
    sfx(t0 + 0.2, "kids_laugh", 0.5)
    sfx(t0 + 0.4, "confetti", 0.5)


@S(47, 202, 205, "Now, every Sunday: calendar card")
def s47(t0, t1):
    world((0.95, 0.85, 0.5), 0.9)
    box("card_bg", (80, 1, 50), (0, 4, 0), mat("cardbg4", hexc("#ff7a5a"), 0.8), 0)
    light("cardlight", "AREA", (0, -14, 6), 4000, (1, 1, 1), 18, target=(0, 0, 0))
    ob = text("sun", "EVERY\nSUNDAY", (0, 0, 0), 1.3, mat("suntxt", hexc("#ffffff"), 0.4), rot=(90, 0, 0), extrude=0.25, font=FONT)
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


@S(48, 205, 209, "Dad unplugged the router")
def s48(t0, t1):
    room()
    router(green_from=0.0)
    d = dad(t0, t1, "smile")
    d.pose(t0, loc=(5.2, 6.8, 0), rot=facing((5.2, 6.8), (7.5, 9.1)))
    d.act(t0 + 0.3, "reach", expr="grin")
    cord = cyl("plug", 0.06, 2.4, (7.0, 9.0, 5.8), mat("plugm", hexc("#222222"), 0.6), 6, rot=(0, 0, 0))
    move(cord, t0, loc=(7.0, 9.0, 5.8))
    move(cord, t0 + 0.7, loc=(5.5, 8.0, 5.0), rot=(30, 0, 20))
    cam = Cam()
    cam.key(t0, (3.0, -1.0, 6.0), (6.2, 8.5, 5.6), lens=28)
    cam.key(t1, (5.0, 2.8, 6.4), (6.8, 8.8, 5.8), lens=34, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.7, "pop", 0.7)
    sfx(t0 + 0.7, "u_slap", 0.3)


@S(49, 209, 214, "Family cave night, spear optional")
def s49(t0, t1):
    room()
    fire((10.0, 2.0, 0.6), 0.0, None, 1.0, 5000)
    P = crew(t0, t1, who="dmgas", cave=("d", "m", "g", "a", "s"))
    for w_, ch in P.items():
        ch.act(t0 + 0.2, "cheer", expr="grin")
    cyl("spearx", 0.12, 6, (-8.5, 1.0, 3.0), mat("spear", hexc("#7a5a3a"), 0.7), 8, rot=(0, 15, 0))
    cam = Cam()
    cam.key(t0, (-6, -10, 5.0), (0, 2.5, 4.0), lens=24)
    cam.key(t1, (6, -10, 5.0), (0, 2.5, 4.0), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    ctext(cam, "CAVE\nNIGHT", t0 + 0.2, 1.8, 0.9, "#ffd36b", (0, 2.8, -9))
    sfx(t0 + 0.2, "cheer", 0.5)
    sfx(t0 + 0.3, "u_1-108", 0.4)
    sfx(t0 + 1.4, "rimshot", 0.5)


@S(50, 214, 218, "But yesterday, my sister...")
def s50(t0, t1):
    room()
    router(green_from=0.0)
    s = sis(t0, t1, "smug")
    s.pose(t0, loc=(3.5, 4.0, 0), rot=0)
    s.act(t0 + 0.3, "cross", expr="sus")
    cam = pc(t0, t1, (3.5, 4.0, 3.6), 10, 6.5, yaw=-18, lens=28, yaw1=0, hh=1.0)
    sfx(t0 + 0.4, "rise", 0.5)


@S(51, 218, 221, "unplugged it herself")
def s51(t0, t1):
    room()
    router(green_from=0.0, off=False)
    s = sis(t0, t1, "grin")
    s.pose(t0, loc=(5.6, 7.2, 0), rot=facing((5.6, 7.2), (7.5, 9.1)))
    s.act(t0 + 0.2, "reach", expr="grin")
    cam = Cam()
    cam.key(t0, (2.5, 0.5, 5.2), (6.4, 8.8, 4.2), lens=28)
    cam.key(t1, (4.8, 3.2, 5.4), (6.9, 9.0, 4.8), lens=34, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.4, "pop", 0.8)
    sfx(t0 + 0.4, "glitch", 0.7)


@S(52, 221, None, "And she's already sharpening a stick")
def s52(t0, t1):
    room(dark=True)
    s = sis(t0, t1, "grin")
    s.pose(t0, loc=(0, 3.0, 0), rot=0)
    cavefy(s)
    s.act(t0 + 0.2, "hold", expr="smug")
    stick = cyl("sharp", 0.14, 3.0, (0, -1.5, 1.4), mat("stickm", hexc("#7a5a3a"), 0.8), 8, parent=s.hip, rot=(90, 0, 20))
    cyl("sharp_tip", 0.18, 0.6, (0, 0, 1.7), mat("speartip", hexc("#d8d8e0"), 0.3, metal=0.5), 8, parent=stick, r2=0.01)
    swing(s.shL, t0 + 0.4, t1, 0, 14, 7, 60)
    cam = Cam()
    cam.key(t0, (-2.0, -7.0, 3.6), (0, 3.0, 3.0), lens=30)
    cam.key(t1, (0.4, -3.6, 3.6), (0, 3.0, 3.4), lens=36, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.3, "rope", 0.5)
    sfx(t0 + 0.7, "click", 0.6)
    sfx(t0 + 1.3, "zombie", 0.5)
    sfx(t0 + 1.8, "rimshot", 0.4)
