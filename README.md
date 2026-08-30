# Bidang Euklides dan Kerabatnya — Bahasa Indonesia

Edisi Bahasa Indonesia independen dan lengkap untuk peran kurikulum C100,
berdasarkan *Euclidean Plane and Its Relatives: A Minimalist Introduction*
karya Anton Petrunin.

## Baca dan unduh

- [Pembaca HTML lengkap](https://kokunoyumeto.github.io/bidang-euklides-dan-kerabatnya-id/)
- [PDF utama lengkap](output/BIDANG_EUKLIDES_DAN_KERABATNYA_ID_SPINE_COMPLETE.pdf)
- [Rilis kursus lengkap](https://github.com/KokunoYumeto/bidang-euklides-dan-kerabatnya-id/releases/tag/2026.08.25-complete-course-a11y-ch20-portable)
- [DOI kursus lengkap](https://doi.org/10.5281/zenodo.22102628)
- [Buku kerja geometri dua dimensi, Unit 001–022](https://github.com/KokunoYumeto/bidang-euklides-dan-kerabatnya-id/releases/tag/2026.08.29-unit001-022)
- [DOI buku kerja](https://doi.org/10.5281/zenodo.22151703)

Rilis utama memuat terjemahan lengkap 20 bab, pendamping orisinal enam unit,
solusi dan bahan penguasaan lengkap, pembaca HTML/EPUB semantik, empat
pemeriksaan kumulatif, serta dua capstone. Buku kerja Clemens–Snapp dipelihara
sebagai rilis terpisah karena narasinya berlisensi CC BY-NC-SA 4.0 dan lapisan
bangunnya GPL-2.0; buku kerja itu tidak digabung atau dilisensikan ulang ke
dalam rilis utama CC BY-SA.

## Identitas sumber

- Sumber kerja resmi: commit
  `0b0858e1e985f4c8dadbb6075ae9e095cd4a8981`, tree
  `4c931765feb8e83b77b079e618b994a74efa5cf3`.
- Saksi terbit: arXiv `1302.1630v25`, edisi ketiga, cetakan kesepuluh,
  revisi 2025-07-07.
- [Laman penulis](https://anton-petrunin.github.io/birkhoff/)
- [Repositori sumber](https://github.com/anton-petrunin/birkhoff)

Snapshot GitHub yang lebih baru dipakai sebagai sumber kerja terjemahan dan
backend, tetapi tidak dinyatakan sebagai edisi atau cetakan bernomor baru.
Edisi ini merupakan karya turunan independen dan tidak menyiratkan dukungan
atau pengesahan oleh penulis sumber.

## Struktur repositori

- `source/id-ID/`: sumber LaTeX dan lokalisasi Bahasa Indonesia;
- `backend/`: ID stabil, urutan unit, relasi latihan–petunjuk–jawaban–solusi,
  hak komponen, dan ekspor deterministik;
- `companion/id-ID/`: pendamping instruksional enam unit;
- `solutions/id-ID/`: solusi, penguasaan, pemeriksaan, dan capstone;
- `accessible/id-ID/`: pembaca HTML dan EPUB semantik lengkap;
- `00_control/`: otoritas, keputusan, hak, kursor, dan bukti build/QA;
- `scripts/`: build deterministik dan pemeriksaan struktural;
- `output/`: pembaca serta paket rilis yang telah diverifikasi.

Backend bersifat aditif: label sumber tetap dipertahankan, sedangkan ID
netral-lokal memungkinkan bab, konsep, latihan, petunjuk, solusi, dan aset
dipilih kembali sebagai unit stabil untuk bahasa lain.

## Build, hak, dan provenance

Paket rilis sumber/backend dibentuk dari allowlist dan mengecualikan sampul,
font P22 berpemberitahuan hak milik, `mppics/macros.mp` yang provenance
lisensinya belum cukup, log mentah, cache, jalur lokal, serta kredensial.
Rincian per komponen ada di `00_control/RIGHTS_AND_COMPONENTS.md` dan manifest
rilis.

Karya asli dan adaptasi utama menggunakan
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Atribusi dan
ShareAlike tetap wajib. Hak komponen lain tidak digeneralisasi. Pembaca PDF
adalah permukaan cetak; HTML dan EPUB menyediakan urutan semantik, MathML,
deskripsi gambar, dan tautan stabil.

Terjemahan, penyuntingan teknis, produksi pembaca, dan pemeriksaan
deterministik dibantu oleh OpenAI Codex gpt-5.6-sol, Ultra, atas instruksi
pengguna. Kredit penulis sumber dan seluruh atribusi komponen tetap
dipertahankan.
