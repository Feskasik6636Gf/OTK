"""knock: Never open the door after midnight. The knockers sound like the people you love.
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


# ================================================================== knock-story helpers
def hall_set(night=True, lamp=True):
    """Dark hallway: front door at the back (y=11.6) with 3 locks, a bell and a sign; bedroom door on the left,
    window on the right. Camera usually at y -9..-2 looking +Y."""
    world((0.12, 0.14, 0.24), 0.28)
    room("#6f6a7a", "#4a3a2e", night=True, key=2200)
    Mw = M("#2a1c14", 0.6)
    box("fdoor", (4.4, 0.35, 8.4), (0, 11.5, 4.2), wood("wood_fd", "#4a2c18", "#6e4229", 2.0), 0.08)
    box("fdoor_frame", (5.2, 0.5, 9.0), (0, 11.8, 4.5), M("#2a1a10", 0.6), 0.05)
    Mg = M("#d9b24a", 0.25, metal=0.8)
    for i, z in enumerate((2.6, 4.2, 5.8)):
        box(f"lock{i}", (0.7, 0.25, 0.9), (1.5, 11.2, z), Mg, 0.08)
        cyl(f"lockh{i}", 0.22, 0.2, (1.5, 11.05, z), M("#1a1a1a", 0.4), 12, rot=(90, 0, 0))
    sphere("bell", 0.5, (-2.9, 11.0, 7.0), Mg)
    cyl("bellr", 0.06, 0.8, (-2.9, 11.2, 7.7), Mg, 8)
    card("dsign", 1.8, 2.2, (-2.9, 11.0, 4.6), img_mat("sign_door", os.path.join(TEX, "sign_door.png"), 0.5), "-Y")
    box("bdoor", (0.35, 3.6, 8.0), (-14.6, 4, 4.0), wood("wood_bd", "#5a3a22", "#7a5238", 2.0), 0.06)
    box("window", (0.2, 3.4, 4.4), (14.7, 3, 5.5), mat("moonglass", (0.55, 0.7, 1.0), 0.2, emit=(0.5, 0.65, 1.0), estr=2.5), 0.05)
    box("wframe", (0.3, 3.8, 4.8), (14.65, 3, 5.5), M("#e8e8e8", 0.5), 0.05)
    light("moonw", "AREA", (13, 3, 6), 1800, (0.5, 0.65, 1.0), 4, target=(0, 3, 2))
    if lamp:
        light("hall_lamp", "POINT", (0, 2, 11), 500, (1.0, 0.75, 0.45), 0.8)


def door_knock(t, power=1.0):
    """A shake of the front door (call inside a shot, after hall_set)."""
    d = bpy.data.objects.get("fdoor")
    if d is None:
        return
    for k, dx in enumerate((0.0, -0.12, 0.05, -0.1, 0.0)):
        d.location[1] = 11.5 + dx * power
        d.keyframe_insert("location", index=1, frame=F(t + k * 0.05))
    sfx(t, "thud", 0.9)
    sfx(t, "door", 0.7)


def hood_eyes(ch, scale=0.13):
    for sx in (-1, 1):
        sphere(f"{ch.name}_ge{sx}", scale, (sx * 0.22, -0.64, 0.08), mat("eye_glow", (1, 1, 0.9), 0.3, emit=(1, 1, 0.85), estr=12.0),
               parent=ch.head, coll=ch.coll)


def double_dad(t0, t1, expr="happy"):
    D2 = dadc(t0, t1, expr)
    hood_eyes(D2, 0.14)
    return D2


def snow(t0, t1, n=40, area=((-14, 14), (-24, 10)), seed=1, top=16):
    rnd = random.Random(seed)
    Ms = mat("snowm", (1, 1, 1), 0.5, emit=(1, 1, 1), estr=1.5)
    for i in range(n):
        x, y = rnd.uniform(*area[0]), rnd.uniform(*area[1])
        sp = sphere(f"snow{seed}_{i}", 0.1, (x, y, top), Ms)
        a = t0 + rnd.uniform(0, 0.6)
        sp.keyframe_insert("location", frame=F(t0))
        sp.location = (x + rnd.uniform(-1, 1), y, 0.3)
        sp.keyframe_insert("location", frame=F(max(a + 2.2, t0 + 0.5)))


def woods(back=True):
    rnd = random.Random(4)
    for i in range(46):
        x, y = rnd.uniform(-40, 40), rnd.uniform(46, 80)
        h = rnd.uniform(9, 16)
        cyl(f"tr{i}", 0.5, h, (x, y, h / 2), M("#241a16", 0.9), 8)
        sphere(f"trc{i}", rnd.uniform(3, 5), (x, y, h + 1), M("#16241c", 0.9), (1, 1, 1.4), seg=10)


def knock_street(night=True, fog=True):
    night_street(night=night, fog=fog, lamps=True, houses=True)
    woods()


def bed_set():
    room("#7a7a9a", "#6a4a32", night=True, key=2200)
    box("bed", (9, 12, 1.6), (-4, 5, 0.8), M("#5a7ac8", 0.8), 0.2)
    box("bed_head", (9.4, 0.6, 4.0), (-4, 11.2, 2.4), wood("wood_dark", "#6e4229", "#a06a45", 2.5), 0.1)
    box("pillow", (5.0, 2.8, 1.0), (-4, 9.4, 2.0), M("#f4f4f2", 0.9), 0.4)
    box("blanket", (8.6, 7, 0.8), (-4, 4.4, 1.9), M("#3a5aa8", 0.9), 0.3)
    box("moon_win", (4.0, 0.2, 5.0), (8, 11.6, 7.0), mat("moonglass", (0.6, 0.75, 1.0), 0.2, emit=(0.5, 0.65, 1.0), estr=2.0), 0.05)
    light("br_moon", "AREA", (8, 9, 8), 1500, (0.45, 0.6, 1.0), 6, target=(-2, 4, 1))
    light("br_lamp", "POINT", (-10, 8, 4.0), 110, (1.0, 0.75, 0.45), 0.5)


def sleeper(ch, t0, t1, bob=0.15):
    ch.pose(t0, loc=(-4, 6.0, 2.05), rot=0, torso=(0, 85, 0), head=(0, 25, 0), armL=(0, 8), armR=(0, 8), legL=(88, 3), legR=(88, -3))
    ch.face(t0, eyes="closed", mouth="flat")
    for i in range(int((t1 - t0) / 0.9) + 1):
        ch.pose(t0 + i * 0.9, hipz=0.0)
        ch.pose(t0 + i * 0.9 + 0.45, hipz=bob)
    return ch


def zzz(t0, t1, loc, n=3):
    for i in range(n):
        ob = text(f"zz{i}_{random.randint(0, 999)}", "Z", (loc[0] + i * 0.7, loc[1], loc[2] + i * 0.9), 0.9 - i * 0.12,
                  mat("zzm", (0.8, 0.9, 1), 0.4, emit=(0.8, 0.9, 1), estr=3.0), rot=(90, 0, 0))
        ob.keyframe_insert("location", frame=F(t0 + i * 0.25))
        ob.location[2] += 1.8
        ob.keyframe_insert("location", frame=F(t0 + i * 0.25 + 1.6))
        sets.set_obj_visible(ob, t0 + i * 0.25 - 0.05, False)
        sets.set_obj_visible(ob, t0 + i * 0.25, True)


# ================================================================== PART 1: the rule (0-30s)
@S(1, 0, 3, "HOOK: Eddie by the window, snowy night town, whip to door")
def k01(t0, t1):
    knock_street(night=True)
    snow(t0, t1, 40, seed=1)
    E = eddie(t0, t1, "worried")
    E.walk(t0, t1, (-1.2, -18, 0), (-0.4, -12, 0), rate=2.2)
    cam = Cam()
    cam.key(t0, (7, -30, 1.2), (0, -8, 6), lens=22, focus=(0, -14, 4), fstop=4)
    cam.key(t1, (2.4, -22, 5.2), (-0.4, -12, 5), lens=28, focus=(-0.4, -12, 4.7), fstop=3, ease="EASE_OUT")
    cam.crash(t0 + 1.7, 28, 34, 0.12)
    cam.handheld(1.3)
    sfx(t0, "whoosh")
    sfx(t0 + 0.2, "wind", 0.7)


@S(2, 3, 10, "You never open the door after midnight: front door, locks, clock")
def k02(t0, t1):
    hall_set()
    card("clk", 2.6, 2.6, (6, 11.4, 8.5), img_mat("clock_1200", os.path.join(TEX, "clock_1200.png"), 0.5), "-Y")
    cam = Cam()
    cam.key(t0, (-4, -8, 3.2), (0, 11, 5), lens=22, focus=(0, 11, 5), fstop=5)
    cam.key(t1, (0.6, 2, 5.0), (0, 11, 5), lens=26, focus=(0, 11, 5), fstop=5, ease="EASE_IN")
    cam.crash(t0 + 0.4, 22, 32, 0.12)
    cam.handheld(1.1)
    sfx(t0 + 0.4, "boom")
    sfx(t0 + 0.45, "sting")
    sfx(t0 + 2.2, "ding", 0.6)


@S(3, 10, 13, "Not for friends: Tootie's shape outside, red X")
def k03(t0, t1):
    hall_set()
    bubble(t0 + 0.2, t1, (0, 9.6, 7.4), "TOOTIE?", (1, 0.85, 0.7), 1.2)
    text("x1", "X", (0, 9.4, 4.0), 3.0, mat("red_txt", (1, 0.1, 0.1), 0.4, emit=(1, 0.1, 0.1), estr=4.0), rot=(90, 0, 0), extrude=0.3)
    cam = push_cam(t0, t1, (0, 11, 4.8), 18, 12, yaw=-8, yaw1=8, lens=24)
    door_knock(t0 + 0.4)
    sfx(t0 + 0.9, "buzzer", 0.6)


@S(4, 13, 16, "Not for family: FAMILY? bubble, red X")
def k04(t0, t1):
    hall_set()
    bubble(t0 + 0.2, t1, (0, 9.6, 7.4), "FAMILY?", (1, 0.85, 0.7), 1.2)
    text("x1", "X", (0, 9.4, 4.0), 3.0, mat("red_txt", (1, 0.1, 0.1), 0.4, emit=(1, 0.1, 0.1), estr=4.0), rot=(90, 0, 0), extrude=0.3)
    cam = push_cam(t0, t1, (0, 11, 4.8), 12, 17, yaw=10, yaw1=-8, lens=24)
    door_knock(t0 + 0.3)
    sfx(t0 + 0.9, "buzzer", 0.6)


@S(5, 16, 20, "Not even for Mom: Mom behind the door glow, red X")
def k05(t0, t1):
    hall_set()
    bubble(t0 + 0.2, t1, (0, 9.6, 7.4), "MOM?", (1, 0.85, 0.7), 1.5)
    text("x1", "X", (0, 9.4, 4.0), 3.0, mat("red_txt", (1, 0.1, 0.1), 0.4, emit=(1, 0.1, 0.1), estr=4.0), rot=(90, 0, 0), extrude=0.3)
    cam = push_cam(t0, t1, (0, 11, 4.8), 14, 8, yaw=0, lens=24, lens1=34)
    door_knock(t0 + 0.2)
    cam.crash(t0 + 0.2, 24, 34, 0.12)
    sfx(t0 + 0.9, "buzzer", 0.7)
    sfx(t0 + 1.0, "sting")


@S(6, 20, 25, "Three locks: locks close-up, they click shut")
def k06(t0, t1):
    hall_set()
    cam = Cam()
    cam.key(t0, (-1.5, 2, 2.0), (1.5, 11, 4.2), lens=34, focus=(1.5, 11, 4.2), fstop=3)
    cam.key(t1, (0.4, 6, 5.8), (1.5, 11, 4.2), lens=34, focus=(1.5, 11, 4.2), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    for i in range(3):
        sfx(t0 + 0.5 + i * 0.7, "click")
        sfx(t0 + 0.5 + i * 0.7, "clink", 0.5)


@S(7, 25, 28, "A bell")
def k07(t0, t1):
    hall_set()
    b = bpy.data.objects["bell"]
    for i in range(10):
        b.rotation_euler[1] = math.radians(14 * (-1) ** i)
        b.keyframe_insert("rotation_euler", index=1, frame=F(t0 + 0.3 + i * 0.12))
    cam = Cam()
    cam.key(t0, (-5, 3, 5.4), (-2.9, 11, 7.0), lens=38, focus=(-2.9, 11, 7.0), fstop=2.5)
    cam.key(t1, (-3.4, 7, 6.8), (-2.9, 11, 7.0), lens=40, focus=(-2.9, 11, 7.0), fstop=2.5, ease="EASE_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.3, "ding")
    sfx(t0 + 0.6, "ding", 0.7)


@S(8, 28, 30, "And a sign")
def k08(t0, t1):
    hall_set()
    cam = Cam()
    cam.key(t0, (-6, 2, 4.0), (-2.9, 11, 4.6), lens=32, focus=(-2.9, 11, 4.6), fstop=3)
    cam.key(t1, (-3.2, 6, 4.8), (-2.9, 11, 4.6), lens=36, focus=(-2.9, 11, 4.6), fstop=3, ease="EASE_IN")
    cam.crash(t0 + 0.1, 32, 40, 0.1)
    cam.handheld(1.0)
    sfx(t0, "stomp", 0.8)
    sfx(t0 + 0.05, "sting", 0.7)


@S(9, 30, 36, "If they knock, it's not them: three knocks, crash zoom, red flash")
def k09(t0, t1):
    hall_set()
    for i in range(3):
        door_knock(t0 + 0.5 + i * 0.6, 1.4)
    bubble(t0 + 1.9, t1, (0, 9.6, 7.4), "NOT THEM", (1, 0.2, 0.2), 1.4)
    cam = push_cam(t0, t1, (0, 11, 4.8), 16, 8, yaw=0, lens=24, lens1=36, hh=1.8)
    cam.crash(t0 + 1.9, 28, 40, 0.1)
    sfx(t0 + 1.9, "boom")
    sfx(t0 + 1.95, "sting")


@S(10, 36, 42, "The knockers come from the woods: dark woods, glowing eyes")
def k10(t0, t1):
    knock_street(night=True)
    for i, (x, y) in enumerate(((-14, 46), (-6, 52), (4, 48), (12, 54), (0, 58))):
        for sx in (-1, 1):
            sphere(f"ke{i}{sx}", 0.18, (x + sx * 0.4, y, 5.0 + (i % 2)), mat("eye_glow", (1, 1, 0.85), 0.3, emit=(1, 1, 0.85), estr=14.0))
    cam = Cam()
    cam.key(t0, (-6, -6, 3.5), (0, 52, 5), lens=22, focus=(0, 50, 5), fstop=8)
    cam.key(t1, (4, 14, 5.0), (0, 52, 5), lens=28, focus=(0, 52, 5), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0, "wind", 0.8)
    sfx(t0 + 1.4, "zombie", 0.5)
    sfx(t0 + 3.4, "sting", 0.6)


@beat(42, 50, n=2, focus=(0, 40, 4.4), d=22, lens=24, desc="They sound exactly like the people you love: voices from the dark", pitch=3)
def k11(t0, t1):
    knock_street(night=True)
    D2 = double_dad(t0, t1, "happy")
    D2.pose(t0, loc=(-6, 44, 0), rot=180)
    Mm = mom(t0, t1, "happy")
    hood_eyes(Mm)
    Mm.pose(t0, loc=(6, 46, 0), rot=180)
    for i, (b, x) in enumerate((("DAD?", -6), ("HONEY?", 6), ("OPEN UP!", 0))):
        bubble(t0 + 0.4 + i * 0.7, t1, (x, 40, 10 - i), b, (0.8, 0.9, 1), 1.2)
        sfx(t0 + 0.4 + i * 0.7, "pop")
    cam = push_cam(t0, t1, (0, 40, 4.4), 26, 18, yaw=0, yaw1=-10, lens=24)


@S(12, 50, 55, "Mrs. Dean opens the door for her husband")
def k12(t0, t1):
    hall_set()
    G = story_grandma = grandma(t0, t1, "happy")
    G.pose(t0, loc=(0, 6, 0), rot=180)
    G.walk(t0, t0 + 1.4, (0, 2, 0), (0, 8.4, 0), rate=2.0)
    G.pose(t0 + 1.4, rot=180)
    G.act(t0 + 1.6, "reach", expr="happy")
    bubble(t0 + 0.3, t0 + 2.0, (0, 9.6, 8.2), "HONEY?", (1, 0.85, 0.7), 1.2)
    d = bpy.data.objects["fdoor"]
    d.keyframe_insert("location", index=0, frame=F(t0 + 2.2))
    d.location[0] = 3.4
    d.keyframe_insert("location", index=0, frame=F(t1))
    light("outl", "POINT", (0, 13, 4), 1400, (0.8, 0.9, 1.0), 1.0)
    cam = push_cam(t0, t1, (0, 8, 4.8), 11, 7.5, yaw=-14, yaw1=10, lens=26, hh=1.3)
    sfx(t0 + 0.4, "footsteps", 0.6)
    sfx(t0 + 1.6, "click")
    sfx(t0 + 2.2, "door")
    sfx(t0 + 2.4, "sting")


@S(13, 55, 59, "...for her husband, once: Mrs. Dean on the doorstep, a shape grows behind her")
def k13(t0, t1):
    hall_set()
    G = grandma(t0, t1, "gasp")
    G.pose(t0, loc=(0, 8.4, 0), rot=180)
    d = bpy.data.objects["fdoor"]
    d.location[0] = 3.4
    D2 = double_dad(t0, t1, "happy")
    D2.pose(t0, loc=(0, 14, 0), rot=0)
    D2.pose(t1, loc=(0, 10, 0))
    light("outl", "POINT", (0, 13, 4), 1400, (0.8, 0.9, 1.0), 1.0)
    cam = push_cam(t0, t1, (0, 10, 4.8), 10, 6.5, yaw=-8, yaw1=8, lens=28, lens1=34, hh=1.4)
    sfx(t0, "sting")


@S(14, 59, 65, "In the morning she was gone: empty hallway, door ajar, a slipper")
def k14(t0, t1):
    hall_set()
    d = bpy.data.objects["fdoor"]
    d.location[0] = 3.4
    box("slipper", (0.9, 1.5, 0.4), (-1, 5, 0.25), M("#c8508a", 0.8), 0.15)
    light("morn", "AREA", (0, 13, 6), 1500, (1.0, 0.9, 0.7), 8, target=(0, 0, 1))
    cam = Cam()
    cam.key(t0, (1.5, -7, 2.4), (0, 8, 1.8), lens=26, focus=(-1, 5, 0.5), fstop=3)
    cam.key(t1, (-0.2, -2, 1.4), (-1, 8, 1.0), lens=30, focus=(-1, 5, 0.5), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "wind", 0.6)
    sfx(t0 + 1.8, "crickets", 0.7)


@beat(65, 74, n=2, focus=(-4, 6, 3.4), d=12, lens=26, desc="Her husband had been asleep upstairs the whole time")
def k15(t0, t1):
    bed_set()
    H = dadc(t0, t1, "sleepy")
    sleeper(H, t0, t1)
    zzz(t0 + 0.2, t1, (-2, 6, 4.5))
    cam = push_cam(t0, t1, (-4, 6, 3.2), 14, 9, yaw=-18, yaw1=14, lens=26)
    sfx(t0 + 0.4, "snort", 0.5)
    sfx(t0 + 1.6, "crickets", 0.6)
    sfx(t0 + 4.8, "snort", 0.5)


@S(16, 74, 79, "So we sleep with earplugs: Eddie in bed, earplugs pop in")
def k16(t0, t1):
    bed_set()
    E = eddie(t0, t1, "happy")
    sleeper(E, t0, t1)
    E.face(t0 + 0.2, "relief")
    cam = push_cam(t0, t1, (-4, 7, 3.6), 11, 6.5, yaw=-20, yaw1=10, lens=28, lens1=34)
    sfx(t0 + 0.8, "pop")
    sfx(t0 + 1.4, "pop")
    sfx(t0 + 2.6, "aww", 0.5)


@S(17, 79, 84, "Even babies wear tiny headphones")
def k17(t0, t1):
    room("#f6dce8", "#e8d8c0", key=5200)
    for i, x in enumerate((-6, 0, 6)):
        box(f"crib{i}", (4.6, 4.0, 0.3), (x, 7, 1.6), M("#ffffff", 0.5), 0.05)
        b = baby(i, t0, t1, "happy")
        b.root.scale = (0.85,) * 3
        b.pose(t0, loc=(x, 7, 2.2), rot=0)
        for sx in (-1, 1):
            cyl(f"hp{i}{sx}", 0.4, 0.3, (sx * 0.78, 0, 0.1), M("#e8423a", 0.4), 16, rot=(0, 90, 0), parent=b.head)
        box(f"hpb{i}", (1.6, 0.18, 0.18), (0, 0, 0.72), M("#2a2a2e", 0.4), 0.05, parent=b.head)
        b.talk(t0, t1, open_m="ah", wide_m="open_smile", rest="smile", syll=0.3)
    cam = push_cam(t0, t1, (0, 7, 3.8), 14, 9, yaw=-10, yaw1=10, lens=26)
    sfx(t0 + 0.3, "aww", 0.7)
    sfx(t0 + 2.0, "squeak", 0.6)


@beat(84, 99, n=2, focus=(0, -8, 4.6), d=11, lens=28, desc="Tootie explains: the knockers can't come in unless you open the door")
def k18(t0, t1):
    hall_set()
    T = tootie(t0, t1, "smug")
    T.pose(t0, loc=(2, -2, 0), rot=-30)
    T.act(t0 + 0.4, "point", expr="smug")
    T.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk_wide", rest="smile")
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(-2.2, -2, 0), rot=30)
    cam = push_cam(t0, t1, (0, -2, 4.6), 12, 8, yaw=-10, yaw1=12, lens=28)
    sfx(t0 + 2.0, "click", 0.6)


@S(19, 99, 105, "Rock and roll! We're losing control!")
def k19(t0, t1):
    hall_set()
    T = tootie(t0, t1, "scream")
    T.pose(t0, loc=(2, -2, 0), rot=-15)
    T.panic(t0, t1, rate=7)
    E = eddie(t0, t1, "scream")
    E.pose(t0, loc=(-2, -2, 0), rot=15)
    E.panic(t0 + 0.1, t1, rate=6)
    cam = push_cam(t0, t1, (0, -2, 4.6), 12, 7.5, yaw=-10, yaw1=12, lens=26, hh=2.8)
    sfx(t0, "whoosh")
    sfx(t0 + 0.9, "rimshot", 0.6)


# ================================================================== PART 2: the night (105-end)
@S(20, 105, 112, "Last night, at 3 a.m., someone knocked: clock at 3:00")
def k20(t0, t1):
    hall_set()
    card("clk", 4.0, 4.0, (0, 11.4, 8.5), img_mat("clock_0300", os.path.join(TEX, "clock_0300.png"), 0.5), "-Y")
    door_knock(t0 + 4.6)
    cam = Cam()
    cam.key(t0, (-4, -6, 5.0), (0, 11, 8.5), lens=26, focus=(0, 11, 8.5), fstop=4)
    cam.key(t1, (0.6, 3, 8.4), (0, 11, 8.5), lens=32, focus=(0, 11, 8.5), fstop=4, ease="EASE_IN")
    cam.crash(t0 + 4.6, 32, 42, 0.1)
    cam.handheld(1.1)
    sfx(t0, "ding", 0.6)
    sfx(t0 + 2.4, "crickets", 0.6)


@S(21, 112, 115, "Three slow knocks: the door shakes with each, cam punches")
def k21(t0, t1):
    hall_set()
    for i in range(3):
        door_knock(t0 + 0.25 + i * 0.95, 1.6)
    cam = push_cam(t0, t1, (0, 11, 4.8), 14, 9, yaw=0, lens=26, lens1=32, hh=2.0)
    for i in range(3):
        cam.crash(t0 + 0.25 + i * 0.95, 26, 33, 0.1)
        sfx(t0 + 0.25 + i * 0.95, "boom", 0.6)


@S(22, 115, 118, "Buddy, it's Dad!: Eddie hears it, bubble")
def k22(t0, t1):
    hall_set()
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(0, 0, 0), rot=180)
    bubble(t0 + 0.1, t1, (0, 9.6, 8.0), "BUDDY, IT'S DAD!", (1, 0.85, 0.6), 1.0)
    cam = push_cam(t0, t1, (0, 2, 4.8), 8, 5.4, yaw=170, yaw1=190, lens=28, hh=1.2)
    sfx(t0 + 0.1, "ding")
    sfx(t0 + 0.2, "gasp")


@S(23, 118, 131, "I went out to check the car and the door locked behind me: Eddie listens")
def k23(t0, t1):
    hall_set()
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(0, -4, 0), rot=0)
    E.act(t0 + 0.4, "think", expr="sus")
    bubble(t0 + 0.1, t1, (0, 9.6, 8.0), "I WENT TO CHECK THE CAR...", (1, 0.85, 0.6), 0.7)
    cam = push_cam(t0, t1, (0, -4, 4.6), 9, 6, yaw=-14, yaw1=10, lens=28, lens1=34)
    sfx(t0 + 0.4, "click", 0.6)
    sfx(t0 + 2.4, "click", 0.6)


@S(24, 131, 134, "Let me in!: door slams")
def k24(t0, t1):
    hall_set()
    for i in range(3):
        door_knock(t0 + i * 0.35, 1.8)
    bubble(t0 + 0.1, t1, (0, 9.6, 8.0), "LET ME IN!", (1, 0.4, 0.3), 1.6)
    cam = push_cam(t0, t1, (0, 11, 4.8), 12, 7, yaw=0, lens=26, lens1=36, hh=2.6)
    cam.crash(t0, 26, 40, 0.1)
    sfx(t0 + 0.1, "sting")


@S(25, 134, 139, "I looked down the hallway: Eddie turns, long hallway view")
def k25(t0, t1):
    hall_set()
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(0, 2, 0), rot=180)
    look(E, t0 + 0.6, -60, 0)
    cam = Cam()
    cam.key(t0, (6, -8, 4.0), (-14, 4, 4.0), lens=22, focus=(-14, 4, 4), fstop=5)
    cam.key(t1, (3, -6, 4.6), (-14, 4, 4.0), lens=26, focus=(-14, 4, 4), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.5, "footsteps", 0.5)


@S(26, 139, 144, "Dad's bedroom door was open: dark doorway with warm slit")
def k26(t0, t1):
    hall_set()
    bd = bpy.data.objects["bdoor"]
    bd.rotation_euler[2] = math.radians(70)
    bd.location = (-13.2, 5.6, 4.0)
    box("darkhole", (0.2, 3.4, 8.0), (-14.9, 4, 4.0), M("#050505", 0.9), 0)
    light("slit", "SPOT", (-14.2, 4, 7), 600, (1.0, 0.7, 0.4), 0.5, spot=30, target=(-6, 3, 0))
    cam = Cam()
    cam.key(t0, (-3, -2, 3.8), (-14.6, 4, 4.0), lens=26, focus=(-14.6, 4, 4), fstop=4)
    cam.key(t1, (-8, 2, 4.2), (-14.6, 4, 4.0), lens=30, focus=(-14.6, 4, 4), fstop=4, ease="EASE_IN")
    cam.handheld(1.0)
    sfx(t0, "door", 0.6)
    sfx(t0 + 0.3, "sting", 0.7)


@S(27, 144, 149, "I could hear him snoring: ZZZ near the doorway")
def k27(t0, t1):
    hall_set()
    box("darkhole", (0.2, 3.4, 8.0), (-14.9, 4, 4.0), M("#050505", 0.9), 0)
    zzz(t0 + 0.2, t1, (-12, 4, 5.5), n=4)
    cam = Cam()
    cam.key(t0, (-6, -3, 4.4), (-14.6, 4, 5.0), lens=30, focus=(-14.6, 4, 5), fstop=3)
    cam.key(t1, (-9.5, 1, 4.8), (-14.6, 4, 5.0), lens=34, focus=(-14.6, 4, 5), fstop=3, ease="EASE_OUT")
    cam.handheld(0.9)
    for i in range(3):
        sfx(t0 + 0.3 + i * 1.3, "snort", 0.4)


@S(28, 149, 154, "So, it was a knocker: realization, crash zoom")
def k28(t0, t1):
    hall_set()
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(0, -2, 0), rot=0)
    E.act(t0 + 0.9, "shock", expr="terror")
    cam = push_cam(t0, t1, (0, -2, 4.8), 10, 5.5, yaw=-10, yaw1=8, lens=30, lens1=38, hh=1.6)
    cam.crash(t0 + 1.0, 30, 42, 0.1)
    sfx(t0 + 0.9, "boom")
    sfx(t0 + 0.95, "sting")


@S(29, 154, 157, "I didn't move: frozen Eddie, sweat")
def k29(t0, t1):
    hall_set()
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(0, -2, 0), rot=0)
    cam = push_cam(t0, t1, (0, -2, 4.8), 8, 4.8, yaw=0, lens=32, lens1=42, hh=0.7)
    sfx(t0, "rise", 0.7)


@S(30, 157, 164, "The knocking stopped. Then it started again: silence then door shakes")
def k30(t0, t1):
    hall_set()
    door_knock(t0 + 3.2, 1.5)
    door_knock(t0 + 3.5, 1.5)
    cam = push_cam(t0, t1, (0, 11, 4.8), 15, 12, yaw=0, lens=24, hh=0.8)
    cam.crash(t0 + 3.2, 24, 34, 0.1)
    sfx(t0 + 0.6, "crickets", 0.8)


@S(31, 164, 165, "Faster.")
def k31(t0, t1):
    hall_set()
    for i in range(8):
        door_knock(t0 + i * 0.12, 1.2)
    cam = push_cam(t0, t1, (0, 11, 4.8), 12, 8, yaw=0, lens=26, lens1=34, hh=3.0)
    sfx(t0, "thud")


@S(32, 165, 166, "Different. (slow knocks)")
def k32(t0, t1):
    hall_set()
    door_knock(t0 + 0.1, 2.0)
    cam = push_cam(t0, t1, (0, 11, 4.8), 8, 6, yaw=0, lens=30, lens1=38, hh=1.0)
    sfx(t0, "sting", 0.7)


@beat(166, 183, n=2, focus=(0, 8, 4.6), d=9, lens=30, desc="Son, listen to me. Don't open the door. Don't wake the one sleeping in my bed")
def k33(t0, t1):
    hall_set()
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(0, 2, 0), rot=180)
    bubble(t0 + 0.1, t1, (0, 9.6, 8.0), "DON'T OPEN THE DOOR", (0.8, 0.9, 1.0), 0.9)
    cam = push_cam(t0, t1, (0, 2, 4.6), 10, 6, yaw=160, yaw1=190, lens=28, hh=1.0)
    sfx(t0 + 0.1, "sting", 0.7)
    sfx(t0 + 2.2, "whoosh", 0.5)


@S(34, 183, 188, "My whole body went cold: Eddie shivers, frost vignette")
def k34(t0, t1):
    hall_set()
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(0, -2, 0), rot=0)
    for i in range(14):
        E.pose(t0 + i * 0.1, head=(2 * (-1) ** i, 4, 3 * (-1) ** i), torso=(0, 3, 2 * (-1) ** i))
    cam = push_cam(t0, t1, (0, -2, 4.8), 9, 5, yaw=-8, yaw1=8, lens=30, lens1=40, hh=2.2)
    sfx(t0, "rise", 0.8)
    sfx(t0 + 0.3, "wind", 0.6)


@S(35, 188, 194, "The snoring stopped: dark doorway, ZZZ vanish")
def k35(t0, t1):
    hall_set()
    box("darkhole", (0.2, 3.4, 8.0), (-14.9, 4, 4.0), M("#050505", 0.9), 0)
    zzz(t0, t0 + 0.8, (-12, 4, 5.5), n=3)
    cam = Cam()
    cam.key(t0, (-6, -3, 4.4), (-14.6, 4, 4.6), lens=30, focus=(-14.6, 4, 4.6), fstop=3)
    cam.key(t1, (-8, 0, 4.4), (-14.6, 4, 4.6), lens=36, focus=(-14.6, 4, 4.6), fstop=3, ease="EASE_IN")
    cam.handheld(0.8)
    sfx(t0 + 0.8, "crickets", 0.8)
    sfx(t0 + 3.4, "sting", 0.7)


@beat(194, 200, n=2, focus=(-8, 4, 3.0), d=16, lens=24, desc="Footsteps. Slow. Coming down the hallway.", pitch=3)
def k36(t0, t1):
    hall_set()
    D2 = double_dad(t0, t1, "happy")
    D2.pose(t0, loc=(-13.6, 4, 0), rot=90)
    D2.walk(t0, t1, (-13.6, 4, 0), (-3, 1, 0), rate=1.7)
    D2.pose(t0, rot=90)
    cam = push_cam(t0, t1, (-8, 3, 3.0), 18, 12, yaw=10, yaw1=-14, lens=24, hh=1.2)
    for i in range(5):
        sfx(t0 + 0.3 + i * 0.9, "footsteps", 0.7)


@S(37, 200, 205, "Buddy? Said a voice behind me: Eddie's back, Dad double behind")
def k37(t0, t1):
    hall_set()
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(0, 2, 0), rot=180)
    D2 = double_dad(t0, t1, "happy")
    D2.pose(t0, loc=(0, -6, 0), rot=0)
    D2.pose(t1, loc=(0, -3, 0))
    bubble(t0 + 0.2, t1, (2.4, -1, 8.0), "BUDDY?", (1, 0.9, 0.7), 1.1, rot=(90, 0, 180))
    cam = Cam()
    cam.key(t0, (0, 9, 5.5), (0, 0, 4.4), lens=26, focus=(0, 2, 4.4), fstop=3)
    cam.key(t1, (0.4, 6, 5.2), (0, 0, 4.6), lens=32, focus=(0, 2, 4.6), fstop=3, ease="EASE_IN")
    cam.handheld(1.4)
    sfx(t0 + 0.2, "sting")
    sfx(t0 + 0.3, "rise", 0.7)


@S(38, 205, 210, "Dad's voice. Sleepy. Kind.: warm smile of the double, but glowing eyes")
def k38(t0, t1):
    hall_set()
    D2 = double_dad(t0, t1, "happy")
    D2.pose(t0, loc=(0, -2, 0), rot=0)
    D2.act(t0 + 0.4, "lean", expr="happy")
    D2.face(t0 + 1.5, "smile")
    cam = push_cam(t0, t1, (0, -2, 4.9), 9, 5.4, yaw=-10, yaw1=10, lens=30, lens1=36, hh=1.0)
    sfx(t0 + 0.2, "aww", 0.5)
    sfx(t0 + 2.0, "zombie", 0.4)


@S(39, 210, 214, "Who's at the door?: Dad double leans toward the camera")
def k39(t0, t1):
    hall_set()
    D2 = double_dad(t0, t1, "smile")
    D2.pose(t0, loc=(0, -2, 0), rot=0)
    D2.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk", rest="smile")
    cam = push_cam(t0, t1, (0, -2, 4.9), 7, 4.6, yaw=0, lens=32, lens1=44, hh=1.2)
    sfx(t0 + 0.3, "sting", 0.6)


@S(40, 214, 218, "I didn't turn around: Eddie sweating, eyes shut")
def k40(t0, t1):
    hall_set()
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(0, 2, 0), rot=180)
    E.face(t0 + 0.6, eyes="closed", mouth="grimace_wide")
    cam = Cam()
    cam.key(t0, (-2, 9, 5.0), (0, 2, 4.6), lens=30, focus=(0, 2, 4.6), fstop=2.8)
    cam.key(t1, (0.2, 6.5, 5.0), (0, 2, 4.6), lens=40, focus=(0, 2, 4.6), fstop=2.8, ease="EASE_IN")
    cam.handheld(2.0)
    sfx(t0, "rise", 0.9)


@S(41, 218, 224, "Outside, the real Dad whispered: through the window, Dad outside in the snow")
def k41(t0, t1):
    hall_set()
    snow(t0, t1, 30, area=((8, 18), (-2, 8)), seed=3)
    D_ = dadc(t0, t1, "worried")
    D_.pose(t0, loc=(18, 3, 0), rot=90)
    D_.act(t0 + 0.4, "reach", expr="scared")
    D_.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk", rest="frown")
    light("outw", "POINT", (17, 2, 6), 800, (0.7, 0.8, 1.0), 1.0)
    cam = Cam()
    cam.key(t0, (6, -4, 4.8), (14.7, 3, 5.0), lens=28, focus=(14.7, 3, 5.0), fstop=4)
    cam.key(t1, (11, 1, 5.0), (14.7, 3, 5.0), lens=34, focus=(14.7, 3, 5.0), fstop=4, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0, "wind", 0.7)


@S(42, 224, 231, "It slipped inside when I opened the door: Dad's face, worried, bubble")
def k42(t0, t1):
    hall_set()
    D_ = dadc(t0, t1, "worried")
    D_.pose(t0, loc=(18, 3, 0), rot=90)
    D_.talk(t0, t1, V.span(t0, t1), open_m="talk", wide_m="talk_wide", rest="frown")
    bubble(t0 + 0.2, t1, (13.6, 2.4, 9), "IT'S INSIDE!", (1, 0.8, 0.6), 1.2, rot=(90, 0, 90))
    light("outw", "POINT", (17, 2, 6), 800, (0.7, 0.8, 1.0), 1.0)
    cam = Cam()
    cam.key(t0, (8, -2, 5.0), (14.7, 3, 5.0), lens=30, focus=(14.7, 3, 5.0), fstop=3)
    cam.key(t1, (12, 2.4, 5.2), (14.7, 3, 5.0), lens=38, focus=(14.7, 3, 5.0), fstop=3, ease="EASE_IN")
    cam.handheld(1.4)
    sfx(t0 + 0.2, "sting")
    sfx(t0 + 3.5, "rise", 0.7)


@S(43, 231, 235, "Run to the window!: window crash zoom")
def k43(t0, t1):
    hall_set()
    D_ = dadc(t0, t1, "scream")
    D_.pose(t0, loc=(18, 3, 0), rot=90)
    D_.panic(t0, t1, rate=6)
    cam = Cam()
    cam.key(t0, (6, -4, 4.8), (14.7, 3, 5.0), lens=26, focus=(14.7, 3, 5.0), fstop=4)
    cam.key(t1, (11, 1, 5.0), (14.7, 3, 5.0), lens=28, focus=(14.7, 3, 5.0), fstop=4, ease="EASE_IN")
    cam.crash(t0 + 0.2, 26, 40, 0.1)
    cam.handheld(2.4)
    sfx(t0 + 0.2, "boom", 0.7)
    sfx(t0 + 0.4, "whoosh")


@S(44, 235, 238, "I ran: Eddie sprints to the window")
def k44(t0, t1):
    hall_set()
    E = eddie(t0, t1, "scream")
    E.pose(t0, loc=(0, 2, 0), rot=-90)
    E.run(t0, t1, (0, 2, 0), (12.6, 3, 0))
    E.pose(t0, rot=-90)
    cam = Cam()
    cam.key(t0, (-6, -6, 4.0), (4, 2, 4), lens=22, focus=(4, 2, 4), fstop=6)
    cam.key(t1, (6, -8, 4.5), (12, 3, 4.4), lens=22, focus=(12, 3, 4.4), fstop=6, ease="EASE_IN")
    cam.handheld(2.0)
    sfx(t0, "whoosh")
    sfx(t0 + 0.2, "footsteps", 0.9)


@S(45, 238, 245, "I jumped out and fell into the snow: window shatters, Eddie lands in a snow drift")
def k45(t0, t1):
    knock_street(night=True, fog=False)
    house_front((0, -14, 0))
    box("drift", (14, 7, 1.8), (0, -22, 0.8), M("#f4f6ff", 0.9), 0.5)
    snow(t0, t1, 36, seed=5)
    E = eddie(t0, t1, "scream")
    E.pose(t0, loc=(8, -18, 9.0), rot=90)
    E.pose(t0 + 0.7, loc=(8, -20, 9.0))
    E.pose(t0 + 1.6, loc=(8, -22, 1.6))
    E.panic(t0, t0 + 1.6, rate=7)
    E.face(t0 + 1.7, "shock")
    E.pose(t0 + 1.9, rot=180, hipz=-0.8, torso=(0, 20, 0))
    cam = Cam()
    cam.key(t0, (-4, -42, 5), (6, -18, 8), lens=22, focus=(6, -18, 8), fstop=6)
    cam.key(t1, (3, -36, 4), (6, -22, 2), lens=24, focus=(6, -22, 2), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(1.5)
    sfx(t0 + 0.4, "window")
    sfx(t0 + 1.6, "splat")
    sfx(t0 + 1.65, "thud", 0.7)


@beat(245, 257, n=2, focus=(0, -30, 4.2), d=15, lens=24, desc="Dad grabbed me and we ran all the way to Tootie's house", pitch=3)
def k46(t0, t1):
    knock_street(night=True)
    snow(t0, t1, 30, seed=7)
    D_ = dadc(t0, t1, "worried")
    D_.pose(t0, loc=(-1.5, -14, 0), rot=0)
    D_.run(t0, t1, (-1.5, -14, 0), (-1.5, -44, 0))
    E = eddie(t0, t1, "scream")
    E.pose(t0, loc=(1.5, -14, 0), rot=0)
    E.run(t0, t1, (1.5, -14, 0), (1.5, -44, 0))
    cam = Cam()
    cam.key(t0, (-8, -8, 3.5), (0, -20, 4.2), lens=24, focus=(0, -20, 4.2), fstop=6)
    cam.key(t1, (8, -38, 4.5), (0, -42, 4.2), lens=26, focus=(0, -42, 4.2), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(2.0)
    sfx(t0, "footsteps", 0.9)
    sfx(t0 + 1.2, "footsteps", 0.9)
    sfx(t0 + 2.4, "footsteps", 0.9)
    sfx(t0 + 2.5, "whoosh", 0.5)


@S(47, 257, 264, "Behind us, our front door slowly opened: house front, door slides open, warm glow")
def k47(t0, t1):
    knock_street(night=True, fog=False)
    house_front((0, -14, 0))
    d = bpy.data.objects["hs_door"]
    d.keyframe_insert("location", index=0, frame=F(t0 + 2.4))
    d.location[0] = 3.0
    d.keyframe_insert("location", index=0, frame=F(t0 + 5.4))
    set_interp(d, "location", F(t0 + 2.4), "BEZIER", "EASE_IN_OUT")
    box("dark_in", (2.4, 0.2, 5.0), (0, -17.05, 5.5), M("#050505", 0.9), 0)
    light("inglow", "POINT", (0, -15, 4.5), 500, (1.0, 0.7, 0.35), 1.0)
    snow(t0, t1, 30, seed=9)
    cam = Cam()
    cam.key(t0, (14, -48, 2.4), (0, -14, 4.5), lens=26, focus=(0, -14, 4.5), fstop=5)
    cam.key(t1, (3, -38, 3.2), (0, -14, 4.8), lens=34, focus=(0, -14, 4.8), fstop=4, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 2.4, "door")
    sfx(t0 + 2.6, "rise", 0.7)
    sfx(t0 + 5.2, "sting")


@beat(264, None, n=3, focus=(0, -17, 4.6), d=16, lens=30, desc="Something with Dad's face waved goodbye", pitch=3)
def k48(t0, t1):
    knock_street(night=True, fog=False)
    house_front((0, -14, 0))
    d = bpy.data.objects["hs_door"]
    d.location[0] = 3.0
    box("dark_in", (2.4, 0.2, 5.0), (0, -17.05, 5.5), M("#050505", 0.9), 0)
    light("inglow", "POINT", (0, -15, 4.5), 700, (1.0, 0.7, 0.35), 1.0)
    D2 = double_dad(t0, t1, "grin")
    D2.pose(t0, loc=(0, -16.4, 0.6), rot=0)
    D2.act(t0 + 0.4, "wave", expr="grin")
    D2.pose(t0 + 0.5, armR=(165, 25))
    wiggle = acting.wiggle
    wiggle(D2, t0 + 0.7, t1, "armR", (10, 15), 4.0, (160, 25))
    snow(t0, t1, 30, seed=11)
    cam = push_cam(t0, t1, (0, -17, 4.6), 18, 9, yaw=0, yaw1=-6, lens=28, lens1=34, hh=0.8)
    sfx(t0 + 0.4, "sting")
    sfx(t0 + 1.0, "zombie", 0.5)
    sfx(t0 + 2.8, "wind", 0.7)
