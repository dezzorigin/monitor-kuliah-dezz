#!/usr/bin/env python3
"""Monitor gate untuk cron absen-watcher-dezz.
Output konstan ('idle') di luar window kuliah -> agent skip.
Di dalam window: output berubah tiap tick (timestamp) -> agent jalan tiap interval.
MK yang sudah 'done' di absen_state.json dikeluarkan -> setelah absen, output balik 'idle'.

Jalur data via env MONITOR_KULIAH_DATA_DIR (default /opt/data/monitor-kuliah).
Pemakaian: python3 scripts/absen_gate.py
"""
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_schedule import HARI_MAP, TZ, load_jadwal  # noqa: E402

DATA_DIR = os.environ.get("MONITOR_KULIAH_DATA_DIR", "/opt/data/monitor-kuliah")
STATE_PATH = os.path.join(DATA_DIR, "absen_state.json")
WINDOW_PRE_MIN = 10
WINDOW_POST_MIN = 10  # setelah jam selesai kuliah


def load_done(state_path=STATE_PATH, now=None):
    """Map akun -> set kode MK done hari ini. Format baru 'akun' atau lama flat."""
    now = now or datetime.now(TZ)
    try:
        d = json.load(open(state_path))
    except Exception:
        return {"dezz": set(), "rizki": set()}
    if d.get("tanggal") != now.strftime("%Y-%m-%d"):
        return {"dezz": set(), "rizki": set()}
    if "akun" in d:
        return {k: set(v.get("done", [])) for k, v in d["akun"].items()}
    return {"dezz": set(d.get("done", [])), "rizki": set()}


def compute_gate(mata_kuliah, done_map, now):
    """Return list kode MK aktif (belum done di kedua akun, di dalam window).

    Window: 10 menit sebelum kelas mulai s/d 10 menit setelah jam selesai
    (dosen bisa buka presensi kapan pun selama jam kuliah).
    Fungsi murni supaya bisa diuji dengan waktu palsu.
    """
    hari_ini = HARI_MAP[now.strftime("%A")]
    done_both = done_map.get("dezz", set()) & done_map.get("rizki", set())
    aktif = []
    for mk in mata_kuliah:
        if mk["hari"] != hari_ini or mk["kode"] in done_both:
            continue
        mulai = datetime.strptime(mk["mulai"], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day, tzinfo=TZ)
        selesai = datetime.strptime(mk["selesai"], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day, tzinfo=TZ)
        if mulai - timedelta(minutes=WINDOW_PRE_MIN) <= now <= selesai + timedelta(minutes=WINDOW_POST_MIN):
            aktif.append(mk["kode"])
    return aktif


def main():
    now = datetime.now(TZ)
    try:
        mata_kuliah = load_jadwal()
    except FileNotFoundError:
        print("idle")
        return 0
    done_map = load_done(now=now)
    aktif = compute_gate(mata_kuliah, done_map, now)
    if not aktif:
        print("idle")
        return 0
    parts = []
    for k in aktif:
        pend = [a for a in ("dezz", "rizki") if k not in done_map.get(a, set())]
        parts.append(f"{k}(pending:{','.join(pend) or '-'})")
    print(" ".join(parts) + " @" + now.strftime("%H:%M"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
