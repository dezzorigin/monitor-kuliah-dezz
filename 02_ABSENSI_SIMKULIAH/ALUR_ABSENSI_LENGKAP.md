# Alur Absensi SIMKULIAH USK (100% Selalu Berhasil)

Dokumen ini adalah cetak biru teknis otomasi absensi mahasiswa pada portal SIMKULIAH Universitas Syiah Kuala (`https://simkuliah.usk.ac.id`).

---

## 1. Tantangan Teknis Portal SIMKULIAH
Portal SIMKULIAH berbasis CodeIgniter 3 dengan beberapa proteksi:
1. **CAPTCHA Gambar Numerik**: CAPTCHA 5 digit angka yang di-generate via GD library PHP.
2. **Session-Bound Captcha**: Gambar captcha terikat ketat dengan cookie sesi PHP (`ci_session`). Jika request gambar dilakukan dengan sesi berbeda, validasi server akan gagal.
3. **SweetAlert Confirmation Dialog**: Dialog konfirmasi JavaScript (`swal()`) sering gagal merespons klik otomatis browser headless, mengakibatkan pesan palsu atau timeout.
4. **Parameter Dinamis Inline**: Parameter jadwal absensi di-inject langsung ke dalam event handler jQuery tombol.

---

## 2. Alur Eksekusi Terbukti (Step-by-Step)

```
[Cron Tick / Window Kuliah Aktif]
                 │
                 ▼
[1. Ambil Sandi dari Vault (Fernet Decrypt)]
                 │
                 ▼
[2. Inisiasi requests.Session -> GET /]
                 │
                 ▼
[3. Unduh Captcha dengan Cache-Buster (?t=...)]
                 │
                 ▼
[4. OCR Lokal Cepat via ddddocr (5 Digit)]
                 │
                 ▼
[5. POST /index.php/login/auth]
                 │
         ┌───────┴───────┐
      (Sukses)        (Gagal)
         │               │
         │          (Loop Retry max 6x dgn Gambar Baru)
         ▼
[6. GET /index.php/absensi]
                 │
         ┌───────┴───────────────────────────┐
   (Belum Waktu /                       (Tombol Konfirmasi Ada)
    Dosen Belum Buka)                        │
         │                                   ▼
   (Catat Status)          [7. Regex Ekstraksi Parameter Inline JS]
                                             │
                                             ▼
                           [8. POST Langsung ke /absensi/konfirmasi_kehadiran]
                                             │
                                             ▼
                           [9. Respon 'success' -> Catat absen_state.json]
                                             │
                                             ▼
                           [10. Kirim Notifikasi Discord + Screenshot Bukti]
```

---

## 3. Ekstraksi Parameter Konfirmasi (Bypass SweetAlert)
Pada halaman `/index.php/absensi`, tombol konfirmasi kehadiran dirender seperti ini:
```html
<button class="btn btn-primary" id="konfirmasi-kehadiran-6819201">Konfirmasi Kehadiran</button>
<script>
$("#konfirmasi-kehadiran-6819201").on("click", function() {
    var kelas = 'A';
    var kd_mt_kul8 = 'SINF2015';
    var jadwal_mulai = '08:00';
    var jadwal_berakhir = '09:40';
    var pertemuan = '7';
    var sks_mengajar = '2';
    var id = '6819201';
    swal({ ... });
});
</script>
```

### Solusi Cerdas:
Alih-alih mengklik tombol dan berurusan dengan dialog SweetAlert yang tidak stabil:
1. Skrip `absen_run.py` mengekstrak seluruh variabel di atas menggunakan Regex.
2. Mengirimkan HTTP POST langsung menggunakan `requests.Session` yang sama ke:
   `https://simkuliah.usk.ac.id/index.php/absensi/konfirmasi_kehadiran`
3. Payload POST:
   ```python
   payload = {
       "kelas": kelas,
       "kd_mt_kul8": kd_mt_kul8,
       "jadwal_mulai": jadwal_mulai,
       "jadwal_berakhir": jadwal_berakhir,
       "pertemuan": pertemuan,
       "sks_mengajar": sks_mengajar,
       "id": id
   }
   ```
4. Server membalas: `{"status": "success"}` -> Presensi tervalidasi 100%!

---

## 4. Multi-Akun (Dezz & Muhammad Rizki)
Skrip mendukung pemrosesan paralel dua akun:
- **Dezz**: NPM `250810701100090` (Nabil Aulia Dika)
- **Rizki**: NPM `250810701100049` (Teman sekelas)
Catatan: Pada praktikum (misal SINF2017), Dezz masuk Kelas A dan Rizki Kelas B. Parameter tombol diekstrak secara independen per akun agar tidak tertukar.
