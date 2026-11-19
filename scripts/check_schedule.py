#!/usr/bin/env python3
"""Cek apakah sekarang dalam window absen. Output: JSON list MK yang aktif.

Jadwal dibaca dari ``<DATA_DIR>/jadwal.json`` dan status absen dari
``<DATA_DIR>/absen_state.json``. ``DATA_DIR`` diambil dari env
``MONITOR_KULIAH_DATA_DIR`` (default ``/opt/data/monitor-kuliah`` —
jalur server Hermes; di repo ini contohnya ada di ``data/``).

Format state yang didukung: baru (``{"akun": {"dezz": {"done": [...]}}}``)
dan lama (``{"done": [...]}`` — flat).

Pemakaian:
    python3 scripts/check_schedule.py
    MONITOR_KULIAH_DATA_DIR=data python3 scripts/check_schedule.py
"""
import json
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

DATA_DIR = os.environ.get("MONITOR_KULIAH_DATA_DIR", "/opt/data/monitor-kuliah")
JADWAL_PATH = os.path.join(DATA_DIR, "jadwal.json")
STATE_PATH = os.path.join(DATA_DIR, "absen_state.json")
TZ = ZoneInfo("Asia/Jakarta")
WINDOW_PRE_MIN = 15   # mulai cek 15 menit sebelum kelas
WINDOW_POST_MIN = 30  # stop cek 30 menit setelah kelas mulai

HARI_MAP = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu",
    "Sunday": "Minggu",
}


def load_absen_done(state_path=STATE_PATH, now=None):
    """Return set kode MK yang sudah absen hari ini (semua akun)."""
    now = now or datetime.now(TZ)
    try:
        with open(state_path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return set()
    if data.get("tanggal") != now.strftime("%Y-%m-%d"):
        return set()
    done = set()
    if isinstance(data.get("akun"), dict):
        for akun in data["akun"].values():
            done |= set(akun.get("done", []))
    done |= set(data.get("done", []))
    return done


def load_jadwal(jadwal_path=JADWAL_PATH):
    """Baca jadwal; terima `jadwal.json` (nama server) atau
    `jadwal-kuliah.json` (nama file contoh di repo ini)."""
    candidates = [jadwal_path]
    if jadwal_path.endswith("jadwal.json"):
        candidates.append(jadwal_path.replace("jadwal.json", "jadwal-kuliah.json"))
    for path in candidates:
        try:
            with open(path) as f:
                return json.load(f)["mata_kuliah"]
        except FileNotFoundError:
            continue
    raise FileNotFoundError(candidates[0])


def active_courses(mata_kuliah, done, now):
    """MK yang harinya cocok, belum absen, dan now di dalam window.

    Window: 15 menit sebelum jam mulai s/d 30 menit setelah jam mulai.
    Fungsi murni (tanpa I/O) supaya bisa diuji dengan waktu palsu.
    """
    hari_ini = HARI_MAP[now.strftime("%A")]
    aktif = []
    for mk in mata_kuliah:
        if mk["hari"] != hari_ini:
            continue
        if mk["kode"] in done:
            continue  # sudah absen hari ini
        mulai = datetime.strptime(mk["mulai"], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day, tzinfo=TZ
        )
        win_start = mulai - timedelta(minutes=WINDOW_PRE_MIN)
        win_end = mulai + timedelta(minutes=WINDOW_POST_MIN)
        if win_start <= now <= win_end:
            aktif.append({
                "kode": mk["kode"],
                "nama": mk["nama"],
                "kelas": mk["kelas"],
                "jam": f'{mk["mulai"]}-{mk["selesai"]}',
                "ruang": mk["ruang"],
                "window_start": win_start.isoformat(),
                "window_end": win_end.isoformat(),
            })
    return aktif


def main():
    now = datetime.now(TZ)
    try:
        mata_kuliah = load_jadwal()
    except FileNotFoundError:
        print(f"jadwal tidak ditemukan: {JADWAL_PATH}", file=sys.stderr)
        print("set MONITOR_KULIAH_DATA_DIR ke folder berisi jadwal.json "
              "(contoh: data/)", file=sys.stderr)
        return 1
    done_today = load_absen_done(now=now)
    aktif = active_courses(mata_kuliah, done_today, now)
    print(json.dumps({"now": now.isoformat(), "hari": HARI_MAP[now.strftime("%A")],
                      "absen_aktif": aktif}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
