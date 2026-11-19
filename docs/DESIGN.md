# DESIGN.md — Monitor Kuliah Dezz (landing etalase)

Kontrak arah desain — ditulis SEBELUM coding, mengikuti
`~/workspace/github-actions/ui-anti-slop.md`.

## Referensi (tour 19 Nov 2026)

Kebutuhan: etalase otomasi monitor kuliah — bukan dashboard jadwal,
melainkan **buku log / arsip absensi**: satu kolom linimasa berisi entri
tercatat (absen masuk, tugas terdeteksi, draft selesai, submit
terkonfirmasi), lengkap dengan stempel dan nomor halaman, seperti buku
register kehadiran yang dibuka di meja TU.
Keyword: `logbook ledger archive record`, `memo book field notes`,
`attendance register ruled paper`.

Kandidat:
1. **Field Notes / Draplin — arsip memo-book** (TypeRoom,
   https://www.typeroom.eu/the-list/memo-book-archive) — buku saku
   ber-garis (ruled paper) dari akhir 1800-an sampai 1980-an, sampul
   dan halaman bernomor stempel, satu kolom catatan bertanggal.
   Struktur paling dekat: halaman buku log yang dibaca dari atas ke
   bawah, tiap baris satu kejadian.
2. **Albert Chamillard — gambar di buku ledger bekas** (Abakcus,
   https://abakcus.com/articles/albert-chamillard-geometric-drawings)
   — garis biru dan merah cetak buku kas tetap terlihat dan menentukan
   tinggi tiap baris. Pelajaran: garis aturan (rules) adalah struktur,
   bukan hiasan.
3. **Stet — proof sheet** (template BeaverHero) — nomor baris di
   margin, coretan pensil biru, teks di-typeset rapi. Pelajaran:
   margin kiri sebagai tempat nomor/stempel, bukan kolom kedua.

**Pemenang: #1 arsip memo-book / buku ledger.** Yang di-clone
strukturnya: satu halaman buku ber-garis dengan lubang jilid di kiri,
garis margin merah, tiap entri log satu baris (jam di margin, isi di
kanan garis), nomor halaman di-stempel di pojok. Yang diubah dan
kenapa: buku aslinya kertas kusam tanpa warna; di sini kertas arsip
terang dengan tinta hijau-hitam, garis biru arsip, dan cap merah
`HADIR` sebagai aksen status — supaya tetap terbaca sebagai arsip
kampus 2026, bukan fotokopi dokumen 1920. Status tugas diambil dari
isi repo sendiri (template `state.json` / `absen_state.json`), bukan
angka vanity.

## Palet (5 warna bernama + 1 netral)

| Nama | Hex | Peran |
|---|---|---|
| Kertas Arsip | `#F2F0E6` | latar halaman — kertas buku log |
| Tinta Arsip | `#22271F` | teks utama, judul mesin ketik |
| Merah Cap | `#A63A2B` | aksen — stempel `HADIR`, garis margin, urgensi |
| Biru Garis | `#33546D` | garis aturan buku, tautan, label sistem |
| Kuning Arsip | `#C99A2E` | sorot — entri hari ini / deadline dekat (ochre, bukan stabilo neon) |
| Abu Pensil | `#8A8578` | teks sekunder, nomor halaman (netral, bukan warna aksi) |

Tidak ada gradient (P0). Palet bukan satu hue (kertas hangat + tinta
hijau-hitam + merah cap + biru garis + ochre). Bukan klise
krim+terracotta: warna merah dan biru di sini adalah garis aturan dan
cap stempel buku ledger — keduanya punya tugas struktural, bukan
sekadar pasangan hangat.

## Tipografi (2 keluarga)

- Display/data mesin ketik: **Special Elite** — judul, stempel cap,
  jam dan kode MK di margin (rasa ketikan arsip).
- Body: **Libre Franklin** — teks penjelasan, label, angka
  (`font-variant-numeric: tabular-nums` untuk jam dan SKS).

## Layout (satu kalimat)

Satu halaman buku log: sampul arsip (judul + metadata register) lalu
satu kolom linimasa entri ber-garis dengan jam di margin kiri, disusul
tabel jadwal 13 MK sebagai lampiran register dan 4 baris cara kerja.

## Detail khas (signature)

**Jilid buku ledger** — lubang jilid bulat + garis margin merah
vertikal di tepi kiri halaman, entri dipisah garis aturan biru,
stempel `HADIR` miring bergaris tepi ganda, dan nomor halaman
`No. 047` di-stempel di pojok kanan atas. Radius 0 di semua permukaan
(kertas dipotong, bukan kartu melayang). Tidak ada kartu 3-simetris,
tidak ada emoji (ikon = SVG garis tipis 1.5px).

## Beda dari repo #46 (hermes-monitor-kuliah)

| Sumbu | #46 | Repo ini |
|---|---|---|
| Palet | kertas `#FFFEF9` + Hijau Papan `#14684E` + Stabilo `#F7C948` | kertas arsip `#F2F0E6` + Merah Cap `#A63A2B` + Biru Garis `#33546D` + ochre |
| Tipografi | Fraunces + IBM Plex Sans | Special Elite (mesin ketik) + Libre Franklin |
| Layout | dua kolom papan: jadwal + status monitor | satu kolom linimasa buku log |
| Radius/spacing | radius 6px, bayangan offset keras 3px | radius 0, garis aturan + lubang jilid |
| Detail khas | stempel status karet + sorot stabilo | jilid ledger + garis margin merah + nomor halaman stempel |
