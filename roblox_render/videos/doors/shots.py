"""doors / "The green door": hundreds of doors appear every night; Mom came back wrong.
Horror-lite Roblox short. Shots keyed to script word indices (audio/words.json)."""
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
    rt, pv = door("k_exit", (0, -14.0, 0), GREEN, rot=180, s=1.0, glow=2.5, coll=c)
    if door_t is not None:
        swing(pv, door_t[0], -105 if False else 105, 0.4)
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


# ================================================================== 1  HOOK: doors appear every night
@S(1, 0, 3, "HOOK: night street, doors slam into existence")
def s01(t0, t1):
    c, ds = street(t0, t1, n=45, seed=1)
    K = hero(t0, t1, "gasp", loc=(0, 12, 0))
    K.act(t0 + 0.5, "shock")
    cam = Cam()
    cam.push(t0, t1, (0, 12, 4.6), 24, 10, yaw=14, pitch=2, lens=22, yaw1=-8, fstop=5)
    cam.crash(w(1) + 0.1, 22, 34, 0.1)
    cam.handheld(1.4)
    for k in range(4):
        sfx(t0 + 0.12 + k * 0.28, "pop", 0.7)
    sfx(t0, "whoosh", 0.9)
    sfx(t0 + 0.5, "rise", 0.6)


@S(2, 3, 7, "High crane: hundreds of doors pop up across the city")
def s02(t0, t1):
    c, ds = street(t0, t1, n=80, seed=2, clear=0)
    cam = Cam()
    cam.key(t0, (-24, -8, 44), (0, 40, 2), lens=24, focus=50, fstop=8)
    cam.key(t1, (18, 6, 30), (0, 46, 2), lens=24, focus=50, fstop=8)
    cam.handheld(0.9)
    for k in range(6):
        sfx(t0 + k * 0.17, "pop", 0.6)
    sfx(t0, "whoosh", 0.8)


@S(3, 7, 10, "Hero at night, doors glowing behind")
def s03(t0, t1):
    c, ds = street(t0, t1, n=30, seed=3, pop_in=False)
    K = hero(t0, t1, "neutral")
    K.walk(t0, t1, (-6, -2, 0), (4, -2, 0), rate=2.2, face_dir=False)
    K.pose(t0, rot=-30)
    K.pose(t1, rot=-60)
    look_at(K, t0 + 0.2, (6, 40, 6))
    cam = Cam()
    cam.track(K, t0, t1, offset=(-3.5, -9, 1.5), look_up=4.2, lens=30, fstop=3)
    cam.handheld(1.0)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.2, "footsteps", 0.5)


@S(4, 10, 15, "A door opens: light spills, leads somewhere")
def s04(t0, t1):
    c, ds = street(t0, t1, n=14, seed=4, pop_in=False, clear=12)
    rt, pv = door("main", (0, 7, 0), "#ff7a2e", s=1.0, portal="#fff0c8", coll=c)
    K = hero(t0, t1, "gasp", loc=(-4, 0, 0), rot=15)
    light("dglow", "POINT", (0, 3, 6), 7000, (1.0, 0.8, 0.55), 2.0)
    swing(pv, t0 + 0.5, 105, 0.5)
    look_at(K, t0 + 0.1, (0, 7, 6))
    K.act(t0 + 0.6, "shock")
    cam = Cam()
    cam.key(t0, (3, -10, 3.2), (0, 7, 5), lens=26, focus=14, fstop=3)
    cam.key(t1, (1.5, -4.5, 5.0), (0, 7, 5), lens=22, focus=9, fstop=3)
    cam.crash(t0 + 0.55, 26, 18, 0.15)
    cam.handheld(1.0)
    sfx(t0 + 0.5, "door", 0.9)
    sfx(t0 + 0.55, "sparkle", 0.8)


@S(5, 15, 17, "Sunrise creeps up behind the roofs")
def s05(t0, t1):
    c, ds = street(t0, t1, n=26, seed=5, pop_in=False, dawn=True)
    K = hero(t0, t1, "worried", loc=(0, 0, 0))
    look_at(K, t0, (0, 150, 14))
    cam = Cam()
    cam.key(t0, (-4, -10, 1.5), (4, 60, 12), lens=24, focus=30, fstop=5)
    cam.key(t1, (-2, -8, 3.5), (4, 60, 12), lens=18, focus=30, fstop=5)
    cam.handheld(1.0)
    sfx(t0, "rise", 0.7)


@S(6, 17, 19, "Doors vanish one by one with poofs")
def s06(t0, t1):
    c, ds = street(t0, t1, n=26, seed=6, pop_in=False, dawn=True)
    for k, (rt, pv, col) in enumerate(ds):
        tv = t0 + 0.03 + (k / len(ds)) * (t1 - t0 - 0.2)
        shrink(rt, tv, rt.scale[0], 0.2)
        if k % 3 == 0:
            W2.poof(f"pf{k}", (rt.location[0], rt.location[1] - 1.2, 3.5), tv, 1.2, n=4, seed=k)
    cam = Cam()
    cam.key(t0, (0, -4, 6), (0, 40, 5), lens=20, focus=30, fstop=5)
    cam.key(t1, (0, -2, 9), (0, 40, 5), lens=26, focus=30, fstop=5)
    cam.handheld(1.3)
    for k in range(5):
        sfx(t0 + 0.08 + k * 0.14, "poof", 0.7)


# ================================================================== 2  Tarasic and the purple door
@S(7, 19, 22, "Friend Tarasic waves, huge grin")
def s07(t0, t1):
    c, ds = street(t0, t1, n=22, seed=7, pop_in=False, clear=14)
    T = tara(t0, t1, "happy", loc=(0, 0, 0))
    T.act(t0 + 0.15, "wave", expr="happy")
    lips(T, t0, t1)
    camL(t0, t1, (0, 0, 0), 11, 6, yaw=18, yaw1=-4, lens=45)
    sfx(t0 + 0.3, "whoosh", 0.5)


@S(8, 22, 26, "He opens a purple door: light pours out")
def s08(t0, t1):
    c, ds = street(t0, t1, n=14, seed=8, pop_in=False, clear=14)
    rt, pv = door("pdoor", (0, 6, 0), PURPLE, portal="#ffffff", coll=c)
    T = tara(t0, t1, "happy", loc=(0, 0, 0), rot=0)
    T.act(t0 + 0.2, "reach", expr="happy")
    beach_card("bcard", (0, 5.9, 0), s=1.0)
    swing(pv, t0 + 0.4, 110, 0.4)
    light("pglow", "POINT", (0, 3, 6), 9000, (0.9, 0.7, 1.0), 2.0)
    cam = Cam()
    cam.key(t0, (-5, -8, 3), (0, 6, 4.5), lens=26, focus=12, fstop=3)
    cam.key(t1, (-1.5, -3.5, 4.5), (0, 6, 4.5), lens=20, focus=9, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.4, "door", 0.8)
    sfx(t0 + 0.45, "rise", 0.7)


@S(9, 26, 29, "Reveal: a sunny beach")
def s09(t0, t1):
    beach_full()
    T = tara(t0, t1, "joy", loc=(0, 4, 0), rot=0)
    T.act(t0 + 0.1, "cheer", expr="joy")
    cam = Cam()
    cam.push(t0, t1, (0, 4, 4.5), 12, 7.5, yaw=-16, pitch=3, lens=26, yaw1=14, fstop=4)
    cam.handheld(1.0)
    sfx(t0, "sparkle", 0.9)
    sfx(t0 + 0.1, "kids_laugh", 0.5)


@S(10, 29, 33, "Square waves bobbing, low dolly")
def s10(t0, t1):
    beach_full()
    cam = Cam()
    cam.key(t0, (-10, 20, 3.0), (0, 38, 1.2), lens=24, focus=22, fstop=4)
    cam.key(t1, (6, 24, 3.6), (0, 38, 1.2), lens=24, focus=18, fstop=4)
    cam.handheld(1.1)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 0.6, "splat", 0.5)


@S(11, 33, 38, "ONE RULE pop text")
def s11(t0, t1):
    street(t0, t1, n=22, seed=11, pop_in=False)
    K = hero(t0, t1, "determined", loc=(0, 0, 0))
    K.act(t0 + 0.1, "point_l")
    lips(K, t0, t1)
    pop_text("rule", "ONE RULE", (4.5, 0, 9), t0 + 0.55, 1.6, "#ff4f4f", yaw=-18)
    camL(t0, t1, (0, 0, 0), 9, 6, yaw=12, yaw1=-6, lens=35)
    sfx(t0 + 0.55, "boom", 0.8)


@S(12, 38, 42, "Be back before sunrise: glance at the dark horizon")
def s12(t0, t1):
    c, ds = street(t0, t1, n=24, seed=12, pop_in=False)
    K = hero(t0, t1, "worried", loc=(0, 0, 0))
    look_at(K, t0, (0, 150, 14))
    K.act(t0 + 0.3, "think")
    cam = Cam()
    cam.key(t0, (3, -7, 2.0), (0, 40, 13), lens=22, focus=8, fstop=3)
    cam.key(t1, (-2, -6, 4.0), (0, 40, 15), lens=22, focus=8, fstop=3)
    cam.handheld(1.0)
    sfx(t0, "crickets", 0.5)


@S(13, 42, 46, "Door starts to fade / shrink")
def s13(t0, t1):
    c, ds = street(t0, t1, n=10, seed=13, pop_in=False, clear=14, dawn=True)
    rt, pv = door("vdoor", (0, 8, 0), PURPLE, portal="#ffffff", coll=c)
    beach_card("bcard2", (0, 7.9, 0))
    swing(pv, t0, 100, 0.1)
    shrink(rt, t0 + 1.0, 1.0, 0.7)
    W2.poof("pv", (0, 6.5, 4.0), t0 + 1.0, 1.6, n=5, seed=3)
    cam = Cam()
    cam.push(t0, t1, (0, 8, 4.4), 14, 8, yaw=-12, pitch=3, lens=30, yaw1=10, fstop=4)
    cam.crash(t0 + 0.95, 30, 22, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.2, "rise", 0.8)
    sfx(t0 + 1.0, "poof", 0.9)


@S(14, 46, 49, "Tarasic panics, door vanishing with him inside")
def s14(t0, t1):
    beach_full()
    T = tara(t0, t1, "terror", loc=(0, 6, 0))
    T.act(t0 + 0.1, "hands_head", expr="terror")
    T.panic(t0 + 0.4, t1, rate=8)
    rt, pv = door("vd2", (0, 12, 0), PURPLE, portal="#ffffff")
    shrink(rt, t0 + 0.6, 1.0, 0.8)
    cam = Cam()
    cam.push(t0, t1, (0, 6, 4.8), 8, 4.2, yaw=0, pitch=2, lens=34, fstop=2.8)
    cam.crash(t0 + 0.1, 34, 50, 0.1)
    cam.handheld(2.0)
    sfx(t0 + 0.1, "gasp", 0.8)
    sfx(t0 + 0.6, "rise", 0.8)


# ================================================================== 3  Dad & Mom
@S(15, 49, 52, "Dad, serious, by the kitchen window")
def s15(t0, t1):
    kitchen("dinner")
    Dd = dad(t0, t1, "angry", loc=(0, -1, 0))
    Dd.act(t0 + 0.2, "point", expr="angry")
    lips(Dd, t0, t1)
    camL(t0, t1, (0, -1, 0), 12, 7.5, yaw=-14, yaw1=8, lens=40)
    sfx(t0 + 0.1, "stomp", 0.5)


@S(16, 52, 56, "TRAP: the door as a trap")
def s16(t0, t1):
    c, ds = street(t0, t1, n=12, seed=16, pop_in=False, clear=14)
    rt, pv = door("td", (0, 8, 0), "#e8423a", portal="#ff2a2a", glow=3, coll=c)
    swing(pv, t0 + 0.3, 40, 0.3)
    swing(pv, t0 + 0.9, 0, 0.1, 40)
    pop_text("trap", "TRAP!", (0, 2, 12), t0 + 0.4, 2.2, "#ff3a3a")
    for k in range(5):
        box(f"tooth{k}", (0.3, 0.2, 1.0), (-1.6 + k * 0.8, 6.3, 5.0), M("#f4f4f4", 0.4), 0.08, rot=(0, 0, 180))
    cam = Cam()
    cam.push(t0, t1, (0, 8, 4.6), 16, 9, yaw=-18, pitch=4, lens=32, yaw1=10, fstop=4)
    cam.crash(t0 + 0.4, 32, 22, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.3, "boom", 0.8)
    sfx(t0 + 0.9, "hammer", 0.8)
    sfx(t0 + 0.4, "alarm", 0.4)


@S(17, 56, 59, "Mom walks off, smiling, ignoring")
def s17(t0, t1):
    c, ds = street(t0, t1, n=18, seed=17, pop_in=False, clear=12)
    Mo = mom(t0, t1, "smile", loc=(-6, 0, 0))
    Mo.walk(t0, t1, (-6, 0, 0), (5, 14, 0), rate=2.2)
    Dd = dad(t0, t1, "worried", loc=(-9, -4, 0), rot=-60)
    Dd.act(t0 + 0.1, "hands_head", expr="worried")
    cam = Cam()
    cam.track(Mo, t0, t1, offset=(-5, -11, 2.0), look_up=4.0, lens=26, fstop=4)
    cam.handheld(1.0)
    sfx(t0, "footsteps", 0.6)


# ================================================================== 4  A year ago
@S(18, 59, 62, "A YEAR AGO title, evening street")
def s18(t0, t1):
    c, ds = street(t0, t1, n=16, seed=18, pop_in=False, clear=12, dawn=True)
    pop_text("yago", "1 YEAR AGO", (0, 6, 10), t0 + 0.1, 1.5, "#ffe14a", yaw=0)
    Mo = mom(t0, t1, "smile", loc=(0, 0, 0))
    cam = Cam()
    cam.key(t0, (0, -12, 3.5), (0, 8, 7), lens=26, focus=16, fstop=4)
    cam.key(t1, (0, -8, 5.5), (0, 8, 8), lens=20, focus=14, fstop=4)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "ding", 0.7)
    sfx(t0 + 0.12, "whoosh", 0.7)


@S(19, 62, 66, "Mom walks into a green door")
def s19(t0, t1):
    c, ds = street(t0, t1, n=14, seed=19, pop_in=False, clear=14)
    rt, pv = door("gdoor", (0, 8, 0), GREEN, portal="#aaffcc", glow=3.0, coll=c)
    light("gg", "POINT", (0, 3, 6), 9000, (0.2, 1.0, 0.45), 2.0)
    swing(pv, t0 + 0.2, 100, 0.4)
    Mo = mom(t0, t1, "smile", loc=(0, -6, 0), rot=180)
    Mo.walk(t0, t1, (0, -6, 0), (0, 8.6, 0), rate=2.4, face_dir=True)
    cam = Cam()
    cam.track(Mo, t0, t1, offset=(3, -9, 1.2), look_up=4.2, lens=26, fstop=4)
    cam.handheld(0.9)
    sfx(t0, "footsteps", 0.6)
    sfx(t0 + 0.2, "door", 0.8)
    sfx(t0 + 0.3, "sparkle", 0.6)


@S(20, 66, 70, "Mom at the doorway turns, waves")
def s20(t0, t1):
    c, ds = street(t0, t1, n=10, seed=20, pop_in=False, clear=14)
    rt, pv = door("gdoor", (0, 8, 0), GREEN, portal="#3a9a5a", glow=1.5, coll=c)
    swing(pv, t0, 100, 0.01)
    light("gg", "POINT", (0, 3, 6), 9000, (0.2, 1.0, 0.45), 2.0)
    Mo = mom(t0, t1, "smile", loc=(0, 7, 0), rot=0)
    Mo.act(t0 + 0.2, "wave", expr="happy")
    lips(Mo, t0, t1)
    camL(t0, t1, (0, 7, 0), 9, 5.5, yaw=-20, yaw1=6, lens=40)
    sfx(t0 + 0.4, "whoosh", 0.4)


@S(21, 70, 74, '"Just a quick look" - Mom close-up')
def s21(t0, t1):
    c, ds = street(t0, t1, n=10, seed=21, pop_in=False, clear=14)
    Mo = mom(t0, t1, "wink", loc=(0, 0, 0))
    lips(Mo, t0, t1)
    light("gg2", "POINT", (3, -3, 6), 5000, (0.2, 1.0, 0.45), 2.0)
    camL(t0, t1, (0, 0, 0), 6.5, 4.2, yaw=16, yaw1=-8, lens=50)
    sfx(t0 + 0.5, "ding", 0.5)


@S(22, 74, 79, "Dawn: Mom steps out of the door, smiling")
def s22(t0, t1):
    c, ds = street(t0, t1, n=8, seed=22, pop_in=False, clear=14, dawn=True)
    rt, pv = door("gdoor", (0, 8, 0), GREEN, portal="#aaffcc", glow=3.0, coll=c)
    swing(pv, t0 - 0.3, 100, 0.3)
    Mo = mom(t0, t1, "grin", loc=(0, 8, 0), rot=0)
    Mo.walk(t0, t1, (0, 7.5, 0), (0, -4, 0), rate=2.2)
    cam = Cam()
    cam.key(t0, (-2, -12, 1.6), (0, 8, 5), lens=24, focus=20, fstop=3)
    cam.key(t1, (2, -9, 3.2), (0, 0, 5), lens=30, focus=9, fstop=3)
    cam.handheld(1.0)
    sfx(t0, "door", 0.7)
    sfx(t0 + 0.3, "footsteps", 0.5)


@S(23, 79, 84, "But something was off: dolly zoom on grin")
def s23(t0, t1):
    kitchen("creep")
    Mo = mom(t0, t1, "grin", loc=(0, -1, 0), fake=False)
    Mo.face(t0, eyes="wide", mouth="grin")
    cam = Cam()
    p = hp((0, -1, 0))
    cam.key(t0, (0, -12, 4.8), p, lens=24, focus=11, fstop=2.4)
    cam.key(t1, (0, -5, 4.7), p, lens=62, focus=4.5, fstop=2.4)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "rise", 0.9)
    sfx(t0 + 1.3, "zombie", 0.4)


@S(24, 84, 87, "Humming songs: notes floating")
def s24(t0, t1):
    kitchen("dinner")
    Mo = mom(t0, t1, "smile", loc=(0, -1, 0))
    Mo.face(t0, eyes="closed", mouth="smile")
    Mo.pose(t0, head=(0, -5, 8))
    Mo.pose(t1, head=(0, -5, -8))
    for k in range(5):
        n = sphere(f"note{k}", 0.35, (1.6 + k * 0.3, -3.5, 5.0), emitm("#ffe14a", 4), (1, 0.6, 1), seg=10)
        n.keyframe_insert("location", frame=F(t0 + k * 0.1))
        n.location = (1.6 + k * 0.3 + 1.0, -3.5, 9.5 + k * 0.5)
        n.keyframe_insert("location", frame=F(t1))
    camL(t0, t1, (0, -1, 0), 9, 6, yaw=14, yaw1=-10, lens=36)
    sfx(t0, "sparkle", 0.5)


@S(25, 87, 91, "Hero confused: never heard it")
def s25(t0, t1):
    kitchen("dinner")
    K = hero(t0, t1, "confused", loc=(-4.5, -1, 0))
    K.face(t0 + 0.8, "sus")
    K.pose(t0, head=(10, 4, 0))
    camL(t0, t1, (-4.5, -1, 0), 6.5, 4.4, yaw=-16, yaw1=10, lens=50)
    sfx(t0 + 0.2, "chat", 0.4)


@S(26, 91, 96, "She forgot I hate mushrooms: plate of mushrooms")
def s26(t0, t1):
    kitchen("dinner")
    K = hero(t0, t1, "sus", loc=(-4.5, -1, 0))
    sit_on(K, t0, (-4.5, -1.2, 2.1))
    K.act(t0 + 0.9, "recoil", expr="scream")
    cam = Cam()
    cam.key(t0, (-1, -9, 5.4), (-4.5, -5, 3.0), lens=36, focus=7, fstop=2.8)
    cam.key(t1, (-3.6, -7.5, 4.6), (-4.5, -5, 3.0), lens=48, focus=4, fstop=2.8)
    cam.crash(t0 + 0.9, 42, 60, 0.1)
    cam.handheld(1.0)
    sfx(t0 + 0.9, "splat", 0.5)
    sfx(t0 + 0.9, "gasp", 0.6)
    sfx(t0 + 0.1, "place", 0.6)


@S(27, 96, 99, "Dad's side-eye")
def s27(t0, t1):
    kitchen("dinner")
    Dd = dad(t0, t1, "side_r", loc=(4.5, -1, 0))
    Dd.face(t0, eyes="side_l", mouth="frown")
    camL(t0, t1, (4.5, -1, 0), 6.0, 4.0, yaw=-22, yaw1=0, lens=55)
    sfx(t0 + 0.1, "rise", 0.5)


@S(28, 99, 102, "Wide dinner shot, dad staring all dinner")
def s28(t0, t1):
    kitchen("dinner")
    K = hero(t0, t1, "worried")
    Mo = mom(t0, t1, "grin")
    Dd = dad(t0, t1, "neutral")
    for ch, x in ((K, -4.5), (Mo, 0), (Dd, 4.5)):
        sit_on(ch, t0, (x, -1.2, 2.1))
    Dd.face(t0, eyes="side_l", mouth="frown")
    Mo.face(t0, eyes="normal", mouth="grin")
    cam = Cam()
    cam.key(t0, (-4, -13.2, 7), (0, 0, 4.6), lens=22, focus=14, fstop=4)
    cam.key(t1, (4, -12.4, 6.4), (0, 0, 4.6), lens=22, focus=13, fstop=4)
    cam.handheld(0.8)
    sfx(t0, "clink", 0.4)


@S(29, 102, 105, "Dad leans in to whisper")
def s29(t0, t1):
    kitchen("dinner")
    Dd = dad(t0, t1, "worried", loc=(0, -1, 0))
    Dd.pose(t0, torso=(0, 0, 0))
    Dd.pose(t0 + 0.3, torso=(-20, 14, 0), head=(-20, 0, 8))
    camL(t0, t1, (0, -1, 0), 7, 4.4, yaw=-28, yaw1=-18, lens=50)
    sfx(t0 + 0.1, "whoosh", 0.4)


@S(30, 105, 110, "Rock and roll, lose control: whisper close-up")
def s30(t0, t1):
    kitchen("dinner")
    Dd = dad(t0, t1, "worried", loc=(0, -1, 0))
    lips(Dd, t0, t1)
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 6.5, 3.0, yaw=0, pitch=2, lens=60, fstop=2.0)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "wind", 0.4)


@S(31, 110, 115, "Our secret code for run: RUN pop")
def s31(t0, t1):
    kitchen("dinner")
    K = hero(t0, t1, "gasp", loc=(0, -1, 0))
    K.act(t0 + 0.2, "recoil", expr="shock")
    pop_text("runtxt", "RUN", (0, -5, 11), t0 + 0.9, 3.0, "#ff3a3a")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 8, 4.2, yaw=12, pitch=3, lens=42, yaw1=-8, fstop=2.4)
    cam.crash(t0 + 0.9, 42, 28, 0.1)
    cam.handheld(1.4)
    sfx(t0 + 0.2, "gasp", 0.7)
    sfx(t0 + 0.9, "boom", 0.9)


# ================================================================== 5  The green door, last week
@S(32, 115, 118, "Last week, I... hero marches through a night street")
def s32(t0, t1):
    c, ds = street(t0, t1, n=30, seed=32, pop_in=False)
    K = hero(t0, t1, "determined", loc=(0, 20, 0), rot=180)
    K.walk(t0, t1, (0, 14, 0), (0, -4, 0), rate=2.4)
    cam = Cam()
    cam.track(K, t0, t1, offset=(2.6, -7.5, 1.2), look_up=4.4, lens=26, fstop=4)
    cam.handheld(1.2)
    sfx(t0, "footsteps", 0.7)
    sfx(t0 + 0.4, "wind", 0.4)


@S(33, 118, 121, "Searching: whip around, running between doors")
def s33(t0, t1):
    c, ds = street(t0, t1, n=40, seed=33, pop_in=False, clear=3)
    K = hero(t0, t1, "worried", loc=(0, 0, 0))
    K.walk(t0, t1, (-6, 4, 0), (8, 22, 0), rate=3.4, swing=48, arm=55, bob=0.3)
    cam = Cam()
    cam.key(t0, (-14, -6, 5), (-6, 4, 5), lens=22, focus=14, fstop=4)
    cam.key(t1, (14, 4, 4), (8, 22, 5), lens=22, focus=14, fstop=4)
    cam.handheld(2.0)
    sfx(t0, "whoosh", 0.8)
    sfx(t0 + 0.2, "footsteps", 0.6)


@S(34, 121, 124, "The green door among the others: push in")
def s34(t0, t1):
    c, ds = street(t0, t1, n=30, seed=34, pop_in=False, clear=3)
    rt, pv = door("gdoor", (0, 14, 0), GREEN, portal="#aaffcc", glow=4.0, coll=c)
    light("gg", "POINT", (0, 8, 7), 12000, (0.2, 1.0, 0.45), 2.0)
    cam = Cam()
    cam.push(t0, t1, (0, 14, 4.6), 24, 9, yaw=14, pitch=2, lens=28, yaw1=-6, fstop=3)
    cam.crash(t0 + 0.2, 28, 20, 0.12)
    cam.handheld(1.2)
    sfx(t0, "rise", 0.8)
    sfx(t0 + 0.2, "ding", 0.7)


@S(35, 124, 129, "It appears behind the school with a poof")
def s35(t0, t1):
    c, ds = street(t0, t1, n=6, seed=35, pop_in=False, school=True, clear=20)
    rt, pv = door("gdoor", (12, 23.0, 0), GREEN, portal="#aaffcc", glow=4.0, coll=c)
    pop(rt, t0 + 0.4, 1.0, 0.25)
    W2.poof("gp", (12, 22.0, 4.0), t0 + 0.4, 1.6, n=6, seed=1)
    light("gg", "POINT", (12, 18, 7), 12000, (0.2, 1.0, 0.45), 2.0)
    K = hero(t0, t1, "gasp", loc=(2, 8, 0), rot=-10)
    cam = Cam()
    cam.key(t0, (-16, -4, 3.4), (8, 23, 6), lens=22, focus=34, fstop=4)
    cam.key(t1, (-2, 2, 4.2), (12, 23, 6), lens=22, focus=24, fstop=4)
    cam.handheld(1.2)
    sfx(t0 + 0.4, "poof", 0.9)
    sfx(t0 + 0.5, "sparkle", 0.7)


@S(36, 129, 134, "Glowing like a candy wrapper: orbit")
def s36(t0, t1):
    c, ds = street(t0, t1, n=4, seed=36, pop_in=False, school=True, clear=30)
    rt, pv = door("gdoor", (0, 22.5, 0), GREEN, portal="#aaffcc", glow=5.0, coll=c)
    light("gg", "POINT", (0, 15, 7), 16000, (0.2, 1.0, 0.45), 2.0)
    cam = Cam()
    cam.orbit(t0, t1, (0, 22.5, 4.4), 16, -35, 35, pitch=6, lens=32, steps=5, fstop=3)
    cam.handheld(0.8)
    sfx(t0, "sparkle", 0.8)
    sfx(t0 + 0.7, "rise", 0.5)


@S(37, 134, 139, '"If you don\'t come back" Tarasic, worried')
def s37(t0, t1):
    c, ds = street(t0, t1, n=10, seed=37, pop_in=False, clear=14)
    T = tara(t0, t1, "worried", loc=(0, 0, 0))
    lips(T, t0, t1)
    light("gg3", "POINT", (-3, -2, 6), 4000, (0.2, 1.0, 0.45), 2.0)
    camL(t0, t1, (0, 0, 0), 6.5, 4.4, yaw=-16, yaw1=8, lens=50)
    sfx(t0 + 0.2, "wind", 0.4)


@S(38, 139, 145, "I'll tell everyone you were brave: salute, hero nervous")
def s38(t0, t1):
    c, ds = street(t0, t1, n=10, seed=38, pop_in=False, clear=14)
    T = tara(t0, t1, "smile", loc=(3, 0, 0), rot=-12)
    T.act(t0 + 1.4, "cheer", expr="smile")
    lips(T, t0, t1)
    K = hero(t0, t1, "worried", loc=(-3, 0, 0), rot=12)
    K.act(t0 + 0.2, "slump", expr="worried")
    cam = Cam()
    cam.push(t0, t1, (0, 0, 4.4), 22, 14, yaw=0, pitch=3, lens=35, yaw1=-10, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 1.2, "ding", 0.5)


@S(39, 145, 148, "I stepped inside: POV into the green light")
def s39(t0, t1):
    c, ds = street(t0, t1, n=4, seed=39, pop_in=False, clear=30, school=True)
    rt, pv = door("gdoor", (0, 14, 0), GREEN, portal="#ccffdd", glow=4.0, coll=c)
    swing(pv, t0 + 0.1, 105, 0.35)
    light("gg", "POINT", (0, 10, 7), 20000, (0.2, 1.0, 0.45), 2.0)
    cam = Cam()
    cam.key(t0, (0, -2, 4.4), (0, 14, 4.2), lens=26, focus=16, fstop=3)
    cam.key(t1, (0, 13.4, 4.2), (0, 20, 4.2), lens=18, focus=2, fstop=3)
    flash("wf", t1 - 0.15, 0.2, (0.4, 1, 0.6), at=(0, 12, 4))
    cam.handheld(1.3)
    sfx(t0, "footsteps", 0.6)
    sfx(t0 + 0.1, "door", 0.8)
    sfx(t0 + 0.4, "whoosh", 0.8)


# ================================================================== 6  Inside: the real mom
@S(40, 148, 151, "Darkness: hero's face lit only by green")
def s40(t0, t1):
    kitchen("dark")
    K = hero(t0, t1, "scared", loc=(0, -9, 0), rot=180)
    K.act(t0 + 0.2, "brace", expr="scared")
    cam = Cam()
    cam.push(t0, t1, hp((0, -9, 0)), 7, 4.5, yaw=180, pitch=2, lens=40, yaw1=170, fstop=2.0)
    cam.handheld(1.2)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.3, "heartbeat", 0.6)


@S(41, 151, 154, "Lights flick on: it's my kitchen")
def s41(t0, t1):
    kitchen("creep")
    K = hero(t0, t1, "gasp", loc=(0, -6, 0), rot=0)
    look_at(K, t0, (0, 6, 5))
    cam = Cam()
    cam.key(t0, (-4, -13.2, 6), (0, 4, 4), lens=20, focus=16, fstop=5)
    cam.key(t1, (2, -12.6, 5.5), (0, 4, 4), lens=24, focus=14, fstop=5)
    flash("lf", t0 + 0.1, 0.25, (1, 1, 0.9), at=(0, -6, 12), e=60000)
    cam.crash(t0 + 0.1, 20, 28, 0.12)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "click", 0.9)
    sfx(t0 + 0.12, "ding", 0.6)


def tied_mom(t0, t1, expr="scared"):
    Mo = mom(t0, t1, expr, loc=(0, -1, 0), name="RealMom")
    sit_on(Mo, t0, (0, -1.2, 2.1))
    Mo.pose(t0, armL=(5, 28), armR=(5, 28), legL=(85, 3), legR=(85, -3))
    Mr = M("#8a5a32", 0.8)
    box("rope1", (2.5, 1.35, 0.22), (0, -1.2, 3.6), Mr, 0.06)
    box("rope2", (2.5, 1.35, 0.22), (0, -1.2, 2.9), Mr, 0.06)
    return Mo


@S(42, 154, 160, "At the table sat my real mom: push in")
def s42(t0, t1):
    kitchen("creep")
    Mo = tied_mom(t0, t1)
    Mo.face(t0, "scared")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 12, 7, yaw=-16, pitch=8, lens=28, yaw1=4, fstop=3)
    cam.handheld(1.2)
    sfx(t0, "rise", 0.8)
    sfx(t0 + 0.8, "rope", 0.6)


@S(43, 160, 165, "Tied to a chair: ropes close-up")
def s43(t0, t1):
    kitchen("creep")
    Mo = tied_mom(t0, t1)
    Mo.pose(t0, torso=(0, 0, 3))
    Mo.pose(t0 + 0.2, torso=(0, 0, -3))
    Mo.pose(t0 + 0.4, torso=(0, 0, 3))
    Mo.pose(t0 + 0.6, torso=(0, 0, -3))
    cam = Cam()
    cam.key(t0, (2.8, -7, 4.2), (0, -1.6, 4.0), lens=45, focus=7, fstop=2.2)
    cam.key(t1, (-2.4, -6, 4.6), (0, -1.6, 4.0), lens=55, focus=6, fstop=2.2)
    cam.handheld(1.2)
    sfx(t0, "rope", 0.8)
    sfx(t0 + 0.4, "thud", 0.5)


@S(44, 165, 168, '"Run," she mouthed: extreme close up')
def s44(t0, t1):
    kitchen("creep")
    Mo = tied_mom(t0, t1)
    Mo.face(t0, eyes="terror", mouth="talk_wide")
    Mo.face(t0 + 0.25, mouth="o")
    Mo.face(t0 + 0.5, mouth="talk_wide")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 6.5, 2.6, yaw=0, pitch=2, lens=55, fstop=1.8)
    cam.crash(t0 + 0.1, 55, 75, 0.1)
    cam.handheld(1.6)
    sfx(t0 + 0.1, "heartbeat", 0.8)
    sfx(t0 + 0.1, "gasp", 0.5)


@S(45, 168, 174, "The door slams shut behind me")
def s45(t0, t1):
    kitchen("creep")
    c = None
    K = hero(t0, t1, "gasp", loc=(0, -9, 0), rot=180)
    for ob in list(D.objects):
        if ob.name == "k_exit_piv":
            swing(ob, t0 + 0.1, 0, 0.01, 0)
            slam(ob, t0 + 0.9, 105, 0.12)
    K.act(t0 + 1.0, "shock", expr="shock")
    cam = Cam()
    cam.key(t0, (0, -2, 5.5), (0, -14, 4), lens=22, focus=12, fstop=4)
    cam.key(t1, (1, -3, 5.2), (0, -14, 4), lens=28, focus=11, fstop=4)
    cam.crash(t0 + 0.95, 22, 38, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.9, "door", 1.0)
    sfx(t0 + 0.92, "boom", 0.9)
    flash("sl", t0 + 0.92, 0.3, (0.3, 1, 0.5), at=(0, -10, 6), e=30000)


@S(46, 174, 176, "Mom laughs: hero turns")
def s46(t0, t1):
    kitchen("creep", ceil=True)
    K = hero(t0, t1, "scared", loc=(0, -6, 0), rot=0)
    K.pose(t0, head=(30, 0, 0))
    K.face(t0 + 0.3, "terror")
    camL(t0, t1, (0, -6, 0), 6.5, 4.4, yaw=-14, yaw1=14, lens=50)
    sfx(t0, "zombie", 0.5)


@S(47, 176, 182, "...it came from the ceiling: tilt up")
def s47(t0, t1):
    kitchen("creep", ceil=True)
    ceiling_faces(t0, t1, 4, 2)
    cam = Cam()
    cam.key(t0, (0, -9, 5), (0, -2, 6), lens=26, focus=9, fstop=4)
    cam.key(t1, (0, -9, 6), (0, -3, 16), lens=22, focus=12, fstop=4)
    cam.handheld(1.2)
    sfx(t0, "rise", 0.9)
    sfx(t0 + 0.3, "kids_laugh", 0.3)


@S(48, 182, 190, "Dozens of faces pressed into the plaster")
def s48(t0, t1):
    kitchen("creep", ceil=True)
    ceiling_faces(t0, t1, 5, 3)
    cam = Cam()
    cam.key(t0, (-12, -10, 7), (0, -1, 15), lens=24, focus=14, fstop=4)
    cam.key(t1, (10, -8, 8), (0, -1, 15), lens=24, focus=12, fstop=4)
    cam.handheld(1.0)
    sfx(t0, "zombie", 0.6)
    sfx(t0 + 0.5, "glitch", 0.5)


@S(49, 190, 195, "All wearing my mother's smile: extreme close-up")
def s49(t0, t1):
    kitchen("creep", ceil=True)
    fs = ceiling_faces(t0, t1, 3, 2, seed=5)
    cam = Cam()
    cam.key(t0, (-2, -8, 11), (0, -3.5, 14.5), lens=36, focus=7, fstop=2.0)
    cam.key(t1, (0, -6, 12.5), (0, -3.5, 14.5), lens=60, focus=4, fstop=2.0)
    cam.crash(t0 + 1.0, 36, 70, 0.1)
    cam.handheld(0.8)
    sfx(t0, "zombie", 0.5)
    sfx(t0 + 1.0, "boom", 0.6)


@S(50, 195, 200, "I cut the ropes: hero hacks at the rope")
def s50(t0, t1):
    kitchen("creep")
    Mo = tied_mom(t0, t1)
    K = hero(t0, t1, "determined", loc=(2.5, -6.5, 0), rot=-20)
    K.act(t0 + 0.2, "reach", expr="determined")
    camL(t0, t1, (1.2, -3.5, 0), 9, 6, yaw=-25, yaw1=-8, lens=36)
    sfx(t0 + 0.1, "rope", 0.8)
    sfx(t0 + 0.4, "whoosh", 0.5)


@S(51, 200, 203, "A butter knife: insert close-up")
def s51(t0, t1):
    kitchen("creep")
    root = empty("knife", (0, -3.5, 4.0), rot=(0, 0, 30))
    box("kn_blade", (0.45, 0.08, 2.4), (0, 0, 1.2), M("#e8e8ee", 0.2, metal=0.9), 0.04, parent=root)
    box("kn_h", (0.5, 0.18, 1.5), (0, 0, -0.6), M("#d9a050", 0.5), 0.07, parent=root)
    noise(root, "rotation_euler", 1, 0.5, 4)
    box("kn_rope", (3.0, 0.5, 0.3), (0, -3.3, 3.9), M("#8a5a32", 0.8), 0.08)
    cam = Cam()
    cam.key(t0, (1.5, -6, 4.8), (0, -3.5, 4.4), lens=60, focus=5, fstop=1.6)
    cam.key(t1, (-1.0, -5.5, 4.4), (0, -3.5, 4.4), lens=80, focus=4, fstop=1.6)
    cam.handheld(1.5)
    sfx(t0 + 0.1, "clink", 0.8)
    sfx(t0 + 0.5, "rope", 0.8)


@S(52, 203, 209, "We sprinted through hallways that breathed")
def s52(t0, t1):
    hallway(t0, t1)
    K = hero(t0, t1, "scream")
    Mo = mom(t0, t1, "scared", name="RealMom")
    K.walk(t0, t1, (-1.8, 70, 0), (-1.8, 0, 0), rate=3.6, swing=50, arm=60, bob=0.3)
    Mo.walk(t0, t1, (2.0, 74, 0), (2.0, 4, 0), rate=3.6, swing=50, arm=60, bob=0.3)
    K.pose(t0, rot=0)
    cam = Cam()
    cam.track(K, t0, t1, offset=(0.5, -10, 2.2), look_up=4.4, lens=24, fstop=4)
    cam.handheld(2.2)
    sfx(t0, "footsteps", 0.9)
    sfx(t0 + 0.3, "whoosh", 0.6)
    sfx(t0 + 1.0, "zombie", 0.3)


@S(53, 209, 213, "The window turned gold")
def s53(t0, t1):
    hallway(t0, t1, gold_t=t0 + 0.8)
    K = hero(t0, t1, "gasp")
    Mo = mom(t0, t1, "gasp", name="RealMom")
    K.walk(t0, t1, (-1.8, 34, 0), (-1.8, 6, 0), rate=3.6, swing=50, arm=60, bob=0.3)
    Mo.walk(t0, t1, (2.0, 37, 0), (2.0, 9, 0), rate=3.6, swing=50, arm=60, bob=0.3)
    cam = Cam()
    cam.key(t0, (0, 46, 5.4), (0, -14, 6), lens=24, focus=40, fstop=5)
    cam.key(t1, (0, 30, 5.6), (0, -14, 6), lens=22, focus=40, fstop=5)
    cam.handheld(1.8)
    sfx(t0 + 0.8, "ding", 0.9)
    sfx(t0 + 0.8, "sparkle", 0.9)
    sfx(t0, "footsteps", 0.9)


@S(54, 213, 219, "We dove through the closing door")
def s54(t0, t1):
    c = collection("DIVE")
    world((0.1, 0.1, 0.08), 0.3)
    box("dv_floor", (30, 80, 0.4), (0, 10, -0.2), M("#3a2630", 0.5), 0, coll=c)
    box("dv_wl", (0.5, 80, 12), (-8, 10, 6), M("#5a3a4a", 0.9), 0, coll=c)
    box("dv_wr", (0.5, 80, 12), (8, 10, 6), M("#5a3a4a", 0.9), 0, coll=c)
    box("dv_wall", (16, 0.5, 12), (0, -12, 6), M("#5a3a4a", 0.9), 0, coll=c)
    rt, pv = door("dvd", (0, -11.5, 0), "#ffc83a", rot=180, portal="#fff0b0", glow=3.5, coll=c)
    swing(pv, t0, 100, 0.01)
    slam(pv, t0 + 1.4, 100, 0.55)
    light("dvl", "POINT", (0, -8, 6), 18000, (1.0, 0.8, 0.35), 3.0)
    light("dvf", "AREA", (0, 30, 12), 2500, (1.0, 0.7, 0.6), 12, coll=c, target=(0, 0, 3))
    K = hero(t0, t1, "scream")
    Mo = mom(t0, t1, "scream", name="RealMom")
    K.walk(t0, t0 + 1.1, (-1.8, 22, 0), (-1.8, -6, 0), rate=3.6, swing=50, arm=60, bob=0.3)
    Mo.walk(t0, t0 + 1.1, (2.0, 24, 0), (2.0, -5, 0), rate=3.6, swing=50, arm=60, bob=0.3)
    K.pose(t0 + 1.1, loc=(-1.8, -6, 0), armL=(160, 20), armR=(160, 20))
    K.pose(t0 + 1.5, loc=(-1.8, -14, 3), armL=(170, 10), armR=(170, 10), legL=(-30, 0), legR=(-30, 0))
    Mo.pose(t0 + 1.1, loc=(2.0, -5, 0), armL=(160, 20), armR=(160, 20))
    Mo.pose(t0 + 1.5, loc=(2.0, -13, 3), armL=(170, 10), armR=(170, 10), legL=(-30, 0), legR=(-30, 0))
    cam = Cam()
    cam.key(t0, (0, 38, 4.5), (0, 0, 5), lens=24, focus=30, fstop=5)
    cam.key(t0 + 1.1, (0, 14, 4.0), (0, -8, 5), lens=22, focus=20, fstop=5)
    cam.key(t1, (-3, -2, 3.0), (0, -12, 4), lens=20, focus=10, fstop=5)
    cam.handheld(2.0)
    sfx(t0 + 1.0, "whoosh", 0.9)
    sfx(t0 + 1.4, "door", 1.0)
    sfx(t0 + 1.3, "jet", 0.4)


@S(55, 219, 224, "Just as the sun rose: outside, collapsed on the grass, door vanishing")
def s55(t0, t1):
    c, ds = street(t0, t1, n=8, seed=55, pop_in=False, dawn=True, clear=14)
    rt, pv = door("fdoor", (0, 12, 0), GREEN, portal="#aaffcc", glow=3.0, coll=c)
    swing(pv, t0 - 0.2, 0, 0.01, 0)
    shrink(rt, t0 + 0.8, 1.0, 0.5)
    W2.poof("fp", (0, 10.5, 4), t0 + 0.8, 2.0, n=6, seed=4)
    K = hero(t0, t1, "relief", loc=(-1.8, 6, 0), rot=0)
    K.act(t0 + 0.1, "slump", expr="relief")
    Mo = mom(t0, t1, "relief", loc=(1.8, 6, 0), name="RealMom")
    Mo.act(t0 + 0.2, "slump", expr="relief")
    cam = Cam()
    cam.key(t0, (-9, -6, 2.0), (0, 8, 5), lens=24, focus=16, fstop=3)
    cam.key(t1, (5, -5, 4.5), (0, 10, 7), lens=22, focus=16, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.8, "poof", 0.9)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 1.0, "ding", 0.5)


# ================================================================== 7  Home, dawn
@S(56, 224, 228, "Dad was making pancakes: back at the stove, pancake flip")
def s56(t0, t1):
    kitchen("dawn", chairs=False)
    Dd = dad(t0, t1, "happy", loc=(6.0, 4.2, 0), rot=180)
    pc = cyl("flipcake", 0.62, 0.12, (6.0, 5.8, 3.4), M("#e8b060", 0.6), 16)
    pc.keyframe_insert("location", frame=F(t0 + 0.6))
    pc.location = (6.0, 5.4, 8.5)
    pc.keyframe_insert("location", frame=F(t0 + 0.95))
    pc.location = (6.0, 5.8, 3.4)
    pc.keyframe_insert("location", frame=F(t0 + 1.4))
    cam = Cam()
    cam.key(t0, (-3, -5, 6), (5, 4, 4.4), lens=28, focus=11, fstop=4)
    cam.key(t1, (2, -3, 5.6), (6, 4, 4.4), lens=34, focus=9, fstop=4)
    cam.handheld(0.9)
    sfx(t0 + 0.2, "ding", 0.6)
    sfx(t0 + 0.6, "pop", 0.6)
    sfx(t0 + 1.4, "place", 0.6)


@S(57, 228, 232, "Mom squeezed my hand: close-up of hands")
def s57(t0, t1):
    kitchen("dawn", chairs=False)
    Mo = mom(t0, t1, "worried", loc=(0.5, -1, 0), rot=-10, name="RealMom")
    K = hero(t0, t1, "relief", loc=(-2.0, -1, 0), rot=10)
    Mo.pose(t0 + 0.3, armL=(70, -10))
    K.pose(t0 + 0.3, armR=(70, -10))
    cam = Cam()
    cam.key(t0, (-3, -11, 4.6), (-0.6, -1, 3.8), lens=40, focus=11, fstop=2.4)
    cam.key(t1, (-1.5, -7.5, 4.4), (-0.6, -1, 3.8), lens=44, focus=7, fstop=2.4)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "place", 0.5)


@S(58, 232, 236, '"Listen carefully," she whispered')
def s58(t0, t1):
    kitchen("dawn")
    Mo = mom(t0, t1, "worried", loc=(0, -1, 0), name="RealMom")
    lips(Mo, t0, t1)
    Mo.act(t0 + 0.3, "lean")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 7, 3.4, yaw=14, pitch=3, lens=55, yaw1=-6, fstop=1.8)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "rise", 0.6)


@S(59, 236, 246, "Your father went through that door the night after me: flashback")
def s59(t0, t1):
    c, ds = street(t0, t1, n=10, seed=59, pop_in=False, clear=14)
    rt, pv = door("gdoor", (0, 14, 0), GREEN, portal="#aaffcc", glow=3.5, coll=c)
    swing(pv, t0 + 1.2, 100, 0.4)
    light("gg", "POINT", (0, 8, 7), 12000, (0.2, 1.0, 0.45), 2.0)
    Dd = dad(t0, t1, "worried", loc=(0, -6, 0), rot=180)
    Dd.walk(t0 + 0.4, t1 - 0.6, (0, -6, 0), (0, 14.5, 0), rate=2.4)
    cam = Cam()
    cam.key(t0, (-9, -14, 3), (0, 4, 5), lens=24, focus=20, fstop=4)
    cam.key(t1, (6, 0, 4.5), (0, 14, 5), lens=20, focus=14, fstop=4)
    cam.handheld(1.2)
    sfx(t0, "wind", 0.6)
    sfx(t0 + 0.4, "footsteps", 0.6)
    sfx(t0 + 1.2, "door", 0.8)


@S(60, 246, 250, "He never came back: hero's shock, crash zoom")
def s60(t0, t1):
    kitchen("dawn")
    K = hero(t0, t1, "shock", loc=(0, -1, 0))
    K.act(t0 + 0.5, "recoil", expr="terror")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 8, 3.4, yaw=0, pitch=2, lens=50, fstop=2.0)
    cam.crash(t0 + 0.55, 50, 85, 0.12)
    cam.handheld(1.4)
    sfx(t0 + 0.5, "boom", 0.9)
    sfx(t0 + 0.5, "gasp", 0.7)
    sfx(t0 + 0.2, "heartbeat", 0.7)


@S(61, 250, 255, "The man at the stove: creeping toward his back")
def s61(t0, t1):
    kitchen("dawn", chairs=False)
    Dd = dad(t0, t1, "happy", loc=(6.0, 4.2, 0), rot=180)
    cam = Cam()
    cam.key(t0, (-2, -12, 6.5), (6, 4.8, 5.2), lens=26, focus=20, fstop=3)
    cam.key(t1, (5.0, -3.0, 5.6), (6, 4.8, 5.2), lens=30, focus=9, fstop=3)
    cam.handheld(1.0)
    sfx(t0, "rise", 0.9)
    sfx(t0 + 0.5, "heartbeat", 0.7)


@S(62, 255, 257, "...turned around: whip around, the man's face")
def s62(t0, t1):
    kitchen("dawn", chairs=False)
    Dd = dad(t0, t1, "neutral", loc=(6.0, 4.2, 0), rot=180, fake=True)
    Dd.pose(t0 + 0.15, rot=180)
    Dd.pose(t0 + 0.85, rot=360)
    Dd.face(t0 + 0.85, eyes="normal", mouth="flat")
    cam = Cam()
    cam.key(t0, (7.5, -2.0, 5.6), (6, 4.8, 5.0), lens=36, focus=7, fstop=2.4)
    cam.key(t1, (7.0, -1.8, 5.4), (6, 4.8, 5.0), lens=44, focus=7, fstop=2.4)
    cam.handheld(1.4)
    sfx(t0 + 0.1, "whoosh", 0.8)
    sfx(t0 + 0.7, "thud", 0.7)


@S(63, 257, 259, "He smiled: extreme close-up of the wrong smile")
def s63(t0, t1):
    kitchen("dawn")
    Dd = dad(t0, t1, "grin", loc=(0, -1, 0), fake=True)
    Dd.face(t0, eyes="normal", mouth="grin")
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 6, 3.0, yaw=0, pitch=0, lens=60, fstop=1.8)
    cam.crash(t0, 60, 90, 0.2)
    cam.handheld(0.7)
    sfx(t0, "zombie", 0.8)
    sfx(t0, "glitch", 0.6)


@S(64, 259, 264, '"Rock and roll," he said: dad with green rim, glitch')
def s64(t0, t1):
    kitchen("creep")
    Dd = dad(t0, t1, "grin", loc=(0, -1, 0), fake=True)
    lips(Dd, t0, t1)
    Dd.face(t0, eyes="normal", mouth="grin")
    light("rimg", "POINT", (3, 3, 8), 6000, (0.2, 1.0, 0.45), 2.0)
    cam = Cam()
    cam.push(t0, t1, hp((0, -1, 0)), 8, 4.2, yaw=-12, pitch=-2, lens=48, yaw1=10, fstop=2.0, roll=3)
    cam.handheld(1.2)
    sfx(t0, "rise", 0.9)
    sfx(t0 + 0.9, "glitch", 0.5)


@S(65, 264, None, '"Lose control": hero terror, cut to black')
def s65(t0, t1):
    kitchen("creep")
    K = hero(t0, t1, "panic", loc=(-3, -4, 0))
    K.act(t0 + 0.4, "hands_head", expr="panic")
    Dd = dad(t0, t1, "grin", loc=(3.5, -2, 0), rot=15, fake=True)
    Dd.face(t0, eyes="normal", mouth="grin")
    cam = Cam()
    cam.push(t0, t1, hp((-1, -3, 0)), 12, 3.4, yaw=-12, pitch=2, lens=36, yaw1=6, fstop=2.4)
    cam.crash(t0 + 0.6, 36, 70, 0.12)
    cam.handheld(2.2)
    sfx(t0 + 0.6, "boom", 1.0)
    sfx(t0 + 0.6, "gasp", 0.8)
    sfx(t0 + 1.4, "zombie", 0.7)
