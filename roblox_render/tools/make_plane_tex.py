"""Textures for the 'plane windows' story (Cyrillic labels, drawn with Pillow). python tools/make_plane_tex.py"""
import os, math
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "tex")
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s): return ImageFont.truetype(FB, s)
def ctext(d, xy, s, f, fill, anchor="mm"): d.text(xy, s, font=f, fill=fill, anchor=anchor)

def blueprint(name, round_w):
    W, H = 1600, 800
    im = Image.new("RGB", (W, H), (24, 70, 140)); d = ImageDraw.Draw(im)
    for x in range(0, W, 40): d.line([(x, 0), (x, H)], fill=(40, 96, 170), width=1)
    for y in range(0, H, 40): d.line([(0, y), (W, y)], fill=(40, 96, 170), width=1)
    d.rounded_rectangle([140, 260, 1460, 560], 150, outline=(235, 245, 255), width=8)       # fuselage
    d.polygon([(1250, 300), (1500, 150), (1560, 150), (1420, 330)], outline=(235, 245, 255))   # tail fin
    for i in range(9):
        cx = 330 + i * 110; cy = 340
        if round_w:
            d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=(255, 255, 255), width=7)
        else:
            d.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], outline=(255, 255, 255), width=7)
    ctext(d, (800, 90), "ЛАЙНЕР · ОКНА " + ("КРУГЛЫЕ" if round_w else "КВАДРАТНЫЕ"), font(64), (255, 255, 255))
    ctext(d, (800, 700), "ПРОЕКТ №1", font(46), (170, 210, 255))
    im.save(os.path.join(OUT, name))

def news(name):
    W, H = 1200, 1600
    im = Image.new("RGB", (W, H), (236, 226, 200)); d = ImageDraw.Draw(im)
    ctext(d, (600, 120), "ВЕСТНИК", font(110), (30, 26, 22))
    d.line([(60, 200), (1140, 200)], fill=(30, 26, 22), width=6)
    ctext(d, (600, 330), "ЛАЙНЕР", font(190), (160, 20, 20))
    ctext(d, (600, 520), "БУДУЩЕГО!", font(150), (160, 20, 20))
    d.rectangle([160, 640, 1040, 1080], fill=(150, 190, 225), outline=(30, 26, 22), width=8)
    d.rounded_rectangle([250, 820, 960, 940], 60, fill=(250, 250, 250), outline=(60, 60, 60), width=4)
    for i in range(6):
        cx = 330 + i * 100; d.rectangle([cx - 24, 855, cx + 24, 905], fill=(30, 40, 60))
    d.polygon([(900, 840), (1010, 720), (1030, 720), (960, 860)], fill=(70, 120, 200))
    for y in range(1150, 1560, 34): d.line([(120, y), (1080, y)], fill=(90, 84, 72), width=10)
    im.save(os.path.join(OUT, name))

def sold(name):
    W, H = 1600, 700
    im = Image.new("RGB", (W, H), (190, 28, 28)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([30, 30, W - 30, H - 30], 60, outline=(255, 255, 255), width=14)
    ctext(d, (800, 250), "БИЛЕТОВ", font(230), (255, 255, 255)); ctext(d, (800, 500), "НЕТ!", font(260), (255, 235, 90))
    im.save(os.path.join(OUT, name))

def laugh(name):
    W, H = 900, 500
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([20, 20, W - 20, H - 80], fill=(255, 255, 255, 255), outline=(20, 20, 24, 255), width=14)
    d.polygon([(200, H - 120), (140, H - 10), (330, H - 100)], fill=(255, 255, 255, 255), outline=(20, 20, 24, 255))
    d.rectangle([170, H - 130, 320, H - 108], fill=(255, 255, 255, 255))
    ctext(d, (450, 215), "ХА-ХА!", font(190), (20, 20, 24, 255))
    im.save(os.path.join(OUT, name))

def label(name, line1, line2="", col=(255, 255, 255), bg=(20, 24, 34)):
    W, H = 1400, 500
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, W - 20, H - 20], 40, outline=col, width=10)
    ctext(d, (700, 200 if line2 else 250), line1, font(170), col)
    if line2: ctext(d, (700, 370), line2, font(110), col)
    im.save(os.path.join(OUT, name))

blueprint("plane_bp_sq.png", False); blueprint("plane_bp_round.png", True)
news("plane_news.png"); sold("plane_sold.png"); laugh("plane_laugh.png")
label("plane_sq_bad.png", "КВАДРАТ", "ДЕШЕВЛЕ!", (255, 235, 90), (30, 30, 40))
print("ok")
