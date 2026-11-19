# Submission & Cron

> Dipindah dari `05_SUBMISSION_DAN_CRON/` tanpa mengubah isi.

# Alur Pengumpulan Tugas (Submission) ke Moodle

## 1. Aturan Otorisasi Manusia (Human-in-the-Loop)
**Aturan Mengikat Soul**:
Asisten **TIDAK PERNAH** menekan tombol submit akhir ke sistem kampus sebelum Dezz melihat draft dan memberikan konfirmasi eksplisit (misal: *"Submit sekarang men"* atau *"Udah aman, kirimkan"*).

---

## 2. Alur Eksekusi Pengumpulan via Browser
Setelah Dezz mengonfirmasi:
1. Buka halaman submission tugas: `https://elearning.usk.ac.id/mod/assign/view.php?id=<ASSIGN_ID>`.
2. Klik tombol **"Add submission"** (atau **"Edit submission"** jika merevisi).
3. Unggah file dokumen PDF yang telah siap (misal: `Latihan_Getter_Setter_PBO.pdf`).
4. Klik tombol **"Save changes"**.
5. Baca kembali tabel ringkasan status pengumpulan:
   - Pastikan baris *Submission status* berubah menjadi: **Submitted for grading** (berwarna hijau).
   - Pastikan nama file muncul di baris *File submissions*.
   - Ambil screenshot bukti pengumpulan dan simpan di `evidence/submission_<ASSIGN_ID>.png`.
6. Laporkan bukti berhasil ke Discord Dezz.

---

## Penjadwalan Otomatis (Cron Jobs)

# Panduan Penjadwalan Otomatis (Cron Jobs)

Dua cron job utama yang mengoperasikan sistem pemantauan kuliah Dezz:

---

## 1. `absen-watcher-dezz` (Pemantau Presensi Kuliah)
- **ID Job**: `b033d7185cc3`
- **Jadwal**: Setiap 10 menit (`interval 10m`).
- **Mekanisme Hemat Resource (Monitor Gate)**:
  Job ini menggunakan `monitor_script: "absen_gate.sh"`.
  - Jika saat ini di luar jam kuliah (atau jika semua kelas hari ini sudah diabsen), script mengembalikan string `"idle"`.
  - Jika output bernilai `"idle"` (tidak berubah), AI Agent **tidak akan dibangunkan**, menghemat token dan resource server.
  - Begitu memasuki 10 menit sebelum kelas dimulai, output gate berubah memuat daftar kode MK yang aktif, sehingga agen otomatis aktif dan mengeksekusi absensi.

---

## 2. `monitor-tugas-dezz` (Pemantau Tugas & Pengumuman Moodle)
- **ID Job**: `1cd21a06adcb`
- **Jadwal**: 4 kali sehari pada jam 06:00, 12:00, 18:00, dan 00:00 WIB (`expr: "0 23,5,11,17 * * *"` UTC).
- **Tugas**:
  1. Login ke Moodle USK via credential vault.
  2. Memeriksa Linimasa Dashboard dan seluruh halaman 12 mata kuliah.
  3. Memeriksa Google Classroom jika sesi aktif.
  4. Melaporkan item baru, kuis, atau perubahan deadline ke channel Discord.

---
