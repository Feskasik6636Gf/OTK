"""pip: Every kid gets a monster bodyguard at ten. Pip is the size of a potato, until I believe in him.
Shots keyed to script word indices (audio/words.json), 9:16, original Roblox-style blocky cast."""
from shotkit import *
from rbx import story
from rbx.story import *
import math, random
from mathutils import Vector
from rbx.sets import wood, planks

V = Video(__file__)
story.bind(V)
TEX = os.path.join(rbx.ASSETS, "tex")
SQ = (0.0, -30.0, 0.0)        # open street = "the square"


def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


look = acting.look


def head(ch, dz=0.0):
    p = ch.root.location
    return (p[0], p[1], p[2] + FH * ch.root.scale[2] + dz)


def pt(x, y, z):
    return (x, y, z)



# ---- auto shot ids + multi-angle beats ---------------------------------------------------------
_ID = [0]
BEAT = [None]


def _reg(a, b, desc, fn, k=0, alt=None, t0=None, t1=None):
    _ID[0] += 1
    i = _ID[0]
    t0 = w(a) if t0 is None else t0
    t1 = (V.end if b is None else w(b)) if t1 is None else t1

    def run():
        random.seed(i)
        fn(t0, t1)
        if alt is not None:
            alt(t0, t1)
        CUES[:] = [c for c in CUES if t0 - 0.05 <= c["t"] <= t1 - 0.05]
    V.shot(i, t0, t1, desc)(run)


def S(i, a, b, desc=""):
    def deco(fn):
        _reg(a, b, desc, fn)
        return fn
    return deco


def beat(a, b, n=2, focus=(0, -30, 4.5), d=10.0, lens=28, desc="", pitch=4):
    """Same scene, n sub-shots with different camera angles (cut on word starts)."""
    def deco(fn):
        T0 = w(a)
        T1 = V.end if b is None else w(b)
        words = [x["start"] for x in V.words if T0 < x["start"] < T1]
        cuts = [T0]
        for k in range(1, n):
            tt = T0 + (T1 - T0) * k / n
            cuts.append(min(words, key=lambda x: abs(x - tt)) if words else tt)
        cuts.append(T1)
        for k in range(n):
            t0, t1 = cuts[k], cuts[k + 1]

            def run(t0, t1, k=k):
                BEAT[0] = (T0, T1)
                fn(t0, t1)
                BEAT[0] = None
            alt = None
            if k > 0:
                def alt(t0, t1, k=k):
                    yaw = (-38, 34, -20, 24)[(k - 1) % 4]
                    dd = d * (0.7 if k % 2 else 1.15)
                    cam = Cam()
                    cam.push(t0, t1, focus, dd, dd * 0.82, yaw=yaw, pitch=pitch + 2, lens=lens, yaw1=yaw * 0.4, lens1=lens)
                    cam.handheld(1.2)
            _reg(a, b, desc, run, k, alt, t0, t1)
        return fn
    return deco


# ================================================================== cast
def tootie(t0, t1, expr="smug"):
    T = chars.Char("Tootie", skin="#d9b48f", shirt="#6a3fb0", pants="#2d2f45", hair="messy", hair_color="#1d1714",
                   face="kid", vneck="#b79af0", extras=("backpack:TOOTIE",))
    return story._live(T, t0, t1, expr)


def mom(t0, t1, expr="happy"):
    return story._live(chars.girl("Mom", shirt="#e0457b", pants="#5a4a8a", hair_color="#5a3a22"), t0, t1, expr)


def dadc(t0, t1, expr="neutral"):
    return story._live(chars.dad("Dad", shirt="#e8e8e0", pants="#3b3f4a"), t0, t1, expr)


def cop(t0, t1, expr="neutral", name="Cop"):
    return pilot(t0, t1, expr, name=name, shirt="#2b4aa0")


def teacher(t0, t1, expr="neutral"):
    return story._live(chars.teacher("Teacher"), t0, t1, expr)


def clown(i, t0, t1, expr="neutral"):
    wig = ["#ff3d7f", "#35c6f4", "#ffd23a", "#7ddc5a"][i % 4]
    shirts = ["#ff5a3c", "#7a5af0", "#ffb020", "#26b0a0"]
    C = chars.Char(f"Clown{i}", skin="#f7f1ea", shirt=shirts[i % 4], pants="#ffd23a" if i % 2 else "#4a7ad0",
                   hair="messy", hair_color=wig, face="kid", vneck="#ffffff", sleeves="long")
    sphere(f"Clown{i}_nose", 0.17, (0, -0.64, -0.06), M("#e83a30", 0.3), parent=C.head, coll=C.coll)
    return story._live(C, t0, t1, expr)


def baby(i, t0, t1, expr="cry"):
    return story._live(chars.kid(40 + i, scale=0.5), t0, t1, expr)


def fartan(t0, t1, expr="happy"):
    P = chars.Char("Fartan", skin="#e9c7a6", shirt="#b9904a", pants="#4a3a28", hair="bald", face="mustache",
                   sleeves="long", extras=("glasses",), vneck="#f4f4f4", scale=1.15)
    box("Fartan_tie", (0.36, 0.06, 1.3), (0, -0.57, 1.25), M("#2a8f5a", 0.4), 0.03, parent=P.hip, coll=P.coll)
    return story._live(P, t0, t1, expr)


# ================================================================== props / sets
def water(z0, z1, t0, t1, ease="EASE_IN_OUT", size=900, c=(0.10, 0.42, 0.62), alpha=0.8, y=-20, name="water"):
    if BEAT[0]:
        B0, B1 = BEAT[0]
        zz = lambda t: z0 + (z1 - z0) * (t - B0) / max(B1 - B0, 1e-3)
        if ease == "LINEAR":
            z0, z1 = zz(t0), zz(t1)
    ob = plane(name, size, size, (0, y, z0), mat("wat" + str(c), c, 0.06, alpha=alpha, spec=1.0))
    ob.keyframe_insert("location", index=2, frame=F(t0))
    ob.location[2] = z1
    ob.keyframe_insert("location", index=2, frame=F(t1))
    if ease == "LINEAR":
        set_interp(ob, "location", F(t0), "LINEAR")
    else:
        set_interp(ob, "location", F(t0), "BEZIER", ease)
    noise(ob, "location", 2, 0.05, 9)
    return ob


def pole(loc, rot=0, swivel=None, sign="sign_nolaugh.png", sign_z=6.2, red=True, name="pole"):
    """Street pole with a laugh-detector camera on top and a sign. Returns the camera head empty."""
    x, y, z = loc
    cyl(name + "_p", 0.32, 11.5, (x, y, z + 5.75), M("#6b6f78", 0.5, metal=0.5), 16)
    cyl(name + "_b", 0.5, 0.6, (x, y, z + 0.3), M("#4a4d55", 0.5), 16)
    hd = empty(name + "_head", (x, y, z + 11.6), rot=(0, 0, rot))
    box(name + "_cam", (1.6, 2.0, 1.1), (0, -0.7, 0.3), M("#2a2c33", 0.3), 0.15, parent=hd)
    cyl(name + "_lens", 0.42, 0.7, (0, -1.8, 0.3), M("#101216", 0.15, metal=0.4), 20, rot=(90, 0, 0), parent=hd)
    sphere(name + "_led", 0.2, (0.55, -1.0, 0.95), mat("led_red", (1, 0.1, 0.1), 0.3, emit=(1, 0.1, 0.1), estr=8.0), parent=hd)
    if sign:
        card(name + "_sign", 2.8, 2.8, (x, y - 0.45, z + sign_z), img_mat("s" + sign, os.path.join(TEX, sign), 0.5), "-Y")
    if swivel:
        t0, t1, a0, a1 = swivel
        hd.rotation_euler[2] = math.radians(a0)
        hd.keyframe_insert("rotation_euler", index=2, frame=F(t0))
        hd.rotation_euler[2] = math.radians(a1)
        hd.keyframe_insert("rotation_euler", index=2, frame=F(t1))
    return hd


def room(wall="#cdd6ea", floor="#b5764e", night=False, key=6500):
    world((0.8, 0.85, 1.0), 0.08 if night else 0.35)
    Mw = M(wall, 0.85)
    box("r_floor", (34, 30, 0.4), (0, 2, -0.2), M(floor, 0.6), 0)
    box("r_back", (34, 0.5, 14), (0, 12, 7), Mw, 0)
    box("r_left", (0.5, 30, 14), (-15, 2, 7), Mw, 0)
    box("r_right", (0.5, 30, 14), (15, 2, 7), Mw, 0)
    box("r_ceil", (34, 30, 0.4), (0, 2, 13.4), M("#eeeeee", 0.9), 0)
    e = 0.3 if night else 1.0
    light("r_key", "AREA", (0, 0, 12.5), key * e, (0.8, 0.85, 1.0) if night else (1, 0.96, 0.9), 12, target=(0, 6, 0))
    light("r_fill", "AREA", (0, -10, 7), 2600 * e, (0.9, 0.93, 1.0), 10, target=(0, 6, 3))
    light("r_back", "AREA", (0, 9, 9), 1600 * e, (1, 0.95, 0.9), 10, target=(0, 0, 3))


def table(name, loc, size=(6, 3, 0.4), h=3.2, col="#8a5a38"):
    x, y, z = loc
    box(name + "_top", (size[0], size[1], size[2]), (x, y, z + h), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"{name}_l{sx}{sy}", (0.4, 0.4, h), (x + sx * (size[0] / 2 - 0.4), y + sy * (size[1] / 2 - 0.4), z + h / 2),
                wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0.03)


def bill(name, loc, rot=(0, 0, 0), s=1.0):
    return plane(name, 1.8 * s, 0.8 * s, loc, img_mat("dollar", os.path.join(TEX, "dollar.png"), 0.6), rot)


def note_card(name, loc, tex="note_one.png", s=1.0, rot=(90, 0, 0)):
    return plane(name, 1.4 * s, 1.0 * s, loc, img_mat(tex, os.path.join(TEX, tex), 0.6), rot)


def barrel(loc, name="barrel"):
    x, y, z = loc
    cyl(name, 1.3, 3.0, (x, y, z + 1.5), M("#8a5a38", 0.7), 24, bev=0.08)
    for dz in (0.5, 2.5):
        cyl(f"{name}_h{dz}", 1.34, 0.18, (x, y, z + dz), M("#2a2a2e", 0.4, metal=0.6), 24)


def house_front(loc, w=14, h=11, wall="#e2725b", roof="#a33b2f", name="hs"):
    """A house facade facing -Y with a door, first-floor windows and small basement windows."""
    x, y, z = loc
    box(name + "_wall", (w, 6, h), (x, y, z + h / 2), M(wall, 0.7), 0.15)
    box(name + "_roof", (w + 1.2, 7, 1.4), (x, y, z + h + 0.7), M(roof, 0.7), 0.2)
    gl = mat("glass_blue", (0.7, 0.88, 1.0), 0.1, emit=(0.5, 0.75, 1.0), estr=0.8)
    box(name + "_door", (2.4, 0.2, 5.0), (x, y - 3.05, z + 2.5 + 3.0), M("#6e4229", 0.6), 0.05)
    for sx in (-1, 1):
        box(f"{name}_w{sx}", (2.6, 0.2, 3.0), (x + sx * 4.6, y - 3.05, z + 6.8), gl, 0.05)
        box(f"{name}_wf{sx}", (3.0, 0.15, 3.4), (x + sx * 4.6, y - 3.0, z + 6.8), M("#ffffff", 0.5), 0.05)
        box(f"{name}_bw{sx}", (1.8, 0.2, 1.0), (x + sx * 4.6, y - 3.05, z + 1.4), gl, 0.05)
    box(name + "_step", (3.2, 1.4, 0.6), (x, y - 3.4, z + 0.3), M("#9a9a9a", 0.8), 0.05)


def street_pair(t0, t1, n=6, seed=0):
    """A few townsfolk standing around (static, blinking)."""
    out = []
    rnd = random.Random(seed)
    for i in range(n):
        k = townie(i + seed, t0, t1, "neutral")
        k.pose(t0, loc=(rnd.uniform(-9, 9), rnd.uniform(-38, -22), 0), rot=rnd.uniform(-30, 30))
        out.append(k)
    return out


def scream_crowd(t0, t1, n=10, area=((-12, 12), (-36, -22)), seed=1, z=0.0):
    rnd = random.Random(seed)
    ks = []
    for i in range(n):
        k = townie(i + 3, t0, t1, "scream")
        k.pose(t0, loc=(rnd.uniform(*area[0]), rnd.uniform(*area[1]), z), rot=rnd.uniform(-35, 35))
        k.panic(t0, t1, rate=rnd.uniform(5, 8))
        k.jump(t0 + rnd.uniform(0, 0.4), 1.0, 0.45)
        ks.append(k)
    return ks


def mouth_flap(ch, t0, t1, mode="talk"):
    return lips(ch, t0, t1, mode)


def shake_cam(cam, t0, t1, strength=1.0):
    cam.handheld(strength)
    return cam


def jail_set(open_t=None):
    world((0.7, 0.75, 0.9), 0.3)
    Mw = tiles("jail_wall", "#9a9a96", "#6a6a66", 1.0, 1.6, 0.8, 0.9, c2="#8e8e8a", axis="XZ")
    box("jail_floor", (30, 22, 0.4), (0, 4, -0.2), M("#5a5a58", 0.9), 0)
    box("jail_back", (30, 0.5, 14), (0, 10, 7), Mw, 0)
    for sx in (-1, 1):
        box(f"jail_side{sx}", (0.5, 16, 14), (sx * 9, 3, 7), Mw, 0)
    box("jail_ceil", (30, 22, 0.4), (0, 4, 13.6), M("#444448", 0.9), 0)
    Mb = mat("jail_bars", hexc("#2a2a2e"), 0.3, metal=0.8)
    door = empty("jail_door", (3.6, -3.0, 0))
    for i in range(5):
        cyl(f"jail_dbar{i}", 0.12, 11, (i * 0.9 - 3.6 + 0.0, 0, 5.5), Mb, 10, parent=door)
    for z in (0.3, 10.8):
        box(f"jail_drail{z}", (4.0, 0.3, 0.3), (-1.8, 0, z), Mb, 0.02, parent=door)
    for i in range(19):
        x = -9 + i * 1.0
        if 0.1 < x < 3.5:
            continue
        cyl(f"jail_bar{i}", 0.12, 11, (x, -3.0, 5.5), Mb, 10)
    for z in (0.3, 10.8):
        box(f"jail_rail{z}", (18.0, 0.3, 0.3), (0, -3.0, z), Mb, 0.02)
    box("jail_bench", (6, 1.8, 0.5), (-5.0, 8.0, 2.0), wood("wood_bench", "#6e4229", "#a06a45", 2.0), 0.05)
    card("jail_sign", 3.2, 4.0, (3.5, 9.6, 7.5), img_mat("wanted_t", os.path.join(TEX, "wanted_tootie.png"), 0.5), "-Y")
    light("jail_lamp", "SPOT", (0, -2, 12.5), 11000, (1.0, 0.92, 0.75), 0.3, spot=75, target=(0, 4, 0))
    light("jail_fill", "AREA", (0, -10, 7), 3200, (0.7, 0.8, 1.0), 10, target=(0, 4, 3))
    if open_t is not None:
        door.rotation_euler[2] = 0
        door.keyframe_insert("rotation_euler", index=2, frame=F(open_t))
        door.rotation_euler[2] = math.radians(-115)
        door.keyframe_insert("rotation_euler", index=2, frame=F(open_t + 0.4))
        set_interp(door, "rotation_euler", F(open_t), "BEZIER", "EASE_OUT")
    return door


def tiles(*a, **k):
    return sets.tiles(*a, **k)


def office_set():
    room("#d6e4d2", "#8a8f98", key=7000)
    table("desk", (0, 6.5, 0), (9, 3.4, 0.4), 3.4)
    box("monitor", (4.2, 0.3, 2.8), (0, 7.3, 6.5), M("#18181c", 0.3), 0.08)
    card("monitor_scr", 3.8, 2.4, (0, 7.12, 6.5), img_mat("tv_show", os.path.join(TEX, "tv_show.png"), 0.3, emit=2.0), "-Y")
    box("monitor_stand", (0.5, 0.5, 1.0), (0, 7.3, 4.0), M("#18181c", 0.3), 0.04)
    card("o_clock", 2.2, 2.2, (6.0, 11.6, 9.5), img_mat("clock_1159", os.path.join(TEX, "clock_1159.png"), 0.5), "-Y")
    sets.plant("o_plant", (-9, 9, 0), None, 1.4)


def tv_set():
    room("#c6b7e0", "#8d6a4a", key=4500)
    box("tv_stand", (9, 2.4, 2.2), (0, 9.5, 1.1), wood("wood_tv", "#a0703f", "#c89260", 2.0), 0.05)
    box("tv_body", (9.6, 0.5, 5.4), (0, 9.5, 5.0), M("#111114", 0.3), 0.1)
    card("tv_scr", 9.0, 4.8, (0, 9.22, 5.0), img_mat("tv_show", os.path.join(TEX, "tv_show.png"), 0.3, emit=2.2), "-Y")
    light("tv_glow", "AREA", (0, 7.5, 5.0), 600, (0.7, 0.85, 1.0), 5, target=(0, -6, 3.5))
    box("couch", (11, 3.2, 2.6), (0, -3.0, 1.3), M("#5a8f6a", 0.8), 0.3)
    box("couch_back", (11, 1.0, 3.6), (0, -4.6, 3.0), M("#4d7d5c", 0.8), 0.3)
    box("mute", (0, 0, 0) and (1.2, 0.1, 0.8), (3.8, 9.2, 8.2), M("#ff3b3b", 0.3, emit=hexc("#ff3b3b"), estr=2.0), 0.02)


def nursery_set(t_clock=None):
    room("#f6dce8", "#e8d8c0", key=7000)
    box("nur_mat", (24, 12, 0.1), (0, 5, 0.05), M("#8fd0ff", 0.9), 0)
    card("n_clock", 3.0, 3.0, (0, 11.6, 10.0), img_mat("clock_1200", os.path.join(TEX, "clock_1200.png"), 0.5), "-Y")
    for i, x in enumerate((-7, 0, 7)):
        box(f"crib{i}_b", (4.6, 4.0, 0.3), (x, 7, 1.6), M("#ffffff", 0.5), 0.05)
        for k in range(6):
            box(f"crib{i}_r{k}", (0.12, 0.12, 2.4), (x - 2.2 + k * 0.88, 5.0, 2.7), M("#ffffff", 0.5), 0.02)
            box(f"crib{i}_s{k}", (0.12, 0.12, 2.4), (x - 2.2 + k * 0.88, 9.0, 2.7), M("#ffffff", 0.5), 0.02)


def bedroom_set():
    room("#9fb3d8", "#a86a44", night=True)
    box("bed", (9, 12, 1.6), (-4, 5, 0.8), M("#5a7ac8", 0.8), 0.2)
    box("bed_head", (9.4, 0.6, 4.0), (-4, 11.2, 2.4), wood("wood_dark", "#6e4229", "#a06a45", 2.5), 0.1)
    box("pillow", (5.0, 2.8, 1.0), (-4, 9.4, 2.0), M("#f4f4f2", 0.9), 0.4)
    box("moon_win", (4.0, 0.2, 5.0), (8, 11.6, 7.0), mat("moonglass", (0.6, 0.75, 1.0), 0.2, emit=(0.5, 0.65, 1.0), estr=2.0), 0.05)
    light("br_moon", "AREA", (8, 9, 8), 1500, (0.45, 0.6, 1.0), 6, target=(-2, 4, 1))
    light("br_lamp", "POINT", (-10, 8, 4.0), 90, (1.0, 0.75, 0.45), 0.5)


def swamp_set(t0=0.0):
    W.sky(0.9, top=(0.35, 0.5, 0.4), bottom=(0.65, 0.7, 0.55))
    W.sun(2.2, rot=(60, 0, 20))
    plane("swamp", 900, 900, (0, 0, 0.0), mat("swamp_g", (0.18, 0.28, 0.14), 0.15, alpha=0.95, spec=1.0))
    rnd = random.Random(5)
    for i in range(36):
        x, y = rnd.uniform(-60, 60), rnd.uniform(-10, 70)
        h = rnd.uniform(4, 9)
        cyl(f"reed{i}", 0.12, h, (x, y, h / 2), M("#6f8f3a", 0.8), 8)
        sphere(f"reedtop{i}", 0.28, (x, y, h), M("#5a3a22", 0.8), (1, 1, 2.2))
    for i in range(14):
        sphere(f"bub{i}", 0.4, (rnd.uniform(-14, 14), rnd.uniform(0, 30), 0.1), mat("bubble", (0.6, 0.8, 0.5), 0.2, alpha=0.6), (1, 1, 0.4))


def fire_pile(loc, t0, n=5):
    x, y, z = loc
    for i in range(n):
        note_card(f"pile{i}", (x + random.uniform(-0.8, 0.8), y + random.uniform(-0.5, 0.5), z + 0.15 + i * 0.1), "note_one.png", 0.8,
                  rot=(0, 0, random.uniform(0, 180)))
    fx.fire_cluster("pf", (x, y, z), spread=(1.2, 1.0, 0), n=6, h=(2.5, 4.2), w=(1.5, 2.4), seed=3)
    light("pf_l", "POINT", (x, y - 1.4, z + 2.0), 2200, (1.0, 0.5, 0.15), 1.0)


# ================================================================== fog-story helpers
def dusk_sky(night=False):
    if night:
        W.sky(0.18, top=(0.01, 0.02, 0.07), bottom=(0.06, 0.08, 0.17))
        W.sun(0.9, rot=(62, 0, 200))
    else:
        W.sky(0.75, top=(0.30, 0.33, 0.46), bottom=(0.62, 0.64, 0.72))
        W.sun(1.6, rot=(72, 0, 25))


def fogballs(n, area, z=(0.6, 5.0), size=(3.0, 7.0), seed=1, alpha=0.2, name="fog"):
    rnd = random.Random(seed)
    Mf = mat(f"fogm{alpha}", (0.86, 0.89, 0.96), 1.0, emit=(0.8, 0.85, 0.95), estr=0.3, alpha=alpha)
    for i in range(n):
        s = rnd.uniform(*size)
        ob = sphere(f"{name}{seed}_{i}", s, (rnd.uniform(*area[0]), rnd.uniform(*area[1]), rnd.uniform(*z)), Mf,
                    (1.5, 1.5, 0.55), seg=12)
        noise(ob, "location", 0, 1.4, 40)
        noise(ob, "location", 1, 0.9, 55)


def bridge(y0=30.0, length=34.0):
    """Old wooden bridge along +Y over a dark river; the far end disappears in the fog."""
    Mw = wood("wood_bridge", "#5a3a28", "#7a5238", 2.0)
    box("river", (160, 120, 0.2), (0, y0 + 30, 0.1), mat("river_dark", (0.05, 0.1, 0.16), 0.08, alpha=0.9, spec=1.0), 0)
    box("bank_l", (60, 14, 2.4), (-40, y0 - 4, 1.2), M("#2f4a2a", 0.9), 0)
    box("bank_r", (60, 14, 2.4), (40, y0 - 4, 1.2), M("#2f4a2a", 0.9), 0)
    box("deck", (9, length, 0.7), (0, y0 + length / 2, 2.1), Mw, 0.05)
    for k in range(0, int(length), 4):
        for sx in (-1, 1):
            box(f"post{k}{sx}", (0.5, 0.5, 3.6), (sx * 4.3, y0 + k + 1, 4.0), Mw, 0.05)
            cyl(f"pil{k}{sx}", 0.45, 3.0, (sx * 3.6, y0 + k + 1, 0.8), Mw, 8)
    for sx in (-1, 1):
        box(f"rail{sx}", (0.35, length, 0.35), (sx * 4.3, y0 + length / 2, 4.6), Mw, 0.03)
        box(f"rail2{sx}", (0.3, length, 0.3), (sx * 4.3, y0 + length / 2, 3.4), Mw, 0.03)


def night_street(night=True, fog=True, lamps=True, houses=True):
    dusk_sky(night)
    world((0.2, 0.25, 0.4) if night else (0.5, 0.52, 0.6), 0.5 if night else 0.5)
    if night:
        light("nfill", "AREA", (0, -22, 9), 5200, (0.7, 0.8, 1.0), 14, target=(0, -8, 4))
        light("nfill2", "AREA", (8, -16, 6), 2600, (1.0, 0.85, 0.7), 8, target=(0, -8, 4))
    box("g", (240, 240, 0.4), (0, 20, -0.2), M("#2b3d2a" if night else "#4a6a3a", 0.95), 0)
    box("road", (12, 240, 0.1), (0, 20, 0.03), M("#2a2b33" if night else "#55565e", 0.85), 0)
    if houses:
        for i, y in enumerate((-30, -12, 6, 24)):
            house_front((-24, y, 0), w=12, h=9, wall=["#8a6a5a", "#6a7a8a", "#7a6a8a", "#8a8a6a"][i % 4], name=f"hl{i}")
            house_front((24, y, 0), w=12, h=9, wall=["#6a7a8a", "#8a6a5a", "#8a8a6a", "#7a6a8a"][i % 4], name=f"hr{i}")
            bpy.data.objects[f"hl{i}_wall"].rotation_euler[2] = math.radians(-90)
            bpy.data.objects[f"hr{i}_wall"].rotation_euler[2] = math.radians(90)
    if lamps:
        for i, y in enumerate((-20, -2, 16)):
            for sx in (-1, 1):
                cyl(f"lp{i}{sx}", 0.18, 7, (sx * 7, y, 3.5), M("#2a2c33", 0.5), 8)
                sphere(f"lb{i}{sx}", 0.5, (sx * 7, y, 7.2), mat("lamp_y", (1, 0.85, 0.5), 0.3, emit=(1, 0.8, 0.4), estr=6.0))
                light(f"ll{i}{sx}", "POINT", (sx * 7, y, 7), 600 if night else 200, (1, 0.8, 0.5), 0.6)
    bridge()
    if fog:
        fogballs(26, ((-22, 22), (24, 62)), seed=3, alpha=0.2)
        fogballs(8, ((-14, 14), (6, 24)), z=(0.5, 2.0), size=(3, 5), seed=5, alpha=0.12)


def caller(i, t0, t1, loc, rot=0, scale=1.55, reach=True):
    C = chars.Char(f"Caller{i}", skin="#b9bac8", shirt="#0a0a10", pants="#0a0a10", hair="bald", face=None, sleeves="long",
                   scale=scale)
    for sx in (-1, 1):
        sphere(f"Caller{i}_eye{sx}", 0.11, (sx * 0.22, -0.6, 0.08), mat("eye_glow", (1, 1, 0.9), 0.3, emit=(1, 1, 0.85), estr=12.0),
               parent=C.head, coll=C.coll)
    story._live(C, t0, t1, "neutral", 0.4)
    C.pose(t0, loc=loc, rot=rot)
    if reach:
        C.pose(t0 + 0.2, armL=(100, 0), armR=(100, 0))
    return C


def bubble(t0, t1, loc, body, col=(1, 0.95, 0.75), size=1.6, rot=(90, 0, 0)):
    ob = text(f"say_{body[:5]}_{random.randint(0, 999)}", body, loc, size,
              mat("bub" + str(col), col, 0.4, emit=col, estr=3.0), rot=rot, extrude=0.08)
    sets.set_obj_visible(ob, t0 - 0.05, False)
    sets.set_obj_visible(ob, t0, True)
    sets.set_obj_visible(ob, t1, False)
    ob.scale = (0.2, 0.2, 0.2)
    ob.keyframe_insert("scale", frame=F(t0))
    ob.scale = (1.15, 1.15, 1.15)
    ob.keyframe_insert("scale", frame=F(t0 + 0.12))
    ob.scale = (1, 1, 1)
    ob.keyframe_insert("scale", frame=F(t0 + 0.25))
    return ob


def grandpa(t0, t1, expr="shock"):
    G = chars.Char("Grandpa", skin="#efd9c0", shirt="#7a5a3a", pants="#4a3f30", hair="bald", face="mustache", sleeves="long",
                   extras=("glasses", "beard"))
    return story._live(G, t0, t1, expr)


def doctor(t0, t1, expr="neutral"):
    D_ = chars.Char("Doctor", skin="#e9c7a6", shirt="#f4f4f4", pants="#7fa0c0", hair="short", hair_color="#3a2a1e", face="mustache",
                    sleeves="long", extras=("glasses",))
    return story._live(D_, t0, t1, expr)


def priest(t0, t1, expr="neutral"):
    P = chars.Char("Priest", skin="#efd9c0", shirt="#1a1a1e", pants="#1a1a1e", hair="bald", face="mustache", sleeves="long",
                   extras=("collar:#ffffff",))
    return story._live(P, t0, t1, expr)


def church_set():
    room("#e6dcc8", "#6a4a32", key=6500)
    box("altar", (8, 3, 3.2), (0, 9.5, 1.6), wood("wood_alt", "#7d4f32", "#b07a52", 2.0), 0.05)
    box("cross_v", (0.6, 0.5, 6.0), (0, 11.6, 8.5), M("#d9b24a", 0.3, metal=0.7), 0.05)
    box("cross_h", (3.2, 0.5, 0.6), (0, 11.6, 9.6), M("#d9b24a", 0.3, metal=0.7), 0.05)
    box("win", (4.5, 0.3, 7.0), (8, 11.7, 7.0), mat("stain", (0.9, 0.5, 0.3), 0.3, emit=(0.95, 0.5, 0.3), estr=2.0), 0.05)
    for i, y in enumerate((-4, -8)):
        for sx in (-1, 1):
            box(f"pew{i}{sx}", (5, 1.4, 2.2), (sx * 6, y, 1.1), wood("wood_pew", "#6e4229", "#a06a45", 2.0), 0.05)


def doctor_set():
    room("#d6e8ee", "#c8d2d8", key=8000)
    box("bed", (5, 9, 1.6), (4, 6, 1.0), M("#f4f4f4", 0.8), 0.15)
    box("bedp", (4.6, 2, 0.5), (4, 9.5, 2.0), M("#cfe0f0", 0.9), 0.2)
    box("cab", (6, 2, 7), (-9, 10.5, 3.5), wood("wood_cab", "#8a8f98", "#a0a6ae", 2.0), 0.05)
    box("cross", (1.6, 0.2, 0.5), (-9, 9.4, 8.0), M("#d93a3a", 0.4), 0.02)
    box("cross2", (0.5, 0.2, 1.6), (-9, 9.4, 8.0), M("#d93a3a", 0.4), 0.02)


def home_set():
    room("#e8cfa8", "#a86a44", key=5200)
    box("sofa", (9, 3, 2.4), (-5, 8.5, 1.2), M("#a8523a", 0.8), 0.3)
    box("rug", (10, 8, 0.08), (2, 2, 0.05), M("#7a9ad0", 0.9), 0)
    box("lamp_b", (0.8, 0.8, 5), (7, 9, 2.5), M("#4a3a2a", 0.6), 0.1)
    sphere("lamp_s", 1.1, (7, 9, 5.6), mat("lampshade", (1, 0.85, 0.5), 0.5, emit=(1, 0.8, 0.45), estr=2.5))
    light("lamp_l", "POINT", (7, 8, 5.5), 600, (1.0, 0.75, 0.4), 0.6)


def cat_prop(loc, rot=0, scale=0.7, color="#f0a040"):
    return W2.cat("cat" + str(random.randint(0, 999)), loc, None, color, rot, True, scale)


def hood_on_chest(T):
    sphere("hood_f", 0.75, (0, -0.65, 1.7), M("#6a3fb0", 0.7), (1.2, 0.45, 0.8), parent=T.hip, coll=T.coll)


def push_cam(t0, t1, target, d0, d1, yaw=0.0, yaw1=None, pitch=4.0, lens=28, lens1=None, hh=1.2):
    cam = Cam()
    cam.push(t0, t1, target, d0, d1, yaw=yaw, pitch=pitch, lens=lens, yaw1=yaw if yaw1 is None else yaw1, lens1=lens if lens1 is None else lens1)
    cam.handheld(hh)
    return cam


EDDIE_P = (0.0, -10.0, 0.0)
EH = (0.0, -10.0, 4.7)


def zzz(t0, t1, loc, n=3):
    for i in range(n):
        ob = text(f"zz{i}_{random.randint(0, 999)}", "Z", (loc[0] + i * 0.7, loc[1], loc[2] + i * 0.9), 0.9 - i * 0.12,
                  mat("zzm", (0.8, 0.9, 1), 0.4, emit=(0.8, 0.9, 1), estr=3.0), rot=(90, 0, 0))
        ob.keyframe_insert("location", frame=F(t0 + i * 0.25))
        ob.location[2] += 1.8
        ob.keyframe_insert("location", frame=F(t0 + i * 0.25 + 1.6))
        sets.set_obj_visible(ob, t0 + i * 0.25 - 0.05, False)
        sets.set_obj_visible(ob, t0 + i * 0.25, True)


def woods(back=True):
    rnd = random.Random(4)
    for i in range(46):
        x, y = rnd.uniform(-40, 40), rnd.uniform(46, 80)
        h = rnd.uniform(9, 16)
        cyl(f"tr{i}", 0.5, h, (x, y, h / 2), M("#241a16", 0.9), 8)
        sphere(f"trc{i}", rnd.uniform(3, 5), (x, y, h + 1), M("#16241c", 0.9), (1, 1, 1.4), seg=10)


# ================================================================== pip-story helpers
def hero(t0, t1, expr="neutral"):
    """The narrator: green hoodie kid with a hood on his back."""
    K = chars.Char("Max", skin="#e9c39e", shirt="#4fbf5a", pants="#2f3f6a", hair="short", hair_color="#3a2a1e", face="kid",
                   vneck="#8fe39a")
    box("Max_hood", (1.8, 0.9, 1.1), (0, 0.8, 2.6), M("#3d9a48", 0.7), 0.3, parent=K.hip, coll=K.coll)
    return story._live(K, t0, t1, expr)


def eyeball(name, parent, loc, r=0.16, col="#ffffff", pupil=0.07):
    sphere(name, r, loc, M(col, 0.3), parent=parent)
    sphere(name + "p", pupil, (loc[0], loc[1] - r * 0.85, loc[2]), M("#111111", 0.3), parent=parent)


def pip(loc, s=1.0, name="Pip", parent=None, tooth=True):
    """Potato-sized one-toothed green monster."""
    root = empty(name, loc, parent=parent)
    root.scale = (s,) * 3
    body = sphere(name + "_b", 0.9, (0, 0, 0.8), M("#8fd18c", 0.6), (1.0, 0.85, 0.9), parent=root)
    for sx in (-1, 1):
        eyeball(f"{name}_e{sx}", root, (sx * 0.34, -0.66, 1.05), 0.26, "#ffffff", 0.12)
        sphere(f"{name}_ear{sx}", 0.28, (sx * 0.62, 0, 1.55), M("#6fb36c", 0.6), (0.6, 0.5, 1.0), parent=root)
    box(name + "_m", (0.5, 0.1, 0.12), (0, -0.82, 0.55), M("#2a1a1a", 0.5), 0.03, parent=root)
    if tooth:
        box(name + "_t", (0.14, 0.1, 0.22), (0.08, -0.84, 0.44), M("#ffffff", 0.3), 0.02, parent=root)
    for sx in (-1, 1):
        sphere(f"{name}_f{sx}", 0.22, (sx * 0.4, -0.2, 0.12), M("#6fb36c", 0.6), (1, 1.2, 0.6), parent=root)
    return root


def grow(ob, t0, t1, s0, s1, ease="EASE_IN_OUT"):
    ob.scale = (s0,) * 3
    ob.keyframe_insert("scale", frame=F(t0))
    ob.scale = (s1,) * 3
    ob.keyframe_insert("scale", frame=F(t1))
    set_interp(ob, "scale", F(t0), "BEZIER", ease)


def shiver(ob, t0, t1, amp=0.05, rate=14):
    t, k = t0, 0
    base = ob.location.copy()
    while t < t1:
        ob.location = (base[0] + amp * (-1) ** k, base[1], base[2])
        ob.keyframe_insert("location", frame=F(t))
        t += 1.0 / rate
        k += 1
    ob.location = base
    ob.keyframe_insert("location", frame=F(t1))


def hop(ob, t, h=1.0, dur=0.4):
    b = ob.location.copy()
    ob.location = b
    ob.keyframe_insert("location", frame=F(t))
    ob.location = (b[0], b[1], b[2] + h)
    ob.keyframe_insert("location", frame=F(t + dur * 0.5))
    ob.location = b
    ob.keyframe_insert("location", frame=F(t + dur))


def bear(loc, s=1.0, name="Bear", pack=True):
    root = empty(name, loc)
    root.scale = (s,) * 3
    Mb = M("#7a4a2a", 0.8)
    box(name + "_body", (4.4, 3.2, 4.2), (0, 0, 3.4), Mb, 0.8, parent=root)
    box(name + "_head", (3.2, 2.8, 2.6), (0, -0.2, 6.6), Mb, 0.7, parent=root)
    for sx in (-1, 1):
        sphere(f"{name}_ear{sx}", 0.6, (sx * 1.4, 0, 8.1), Mb, parent=root)
        box(f"{name}_arm{sx}", (1.3, 1.3, 3.4), (sx * 2.9, -0.2, 3.6), Mb, 0.4, parent=root)
        box(f"{name}_leg{sx}", (1.5, 1.6, 2.0), (sx * 1.1, 0, 1.0), Mb, 0.4, parent=root)
    for i, x in enumerate((-0.9, 0, 0.9)):
        eyeball(f"{name}_eye{i}", root, (x, -1.5, 6.9 + (0.25 if i == 1 else 0)), 0.34, "#ffe96a", 0.14)
    box(name + "_snout", (1.4, 0.8, 1.0), (0, -1.7, 6.0), M("#c89a6a", 0.8), 0.3, parent=root)
    sphere(name + "_nose", 0.25, (0, -2.2, 6.2), M("#111111", 0.3), parent=root)
    if pack:
        box(name + "_pack", (2.6, 1.2, 2.8), (0, 2.0, 3.8), M("#e2582a", 0.6), 0.3, parent=root)
    return root


def lizard(loc, s=1.0, name="Lizard", fire=True):
    root = empty(name, loc)
    root.scale = (s,) * 3
    Mo = M("#ff7a2a", 0.5)
    box(name + "_body", (1.6, 4.0, 1.5), (0, 0, 1.4), Mo, 0.5, parent=root)
    box(name + "_head", (1.5, 1.8, 1.2), (0, -2.6, 1.9), Mo, 0.4, parent=root)
    box(name + "_tail", (0.7, 3.4, 0.6), (0, 3.4, 1.0), Mo, 0.3, parent=root, rot=(10, 0, 0))
    for sx in (-1, 1):
        for sy in (-1.2, 1.2):
            box(f"{name}_l{sx}{sy}", (0.5, 0.6, 1.2), (sx * 1.0, sy, 0.6), Mo, 0.2, parent=root)
        eyeball(f"{name}_e{sx}", root, (sx * 0.45, -3.2, 2.2), 0.2, "#ffffff", 0.09)
    for i in range(5):
        box(f"{name}_sp{i}", (0.2, 0.4, 0.5), (0, -1.0 + i * 0.9, 2.4), M("#ffd23a", 0.4), 0.05, parent=root)
    if fire:
        sphere(name + "_flame", 0.55, (0, 6.3, 1.4), mat("flame_o", (1, 0.55, 0.1), 0.3, emit=(1, 0.5, 0.1), estr=14.0), (1, 1, 1.5), parent=root)
    return root


def skunk(loc, s=1.0, name="Skunk"):
    root = empty(name, loc)
    root.scale = (s,) * 3
    Mk = M("#1a1a1e", 0.8)
    sphere(name + "_body", 1.6, (0, 0, 1.6), Mk, (1.2, 1.5, 0.9), parent=root)
    box(name + "_stripe", (0.6, 3.6, 0.12), (0, 0, 2.9), M("#ffffff", 0.7), 0.03, parent=root)
    sphere(name + "_head", 1.0, (0, -2.3, 1.9), Mk, parent=root)
    sphere(name + "_tail", 1.5, (0, 2.8, 2.8), M("#f4f4f4", 0.8), (0.7, 0.9, 1.6), parent=root)
    for sx in (-1, 1):
        eyeball(f"{name}_e{sx}", root, (sx * 0.4, -3.1, 2.2), 0.2, "#ffffff", 0.09)
        box(f"{name}_l{sx}", (0.6, 0.6, 1.0), (sx * 0.9, -1.2, 0.5), Mk, 0.15, parent=root)
    return root


def devourer(loc, s=1.0, name="Dev"):
    root = empty(name, loc)
    root.scale = (s,) * 3
    Md = mat("devm", (0.02, 0.02, 0.03), 0.9, emit=(0.05, 0.02, 0.1), estr=0.4)
    rnd = random.Random(3)
    sphere(name + "_core", 4.0, (0, 0, 7), Md, (1.2, 1.0, 1.7), parent=root)
    for i in range(9):
        ob = sphere(f"{name}_puff{i}", rnd.uniform(1.8, 3.2), (rnd.uniform(-4, 4), rnd.uniform(-2, 2), rnd.uniform(2, 15)), Md, parent=root)
        noise(ob, "location", 0, 0.7, 30)
        noise(ob, "location", 2, 0.9, 40)
    Me = mat("dev_eye", (1, 0.1, 0.1), 0.3, emit=(1, 0.1, 0.1), estr=16.0)
    for sx in (-1, 1):
        sphere(f"{name}_eye{sx}", 0.7, (sx * 1.6, -3.4, 10.5), Me, (1, 0.6, 1.4), parent=root)
    Mt = M("#f4f4f2", 0.4)
    for i in range(10):
        x = -3.2 + i * 0.72
        for z, rot in ((6.2, 0), (4.6, 180)):
            cyl(f"{name}_tooth{i}{z}", 0.32, 1.6, (x, -3.7, z), Mt, 8, parent=root, rot=(rot, 0, 0), r2=0.02)
    return root


def mon_crowd(t0, t1, n=10, seed=2, area=((-18, 18), (-40, -22)), run_to=(0, -60)):
    rnd = random.Random(seed)
    cols = ["#7a4a2a", "#ff7a2a", "#8fd18c", "#6a7ae0", "#d06aa0"]
    out = []
    for i in range(n):
        x, y = rnd.uniform(*area[0]), rnd.uniform(*area[1])
        r = empty(f"mon{seed}_{i}", (x, y, 0))
        c = cols[i % 5]
        sphere(f"mon{seed}_{i}b", 1.3, (0, 0, 1.4), M(c, 0.6), (1, 1, 1.1), parent=r)
        for sx in (-1, 1):
            eyeball(f"mon{seed}_{i}e{sx}", r, (sx * 0.5, -1.15, 1.9), 0.3, "#ffffff", 0.12)
        r.keyframe_insert("location", frame=F(t0))
        r.location = (x + rnd.uniform(-8, 8), run_to[1] - rnd.uniform(0, 15), 0)
        r.keyframe_insert("location", frame=F(t1))
        noise(r, "location", 2, 0.5, 6)
        out.append(r)
    return out


def sparkles(t0, center, n=28, spread=3.0, seed=1, dur=1.6):
    rnd = random.Random(seed)
    Ms = mat("spark_y", (1, 0.9, 0.4), 0.3, emit=(1, 0.85, 0.3), estr=8.0)
    for i in range(n):
        a = rnd.uniform(0, math.tau)
        r = rnd.uniform(0.4, spread)
        ob = sphere(f"sp{seed}_{i}", rnd.uniform(0.06, 0.16), center, Ms)
        ob.keyframe_insert("location", frame=F(t0))
        ob.location = (center[0] + math.cos(a) * r, center[1] + rnd.uniform(-1, 1), center[2] + math.sin(a) * r + rnd.uniform(0, 2))
        ob.keyframe_insert("location", frame=F(t0 + dur))
        sets.set_obj_visible(ob, t0 - 0.05, False)
        sets.set_obj_visible(ob, t0, True)


def day_street():
    return town_scene()


def night_forest():
    night_street(night=True, fog=False, lamps=True, houses=True)
    woods()


def siren(t0, t1):
    """Pulsing red light + sound."""
    L = light("siren", "POINT", (0, -20, 14), 4000, (1.0, 0.1, 0.1), 2.0)
    t = t0
    k = 0
    while t < t1:
        L.data.energy = 6000 if k % 2 == 0 else 200
        L.data.keyframe_insert("energy", frame=F(t))
        t += 0.3
        k += 1


# ================================================================== PART 1: monsters of the town (0-35s)
@S(1, 0, 3, "HOOK: Tootie strolls with his giant three-eyed bear, whip + push")
def p01(t0, t1):
    day_street()
    B = bear((6, -30, 0), 1.0, "bearH", pack=True)
    B.keyframe_insert("location", frame=F(t0))
    B.location = (3, -36, 0)
    B.keyframe_insert("location", frame=F(t1))
    T = tootie(t0, t1, "grin")
    T.walk(t0, t1, (-1.5, -28, 0), (-1.5, -36, 0), rate=2.4)
    cam = Cam()
    cam.key(t0, (-9, -52, 2.0), (3, -30, 5), lens=22, focus=(3, -30, 5), fstop=4)
    cam.key(t1, (6, -50, 5.0), (1, -36, 5), lens=26, focus=(1, -36, 5), fstop=4, ease="EASE_OUT")
    cam.crash(t0 + 1.6, 26, 32, 0.12)
    cam.handheld(1.3)
    sfx(t0, "whoosh")
    sfx(t0 + 0.9, "stomp", 0.8)
    sfx(t0 + 1.6, "stomp", 0.8)


@beat(3, 13, n=3, focus=(0, -32, 4.2), d=14, lens=26, desc="Every kid gets a monster bodyguard on their tenth birthday: party, box, poof")
def p02(t0, t1):
    day_street()
    box("table", (6, 3, 0.3), (0, -32, 3.2), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0.05)
    cyl("cake", 1.3, 1.2, (0, -32, 4.1), M("#f09ac2", 0.6), 24)
    text("ten", "10", (0, -33.4, 4.6), 1.2, mat("ten_y", (1, 0.85, 0.2), 0.4, emit=(1, 0.8, 0.2), estr=2.0), rot=(90, 0, 0), extrude=0.15)
    K = hero(t0, t1, "happy")
    K.pose(t0, loc=(0, -36, 0), rot=0)
    K.act(t0 + 0.6, "cheer", expr="joy")
    gift = box("gift", (2.2, 2.2, 2.2), (3.4, -34, 1.1), M("#6a7ae0", 0.5), 0.1)
    box("giftrb", (2.3, 0.4, 2.3), (3.4, -34, 1.1), M("#ffd23a", 0.4), 0.05)
    confetti("cf", (0, -34, 6), (6, 3, 4), t0 + 0.2, 1.8, 60, 2, 10)
    sparkles(t0 + 3.2, (3.4, -34, 3.0), 30, 3.0, 4)
    P = pip((3.4, -34, 2.2), 1.0)
    grow(P, t0 + 3.0, t0 + 3.3, 0.01, 1.0)
    cam = push_cam(t0, t1, (1, -34, 3.6), 16, 10, yaw=-14, yaw1=14, lens=26, hh=1.2)
    sfx(t0 + 0.2, "confetti")
    sfx(t0 + 0.4, "cheer", 0.6)
    sfx(t0 + 3.0, "poof")
    sfx(t0 + 3.1, "sparkle")


@beat(13, 22, n=2, focus=(0, -32, 4.4), d=15, lens=26, desc="It follows you everywhere and protects you from anything")
def p03(t0, t1):
    day_street()
    K = townie(2, t0, t1, "worried")
    K.pose(t0, loc=(-2, -30, 0), rot=0)
    B = bear((3.5, -28, 0), 0.8, "bearP", pack=False)
    G = gus(t0, t1, "angry", loc=(-12, -40, 0), rot=-60)
    G.walk(t0 + 0.4, t0 + 2.6, (-12, -40, 0), (-4, -32, 0), rate=2.4)
    G.pose(t0 + 3.0, loc=(-4, -32, 0))
    G.pose(t0 + 3.8, loc=(-14, -44, 0), rot=-60)
    grow(B, t0 + 2.6, t0 + 2.8, 0.8, 1.1)
    cam = push_cam(t0, t1, (0, -32, 4.4), 18, 11, yaw=10, yaw1=-12, lens=24, hh=1.3)
    sfx(t0 + 0.6, "footsteps", 0.6)
    sfx(t0 + 2.8, "boom", 0.7)
    sfx(t0 + 3.2, "gasp")


@S(4, 22, 30, "Tootie got a giant bear with three eyes: bear reveal, three eyes, crash zoom")
def p04(t0, t1):
    day_street()
    B = bear((0, -30, 0), 1.0, "bear3", pack=False)
    T = tootie(t0, t1, "grin")
    T.pose(t0, loc=(4.5, -33, 0), rot=-30)
    T.act(t0 + 0.4, "point", expr="grin")
    cam = Cam()
    cam.key(t0, (0, -48, 1.2), (0, -30, 5), lens=22, focus=(0, -30, 5), fstop=4)
    cam.key(t0 + 2.0, (0, -44, 5.0), (0, -30, 6.6), lens=26, focus=(0, -30, 6.6), fstop=3)
    cam.key(t1, (0, -38, 6.6), (0, -31.5, 6.9), lens=34, focus=(0, -31.5, 6.9), fstop=3, ease="EASE_IN")
    cam.crash(t0 + 1.2, 26, 36, 0.1)
    cam.handheld(1.0)
    sfx(t0, "stomp", 0.9)
    sfx(t0 + 1.2, "boom")
    sfx(t0 + 1.3, "sting")


@S(5, 30, 34, "It carries his backpack: bear lumbers, backpack bounces")
def p05(t0, t1):
    day_street()
    B = bear((0, -26, 0), 0.9, "bearK", pack=True)
    B.keyframe_insert("location", frame=F(t0))
    B.location = (0, -38, 0)
    B.keyframe_insert("location", frame=F(t1))
    noise(B, "location", 2, 0.4, 7)
    T = tootie(t0, t1, "smug")
    T.walk(t0, t1, (-5, -26, 0), (-5, -38, 0), rate=2.4)
    cam = Cam()
    cam.key(t0, (8, -20, 3.5), (0, -26, 4.5), lens=24, focus=(0, -26, 4.5), fstop=5)
    cam.key(t1, (10, -36, 3.8), (0, -38, 4.5), lens=24, focus=(0, -38, 4.5), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    for i in range(3):
        sfx(t0 + 0.2 + i * 1.1, "stomp", 0.7)


@S(6, 34, 39, "Eddie got a fire lizard: lizard roars a flame")
def p06(t0, t1):
    day_street()
    L = lizard((0, -30, 0), 1.0, "liz1")
    E = eddie(t0, t1, "grin")
    E.pose(t0, loc=(4.4, -33, 0), rot=-35)
    E.act(t0 + 0.4, "cheer", expr="grin")
    light("fl", "POINT", (0, -34, 4), 2200, (1.0, 0.55, 0.15), 1.5)
    cam = push_cam(t0, t1, (0, -30, 3.0), 16, 9, yaw=-18, yaw1=14, lens=26, hh=1.4)
    cam.crash(t0 + 1.4, 26, 36, 0.1)
    sfx(t0 + 1.4, "boom", 0.6)
    sfx(t0 + 1.5, "jet", 0.7)


@S(7, 39, 43, "Nobody bullies Eddie anymore: Gus runs away from a flamethrower tail")
def p07(t0, t1):
    day_street()
    L = lizard((0, -30, 0), 1.0, "liz2")
    G = gus(t0, t1, "terror", loc=(-3, -36, 0), rot=60)
    G.run(t0 + 0.5, t1, (-3, -36, 0), (-18, -50, 0))
    G.panic(t0 + 0.5, t1, rate=7)
    light("fl", "POINT", (0, -34, 4), 2200, (1.0, 0.55, 0.15), 1.5)
    cam = push_cam(t0, t1, (-4, -34, 3.0), 14, 10, yaw=-12, yaw1=14, lens=24, hh=1.8)
    sfx(t0 + 0.2, "jet", 0.7)
    sfx(t0 + 0.7, "gasp")
    sfx(t0 + 1.2, "whoosh")


@S(8, 43, 49, "Principal Fartan got a skunk monster: principal and skunk")
def p08(t0, t1):
    day_street()
    S_ = skunk((3, -30, 0), 1.1, "sk1")
    P = fartan(t0, t1, "happy")
    P.pose(t0, loc=(-2, -31, 0), rot=15)
    P.act(t0 + 0.4, "cheer", expr="happy")
    cam = push_cam(t0, t1, (0, -31, 3.4), 16, 10, yaw=-14, yaw1=12, lens=26, hh=1.2)
    sfx(t0 + 0.3, "ding", 0.6)
    sfx(t0 + 1.2, "squeak", 0.6)


@S(9, 49, 55, "And honestly, that explains a lot: green stink cloud, townies hold their noses")
def p09(t0, t1):
    day_street()
    S_ = skunk((0, -30, 0), 1.1, "sk2")
    Mg = mat("stink", (0.5, 0.85, 0.2), 0.9, emit=(0.4, 0.8, 0.15), estr=0.6, alpha=0.5)
    for i in range(12):
        ob = sphere(f"st{i}", random.uniform(1.4, 2.6), (random.uniform(-2, 2), -27 + random.uniform(-1, 3), random.uniform(1.5, 3.5)), Mg, (1, 1, 0.8))
        ob.keyframe_insert("scale", frame=F(t0 + 1.2))
        ob.scale = (0.01,) * 3
        ob.keyframe_insert("scale", frame=F(t0 + 1.1))
        ob.scale = (1, 1, 1)
        ob.keyframe_insert("scale", frame=F(t0 + 2.2))
    ks = street_pair(t0, t1, 5, 4)
    for k in ks:
        k.act(t0 + 1.4, "recoil", expr="scream")
    P = fartan(t0, t1, "smug")
    P.pose(t0, loc=(-3, -33, 0), rot=15)
    cam = push_cam(t0, t1, (0, -30, 3.4), 15, 10, yaw=-12, yaw1=14, lens=26, hh=1.6)
    sfx(t0 + 1.1, "fart")
    sfx(t0 + 1.4, "gasp")
    sfx(t0 + 2.4, "rimshot", 0.6)


# ================================================================== PART 2: Pip (55-126)
@S(10, 55, 58, "I got Pip: kid holds Pip in his palm, closeup")
def p10(t0, t1):
    day_street()
    K = hero(t0, t1, "happy")
    K.pose(t0, loc=(0, -32, 0), rot=0)
    K.act(t0 + 0.2, "hold", expr="happy")
    P = pip((0.0, -34.2, 3.2), 0.5, "PipH")
    grow(P, t0, t0 + 0.4, 0.1, 0.5)
    cam = push_cam(t0, t1, (0, -33, 4.0), 10, 5.5, yaw=-16, yaw1=8, lens=30, lens1=36, hh=1.2)
    sfx(t0 + 0.1, "pop")
    sfx(t0 + 0.4, "aww", 0.7)


@S(11, 58, 65, "Pip is the size of a potato: a potato next to Pip")
def p11(t0, t1):
    world((0.9, 0.9, 0.85), 0.7)
    box("desk", (30, 30, 0.4), (0, 0, -0.2), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0)
    sphere("potato", 0.9, (2.2, 0, 0.7), M("#b08a5a", 0.9), (1.2, 0.9, 0.8))
    P = pip((-1.2, 0, 0.1), 0.9, "PipP")
    light("l1", "AREA", (0, -4, 8), 1600, (1, 0.97, 0.9), 6, target=(0, 0, 0))
    cam = Cam()
    cam.key(t0, (-3, -7, 3.0), (0, 0, 1.0), lens=30, focus=(0, 0, 1), fstop=2.2)
    cam.key(t1, (1.4, -5, 2.2), (0, 0, 1.0), lens=34, focus=(0, 0, 1), fstop=2.2, ease="EASE_IN_OUT")
    cam.handheld(0.8)
    sfx(t0 + 0.2, "aww")
    sfx(t0 + 2.4, "squeak", 0.8)


@beat(65, 79, n=2, focus=(0, -32, 4.4), d=9, lens=30, desc="He has one tooth and hides in my hood when a bird flies by")
def p12(t0, t1):
    day_street()
    K = hero(t0, t1, "worried")
    K.pose(t0, loc=(0, -32, 0), rot=0)
    P = pip((0.0, -34.0, 4.2), 0.55, "PipT")
    W.pigeon("pig", (-20, -30, 14))
    pg = bpy.data.objects.get("pig")
    pt0, pt1 = t0 + 3.4, t0 + 5.0
    if pg:
        pg.keyframe_insert("location", frame=F(pt0))
        pg.location = (-2, -33, 7)
        pg.keyframe_insert("location", frame=F(pt1))
    grow(P, t0 + 5.0, t0 + 5.3, 0.55, 0.01)
    P.location = (0.0, -34.0, 4.2)
    P.keyframe_insert("location", frame=F(t0 + 4.9))
    P.location = (0, -31.2, 4.8)
    P.keyframe_insert("location", frame=F(t0 + 5.3))
    cam = push_cam(t0, t1, (0, -33, 4.4), 10, 6.4, yaw=-14, yaw1=14, lens=30, lens1=36, hh=1.3)
    sfx(t0 + 1.6, "squeak", 0.5)
    sfx(t0 + 3.4, "pigeon", 0.8)
    sfx(t0 + 5.0, "whoosh", 0.6)


@S(13, 79, 88, "The whole class laughed at us for a week")
def p13(t0, t1):
    R, ks = class_scene(t0, t1, kids=8, board="chalk_joke.png")
    for k in ks:
        laugh(k, t0, t1, belly=True, flail=False, rate=5)
    K = hero(t0, t1, "cry")
    K.pose(t0, loc=(5, 12, 0), rot=0)
    K.act(t0 + 0.6, "slump", expr="cry")
    cam = push_cam(t0, t1, (6, 6, 4.6), 15, 10, yaw=0, yaw1=-10, lens=24, hh=1.4)
    sfx(t0, "kids_laugh")
    sfx(t0 + 1.4, "cheer", 0.4)
    sfx(t0 + 3.0, "kids_laugh", 0.8)


@S(14, 88, 94, "Rock and roll! We're losing control!")
def p14(t0, t1):
    day_street()
    T = tootie(t0, t1, "scream")
    T.pose(t0, loc=(2.2, -32, 0), rot=-15)
    T.panic(t0, t1, rate=7)
    K = hero(t0, t1, "scream")
    K.pose(t0, loc=(-2.2, -32, 0), rot=15)
    K.panic(t0 + 0.1, t1, rate=6)
    cam = push_cam(t0, t1, (0, -32, 4.4), 14, 8, yaw=-10, yaw1=12, lens=26, hh=2.8)
    sfx(t0, "whoosh")
    sfx(t0 + 0.9, "rimshot", 0.6)


@S(15, 94, 102, "Monsters grow when their kid believes in them: bear bigger with sparkles")
def p15(t0, t1):
    day_street()
    B = bear((0, -28, 0), 1.0, "bearG", pack=True)
    grow(B, t0 + 1.0, t1 - 0.5, 1.0, 1.8)
    T = tootie(t0, t1, "joy")
    T.pose(t0, loc=(5, -36, 0), rot=-30)
    T.act(t0 + 0.4, "cheer", expr="joy")
    sparkles(t0 + 1.0, (0, -34, 6), 36, 6.0, 5, 3.0)
    cam = Cam()
    cam.key(t0, (-12, -46, 3.0), (0, -28, 5), lens=22, focus=(0, -28, 6), fstop=6)
    cam.key(t1, (6, -50, 8.0), (0, -28, 9), lens=22, focus=(0, -28, 9), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 1.0, "rise")
    sfx(t0 + 1.2, "sparkle")
    sfx(t0 + 4.0, "stomp", 0.9)


@S(16, 102, 112, "Tootie's bear grew so big it sleeps on the roof: huge bear on the school, Zzz")
def p16(t0, t1):
    day_street()
    B = bear((0, 14, 17), 2.2, "bearR", pack=False)
    zzz(t0 + 0.5, t1, (-6, -12, 28), n=4)
    T = tootie(t0, t1, "smug")
    T.pose(t0, loc=(0, -30, 0), rot=0)
    T.act(t0 + 0.6, "shrug", expr="smug")
    cam = Cam()
    cam.key(t0, (-12, -52, 3), (0, 10, 18), lens=22, focus=(0, 10, 18), fstop=8)
    cam.key(t1, (10, -46, 12), (0, 10, 22), lens=22, focus=(0, 10, 22), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "ding", 0.5)
    for i in range(3):
        sfx(t0 + 0.6 + i * 1.4, "snort", 0.7)


@S(17, 112, 116, "But Pip stayed tiny")
def p17(t0, t1):
    day_street()
    K = hero(t0, t1, "worried")
    K.pose(t0, loc=(0, -32, 0), rot=0)
    P = pip((0.0, -31.2, 4.8), 0.5, "PipS")
    cam = push_cam(t0, t1, (0, -32, 4.6), 12, 7.5, yaw=14, yaw1=-8, lens=28, hh=1.0)
    sfx(t0 + 0.2, "squeak", 0.6)


@S(18, 116, 122, "Because I didn't believe in him: Max looks away from Pip")
def p18(t0, t1):
    day_street()
    K = hero(t0, t1, "bored")
    K.pose(t0, loc=(0, -32, 0), rot=0)
    look(K, t0 + 0.3, -50, 0)
    P = pip((0.0, -31.2, 4.8), 0.5, "PipS")
    P.keyframe_insert("location", frame=F(t0))
    cam = push_cam(t0, t1, (0, -32, 4.6), 9, 6, yaw=-12, yaw1=12, lens=30, lens1=36, hh=1.0)
    sfx(t0 + 0.3, "sting", 0.6)


@S(19, 122, 126, "Not even a little: Pip's sad eyes, tiny")
def p19(t0, t1):
    day_street()
    P = pip((0, -34, 3.0), 1.4, "PipC")
    cam = Cam()
    cam.key(t0, (-1, -42, 3.4), (0, -34, 3.2), lens=36, focus=(0, -34, 3.2), fstop=2.2)
    cam.key(t1, (0.2, -39, 3.2), (0, -34, 3.2), lens=44, focus=(0, -34, 3.2), fstop=2.2, ease="EASE_IN")
    cam.handheld(0.8)
    sfx(t0, "aww", 0.8)
    sfx(t0 + 0.8, "crickets", 0.6)


# ================================================================== PART 3: the Devourer (126-209)
@S(20, 126, 133, "Then one night, the sirens went off")
def p20(t0, t1):
    night_street(night=True, fog=False)
    siren(t0, t1)
    ks = street_pair(t0, t1, 6, 3)
    for k in ks:
        k.face(t0, "gasp")
    cam = Cam()
    cam.key(t0, (0, -46, 3.0), (0, -20, 14), lens=22, focus=(0, -20, 12), fstop=8)
    cam.key(t1, (0, -40, 9), (0, -20, 14), lens=24, focus=(0, -20, 12), fstop=8, ease="EASE_OUT")
    cam.handheld(1.4)
    sfx(t0, "alarm")
    sfx(t0 + 2.4, "alarm", 0.8)
    sfx(t0 + 0.4, "gasp", 0.7)


@beat(133, 150, n=3, focus=(0, 48, 14), d=44, lens=24, desc="The Devourer came out of the forest, taller than the school, made of black smoke and teeth", pitch=4)
def p21(t0, t1):
    night_forest()
    siren(t0, t1)
    D = devourer((0, 56, 0), 1.4, "Dev")
    D.keyframe_insert("location", frame=F(t0))
    D.location = (0, 30, 0)
    D.keyframe_insert("location", frame=F(t1 + 1.0))
    cam = Cam()
    cam.key(t0, (-4, -8, 3.0), (0, 40, 12), lens=22, focus=(0, 40, 12), fstop=8)
    cam.key(t1, (4, -4, 6.0), (0, 40, 14), lens=22, focus=(0, 40, 14), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0, "zombie", 0.7)
    sfx(t0 + 0.4, "alarm", 0.7)
    sfx(t0 + 1.8, "boom", 0.8)
    sfx(t0 + 3.4, "boom", 0.8)


@S(22, 150, 158, "It swallowed the fire lizard in one bite: chomp")
def p22(t0, t1):
    night_forest()
    D = devourer((0, 14, 0), 1.0, "Dev2")
    L = lizard((0, -4, 0), 0.9, "liz3")
    L.keyframe_insert("scale", frame=F(t0 + 3.5))
    L.scale = (0.01,) * 3
    L.keyframe_insert("scale", frame=F(t0 + 3.7))
    cam = Cam()
    cam.key(t0, (6, -16, 4.0), (0, 4, 5.0), lens=24, focus=(0, 4, 5), fstop=6)
    cam.key(t1, (4, -12, 3.6), (0, 6, 5.5), lens=30, focus=(0, 6, 5.5), fstop=5, ease="EASE_IN")
    cam.crash(t0 + 3.4, 30, 42, 0.1)
    cam.handheld(1.8)
    sfx(t0 + 0.4, "jet", 0.7)
    sfx(t0 + 3.5, "boom")
    sfx(t0 + 3.55, "thud")
    sfx(t0 + 3.6, "stomp")


@S(23, 158, 163, "Tootie's bear ran away screaming")
def p23(t0, t1):
    night_forest()
    B = bear((0, -8, 0), 1.0, "bearF", pack=True)
    B.keyframe_insert("location", frame=F(t0))
    B.location = (0, -50, 0)
    B.keyframe_insert("location", frame=F(t1))
    noise(B, "location", 2, 0.6, 5)
    T = tootie(t0, t1, "scream")
    T.run(t0, t1, (-3, -10, 0), (-3, -50, 0))
    T.panic(t0, t1, rate=7)
    cam = Cam()
    cam.key(t0, (10, -12, 4.0), (0, -10, 5), lens=22, focus=(0, -10, 5), fstop=6)
    cam.key(t1, (12, -44, 4.5), (0, -48, 5), lens=22, focus=(0, -48, 5), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(2.2)
    sfx(t0, "stomp", 0.9)
    sfx(t0 + 0.5, "whoosh")
    sfx(t0 + 1.0, "stomp", 0.9)
    sfx(t0 + 1.6, "stomp", 0.9)
    sfx(t0 + 0.8, "gasp")


@S(24, 163, 171, "Every monster in town ran. Every single one: stampede")
def p24(t0, t1):
    night_forest()
    mon_crowd(t0, t1, 18, 2, area=((-18, 18), (-6, 14)), run_to=(0, -50))
    cam = Cam()
    cam.key(t0, (0, -30, 12), (0, 0, 2), lens=22, focus=(0, 0, 2), fstop=8)
    cam.key(t1, (6, -38, 7), (0, -30, 1.5), lens=22, focus=(0, -30, 1.5), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(2.2)
    sfx(t0, "stomp", 0.9)
    sfx(t0 + 0.2, "crowd")
    sfx(t0 + 1.2, "whoosh")
    sfx(t0 + 3.4, "stomp", 0.8)


@S(25, 171, 173, "Except Pip: the street is empty, Pip stands alone")
def p25(t0, t1):
    night_forest()
    K = hero(t0, t1, "terror")
    K.pose(t0, loc=(0, -14, 0), rot=0)
    P = pip((0.0, -12.2, 4.8), 0.5, "PipE")
    cam = Cam()
    cam.key(t0, (4, -24, 3.4), (0, -12, 4.8), lens=26, focus=(0, -12, 4.8), fstop=4)
    cam.key(t1, (1.2, -19, 4.8), (0, -12, 4.8), lens=34, focus=(0, -12, 4.8), fstop=3, ease="EASE_IN")
    cam.crash(t0 + 0.2, 26, 36, 0.1)
    cam.handheld(1.0)
    sfx(t0, "sting")
    sfx(t0 + 0.1, "crickets", 0.6)


@beat(173, 189, n=2, focus=(0, -14, 3.0), d=10, lens=28, desc="He climbed out of my hood, jumped to the ground, and stood in front of me", pitch=3)
def p26(t0, t1):
    night_forest()
    K = hero(t0, t1, "worried")
    K.pose(t0, loc=(0, -14, 0), rot=0)
    P = pip((0.0, -12.2, 4.8), 0.5, "PipJ")
    P.keyframe_insert("location", frame=F(t0 + 1.0))
    P.location = (-0.6, -13.0, 7.0)
    P.keyframe_insert("location", frame=F(t0 + 1.7))
    P.location = (0.0, -16.6, 0.2)
    P.keyframe_insert("location", frame=F(t0 + 2.3))
    grow(P, t0 + 2.3, t0 + 2.4, 0.5, 0.8)
    D = devourer((0, 22, 0), 1.2, "Dev3")
    cam = Cam()
    cam.key(t0, (4, -22, 5.0), (0, -14, 5), lens=26, focus=(0, -14, 5), fstop=4)
    cam.key(t1, (0.5, -26, 2.2), (0, -14, 2.4), lens=26, focus=(0, -16.6, 1.5), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.3)
    sfx(t0 + 1.0, "pop", 0.8)
    sfx(t0 + 2.2, "thud", 0.7)
    sfx(t0 + 3.4, "sting", 0.7)


@S(27, 189, 192, "Shaking, tiny, alone: Pip trembles")
def p27(t0, t1):
    night_forest()
    P = pip((0, -16.6, 0.2), 0.9, "PipSh")
    shiver(P, t0, t1, 0.08, 16)
    cam = Cam()
    cam.key(t0, (1.5, -22, 2.0), (0, -16.6, 1.2), lens=32, focus=(0, -16.6, 1.2), fstop=2.4)
    cam.key(t1, (0.3, -19.5, 1.6), (0, -16.6, 1.2), lens=42, focus=(0, -16.6, 1.2), fstop=2.4, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0, "rise", 0.7)


@S(28, 192, 200, "The Devourer looked down at him and laughed: looming face, teeth")
def p28(t0, t1):
    night_forest()
    D = devourer((0, -4, 0), 1.3, "Dev4")
    P = pip((0, -16.6, 0.2), 0.9, "PipSh2")
    shiver(P, t0, t1, 0.06, 16)
    cam = Cam()
    cam.key(t0, (0, -26, 2.2), (0, 0, 9), lens=22, focus=(0, -3, 9), fstop=5)
    cam.key(t1, (0, -24, 1.8), (0, 0, 12), lens=24, focus=(0, -3, 11), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.8)
    sfx(t0 + 0.4, "zombie", 0.8)
    sfx(t0 + 1.2, "boom", 0.6)
    sfx(t0 + 2.4, "kids_laugh", 0.5)
    sfx(t0 + 3.0, "boom", 0.6)


@S(29, 200, 209, "And Pip squeaked the bravest squeak I've ever heard: SQUEAK!")
def p29(t0, t1):
    night_forest()
    P = pip((0, -16.6, 0.2), 1.1, "PipB")
    P.keyframe_insert("scale", frame=F(t0))
    grow(P, t0 + 0.6, t0 + 1.6, 1.1, 1.5)
    bubble(t0 + 0.9, t1, (0, -17.5, 5.5), "SQUEAK!", (1, 0.95, 0.5), 2.0)
    D = devourer((0, -4, 0), 1.2, "Dev5")
    cam = Cam()
    cam.key(t0, (3, -24, 2.0), (0, -16.6, 1.5), lens=28, focus=(0, -16.6, 1.5), fstop=3)
    cam.key(t1, (0.4, -21, 2.2), (0, -16.6, 2.0), lens=40, focus=(0, -16.6, 2.0), fstop=3, ease="EASE_IN")
    cam.crash(t0 + 0.9, 28, 44, 0.1)
    cam.handheld(1.4)
    sfx(t0 + 0.9, "squeak")
    sfx(t0 + 0.95, "sting")
    sfx(t0 + 1.0, "boom", 0.6)
    sfx(t0 + 2.6, "aww", 0.6)


# ================================================================== PART 4: belief (209-end)
@S(30, 209, 213, "That's when I understood: Max's face, realization")
def p30(t0, t1):
    night_forest()
    K = hero(t0, t1, "gasp")
    K.pose(t0, loc=(0, -14, 0), rot=0)
    K.act(t0 + 0.6, "shock", expr="gasp")
    cam = push_cam(t0, t1, (0, -14, 4.8), 9, 5.0, yaw=-10, yaw1=8, lens=30, lens1=40, hh=1.4)
    cam.crash(t0 + 0.6, 30, 40, 0.1)
    sfx(t0 + 0.6, "ding")


@S(31, 213, 219, "He was never scared for himself: Pip shakes, but looks at the Devourer, not himself")
def p31(t0, t1):
    night_forest()
    P = pip((0, -16.6, 0.2), 1.3, "PipBrave")
    shiver(P, t0, t1, 0.05, 14)
    D = devourer((0, -4, 0), 1.2, "Dev6")
    cam = Cam()
    cam.key(t0, (-2, -24, 2.0), (0, -16.6, 1.5), lens=30, focus=(0, -16.6, 1.5), fstop=2.6)
    cam.key(t1, (-0.4, -21, 1.8), (0, -16.6, 1.8), lens=38, focus=(0, -16.6, 1.8), fstop=2.6, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0, "aww", 0.6)


@S(32, 219, 224, "He was scared for me: Max and Pip, Pip glances back")
def p32(t0, t1):
    night_forest()
    K = hero(t0, t1, "cry")
    K.pose(t0, loc=(0, -14, 0), rot=0)
    P = pip((0, -16.6, 0.2), 1.0, "PipLook")
    cam = Cam()
    cam.key(t0, (4, -26, 2.8), (0, -15, 2.4), lens=28, focus=(0, -15, 2.4), fstop=3)
    cam.key(t1, (1.5, -21, 3.2), (0, -15, 3.0), lens=34, focus=(0, -15, 3.0), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.2, "aww", 0.8)
    sfx(t0 + 2.0, "sparkle", 0.4)


@S(33, 224, 229, "So I believed in him: Max closes eyes, fists, warm glow starts")
def p33(t0, t1):
    night_forest()
    K = hero(t0, t1, "determined")
    K.pose(t0, loc=(0, -14, 0), rot=0)
    K.act(t0 + 0.2, "fists", expr="determined")
    K.face(t0 + 1.0, eyes="closed", mouth="flat")
    light("warm", "POINT", (0, -12, 6), 1500, (1.0, 0.8, 0.4), 1.5)
    cam = push_cam(t0, t1, (0, -14, 4.8), 10, 5.4, yaw=-12, yaw1=10, lens=30, lens1=38, hh=1.2)
    sfx(t0 + 0.2, "rise", 0.9)


@S(34, 229, 237, "With everything I had, Pip started to grow: sparkle and growth")
def p34(t0, t1):
    night_forest()
    K = hero(t0, t1, "determined")
    K.pose(t0, loc=(0, -14, 0), rot=0)
    P = pip((0, -16.6, 0.2), 1.0, "PipGrow")
    grow(P, t0 + 2.4, t1, 1.0, 3.2, "EASE_IN")
    sparkles(t0 + 1.6, (0, -16.6, 3.0), 40, 5.0, 6, 3.0)
    light("warm", "POINT", (0, -14, 5), 2400, (1.0, 0.8, 0.4), 1.5)
    cam = Cam()
    cam.key(t0, (4, -26, 2.4), (0, -16.6, 2.0), lens=26, focus=(0, -16.6, 2.0), fstop=4)
    cam.key(t1, (6, -30, 6.0), (0, -16.6, 4.5), lens=24, focus=(0, -16.6, 4.5), fstop=4, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    sfx(t0 + 1.6, "sparkle")
    sfx(t0 + 1.7, "rise")
    sfx(t0 + 3.2, "boom", 0.6)


@S(35, 237, 241, "Bigger than a car: Pip next to a car")
def p35(t0, t1):
    night_forest()
    W.car("car", (6, -16, 0), color="#d9453a")
    P = pip((-4, -16, 0.2), 3.2, "PipCar")
    grow(P, t0, t1, 3.2, 4.4)
    cam = push_cam(t0, t1, (0, -16, 4.0), 22, 16, yaw=-16, yaw1=14, lens=24, hh=1.6)
    sfx(t0, "boom", 0.6)
    sfx(t0 + 0.1, "stomp", 0.9)


@S(36, 241, 245, "Bigger than a house")
def p36(t0, t1):
    night_forest()
    house_front((10, -22, 0), w=12, h=10)
    P = pip((-6, -18, 0.2), 6.0, "PipHouse")
    grow(P, t0, t1, 6.0, 7.5)
    cam = push_cam(t0, t1, (0, -20, 8), 34, 26, yaw=-16, yaw1=14, lens=24, hh=1.6)
    sfx(t0, "boom", 0.7)
    sfx(t0 + 0.1, "stomp", 0.9)


@S(37, 245, 249, "Bigger than the Devourer: Pip towers over it")
def p37(t0, t1):
    night_forest()
    D = devourer((8, -4, 0), 1.0, "DevS")
    P = pip((-6, -16, 0.2), 11.0, "PipHuge")
    grow(P, t0, t1, 11.0, 14.0)
    cam = Cam()
    cam.key(t0, (-4, -58, 4.0), (-2, -6, 12), lens=22, focus=(-2, -6, 12), fstop=8)
    cam.key(t1, (4, -52, 12.0), (-2, -6, 14), lens=22, focus=(-2, -6, 14), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    sfx(t0, "boom")
    sfx(t0 + 0.2, "stomp")
    sfx(t0 + 1.8, "sting")


@S(38, 249, 259, "He opened his mouth with one giant tooth and roared: closeup, shockwave")
def p38(t0, t1):
    night_forest()
    P = pip((0, -20, 0.2), 14.0, "PipRoar")
    box("big_m", (4.6, 0.3, 2.0), (0, -20 - 11.4, 8.2), M("#2a0a0a", 0.5), 0.2)
    cam = Cam()
    cam.key(t0, (0, -60, 6.0), (0, -20, 11), lens=26, focus=(0, -30, 10), fstop=6)
    cam.key(t0 + 3.0, (0, -52, 9.0), (0, -34, 9.0), lens=30, focus=(0, -34, 9), fstop=4)
    cam.key(t1, (0, -45, 8.6), (0, -34, 8.8), lens=44, focus=(0, -34, 8.8), fstop=3, ease="EASE_IN")
    cam.crash(t0 + 3.4, 30, 46, 0.12)
    cam.handheld(2.4)
    sfx(t0 + 3.4, "boom")
    sfx(t0 + 3.45, "rocket", 0.7)
    sfx(t0 + 3.5, "zombie", 0.8)
    sfx(t0 + 3.6, "blast", 0.7)


@S(39, 259, 270, "The Devourer ran back to the forest and never came back")
def p39(t0, t1):
    night_forest()
    D = devourer((0, 4, 0), 1.2, "DevR")
    D.keyframe_insert("location", frame=F(t0 + 0.6))
    D.location = (0, 60, 0)
    D.keyframe_insert("location", frame=F(t1))
    set_interp(D, "location", F(t0 + 0.6), "BEZIER", "EASE_IN")
    P = pip((-6, -20, 0.2), 12.0, "PipWin")
    cam = Cam()
    cam.key(t0, (-4, -46, 4.0), (0, 6, 10), lens=22, focus=(0, 6, 10), fstop=8)
    cam.key(t1, (6, -34, 7.0), (0, 40, 8), lens=22, focus=(0, 40, 8), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    sfx(t0, "whoosh")
    sfx(t0 + 0.8, "stomp", 0.9)
    sfx(t0 + 2.4, "stomp", 0.9)
    sfx(t0 + 3.6, "wind", 0.7)


@S(40, 270, 281, "The next morning, Pip was tiny again, asleep in my hood")
def p40(t0, t1):
    day_street()
    K = hero(t0, t1, "smile")
    K.pose(t0, loc=(0, -30, 0), rot=0)
    K.walk(t0, t1, (0, -30, 0), (0, -40, 0), rate=2.2)
    P = pip((0, -28.4, 4.8), 0.5, "PipZ")
    P.keyframe_insert("location", frame=F(t0))
    P.location = (0, -38.4, 4.8)
    P.keyframe_insert("location", frame=F(t1))
    zzz(t0 + 0.5, t1, (1.8, -32, 6.5), n=4)
    cam = Cam()
    cam.key(t0, (4, -40, 3.8), (0, -31, 4.6), lens=28, focus=(0, -31, 4.6), fstop=3)
    cam.key(t1, (3.6, -48, 3.8), (0, -39, 4.8), lens=34, focus=(0, -39, 4.8), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 0.8, "footsteps", 0.6)
    sfx(t0 + 2.0, "aww", 0.8)


@S(41, 281, None, "Nobody laughs at us anymore: class cheers for Max and Pip")
def p41(t0, t1):
    R, ks = class_scene(t0, t1, kids=8, board="chalk_joke.png")
    for k in ks:
        k.act(t0 + 0.2, "cheer", expr="joy")
    K = hero(t0, t1, "joy")
    K.pose(t0, loc=(5, 12, 0), rot=0)
    K.act(t0 + 0.4, "cheer", expr="joy")
    P = pip((5, 10.8, 5.0), 0.7, "PipEnd")
    confetti("cf", (5, 8, 8), (6, 3, 4), t0 + 0.4, 1.8, 60, 2, 10)
    cam = push_cam(t0, t1, (5, 11, 4.6), 13, 9, yaw=8, yaw1=-8, lens=24, hh=1.0)
    sfx(t0, "cheer")
    sfx(t0 + 0.2, "confetti")
    sfx(t0 + 1.6, "aww", 0.8)
    sfx(t0 + 2.0, "squeak", 0.7)
