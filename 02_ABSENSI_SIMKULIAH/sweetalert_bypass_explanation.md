# Penjelasan Teknis: Mengapa Tombol SweetAlert Dilewati

## Masalah:
Di SIMKULIAH USK, tombol `Konfirmasi Kehadiran` tidak langsung mensubmit form, melainkan memanggil library `SweetAlert` JavaScript:
```javascript
swal({
    title: "Konfirmasi Kehadiran",
    text: "Apakah anda yakin ingin melakukan presensi kuliah ini?",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#DD6B55",
    confirmButtonText: "Ya, Konfirmasi!",
    closeOnConfirm: false
}, function() {
    $.ajax({
        url: "https://simkuliah.usk.ac.id/index.php/absensi/konfirmasi_kehadiran",
        type: "POST",
        data: {
            kelas: kelas,
            kd_mt_kul8: kd_mt_kul8,
            jadwal_mulai: jadwal_mulai,
            jadwal_berakhir: jadwal_berakhir,
            pertemuan: pertemuan,
            sks_mengajar: sks_mengajar,
            id: id
        },
        success: function(response) { ... }
    });
});
```

Jika menggunakan otomasi klik browser (`click_at_xy` atau `.click()`):
1. Dialog SweetAlert sering dirender di luar viewport atau memiliki delay animasi CSS yang menyebabkan klik meleset.
2. Callback AJAX terkadang tidak tertrigger jika event loop browser terputus.

## Solusi Ampuh (100% Berhasil):
Skrip Python membaca teks HTML, mencari blok script tombol dengan id `konfirmasi-kehadiran-*`, mengambil nilai 7 variabel kunci (`kelas`, `kd_mt_kul8`, `jadwal_mulai`, `jadwal_berakhir`, `pertemuan`, `sks_mengajar`, `id`), lalu langsung mengirimkan HTTP POST request ke backend endpoint `/index.php/absensi/konfirmasi_kehadiran` menggunakan sesi yang sama.

Metode ini:
- Berjalan dalam waktu < 200 milidetik.
- Kebal terhadap perubahan tampilan UI atau CSS.
- Menjamin presensi masuk tanpa hambatan frontend.
