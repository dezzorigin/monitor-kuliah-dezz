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
