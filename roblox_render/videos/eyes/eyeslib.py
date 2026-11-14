"""Shared sets, props and cast for the 'back eyes' story (runs inside Blender)."""
import math, os, random
import bpy
import rbx
from mathutils import Vector
from shotkit import *          # noqa
from rbx import story
from rbx.story import *        # noqa
from rbx.sets import wood, planks
from rbx.acting import EYE

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "fonts", "TitanOne-Regular.ttf")
CTOP = 3.2
MUG = (-9.0, 5.8, CTOP)
TABLE_Z = 2.8
DOOR_X = 14.0
CAR = (0.0, 2.0, 0.0)
HINGE = (-4.1, -1.75, 0.0)
GAP_Z = 5.45
HANDLE = (-1.0, -1.9, 3.25)
BUTTON = (-1.4, -1.35, 3.45)
KEYS = (-1.2, 1.4, 3.2)
SEAT = (-1.6, 0.4, 3.1)

def M(c, r=0.5, **kw):
    return mat("m" + c + str(r), hexc(c), r, **kw)


def emitm(c, s=3.0):
    return mat("e" + c + str(s), hexc(c), 0.4, emit=hexc(c), estr=s)


def head(p, s=1.0):
    return (p[0], p[1], p[2] + 4.6 * s)


def sit_on(ch, t, seat_top, rot=0, s=1.0, **kw):
    x, y, z = seat_top
    ch.pose(t, loc=(x, y, z - 1.96 * s), rot=rot, legL=(85, 3), legR=(85, -3), armL=(30, 6), armR=(30, 6), **kw)


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


def pop_text(name, body, loc, t, size=1.0, col="#ffe14a", yaw=0, dur=None, outline="#1a1a22"):
    root = empty(name, loc, rot=(0, 0, yaw))
    text(name + "_t", body, (0, 0, 0), size, emitm(col, 2.5), extrude=0.08 * size, parent=root, font=FONT)
    text(name + "_o", body, (0.04 * size, 0.06 * size, -0.04 * size), size, M(outline, 0.6), extrude=0.06 * size, parent=root, font=FONT)
    root.scale = (0.01,) * 3; root.keyframe_insert("scale", frame=F(t - 0.04))
    root.scale = (1.25,) * 3; root.keyframe_insert("scale", frame=F(t + 0.08))
    root.scale = (1.0,) * 3; root.keyframe_insert("scale", frame=F(t + 0.16))
    if dur:
        root.keyframe_insert("scale", frame=F(t + dur - 0.1))
        root.scale = (0.01,) * 3; root.keyframe_insert("scale", frame=F(t + dur))
    noise(root, "rotation_euler", 1, 0.04, 8)
    return root


def mug_big(loc, coll=None, col="#e8423a"):
    root = empty("mugb", loc, coll=coll)
    cyl("mug_b", 0.75, 1.7, (0, 0, 0.85), M(col, 0.3), 24, parent=root, coll=coll)
    cyl("mug_c", 0.66, 0.05, (0, 0, 1.68), M("#4a2a16", 0.2), 24, parent=root, coll=coll)
    box("mug_h", (0.2, 0.25, 1.0), (0.85, 0, 0.9), M(col, 0.3), 0.1, parent=root, coll=coll)
    text("mug_t", "#1 DAD", (0, -0.78, 0.9), 0.3, M("#ffffff", 0.5), extrude=0.01, parent=root, coll=coll)
    return root


def keys_prop(name, loc, coll=None, s=1.0, rot=0):
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    Mk = M("#d8d8de", 0.2, metal=0.95)
    cyl(name + "_ring", 0.22, 0.04, (0, 0, 0.03), Mk, 18, parent=root, coll=coll)
    box(name + "_k1", (0.12, 0.7, 0.04), (0.08, -0.5, 0.03), Mk, 0.02, parent=root, coll=coll, rot=(0, 0, 18))
    box(name + "_k1h", (0.34, 0.3, 0.05), (0.0, -0.18, 0.03), M("#222226", 0.4), 0.06, parent=root, coll=coll)
    box(name + "_k2", (0.12, 0.6, 0.04), (-0.25, -0.35, 0.03), M("#e2b23a", 0.2, metal=0.9), 0.02, parent=root, coll=coll,
        rot=(0, 0, -35))
    return root


def day(strength=4.0, rot=(50, 0, 32)):
    W.sky(1.0)
    W.sun(strength, rot=rot)


def kitchen(night=False, door=False, table=None):
    if night:
        world((0.12, 0.15, 0.3), 0.6)
    else:
        world((0.9, 0.93, 1.0), 0.45)
    c = collection("KITCH")
    box("k_floor", (60, 50, 0.4), (0, 0, -0.2), sets.checker_mat("k_fl", "#f2ece0", "#d8cdb8", 0.18), 0, coll=c)
    box("k_back", (60, 0.5, 16), (0, 8.25, 8), M("#bfe0d0" if not night else "#7a8fa0", 0.85), 0, coll=c)
    box("k_left", (0.5, 50, 16), (-16, 0, 8), M("#b0d4c4" if not night else "#6a7d8e", 0.85), 0, coll=c)
    Mc = wood("k_cab", "#e8e2d4", "#f4efe4", 2.0)
    box("k_counter", (20, 3.2, CTOP - 0.2), (0, 6.5, (CTOP - 0.2) / 2), M("#4f86c6", 0.6), 0.06, coll=c)
    box("k_top", (20.4, 3.5, 0.2), (0, 6.4, CTOP - 0.1), M("#f4f1ea", 0.25), 0.04, coll=c)
    for i in range(5):
        box(f"k_door{i}", (3.4, 0.08, 2.2), (-8 + i * 4, 4.86, 1.6), M("#5f96d6", 0.55), 0.06, coll=c)
        sphere(f"k_knob{i}", 0.12, (-8 + i * 4 + 1.2, 4.8, 2.3), M("#e2b23a", 0.3, metal=0.8), coll=c, seg=8)
    for i in range(4):
        box(f"k_up{i}", (3.6, 1.6, 3.0), (-6 + i * 4, 7.4, 10.0), Mc, 0.08, coll=c)
    # sink + faucet
    box("k_sink", (3.4, 2.2, 0.15), (-5, 6.2, CTOP + 0.02), M("#b8bcc4", 0.2, metal=0.8), 0.05, coll=c)
    cyl("k_fau", 0.14, 1.6, (-5, 7.3, CTOP + 0.8), M("#c8ccd4", 0.15, metal=0.9), 10, coll=c)
    box("k_spout", (0.24, 1.1, 0.24), (-5, 6.85, CTOP + 1.55), M("#c8ccd4", 0.15, metal=0.9), 0.08, coll=c)
    # window over the sink
    box("k_wfr", (5.0, 0.3, 4.0), (-5, 8.0, 7.0), M("#f4f4f4"), 0.04, coll=c)
    card("k_wsky", 4.4, 3.4, (-5, 7.85, 7.0), emitm("#bfe3ff" if not night else "#1a2a5a", 2.5 if not night else 1.0),
         "-Y", coll=c)
    # fridge
    box("k_fridge", (4, 3.6, 9), (-12.5, 6.2, 4.5), M("#e8eef4", 0.25, metal=0.3), 0.15, coll=c)
    box("k_fh", (0.25, 0.3, 2.4), (-11.0, 4.3, 5.5), M("#c8ccd4", 0.2, metal=0.8), 0.06, coll=c)
    cookie_jar(JAR, c)
    if table if table is not None else night:
        Mt = wood("k_tab", "#a0703f", "#c89260", 2.0)
        box("k_table", (8, 5, 0.3), (1, -5, TABLE_Z - 0.15), Mt, 0.06, coll=c)
        for sx in (-1, 1):
            for sy in (-1, 1):
                box(f"k_tl{sx}{sy}", (0.35, 0.35, TABLE_Z - 0.3), (1 + sx * 3.5, -5 + sy * 2.1, (TABLE_Z - 0.3) / 2),
                    M("#704a2a"), 0.02, coll=c)
    if door:
        Mw = M("#bfe0d0" if not night else "#7a8fa0", 0.85)
        box("k_dw1", (6, 0.5, 16), (DOOR_X - 4.6, -3, 8), Mw, 0, coll=c)
        box("k_dw2", (6, 0.5, 16), (DOOR_X + 4.6, -3, 8), Mw, 0, coll=c)
        box("k_dw3", (3.2, 0.5, 9.6), (DOOR_X, -3, 6.2 + 4.8), Mw, 0, coll=c)
        Mf = M("#f4f4f4", 0.5)
        for sx in (-1, 1):
            box(f"k_df{sx}", (0.3, 0.7, 6.2), (DOOR_X + sx * 1.6, -3, 3.1), Mf, 0.04, coll=c)
        box("k_dft", (3.5, 0.7, 0.3), (DOOR_X, -3, 6.2), Mf, 0.04, coll=c)
        box("k_hall", (6, 0.5, 8), (DOOR_X, 3, 4), M("#e8d8b8", 0.85), 0, coll=c)
    if night:
        cyl("k_pend", 0.05, 4, (1, -5, 11), M("#2a2a2a"), 6, coll=c)
        sphere("k_shade", 1.0, (1, -5, 8.6), emitm("#ffd890", 3.0), (1, 1, 0.5), coll=c, seg=16)
        light("k_lamp", "POINT", (1, -5, 7.8), 6000, (1.0, 0.82, 0.55), 2.0, coll=c)
        light("k_fill", "AREA", (0, -16, 10), 2500, (0.6, 0.7, 1.0), 14, coll=c, target=(0, 0, 3))
        light("k_fill2", "AREA", (9, -15, 10), 3500, (1.0, 0.85, 0.7), 10, coll=c, target=(9, -5, 3))
    else:
        light("k_key", "AREA", (0, -6, 13), 5000, (1.0, 0.97, 0.92), 12, coll=c, target=(0, 4, 2))
        light("k_fill", "AREA", (-10, -4, 6), 1500, (0.9, 0.95, 1.0), 6, coll=c, target=(0, 4, 3))
    return c


def car_set(open_t=None, pane_up=None, door_open=False):
    """Family car on the driveway. The driver door is a hinged root with the window, handle and unlock button."""
    c = collection("CAR")
    root = empty("car", CAR, coll=c)
    Mb = M("#3fa7d9", 0.25, metal=0.35)
    Mg = mat("carglass", hexc("#9fd0ee"), 0.05, metal=0.2, alpha=0.28)
    Mi = M("#3a3a44", 0.8)
    x0, y0 = CAR[0], CAR[1]
    box("car_body_f", (4.0, 7.5, 2.6), (x0 - 6.0, y0, 2.3), Mb, 0.5, coll=c)
    box("car_body_r", (7.6, 7.5, 2.6), (x0 + 4.2, y0, 2.3), Mb, 0.5, coll=c)
    box("car_floor", (16, 7.3, 0.4), (x0, y0, 1.2), Mi, 0.05, coll=c)
    box("car_pside", (16, 0.3, 2.6), (x0, y0 + 3.6, 2.3), Mb, 0.1, coll=c)
    box("car_roof", (9.2, 7.3, 0.35), (x0 + 0.5, y0, 6.1), Mb, 0.15, coll=c)
    for x in (-4.0, 4.9):
        for sy in (-1, 1):
            box(f"car_pil{x}{sy}", (0.35, 0.35, 2.5), (x0 + x, y0 + sy * 3.55, 4.85), Mb, 0.05, coll=c)
    box("car_bpil", (0.4, 0.35, 2.5), (x0 + 0.5, y0 - 3.55, 4.85), Mb, 0.05, coll=c)
    box("car_wsh", (0.08, 7.0, 2.6), (x0 - 4.5, y0, 4.8), Mg, 0.02, coll=c, rot=(0, -28, 0))
    box("car_rear", (0.08, 7.0, 2.5), (x0 + 5.2, y0, 4.8), Mg, 0.02, coll=c, rot=(0, 20, 0))
    box("car_backwin", (4.0, 0.08, 2.3), (x0 + 2.7, y0 - 3.6, 4.85), Mg, 0.02, coll=c)
    box("car_pwin", (8.6, 0.08, 2.3), (x0 + 0.4, y0 + 3.6, 4.85), Mg, 0.02, coll=c)
    box("car_rdoor", (4.3, 0.3, 2.6), (x0 + 2.7, y0 - 3.6, 2.3), Mb, 0.1, coll=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(f"car_wh{sx}{sy}", 1.3, 0.8, (x0 + sx * 5.4, y0 + sy * 3.5, 1.3), M("#151515", 0.7), 22, rot=(90, 0, 0), coll=c)
            cyl(f"car_hub{sx}{sy}", 0.6, 0.85, (x0 + sx * 5.4, y0 + sy * 3.5, 1.3), M("#c8ccd4", 0.2, metal=0.9), 16,
                rot=(90, 0, 0), coll=c)
    for sy in (-1, 1):
        sphere(f"car_hl{sy}", 0.45, (x0 - 8.0, y0 + sy * 2.6, 2.8), emitm("#fff6d0", 1.5), (0.4, 1, 1), coll=c, seg=12)
        sphere(f"car_tl{sy}", 0.4, (x0 + 8.0, y0 + sy * 2.6, 2.8), emitm("#ff3a3a", 1.2), (0.4, 1, 1), coll=c, seg=12)
    # interior
    Ms = M("#5a4a3a", 0.8)
    for y, nm in ((y0 - 1.6, "d"), (y0 + 1.7, "p")):
        box(f"seat_{nm}", (2.6, 2.6, 0.8), (x0 - 1.6, y, 2.7), Ms, 0.25, coll=c)
        box(f"seatb_{nm}", (0.7, 2.6, 2.8), (x0 - 0.1, y, 3.9), Ms, 0.3, coll=c, rot=(0, 10, 0))
    box("seat_back", (2.6, 6.6, 0.8), (x0 + 3.2, y0, 2.7), Ms, 0.25, coll=c)
    box("dash", (1.4, 7.0, 1.2), (x0 - 3.7, y0, 3.9), M("#2a2a32", 0.6), 0.2, coll=c)
    cyl("wheel", 0.85, 0.15, (x0 - 2.9, y0 - 1.6, 4.5), M("#18181c", 0.5), 24, rot=(0, 65, 0), coll=c)
    pass
    light("car_in", "POINT", (x0 - 1.0, y0, 5.4), 1500, (1.0, 0.95, 0.85), 1.0, coll=c)
    # driver door on a hinge
    door = empty("ddoor", HINGE, coll=c)
    lx, ly = -HINGE[0], -HINGE[1]

    def dl(p):
        return (p[0] - HINGE[0], p[1] - HINGE[1], p[2] - HINGE[2])
    box("dd_panel", (4.4, 0.3, 2.6), dl((x0 - 1.85, y0 - 3.6, 2.3)), Mb, 0.1, parent=door, coll=c)
    box("dd_inner", (4.2, 0.3, 2.4), dl((x0 - 1.85, y0 - 3.3, 2.4)), M("#4a4a54", 0.8), 0.08, parent=door, coll=c)
    box("dd_arm", (2.4, 0.6, 0.3), dl((x0 - 1.6, y0 - 3.15, 3.25)), M("#3a3a44", 0.8), 0.1, parent=door, coll=c)
    btn = box("dd_btn", (0.6, 0.4, 0.22), dl(BUTTON), emitm("#ff3a3a", 1.5), 0.08, parent=door, coll=c)
    box("dd_handle", (1.0, 0.3, 0.28), dl(HANDLE), M("#d8d8de", 0.2, metal=0.9), 0.1, parent=door, coll=c)
    for z in (3.6, 6.0):
        box(f"dd_fr{z}", (4.4, 0.25, 0.22), dl((x0 - 1.85, y0 - 3.55, z)), Mb, 0.05, parent=door, coll=c)
    box("dd_frb", (0.22, 0.25, 2.4), dl((x0 + 0.3, y0 - 3.55, 4.8)), Mb, 0.05, parent=door, coll=c)
    pane = box("dd_glass", (4.1, 0.08, 1.85), dl((x0 - 1.85, y0 - 3.55, GAP_Z - 0.93)), Mg, 0.02, parent=door, coll=c)
    pin = cyl("dd_pin", 0.08, 0.45, dl((x0 + 0.0, y0 - 3.35, 3.75)), M("#c8ccd4", 0.3, metal=0.8), 8, parent=door, coll=c)
    if pane_up is not None:
        t0, t1 = pane_up
        z = pane.location[2]
        pane.location[2] = z - 1.6; pane.keyframe_insert("location", index=2, frame=F(t0))
        pane.location[2] = z; pane.keyframe_insert("location", index=2, frame=F(t1))
    if open_t is not None:
        door.rotation_euler = (0, 0, 0); door.keyframe_insert("rotation_euler", frame=F(open_t))
        door.rotation_euler = (0, 0, math.radians(-68)); door.keyframe_insert("rotation_euler", frame=F(open_t + 0.45))
        set_interp(door, "rotation_euler", F(open_t), "BEZIER", "EASE_OUT")
    if door_open:
        door.rotation_euler = (0, 0, math.radians(-68))
    return dict(coll=c, door=door, pane=pane, btn=btn, pin=pin)


# ================================================================== deferred blinks
PENDING = []
_orig_live = story._live


def _live_deferred(ch, t0, t1, expr="neutral", br=0.8):
    ch.face(t0, expr)
    PENDING.append(lambda: ch.blink(t0, t1))
    ch.breathe(br)
    return ch


story._live = _live_deferred


def SB(i, a, b, desc=""):
    """Shot decorator: like story.S, but blinks are keyed after the shot is built (so they never undo
    an expression change made later in the shot code)."""
    def deco(fn):
        def run(t0, t1):
            PENDING.clear()
            fn(t0, t1)
            for f in PENDING:
                f()
            PENDING.clear()
        story.S(i, a, b, desc)(run)
        return fn
    return deco


# ================================================================== layout
JAR = (5.0, 6.0, CTOP)            # cookie jar on the kitchen counter
MOM_K = (-5.0, 3.5, 0.0)          # mom at the sink, back to the room (rot 180)
KID_K = (6.0, -6.0, 0.0)
FH = 4.62


def hd(p, s=1.0):
    return (p[0], p[1], p[2] + FH * s)


def bk(p, s=1.0, d=0.0):
    """Point at the back-eyes of a character facing +Y (rot 180) at p: back of the head is on -Y."""
    return (p[0], p[1] - 0.6 * s - d, p[2] + (FH + 0.1) * s)


# ================================================================== back eyes
def _eyes_shell_mat(name, atlas):
    m = D.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; N, L = nt.nodes, nt.links
    out = next(n for n in N if n.type == "OUTPUT_MATERIAL")
    b = next(n for n in N if n.type == "BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value = 0.45
    tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ")
    L.new(tc.outputs["Object"], sep.inputs[0])

    def Mx(op, a, bv=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        (L.new(a, n.inputs[0]) if not isinstance(a, float) else setattr(n.inputs[0], "default_value", a))
        if bv is not None:
            (L.new(bv, n.inputs[1]) if not isinstance(bv, float) else setattr(n.inputs[1], "default_value", bv))
        return n.outputs[0]
    import rbx.chars as C
    u = Mx("ADD", Mx("DIVIDE", sep.outputs["X"], -C.FACE_W), 0.5)          # mirrored: reads right from behind
    v = Mx("ADD", Mx("DIVIDE", Mx("SUBTRACT", sep.outputs["Z"], C.FACE_Z), C.FACE_H), 0.5)
    mask = Mx("MULTIPLY", Mx("MULTIPLY", Mx("MULTIPLY", Mx("GREATER_THAN", u, 0.0), Mx("LESS_THAN", u, 1.0)),
                                Mx("MULTIPLY", Mx("GREATER_THAN", v, 0.0), Mx("LESS_THAN", v, 1.0))),
              Mx("GREATER_THAN", sep.outputs["Y"], 0.05))
    cmb = N.new("ShaderNodeCombineXYZ"); L.new(u, cmb.inputs[0]); L.new(v, cmb.inputs[1])
    mp = N.new("ShaderNodeMapping"); mp.name = "BackMap"; mp.vector_type = "POINT"
    mp.inputs["Scale"].default_value = (0.25, 0.25, 1)
    mp.inputs["Location"].default_value = (0.0, 0.75, 0)
    L.new(cmb.outputs[0], mp.inputs[0])
    tx = N.new("ShaderNodeTexImage")
    tx.image = D.images.load(os.path.join(rbx.ASSETS, "faces", atlas + ".png"), check_existing=True)
    tx.extension = "CLIP"; tx.interpolation = "Cubic"
    L.new(mp.outputs[0], tx.inputs[0])
    L.new(tx.outputs["Color"], b.inputs["Base Color"])
    a = Mx("MULTIPLY", tx.outputs["Alpha"], mask)
    tr = N.new("ShaderNodeBsdfTransparent")
    mix = N.new("ShaderNodeMixShader")
    L.new(a, mix.inputs[0]); L.new(tr.outputs[0], mix.inputs[1]); L.new(b.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], out.inputs["Surface"])
    try:
        m.surface_render_method = "DITHERED"
    except Exception:
        pass
    m.diffuse_color = (1, 1, 1, 0)
    return m


class BackEyes:
    def __init__(self, ch, atlas="girl_eyes", expr="normal"):
        import rbx.chars as C
        self.ch = ch
        self.mat = _eyes_shell_mat(ch.name + "_backeyes", atlas)
        self.ob = cyl(ch.name + "_bshell", C.HEAD_R * 1.012, C.HEAD_H * 1.004, (0, 0, 0), self.mat, 40, bev=0.26,
                      parent=ch.head, coll=ch.coll, seg=5)
        try:
            self.ob.visible_shadow = False
        except Exception:
            pass
        self.track = []
        self.key(-10.0, expr)

    def key(self, t, eyes):
        idx = EYE[eyes] if isinstance(eyes, str) else eyes
        nt = self.mat.node_tree
        mp = nt.nodes["BackMap"]
        mp.inputs["Location"].default_value = ((idx % 4) * 0.25, (3 - idx // 4) * 0.25, 0)
        mp.inputs["Location"].keyframe_insert("default_value", frame=F(t))
        for fc in fcurves(nt.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
        self.track.append((t, idx))
        return self

    def cur(self, t):
        best = (-1e9, 0)
        for tt, e in self.track:
            if best[0] <= tt <= t:
                best = (tt, e)
        return best[1]

    def blink(self, t0, t1, every=(1.4, 2.8), seed=3):
        rnd = random.Random(seed)
        t = t0 + rnd.uniform(0.25, every[0])
        while t < t1 - 0.12:
            c = self.cur(t)
            near = [tt for tt, _ in self.track if t - 0.05 < tt < t + 0.18]
            if c not in (EYE["closed"], EYE["happy"]) and not near:
                self.key(t, "closed"); self.key(t + 0.1, c)
            t += rnd.uniform(*every)
        return self

    def snap(self, t, eyes, snd=True, vol=0.7):
        """Eyes close for 2 frames then pop to the new state (the 'Blink.' beat)."""
        self.key(t - 0.07, "closed")
        self.key(t, eyes)
        if snd:
            sfx(t, "blink", vol)
        return self


# ================================================================== cast
def kid_c(t0, t1, expr="neutral", dog=False, name="Kid", s=1.0):
    K = chars.Char(name, skin="#e8c39e", shirt="#ff8a3d" if not dog else "#b07a46", pants="#2f3f6a" if not dog else "#8a5a32",
                   hair="spiky", hair_color="#5a3a22", face="kid", vneck="#ffc08a" if not dog else "#e8c8a0", scale=s)
    story._live(K, t0, t1, expr)
    if dog:
        Mb = M("#8a5a32", 0.7)
        for sx in (-1, 1):
            e = box(f"{name}_dear{sx}", (0.32, 0.18, 0.8), (sx * 0.62, 0.05, 0.3), Mb, 0.1, parent=K.head, coll=K.coll,
                    rot=(0, sx * -20, 0))
            noise(e, "rotation_euler", 1, 0.15, 6)
        sphere(f"{name}_dnose", 0.13, (0, -0.68, 0.0), M("#151515", 0.3), parent=K.head, coll=K.coll, seg=12)
        tl = box(f"{name}_dtail", (0.2, 0.2, 1.1), (0, 0.55, 0.2), Mb, 0.08, parent=K.hip, coll=K.coll, rot=(-35, 0, 0))
        noise(tl, "rotation_euler", 1, 0.9, 2)
        K.tail = tl
    return K


def mom_c(t0, t1, expr="neutral", back="normal", beanie=None, name="Mom", shirt="#e8579a", s=1.0, blink=True,
          hair_color="#7a3a1e", skin="#f1dfc6"):
    """Mom: hair up in a bun so the back of her head (and her second pair of eyes) is bare.
    beanie: None = no hat, True = wearing it, (t_on,) = pops on at t_on, ('off', t) = ripped off at t."""
    Mo = chars.Char(name, skin=skin, shirt=shirt, pants="#2b2b3a", hair="none", face="girl", sleeves="long",
                    vneck="#f6c0a8", scale=s)
    story._live(Mo, t0, t1, expr)
    Mh = mat(name + "_hairm", hexc(hair_color), 0.38, coat=0.3)
    h = Mo.head
    sphere(name + "_hcap", 0.7, (0, 0.04, 0.5), Mh, (1.0, 1.0, 0.42), parent=h, coll=Mo.coll, seg=32)
    sphere(name + "_hbun", 0.36, (0, 0.12, 0.98), Mh, parent=h, coll=Mo.coll, seg=20)
    box(name + "_hfr", (1.12, 0.3, 0.26), (0, -0.48, 0.5), Mh, 0.12, parent=h, coll=Mo.coll)
    for sx in (-1, 1):
        box(f"{name}_hside{sx}", (0.16, 0.5, 0.75), (sx * 0.63, -0.14, 0.12), Mh, 0.08, parent=h, coll=Mo.coll)
    Mo.back = BackEyes(Mo, "girl_eyes", back)
    if blink:
        PENDING.append(lambda: Mo.back.blink(t0, t1, seed=len(name) + int(t0 * 7)))
    Mo.beanie = None
    if beanie is not None:
        Mo.beanie = beanie_on(Mo, beanie)
    return Mo


def beanie_obj(name, coll=None):
    root = empty(name, (0, 0, 0), coll=coll)
    Mk = sets.checker_mat(name + "_knit", "#d8443a", "#c43a32", 14.0, 0.95)
    tilt = empty(name + "_tilt", (0, 0, 0), parent=root, coll=coll, rot=(-24, 0, 0))
    sphere(name + "_dome", 0.8, (0, 0.06, 0.42), Mk, (1.0, 1.0, 1.12), parent=tilt, coll=coll, seg=32)
    cyl(name + "_band", 0.82, 0.4, (0, 0.06, 0.2), M("#f4f0e6", 0.95), 40, bev=0.1, parent=tilt, coll=coll)
    sphere(name + "_pom", 0.3, (0, 0.1, 1.38), M("#f4f0e6", 0.95), parent=tilt, coll=coll, seg=16)
    return root


def beanie_on(ch, mode=True):
    b = beanie_obj(ch.name + "_beanie", ch.coll)
    b.parent = ch.head
    b.location = (0, 0.04, 0.08)
    if isinstance(mode, tuple) and mode[0] == "off":
        t = mode[1]
        b.keyframe_insert("location", frame=F(t)); b.keyframe_insert("rotation_euler", frame=F(t))
        b.location = (1.2, 2.6, 3.6); b.rotation_euler = (math.radians(-160), math.radians(40), math.radians(200))
        b.keyframe_insert("location", frame=F(t + 0.5)); b.keyframe_insert("rotation_euler", frame=F(t + 0.5))
        set_interp(b, "location", F(t), "BEZIER", "EASE_OUT")
    elif isinstance(mode, tuple):
        t = mode[0]
        for dt, z, k in ((-0.2, 2.4, 1.0), (0.0, 0.0, 1.0), (0.06, -0.08, 1.12), (0.16, 0.0, 1.0)):
            b.location = (0, 0.04, 0.08 + z); b.scale = (k, k, 2 - k)
            b.keyframe_insert("location", frame=F(t + dt)); b.keyframe_insert("scale", frame=F(t + dt))
        sets.set_obj_visible(b, t - 0.25, False)
        for o in b.children_recursive:
            sets.set_obj_visible(o, t - 0.25, False)
            sets.set_obj_visible(o, t - 0.2, True)
    return b


def sis_c(t0, t1, expr="happy"):
    Si = chars.Char("Sis", skin="#f1dfc6", shirt="#f2c14e", pants="#f6c0d8", hair="bun", hair_color="#c87a3a",
                    face="girl", scale=0.62)
    return story._live(Si, t0, t1, expr)


def dad_c(t0, t1, expr="sleepy", back_open=False):
    D_ = chars.Char("Dad", skin="#e9c7a6", shirt="#3f7fd9", pants="#c8b48a", hair="buzz", hair_color="#3a2a1e",
                    face="mustache", vneck="#f4f4f4")
    story._live(D_, t0, t1, expr, 0.6)
    D_.back = BackEyes(D_, "dadback_eyes", "normal" if back_open else "closed")
    return D_


ADULTS = [("#3f7fd9", "#c8b48a", "short", "#3a2a1e"), ("#63c06a", "#2b2b3a", "slick", "#151212"),
          ("#9b6ad6", "#55565e", "buzz", "#2a1d16"), ("#e8b520", "#3b3f4a", "short", "#6b3a1e"),
          ("#e8423a", "#2b2b2b", "slick", "#5a3a22"), ("#4fb3b8", "#3d5fb8", "buzz", "#1d1714")]
SKINS = ["#e9c7a6", "#c9926a", "#f1dfc6", "#a8714a", "#d9b48f", "#ecd2b8"]


def adult(i, t0, t1, expr="neutral", s=1.0, extras=()):
    sh, pa, hr, hc = ADULTS[i % len(ADULTS)]
    A = chars.Char(f"Ad{i}", skin=SKINS[i % len(SKINS)], shirt=sh, pants=pa, hair=hr, hair_color=hc,
                   face="mustache" if i % 2 == 0 else "hero", scale=s, extras=extras)
    return story._live(A, t0, t1, expr, 0.6)


def dog_pose(ch, t, loc, rot=0, s=1.0, head_up=60):
    """On all fours (crawling / dog costume)."""
    ch.root.rotation_euler[0] = math.radians(80)
    ch.root.keyframe_insert("rotation_euler", index=0, frame=F(t))
    ch.pose(t, loc=(loc[0], loc[1], loc[2] + 1.75 * s), rot=rot, legL=(80, 4), legR=(80, -4), armL=(85, 6), armR=(85, 6),
            head=(0, -head_up, 0))
    return ch


def crawl(ch, t0, t1, p0, p1, rot=0, s=1.0, rate=2.4):
    dog_pose(ch, t0, p0, rot, s)
    ch.pose(t0, loc=(p0[0], p0[1], p0[2] + 1.75 * s), interp="LINEAR")
    ch.pose(t1, loc=(p1[0], p1[1], p1[2] + 1.75 * s), interp="LINEAR")
    t, k = t0, 0
    while t < t1:
        sgn = 1 if k % 2 == 0 else -1
        ch.pose(t, legL=(80 + 18 * sgn, 4), legR=(80 - 18 * sgn, -4), armL=(85 - 20 * sgn, 6), armR=(85 + 20 * sgn, 6))
        t += 1.0 / (rate * 2); k += 1
    return ch


def point_back(ch, t, side="R"):
    """Mom points over her shoulder without turning around."""
    if side == "R":
        ch.pose(t, armR=(150, -30, 0), head=(0, -4, 0))
        ch.pose(t + 0.12, armR=(175, -20, 0))
    else:
        ch.pose(t, armL=(150, -30, 0), head=(0, -4, 0))
        ch.pose(t + 0.12, armL=(175, -20, 0))
    return ch


# ================================================================== props
def cookie(name, loc, coll=None, s=1.0, rot=(0, 0, 0)):
    root = empty(name, loc, coll=coll, rot=rot)
    root.scale = (s,) * 3
    cyl(name + "_c", 0.42, 0.12, (0, 0, 0), M("#d9a05a", 0.75), 20, bev=0.04, parent=root, coll=coll)
    rnd = random.Random(len(name))
    for i in range(6):
        a = rnd.uniform(0, math.tau); r = rnd.uniform(0.05, 0.3)
        sphere(f"{name}_ch{i}", 0.055, (math.cos(a) * r, math.sin(a) * r, 0.06), M("#4a2a16", 0.6), parent=root, coll=coll, seg=8)
    return root


def cookie_jar(loc, coll=None, lid_t=None):
    root = empty("jar", loc, coll=coll)
    Mg = mat("jar_glass", hexc("#cfe8ff"), 0.05, alpha=0.3)
    cyl("jar_body", 0.95, 1.9, (0, 0, 0.95), Mg, 32, bev=0.2, parent=root, coll=coll)
    lid = empty("jar_lidp", (0, 0, 1.92), parent=root, coll=coll)
    cyl("jar_lid", 1.0, 0.24, (0, 0, 0.0), M("#e8423a", 0.4), 32, bev=0.06, parent=lid, coll=coll)
    sphere("jar_knob", 0.2, (0, 0, 0.22), M("#e8423a", 0.4), parent=lid, coll=coll, seg=12)
    for i in range(9):
        cookie(f"jarc{i}", (((i % 3) - 1) * 0.35, ((i // 3) - 1) * 0.3, 0.25 + (i % 4) * 0.33), coll, 1.0,
               rot=(math.radians(20 * ((i % 3) - 1)), math.radians(15 * ((i // 3) - 1)), 0)).parent = root
    text("jar_lbl", "COOKIES", (0, -0.97, 1.1), 0.28, M("#e8423a", 0.5), extrude=0.02, parent=root, coll=coll, font=FONT)
    if lid_t is not None:
        lid.keyframe_insert("location", frame=F(lid_t)); lid.keyframe_insert("rotation_euler", frame=F(lid_t))
        lid.location = (0.6, 0.6, 2.3); lid.rotation_euler = (0, math.radians(-35), 0)
        lid.keyframe_insert("location", frame=F(lid_t + 0.25)); lid.keyframe_insert("rotation_euler", frame=F(lid_t + 0.25))
    return root


def sleep_mask(name, coll=None):
    root = empty(name, (0, 0, 0), coll=coll)
    box(name + "_m", (1.3, 0.18, 0.5), (0, 0, 0), M("#3a3f9a", 0.6), 0.2, parent=root, coll=coll)
    box(name + "_s", (2.2, 0.06, 0.08), (0, 0.05, 0), M("#222230", 0.6), 0.02, parent=root, coll=coll)
    return root


def ice_cream(name, loc=(0, 0, 0), coll=None, col="#f6b8d0", s=1.0):
    root = empty(name, loc, coll=coll)
    root.scale = (s,) * 3
    cyl(name + "_cone", 0.3, 0.9, (0, 0, -0.45), M("#d9a05a", 0.8), 12, r2=0.02, rot=(180, 0, 0), parent=root, coll=coll)
    sphere(name + "_sc", 0.34, (0, 0, 0.12), M(col, 0.5), parent=root, coll=coll, seg=16)
    sphere(name + "_sc2", 0.3, (0, 0, 0.5), M("#fff0d0", 0.5), parent=root, coll=coll, seg=16)
    return root


def duck(name, loc, coll=None, s=1.0, rot=0):
    """Inflatable duck ring (yellow)."""
    root = empty(name, loc, coll=coll, rot=(0, 0, rot))
    root.scale = (s,) * 3
    My = M("#ffd21e", 0.25, coat=0.6) if False else mat("duck_y", hexc("#ffd21e"), 0.22)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.25, minor_radius=0.5, major_segments=40, minor_segments=16)
    tor = bpy.context.active_object
    tor.name = name + "_ring"
    for c in tor.users_collection:
        c.objects.unlink(tor)
    (coll or bpy.context.scene.collection).objects.link(tor)
    tor.data.materials.append(My)
    bpy.ops.object.shade_smooth() if False else None
    for p in tor.data.polygons:
        p.use_smooth = True
    tor.parent = root
    tor.location = (0, 0, 0.5)
    sphere(name + "_neck", 0.45, (0, -1.35, 1.25), My, (1, 1, 1.4), parent=root, coll=coll, seg=20)
    sphere(name + "_head", 0.55, (0, -1.5, 2.05), My, parent=root, coll=coll, seg=20)
    sphere(name + "_bill", 0.3, (0, -2.0, 1.95), M("#ff8a1e", 0.3), (1.0, 1.3, 0.45), parent=root, coll=coll, seg=14)
    for sx in (-1, 1):
        sphere(f"{name}_eye{sx}", 0.1, (sx * 0.27, -1.98, 2.25), M("#151515", 0.2), parent=root, coll=coll, seg=10)
    sphere(name + "_tail", 0.3, (0, 1.4, 1.0), My, (1, 1.2, 0.8), parent=root, coll=coll, seg=12)
    return root


def bob(ob, amp=0.25, rot=0.08, scale=14):
    noise(ob, "location", 2, amp, scale)
    noise(ob, "rotation_euler", 0, rot, scale * 1.3)
    noise(ob, "rotation_euler", 1, rot, scale * 1.1)


def calendar(name, loc, t0, t1, labels, coll=None, yaw=0, s=1.0):
    """Wall calendar whose pages flip up one after another over [t0, t1]."""
    root = empty(name, loc, coll=coll, rot=(0, 0, yaw))
    root.scale = (s,) * 3
    box(name + "_back", (3.2, 0.15, 3.6), (0, 0.1, -1.8), M("#2a2a32", 0.6), 0.04, parent=root, coll=coll)
    for i in range(2):
        cyl(f"{name}_ring{i}", 0.12, 0.3, (-0.8 + i * 1.6, -0.1, 0.05), M("#c8ccd4", 0.2, metal=0.9), 12, rot=(90, 0, 0),
            parent=root, coll=coll)
    n = len(labels)
    for i, lab in enumerate(labels):
        piv = empty(f"{name}_pg{i}", (0, -0.05 - (n - i) * 0.004, 0), parent=root, coll=coll)
        box(f"{name}_pp{i}", (3.0, 0.02, 3.4), (0, 0, -1.75), M("#fbf8f0", 0.7), 0.01, parent=piv, coll=coll)
        box(f"{name}_ph{i}", (3.0, 0.03, 0.8), (0, -0.01, -0.45), M("#e8423a", 0.5), 0.01, parent=piv, coll=coll)
        text(f"{name}_pt{i}", lab, (0, -0.04, -0.5), 0.5, M("#ffffff", 0.5), extrude=0.01, parent=piv, coll=coll, font=FONT)
        for r in range(4):
            for c in range(5):
                box(f"{name}_d{i}{r}{c}", (0.36, 0.02, 0.36), (-1.1 + c * 0.55, -0.015, -1.3 - r * 0.55),
                    M("#d8d4cc", 0.7), 0.0, parent=piv, coll=coll)
        if i < n - 1:
            tf = t0 + (t1 - t0) * (i + 1) / n
            piv.keyframe_insert("rotation_euler", frame=F(tf - 0.08))
            piv.rotation_euler = (math.radians(-175), 0, 0)
            piv.keyframe_insert("rotation_euler", frame=F(tf + 0.04))
            sets.set_obj_visible(piv, tf + 0.05, True)
            for o in piv.children:
                sets.set_obj_visible(o, tf + 0.04, True)
                sets.set_obj_visible(o, tf + 0.12, False)
            sfx(tf - 0.05, "paper", 0.35)
    return root


def zzz(name, loc, t0, t1, coll=None, s=1.0, every=0.55):
    t, k = t0, 0
    while t < t1:
        z = pop_text(f"{name}{k}", "Z", (loc[0] + 0.25 * k % 3 * s, loc[1], loc[2]), t, 0.6 * s * (1 + 0.25 * (k % 3)),
                     "#bfe3ff", dur=1.1)
        z.keyframe_insert("location", frame=F(t))
        z.location = (z.location[0] + 0.8 * s, z.location[1], z.location[2] + 1.6 * s)
        z.keyframe_insert("location", frame=F(t + 1.1))
        t += every; k += 1


def tears(name, ch, t0, t1, back=False, coll=None):
    """Little blue drops falling from the eyes (front or back)."""
    Mt = mat("tear_blue", hexc("#7fc8ff"), 0.05, emit=hexc("#7fc8ff"), estr=0.6)
    y = 0.66 if back else -0.66
    t, k = t0, 0
    while t < t1 - 0.2:
        for sx in (-1, 1):
            d = sphere(f"{name}{k}{sx}", 0.07, (sx * 0.24, y, -0.05), Mt, (1, 1, 1.4), parent=ch.head, coll=ch.coll, seg=8)
            sets.set_obj_visible(d, t - 0.02, False)
            sets.set_obj_visible(d, t, True)
            d.keyframe_insert("location", frame=F(t))
            d.location = (sx * 0.3, y * 1.25, -1.1)
            d.keyframe_insert("location", frame=F(t + 0.45))
            sets.set_obj_visible(d, t + 0.46, False)
        t += 0.3; k += 1


# ================================================================== more sets
def room(name, wall="#f2e2c8", floor=None, w=40, back_y=8.25, h=16, light_e=5000):
    world((0.9, 0.93, 1.0), 0.45)
    c = collection(name)
    box(name + "_floor", (w, 50, 0.4), (0, 0, -0.2), floor or sets.checker_mat(name + "_fl", "#f2ece0", "#d8cdb8", 0.18), 0, coll=c)
    box(name + "_back", (w, 0.5, h), (0, back_y, h / 2), M(wall, 0.85), 0, coll=c)
    box(name + "_left", (0.5, 50, h), (-w / 2, 0, h / 2), M(wall, 0.85), 0, coll=c)
    box(name + "_right", (0.5, 50, h), (w / 2, 0, h / 2), M(wall, 0.85), 0, coll=c)
    light(name + "_key", "AREA", (0, -6, 13), light_e, (1.0, 0.97, 0.92), 12, coll=c, target=(0, 4, 2))
    light(name + "_fill", "AREA", (-10, -4, 6), 1500, (0.9, 0.95, 1.0), 6, coll=c, target=(0, 4, 3))
    return c


BARB_CH = (0.0, 2.0, 0.0)


def barbershop():
    c = room("BARB", wall="#cfe6f2", floor=sets.checker_mat("barb_fl", "#1d1d22", "#f4f4f4", 0.3))
    box("barb_mir", (6.5, 0.2, 5.0), (0, 7.9, 7.0), mat("barb_mirror", hexc("#dfeef8"), 0.02, metal=1.0), 0.05, coll=c)
    box("barb_mfr", (7.0, 0.3, 5.5), (0, 8.05, 7.0), M("#e2b23a", 0.3, metal=0.8), 0.05, coll=c)
    box("barb_shelf", (8, 1.2, 0.3), (0, 7.4, 4.2), M("#f4f4f4", 0.4), 0.05, coll=c)
    for i, col in enumerate(["#3fa7d9", "#e8423a", "#63c06a", "#f2c14e"]):
        cyl(f"barb_bt{i}", 0.25, 0.9, (-2.2 + i * 1.4, 7.3, 4.8), M(col, 0.25), 12, coll=c)
    # striped pole
    pole = cyl("barb_pole", 0.45, 4.0, (-8, 7.6, 6.0), sets.checker_mat("barb_pol", "#e8423a", "#ffffff", 6.0, 0.3), 24, coll=c)
    pole.keyframe_insert("rotation_euler", index=2, frame=1)
    pole.rotation_euler[2] = math.radians(720)
    pole.keyframe_insert("rotation_euler", index=2, frame=600)
    Mc = M("#c8261e", 0.4)
    box("barb_seat", (2.6, 2.4, 0.7), (BARB_CH[0], BARB_CH[1], 2.4), Mc, 0.2, coll=c)
    box("barb_cback", (2.6, 0.5, 2.0), (BARB_CH[0], BARB_CH[1] - 1.3, 3.6), Mc, 0.2, coll=c)
    cyl("barb_base", 0.9, 2.0, (BARB_CH[0], BARB_CH[1], 1.0), M("#c8ccd4", 0.2, metal=0.9), 24, coll=c)
    return c


def clippers(name, coll=None):
    root = empty(name, (0, 0, 0), coll=coll)
    box(name + "_b", (0.32, 0.28, 0.9), (0, 0, 0), M("#2a2a32", 0.35), 0.1, parent=root, coll=coll)
    box(name + "_h", (0.36, 0.3, 0.12), (0, 0, 0.5), M("#c8ccd4", 0.2, metal=0.9), 0.02, parent=root, coll=coll)
    noise(root, "location", 0, 0.012, 1)
    return root


def car_int(scenery=True, t0=0.0, t1=10.0, speed=40.0):
    """Car interior (driving -X) with tall roof + scenery streaming past."""
    W.sky(1.0); W.sun(3.5, rot=(50, 0, 30))
    c = collection("CARI")
    Mb = M("#3fa7d9", 0.25, metal=0.35)
    Mg = mat("carglass", hexc("#bfe3ff"), 0.05, metal=0.2, alpha=0.12)
    Mi = M("#3a3a44", 0.8)
    box("ci_floor", (16, 7.3, 0.4), (0, 0, 1.2), Mi, 0.05, coll=c)
    for sy in (-1, 1):
        box(f"ci_side{sy}", (16, 0.3, 2.6), (0, sy * 3.6, 2.3), Mb, 0.1, coll=c)
        box(f"ci_win{sy}", (11, 0.08, 3.4), (0.5, sy * 3.6, 5.3), Mg, 0.02, coll=c)
    box("ci_roof", (11, 7.5, 0.35), (0.5, 0, 7.4), Mb, 0.15, coll=c)
    box("ci_ceil", (10.6, 7.0, 0.1), (0.5, 0, 7.2), M("#d8d0c0", 0.9), 0.0, coll=c)
    for x in (-4.6, 0.5, 5.6):
        for sy in (-1, 1):
            box(f"ci_pil{x}{sy}", (0.4, 0.4, 3.8), (x, sy * 3.55, 5.4), Mb, 0.05, coll=c)
    box("ci_wsh", (0.08, 7.0, 3.6), (-5.2, 0, 5.3), Mg, 0.02, coll=c, rot=(0, -25, 0))
    box("ci_rear", (0.08, 7.0, 3.4), (6.0, 0, 5.3), Mg, 0.02, coll=c, rot=(0, 18, 0))
    box("ci_hood", (4.0, 7.4, 1.0), (-7.6, 0, 3.0), Mb, 0.4, coll=c)
    Ms = M("#5a4a3a", 0.8)
    for y, nm in ((-1.6, "d"), (1.7, "p")):
        box(f"ci_seat_{nm}", (2.6, 2.6, 0.8), (-1.6, y, 2.7), Ms, 0.25, coll=c)
        box(f"ci_seatb_{nm}", (0.7, 2.6, 2.6), (-0.1, y, 3.9), Ms, 0.3, coll=c, rot=(0, 10, 0))
        box(f"ci_rest_{nm}", (0.5, 1.4, 0.7), (-0.2, y, 5.55), Ms, 0.2, coll=c)
    box("ci_bseat", (2.6, 6.6, 0.8), (3.4, 0, 2.7), Ms, 0.25, coll=c)
    box("ci_bback", (0.7, 6.6, 2.8), (4.9, 0, 3.9), Ms, 0.3, coll=c, rot=(0, 10, 0))
    box("ci_dash", (1.4, 7.0, 1.4), (-4.2, 0, 3.9), M("#2a2a32", 0.6), 0.2, coll=c)
    cyl("ci_wheel", 0.85, 0.15, (-3.2, -1.6, 4.6), M("#18181c", 0.5), 24, rot=(0, 65, 0), coll=c)
    light("ci_in", "AREA", (0, 0, 6.9), 900, (1.0, 0.97, 0.9), 4, coll=c, target=(0, 0, 0))
    if scenery:
        sc = collection("CARI_OUT")
        piv = empty("ci_scen", (0, 0, 0), coll=sc)
        box("ci_road", (2000, 22, 0.1), (0, 0, 0.0), M("#3a3a40", 0.9), 0, coll=sc)
        box("ci_grass", (2000, 600, 0.1), (0, 0, -0.1), M("#5fb04a", 0.9), 0, coll=sc)
        rnd = random.Random(4)
        for i in range(70):
            x = -60 + i * 12 + rnd.uniform(-3, 3)
            for sy in (-1, 1):
                y = sy * rnd.uniform(16, 30)
                tt = cyl(f"ci_tt{i}{sy}", 0.5, 5, (x, y, 2.5), M("#6a4a2a"), 8, coll=sc)
                tc = sphere(f"ci_tc{i}{sy}", rnd.uniform(2.5, 3.6), (x, y, 7), M("#3f8f3a", 0.9), coll=sc, seg=12)
                tt.parent = piv; tc.parent = piv
            st = box(f"ci_str{i}", (4, 0.4, 0.05), (x, 0, 0.08), M("#f4f4f4", 0.6), 0, coll=sc)
            st.parent = piv
        piv.keyframe_insert("location", frame=F(t0))
        piv.location = (speed * (t1 - t0), 0, 0)
        piv.keyframe_insert("location", frame=F(t1))
        set_interp(piv, "location", F(t0), "LINEAR")
    return c


DRV = (-1.6, -1.6, 3.1)     # driver seat top
BSEAT = (3.4, -1.6, 3.1)    # back seat (behind the driver)


# ------------------------------------------------------------------ beach
SHORE = 22.0
STAND = (-14.0, -16.0, 0.0)       # ice cream stand (front faces +Y)
MOM_B = (-14.0, -12.4, 0.0)        # mom at the stand, rot 0 (faces the stand), back eyes face the sea
KID_B = (-9.5, -10.0, 0.0)
TOWER = (14.0, 10.0, 0.0)
DOT = (26.0, 150.0, 0.0)


def ocean_mat():
    m = D.materials.new("ocean")
    m.use_nodes = True
    nt = m.node_tree; N, L = nt.nodes, nt.links
    b = next(n for n in N if n.type == "BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value = 0.08
    tc = N.new("ShaderNodeTexCoord")
    wv = N.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 0.06; wv.inputs["Distortion"].default_value = 6
    wv.wave_type = "BANDS"; wv.bands_direction = "Y"
    L.new(tc.outputs["Object"], wv.inputs["Vector"])
    nz = N.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.25; nz.inputs["Detail"].default_value = 4
    L.new(tc.outputs["Object"], nz.inputs["Vector"])
    cr = N.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[0].color = (*hexc("#1e7fd0"), 1)
    cr.color_ramp.elements[1].position = 0.9; cr.color_ramp.elements[1].color = (*hexc("#3fd0e8"), 1)
    mx = N.new("ShaderNodeMath"); mx.operation = "MULTIPLY"
    L.new(wv.outputs["Fac"], mx.inputs[0]); L.new(nz.outputs["Fac"], mx.inputs[1])
    L.new(nz.outputs["Fac"], cr.inputs[0])
    L.new(cr.outputs[0], b.inputs["Base Color"])
    bm = N.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.35
    L.new(mx.outputs[0], bm.inputs["Height"]); L.new(bm.outputs[0], b.inputs["Normal"])
    return m


def umbrella(name, loc, col, coll=None, tilt=0):
    root = empty(name, loc, coll=coll, rot=(math.radians(tilt), 0, 0))
    cyl(name + "_pole", 0.1, 6.0, (0, 0, 3.0), M("#f4f4f4", 0.4), 8, parent=root, coll=coll)
    cyl(name + "_top", 3.4, 1.4, (0, 0, 6.3), sets.checker_mat("umb" + col, col, "#ffffff", 3.0, 0.5), 16, r2=0.15,
        parent=root, coll=coll)
    return root


def towel(name, loc, col, coll=None, rot=0):
    return box(name, (2.4, 4.6, 0.06), loc, sets.checker_mat("tw" + col, col, "#ffffff", 2.0, 0.8), 0.0, coll=coll,
               rot=(0, 0, rot))


def foam(name, x0, x1, y, t0, t1, coll=None, seed=0, z=0.25):
    """A white wave line rolling in to the shore and back."""
    rnd = random.Random(seed)
    root = empty(name, (0, y, 0), coll=coll)
    Mf = mat("foam", (0.97, 0.98, 1.0), 0.6, emit=(0.6, 0.7, 0.8), estr=0.25)
    x = x0
    i = 0
    while x < x1:
        sphere(f"{name}{i}", rnd.uniform(0.45, 0.75), (x, rnd.uniform(-0.3, 0.3), z * 0.5), Mf, (3.0, 0.9, 0.18), parent=root,
               coll=coll, seg=10)
        x += rnd.uniform(2.6, 3.6); i += 1
    root.keyframe_insert("location", frame=F(t0))
    root.location = (0, y - 6, 0)
    root.keyframe_insert("location", frame=F((t0 + t1) / 2))
    root.location = (0, y, 0)
    root.keyframe_insert("location", frame=F(t1))
    return root


def beach(t0=0.0, t1=10.0, crowd_n=140, people=True, umbrellas=True, stand=True, tower=True, seed=2, dense=None, dense_u=None):
    W.sky(1.0)
    W.sun(5.0, rot=(45, 0, 160))
    c = collection("BEACH")
    box("bc_sand", (900, 400, 1.0), (0, SHORE - 200, -0.5), M("#f2d898", 0.95), 0, coll=c)
    box("bc_wet", (900, 6, 1.0), (0, SHORE - 2, -0.52), M("#d9b876", 0.6), 0, coll=c)
    sea = plane("bc_sea", 1600, 1200, (0, SHORE + 600, 0.12), ocean_mat(), coll=c)
    noise(sea, "location", 2, 0.06, 30)
    for k in range(3):
        foam(f"bc_foam{k}", -120, 120, SHORE + 2 + k * 9, t0 - k * 1.3, t0 - k * 1.3 + 4.0, coll=c, seed=k)
    rnd = random.Random(seed)
    cols = ["#e8423a", "#3f7fd9", "#f2c14e", "#63c06a", "#f09ac2", "#9b6ad6", "#ff8a3d"]
    if umbrellas:
        for i in range(70):
            x = rnd.uniform(-90, 90); y = rnd.uniform(-70, SHORE - 8)
            if abs(x - STAND[0]) < 9 and abs(y - STAND[1]) < 10:
                continue
            if abs(x - KID_B[0]) < 5 and abs(y - KID_B[1]) < 6:
                continue
            umbrella(f"bc_u{i}", (x, y, 0), cols[i % len(cols)], c, tilt=rnd.uniform(-8, 8))
        if dense_u:
            cx, cy, r, n = dense_u
            for i in range(n):
                umbrella(f"bc_du{i}", (cx + rnd.uniform(-r, r), cy + rnd.uniform(-r, r), 0), cols[(i * 3) % len(cols)], c,
                         tilt=rnd.uniform(-10, 10))
            towel(f"bc_t{i}", (x + 2.5, y + 1, 0.03), cols[(i + 3) % len(cols)], c, rot=rnd.uniform(-20, 20))
    if stand:
        Ms = M("#f4f4f4", 0.5)
        box("st_body", (8, 4, 4), (STAND[0], STAND[1], 2.0), M("#7fd0e8", 0.5), 0.1, coll=c)
        box("st_top", (8.4, 4.4, 0.3), (STAND[0], STAND[1], 4.1), Ms, 0.05, coll=c)
        for sx in (-1, 1):
            cyl(f"st_post{sx}", 0.18, 5, (STAND[0] + sx * 3.8, STAND[1] + 1.8, 6.5), Ms, 8, coll=c)
        box("st_awn", (8.8, 4.6, 0.3), (STAND[0], STAND[1] + 0.6, 9.1), sets.checker_mat("st_aw", "#f09ac2", "#ffffff", 2.0, 0.5),
            0.05, coll=c, rot=(-12, 0, 0))
        box("st_sign", (6.0, 0.3, 1.6), (STAND[0], STAND[1] + 2.2, 10.4), M("#ffffff", 0.4), 0.1, coll=c)
        text("st_txt", "ICE CREAM", (STAND[0], STAND[1] + 2.45, 10.4), 0.9, M("#e8423a", 0.4), extrude=0.04, rot=(90, 0, 180),
             coll=c, font=FONT)
        for i, col in enumerate(["#f6b8d0", "#fff0d0", "#7a4a2a", "#9fe0b0"]):
            ice_cream(f"st_ic{i}", (STAND[0] - 2.4 + i * 1.6, STAND[1] + 1.4, 4.9), c, col, 1.0)
    if tower:
        Mt = M("#ffffff", 0.5)
        for sx in (-1, 1):
            for sy in (-1, 1):
                cyl(f"tw_leg{sx}{sy}", 0.18, 6, (TOWER[0] + sx * 1.6, TOWER[1] + sy * 1.6, 3), Mt, 8, coll=c)
        box("tw_plat", (4.0, 4.0, 0.3), (TOWER[0], TOWER[1], 6.1), M("#e8423a", 0.5), 0.05, coll=c)
        box("tw_back", (4.0, 0.3, 2.4), (TOWER[0], TOWER[1] + 1.9, 7.4), M("#e8423a", 0.5), 0.05, coll=c)
        box("tw_roof", (4.6, 4.6, 0.25), (TOWER[0], TOWER[1], 10.2), M("#e8423a", 0.5), 0.05, coll=c)
        for sx in (-1, 1):
            cyl(f"tw_rp{sx}", 0.1, 4, (TOWER[0] + sx * 1.9, TOWER[1] + 1.9, 8.2), Mt, 6, coll=c)
    if people and crowd_n:
        srcs = []
        for j in range(4):
            src = crowd_src(f"BCROWD{j}", t0, t1, [30 + j * 3, 31 + j * 3], mode="lookup" if False else "idle", spread=2.5,
                            seed=j)
            srcs.append(src)
        for i in range(crowd_n):
            x = rnd.uniform(-100, 100); y = rnd.uniform(-80, SHORE - 3)
            if abs(x - STAND[0]) < 10 and abs(y - STAND[1]) < 12:
                continue
            if abs(x - KID_B[0]) < 6 and abs(y - KID_B[1]) < 8:
                continue
            ob = instance(f"bcp{i}", srcs[i % 4], (x, y, 0), rot=(0, 0, rnd.uniform(-180, 180)))
            noise(ob, "location", 2, 0.05, 6 + i % 5)
        if dense:
            cx, cy, r, n = dense
            for i in range(n):
                ob = instance(f"bcd{i}", srcs[i % 4], (cx + rnd.uniform(-r, r), cy + rnd.uniform(-r, r), 0),
                              rot=(0, 0, rnd.uniform(-180, 180)))
    return c


def sea_only(t0=0.0, t1=10.0):
    """Open sea, no beach props (for far-out shots)."""
    W.sky(1.0)
    W.sun(5.0, rot=(45, 0, 160))
    c = collection("SEA")
    plane("sea_far", 3000, 3000, (0, 0, 0.12), ocean_mat(), coll=c)
    box("sea_sand", (900, 400, 1.0), (0, SHORE - 200, -0.5), M("#f2d898", 0.95), 0, coll=c)
    return c


def swell(ob, amp=0.35, scale=10):
    bob(ob, amp, 0.12, scale)
