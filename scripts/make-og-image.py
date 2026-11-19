#!/usr/bin/env python3
"""Generate landing/og-image.png 1200x630 (PIL, lokal, tanpa jaringan).

Desain mengikuti palet landing (docs/DESIGN.md): kertas arsip #F2F0E6,
tinta #22271F, merah cap #A63A2B, biru garis #33546D, ochre #C99A2E.
Kartu arsip buku log — BUKAN screenshot asli.
Usage: python3 scripts/make-og-image.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (242, 240, 230)   # #F2F0E6
INK = (34, 39, 31)        # #22271F
RED = (166, 58, 43)       # #A63A2B
BLUE = (51, 84, 109)      # #33546D
OCHRE = (201, 154, 46)    # #C99A2E
PENCIL = (138, 133, 120)  # #8A8578

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "landing", "og-image.png")

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# garis aturan buku (biru, horizontal) + garis margin merah vertikal
for y in range(150, H - 60, 46):
    d.line([(90, y), (W - 90, y)], fill=BLUE, width=1)
d.line([(150, 0), (150, H)], fill=RED, width=3)

# lubang jilid
for y in (140, 315, 490):
    d.ellipse([52, y - 16, 84, y + 16], outline=PENCIL, width=3)
    d.ellipse([60, y - 8, 76, y + 8], fill=(226, 223, 210))

# nomor halaman stempel
f_no = ImageFont.truetype(MONO_B, 28)
d.text((W - 250, 44), "No. 047", font=f_no, fill=RED)

# kicker
f_kick = ImageFont.truetype(MONO_B, 30)
d.text((190, 56), "BUKU LOG  ·  ARSIP ABSENSI  ·  USK", font=f_kick, fill=BLUE)

# judul
f_title = ImageFont.truetype(SERIF_B, 96)
d.text((186, 104), "Monitor Kuliah", font=f_title, fill=INK)
d.text((186, 204), "Dezz", font=f_title, fill=INK)

# stempel HADIR (miring, garis ganda) — digambar di layer terpisah lalu diputar
stamp = Image.new("RGBA", (340, 150), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
f_stamp = ImageFont.truetype(SANS_B, 64)
sd.rectangle([6, 6, 334, 144], outline=RED, width=5)
sd.rectangle([16, 16, 324, 134], outline=RED, width=2)
sd.text((42, 42), "HADIR", font=f_stamp, fill=RED)
stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (860, 290), stamp)

# subjudul
f_sub = ImageFont.truetype(SANS, 34)
d.text((190, 322), "Otomasi absensi SIMKULIAH + monitor", font=f_sub, fill=INK)
d.text((190, 366), "Moodle & Google Classroom.", font=f_sub, fill=INK)

# baris entri contoh (di atas garis aturan)
f_row = ImageFont.truetype(MONO, 27)
d.text((190, 434), "16:47  SINF2023  absen masuk  ·  success", font=f_row, fill=INK)
d.text((190, 480), "01:13  PBO       draft siap kumpul  ·  PDF", font=f_row, fill=INK)

# footer
f_foot = ImageFont.truetype(MONO_B, 28)
d.text((190, 548), "13 MK  ·  21 SKS  ·  S1 SISTEM INFORMASI", font=f_foot, fill=OCHRE)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG")
print(f"{OUT}  {os.path.getsize(OUT)} byte")
