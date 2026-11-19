# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Proper P1 #47 (19 Nov 2026): folder `01_`–`05_` dirapikan menjadi `docs/`
  (soul, absensi-simkuliah, moodle, tugas-pdf, submission-cron) tanpa
  mengubah isi; contoh state + jadwal pindah ke `data/`.
- `scripts/` portabel: jalur data via `MONITOR_KULIAH_DATA_DIR`, vault via
  env; `absen_run.py --demo` (mode aman tanpa vault/jaringan/login).
- `tests/`: 26 tes unittest (jadwal, jendela absen, parser Pola A/B,
  demo, sanitasi PDF) — tanpa jaringan/kredensial.
- CI (`.github/workflows/ci.yml`): ruff, pytest, gitleaks (riwayat penuh),
  advisory-sweep OSV, gate statis landing, Playwright e2e (CI saja), smoke.
- Landing etalase statis `landing/` (buku log / arsip absensi) + og-image
  PIL, deploy Cloudflare Pages (`monitor-kuliah-dezz.pages.dev`).
- `requirements.txt` (dependensi produksi dipin), `pyproject.toml` (ruff),
  `.env.example`, `docs/ARCHITECTURE.md` (+ diagram SVG), `docs/TESTING.md`,
  `docs/DEPLOYMENT.md`, `docs/DESIGN.md`.

### Changed
- README + PRD ditulis ulang dari template generik menjadi isi nyata repo
  (alur absensi, sistem yang dipantau, aturan keras, output demo asli).
- `generate_pdfs.py`: dibungkus fungsi + argumen `--out`, metadata PDF
  disanitasi eksplisit (author/creator/producer), cek string terlarang.
- `simkuliah_login.py` / `krs_login.py`: `ddddocr` di-import malas supaya
  modul bisa di-import tanpa OCR (demo + tes).
- `check_schedule.py`: `load_absen_done` mendukung format state baru
  (`akun`) dan lama (flat); `load_jadwal` menerima `jadwal-kuliah.json`.
- `absen_run.py`: pemetaan tombol → MK memakai `kd_mt_kul8` dari script
  inline dulu (format 2026), fallback posisi terdekat.

### Fixed
- `check_schedule.py` sebelumnya crash `FileNotFoundError` di luar server
  (jalur `/opt/data/...` hardcode tanpa pesan jelas) — sekarang ada pesan
  + env override + contoh data di `data/`.
- `absen_run.py` sebelumnya memetakan tombol ke MK tetangga yang salah
  (heuristik jarak di HTML contoh: SINF2009, seharusnya SINF2015).

## [1.0.0] - 2026-10-15

### Added
- Soul monitor-kuliah (Discord #monitor-kuliah-dezz) + panduan setup.
- Alur absensi SIMKULIAH lengkap (captcha ddddocr, bypass SweetAlert,
  multi-akun Dezz & Rizki) + skrip `absen_run.py`, `simkuliah_login.py`,
  `krs_login.py`, `absen_gate.py`, `check_schedule.py`.
- Workflow Moodle (dual-form login) + dedupe `state.json`.
- Workflow pengerjaan tugas + `generate_pdfs.py` (3 PDF) + aturan
  sanitasi metadata.
- Submission flow + cron jobs (`absen-watcher-dezz`, `monitor-tugas-dezz`).
- README, PRD, LICENSE MIT, CHANGELOG, CODE_OF_CONDUCT.
