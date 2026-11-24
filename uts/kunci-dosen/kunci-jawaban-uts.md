# Kunci Dosen: UTS Bisnis Intelegent (8 Paket)

Dokumen ini khusus dosen. Jangan dibagikan ke mahasiswa.

## Ringkasan paket

| Paket | Bisnis | Berkas mahasiswa |
|---|---|---|
| 01 | KopiKita | `publik/paket-mahasiswa/dataset-01-kopikita.zip` |
| 02 | Apotek Sehat Sentosa | `publik/paket-mahasiswa/dataset-02-apotek-sehat.zip` |
| 03 | EduPlus Academy | `publik/paket-mahasiswa/dataset-03-eduplus.zip` |
| 04 | Hotel Nusa Group | `publik/paket-mahasiswa/dataset-04-hotelnusa.zip` |
| 05 | FashionKu | `publik/paket-mahasiswa/dataset-05-fashionku.zip` |
| 06 | KirimCepat Express | `publik/paket-mahasiswa/dataset-06-kirimcepat.zip` |
| 07 | CineKita Cinema | `publik/paket-mahasiswa/dataset-07-cinekita.zip` |
| 08 | BukuKita | `publik/paket-mahasiswa/dataset-08-bukukita.zip` |

Setiap zip berisi: soal (`soal-uts.html`), CSV master, Excel (item + cabang), SQL transaksi, dan CSV cadangan transaksi. Berkas bersih per paket ada di `kunci-dosen/dataset-XX-.../` (fact_bersih.csv dan tiga dimensi bersih).

## Aturan hitung (sama untuk semua paket)

- Hapus duplikat berdasarkan `ID_Transaksi`; seragamkan kunci; tanggal ke Date.
- `Qty` kosong, nol, negatif atau lebih dari 50 diberi `Status_Kualitas = Qty Tidak Valid` (baris tetap di fakta, tidak dihitung). Qty tidak valid dicek lebih dulu, baru `Batal`, jadi dua kelompok itu tidak tumpang tindih.
- `Harga_Satuan` null diisi dari harga master. Diskon kosong = 0. `Nilai_Bersih = Qty x Harga x (1 - Diskon)`.
- Dihitung bila `Status_Kualitas = OK` dan Status bukan `Batal`. Status null menjadi `Tidak Diketahui` dan **tetap dihitung**.
- Kunci yatim tidak dihapus; dipetakan ke baris `UNK` (Tidak Terdaftar).
- Dua harga master dikosongkan sengaja; transaksi untuk keduanya tidak pernah bernilai null, jadi tidak memengaruhi total.

## Rancangan star schema acuan (semua paket)

Grain: satu baris transaksi (`ID_Transaksi`). Fakta: tanggal, kunci tiga dimensi, Qty, Harga_Satuan, Diskon, Metode_Bayar, Status, Status_Kualitas, Nilai_Bersih. Metode_Bayar dan Status boleh tetap di fakta sebagai degenerate attribute atau dipindah ke dimensi kecil (keduanya diterima).

| Tabel | Kunci | Relasi |
|---|---|---|
| Fact | `ID_Transaksi` | fakta, sisi Many |
| Dim pelanggan | ID unik | 1 ke Many |
| Dim item (Kode, Nama, Kategori, Harga, Satuan, Pemasok, Aktif) | Kode unik | 1 ke Many |
| Dim cabang | Kode unik | 1 ke Many |
| Dim_Tanggal | Tanggal | 1 ke Many |

Kesalahan umum: kategori dipisah menjadi tabel sendiri (snowflake) tanpa alasan, relasi Many-to-Many, Dim_Tanggal diambil dari tanggal transaksi saja (berlubang), kunci belum seragam sehingga relasi kosong, menghapus kunci yatim.

Penilaian Dim_Tanggal: bila mahasiswa membuat dari tanggal pertama sampai terakhir **di data transaksi** (bukan kalender penuh periode), jumlah harinya mengikuti angka (hari antara tanggal transaksi pertama dan terakhir) pada tiap paket; keduanya diterima asal tanpa celah.

---

## Paket 01: KopiKita

Database `kopikita`, tabel `penjualan`. Periode 2025-01-01 sampai 2025-06-30 (kalender penuh 181 hari; hari antara tanggal transaksi pertama dan terakhir: 181).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Member (CSV) | 105 | 5 | 100 |
| Menu (Excel, data saja) | 22 | 2 | 20 |
| Outlet (Excel) | 6 | 1 | 5 |
| penjualan (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: member tak terdaftar **8** baris, menu tak terdaftar **5** baris. Harga kosong di master: `MNU-011, MNU-017`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 25.540.100** |
| Jumlah transaksi dihitung | 290 |
| Rata-rata nilai transaksi | Rp 88.069 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 37 |
| Dikecualikan karena Batal | 73 |
| Member unik yang bertransaksi | 100 |
| Outlet tertinggi | KopiKita Dago (Rp 5.987.600) |
| Bulan tertinggi | 2025-01 (Rp 5.608.000) |

Per kategori:

| Kategori | Total |
|---|---|
| Non-Kopi | Rp 7.641.900 |
| Makanan | Rp 6.513.700 |
| Kopi | Rp 6.089.700 |
| Camilan | Rp 5.022.800 |
| Tidak Terdaftar | Rp 272.000 |

Per outlet:

| Outlet | Total |
|---|---|
| KopiKita Dago | Rp 5.987.600 |
| KopiKita Kuta | Rp 5.860.550 |
| KopiKita Braga | Rp 4.989.200 |
| KopiKita Tunjungan | Rp 4.580.700 |
| KopiKita Kemang | Rp 4.122.050 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-01 | Rp 5.608.000 |
| 2025-02 | Rp 3.767.150 |
| 2025-03 | Rp 4.096.100 |
| 2025-04 | Rp 2.774.650 |
| 2025-05 | Rp 5.419.500 |
| 2025-06 | Rp 3.874.700 |

5 teratas:

| Nama | Total |
|---|---|
| Cokelat Panas | Rp 2.597.400 |
| Matcha Latte | Rp 1.596.000 |
| Sandwich Ayam | Rp 1.555.400 |
| Red Velvet Latte | Rp 1.552.950 |
| Kopi Susu Gula Aren | Rp 1.476.000 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_huruf` | 1 |
| `cb_kode_spasi` | 1 |
| `cb_kota_variasi` | 1 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 9 |
| `d1_email_kosong` | 4 |
| `d1_email_spasi` | 7 |
| `d1_email_tanpa_at` | 4 |
| `d1_hp_format` | 38 |
| `d1_hp_kosong` | 3 |
| `d1_kota_alias` | 1 |
| `d1_kota_variasi` | 24 |
| `d1_nama_huruf` | 26 |
| `d1_nama_spasi` | 9 |
| `d1_segmen_huruf` | 12 |
| `d1_segmen_kosong` | 6 |
| `d1_tgl_slash` | 23 |
| `d1_tgl_strip` | 13 |
| `d1_tgl_teks` | 11 |
| `f_cb_huruf` | 43 |
| `f_cb_spasi` | 41 |
| `f_cb_tanpa_strip` | 20 |
| `f_d1_huruf` | 35 |
| `f_d1_spasi` | 33 |
| `f_d1_tanpa_strip` | 34 |
| `f_diskon_format` | 177 |
| `f_diskon_kosong` | 18 |
| `f_duplikat` | 10 |
| `f_harga_null` | 22 |
| `f_item_huruf` | 46 |
| `f_item_spasi` | 27 |
| `f_item_tanpa_strip` | 12 |
| `f_metode_variasi` | 135 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 16 |
| `f_qty_tidak_wajar` | 21 |
| `f_status_null` | 10 |
| `f_status_variasi` | 71 |
| `f_tgl_slash` | 110 |
| `f_tgl_strip` | 58 |
| `it_aktif_variasi` | 6 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 8 |
| `it_kat_variasi` | 2 |
| `it_kode_huruf` | 1 |
| `it_nama_huruf` | 4 |
| `it_stok_negatif` | 4 |
| `it_stok_teks` | 1 |

---

## Paket 02: Apotek Sehat Sentosa

Database `apotek_sehat`, tabel `penjualan`. Periode 2025-02-01 sampai 2025-07-31 (kalender penuh 181 hari; hari antara tanggal transaksi pertama dan terakhir: 181).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Pasien (CSV) | 105 | 5 | 100 |
| Obat (Excel, data saja) | 22 | 2 | 20 |
| Apotek (Excel) | 6 | 1 | 5 |
| penjualan (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: pasien tak terdaftar **8** baris, obat tak terdaftar **5** baris. Harga kosong di master: `OBT-005, OBT-006`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 48.245.625** |
| Jumlah transaksi dihitung | 281 |
| Rata-rata nilai transaksi | Rp 171.693 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 38 |
| Dikecualikan karena Batal | 81 |
| Pasien unik yang bertransaksi | 98 |
| Apotek tertinggi | Sehat Sentosa Pusat (Rp 13.127.725) |
| Bulan tertinggi | 2025-07 (Rp 12.316.925) |

Per kategori:

| Kategori | Total |
|---|---|
| Alat Kesehatan | Rp 19.631.025 |
| Perawatan | Rp 12.610.550 |
| Vitamin | Rp 11.469.100 |
| Obat Bebas | Rp 4.323.075 |
| Tidak Terdaftar | Rp 211.875 |

Per apotek:

| Apotek | Total |
|---|---|
| Sehat Sentosa Pusat | Rp 13.127.725 |
| Sehat Sentosa Sanur | Rp 12.384.350 |
| Sehat Sentosa Darmo | Rp 8.332.000 |
| Sehat Sentosa Dago | Rp 7.977.050 |
| Sehat Sentosa Kemang | Rp 6.424.500 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-02 | Rp 3.900.350 |
| 2025-03 | Rp 4.635.700 |
| 2025-04 | Rp 9.813.375 |
| 2025-05 | Rp 5.731.850 |
| 2025-06 | Rp 11.847.425 |
| 2025-07 | Rp 12.316.925 |

5 teratas:

| Nama | Total |
|---|---|
| Tensimeter Digital | Rp 13.088.000 |
| Sunscreen SPF 50 | Rp 4.681.600 |
| Vitamin D3 1000IU | Rp 4.471.000 |
| Pelembap Wajah | Rp 3.578.600 |
| Masker Medis 50s | Rp 3.115.000 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kota_variasi` | 1 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 9 |
| `d1_email_kosong` | 7 |
| `d1_email_spasi` | 3 |
| `d1_email_tanpa_at` | 5 |
| `d1_hp_format` | 36 |
| `d1_hp_kosong` | 6 |
| `d1_kota_variasi` | 25 |
| `d1_nama_huruf` | 23 |
| `d1_nama_spasi` | 5 |
| `d1_segmen_huruf` | 5 |
| `d1_segmen_kosong` | 13 |
| `d1_tgl_slash` | 23 |
| `d1_tgl_strip` | 9 |
| `d1_tgl_teks` | 13 |
| `f_cb_huruf` | 54 |
| `f_cb_spasi` | 42 |
| `f_cb_tanpa_strip` | 28 |
| `f_d1_huruf` | 34 |
| `f_d1_spasi` | 40 |
| `f_d1_tanpa_strip` | 35 |
| `f_diskon_format` | 177 |
| `f_diskon_kosong` | 19 |
| `f_duplikat` | 10 |
| `f_harga_null` | 22 |
| `f_item_huruf` | 57 |
| `f_item_spasi` | 34 |
| `f_item_tanpa_strip` | 23 |
| `f_metode_variasi` | 137 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 21 |
| `f_qty_tidak_wajar` | 17 |
| `f_status_null` | 13 |
| `f_status_variasi` | 73 |
| `f_tgl_slash` | 88 |
| `f_tgl_strip` | 60 |
| `it_aktif_variasi` | 7 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 1 |
| `it_kat_variasi` | 1 |
| `it_kode_huruf` | 1 |
| `it_kode_spasi` | 3 |
| `it_nama_huruf` | 3 |
| `it_stok_kosong` | 2 |
| `it_stok_negatif` | 1 |
| `it_stok_teks` | 1 |

---

## Paket 03: EduPlus Academy

Database `eduplus`, tabel `pendaftaran`. Periode 2025-07-01 sampai 2025-12-31 (kalender penuh 184 hari; hari antara tanggal transaksi pertama dan terakhir: 183).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Peserta (CSV) | 105 | 5 | 100 |
| Kursus (Excel, data saja) | 22 | 2 | 20 |
| Kampus Mitra (Excel) | 6 | 1 | 5 |
| pendaftaran (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: peserta tak terdaftar **8** baris, kursus tak terdaftar **5** baris. Harga kosong di master: `KRS-014, KRS-016`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 673.648.000** |
| Jumlah transaksi dihitung | 295 |
| Rata-rata nilai transaksi | Rp 2.283.553 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 38 |
| Dikecualikan karena Batal | 67 |
| Peserta unik yang bertransaksi | 99 |
| Kampus Mitra tertinggi | Universitas Bina Insani (Rp 153.975.000) |
| Bulan tertinggi | 2025-11 (Rp 127.762.500) |

Per kategori:

| Kategori | Total |
|---|---|
| Desain | Rp 203.532.500 |
| Bahasa | Rp 186.542.500 |
| Data | Rp 145.955.000 |
| Bisnis | Rp 136.782.500 |
| Tidak Terdaftar | Rp 835.500 |

Per kampus mitra:

| Kampus Mitra | Total |
|---|---|
| Universitas Bina Insani | Rp 153.975.000 |
| Institut Teknologi Mandala | Rp 139.830.000 |
| Politeknik Nusantara | Rp 134.917.500 |
| Universitas Cendekia | Rp 132.488.000 |
| Akademi Digital Utama | Rp 112.437.500 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-07 | Rp 98.713.000 |
| 2025-08 | Rp 89.722.500 |
| 2025-09 | Rp 121.965.000 |
| 2025-10 | Rp 121.505.000 |
| 2025-11 | Rp 127.762.500 |
| 2025-12 | Rp 113.980.000 |

5 teratas:

| Nama | Total |
|---|---|
| Persiapan IELTS | Rp 63.060.000 |
| Bahasa Jepang N5 | Rp 56.355.000 |
| Editing Video | Rp 52.682.500 |
| UI/UX Fundamental | Rp 50.310.000 |
| Manajemen Proyek | Rp 47.975.000 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_huruf` | 1 |
| `cb_kode_spasi` | 1 |
| `cb_kota_variasi` | 3 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 4 |
| `d1_email_kosong` | 6 |
| `d1_email_spasi` | 5 |
| `d1_email_tanpa_at` | 5 |
| `d1_hp_format` | 26 |
| `d1_hp_kosong` | 5 |
| `d1_kota_alias` | 3 |
| `d1_kota_variasi` | 17 |
| `d1_nama_huruf` | 27 |
| `d1_nama_spasi` | 17 |
| `d1_segmen_huruf` | 12 |
| `d1_segmen_kosong` | 8 |
| `d1_tgl_slash` | 22 |
| `d1_tgl_strip` | 12 |
| `d1_tgl_teks` | 18 |
| `f_cb_huruf` | 35 |
| `f_cb_spasi` | 46 |
| `f_cb_tanpa_strip` | 21 |
| `f_d1_huruf` | 32 |
| `f_d1_spasi` | 51 |
| `f_d1_tanpa_strip` | 25 |
| `f_diskon_format` | 183 |
| `f_diskon_kosong` | 21 |
| `f_duplikat` | 10 |
| `f_harga_null` | 16 |
| `f_item_huruf` | 36 |
| `f_item_spasi` | 36 |
| `f_item_tanpa_strip` | 24 |
| `f_metode_variasi` | 137 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 13 |
| `f_qty_tidak_wajar` | 25 |
| `f_status_null` | 13 |
| `f_status_variasi` | 66 |
| `f_tgl_slash` | 89 |
| `f_tgl_strip` | 81 |
| `it_aktif_variasi` | 10 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 5 |
| `it_kat_variasi` | 6 |
| `it_kode_huruf` | 3 |
| `it_nama_huruf` | 2 |
| `it_stok_negatif` | 1 |

---

## Paket 04: Hotel Nusa Group

Database `hotelnusa`, tabel `reservasi`. Periode 2025-01-01 sampai 2025-06-30 (kalender penuh 181 hari; hari antara tanggal transaksi pertama dan terakhir: 181).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Tamu (CSV) | 105 | 5 | 100 |
| Layanan (Excel, data saja) | 22 | 2 | 20 |
| Hotel (Excel) | 6 | 1 | 5 |
| reservasi (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: tamu tak terdaftar **8** baris, layanan tak terdaftar **5** baris. Harga kosong di master: `LYN-009, LYN-012`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 1.101.417.250** |
| Jumlah transaksi dihitung | 301 |
| Rata-rata nilai transaksi | Rp 3.659.194 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 28 |
| Dikecualikan karena Batal | 71 |
| Tamu unik yang bertransaksi | 100 |
| Hotel tertinggi | Nusa Bali (Rp 284.321.500) |
| Bulan tertinggi | 2025-01 (Rp 251.362.500) |

Per kategori:

| Kategori | Total |
|---|---|
| Ruang Rapat | Rp 564.091.000 |
| Kamar | Rp 369.960.000 |
| Spa | Rp 131.341.500 |
| Makan | Rp 35.701.750 |
| Tidak Terdaftar | Rp 323.000 |

Per hotel:

| Hotel | Total |
|---|---|
| Nusa Bali | Rp 284.321.500 |
| Nusa Bandung | Rp 250.600.000 |
| Nusa Jakarta | Rp 234.724.000 |
| Nusa Yogyakarta | Rp 191.679.750 |
| Nusa Surabaya | Rp 140.092.000 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-01 | Rp 251.362.500 |
| 2025-02 | Rp 146.194.750 |
| 2025-03 | Rp 213.850.750 |
| 2025-04 | Rp 150.707.500 |
| 2025-05 | Rp 208.879.500 |
| 2025-06 | Rp 130.422.250 |

5 teratas:

| Nama | Total |
|---|---|
| Ballroom Setengah Hari | Rp 354.575.000 |
| Suite Eksekutif | Rp 186.165.000 |
| Ruang Rapat Sedang | Rp 128.800.000 |
| Suite Junior | Rp 87.815.000 |
| Ruang Rapat Kecil | Rp 62.775.000 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_huruf` | 2 |
| `cb_kode_spasi` | 1 |
| `cb_kota_variasi` | 2 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 8 |
| `d1_email_kosong` | 4 |
| `d1_email_spasi` | 4 |
| `d1_email_tanpa_at` | 4 |
| `d1_hp_format` | 26 |
| `d1_hp_kosong` | 2 |
| `d1_kota_alias` | 1 |
| `d1_kota_variasi` | 15 |
| `d1_nama_huruf` | 25 |
| `d1_nama_spasi` | 9 |
| `d1_segmen_huruf` | 9 |
| `d1_segmen_kosong` | 5 |
| `d1_tgl_slash` | 26 |
| `d1_tgl_strip` | 10 |
| `d1_tgl_teks` | 20 |
| `f_cb_huruf` | 40 |
| `f_cb_spasi` | 47 |
| `f_cb_tanpa_strip` | 18 |
| `f_d1_huruf` | 56 |
| `f_d1_spasi` | 34 |
| `f_d1_tanpa_strip` | 28 |
| `f_diskon_format` | 188 |
| `f_diskon_kosong` | 17 |
| `f_duplikat` | 10 |
| `f_harga_null` | 21 |
| `f_item_huruf` | 58 |
| `f_item_spasi` | 37 |
| `f_item_tanpa_strip` | 23 |
| `f_metode_variasi` | 130 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 14 |
| `f_qty_tidak_wajar` | 14 |
| `f_status_null` | 16 |
| `f_status_variasi` | 68 |
| `f_tgl_slash` | 102 |
| `f_tgl_strip` | 56 |
| `it_aktif_variasi` | 8 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 6 |
| `it_kat_variasi` | 5 |
| `it_kode_huruf` | 2 |
| `it_kode_spasi` | 3 |
| `it_nama_huruf` | 1 |
| `it_stok_negatif` | 4 |
| `it_stok_teks` | 3 |

---

## Paket 05: FashionKu

Database `fashionku`, tabel `pesanan`. Periode 2025-03-01 sampai 2025-08-31 (kalender penuh 184 hari; hari antara tanggal transaksi pertama dan terakhir: 184).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Pembeli (CSV) | 105 | 5 | 100 |
| Produk (Excel, data saja) | 22 | 2 | 20 |
| Gudang (Excel) | 6 | 1 | 5 |
| pesanan (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: pembeli tak terdaftar **8** baris, produk tak terdaftar **5** baris. Harga kosong di master: `SKU-001, SKU-010`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 201.074.850** |
| Jumlah transaksi dihitung | 295 |
| Rata-rata nilai transaksi | Rp 681.610 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 47 |
| Dikecualikan karena Batal | 58 |
| Pembeli unik yang bertransaksi | 94 |
| Gudang tertinggi | Gudang Makassar (Rp 47.146.650) |
| Bulan tertinggi | 2025-05 (Rp 41.531.900) |

Per kategori:

| Kategori | Total |
|---|---|
| Sepatu | Rp 86.459.500 |
| Atasan | Rp 53.511.750 |
| Bawahan | Rp 41.529.250 |
| Aksesori | Rp 19.084.500 |
| Tidak Terdaftar | Rp 489.850 |

Per gudang:

| Gudang | Total |
|---|---|
| Gudang Makassar | Rp 47.146.650 |
| Gudang Jakarta Pusat | Rp 43.430.500 |
| Gudang Bandung Timur | Rp 41.039.750 |
| Gudang Medan Kota | Rp 34.905.350 |
| Gudang Surabaya Barat | Rp 34.552.600 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-03 | Rp 31.974.800 |
| 2025-04 | Rp 36.580.400 |
| 2025-05 | Rp 41.531.900 |
| 2025-06 | Rp 31.008.850 |
| 2025-07 | Rp 29.731.000 |
| 2025-08 | Rp 30.247.900 |

5 teratas:

| Nama | Total |
|---|---|
| Sepatu Lari Ringan | Rp 30.691.500 |
| Sneakers Putih | Rp 23.497.500 |
| Sepatu Kulit Formal | Rp 22.275.000 |
| Celana Jeans Slim | Rp 15.928.500 |
| Kemeja Batik Modern | Rp 15.072.000 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_spasi` | 2 |
| `cb_kota_variasi` | 1 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 9 |
| `d1_email_kosong` | 4 |
| `d1_email_spasi` | 8 |
| `d1_email_tanpa_at` | 4 |
| `d1_hp_format` | 39 |
| `d1_hp_kosong` | 1 |
| `d1_kota_variasi` | 20 |
| `d1_nama_huruf` | 28 |
| `d1_nama_spasi` | 13 |
| `d1_segmen_huruf` | 8 |
| `d1_segmen_kosong` | 9 |
| `d1_tgl_slash` | 21 |
| `d1_tgl_strip` | 11 |
| `d1_tgl_teks` | 20 |
| `f_cb_huruf` | 38 |
| `f_cb_spasi` | 44 |
| `f_cb_tanpa_strip` | 25 |
| `f_d1_huruf` | 51 |
| `f_d1_spasi` | 26 |
| `f_d1_tanpa_strip` | 18 |
| `f_diskon_format` | 183 |
| `f_diskon_kosong` | 12 |
| `f_duplikat` | 10 |
| `f_harga_null` | 20 |
| `f_item_huruf` | 56 |
| `f_item_spasi` | 37 |
| `f_item_tanpa_strip` | 20 |
| `f_metode_variasi` | 140 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 23 |
| `f_qty_tidak_wajar` | 24 |
| `f_status_null` | 19 |
| `f_status_variasi` | 56 |
| `f_tgl_slash` | 96 |
| `f_tgl_strip` | 57 |
| `it_aktif_variasi` | 7 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 6 |
| `it_kat_variasi` | 8 |
| `it_kode_spasi` | 2 |
| `it_nama_huruf` | 4 |
| `it_stok_negatif` | 1 |
| `it_stok_teks` | 1 |

---

## Paket 06: KirimCepat Express

Database `kirimcepat`, tabel `pengiriman`. Periode 2025-04-01 sampai 2025-09-30 (kalender penuh 183 hari; hari antara tanggal transaksi pertama dan terakhir: 183).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Pengirim (CSV) | 105 | 5 | 100 |
| Layanan (Excel, data saja) | 22 | 2 | 20 |
| Hub (Excel) | 6 | 1 | 5 |
| pengiriman (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: pengirim tak terdaftar **8** baris, layanan tak terdaftar **5** baris. Harga kosong di master: `LYN-007, LYN-013`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 72.791.300** |
| Jumlah transaksi dihitung | 307 |
| Rata-rata nilai transaksi | Rp 237.105 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 35 |
| Dikecualikan karena Batal | 58 |
| Pengirim unik yang bertransaksi | 101 |
| Hub tertinggi | Hub Makassar (Rp 19.263.750) |
| Bulan tertinggi | 2025-08 (Rp 16.465.650) |

Per kategori:

| Kategori | Total |
|---|---|
| Kargo | Rp 45.309.250 |
| Instan | Rp 16.183.600 |
| Ekspres | Rp 8.259.900 |
| Reguler | Rp 2.912.800 |
| Tidak Terdaftar | Rp 125.750 |

Per hub:

| Hub | Total |
|---|---|
| Hub Makassar | Rp 19.263.750 |
| Hub Medan Barat | Rp 15.699.600 |
| Hub Jakarta Timur | Rp 15.480.900 |
| Hub Surabaya Utara | Rp 11.493.450 |
| Hub Bandung Kota | Rp 10.853.600 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-04 | Rp 12.814.400 |
| 2025-05 | Rp 8.167.950 |
| 2025-06 | Rp 9.900.500 |
| 2025-07 | Rp 11.994.250 |
| 2025-08 | Rp 16.465.650 |
| 2025-09 | Rp 13.448.550 |

5 teratas:

| Nama | Total |
|---|---|
| Kargo Pindahan Rumah | Rp 19.162.500 |
| Kargo Barang Besar | Rp 14.311.000 |
| Kurir Mobil Box | Rp 8.745.000 |
| Kargo Udara per 10kg | Rp 6.856.250 |
| Kargo Darat per 10kg | Rp 3.163.500 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_huruf` | 2 |
| `cb_kode_spasi` | 1 |
| `cb_kota_variasi` | 3 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 11 |
| `d1_email_kosong` | 7 |
| `d1_email_spasi` | 6 |
| `d1_email_tanpa_at` | 1 |
| `d1_hp_format` | 34 |
| `d1_hp_kosong` | 3 |
| `d1_kota_alias` | 2 |
| `d1_kota_variasi` | 23 |
| `d1_nama_huruf` | 32 |
| `d1_nama_spasi` | 12 |
| `d1_segmen_huruf` | 10 |
| `d1_segmen_kosong` | 6 |
| `d1_tgl_slash` | 28 |
| `d1_tgl_strip` | 7 |
| `d1_tgl_teks` | 15 |
| `f_cb_huruf` | 44 |
| `f_cb_spasi` | 44 |
| `f_cb_tanpa_strip` | 20 |
| `f_d1_huruf` | 69 |
| `f_d1_spasi` | 26 |
| `f_d1_tanpa_strip` | 26 |
| `f_diskon_format` | 174 |
| `f_diskon_kosong` | 19 |
| `f_duplikat` | 10 |
| `f_harga_null` | 12 |
| `f_item_huruf` | 47 |
| `f_item_spasi` | 42 |
| `f_item_tanpa_strip` | 18 |
| `f_metode_variasi` | 148 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 17 |
| `f_qty_tidak_wajar` | 18 |
| `f_status_null` | 17 |
| `f_status_variasi` | 71 |
| `f_tgl_slash` | 99 |
| `f_tgl_strip` | 63 |
| `it_aktif_variasi` | 8 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 4 |
| `it_kat_variasi` | 7 |
| `it_kode_huruf` | 1 |
| `it_kode_spasi` | 2 |
| `it_nama_huruf` | 3 |
| `it_stok_negatif` | 1 |
| `it_stok_teks` | 2 |

---

## Paket 07: CineKita Cinema

Database `cinekita`, tabel `penjualan_tiket`. Periode 2025-05-01 sampai 2025-10-31 (kalender penuh 184 hari; hari antara tanggal transaksi pertama dan terakhir: 183).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Anggota (CSV) | 105 | 5 | 100 |
| Produk (Excel, data saja) | 22 | 2 | 20 |
| Bioskop (Excel) | 6 | 1 | 5 |
| penjualan_tiket (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: anggota tak terdaftar **8** baris, produk tak terdaftar **5** baris. Harga kosong di master: `PRD-008, PRD-011`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 70.364.575** |
| Jumlah transaksi dihitung | 294 |
| Rata-rata nilai transaksi | Rp 239.335 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 35 |
| Dikecualikan karena Batal | 71 |
| Anggota unik yang bertransaksi | 104 |
| Bioskop tertinggi | CineKita Beachwalk (Rp 16.693.100) |
| Bulan tertinggi | 2025-08 (Rp 16.833.925) |

Per kategori:

| Kategori | Total |
|---|---|
| Paket Combo | Rp 29.303.000 |
| Tiket | Rp 20.597.500 |
| Popcorn | Rp 13.988.250 |
| Minuman | Rp 6.349.200 |
| Tidak Terdaftar | Rp 126.625 |

Per bioskop:

| Bioskop | Total |
|---|---|
| CineKita Beachwalk | Rp 16.693.100 |
| CineKita Sun Plaza | Rp 16.096.725 |
| CineKita Paris Van Java | Rp 15.307.550 |
| CineKita Tunjungan Plaza | Rp 12.775.300 |
| CineKita Grand Indonesia | Rp 9.491.900 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-05 | Rp 10.087.600 |
| 2025-06 | Rp 8.765.850 |
| 2025-07 | Rp 13.018.950 |
| 2025-08 | Rp 16.833.925 |
| 2025-09 | Rp 12.646.650 |
| 2025-10 | Rp 9.011.600 |

5 teratas:

| Nama | Total |
|---|---|
| Combo Keluarga | Rp 9.672.000 |
| Tiket Premier | Rp 8.388.000 |
| Combo Berdua | Rp 6.979.500 |
| Tiket Sweetbox | Rp 6.227.000 |
| Popcorn Mix Jumbo | Rp 4.743.000 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_huruf` | 1 |
| `cb_kode_spasi` | 1 |
| `cb_kota_variasi` | 2 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 8 |
| `d1_email_kosong` | 6 |
| `d1_email_spasi` | 11 |
| `d1_email_tanpa_at` | 3 |
| `d1_hp_format` | 39 |
| `d1_hp_kosong` | 3 |
| `d1_kota_variasi` | 27 |
| `d1_nama_huruf` | 32 |
| `d1_nama_spasi` | 16 |
| `d1_segmen_huruf` | 10 |
| `d1_segmen_kosong` | 5 |
| `d1_tgl_slash` | 23 |
| `d1_tgl_strip` | 11 |
| `d1_tgl_teks` | 16 |
| `f_cb_huruf` | 61 |
| `f_cb_spasi` | 40 |
| `f_cb_tanpa_strip` | 26 |
| `f_d1_huruf` | 56 |
| `f_d1_spasi` | 43 |
| `f_d1_tanpa_strip` | 34 |
| `f_diskon_format` | 186 |
| `f_diskon_kosong` | 26 |
| `f_duplikat` | 10 |
| `f_harga_null` | 17 |
| `f_item_huruf` | 48 |
| `f_item_spasi` | 36 |
| `f_item_tanpa_strip` | 26 |
| `f_metode_variasi` | 165 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 16 |
| `f_qty_tidak_wajar` | 19 |
| `f_status_null` | 9 |
| `f_status_variasi` | 67 |
| `f_tgl_slash` | 98 |
| `f_tgl_strip` | 57 |
| `it_aktif_variasi` | 13 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 5 |
| `it_kat_variasi` | 5 |
| `it_kode_huruf` | 1 |
| `it_kode_spasi` | 3 |
| `it_nama_huruf` | 2 |
| `it_stok_kosong` | 2 |
| `it_stok_negatif` | 2 |
| `it_stok_teks` | 2 |

---

## Paket 08: BukuKita

Database `bukukita`, tabel `penjualan`. Periode 2025-08-01 sampai 2026-01-31 (kalender penuh 184 hari; hari antara tanggal transaksi pertama dan terakhir: 184).

### Jumlah baris (A1, A3)

| Tabel | Baris di file | Duplikat | Baris bersih |
|---|---|---|---|
| Pelanggan (CSV) | 105 | 5 | 100 |
| Produk (Excel, data saja) | 22 | 2 | 20 |
| Toko (Excel) | 6 | 1 | 5 |
| penjualan (SQL) | 410 | 10 | 400 |

Kunci yatim setelah dibersihkan: pelanggan tak terdaftar **8** baris, produk tak terdaftar **5** baris. Harga kosong di master: `PRD-013, PRD-014`.

### Angka validasi (C3)

| Ukuran | Nilai |
|---|---|
| **Total Penjualan Bersih** | **Rp 91.117.450** |
| Jumlah transaksi dihitung | 307 |
| Rata-rata nilai transaksi | Rp 296.800 |
| Baris fakta setelah bersih | 400 |
| Dikecualikan karena Qty tidak valid | 27 |
| Dikecualikan karena Batal | 66 |
| Pelanggan unik yang bertransaksi | 99 |
| Toko tertinggi | BukuKita Ubud (Rp 23.561.050) |
| Bulan tertinggi | 2025-10 (Rp 17.920.100) |

Per kategori:

| Kategori | Total |
|---|---|
| Buku Nonfiksi | Rp 38.758.300 |
| Buku Fiksi | Rp 28.885.100 |
| Hobi dan Kado | Rp 12.877.000 |
| Alat Tulis | Rp 9.932.050 |
| Tidak Terdaftar | Rp 665.000 |

Per toko:

| Toko | Total |
|---|---|
| BukuKita Ubud | Rp 23.561.050 |
| BukuKita Malioboro | Rp 19.415.200 |
| BukuKita Tunjungan | Rp 16.772.000 |
| BukuKita Pusat | Rp 15.916.150 |
| BukuKita Dipatiukur | Rp 15.453.050 |

Per bulan:

| Bulan | Total |
|---|---|
| 2025-08 | Rp 15.397.550 |
| 2025-09 | Rp 10.401.650 |
| 2025-10 | Rp 17.920.100 |
| 2025-11 | Rp 14.754.950 |
| 2025-12 | Rp 16.956.950 |
| 2026-01 | Rp 15.686.250 |

5 teratas:

| Nama | Total |
|---|---|
| Sejarah Indonesia Modern | Rp 11.824.750 |
| Novel Bumi Manusia | Rp 10.450.000 |
| Atomic Habits Edisi Indonesia | Rp 8.866.800 |
| Belajar Python dari Nol | Rp 8.124.000 |
| Novel Laskar Pelangi | Rp 6.840.400 |

### Masalah yang ditanam

| Kode | Jumlah |
|---|---|
| `cb_duplikat` | 1 |
| `cb_kode_huruf` | 1 |
| `cb_kode_spasi` | 2 |
| `cb_kota_variasi` | 2 |
| `d1_duplikat` | 5 |
| `d1_email_huruf` | 7 |
| `d1_email_kosong` | 1 |
| `d1_email_spasi` | 8 |
| `d1_email_tanpa_at` | 4 |
| `d1_hp_format` | 29 |
| `d1_hp_kosong` | 6 |
| `d1_kota_alias` | 1 |
| `d1_kota_variasi` | 24 |
| `d1_nama_huruf` | 29 |
| `d1_nama_spasi` | 19 |
| `d1_segmen_huruf` | 10 |
| `d1_segmen_kosong` | 4 |
| `d1_tgl_slash` | 30 |
| `d1_tgl_strip` | 7 |
| `d1_tgl_teks` | 15 |
| `f_cb_huruf` | 58 |
| `f_cb_spasi` | 35 |
| `f_cb_tanpa_strip` | 21 |
| `f_d1_huruf` | 33 |
| `f_d1_spasi` | 38 |
| `f_d1_tanpa_strip` | 29 |
| `f_diskon_format` | 174 |
| `f_diskon_kosong` | 23 |
| `f_duplikat` | 10 |
| `f_harga_null` | 27 |
| `f_item_huruf` | 49 |
| `f_item_spasi` | 28 |
| `f_item_tanpa_strip` | 31 |
| `f_metode_variasi` | 136 |
| `f_orphan_d1` | 8 |
| `f_orphan_item` | 5 |
| `f_qty_kosong` | 15 |
| `f_qty_tidak_wajar` | 12 |
| `f_status_null` | 15 |
| `f_status_variasi` | 75 |
| `f_tgl_slash` | 115 |
| `f_tgl_strip` | 56 |
| `it_aktif_variasi` | 10 |
| `it_duplikat` | 2 |
| `it_harga_kosong` | 2 |
| `it_harga_teks` | 4 |
| `it_kat_variasi` | 4 |
| `it_kode_huruf` | 1 |
| `it_kode_spasi` | 3 |
| `it_nama_huruf` | 1 |
| `it_stok_kosong` | 1 |
| `it_stok_teks` | 2 |

---

## Kunci Bagian D (ringkas)

**Varian A.** (1) OLTP dioptimalkan untuk transaksi harian; query analitik berat menurunkan kinerja dan struktur ter-normalisasi menyulitkan analisis. ETL menarik, membersihkan, dan memuat data ke wadah analitik terpisah. (2) Relasi mencocokkan nilai persis; `mbr0045`, ` MBR-0045 `, dan `MBR-0045` dianggap kunci berbeda sehingga baris fakta tidak menemukan pasangan. (3) Calculated column dihitung per baris saat refresh dan disimpan (cocok untuk `Nilai_Bersih`, atau dihitung di Power Query); measure dihitung saat query sesuai konteks filter (wajib untuk `Total Penjualan Bersih`, agar dinamis terhadap slicer).

**Varian B.** (1) Fakta berisi peristiwa terukur (Qty, Nilai_Bersih); dimensi berisi konteks (Kategori, Kota, Nama Bulan). (2) Nilai terhitung ganda karena satu kunci cocok ke banyak baris dimensi, sehingga total membesar dan filter ambigu. (3) Menghapus kehilangan jejak audit dan mengubah jumlah transaksi/rata-rata tanpa kontrol; baris yang dihapus tidak dapat dipulihkan atau ditelusuri; menandai memungkinkan analisis kualitas data dan aturan bisa diubah.
