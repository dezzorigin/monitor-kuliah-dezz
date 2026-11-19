# Testing — Monitor Kuliah Dezz

Semua tes jalan tanpa jaringan, tanpa kredensial, dan tanpa login nyata
ke sistem kampus.

## Menjalankan

```bash
python3 -m unittest discover -s tests -v   # stdlib, tanpa install apa pun
# atau, setelah pip install -r requirements.txt:
python3 -m pytest tests/ -q
```

## Cakupan (26 tes, 2 skip lokal tanpa reportlab)

| File | Yang diuji |
|---|---|
| `tests/test_schedule.py` | Jadwal 13 MK / 21 SKS; bentrok Sabtu 08:00; window absen (15 mnt sebelum s/d 30 mnt setelah mulai); MK done dikeluarkan; Minggu kosong; gerbang idle/aktif; `load_done` format baru + lama |
| `tests/test_parser.py` | `parse_absensi`: Pola A (format 2026), Pola B (legacy), fallback onclick, status teks (`sudah absen`, `dosen belum absen`), halaman kosong |
| `tests/test_demo.py` | `absen_run.py --demo` end-to-end (fixture lokal, tanpa POST/login/vault); sanitasi PDF menolak string terlarang; build 3 PDF + metadata bersih (skip lokal kalau reportlab belum terpasang — jalan di CI) |

## Mode demo (dry-run)

```bash
python3 scripts/absen_run.py --demo
```

Output nyata (19 Nov 2026, 16:51 WIB):

```json
{
 "mode": "demo",
 "ts": "2026-11-19T16:51:59+07:00",
 "status_teks": "belum masuk waktu absen",
 "mk_terlihat": ["SINF2009", "SINF2015"],
 "hasil": [
  {
   "mk": "SINF2015",
   "id_tombol": "6819201",
   "params": {"kelas": "A", "kd_mt_kul8": "SINF2015",
              "jadwal_mulai": "08:00", "jadwal_berakhir": "09:40",
              "pertemuan": "7", "sks_mengajar": "2", "id": "6819201"},
   "aksi": "demo: TIDAK di-POST (mode aman)"
  }
 ]
}
```

## Cek jadwal & gerbang (data contoh)

```bash
MONITOR_KULIAH_DATA_DIR=data python3 scripts/check_schedule.py
# Kamis 19 Nov 2026 16:51 WIB → absen_aktif: SINF2023 Sistem Operasi 16:35–18:15
MONITOR_KULIAH_DATA_DIR=data python3 scripts/absen_gate.py
# → SINF2023(pending:dezz,rizki) @16:52
```

## Yang TIDAK dites di sini

- Login nyata ke SIMKULIAH / KRS / Moodle (butuh kredensial vault + sesi
  kampus) — hanya jalan di server Hermes, bukan di CI.
- Playwright e2e landing — hanya di CI (job `playwright-e2e`).
- Screenshot / video demo landing — follow-up browser live (Chrome lokal
  tidak bisa start di VM dev).
