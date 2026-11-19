# PRD — Monitor Kuliah Dezz

## 1. Informasi Proyek

| Field | Nilai |
|---|---|
| Nama Proyek | Monitor Kuliah Dezz |
| Tech Stack | Python 3.12 (requests, ddddocr, cryptography, reportlab) + landing HTML/CSS/JS statis |
| Status | Dalam pengembangan aktif — dipakai harian via cron Hermes sejak Sep 2026 |
| Penanggung Jawab | Nabil Aulia Dika (Dezz) |
| Versi Dokumen | 2.0 (proper P1 #47, 19 Nov 2026) |
| Tanggal | 2026-11-19 |

## 2. Latar Belakang

Dezz kuliah S1 Sistem Informasi USK, 13 MK / 21 SKS, Senin–Sabtu.
Presensi SIMKULIAH hanya dibuka dosen selama jam kuliah (jendela ~10
menit) dan tugas tersebar di Moodle (12 course) + Google Classroom
(2 akun). Mengecek semuanya manual tiap hari tidak scalable — karena
itu ada otomasi ini: gerbang cron yang hemat token, login + captcha
otomatis, dan laporan terstruktur ke Discord.

## 3. Masalah yang Diselesaikan

1. **Absen kelewat jendela** — dosen buka presensi kapan saja selama jam
   kuliah; watcher cek tiap 10 menit dan absen begitu tombol muncul.
2. **Tugas terlewat** — Moodle + Classroom dipindai 4x/hari, item baru /
   perubahan deadline dilaporkan sekali (dedupe hash instruksi).
3. **Draft tugas lambat jadi PDF** — `generate_pdfs.py` menghasilkan
   laporan siap kumpul dengan metadata yang sudah disanitasi.
4. **Submit tanpa sengaja** — aturan keras: tidak ada submit/kuis/ujian
   sebelum Dezz mengonfirmasi draft.

## 4. Tujuan & Sasaran

- Absen masuk dalam jendela setiap sesi yang dibuka dosen (target: 100%
  sesi terpantau; bukti: `absen_state.json`).
- Nol laporan tugas duplikat (dedupe hash di `state.json`).
- Nol kredensial bocor ke repo (gitleaks seluruh riwayat, CI wajib hijau).
- Draft PDF lolos sanitasi metadata sebelum dikumpulkan.

## 5. Ruang Lingkup

### In Scope
- Watcher absensi SIMKULIAH (2 akun: Dezz & Rizki) + login KRS.
- Monitor Moodle USK + Google Classroom (baca + lapor saja).
- Draft tugas + PDF (ReportLab) + sanitasi metadata.
- Soul Discord + cron Hermes + landing etalase statis.

### Out of Scope
- Mengerjakan / submit kuis & ujian otomatis (hanya dilaporkan).
- Submit tugas tanpa konfirmasi eksplisit Dezz.
- Infrastruktur production selain cron + vault di VPS Hermes.
- Menyimpan kredensial apa pun di repo.

## 6. Fitur & Persyaratan Fungsional

| # | Fitur | Kriteria |
|---|---|---|
| F1 | Gerbang absen (`absen_gate.py`) | `idle` di luar jam kuliah; MK aktif 10 mnt sebelum s/d 10 mnt setelah selesai |
| F2 | Window absen (`check_schedule.py`) | MK aktif 15 mnt sebelum s/d 30 mnt setelah jam mulai; MK done dikeluarkan |
| F3 | Login SIMKULIAH | Session-bound captcha, OCR ddddocr lokal, retry ≤ 6x |
| F4 | Konfirmasi presensi | Ekstrak 7 parameter inline (Pola A 2026 + Pola B legacy + fallback onclick), POST langsung, verifikasi ulang |
| F5 | Multi-akun | Parameter diekstrak per akun (kelas bisa beda per praktikum) |
| F6 | Monitor Moodle/GCR | Linimasa + per-course; dedupe hash; lapor format `SUMBER \| MK \| Item \| Deadline \| Status \| Aksi` |
| F7 | Draft + PDF | 3 PDF contoh (getter/setter, inheritance, interpolasi); metadata disanitasi |
| F8 | Mode demo | `absen_run.py --demo`: parse fixture lokal, tanpa vault/jaringan/login |
| F9 | Landing etalase | Buku log satu kolom + jadwal 13 MK + OG preview, deploy Cloudflare Pages |

## 7. Persyaratan Non-Fungsional

- **Keamanan:** rahasia tidak boleh ter-commit (`.env` + vault di luar repo,
  gitleaks CI); sandi tidak pernah di-print/di-log.
- **Keandalan:** login retry captcha; verifikasi ulang pasca-POST; state
  ditulis tiap run.
- **Hemat resource:** gerbang `idle` mencegah agen bangun di luar jam kuliah.
- **Portabilitas:** jalur data via env `MONITOR_KULIAH_DATA_DIR` (default
  `/opt/data/monitor-kuliah`); dapat dijalankan di Linux/macOS/Windows
  untuk mode demo + tes.
- **Keterujian:** 26 tes tanpa jaringan/kredensial; e2e landing hanya di CI.

## 8. Arsitektur & Tech Stack

Lihat [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) (diagram SVG).
Python 3.12: `requests`, `urllib3`, `cryptography` (vault Fernet),
`ddddocr` + `pillow` (OCR captcha), `reportlab` (PDF), `pypdf`
(verifikasi sanitasi). Landing: HTML + CSS + JS tanpa build step.

## 9. Milestone / Roadmap

| Fase | Status |
|---|---|
| Soul + docs awal (folder 01_–05_) | ✅ Sep–Okt 2026 |
| Absensi otomatis terbukti (SINF2023, 15 Okt 2026) | ✅ |
| Draft + PDF tugas (PBO, Komnum) | ✅ |
| Proper P1 #47: docs/ rapi, tes, CI, landing, deploy | ✅ 19 Nov 2026 |
| Screenshot + video demo landing (browser live) | ⏳ follow-up |
| Verifikasi login Moodle/GCR pasca-rotate sesi | ⏳ operasional |

## 10. Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| Kredensial bocor ke repo | Vault Fernet di luar repo + gitleaks seluruh riwayat di CI |
| CAPTCHA gagal / berubah format | Retry 6x gambar baru; parser Pola A + B + fallback |
| SweetAlert tidak stabil diklik | POST langsung, bypass dialog |
| Sesi Moodle/GCR kedaluwarsa | Lapor + skip; re-login manual (tidak ditebak) |
| Submit tanpa izin | Aturan keras soul + human-in-the-loop |
| Jejak server di PDF | Sanitasi metadata + teks, ditegakkan `generate_pdfs.py` + tes |
| Dependency usang / rentan | Pin di `requirements.txt` + OSV sweep di CI |

## 11. Kriteria Keberhasilan

- `absen_run.py --demo` + 26 tes hijau tanpa kredensial.
- CI hijau penuh (ruff, pytest, gitleaks, OSV, gate statis, e2e, smoke).
- Landing live di Cloudflare Pages dengan OG preview lengkap.
- Tidak ada secret yang ter-commit (gitleaks 0 temuan).

## 12. Lampiran

- Arsitektur: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Testing: [docs/TESTING.md](docs/TESTING.md)
- Deployment: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- Desain landing: [docs/DESIGN.md](docs/DESIGN.md)
- Lisensi: MIT (LICENSE)
