"""town: "In this town, laughing is illegal." Laughter keeps the swamp town afloat.
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


# ================================================================== PART 1 : the rule (0 - 16s)
@S(1, 0, 3, "HOOK: Eddie bites his lips on the street while a detector pole turns toward him")
def s01(t0, t1):
    town_scene()
    pole((7, -27, 0), swivel=(t0, t1, 40, -20))
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(-1.5, -31, 0), rot=0)
    E.walk(t0, t1, (-1.5, -31, 0), (-0.5, -34, 0), rate=2.6)
    E.pose(t0 + 0.5, armR=(150, -30)); E.pose(t1, armR=(150, -30))
    street_pair(t0, t1, 4, 2)
    cam = Cam()
    cam.key(t0, (13, -40, 1.0), (0, -30, 9), lens=22, focus=(-1, -32, 4.6), fstop=3.0)
    cam.key(t1, (3.5, -41.5, 5.4), (-0.8, -33, 5.0), lens=26, focus=(-0.8, -33, 4.6), fstop=3.0, ease="EASE_OUT")
    cam.crash(t0 + 1.9, 26, 32)
    cam.handheld(1.2)
    sfx(t0, "whoosh")


@S(2, 3, 6, "BIG sign: NO LAUGHING pole, crash zoom")
def s02(t0, t1):
    town_scene()
    pole((0, -30, 0), swivel=(t0, t1, 25, -10))
    cam = Cam()
    cam.key(t0, (6, -44, 6.4), (0, -30, 6.2), lens=26, focus=(0, -30, 6.2), fstop=4)
    cam.key(t1, (1.5, -37, 6.3), (0, -30, 6.2), lens=22, focus=(0, -30, 6.2), fstop=4, ease="EASE_IN")
    cam.crash(t0 + 0.3, 26, 40, 0.14)
    cam.handheld(1.0)
    sfx(t0, "boom")
    sfx(t0 + 0.05, "sting")


@S(3, 6, 9, "A kid laughs on the street: LAUGH ONCE")
def s03(t0, t1):
    town_scene()
    pole((9, -29, 0), swivel=(t0, t1, 50, 5))
    K = townie(2, t0, t1, "joy")
    K.pose(t0, loc=(-1, -32, 0), rot=0)
    laugh(K, t0 + 0.2, t1, flail=False)
    K.pose(t0 + 0.2, armL=(60, -20), armR=(60, -20))
    cam = Cam()
    cam.push(t0, t1, (-1, -32, 4.4), 12, 7.5, yaw=-18, pitch=5, lens=28, yaw1=-6, lens1=32)
    cam.crash(t0 + 0.2, 28, 36, 0.1)
    cam.handheld(1.4)
    sfx(t0 + 0.15, "kids_laugh")
    sfx(t0 + 1.55, "mclick")


@S(4, 9, 13, "A cop writes the fine, bills fly out of the kid's pockets")
def s04(t0, t1):
    town_scene()
    K = townie(2, t0, t1, "worried")
    K.pose(t0, loc=(-2.2, -32, 0), rot=25)
    C = cop(t0, t1, "angry")
    C.pose(t0, loc=(2.4, -32, 0), rot=-25)
    C.act(t0 + 0.2, "point", expr="shout")
    tk = plane("ticket", 1.4, 1.8, (0.3, -34.0, 4.5), img_mat("fine_ticket", os.path.join(TEX, "fine_ticket.png"), 0.6), (90, 0, 8))
    tk.scale = (0.01,) * 3
    tk.keyframe_insert("scale", frame=F(t0 + 0.4))
    tk.scale = (1, 1, 1)
    tk.keyframe_insert("scale", frame=F(t0 + 0.7))
    for i in range(7):
        b = bill(f"b{i}", (-2.2, -32.5, 3.0), rot=(90, 0, random.uniform(-30, 30)))
        spin(b, t0 + 1.8 + i * 0.07, t0 + 3.1, 0.0, seed=i)
        b.location = (-2.2, -32.5, 3.0)
        b.keyframe_insert("location", frame=F(t0 + 1.7 + i * 0.07))
        b.location = (random.uniform(-6, 6), random.uniform(-36, -33), random.uniform(5, 9))
        b.keyframe_insert("location", frame=F(t0 + 3.2))
        sets.set_obj_visible(b, t0 + 1.6 + i * 0.07, False)
        sets.set_obj_visible(b, t0 + 1.7 + i * 0.07, True)
    K.act(t0 + 1.6, "hands_head", expr="scream")
    cam = Cam()
    cam.push(t0, t1, (0, -32.5, 4.8), 13, 9, yaw=-10, pitch=4, lens=26, yaw1=14, lens1=30)
    cam.handheld(1.2)
    sfx(t0 + 0.4, "slap")
    sfx(t0 + 1.7, "chaching")


@S(5, 13, 18, "Track along the street poles")
def s05(t0, t1):
    town_scene()
    for i in range(5):
        pole((-6 + (i % 2) * 12, -22 - i * 7.5, 0), rot=(-1) ** i * 20, name=f"pl{i}", swivel=(t0, t1, 30 * (-1) ** i, -30 * (-1) ** i))
    cam = Cam()
    cam.key(t0, (0, -12, 3.0), (0, -50, 8.5), lens=20, focus=(0, -45, 8))
    cam.key(t1, (0, -26, 7.0), (0, -60, 11), lens=24, focus=(0, -50, 9), ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "whoosh")


@S(6, 18, 21, "Detector camera close-up: red light, swivel to lens")
def s06(t0, t1):
    town_scene()
    pole((0, -30, 0), swivel=(t0, t1 - 0.2, 70, 0), sign=None)
    cam = Cam()
    cam.key(t0, (-5, -40, 9.5), (0, -30, 11.8), lens=34, focus=(0, -31, 11.8), fstop=2.2)
    cam.key(t1, (-0.3, -35.5, 11.6), (0, -31, 11.9), lens=40, focus=(0, -31.7, 11.9), fstop=2.2, ease="EASE_IN")
    cam.handheld(0.8)
    sfx(t0 + 0.2, "notif")
    sfx(t1 - 0.5, "mclick")


@S(7, 21, 27, "Clowns in jail")
def s07(t0, t1):
    jail_set()
    cs = []
    for i, (x, y, r) in enumerate(((-5.5, 6.0, 10), (-1.0, 4.5, -8), (3.2, 6.5, 0))):
        c = clown(i, t0, t1, "cry" if i != 1 else "worried")
        c.pose(t0, loc=(x, y, 0), rot=r)
        c.act(t0 + 0.2 + i * 0.1, "slump")
        cs.append(c)
    cs[1].act(t0 + 0.3, "hands_face", expr="cry")
    cam = Cam()
    cam.push(t0, t1, (-1, 6, 4.0), 17, 12, yaw=-8, pitch=4, lens=26, yaw1=10, lens1=28)
    cam.handheld(0.8)
    sfx(t0 + 0.6, "door")
    sfx(t0 + 2.0, "crickets")


@beat(27, 33, n=2, focus=(0, 5, 4.5), d=12, lens=26, desc="Comedies play with no sound: family stares at a muted TV")
def s08(t0, t1):
    tv_set()
    fam = []
    for i, (x, mk) in enumerate(((-3.2, dadc), (0, mom), (3.2, None))):
        if mk:
            f = mk(t0, t1, "neutral")
        else:
            f = townie(5, t0, t1, "neutral")
        f.pose(t0, loc=(x, -1.5, 2.6), rot=180)
        fam.append(f)
    cam = Cam()
    cam.key(t0, (3.0, -17, 7.5), (0, 8, 4.6), lens=24, focus=(0, 8, 4.6), fstop=4)
    cam.key(t1, (-2.0, -12, 6.0), (0, 9, 4.6), lens=26, focus=(0, 9, 4.6), fstop=4, ease="EASE_IN_OUT")
    cam.handheld(0.7)
    sfx(t0 + 1.5, "crickets")
    sfx(t0 + 3.0, "faaah", 0.7)


# ================================================================== PART 2 : examples (33 - 62)
@S(9, 33, 38, "Dad giggles at work")
def s09(t0, t1):
    office_set()
    D = dadc(t0, t1, "neutral")
    D.pose(t0, loc=(0, 3.2, 0), rot=180 + 180)
    D.pose(t0, loc=(0, 3.4, 0), rot=0)
    D.face(t0 + 0.9, "grin")
    laugh(D, t0 + 1.0, t1, belly=False, amp=0.7, rate=7)
    D.pose(t0 + 1.0, armL=(100, -20), armR=(100, -20))
    D.face(t0 + 1.0, "joy")
    cam = Cam()
    cam.push(t0, t1, (0, 3.4, 5.0), 12, 8.2, yaw=-12, pitch=3, lens=28, yaw1=12, lens1=32)
    cam.crash(t0 + 1.0, 28, 34, 0.1)
    cam.handheld(1.2)
    sfx(t0 + 0.9, "pop")
    sfx(t0 + 1.0, "snort")


@beat(38, 46, n=2, focus=(0, 3.4, 5), d=10, lens=28, desc="He's still paying off the loan: Dad under a huge loan paper")
def s10(t0, t1):
    office_set()
    D = dadc(t0, t1, "worried")
    D.pose(t0, loc=(0, 3.4, 0), rot=0)
    D.act(t0 + 0.3, "slump", expr="cry")
    ln = plane("loan", 6.4, 4.3, (0, 1.0, 7.4), img_mat("loan", os.path.join(TEX, "loan.png"), 0.5), (90, 0, 0))
    ln.scale = (0.01,) * 3
    ln.keyframe_insert("scale", frame=F(t0 + 0.9))
    ln.scale = (1.1, 1.1, 1.1)
    ln.keyframe_insert("scale", frame=F(t0 + 1.15))
    ln.scale = (1, 1, 1)
    ln.keyframe_insert("scale", frame=F(t0 + 1.5))
    for i in range(12):
        b = bill(f"b{i}", (random.uniform(-5, 5), random.uniform(0, 3), 14), rot=(random.uniform(0, 60), 0, random.uniform(0, 180)))
        b.keyframe_insert("location", frame=F(t0 + 2.0 + i * 0.08))
        b.location[2] = 0.2
        b.keyframe_insert("location", frame=F(t0 + 3.3 + i * 0.08))
    cam = Cam()
    cam.push(t0, t1, (0, 3.4, 5.5), 15, 9, yaw=10, pitch=4, lens=26, yaw1=-8, lens1=30)
    cam.handheld(1.0)
    sfx(t0 + 0.95, "sting")
    sfx(t0 + 2.2, "chaching")


@beat(46, 52, n=2, focus=(6, 8, 4.6), d=12, lens=26, desc="Teacher checks the class, scanning kids")
def s11(t0, t1):
    R, ks = class_scene(t0, t1, kids=7, board="chalk_joke.png")
    T = teacher(t0, t1, "angry")
    T.pose(t0, loc=(5, 13, 0), rot=0)
    T.walk(t0, t1, (5, 13, 0), (7.5, 4.5, 0), rate=2.3)
    for k in ks:
        k.face(t0, "worried")
    cam = Cam()
    cam.key(t0, (4, -4, 7.5), (6, 10, 5.0), lens=22, focus=(6, 10, 5), fstop=4)
    cam.key(t1, (8.5, -2, 6.0), (7.5, 8, 4.6), lens=28, focus=(7.5, 6, 4.6), fstop=3.5, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.2, "footsteps")


@S(12, 52, 55, "Teacher tickles Leo, he fights the laugh")
def s12(t0, t1):
    R, ks = class_scene(t0, t1, kids=4, skip=(E_DESK, L_DESK))
    L = leo(t0, t1, "worried")
    W.sit(L, t0, L_DESK)
    T = teacher(t0, t1, "angry")
    T.pose(t0, loc=(L_SEAT[0] - 1.0, L_SEAT[1] - 2.0, 0), rot=180)
    T.act(t0 + 0.2, "reach")
    for i in range(6):
        L.pose(t0 + 0.3 + i * 0.22, head=(0, 5, 6 * (-1) ** i), torso=(0, 0, 3 * (-1) ** i))
    L.face(t0 + 0.3, eyes="closed", mouth="grimace_wide")
    cam = Cam()
    cam.push(t0, t1, (L_SEAT[0], L_SEAT[1], L_SEAT[2] + 4.4), 8, 5.8, yaw=164, pitch=3, lens=28, yaw1=196, lens1=34)
    cam.crash(t0 + 0.3, 28, 36, 0.1)
    cam.handheld(1.6)
    sfx(t0 + 0.3, "squeak")
    sfx(t0 + 1.2, "squeak")
    sfx(t0 + 2.3, "squeak")


@S(13, 55, 59, "Babies in cribs cry in sync")
def s13(t0, t1):
    nursery_set()
    for i, x in enumerate((-7, 0, 7)):
        b = baby(i, t0, t1, "cry")
        b.root.scale = (0.8,) * 3
        b.pose(t0, loc=(x, 7, 2.2), rot=0)
        b.talk(t0, t1, open_m="scream", wide_m="ah", rest="ah", syll=0.2)
        b.panic(t0, t1, 6)
    cam = Cam()
    cam.push(t0, t1, (0, 7, 4.2), 14, 10, yaw=-10, pitch=2, lens=26, yaw1=8, lens1=26)
    cam.handheld(1.2)
    sfx(t0, "alarm", 0.5)
    sfx(t0 + 0.4, "aww", 0.6)


@S(14, 59, 62, "Strict schedule: clock strikes 12, babies stop")
def s14(t0, t1):
    nursery_set()
    for i, x in enumerate((-7, 0, 7)):
        b = baby(i, t0, t1, "cry")
        b.pose(t0, loc=(x, 7, 2.2), rot=0)
        b.talk(t0, t0 + 1.2, open_m="scream", wide_m="ah", rest="ah", syll=0.2)
        b.face(t0 + 1.25, "neutral")
    cam = Cam()
    cam.key(t0, (0, -6, 9.0), (0, 11, 9.6), lens=30, focus=(0, 11.6, 9.6), fstop=3)
    cam.key(t1, (0, 2, 9.8), (0, 11, 9.8), lens=40, focus=(0, 11.6, 9.8), fstop=3, ease="EASE_IN")
    cam.crash(t0 + 0.5, 30, 38, 0.12)
    cam.handheld(0.8)
    sfx(t0 + 0.2, "ding")
    sfx(t0 + 1.3, "crickets")


# ================================================================== PART 3 : Tootie (62 - 110)
@S(15, 62, 66, "Tootie intro: smuggler walks in from the shadows, backpack")
def s15(t0, t1):
    town_scene()
    T = tootie(t0, t1, "smug")
    T.walk(t0, t1, (-8, -34, 0), (-0.5, -32, 0), rate=2.2)
    T.pose(t0, rot=-60)
    T.pose(t0 + 1.4, rot=0)
    cam = Cam()
    cam.key(t0, (-1, -42, 1.2), (-6, -34, 4.4), lens=20, focus=(-6, -34, 4.4), fstop=3)
    cam.key(t1, (1.5, -39, 4.6), (-0.5, -32, 4.6), lens=30, focus=(-0.5, -32, 4.6), fstop=3, ease="EASE_OUT")
    cam.handheld(1.0)
    sfx(t0, "whoosh", 0.6)
    sfx(t0 + 0.6, "footsteps")


@S(16, 66, 69, "'Smuggler' - Tootie looks sideways, sus, coat-flash")
def s16(t0, t1):
    town_scene()
    T = tootie(t0, t1, "sus")
    T.pose(t0, loc=(0, -32, 0), rot=15)
    look(T, t0 + 0.2, -50, 0)
    look(T, t0 + 1.0, 50, 0)
    T.act(t0 + 1.2, "think", expr="smug")
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.7), 10, 6.2, yaw=-20, pitch=3, lens=28, yaw1=20, lens1=36)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "sting")
    sfx(t0 + 1.9, "rizz", 0.6)


@beat(69, 76, n=2, focus=(0, 10.2, 5.5), d=11, lens=28, desc="Great-grandpa, the last clown: old clown portrait")
def s17(t0, t1):
    room("#d7c2a0", "#6a4a32", key=5200)
    box("frame", (9, 0.5, 11), (0, 11.4, 7.5), M("#c9a14a", 0.35, metal=0.6), 0.2)
    box("frame_in", (7.6, 0.4, 9.6), (0, 11.1, 7.5), M("#e8d9b0", 0.9), 0.1)
    C = clown(1, t0, t1, "smile")
    C.pose(t0, loc=(0, 10.2, 3.0), rot=0, hipz=0)
    C.act(t0 + 0.2, "idle", expr="happy")
    box("grandpa_beard", (1.2, 0.3, 0.8), (0, -0.55, -0.35), M("#f4f4f4", 0.9), 0.15) if False else None
    cam = Cam()
    cam.push(t0, t1, (0, 10.2, 5.8), 14, 9, yaw=0, pitch=2, lens=28, yaw1=0, lens1=32)
    cam.handheld(0.8)
    sfx(t0 + 0.3, "quack")
    sfx(t0 + 1.4, "aww", 0.7)


@S(18, 76, 82, "Tootie opens his backpack: tiny notes fly out")
def s18(t0, t1):
    town_scene()
    T = tootie(t0, t1, "smug")
    T.pose(t0, loc=(0, -32, 0), rot=180)
    T.act(t0 + 0.2, "reach", expr="smug")
    T.pose(t0 + 0.6, head=(-50, 0, 0))
    for i in range(10):
        n = note_card(f"fly{i}", (0, -31.0, 3.8), "note_one.png", 0.6, rot=(random.uniform(0, 80), random.uniform(0, 80), random.uniform(0, 180)))
        n.keyframe_insert("location", frame=F(t0 + 1.0 + i * 0.08))
        n.location = (random.uniform(-5, 5), random.uniform(-34, -28), random.uniform(4.5, 8))
        n.keyframe_insert("location", frame=F(t0 + 2.4 + i * 0.08))
        for ax in range(3):
            noise(n, "rotation_euler", ax, 2.0, 6)
        sets.set_obj_visible(n, t0 + 0.9 + i * 0.08, False)
        sets.set_obj_visible(n, t0 + 1.0 + i * 0.08, True)
    cam = Cam()
    cam.push(t0, t1, (0, -31, 4.5), 11, 7.5, yaw=155, pitch=10, lens=26, yaw1=190, lens1=30)
    cam.handheld(1.2)
    sfx(t0 + 0.9, "paper")
    sfx(t0 + 1.2, "paper", 0.7)
    sfx(t0 + 1.8, "sparkle", 0.6)


@S(19, 82, 86, "Extreme close-up of a tiny joke note")
def s19(t0, t1):
    world((0.9, 0.9, 0.85), 0.7)
    box("desk", (30, 30, 0.4), (0, 0, -0.2), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0)
    n = plane("note", 3.0, 2.2, (0, 0, 0.1), img_mat("note_rock", os.path.join(TEX, "note_rock.png"), 0.6), (0, 0, 8))
    n.keyframe_insert("rotation_euler", frame=F(t0))
    n.rotation_euler[2] = math.radians(-4)
    n.keyframe_insert("rotation_euler", frame=F(t1))
    light("l1", "AREA", (0, -3, 8), 1200, (1, 0.97, 0.9), 6, target=(0, 0, 0))
    cam = Cam()
    cam.key(t0, (-1.5, -2.8, 3.4), (0, 0, 0), lens=30, focus=(0, 0, 0), fstop=1.8)
    cam.key(t1, (0.8, -1.4, 3.6), (0, 0, 0), lens=34, focus=(0, 0, 0), fstop=1.8, ease="EASE_OUT")
    cam.handheld(0.8)
    sfx(t0, "paper")


@S(20, 86, 91, "One note costs a dollar: Eddie hands a bill")
def s20(t0, t1):
    town_scene()
    E = eddie(t0, t1, "happy")
    E.pose(t0, loc=(-2.4, -32, 0), rot=-28)
    T = tootie(t0, t1, "smug")
    T.pose(t0, loc=(2.4, -32, 0), rot=28)
    T.act(t0 + 0.2, "reach")
    E.act(t0 + 0.5, "reach")
    b = bill("hand_bill", (-1.2, -33.5, 3.2), rot=(90, 0, 10), s=1.1)
    b.keyframe_insert("location", frame=F(t0 + 0.7))
    b.location = (1.2, -33.5, 3.4)
    b.keyframe_insert("location", frame=F(t0 + 1.2))
    sets.set_obj_visible(b, t0 + 0.6, False)
    sets.set_obj_visible(b, t0 + 0.7, True)
    cam = Cam()
    cam.push(t0, t1, (0, -33, 4.2), 12, 8.5, yaw=-5, pitch=4, lens=26, yaw1=10, lens1=30)
    cam.handheld(1.0)
    sfx(t0 + 1.2, "chaching")


@S(21, 91, 96, "Mother-in-law joke costs two: two bills, bigger sparkle")
def s21(t0, t1):
    town_scene()
    E = eddie(t0, t1, "wink")
    E.pose(t0, loc=(-2.4, -32, 0), rot=-28)
    T = tootie(t0, t1, "grin")
    T.pose(t0, loc=(2.4, -32, 0), rot=28)
    for k, dy in enumerate((0, 0.25)):
        b = bill(f"hb{k}", (-1.2, -33.5, 3.2 + dy), rot=(90, 0, 10 - 8 * k), s=1.1)
        b.keyframe_insert("location", frame=F(t0 + 0.5))
        b.location = (1.2, -33.5, 3.4 + dy)
        b.keyframe_insert("location", frame=F(t0 + 1.1))
        sets.set_obj_visible(b, t0 + 0.4, False)
        sets.set_obj_visible(b, t0 + 0.5, True)
    n = note_card("mil", (1.6, -33.8, 5.6), "note_mil.png", 1.6, rot=(90, 0, 0))
    n.scale = (0.01,) * 3
    n.keyframe_insert("scale", frame=F(t0 + 1.2))
    n.scale = (1, 1, 1)
    n.keyframe_insert("scale", frame=F(t0 + 1.45))
    cam = Cam()
    cam.push(t0, t1, (0, -33, 4.6), 13, 8.0, yaw=10, pitch=3, lens=26, yaw1=-6, lens1=30)
    cam.handheld(1.0)
    sfx(t0 + 0.6, "chaching")
    sfx(t0 + 0.95, "coin")
    sfx(t0 + 1.3, "sparkle")


@S(22, 96, 99, "Close-up of the note: ROCK AND ROLL")
def s22(t0, t1):
    world((0.9, 0.9, 0.85), 0.7)
    box("desk", (30, 30, 0.4), (0, 0, -0.2), wood("wood_t", "#7d4f32", "#b07a52", 2.0), 0)
    plane("note", 3.4, 2.4, (0, 0, 0.1), img_mat("note_rock", os.path.join(TEX, "note_rock.png"), 0.6), (0, 0, -6))
    light("l1", "AREA", (0, -3, 8), 1200, (1, 0.97, 0.9), 6, target=(0, 0, 0))
    cam = Cam()
    cam.key(t0, (0.4, -2.2, 3.2), (0, 0, 0), lens=34, focus=(0, 0, 0), fstop=1.8)
    cam.key(t1, (-0.2, -0.9, 3.8), (0, 0, 0), lens=36, focus=(0, 0, 0), fstop=1.8, ease="EASE_IN")
    cam.handheld(1.2)
    sfx(t0 + 0.1, "pop")
    sfx(t0 + 1.4, "rise", 0.5)


@S(23, 99, 102, "Eddie holds the laugh: cheeks puff, trembling")
def s23(t0, t1):
    town_scene()
    E = eddie(t0, t1, "grin")
    E.pose(t0, loc=(0, -32, 0), rot=0)
    E.face(t0, eyes="closed", mouth="grimace_wide")
    for i in range(8):
        s = (-1) ** i
        E.pose(t0 + i * 0.18, head=(2 * s, 4, 4 * s), torso=(0, 2, 2 * s))
    E.act(t0 + 0.1, "hands_face")
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.7), 9, 5.0, yaw=0, pitch=2, lens=30, yaw1=4, lens1=38)
    cam.handheld(2.2)
    sfx(t0 + 0.2, "rise", 0.7)
    sfx(t0 + 1.9, "pop")


@S(24, 102, 105, "Tootie whispers in Eddie's ear")
def s24(t0, t1):
    town_scene()
    T = tootie(t0, t1, "smug")
    T.pose(t0, loc=(2.0, -32, 0), rot=60)
    T.talk(t0, t1, open_m="talk", wide_m="talk", rest="flat", syll=0.16)
    E = eddie(t0, t1, "sus")
    E.pose(t0, loc=(-1.2, -32, 0), rot=-60)
    cam = Cam()
    cam.key(t0, (0.2, -42, 5.4), (0.4, -32, 4.8), lens=30, focus=(0.4, -32, 4.8), fstop=2.5)
    cam.key(t1, (0.5, -38.5, 5.0), (0.4, -32, 4.8), lens=34, focus=(0.4, -32, 4.8), fstop=2.5, ease="EASE_OUT")
    cam.handheld(1.0)
    sfx(t0, "whoosh", 0.5)


@S(25, 105, 110, "I choke into my pillow (night bedroom)")
def s25(t0, t1):
    bedroom_set()
    E = eddie(t0, t1, "joy")
    E.pose(t0, loc=(-4, 6.0, 1.7), rot=180 + 180, torso=(0, 70, 0))
    E.pose(t0, loc=(-4, 7.6, 2.2), rot=0, torso=(0, 85, 0), head=(0, 40, 0))
    for i in range(14):
        s = (-1) ** i
        E.pose(t0 + i * 0.16, torso=(0, 82 + 3 * s, 4 * s), head=(0, 40, 3 * s))
    E.pose(t0, armL=(120, 10), armR=(120, 10))
    laugh(E, t0, t1, belly=False, rate=6, amp=0.3)
    E.face(t0, expr="joy")
    cam = Cam()
    cam.push(t0, t1, (-4, 7.6, 3.4), 13, 9, yaw=-25, pitch=18, lens=26, yaw1=-8, lens1=28)
    cam.handheld(1.4)
    sfx(t0 + 0.2, "snort")
    sfx(t0 + 0.5, "kids_laugh", 0.5)
    sfx(t0 + 1.5, "crickets", 0.6)


# ================================================================== PART 4 : something is weird (110 - 138)
@S(26, 110, 113, "But something's weird: Eddie, suspicious push-in")
def s26(t0, t1):
    town_scene()
    E = eddie(t0, t1, "sus")
    E.pose(t0, loc=(0, -32, 0), rot=0)
    look(E, t0 + 0.3, 20, 10)
    look(E, t0 + 1.4, -25, -6)
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.7), 11, 5.5, yaw=-10, pitch=0, lens=30, yaw1=8, lens1=40)
    cam.handheld(1.1)
    sfx(t0, "rise", 0.9)
    sfx(t0 + 0.1, "sting")


@beat(113, 117, n=2, focus=(2, -30, 3), d=30, lens=22, desc="Every year the town sinks: wide of the town, water creeping")
def s27(t0, t1):
    town_scene()
    water(-0.6, 1.0, t0, t1 + 8, ease="LINEAR")
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(0, -34, 0), rot=180)
    cam = Cam()
    cam.key(t0, (-14, -46, 11), (2, -30, 3), lens=22, focus=(2, -30, 3), fstop=8)
    cam.key(t1, (-6, -44, 6), (2, -30, 2), lens=22, focus=(2, -30, 2), fstop=8, ease="EASE_OUT")
    cam.handheld(1.0)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 1.0, "rise", 0.5)


@beat(117, 124, n=2, focus=(0, -14, 4.5), d=22, lens=24, desc="Houses lower into the ground: ruler marks, water lap")
def s28(t0, t1):
    town_scene()
    house_front((0, -14, 0))
    water(-1.2, 1.8, t0, t1)
    for k in range(0, 9):
        box(f"mark{k}", (0.5, 0.2, 0.1), (-9.5, -17.2, 1.0 + k * 1.2), M("#ffffff", 0.5), 0.02)
    cam = Cam()
    cam.key(t0, (-12, -36, 3.4), (0, -14, 4.6), lens=24, focus=(0, -14, 4.6), fstop=6)
    cam.key(t1, (8, -33, 1.6), (0, -14, 3.8), lens=26, focus=(0, -14, 3.8), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "rise", 0.5)
    sfx(t0 + 1.5, "thud", 0.7)


@S(29, 124, 128, "First the basements vanished: basement windows go under")
def s29(t0, t1):
    town_scene()
    house_front((0, -14, 0))
    water(0.2, 2.2, t0, t1, ease="EASE_IN")
    cam = Cam()
    cam.key(t0, (-5, -26, 1.8), (-4.6, -17, 1.6), lens=30, focus=(-4.6, -17, 1.4), fstop=3)
    cam.key(t1, (-4, -23, 1.4), (-4.6, -17, 1.6), lens=34, focus=(-4.6, -17, 1.4), fstop=3, ease="EASE_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.3, "splat", 0.6)
    sfx(t0 + 1.4, "thud", 0.7)


@S(30, 128, 132, "Then the first floors: door and windows go under")
def s30(t0, t1):
    town_scene()
    house_front((0, -14, 0))
    water(2.2, 6.4, t0, t1, ease="EASE_IN_OUT")
    cam = Cam()
    cam.key(t0, (0, -34, 4.2), (0, -14, 4.6), lens=26, focus=(0, -14, 4.6), fstop=5)
    cam.key(t1, (0, -29, 6.2), (0, -14, 5.6), lens=24, focus=(0, -14, 5.6), fstop=5, ease="EASE_OUT")
    cam.handheld(1.2)
    sfx(t0 + 0.2, "boom", 0.5)
    sfx(t0 + 1.8, "rise", 0.5)


@beat(132, 138, n=2, focus=(0, -29.5, 6), d=10, lens=28, desc="Mayor Pop: 'totally normal', thumbs up, water at the podium")
def s31(t0, t1):
    town_scene()
    water(0.5, 1.5, t0, t1, ease="LINEAR")
    box("podium", (5, 3, 4.2), (0, -30, 2.1), M("#6e4229", 0.6), 0.1)
    M_ = mayor(t0, t1, "smile")
    M_.pose(t0, loc=(0, -29.2, 3.8), rot=0)
    M_.act(t0 + 0.3, "cheer", expr="smile")
    M_.pose(t0 + 1.0, armL=(10, 6), armR=(100, -20))
    M_.talk(t0, t1, open_m="talk", wide_m="talk_wide", rest="smile")
    cam = Cam()
    cam.push(t0, t1, (0, -29.5, 8.6), 16, 9.0, yaw=-12, pitch=-2, lens=26, yaw1=12, lens1=30)
    cam.handheld(1.0)
    sfx(t0 + 1.3, "cheer", 0.3)
    sfx(t0 + 2.6, "ding")


# ================================================================== PART 5 : Tootie caught (138 - 187)
@S(32, 138, 143, "Tootie gets caught: cops grab him, notes fly")
def s32(t0, t1):
    town_scene()
    T = tootie(t0, t1, "scream")
    T.pose(t0, loc=(0, -32, 0), rot=0)
    T.run(t0, t0 + 0.8, (6, -30, 0), (0, -32, 0))
    T.act(t0 + 0.9, "hands_head", expr="scream")
    C1 = cop(t0, t1, "angry", name="C1")
    C1.pose(t0, loc=(-3.0, -33, 0), rot=-40)
    C1.act(t0 + 0.7, "reach", expr="shout")
    C2 = cop(t0, t1, "angry", name="C2")
    C2.pose(t0, loc=(3.0, -33, 0), rot=40)
    C2.act(t0 + 0.7, "reach", expr="shout")
    for i in range(12):
        n = note_card(f"fl{i}", (0, -32.2, 3.8), "note_one.png", 0.6)
        n.keyframe_insert("location", frame=F(t0 + 0.85))
        n.location = (random.uniform(-6, 6), random.uniform(-36, -29), random.uniform(3, 9))
        n.keyframe_insert("location", frame=F(t0 + 2.4))
        for ax in range(3):
            noise(n, "rotation_euler", ax, 2.5, 5)
        sets.set_obj_visible(n, t0 + 0.8, False)
        sets.set_obj_visible(n, t0 + 0.85, True)
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.6), 14, 9, yaw=-30, pitch=6, lens=24, yaw1=20, lens1=28)
    cam.crash(t0 + 0.85, 24, 34, 0.1)
    cam.handheld(2.0)
    sfx(t0, "whoosh")
    sfx(t0 + 0.85, "slap")
    sfx(t0 + 0.9, "alarm", 0.6)


@beat(143, 152, n=3, focus=(0, -30, 3.5), d=18, lens=24, desc="They put him in the middle of the square: crowd, cops, Tootie in the center")
def s33(t0, t1):
    town_scene()
    T = tootie(t0, t1, "worried")
    T.pose(t0, loc=(0, -30, 0), rot=0)
    T.act(t0 + 0.4, "slump", expr="cry")
    for i, (x, y) in enumerate(((-4, -33), (4, -33), (-6, -27), (6, -27))):
        c = cop(t0, t1, "angry", name=f"CC{i}")
        c.pose(t0, loc=(x, y, 0), rot=facing((x, y, 0), (0, -30, 0)) )
    ks = street_pair(t0, t1, 10, 8)
    for k in ks:
        r = k.root.location
        k.pose(t0, loc=(r[0] * 1.5, r[1] - 6, 0))
    cam = Cam()
    cam.key(t0, (-20, -58, 9), (0, -30, 3.5), lens=22, focus=(0, -30, 3.5), fstop=8)
    cam.key(t1, (6, -46, 14), (0, -30, 4.0), lens=22, focus=(0, -30, 4.0), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "crowd", 0.8)
    sfx(t0 + 1.4, "stomp", 0.6)


@S(34, 152, 157, "Burn all his notes: fire pile, Tootie's despair")
def s34(t0, t1):
    town_scene()
    fire_pile((0, -33, 0), t0)
    T = tootie(t0, t1, "cry")
    T.pose(t0, loc=(0, -29, 0), rot=0)
    T.act(t0 + 0.3, "hands_head", expr="scream")
    cam = Cam()
    cam.push(t0, t1, (0, -31, 3.2), 14, 8.5, yaw=-20, pitch=-4, lens=26, yaw1=5, lens1=30)
    cam.handheld(1.4)
    sfx(t0 + 0.1, "blast", 0.8)
    sfx(t0 + 0.3, "boom", 0.5)
    sfx(t0 + 1.0, "faaah", 0.7)


@S(35, 157, 163, "And right then: town trembles, everyone freezes")
def s35(t0, t1):
    town_scene()
    water(0.0, 0.8, t0, t1, ease="EASE_IN")
    ks = street_pair(t0, t1, 8, 3)
    for k in ks:
        k.face(t0 + 0.5, "gasp")
        k.pose(t0 + 0.5, armL=(40, 40), armR=(40, 40))
    T = tootie(t0, t1, "gasp")
    T.pose(t0, loc=(0, -30, 0), rot=0)
    cam = Cam()
    cam.push(t0, t1, (0, -30, 4.5), 22, 12, yaw=0, pitch=4, lens=24, yaw1=-6, lens1=26)
    cam.handheld(2.0)
    sfx(t0 + 0.1, "rise", 0.9)


@S(36, 163, 167, "Sank another three feet: camera dumps down, hard shake")
def s36(t0, t1):
    town_scene()
    water(0.8, 3.6, t0, t0 + 1.4, ease="EASE_OUT")
    ks = street_pair(t0, t1, 8, 3)
    for k in ks:
        k.act(t0 + 0.2, "recoil", expr="scream")
    cam = Cam()
    cam.key(t0, (0, -48, 6.0), (0, -30, 5.0), lens=24, focus=(0, -30, 5.0), fstop=8)
    cam.key(t0 + 0.3, (0, -48, 3.4), (0, -30, 4.0), lens=24, focus=(0, -30, 5.0), fstop=8, ease="EASE_IN")
    cam.key(t1, (0, -47, 3.0), (0, -30, 4.2), lens=22, focus=(0, -30, 5.0), fstop=8, ease="EASE_OUT")
    cam.crash(t0 + 0.3, 24, 18, 0.12)
    cam.handheld(3.0)
    sfx(t0 + 0.2, "boom")
    sfx(t0 + 0.3, "blast", 0.6)
    sfx(t0 + 0.6, "splat")


@S(37, 167, 172, "Water pours through the windows (classroom)")
def s37(t0, t1):
    R, ks = class_scene(t0, t1, kids=8)
    for k in ks:
        k.act(t0 + 1.0, "recoil", expr="scream")
    wt = box("flood", (30, 24, 8), (5, 1, -4), mat("floodw", (0.1, 0.42, 0.62), 0.06, alpha=0.78, spec=1.0), 0)
    wt.keyframe_insert("location", index=2, frame=F(t0 + 0.2))
    wt.location[2] = 0.5
    wt.keyframe_insert("location", index=2, frame=F(t1))
    set_interp(wt, "location", F(t0 + 0.2), "BEZIER", "EASE_OUT")
    cam = Cam()
    cam.key(t0, (4, 0, 7.5), (5, 12, 4.5), lens=20, focus=(5, 12, 4.5), fstop=5)
    cam.key(t1, (5, 2, 4.5), (5, 12, 3.8), lens=20, focus=(5, 12, 3.8), fstop=5, ease="EASE_OUT")
    cam.handheld(2.4)
    sfx(t0 + 0.2, "splat")
    sfx(t0 + 0.3, "window")
    sfx(t0 + 0.7, "rise", 0.6)


@S(38, 172, 174, "People screamed: panic crowd")
def s38(t0, t1):
    town_scene()
    water(2.5, 3.0, t0, t1, ease="LINEAR")
    scream_crowd(t0, t1, 12, area=((-10, 10), (-36, -24)), seed=4, z=2.0)
    cam = Cam()
    cam.push(t0, t1, (0, -30, 6.5), 14, 9.5, yaw=0, pitch=2, lens=24, yaw1=-14, lens1=24)
    cam.handheld(2.6)
    sfx(t0 + 0.1, "gasp")
    sfx(t0 + 0.2, "crowd", 0.9)


@S(39, 174, 179, "Eddie looks at Tootie")
def s39(t0, t1):
    town_scene()
    water(2.5, 2.9, t0, t1, ease="LINEAR")
    E = eddie(t0, t1, "terror")
    E.pose(t0, loc=(-2.5, -30, 2.4), rot=-25)
    look(E, t0 + 0.8, 40, 0)
    E.face(t0 + 0.9, "worried")
    cam = Cam()
    cam.push(t0, t1, (-2.5, -30, 7.0), 8, 5.4, yaw=18, pitch=2, lens=30, yaw1=0, lens1=34)
    cam.handheld(1.2)
    sfx(t0 + 0.8, "sting")


@S(40, 179, 184, "Tootie looks at Eddie")
def s40(t0, t1):
    town_scene()
    water(2.5, 2.9, t0, t1, ease="LINEAR")
    T = tootie(t0, t1, "terror")
    T.pose(t0, loc=(2.5, -30, 2.4), rot=25)
    look(T, t0 + 0.8, -40, 0)
    T.face(t0 + 0.9, "worried")
    cam = Cam()
    cam.push(t0, t1, (2.5, -30, 7.0), 8, 5.4, yaw=-18, pitch=2, lens=30, yaw1=0, lens1=34)
    cam.handheld(1.2)


@S(41, 184, 187, "We got it: both gasp, light bulb, crash zoom")
def s41(t0, t1):
    town_scene()
    water(2.6, 2.8, t0, t1, ease="LINEAR")
    E = eddie(t0, t1, "gasp")
    E.pose(t0, loc=(-2.4, -30, 2.4), rot=-20)
    T = tootie(t0, t1, "gasp")
    T.pose(t0, loc=(2.4, -30, 2.4), rot=20)
    E.act(t0 + 0.4, "shock", expr="gasp")
    T.act(t0 + 0.4, "shock", expr="gasp")
    bulb = sphere("bulb", 0.5, (0, -30.3, 12.4), mat("bulb_y", (1, 0.9, 0.3), 0.3, emit=(1, 0.85, 0.2), estr=14), seg=16)
    bulb.scale = (0.01,) * 3
    bulb.keyframe_insert("scale", frame=F(t0 + 0.4))
    bulb.scale = (1.2, 1.2, 1.2)
    bulb.keyframe_insert("scale", frame=F(t0 + 0.6))
    cam = Cam()
    cam.push(t0, t1, (0, -30, 9.0), 14, 8.0, yaw=0, pitch=0, lens=26, yaw1=0, lens1=30)
    cam.crash(t0 + 0.4, 26, 38, 0.1)
    cam.handheld(1.3)
    sfx(t0 + 0.4, "ding")
    sfx(t0 + 0.45, "sparkle")
    sfx(t0 + 0.4, "correct", 0.7)


# ================================================================== PART 6 : the secret (187 - 222)
@beat(187, 194, n=2, focus=(0, 30, 5), d=24, lens=22, desc="A hundred years ago, swamp: murky water, reeds, tiny village")
def s42(t0, t1):
    swamp_set()
    for i in range(5):
        house_front((-18 + i * 9, 38 + (i % 2) * 6, 0.2), w=7, h=6, wall=["#e2725b", "#f2c14e", "#6fb3e0", "#9b8fd6", "#8fd18c"][i], name=f"sh{i}")
    cam = Cam()
    cam.key(t0, (-20, -14, 3.0), (0, 30, 4.0), lens=22, focus=(0, 30, 4), fstop=6)
    cam.key(t1, (12, -10, 5.0), (0, 30, 4.5), lens=24, focus=(0, 30, 4.5), fstop=6, ease="EASE_IN_OUT")
    cam.handheld(0.9)
    sfx(t0, "wind", 0.5)
    sfx(t0 + 1.2, "pigeon", 0.4)


@S(43, 194, 199, "Built on a swamp: bubbles, frog-like plops, houses wobbling")
def s43(t0, t1):
    swamp_set()
    h = house_front((0, 22, 0.2), w=9, h=7)
    cam = Cam()
    cam.key(t0, (0, 6, 0.8), (0, 22, 3.0), lens=28, focus=(0, 22, 3), fstop=3)
    cam.key(t1, (3, 4, 1.8), (0, 22, 3.8), lens=24, focus=(0, 22, 3.8), fstop=3, ease="EASE_OUT")
    cam.handheld(1.4)
    sfx(t0 + 0.3, "pop")
    sfx(t0 + 1.2, "pop", 0.7)
    sfx(t0 + 2.0, "splat", 0.5)


@beat(199, 204, n=2, focus=(0, 16, 5), d=16, lens=22, desc="Only laughter kept it afloat: laughing crowd lifts houses, HA letters")
def s44(t0, t1):
    swamp_set()
    house_front((0, 26, 0.2), w=9, h=7, name="a")
    for i in range(7):
        k = townie(i + 1, t0, t1, "joy")
        k.pose(t0, loc=(-9 + i * 3, 12 + (i % 3) * 2, 0), rot=random.uniform(-25, 25))
        laugh(k, t0, t1, flail=False, rate=5)
    for i in range(10):
        t = text(f"ha{i}", random.choice(["HA!", "HA HA", "HO!", "HEE!"]), (random.uniform(-10, 10), 9.0, 2.0), 1.6,
                 mat("ha_y", (1, 0.85, 0.2), 0.4, emit=(1, 0.8, 0.2), estr=2.0), rot=(90, 0, 0))
        t.keyframe_insert("location", frame=F(t0 + 0.1 * i))
        t.location = (t.location[0] + random.uniform(-2, 2), 9.0, 11 + random.uniform(0, 5))
        t.keyframe_insert("location", frame=F(t0 + 1.8 + 0.1 * i))
    cam = Cam()
    cam.key(t0, (0, -4, 2.5), (0, 20, 5), lens=22, focus=(0, 14, 4), fstop=5)
    cam.key(t1, (0, -2, 9.5), (0, 20, 8), lens=22, focus=(0, 14, 6), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0, "kids_laugh", 0.9)
    sfx(t0 + 1.0, "rise", 0.7)
    sfx(t0 + 2.4, "sparkle")


@beat(204, 209, n=2, focus=(0, -30, 2.5), d=9, lens=26, desc="Water reached our knees: low camera at waterline, Eddie wading")
def s45(t0, t1):
    town_scene()
    water(1.5, 2.2, t0, t1, ease="LINEAR")
    E = eddie(t0, t1, "worried")
    E.pose(t0, loc=(-2.4, -30, 0.7), rot=-15)
    T = tootie(t0, t1, "worried")
    T.pose(t0, loc=(2.4, -30, 0.7), rot=15)
    cam = Cam()
    cam.key(t0, (0, -36, 2.6), (0, -30, 2.2), lens=26, focus=(0, -30, 2.0), fstop=3)
    cam.key(t1, (0, -35, 1.9), (0, -30, 2.4), lens=24, focus=(0, -30, 2.0), fstop=3, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    sfx(t0 + 0.2, "splat", 0.5)
    sfx(t0 + 1.4, "splat", 0.4)


@beat(209, 216, n=2, focus=(0, -30, 5), d=10, lens=26, desc="Tootie climbs a barrel, hero low angle")
def s46(t0, t1):
    town_scene()
    water(2.0, 2.6, t0, t1, ease="LINEAR")
    barrel((0, -30, 0))
    T = tootie(t0, t1, "determined")
    T.pose(t0, loc=(3.0, -30, 1.0), rot=-45)
    T.jump(t0 + 0.6, 2.2, 0.6, loc=(3.0, -30, 1.0))
    T.pose(t0 + 1.3, loc=(0, -30, 3.0), rot=0)
    T.act(t0 + 1.5, "fists", expr="determined")
    cam = Cam()
    cam.key(t0, (-7, -40, 2.0), (0, -30, 3.5), lens=24, focus=(0, -30, 3.5), fstop=3.5)
    cam.key(t1, (0, -38, 3.0), (0, -30, 6.8), lens=26, focus=(0, -30, 6.8), fstop=3.5, ease="EASE_IN_OUT")
    cam.handheld(1.2)
    sfx(t0 + 1.3, "thud")
    sfx(t0 + 1.7, "sting")


@S(47, 216, 219, "Tootie yells the joke: close-up")
def s47(t0, t1):
    town_scene()
    barrel((0, -30, 0))
    T = tootie(t0, t1, "shout")
    T.pose(t0, loc=(0, -30, 3.0), rot=0)
    T.act(t0, "fists", expr="shout")
    T.talk(t0, t1, V.span(t0, t1), open_m="talk_wide", wide_m="scream", rest="grimace")
    cam = Cam()
    cam.push(t0, t1, (0, -30, 7.6), 9, 6.0, yaw=-10, pitch=-8, lens=28, yaw1=8, lens1=34)
    cam.handheld(1.4)
    sfx(t0, "whoosh", 0.5)


@S(48, 219, 223, "Principal Fartan walks into an elevator (insert)")
def s48(t0, t1):
    room("#c9d3dc", "#6a6e78", key=6000)
    el = plane("elev", 11, 13.75, (0, 11.4, 6.9), img_mat("elevator", os.path.join(TEX, "elevator.png"), 0.4), (90, 0, 0))
    P = fartan(t0, t1, "happy")
    P.pose(t0, loc=(-5.5, 3, 0), rot=-60)
    P.walk(t0, t0 + 1.2, (-5.5, 3, 0), (0, 8.0, 0), rate=2.4)
    P.pose(t0 + 1.2, rot=0)
    P.act(t0 + 1.4, "shrug", expr="happy")
    cam = Cam()
    cam.push(t0, t1, (0, 8.0, 4.6), 17, 12, yaw=0, pitch=2, lens=26, yaw1=-8, lens1=26)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "ding")
    sfx(t0 + 1.9, "fart")
    sfx(t0 + 2.0, "rimshot", 0.5)


# ================================================================== PART 7 : laughter wins (223 - 284)
@S(49, 223, 227, "I couldn't hold it: cheeks puff, eyes squeezed, sweat")
def s49(t0, t1):
    town_scene()
    water(2.0, 2.4, t0, t1, ease="LINEAR")
    E = eddie(t0, t1, "grin")
    E.pose(t0, loc=(0, -30, 0.5), rot=0)
    E.face(t0, eyes="closed", mouth="grimace_wide")
    for i in range(10):
        s = (-1) ** i
        E.pose(t0 + i * 0.12, head=(3 * s, 6, 4 * s), torso=(0, 4, 3 * s))
    E.act(t0 + 0.2, "hands_face")
    cam = Cam()
    cam.push(t0, t1, (0, -30, 5.2), 10, 4.2, yaw=0, pitch=2, lens=30, yaw1=0, lens1=42)
    cam.handheld(2.4)
    sfx(t0, "rise", 0.8)
    sfx(t0 + 1.2, "snort")


@S(50, 227, 231, "I burst out laughing: explosion pose, confetti flash")
def s50(t0, t1):
    town_scene()
    water(2.0, 2.4, t0, t1, ease="LINEAR")
    E = eddie(t0, t1, "joy")
    E.pose(t0, loc=(0, -30, 0.5), rot=0)
    E.act(t0 + 0.05, "cheer", expr="joy", strength=1.0)
    laugh(E, t0 + 0.1, t1, flail=True, rate=6)
    E.jump(t0 + 0.1, 1.2, 0.5, loc=(0, -30, 0.5))
    confetti("cf", (0, -31, 6), (4, 3, 4), t0 + 0.1, 1.6, 60, 2, 9)
    cam = Cam()
    cam.key(t0, (0, -36, 4.8), (0, -30, 4.8), lens=40, focus=(0, -30, 4.8), fstop=3)
    cam.key(t1, (0, -41, 5.8), (0, -30, 5.0), lens=22, focus=(0, -30, 5.0), fstop=3, ease="EASE_OUT")
    cam.crash(t0 + 0.05, 40, 22, 0.15)
    cam.handheld(2.0)
    sfx(t0 + 0.05, "boom")
    sfx(t0 + 0.1, "kids_laugh")
    sfx(t0 + 0.12, "confetti")


@beat(231, 238, n=2, focus=(0, -30, 4), d=12, lens=24, desc="The ground shook and rose a little: camera shake, water level drops")
def s51(t0, t1):
    town_scene()
    water(2.6, 0.6, t0, t1, ease="EASE_IN_OUT")
    E = eddie(t0, t1, "joy")
    E.pose(t0, loc=(-2.5, -30, 0.5), rot=-10)
    laugh(E, t0, t1, flail=True)
    T = tootie(t0, t1, "joy")
    T.pose(t0, loc=(2.5, -30, 3.0), rot=10)
    laugh(T, t0, t1, flail=False)
    barrel((2.5, -30, 0))
    cam = Cam()
    cam.key(t0, (-3, -38, 1.0), (0, -30, 3), lens=22, focus=(0, -30, 3), fstop=5)
    cam.key(t1, (4, -40, 5.0), (0, -30, 5.0), lens=22, focus=(0, -30, 5), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(2.4)
    sfx(t0, "rise")
    sfx(t0 + 0.2, "stomp", 0.8)
    sfx(t0 + 1.4, "kids_laugh")


@S(52, 238, 241, "Then Mom laughed")
def s52(t0, t1):
    town_scene()
    water(1.0, 0.6, t0, t1, ease="LINEAR")
    Mm = mom(t0, t1, "joy")
    Mm.pose(t0, loc=(0, -30, 0.5), rot=0)
    laugh(Mm, t0, t1, belly=True, amp=1.2)
    cam = Cam()
    cam.push(t0, t1, (0, -30, 4.7), 11, 6.5, yaw=-18, pitch=3, lens=28, yaw1=10, lens1=34)
    cam.handheld(1.8)
    sfx(t0 + 0.1, "kids_laugh")
    sfx(t0 + 0.2, "ding", 0.6)


@S(53, 241, 243, "Then Dad")
def s53(t0, t1):
    town_scene()
    water(1.0, 0.6, t0, t1, ease="LINEAR")
    D = dadc(t0, t1, "joy")
    D.pose(t0, loc=(0, -30, 0.5), rot=0)
    laugh(D, t0, t1, belly=True, amp=1.2)
    cam = Cam()
    cam.push(t0, t1, (0, -30, 4.7), 12, 7.0, yaw=14, pitch=3, lens=28, yaw1=-8, lens1=34)
    cam.handheld(1.8)
    sfx(t0 + 0.05, "kids_laugh")
    sfx(t0 + 0.1, "snort")


@S(54, 243, 246, "Then the police")
def s54(t0, t1):
    town_scene()
    water(1.0, 0.6, t0, t1, ease="LINEAR")
    for i, x in enumerate((-3, 3)):
        c = cop(t0, t1, "joy", name=f"P{i}")
        c.pose(t0, loc=(x, -30, 0.5), rot=-x * 5)
        laugh(c, t0, t1, belly=True, amp=1.3, rate=5 + i)
    cam = Cam()
    cam.push(t0, t1, (0, -30, 4.7), 15, 9.0, yaw=-10, pitch=3, lens=26, yaw1=10, lens1=30)
    cam.handheld(1.8)
    sfx(t0 + 0.05, "kids_laugh")
    sfx(t0 + 0.4, "quack", 0.7)
    sfx(t0 + 1.2, "slap", 0.6)


@beat(246, 251, n=2, focus=(0, -30, 3), d=26, lens=22, desc="Whole square laughs: big crowd wide, rising")
def s55(t0, t1):
    town_scene()
    water(0.8, -0.4, t0, t1, ease="EASE_IN_OUT")
    src = crowd_src("LC", t0, t1, [1, 2, 3, 4, 5, 6], mode="laugh", spread=3.5, seed=2)
    crowd(src, t0, t1, 18, ((-14, 14), (-40, -20)), z0=(0.5, 0.9), z1=(1.2, 2.6), delay=(0.0, 0.6), seed=3)
    cam = Cam()
    cam.key(t0, (-12, -52, 6), (0, -30, 3.0), lens=22, focus=(0, -30, 3), fstop=8)
    cam.key(t1, (14, -50, 10), (0, -30, 4.0), lens=22, focus=(0, -30, 4), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.6)
    sfx(t0, "crowd")
    sfx(t0 + 0.1, "kids_laugh")
    sfx(t0 + 1.0, "cheer", 0.6)


@S(56, 251, 255, "So hard the windows rattled: house windows shake, shards")
def s56(t0, t1):
    town_scene()
    house_front((0, -14, 0))
    for sx in (-1, 1):
        w_ = bpy.data.objects.get(f"hs_w{sx}")
        if w_:
            for i in range(14):
                w_.location[2] += 0.06 * (-1) ** i
                w_.keyframe_insert("location", index=2, frame=F(t0 + i * 0.1))
    Mg = mat("shard", (0.85, 0.92, 1.0), 0.05, alpha=0.4, spec=1.0)
    for i in range(8):
        sh = box(f"shard{i}", (0.5, 0.05, 0.4), (random.uniform(-6, 6), -17.5, 6.8), Mg, 0)
        spin(sh, t0 + 1.2, t0 + 2.4, -6.0, seed=i)
    scream_crowd(t0, t1, 6, area=((-6, 6), (-30, -24)), seed=9)
    cam = Cam()
    cam.key(t0, (0, -34, 4.4), (0, -14, 5.8), lens=24, focus=(0, -14, 5.8), fstop=5)
    cam.key(t1, (0, -28, 5.2), (0, -14, 6.4), lens=28, focus=(0, -14, 6.4), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(3.0)
    sfx(t0, "window")
    sfx(t0 + 0.5, "window", 0.7)
    sfx(t0 + 1.2, "kids_laugh")


@beat(255, 261, n=2, focus=(0, -30, 5), d=24, lens=22, desc="The town rose higher and higher: crane up, sun burst")
def s57(t0, t1):
    town_scene()
    water(0.6, -2.0, t0, t1, ease="EASE_IN_OUT")
    src = crowd_src("LC", t0, t1, [1, 2, 3, 4], mode="cheer", spread=3.5, seed=2)
    crowd(src, t0, t1, 10, ((-12, 12), (-40, -22)), z0=(0.5, 0.9), z1=(2.0, 3.4), delay=(0.0, 0.6), seed=5)
    cam = Cam()
    cam.key(t0, (0, -44, 2.4), (0, -30, 4.0), lens=22, focus=(0, -30, 4), fstop=8)
    cam.key(t1, (0, -52, 30), (0, -30, 5.0), lens=24, focus=(0, -30, 5), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.4)
    sfx(t0, "rise")
    sfx(t0 + 1.0, "cheer")
    sfx(t0 + 2.6, "sparkle")


@S(58, 261, 265, "The fines were canceled: cop tears the ticket, confetti")
def s58(t0, t1):
    town_scene()
    C = cop(t0, t1, "joy")
    C.pose(t0, loc=(0, -31, 0), rot=0)
    laugh(C, t0 + 0.6, t1, belly=False, amp=0.8)
    tk = plane("ticket", 2.0, 2.5, (0, -32.4, 4.0), img_mat("fine_ticket", os.path.join(TEX, "fine_ticket.png"), 0.6), (90, 0, 0))
    tk.keyframe_insert("location", frame=F(t0 + 0.5))
    tk.keyframe_insert("rotation_euler", frame=F(t0 + 0.5))
    tk.location = (random.uniform(-3, 3), -33, 1.0)
    tk.rotation_euler = (math.radians(200), math.radians(40), math.radians(120))
    tk.keyframe_insert("location", frame=F(t1))
    tk.keyframe_insert("rotation_euler", frame=F(t1))
    confetti("cf", (0, -32, 6), (5, 3, 4), t0 + 0.5, 1.6, 70, 4, 10)
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.4), 11, 7.0, yaw=-14, pitch=2, lens=26, yaw1=8, lens1=30)
    cam.handheld(1.3)
    sfx(t0 + 0.5, "paper")
    sfx(t0 + 0.55, "confetti")
    sfx(t0 + 0.6, "correct", 0.7)


@S(59, 265, 270, "The clowns were set free: jail door swings, clowns run out honking")
def s59(t0, t1):
    jail_set(open_t=t0 + 0.4)
    for i, (x, y) in enumerate(((0.4, 5.0), (1.8, 6.5), (3.0, 5.0))):
        c = clown(i, t0, t1, "joy")
        c.pose(t0, loc=(x, y, 0), rot=0)
        c.run(t0 + 0.6, t1, (x, y, 0), (-2.5 + i * 4.5, -12 - i * 2, 0))
        c.pose(t0 + 0.6, rot=-10 * (i - 1) + 0)
        c.panic(t0 + 0.7, t1, rate=6)
        c.face(t0 + 0.6, "joy")
    confetti("cf", (0, 2, 6), (4, 3, 4), t0 + 0.5, 1.6, 50, 6, 10)
    cam = Cam()
    cam.push(t0, t1, (0, 2, 4.8), 18, 12, yaw=0, pitch=5, lens=26, yaw1=10, lens1=26)
    cam.handheld(1.6)
    sfx(t0 + 0.3, "door")
    sfx(t0 + 0.5, "quack")
    sfx(t0 + 0.9, "quack", 0.7)
    sfx(t0 + 1.2, "cheer")
    sfx(t0 + 1.4, "confetti")


@beat(270, 276, n=2, focus=(0, -40, 6), d=22, lens=24, desc="Now every pole has a sign: pole row, dolly")
def s60(t0, t1):
    town_scene()
    for i in range(4):
        pole((-6 + (i % 2) * 12, -22 - i * 8, 0), rot=(-1) ** i * 15, name=f"pl{i}", sign="sign_drown.png", sign_z=6.0)
    cam = Cam()
    cam.key(t0, (-3, -14, 2.8), (2, -50, 6.5), lens=22, focus=(0, -40, 6), fstop=8)
    cam.key(t1, (4, -22, 5.4), (0, -50, 6.5), lens=24, focus=(0, -40, 6), fstop=8, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0, "whoosh")
    sfx(t0 + 1.2, "whoosh", 0.5)


@S(61, 276, 279, "Laugh or drown: sign close-up, crash zoom")
def s61(t0, t1):
    town_scene()
    water(-0.2, 1.0, t0, t1, ease="LINEAR")
    pole((0, -30, 0), sign="sign_drown.png", sign_z=6.4, name="fin")
    cam = Cam()
    cam.key(t0, (4, -42, 6.6), (0, -30, 6.4), lens=24, focus=(0, -30, 6.4), fstop=4)
    cam.key(t1, (0.6, -36, 6.4), (0, -30, 6.4), lens=24, focus=(0, -30, 6.4), fstop=4, ease="EASE_IN")
    cam.crash(t0 + 0.2, 24, 36, 0.12)
    cam.handheld(1.0)
    sfx(t0 + 0.2, "boom")
    sfx(t0 + 0.25, "sting")


# ================================================================== PART 8 : button (279 - end)
@S(62, 279, 284, "Only Mayor Pop never laughed: grim mayor, crowd laughing behind")
def s62(t0, t1):
    town_scene()
    M_ = mayor(t0, t1, "angry")
    M_.pose(t0, loc=(0, -31, 0), rot=0)
    M_.act(t0 + 0.2, "cross", expr="angry")
    src = crowd_src("LC", t0, t1, [1, 2, 3, 4], mode="laugh", spread=3.0, seed=7)
    crowd(src, t0, t1, 12, ((-14, 14), (-24, -14)), z0=(0.3, 0.8), z1=(0.4, 1.0), seed=3)
    cam = Cam()
    cam.push(t0, t1, (0, -31, 5.0), 11, 6.0, yaw=-10, pitch=1, lens=28, yaw1=6, lens1=34)
    cam.handheld(1.0)
    sfx(t0 + 0.1, "crowd", 0.6)
    sfx(t0 + 0.3, "sting")


@beat(284, 292, n=2, focus=(0, -24, 10), d=30, lens=26, desc="His house is the only one still underwater: mayor on the roof, water to the windows")
def s63(t0, t1):
    town_scene()
    house_front((0, -24, 0), w=16, h=12, wall="#d9d0c0", roof="#2a2a30", name="mh")
    water(7.6, 7.9, t0, t1, ease="LINEAR", size=60, y=-24, name="mwater")
    M_ = mayor(t0, t1, "cry")
    M_.pose(t0, loc=(0, -24, 13.4), rot=0)
    M_.act(t0 + 0.3, "slump", expr="cry")
    cam = Cam()
    cam.key(t0, (-16, -52, 10), (0, -24, 9), lens=24, focus=(0, -24, 9), fstop=8)
    cam.key(t1, (6, -46, 16), (0, -24, 12), lens=30, focus=(0, -24, 13.4), fstop=5, ease="EASE_IN_OUT")
    cam.handheld(1.0)
    sfx(t0 + 0.5, "faaaa", 0.9)
    sfx(t0 + 1.5, "splat", 0.4)


@beat(292, 298, n=2, focus=(0, -32, 4.7), d=8, lens=28, desc="Tootie smirks, still hasn't told: close")
def s64(t0, t1):
    town_scene()
    T = tootie(t0, t1, "smug")
    T.pose(t0, loc=(0, -32, 0), rot=0)
    T.act(t0 + 0.4, "cross", expr="smug")
    T.face(t0 + 2.0, "wink")
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.7), 10, 6.0, yaw=14, pitch=2, lens=28, yaw1=-10, lens1=34)
    cam.handheld(1.0)
    sfx(t0 + 0.3, "rizz", 0.7)
    sfx(t0 + 2.0, "ding", 0.7)


@beat(298, None, n=2, focus=(0, -32, 4.7), d=9, lens=28, desc="Eddie waits for the punchline, button")
def s65(t0, t1):
    town_scene()
    E = eddie(t0, t1, "sus")
    E.pose(t0, loc=(0, -32, 0), rot=0)
    E.act(t0 + 0.3, "shrug", expr="confused")
    cam = Cam()
    cam.push(t0, t1, (0, -32, 4.7), 12, 6.0, yaw=-8, pitch=2, lens=28, yaw1=6, lens1=34)
    cam.handheld(0.9)
    sfx(t0 + 0.4, "ding")
    sfx(t0 + 1.8, "crickets", 0.7)
    sfx(t0 + 2.6, "rimshot")
