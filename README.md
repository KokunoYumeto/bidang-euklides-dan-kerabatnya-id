# Bidang Euklides dan Kerabatnya — Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Euclidean Plane and Its Relatives: A
Minimalist Introduction* karya Anton Petrunin, untuk peran kurikulum C100
Fondasi Geometri.

Status produksi saat ini: Prakata serta Bab 1–4 lengkap telah diterjemahkan,
dipetakan dalam backend, dibangun secara deterministik, dan diperiksa secara
visual. Pembaca yang tersedia di bawah tetap Unit Produksi 001: rilis parsial
yang hanya memuat Prakata, Bab 1, 16 latihan Bab 1, 16 petunjuk, dan gambar
terkait. Edisi lengkap belum dinyatakan selesai dan repositori tetap privat.

- [Baca Unit Produksi 001](output/BIDANG_EUKLIDES_DAN_KERABATNYA_ID_UNIT_001.pdf)
- [DOI Zenodo Unit 001](https://doi.org/10.5281/zenodo.22044358)
- [Cakupan dan checksum rilis](README_RELEASE.md)

## Sumber resmi

- Situs karya: <https://anton-petrunin.github.io/birkhoff/>
- Repositori penulis: <https://github.com/anton-petrunin/birkhoff>
- Saksi edisi terbit: arXiv `1302.1630v25`, edisi ketiga, cetakan kesepuluh
- Revisi sumber kerja: commit
  `0b0858e1e985f4c8dadbb6075ae9e095cd4a8981`

Revisi sumber kerja lebih baru daripada v25, tetapi tidak disebut sebagai
cetakan atau edisi baru. Perbedaan ini dipertahankan dalam provenance.

## Isi repositori edisi

- `source/id-ID/`: sumber LaTeX edisi dan berkas lokalisasi;
- `backend/`: ID semantik netral-lokal, urutan unit, pasangan latihan–petunjuk,
  deskripsi gambar, hak komponen, dan ekspor deterministik;
- `00_control/`: otoritas, keputusan, kursor, terminologi, hak, dan bukti build;
- `scripts/`: build deterministik dan QA struktural;
- `output/`: pembaca yang telah melewati batas verifikasi.

Backend bersifat aditif. Label LaTeX asli tetap dipertahankan, sedangkan ID
backend memungkinkan bab, konsep, latihan, petunjuk, dan aset dipilih sebagai
unit yang stabil untuk bahasa lain.

## Build

Repositori edisi mendistribusikan overlay terjemahan, bukan salinan generator
MetaPost yang provenance lisensinya belum selesai. Dari akar repositori,
perintah berikut mengambil arsip resmi yang dipatok, memverifikasi SHA-256,
menghapus `cover/`, menerapkan overlay, dan membangun badan buku dalam direktori
kerja serta keluaran yang baru:

```powershell
.\scripts\fetch_and_build_unit001.ps1 `
  -WorkRoot C:\path\to\new-work-directory `
  -OutputRoot C:\path\to\new-build-directory
```

Skrip tingkat bawah `build_reader_id.ps1` menetapkan waktu sumber ke waktu
commit resmi, membangun gambar MetaPost, menjalankan LaTeX/MakeIndex/Biber, dan
mensyaratkan dua PDF akhir yang identik secara byte.

## Lisensi dan perubahan

Karya asli dan adaptasi ini menggunakan
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Karya asli oleh
Anton Petrunin. Edisi ini menerjemahkan teks ke Bahasa Indonesia serta menambah
lokalisasi, indeks mesin, provenance, QA, dan aksesibilitas; edisi ini bukan
dukungan atau pengesahan oleh penulis asli.

Komponen pihak ketiga tidak digeneralisasi sebagai CC BY-SA. Direktori sampul
dan kedua font P22 dikecualikan. `fiziko.mp` berlisensi GPL-3.0-or-later;
`mppics/macros.mp` mempunyai provenance lisensi yang belum cukup untuk paket
sumber publik, sehingga generator tersebut tidak akan dikemas sampai batas hak
itu terselesaikan. Rincian ada di `00_control/RIGHTS_AND_COMPONENTS.md`.
