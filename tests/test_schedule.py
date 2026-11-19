"""Tes jadwal + jendela absen (scripts/check_schedule.py, scripts/absen_gate.py).

Tanpa jaringan, tanpa kredensial, tanpa login nyata. Waktu dipalsukan
via parameter `now` pada fungsi murni.
"""
import os
import sys
import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from check_schedule import active_courses, load_absen_done, load_jadwal
from absen_gate import compute_gate, load_done

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo("Asia/Jakarta")


def dt(iso):
    return datetime.fromisoformat(iso).replace(tzinfo=TZ)


class TestJadwal(unittest.TestCase):
    def setUp(self):
        self.jadwal = load_jadwal(
            os.path.join(ROOT, "data", "jadwal-kuliah.json"))

    def test_jumlah_mk_dan_sks(self):
        self.assertEqual(len(self.jadwal), 13)
        self.assertEqual(sum(mk["sks"] for mk in self.jadwal), 21)

    def test_sabtu_bentrok_dua_mk_jam_sama(self):
        sabtu = [m for m in self.jadwal if m["hari"] == "Sabtu"]
        self.assertEqual(len(sabtu), 2)
        self.assertEqual({m["mulai"] for m in sabtu}, {"08:00"})
        self.assertEqual({m["kode"] for m in sabtu},
                         {"SINF2017", "MKWU2001"})

    def test_semua_mk_punya_ruang_dan_kelas(self):
        for mk in self.jadwal:
            self.assertTrue(mk["ruang"])
            self.assertTrue(mk["kelas"])
            self.assertIn(mk["jenis"], ("teori", "praktikum"))


class TestWindowAbsen(unittest.TestCase):
    def setUp(self):
        self.jadwal = load_jadwal(
            os.path.join(ROOT, "data", "jadwal-kuliah.json"))

    def test_di_dalam_window_15_menit_sebelum_mulai(self):
        # Rabu 07:50 — PBO (SINF2015) mulai 08:00, window buka 07:45.
        aktif = active_courses(self.jadwal, set(), dt("2026-10-14T07:50:00"))
        self.assertEqual([a["kode"] for a in aktif], ["SINF2015"])

    def test_di_luar_window_terlalu_awal(self):
        aktif = active_courses(self.jadwal, set(), dt("2026-10-14T07:44:00"))
        self.assertEqual(aktif, [])

    def test_di_dalam_window_30_menit_setelah_mulai(self):
        aktif = active_courses(self.jadwal, set(), dt("2026-10-14T08:30:00"))
        self.assertEqual([a["kode"] for a in aktif], ["SINF2015"])

    def test_di_luar_window_terlalu_telat(self):
        aktif = active_courses(self.jadwal, set(), dt("2026-10-14T08:31:00"))
        self.assertEqual(aktif, [])

    def test_mk_sudah_absen_dikeluarkan(self):
        aktif = active_courses(self.jadwal, {"SINF2015"},
                               dt("2026-10-14T07:50:00"))
        self.assertEqual(aktif, [])

    def test_minggu_tidak_ada_kuliah(self):
        aktif = active_courses(self.jadwal, set(), dt("2026-10-18T08:00:00"))
        self.assertEqual(aktif, [])

    def test_sabtu_kedua_mk_aktif_bersama(self):
        # Sabtu 08:00 — dua MK bentrok, keduanya dicek.
        aktif = active_courses(self.jadwal, set(), dt("2026-10-17T08:00:00"))
        self.assertEqual({a["kode"] for a in aktif},
                         {"SINF2017", "MKWU2001"})


class TestGate(unittest.TestCase):
    def setUp(self):
        self.jadwal = load_jadwal(
            os.path.join(ROOT, "data", "jadwal-kuliah.json"))

    def test_gate_idle_di_luar_jam(self):
        self.assertEqual(
            compute_gate(self.jadwal, {"dezz": set(), "rizki": set()},
                         dt("2026-10-14T12:00:00")), [])

    def test_gate_aktif_di_dalam_jam_kuliah(self):
        self.assertEqual(
            compute_gate(self.jadwal, {"dezz": set(), "rizki": set()},
                         dt("2026-10-14T08:30:00")), ["SINF2015"])

    def test_gate_idle_kalau_done_kedua_akun(self):
        done = {"dezz": {"SINF2015"}, "rizki": {"SINF2015"}}
        self.assertEqual(
            compute_gate(self.jadwal, done, dt("2026-10-14T08:30:00")), [])

    def test_gate_tetap_aktif_kalau_baru_satu_akun_done(self):
        done = {"dezz": {"SINF2015"}, "rizki": set()}
        self.assertEqual(
            compute_gate(self.jadwal, done, dt("2026-10-14T08:30:00")),
            ["SINF2015"])

    def test_load_done_format_baru_dan_lama(self):
        # Format baru: template state repo (tanggal 2026-10-15).
        baru = load_done(
            os.path.join(ROOT, "data", "templates", "absen_state.json"),
            now=dt("2026-10-15T12:00:00"))
        self.assertEqual(baru["dezz"], {"SINF2023"})
        self.assertEqual(baru["rizki"], {"SINF2023"})
        # Tanggal beda -> kosong.
        self.assertEqual(
            load_done(os.path.join(ROOT, "data", "templates",
                                   "absen_state.json"),
                      now=dt("2026-10-16T12:00:00")),
            {"dezz": set(), "rizki": set()})

    def test_load_absen_done_gabung_kedua_akun(self):
        done = load_absen_done(
            os.path.join(ROOT, "data", "templates", "absen_state.json"),
            now=dt("2026-10-15T12:00:00"))
        self.assertEqual(done, {"SINF2023"})


if __name__ == "__main__":
    unittest.main()
