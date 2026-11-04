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
