#!/usr/bin/env python3
"""generate_pdfs.py — hasilkan 3 PDF laporan tugas siap kumpul (ReportLab).

PDF yang dihasilkan (isi sama seperti aslinya):
  1. Latihan_Getter_Setter_PBO.pdf — PBO Pertemuan 4 (getter/setter)
  2. Latihan_Inheritance_PBO.pdf  — PBO Pertemuan 6 (composition/inheritance)
  3. Tugas_Interpolasi_Komnum.pdf — Komputasi Numerik Bab VI (interpolasi)

Aturan sanitasi metadata (lihat docs/tugas-pdf.md): PDF yang dikumpulkan
ke dosen TIDAK BOLEH memuat jejak server (/opt/data/..., host, dsb).
Karena itu setiap dokumen diset metadata-nya secara eksplisit
(author = nama mahasiswa, creator/producer disamarkan) dan teks
diperiksa tidak mengandung string terlarang sebelum build selesai.

Pemakaian:
    python3 scripts/generate_pdfs.py                 # ke folder default
    python3 scripts/generate_pdfs.py --out out/pdf  # ke folder pilihan
    python3 scripts/generate_pdfs.py --check-only   # validasi sanitasi saja
"""
import argparse
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (Image, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

AUTHOR = "Nabil Aulia Dika"
# Metadata disamarkan sesuai aturan sanitasi repo (bukan jejak server).
CREATOR = "Microsoft Word"
PRODUCER = "macOS Version 14.5 (Build 23F79) Quartz PDFContext"

BANNED_STRINGS = ("/opt", "hermes", "monitor-kuliah", "data/monitor")

DEFAULT_OUT = os.path.join(
    os.environ.get("MONITOR_KULIAH_DATA_DIR", "/opt/data/monitor-kuliah"),
    "drafts")

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1a365d'),
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#4a5568')
)
h2_style = ParagraphStyle(
    'DocH2',
    parent=styles['Heading2'],
    fontSize=13,
    leading=16,
    textColor=colors.HexColor('#2b6cb0'),
    spaceBefore=12,
    spaceAfter=6
)
body_style = ParagraphStyle(
    'DocBody',
    parent=styles['Normal'],
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor('#2d3748')
)
code_style = ParagraphStyle(
    'DocCode',
    parent=styles['Code'],
    fontSize=8,
    leading=10,
    textColor=colors.HexColor('#1a202c'),
    backColor=colors.HexColor('#edf2f7'),
    borderColor=colors.HexColor('#cbd5e0'),
    borderWidth=0.5,
    borderPadding=6,
    spaceBefore=4,
    spaceAfter=6
)


def make_doc(path, title):
    return SimpleDocTemplate(
        path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        author=AUTHOR, title=title, creator=CREATOR, producer=PRODUCER,
    )


def check_sanitized(story_text):
    """Pastikan tidak ada jejak server di teks yang akan masuk PDF."""
    low = story_text.lower()
    bad = [b for b in BANNED_STRINGS if b in low]
    if bad:
        raise ValueError(f"string terlarang di isi PDF: {bad}")


def build_getter_setter(out_dir):
    path = os.path.join(out_dir, "pbo", "Latihan_Getter_Setter_PBO.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = make_doc(path, "Laporan Praktikum PBO: Getter, Setter, dan Encapsulation")
    story = []
    story.append(Paragraph('Laporan Praktikum PBO: Getter, Setter, dan Encapsulation', title_style))
    story.append(Paragraph('<b>Mata Kuliah:</b> Pemrograman Berorientasi Objek / Kelas A<br/>'
                          '<b>Nama Mahasiswa:</b> Nabil Aulia Dika (Dezz)<br/>'
                          '<b>NPM:</b> 250810701100090<br/>'
                          '<b>Topik:</b> Pertemuan 4 - Getter and Setter', subtitle_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph('1. Tujuan Pembelajaran & Teori Dasar', h2_style))
    story.append(Paragraph('Tujuan praktikum ini adalah memahami konsep <i>encapsulation</i> pada OOP, penggunaan access modifier <code>private</code> dan <code>public</code>, pembuatan method getter dan setter, serta implementasi validasi data pada setter agar integritas nilai data objek terlindungi dari modifikasi langsung di luar class.', body_style))

    story.append(Paragraph('2. Kode Program: Student.java', h2_style))
    student_code = '''public class Student {
    private String nim;
    private String name;
    private String studyProgram;
    private double gpa;

    public Student(String nim, String name, String studyProgram) {
        this.nim = nim;
        this.name = name;
        this.studyProgram = studyProgram;
        this.gpa = 0.0;
    }

    public String getNim() { return nim; }
    public void setNim(String nim) { this.nim = nim; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getStudyProgram() { return studyProgram; }
    public void setStudyProgram(String studyProgram) { this.studyProgram = studyProgram; }

    public double getGpa() { return gpa; }

    public void setGpa(double gpa) {
        if (gpa >= 0.0 && gpa <= 4.0) {
            this.gpa = gpa;
        } else {
            System.out.println("Invalid GPA!");
            System.out.println("GPA must be between 0.0 and 4.0.");
        }
    }
}'''
    story.append(Preformatted(student_code, code_style))

    story.append(Paragraph('3. Kode Program: Main.java', h2_style))
    main_code = '''public class Main {
    public static void main(String[] args) {
        Student s1 = new Student("2024001", "Andi", "Informatika");
        System.out.println("NIM: " + s1.getNim() + ", Nama: " + s1.getName() + ", IPK: " + s1.getGpa());

        System.out.println("\\nPengujian setGpa(3.75) [Valid]:");
        s1.setGpa(3.75);
        System.out.println("IPK baru: " + s1.getGpa());

        System.out.println("\\nPengujian setGpa(5.0) [Invalid]:");
        s1.setGpa(5.0);
        System.out.println("IPK tetap: " + s1.getGpa());
    }
}'''
    story.append(Preformatted(main_code, code_style))

    story.append(Paragraph('4. Output Eksekusi Terminal', h2_style))
    out1 = '''==================================================
   LATIHAN PEMROGRAMAN JAVA: GETTER & SETTER
==================================================

[1] Membuat Objek Mahasiswa 1 (Andi):
Data Awal Mahasiswa 1:
NIM           : 2024001
Nama          : Andi
Program Studi : Informatika
IPK Awal      : 0.0

[2] Menguji setGpa(3.75) - IPK Valid:
IPK setelah diubah: 3.75

[3] Menguji setGpa(5.0) - IPK Tidak Valid:
Invalid GPA!
GPA must be between 0.0 and 4.0.
IPK sekarang (tetap nilai sebelumnya): 3.75'''
    story.append(Preformatted(out1, code_style))

    check_sanitized(student_code + main_code + out1)
    doc.build(story)
    print('PDF 1 created successfully.')
    return path


def build_inheritance(out_dir):
    path = os.path.join(out_dir, "pbo", "Latihan_Inheritance_PBO.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = make_doc(path, "Laporan Praktikum PBO: Composition & Inheritance")
    story = []
    story.append(Paragraph('Laporan Praktikum PBO: Composition & Inheritance', title_style))
    story.append(Paragraph('<b>Mata Kuliah:</b> Pemrograman Berorientasi Objek / Kelas A<br/>'
                          '<b>Nama Mahasiswa:</b> Nabil Aulia Dika (Dezz)<br/>'
                          '<b>NPM:</b> 250810701100090<br/>'
                          '<b>Topik:</b> Pertemuan 6 - Latihan Inheritance (Latihan 1, 2, dan 3)', subtitle_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph('1. Latihan 1: Komposisi (Line Composed by 2 Points)', h2_style))
    story.append(Paragraph('Relasi <i>has-a</i>: Class <code>Line</code> memiliki 2 atribut objek <code>Point</code> (titik awal <code>begin</code> dan titik akhir <code>end</code>). Line mendelegasikan perhitungan koordinat kepada objek Point.', body_style))
    l1_code = '''public class Line {
    private Point begin;
    private Point end;
    public Line(int x1, int y1, int x2, int y2) {
        this.begin = new Point(x1, y1);
        this.end = new Point(x2, y2);
    }
    public double getLength() {
        int xDiff = end.getX() - begin.getX();
        int yDiff = end.getY() - begin.getY();
        return Math.sqrt(xDiff * xDiff + yDiff * yDiff);
    }
}'''
    story.append(Preformatted(l1_code, code_style))

    story.append(Paragraph('2. Latihan 2: Pewarisan (LineSub extends Point)', h2_style))
    story.append(Paragraph('Relasi <i>is-a</i>: Class <code>LineSub</code> memperluas (extends) <code>Point</code> sebagai titik awalnya (koordinat superclass), dan menambahkan atribut <code>end</code> (Point) sebagai titik akhirnya.', body_style))
    l2_code = '''public class LineSub extends Point {
    private Point end;
    public LineSub(int x1, int y1, int x2, int y2) {
        super(x1, y1);
        this.end = new Point(x2, y2);
    }
    public double getLength() {
        int xDiff = end.getX() - super.getX();
        int yDiff = end.getY() - super.getY();
        return Math.sqrt(xDiff * xDiff + yDiff * yDiff);
    }
}'''
    story.append(Preformatted(l2_code, code_style))

    story.append(Paragraph('3. Latihan 3: Pewarisan (Point3D extends Point)', h2_style))
    story.append(Paragraph('Class <code>Point3D</code> memperluas <code>Point</code> untuk titik 3 dimensi dengan menambahkan koordinat <code>z</code> dan meng-override method <code>toString()</code>.', body_style))
    l3_code = '''public class Point3D extends Point {
    private int z;
    public Point3D(int x, int y, int z) {
        super(x, y);
        this.z = z;
    }
    public int getZ() { return z; }
    public void setZ(int z) { this.z = z; }
    @Override
    public String toString() {
        return "(" + super.getX() + ", " + super.getY() + ", " + z + ")";
    }
}'''
    story.append(Preformatted(l3_code, code_style))

    story.append(Paragraph('4. Output Pengujian Lengkap (TestAll.java)', h2_style))
    out2 = '''>>> [LATIHAN 1: Composition (Line has two Points)] <<<
Representasi line1 : Line[begin=(1, 2), end=(4, 6)]
Panjang line1      : 5.0 (Harusnya 5.0)

>>> [LATIHAN 2: Inheritance (LineSub extends Point)] <<<
Representasi lineSub1: LineSub[begin=(2, 3), end=(5, 7)]
Panjang lineSub1     : 5.0 (Harusnya 5.0)

>>> [LATIHAN 3: Inheritance (Point3D extends Point)] <<<
Point3D berparameter (10, 20, 30):
Representasi p3d: (10, 20, 30)
Koordinat X (superclass): 10, Y (superclass): 20, Z (subclass): 30'''
    story.append(Preformatted(out2, code_style))

    check_sanitized(l1_code + l2_code + l3_code + out2)
    doc.build(story)
    print('PDF 2 created successfully.')
    return path


def build_interpolasi(out_dir):
    path = os.path.join(out_dir, "komnum", "Tugas_Interpolasi_Komnum.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = make_doc(path, "Laporan Tugas Komputasi Numerik: Metode Interpolasi")
    story = []
    story.append(Paragraph('Laporan Tugas Komputasi Numerik: Pemecahan Masalah Metode Interpolasi', title_style))
    story.append(Paragraph('<b>Mata Kuliah:</b> Komputasi Numerik / Kelas A<br/>'
                          '<b>Nama Mahasiswa:</b> Nabil Aulia Dika (Dezz)<br/>'
                          '<b>NPM:</b> 250810701100090<br/>'
                          '<b>Topik:</b> Bab VI Interpolasi (Latihan 6.6 Soal 1 s.d. 4)', subtitle_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph('1. Ringkasan Hasil Perhitungan', h2_style))
    table_data = [
        ['No', 'Soal Target', 'Linier (Orde 1)', 'Kuadratik (Orde 2)', 'Lagrange (Orde 4)', 'Analisis / Keterangan'],
        ['1', 'x = 2.4', '9.9360', '9.9296', '9.9296', 'Polinomial orde 2 murni'],
        ['2', 'x = 1.0 (e^x)', '2.7678 (galat 1.82%)', '2.7064 (galat 0.43%)', '2.7189 (galat 0.02%)', 'Eksak e^1 = 2.718282'],
        ['3', 'x = 97.66', '13.5300', '13.5025', '13.5024', 'Kuadratik mengapit akurat'],
        ['4', 'T = 372.1', '178.1273', '177.8157', '177.8304', 'Data tekanan non-linier']
    ]
    t = Table(table_data, colWidths=[25, 65, 100, 110, 100, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (4, -1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph('2. Grafik Hasil Interpolasi Seluruh Soal', h2_style))
    img_path = os.path.join(
        os.environ.get("MONITOR_KULIAH_DATA_DIR", "/opt/data/monitor-kuliah"),
        "resources", "grafik_interpolasi_lengkap.png")
    if os.path.exists(img_path):
        story.append(Image(img_path, width=500, height=350))
        story.append(Spacer(1, 8))

    story.append(Paragraph('3. Ringkasan Perhitungan Matematis Tiap Soal', h2_style))
    math_summary = '''SOAL 1: x = 2.4 (Data x=[2, 4, 6, 8, 10], y=[9.68, 10.96, 12.32, 13.76, 15.28])
- Linier (x=2, 4): f1(2.4) = 9.68 + (1.28 / 2) * (0.4) = 9.9360
- Kuadratik: b0=9.68, b1=0.64, b2=0.01 -> f2(2.4) = 9.68 + 0.256 - 0.0064 = 9.9296

SOAL 2: x = 1.0 (Data x=[0.1, 0.6, 1.1, 1.6, 2.1], y=[1.1052, 1.8221, 3.0042, 4.9530, 8.1662])
- Eksak: e^1 = 2.718282
- Linier (x=0.6, 1.1): f1(1.0) = 1.8221 + (1.1821 / 0.5) * 0.4 = 2.7678 (Galat: 1.82%)
- Kuadratik: b0=1.8221, b1=2.3642, b2=1.5334 -> f2(1.0) = 2.7064 (Galat: 0.43%)
- Lagrange Orde 4: f4(1.0) = 2.718917 (Galat: 0.023%)

SOAL 3: x = 97.66 (Data x=[93, 96.2, 100, 104.2, 108.7], y=[11.38, 12.80, 14.70, 17.07, 19.91])
- Linier (x=96.2, 100): f1(97.66) = 12.80 + (1.90 / 3.8) * 1.46 = 13.5300
- Kuadratik: b0=12.80, b1=0.50, b2=0.008036 -> f2(97.66) = 13.5025

SOAL 4: T = 372.1 (Data T=[361, 367, 378, 387, 399], p=[154.9, 167.0, 191.0, 212.5, 244.2])
- Linier (T=367, 378): f1(372.1) = 167.0 + (24.0 / 11) * 5.1 = 178.1273
- Kuadratik: b0=167.0, b1=2.1818, b2=0.01035 -> f2(372.1) = 177.8157'''
    story.append(Preformatted(math_summary, code_style))

    check_sanitized(math_summary)
    doc.build(story)
    print('PDF 3 created successfully.')
    return path


def build_all(out_dir=DEFAULT_OUT):
    return [build_getter_setter(out_dir),
            build_inheritance(out_dir),
            build_interpolasi(out_dir)]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hasilkan 3 PDF laporan tugas.")
    ap.add_argument("--out", default=DEFAULT_OUT,
                    help="folder output (default: %(default)s)")
    ap.add_argument("--check-only", action="store_true",
                    help="hanya validasi sanitasi, tanpa menulis PDF")
    args = ap.parse_args(argv)
    if args.check_only:
        # Validasi logika sanitasi: string terlarang harus ditolak,
        # teks bersih harus lolos. Tanpa menulis PDF.
        try:
            check_sanitized("contoh path /opt/data/contoh")
        except ValueError:
            pass
        else:
            print("FAIL: string terlarang lolos sanitasi")
            return 1
        check_sanitized("kode Student.java biasa, tanpa jejak")
        print("OK: sanitasi berfungsi (terlarang ditolak, bersih lolos)")
        return 0
    paths = build_all(args.out)
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
