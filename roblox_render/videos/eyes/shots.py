"""eyes / back eyes: "Every mom has a second pair of eyes on the back of her head."
Max spends a year making mom hide them under a beanie, then rips it off at the beach to find his sister.
Shots are keyed to script word indices (audio/words.json)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eyeslib import *   # noqa

V = Video(__file__)
story.bind(V)
S = SB


def no_back_wall():
    """Living room: drop the back wall so the camera can sit behind the couch."""
    for ob in list(bpy.data.objects):
        if ob.name.startswith(("lr_back", "lr_trim", "lr_win", "lr_out", "lr_car")):
            bpy.data.objects.remove(ob, do_unlink=True)
    light("lr_rear", "AREA", (0, 14, 9), 2500, (1.0, 0.96, 0.9), 8, target=(0, 6, 4))


def bkb(p, s=1.0):
    """Back-eyes point of a character facing -Y (rot 0): back of head on +Y."""
    return (p[0], p[1] + 0.6 * s, p[2] + (FH + 0.1) * s)


def kit_mom(t0, t1, expr="neutral", back="normal", beanie=None, loc=MOM_K, rot=180, wash=True):
    m = mom_c(t0, t1, expr, back, beanie)
    m.pose(t0, loc=loc, rot=rot)
    if wash:
        m.pose(t0, armL=(70, -10), armR=(70, -10))
        noise(m.shL, "rotation_euler", 0, 0.12, 3)
        noise(m.shR, "rotation_euler", 0, 0.12, 3.5)
    return m


def snap_eyes(cam, t, tgt, lens0=34, lens1=50):
    cam.crash(t, lens0, lens1, 0.08)


# ================================================================== HOOK
@S(1, 0, 5, "HOOK: Max sneaks up behind mom at the sink with a sleep mask, whip in")
def s01(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "normal")
    k = kid_c(t0, t1, "smug")
    p0, p1 = (-1.0, -3.0, 0), (-3.6, 1.2, 0)
    k.walk(t0, t1, p0, p1, rate=1.6, swing=18, arm=0, bob=0.18)
    k.pose(t0, armL=(120, -20), armR=(120, -20))
    k.pose(t1, armL=(140, -25), armR=(140, -25))
    mk = sleep_mask("mask")
    locs.hand_prop(k, "R", mk, offset=(-1.0, -0.4, -2.0))
    m.back.key(t0, "normal"); m.back.key(t0 + 0.9, "side_r"); m.back.key(t1 - 0.3, "side_l")
    tg = (-3.8, 1.0, 4.0)
    cam = Cam()
    cam.whip(t0, t0 + 0.22, orbit_pos(up(JAR, 1.0), 6, -20, 4), up(JAR, 1.0), orbit_pos(tg, 11.5, -40, 10), tg, lens=22)
    cam.key(t1, orbit_pos(tg, 9.0, -32, 12), tg, lens=24, focus=tg, fstop=3)
    cam.handheld(0.6)
    sfx(t0 + 0.3, "footsteps", 0.35)


@S(2, 5, 9, "Trying to blind: Max stretches the mask toward the back eyes, they swivel to him")
def s02(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "side_l")
    k = kid_c(t0, t1, "smug")
    kp = (-3.0, 1.7, 0)
    k.pose(t0, loc=kp, rot=facing(kp, MOM_K))
    k.pose(t0, armL=(150, -25), armR=(150, -25))
    k.pose(t1, armL=(165, -15), armR=(165, -15), torso=(0, 10, 0))
    tg = bk(MOM_K)
    m.back.snap(w(7), "wide")
    k.face(w(7) + 0.1, "shock")
    cam = Cam()
    cam.push(t0, t1, tg, 5.8, 4.6, yaw=-80, yaw1=-68, pitch=6, lens=30, fstop=2.2)
    cam.crash(w(7), 32, 40, 0.08)
    cam.handheld(0.5)


@S(3, 9, 10, "...my mom: back eyes glare, crash zoom")
def s03(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "angry", wash=False)
    tg = bk(MOM_K)
    cam = Cam()
    cam.push(t0, t1, tg, 4.4, 3.8, yaw=0, pitch=2, lens=30, fstop=1.8)
    cam.crash(t0 + 0.05, 30, 40, 0.08)
    cam.handheld(1.4)
    sfx(t0, "bonk", 0.5)


@S(4, 10, 13, "Then her secret eyes: beach, back eyes open in blazing sun")
def s04(t0, t1):
    beach(t0, t1, crowd_n=40, umbrellas=True)
    m = mom_c(t0, t1, "determined", "wide")
    m.pose(t0, loc=MOM_B, rot=0)
    tg = bkb(MOM_B)
    sparkle_on("sp4", tg, t0 + 0.1, 1.2, 12, seed=4)
    cam = Cam()
    cam.push(t0, t1, tg, 2.6, 3.6, yaw=170, yaw1=190, pitch=-8, lens=28, fstop=2)
    cam.handheld(0.6)
    sfx(t0, "rise", 0.5)
    sfx(t0 + 0.1, "sparkle", 0.6)


@S(5, 13, 16, "Saved my little: mom runs BACKWARDS into the surf")
def s05(t0, t1):
    beach(t0, t1, crowd_n=30, stand=False)
    m = mom_c(t0, t1, "determined", "angry")
    p0, p1 = (-4, SHORE - 6, 0), (-4, SHORE + 4, -0.8)
    m.walk(t0, t1, p0, p1, rate=3.4, swing=50, arm=60, bob=0.3, face_dir=False)
    m.pose(t0, rot=0)
    W2.poof("spl5", (-4, SHORE + 2, 0.4), t1 - 0.25, s=1.5, seed=5)
    cam = Cam()
    cam.key(t0, (3, SHORE + 9, 3.2), (-4, SHORE - 5, 4.0), lens=26, focus=14, fstop=4)
    cam.key(t1, (4, SHORE + 12, 2.8), (-4, SHORE + 2, 3.6), lens=28, focus=11, fstop=4)
    cam.handheld(1.4)
    sfx(t0, "whoosh", 0.6)
    sfx(t1 - 0.25, "splash", 0.8)


@S(6, 16, 19, "Sister's life: mom carries sister + duck out of the water, heroic low angle")
def s06(t0, t1):
    beach(t0, t1, crowd_n=40, stand=False)
    m = mom_c(t0, t1, "grin", "happy")
    p = (2, SHORE - 1, 0)
    m.walk(t0, t1, (2, SHORE + 1.5, -0.4), p, rate=1.8, swing=24, arm=0)
    m.pose(t0, armL=(80, -10), armR=(80, -10))
    si = sis_c(t0, t1, "joy")
    si.root.parent = m.hip
    si.root.location = (0, -1.1, 0.6)
    si.pose(t0, armL=(160, 30), armR=(160, 30))
    dk = duck("dk6", (0, 0, 0), s=0.55)
    dk.parent = m.hip
    dk.location = (0, -1.2, -0.4)
    sparkle_on("sp6", (p[0], p[1], 6), t0 + 0.3, 2.0, 14, seed=6)
    cam = Cam()
    tg = (p[0], p[1], 4.5)
    cam.orbit(t0, t1, tg, 9, -30, 10, pitch=-12, lens=24, fstop=3)
    cam.handheld(0.6)
    sfx(t0 + 0.3, "sparkle", 0.6)
    sfx(t0 + 0.2, "cheer", 0.35)


# ================================================================== RULE
@S(7, 19, 24, "You see, in this world: kitchen wide, mom at the sink, crane down")
def s07(t0, t1):
    kitchen(table=True)
    m = kit_mom(t0, t1, "smile", "normal")
    k = kid_c(t0, t1, "happy")
    sit_on(k, t0, (1, -2.8, 2.6), rot=0)
    cam = Cam()
    cam.key(t0, (9, -16, 13), (-2, 3, 3), lens=22, focus=18, fstop=6)
    cam.key(t1, (6, -14, 7), (-3, 3, 4), lens=24, focus=17, fstop=6)
    cam.handheld(0.5)
    sfx(t0 + 0.05, "whoosh", 0.5)


@S(8, 24, 28, "Every mom has a: mom turns to camera, front face, smile")
def s08(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "smile", "normal")
    m.pose(t0, loc=p, rot=150)
    m.pose(t0 + 0.3, rot=0)
    m.face(t0 + 0.35, "grin")
    m.act(t0 + 0.35, "wave")
    cam = Cam()
    cam.push(t0, t1, hd(p), 5.0, 3.6, yaw=-10, yaw1=5, pitch=4, lens=30, fstop=2.2)
    cam.handheld(0.5)


@S(9, 28, 31, "Second pair: orbit from her face around to the back of her head")
def s09(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "grin", "happy")
    m.pose(t0, loc=p, rot=0)
    m.back.key(t0, "normal")
    tg = up(hd(p), 0.1)
    cam = Cam()
    cam.orbit(t0, t1, tg, 3.2, -10, -180, pitch=4, lens=32, steps=6, fstop=2)
    cam.handheld(0.3)
    sfx(t0, "whoosh", 0.7)
    sfx(t1 - 0.15, "ding", 0.5)


@S(10, 31, 38, "Of eyes on the back of her head: push into the back eyes")
def s10(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "smile", "normal", blink=False)
    m.pose(t0, loc=p, rot=0)
    m.back.key(w(34), "wide")
    m.back.key(w(36) + 0.1, "normal")
    tg = bkb(p)
    cam = Cam()
    cam.push(t0, t1, tg, 5.2, 3.8, yaw=175, yaw1=185, pitch=3, lens=32, fstop=1.8)
    cam.handheld(0.3)


@S(11, 38, 40, "Real ones: the eyes look left, right, straight into the lens")
def s11(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "smile", "side_l", blink=False)
    m.pose(t0, loc=p, rot=0)
    m.back.key(t0 + 0.15, "side_r")
    m.back.key(t1 - 0.15, "normal")
    tg = bkb(p)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.7, yaw=180, pitch=0, lens=34, fstop=1.6)
    cam.handheld(0.4)
    sfx(t1 - 0.15, "ding", 0.4)


@S(12, 40, 42, "They blink")
def s12(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "smile", "normal", blink=False)
    m.pose(t0, loc=p, rot=0)
    for tt in (w(41), w(41) + 0.3):
        m.back.key(tt, "closed"); m.back.key(tt + 0.1, "normal")
        sfx(tt, "blink", 0.8)
    tg = bkb(p)
    cam = Cam()
    cam.push(t0, t1, tg, 4.0, 3.6, yaw=200, pitch=2, lens=34, fstop=1.6)
    cam.handheld(0.4)


@S(13, 42, 44, "They roll: big eye roll")
def s13(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "smile", "normal", blink=False)
    m.pose(t0, loc=p, rot=0)
    tr = w(43)
    m.back.key(tr, "up"); m.back.key(tr + 0.15, "side_l"); m.back.key(tr + 0.3, "half")
    tg = bkb(p)
    cam = Cam()
    cam.key(t0, orbit_pos(tg, 4.0, 160, 0), tg, lens=34, focus=tg, fstop=1.6, roll=0.0)
    cam.key(t1, orbit_pos(tg, 3.7, 180, 4), tg, lens=34, focus=tg, fstop=1.6, roll=0.12)
    cam.handheld(0.4)
    sfx(tr, "boing", 0.35)


@S(14, 44, 48, "They cry at movies: mom on the couch, the back eyes weep at the camera behind")
def s14(t0, t1):
    L = W.tv_room()
    no_back_wall()
    m = mom_c(t0, t1, "cry", "cry", blink=False)
    seat = (0, 6.2, 2.2)
    sit_on(m, t0, seat, rot=0)
    m.pose(t0, armL=(60, -20), armR=(60, -20))
    tears("tb", m, t0 + 0.1, t1, back=True)
    tg = bkb((0, 6.2, 0.24))
    cam = Cam()
    cam.push(t0, t1, tg, 3.6, 3.0, yaw=170, yaw1=190, pitch=12, lens=28, fstop=2)
    light("backfill", "AREA", (0, 9.6, 7.5), 900, (1.0, 0.95, 0.9), 3, target=tg)
    cam.handheld(0.4)
    sfx(t0 + 0.1, "aww", 0.6)


@S(15, 48, 52, "So moms see everything: 360 orbit, eyes dart everywhere")
def s15(t0, t1):
    kitchen()
    p = (-3, 1.0, 0)
    m = mom_c(t0, t1, "smug", "side_l", blink=False)
    m.pose(t0, loc=p, rot=0)
    for i, e in enumerate(["side_r", "up", "side_l", "wide"]):
        m.back.key(t0 + 0.2 + i * 0.22, e)
    for i, e in enumerate(["side_l", "side_r", "normal"]):
        m.face(t0 + 0.25 + i * 0.3, eyes=e)
    tg = up(hd(p), 0.0)
    cam = Cam()
    cam.orbit(t0, t1, tg, 4.0, 90, 450, pitch=6, lens=30, steps=8, fstop=2.2)
    cam.handheld(0.3)
    sfx(t0, "whoosh", 0.6)
    sfx(t1 - 0.25, "sparkle", 0.6)


# ================================================================== SOCIETY
TEACH = (-1.5, 11.6, 0)


def class_set(t0, t1):
    R, ks = class_scene(t0, t1, kids=8, board="chalkboard.png", skip=((-2.5, 1.5), (2.5, 1.5)))
    a = kid_c(t0, t1, "smug", name="NoteA")
    W.sit(a, t0, (-2.5, 1.5))
    b = townie(9, t0, t1, "happy")
    W.sit(b, t0, (2.5, 1.5))
    tch = mom_c(t0, t1, "neutral", "normal", name="Teach", shirt="#63c06a", hair_color="#2a1d16", skin="#c9926a")
    tch.pose(t0, loc=TEACH, rot=180, armR=(150, 10))
    noise(tch.shR, "rotation_euler", 1, 0.15, 3)
    return tch, a, b


@S(16, 52, 58, "Teachers face the board: from the back of the class, teacher writing")
def s16(t0, t1):
    tch, a, b = class_set(t0, t1)
    tg = bk(TEACH)
    cam = Cam()
    cam.key(t0, (2, -8, 10.5), (-1, 8, 5), lens=24, focus=18, fstop=5)
    cam.key(t1, (0.5, -1, 9.0), tg, lens=30, focus=13, fstop=3)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "paper", 0.25)


@S(17, 58, 62, "Catch you passing notes: note slides, back eyes snap, teacher points back")
def s17(t0, t1):
    tch, a, b = class_set(t0, t1)
    note = box("note", (0.8, 0.6, 0.03), (-1.2, 1.5, 3.45), M("#fbf8f0", 0.6), 0.0, rot=(0, 0, 10))
    note.keyframe_insert("location", frame=F(t0 + 0.1))
    note.location = (1.4, 1.5, 3.45)
    note.keyframe_insert("location", frame=F(t0 + 0.6))
    a.act(t0, "reach", expr="smug")
    tc = w(58) + 0.05
    tch.back.snap(tc, "angry")
    point_back(tch, tc + 0.15, "L")
    a.face(tc + 0.2, "shock"); b.face(tc + 0.2, "shock")
    a.act(tc + 0.2, "recoil")
    cam = Cam()
    tg = (0.0, 1.5, 4.2)
    cam.key(t0, (0.5, -4, 6.5), tg, lens=30, focus=6, fstop=3)
    cam.whip(tc + 0.1, tc + 0.3, (0.5, -4, 6.5), tg, (0, 7.4, 6.0), bk(TEACH), lens=34)
    cam.key(t1, (0, 8.6, 5.6), bk(TEACH), lens=36, focus=3.0, fstop=2)
    cam.handheld(0.8)
    sfx(tc, "blink", 0.8)
    sfx(tc + 0.15, "buzzer", 0.5)


def car_cast(t0, t1, mom_back="normal", kid_expr="nervous"):
    m = mom_c(t0, t1, "smile", mom_back)
    sit_on(m, t0, DRV, rot=-90)
    m.pose(t0, armL=(80, -12), armR=(80, -12))
    noise(m.root, "location", 2, 0.04, 4)
    k = kid_c(t0, t1, "worried" if kid_expr == "nervous" else kid_expr)
    sit_on(k, t0, BSEAT, rot=-90)
    noise(k.root, "location", 2, 0.04, 4)
    return m, k


@S(18, 62, 66, "Moms drive forward: through the windshield, mom driving, trees streaming")
def s18(t0, t1):
    car_int(True, t0, t1)
    m, k = car_cast(t0, t1)
    tg = (-1.6, -1.6, 5.6)
    cam = Cam()
    cam.push(t0, t1, tg, 7.5, 6.0, yaw=-92, yaw1=-80, pitch=6, lens=28, fstop=3)
    cam.handheld(0.8)
    sfx(t0, "wind", 0.3)


@S(19, 66, 71, "Stare at the back seat: Max's POV, the back eyes stare at him")
def s19(t0, t1):
    car_int(True, t0, t1)
    m, k = car_cast(t0, t1, "squint")
    m.back.key(w(66), "angry")
    k.face(w(68), "scared")
    k.pose(w(68), hipz=-0.3, torso=(0, 10, 0))
    tg = (-0.98, -1.6, 5.8)
    cam = Cam()
    cam.key(t0, (4.4, 1.2, 6.5), tg, lens=28, focus=tg, fstop=2.4)
    cam.key(t1, (3.6, 0.8, 6.3), tg, lens=32, focus=tg, fstop=2.0)
    cam.handheld(0.7)
    sfx(w(66), "blink", 0.6)


@S(20, 71, 75, "At the same time: side view, front eyes on the road, back eyes on Max")
def s20(t0, t1):
    car_int(True, t0, t1)
    m, k = car_cast(t0, t1, "angry", "scared")
    m.face(t0, "smile")
    for nm in ("ci_side1", "ci_win1", "ci_pil-4.61", "ci_pil0.51", "ci_pil5.61", "ci_seat_p", "ci_seatb_p", "ci_rest_p"):
        ob = bpy.data.objects.get(nm)
        if ob:
            bpy.data.objects.remove(ob, do_unlink=True)
    tg = (0.9, -1.6, 5.4)
    cam = Cam()
    cam.push(t0, t1, tg, 12, 10, yaw=180, yaw1=170, pitch=6, lens=26, fstop=5)
    cam.handheld(0.6)


def barber_cast(t0, t1, back="worried"):
    barbershop()
    cu = mom_c(t0, t1, "worried", back, name="Cust", shirt="#9b6ad6", hair_color="#d9a83a")
    sit_on(cu, t0, (0, 2.0, 2.75), rot=180)
    cape = box("cape", (2.8, 1.6, 2.4), (0, 0, 1.0), M("#f4f4f4", 0.7), 0.4, parent=cu.hip, coll=cu.coll)
    bp = (2.6, -0.4, 0)
    ba = adult(2, t0, t1, "worried")
    ba.pose(t0, loc=bp, rot=facing(bp, (0, 2.0)))
    ba.pose(t0, armR=(110, -20), armL=(60, -10))
    return cu, ba


@S(21, 75, 81, "Barbers have to cut around them: barbershop wide, clippers buzz")
def s21(t0, t1):
    cu, ba = barber_cast(t0, t1, "side_r")
    cl = clippers("clip")
    cl.location = (1.2, 0.9, 5.6); cl.rotation_euler = (math.radians(60), 0, math.radians(40))
    cl.keyframe_insert("location", frame=F(t0))
    cl.location = (0.6, 1.1, 5.7)
    cl.keyframe_insert("location", frame=F(t1))
    tg = (0.6, 1.2, 4.8)
    cam = Cam()
    cam.push(t0, t1, tg, 11, 8.5, yaw=-25, yaw1=-12, pitch=8, lens=26, fstop=4)
    cam.handheld(0.6)
    sfx(t0 + 0.1, "clipper", 0.5)


@S(22, 81, 84, "Very, very carefully: macro, clippers inch around the nervous back eyes")
def s22(t0, t1):
    cu, ba = barber_cast(t0, t1, "worried")
    cl = clippers("clip")
    hp = (0, 1.36, 5.41)
    path = [(0.55, 1.2, 5.95), (0.2, 1.15, 6.0), (-0.2, 1.15, 6.0), (-0.55, 1.2, 5.95)]
    for i, q in enumerate(path):
        cl.location = q
        cl.rotation_euler = (math.radians(80), 0, math.radians(10 - i * 7))
        cl.keyframe_insert("location", frame=F(t0 + i * (t1 - t0) / 3.2))
        cl.keyframe_insert("rotation_euler", frame=F(t0 + i * (t1 - t0) / 3.2))
    cu.back.key(t0, "side_r"); cu.back.key(t0 + 0.45, "up"); cu.back.key(t0 + 0.9, "side_l"); cu.back.key(t1 - 0.3, "scared")
    tg = (0, 1.3, 5.6)
    cam = Cam()
    cam.push(t0, t1, tg, 3.8, 3.2, yaw=-8, yaw1=6, pitch=6, lens=32, fstop=1.6)
    cam.handheld(0.5)
    sfx(t0, "clipper", 0.45)
    sfx(w(82) - 0.05, "gasp", 0.3)


# ================================================================== COOKIES
@S(23, 84, 88, "No kid in history: cookie jar hero shot under a spotlight")
def s23(t0, t1):
    kitchen()
    light("jar_spot", "SPOT", (JAR[0], JAR[1] - 4, CTOP + 9), 2500, (1.0, 0.92, 0.7), 0.5, target=up(JAR, 1.0), spot=35)
    tg = up(JAR, 1.1)
    cam = Cam()
    cam.push(t0, t1, tg, 6.0, 4.2, yaw=-20, yaw1=0, pitch=-4, lens=30, fstop=2)
    cam.handheld(0.3)
    sfx(t0 + 0.05, "rise", 0.4)


@S(24, 88, 94, "Has ever stolen a cookie: '0 STOLEN' pops over the jar")
def s24(t0, t1):
    kitchen()
    tg = up(JAR, 1.6)
    pop_text("z0", "0", (JAR[0], JAR[1] - 1.4, CTOP + 3.8), w(89), 1.6, "#ffe14a")
    pop_text("z1", "COOKIES STOLEN", (JAR[0], JAR[1] - 1.4, CTOP + 2.8), w(89) + 0.1, 0.5, "#ffffff")
    cam = Cam()
    cam.push(t0, t1, tg, 7.0, 6.0, yaw=0, pitch=2, lens=30, fstop=3)
    cam.crash(w(89), 30, 36, 0.08)
    cam.handheld(0.4)
    sfx(w(89), "ding", 0.7)


@S(25, 94, 95, "Ever: back eyes, smug half-lids, mom nods without turning")
def s25(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smug", "half")
    m.nod(t0 + 0.05, 1, 10)
    tg = bk(MOM_K)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.6, yaw=-10, pitch=2, lens=32, fstop=1.8)
    cam.handheld(0.4)


@S(26, 95, 97, "Except me: Max smirk close-up, rubs hands")
def s26(t0, t1):
    kitchen()
    p = (4, -3, 0)
    k = kid_c(t0, t1, "smug")
    k.pose(t0, loc=p, rot=-15)
    k.pose(t0, armL=(70, -40), armR=(70, -40))
    noise(k.shL, "rotation_euler", 2, 0.4, 2); noise(k.shR, "rotation_euler", 2, 0.4, 2.2)
    k.face(t0 + 0.2, "wink")
    cam = Cam()
    cam.push(t0, t1, hd(p), 4.2, 3.2, yaw=-30, yaw1=-15, pitch=-6, lens=30, fstop=2)
    cam.crash(t0 + 0.15, 30, 36, 0.08)
    cam.handheld(0.5)
    sfx(t0 + 0.2, "sparkle", 0.4)


@S(27, 97, 102, "I tried every single day: calendar days flip, Max peeks past it")
def s27(t0, t1):
    kitchen()
    calendar("cal", (-9.15, 8.0, 10.2), t0, t1, ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"], s=0.8)
    k = kid_c(t0, t1, "determined")
    p = (-7.6, 3.6, 0)
    k.pose(t0, loc=p, rot=-25)
    k.act(t0 + 0.3, "fists", expr="determined")
    tg = (-8.6, 6.0, 7.2)
    cam = Cam()
    cam.push(t0, t1, tg, 9.5, 8.0, yaw=-12, yaw1=2, pitch=-2, lens=28, fstop=3)
    cam.handheld(0.5)


MOM_S = (0.0, 3.5, 0.0)


def sneak_set(t0, t1, back="normal"):
    kitchen()
    m = kit_mom(t0, t1, "smile", back, loc=MOM_S)
    return m


@S(28, 102, 104, "I tiptoed: low tracking, Max tiptoes toward the jar")
def s28(t0, t1):
    m = sneak_set(t0, t1, "closed")
    k = kid_c(t0, t1, "sus")
    p0, p1 = (9, -2, 0), (6.4, 2.6, 0)
    k.walk(t0, t1, p0, p1, rate=1.6, swing=16, arm=8, bob=0.25)
    k.pose(t0, armL=(60, 30), armR=(60, 30))
    cam = Cam()
    cam.key(t0, (11, -10, 4.0), (5.5, 1.0, 3.0), lens=24, focus=10, fstop=4)
    cam.key(t1, (10, -8, 3.6), (4.5, 2.2, 3.2), lens=26, focus=9, fstop=4)
    cam.handheld(0.5)
    sfx(t0 + 0.1, "footsteps", 0.25)


@S(29, 104, 105, "BLINK: back eyes pop open")
def s29(t0, t1):
    m = sneak_set(t0, t1, "closed")
    m.back.key(t0 + 0.06, "wide")
    sfx(t0 + 0.06, "blink", 1.0)
    tg = bk(MOM_S)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.7, yaw=15, pitch=2, lens=32, fstop=1.6)
    cam.crash(t0 + 0.06, 32, 42, 0.07)
    cam.handheld(1.2)


@S(30, 105, 108, "Put it back: mom points over her shoulder; Max freezes with a cookie")
def s30(t0, t1):
    m = sneak_set(t0, t1, "squint")
    point_back(m, t0, "L")
    k = kid_c(t0, t1, "shock")
    kp = (5.2, 2.9, 0)
    k.pose(t0, loc=kp, rot=170, armR=(140, 0))
    ck = cookie("ck30", (0, 0, 0), s=1.0)
    locs.hand_prop(k, "R", ck, offset=(0, -0.2, -2.2))
    k.act(t0 + 0.1, "recoil", expr="shock")
    tg = (2.6, 3.0, 4.2)
    cam = Cam()
    cam.push(t0, t1, tg, 12, 10, yaw=-10, yaw1=0, pitch=4, lens=24, fstop=5)
    cam.handheld(0.6)


@S(31, 108, 110, "I crawled: Max army-crawls across the floor, ground-level")
def s31(t0, t1):
    m = sneak_set(t0, t1, "closed")
    k = kid_c(t0, t1, "determined")
    crawl(k, t0, t1, (8, -3, 0), (6, 0.5, 0), rot=facing((8, -3), (6, 0.5)))
    cam = Cam()
    cam.key(t0, (12.5, -6.5, 2.4), (7.6, -2.0, 1.6), lens=26, focus=6.5, fstop=3)
    cam.key(t1, (10.8, -3.6, 2.4), (6.2, 0.3, 1.6), lens=26, focus=6.0, fstop=3)
    cam.handheld(0.6)


@S(32, 110, 111, "BLINK: eyes open and look down at him")
def s32(t0, t1):
    m = sneak_set(t0, t1, "closed")
    m.back.key(t0 + 0.05, "down")
    sfx(t0 + 0.05, "blink", 1.0)
    tg = bk(MOM_S)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.7, yaw=25, pitch=-14, lens=32, fstop=1.6)
    cam.crash(t0 + 0.05, 32, 42, 0.07)
    cam.handheld(1.0)


@S(33, 111, 114, "Put it back: Max slumps and drops the cookie back in the jar")
def s33(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "down", loc=(-1.0, 3.5, 0))
    point_back(m, t0, "L")
    k = kid_c(t0, t1, "worried")
    kp = (5.0, 3.1, 0)
    k.pose(t0, loc=kp, rot=180, armR=(120, 0))
    k.act(t0 + 0.4, "slump", expr="worried")
    ck = cookie("ck33", (JAR[0], JAR[1] - 0.6, CTOP + 3.0), s=1.0, rot=(1.2, 0, 0))
    ck.keyframe_insert("location", frame=F(t0 + 0.3))
    ck.location = (JAR[0], JAR[1], CTOP + 1.4)
    ck.keyframe_insert("location", frame=F(t0 + 0.6))
    tg = (2.0, 3.5, 4.0)
    cam = Cam()
    cam.push(t0, t1, tg, 9, 8, yaw=10, yaw1=0, pitch=8, lens=26, fstop=4)
    cam.handheld(0.5)
    sfx(t0 + 0.6, "clink", 0.5)


@S(34, 114, 120, "Dressed up as the dog: dog-costume Max on all fours, tail wagging")
def s34(t0, t1):
    m = sneak_set(t0, t1, "closed")
    k = kid_c(t0, t1, "grin", dog=True)
    crawl(k, t0, t1, (9, -3, 0), (6.5, 0.8, 0), rot=facing((9, -3), (6.5, 0.8)), rate=1.8)
    cam = Cam()
    cam.key(t0, (2.6, 4.2, 3.0), (8.2, -2.0, 1.8), lens=22, focus=7.5, fstop=3)
    cam.key(t1, (2.4, 4.4, 2.8), (6.8, 0.4, 1.8), lens=22, focus=5.5, fstop=3)
    cam.handheld(0.5)
    sfx(t0 + 0.4, "pop", 0.4)
    sfx(w(119), "boing", 0.3)


@S(35, 120, 121, "BLINK: suspicious squint")
def s35(t0, t1):
    m = sneak_set(t0, t1, "closed")
    m.back.key(t0 + 0.05, "squint")
    sfx(t0 + 0.05, "blink", 1.0)
    tg = bk(MOM_S)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.7, yaw=-20, pitch=2, lens=32, fstop=1.6)
    cam.crash(t0 + 0.05, 32, 42, 0.07)
    cam.handheld(1.0)


@S(36, 121, 125, "Put it back, Max: mom points back, dog-Max drops the cookie, ears droop")
def s36(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smug", "squint", loc=(-1.0, 3.5, 0))
    point_back(m, t0, "L")
    lips(m, t0, t1)
    k = kid_c(t0, t1, "shock", dog=True)
    dog_pose(k, t0, (4.2, 0.2, 0), rot=facing((4.2, 0.2), (-1, 3.5)))
    ck = cookie("ck36", (0, 0, 0))
    ck.parent = k.head; ck.location = (0, -0.8, -0.35); ck.rotation_euler = (math.radians(90), 0, 0)
    sets.set_obj_visible(ck, w(124), True); sets.set_obj_visible(ck, w(124) + 0.04, False)
    k.face(w(124), "cry")
    tg = (1.6, 1.8, 3.4)
    cam = Cam()
    cam.push(t0, t1, tg, 9, 7.5, yaw=-30, yaw1=-15, pitch=8, lens=26, fstop=4)
    cam.crash(w(124), 26, 32, 0.08)
    cam.handheld(0.6)
    sfx(w(124), "rimshot", 0.5)


# ================================================================== BIRTHDAY
CAKE = (1.0, -5.0, TABLE_Z)
KID_T = (1.0, -1.8, 0)          # behind the table, facing -Y (toward the cake + camera)
MOM_T = (5.6, -4.6, 0)


def cake(loc, t_out=None, coll=None):
    root = empty("cake", loc, coll=coll)
    cyl("cake_b", 1.5, 1.0, (0, 0, 0.5), M("#f6c0d8", 0.6), 32, bev=0.08, parent=root, coll=coll)
    cyl("cake_t", 1.1, 0.8, (0, 0, 1.4), M("#ffffff", 0.6), 32, bev=0.08, parent=root, coll=coll)
    for i in range(10):
        a = i / 10 * math.tau
        sphere(f"cake_dot{i}", 0.12, (math.cos(a) * 1.5, math.sin(a) * 1.5, 0.9), M(["#e8423a", "#3f7fd9", "#f2c14e"][i % 3], 0.4),
               parent=root, coll=coll, seg=8)
    fl = []
    for i in range(5):
        a = i / 5 * math.tau
        x, y = math.cos(a) * 0.6, math.sin(a) * 0.6
        cyl(f"cake_c{i}", 0.07, 0.7, (x, y, 2.15), M(["#3f7fd9", "#63c06a", "#f2c14e", "#e8423a", "#9b6ad6"][i], 0.4), 8,
            parent=root, coll=coll)
        f = sphere(f"cake_f{i}", 0.12, (x, y, 2.62), emitm("#ffb030", 12), (1, 1, 1.7), parent=root, coll=coll, seg=8)
        noise(f, "scale", 2, 0.25, 2)
        fl.append(f)
    if t_out is not None:
        for f in fl:
            sets.set_obj_visible(f, t_out, True)
            sets.set_obj_visible(f, t_out + 0.04, False)
    lt = light("cake_glow", "POINT", (loc[0], loc[1], loc[2] + 3.4), 220, (1.0, 0.7, 0.35), 0.6)
    if t_out is not None:
        lt.data.keyframe_insert("energy", frame=F(t_out))
        lt.data.energy = 0
        lt.data.keyframe_insert("energy", frame=F(t_out + 0.05))
    return root


def balloons(base, n=5, seed=1):
    rnd = random.Random(seed)
    cols = ["#e8423a", "#3f7fd9", "#f2c14e", "#63c06a", "#f09ac2"]
    for i in range(n):
        p = (base[0] + rnd.uniform(-2, 2), base[1] + rnd.uniform(-1, 1), base[2] + rnd.uniform(0, 2.5))
        b = sphere(f"bal{seed}{i}", 0.9, p, M(cols[i % 5], 0.2), (1, 1, 1.2), seg=16)
        noise(b, "location", 2, 0.2, 18 + i)
        noise(b, "location", 0, 0.15, 22 + i)
        cyl(f"bals{seed}{i}", 0.02, 4.0, (p[0], p[1], p[2] - 3.0), M("#ffffff", 0.5), 4, parent=None)


def party_hat(ch, col="#3f7fd9"):
    cyl(ch.name + "_ph", 0.45, 1.1, (0.1, -0.05, 1.05), sets.checker_mat("ph" + col, col, "#ffffff", 3.0, 0.5), 16, r2=0.02,
        parent=ch.head, coll=ch.coll, rot=(0, -12, 0))


def bday(t0, t1, t_out=None, mom=True, mom_back="normal", beanie=None, mom_expr="smile", kid_expr="joy"):
    kitchen(table=True)
    cake(CAKE, t_out)
    balloons((-6, 2, 6), 6, 1)
    balloons((9, 0, 6), 5, 2)
    k = kid_c(t0, t1, kid_expr)
    k.pose(t0, loc=KID_T, rot=0)
    party_hat(k)
    m = None
    if mom:
        m = mom_c(t0, t1, mom_expr, mom_back, beanie)
        m.pose(t0, loc=MOM_T, rot=facing(MOM_T, KID_T))
        party_hat(m, "#e8423a")
    return k, m


@S(37, 125, 129, "On my birthday: party, balloons, confetti, whip in")
def s37(t0, t1):
    k, m = bday(t0, t1)
    k.act(t0 + 0.2, "cheer", expr="joy")
    confetti("cf37", (1, -4, 7), (5, 3, 2), t0 + 0.15, 1.6, 70, seed=37)
    tg = (2.0, -4, 4.0)
    cam = Cam()
    cam.whip(t0, t0 + 0.22, orbit_pos(tg, 12, -60, 10), tg, orbit_pos(tg, 10, -15, 12), tg, lens=26)
    cam.key(t1, orbit_pos(tg, 8.5, -5, 10), tg, lens=26, focus=tg, fstop=4)
    cam.handheld(0.5)
    sfx(t0 + 0.15, "confetti", 0.7)
    sfx(t0 + 0.2, "cheer", 0.4)


@S(38, 129, 133, "Made my wish: eyes shut, big blow, candles out")
def s38(t0, t1):
    tb = w(132) + 0.1
    k, m = bday(t0, t1, t_out=tb, mom=False, kid_expr="relief")
    k.pose(t0, torso=(0, 12, 0))
    k.face(tb - 0.25, eyes="closed", mouth="o")
    k.face(tb + 0.3, "grin")
    tg = (1.0, -2.6, 4.4)
    cam = Cam()
    cam.push(t0, t1, tg, 6.5, 5.2, yaw=-15, yaw1=0, pitch=16, lens=30, fstop=2.2)
    cam.handheld(0.4)
    sfx(tb - 0.1, "wind", 0.5)
    sfx(tb + 0.05, "poof", 0.3)


@S(39, 133, 137, "Mom, I want privacy: Max talks to mom face to face")
def s39(t0, t1):
    k, m = bday(t0, t1, t_out=t0 - 1)
    k.pose(t0, rot=facing(KID_T, MOM_T))
    k.face(t0, "determined")
    lips(k, t0, t1)
    k.act(t0 + 0.1, "point", expr="determined")
    m.face(t0 + 0.3, "confused")
    tg = up(hd(KID_T), -0.3)
    cam = Cam()
    yk = facing(KID_T, MOM_T)
    cam.push(t0, t1, tg, 5.0, 4.0, yaw=yk - 35, yaw1=yk - 20, pitch=2, lens=30, fstop=2)
    cam.handheld(0.5)


@S(40, 137, 142, "Please cover your back eyes: from behind mom, her back eyes go worried")
def s40(t0, t1):
    k, m = bday(t0, t1, t_out=t0 - 1, mom_back="normal")
    k.pose(t0, rot=facing(KID_T, MOM_T))
    lips(k, t0, t1)
    k.act(t0 + 0.2, "point", expr="determined")
    m.back.key(w(140), "worried")
    m.face(w(140), "worried")
    yaw_m = facing(MOM_T, KID_T)
    tg = (MOM_T[0], MOM_T[1], FH + 0.1)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 2.8, yaw=yaw_m + 165, yaw1=yaw_m + 180, pitch=4, lens=30, fstop=2)
    cam.handheld(0.4)


@S(41, 142, 143, "Forever: Max crash-zoom, dead serious")
def s41(t0, t1):
    k, m = bday(t0, t1, t_out=t0 - 1)
    k.pose(t0, rot=facing(KID_T, MOM_T))
    k.face(t0, "angry")
    lips(k, t0, t1, "shout")
    tg = hd(KID_T)
    yk = facing(KID_T, MOM_T)
    cam = Cam()
    cam.push(t0, t1, tg, 4.4, 3.8, yaw=yk - 15, pitch=-4, lens=30, fstop=1.6)
    cam.crash(t0 + 0.04, 30, 40, 0.07)
    cam.handheld(1.0)
    sfx(t0 + 0.04, "thud", 0.5)


@S(42, 143, 150, "Sad with all four eyes: front face cries, orbit round to the back eyes crying")
def s42(t0, t1):
    k, m = bday(t0, t1, t_out=t0 - 1, mom_back="cry", mom_expr="cry")
    tears("tf", m, t0 + 0.1, t1, back=False)
    tears("tbk", m, t0 + 0.1, t1, back=True)
    yaw_m = facing(MOM_T, KID_T)
    tg = (MOM_T[0], MOM_T[1], FH + 0.1)
    cam = Cam()
    cam.orbit(t0, t1, tg, 3.4, yaw_m + 10, yaw_m + 190, pitch=4, lens=30, steps=6, fstop=1.8)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "aww", 0.7)


@S(43, 150, 158, "Big wool beanie: it drops onto her head and swallows the back eyes")
def s43(t0, t1):
    tb = w(156)
    k, m = bday(t0, t1, t_out=t0 - 1, mom_back="cry", mom_expr="worried", beanie=(tb,))
    yaw_m = facing(MOM_T, KID_T)
    tg = (MOM_T[0], MOM_T[1], FH + 0.4)
    cam = Cam()
    cam.push(t0, t1, tg, 4.8, 3.6, yaw=yaw_m + 150, yaw1=yaw_m + 165, pitch=8, lens=30, fstop=2)
    cam.crash(tb + 0.02, 30, 36, 0.08)
    cam.handheld(0.5)
    sfx(tb - 0.2, "whoosh", 0.5)
    sfx(tb, "pop", 0.9)


@S(44, 158, 163, "For a whole year: calendar months flip")
def s44(t0, t1):
    kitchen()
    calendar("cal2", (-9.15, 8.0, 10.2), t0, t1, ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
                                               "NOV", "DEC"], s=0.8)
    tg = (-9.15, 7.6, 8.8)
    cam = Cam()
    cam.push(t0, t1, tg, 6.5, 4.6, yaw=-8, yaw1=6, pitch=-2, lens=30, fstop=3)
    cam.handheld(0.4)


@S(45, 163, 168, "She never took it off: mom in the beanie at the sink, orbit")
def s45(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "closed", beanie=True)
    tg = (MOM_K[0], MOM_K[1], FH + 0.3)
    cam = Cam()
    cam.orbit(t0, t1, tg, 5.0, 30, -25, pitch=6, lens=28, fstop=2.4)
    cam.handheld(0.4)


@S(46, 168, 171, "Best year ever: Max cheers, confetti")
def s46(t0, t1):
    kitchen()
    p = (2, -3, 0)
    k = kid_c(t0, t1, "joy")
    k.pose(t0, loc=p, rot=-10)
    k.act(t0, "cheer", expr="joy")
    k.jump(t0 + 0.1, 1.4, 0.5)
    confetti("cf46", (2, -3, 9), (4, 3, 2), t0 + 0.05, 1.6, 60, seed=46)
    cam = Cam()
    cam.push(t0, t1, up(hd(p), -0.6), 7, 5.2, yaw=-20, yaw1=5, pitch=-10, lens=26, fstop=3)
    cam.handheld(0.6)
    sfx(t0 + 0.05, "confetti", 0.6)
    sfx(t0 + 0.1, "cheer", 0.5)


@S(47, 171, 174, "Cookies for breakfast: cookie tower, Max munches")
def s47(t0, t1):
    kitchen(table=True)
    k = kid_c(t0, t1, "joy")
    sit_on(k, t0, (1, -2.6, 2.6), rot=0)
    for i in range(12):
        cookie(f"tw{i}", (1.0 + (i % 2) * 0.1, -4.6, TABLE_Z + 0.08 + i * 0.13), s=1.4, rot=(0, 0, i * 0.5))
    ck = cookie("ckh", (0, 0, 0), s=1.0)
    locs.hand_prop(k, "R", ck, offset=(0, -0.2, -2.2))
    k.pose(t0, armR=(150, -30))
    k.talk(t0, t1, open_m="open_smile", wide_m="laugh", rest="grin", syll=0.11)
    tg = (1.0, -3.6, 4.6)
    cam = Cam()
    cam.push(t0, t1, tg, 5.0, 3.8, yaw=20, yaw1=5, pitch=4, lens=30, fstop=2)
    cam.handheld(0.5)
    sfx(t0 + 0.2, "crunch", 0.6)


@S(48, 174, 178, "Video games at 3AM: dark living room, TV glow, 3:00 AM pops")
def s48(t0, t1):
    L = W.tv_room()
    world((0.02, 0.03, 0.08), 0.2)
    for ob in list(bpy.data.objects):
        if ob.type == "LIGHT" and ob.name != "tv_glow":
            ob.data.energy *= 0.06
    tvg = bpy.data.objects.get("tv_glow")
    if tvg:
        tvg.data.energy = 900
        noise(tvg.data, "energy", -1, 300, 2) if False else None
    k = kid_c(t0, t1, "grin")
    sit_on(k, t0, (0, 6.2, 2.2), rot=0)
    k.pose(t0, armL=(70, -25), armR=(70, -25))
    pad = box("pad", (1.4, 0.5, 0.2), (0, 3.4, 3.6), M("#2a2a32", 0.4), 0.1)
    noise(pad, "location", 2, 0.05, 2)
    noise(k.shL, "rotation_euler", 0, 0.1, 1.5); noise(k.shR, "rotation_euler", 0, 0.1, 1.7)
    pop_text("t3", "3:00 AM", (0.0, 3.0, 7.4), w(177), 0.9, "#ff5a5a")
    tg = hd((0, 6.2, 0.24))
    cam = Cam()
    cam.push(t0, t1, tg, 9.0, 7.0, yaw=-20, yaw1=-5, pitch=4, lens=28, fstop=2.8)
    cam.handheld(0.5)
    sfx(t0 + 0.05, "game", 0.5)
    sfx(w(177), "ding", 0.5)


@S(49, 178, 179, "Freedom! Max jumps on the couch, arms up")
def s49(t0, t1):
    L = W.tv_room()
    p = (0, 6.0, 2.2)
    k = kid_c(t0, t1, "joy")
    k.pose(t0, loc=p, rot=0)
    k.act(t0, "cheer", expr="joy")
    k.jump(t0 + 0.02, 2.2, 0.5, loc=p)
    confetti("cf49", (0, 5, 11), (6, 3, 1), t0 + 0.05, 1.2, 60, seed=49)
    cam = Cam()
    cam.push(t0, t1, (0, 6, 7.6), 9, 6, yaw=0, pitch=-16, lens=24, fstop=3)
    cam.handheld(1.0)
    sfx(t0 + 0.05, "cheer", 0.6)


# ================================================================== BEACH
@S(50, 179, 186, "But then we went to the beach: crane down from the sky")
def s50(t0, t1):
    beach(t0, t1, crowd_n=160)
    cam = Cam()
    cam.key(t0, (-20, -60, 45), (0, 20, 30), lens=24, focus=80, fstop=11)
    cam.key(t1, (-26, -48, 12), (0, 10, 2), lens=24, focus=60, fstop=11)
    cam.handheld(0.4)
    sfx(t0 + 0.1, "waves", 0.6)
    sfx(t0 + 0.6, "seagull", 0.4)


@S(51, 186, 189, "Thousands of people: high wide sweep over the crowd")
def s51(t0, t1):
    beach(t0, t1, crowd_n=260)
    cam = Cam()
    cam.key(t0, (40, -70, 40), (0, -10, 0), lens=28, focus=90, fstop=11)
    cam.key(t1, (10, -75, 36), (-10, -10, 0), lens=28, focus=90, fstop=11)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "crowd", 0.5)


@S(52, 189, 194, "Mom buying ice cream: at the stand in the beanie, gets a cone")
def s52(t0, t1):
    beach(t0, t1, crowd_n=60)
    m = mom_c(t0, t1, "smile", "closed", beanie=True)
    m.pose(t0, loc=MOM_B, rot=0)
    m.act(t0 + 0.3, "reach", expr="happy")
    ic = ice_cream("ic52", s=1.0)
    locs.hand_prop(m, "R", ic, offset=(0, -0.3, -2.4))
    sets.set_obj_visible(ic, t0, False)
    for o in ic.children:
        sets.set_obj_visible(o, t0, False); sets.set_obj_visible(o, w(192), True)
    v = adult(3, t0, t1, "grin")
    v.pose(t0, loc=(STAND[0], STAND[1] - 1.0, 1.2), rot=180)
    v.act(t0 + 0.1, "hold", expr="grin")
    tg = (MOM_B[0], MOM_B[1] - 1.5, 4.8)
    cam = Cam()
    cam.push(t0, t1, tg, 9, 7, yaw=-120, yaw1=-105, pitch=4, lens=28, fstop=3)
    cam.handheld(0.5)
    sfx(w(192), "cashier", 0.5)


@S(53, 194, 197, "Facing the stand: from behind, only the beanie faces the sea")
def s53(t0, t1):
    beach(t0, t1, crowd_n=60)
    m = mom_c(t0, t1, "smile", "closed", beanie=True)
    m.pose(t0, loc=MOM_B, rot=0)
    tg = (MOM_B[0], MOM_B[1], FH + 0.2)
    cam = Cam()
    cam.push(t0, t1, tg, 6, 4.2, yaw=165, yaw1=180, pitch=6, lens=30, fstop=2.2)
    cam.handheld(0.4)


DUCK0 = (-4.0, SHORE + 3.0, 0.0)


def duck_sis(t0, t1, p0, p1, expr="joy", s=1.0):
    dk = duck("dk", p0, s=s)
    si = sis_c(t0, t1, expr)
    si.root.parent = dk
    si.root.location = (0, 0.2, -0.2)
    si.pose(t0, legL=(80, 10), legR=(80, -10), armL=(150, 30), armR=(150, 30))
    dk.keyframe_insert("location", frame=F(t0))
    dk.location = p1
    dk.keyframe_insert("location", frame=F(t1))
    set_interp(dk, "location", F(t0), "LINEAR")
    bob(dk, 0.18, 0.06, 10)
    return dk, si


@S(54, 197, 202, "Sister floated away: duck drifts off the shoreline, she waves")
def s54(t0, t1):
    beach(t0, t1, crowd_n=40, stand=False)
    dk, si = duck_sis(t0, t1, DUCK0, (-2.0, SHORE + 12.0, 0.0))
    noise(si.shR, "rotation_euler", 1, 0.6, 3)
    si.talk(t0, t1, open_m="laugh", wide_m="open_smile", rest="open_smile", syll=0.13)
    cam = Cam()
    cam.key(t0, (-9, SHORE - 7, 3.5), (-4, SHORE + 3, 1.6), lens=30, focus=11, fstop=3)
    cam.key(t1, (-8, SHORE - 3, 3.0), (-2, SHORE + 12, 1.4), lens=36, focus=16, fstop=3)
    cam.handheld(0.5)
    sfx(t0 + 0.2, "kids_laugh", 0.35)
    sfx(t0, "waves", 0.5)


@S(55, 202, 207, "On her inflatable duck: close, squeak")
def s55(t0, t1):
    sea_only(t0, t1)
    p = (0, SHORE + 14, 0.0)
    dk, si = duck_sis(t0, t1, p, (0.6, SHORE + 15, 0.0))
    tg = (0, SHORE + 13.0, 1.8)
    cam = Cam()
    cam.orbit(t0, t1, tg, 6.5, -40, 10, pitch=6, lens=30, fstop=2.4)
    cam.handheld(0.6)
    sfx(w(206), "squeak", 0.7)


@S(56, 207, 208, "Further: wide, the duck shrinks into the blue")
def s56(t0, t1):
    beach(t0, t1, crowd_n=30, stand=False)
    dk, si = duck_sis(t0, t1, (0, SHORE + 30, 0), (1, SHORE + 34, 0))
    cam = Cam()
    cam.push(t0, t1, (0, SHORE + 30, 1.5), 22, 26, yaw=8, pitch=6, lens=34, fstop=6)
    cam.handheld(0.5)
    sfx(t0, "whoosh", 0.35)


@S(57, 208, 210, "And further")
def s57(t0, t1):
    beach(t0, t1, crowd_n=30, stand=False)
    dk, si = duck_sis(t0, t1, (2, SHORE + 60, 0), (3, SHORE + 64, 0))
    cam = Cam()
    cam.push(t0, t1, (2, SHORE + 60, 1.5), 45, 52, yaw=-6, pitch=5, lens=40, fstop=8)
    cam.handheld(0.5)
    sfx(t0, "whoosh", 0.35)


@S(58, 210, 213, "Out to sea: aerial, a yellow speck in an endless ocean")
def s58(t0, t1):
    sea_only(t0, t1)
    dk, si = duck_sis(t0, t1, DOT, (DOT[0] + 1, DOT[1] + 3, 0), s=1.0)
    cam = Cam()
    cam.key(t0, (DOT[0], DOT[1] - 30, 40), DOT, lens=30, focus=50, fstop=11)
    cam.key(t1, (DOT[0], DOT[1] - 50, 75), DOT, lens=30, focus=90, fstop=11)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "wind", 0.4)


@S(59, 213, 215, "I screamed: Max scream close-up, shake")
def s59(t0, t1):
    beach(t0, t1, crowd_n=40)
    k = kid_c(t0, t1, "scream")
    k.pose(t0, loc=KID_B, rot=180)
    k.act(t0, "hands_face", expr="scream")
    tg = hd(KID_B)
    cam = Cam()
    cam.push(t0, t1, tg, 4.6, 3.8, yaw=180, pitch=-4, lens=30, fstop=1.8)
    cam.crash(t0 + 0.04, 30, 40, 0.07)
    cam.shake(0.03, 2)
    sfx(t0 + 0.04, "gasp", 0.6)


@S(60, 215, 218, "Where is she? Max spins, whip pans")
def s60(t0, t1):
    beach(t0, t1, crowd_n=80)
    k = kid_c(t0, t1, "panic")
    k.pose(t0, loc=KID_B, rot=180)
    k.pose(t0 + 0.4, rot=120); k.pose(t0 + 0.8, rot=230)
    k.act(t0, "hands_head", expr="panic")
    lips(k, t0, t1, "shout")
    tg = hd(KID_B)
    cam = Cam()
    cam.whip(t0, t0 + 0.2, orbit_pos(tg, 7.5, 120, 2), tg, orbit_pos(tg, 7.5, 200, 2), tg, lens=28)
    cam.key(t1, orbit_pos(tg, 6.5, 230, 0), tg, lens=28, focus=tg, fstop=2)
    cam.handheld(1.4)


@S(61, 218, 221, "Thousands of heads: top-down over the crowd")
def s61(t0, t1):
    beach(t0, t1, crowd_n=120, umbrellas=False, dense=(-30, -30, 16, 110))
    cam = Cam()
    cam.key(t0, (-34, -34, 30), (-34, -33.9, 0), lens=30, focus=30, fstop=11, roll=0.0)
    cam.key(t1, (-26, -28, 26), (-26, -27.9, 0), lens=30, focus=26, fstop=11, roll=0.3)
    cam.handheld(0.3)
    sfx(t0, "crowd", 0.4)


@S(62, 221, 224, "Thousands of umbrellas: top-down sea of umbrellas")
def s62(t0, t1):
    beach(t0, t1, crowd_n=40, umbrellas=True, seed=9, dense_u=(30, -40, 20, 70))
    cam = Cam()
    cam.key(t0, (34, -44, 40), (34, -43.9, 0), lens=26, focus=40, fstop=11, roll=0.6)
    cam.key(t1, (26, -38, 34), (26, -37.9, 0), lens=26, focus=34, fstop=11, roll=0.2)
    cam.handheld(0.3)
    sfx(t0, "whoosh", 0.4)


@S(63, 224, 226, "Waves everywhere: low over the water, waves block the view")
def s63(t0, t1):
    sea_only(t0, t1)
    for k in range(5):
        foam(f"wf{k}", -60, 60, SHORE + 10 + k * 7, t0 - k * 0.4, t0 - k * 0.4 + 2.4, seed=k + 10, z=0.5)
    cam = Cam()
    cam.key(t0, (0, SHORE + 2, 1.2), (6, SHORE + 60, 1.0), lens=26, focus=20, fstop=4)
    cam.key(t1, (2, SHORE + 4, 1.6), (-6, SHORE + 60, 1.0), lens=26, focus=20, fstop=4)
    cam.shake(0.02, 3)
    sfx(t0, "waves", 0.8)


@S(64, 226, 230, "I couldn't find her: Max hands on head, slow push, defeated")
def s64(t0, t1):
    beach(t0, t1, crowd_n=40)
    k = kid_c(t0, t1, "cry")
    k.pose(t0, loc=KID_B, rot=180)
    k.act(t0, "hands_head", expr="cry")
    k.act(t0 + 0.8, "slump", expr="cry")
    tg = up(hd(KID_B), -0.3)
    cam = Cam()
    cam.push(t0, t1, tg, 6.5, 4.6, yaw=200, yaw1=190, pitch=14, lens=28, fstop=2)
    cam.handheld(0.4)


# ================================================================== THE TURN
@S(65, 230, 234, "Then I noticed something: eyes go wide, crash zoom")
def s65(t0, t1):
    beach(t0, t1, crowd_n=40)
    k = kid_c(t0, t1, "cry")
    k.pose(t0, loc=KID_B, rot=180)
    tn = w(232)
    k.face(tn, "gasp")
    k.look(tn, -50, 0)
    tg = hd(KID_B)
    cam = Cam()
    cam.push(t0, t1, tg, 4.8, 4.0, yaw=185, pitch=0, lens=30, fstop=1.8)
    cam.crash(tn, 30, 38, 0.08)
    cam.handheld(0.4)
    sfx(tn - 0.2, "rise", 0.6)


@S(66, 234, 236, "Mom's beanie: rack focus to the beanie at the stand")
def s66(t0, t1):
    beach(t0, t1, crowd_n=40)
    m = mom_c(t0, t1, "smile", "closed", beanie=True)
    m.pose(t0, loc=MOM_B, rot=0)
    k = kid_c(t0, t1, "gasp")
    k.pose(t0, loc=KID_B, rot=facing(KID_B, MOM_B))
    tg = (MOM_B[0], MOM_B[1], FH + 0.5)
    cam = Cam()
    cam.key(t0, (KID_B[0] + 2, KID_B[1] + 5, 5.4), tg, lens=34, focus=KID_B[1] + 4 - 0, fstop=1.6)
    cam.key(t1, (KID_B[0] + 0.5, KID_B[1] + 4, 5.2), tg, lens=46, focus=tg, fstop=1.6)
    cam.handheld(0.4)
    sfx(t0 + 0.05, "ding", 0.5)


@S(67, 236, 243, "Those eyes were made for exactly this: Max steels himself, heroic orbit")
def s67(t0, t1):
    beach(t0, t1, crowd_n=40)
    k = kid_c(t0, t1, "determined")
    k.pose(t0, loc=KID_B, rot=facing(KID_B, MOM_B))
    k.act(t0 + 0.3, "fists", expr="determined")
    k.nod(w(241), 1, 12)
    tg = up(hd(KID_B), -0.4)
    cam = Cam()
    yk = facing(KID_B, MOM_B)
    cam.orbit(t0, t1, tg, 5.0, yk - 45, yk + 25, pitch=-12, lens=26, fstop=2.2)
    cam.handheld(0.4)
    sfx(t0 + 0.3, "rise", 0.4)


RIP = (MOM_B[0] + 1.2, MOM_B[1] + 2.0, 0)


@S(68, 243, 246, "I jumped up: Max leaps behind mom, low angle")
def s68(t0, t1):
    beach(t0, t1, crowd_n=40)
    m = mom_c(t0, t1, "smile", "closed", beanie=True)
    m.pose(t0, loc=MOM_B, rot=0)
    k = kid_c(t0, t1, "angry")
    k.pose(t0, loc=RIP, rot=facing(RIP, MOM_B))
    k.jump(w(244), 2.4, 0.6, loc=RIP)
    k.pose(w(244) + 0.3, armL=(170, 10), armR=(170, 10))
    tg = (MOM_B[0] + 0.6, MOM_B[1] + 1.2, 5.0)
    cam = Cam()
    tg = (RIP[0] - 0.6, RIP[1] - 1.0, 4.6)
    cam.key(t0, (-5.5, -16.5, 2.8), tg, lens=24, focus=tg, fstop=3)
    cam.key(t1, (-6.5, -15.5, 3.0), tg, lens=26, focus=tg, fstop=3)
    cam.handheld(0.8)
    sfx(w(244), "boing", 0.4)


@S(69, 246, 250, "Ripped it off: the beanie flies off spinning")
def s69(t0, t1):
    beach(t0, t1, crowd_n=40)
    tr = w(247)
    m = mom_c(t0, t1, "gasp", "closed", beanie=("off", tr))
    m.pose(t0, loc=MOM_B, rot=0)
    k = kid_c(t0, t1, "angry")
    k.pose(t0, loc=(RIP[0], RIP[1], 2.0), rot=facing(RIP, MOM_B), armL=(175, 10), armR=(175, 10))
    k.pose(tr + 0.2, loc=RIP, armL=(160, 40), armR=(170, -30))
    k.face(tr + 0.1, "grin")
    tg = (MOM_B[0], MOM_B[1], FH + 0.4)
    cam = Cam()
    cam.push(t0, t1, tg, 6.5, 7.0, yaw=230, yaw1=212, pitch=10, lens=26, fstop=2.4)
    cam.crash(tr, 26, 32, 0.08)
    cam.handheld(1.0)
    sfx(tr - 0.05, "whoosh", 0.8)
    sfx(tr, "pop", 0.8)


@S(70, 250, 254, "The back eyes opened: ECU, lids crack open, light pours in")
def s70(t0, t1):
    beach(t0, t1, crowd_n=20)
    m = mom_c(t0, t1, "gasp", "closed", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    to = w(253)
    m.back.key(to - 0.2, "half")
    m.back.key(to, "wide")
    sparkle_on("sp70", bkb(MOM_B), to, 0.9, 14, seed=70)
    tg = bkb(MOM_B)
    cam = Cam()
    cam.push(t0, t1, tg, 4.6, 3.7, yaw=180, pitch=0, lens=34, fstop=1.6)
    cam.handheld(0.3)
    sfx(to - 0.3, "rise", 0.7)
    sfx(to, "sparkle", 0.7)


@S(71, 254, 261, "For the first time in a year: slow heroic push, sun behind")
def s71(t0, t1):
    beach(t0, t1, crowd_n=40)
    m = mom_c(t0, t1, "gasp", "wide", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    m.back.key(t0 + 0.9, "normal")
    light("god", "SPOT", (MOM_B[0], MOM_B[1] + 8, 14), 6000, (1.0, 0.95, 0.75), 1.0, target=bkb(MOM_B), spot=25)
    tg = bkb(MOM_B)
    cam = Cam()
    cam.push(t0, t1, tg, 5.6, 4.0, yaw=165, yaw1=180, pitch=4, lens=30, fstop=2)
    cam.handheld(0.3)


@S(72, 261, 266, "They squinted in the sun")
def s72(t0, t1):
    beach(t0, t1, crowd_n=20)
    m = mom_c(t0, t1, "gasp", "normal", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    m.back.key(w(262), "squint")
    tg = bkb(MOM_B)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.7, yaw=195, pitch=-6, lens=34, fstop=1.6)
    cam.handheld(0.4)


@S(73, 266, 267, "Blinked")
def s73(t0, t1):
    beach(t0, t1, crowd_n=20)
    m = mom_c(t0, t1, "gasp", "squint", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    m.back.snap(t0 + 0.08, "normal")
    tg = bkb(MOM_B)
    cam = Cam()
    cam.push(t0, t1, tg, 4.0, 3.6, yaw=170, pitch=0, lens=34, fstop=1.6)
    cam.handheld(0.5)


@S(74, 267, 269, "Looked left")
def s74(t0, t1):
    beach(t0, t1, crowd_n=20)
    m = mom_c(t0, t1, "gasp", "normal", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    m.back.key(w(268), "side_l")
    tg = bkb(MOM_B)
    cam = Cam()
    cam.key(t0, orbit_pos(tg, 3.9, 175, 0), tg, lens=34, focus=tg, fstop=1.6)
    cam.key(t1, orbit_pos(tg, 3.9, 195, 0), tg, lens=34, focus=tg, fstop=1.6)
    cam.handheld(0.5)
    sfx(w(268), "whoosh", 0.4)


@S(75, 269, 270, "Right")
def s75(t0, t1):
    beach(t0, t1, crowd_n=20)
    m = mom_c(t0, t1, "gasp", "side_l", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    m.back.key(t0 + 0.05, "side_r")
    tg = bkb(MOM_B)
    cam = Cam()
    cam.key(t0, orbit_pos(tg, 3.9, 195, 0), tg, lens=34, focus=tg, fstop=1.6)
    cam.key(t1, orbit_pos(tg, 3.9, 165, 0), tg, lens=34, focus=tg, fstop=1.6)
    cam.handheld(0.5)
    sfx(t0 + 0.05, "whoosh", 0.4)


@S(76, 270, 274, "Then they locked onto: eyes narrow, focus, crash zoom")
def s76(t0, t1):
    beach(t0, t1, crowd_n=20)
    m = mom_c(t0, t1, "gasp", "side_r", blink=False)
    m.pose(t0, loc=MOM_B, rot=0)
    tl = w(272)
    m.back.key(tl, "angry")
    tg = bkb(MOM_B)
    cam = Cam()
    cam.push(t0, t1, tg, 4.4, 3.6, yaw=180, pitch=0, lens=34, fstop=1.6)
    cam.crash(tl, 34, 46, 0.08)
    cam.handheld(0.6)
    sfx(tl, "click", 0.8)
    sfx(tl + 0.02, "thud", 0.4)


@S(77, 274, 278, "One tiny yellow dot: POV over the sea, crash zoom to the speck")
def s77(t0, t1):
    beach(t0, t1, crowd_n=60, stand=False)
    dk, si = duck_sis(t0, t1, DOT, (DOT[0] + 0.5, DOT[1] + 1, 0))
    p = bkb(MOM_B)
    cam = Cam()
    cam.key(t0, p, (DOT[0], DOT[1], 1.0), lens=24, focus=150, fstop=16)
    cam.key(w(275), p, (DOT[0], DOT[1], 1.0), lens=30, focus=150, fstop=16)
    cam.key(t1, p, (DOT[0], DOT[1], 1.5), lens=180, focus=160, fstop=16, ease="EASE_OUT")
    cam.handheld(0.15)
    sfx(w(275), "rise", 0.6)
    sfx(w(276), "ding", 0.6)


@S(78, 278, 283, "Far out on the waves: duck bobbing, sister waving")
def s78(t0, t1):
    sea_only(t0, t1)
    dk, si = duck_sis(t0, t1, DOT, (DOT[0] + 0.8, DOT[1] + 1.5, 0), expr="worried")
    noise(si.shR, "rotation_euler", 1, 0.7, 3)
    for k in range(3):
        foam(f"wd{k}", DOT[0] - 30, DOT[0] + 30, DOT[1] - 6 + k * 6, t0 - k * 0.5, t0 - k * 0.5 + 2.6, seed=20 + k, z=0.4)
    tg = (DOT[0], DOT[1], 1.8)
    cam = Cam()
    cam.orbit(t0, t1, tg, 7.5, 20, -20, pitch=8, lens=30, fstop=2.4)
    cam.handheld(0.8)
    sfx(t0, "waves", 0.7)


@S(79, 283, 284, "There! Max points and shouts")
def s79(t0, t1):
    beach(t0, t1, crowd_n=40)
    k = kid_c(t0, t1, "shout")
    k.pose(t0, loc=RIP, rot=180)
    k.act(t0, "point", expr="shout")
    lips(k, t0, t1, "shout")
    tg = hd(RIP)
    cam = Cam()
    cam.push(t0, t1, tg, 4.0, 3.2, yaw=150, pitch=-4, lens=30, fstop=1.8)
    cam.crash(t0 + 0.04, 30, 40, 0.07)
    cam.handheld(1.2)


@S(80, 284, 289, "Mom didn't even turn around: she faces the stand, cone in hand, deadpan")
def s80(t0, t1):
    beach(t0, t1, crowd_n=40)
    m = mom_c(t0, t1, "determined", "angry")
    m.pose(t0, loc=MOM_B, rot=0)
    ic = ice_cream("ic80")
    locs.hand_prop(m, "R", ic, offset=(0, -0.3, -2.4))
    m.pose(t0, armR=(70, 0))
    tg = hd(MOM_B)
    cam = Cam()
    cam.push(t0, t1, tg, 5.0, 4.2, yaw=-78, yaw1=-62, pitch=4, lens=30, fstop=1.8)
    cam.handheld(0.4)


RUN0 = (MOM_B[0], MOM_B[1], 0)
RUN1 = (-6.0, SHORE - 1.0, 0)


@S(81, 289, 292, "She ran backwards: tracking, mom sprints back-first across the sand")
def s81(t0, t1):
    beach(t0, t1, crowd_n=60)
    m = mom_c(t0, t1, "determined", "angry")
    m.walk(t0, t1, RUN0, RUN1, rate=4.2, swing=55, arm=65, bob=0.35, face_dir=False)
    m.pose(t0, rot=-15); m.pose(t1, rot=-15)
    cam = Cam()
    cam.track(m, t0, t1, offset=(7.0, 2.0, 2.2), look_up=4.0, lens=24, step=0.2, fstop=4)
    cam.handheld(1.2)
    sfx(t0, "footsteps", 0.6)
    sfx(t0 + 0.05, "whoosh", 0.6)


@S(82, 292, 295, "Into the ocean: back-first splash")
def s82(t0, t1):
    beach(t0, t1, crowd_n=30, stand=False)
    m = mom_c(t0, t1, "determined", "angry")
    p0, p1 = (-6, SHORE - 3, 0), (-6, SHORE + 5, -1.6)
    m.walk(t0, t1, p0, p1, rate=4.2, swing=55, arm=65, bob=0.3, face_dir=False)
    m.pose(t0, rot=0)
    ts = w(293)
    W2.poof("spl82", (-6, SHORE + 1, 0.3), ts, s=2.0, seed=82)
    W2.poof("spl82b", (-6, SHORE + 4, 0.3), ts + 0.4, s=2.4, seed=83)
    cam = Cam()
    cam.key(t0, (4, SHORE - 6, 2.0), (-6, SHORE + 0, 3.0), lens=24, focus=10, fstop=4)
    cam.key(t1, (2, SHORE - 3, 1.6), (-6, SHORE + 5, 2.0), lens=26, focus=9, fstop=4)
    cam.handheld(1.4)
    sfx(ts, "splash", 0.9)
    sfx(ts + 0.4, "splash", 0.7)


@S(83, 295, 299, "Faster than any lifeguard: lifeguard on the tower, jaw drops as she rockets past")
def s83(t0, t1):
    beach(t0, t1, crowd_n=30, stand=False)
    lg = adult(4, t0, t1, "gasp", extras=())
    lg.pose(t0, loc=(TOWER[0], TOWER[1], 6.25), rot=-160)
    lg.act(t0 + 0.4, "shock", expr="shock")
    lg.look(t0 + 0.3, 45, 0)
    m = mom_c(t0, t1, "determined", "angry")
    m.pose(t0, loc=(TOWER[0] - 30, SHORE + 8, -2.4), rot=90)
    m.pose(t1, loc=(TOWER[0] + 40, SHORE + 12, -2.4))
    set_interp(m.root, "location", F(t0), "LINEAR")
    for i in range(10):
        wk = sphere(f"wake{i}", 0.9, (TOWER[0] - 30 + i * 7, SHORE + 8 + i * 0.4, 0.2), mat("foam", (0.97, 0.98, 1.0), 0.6, emit=(0.6, 0.7, 0.8), estr=0.25), (2.5, 1, 0.3), seg=10)
    tg = (TOWER[0], TOWER[1], 10.5)
    cam = Cam()
    cam.push(t0, t1, tg, 10, 8.5, yaw=200, yaw1=215, pitch=-4, lens=26, fstop=3)
    cam.handheld(0.6)
    sfx(t0 + 0.3, "jet", 0.6)
    sfx(t0 + 0.4, "gasp", 0.3)


SWIM_P = (DOT[0], DOT[1] - 14, -2.4)


@S(84, 299, 305, "Swam straight to the duck: backstroke with a huge wake, duck ahead")
def s84(t0, t1):
    sea_only(t0, t1)
    dk, si = duck_sis(t0, t1, DOT, (DOT[0], DOT[1] + 0.6, 0), expr="worried")
    m = mom_c(t0, t1, "determined", "angry")
    m.root.rotation_euler[0] = math.radians(-80)
    m.root.keyframe_insert("rotation_euler", index=0, frame=F(t0))
    p0 = (DOT[0], DOT[1] - 30, 0.0)
    p1 = (DOT[0], DOT[1] - 6, 0.0)
    m.pose(t0, loc=p0, rot=0)
    m.pose(t1, loc=p1)
    set_interp(m.root, "location", F(t0), "LINEAR")
    t, kk = t0, 0
    while t < t1:
        s = 1 if kk % 2 == 0 else -1
        m.pose(t, armL=(180 * (kk % 2), 10), armR=(180 * ((kk + 1) % 2), 10), legL=(20 * s, 0), legR=(-20 * s, 0))
        t += 0.18; kk += 1
    for i in range(14):
        wk = sphere(f"wk{i}", 0.8, (DOT[0] + (i % 2 - 0.5) * 2, DOT[1] - 30 + i * 1.8, 0.2),
                    mat("foam", (0.97, 0.98, 1.0), 0.6, emit=(0.6, 0.7, 0.8), estr=0.25), (1.4, 2.0, 0.35), seg=10)
    cam = Cam()
    cam.track(m, t0, t1, offset=(-6.0, -8.0, 4.5), look_up=0.5, lens=24, step=0.25, fstop=5)
    cam.handheld(1.0)
    sfx(t0, "splash", 0.5)
    sfx(t0 + 0.6, "whoosh", 0.5)


@S(85, 305, 306, "SPLASH! at the duck, crash zoom")
def s85(t0, t1):
    sea_only(t0, t1)
    dk, si = duck_sis(t0, t1, DOT, (DOT[0], DOT[1], 0), expr="gasp")
    W2.poof("spl85", (DOT[0], DOT[1] - 2.5, 0.6), t0 + 0.04, s=1.5, seed=85)
    tg = (DOT[0], DOT[1] - 1, 1.8)
    cam = Cam()
    cam.push(t0, t1, tg, 14, 12, yaw=-25, pitch=10, lens=26, fstop=4)
    cam.crash(t0 + 0.04, 26, 34, 0.07)
    cam.shake(0.03, 2)
    sfx(t0 + 0.04, "splash", 1.0)


@S(86, 306, 311, "Brought my sister back: walks out of the surf carrying her, crowd cheers")
def s86(t0, t1):
    beach(t0, t1, crowd_n=120)
    m = mom_c(t0, t1, "grin", "happy")
    p = (-4, SHORE - 3, 0)
    m.walk(t0, t1, (-4, SHORE + 2, -0.6), p, rate=1.8, swing=22, arm=0)
    m.pose(t0, armL=(80, -10), armR=(80, -10))
    si = sis_c(t0, t1, "joy")
    si.root.parent = m.hip
    si.root.location = (0, -1.1, 0.6)
    si.pose(t0, armL=(160, 30), armR=(160, 30))
    srcc = crowd_src("CHEER", t0, t1, [41, 42, 43], mode="cheer", spread=3)
    for i, x in enumerate((-16, -9, 4, 10)):
        instance(f"chr{i}", srcc, (x, SHORE - 12 - (i % 2) * 3, 0), rot=(0, 0, 180 + (i * 37) % 60 - 30))
    tg = (-4, SHORE - 3, 4.0)
    cam = Cam()
    cam.push(t0, t1, tg, 13, 10, yaw=-20, yaw1=-5, pitch=4, lens=24, fstop=4)
    cam.handheld(0.6)
    sfx(t0 + 0.2, "cheer", 0.7)
    sfx(t0 + 0.2, "crowd", 0.4)


@S(87, 311, 312, "Safe: group hug, sparkles")
def s87(t0, t1):
    beach(t0, t1, crowd_n=40)
    p = (-4, SHORE - 4, 0)
    m = mom_c(t0, t1, "relief", "happy")
    m.pose(t0, loc=p, rot=0, armL=(90, -35), armR=(90, -35))
    si = sis_c(t0, t1, "joy")
    si.pose(t0, loc=(p[0], p[1] - 1.2, 1.6), rot=180, armL=(90, -30), armR=(90, -30))
    k = kid_c(t0, t1, "relief")
    k.pose(t0, loc=(p[0] + 1.8, p[1] - 1.6, 0), rot=150, armL=(90, -30), armR=(90, -30))
    sparkle_on("sp87", up(p, 6.5), t0 + 0.05, 1.0, 12, seed=87)
    tg = (p[0] + 0.6, p[1] - 0.8, 4.4)
    cam = Cam()
    cam.push(t0, t1, tg, 7.0, 6.0, yaw=-15, yaw1=-5, pitch=6, lens=28, fstop=2.4)
    cam.handheld(0.3)
    sfx(t0 + 0.05, "aww", 0.6)


# ================================================================== PAYOFF
TRASH = (6.0, -2.0, 0)


@S(88, 312, 321, "That night: Max tosses the beanie into the trash, lid slams")
def s88(t0, t1):
    kitchen(night=True)
    can = empty("can", TRASH)
    cyl("can_b", 1.0, 2.6, (0, 0, 1.3), M("#7a8a9a", 0.3, metal=0.6), 24, parent=can)
    lid = empty("can_lidp", (0, 0.95, 2.6), parent=can)
    cyl("can_lid", 1.06, 0.2, (0, -0.95, 0.1), M("#8a9aaa", 0.3, metal=0.6), 24, parent=lid)
    lid.rotation_euler = (math.radians(-100), 0, 0)
    tt = w(319)
    lid.keyframe_insert("rotation_euler", frame=F(tt + 0.25))
    lid.rotation_euler = (0, 0, 0)
    lid.keyframe_insert("rotation_euler", frame=F(tt + 0.4))
    kp = (2.6, -3.4, 0)
    k = kid_c(t0, t1, "smug")
    k.pose(t0, loc=kp, rot=facing(kp, TRASH))
    k.act(tt - 0.5, "point", expr="smug")
    bn = beanie_obj("btoss")
    bn.location = (kp[0] + 0.8, kp[1] - 0.5, 5.5)
    bn.keyframe_insert("location", frame=F(tt - 0.4)); bn.keyframe_insert("rotation_euler", frame=F(tt - 0.4))
    bn.location = (4.6, -2.6, 7.0)
    bn.keyframe_insert("location", frame=F(tt - 0.1))
    bn.location = (TRASH[0], TRASH[1], 2.0)
    bn.rotation_euler = (math.radians(200), math.radians(60), 0)
    bn.keyframe_insert("location", frame=F(tt + 0.15)); bn.keyframe_insert("rotation_euler", frame=F(tt + 0.15))
    tg = (4.4, -2.8, 3.6)
    cam = Cam()
    cam.push(t0, t1, tg, 12, 10, yaw=-35, yaw1=-20, pitch=14, lens=26, fstop=3)
    cam.handheld(0.5)
    sfx(tt - 0.4, "whoosh", 0.6)
    sfx(tt + 0.4, "thud", 0.7)


MOM_N = (-1.0, -1.0, 0)
KID_N = (2.6, -3.4, 0)


@S(89, 321, 325, "Keep them open, Mom: Max to mom")
def s89(t0, t1):
    kitchen(night=True)
    m = mom_c(t0, t1, "gasp", "wide")
    m.pose(t0, loc=MOM_N, rot=facing(MOM_N, KID_N))
    k = kid_c(t0, t1, "smile")
    k.pose(t0, loc=KID_N, rot=facing(KID_N, MOM_N))
    lips(k, t0, t1)
    k.act(t0 + 0.1, "point", expr="smile")
    tg = up(hd(KID_N), -0.2)
    cam = Cam()
    cam.push(t0, t1, tg, 5, 4, yaw=facing(KID_N, MOM_N) - 30, yaw1=facing(KID_N, MOM_N) - 15, pitch=2, lens=30, fstop=2)
    cam.handheld(0.4)


@S(90, 325, 326, "Forever: Max grins")
def s90(t0, t1):
    kitchen(night=True)
    k = kid_c(t0, t1, "grin")
    k.pose(t0, loc=KID_N, rot=facing(KID_N, MOM_N))
    lips(k, t0, t1)
    tg = hd(KID_N)
    yk = facing(KID_N, MOM_N)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.6, yaw=yk - 10, pitch=-2, lens=30, fstop=1.6)
    cam.handheld(0.4)
    sfx(t0 + 0.05, "sparkle", 0.4)


@S(91, 326, 332, "All four eyes cried: happy tears, orbit front to back")
def s91(t0, t1):
    kitchen(night=True)
    m = mom_c(t0, t1, "cry", "cry", blink=False)
    m.pose(t0, loc=MOM_N, rot=facing(MOM_N, KID_N))
    m.face(t0 + 0.6, eyes="cry", mouth="smile")
    tears("tf91", m, t0 + 0.1, t1)
    tears("tb91", m, t0 + 0.1, t1, back=True)
    ym = facing(MOM_N, KID_N)
    tg = up(hd(MOM_N), 0.1)
    cam = Cam()
    cam.orbit(t0, t1, tg, 3.4, ym - 10, ym + 175, pitch=4, lens=30, steps=6, fstop=1.8)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "aww", 0.7)


@S(92, 332, 335, "The next morning: sunny kitchen, crane down")
def s92(t0, t1):
    kitchen()
    light("sunbeam", "SPOT", (-5, 9, 12), 5000, (1.0, 0.9, 0.7), 1.0, target=(-2, 0, 0), spot=40)
    m = kit_mom(t0, t1, "smile", "normal")
    cam = Cam()
    cam.key(t0, (6, -14, 12), (-1, 3, 4), lens=24, focus=17, fstop=6)
    cam.key(t1, (5, -12, 7), (-1, 3, 4), lens=24, focus=15, fstop=6)
    cam.handheld(0.4)
    sfx(t0, "pigeon", 0.3)


@S(93, 335, 340, "I reached for a cookie: Max's hand dips into the jar")
def s93(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "closed", loc=(-1.0, 3.5, 0))
    kp = (5.0, 3.1, 0)
    k = kid_c(t0, t1, "smug")
    k.pose(t0, loc=kp, rot=180)
    cookie_jar(JAR, lid_t=t0 + 0.2) if False else None
    k.act(t0 + 0.3, "reach", expr="smug")
    k.pose(t1, armR=(130, 0))
    tg = (JAR[0], JAR[1] - 1.0, CTOP + 1.8)
    cam = Cam()
    cam.push(t0, t1, tg, 6.0, 4.8, yaw=78, yaw1=62, pitch=10, lens=30, fstop=2)
    cam.handheld(0.4)


@S(94, 340, 341, "BLINK (again)")
def s94(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "smile", "closed", loc=(-1.0, 3.5, 0))
    m.back.key(t0 + 0.05, "happy")
    sfx(t0 + 0.05, "blink", 1.0)
    tg = bk((-1.0, 3.5, 0))
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.7, yaw=-15, pitch=2, lens=32, fstop=1.6)
    cam.crash(t0 + 0.05, 32, 42, 0.07)
    cam.handheld(0.9)


@S(95, 341, 344, "Put it back: mom points back, smiling, Max laughs")
def s95(t0, t1):
    kitchen()
    m = kit_mom(t0, t1, "grin", "happy", loc=(-1.0, 3.5, 0))
    point_back(m, t0, "L")
    k = kid_c(t0, t1, "joy")
    kp = (5.0, 3.1, 0)
    k.pose(t0, loc=kp, rot=200)
    tg = (2.0, 3.0, 4.2)
    cam = Cam()
    cam.push(t0, t1, tg, 10, 8.5, yaw=-5, yaw1=8, pitch=4, lens=26, fstop=4)
    cam.handheld(0.5)


@S(96, 344, 347, "Totally worth it: Max grins at the camera, wink")
def s96(t0, t1):
    kitchen()
    kp = (5.0, 2.0, 0)
    k = kid_c(t0, t1, "grin")
    k.pose(t0, loc=kp, rot=-10)
    k.face(t0 + 0.4, "wink")
    k.act(t0 + 0.2, "point", expr="grin")
    tg = hd(kp)
    cam = Cam()
    cam.push(t0, t1, tg, 4.2, 3.2, yaw=-10, yaw1=0, pitch=-2, lens=30, fstop=1.8)
    cam.handheld(0.4)
    sfx(t0 + 0.4, "sparkle", 0.4)


DAD_SEAT = (0, 6.2, 2.2)


@S(97, 347, 352, "But then I found out: record scratch, Max freezes")
def s97(t0, t1):
    L = W.tv_room()
    kp = (6.0, 1.0, 0)
    k = kid_c(t0, t1, "gasp")
    k.pose(t0, loc=kp, rot=facing(kp, DAD_SEAT))
    k.act(t0 + 0.05, "recoil", expr="gasp")
    tg = hd(kp)
    cam = Cam()
    cam.push(t0, t1, tg, 4.0, 3.2, yaw=facing(kp, DAD_SEAT) - 20, pitch=0, lens=30, fstop=1.8)
    cam.crash(t0 + 0.05, 30, 40, 0.07)
    cam.handheld(0.8)
    sfx(t0 + 0.02, "scratch", 0.8)


@S(98, 352, 356, "Dads have one eye: dad on the couch, from behind, one big eye on the back of his head")
def s98(t0, t1):
    L = W.tv_room()
    no_back_wall()
    d = dad_c(t0, t1)
    sit_on(d, t0, DAD_SEAT, rot=0)
    d.pose(t0, armL=(40, -20), armR=(40, -20))
    tg = bkb((0, 6.2, 0.24))
    cam = Cam()
    cam.push(t0, t1, tg, 3.6, 3.0, yaw=160, yaw1=180, pitch=14, lens=28, fstop=2)
    light("backfill", "AREA", (0, 9.6, 7.5), 900, (1.0, 0.95, 0.9), 3, target=tg)
    cam.handheld(0.3)
    sfx(t0 + 0.1, "rise", 0.3)


@S(99, 356, 363, "On the back of their head too: ECU on the single eye, it twitches")
def s99(t0, t1):
    L = W.tv_room()
    no_back_wall()
    d = dad_c(t0, t1)
    sit_on(d, t0, DAD_SEAT, rot=0)
    tg = bkb((0, 6.2, 0.24))
    d.back.key(w(360), "half")
    d.back.key(w(360) + 0.25, "closed")
    cam = Cam()
    cam.push(t0, t1, tg, 3.4, 2.9, yaw=180, pitch=8, lens=32, fstop=1.6)
    light("backfill", "AREA", (0, 9.6, 7.5), 900, (1.0, 0.95, 0.9), 3, target=tg)
    cam.handheld(0.3)


@S(100, 363, None, "It's just always asleep: snore, Z's float up, pull out")
def s100(t0, t1):
    L = W.tv_room()
    no_back_wall()
    d = dad_c(t0, t1)
    sit_on(d, t0, DAD_SEAT, rot=0)
    tg = bkb((0, 6.2, 0.24))
    zzz("zz", (tg[0] + 0.4, tg[1] + 0.6, tg[2] + 0.4), t0 + 0.05, t1, s=0.7)
    noise(d.hip, "location", 2, 0.05, 20)
    cam = Cam()
    cam.push(t0, t1, tg, 3.0, 4.2, yaw=180, yaw1=170, pitch=10, lens=30, fstop=2)
    light("backfill", "AREA", (0, 9.6, 7.5), 900, (1.0, 0.95, 0.9), 3, target=tg)
    cam.handheld(0.3)
    sfx(t0 + 0.05, "snore", 0.9)
