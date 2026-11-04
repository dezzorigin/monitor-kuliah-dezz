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
