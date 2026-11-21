"""Props for the 'town' story (Pillow, Titan One). python tools/make_textures3.py"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets", "tex")
FONT = os.path.join(os.path.dirname(HERE), "assets", "fonts", "TitanOne-Regular.ttf")
f = lambda s: ImageFont.truetype(FONT, s)


def smiley(d, cx, cy, r, laugh=True):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 64), outline=(40, 30, 20), width=max(4, r // 14))
    for sx in (-1, 1):
        d.ellipse([cx + sx * r * .38 - r * .1, cy - r * .3 - r * .14, cx + sx * r * .38 + r * .1, cy - r * .3 + r * .14], fill=(40, 30, 20))
    d.pieslice([cx - r * .55, cy - r * .1, cx + r * .55, cy + r * .6], 0, 180, fill=(120, 30, 30), outline=(40, 30, 20), width=max(3, r // 20))


def sign_nolaugh():
    im = Image.new("RGB", (1024, 1024), (245, 245, 240)); d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 1004, 1004], outline=(200, 30, 30), width=36)
    smiley(d, 512, 400, 250)
    d.ellipse([212, 100, 812, 700], outline=(210, 30, 30), width=48)
    d.line([(300, 190), (724, 610)], fill=(210, 30, 30), width=56)
    d.text((512, 860), "NO LAUGHING", font=f(150), fill=(200, 30, 30), anchor="mm")
    im.save(os.path.join(OUT, "sign_nolaugh.png"))


def sign_drown():
    im = Image.new("RGB", (1600, 800), (40, 110, 200)); d = ImageDraw.Draw(im)
    d.rectangle([24, 24, 1576, 776], outline=(255, 214, 64), width=24)
    d.text((800, 300), "LAUGH", font=f(250), fill=(255, 255, 255), anchor="mm", stroke_width=10, stroke_fill=(20, 50, 110))
    d.text((800, 560), "OR DROWN!", font=f(250), fill=(255, 214, 64), anchor="mm", stroke_width=10, stroke_fill=(20, 50, 110))
    im.save(os.path.join(OUT, "sign_drown.png"))


def fine_ticket():
    im = Image.new("RGB", (800, 1000), (250, 244, 214)); d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 780, 980], outline=(200, 30, 30), width=18)
    d.text((400, 200), "FINE!", font=f(220), fill=(200, 30, 30), anchor="mm")
    d.text((400, 460), "$100", font=f(260), fill=(30, 30, 30), anchor="mm")
    d.text((400, 720), "HA HA = BAD", font=f(100), fill=(30, 30, 30), anchor="mm")
    smiley(d, 400, 880, 60)
    im.save(os.path.join(OUT, "fine_ticket.png"))


def loan():
    im = Image.new("RGB", (1200, 800), (250, 244, 214)); d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 1180, 780], outline=(60, 60, 60), width=14)
    d.text((600, 190), "GIGGLE LOAN", font=f(150), fill=(30, 30, 30), anchor="mm")
    d.text((600, 450), "$1,000,000", font=f(210), fill=(200, 30, 30), anchor="mm")
    d.text((600, 660), "PAY BACK: FOREVER", font=f(90), fill=(60, 60, 60), anchor="mm")
    im.save(os.path.join(OUT, "loan.png"))


def note(name, lines, w=700, h=500):
    im = Image.new("RGB", (w, h), (252, 246, 222)); d = ImageDraw.Draw(im)
    d.rectangle([6, 6, w - 6, h - 6], outline=(200, 190, 150), width=6)
    n = len(lines)
    for i, ln in enumerate(lines):
        d.text((w // 2, int(h * (i + 1) / (n + 1))), ln, font=f(64), fill=(40, 40, 110), anchor="mm")
    im.save(os.path.join(OUT, name))


def dollar():
    im = Image.new("RGB", (900, 400), (110, 180, 110)); d = ImageDraw.Draw(im)
    d.rectangle([14, 14, 886, 386], outline=(40, 100, 50), width=10)
    d.ellipse([300, 70, 600, 330], fill=(150, 210, 150), outline=(40, 100, 50), width=8)
    d.text((450, 200), "$", font=f(190), fill=(40, 100, 50), anchor="mm")
    d.text((90, 70), "1", font=f(70), fill=(40, 100, 50), anchor="mm")
    d.text((810, 330), "1", font=f(70), fill=(40, 100, 50), anchor="mm")
    im.save(os.path.join(OUT, "dollar.png"))


def wanted_tootie():
    im = Image.new("RGB", (800, 1000), (236, 214, 160)); d = ImageDraw.Draw(im)
    d.text((400, 130), "WANTED", font=f(190), fill=(90, 40, 20), anchor="mm")
    smiley(d, 400, 500, 210)
    d.text((400, 820), "TOOTIE", font=f(150), fill=(90, 40, 20), anchor="mm")
    d.text((400, 940), "FOR JOKES", font=f(80), fill=(90, 40, 20), anchor="mm")
    im.save(os.path.join(OUT, "wanted_tootie.png"))


def elevator():
    im = Image.new("RGB", (800, 1000), (170, 175, 185)); d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 740, 960], fill=(205, 208, 214), outline=(60, 60, 70), width=14)
    d.line([(400, 60), (400, 960)], fill=(60, 60, 70), width=12)
    d.text((400, 30), "", font=f(10))
    d.rectangle([260, 8, 540, 56], fill=(30, 30, 36)); d.text((400, 34), "1  2  3", font=f(34), fill=(255, 80, 60), anchor="mm")
    im.save(os.path.join(OUT, "elevator.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sign_nolaugh(); sign_drown(); fine_ticket(); loan(); dollar(); wanted_tootie(); elevator()
    note("note_rock.png", ["ROCK AND ROLL,", "WE'RE LOSING", "CONTROL!"])
    note("note_mil.png", ["MOTHER-IN-LAW", "JOKE  -  $2"])
    note("note_one.png", ["JOKE", "$1"])
    print("ok")
