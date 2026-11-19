"""Tes parser halaman absensi SIMKULIAH (scripts/absen_run.py: parse_absensi).

Pola A (format 2026, var-style), Pola B (legacy konfirmasiKehadiran),
fallback onclick, dan status teks. Tanpa jaringan / login.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from absen_run import parse_absensi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(ROOT, "data", "examples", "absensi_contoh.html")

POLA_B_HTML = """
<html><body>
<p>Anda belum absen</p>
<table><tr><td>SINF2023</td><td>SISTEM OPERASI</td></tr></table>
<button id="konfirmasi-kehadiran-6819301">Konfirmasi Kehadiran</button>
<script>
konfirmasiKehadiran('B','SINF2023','16:35','18:15','9','2','6819301');
</script>
</body></html>
"""

ONCLICK_HTML = """
<html><body>
<button id="konfirmasi-kehadiran-6819401"
  onclick="konfirmasiKehadiran('A','SINF2011','16:35','18:15','7','2','6819401')">Konfirmasi</button>
</body></html>
"""


class TestParseAbsensi(unittest.TestCase):
    def test_fixture_pola_a(self):
        with open(FIXTURE) as f:
            info = parse_absensi(f.read())
        self.assertEqual(len(info["tombol"]), 1)
        t = info["tombol"][0]
        self.assertEqual(t["id_tombol"], "6819201")
        self.assertEqual(t["params"], {
            "kelas": "A", "kd_mt_kul8": "SINF2015",
            "jadwal_mulai": "08:00", "jadwal_berakhir": "09:40",
            "pertemuan": "7", "sks_mengajar": "2", "id": "6819201",
        })
        self.assertIn("SINF2015", info["rows"])
        self.assertIn("SINF2009", info["rows"])

    def test_pola_b_legacy(self):
        info = parse_absensi(POLA_B_HTML)
        self.assertEqual(len(info["tombol"]), 1)
        self.assertEqual(info["tombol"][0]["params"]["kd_mt_kul8"], "SINF2023")
        self.assertEqual(info["tombol"][0]["params"]["kelas"], "B")

    def test_fallback_onclick(self):
        info = parse_absensi(ONCLICK_HTML)
        self.assertEqual(len(info["tombol"]), 1)
        self.assertEqual(info["tombol"][0]["params"]["kd_mt_kul8"], "SINF2011")

    def test_tanpa_tombol_status_sudah_absen(self):
        info = parse_absensi("<html><body><p>Anda sudah absen</p></body></html>")
        self.assertEqual(info["tombol"], [])
        self.assertEqual(info["status_teks"], "anda sudah absen")

    def test_status_dosen_belum_absen(self):
        info = parse_absensi("<html><body><p>Dosen belum absen</p></body></html>")
        self.assertEqual(info["status_teks"], "dosen belum absen")

    def test_halaman_kosong(self):
        info = parse_absensi("<html><body></body></html>")
        self.assertEqual(info, {"tombol": [], "status_teks": None, "rows": []})


if __name__ == "__main__":
    unittest.main()
