"""Tes mode demo + sanitasi PDF (tanpa jaringan, tanpa kredensial).

- absen_run.py --demo: parse fixture lokal, TIDAK ada POST/login.
- generate_pdfs.py: cek sanitasi menolak string terlarang; build 3 PDF
  (skip kalau reportlab belum terpasang — di CI terpasang via
  requirements.txt).
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")

try:
    import reportlab  # noqa: F401
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class TestDemoMode(unittest.TestCase):
    def test_demo_tanpa_jaringan(self):
        r = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "absen_run.py"), "--demo"],
            capture_output=True, text=True, cwd=ROOT, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["mode"], "demo")
        self.assertEqual(len(out["hasil"]), 1)
        self.assertEqual(out["hasil"][0]["mk"], "SINF2015")
        self.assertEqual(out["hasil"][0]["id_tombol"], "6819201")
        self.assertEqual(out["hasil"][0]["params"]["kd_mt_kul8"], "SINF2015")
        self.assertIn("TIDAK di-POST", out["hasil"][0]["aksi"])
        self.assertIn("SINF2015", out["mk_terlihat"])

    def test_demo_tidak_butuh_vault(self):
        env = dict(os.environ)
        env["MONITOR_KULIAH_VAULT_KEY"] = "/tidak/ada/vault.key"
        env["MONITOR_KULIAH_VAULT_ENC"] = "/tidak/ada/vault.json.enc"
        r = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, "absen_run.py"), "--demo"],
            capture_output=True, text=True, cwd=ROOT, timeout=60, env=env)
        self.assertEqual(r.returncode, 0, r.stderr)


class TestPdfSanitasi(unittest.TestCase):
    @unittest.skipUnless(HAS_REPORTLAB, "reportlab belum terpasang")
    def test_string_terlarang_ditolak(self):
        sys.path.insert(0, SCRIPTS)
        import generate_pdfs
        with self.assertRaises(ValueError):
            generate_pdfs.check_sanitized("path /opt/data/monitor-kuliah/x")
        generate_pdfs.check_sanitized("kode Student.java biasa, tanpa jejak")

    @unittest.skipUnless(HAS_REPORTLAB, "reportlab belum terpasang")
    def test_build_tiga_pdf_dan_metadata_bersih(self):
        sys.path.insert(0, SCRIPTS)
        import generate_pdfs
        from pypdf import PdfReader
        with tempfile.TemporaryDirectory() as tmp:
            paths = generate_pdfs.build_all(tmp)
            self.assertEqual(len(paths), 3)
            for p in paths:
                self.assertTrue(os.path.getsize(p) > 1000, p)
                reader = PdfReader(p)
                meta = reader.metadata
                self.assertEqual(meta.author, "Nabil Aulia Dika")
                self.assertNotIn("/opt", (meta.creator or "") + (meta.producer or ""))
                text = "\n".join((pg.extract_text() or "") for pg in reader.pages)
                for banned in ("/opt", "hermes", "monitor-kuliah"):
                    self.assertNotIn(banned, text.lower())


if __name__ == "__main__":
    unittest.main()
