# Deployment — Monitor Kuliah Dezz

Dua hal yang di-deploy, dan keduanya berbeda:

## 1. Automation (server Hermes — BUKAN repo ini yang di-deploy)

Skrip di `scripts/` berjalan di VPS Hermes sebagai cron + soul Discord.
Tidak ada proses deploy dari repo ini ke server — file disalin ke
`/opt/data/monitor-kuliah/scripts/` di server, lalu cron
`absen-watcher-dezz` (tiap 10 menit) dan `monitor-tugas-dezz`
(06:00/12:00/18:00/00:00 WIB) menjalankannya. Detail cron:
`docs/submission-cron.md`.

Yang harus ada di server (di luar repo):

- `MONITOR_KULIAH_DATA_DIR` = `/opt/data/monitor-kuliah` berisi
  `jadwal.json`, `absen_state.json`, `state.json`, folder `evidence/`,
  `drafts/`, `tmp/`.
- Vault Fernet di `/opt/data/vault/vault.key` + `vault.json.enc`.
- venv captcha: `.venv-captcha` berisi `ddddocr`, `pillow`, `requests`.
- `requirements.txt` untuk dependensi Python (`requests`, `urllib3`,
  `cryptography`, `ddddocr`, `pillow`, `reportlab`, `pypdf`).

## 2. Landing (Cloudflare Pages — yang di-deploy dari repo ini)

Hanya folder `landing/` yang di-deploy — BUKAN seluruh repo, supaya file
state, evidence, dan draft tidak ikut publik.

```bash
python3 ~/workspace/github-actions/cf_pages.py deploy monitor-kuliah-dezz landing/
```

- Project: `monitor-kuliah-dezz` → `https://monitor-kuliah-dezz.pages.dev/`
- Isi deploy: `index.html`, `styles.css`, `app.js`, `favicon.svg`,
  `og-image.png` (5 file, statis, tanpa build step).
- Verifikasi live: root 200 + judul + semua tag OG/Twitter + `og-image.png`
  200 dengan `Content-Type: image/*`.

## CI

`.github/workflows/ci.yml` (7 job, semua harus hijau sebelum merge):

| Job | Isi |
|---|---|
| `python-test` | `py_compile` semua `.py` + pytest 26 tes (tanpa jaringan/kredensial) |
| `lint-ruff` | `ruff check .` (E4/E7/E9/F) |
| `gitleaks` | secret-scan seluruh riwayat (`fetch-depth: 0`) — WAJIB hijau |
| `advisory-sweep` | OSV batch dependensi produksi PyPI — HIGH/CRITICAL = gagal |
| `static-checks` | gate P0 anti-slop + tag OG/Twitter + data asli repo |
| `playwright-e2e` | landing di server lokal (desktop + mobile) — HANYA di CI |
| `smoke` | file deploy ada & tidak kosong, og-image ≥ 10 KB |
