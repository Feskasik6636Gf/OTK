"""numbers: everyone has a number above their head that drops each midnight. Shots keyed to script word indices."""
from shotkit import *
from rbx import story
from rbx.story import *
from rbx import world2 as W2
import math, random
from rbx.sets import wood
from mathutils import Vector

V = Video(__file__)
story.bind(V)

DOORC = ["#8a4bd6", "#ff7a2e", "#2aa7ff", "#ff4f93", "#ffd23a", "#35d0a0", "#e8423a", "#7a5cff", "#40e0e0"]
GREEN = "#2fe86a"
PURPLE = "#a04dff"
HX = 4.62                      # root -> head centre


def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def emitm(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


def hp(p, k=1.0):
    return (p[0], p[1], p[2] + HX * k)


# ================================================================== cast
def hero(t0, t1, expr="neutral", loc=(0, 0, 0), rot=0):
    K = chars.Char("Hero", skin="#e8c39e", shirt="#ff8a3d", pants="#2f3f6a", hair="spiky", hair_color="#5a3a22",
                   face="kid", vneck="#ffc08a")
    story._live(K, t0, t1, expr)
    K.pose(t0, loc=loc, rot=rot)
    return K


def tara(t0, t1, expr="happy", loc=(0, 0, 0), rot=0):
    T = chars.Char("Tara", skin="#c99a72", shirt="#4fbf5a", pants="#2f3f6a", hair="messy", hair_color="#1d1714",
                   face="kid", vneck="#8fe39a")
    story._live(T, t0, t1, expr)
    T.pose(t0, loc=loc, rot=rot)
    return T


def mom(t0, t1, expr="smile", loc=(0, 0, 0), rot=0, fake=False, name="Mom"):
    skin = "#dfe9cc" if fake else "#f1dfc6"
    Mo = chars.Char(name, skin=skin, shirt="#e8744a", pants="#2b2b3a", hair="bob", hair_color="#7a3a1e",
                    face="girl", sleeves="long", vneck="#f6c0a8")
    story._live(Mo, t0, t1, expr)
    Mo.pose(t0, loc=loc, rot=rot)
    return Mo


def dad(t0, t1, expr="neutral", loc=(0, 0, 0), rot=0, fake=False):
    skin = "#dfe9cc" if fake else "#e9c7a6"
    D_ = chars.Char("Dad", skin=skin, shirt="#3f7fd9", pants="#c8b48a", hair="short", hair_color="#3a2a1e",
                    face="mustache", vneck="#f4f4f4")
    story._live(D_, t0, t1, expr, 0.6)
    D_.pose(t0, loc=loc, rot=rot)
    return D_


def sit_on(ch, t, seat_top, rot=0, **kw):
    x, y, z = seat_top
    ch.pose(t, loc=(x, y, z - 1.96), rot=rot, legL=(85, 3), legR=(85, -3), armL=(30, 6), armR=(30, 6), **kw)


# ================================================================== fx helpers
def pop(ob, t, s=1.0, dur=0.24):
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.04))
    ob.scale = (s * 1.15,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur * 0.6))
    ob.scale = (s,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur))


def shrink(ob, t, s=1.0, dur=0.28):
    ob.scale = (s,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.04))
    ob.scale = (s * 1.12,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur * 0.3))
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t + dur))


def pop_text(name, body, loc, t, size=1.0, col="#ffe14a", yaw=0, dur=None, outline="#1a1a22"):
    root = empty(name, loc, rot=(0, 0, yaw))
    text(name + "_t", body, (0, 0, 0), size, emitm(col, 2.5), extrude=0.08 * size, parent=root)
    text(name + "_o", body, (0.04 * size, 0.06 * size, -0.04 * size), size, M(outline, 0.6), extrude=0.06 * size, parent=root)
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


def sparkles(name, loc, t, s=1.0, n=10, seed=0, col="#bfffd0"):
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


def flash(name, t, dur=0.2, col=(1, 1, 1), at=(0, -3, 6), e=40000):
    lt = light(name, "POINT", at, 0, col, 3.0)
    lt.data.keyframe_insert("energy", frame=F(t - 0.03))
    lt.data.energy = e
    lt.data.keyframe_insert("energy", frame=F(t + 0.03))
    lt.data.energy = 0
    lt.data.keyframe_insert("energy", frame=F(t + dur))


# ================================================================== props
def door(name, loc, color, rot=0, s=1.0, glow=2.0, portal=None, coll=None):
    """Glowing door in a dark frame. Hinged panel `piv` swings away from the viewer (rotation z > 0)."""
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    Mf = M("#15151e", 0.6)
    box(name + "_fl", (0.7, 0.8, 8.8), (-2.15, 0, 4.4), Mf, 0.05, parent=root, coll=coll)
    box(name + "_fr", (0.7, 0.8, 8.8), (2.15, 0, 4.4), Mf, 0.05, parent=root, coll=coll)
    box(name + "_ft", (5.0, 0.8, 0.7), (0, 0, 8.55), Mf, 0.05, parent=root, coll=coll)
    if portal:
        box(name + "_pt", (3.6, 0.1, 8.2), (0, 0.3, 4.1), emitm(portal, 3.5), 0.0, parent=root, coll=coll)
    piv = empty(name + "_piv", (-1.8, -0.15, 0), parent=root, coll=coll)
    box(name + "_pn", (3.6, 0.3, 8.2), (1.8, 0, 4.1), emitm(color, glow), 0.06, parent=piv, coll=coll)
    box(name + "_i1", (2.5, 0.1, 3.2), (1.8, -0.2, 5.9), M(color, 0.5), 0.05, parent=piv, coll=coll)
    box(name + "_i2", (2.5, 0.1, 2.6), (1.8, -0.2, 2.4), M(color, 0.5), 0.05, parent=piv, coll=coll)
    sphere(name + "_kn", 0.25, (3.1, -0.4, 4.0), M("#e2b23a", 0.25, metal=0.9), parent=piv, coll=coll, seg=10)
    return root, piv


def swing(piv, t, ang=100, dur=0.45, a0=0):
    piv.rotation_euler = (0, 0, math.radians(a0))
    piv.keyframe_insert("rotation_euler", frame=F(t))
    piv.rotation_euler = (0, 0, math.radians(ang))
    piv.keyframe_insert("rotation_euler", frame=F(t + dur))


def slam(piv, t, a_open=100, dur=0.12):
    piv.rotation_euler = (0, 0, math.radians(a_open))
    piv.keyframe_insert("rotation_euler", frame=F(t))
    piv.rotation_euler = (0, 0, 0)
    piv.keyframe_insert("rotation_euler", frame=F(t + dur))
    set_interp(piv, "rotation_euler", F(t), "BEZIER", "EASE_IN")


def clouds_glow(col, n=6, seed=0, at=(0, 0, 0), spread=(30, 20)):
    rnd = random.Random(seed)
    for i in range(n):
        light(f"gl{i}_{seed}", "POINT", (at[0] + rnd.uniform(-1, 1) * spread[0], at[1] + rnd.uniform(0, 1) * spread[1], 6),
              3500, col, 3.0)


def beach_card(name, loc, coll=None, s=1.0, t0=0.0):
    """Flat beach 'painting' (sky, water of cubes, sand) used as the view through the purple door."""
    root = empty(name, loc, coll=coll)
    root.scale = (s,) * 3
    box(name + "_sky", (3.6, 0.1, 5.2), (0, 0.2, 5.7), emitm("#8fd8ff", 2.2), 0, parent=root, coll=coll)
    sphere(name + "_sun", 0.7, (0.9, 0.0, 7.4), emitm("#fff2a0", 6), parent=root, coll=coll)
    box(name + "_sand", (3.6, 0.1, 2.2), (0, 0.2, 1.1), emitm("#f0d890", 1.6), 0, parent=root, coll=coll)
    for i in range(5):
        wv = box(f"{name}_w{i}", (0.8, 0.5, 0.8), (-1.5 + i * 0.75, -0.1, 3.2), emitm("#2f9bff", 2.0), 0.03, parent=root, coll=coll)
        noise(wv, "location", 2, 0.35, 5 + i)
    return root


def beach_full(c=None):
    """Full beach set (Tarasic's side). Camera from -Y, water behind (+Y)."""
    world((0.55, 0.8, 1.0), 1.0)
    c = c or collection("BEACH")
    box("bf_sand", (200, 120, 0.4), (0, 20, -0.2), M("#f0d890", 0.9), 0, coll=c)
    box("bf_sea", (200, 80, 0.3), (0, 90, 0.0), M("#2f9bff", 0.15, metal=0.2), 0, coll=c)
    sphere("bf_sun", 6, (-40, 220, 80), emitm("#fff2a0", 8), coll=c)
    light("bf_key", "SUN", (0, 0, 50), 4.0, (1.0, 0.95, 0.85), 2.0, rot=(50, 0, 25), coll=c)
    rnd = random.Random(3)
    for i in range(34):
        x, y = -30 + (i % 17) * 3.6, 34 + (i // 17) * 5.0
        wv = box(f"bf_w{i}", (3.0, 3.0, 3.0), (x, y, 1.0), M("#3aa7ff", 0.1, metal=0.3), 0.15, coll=c)
        noise(wv, "location", 2, 0.8, 6 + (i % 5))
    sand_ball = sphere("bf_ball", 1.1, (6, 6, 1.1), M("#ff4f93", 0.4), coll=c)
    return c


def street(t0=0.0, t1=1.0, n=40, seed=1, dawn=False, school=False, pop_in=True, clear=8.0, tint=None):
    rnd = random.Random(seed)
    if dawn:
        world((1.0, 0.6, 0.35), 0.9)
    else:
        world((0.05, 0.06, 0.16), 0.55)
    c = collection("STREET")
    box("st_ground", (400, 400, 0.4), (0, 60, -0.2), M("#5a4a52" if dawn else "#1c2034", 0.9), 0, coll=c)
    box("st_road", (26, 400, 0.42), (0, 60, -0.18), M("#6a5a60" if dawn else "#2a2f48", 0.8), 0, coll=c)
    for i in range(16):
        x = -110 + i * 14 + rnd.uniform(-3, 3)
        h = rnd.uniform(16, 44)
        box(f"st_b{i}", (11, 8, h), (x, 105, h / 2), M("#3a3550" if dawn else "#151a2c", 0.9), 0, coll=c)
        for k in range(rnd.randint(2, 5)):
            card(f"st_w{i}_{k}", 1.6, 2.0, (x + rnd.uniform(-3.5, 3.5), 100.9, rnd.uniform(4, h - 3)),
                 emitm("#ffd890", 1.4), "-Y", coll=c)
    if dawn:
        sp = sphere("st_sun", 9, (10, 150, 14), emitm("#ffb24a", 9), coll=c)
        light("st_key", "SUN", (0, 0, 50), 3.5, (1.0, 0.65, 0.4), 2.0, rot=(75, 0, 170), coll=c)
    else:
        sphere("st_moon", 8, (-40, 160, 70), emitm("#dfe8ff", 6), coll=c)
        light("st_key", "SUN", (0, 0, 50), 1.6, (0.55, 0.65, 1.0), 2.0, rot=(55, 0, 25), coll=c)
        light("st_fill", "AREA", (0, -14, 12), 1600, (0.7, 0.75, 1.0), 14, coll=c, target=(0, 0, 4))
    if school:
        box("sc_wall", (60, 8, 20), (0, 30, 10), M("#8a4a3a", 0.9), 0.1, coll=c)
        box("sc_roof", (62, 9, 1.2), (0, 30, 20.4), M("#4a2a28", 0.8), 0.1, coll=c)
        for k in range(8):
            card(f"sc_win{k}", 3.0, 3.6, (-24 + k * 6.8, 25.9, 11), emitm("#ffd890", 0.6), "-Y", coll=c)
        text("sc_sign", "SCHOOL", (0, 25.6, 17.2), 3.0, emitm("#f4f4f4", 1.6), extrude=0.2, coll=c)
    doors = []
    tmax = max(0.2, (t1 - t0) * 0.7)
    for i in range(n):
        for _ in range(20):
            x, y = rnd.uniform(-48, 48), rnd.uniform(10, 80)
            if abs(x) > clear or y > 24:
                break
        col = DOORC[rnd.randrange(len(DOORC))]
        rt, pv = door(f"dr{i}", (x, y, 0), col, rot=rnd.uniform(-22, 22), s=rnd.uniform(0.9, 1.5), portal="#ffffff", coll=c)
        doors.append((rt, pv, col))
        if pop_in:
            pop(rt, t0 + rnd.uniform(0, tmax), rt.scale[0])
    return c, doors


# ---------------------------------------------------------------- interiors
def kitchen(mood="dinner", ceil=False, door_gap=True, door_t=None, chairs=True):
    c = collection("KITCH")
    if mood == "dawn":
        world((1.0, 0.75, 0.5), 0.8)
        wallc, flc, wc = "#f0d8b0", "#d9b890", "#ffd890"
    elif mood == "dark":
        world((0.01, 0.015, 0.02), 0.2)
        wallc, flc, wc = "#2a3a34", "#1c2420", "#10261c"
    elif mood == "creep":
        world((0.05, 0.08, 0.08), 0.3)
        wallc, flc, wc = "#6a8a78", "#3a4a44", "#3a8a60"
    else:
        world((0.1, 0.12, 0.25), 0.4)
        wallc, flc, wc = "#c9b99a", "#8a6a4a", "#1a2a5a"
    box("k_floor", (60, 40, 0.4), (0, -2, -0.2), sets.checker_mat("k_fl_" + mood, flc, "#" + "3a3a3a" if mood == "dark" else flc, 0.2), 0, coll=c)
    box("k_back", (60, 0.5, 16), (0, 8.25, 8), M(wallc, 0.85), 0, coll=c)
    box("k_left", (0.5, 40, 16), (-18, -2, 8), M(wallc, 0.85), 0, coll=c)
    box("k_right", (0.5, 40, 16), (18, -2, 8), M(wallc, 0.85), 0, coll=c)
    Mw = M(wallc, 0.85)
    if door_gap:
        box("k_fw1", (13.5, 0.5, 16), (-11.25, -14.25, 8), Mw, 0, coll=c)
        box("k_fw2", (13.5, 0.5, 16), (11.25, -14.25, 8), Mw, 0, coll=c)
        box("k_fw3", (9, 0.5, 6.8), (0, -14.25, 12.6), Mw, 0, coll=c)
    else:
        box("k_fw", (60, 0.5, 16), (0, -14.25, 8), Mw, 0, coll=c)
    if ceil:
        box("k_ceil", (60, 40, 0.8), (0, -2, 16.0), M("#d8d2c4", 0.95), 0, coll=c)
    counter = M("#4f86c6", 0.6)
    box("k_counter", (22, 3.2, 2.8), (4, 6.5, 1.4), counter, 0.06, coll=c)
    box("k_top", (22.4, 3.5, 0.2), (4, 6.4, 2.9), M("#f4f1ea", 0.25), 0.04, coll=c)
    # stove
    box("k_stove", (4.4, 3.4, 3.0), (7, 6.4, 1.5), M("#d8dce4", 0.3, metal=0.4), 0.08, coll=c)
    for bx in (-1, 1):
        for by in (-1, 1):
            cyl(f"k_bur{bx}{by}", 0.55, 0.06, (7 + bx * 1.0, 6.4 + by * 0.8, 3.02), M("#18181c", 0.4), 16, coll=c)
    cyl("k_pan", 0.9, 0.22, (6.0, 5.8, 3.15), M("#222226", 0.3, metal=0.6), 20, coll=c)
    box("k_panh", (1.6, 0.25, 0.14), (7.4, 5.8, 3.2), M("#222226", 0.3), 0.04, coll=c)
    for i in range(3):
        cyl(f"k_pc{i}", 0.62, 0.12, (6.0, 5.8, 3.33 + i * 0.14), M("#d9a050", 0.6), 16, coll=c)
    # hood + window + fridge
    box("k_hood", (4.6, 2.4, 1.4), (7, 7.0, 9.4), M("#c8ccd4", 0.3, metal=0.6), 0.1, coll=c)
    box("k_wfr", (5.4, 0.3, 4.6), (-6, 7.95, 8.2), M("#f4f4f4"), 0.04, coll=c)
    wcard = card("k_wsky", 4.8, 4.0, (-6, 7.78, 8.2), emitm(wc, 2.5 if mood != "dark" else 0.4), "-Y", coll=c)
    box("k_fridge", (4, 3.6, 9), (-14, 6.2, 4.5), M("#e8eef4", 0.25, metal=0.3), 0.15, coll=c)
    # table + chairs
    Mt = wood("k_tab", "#a0703f", "#c89260", 2.0)
    box("k_table", (13, 5, 0.3), (0, -5.5, 2.65), Mt, 0.06, coll=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"k_tl{sx}{sy}", (0.35, 0.35, 2.5), (sx * 5.8, -5.5 + sy * 2.1, 1.25), M("#704a2a"), 0.02, coll=c)
    for i, x in enumerate((-4.5, 0, 4.5) if chairs else ()):
        box(f"k_ch{i}", (2.6, 2.6, 0.3), (x, -1.2, 1.85), M("#c0392b", 0.6), 0.08, coll=c)
        box(f"k_cb{i}", (2.6, 0.3, 3.0), (x, -0.1, 3.4), M("#c0392b", 0.6), 0.08, coll=c)
        for sx in (-1, 1):
            for sy in (-1, 1):
                box(f"k_cl{i}{sx}{sy}", (0.25, 0.25, 1.8), (x + sx * 1.1, -1.2 + sy * 1.1, 0.9), M("#704a2a"), 0.02, coll=c)
    cyl("k_plate", 0.9, 0.1, (-4.5, -5.0, 2.85), M("#f4f4f4", 0.2), 22, coll=c)
    cyl("k_plate2", 0.9, 0.1, (0, -5.0, 2.85), M("#f4f4f4", 0.2), 22, coll=c)
    cyl("k_plate3", 0.9, 0.1, (4.5, -5.0, 2.85), M("#f4f4f4", 0.2), 22, coll=c)
    for i in range(3):
        sphere(f"k_mush{i}", 0.34, (-4.9 + i * 0.4, -5.0, 3.05), M("#c8b49a", 0.7), (1, 1, 0.7), coll=c)
    # the exit door (green) in the front wall, facing into the room
    pv = None
    if door_gap:
        rt, pv = door("k_exit", (0, -14.0, 0), GREEN, rot=180, s=1.0, glow=2.5, coll=c)
    # lights
    if mood == "dinner":
        sphere("k_shade", 1.3, (0, -5, 9.2), emitm("#ffd890", 3.0), (1, 1, 0.5), coll=c)
        light("k_lamp", "POINT", (0, -5, 8.4), 9000, (1.0, 0.82, 0.55), 2.0, coll=c)
        light("k_fill", "AREA", (0, -16, 10), 3500, (0.7, 0.75, 1.0), 14, coll=c, target=(0, 0, 3))
    elif mood == "dawn":
        light("k_key", "AREA", (-6, -4, 11), 6500, (1.0, 0.85, 0.6), 10, coll=c, target=(2, 0, 3))
        light("k_fill", "AREA", (0, -16, 9), 2500, (1.0, 0.9, 0.75), 14, coll=c, target=(0, 0, 3))
    elif mood == "dark":
        light("k_dg", "POINT", (0, -12, 6), 6000, (0.2, 1.0, 0.45), 2.0, coll=c)
        light("k_df", "POINT", (0, -2, 8), 3500, (0.4, 1.0, 0.6), 2.0, coll=c)
    else:
        light("k_key", "AREA", (0, -8, 12), 5000, (0.6, 1.0, 0.75), 14, coll=c, target=(0, 0, 3))
        light("k_dg", "POINT", (0, -12, 6), 4000, (0.2, 1.0, 0.45), 2.0, coll=c)
        light("k_fill", "AREA", (0, -16, 10), 1800, (0.8, 0.5, 1.0), 14, coll=c, target=(0, 0, 3))
    return c, pv, wcard


def ceiling_faces(t0, t1, n_x=5, n_y=3, seed=2, z=15.7):
    """Mom's smile, pressed into the plaster (upside-down heads poking out of the ceiling)."""
    rnd = random.Random(seed)
    out = []
    for i in range(n_x):
        for j in range(n_y):
            x = -10 + i * 5 + rnd.uniform(-1, 1)
            y = -6 + j * 5.5 + rnd.uniform(-1, 1)
            F_ = mom(t0, t1, "grin", name=f"Face{i}_{j}", fake=True)
            F_.root.location = (x, y, z + 4.9)
            F_.root.rotation_euler = (math.pi, 0, math.pi + rnd.uniform(-0.4, 0.4))
            F_.root.scale = (1.25,) * 3
            F_.root.keyframe_insert("location", frame=F(t0))
            F_.root.keyframe_insert("rotation_euler", frame=F(t0))
            F_.root.keyframe_insert("scale", frame=F(t0))
            F_.face(t0 + rnd.uniform(0, 0.6), eyes=rnd.choice(["side_l", "side_r", "normal"]), mouth="grin")
            out.append(F_)
    return out


def hallway(t0, t1, gold_t=None, L=140, breathe=True):
    world((0.03, 0.03, 0.05), 0.25)
    c = collection("HALL")
    cy = L / 2 - 14
    box("h_floor", (14, L, 0.4), (0, cy, -0.2), M("#3a2630", 0.5), 0, coll=c)
    ceil = box("h_ceil", (14, L, 0.4), (0, cy, 12), M("#4a3040", 0.9), 0, coll=c)
    wl = box("h_wl", (0.5, L, 12), (-7.2, cy, 6), M("#5a3a4a", 0.9), 0, coll=c)
    wr = box("h_wr", (0.5, L, 12), (7.2, cy, 6), M("#5a3a4a", 0.9), 0, coll=c)
    if breathe:
        k = 0
        t = t0
        while t < t1 + 0.4:
            a = 0.45 if k % 2 == 0 else -0.45
            for wob, sx in ((wl, -7.2), (wr, 7.2)):
                wob.location = (sx - math.copysign(a, sx), cy, 6)
                wob.keyframe_insert("location", frame=F(t))
            ceil.location = (0, cy, 12 + a * 0.6)
            ceil.keyframe_insert("location", frame=F(t))
            t += 0.42
            k += 1
    for i in range(7):
        y = i * 18 - 6
        for sx in (-1, 1):
            door(f"h_d{i}{sx}", (sx * 6.9, y, 0), "#7a4a6a", rot=90 * sx * -1 + 180 if False else (90 if sx < 0 else -90),
                 s=1.0, glow=0.6, coll=c)
        light(f"h_l{i}", "POINT", (0, y, 10), 11000, (1.0, 0.6, 0.5), 3.0, coll=c)
    wincol = ["#2a4aa0", "#ffc83a"]
    win = box("h_win", (6, 0.4, 7), (0, -14.0, 6.2), emitm(wincol[0], 3.5), 0.2, coll=c)
    box("h_winf", (6.8, 0.3, 7.8), (0, -13.8, 6.2), M("#1a1a22", 0.6), 0.1, coll=c)
    lt = light("h_wl", "POINT", (0, -12, 6), 2000, (0.3, 0.4, 1.0), 3.0, coll=c)
    if gold_t is not None:
        m = win.data.materials[0].copy() if False else None
        mg = emitm(wincol[1], 7.0)
        win.data.materials.append(mg)
        win.data.materials[0] = emitm(wincol[0], 3.5)
        # swap material by hiding: make a second plane that pops in gold
        gw = box("h_wing", (6, 0.4, 7), (0, -14.2, 6.2), emitm(wincol[1], 8.0), 0.2, coll=c)
        sets.set_obj_visible(gw, gold_t - 1.0 / 30, False)
        sets.set_obj_visible(gw, gold_t, True)
        lt.data.keyframe_insert("energy", frame=F(gold_t - 0.05))
        lt.data.color = (1.0, 0.8, 0.3)
        lt.data.energy = 9000
        lt.data.keyframe_insert("energy", frame=F(gold_t + 0.2))
        lt.data.keyframe_insert("color", frame=F(gold_t + 0.2))
    return c, win


def dawn_ground():
    return street(0, 1, n=14, seed=9, dawn=True, pop_in=False, clear=10)


def camL(t0, t1, p, d0=8.0, d1=5.5, yaw=0.0, pitch=4.0, lens=40, yaw1=None, fs=2.0, roll=0.0, hh=0.9, k=1.0):
    cam = Cam()
    cam.push(t0, t1, hp(p, k), d0, d1, yaw=yaw, pitch=pitch, lens=lens, yaw1=yaw1, fstop=fs, roll=roll)
    cam.handheld(hh)
    return cam


RED = "#ff4a4a"
GOLD = "#ffe14a"


def numtag(ch, body, col=GOLD, size=1.3, z=7.7, t_on=None, t_off=None, tag=""):
    nm = f"nt_{ch.name}_{body}_{tag}"
    root = empty(nm, (0, 0, z), parent=ch.root)
    text(nm + "_t", body, (0, 0, 0), size, emitm(col, 3.0), extrude=0.14 * size, parent=root)
    text(nm + "_o", body, (0.05 * size, 0.09 * size, -0.05 * size), size, M("#101018", 0.6), extrude=0.12 * size, parent=root)
    noise(root, "location", 2, 0.18, 12)
    noise(root, "rotation_euler", 2, 0.05, 9)
    if t_on is not None:
        pop(root, t_on, 1.0, 0.22)
    if t_off is not None:
        shrink(root, t_off, 1.0, 0.18)
    return root


def numseq(ch, seq, col=GOLD, size=1.3, z=7.7, t0=0.0):
    """seq: [(t, 'text')]; the first entry is shown from the start if t <= t0."""
    for k, (t, b) in enumerate(seq):
        off = seq[k + 1][0] if k + 1 < len(seq) else None
        numtag(ch, b, col, size, z, None if (k == 0 and t <= t0) else t, off, tag=str(k))


def clock(loc, t_strike=None, rot=0, s=1.0, coll=None, minute0=-35):
    root = empty("clk", loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    cyl("clk_r", 1.55, 0.2, (0, 0.08, 0), M("#2a2a3a", 0.4), 32, rot=(90, 0, 0), parent=root, coll=coll)
    cyl("clk_b", 1.4, 0.25, (0, 0, 0), M("#f6f0e0", 0.5), 32, rot=(90, 0, 0), parent=root, coll=coll)
    for k in range(12):
        a = math.radians(k * 30)
        box(f"clk_t{k}", (0.1, 0.05, 0.22), (math.sin(a) * 1.15, -0.15, math.cos(a) * 1.15), M("#1a1a1a"), 0.0, parent=root,
            coll=coll, rot=(0, -k * 30, 0))
    hp_ = empty("clk_hp", (0, -0.17, 0), parent=root, coll=coll)
    box("clk_h", (0.14, 0.05, 0.8), (0, 0, 0.4), M("#1a1a1a"), 0.02, parent=hp_, coll=coll)
    mp = empty("clk_mp", (0, -0.2, 0), parent=root, coll=coll)
    box("clk_m", (0.09, 0.05, 1.15), (0, 0, 0.57), M("#c8261e"), 0.02, parent=mp, coll=coll)
    if t_strike is not None:
        mp.rotation_euler = (0, math.radians(minute0), 0)
        mp.keyframe_insert("rotation_euler", frame=F(t_strike - 1.5))
        mp.rotation_euler = (0, 0, 0)
        mp.keyframe_insert("rotation_euler", frame=F(t_strike))
    else:
        mp.rotation_euler = (0, math.radians(minute0), 0)
        noise(mp, "rotation_euler", 1, 0.05, 6)
    return root


def city(t0=0.0, t1=1.0, night=False, people=8, seed=1, tower=True, sunlit=True):
    rnd = random.Random(seed)
    if night:
        world((0.05, 0.06, 0.16), 0.5)
    else:
        world((0.22, 0.5, 1.0), 1.3)
    c = collection("CITY")
    box("ct_ground", (400, 400, 0.4), (0, 60, -0.2), M("#2a2f48" if night else "#8aa05a", 0.9), 0, coll=c)
    box("ct_road", (30, 400, 0.42), (0, 60, -0.18), M("#3a3f58" if night else "#6a6f7a", 0.8), 0, coll=c)
    pastel = ["#f2a0a0", "#f2d28a", "#a0d2f2", "#b8e0a0", "#d0a8f0", "#f0b8d8"]
    for i in range(18):
        x = -120 + i * 14 + rnd.uniform(-2, 2)
        h = rnd.uniform(14, 36)
        col = "#1a2038" if night else pastel[i % len(pastel)]
        box(f"ct_b{i}", (11, 8, h), (x, 95, h / 2), M(col, 0.8), 0.05, coll=c)
        for k in range(rnd.randint(3, 7)):
            card(f"ct_w{i}_{k}", 1.6, 2.0, (x + rnd.uniform(-3.5, 3.5), 90.9, rnd.uniform(3, h - 3)),
                 emitm("#ffd890", 1.2 if night else 0.2), "-Y", coll=c)
    if night:
        sphere("ct_moon", 8, (-40, 160, 70), emitm("#dfe8ff", 6), coll=c)
        light("ct_key", "SUN", (0, 0, 50), 1.6, (0.55, 0.65, 1.0), 2.0, rot=(55, 0, 25), coll=c)
        light("ct_fill", "AREA", (0, -14, 12), 1600, (0.7, 0.75, 1.0), 14, coll=c, target=(0, 0, 4))
    else:
        sphere("ct_sun", 9, (50, 190, 90), emitm("#fff2a0", 8), coll=c)
        light("ct_key", "SUN", (0, 0, 50), 4.0, (1.0, 0.95, 0.85), 2.0, rot=(50, 0, 25), coll=c)
    if tower:
        box("ct_tw", (7, 7, 34), (0, 70, 17), M("#d8c8b0", 0.8), 0.1, coll=c)
        box("ct_twt", (8.4, 8.4, 3), (0, 70, 35.5), M("#8a4a3a", 0.8), 0.1, coll=c)
        clock((0, 66.2, 27), t_strike=None, s=2.4, coll=c, minute0=-8)
    return c


def crowd_nums(t0, t1, n=7, seed=2, spread=(-16, 16), y=(2, 14), zero_idx=None, tzero=None):
    rnd = random.Random(seed)
    kids = []
    for i in range(n):
        x = spread[0] + (spread[1] - spread[0]) * (i + rnd.uniform(0.1, 0.9)) / n
        yy = rnd.uniform(*y)
        K = townie(i + 3, t0, t1, rnd.choice(["happy", "neutral", "smile"]), loc=(x, yy, 0), rot=rnd.uniform(-25, 25)) if False else None
        K = story.townie(i + 3, t0, t1, rnd.choice(["happy", "neutral", "smile"]))
        K.pose(t0, loc=(x, yy, 0), rot=rnd.uniform(-20, 20))
        v = rnd.choice(["3,087", "7,411", "812", "5,230", "2,964", "6,115", "1,402", "8,826"])
        numtag(K, v, rnd.choice([GOLD, "#8fe39a", "#8ad2ff"]), 1.15, tag=str(i))
        kids.append(K)
    return kids


def library():
    world((0.1, 0.07, 0.05), 0.35)
    c = collection("LIB")
    box("lb_floor", (60, 40, 0.4), (0, 0, -0.2), wood("lb_fl", "#5a3a22", "#7a4f32", 2.0), 0, coll=c)
    box("lb_back", (60, 0.5, 18), (0, 9, 9), M("#3a2a22", 0.9), 0, coll=c)
    rnd = random.Random(4)
    cols = ["#c0392b", "#2a6fb8", "#2e8b57", "#d9a050", "#7a4ab8", "#e8e2d4"]
    for row in range(4):
        box(f"lb_sh{row}", (46, 1.4, 0.3), (0, 8.2, 3 + row * 3.6), M("#6a4a2a", 0.7), 0.05, coll=c)
        x = -22
        k = 0
        while x < 22:
            w = rnd.uniform(0.35, 0.8)
            h = rnd.uniform(2.0, 3.2)
            box(f"lb_bk{row}_{k}", (w, 1.0, h), (x + w / 2, 8.2, 3.15 + row * 3.6 + h / 2), M(rnd.choice(cols), 0.6), 0.03, coll=c)
            x += w + 0.05
            k += 1
    box("lb_desk", (9, 4, 0.4), (0, 1.5, 2.7), wood("lb_dk", "#8a5a32", "#a8743f", 2.0), 0.06, coll=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"lb_dl{sx}{sy}", (0.4, 0.4, 2.6), (sx * 4.0, 1.5 + sy * 1.6, 1.3), M("#5a3a22"), 0.02, coll=c)
    cyl("lb_lampb", 0.5, 0.2, (-3, 2.2, 3.0), M("#e2b23a", 0.3, metal=0.8), 14, coll=c)
    cyl("lb_lampp", 0.07, 1.6, (-3, 2.2, 3.8), M("#e2b23a", 0.3, metal=0.8), 8, coll=c)
    sphere("lb_lampg", 0.5, (-3, 2.2, 4.8), emitm("#ffd890", 5), coll=c)
    light("lb_lamp", "POINT", (-3, 1.0, 5.2), 4500, (1.0, 0.8, 0.5), 1.5, coll=c)
    light("lb_fill", "AREA", (0, -14, 10), 1800, (1.0, 0.85, 0.65), 14, coll=c, target=(0, 2, 3))
    box("lb_page", (1.7, 1.9, 0.05), (0.3, 0.6, 2.93), M("#efe6c8", 0.9), 0.01, coll=c, rot=(0, 0, 8))
    for k in range(6):
        box(f"lb_ln{k}", (1.2, 0.05, 0.02), (0.3, 0.1 + k * 0.28, 2.97), M("#6a5a3a"), 0.0, coll=c, rot=(0, 0, 8))
    return c


def hospital(t0, t1):
    world((0.9, 0.95, 1.0), 1.0)
    c = collection("HOSP")
    box("hs_floor", (50, 40, 0.4), (0, 0, -0.2), M("#d8dee6", 0.4), 0, coll=c)
    box("hs_back", (50, 0.5, 16), (0, 8, 8), M("#c8e0e8", 0.9), 0, coll=c)
    box("hs_bed", (4, 7, 1.0), (0, 2, 1.8), M("#f4f4f8", 0.5), 0.1, coll=c)
    box("hs_blank", (4.2, 4.5, 0.4), (0, 0.8, 2.6), M("#7ac0e8", 0.7), 0.1, coll=c)
    box("hs_mon", (2.6, 0.6, 2.0), (6, 6.5, 6.4), M("#2a2a32", 0.4), 0.08, coll=c)
    box("hs_scr", (2.2, 0.1, 1.5), (6, 6.15, 6.4), emitm("#2aff7a", 2.0), 0.02, coll=c)
    box("hs_stand", (0.3, 0.3, 4.4), (6, 6.5, 2.2), M("#8a8a92"), 0.04, coll=c)
    light("hs_key", "AREA", (0, -10, 14), 4000, (1.0, 1.0, 1.0), 14, coll=c, target=(0, 2, 3))
    return c


def gift(loc, t, coll=None, s=1.0):
    root = empty("gift", loc, coll=coll)
    box("gf_b", (1.6, 1.6, 1.4), (0, 0, 0.7), M("#e8423a", 0.4), 0.06, parent=root, coll=coll)
    box("gf_r1", (0.3, 1.7, 1.45), (0, 0, 0.72), M("#ffe14a", 0.3), 0.02, parent=root, coll=coll)
    box("gf_r2", (1.7, 0.3, 1.45), (0, 0, 0.72), M("#ffe14a", 0.3), 0.02, parent=root, coll=coll)
    sphere("gf_bow", 0.4, (0, 0, 1.6), M("#ffe14a", 0.3), (1.6, 0.8, 0.7), parent=root, coll=coll)
    pop(root, t, s, 0.3)
    return root


def poof_at(name, ch, t, s=1.2):
    W2.vanish(ch, t)
    p = ch.root.location
    W2.poof(name, (p[0], p[1] - 0.6, 3.6 * ch.root.scale[0]), t, s)


def NK(mood="dinner", **kw):
    return kitchen(mood, door_gap=False, chairs=False, **kw)


def tara2(t0, t1, expr="happy", loc=(0, 0, 0), rot=0, pale=False):
    T = chars.Char("Tara", skin="#bfd0b8" if pale else "#c99a72", shirt="#4fbf5a", pants="#2f3f6a", hair="messy",
                   hair_color="#1d1714", face="kid", vneck="#8fe39a")
    story._live(T, t0, t1, expr)
    T.pose(t0, loc=loc, rot=rot)
    return T


def num_burst(center, t, n=26, seed=1, spread=14.0):
    rnd = random.Random(seed)
    for k in range(n):
        body = rnd.choice(["1,204", "9,999", "3,500", "7,777", "5,120", "8,008", "2,468", "6,000"])
        o = text(f"nb{k}", body, tuple(center), rnd.uniform(0.7, 1.4), emitm(rnd.choice([GOLD, "#8fe39a", "#8ad2ff", "#ff9ad2"]), 3.0),
                 extrude=0.1)
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(t - 0.02))
        o.keyframe_insert("location", frame=F(t - 0.02))
        a = rnd.uniform(0, math.tau)
        d = rnd.uniform(0.4, 1.0) * spread
        o.scale = (1.0,) * 3
        o.keyframe_insert("scale", frame=F(t + 0.2))
        o.location = (center[0] + math.cos(a) * d, center[1] - rnd.uniform(0, 6), center[2] + math.sin(a) * d * 0.8)
        o.keyframe_insert("location", frame=F(t + 0.9))
        o.scale = (0.01,) * 3
        o.keyframe_insert("scale", frame=F(t + 1.5))


def foreheads(a, b, t, xa=-1.05, xb=1.05, y=-1.0, press=True):
    """Two characters face to face, heads tilted so foreheads touch (profile view from -Y)."""
    a.pose(t, loc=(xa, y, 0), rot=90, head=(0, 14, 0), torso=(0, 6, 0))
    b.pose(t, loc=(xb, y, 0), rot=-90, head=(0, 14, 0), torso=(0, 6, 0))


# ================================================================== 1 HOOK: the city of numbers
@S(1, 0, 3, "HOOK: bright city, everybody with a floating number")
def s01(t0, t1):
    city(t0, t1)
    crowd_nums(t0, t1, 9, 1, (-14, 14), (4, 16))
    cam = Cam()
    cam.push(t0, t1, (0, 10, 6), 26, 10, yaw=12, pitch=6, lens=24, yaw1=-10, fstop=6)
    cam.crash(w(1) + 0.1, 24, 34, 0.1)
    cam.handheld(1.4)
    sfx(t0, "whoosh", 0.9)
    sfx(t0 + 0.5, "pop", 0.6)
    sfx(t0 + 0.9, "sparkle", 0.5)


@S(2, 3, 8, "A kid and the number popping above his head")
def s02(t0, t1):
    city(t0, t1)
    K = story.townie(5, t0, t1, "happy")
    K.pose(t0, loc=(0, 3, 0))
    numtag(K, "3,087", GOLD, 1.4, t_on=w(6) - 0.1)
    cam = Cam()
    cam.push(t0, t1, (0, 3, 6.0), 14, 8, yaw=-14, pitch=4, lens=32, yaw1=10, fstop=3)
    cam.handheld(1.0)
    sfx(w(6) - 0.1, "pop", 0.9)
    sfx(w(7), "sparkle", 0.5)


@S(3, 8, 11, "Low angle: numbers floating above every head")
def s03(t0, t1):
    city(t0, t1)
    crowd_nums(t0, t1, 8, 7, (-12, 12), (3, 9))
    cam = Cam()
    cam.key(t0, (-10, -4, 0.8), (-2, 8, 9), lens=22, focus=14, fstop=4)
    cam.key(t1, (8, -4, 0.8), (2, 8, 9), lens=22, focus=14, fstop=4)
    cam.handheld(1.0)
    sfx(t0, "whoosh", 0.6)


@S(4, 11, 18, "It drops by one every midnight: kid's number, tower clock strikes")
def s04(t0, t1):
    city(t0, t1)
    K = story.townie(6, t0, t1, "happy")
    K.pose(t0, loc=(0, 14, 0))
    numseq(K, [(t0, "9"), (w(17) + 0.1, "8")], GOLD, 1.5, t0=t0)
    cam = Cam()
    cam.key(t0, (3, 2, 3.5), (0, 14, 6.5), lens=26, focus=13, fstop=4)
    cam.key(w(16), (1, 2, 3.5), (0, 14, 7.5), lens=26, focus=13, fstop=4)
    cam.key(t1, (0, 2, 6), (0, 66, 27), lens=24, focus=60, fstop=6)
    cam.handheld(1.0)
    flash("tw", w(17) + 0.1, 0.4, (1, 0.95, 0.7), at=(0, 40, 20), e=90000)
    sfx(w(17) + 0.05, "ding", 0.9)
    sfx(w(17) + 0.1, "click", 0.8)
    sfx(w(15), "rise", 0.6)


@S(5, 18, 23, "Nobody can see their own: hero looks up, can't see")
def s05(t0, t1):
    city(t0, t1)
    K = hero(t0, t1, "lookup", loc=(0, 4, 0))
    numtag(K, "?", RED, 1.6)
    K.act(t0 + 0.3, "shrug", expr="confused")
    cam = Cam()
    cam.push(t0, t1, (0, 4, 4.8), 12, 6.5, yaw=10, pitch=-6, lens=30, yaw1=-8, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "chat", 0.4)


@S(6, 23, 27, "At zero, you vanish")
def s06(t0, t1):
    city(t0, t1)
    K = story.townie(7, t0, t1, "worried")
    K.pose(t0, loc=(0, 5, 0))
    numseq(K, [(t0, "1"), (w(24) - 0.15, "0")], RED, 1.6, t0=t0)
    tv = w(26) + 0.05
    poof_at("vz", K, tv, 1.3)
    cam = Cam()
    cam.push(t0, t1, (0, 5, 5.5), 15, 7, yaw=-10, pitch=2, lens=30, yaw1=8, fstop=3)
    cam.crash(tv, 30, 22, 0.1)
    cam.handheld(1.0)
    sfx(w(24) - 0.15, "click", 0.8)
    sfx(tv, "poof", 1.0)


@S(7, 27, 34, "Nobody ever says your name again: alone, empty street")
def s07(t0, t1):
    city(t0, t1, night=True)
    K = hero(t0, t1, "sad" if False else "worried", loc=(0, 6, 0))
    K.act(t0 + 0.3, "slump", expr="worried")
    numtag(K, "?", RED, 1.6)
    cam = Cam()
    cam.orbit(t0, t1, (0, 6, 4.6), 16, -30, 25, pitch=4, lens=30, steps=4, fstop=3)
    cam.handheld(0.8)
    sfx(t0, "wind", 0.7)
    sfx(t0 + 1.5, "crickets", 0.5)


@S(8, 34, 37, "Tarasik has 9,412")
def s08(t0, t1):
    city(t0, t1)
    T = tara2(t0, t1, "grin", loc=(0, 4, 0))
    numtag(T, "9,412", GOLD, 1.5, t_on=w(36) - 0.05)
    T.act(t0 + 0.2, "cheer", expr="grin")
    cam = Cam()
    cam.push(t0, t1, (0, 4, 6.0), 13, 8, yaw=14, pitch=3, lens=30, yaw1=-8, fstop=3)
    cam.crash(w(36), 30, 24, 0.1)
    cam.handheld(1.0)
    sfx(w(36) - 0.05, "pop", 0.9)
    sfx(w(36), "coin", 0.6)


@S(9, 37, 41, "...and brags about it")
def s09(t0, t1):
    city(t0, t1)
    T = tara2(t0, t1, "smug", loc=(0, 4, 0))
    numtag(T, "9,412", GOLD, 1.5)
    T.act(t0 + 0.2, "cross", expr="smug")
    lips(T, t0, t1)
    cam = Cam()
    cam.orbit(t0, t1, (0, 4, 4.8), 11, 24, -18, pitch=3, lens=34, steps=4, fstop=2.8)
    cam.handheld(1.0)
    sfx(t0 + 0.6, "rimshot", 0.4)


@S(10, 41, 46, "My mom's number is 11 (red)")
def s10(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "worried", loc=(0, -1, 0))
    numtag(Mo, "11", RED, 1.6, t_on=w(45) - 0.05)
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 12, 6.5, yaw=10, pitch=2, lens=34, yaw1=-8, fstop=2.8)
    cam.crash(w(45), 34, 26, 0.1)
    cam.handheld(1.0)
    sfx(w(45) - 0.05, "pop", 0.9)
    sfx(w(45), "rise", 0.7)


@S(11, 46, 51, '"It\'s a mistake," she says')
def s11(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "smile", loc=(0, -1, 0))
    numtag(Mo, "11", RED, 1.6)
    Mo.act(t0 + 0.2, "shrug", expr="smile")
    lips(Mo, t0, t1)
    camL(t0, t1, (0, -1, 0), 8, 5.4, yaw=-14, yaw1=10, lens=40)
    sfx(t0 + 0.3, "whoosh", 0.3)


@S(12, 51, 57, "Every morning I watch it fall: hero staring up at mom's number")
def s12(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "smile", loc=(3, -1, 0), rot=-10)
    numtag(Mo, "11", RED, 1.6)
    K = hero(t0, t1, "worried", loc=(-3, -1, 0), rot=10)
    look_at(K, t0 + 0.2, (3, -1, 7.7))
    cam = Cam()
    cam.key(t0, (-4, -10, 4), (1.2, -1, 5.4), lens=26, focus=10, fstop=3.5)
    cam.key(t1, (0, -8, 5), (1.5, -1, 6.2), lens=28, focus=8, fstop=3.5)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "click", 0.5)
    sfx(t0 + 2.0, "wind", 0.4)


def tagshot(t0, t1, val, yaw, crash=True):
    NK("dawn")
    Mo = mom(t0, t1, "smile", loc=(0, -1, 0))
    numtag(Mo, val, RED, 1.9, t_on=t0 + 0.02)
    cam = Cam()
    cam.push(t0, t1, (0, -1, 7.7), 9, 6, yaw=yaw, pitch=-8, lens=36, yaw1=-yaw * 0.5, fstop=2.8)
    if crash:
        cam.crash(t0 + 0.02, 36, 28, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.02, "click", 0.9)
    sfx(t0 + 0.04, "ding", 0.6)


@S(13, 57, 58, "10")
def s13(t0, t1):
    tagshot(t0, t1, "10", 12)


@S(14, 58, 59, "9")
def s14(t0, t1):
    tagshot(t0, t1, "9", -14)


@S(15, 59, 60, "8 (hero's worried reaction)")
def s15(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "worried", loc=(0, -1, 0))
    K.act(t0 + 0.05, "hands_face", expr="worried")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 7, 4.4, yaw=-10, pitch=2, lens=45, yaw1=8, fstop=2.2)
    cam.crash(t0 + 0.02, 45, 62, 0.1)
    cam.handheld(1.5)
    sfx(t0 + 0.02, "boom", 0.7)
    sfx(t0 + 0.04, "heartbeat", 0.7)


# ================================================================== 2 the library
@S(16, 60, 63, "In the library")
def s16(t0, t1):
    library()
    K = hero(t0, t1, "neutral", loc=(-6, -4, 0))
    K.walk(t0, t1, (-8, -6, 0), (-2, -2.5, 0), rate=2.2)
    cam = Cam()
    cam.key(t0, (-5, -15, 7), (0, 2, 5), lens=24, focus=17, fstop=4)
    cam.key(t1, (3, -12, 6), (0, 2, 4.6), lens=24, focus=14, fstop=4)
    cam.handheld(1.0)
    sfx(t0, "footsteps", 0.6)
    sfx(t0 + 0.2, "paper", 0.4)


@S(17, 63, 68, "I found a torn page")
def s17(t0, t1):
    library()
    K = hero(t0, t1, "gasp", loc=(0, -2.5, 0))
    K.act(t0 + 0.5, "point", expr="gasp")
    look_at(K, t0 + 0.2, (0.3, 0.6, 3))
    cam = Cam()
    cam.key(t0, (1.5, -9, 5.8), (0.2, 0.6, 3.0), lens=45, focus=9, fstop=2.2)
    cam.key(t1, (0.4, -4.5, 6.5), (0.3, 0.6, 2.95), lens=50, focus=5, fstop=2.2)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "paper", 0.8)
    sfx(t0 + 1.0, "ding", 0.5)


@S(18, 68, 73, "A number can be given (text over the page)")
def s18(t0, t1):
    library()
    pop_text("pg1", "A NUMBER", (0.3, -1.5, 6.4), t0 + 0.2, 0.6, "#ffe14a")
    pop_text("pg2", "CAN BE GIVEN", (0.3, -1.5, 5.4), t0 + 0.6, 0.6, "#ffffff")
    cam = Cam()
    cam.key(t0, (-1.5, -9, 5.6), (0.3, 0.6, 4.4), lens=36, focus=9, fstop=3)
    cam.key(t1, (0.8, -7.5, 5.4), (0.3, 0.6, 4.4), lens=40, focus=8, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "pop", 0.8)
    sfx(t0 + 0.6, "boom", 0.6)
    sfx(t0 + 0.6, "sparkle", 0.6)


@S(19, 73, 80, "Press your forehead to theirs: demo, profile view")
def s19(t0, t1):
    library()
    A = hero(t0, t1, "closed" if False else "neutral")
    B = mom(t0, t1, "smile", name="Mom")
    foreheads(A, B, t0)
    A.face(t0 + 0.2, eyes="closed", mouth="flat")
    B.face(t0 + 0.2, eyes="closed", mouth="smile")
    cam = Cam()
    cam.push(t0, t1, (0, -1, 4.8), 12, 6.5, yaw=-6, pitch=2, lens=34, yaw1=6, fstop=3)
    cam.handheld(0.8)
    sfx(t0 + 0.6, "whoosh", 0.4)
    sfx(t0 + 1.4, "sparkle", 0.5)


@S(20, 80, 82, "take mine.")
def s20(t0, t1):
    library()
    pop_text("tm", "TAKE MINE", (0, -1.5, 6.0), t0 + 0.1, 0.95, "#ff9ad2")
    sparkles("tms", (0, -2, 5), t0 + 0.1, 1.6, 18, 4, "#ffd0f0")
    cam = Cam()
    cam.push(t0, t1, (0, -1.5, 5.6), 12, 7, yaw=0, pitch=0, lens=32, fstop=3)
    cam.crash(t0 + 0.1, 32, 24, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.1, "boom", 0.8)
    sfx(t0 + 0.12, "sparkle", 0.8)


# ================================================================== 3 the night
@S(21, 82, 86, "That night: moon over the kitchen")
def s21(t0, t1):
    NK("dinner")
    Mo = mom(t0, t1, "sleepy", loc=(0, -1, 0))
    Mo.act(t0 + 0.2, "slump", expr="sleepy")
    cam = Cam()
    cam.key(t0, (-8, -12, 6), (-6, 8, 8), lens=24, focus=22, fstop=4)
    cam.key(t1, (-1, -9, 4.6), (0, -1, 4.2), lens=30, focus=9, fstop=4)
    cam.handheld(0.9)
    sfx(t0, "crickets", 0.6)
    sfx(t0 + 0.2, "wind", 0.4)


@S(22, 86, 89, "Two days left: tag 2")
def s22(t0, t1):
    NK("dinner")
    Mo = mom(t0, t1, "sleepy", loc=(0, -1, 0))
    numseq(Mo, [(t0, "3"), (t0 + 0.25, "2")], RED, 1.9, t0=t0)
    cam = Cam()
    cam.push(t0, t1, (0, -1, 7.7), 9, 5.5, yaw=10, pitch=-8, lens=36, yaw1=-10, fstop=2.8)
    cam.crash(t0 + 0.3, 36, 28, 0.1)
    cam.handheld(1.3)
    sfx(t0 + 0.25, "click", 0.9)
    sfx(t0 + 0.3, "boom", 0.6)
    sfx(t0 + 0.4, "heartbeat", 0.8)


@S(23, 89, 95, "I pressed my forehead to hers")
def s23(t0, t1):
    NK("dinner")
    A = hero(t0, t1, "neutral")
    B = mom(t0, t1, "smile")
    foreheads(A, B, t0)
    A.face(t0 + 0.8, eyes="closed", mouth="flat")
    B.face(t0 + 0.5, eyes="closed", mouth="smile")
    cam = Cam()
    cam.orbit(t0, t1, (0, -1, 4.8), 13, -22, 22, pitch=2, lens=34, steps=4, fstop=3)
    cam.handheld(0.8)
    sfx(t0 + 0.5, "whoosh", 0.4)
    sfx(t0 + 1.2, "heartbeat", 0.5)


@S(24, 95, 99, "...and whispered the words: glow")
def s24(t0, t1):
    NK("dinner")
    A = hero(t0, t1, "neutral")
    B = mom(t0, t1, "smile")
    foreheads(A, B, t0)
    A.face(t0, eyes="closed", mouth="flat")
    lips(A, t0, t1)
    sparkles("wh", (0, -1.6, 5.4), t0 + 0.2, 0.8, 16, 2, "#ffe9a0")
    cam = Cam()
    cam.push(t0, t1, (0, -1.2, 5.2), 7, 4.0, yaw=-8, pitch=2, lens=50, yaw1=4, fstop=2.0)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "sparkle", 0.7)
    sfx(t0 + 0.4, "wind", 0.4)


@S(25, 99, 102, "In the morning: dawn kitchen")
def s25(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "sleepy", loc=(0, -1, 0))
    cam = Cam()
    cam.key(t0, (-5, -9, 5), (-6, 8, 8), lens=24, focus=17, fstop=4)
    cam.key(t1, (-1, -8, 4.6), (0, -1, 4.4), lens=30, focus=8, fstop=4)
    cam.handheld(0.9)
    sfx(t0, "sparkle", 0.4)
    sfx(t0 + 0.2, "whoosh", 0.4)


@S(26, 102, 107, "Above her head floated 400: tilt up to gold number")
def s26(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "gasp", loc=(0, -1, 0))
    numtag(Mo, "400", GOLD, 2.0, t_on=w(106) - 0.05)
    cam = Cam()
    cam.key(t0, (1, -8, 2.8), (0, -1, 4.8), lens=28, focus=8, fstop=3)
    cam.key(t1, (0.5, -8, 3.4), (0, -1, 8.4), lens=26, focus=8, fstop=3)
    cam.crash(w(106), 26, 20, 0.1)
    cam.handheld(1.0)
    sfx(w(106) - 0.05, "pop", 0.9)
    sfx(w(106), "coin", 0.8)
    sfx(w(104), "rise", 0.7)


@S(27, 107, 112, "Mom woke up and screamed")
def s27(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "scream", loc=(0, -1, 0))
    numtag(Mo, "400", GOLD, 1.8)
    Mo.act(t0 + 0.7, "recoil", expr="scream")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 8, 4.2, yaw=0, pitch=2, lens=46, fstop=2.2)
    cam.crash(w(111), 46, 66, 0.1)
    cam.handheld(1.8)
    sfx(w(111), "gasp", 0.8)
    sfx(w(111), "boom", 0.7)


@S(28, 112, 116, '"What did you do?"')
def s28(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "furious", loc=(0, -1, 0))
    lips(Mo, t0, t1, "shout")
    Mo.act(t0 + 0.1, "fists", expr="furious")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 7, 3.6, yaw=-12, pitch=2, lens=50, yaw1=8, fstop=2.0)
    cam.handheld(2.0)
    sfx(t0 + 0.1, "stomp", 0.6)


@S(29, 116, 123, "Tarasik stared at me and went pale")
def s29(t0, t1):
    NK("dawn")
    T = tara2(t0, t1, "terror", loc=(0, -1, 0), pale=True)
    T.act(t0 + 0.4, "recoil", expr="terror")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 10, 4.6, yaw=12, pitch=2, lens=40, yaw1=-8, fstop=2.4)
    cam.crash(w(122) - 0.4, 40, 56, 0.12)
    cam.handheld(1.2)
    sfx(t0 + 0.3, "gasp", 0.7)
    sfx(t0 + 2.0, "rise", 0.6)


@S(30, 123, 127, '"Your number is one."')
def s30(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "gasp", loc=(0, -1, 0))
    numtag(K, "1", RED, 2.2, t_on=w(126) - 0.05)
    T = tara2(t0, t1, "terror", loc=(-5, -2, 0), rot=-25, pale=True)
    T.act(t0 + 0.1, "point_l", expr="terror")
    cam = Cam()
    cam.key(t0, (-1, -11, 4.6), (-1, -1, 5.2), lens=26, focus=10, fstop=3.5)
    cam.key(t1, (0, -8, 4.0), (0, -1, 7.2), lens=28, focus=7, fstop=3.5)
    cam.crash(w(126), 28, 20, 0.1)
    cam.handheld(1.2)
    sfx(w(126) - 0.05, "boom", 0.9)
    sfx(w(126), "heartbeat", 0.9)


@S(31, 127, 131, "Mom grabbed my face")
def s31(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "shock", loc=(-1.4, -1, 0), rot=90)
    Mo = mom(t0, t1, "furious", loc=(1.4, -1, 0), rot=-90)
    Mo.pose(t0 + 0.2, armL=(100, 10), armR=(100, 10))
    K.pose(t0, head=(0, 6, 0))
    cam = Cam()
    cam.push(t0, t1, (0, -1, 4.8), 11, 6, yaw=-24, pitch=4, lens=34, yaw1=-8, fstop=2.8)
    cam.handheld(1.8)
    sfx(t0 + 0.2, "thud", 0.7)
    sfx(t0 + 0.2, "whoosh", 0.5)


@S(32, 131, 136, '"Take it back, right now!"')
def s32(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "furious", loc=(0, -1, 0))
    lips(Mo, t0, t1, "shout")
    Mo.act(t0 + 0.2, "point", expr="furious")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 6.5, 3.2, yaw=10, pitch=2, lens=55, yaw1=-10, fstop=1.8)
    cam.crash(w(135) - 0.2, 55, 80, 0.1)
    cam.handheld(2.4)
    sfx(t0 + 0.1, "stomp", 0.8)
    sfx(w(135) - 0.2, "boom", 0.7)


@S(33, 136, 140, '"I can\'t," I said')
def s33(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "cry", loc=(0, -1, 0))
    lips(K, t0, t1)
    K.act(t0 + 0.3, "slump", expr="cry")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 8, 4.6, yaw=-10, pitch=3, lens=42, yaw1=6, fstop=2.2)
    cam.handheld(0.9)
    sfx(t0 + 0.2, "aww", 0.5)


@S(34, 140, 145, '"A gift can\'t be returned."')
def s34(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "cry", loc=(0, -1, 0))
    K.act(t0 + 0.2, "hold", expr="cry")
    gift((0, -3.5, 4.4), t0 + 0.4, s=0.9)
    sparkles("gfs", (0, -3.5, 5.5), t0 + 0.4, 2.0, 12, 1)
    cam = Cam()
    cam.push(t0, t1, (0, -2, 5), 12, 7, yaw=14, pitch=3, lens=32, yaw1=-8, fstop=2.8)
    cam.handheld(1.0)
    sfx(t0 + 0.4, "pop", 0.8)
    sfx(t0 + 0.45, "sparkle", 0.7)


@S(35, 145, 148, "Then she stopped.")
def s35(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "neutral", loc=(0, -1, 0))
    Mo.face(t0, eyes="wide", mouth="o")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 7, 4.4, yaw=0, pitch=1, lens=48, fstop=2.0)
    cam.handheld(0.5)
    sfx(t0, "heartbeat", 0.9)


@S(36, 148, 156, '"Do you know why mine was 11?" she asked')
def s36(t0, t1):
    NK("dawn")
    Mo = mom(t0, t1, "worried", loc=(0, -1, 0))
    numtag(Mo, "400", GOLD, 1.6)
    lips(Mo, t0, t1)
    Mo.act(t0 + 0.3, "lean", expr="worried")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 9, 5.0, yaw=-14, pitch=2, lens=42, yaw1=10, fstop=2.2)
    cam.handheld(0.9)
    sfx(t0 + 0.3, "whoosh", 0.3)


@S(37, 156, 161, "I shook my head")
def s37(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "worried", loc=(0, -1, 0))
    K.shake(t0 + 0.8, 4, 20, 7)
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 7.5, 4.6, yaw=8, pitch=2, lens=44, yaw1=-8, fstop=2.2)
    cam.handheld(1.0)
    sfx(t0 + 0.8, "whoosh", 0.4)


@S(38, 161, 165, "You were born sick: hospital, tiny hero in bed")
def s38(t0, t1):
    hospital(t0, t1)
    K = hero(t0, t1, "sleepy", loc=(0, 2, 2.0))
    K.root.scale = (0.5,) * 3
    K.pose(t0, loc=(0, 2.2, 2.3), rot=0, legL=(85, 0), legR=(85, 0))
    numtag(K, "3", RED, 2.4, z=9.5)
    cam = Cam()
    cam.push(t0, t1, (0, 2.2, 5.0), 14, 8, yaw=-14, pitch=6, lens=34, yaw1=8, fstop=3)
    cam.handheld(0.9)
    sfx(t0, "ding", 0.5)
    sfx(t0 + 0.3, "heartbeat", 0.7)


@S(39, 165, 171, "The doctors gave you three days: monitor beeping")
def s39(t0, t1):
    hospital(t0, t1)
    K = hero(t0, t1, "sleepy", loc=(0, 2.2, 2.3))
    K.root.scale = (0.5,) * 3
    K.pose(t0, loc=(0, 2.2, 2.3), legL=(85, 0), legR=(85, 0))
    numtag(K, "3", RED, 2.4, z=9.5)
    cam = Cam()
    cam.key(t0, (5, -4, 5.5), (6, 6.4, 6.4), lens=40, focus=11, fstop=2.8)
    cam.key(t1, (2, -6, 4.8), (0, 2.2, 6.0), lens=34, focus=9, fstop=2.8)
    cam.handheld(1.0)
    for k in range(5):
        sfx(t0 + 0.2 + k * 0.9, "click", 0.5)
    sfx(t0, "heartbeat", 0.8)


@S(40, 171, 175, "So every night since: mom at the bedside, forehead to forehead")
def s40(t0, t1):
    hospital(t0, t1)
    K = hero(t0, t1, "sleepy", loc=(0.3, 2.4, 2.3))
    K.root.scale = (0.5,) * 3
    K.pose(t0, loc=(0.3, 2.4, 2.3), legL=(85, 0), legR=(85, 0))
    Mo = mom(t0, t1, "smile", loc=(-2.2, 2.0, 0), rot=90)
    Mo.pose(t0, head=(0, 22, 0), torso=(0, 12, 0))
    Mo.face(t0, eyes="closed", mouth="smile")
    cam = Cam()
    cam.orbit(t0, t1, (-0.5, 2.2, 5.0), 11, -32, 18, pitch=4, lens=36, steps=3, fstop=3)
    cam.handheld(0.8)
    sfx(t0, "wind", 0.4)
    sfx(t0 + 0.4, "sparkle", 0.4)


@S(41, 175, 181, "I whispered those words to you: close on mom")
def s41(t0, t1):
    NK("dinner")
    Mo = mom(t0, t1, "smile", loc=(0, -1, 0))
    Mo.face(t0, eyes="closed", mouth="smile")
    lips(Mo, t0, t1)
    sparkles("wm", (0, -2, 5.6), t0 + 0.3, 2.0, 18, 8, "#ffe9a0")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 7, 3.8, yaw=12, pitch=2, lens=52, yaw1=-6, fstop=1.9)
    cam.handheld(0.7)
    sfx(t0 + 0.3, "sparkle", 0.6)
    sfx(t0, "wind", 0.3)


@S(42, 181, 186, "Your number was never yours")
def s42(t0, t1):
    NK("dawn")
    K = hero(t0, t1, "shock", loc=(0, -1, 0))
    numtag(K, "1", RED, 2.0)
    K.act(t0 + 0.5, "hands_head", expr="terror")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 9, 4.0, yaw=-6, pitch=2, lens=44, yaw1=6, fstop=2.2)
    cam.crash(w(184), 44, 64, 0.12)
    cam.handheld(1.6)
    sfx(w(184), "boom", 0.8)
    sfx(w(184), "gasp", 0.7)


# ================================================================== 4 midnight
@S(43, 186, 191, "Midnight was an hour away: clock ticking")
def s43(t0, t1):
    NK("dinner")
    clock((0, 7.0, 7.0), t_strike=None, s=2.6, minute0=-35)
    cam = Cam()
    cam.push(t0, t1, (0, 7.0, 7.0), 14, 7, yaw=-8, pitch=0, lens=34, yaw1=8, fstop=3)
    cam.handheld(1.0)
    for k in range(5):
        sfx(t0 + 0.2 + k * 0.9, "click", 0.6)
    sfx(t0, "rise", 0.5)


@S(44, 191, 197, "Mom pressed her forehead to mine")
def s44(t0, t1):
    NK("dinner")
    A = hero(t0, t1, "sad" if False else "worried")
    B = mom(t0, t1, "smile")
    foreheads(A, B, t0, -2.6, 2.6)
    B.pose(t0 + 1.4, loc=(1.4, -1, 0))
    A.pose(t0 + 1.4, loc=(-1.4, -1, 0))
    A.face(t0 + 1.2, eyes="closed", mouth="flat")
    B.face(t0 + 1.2, eyes="closed", mouth="smile")
    cam = Cam()
    cam.push(t0, t1, (0, -1, 4.8), 13, 7, yaw=-14, pitch=2, lens=34, yaw1=0, fstop=3)
    cam.handheld(0.8)
    sfx(t0 + 1.4, "thud", 0.4)
    sfx(t0, "wind", 0.4)


@S(45, 197, 200, "One last time: tears")
def s45(t0, t1):
    NK("dinner")
    A = hero(t0, t1, "cry")
    B = mom(t0, t1, "smile")
    foreheads(A, B, t0)
    A.face(t0, eyes="closed", mouth="ah")
    B.face(t0, eyes="closed", mouth="smile")
    cam = Cam()
    cam.orbit(t0, t1, (0, -1, 4.6), 7, -20, 12, pitch=2, lens=48, steps=3, fstop=2.0)
    cam.handheld(0.7)
    sfx(t0, "aww", 0.6)
    sfx(t0 + 0.3, "heartbeat", 0.7)


@S(46, 200, 204, '"Take mine," she said')
def s46(t0, t1):
    NK("dinner")
    Mo = mom(t0, t1, "smile", loc=(0, -1, 0))
    lips(Mo, t0, t1)
    Mo.face(t0, eyes="happy", mouth="smile")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 6.5, 3.4, yaw=0, pitch=2, lens=56, fstop=1.8)
    cam.handheld(0.6)
    sfx(t0 + 0.3, "rise", 0.7)


@S(47, 204, 206, "Tarasik gasped")
def s47(t0, t1):
    NK("dinner")
    T = tara2(t0, t1, "gasp", loc=(0, -1, 0), pale=True)
    T.act(t0 + 0.2, "recoil", expr="gasp")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 8, 4.4, yaw=10, pitch=2, lens=44, yaw1=-8, fstop=2.2)
    cam.crash(t0 + 0.2, 44, 62, 0.1)
    cam.handheld(1.4)
    sfx(t0 + 0.2, "gasp", 0.9)


@S(48, 206, 214, "The number exploded into thousands")
def s48(t0, t1):
    NK("dinner")
    K = hero(t0, t1, "gasp", loc=(0, -1, 0))
    tb = w(211)
    numtag(K, "1", RED, 2.0, t_off=tb)
    numtag(K, "4,512", GOLD, 2.2, t_on=tb, tag="big")
    num_burst((0, -1, 8.4), tb, 26, 3, 12)
    K.act(tb, "cheer", expr="gasp")
    cam = Cam()
    cam.key(t0, (0, -9, 3.6), (0, -1, 5.0), lens=28, focus=8, fstop=3)
    cam.key(tb, (0, -8, 4.0), (0, -1, 7.5), lens=26, focus=8, fstop=3)
    cam.key(t1, (0, -10, 5.5), (0, -1, 8.4), lens=22, focus=9, fstop=4)
    cam.crash(tb, 26, 18, 0.12)
    cam.handheld(1.4)
    flash("ex", tb, 0.5, (1, 0.9, 0.5), at=(0, -4, 8), e=70000)
    sfx(tb, "boom", 1.0)
    sfx(tb, "confetti", 0.8)
    sfx(tb + 0.1, "sparkle", 0.9)
    sfx(tb - 0.3, "rise", 0.8)


@S(49, 214, 218, "Above hers was zero")
def s49(t0, t1):
    NK("dinner")
    Mo = mom(t0, t1, "smile", loc=(0, -1, 0))
    numseq(Mo, [(t0, "400"), (w(217) - 0.1, "0")], "#dfe6f0", 2.0, t0=t0)
    cam = Cam()
    cam.key(t0, (0, -8, 3), (0, -1, 5), lens=28, focus=8, fstop=3)
    cam.key(t1, (0, -8, 3.6), (0, -1, 8.2), lens=28, focus=8, fstop=3)
    cam.handheld(0.9)
    sfx(w(217) - 0.1, "click", 0.9)
    sfx(w(217), "heartbeat", 0.8)


@S(50, 218, 224, "She smiled and kissed my hair")
def s50(t0, t1):
    NK("dinner")
    K = hero(t0, t1, "relief", loc=(-1.0, -1, 0), rot=15)
    Mo = mom(t0, t1, "smile", loc=(1.2, -1, 0), rot=-60)
    numseq(Mo, [(t0, "0")], "#dfe6f0", 1.6, t0=t0)
    Mo.pose(t0 + 1.0, head=(0, 25, 0), torso=(0, 10, 0))
    Mo.face(t0 + 1.0, eyes="closed", mouth="smile")
    sparkles("kiss", (-0.3, -1.6, 6.6), t0 + 1.3, 2.0, 14, 5, "#ffd0f0")
    cam = Cam()
    cam.push(t0, t1, (0, -1, 5), 11, 6.5, yaw=-26, pitch=4, lens=34, yaw1=-8, fstop=2.8)
    cam.handheld(0.8)
    sfx(t0 + 1.3, "sparkle", 0.7)
    sfx(t0 + 1.3, "aww", 0.6)


@S(51, 224, 229, "Then the clock struck 12")
def s51(t0, t1):
    NK("dinner")
    clock((0, 7.0, 7.5), t_strike=w(228) - 0.3, s=2.8, minute0=-25)
    cam = Cam()
    cam.push(t0, t1, (0, 7.0, 7.5), 15, 7, yaw=0, pitch=0, lens=34, fstop=3)
    cam.crash(w(228) - 0.3, 34, 22, 0.12)
    cam.handheld(1.6)
    flash("ck", w(228) - 0.3, 0.6, (1, 0.9, 0.7), at=(0, 2, 8), e=25000)
    for k in range(6):
        sfx(w(228) - 0.3 + k * 0.28, "ding", 0.9)
    sfx(w(228) - 0.3, "boom", 1.0)
    sfx(t0, "click", 0.6)


@S(52, 229, 234, "and the kitchen was empty")
def s52(t0, t1):
    NK("dinner")
    K = hero(t0, t1, "cry", loc=(0, -2, 0))
    K.pose(t0, loc=(0, -2, 0), torso=(0, 14, 0), head=(0, 22, 0))
    Mo = mom(t0, t1, "smile", loc=(2.0, -2, 0), rot=-60)
    poof_at("mp", Mo, t0 + 0.2, 1.4)
    cam = Cam()
    cam.key(t0, (4, -9, 4.5), (1, -2, 5), lens=30, focus=9, fstop=3)
    cam.key(t1, (-2, -13, 7), (0, -1, 4), lens=22, focus=14, fstop=4)
    cam.handheld(0.9)
    sfx(t0 + 0.2, "poof", 1.0)
    sfx(t0 + 0.5, "aww", 0.6)
    sfx(t0 + 1.5, "wind", 0.5)


# ================================================================== 5 the name
@S(53, 234, 241, "Everyone says I must forget her name")
def s53(t0, t1):
    city(t0, t1, night=True)
    K = hero(t0, t1, "worried", loc=(0, 5, 0))
    K.act(t0 + 0.3, "slump", expr="worried")
    numtag(K, "4,512", GOLD, 1.6)
    ks = crowd_nums(t0, t1, 7, 11, (-14, 14), (8, 14))
    for k in ks:
        k.act(t0 + 0.5, "point", expr="neutral")
        look_at(k, t0 + 0.3, (0, 5, 4.6))
    cam = Cam()
    cam.orbit(t0, t1, (0, 5, 4.6), 16, -30, 30, pitch=5, lens=30, steps=4, fstop=3)
    cam.handheld(0.9)
    sfx(t0, "crowd", 0.5)
    sfx(t0 + 0.5, "chat", 0.5)


@S(54, 241, 248, "Every midnight, I whisper it anyway: at the window")
def s54(t0, t1):
    NK("dinner")
    K = hero(t0, t1, "sleepy", loc=(-6, 4.5, 0), rot=180)
    lips(K, t0, t1)
    cam = Cam()
    cam.key(t0, (-1, -6, 5.5), (-6, 7.8, 6.5), lens=30, focus=14, fstop=3)
    cam.key(t1, (-3, -2, 6.0), (-6, 7.8, 6.2), lens=30, focus=9, fstop=3)
    cam.handheld(0.8)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.4, "crickets", 0.5)


@S(55, 248, 249, '"Marina."')
def s55(t0, t1):
    NK("dinner")
    K = hero(t0, t1, "sad" if False else "worried", loc=(0, -1, 0))
    lips(K, t0, t1)
    K.face(t0, eyes="closed", mouth="talk")
    sparkles("mar", (0, -2, 5.5), t0 + 0.1, 0.8, 12, 9, "#ffd0f0")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 6.5, 3.6, yaw=0, pitch=2, lens=56, fstop=1.8)
    cam.handheld(0.6)
    sfx(t0, "sparkle", 0.8)
    sfx(t0, "aww", 0.5)


@S(56, 249, None, "The number above my head has never dropped: tilt up, frozen")
def s56(t0, t1):
    NK("dinner")
    K = hero(t0, t1, "worried", loc=(0, -1, 0))
    numtag(K, "4,512", GOLD, 1.7, z=7.9)
    clock((8, 7.0, 8.0), t_strike=w(255), s=1.8, minute0=-12)
    cam = Cam()
    cam.key(t0, (0, -8, 3.4), (0, -1, 5.0), lens=28, focus=8, fstop=3)
    cam.key(t1, (0, -9, 4.2), (0, -1, 8.2), lens=24, focus=9, fstop=3)
    cam.crash(t1 - 1.0, 24, 18, 0.2)
    cam.handheld(0.8)
    flash("fin", w(255), 0.5, (1, 0.9, 0.7), at=(6, 2, 9), e=40000)
    sfx(w(255), "ding", 0.8)
    sfx(w(255), "boom", 0.7)
    sfx(w(255) + 0.5, "heartbeat", 0.8)
