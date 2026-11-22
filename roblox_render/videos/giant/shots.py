"""giant: "Every night at 9 all the lights go out, because a giant sleeps under the town."
Narrator Eddie + Tooty find the lonely giant and turn the town's lights on. Shots keyed to script word indices."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from rbx.sets import wood, planks, checker_mat, set_obj_visible

V = Video(__file__)
story.bind(V)

GS = 10.0                       # giant scale
GIANT_Y = 150.0                 # giant seat in the cave (y)
CUT_FLOOR = -62.0               # cavern floor height in the cutaway
CUT_LOC = (0.0, 4.0, CUT_FLOOR)
CAVE_LOC = (0.0, GIANT_Y, 0.0)


def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def emitm(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


def fill(loc, target, energy=2500, color=(0.7, 0.8, 1.0), size=6.0):
    return light("fill", "AREA", loc, energy, color, size, target=target)


def lamp_energy(lt, t, e):
    lt.data.energy = e
    lt.data.keyframe_insert("energy", frame=F(t))


def pop_text(name, body, loc, t, size=1.0, col="#ffffff", yaw=0, dur=None, outline="#14141c"):
    root = empty(name, loc, rot=(0, 0, yaw))
    text(name + "_t", body, (0, 0, 0), size, emitm(col, 2.5), extrude=0.08 * size, parent=root)
    text(name + "_o", body, (0.04 * size, 0.06 * size, -0.05 * size), size, M(outline, 0.6), extrude=0.07 * size, parent=root)
    root.scale = (0.01,) * 3
    root.keyframe_insert("scale", frame=F(t - 0.04))
    root.scale = (1.3,) * 3
    root.keyframe_insert("scale", frame=F(t + 0.08))
    root.scale = (1.0,) * 3
    root.keyframe_insert("scale", frame=F(t + 0.17))
    if dur:
        root.keyframe_insert("scale", frame=F(t + dur - 0.1))
        root.scale = (0.01,) * 3
        root.keyframe_insert("scale", frame=F(t + dur))
    noise(root, "rotation_euler", 1, 0.05, 8)
    return root


# ================================================================== cast
def eddy(t0, t1, expr="neutral"):
    return story.eddie(t0, t1, expr)


def tooty(t0, t1, expr="grin"):
    T = chars.Char("Tooty", skin="#e8c39e", shirt="#ff8a3d", pants="#2f3f6a", hair="spiky", hair_color="#d99a1e",
                   face="kid", vneck="#ffc08a")
    return story._live(T, t0, t1, expr)


def dadc(t0, t1, expr="neutral"):
    D_ = chars.Char("Dad", skin="#efd9c0", shirt="#6aa0d8", pants="#3b3f4a", hair="short", hair_color="#5a4430",
                    face="mustache", extras=("glasses",), sleeves="long")
    return story._live(D_, t0, t1, expr)


def teachc(t0, t1, expr="neutral"):
    return story._live(chars.teacher(), t0, t1, expr)


def mayorc(t0, t1, expr="smug"):
    return story.mayor(t0, t1, expr)


def giant(t0, t1, expr="sleepy"):
    G = chars.Char("Giant", skin="#9db0d4", shirt="#3d4a78", pants="#3a3340", hair="bald", face="plain",
                   sleeves="long", vneck="#c8d4f0", extras=("beard:#e8eef8",), scale=GS)
    story._live(G, t0, t1, expr, 0.35)
    return G


def sit_floor(ch, t, loc, s=1.0, rot=0, **kw):
    x, y, z = loc
    ch.pose(t, loc=(x, y, z - 1.96 * s), rot=rot, legL=(85, 4), legR=(85, -4), armL=(25, 8), armR=(25, 8), **kw)


def giant_sleep(G, t, loc=CAVE_LOC, bow=26):
    sit_floor(G, t, loc, GS, rot=0, head=(0, bow, 4), torso=(0, 8, 0))
    G.pose(t, armL=(52, -4), armR=(52, -4))
    G.face(t, eyes="closed", mouth="wavy")


def giant_head(loc=CAVE_LOC):
    """World position of the giant's face centre when he sits at loc."""
    return (loc[0], loc[1] - 0.62 * GS, loc[2] + 2.64 * GS)


# ================================================================== props
def clock9(loc, coll=None, yaw=0, s=1.0):
    root = empty("clk", loc, coll=coll, rot=(0, 0, yaw))
    root.scale = (s,) * 3
    cyl("clk_b", 1.3, 0.25, (0, 0, 0), M("#f6f0e0", 0.5), 32, rot=(90, 0, 0), parent=root, coll=coll)
    cyl("clk_r", 1.42, 0.2, (0, 0.06, 0), M("#2a2a3a", 0.4), 32, rot=(90, 0, 0), parent=root, coll=coll)
    box("clk_h", (0.12, 0.05, 0.8), (-0.4, -0.16, 0), M("#1a1a1a"), 0.02, parent=root, coll=coll, rot=(0, 90, 0))
    box("clk_m", (0.08, 0.05, 1.1), (0, -0.18, 0.45), M("#1a1a1a"), 0.02, parent=root, coll=coll)
    text("clk_9", "9", (-0.95, -0.15, -0.15), 0.38, M("#1a1a1a"), extrude=0.01, parent=root, coll=coll)
    text("clk_12", "12", (0, -0.15, 0.8), 0.32, M("#1a1a1a"), extrude=0.01, parent=root, coll=coll)
    text("clk_3", "3", (0.95, -0.15, -0.15), 0.38, M("#1a1a1a"), extrude=0.01, parent=root, coll=coll)
    text("clk_6", "6", (0, -0.15, -0.95), 0.38, M("#1a1a1a"), extrude=0.01, parent=root, coll=coll)
    return root


def house(name, x, y, w, d, h, color, facing="-Y", coll=None, win_on=None, win_off=None, lit0=True, idx=0):
    """Box house + roof + door + two windows (on/off card pairs) on the street-facing side."""
    sgn = -1 if facing == "-Y" else 1
    box(name + "_b", (w, d, h), (x, y, h / 2), M(color, 0.75), 0.15, coll=coll)
    box(name + "_r", (w + 1.0, d + 1.0, 1.2), (x, y, h + 0.6), M(["#6b2e2a", "#3a4156", "#5a3a22"][idx % 3], 0.8), 0.2, coll=coll)
    box(name + "_ch", (1.2, 1.2, 2.4), (x + w * 0.3, y, h + 2.0), M("#4a4048", 0.8), 0.1, coll=coll)
    fy = y + sgn * (d / 2 + 0.02)
    box(name + "_d", (1.8, 0.2, 3.4), (x, fy + sgn * 0.05, 1.7), M("#3a2418", 0.7), 0.05, coll=coll)
    for k, dx in enumerate((-2.4, 2.4)):
        dz = h * 0.62
        on = card(f"{name}_won{k}", 1.9, 1.7, (x + dx, fy + sgn * 0.02, dz), emitm("#ffd27a", 5.0), facing, coll=coll)
        off = card(f"{name}_wof{k}", 1.9, 1.7, (x + dx, fy + sgn * 0.01, dz), M("#1b2540", 0.2), facing, coll=coll)
        win_on.append(on); win_off.append(off)
        set_obj_visible(on, 0.0, lit0); set_obj_visible(off, 0.0, not lit0)


def night_world(strength=1.5, moon=3.2):
    W.sky(strength, top=(0.004, 0.01, 0.06), bottom=(0.05, 0.1, 0.28))
    light("moon", "SUN", (0, 0, 50), moon, (0.55, 0.68, 1.0), 2, rot=(52, 0, 205))


def switch_all(won, wof, lps, t, on, cascade):
    """Cascade windows (left to right) and lamps on or off starting at t."""
    ordered = sorted(range(len(won)), key=lambda k: won[k].location.x)
    for j, k in enumerate(ordered):
        tt = t + j * cascade
        set_obj_visible(won[k], tt - 0.04, not on); set_obj_visible(won[k], tt, on)
        set_obj_visible(wof[k], tt - 0.04, on); set_obj_visible(wof[k], tt, not on)
    for j, (o, f, lt) in enumerate(lps):
        tt = t + j * cascade * 5
        set_obj_visible(o, tt - 0.04, not on); set_obj_visible(o, tt, on)
        set_obj_visible(f, tt - 0.04, on); set_obj_visible(f, tt, not on)
        lamp_energy(lt, tt - 0.04, 0 if on else 2200); lamp_energy(lt, tt, 2200 if on else 0)


def night_town(t0, t1, off_at=None, on_at=None, lit0=True, cascade=0.045, tower=True, moon=3.2, dusk=False):
    """Dark-blue night street along X (y in -5..5), houses both sides. Windows/lamps can switch off/on at a time."""
    if dusk:
        W.sky(1.2, top=(0.1, 0.12, 0.38), bottom=(1.0, 0.5, 0.25))
        light("sunset", "SUN", (0, 0, 50), 4.0, (1.0, 0.6, 0.35), 2, rot=(80, 0, 20))
    else:
        night_world(moon=moon)
    c = collection("NT")
    box("nt_ground", (320, 320, 0.4), (0, 0, -0.2), M("#1f3a2e", 0.95), 0, coll=c)
    box("nt_road", (320, 11, 0.08), (0, 0, 0.04), M("#2e3340", 0.7), 0, coll=c)
    for sy in (-1, 1):
        box(f"nt_walk{sy}", (320, 3, 0.14), (0, sy * 7, 0.07), M("#6c7080", 0.8), 0, coll=c)
    for i in range(-8, 9):
        box(f"nt_dash{i}", (3.0, 0.35, 0.02), (i * 8, 0, 0.1), M("#c8c8b8", 0.8), 0, coll=c)
    won, wof = [], []
    cols = ["#d9755f", "#e6c260", "#6fa0d8", "#9a8fd6", "#cfd6e0", "#84c08a", "#e58fb0"]
    xs = (-62, -48, -34, -20, -6, 8, 22, 36, 50, 64)
    for i, x in enumerate(xs):
        house(f"nh{i}", x, 20, 10, 8, 7 + (i * 3) % 4, cols[i % 7], "-Y", c, won, wof, lit0, idx=i)
        house(f"nb{i}", x + 6, -22, 10, 8, 7 + (i * 5) % 3, cols[(i + 3) % 7], "+Y", c, won, wof, lit0, idx=i + 1)
    rnd = random.Random(4)
    for i in range(14):
        sphere(f"nt_tree{i}", 2.4, (rnd.uniform(-70, 70), rnd.choice((12.5, -14.5)) + rnd.uniform(-1, 1), 3.2),
               M("#1d4a34", 0.9), (1, 1, 1.4), coll=c)
    if tower:
        box("nt_tw", (7, 7, 26), (0, 40, 13), M("#9a8f84", 0.8), 0.2, coll=c)
        box("nt_twr", (8, 8, 3), (0, 40, 27.5), M("#5a2e2a", 0.8), 0.2, coll=c)
        clock9((0, 36.4, 22), c, 0, 2.0)
        light("nt_tw_l", "SPOT", (0, 20, 25), 9000, (1.0, 0.9, 0.7), 1, coll=c, target=(0, 36, 22), spot=40)
    lps = []
    for x in (-34, -16, 2, 20, 38):
        box(f"lp_pole{x}", (0.35, 0.35, 8), (x, -6.8, 4), M("#232832", 0.5), 0.05, coll=c)
        on = sphere(f"lp_on{x}", 0.75, (x, -6.8, 8.3), emitm("#ffd88a", 9.0), coll=c, seg=12)
        off = sphere(f"lp_off{x}", 0.75, (x, -6.8, 8.3), M("#2b3040", 0.2), coll=c, seg=12)
        lt = light(f"lp_l{x}", "POINT", (x, -7.2, 8.0), 2200, (1.0, 0.8, 0.5), 1.5, coll=c)
        lps.append((on, off, lt))
        set_obj_visible(on, 0.0, lit0); set_obj_visible(off, 0.0, not lit0)
        lamp_energy(lt, 0.0, 2200 if lit0 else 0)
    if off_at is not None:
        switch_all(won, wof, lps, off_at, False, cascade)
    if on_at is not None:
        switch_all(won, wof, lps, on_at, True, cascade)
    return dict(won=won, wof=wof, lamps=lps, coll=c)


def dark_room(offs=None):
    """A cosy living room at night. offs = {lamp, tv, phone, candle: time it goes dark}."""
    offs = offs or {}
    world((0.05, 0.07, 0.16), 0.9)
    c = collection("DR")
    box("dr_floor", (60, 40, 0.4), (0, 8, -0.2), planks("dr_plank"), 0, coll=c)
    box("dr_back", (60, 0.5, 18), (0, 16, 9), M("#3b4a74", 0.85), 0, coll=c)
    box("dr_left", (0.5, 40, 18), (-22, 8, 9), M("#35426a", 0.85), 0, coll=c)
    light("dr_moon", "AREA", (-4, -4, 14), 2600, (0.5, 0.62, 1.0), 10, coll=c, target=(0, 8, 2))
    light("dr_fill", "AREA", (4, -10, 9), 1800, (0.55, 0.65, 1.0), 8, coll=c, target=(6, 4, 2))
    box("dr_tab", (6, 4, 0.4), (-11, 9, 4.2), wood("dr_wood", "#6e4229", "#a06a45", 2.0), 0.05, coll=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"dr_tl{sx}{sy}", (0.4, 0.4, 4.0), (-11 + sx * 2.5, 9 + sy * 1.4, 2.0), M("#5a3822"), 0.04, coll=c)
    cyl("dr_lbase", 0.5, 1.2, (-11, 9, 5.0), M("#c8a050", 0.3, metal=0.8), 16, coll=c)
    lon = cyl("dr_lshade_on", 1.1, 1.3, (-11, 9, 6.2), emitm("#ffd890", 6), 24, coll=c, r2=0.75)
    loff = cyl("dr_lshade_off", 1.1, 1.3, (-11, 9, 6.2), M("#8a806a", 0.6), 24, coll=c, r2=0.75)
    ll = light("dr_lamp_l", "POINT", (-11, 8, 6.0), 1400, (1.0, 0.8, 0.5), 1.0, coll=c)
    box("dr_stand", (8, 2.4, 2.4), (0, 12, 1.2), wood("dr_wood2", "#5a3822", "#7a4c2e", 2.0), 0.05, coll=c)
    box("dr_tv", (8.4, 0.5, 5.0), (0, 12.4, 5.2), M("#101014", 0.3), 0.1, coll=c)
    ton = card("dr_tvon", 7.8, 4.4, (0, 12.1, 5.2), img_mat("tv_show", os.path.join(W.TEX, "tv_show.png"), 0.3, emit=2.2), "+Y", coll=c)
    toff = card("dr_tvoff", 7.8, 4.4, (0, 12.12, 5.2), M("#07070a", 0.15), "+Y", coll=c)
    tl = light("dr_tv_l", "AREA", (0, 10, 5.2), 700, (0.6, 0.8, 1.0), 5, coll=c, target=(0, 0, 3))
    cyl("dr_pouf", 1.8, 1.6, (8, 4, 0.8), M("#a05040", 0.8), 24, coll=c)
    box("dr_phone", (1.5, 0.12, 2.8), (8, 3.2, 2.2), M("#18181c", 0.2), 0.12, coll=c, rot=(-60, 0, 0))
    pon = card("dr_phonescr", 1.3, 2.5, (8, 3.15, 2.21), emitm("#7fb0ff", 3.0), "-Y", coll=c)
    pon.rotation_euler = (math.radians(30), 0, 0)
    poff = card("dr_phonescr_off", 1.3, 2.5, (8, 3.16, 2.215), M("#08080c", 0.1), "-Y", coll=c)
    poff.rotation_euler = (math.radians(30), 0, 0)
    pl = light("dr_phone_l", "POINT", (8, 2.4, 3.4), 160, (0.6, 0.75, 1.0), 0.6, coll=c)
    box("dr_shelf", (4, 2.4, 0.3), (13, 8, 2.0), wood("dr_wood3", "#6e4229", "#a06a45", 2.0), 0.04, coll=c)
    cyl("dr_candle", 0.4, 1.6, (13, 8, 3.0), M("#f4ecd8", 0.6), 16, coll=c)
    fon = sphere("dr_flame", 0.32, (13, 8, 4.1), emitm("#ffb040", 9.0), (0.7, 0.7, 1.5), coll=c, seg=12)
    cl_ = light("dr_candle_l", "POINT", (13, 7.4, 4.2), 500, (1.0, 0.65, 0.3), 0.4, coll=c)
    box("dr_sofa", (10, 3.4, 2.8), (2, -4, 1.4), M("#5b3a6e", 0.8), 0.4, coll=c)
    box("dr_sofab", (10, 1.0, 3.6), (2, -2.4, 3.2), M("#5b3a6e", 0.8), 0.4, coll=c)
    for key, ons, offs_, lts in (("lamp", [lon], [loff], [(ll, 1400)]), ("tv", [ton], [toff], [(tl, 700)]),
                                 ("phone", [pon], [poff], [(pl, 160)]), ("candle", [fon], [], [(cl_, 500)])):
        t = offs.get(key)
        for o in ons:
            set_obj_visible(o, 0.0, True)
            if t is not None:
                set_obj_visible(o, t, False)
        for o in offs_:
            set_obj_visible(o, 0.0, False)
            if t is not None:
                set_obj_visible(o, t, True)
        for lt, e in lts:
            lamp_energy(lt, 0.0, e)
            if t is not None:
                lamp_energy(lt, t - 0.04, e); lamp_energy(lt, t, 0)
    return dict(lamp=(-11, 9, 6.2), tv=(0, 12, 5.2), phone=(8, 3.2, 2.2), candle=(13, 8, 4.1), coll=c)


def cutaway(lit=False):
    """Town on a grass slab; under it an open cavern where the giant sits (front, -Y, is open)."""
    if lit:
        W.sky(0.85, top=(0.01, 0.03, 0.14), bottom=(0.1, 0.18, 0.42))
    else:
        W.sky(0.7, top=(0.004, 0.01, 0.06), bottom=(0.05, 0.1, 0.28))
    light("moon", "SUN", (0, 0, 50), 1.5, (0.55, 0.68, 1.0), 2, rot=(55, 0, 205))
    c = collection("CUT")
    strata = checker_mat("cu_strata", "#3a2a30", "#2c2028", 0.25, 0.95)
    box("cu_grass", (200, 40, 0.8), (0, 5, -0.4), M("#2a5a3a", 0.9), 0.05, coll=c)
    box("cu_dirt", (200, 40, 9), (0, 5, -5.3), M("#5a3f36", 0.95), 0.05, coll=c)
    box("cu_back", (230, 2, 130), (0, 26, -48), strata, 0, coll=c)
    for sx in (-1, 1):
        box(f"cu_side{sx}", (2, 40, 130), (sx * 100, 5, -48), strata, 0, coll=c)
    box("cu_floor", (200, 40, 2), (0, 5, CUT_FLOOR - 1), M("#2a2030", 0.95), 0, coll=c)
    rnd = random.Random(9)
    won, wof = [], []
    for i, x in enumerate(range(-80, 81, 16)):
        house(f"ch{i}", x, 8, 9, 7, 7 + (i * 3) % 3, ["#d9755f", "#e6c260", "#6fa0d8", "#9a8fd6", "#cfd6e0", "#84c08a"][i % 6],
              "-Y", c, won, wof, lit, idx=i)
    for k in range(10):
        cyl(f"cu_stal{k}", rnd.uniform(1.5, 3.5), rnd.uniform(6, 14), (rnd.uniform(-60, 60), rnd.uniform(0, 20), -14),
            M("#4a3a46", 0.9), 8, coll=c, r2=0.2, rot=(180, 0, 0))
    for k in range(9):
        x = rnd.uniform(-70, 70)
        col = ["#6ad8ff", "#a878ff", "#ff7ac8"][k % 3]
        cyl(f"cu_cry{k}", 1.0, rnd.uniform(3, 7), (x, rnd.uniform(14, 22), CUT_FLOOR + 2.5), emitm(col, 6), 6, coll=c, r2=0.1)
        light(f"cu_cl{k}", "POINT", (x, 17, CUT_FLOOR + 8), 1800, hexc(col)[:3], 2, coll=c)
    light("cu_gl", "AREA", (0, -40, -30), 90000, (0.55, 0.65, 1.0), 40, coll=c, target=(0, 6, -45))
    return dict(coll=c, won=won, wof=wof)


def giant_cave():
    """Cave behind the tunnel (tunnel mouth at y=110), giant sitting at CAVE_LOC facing the tunnel."""
    world((0.04, 0.04, 0.09), 1.2)
    c = collection("GC")
    rock = checker_mat("gc_rock", "#3a3040", "#2a2230", 0.12, 0.95)
    box("gc_floor", (150, 130, 2), (0, 150, -1), M("#2c2433", 0.95), 0, coll=c)
    box("gc_back", (150, 2, 90), (0, 214, 40), rock, 0, coll=c)
    for sx in (-1, 1):
        box(f"gc_wall{sx}", (2, 130, 90), (sx * 74, 150, 40), rock, 0, coll=c)
    box("gc_ceil", (150, 130, 2), (0, 150, 85), rock, 0, coll=c)
    rnd = random.Random(21)
    for k in range(18):
        cyl(f"gc_stal{k}", rnd.uniform(2, 5), rnd.uniform(8, 22), (rnd.uniform(-60, 60), rnd.uniform(110, 205), 84),
            M("#3d3345", 0.9), 8, coll=c, r2=0.3, rot=(180, 0, 0))
    for k in range(10):
        cyl(f"gc_stag{k}", rnd.uniform(2, 4), rnd.uniform(5, 12), (rnd.uniform(-60, 60), rnd.uniform(115, 205), 3),
            M("#3d3345", 0.9), 8, coll=c, r2=0.3)
    for k in range(9):
        x = rnd.choice((-1, 1)) * rnd.uniform(22, 60)
        y = rnd.uniform(120, 200)
        col = ["#6ad8ff", "#a878ff", "#ff7ac8"][k % 3]
        cyl(f"gc_cry{k}", 1.4, rnd.uniform(5, 10), (x, y, 3), emitm(col, 6), 6, coll=c, r2=0.1)
        light(f"gc_cl{k}", "POINT", (x, y, 8), 2600, hexc(col)[:3], 2.5, coll=c)
    light("gc_top", "AREA", (0, 160, 80), 250000, (0.55, 0.65, 1.0), 60, coll=c, target=(0, 150, 0))
    light("gc_face", "AREA", (0, 100, 40), 150000, (0.7, 0.75, 1.0), 30, coll=c, target=(0, 146, 22))
    light("gc_floorfill", "AREA", (0, 100, 30), 80000, (0.6, 0.65, 1.0), 40, coll=c, target=(0, 100, 0))
    box("gc_fl", (68.6, 2, 90), (-39.7, 85.5, 40), rock, 0, coll=c)
    box("gc_fr", (68.6, 2, 90), (39.7, 85.5, 40), rock, 0, coll=c)
    box("gc_ft", (11, 2, 80), (0, 85.5, 49.5), rock, 0, coll=c)
    return dict(coll=c)


def tunnel(length=52, y0=34):
    """Timber-braced tunnel running +Y from y0, x in -5..5, height 9."""
    c = collection("TUN")
    rock = checker_mat("tun_rock", "#3a3340", "#2c2630", 0.4, 0.95)
    box("tn_floor", (10, length, 0.4), (0, y0 + length / 2, -0.2), M("#2a2430", 0.9), 0, coll=c)
    box("tn_ceil", (12, length, 0.6), (0, y0 + length / 2, 9.2), rock, 0, coll=c)
    for sx in (-1, 1):
        box(f"tn_wall{sx}", (0.8, length, 10), (sx * 5.4, y0 + length / 2, 4.6), rock, 0, coll=c)
    wd = M("#5a4026", 0.85)
    y = y0 + 3
    while y < y0 + length - 2:
        for sx in (-1, 1):
            box(f"tn_post{sx}{int(y)}", (0.5, 0.5, 9), (sx * 4.9, y, 4.5), wd, 0.04, coll=c)
        box(f"tn_beam{int(y)}", (10.4, 0.5, 0.5), (0, y, 9.0), wd, 0.04, coll=c)
        y += 6
    for k, y in enumerate(range(y0 + 12, y0 + length, 20)):
        sphere(f"tn_lant{k}", 0.35, (-4.6, y, 7.6), emitm("#ff9a4a", 5), coll=c, seg=8)
        light(f"tn_ll{k}", "POINT", (-4.4, y, 7.4), 160, (1.0, 0.6, 0.3), 0.5, coll=c)
    return dict(coll=c)


def flashlight(ch, t, energy=7000, spot=52, t_off=None):
    """Torch: body in the right hand + a spot light that follows the head. Clicks on at t."""
    sp = light(ch.name + "_fl", "SPOT", (0, -0.8, 0.1), 0, (1.0, 0.96, 0.82), 0.4, rot=(-90, 0, 0), spot=spot, blend=0.5)
    sp.parent = ch.head
    lamp_energy(sp, t - 0.04, 0)
    lamp_energy(sp, t, energy)
    if t_off is not None:
        lamp_energy(sp, t_off - 0.04, energy)
        lamp_energy(sp, t_off, 0)
    cyl(ch.name + "_torch", 0.28, 1.5, (-0.1, -0.9, -1.9), M("#303038", 0.4, metal=0.5), 12, rot=(90, 0, 0), parent=ch.shR, coll=ch.coll)
    cyl(ch.name + "_torchhd", 0.44, 0.5, (-0.1, -1.75, -1.9), emitm("#fff6d0", 10), 12, rot=(90, 0, 0), parent=ch.shR, coll=ch.coll)
    sfx(t, "u_click", 1.0)
    return sp


def zzz(loc, t, n=3, size=1.0, dz=2.0, col="#cfe0ff"):
    for i in range(n):
        tt = t + i * 0.45
        ob = text(f"zzz{int(t * 100)}_{i}", "Z", (loc[0], loc[1], loc[2]), size * (0.8 + 0.3 * i), emitm(col, 3.0), extrude=0.05)
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(tt))
        ob.keyframe_insert("location", frame=F(tt))
        ob.scale = (1,) * 3
        ob.keyframe_insert("scale", frame=F(tt + 0.25))
        ob.location = (loc[0] + 0.6 * size, loc[1], loc[2] + dz * size)
        ob.keyframe_insert("location", frame=F(tt + 1.1))
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(tt + 1.2))


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


def rings(loc, t, n=3, r1=6.0, gap=0.3, col="#9fc4ff", flat=False):
    """Expanding sound-wave rings (discs facing the camera at -Y, or flat on the floor)."""
    Mr = mat("ring_" + col, hexc(col), 0.3, emit=hexc(col), estr=3.0, alpha=0.5)
    for i in range(n):
        tt = t + i * gap
        ob = cyl(f"ring{int(t * 100)}_{i}", 1.0, 0.06, loc, Mr, 40, rot=(0, 0, 0) if flat else (90, 0, 0))
        a, b = (0, 1) if flat else (0, 2)
        sc = lambda k: (k, k, 1) if flat else (k, 1, k)
        ob.scale = sc(0.01)
        ob.keyframe_insert("scale", frame=F(tt))
        ob.scale = sc(r1)
        ob.keyframe_insert("scale", frame=F(tt + 0.7))
        ob.scale = sc(r1 * 1.1)
        ob.keyframe_insert("scale", frame=F(tt + 0.8))
        ob.scale = sc(0.01)
        ob.keyframe_insert("scale", frame=F(tt + 0.85))


def notes(loc, t, n=6, spread=4.0, dur=2.4, rise=12.0, seed=1, col="#ffe38a", size=1.0):
    """Floating music notes drifting up."""
    rnd = random.Random(seed)
    Mn = mat("note_" + col, hexc(col), 0.3, emit=hexc(col), estr=4.0)
    for i in range(n):
        root = empty(f"note{int(t * 100)}_{i}", (loc[0] + rnd.uniform(-spread, spread), loc[1], loc[2]))
        sphere(f"nh{int(t * 100)}_{i}", 0.45, (0, 0, 0), Mn, (1.2, 0.6, 0.8), parent=root, seg=10, rot=(0, 0, 20))
        box(f"ns{int(t * 100)}_{i}", (0.08, 0.08, 1.5), (0.42, 0, 0.75), Mn, 0.02, parent=root)
        box(f"nf{int(t * 100)}_{i}", (0.5, 0.08, 0.22), (0.66, 0, 1.45), Mn, 0.02, parent=root, rot=(0, 0, -25))
        tt = t + i * dur / (n + 1)
        root.scale = (0.01,) * 3
        root.keyframe_insert("scale", frame=F(tt))
        root.keyframe_insert("location", frame=F(tt))
        root.scale = (1.4 * size,) * 3
        root.keyframe_insert("scale", frame=F(tt + 0.3))
        root.location = (root.location[0] + rnd.uniform(-2, 2), root.location[1], root.location[2] + rise)
        root.keyframe_insert("location", frame=F(tt + dur))
        root.scale = (0.01,) * 3
        root.keyframe_insert("scale", frame=F(tt + dur))
        noise(root, "rotation_euler", 1, 0.3, 8)


def eye3d(loc, r=4.5):
    """Giant bloodshot eye on a skin wall."""
    skin = M("#8fa3c8", 0.55)
    sphere("eye_socket", r * 2.0, (loc[0], loc[1] + r * 1.3, loc[2]), skin, (1.5, 0.5, 1.1), seg=32)
    white = mat("eye_white", hexc("#f3dcd8"), 0.12, coat=1.0)
    ball = sphere("eye_ball", r, loc, white, seg=40)
    iris = cyl("eye_iris", r * 0.5, 0.2, (loc[0], loc[1] - r * 0.96, loc[2]), mat("eye_iris", hexc("#c4181c"), 0.2, coat=1.0), 40, rot=(90, 0, 0))
    cyl("eye_pupil", r * 0.22, 0.22, (loc[0], loc[1] - r * 0.98, loc[2]), M("#07050a", 0.1), 32, rot=(90, 0, 0))
    rnd = random.Random(3)
    Mv = M("#c83a3a", 0.4)
    for k in range(18):
        a = rnd.uniform(0, math.tau); rr = rnd.uniform(0.55, 0.95) * r
        box(f"eye_vein{k}", (0.08, 0.05, rnd.uniform(0.6, 1.8)), (loc[0] + math.cos(a) * rr, loc[1] - r * 0.9, loc[2] + math.sin(a) * rr),
            Mv, 0.01, rot=(0, math.degrees(a), 0))
    sphere("eye_hi", r * 0.14, (loc[0] - r * 0.3, loc[1] - r * 1.0, loc[2] + r * 0.3), emitm("#ffffff", 8), seg=12)
    top = box("eye_lid_top", (r * 2.6, r * 0.9, r * 1.1), (loc[0], loc[1] - r * 0.25, loc[2] + r * 1.05), skin, 0.5)
    bot = box("eye_lid_bot", (r * 2.6, r * 0.9, r * 0.7), (loc[0], loc[1] - r * 0.25, loc[2] - r * 1.0), skin, 0.5)
    return dict(ball=ball, top=top, bot=bot, loc=loc, r=r)


def tear(loc, t, n=1, dur=1.2, drop=7.0, size=0.6):
    Mt = mat("tear_m", hexc("#bfe3ff"), 0.05, emit=hexc("#8fc4ff"), estr=1.2, alpha=0.8, coat=1.0)
    for i in range(n):
        tt = t + i * 0.35
        ob = sphere(f"tear{int(t * 100)}_{i}", size, (loc[0] + i * 0.6, loc[1], loc[2]), Mt, (0.8, 0.8, 1.3), seg=12)
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(tt))
        ob.keyframe_insert("location", frame=F(tt))
        ob.scale = (1,) * 3
        ob.keyframe_insert("scale", frame=F(tt + 0.2))
        ob.location = (loc[0] + i * 0.6, loc[1], loc[2] - drop)
        ob.keyframe_insert("location", frame=F(tt + dur))
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(tt + dur + 0.05))


def crowd_look(t0, t1, n=5, center=(0, -2), spread=6, rot=180, expr="worried", seed=0):
    """A loose group of townies standing facing rot."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        k = townie(i + seed * 7, t0, t1, expr)
        k.pose(t0, loc=(center[0] + rnd.uniform(-spread, spread), center[1] + rnd.uniform(-2, 2), 0.0), rot=rot + rnd.uniform(-15, 15))
        out.append(k)
    return out


def puff(name, loc, t, r=1.4):
    ob = sphere(name, r, loc, mat("puff_white", (0.95, 0.95, 0.95), 0.9, emit=(0.6, 0.6, 0.6), estr=0.4), seg=16)
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t - 0.04))
    ob.scale = (1.2, 1.2, 0.8)
    ob.keyframe_insert("scale", frame=F(t + 0.18))
    ob.scale = (0.01,) * 3
    ob.keyframe_insert("scale", frame=F(t + 0.6))
    return ob


# ================================================================== SHOTS
# ---- 0:00  hook: the lit town, then 9:00, then the lights die
@S(1, 0, 3, "HOOK: fast crane over the warm lit night street, kids walking home")
def s01(t0, t1):
    A = night_town(t0, t1, lit0=True)
    for j, i in enumerate((1, 2, 3)):
        k = townie(i, t0, t1, "happy")
        k.walk(t0, t1, (-14 + j * 5, -2.5, 0), (-4 + j * 5, -2.5, 0), rate=2.6, face_dir=False)
        k.pose(t0, rot=90)
    cam = Cam()
    cam.key(t0, (-30, -26, 22), (-5, 0, 3), lens=22)
    cam.key(t1, (-12, -14, 4.5), (-2, 0, 3.2), lens=28, ease="EASE_OUT")
    cam.handheld(1.4)
    sfx(0.0, "crickets", 0.7, dur=6.0)
    sfx(0.05, "whoosh", 0.9)
    fill((-10, -16, 10), (-6, 0, 3), 3000, (1.0, 0.85, 0.6), 8)


@S(2, 3, 7, "clock tower hits 9")
def s02(t0, t1):
    night_town(t0, t1, lit0=True)
    cam = Cam()
    cam.push(t0, t1, (0, 36, 22), 34, 12, yaw=0, pitch=-3, lens=30, fstop=4.0)
    cam.crash(w(6) - 0.05, 30, 44, 0.1)
    cam.handheld(0.8)
    pop_text("t9", "9:00", (0, 30, 30), w(6) + 0.02, 3.0, "#ffe9a0", dur=1.0)
    sfx(w(6), "ding", 0.9)
    sfx(w(6) + 0.05, "boom", 0.6)
    sfx(t0, "whoosh", 0.7)


@S(3, 7, 12, "all the lights go out in a cascade")
def s03(t0, t1):
    off = w(10) + 0.05
    night_town(t0, t1, lit0=True, off_at=off, cascade=0.05)
    for j in range(3):
        k = townie(j + 2, t0, t1, "shock")
        k.pose(t0, loc=(-6 + j * 5, -2.5, 0), rot=180)
        k.act(off, "shock", expr="shock")
    cam = Cam()
    cam.key(t0, (-34, -12, 4.5), (0, 6, 5.5), lens=22)
    cam.key(t1, (-20, -14, 9.0), (0, 6, 5.0), lens=20, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    for j in range(8):
        sfx(off + j * 0.06, "click", 0.6)
    sfx(off, "u_click", 0.9)
    sfx(off + 0.1, "boom", 0.5)
    sfx(t0, "rise", 0.5)
    fill((-10, -16, 12), (0, 0, 3), 1500, (0.8, 0.85, 1.0), 8)


@S(4, 12, 14, "No lamps: street lamp dies")
def s04(t0, t1):
    off = w(13) + 0.12
    night_town(t0, t1, lit0=True, off_at=off, cascade=0.01)
    cam = Cam()
    cam.push(t0, t1, (2, -6.8, 8.0), 13, 6, yaw=-25, pitch=-14, lens=34, yaw1=-10, fstop=2.2)
    cam.handheld(1.0)
    sfx(off, "click", 1.0)
    sfx(t0, "whoosh", 0.5)


@S(5, 14, 16, "no TVs: the TV screen goes dark")
def s05(t0, t1):
    off = w(15) + 0.45
    R = dark_room({"tv": off})
    cam = Cam()
    cam.push(t0, t1, R["tv"], 22, 12, yaw=18, pitch=2, lens=32, yaw1=-8, fstop=3.0)
    cam.handheld(0.8)
    sfx(off, "pop", 0.9)
    sfx(off, "click", 0.7)
    sfx(t0, "whoosh", 0.5)


@S(6, 16, 18, "no phones: the phone screen goes dark")
def s06(t0, t1):
    off = w(17) + 0.12
    R = dark_room({"tv": 0.001, "lamp": 0.001, "phone": off})
    cam = Cam()
    cam.key(t0, (13, -3, 5.5), (8, 3.2, 2.2), lens=40, focus=(8, 3.2, 2.2), fstop=2.0)
    light("ph_fill", "AREA", (8, -6, 6), 3000, (0.6, 0.7, 1.0), 4, target=(8, 3, 2))
    cam.key(t1, (9.6, 0.6, 3.4), (8, 3.2, 2.2), lens=40, focus=(8, 3.2, 2.2), fstop=2.0, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(off, "click", 0.8)
    sfx(t0 + 0.05, "whoosh", 0.4)


@S(7, 18, 21, "not even candles: Eddie blows the candle out")
def s07(t0, t1):
    off = w(20) + 0.25
    R = dark_room({"tv": 0.001, "lamp": 0.001, "phone": 0.001, "candle": off})
    E = eddy(t0, t1, "shock")
    E.pose(t0, loc=(11.4, 10.5, 0), rot=0)
    E.act(w(19), "lean", expr="shock")
    E.face(off - 0.3, eyes="normal", mouth="o")
    E.face(off + 0.4, "worried")
    puff("candle_smoke", (13, 8, 4.8), off, 0.5)
    cam = Cam()
    cam.push(t0, t1, (12.4, 8, 4.2), 17, 8, yaw=-8, pitch=2, lens=34, yaw1=8, fstop=2.2)
    cam.handheld(0.9)
    sfx(off - 0.05, "whoosh", 0.5)
    sfx(off, "pop", 0.6)


# ---- 0:07  because deep under the town, a giant is sleeping
@S(8, 21, 26, "descend through the ground: the town above, then the cavern")
def s08(t0, t1):
    cutaway(lit=False)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    cam = Cam()
    cam.key(t0, (0, -75, 12), (0, 6, 2), lens=30)
    cam.key(w(24), (0, -80, -10), (0, 6, -14), lens=30, ease="EASE_IN_OUT")
    cam.key(t1, (0, -100, -48), (0, 6, -44), lens=28, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0, "wind", 0.6)
    sfx(t0 + 0.1, "rise", 0.6)
    sfx(w(24), "whoosh", 0.6)


@S(9, 26, 28, "a giant: wide reveal of the sitting giant under the tiny town")
def s09(t0, t1):
    cutaway(lit=False)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    cam = Cam()
    cam.key(t0, (-30, -90, -46), (0, 6, -40), lens=26)
    cam.key(t1, (30, -76, -34), (0, 6, -38), lens=24, ease="EASE_OUT")
    cam.crash(t0 + 0.05, 26, 20, 0.12)
    cam.handheld(1.0)
    sfx(t0, "boom", 0.9)
    sfx(t0 + 0.02, "u_movie", 0.55)
    sfx(t0 + 0.3, "rise", 0.5)


@S(10, 28, 30, "is sleeping: close on the giant's face, zzz, breathing")
def s10(t0, t1):
    cutaway(lit=False)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    G.pose(t1, head=(0, 22, 4))
    fz = giant_head(CUT_LOC)
    zzz((fz[0] + 8, fz[1] - 4, fz[2] + 8), t0 + 0.1, 3, 3.0, 5.0)
    cam = Cam()
    cam.push(t0, t1, fz, 60, 34, yaw=-18, pitch=4, lens=40, yaw1=8, fstop=4.0)
    cam.handheld(0.7)
    sfx(t0, "snore", 0.9)
    sfx(t0 + 0.9, "snore", 0.8)


@S(11, 30, 34, "if he wakes up: giant stirs, ground rumbles, town above shakes")
def s11(t0, t1):
    C = cutaway(lit=False)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    G.pose(w(32), head=(0, 10, -6), torso=(0, 2, 0))
    G.face(w(32), eyes="half", mouth="ah")
    G.pose(t1, head=(0, 0, 6))
    for ob in list(C["coll"].objects):
        if ob.name.startswith(("ch", "cu_grass", "cu_dirt")):
            for ax in (0, 2):
                noise(ob, "location", ax, 0.5, 2.5)
    cam = Cam()
    cam.key(t0, (0, -70, -14), (0, 6, -30), lens=24)
    cam.key(t1, (0, -52, -34), (0, 6, -38), lens=24, ease="EASE_IN_OUT")
    cam.crash(w(32), 24, 32, 0.1)
    cam.handheld(1.8)
    sfx(w(31), "boom", 0.8)
    sfx(w(32), "rise", 0.6)
    sfx(w(33), "boom", 0.6)


@S(12, 34, 38, "the town wakes up: the whole street trembles")
def s12(t0, t1):
    A = night_town(t0, t1, lit0=False)
    ks = crowd_look(t0, t1, 6, (0, -3), 12, 0, "shock", seed=2)
    for k in ks:
        k.act(t0 + 0.1, "hands_head", expr="scream")
        noise(k.root, "location", 2, 0.3, 3)
    for ob in list(A["coll"].objects):
        if ob.name.startswith(("nh", "nb")) and ob.parent is None:
            noise(ob, "rotation_euler", 1, 0.03, 3)
    cam = Cam()
    cam.push(t0, t1, (0, 0, 4), 14, 8, yaw=0, pitch=2, lens=22, yaw1=20, fstop=3.5)
    cam.handheld(2.6)
    sfx(t0, "boom", 0.8)
    sfx(t0 + 0.1, "gasp", 0.7)
    fill((-8, -16, 9), (0, 0, 3), 3000, (0.7, 0.8, 1.0), 8)


@S(13, 38, 41, "inside his stomach: pink cavern, the tiny town and panicking kids")
def s13(t0, t1):
    world((0.25, 0.04, 0.08), 0.5)
    c = collection("ST")
    pink = checker_mat("st_pink", "#c8506a", "#a63a58", 0.2, 0.35)
    box("st_floor", (160, 160, 2), (0, 30, -1), pink, 0, coll=c)
    box("st_back", (160, 2, 80), (0, 80, 38), pink, 0, coll=c)
    for sx in (-1, 1):
        box(f"st_w{sx}", (2, 160, 80), (sx * 70, 30, 38), pink, 0, coll=c)
    box("st_ceil", (160, 160, 2), (0, 30, 78), pink, 0, coll=c)
    acid = mat("st_acid", hexc("#7ae04a"), 0.1, emit=hexc("#5fd03a"), estr=1.5, coat=1.0)
    box("st_pool", (90, 40, 0.5), (0, 40, 0.25), acid, 0.1, coll=c)
    won, wof = [], []
    for i, x in enumerate((-30, -14, 2, 18)):
        house(f"sh{i}", x, 26, 9, 7, 8, ["#d9755f", "#e6c260", "#6fa0d8", "#84c08a"][i], "-Y", c, won, wof, True, idx=i)
    rnd = random.Random(5)
    for k in range(14):
        b = sphere(f"st_bub{k}", rnd.uniform(0.6, 1.6), (rnd.uniform(-30, 30), rnd.uniform(34, 50), 1),
                   mat("bub", (0.8, 1, 0.7), 0.1, emit=(0.5, 0.9, 0.4), estr=0.8, alpha=0.5), coll=c, seg=12)
        b.keyframe_insert("location", frame=F(t0))
        b.location = (b.location[0], b.location[1], rnd.uniform(8, 18))
        b.keyframe_insert("location", frame=F(t1))
    light("st_l", "AREA", (0, -10, 40), 60000, (1.0, 0.5, 0.6), 30, coll=c, target=(0, 30, 4))
    E = eddy(t0, t1, "terror")
    T = tooty(t0, t1, "scream")
    E.pose(t0, loc=(-4, 6, 0), rot=0, armL=(150, 30), armR=(150, 30))
    T.pose(t0, loc=(3, 6, 0), rot=0, armL=(150, 30), armR=(150, 30))
    E.panic(t0, t1, 6.0)
    T.panic(t0, t1, 6.0)
    cam = Cam()
    cam.push(t0, t1, (0, 20, 6), 30, 16, yaw=-15, pitch=6, lens=24, yaw1=15, fstop=3.0)
    cam.handheld(1.6)
    sfx(t0, "splat", 0.7)
    sfx(t0 + 0.2, "rise", 0.6)
    sfx(w(40), "boom", 0.7)


# ---- 0:13  the town's habits
def street_pair(t0, t1, ia=1, ib=2):
    a = townie(ia, t0, t1, "worried")
    b = townie(ib, t0, t1, "worried")
    a.pose(t0, loc=(-1.7, -2, 0), rot=90)
    b.pose(t0, loc=(1.7, -2, 0), rot=-90)
    return a, b


@S(14, 41, 43, "Everyone whispers: a pair whispering into ears, SHHH")
def s14(t0, t1):
    night_town(t0, t1, lit0=False)
    a, b = street_pair(t0, t1)
    a.act(t0 + 0.05, "phone", expr="worried")
    a.pose(t0 + 0.2, torso=(0, 12, 0), head=(-14, 0, 0))
    b.pose(t0 + 0.2, head=(14, 0, 0), torso=(0, 6, 0))
    b.face(t0 + 0.3, eyes="side_l", mouth="flat")
    pop_text("sh1", "SHHH", (0, -4, 9.5), t0 + 0.35, 1.4, "#cfe0ff", dur=0.8)
    cam = Cam()
    cam.push(t0, t1, (0, -2, 4.6), 11, 6, yaw=-14, pitch=3, lens=34, yaw1=10, fstop=2.2)
    cam.handheld(1.0)
    fill((-6, -12, 8), (0, -2, 3), 2500, (0.7, 0.8, 1.0), 6)
    sfx(t0 + 0.2, "shh", 0.9)
    sfx(t0 + 0.05, "whoosh", 0.4)


@S(15, 43, 46, "We walk on tiptoes: a line of kids creeping away from the camera")
def s15(t0, t1):
    night_town(t0, t1, lit0=False)
    for j in range(3):
        k = townie(j + 3, t0, t1, "worried")
        k.walk(t0, t1, (-8 + j * 2.6, -4 - j * 2.2, 0), (-1.5 + j * 2.6, 3 - j * 2.2, 0), rate=1.7, swing=14, arm=6, bob=0.2)
        k.pose(t0 + 0.05, armL=(0, 40), armR=(0, 40))
    cam = Cam()
    cam.key(t0, (-4, -14, 3.0), (-3, 2, 3.4), lens=30)
    cam.key(t1, (-1, -12, 5.0), (-1, 4, 3.2), lens=26, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    fill((-6, -12, 8), (-2, 0, 3), 2600, (0.7, 0.8, 1.0), 6)
    sfx(t0, "footsteps", 0.35, dur=1.0)


@S(16, 46, 47, "tiptoes: low close-up of feet creeping")
def s16(t0, t1):
    night_town(t0, t1, lit0=False)
    k = townie(4, t0, t1, "worried")
    k.walk(t0, t1 + 0.4, (-2.5, -4, 0), (2.5, -4, 0), rate=2.2, swing=18, arm=4, bob=0.25, face_dir=False)
    k.pose(t0, rot=90)
    cam = Cam()
    cam.push(t0, t1, (0, -4, 1.2), 11, 8, yaw=-12, pitch=2, lens=40, yaw1=8, fstop=2.0)
    cam.handheld(0.7)
    fill((-3, -9, 5), (0, -4, 1), 2000, (0.7, 0.8, 1.0), 4)
    sfx(t0, "footsteps", 0.45, dur=0.9)


def dog_socks(d, color="#e8423a"):
    """Tiny stripy socks on the four legs of W.dog."""
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"{d.name}_sock{sx}{sy}", (0.45, 0.45, 0.5), (sx * 0.4, sy * 0.8, 0.26), M("#f4f4f4", 0.8), 0.06, parent=d)
            box(f"{d.name}_sockb{sx}{sy}", (0.47, 0.47, 0.14), (sx * 0.4, sy * 0.8, 0.42), M(color, 0.8), 0.03, parent=d)


@S(17, 47, 49, "Dogs wear: three dogs tiptoeing past")
def s17(t0, t1):
    night_town(t0, t1, lit0=False)
    for j, col in enumerate(("#c98a4a", "#e8e0d0", "#6a5a4a")):
        d = W.dog(f"dog{j}", (-8 + j * 4.5, -4 - j * 1.2, 0), color=col)
        dog_socks(d)
        d.rotation_euler[2] = math.radians(-90)
        d.keyframe_insert("rotation_euler", index=2, frame=F(t0))
        d.keyframe_insert("location", frame=F(t0))
        d.location = (d.location[0] + 7, d.location[1], 0)
        d.keyframe_insert("location", frame=F(t1))
        noise(d, "location", 2, 0.12, 3)
    cam = Cam()
    cam.key(t0, (-9, -12, 2.4), (0, -4, 1.8), lens=32)
    cam.key(t1, (-2, -11, 2.0), (3, -4, 1.6), lens=32, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    fill((-4, -10, 7), (0, -4, 1), 2500, (0.7, 0.8, 1.0), 6)
    sfx(t0, "u_duck", 0.5)
    sfx(t0 + 0.2, "u_duck", 0.4)


@S(18, 49, 51, "tiny socks: close-up of a dog's sock, squeak")
def s18(t0, t1):
    night_town(t0, t1, lit0=False)
    d = W.dog("dogA", (0, -4, 0), color="#c98a4a")
    dog_socks(d, "#e8423a")
    d.rotation_euler[2] = math.radians(-90)
    d.keyframe_insert("rotation_euler", index=2, frame=F(t0))
    d.keyframe_insert("location", frame=F(t0))
    d.location = (2.0, -4, 0)
    d.keyframe_insert("location", frame=F(t1))
    pop_text("sq", "squeak!", (0.5, -6, 2.6), t0 + 0.3, 0.8, "#ffe9a0", dur=0.7)
    cam = Cam()
    cam.push(t0, t1, (0.6, -4.0, 0.6), 4.6, 3.2, yaw=-50, pitch=6, lens=36, yaw1=-30, fstop=2.0)
    cam.handheld(0.6)
    fill((-3, -9, 5), (0, -4, 1), 2200, (0.8, 0.85, 1.0), 4)
    sfx(t0 + 0.1, "u_duck", 0.9)
    sfx(t0 + 0.6, "u_duck", 0.8)
    sfx(t0 + 1.05, "u_duck", 0.8)


def sign_hands(ch, t0, t1, seed=0, rate=4.0):
    """Teacher signing: arms jump between random hand shapes."""
    rnd = random.Random(seed)
    t = t0
    while t < t1:
        ch.pose(t, armL=(rnd.uniform(60, 130), rnd.uniform(-30, 30)), armR=(rnd.uniform(60, 130), rnd.uniform(-30, 30)),
                head=(rnd.uniform(-10, 10), rnd.uniform(-4, 8), rnd.uniform(-5, 5)))
        t += 1.0 / rate


def sunset_scene(t0, t1, sun_z=(14, -8)):
    A = night_town(t0, t1, lit0=True, dusk=True, tower=False)
    sun = sphere("sunball", 16, (0, 270, sun_z[0]), emitm("#ff9a3a", 8.0), seg=24)
    sun.keyframe_insert("location", frame=F(t0))
    sun.location = (0, 270, sun_z[1])
    sun.keyframe_insert("location", frame=F(t1))
    return A


@S(19, 51, 55, "Our teacher speaks only: teacher, kids sitting at sunset")
def s19(t0, t1):
    sunset_scene(t0, t1)
    T = teachc(t0, t1, "smile")
    T.pose(t0, loc=(0, 2, 0), rot=0)
    sign_hands(T, t0 + 0.2, t1, seed=3)
    for j in range(3):
        k = townie(j + 1, t0, t1, "happy")
        sit_floor(k, t0, (-3.5 + j * 3.5, -3, 0), 1.0, 180)
        k.pose(t0 + 0.5, head=(0, 4, 3 * (-1) ** j))
    cam = Cam()
    cam.push(t0, t1, (0, 0, 4.2), 13, 8, yaw=182, pitch=4, lens=30, yaw1=170, fstop=2.8)
    cam.handheld(0.9)
    sfx(t0, "whoosh", 0.4)
    sfx(t0 + 0.4, "crickets", 0.4, dur=2.0)


@S(20, 55, 58, "in sign language: close on the hands")
def s20(t0, t1):
    sunset_scene(t0, t1)
    T = teachc(t0, t1, "smile")
    T.pose(t0, loc=(0, 2, 0), rot=0)
    sign_hands(T, t0, t1, seed=8, rate=5.5)
    cam = Cam()
    cam.push(t0, t1, (0, 2, 3.6), 7, 4.2, yaw=-12, pitch=0, lens=36, yaw1=10, fstop=2.4)
    cam.handheld(1.0)
    sfx(t0, "pop", 0.35)
    sfx(t0 + 0.35, "pop", 0.3)


@S(21, 58, 60, "after sunset: the sun drops below the horizon")
def s21(t0, t1):
    sunset_scene(t0, t1, (6, -22))
    for j in range(3):
        k = townie(j + 1, t0, t1, "relief")
        sit_floor(k, t0, (-3.5 + j * 3.5, -4, 0), 1.0, 180)
    cam = Cam()
    cam.key(t0, (0, -9, 3.0), (0, 200, 14), lens=24)
    cam.key(t1, (0, -12, 3.5), (0, 200, 10), lens=20, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0, "rise", 0.45)
    sfx(t1 - 0.3, "crickets", 0.5, dur=2.0)


@S(22, 60, 65, "My dad sneezed once at night: wind-up and CHOO")
def s22(t0, t1):
    night_town(t0, t1, lit0=False)
    D_ = dadc(t0, t1, "worried")
    D_.pose(t0, loc=(0, -2, 0), rot=0)
    tch = w(65) - 0.03
    W2.sneeze(D_, w(62), tch)
    E = eddy(t0, t1, "worried")
    E.pose(t0, loc=(-4.5, -3, 0), rot=-25)
    E.act(w(62), "shrug", expr="worried")
    cam = Cam()
    cam.push(t0, t1, (0, -2, 4.4), 12, 6, yaw=-8, pitch=2, lens=30, yaw1=10, fstop=2.4)
    cam.crash(tch, 30, 46, 0.1)
    cam.handheld(1.2)
    fill((-6, -12, 8), (0, -2, 3), 2600, (0.7, 0.8, 1.0), 6)
    sfx(tch, "sneeze", 1.0)
    pop_text("ach", "ACHOO!", (0, -5, 8.5), tch + 0.02, 1.4, "#ffe9a0", dur=0.9)


@S(23, 65, 70, "night, and the whole street: everybody freezes and looks")
def s23(t0, t1):
    night_town(t0, t1, lit0=False)
    ks = crowd_look(t0, t1, 7, (-1, -2), 14, 0, "terror", seed=4)
    for k in ks:
        k.act(t0 + 0.04, "recoil", expr="terror")
        k.look(t0 + 0.3, 40, 0)
    cam = Cam()
    cam.key(t0, (-30, -13, 4.5), (0, 0, 4.0), lens=22)
    cam.key(t1, (-12, -14, 5.5), (-2, 0, 4.0), lens=26, ease="EASE_OUT")
    cam.handheld(2.0)
    fill((-12, -14, 9), (0, 0, 3), 3000, (0.7, 0.8, 1.0), 8)
    sfx(t0, "boom", 0.6)
    sfx(t0 + 0.1, "gasp", 0.7)


def table(name, x, y, c=None):
    Mt = wood("tb_wood", "#8a5634", "#c48a58", 2.0)
    box(name + "_top", (6.4, 3.8, 0.4), (x, y, 4.2), Mt, 0.05, coll=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"{name}_l{sx}{sy}", (0.4, 0.4, 4.0), (x + sx * 2.8, y + sy * 1.5, 2.0), Mt, 0.04, coll=c)
    box(name + "_cloth", (6.8, 4.2, 0.12), (x, y, 4.45), M("#d9453a", 0.8), 0.03, coll=c)


TBL = [(-14, -3), (-4, -6), (6, -3), (15, -6), (-9, 3), (11, 3)]


@S(24, 70, 73, "hid under tables: everyone dives under street tables")
def s24(t0, t1):
    night_town(t0, t1, lit0=False)
    for i, (x, y) in enumerate(TBL):
        table(f"tb{i}", x, y)
        k = townie(i, t0, t1, "terror")
        k.pose(t0, loc=(x + 6, y - 2, 0), rot=-60)
        td = t0 + 0.12 + i * 0.1
        k.pose(td - 0.01, loc=(x + 6, y - 2, 0), rot=-60)
        sit_floor(k, td + 0.25, (x, y, 0), 1.0, 0)
        k.act(td + 0.25, "hands_head", expr="terror")
    cam = Cam()
    cam.key(t0, (-16, -14, 6.0), (0, -2, 3.0), lens=24)
    cam.key(t1, (6, -12, 4.5), (0, -2, 3.0), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.8)
    fill((-6, -12, 10), (0, -2, 3), 3500, (0.7, 0.8, 1.0), 8)
    for i in range(6):
        sfx(t0 + 0.2 + i * 0.1, "thud", 0.45)
    sfx(t0, "whoosh", 0.6)


def clock_spin(loc, t0, t1, turns=3.0, s=1.0, hours=0.25):
    root = empty("clkp", loc)
    root.scale = (s,) * 3
    cyl("clkp_b", 1.3, 0.25, (0, 0, 0), M("#f6f0e0", 0.5), 32, rot=(90, 0, 0), parent=root)
    cyl("clkp_r", 1.42, 0.2, (0, 0.06, 0), M("#2a2a3a", 0.4), 32, rot=(90, 0, 0), parent=root)
    mh = empty("clkp_mh", (0, -0.17, 0), parent=root)
    box("clkp_m", (0.09, 0.05, 1.05), (0, 0, 0.5), M("#1a1a1a"), 0.02, parent=mh)
    hh = empty("clkp_hh", (0, -0.15, 0), parent=root)
    box("clkp_h", (0.13, 0.05, 0.7), (0, 0, 0.33), M("#1a1a1a"), 0.02, parent=hh)
    for p, a1 in ((mh, turns * 360.0), (hh, hours * 360.0 * turns)):
        p.rotation_euler = (0, 0, 0)
        p.keyframe_insert("rotation_euler", frame=F(t0))
        p.rotation_euler = (0, math.radians(-a1), 0)
        p.keyframe_insert("rotation_euler", frame=F(t1))
        set_interp(p, "rotation_euler", F(t0), "LINEAR")
        set_interp(p, "rotation_euler", F(t1), "LINEAR")
    return root


@S(25, 73, 76, "for an hour: clock spins, everyone still under the tables")
def s25(t0, t1):
    night_town(t0, t1, lit0=False, tower=False)
    for i, (x, y) in enumerate(TBL):
        table(f"tb{i}", x, y)
        k = townie(i, t0, t1, "terror")
        sit_floor(k, t0, (x, y, 0), 1.0, 0)
        k.pose(t0, armL=(155, 30), armR=(155, 30))
        if i % 2:
            k.face(t0 + 0.4, "sleepy"); k.face(t0 + 0.9, "bored")
    ck = clock_spin((-2, 4, 12), t0, t1, 3.0, 1.8)
    pop_text("hr", "1 HOUR", (4, -2, 17), t0 + 0.15, 1.8, "#ffe9a0", dur=0.9)
    cam = Cam()
    cam.key(t0, (-8, -15, 10.5), (-1, 2, 7.0), lens=28)
    cam.key(t1, (2, -13, 6.5), (0, 0, 5.5), lens=22, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    fill((-6, -12, 10), (0, -2, 5), 3500, (0.7, 0.8, 1.0), 8)
    sfx(t0, "rise", 0.5)
    sfx(t0, "crickets", 0.4, dur=1.1)


# ---- 0:24  Tooty
@S(26, 76, 80, "My best friend Tooty: he skids in and strikes a pose")
def s26(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "grin")
    T.walk(t0, w(78), (-12, -3, 0), (0, -3, 0), rate=3.4, swing=40, arm=40, bob=0.3, face_dir=False)
    T.pose(t0, rot=90)
    T.pose(w(78), rot=0)
    T.act(w(79) - 0.05, "point", expr="grin")
    T.jump(w(79) + 0.2, 1.4, 0.4)
    pop_text("tooty", "TOOTY", (0, -5.5, 9.5), w(79) + 0.1, 1.9, "#ffb040", dur=1.2)
    cam = Cam()
    cam.key(t0, (-14, -12, 2.2), (-8, -3, 3), lens=28)
    cam.key(w(78), (-3, -10, 3.2), (0, -3, 4), lens=30, ease="EASE_IN_OUT")
    cam.key(t1, (0, -9, 4.2), (0, -3, 4.4), lens=34, ease="EASE_OUT")
    cam.handheld(1.2)
    fill((-6, -12, 8), (0, -3, 3), 3200, (1.0, 0.9, 0.8), 8)
    sfx(t0, "whoosh", 0.6)
    sfx(w(78), "stomp", 0.5)
    sfx(w(79) + 0.1, "pop", 0.8)
    sfx(w(79) + 0.1, "sparkle", 0.6)


@S(27, 80, 83, "is the loudest: Tooty SHOUTS, sound rings, windows shake")
def s27(t0, t1):
    A = night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "shout")
    T.pose(t0, loc=(0, -3, 0), rot=0)
    T.act(t0 + 0.1, "cheer", expr="shout")
    T.talk(t0, t1, words=V.span(t0, t1), open_m="talk_wide", wide_m="scream", rest="scream")
    for ob in list(A["coll"].objects):
        if ob.name.startswith(("nh", "nb")) and ob.parent is None:
            noise(ob, "rotation_euler", 1, 0.015, 2)
    cam = Cam()
    cam.push(t0, t1, (0, -3, 4.6), 10, 4.2, yaw=0, pitch=2, lens=26, yaw1=6, fstop=2.4)
    cam.crash(t0 + 0.1, 26, 38, 0.1)
    cam.handheld(2.2)
    fill((-5, -11, 8), (0, -3, 3), 3000, (1.0, 0.9, 0.8), 6)
    sfx(t0 + 0.05, "gasp", 0.5)
    sfx(t0 + 0.1, "u_quack", 0.7)
    sfx(t0 + 0.1, "boom", 0.5)


@S(28, 83, 86, "kid in town: neighbours cover their ears")
def s28(t0, t1):
    night_town(t0, t1, lit0=False)
    ks = crowd_look(t0, t1, 5, (0, -2), 7, 0, "scream", seed=6)
    for k in ks:
        k.pose(t0, armL=(165, -10), armR=(165, -10))
        noise(k.root, "location", 0, 0.2, 3)
    T = tooty(t0, t1, "shout")
    T.pose(t0, loc=(0, -8, 0), rot=180)
    T.act(t0 + 0.1, "cheer", expr="shout")
    cam = Cam()
    cam.key(t0, (6, 6, 3.0), (0, -4, 4.5), lens=24)
    cam.key(t1, (3, 5, 4.5), (0, -4, 4.5), lens=20, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    fill((0, 8, 9), (0, -4, 3), 3500, (0.8, 0.85, 1.0), 8)
    sfx(t0, "gasp", 0.4)


def grounded_sign(loc, t, c=None):
    root = empty("gsign", loc)
    box("gs_b", (7.0, 0.4, 2.4), (0, 0, 0), M("#e8d4a0", 0.8), 0.1)
    text("gs_t", "GROUNDED", (0, -0.28, 0), 0.95, M("#c8261e", 0.5), extrude=0.05, parent=root)
    for sx in (-1, 1):
        box(f"gs_p{sx}", (0.3, 0.3, 4.0), (sx * 2.9, 0.2, -3.0), M("#5a3822"), 0.03, parent=root)
    return root


@S(29, 86, 88, "He's grounded: GROUNDED sign slams down, Tooty slumps")
def s29(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "grin")
    T.pose(t0, loc=(0, -2, 0), rot=0)
    T.act(w(87), "slump", expr="worried")
    gs = grounded_sign((0, -1.0, 12.0), t0)
    gs.scale = (0.55,) * 3
    gs.keyframe_insert("location", frame=F(t0 + 0.1))
    gs.location = (0, -3.4, 9.0)
    gs.keyframe_insert("location", frame=F(t0 + 0.28))
    cam = Cam()
    cam.push(t0, t1, (0, -2, 6), 11, 7, yaw=-10, pitch=0, lens=30, yaw1=8, fstop=2.4)
    cam.handheld(1.4)
    cam.crash(t0 + 0.28, 30, 42, 0.1)
    fill((-5, -11, 9), (0, -2, 4), 3200, (0.8, 0.85, 1.0), 8)
    sfx(t0 + 0.28, "u_slap", 0.8)
    sfx(t0 + 0.28, "thud", 0.7)


@S(30, 88, 91, "every night: Tooty sits bored on the step while the moon crosses the sky")
def s30(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "bored")
    sit_floor(T, t0, (0, -3, 0), 1.0, 0)
    T.pose(t0, armL=(60, 8), armR=(60, 8), head=(0, 6, 0))
    moon = sphere("moonball", 6, (-30, 90, 55), emitm("#e8f0ff", 5), seg=24)
    moon.keyframe_insert("location", frame=F(t0))
    moon.location = (30, 90, 55)
    moon.keyframe_insert("location", frame=F(t1))
    gs = grounded_sign((6, -1.0, 8.0), t0)
    cam = Cam()
    cam.key(t0, (-9, -11, 2.8), (0, -3, 3.4), lens=28)
    cam.key(t1, (5, -12, 3.6), (0, -3, 3.4), lens=24, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    fill((-5, -11, 9), (0, -3, 3), 3000, (0.8, 0.85, 1.0), 8)
    sfx(t0, "crickets", 0.5, dur=2.8)


@S(31, 91, 93, "with a pillow: a pillow flies in and smacks him")
def s31(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "shout")
    T.pose(t0, loc=(0, -2, 0), rot=0)
    T.act(t0 + 0.05, "cheer", expr="shout")
    pil = box("pillow", (2.6, 1.0, 1.9), (-10, -5, 5), M("#ffffff", 0.9), 0.4)
    pil.keyframe_insert("location", frame=F(t0 + 0.15))
    pil.location = (0, -3.0, 4.2)
    pil.keyframe_insert("location", frame=F(t0 + 0.45))
    pil.keyframe_insert("rotation_euler", frame=F(t0 + 0.15))
    pil.rotation_euler = (0.4, 0.2, 1.5)
    pil.keyframe_insert("rotation_euler", frame=F(t0 + 0.45))
    T.act(t0 + 0.45, "recoil", expr="shock")
    cam = Cam()
    cam.push(t0, t1, (0, -2.5, 4.4), 9, 5, yaw=14, pitch=2, lens=32, yaw1=-8, fstop=2.2)
    cam.handheld(1.2)
    fill((-5, -11, 8), (0, -2, 3), 3000, (1.0, 0.9, 0.8), 6)
    sfx(t0 + 0.12, "whoosh", 0.7)
    sfx(t0 + 0.45, "u_slap", 0.9)


@S(32, 93, 96, "in his mouth: close-up, pillow stuffed in, puffed cheeks")
def s32(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "terror")
    T.pose(t0, loc=(0, -2, 0), rot=0)
    box("pillowm", (2.4, 1.0, 1.0), (0, -0.78, -0.28), M("#ffffff", 0.9), 0.35, parent=T.head, coll=T.coll)
    noise(T.head, "rotation_euler", 1, 0.06, 3)
    T.face(t0 + 0.2, eyes="wide", mouth="flat")
    cam = Cam()
    cam.push(t0, t1, (0, -2.6, 4.7), 5, 3, yaw=-10, pitch=2, lens=44, yaw1=8, fstop=2.0)
    cam.handheld(1.0)
    fill((-4, -9, 8), (0, -2, 4), 2600, (1.0, 0.9, 0.8), 5)
    sfx(t0 + 0.05, "pop", 0.6)


def pillow_on(T):
    box("pillowm", (2.4, 1.0, 1.0), (0, -0.78, -0.28), M("#ffffff", 0.9), 0.35, parent=T.head, coll=T.coll)


@S(33, 96, 99, "Rock and roll: Tooty jumps and rocks out, pillow in mouth")
def s33(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "shout")
    T.pose(t0, loc=(0, -3, 0), rot=0)
    pillow_on(T)
    T.act(t0 + 0.05, "cheer", expr="shout")
    T.jump(t0 + 0.2, 1.8, 0.45)
    T.jump(t0 + 0.75, 1.8, 0.45)
    pop_text("mm1", "MMMPH!", (0, -5, 9.0), t0 + 0.2, 1.6, "#ffb040", dur=0.6)
    cam = Cam()
    cam.key(t0, (-5, -10, 2.0), (0, -3, 4.5), lens=24)
    cam.key(t1, (4, -10, 3.0), (0, -3, 5.0), lens=24, ease="EASE_IN_OUT")
    cam.handheld(2.0)
    fill((-5, -11, 8), (0, -3, 3), 3200, (1.0, 0.9, 0.8), 8)
    sfx(t0 + 0.2, "boing", 0.6)
    sfx(t0 + 0.75, "boing", 0.6)
    sfx(t0 + 0.1, "snort", 0.5)


@S(34, 99, 102, "We're losing control: wild rocking, orbit, crash zoom")
def s34(t0, t1):
    night_town(t0, t1, lit0=False)
    T = tooty(t0, t1, "shout")
    T.pose(t0, loc=(0, -3, 0), rot=0)
    pillow_on(T)
    t = t0
    k = 0
    while t < t1:
        s = 1 if k % 2 == 0 else -1
        T.pose(t, head=(18 * s, -10 + 12 * s, 14 * s), torso=(0, 6 * s, 6 * s), armL=(120 + 30 * s, 40), armR=(120 - 30 * s, 40))
        t += 0.14
        k += 1
    pop_text("mm2", "MMMPH!!", (0, -5, 9.0), t0 + 0.9, 1.7, "#ffb040", dur=0.7)
    cam = Cam()
    cam.orbit(t0, t1, (0, -3, 4.6), 9, -50, 50, pitch=4, lens=28, steps=5, fstop=2.8)
    cam.crash(w(101), 28, 44, 0.1)
    cam.handheld(1.8)
    fill((-5, -11, 8), (0, -3, 3), 3200, (1.0, 0.9, 0.8), 8)
    sfx(t0 + 0.05, "u_faaah", 0.6)
    sfx(w(101), "boom", 0.5)


def podium_scene(t0, t1):
    A = night_town(t0, t1, lit0=False, tower=False)
    c = A["coll"]
    box("stage", (14, 7, 1.6), (0, 4, 0.8), M("#6a4a30", 0.8), 0.1, coll=c)
    box("podium", (3, 2, 3.2), (0, 4.5, 3.2), M("#8a5a34", 0.7), 0.1, coll=c)
    box("banner", (16, 0.4, 5), (0, 8.2, 8.5), M("#2c3a6a", 0.8), 0.1, coll=c)
    text("banner_t", "SHHH!", (0, 8.0, 8.5), 2.2, emitm("#ffe9a0", 2.0), extrude=0.06, coll=c)
    return A


@S(35, 102, 106, "Mayor Popp says: the mayor on his stage, finger to lips")
def s35(t0, t1):
    podium_scene(t0, t1)
    Mr = mayorc(t0, t1, "smug")
    Mr.pose(t0, loc=(0, 6, 1.6), rot=0)
    Mr.act(t0 + 0.2, "point", expr="smug")
    lips(Mr, t0 + 0.1, t1 - 0.2)
    cam = Cam()
    cam.push(t0, t1, (0, 6, 6.0), 14, 8, yaw=-12, pitch=-2, lens=30, yaw1=10, fstop=2.6)
    cam.handheld(1.0)
    fill((-6, -8, 9), (0, 6, 4), 3600, (1.0, 0.9, 0.7), 8)
    sfx(t0, "whoosh", 0.5)
    sfx(t0 + 0.1, "chat", 0.35)


@S(36, 106, 110, "the giant has slept: a crayon poster of the giant")
def s36(t0, t1):
    A = podium_scene(t0, t1)
    c = A["coll"]
    root = empty("poster", (0, 7.8, 8.0))
    box("poster_b", (7.5, 0.3, 8.0), (0, 0, 0), M("#f2ead2", 0.9), 0.1, parent=root)
    box("pg_head", (2.6, 0.2, 2.6), (0, -0.2, 2.0), M("#9db0d4", 0.8), 0.1, parent=root)
    box("pg_body", (3.4, 0.2, 3.2), (0, -0.2, -0.5), M("#3d4a78", 0.8), 0.1, parent=root)
    box("pg_legs", (3.4, 0.2, 1.6), (0, -0.2, -2.9), M("#3a3340", 0.8), 0.1, parent=root)
    text("pg_z", "ZZZ", (2.2, -0.35, 3.4), 1.0, M("#2a4a9a", 0.5), extrude=0.03, parent=root)
    Mr = mayorc(t0, t1, "smug")
    Mr.pose(t0, loc=(-3.6, 5.5, 1.6), rot=0)
    Mr.act(t0 + 0.1, "point_l", expr="smug")
    lips(Mr, t0 + 0.1, t1 - 0.2)
    cam = Cam()
    cam.push(t0, t1, (0, 7, 7), 14, 9, yaw=6, pitch=-2, lens=30, yaw1=-8, fstop=2.8)
    cam.handheld(1.0)
    fill((-6, -8, 9), (0, 6, 5), 3600, (1.0, 0.9, 0.7), 8)
    sfx(t0 + 0.1, "paper", 0.7)
    sfx(t0, "whoosh", 0.4)


@S(37, 110, 113, "a thousand years: 1000 YEARS slams in over the mayor")
def s37(t0, t1):
    podium_scene(t0, t1)
    Mr = mayorc(t0, t1, "smug")
    Mr.pose(t0, loc=(0, 6, 1.6), rot=0)
    Mr.act(t0 + 0.1, "cheer", expr="smug")
    pop_text("ky", "1000 YEARS", (0, 3.4, 8.4), w(111) + 0.05, 1.7, "#ffe9a0", dur=1.0)
    cam = Cam()
    cam.key(t0, (-6, -4, 3.5), (0, 6, 6), lens=22)
    cam.key(t1, (4, -3, 5.5), (0, 6, 6.5), lens=20, ease="EASE_IN_OUT")
    cam.crash(w(111) + 0.03, 22, 14, 0.12)
    cam.handheld(1.4)
    fill((-6, -8, 9), (0, 6, 4), 3600, (1.0, 0.9, 0.7), 8)
    sfx(w(111) + 0.05, "boom", 0.8)
    sfx(w(111) + 0.05, "gasp", 0.4)


@S(38, 113, 116, "and we must: townsfolk nod along")
def s38(t0, t1):
    podium_scene(t0, t1)
    ks = crowd_look(t0, t1, 7, (0, -4), 9, 180, "worried", seed=3)
    for k in ks:
        k.nod(t0 + 0.05, 3, 10, 6.0)
    Mr = mayorc(t0, t1, "smug")
    Mr.pose(t0, loc=(0, 6, 1.6), rot=0)
    Mr.act(t0 + 0.1, "point", expr="smug")
    lips(Mr, t0, t1)
    cam = Cam()
    cam.key(t0, (-8, -14, 3.0), (0, 0, 4.5), lens=26)
    cam.key(t1, (5, -13, 4.0), (0, 2, 5), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    fill((-8, -12, 10), (0, 0, 4), 3600, (1.0, 0.9, 0.8), 8)
    sfx(t0, "chat", 0.35)


@S(39, 116, 119, "never ask why: Eddie raises a hand, the mayor glares")
def s39(t0, t1):
    podium_scene(t0, t1)
    E = eddy(t0, t1, "worried")
    E.pose(t0, loc=(2, -3, 0), rot=180)
    E.act(t0 + 0.1, "wave", expr="worried")
    E.act(w(118), "recoil", expr="shock")
    Mr = mayorc(t0, t1, "angry")
    Mr.pose(t0, loc=(0, 6, 1.6), rot=0)
    Mr.act(w(118) - 0.1, "point", expr="furious")
    pop_text("nn", "NO!", (0, 3.0, 9.5), w(118) + 0.05, 2.6, "#ff5a4a", dur=0.9)
    cam = Cam()
    cam.key(t0, (4, -6, 3.0), (0, 4, 5.4), lens=26)
    cam.key(t1, (3, -8, 4.5), (0, 5, 5.6), lens=32, ease="EASE_IN_OUT")
    cam.crash(w(118), 32, 20, 0.1)
    cam.handheld(1.4)
    fill((-6, -8, 9), (0, 4, 4), 3600, (1.0, 0.9, 0.7), 8)
    sfx(w(118) + 0.03, "buzzer", 0.8)
    sfx(w(118) + 0.03, "boom", 0.5)


# ---- 0:36  the sound under the bed
def bedroom_night():
    world((0.05, 0.07, 0.18), 0.8)
    A = sets.bedroom(night=True)
    light("br_fill2", "AREA", (4, -12, 9), 1600, (0.55, 0.65, 1.0), 8, target=(-6, 4, 3))
    return A


BED = (-7.6, 5.25)


def lie_in_bed(E, t=0.0, yaw=0):
    E.pose(t, loc=(BED[0], 3.7, 3.15), rot=yaw)
    E.root.rotation_euler[0] = math.radians(-90)
    E.root.keyframe_insert("rotation_euler", index=0, frame=1)
    E.pose(t, legL=(2, 4), legR=(2, -4), armL=(5, 8), armR=(5, 8))
    return E


@S(40, 119, 123, "But I hear something: Eddie lying awake, head turns, ear")
def s40(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "worried")
    lie_in_bed(E, t0)
    E.pose(t0 + 0.2, head=(35, 0, 0))
    E.look(w(121), 35, -8)
    E.face(w(121), eyes="side_r", mouth="o")
    cam = Cam()
    cam.push(t0, t1, (BED[0], 8.2, 3.9), 9, 5, yaw=20, pitch=40, lens=34, yaw1=-8, pitch1=55, fstop=2.2)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "crickets", 0.3, dur=1.0)
    sfx(w(121), "pop", 0.4)


@S(41, 123, 127, "Every night, right under: wide room, camera sinks toward the bed")
def s41(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "worried")
    lie_in_bed(E, t0)
    E.look(t0 + 0.4, 30, 0)
    cam = Cam()
    cam.key(t0, (7, -10, 8.5), (-6, 4, 3.5), lens=26)
    cam.key(t1, (1, -9, 3.0), (-6.5, 4, 2.0), lens=24, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "wind", 0.35)
    sfx(t0 + 0.1, "whoosh", 0.4)


@S(42, 127, 129, "my bed: floor-level, blue glow pulses from under the bed")
def s42(t0, t1):
    bedroom_night()
    glow = sphere("underglow", 2.6, (BED[0], 3.5, 0.35), emitm("#7fb0ff", 4.0), (1.4, 2.2, 0.35), seg=16)
    light("ug_l", "POINT", (BED[0], 1.5, 0.4), 800, (0.5, 0.7, 1.0), 1.0)
    rings((BED[0], 2.5, 0.12), t0 + 0.05, 3, 7.0, 0.22, "#9fc4ff", flat=True)
    cam = Cam()
    cam.key(t0, (-1, -8, 0.5), (BED[0], 3, 0.6), lens=26)
    cam.key(t1, (-4.5, -4, 0.35), (BED[0], 3, 0.55), lens=22, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "hum", 0.7)


@S(43, 129, 132, "a soft sound: sound rings around Eddie's pillow")
def s43(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "worried")
    lie_in_bed(E, t0)
    E.pose(t0 + 0.1, head=(40, 0, 6))
    E.face(t0 + 0.1, eyes="side_r", mouth="o")
    rings((BED[0], 5, 2.5), t0 + 0.1, 3, 4.5, 0.3, "#9fc4ff", flat=True)
    cam = Cam()
    cam.push(t0, t1, (BED[0], 7.4, 3.7), 7, 4.2, yaw=-30, pitch=28, lens=40, yaw1=-8, fstop=2.0)
    cam.handheld(0.8)
    sfx(t0, "hum", 0.8)
    sfx(t0 + 0.2, "sparkle", 0.3)


@S(44, 132, 134, "Not snoring: ZZZ crossed out")
def s44(t0, t1):
    bedroom_night()
    pop_text("zz", "ZZZ", (BED[0], 3, 6.5), t0 + 0.05, 2.0, "#cfe0ff", yaw=-18)
    x1 = box("xbar1", (5.2, 0.2, 0.5), (BED[0], 2.6, 6.5), emitm("#ff4a4a", 5), 0.05, rot=(0, -38, -18))
    x2 = box("xbar2", (5.2, 0.2, 0.5), (BED[0], 2.6, 6.5), emitm("#ff4a4a", 5), 0.05, rot=(0, 38, -18))
    for xb in (x1, x2):
        xb.scale = (0.01,) * 3
        xb.keyframe_insert("scale", frame=F(t0 + 0.5))
        xb.scale = (1, 1, 1)
        xb.keyframe_insert("scale", frame=F(t0 + 0.62))
    cam = Cam()
    cam.push(t0, t1, (BED[0], 3, 6.5), 12, 8, yaw=-14, pitch=4, lens=30, yaw1=6, fstop=3.0)
    cam.crash(t0 + 0.5, 30, 40, 0.1)
    cam.handheld(1.0)
    sfx(t0 + 0.05, "snore", 0.6)
    sfx(t0 + 0.55, "buzzer", 0.6)


@S(45, 134, 135, "Crying: close on Eddie's face, a tear")
def s45(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "cry")
    lie_in_bed(E, t0)
    E.pose(t0, head=(30, 0, 0))
    E.face(t0, eyes="worried", mouth="frown")
    tear((BED[0] - 0.9, 7.6, 4.0), t0 + 0.3, 1, 0.8, 0.6, 0.18)
    cam = Cam()
    cam.push(t0, t1, (BED[0], 8.4, 4.0), 5.5, 3.2, yaw=-26, pitch=52, lens=44, yaw1=-14, fstop=1.8)
    cam.handheld(0.8)
    sfx(t0 + 0.05, "cry", 0.8)
    sfx(t0 + 0.4, "drip", 0.5)


@S(46, 135, 137, "Last week: Eddie pulls the pillow over his head")
def s46(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "shock")
    lie_in_bed(E, t0)
    E.act(t0 + 0.1, "hands_face", expr="shock")
    pil = box("pillowx", (3.2, 1.2, 2.6), (BED[0] + 4.5, 7.5, 3.8), M("#f7f8fb", 0.8), 0.4)
    pil.keyframe_insert("location", frame=F(t0 + 0.1))
    pil.location = (BED[0], 7.9, 4.3)
    pil.keyframe_insert("location", frame=F(t0 + 0.4))
    cam = Cam()
    cam.key(t0, (-1, -2, 9), (BED[0], 6, 3.5), lens=28)
    cam.key(t1, (-3, 0, 6.5), (BED[0], 6.5, 3.8), lens=30, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0 + 0.38, "thud", 0.6)
    sfx(t0, "whoosh", 0.4)


@S(47, 137, 142, "I couldn't take it anymore: sits up, throws the blanket off")
def s47(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "determined")
    E.pose(t0, loc=(BED[0], 7.0, 2.6 - 1.96), rot=0, legL=(85, 4), legR=(85, -4), armL=(25, 8), armR=(25, 8))
    E.act(w(139), "fists", expr="determined")
    E.look(w(140), 0, -4)
    cam = Cam()
    cam.key(t0, (6, -8, 6.5), (BED[0], 5, 4.2), lens=26)
    cam.key(t1, (-1, -8, 5.0), (BED[0], 6, 4.4), lens=34, ease="EASE_IN_OUT")
    cam.crash(w(140), 34, 46, 0.12)
    cam.handheld(1.2)
    sfx(t0 + 0.3, "whoosh", 0.7)
    sfx(w(140), "rise", 0.5)


@S(48, 142, 146, "I took my flashlight: hand grabs the torch from the nightstand, click")
def s48(t0, t1):
    bedroom_night()
    E = eddy(t0, t1, "determined")
    E.pose(t0, loc=(-3.2 - 2.8, 5.0, 0), rot=180)
    E.act(t0 + 0.2, "reach", expr="determined")
    flashlight(E, w(144) + 0.1, 6000, 50)
    cam = Cam()
    cam.push(t0, t1, (-4.2, 8.4, 4.2), 7, 4.4, yaw=-18, pitch=8, lens=36, yaw1=10, fstop=2.0)
    cam.handheld(1.1)
    sfx(t0 + 0.1, "whoosh", 0.4)


def cellar_set():
    world((0.05, 0.06, 0.12), 1.0)
    c = collection("CEL")
    stone = checker_mat("cel_stone", "#5a5560", "#46414d", 0.18, 0.9)
    box("cl_floor", (16, 44, 0.4), (0, 12, -0.2), stone, 0, coll=c)
    box("cl_back", (16, 0.6, 18), (0, 34.3, 8), stone, 0, coll=c)
    for sx in (-1, 1):
        box(f"cl_wall{sx}", (0.6, 60, 18), (sx * 8.3, 8, 8), stone, 0, coll=c)
    box("cl_ceil", (17, 60, 0.6), (0, 8, 16.3), stone, 0, coll=c)
    n = 14
    for i in range(n):
        top = 9.5 - (i + 1) * (9.5 / n)
        box(f"cl_st{i}", (16, 1.14, max(top, 0.05)), (0, -8 + (i + 0.5) * 1.14, max(top, 0.05) / 2), M("#6a5a46", 0.85), 0.04, coll=c)
    box("cl_land", (16, 8, 9.5), (0, -12, 4.75), M("#6a5a46", 0.85), 0.04, coll=c)
    jar_cols = ["#d9453a", "#e6c260", "#6fa0d8", "#84c08a", "#c88ad8"]
    for k in range(4):
        box(f"cl_shelf{k}", (1.2, 8, 0.3), (-7.4, 16 + (k % 2) * 0 , 3 + k * 2.2), M("#5a3822", 0.8), 0.03, coll=c)
    for k in range(4):
        for j in range(6):
            cyl(f"cl_jar{k}{j}", 0.38, 0.9, (-7.4, 12.6 + j * 1.2, 3.6 + k * 2.2), mat("jar" + str((k + j) % 5), hexc(jar_cols[(k + j) % 5]), 0.2, alpha=0.8), 12, coll=c)
    for k in range(3):
        box(f"cl_crate{k}", (3, 3, 3), (6.0 - k * 1.2, 22 + k * 3.5, 1.5), M("#7a5a36", 0.85), 0.1, coll=c)
    light("cel_amb", "AREA", (0, 12, 15), 60000, (0.55, 0.6, 1.0), 20, coll=c, target=(0, 12, 0))
    # rusty door
    rust = checker_mat("rust", "#7a3e22", "#5a2c18", 7.0, 0.9)
    box("cl_dfl", (1.0, 1.4, 11), (-5.4, 33.6, 5.5), stone, 0.04, coll=c)
    box("cl_dfr", (1.0, 1.4, 11), (5.4, 33.6, 5.5), stone, 0.04, coll=c)
    box("cl_dft", (11.8, 1.4, 1.2), (0, 33.6, 10.9), stone, 0.04, coll=c)
    piv = empty("door_piv", (-4.8, 33.2, 0), coll=c)
    box("cl_door", (9.6, 0.6, 10.2), (4.8, 0, 5.1), rust, 0.06, parent=piv, coll=c)
    for z in (2, 5, 8):
        box(f"cl_band{z}", (9.7, 0.7, 0.4), (4.8, -0.05, z), M("#2a2420", 0.5, metal=0.6), 0.04, parent=piv, coll=c)
    sphere("cl_knob", 0.5, (8.9, -0.6, 5.0), M("#c8a050", 0.3, metal=0.9), parent=piv, coll=c, seg=12)
    return dict(door=piv, coll=c)


@S(49, 146, 149, "and sneaked down: Eddie tiptoes down the stairs, torch beam")
def s49(t0, t1):
    cellar_set()
    E = eddy(t0, t1, "worried")
    E.walk(t0, t1, (0, -6.0, 8.5), (0, 0.5, 4.5), rate=1.9, swing=18, arm=6, bob=0.2)
    E.pose(t0, rot=180)
    E.pose(t0, armR=(80, 8))
    flashlight(E, t0 + 0.02, 6500, 55)
    cam = Cam()
    cam.key(t0, (-5, -11, 13.5), (0, -4, 7.5), lens=26)
    cam.key(t1, (-5, -5, 10.0), (0, 1, 4.6), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "footsteps", 0.45, dur=1.0)


@S(50, 149, 153, "to the old cellar: cellar wide reveal, beam sweeps jars")
def s50(t0, t1):
    cellar_set()
    E = eddy(t0, t1, "worried")
    E.walk(t0, t1, (0, 8.0, 0), (1.5, 18, 0), rate=1.9, swing=18, arm=6, bob=0.2)
    E.pose(t0, armR=(80, 8))
    flashlight(E, t0 + 0.02, 6500, 55)
    cam = Cam()
    cam.key(t0, (6, 4, 4.0), (-2, 18, 4.0), lens=22)
    cam.key(t1, (3, 10, 6.5), (-1, 26, 4.0), lens=22, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "wind", 0.4)
    sfx(t0 + 0.1, "footsteps", 0.35, dur=1.0)


@S(51, 153, 157, "Behind a rusty door: push-in on the rusty door, Eddie's torch")
def s51(t0, t1):
    C = cellar_set()
    E = eddy(t0, t1, "worried")
    E.pose(t0, loc=(0, 24, 0), rot=180, armR=(80, 8))
    flashlight(E, t0 + 0.02, 7000, 50)
    cam = Cam()
    cam.push(t0, t1, (0, 33.2, 5.5), 18, 8, yaw=8, pitch=4, lens=30, yaw1=-8, fstop=3.0)
    cam.crash(t0 + 0.3, 30, 38, 0.1)
    cam.handheld(1.0)
    sfx(t0 + 0.05, "whoosh", 0.5)
    sfx(t0 + 0.6, "door", 0.4)


@S(52, 157, 160, "a tunnel went: the door swings open on darkness")
def s52(t0, t1):
    C = cellar_set()
    tunnel()
    E = eddy(t0, t1, "shock")
    E.pose(t0, loc=(0, 26, 0), rot=180, armR=(80, 8))
    flashlight(E, 0.5, 7000, 50)
    p = C["door"]
    p.keyframe_insert("rotation_euler", index=2, frame=F(t0 + 0.15))
    p.rotation_euler[2] = math.radians(105)
    p.keyframe_insert("rotation_euler", index=2, frame=F(t0 + 0.8))
    cam = Cam()
    cam.key(t0, (-6, 20, 5.0), (0, 34, 5), lens=26)
    cam.key(t1, (-1, 28, 5.0), (0, 40, 4.5), lens=24, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0 + 0.15, "door", 0.8, 0.9)
    sfx(t0 + 0.4, "rise", 0.5)


@S(53, 160, 163, "deeper and deeper: fast track down the tunnel")
def s53(t0, t1):
    tunnel()
    world((0.05, 0.05, 0.1), 1.0)
    light("tn_amb", "AREA", (0, 60, 9), 40000, (0.5, 0.5, 1.0), 20, target=(0, 60, 0))
    E = eddy(t0, t1, "worried")
    E.walk(t0, t1, (0, 40, 0), (0, 68, 0), rate=2.2, swing=20, arm=8, bob=0.2, face_dir=False)
    E.pose(t0, rot=180, armR=(80, 8))
    flashlight(E, 0.02, 7500, 55)
    cam = Cam()
    cam.key(t0, (0, 26, 5.2), (0, 70, 4.5), lens=18)
    cam.key(t1, (0, 55, 5.0), (0, 110, 4.5), lens=16, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0, "wind", 0.5)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 0.3, "footsteps", 0.35, dur=1.0)


def tunnel_pair(t0, t1, purple=False, y=60):
    tunnel()
    world((0.05, 0.05, 0.1), 1.0)
    light("tn_amb", "AREA", (0, y, 9), 40000, (0.5, 0.5, 1.0), 20, target=(0, y, 0))
    E = eddy(t0, t1, "worried")
    E.pose(t0, loc=(-1.6, y + 3, 0), rot=180, armR=(80, 8))
    flashlight(E, 0.02, 6000, 55)
    T = tooty(t0, t1, "worried")
    T.pose(t0, loc=(2.0, y, 0), rot=180)
    return E, T


@S(54, 163, 166, "Tooty followed me: Tooty creeping behind Eddie")
def s54(t0, t1):
    E, T = tunnel_pair(t0, t1)
    T.walk(t0, t1, (2.0, 58, 0), (1.4, 63, 0), rate=2.0, swing=16, arm=5, bob=0.2, face_dir=False)
    T.pose(t0, rot=180)
    cam = Cam()
    cam.key(t0, (-3, 50, 4.4), (1, 64, 4.4), lens=28)
    cam.key(t1, (4, 52, 5.0), (0, 64, 4.4), lens=28, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0, "footsteps", 0.4, dur=1.0)


@S(55, 166, 171, "holding his breath so hard: Tooty close-up, cheeks puffing, eyes bulging")
def s55(t0, t1):
    E, T = tunnel_pair(t0, t1)
    T.pose(t0, loc=(0.5, 56, 0), rot=0)
    T.face(t0, eyes="wide", mouth="o")
    T.pose(t0 + 0.2, head=(0, -4, 0))
    T.face(w(169), eyes="terror", mouth="grimace_wide")
    T.face(w(170) + 0.1, eyes="terror", mouth="flat")
    noise(T.head, "rotation_euler", 1, 0.05, 2)
    cam = Cam()
    cam.push(t0, t1, (0.5, 56, 4.8), 8, 3.6, yaw=-8, pitch=2, lens=40, yaw1=10, fstop=2.0)
    cam.crash(w(170), 40, 52, 0.1)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "gasp", 0.5)
    sfx(w(169), "rise", 0.5)


@S(56, 171, 175, "his face turned purple: skin colour shifts, shaking")
def s56(t0, t1):
    E, T = tunnel_pair(t0, t1)
    T.pose(t0, loc=(0.5, 56, 0), rot=0)
    T.face(t0, eyes="terror", mouth="flat")
    skin = T.face_mat.node_tree.nodes["Skin"].outputs[0]
    skin.default_value = (*hexc("#e8c39e"), 1)
    skin.keyframe_insert("default_value", frame=F(t0))
    skin.default_value = (*hexc("#8a3ad0"), 1)
    skin.keyframe_insert("default_value", frame=F(w(174)))
    noise(T.head, "rotation_euler", 1, 0.08, 2)
    noise(T.head, "rotation_euler", 2, 0.06, 2)
    pop_text("pu", "PURPLE", (0.5, 52, 8.5), w(174), 1.2, "#c88af0", dur=0.7)
    cam = Cam()
    cam.push(t0, t1, (0.5, 56, 4.8), 4.4, 2.8, yaw=8, pitch=2, lens=44, yaw1=-8, fstop=2.0)
    cam.handheld(1.4)
    sfx(t0 + 0.3, "rise", 0.5)
    sfx(w(174), "boing", 0.7)


@S(57, 175, 181, "At the end of the tunnel: they near the mouth, red glow ahead")
def s57(t0, t1):
    giant_cave()
    tunnel()
    light("tn_amb", "AREA", (0, 60, 9), 40000, (0.5, 0.5, 1.0), 20, target=(0, 60, 0))
    E = eddy(t0, t1, "worried")
    E.walk(t0, t1, (-1.6, 62, 0), (-1.6, 80, 0), rate=1.9, swing=18, arm=6, bob=0.2, face_dir=False)
    E.pose(t0, rot=180, armR=(80, 8))
    flashlight(E, 0.02, 6500, 55)
    T = tooty(t0, t1, "worried")
    T.walk(t0, t1, (2.0, 59, 0), (2.0, 77, 0), rate=1.9, swing=16, arm=5, bob=0.2, face_dir=False)
    T.pose(t0, rot=180)
    red = light("endglow", "POINT", (0, 100, 8), 30000, (1.0, 0.2, 0.15), 3, target=None)
    cam = Cam()
    cam.key(t0, (0, 48, 4.4), (0, 80, 4.5), lens=22)
    cam.key(t1, (0, 66, 4.4), (0, 108, 6.0), lens=18, ease="EASE_IN")
    cam.handheld(1.1)
    sfx(t0, "footsteps", 0.35, dur=2.4)
    sfx(t0 + 0.2, "rise", 0.5)


def eye_set():
    giant_cave()
    tunnel()
    E3 = eye3d((0, 128, 17), 6.0)
    return E3


def eye_lids(E3, closed_until, open_at, open_dur=0.45):
    r = E3["r"]; z0 = E3["loc"][2]
    top, bot = E3["top"], E3["bot"]
    top.location[2] = z0 + 0.55 * r
    bot.location[2] = z0 - 0.35 * r
    top.keyframe_insert("location", index=2, frame=F(closed_until))
    bot.keyframe_insert("location", index=2, frame=F(closed_until))
    top.location[2] = z0 + 1.35 * r
    bot.location[2] = z0 - 1.25 * r
    top.keyframe_insert("location", index=2, frame=F(open_at + open_dur))
    bot.keyframe_insert("location", index=2, frame=F(open_at + open_dur))


@S(58, 181, 185, "there was an eye: the eye opens in the dark, crash zoom")
def s58(t0, t1):
    E3 = eye_set()
    eye_lids(E3, t0 + 0.2, w(183) + 0.15)
    E = eddy(t0, t1, "terror")
    E.pose(t0, loc=(-1.6, 84, 0), rot=180, armR=(80, 8))
    flashlight(E, 0.02, 6500, 55)
    T = tooty(t0, t1, "terror")
    T.pose(t0, loc=(2.0, 82, 0), rot=180)
    red = light("eyeglow", "POINT", (0, 120, 17), 60000, (1.0, 0.25, 0.2), 3)
    lamp_energy(red, t0, 0)
    lamp_energy(red, w(183) + 0.15, 0)
    lamp_energy(red, w(183) + 0.5, 60000)
    cam = Cam()
    cam.key(t0, (0, 90, 5.5), (0, 128, 12), lens=22)
    cam.key(t1, (0, 94, 6.5), (0, 128, 16), lens=18, ease="EASE_IN_OUT")
    cam.crash(w(183) + 0.15, 18, 32, 0.12)
    cam.handheld(1.4)
    sfx(w(183) + 0.15, "boom", 0.9)
    sfx(w(183) + 0.15, "u_movie", 0.6)
    sfx(t0, "rise", 0.5)


@S(59, 185, 189, "Bigger than a house: a tiny house next to the eye, kids tiny in front")
def s59(t0, t1):
    E3 = eye_set()
    eye_lids(E3, 0.0, 0.01, 0.1)
    c = collection("SCALE")
    won, wof = [], []
    house("hs", -16, 120, 9, 7, 8, "#d9755f", "-Y", c, won, wof, True)
    E = eddy(t0, t1, "terror")
    E.pose(t0, loc=(-1.6, 86, 0), rot=180, armR=(80, 8))
    flashlight(E, 0.02, 6500, 55)
    T = tooty(t0, t1, "terror")
    T.pose(t0, loc=(2.0, 84, 0), rot=180)
    light("eyeglow", "POINT", (0, 118, 17), 60000, (1.0, 0.25, 0.2), 3)
    cam = Cam()
    cam.key(t0, (0, 82, 3.0), (-6, 124, 12), lens=22)
    cam.key(t1, (0, 76, 7.0), (-2, 124, 14), lens=20, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0, "rise", 0.5)
    sfx(t0 + 0.1, "wind", 0.5)


@S(60, 189, 190, "Wet: extreme close-up of the eye, a tear slides")
def s60(t0, t1):
    E3 = eye_set()
    eye_lids(E3, 0.0, 0.01, 0.1)
    light("eyeglow", "POINT", (0, 112, 17), 40000, (1.0, 0.45, 0.4), 3)
    tear((-3.0, 121, 12.0), t0 + 0.05, 1, 0.65, 6, 0.9)
    cam = Cam()
    cam.push(t0, t1, (0, 128, 15), 22, 12, yaw=6, pitch=-4, lens=36, yaw1=-6, fstop=2.0)
    cam.handheld(0.8)
    sfx(t0 + 0.1, "drip", 0.8)
    sfx(t0 + 0.05, "sparkle", 0.4)


@S(61, 190, 191, "Red: bloodshot iris pulses, crash zoom")
def s61(t0, t1):
    E3 = eye_set()
    eye_lids(E3, 0.0, 0.01, 0.1)
    light("eyeglow", "POINT", (0, 112, 17), 60000, (1.0, 0.2, 0.15), 3)
    cam = Cam()
    cam.push(t0, t1, (0, 126, 17), 16, 8, yaw=0, pitch=0, lens=40, fstop=2.0)
    cam.crash(t0 + 0.05, 40, 60, 0.12)
    cam.handheld(1.0)
    sfx(t0 + 0.05, "boom", 0.8)


@S(62, 191, 193, "We froze: Eddie and Tooty stiff, wide eyes, the eye behind them")
def s62(t0, t1):
    eye_set()
    E = eddy(t0, t1, "terror")
    E.pose(t0, loc=(-1.6, 92, 0), rot=180, armL=(20, 8), armR=(20, 8))
    T = tooty(t0, t1, "terror")
    T.pose(t0, loc=(2.0, 92, 0), rot=180, armL=(20, 8), armR=(20, 8))
    E.act(t0 + 0.05, "recoil", expr="terror")
    T.act(t0 + 0.05, "recoil", expr="terror")
    light("kfill", "AREA", (0, 78, 9), 18000, (1.0, 0.8, 0.7), 6, target=(0, 92, 4))
    cam = Cam()
    cam.push(t0, t1, (0, 92, 4.6), 11, 7, yaw=-62, pitch=2, lens=34, yaw1=-48, fstop=2.2)
    cam.handheld(0.5)
    sfx(t0 + 0.05, "gasp", 0.8)
    sfx(t0 + 0.1, "rise", 0.4)


# ---- 0:58  the giant speaks
def cave_kids(t0, t1, ey=96.0, expr_e="worried", expr_t="worried", torch=True):
    E = eddy(t0, t1, expr_e)
    E.pose(t0, loc=(-2.0, ey, 0), rot=180, armR=(80, 8) if torch else (5, 8))
    T = tooty(t0, t1, expr_t)
    T.pose(t0, loc=(2.2, ey - 2, 0), rot=180)
    if torch:
        flashlight(E, 0.02, 6000, 55)
    return E, T


def giant_awake(t0, t1, expr="cry", head=14, loc=CAVE_LOC):
    G = giant(t0, t1, expr)
    sit_floor(G, t0, loc, GS, 0, head=(0, head, 0), torso=(0, 6, 0))
    G.pose(t0, armL=(48, -4), armR=(48, -4))
    G.face(t0, eyes="cry", mouth="flat")
    return G


@S(63, 193, 196, "The giant whispered: the giant's face fills the frame, kids tiny below")
def s63(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 16)
    G.face(t0 + 0.1, eyes="cry", mouth="talk")
    lips(G, t0 + 0.05, t1)
    cave_kids(t0, t1)
    cam = Cam()
    cam.key(t0, (-6, 90, 3.2), (0, 144, 22), lens=20)
    cam.key(t1, (-3, 92, 4.0), (0, 144, 24), lens=18, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "rise", 0.5)
    sfx(t0 + 0.2, "shh", 0.7)


@S(64, 196, 201, "and the whole cave trembled: rocks fall, dust, kids hug")
def s64(t0, t1):
    C = giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 16)
    cave_kids(t0, t1, 100)
    for ob in list(C["coll"].objects):
        if ob.name.startswith(("gc_stal", "gc_stag", "gc_cry")):
            noise(ob, "location", 0, 0.5, 2)
    rnd = random.Random(11)
    for i in range(14):
        ts = t0 + 0.2 + rnd.uniform(0, 1.8)
        x = rnd.uniform(-8, 8)
        ob = box(f"rock{i}", (rnd.uniform(0.6, 1.4),) * 3, (x, 100 + rnd.uniform(-6, 6), 12), M("#4a3f52", 0.9), 0.1)
        ob.keyframe_insert("location", frame=F(ts))
        ob.location = (x, ob.location[1], 0.5)
        ob.keyframe_insert("location", frame=F(ts + 0.5))
        ob.rotation_euler = (0, 0, 0)
        ob.keyframe_insert("rotation_euler", frame=F(ts))
        ob.rotation_euler = (rnd.uniform(1, 5), rnd.uniform(1, 5), 0)
        ob.keyframe_insert("rotation_euler", frame=F(ts + 0.5))
    cam = Cam()
    cam.key(t0, (-8, 88, 3.0), (0, 104, 6), lens=24)
    cam.key(t1, (6, 92, 5.5), (0, 106, 8), lens=20, ease="EASE_IN_OUT")
    cam.handheld(3.0)
    sfx(t0, "rumble", 0.9)
    sfx(t0 + 0.4, "boom", 0.7)
    sfx(t0 + 1.2, "boom", 0.6)
    sfx(t0 + 1.0, "thud", 0.6)


@S(65, 201, 205, "Why is it always: the giant's sad face talking, huge, from below")
def s65(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 18)
    lips(G, t0, t1)
    G.face(t0, eyes="cry", mouth="talk")
    cave_kids(t0, t1)
    cam = Cam()
    cam.push(t0, t1, giant_head(), 62, 40, yaw=-12, pitch=-16, lens=34, yaw1=6, pitch1=-8, fstop=3.0)
    cam.handheld(0.8)
    sfx(t0, "hum", 0.3)


@S(66, 205, 209, "so dark up there?: his eyes lift to the ceiling, camera cranes up")
def s66(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 18)
    G.pose(w(206), head=(0, -22, 0))
    G.face(w(206), eyes="up", mouth="talk")
    lips(G, t0, t1)
    cave_kids(t0, t1)
    tear((-3, 140, 25), t0 + 0.3, 1, 1.2, 8, 0.7)
    cam = Cam()
    cam.key(t0, (0, 100, 6), (0, 144, 22), lens=22)
    cam.key(t1, (0, 112, 30), (0, 150, 52), lens=22, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0 + 0.8, "drip", 0.5)


@S(67, 209, 211, "I swallowed: Eddie's gulp, sweat drop")
def s67(t0, t1):
    giant_cave()
    tunnel()
    E, T = cave_kids(t0, t1, 96, "shock", "worried")
    E.pose(t0, loc=(0.6, 96, 0), rot=0)
    E.act(t0 + 0.2, "recoil", expr="scared")
    sweat = sphere("sweat", 0.14, (0.9, 95.4, 5.2), mat("sweat_m", hexc("#bfe3ff"), 0.05, emit=hexc("#8fc4ff"), estr=0.6), (0.8, 0.8, 1.3), seg=10)
    sweat.keyframe_insert("location", frame=F(t0 + 0.2))
    sweat.location = (0.9, 95.4, 3.6)
    sweat.keyframe_insert("location", frame=F(t0 + 0.8))
    light("kfill", "AREA", (0, 84, 8), 20000, (0.9, 0.9, 1.0), 6, target=(0, 96, 4))
    cam = Cam()
    cam.push(t0, t1, (0.6, 96, 4.6), 6, 3.2, yaw=-6, pitch=2, lens=42, yaw1=6, fstop=2.0)
    cam.handheld(1.0)
    sfx(t0 + 0.25, "pop", 0.8)
    sfx(t0 + 0.25, "gasp", 0.4)


@S(68, 211, 217, "Because we're scared of waking you: Eddie speaks, Tooty nods")
def s68(t0, t1):
    giant_cave()
    tunnel()
    E, T = cave_kids(t0, t1, 96, "worried", "worried")
    E.pose(t0, loc=(-1.4, 96, 0), rot=0)
    T.pose(t0, loc=(2.4, 96, 0), rot=0)
    lips(E, t0, t1 - 0.2)
    E.act(w(213), "shrug", expr="worried")
    T.nod(w(214), 2, 10, 6.0)
    light("kfill", "AREA", (0, 84, 8), 20000, (0.9, 0.9, 1.0), 6, target=(0, 96, 4))
    cam = Cam()
    cam.push(t0, t1, (0.5, 96, 4.8), 9, 5.5, yaw=-14, pitch=2, lens=34, yaw1=12, fstop=2.2)
    cam.handheld(0.9)
    sfx(t0 + 0.1, "chat", 0.3)


@S(69, 217, 222, "I woke up long ago: giant face, gentle")
def s69(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 14)
    G.face(t0, eyes="cry", mouth="talk")
    lips(G, t0, t1)
    cave_kids(t0, t1)
    cam = Cam()
    cam.push(t0, t1, giant_head(), 46, 30, yaw=10, pitch=-6, lens=36, yaw1=-8, fstop=3.0)
    cam.handheld(0.7)
    sfx(t0, "hum", 0.3)


@S(70, 222, 225, "he said quietly: he lowers his head toward the kids")
def s70(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 14)
    G.pose(t1, head=(0, 28, 0), torso=(0, 14, 0))
    lips(G, t0, t1)
    cave_kids(t0, t1)
    cam = Cam()
    cam.key(t0, (-14, 84, 3.4), (0, 140, 18), lens=22)
    cam.key(t1, (-8, 90, 4.2), (0, 138, 14), lens=24, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0 + 0.1, "wind", 0.4)


def fireflies(center, n, r, t0, t1, seed=0):
    rnd = random.Random(seed)
    Mf = mat("firefly", hexc("#ffd88a"), 0.3, emit=hexc("#ffcf70"), estr=12)
    for i in range(n):
        p = Vector(center) + Vector((rnd.uniform(-r, r), rnd.uniform(-r, r) * 0.4, rnd.uniform(-r, r) * 0.7))
        ob = sphere(f"ff{i}", 0.35, tuple(p), Mf, seg=8)
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(t0 + rnd.uniform(0, 0.8)))
        ob.scale = (1, 1, 1)
        ob.keyframe_insert("scale", frame=F(t0 + 1.0 + rnd.uniform(0, 0.6)))
        ob.keyframe_insert("location", frame=F(t0))
        ob.location = tuple(p + Vector((rnd.uniform(-4, 4), rnd.uniform(-2, 2), rnd.uniform(1, 4))))
        ob.keyframe_insert("location", frame=F(t1))
        noise(ob, "location", 2, 0.8, 5)


@S(71, 225, 228, "I just wanted: giant eye shimmering, close")
def s71(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 22)
    G.face(t0, eyes="worried", mouth="talk")
    lips(G, t0, t1)
    cave_kids(t0, t1)
    cam = Cam()
    cam.push(t0, t1, giant_head(), 36, 22, yaw=-12, pitch=-4, lens=38, yaw1=-4, fstop=2.6)
    cam.handheld(0.7)
    sfx(t0, "hum", 0.3)


@S(72, 228, 232, "to see your lights: tiny lights swirl up around the giant")
def s72(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 22)
    G.face(t0, eyes="happy", mouth="talk")
    G.pose(w(230), head=(0, 4, 0))
    lips(G, t0, t1)
    cave_kids(t0, t1)
    fireflies(giant_head(), 22, 22, t0, t1, 7)
    cam = Cam()
    cam.push(t0, t1, giant_head(), 52, 30, yaw=14, pitch=-8, lens=32, yaw1=-10, fstop=2.8)
    cam.handheld(0.8)
    sfx(t0 + 0.3, "sparkle", 0.6)
    sfx(t0 + 0.6, "ding", 0.3)


@S(73, 232, 238, "He wasn't afraid of the dark: giant sits calm, kids look up")
def s73(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 12)
    G.face(t0, eyes="half", mouth="flat")
    cave_kids(t0, t1, 98)
    cam = Cam()
    cam.key(t0, (14, 92, 6.0), (0, 146, 20), lens=24)
    cam.key(t1, (-4, 100, 3.6), (0, 146, 22), lens=20, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0, "wind", 0.4)


@S(74, 238, 243, "He was lonely in it: crane up and back, tiny giant in a huge dark cave")
def s74(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 28)
    G.face(t0, eyes="worried", mouth="frown")
    cave_kids(t0, t1, 96)
    cam = Cam()
    cam.key(t0, (0, 100, 8), (0, 146, 20), lens=24)
    cam.key(t1, (0, 92, 40), (0, 150, 16), lens=20, ease="EASE_IN_OUT")
    cam.handheld(0.7)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.2, "cry", 0.35)


@S(75, 243, 249, "I turned on my flashlight: torch click, beam lights Eddie's face")
def s75(t0, t1):
    giant_cave()
    tunnel()
    E = eddy(t0, t1, "determined")
    E.pose(t0, loc=(-1.0, 94, 0), rot=0, armR=(70, 6))
    E.act(t0 + 0.15, "fists", expr="determined")
    cyl("torchb", 0.28, 1.5, (-0.1, -0.9, -1.9), M("#303038", 0.4, metal=0.5), 12, rot=(90, 0, 0), parent=E.shR, coll=E.coll)
    sp = light("fl2", "SPOT", (-0.4, 91.5, 4.0), 0, (1.0, 0.96, 0.82), 0.4, rot=(-90, 0, 0), spot=55, blend=0.5)
    sp.parent = E.head
    sp.location = (0, -0.8, 0.1)
    lamp_energy(sp, 0.5, 0)
    lamp_energy(sp, w(246), 7000)
    light("kfill", "AREA", (0, 82, 8), 20000, (0.9, 0.9, 1.0), 6, target=(0, 94, 4))
    cam = Cam()
    cam.push(t0, t1, (-1.0, 94, 4.6), 8, 4.2, yaw=-10, pitch=2, lens=36, yaw1=8, fstop=2.0)
    cam.handheld(1.0)
    sfx(w(246), "u_click", 1.0)
    sfx(w(246), "ding", 0.3)


@S(76, 249, 254, "pointed it at his face: beam sweeps up onto the giant's face")
def s76(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 18)
    G.face(t0, eyes="wide", mouth="o")
    cave_kids(t0, t1, 98)
    spot = light("beam", "SPOT", (-2, 96, 5), 0, (1.0, 0.96, 0.8), 0.6, target=(0, 144, 26), spot=24, blend=0.4)
    lamp_energy(spot, t0, 80000)
    cam = Cam()
    cam.key(t0, (-6, 88, 3.2), (0, 144, 22), lens=20)
    cam.key(t1, (-4, 92, 5.0), (0, 144, 26), lens=24, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "rise", 0.5)
    sfx(w(252), "sparkle", 0.5)


@S(77, 254, 256, "He smiled: the smile spreads across the giant's face")
def s77(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 14)
    G.face(t0, eyes="wide", mouth="flat")
    G.face(t0 + 0.25, eyes="happy", mouth="open_smile")
    G.face(t0 + 0.55, eyes="happy", mouth="grin")
    spot = light("beam", "SPOT", (-2, 96, 5), 60000, (1.0, 0.96, 0.8), 0.6, target=(0, 144, 26), spot=24, blend=0.4)
    cave_kids(t0, t1, 98)
    cam = Cam()
    cam.push(t0, t1, giant_head(), 52, 30, yaw=0, pitch=-6, lens=34, fstop=3.0)
    cam.handheld(0.8)
    sfx(t0 + 0.3, "aww", 0.6)
    sfx(t0 + 0.3, "sparkle", 0.6)


@S(78, 256, 259, "A smile as: mouth close-up, warm glow bursts")
def s78(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 8)
    G.face(t0, eyes="happy", mouth="grin")
    light("beam", "SPOT", (-2, 96, 5), 60000, (1.0, 0.96, 0.8), 0.6, target=(0, 144, 22), spot=24, blend=0.4)
    warm = light("warm", "POINT", (0, 130, 20), 0, (1.0, 0.8, 0.5), 3)
    lamp_energy(warm, t0, 40000)
    sparkle_on("gsp", (0, 138, 22), t0, 10.0, 18, 4)
    cam = Cam()
    cam.push(t0, t1, (0, 143.8, 22), 34, 22, yaw=6, pitch=-8, lens=40, yaw1=-6, fstop=3.0)
    cam.handheld(0.7)
    sfx(t0, "sparkle", 0.8)


@S(79, 259, 263, "wide as a valley: crane up showing the giant glowing in a golden cave")
def s79(t0, t1):
    giant_cave()
    tunnel()
    G = giant_awake(t0, t1, "cry", 8)
    G.face(t0, eyes="happy", mouth="grin")
    warm = light("warm", "POINT", (0, 130, 20), 60000, (1.0, 0.8, 0.5), 3)
    fireflies((0, 140, 20), 24, 30, t0, t1, 3)
    cave_kids(t0, t1, 98)
    cam = Cam()
    cam.key(t0, (0, 90, 6), (0, 146, 22), lens=22)
    cam.key(t1, (0, 92, 36), (0, 150, 16), lens=20, ease="EASE_IN_OUT")
    cam.handheld(0.7)
    sfx(t0, "sparkle", 0.6)
    sfx(t0 + 0.2, "rise", 0.4)


# ---- 1:16  the lights come on
@S(80, 263, 269, "That night, I convinced the whole town: Eddie and Tooty knock on doors")
def s80(t0, t1):
    night_town(t0, t1, lit0=False)
    E = eddy(t0, t1, "happy")
    T = tooty(t0, t1, "joy")
    E.walk(t0, t1, (-12, -3, 0), (-2, -3, 0), rate=3.2, swing=36, arm=34, bob=0.28, face_dir=False)
    T.walk(t0, t1, (-15, -4, 0), (-5, -4, 0), rate=3.2, swing=36, arm=34, bob=0.28, face_dir=False)
    E.pose(t0, rot=90)
    T.pose(t0, rot=90)
    E.act(w(266), "wave", expr="happy")
    cam = Cam()
    cam.key(t0, (-16, -14, 3.0), (-10, -3, 4), lens=26)
    cam.key(t1, (-2, -13, 4.0), (-3, -3, 4.2), lens=26, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    fill((-8, -12, 9), (-6, -3, 3), 3000, (0.9, 0.9, 1.0), 8)
    sfx(t0, "footsteps", 0.5, dur=3.0)
    sfx(w(267), "door", 0.4)


@S(81, 269, 275, "to turn on their lights: the whole town lights up in a cascade")
def s81(t0, t1):
    on = w(271) + 0.1
    night_town(t0, t1, lit0=False, on_at=on, cascade=0.055)
    ks = crowd_look(t0, t1, 6, (0, -2), 12, 0, "joy", seed=9)
    for k in ks:
        k.act(on + 0.2, "cheer", expr="joy")
    cam = Cam()
    cam.key(t0, (-36, -13, 4.5), (0, 6, 6), lens=22)
    cam.key(t1, (-14, -14, 9), (0, 6, 6), lens=20, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    fill((-12, -14, 10), (0, 0, 3), 2500, (1.0, 0.9, 0.7), 8)
    for j in range(8):
        sfx(on + j * 0.07, "click", 0.55)
    sfx(on, "u_correct", 0.8)
    sfx(on + 0.1, "rise", 0.6)
    sfx(on + 0.5, "sparkle", 0.7)


@S(82, 275, 278, "The windows glowed: high wide of the glowing town, crane up")
def s82(t0, t1):
    night_town(t0, t1, lit0=True, tower=True)
    cam = Cam()
    cam.key(t0, (-24, -14, 5), (0, 8, 8), lens=20)
    cam.key(t1, (-6, -15, 15), (0, 14, 9), lens=18, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    fill((-12, -14, 10), (0, 0, 3), 2500, (1.0, 0.9, 0.7), 8)
    sfx(t0, "sparkle", 0.8)
    sfx(t0 + 0.2, "u_applepay", 0.5)


@S(83, 278, 280, "Candles flickered: candle flames in windows, close")
def s83(t0, t1):
    R = dark_room({})
    for k in range(3):
        cyl(f"cx{k}", 0.4, 1.2, (10 + k * 1.6, 8, 2.8), M("#f4ecd8", 0.6), 16)
        f = sphere(f"fx{k}", 0.3, (10 + k * 1.6, 8, 3.8), emitm("#ffb040", 9.0), (0.7, 0.7, 1.5), seg=12)
        noise(f, "scale", 2, 0.35, 3)
        noise(f, "location", 0, 0.05, 4)
    cam = Cam()
    cam.push(t0, t1, (11.6, 8, 3.8), 9, 5, yaw=-14, pitch=2, lens=44, yaw1=10, fstop=1.8)
    cam.handheld(0.9)
    sfx(t0 + 0.05, "sparkle", 0.6)
    sfx(t0 + 0.2, "u_discord", 0.5)


@S(84, 280, 284, "Tooty screamed with joy: Tooty, no pillow, jumps and yells, confetti")
def s84(t0, t1):
    night_town(t0, t1, lit0=True)
    T = tooty(t0, t1, "scream")
    T.pose(t0, loc=(0, -3, 0), rot=0)
    T.act(t0 + 0.05, "cheer", expr="scream")
    T.jump(t0 + 0.25, 2.0, 0.5)
    T.jump(t0 + 0.95, 2.0, 0.5)
    T.talk(t0, t1, words=V.span(t0, t1), open_m="scream", wide_m="laugh", rest="laugh")
    confetti("cf", (0, -3, 6), (8, 3, 4), t0 + 0.4, 1.6, 90, 2, 12)
    cam = Cam()
    cam.orbit(t0, t1, (0, -3, 4.8), 9, -35, 40, pitch=4, lens=26, steps=4, fstop=2.8)
    cam.crash(t0 + 0.25, 26, 34, 0.1)
    cam.handheld(1.4)
    fill((-5, -11, 9), (0, -3, 3), 2800, (1.0, 0.9, 0.8), 8)
    sfx(t0 + 0.2, "cheer", 0.8)
    sfx(t0 + 0.3, "confetti", 0.7)
    sfx(t0 + 0.25, "u_faaah", 0.0)


@S(85, 284, 287, "And far below: camera dives through the glowing town into the cavern")
def s85(t0, t1):
    cutaway(lit=True)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    G.face(t0, eyes="closed", mouth="smile")
    cam = Cam()
    cam.key(t0, (0, -75, 14), (0, 6, 2), lens=28)
    cam.key(t1, (0, -96, -40), (0, 6, -38), lens=28, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 0.1, "rise", 0.5)


@S(86, 287, 292, "the giant finally fell asleep: eyes close, smile, zzz")
def s86(t0, t1):
    cutaway(lit=True)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    G.pose(t0, head=(0, 6, 0), torso=(0, 4, 0))
    G.face(t0, eyes="happy", mouth="smile")
    G.pose(w(290), head=(0, 26, 4))
    G.face(w(290), eyes="closed", mouth="smile")
    fz = giant_head(CUT_LOC)
    zzz((fz[0] + 8, fz[1] - 4, fz[2] + 8), w(290), 3, 3.0, 5.0)
    notes((fz[0], fz[1], fz[2] + 12), t0 + 0.4, 5, 8.0, 2.8, 14.0, 3, "#ffe38a", 1.6)
    cam = Cam()
    cam.push(t0, t1, fz, 80, 40, yaw=-20, pitch=2, lens=34, yaw1=10, fstop=4.0)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "aww", 0.5)
    sfx(w(290), "snore", 0.6)
    sfx(t0 + 0.4, "hum", 0.6)


@S(87, 292, 298, "Now the town is never dark: wide lit town, kids playing in the street")
def s87(t0, t1):
    night_town(t0, t1, lit0=True)
    for j in range(5):
        k = townie(j + 1, t0, t1, "joy")
        k.walk(t0, t1, (-12 + j * 5, -2 - (j % 2) * 3, 0), (-6 + j * 5, -2 - (j % 2) * 3, 0), rate=3.0, swing=34, arm=34, bob=0.25, face_dir=False)
        k.pose(t0, rot=90)
        k.jump(t0 + 0.4 + j * 0.3, 1.2, 0.45)
    cam = Cam()
    cam.key(t0, (-30, -13, 3.5), (0, 0, 5), lens=22)
    cam.key(t1, (-8, -14, 8.0), (0, 2, 5), lens=22, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    fill((-10, -14, 10), (0, 0, 3), 2500, (1.0, 0.9, 0.7), 8)
    sfx(t0, "kids_laugh", 0.6)
    sfx(t0 + 0.2, "cheer", 0.4)


@S(88, 298, 302, "and every night: the clock tower strikes 9 and the lights stay on")
def s88(t0, t1):
    night_town(t0, t1, lit0=True)
    cam = Cam()
    cam.push(t0, t1, (0, 36, 22), 26, 14, yaw=0, pitch=-2, lens=28, fstop=4.0)
    cam.handheld(0.8)
    pop_text("t9b", "9:00", (0, 30, 30), t0 + 0.1, 3.0, "#ffe9a0", dur=0.7)
    sfx(t0 + 0.1, "ding", 0.8)
    sfx(t0 + 0.3, "sparkle", 0.5)


@S(89, 302, None, "the ground hums a lullaby back: notes rise from the ground, final pull-up")
def s89(t0, t1):
    cutaway(lit=True)
    G = giant(t0, t1)
    giant_sleep(G, t0, CUT_LOC)
    G.pose(t0, head=(0, 26, 4))
    G.face(t0, eyes="closed", mouth="smile")
    fz = giant_head(CUT_LOC)
    notes((0, 4, -8), t0 + 0.2, 10, 40.0, 3.4, 26.0, 5, "#ffe38a", 2.2)
    cam = Cam()
    cam.key(t0, (0, -78, -36), (0, 6, -36), lens=28)
    cam.key(w(305), (0, -86, -10), (0, 6, -6), lens=26, ease="EASE_IN_OUT")
    cam.key(t1, (0, -100, 18), (0, 6, 4), lens=24, ease="EASE_IN_OUT")
    cam.handheld(0.5)
    sfx(t0, "hum", 0.9)
    sfx(t0 + 0.5, "sparkle", 0.5)
