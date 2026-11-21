"""fog: Never turn around when someone calls your last name. The caller in the fog is Mom.
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
        W.sun(0.35, rot=(62, 0, 200))
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
    world((0.1, 0.12, 0.2) if night else (0.5, 0.52, 0.6), 0.18 if night else 0.5)
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


# ================================================================== PART 1: the rule (0-36s)
@S(1, 0, 3, "HOOK: Eddie walks the foggy street at dusk, whip + push")
def f01(t0, t1):
    night_street(night=False)
    E = eddie(t0, t1, "worried")
    E.walk(t0, t1, (-1.2, -18, 0), (-0.6, -12, 0), rate=2.4)
    cam = Cam()
    cam.key(t0, (7, -30, 1.2), (0, -8, 6), lens=22, focus=(0, -14, 4), fstop=4)
    cam.key(t1, (2.4, -22, 5.2), (-0.5, -12, 5), lens=28, focus=(-0.5, -12, 4.7), fstop=3, ease="EASE_OUT")
    cam.crash(t0 + 1.7, 28, 34, 0.12)
    cam.handheld(1.3)
    sfx(t0, "whoosh")
    sfx(t0 + 0.2, "wind", 0.6)


@S(2, 3, 8, "NEVER TURN AROUND sign slam")
def f02(t0, t1):
    night_street(night=False, houses=False)
    card("sgn", 5.0, 5.0, (0, -6, 5.2), img_mat("s_turn", os.path.join(TEX, "sign_turn.png"), 0.5), "-Y")
    cyl("sgp", 0.25, 5.2, (0, -5.7, 2.6), M("#4a4d55", 0.5), 12)
    cam = Cam()
    cam.key(t0, (4, -26, 6.4), (0, -6, 5.2), lens=24, focus=(0, -6, 5.2), fstop=4)
    cam.key(t1, (0.6, -17, 5.3), (0, -6, 5.2), lens=24, focus=(0, -6, 5.2), fstop=4, ease="EASE_IN")
    cam.crash(t0 + 0.3, 24, 38, 0.14)
    cam.handheld(1.0)
    sfx(t0, "boom")
    sfx(t0 + 0.05, "sting")


@S(3, 8, 14, "A kid hears his last name called, stiffens")
def f03(t0, t1):
    night_street(night=False)
    K = townie(2, t0, t1, "worried")
    K.pose(t0, loc=(0, -10, 0), rot=0)
    K.act(t0 + 0.8, "brace", expr="scared")
    bubble(t0 + 0.4, t1, (2.5, -9.6, 8.0), "MILLER!", (1, 0.8, 0.6))
    cam = push_cam(t0, t1, (0, -10, 4.4), 12, 7.5, yaw=-18, yaw1=10)
    sfx(t0 + 0.4, "sting")
    sfx(t0 + 1.0, "gasp")


@S(4, 14, 19, "Your first name is fine: kid turns happily")
def f04(t0, t1):
    night_street(night=False)
    K = townie(2, t0, t1, "happy")
    K.pose(t0, loc=(0, -10, 0), rot=180)
    K.pose(t0 + 0.7, rot=0)
    K.act(t0 + 0.8, "wave", expr="joy")
    bubble(t0 + 0.2, t1, (-2.6, -9.6, 8.0), "EDDIE!", (0.7, 1, 0.7))
    cam = push_cam(t0, t1, (0, -10, 4.4), 12, 8, yaw=14, yaw1=-12)
    sfx(t0 + 0.2, "ding")
    sfx(t0 + 0.8, "correct", 0.6)


@S(5, 19, 22, "Your last name? Kid freezes, sweat")
def f05(t0, t1):
    night_street(night=False)
    K = townie(2, t0, t1, "terror")
    K.pose(t0, loc=(0, -10, 0), rot=0)
    K.act(t0 + 0.2, "recoil", expr="terror")
    for i in range(6):
        K.pose(t0 + i * 0.2, head=(2 * (-1) ** i, 4, 3 * (-1) ** i))
    cam = push_cam(t0, t1, (0, -10, 4.7), 9, 5, yaw=0, lens=30, lens1=40, hh=2.2)
    cam.crash(t0 + 0.1, 30, 38, 0.1)
    sfx(t0, "rise", 0.8)


@S(6, 22, 23, "NEVER (big red text)")
def f06(t0, t1):
    night_street(night=False, houses=False, fog=False)
    text("never", "NEVER", (0, -6, 5), 2.6, mat("red_txt", (1, 0.1, 0.1), 0.4, emit=(1, 0.1, 0.1), estr=4.0), rot=(90, 0, 0), extrude=0.3)
    cam = Cam()
    cam.key(t0, (0, -13, 5.2), (0, -6, 5), lens=26, focus=(0, -6, 5), fstop=4)
    cam.key(t1, (0, -9.2, 5.1), (0, -6, 5), lens=26, focus=(0, -6, 5), fstop=4, ease="EASE_IN")
    cam.handheld(1.4)
    sfx(t0, "boom")
    sfx(t0, "sting")


@beat(23, 30, n=2, focus=(0, -4, 4.5), d=14, lens=26, desc="If you turn, the callers take you: arm from the fog drags the kid")
def f07(t0, t1):
    night_street(night=False)
    K = townie(2, t0, t1, "worried")
    K.pose(t0, loc=(0, -6, 0), rot=180)
    K.pose(t0 + 0.9, rot=0)
    K.act(t0 + 1.1, "shock", expr="scream")
    C = caller(0, t0, t1, (0, 10, 0), rot=180, scale=2.0)
    C.pose(t0 + 1.0, loc=(0, 10, 0))
    C.pose(t0 + 1.8, loc=(0, -3.5, 0))
    K.pose(t0 + 2.2, loc=(0, -6, 0))
    K.pose(t1 - 0.2, loc=(0, 14, 0), rot=0)
    cam = push_cam(t0, t1, (0, 0, 4.5), 22, 14, yaw=-12, yaw1=10, lens=24, hh=1.6)
    sfx(t0 + 0.9, "gasp")
    sfx(t0 + 1.1, "sting")
    sfx(t0 + 2.4, "whoosh")


@S(8, 30, 36, "No one has ever come back: empty street, lost hat, fog")
def f08(t0, t1):
    night_street(night=False)
    box("hat", (1.4, 1.4, 0.5), (1.5, -6, 0.3), M("#d9453a", 0.5), 0.2)
    cam = Cam()
    cam.key(t0, (0.5, -16, 1.6), (1.5, -6, 0.6), lens=30, focus=(1.5, -6, 0.6), fstop=3)
    cam.key(t1, (1.0, -10.5, 1.3), (1.5, -6, 0.7), lens=30, focus=(1.5, -6, 0.7), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "wind", 0.7)
    sfx(t0 + 1.4, "crickets", 0.7)


# ================================================================== PART 2: how people live with it (36-81s)
@beat(36, 45, n=2, focus=(6, 8, 4.6), d=13, lens=26, desc="Teachers call us by first names only: roll call")
def f09(t0, t1):
    R, ks = class_scene(t0, t1, kids=7, board="chalk_joke.png")
    T = teacher(t0, t1, "happy")
    T.pose(t0, loc=(5, 12.5, 0), rot=0)
    T.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk_wide", rest="smile")
    T.act(t0 + 0.4, "point", expr="happy")
    bubble(t0 + 1.0, t0 + 2.4, (5, 11, 11), "LEO!", (1, 1, 0.8), 1.4, rot=(90, 0, 180))
    for k in ks:
        k.face(t0, "worried")
    cam = push_cam(t0, t1, (6, 8, 4.6), 15, 11, yaw=0, yaw1=-8, lens=24)
    sfx(t0 + 1.0, "ding")


@S(10, 45, 49, "Doctors: patient on a bed, doctor writing")
def f10(t0, t1):
    doctor_set()
    D_ = doctor(t0, t1, "bored")
    D_.pose(t0, loc=(-2, 4, 0), rot=-30)
    D_.act(t0 + 0.2, "think", expr="bored")
    K = townie(3, t0, t1, "worried")
    K.pose(t0, loc=(4, 6, 2.0), rot=180 + 180)
    K.pose(t0, loc=(4, 6, 2.0), rot=0)
    cam = push_cam(t0, t1, (1, 5, 4.5), 16, 11, yaw=-12, yaw1=12, lens=26)
    sfx(t0, "footsteps", 0.5)


@S(11, 49, 51, "Hey, you. (doctor points)")
def f11(t0, t1):
    doctor_set()
    D_ = doctor(t0, t1, "shout")
    D_.pose(t0, loc=(0, 4, 0), rot=0)
    D_.act(t0 + 0.1, "point", expr="shout")
    D_.talk(t0, t1, V.span(t0, t1), open_m="talk_wide", wide_m="scream", rest="grimace")
    cam = push_cam(t0, t1, (0, 4, 4.7), 8, 5.5, yaw=-12, yaw1=6, lens=30, lens1=36, hh=1.6)
    cam.crash(t0 + 0.2, 30, 38, 0.1)
    sfx(t0 + 0.15, "sting")


@S(12, 51, 60, "Last names in pencil: close-up of a desk, pencil writing")
def f12(t0, t1):
    world((0.9, 0.9, 0.85), 0.7)
    box("desk", (30, 30, 0.4), (0, 0, -0.2), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0)
    plane("paper", 4.6, 2.0, (0, 0, 0.1), img_mat("name_pencil", os.path.join(TEX, "name_pencil.png"), 0.7), (0, 0, 3))
    pc = pencil("pc", (1.8, -0.4, 0.4), rot=(60, 0, 30))
    pc.keyframe_insert("location", frame=F(t0))
    pc.location = (-1.2, -0.2, 0.4)
    pc.keyframe_insert("location", frame=F(t1))
    light("l1", "AREA", (0, -3, 8), 1400, (1, 0.97, 0.9), 6, target=(0, 0, 0))
    cam = Cam()
    cam.key(t0, (-1.8, -3.4, 3.6), (0, 0, 0), lens=30, focus=(0, 0, 0), fstop=1.8)
    cam.key(t1, (0.9, -1.6, 3.4), (0, 0, 0), lens=34, focus=(0, 0, 0), fstop=1.8, ease="EASE_OUT")
    cam.handheld(0.8)
    sfx(t0 + 0.2, "paper")
    sfx(t0 + 1.0, "click", 0.6)
    sfx(t0 + 2.4, "click", 0.6)


@S(13, 60, 65, "Erase them after class: eraser rubs the name away")
def f13(t0, t1):
    world((0.9, 0.9, 0.85), 0.7)
    box("desk", (30, 30, 0.4), (0, 0, -0.2), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0)
    p1 = plane("paper1", 4.6, 2.0, (0, 0, 0.1), img_mat("name_pencil", os.path.join(TEX, "name_pencil.png"), 0.7), (0, 0, 3))
    p2 = plane("paper2", 4.6, 2.0, (0, 0, 0.11), img_mat("name_blank", os.path.join(TEX, "name_blank.png"), 0.7), (0, 0, 3))
    sets.set_obj_visible(p1, t0 + 1.6, True)
    sets.set_obj_visible(p1, t0 + 1.7, False)
    sets.set_obj_visible(p2, t0 + 1.6, False)
    sets.set_obj_visible(p2, t0 + 1.7, True)
    er = box("eraser", (1.2, 0.7, 0.5), (-1.8, 0, 0.5), M("#f09ac2", 0.8), 0.1)
    for i in range(6):
        er.location = (-1.8 + 3.6 * (i % 2), 0.1 * (-1) ** i, 0.5)
        er.keyframe_insert("location", frame=F(t0 + 0.2 + i * 0.3))
    light("l1", "AREA", (0, -3, 8), 1400, (1, 0.97, 0.9), 6, target=(0, 0, 0))
    cam = Cam()
    cam.key(t0, (0, -3.0, 4.0), (0, 0, 0), lens=30, focus=(0, 0, 0), fstop=1.8)
    cam.key(t1, (0.6, -2.0, 3.4), (0, 0, 0), lens=34, focus=(0, 0, 0), fstop=1.8, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.2, "paper", 0.5)
    sfx(t0 + 1.0, "paper", 0.5)
    sfx(t0 + 1.7, "poof", 0.5)


@beat(65, 75, n=2, focus=(0, 6, 4.6), d=14, lens=26, desc="My dad got married without saying his last name")
def f14(t0, t1):
    church_set()
    D_ = dadc(t0, t1, "happy")
    D_.pose(t0, loc=(-2, 7, 0.0), rot=0)
    Mm = mom(t0, t1, "happy")
    Mm.pose(t0, loc=(2, 7, 0.0), rot=0)
    P = priest(t0, t1, "neutral")
    P.pose(t0, loc=(0, 9.8, 3.2), rot=0)
    P.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk", rest="flat")
    D_.act(t0 + 1.5, "shrug", expr="happy")
    cam = push_cam(t0, t1, (0, 7, 4.5), 17, 12, yaw=-8, yaw1=8, lens=24)
    sfx(t0, "ding", 0.5)
    sfx(t0 + 1.8, "aww", 0.5)


@S(15, 75, 81, "The priest just pointed at him")
def f15(t0, t1):
    church_set()
    P = priest(t0, t1, "angry")
    P.pose(t0, loc=(0, 9.8, 3.2), rot=0)
    P.act(t0 + 0.3, "point", expr="angry")
    D_ = dadc(t0, t1, "worried")
    D_.pose(t0, loc=(-2, 7, 0), rot=0)
    D_.act(t0 + 0.8, "recoil", expr="scared")
    cam = push_cam(t0, t1, (0, 8, 5.0), 11, 6.5, yaw=-10, yaw1=12, lens=28, lens1=34, hh=1.6)
    cam.crash(t0 + 0.4, 28, 36, 0.1)
    sfx(t0 + 0.4, "sting")
    sfx(t0 + 0.8, "gasp")


@beat(81, 91, n=3, focus=(0, 38, 4), d=40, lens=24, desc="The callers live in the fog behind the old bridge", pitch=3)
def f16(t0, t1):
    night_street(night=False, houses=False, lamps=False)
    for i, x in enumerate((-8, 0, 8)):
        caller(i + 1, t0, t1, (x, 50 + (i % 2) * 6, 0), rot=180, scale=1.8, reach=False)
    fogballs(14, ((-16, 16), (36, 52)), z=(1, 5), size=(4, 8), seed=9, alpha=0.3)
    cam = Cam()
    cam.key(t0, (-6, -4, 3.5), (0, 40, 5), lens=22, focus=(0, 40, 5), fstop=8)
    cam.key(t1, (3, 10, 4.5), (0, 44, 5), lens=26, focus=(0, 44, 5), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0, "wind", 0.8)
    sfx(t0 + 1.5, "zombie", 0.4)


@S(17, 91, 96, "They can copy any voice: caller with floating speech")
def f17(t0, t1):
    night_street(night=False, houses=False, lamps=False)
    C = caller(1, t0, t1, (0, 30, 0), rot=180, scale=1.8, reach=False)
    C.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk_wide", rest="flat")
    for i, b in enumerate(("HEY!", "MILLER!", "DINNER!", "HELLO?")):
        bubble(t0 + 0.4 + i * 0.4, t1, (-4 + i * 2.8, 27, 10 - (i % 2) * 2), b, (0.8, 0.9, 1), 1.3, rot=(90, 0, 180))
    cam = push_cam(t0, t1, (0, 30, 5), 16, 10, yaw=0, yaw1=-14, lens=26)
    sfx(t0 + 0.4, "pop")
    sfx(t0 + 0.8, "pop")
    sfx(t0 + 1.2, "pop")
    sfx(t0 + 1.6, "pop")


@S(18, 96, 98, "Your dog.")
def f18(t0, t1):
    night_street(night=False, houses=False)
    W.dog("dog", (0, -4, 0), None)
    fogballs(6, ((-6, 6), (2, 14)), z=(0.8, 3), size=(2.5, 4), seed=11, alpha=0.25)
    cam = Cam()
    cam.key(t0, (3, -10, 2.0), (0, -4, 1.6), lens=30, focus=(0, -4, 1.6), fstop=2.5)
    cam.key(t1, (1.2, -8, 1.8), (0, -4, 1.6), lens=34, focus=(0, -4, 1.6), fstop=2.5, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0, "sting")
    sfx(t0 + 0.2, "meow", 0.6)


@S(19, 98, 100, "Your teacher. (in the fog)")
def f19(t0, t1):
    night_street(night=False, houses=False)
    T = teacher(t0, t1, "happy")
    T.pose(t0, loc=(0, 8, 0), rot=0)
    T.act(t0 + 0.1, "wave", expr="happy")
    fogballs(10, ((-8, 8), (10, 22)), z=(0.8, 4), size=(3, 5), seed=12, alpha=0.3)
    cam = push_cam(t0, t1, (0, 8, 4.6), 13, 9, yaw=-10, yaw1=8, lens=28)
    sfx(t0, "sting")


@S(20, 100, 103, "Your best friend. (Tootie waving, glowing eyes)")
def f20(t0, t1):
    night_street(night=False, houses=False)
    T = tootie(t0, t1, "grin")
    T.pose(t0, loc=(0, 8, 0), rot=0)
    T.act(t0 + 0.1, "wave", expr="grin")
    for sx in (-1, 1):
        sphere(f"te{sx}", 0.13, (sx * 0.22, -0.64, 0.08), mat("eye_glow", (1, 1, 0.9), 0.3, emit=(1, 1, 0.85), estr=12.0), parent=T.head, coll=T.coll)
    fogballs(10, ((-8, 8), (10, 22)), z=(0.8, 4), size=(3, 5), seed=13, alpha=0.3)
    cam = push_cam(t0, t1, (0, 8, 4.7), 12, 6.5, yaw=10, yaw1=-8, lens=28, lens1=36, hh=1.6)
    cam.crash(t0 + 0.4, 28, 36, 0.1)
    sfx(t0, "sting")
    sfx(t0 + 0.3, "boom", 0.6)


@beat(103, 114, n=2, focus=(0, -4, 3.0), d=14, lens=26, desc="Tootie turned around once at six")
def f21(t0, t1):
    night_street(night=False)
    T = tootie(t0, t1, "happy")
    T.root.scale = (0.65,) * 3
    T.pose(t0, loc=(0, -4, 0), rot=180)
    T.pose(t0 + 1.2, rot=180)
    T.pose(t0 + 1.8, rot=0)
    T.act(t0 + 1.9, "shock", expr="terror")
    C = caller(0, t0, t1, (0, 22, 0), rot=180, scale=2.2)
    C.pose(t0 + 1.8, loc=(0, 22, 0))
    C.pose(t1, loc=(0, 5, 0))
    bubble(t0 + 1.0, t1, (3, -3.6, 7), "TOOTIE!", (1, 0.85, 0.7), 1.2)
    cam = push_cam(t0, t1, (0, 2, 3.0), 20, 13, yaw=-14, yaw1=8, lens=24, hh=1.5)
    sfx(t0 + 1.0, "sting")
    sfx(t0 + 1.9, "gasp")


@S(22, 114, 121, "His grandpa grabbed him just in time")
def f22(t0, t1):
    night_street(night=False)
    T = tootie(t0, t1, "terror")
    T.root.scale = (0.65,) * 3
    T.pose(t0, loc=(0, 3, 0), rot=0)
    T.pose(t0 + 1.8, loc=(0, 3, 0))
    T.pose(t0 + 2.4, loc=(0, -5, 0))
    G = grandpa(t0, t1, "shock")
    G.pose(t0, loc=(-9, -9, 0), rot=-40)
    G.run(t0 + 0.2, t0 + 1.9, (-9, -9, 0), (-0.8, 1.5, 0))
    G.pose(t0 + 2.0, loc=(-0.8, 1.5, 0), rot=0)
    G.act(t0 + 2.1, "reach", expr="shout")
    G.pose(t0 + 2.6, loc=(0, -6, 0))
    cam = push_cam(t0, t1, (0, 0, 3.4), 20, 13, yaw=0, yaw1=16, lens=24, hh=2.0)
    sfx(t0 + 0.2, "footsteps")
    sfx(t0 + 2.0, "slap")
    sfx(t0 + 2.2, "whoosh")


@S(23, 121, 127, "Rock and roll! We're losing control! (grandpa and Tootie shout)")
def f23(t0, t1):
    night_street(night=False, houses=False)
    G = grandpa(t0, t1, "shout")
    G.pose(t0, loc=(-2, -6, 0), rot=15)
    G.talk(t0, t1, V.span(t0, t1), open_m="talk_wide", wide_m="scream", rest="grimace")
    G.panic(t0, t1, rate=6)
    T = tootie(t0, t1, "scream")
    T.root.scale = (0.65,) * 3
    T.pose(t0, loc=(2, -6, 0), rot=-15)
    T.panic(t0, t1, rate=7)
    cam = push_cam(t0, t1, (0, -6, 3.8), 12, 7.5, yaw=-10, yaw1=12, lens=26, hh=2.8)
    sfx(t0, "whoosh")
    sfx(t0 + 0.8, "rimshot", 0.6)


@beat(127, 136, n=2, focus=(0, -6, 4.5), d=11, lens=28, desc="Tootie wears his hoodie backwards, just in case")
def f24(t0, t1):
    night_street(night=False)
    T = tootie(t0, t1, "smug")
    hood_on_chest(T)
    T.pose(t0, loc=(-6, -8, 0), rot=180)
    T.walk(t0, t1, (-6, -8, 0), (3, -6, 0), rate=2.4, face_dir=False)
    T.pose(t0, rot=180, head=(180, 0, 0))
    T.pose(t1, rot=180, head=(180, 0, 0))
    cam = push_cam(t0, t1, (0, -7, 4.5), 14, 9, yaw=0, yaw1=-8, lens=26)
    sfx(t0 + 0.2, "footsteps", 0.7)
    sfx(t0 + 1.2, "rimshot", 0.6)


# ================================================================== PART 3: Mom (136-185s)
@S(25, 136, 143, "My mom always taught me one rule: Mom and little Eddie at home")
def f25(t0, t1):
    home_set()
    Mm = mom(t0, t1, "smile")
    Mm.pose(t0, loc=(-2, 4, 0), rot=15)
    Mm.act(t0 + 0.3, "lean", expr="smile")
    Mm.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk", rest="smile")
    E = eddie(t0, t1, "happy")
    E.root.scale = (0.7,) * 3
    E.pose(t0, loc=(2.5, 3, 0), rot=-25)
    cam = push_cam(t0, t1, (0, 3.6, 4.0), 13, 8.5, yaw=-10, yaw1=12, lens=26)
    sfx(t0 + 0.5, "aww", 0.5)


@beat(143, 153, n=2, focus=(-2, 4, 4.8), d=9, lens=30, desc="If you ever hear me call your last name, run")
def f26(t0, t1):
    home_set()
    Mm = mom(t0, t1, "angry")
    Mm.pose(t0, loc=(-2, 4, 0), rot=10)
    Mm.act(t0 + 0.2, "point", expr="shout")
    Mm.talk(t0, t1, V.span(t0, t1), open_m="talk_wide", wide_m="talk", rest="grimace")
    cam = push_cam(t0, t1, (-2, 4, 4.8), 9, 6, yaw=-10, yaw1=10, lens=30, lens1=36, hh=1.4)
    sfx(t0 + 1.6, "sting", 0.7)


@S(27, 153, 158, "I will never do that: hand on heart")
def f27(t0, t1):
    home_set()
    Mm = mom(t0, t1, "smile")
    Mm.pose(t0, loc=(-2, 4, 0), rot=0)
    Mm.act(t0 + 0.2, "hands_face", expr="relief")
    Mm.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk", rest="smile")
    cam = push_cam(t0, t1, (-2, 4, 4.8), 8, 5.4, yaw=8, yaw1=-8, lens=30, lens1=38)
    sfx(t0 + 0.4, "aww")


@beat(158, 170, n=2, focus=(0, 2, 4.5), d=14, lens=26, desc="Last winter Mom went to the bridge to find our lost cat")
def f28(t0, t1):
    night_street(night=False)
    for i in range(14):
        sp = sphere(f"snow{i}", 0.12, (random.uniform(-8, 8), random.uniform(-8, 10), 14), mat("snowm", (1, 1, 1), 0.5, emit=(1, 1, 1), estr=1.5))
        sp.keyframe_insert("location", frame=F(t0))
        sp.location[2] = 0.3
        sp.keyframe_insert("location", frame=F(t0 + 3.0))
    Mm = mom(t0, t1, "worried")
    Mm.pose(t0, loc=(0, -10, 0), rot=180)
    Mm.walk(t0, t1, (0, -10, 0), (0, 24, 0), rate=2.4)
    card("poster", 2.4, 3.0, (-5, -12, 4), img_mat("lost_cat", os.path.join(TEX, "lost_cat.png"), 0.6), "-Y")
    cam = Cam()
    cam.key(t0, (-6, -22, 3.0), (0, 4, 4.4), lens=26, focus=(0, 4, 4.4), fstop=6)
    cam.key(t1, (4, -6, 5.5), (0, 16, 4.4), lens=24, focus=(0, 16, 4.4), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0, "wind", 0.7)
    sfx(t0 + 0.4, "footsteps", 0.7)
    sfx(t0 + 3.0, "meow", 0.5)


@S(29, 170, 174, "She never came back: empty bridge, scarf on the rail")
def f29(t0, t1):
    night_street(night=False, houses=False)
    box("scarf", (0.4, 1.8, 0.2), (3.8, 22, 4.8), M("#e0457b", 0.8), 0.1)
    box("scarf2", (0.4, 0.3, 1.4), (3.8, 22.9, 4.2), M("#e0457b", 0.8), 0.1)
    noise(bpy.data.objects["scarf2"], "rotation_euler", 0, 0.3, 14)
    cam = Cam()
    cam.key(t0, (0, 4, 3.4), (3.8, 22, 4.6), lens=26, focus=(3.8, 22, 4.6), fstop=3)
    cam.key(t1, (2.6, 14, 4.2), (3.8, 22, 4.6), lens=30, focus=(3.8, 22, 4.6), fstop=3, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0, "wind", 0.8)
    sfx(t0 + 1.2, "crickets", 0.6)


@beat(174, 185, n=2, focus=(0, 4, 4.5), d=10, lens=28, desc="A year without her voice, until tonight: Eddie alone at night")
def f30(t0, t1):
    home_set()
    E = eddie(t0, t1, "cry")
    E.pose(t0, loc=(0, 4, 0), rot=0)
    E.act(t0 + 0.3, "slump", expr="cry")
    box("photo", (1.6, 0.1, 2.0), (0, 3.2, 4.2), M("#f4f4f2", 0.6), 0.04)
    card("ph", 1.4, 1.8, (0, 3.14, 4.2), img_mat("lost_cat", os.path.join(TEX, "lost_cat.png"), 0.6), "-Y")
    E.act(t0 + 3.0, "lean", expr="gasp")
    cam = push_cam(t0, t1, (0, 4, 4.5), 12, 7.5, yaw=-14, yaw1=10, lens=26)
    sfx(t0 + 0.5, "crickets", 0.6)
    sfx(t0 + 3.2, "sting")


@S(31, 185, 189, "Miller! Sweetie! It's me!: a figure in the fog, speech bubble")
def f31(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(-1.5, -14, 0), rot=180)
    T = tootie(t0, t1, "worried")
    T.pose(t0, loc=(1.5, -14, 0), rot=180)
    Mm = mom(t0, t1, "worried")
    Mm.pose(t0, loc=(0, 40, 0), rot=0)
    light("mom_glow", "POINT", (0, 38, 5), 1500, (1.0, 0.7, 0.4), 1.0)
    bubble(t0 + 0.2, t1, (0, 16, 11), "MILLER!", (1, 0.75, 0.55), 2.0, rot=(90, 0, 180))
    cam = Cam()
    cam.key(t0, (6, -24, 3.2), (0, 10, 5.5), lens=24, focus=(0, 12, 5), fstop=8)
    cam.key(t1, (2.5, -19, 5.4), (0, 14, 5.8), lens=24, focus=(0, 14, 5.5), fstop=8, ease="EASE_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.1, "sting")
    sfx(t0 + 0.2, "rise", 0.8)


@S(32, 189, 192, "I'm so cold! (Eddie close, tears)")
def f32(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "cry")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    E.act(t0 + 0.2, "recoil", expr="cry")
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.8), 8, 5.0, yaw=12, yaw1=-8, lens=32, lens1=40, hh=1.8)
    sfx(t0, "wind", 0.7)


@S(33, 192, 195, "Please, turn around!")
def f33(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    for i in range(8):
        E.pose(t0 + i * 0.14, head=(3 * (-1) ** i, 4, 3 * (-1) ** i))
    bubble(t0, t1, (0, 14, 10), "TURN AROUND!", (1, 0.75, 0.55), 1.6, rot=(90, 0, 180))
    cam = push_cam(t0, t1, (0, -10, 4.8), 9, 4.6, yaw=-8, yaw1=6, lens=30, lens1=42, hh=2.6)
    cam.crash(t0 + 1.8, 30, 40, 0.12)
    sfx(t0, "rise", 0.9)
    sfx(t0 + 1.9, "boom", 0.7)


@S(34, 195, 200, "It sounded exactly like her: Eddie teary close-up")
def f34(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "cry")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    E.talk(t0, t0 + 0.1, rest="ah")
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.8), 7, 4.4, yaw=-10, yaw1=8, lens=34, lens1=44, hh=1.2)
    sfx(t0 + 0.3, "aww", 0.6)


@S(35, 200, 204, "Even her little cough: *cough* in the fog")
def f35(t0, t1):
    night_street(night=True)
    Mm = mom(t0, t1, "worried")
    Mm.pose(t0, loc=(0, 40, 0), rot=0)
    light("mom_glow", "POINT", (0, 38, 5), 1500, (1.0, 0.7, 0.4), 1.0)
    bubble(t0 + 0.6, t1, (0, 20, 9), "*cough*", (1, 0.9, 0.8), 1.6, rot=(90, 0, 180))
    cam = Cam()
    cam.key(t0, (3, -4, 4.0), (0, 38, 5), lens=26, focus=(0, 38, 5), fstop=8)
    cam.key(t1, (0.5, 6, 4.6), (0, 38, 5), lens=30, focus=(0, 38, 5), fstop=8, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0 + 0.6, "pop")
    sfx(t0 + 0.7, "sneeze", 0.4)


@S(36, 204, 208, "Tootie grabbed my arm")
def f36(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(-1.6, -10, 0), rot=-15)
    T = tootie(t0, t1, "scream")
    T.pose(t0, loc=(1.6, -10, 0), rot=15)
    T.act(t0 + 0.3, "reach", expr="scream")
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.6), 11, 7.5, yaw=-14, yaw1=10, lens=28, hh=2.0)
    sfx(t0 + 0.3, "slap", 0.8)


@S(37, 208, 209, "Don't! (crash zoom on Tootie)")
def f37(t0, t1):
    night_street(night=True)
    T = tootie(t0, t1, "shout")
    T.pose(t0, loc=(0, -10, 0), rot=0)
    T.talk(t0, t1, V.span(t0, t1), open_m="talk_wide", wide_m="scream", rest="grimace")
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.7), 9, 5, yaw=0, lens=30, lens1=44, hh=2.4)
    cam.crash(t0, 30, 46, 0.1)
    sfx(t0, "boom", 0.7)


@S(38, 209, 214, "Miller, I found the cat: Mom's silhouette holds the cat")
def f38(t0, t1):
    night_street(night=True)
    Mm = mom(t0, t1, "smile")
    Mm.pose(t0, loc=(0, 40, 0), rot=0)
    Mm.act(t0 + 0.2, "hold", expr="smile")
    cat_prop((0.6, 38.5, 3.2), rot=180, scale=0.9)
    light("mom_glow", "POINT", (0, 37, 5), 1800, (1.0, 0.7, 0.4), 1.0)
    cam = Cam()
    cam.key(t0, (4, -2, 3.8), (0, 40, 5), lens=28, focus=(0, 40, 5), fstop=8)
    cam.key(t1, (1.0, 12, 4.8), (0, 40, 5), lens=34, focus=(0, 40, 5), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.2, "meow")
    sfx(t0 + 0.3, "sparkle", 0.4)


@S(39, 214, 221, "I just want to see your face: Eddie torn, close")
def f39(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "cry")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    for i in range(10):
        E.pose(t0 + 0.2 + i * 0.5, head=(4 * (-1) ** i, 4, 3 * (-1) ** i))
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.8), 10, 4.6, yaw=-14, yaw1=10, lens=30, lens1=42, hh=1.8)
    sfx(t0 + 0.2, "rise", 0.6)


# ================================================================== PART 4: the rule wins (221-end)
@S(40, 221, 225, "My legs were shaking: low shot of trembling legs")
def f40(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    for i in range(12):
        s = (-1) ** i
        E.pose(t0 + i * 0.1, legL=(6 * s, 4), legR=(-6 * s, 4), hipz=-0.1 * s)
    cam = Cam()
    cam.key(t0, (1.5, -15, 0.8), (0, -10, 1.6), lens=30, focus=(0, -10, 1.6), fstop=3)
    cam.key(t1, (0.8, -12.5, 1.2), (0, -10, 2.0), lens=34, focus=(0, -10, 2.0), fstop=3, ease="EASE_IN")
    cam.handheld(2.4)
    sfx(t0, "rise", 0.6)


@S(41, 225, 230, "Then I remembered her rule: flashback of Mom (warm)")
def f41(t0, t1):
    home_set()
    Mm = mom(t0, t1, "angry")
    Mm.pose(t0, loc=(-2, 4, 0), rot=10)
    Mm.act(t0 + 0.2, "point", expr="shout")
    Mm.talk(t0, t1, V.span(t0, t1), open_m="talk_wide", wide_m="talk", rest="grimace")
    light("warm", "POINT", (0, 0, 6), 800, (1.0, 0.7, 0.35), 1.0)
    cam = push_cam(t0, t1, (-2, 4, 4.8), 9, 6, yaw=-10, yaw1=10, lens=30, lens1=36, hh=1.4)
    sfx(t0, "ding", 0.6)
    sfx(t0 + 0.2, "sparkle", 0.5)


@S(42, 230, 237, "Mom would never say my last name: realization")
def f42(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    E.act(t0 + 0.2, "shock", expr="gasp")
    E.face(t0 + 2.4, "determined")
    bulb = sphere("bulb", 0.5, (0, -10.3, 9.4), mat("bulb_y", (1, 0.9, 0.3), 0.3, emit=(1, 0.85, 0.2), estr=14), seg=16)
    bulb.scale = (0.01,) * 3
    bulb.keyframe_insert("scale", frame=F(t0 + 0.4))
    bulb.scale = (1.2,) * 3
    bulb.keyframe_insert("scale", frame=F(t0 + 0.6))
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 5.5), 12, 6.5, yaw=-10, yaw1=10, lens=28, lens1=36, hh=1.4)
    cam.crash(t0 + 0.4, 28, 38, 0.1)
    sfx(t0 + 0.4, "ding")
    sfx(t0 + 0.45, "correct", 0.7)


@S(43, 237, 240, "I didn't turn: fists, steady look")
def f43(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "determined")
    E.pose(t0, loc=(0, -10, 0), rot=0)
    E.act(t0 + 0.2, "fists", expr="determined")
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.8), 8, 5.0, yaw=0, lens=30, lens1=40, hh=1.0)
    sfx(t0, "stomp", 0.7)


@S(44, 240, 244, "I walked home, crying: Eddie walks away down the street")
def f44(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "cry")
    E.pose(t0, loc=(0, -6, 0), rot=0)
    E.walk(t0, t1, (0, -6, 0), (0, -30, 0), rate=2.2)
    cam = Cam()
    cam.key(t0, (-3, 6, 4.2), (0, -10, 4.4), lens=26, focus=(0, -10, 4.4), fstop=5)
    cam.key(t1, (3, -14, 4.2), (0, -26, 4.4), lens=26, focus=(0, -26, 4.4), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "footsteps", 0.8)
    sfx(t0 + 0.2, "aww", 0.4)


@S(45, 244, 250, "Behind me, the voice went quiet: fog, the glow dims")
def f45(t0, t1):
    night_street(night=True)
    light("mom_glow", "POINT", (0, 36, 5), 1800, (1.0, 0.7, 0.4), 1.0)
    Mm = mom(t0, t1, "worried")
    Mm.pose(t0, loc=(0, 40, 0), rot=0)
    cam = Cam()
    cam.key(t0, (2, -18, 3.5), (0, 36, 5), lens=26, focus=(0, 36, 5), fstop=8)
    cam.key(t1, (0, -8, 4.4), (0, 36, 5), lens=30, focus=(0, 36, 5), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.1)
    sfx(t0, "wind", 0.7)
    sfx(t0 + 1.8, "crickets", 0.7)


@S(46, 250, 256, "Then it whispered, softer than ever: fog close, warm glow rising")
def f46(t0, t1):
    night_street(night=True)
    Mm = mom(t0, t1, "smile")
    Mm.pose(t0, loc=(0, 30, 0), rot=0)
    light("mom_glow", "POINT", (0, 28, 5), 2200, (1.0, 0.72, 0.45), 1.2)
    bubble(t0 + 0.4, t1, (0, 12, 7), "good boy...", (1, 0.85, 0.65), 1.2, rot=(90, 0, 180))
    cam = Cam()
    cam.key(t0, (0, -4, 4.2), (0, 30, 5), lens=30, focus=(0, 30, 5), fstop=6)
    cam.key(t1, (0.6, 8, 4.8), (0, 30, 5.2), lens=36, focus=(0, 30, 5.2), fstop=6, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0 + 0.2, "sparkle", 0.4)
    sfx(t0 + 1.5, "aww", 0.6)


@S(47, 256, 261, "Good boy. That's my rule.: Mom's warm silhouette, cat in her arms")
def f47(t0, t1):
    night_street(night=True)
    Mm = mom(t0, t1, "smile")
    Mm.pose(t0, loc=(0, 26, 0), rot=0)
    Mm.act(t0 + 0.2, "hold", expr="smile")
    cat_prop((0.4, 24.8, 3.0), rot=180, scale=0.9)
    light("mom_glow", "POINT", (0, 22, 5), 2600, (1.0, 0.72, 0.45), 1.2)
    cam = Cam()
    cam.key(t0, (3, 2, 4.0), (0, 26, 5), lens=30, focus=(0, 26, 5), fstop=5)
    cam.key(t1, (0.6, 12, 4.8), (0, 26, 5), lens=38, focus=(0, 26, 5), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0 + 0.2, "ding", 0.6)
    sfx(t0 + 0.4, "sparkle", 0.6)


@S(48, 261, 265, "Tootie and I froze")
def f48(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(-1.6, -10, 0), rot=180)
    T = tootie(t0, t1, "gasp")
    T.pose(t0, loc=(1.6, -10, 0), rot=180)
    light("mom_glow", "POINT", (0, 20, 5), 1500, (1.0, 0.72, 0.45), 1.2)
    cam = push_cam(t0, t1, (0, -10, 4.8), 8, 5.4, yaw=170, yaw1=190, lens=28, hh=1.0)
    sfx(t0, "sting")


@S(49, 265, 269, "It wasn't a caller: both turn their faces to each other")
def f49(t0, t1):
    night_street(night=True)
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(-1.6, -10, 0), rot=-20)
    T = tootie(t0, t1, "gasp")
    T.pose(t0, loc=(1.6, -10, 0), rot=20)
    E.act(t0 + 0.5, "hands_face", expr="shock")
    light("fg", "POINT", (0, -6, 6), 400, (1.0, 0.8, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, -10, 4.8), 9, 6.5, yaw=-8, yaw1=10, lens=30, hh=1.4)
    sfx(t0 + 0.4, "gasp")


@S(50, 269, 272, "It was Mom: she steps out of the fog, warm light, face visible")
def f50(t0, t1):
    night_street(night=True)
    Mm = mom(t0, t1, "cry")
    Mm.pose(t0, loc=(0, 30, 0), rot=0)
    Mm.walk(t0, t1, (0, 30, 0), (0, 8, 0), rate=2.0)
    Mm.act(t0 + 1.4, "hands_face", expr="cry")
    light("mom_glow", "POINT", (0, 10, 6), 2600, (1.0, 0.78, 0.55), 1.4)
    cam = Cam()
    cam.key(t0, (1, -6, 4.0), (0, 24, 5), lens=32, focus=(0, 24, 5), fstop=4)
    cam.key(t1, (0.3, -1.5, 5.0), (0, 10, 5), lens=40, focus=(0, 10, 5), fstop=4, ease="EASE_IN")
    cam.handheld(1.0)
    cam.crash(t0 + 0.3, 32, 42, 0.14)
    sfx(t0 + 0.2, "boom", 0.6)
    sfx(t0 + 0.3, "sparkle")
    sfx(t0 + 0.5, "aww", 0.8)


@beat(272, None, n=3, focus=(0, 10, 4.8), d=11, lens=30, desc="She was making sure I'd never come looking for her", pitch=3)
def f51(t0, t1):
    night_street(night=True)
    Mm = mom(t0, t1, "smile")
    Mm.pose(t0, loc=(0, 10, 0), rot=0)
    Mm.pose(t0 + 1.6, loc=(0, 10, 0))
    Mm.walk(t0 + 1.8, t1, (0, 10, 0), (0, 40, 0), rate=1.8)
    Mm.act(t0 + 0.4, "wave", expr="smile")
    cat_prop((0.4, 8.8, 3.0), rot=180, scale=0.9)
    light("mom_glow", "POINT", (0, 8, 6), 2400, (1.0, 0.78, 0.55), 1.4)
    E = eddie(t0, t1, "cry")
    E.pose(t0, loc=(0, -6, 0), rot=180)
    cam = push_cam(t0, t1, (0, 10, 4.8), 12, 9, yaw=0, yaw1=-8, lens=30, hh=0.9)
    sfx(t0 + 0.4, "aww", 0.7)
    sfx(t0 + 1.8, "wind", 0.7)
    sfx(t0 + 3.0, "sparkle", 0.4)
