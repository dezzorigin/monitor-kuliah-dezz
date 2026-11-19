# Pengerjaan Tugas & PDF Siap Kumpul

> Dipindah dari `04_MENGERJAKAN_TUGAS_DAN_PDF/` tanpa mengubah isi.

# Alur Pengerjaan Tugas & Pembuatan PDF Siap Kumpul

Ketika sebuah tugas baru terdeteksi di Moodle atau Google Classroom, asisten secara otomatis menjalankan prosedur berikut:

---

## 1. Analisis Kebutuhan Tugas (Requirements Breakdown)
1. Ekstrak teks deskripsi, batas waktu, dan lampiran PDF/DOCX dari dosen.
2. Identifikasi parameter kunci:
   - Bahasa pemrograman & compiler (contoh: Java 21 LTS, Python 3.12, PostgreSQL).
   - Format deliverable yang diminta (file `.java` murni, file `.zip`, atau laporan `.pdf`).
   - Aturan khusus (misal: "wajib enkapsulasi private", "metode Lagrange", "tugas kelompok vs individu").

---

## 2. Implementasi & Pengujian Kode
1. Tulis kode solusi yang modular dan bersih di folder kerja `/opt/data/monitor-kuliah/<mk>/`.
2. Lakukan kompilasi dan pengujian langsung di terminal:
   ```bash
   # Contoh uji Java:
   javac Student.java Main.java && java Main
   
   # Contoh uji Python:
   python3 interpolasi.py
   ```
3. Uji kasus batas (boundary test cases):
   - Uji input valid standar.
   - Uji input ekstrim / error handling (misal: input IPK negatif atau > 4.0 harus ditolak).
   - Pastikan exit code adalah `0`.

---

## 3. Pembuatan Laporan PDF Menggunakan ReportLab
Gunakan skrip `generate_pdfs.py` untuk menghasilkan dokumen PDF akademik yang rapi dan elegan:
- **Header Resmi**:
  - Judul Tugas (misal: *Laporan Praktikum Pemrograman Berorientasi Objek*)
  - Identitas Mahasiswa:
    - **Nama**: Nabil Aulia Dika
    - **NPM**: 250810701100090
    - **Mata Kuliah / Kelas**: Pemrograman Berorientasi Objek / Kelas A
    - **Program Studi**: S1 Sistem Informasi — Universitas Syiah Kuala
- **Struktur Isi**:
  1. Landasan Teori & Tujuan
  2. Implementasi Kode Sumber (syntax highlighted/monospace block)
  3. Bukti Eksekusi & Screenshot Output Program
  4. Pembahasan & Analisis Hasil

---

## 4. Aturan Sanitasi Metadata (Pembersihan Jejak Server)
**PENTING**: Dokumen yang akan dikumpulkan ke dosen **DILARANG KERAS** memuat jejak internal server penguji:
- Pastikan tidak ada string `/opt/data/...`, nama host server, atau direktori linux di dalam teks PDF maupun di metadata PDF (`Creator`, `Producer`, `Author`).
- Periksa dengan script pembersih:
  ```python
  import pypdf
  reader = pypdf.PdfReader("Laporan.pdf")
  text = "".join(p.extract_text() for p in reader.pages)
  assert "/opt" not in text and "hermes" not in text
  ```

---

## Aturan Sanitasi Dokumen & Metadata PDF

# Aturan Sanitasi Dokumen & Metadata PDF

## Mengapa Sanitasi Mutlak Diperlukan?
Ketika tugas dikerjakan dan di-compile di lingkungan server penguji, compiler atau PDF generator (ReportLab / WeasyPrint / LibreOffice) dapat secara otomatis menyematkan metadata lingkungan ke dalam berkas:
- Jalur file lokal: `/opt/data/monitor-kuliah/...`
- Nama user host: `hermes` / `ubuntu`
- Versi OS server: `Linux x86_64`

Jika file tersebut diunggah ke portal kampus dan diperiksa oleh dosen, metadata tersebut dapat membocorkan bahwa pengerjaan dilakukan di lingkungan server otomasi.

## Prosedur Pembersihan:
1. **ReportLab Canvas Metadata**:
   Saat menginisialisasi `SimpleDocTemplate`:
   ```python
   doc = SimpleDocTemplate(
       pdf_path,
       pagesize=letter,
       author="Nabil Aulia Dika",
       title="Laporan Praktikum",
       creator="Microsoft Word",  # Samarkan creator
       producer="macOS Version 14.5 (Build 23F79) Quartz PDFContext"
   )
   ```
2. **Pembersihan String Body**:
   Pastikan tidak ada teks console log atau output terminal yang mencantumkan nama path Linux server. Ganti semua path dengan path generik mahasiswa:
   - SALAH: `/opt/data/monitor-kuliah/pbo/Student.java`
   - BENAR: `D:\Kuliah\Semester3\PBO\Student.java` atau cukup `Student.java`
3. **Verifikasi Otomatis (Assertion Check)**:
   ```python
   import pypdf
   reader = pypdf.PdfReader(pdf_path)
   text = "\n".join(page.extract_text() for page in reader.pages)
   for banned in ['/opt', 'data', 'monitor', 'hermes', 'home']:
       assert banned not in text.lower(), f"Terdeteksi kata terlarang '{banned}' di dalam PDF!"
   ```

---
