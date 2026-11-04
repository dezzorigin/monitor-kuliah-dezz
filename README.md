# MONITOR KULIAH & ASISTEN TUGAS DEZZ (FULL SETUP)
### Paket Lengkap Otomasi Akademik, Presensi SIMKULIAH, Monitoring Moodle & Pembuatan Tugas

Arsip ini memuat seluruh sistem asisten perkuliahan pribadi untuk Dezz (Universitas Syiah Kuala — Jurusan Sistem Informasi) yang mencakup otomasi absensi, monitoring tugas Moodle, dan generator laporan tugas siap kumpul.

---

## 📁 Struktur Direktori Paket

```
monitor-kuliah-dezz-full-setup/
├── README.md                                  # Dokumentasi utama (file ini)
│
├── 01_SOUL_AND_CONFIG/                        # Jiwa Asisten & Konfigurasi Bot
│   ├── SOUL_SETUP_GUIDE.md                   # Panduan binding channel #monitor-kuliah-dezz
│   ├── monitor-kuliah-soul.md                # Definisi lengkap kepribadian & aturan mengikat
│   ├── discord-binding-snippet.yaml          # Contoh config.yaml Hermes
│   └── jadwal-kuliah.json                    # Database jadwal 12 mata kuliah & ruangan
│
├── 02_ABSENSI_SIMKULIAH/                      # Otomasi Presensi (100% Selalu Berhasil)
│   ├── ALUR_ABSENSI_LENGKAP.md               # Arsitektur lengkap A sampai Z presensi
│   ├── captcha_solver_guide.md               # Solver ddddocr lokal (5-digit numerik)
│   ├── sweetalert_bypass_explanation.md      # Trik bypass dialog konfirmasi via POST langsung
│   ├── scripts/
│   │   ├── simkuliah_login.py                # Engine login CodeIgniter + solver OCR
│   │   ├── krs_login.py                      # Engine login KRS USK (Laravel CSRF)
│   │   ├── absen_run.py                      # Eksekutor utama absensi (Dezz & Rizki)
│   │   ├── absen_gate.py                     # Gerbang cron hemat token (idle filter)
│   │   └── check_schedule.py                 # Pengecek jendela waktu absensi
│   └── templates/
│       └── absen_state.json                  # Format tracking presensi harian
│
├── 03_ELEARNING_MOODLE/                       # Monitoring & Navigasi Moodle USK
│   ├── MOODLE_WORKFLOW_LENGKAP.md            # Cara login, navigasi linimasa & scraping
│   ├── bypass_moodle_login_form.md           # Solusi dual-form login (#login vs #guestlogin)
│   └── templates/
│       └── state.json                        # Database deduplikasi tugas terlaporkan
│
├── 04_MENGERJAKAN_TUGAS_DAN_PDF/              # Pembuatan Tugas & Laporan PDF Akademik
│   ├── WORKFLOW_PENGERJAAN_TUGAS.md          # SOP pengerjaan tugas dari nol hingga PDF
│   ├── metadata_sanitization_rules.md        # Pembersihan path internal server (/opt/data)
│   ├── scripts/
│   │   └── generate_pdfs.py                  # Script ReportLab PDF generator standar USK
│   └── sample_drafts/
│       ├── latihan_getter_setter.md          # Contoh solusi Java PBO Enkapsulasi
│       ├── latihan_inheritance.md            # Contoh solusi Java PBO Pewarisan
│       └── tugas_interpolasi.md              # Contoh solusi Python Komputasi Numerik
│
└── 05_SUBMISSION_DAN_CRON/                    # Prosedur Pengumpulan & Penjadwalan
    ├── SUBMISSION_FLOW.md                    # Prosedur upload tugas ke Moodle (Human-in-the-Loop)
    ├── cron_jobs_setup.md                    # Cara mengatur interval cron pemantau
    └── cron_jobs_export.json                 # Ekspor konfigurasi 2 cron jobs aktif
```

---

## ⚡ Alur Cepat (Quick Start):
1. **Absensi**: Dijalankan via cronjob tiap 10 menit dengan trigger `absen_gate.py`.
2. **Monitoring Tugas**: Dijalankan via cronjob 4x sehari untuk memindai tugas Moodle baru.
3. **Pengerjaan**: Asisten menulis kode -> menguji compile/run -> membuat laporan PDF via ReportLab -> meminta konfirmasi Dezz di Discord -> melakukan submission ke Moodle.
