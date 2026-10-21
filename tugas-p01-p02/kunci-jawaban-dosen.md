# Kunci Jawaban Dosen: Tugas Terpadu P1–P2 (NusaMart)

Dokumen ini khusus dosen. Jangan dibagikan ke mahasiswa.

## Isi paket

| Berkas | Untuk |
|---|---|
| `tugas-p01-p02.html` | Soal untuk mahasiswa (buka di browser) |
| `data/penjualan_jawa.csv` | Sumber 1 |
| `data/penjualan_sumatera.xlsx` | Sumber 2 |
| `data/penjualan_timur.sql` | Sumber 3 (dialek MySQL/MariaDB) |

## Angka acuan rekonsiliasi

| Sumber | Baris data | Total penjualan (Qty × Harga × (1 − Diskon/100)) |
|---|---|---|
| Jawa (CSV) | 180 | Rp 1.176.897.750 |
| Sumatera (Excel) | 150 | Rp 912.270.375 |
| Indonesia Timur (SQL) | 120 | Rp 807.336.000 |
| **Gabungan** | **450** | **Rp 2.896.504.125** |

Total unit terjual: 2.869.

Pendapatan per kategori: Elektronik Rp 2.108.446.700, Fashion Rp 365.072.575, Rumah Tangga Rp 355.261.050, Makanan Rp 67.723.800.

Pendapatan per bulan 2026: Jan Rp 545.549.375, Feb Rp 323.650.625, Mar Rp 310.249.200, Apr Rp 511.182.025, Mei Rp 593.240.650, Jun Rp 612.632.250.

Kota tertinggi: Palembang Rp 343.267.100. Terendah: Manado Rp 140.842.900.

## Jebakan yang sengaja ditanam

| # | Jebakan | Gejala jika salah | Perbaikan |
|---|---|---|---|
| 1 | CSV memakai titik desimal gaya Inggris (`4800000.00`) | Locale Indonesia membaca titik sebagai pemisah ribuan, harga Jawa menjadi 100× lipat; total Jawa jadi ±Rp 117 miliar | Change Type → Using Locale → English (United States) |
| 2 | Excel punya sheet `Catatan` selain `Penjualan` | Query berisi 2 baris teks, bukan transaksi | Pilih sheet `Penjualan` |
| 3 | Header Excel `Harga Satuan` (spasi), file lain `Harga_Satuan` | Setelah Append muncul dua kolom harga, sebagian `null`; total salah | Rename ke `Harga_Satuan` sebelum Append |
| 4 | Sel harga Excel berformat `$#,##0.00` | Mahasiswa mengira mata uang USD | Nilai sebenarnya Rupiah; format ulang ke Rp |
| 5 | SQL harus dijalankan dulu | Tabel tidak ditemukan di Navigator | Eksekusi skrip `.sql` |

Cek cepat jebakan 1: harga produk yang sama antar cabang harus selisih kecil (pengali cabang 1,00 / 1,04 / 1,08, dibulatkan 500). Selisih puluhan kali lipat berarti locale salah.

## Langkah Power Query yang diharapkan

1. Tiga query sumber, tipe data diseragamkan: `Tanggal` Date, `Qty` dan `Diskon_Persen` Whole number, `Harga_Satuan` Fixed decimal.
2. Home → Append Queries as New → Three or more tables → `Penjualan_Gabungan` (450 baris).
3. Custom Column:
   ```
   [Qty] * [Harga_Satuan] * (1 - [Diskon_Persen] / 100)
   ```
   Beri nama `Total_Penjualan`, tipe Fixed decimal.
4. Tiga query sumber: Enable Load dimatikan.

Ekuivalen M untuk append: `Table.Combine({Jawa_CSV, Sumatera_Excel, Timur_SQL})`.

## Format Rupiah yang diharapkan

- Regional Settings: Indonesian (Indonesia).
- Kolom/measure uang: Format Currency Rupiah, atau Custom `"Rp" #,##0`.
- Teks dinamis: `"Rp " & FORMAT([Total Pendapatan], "#,0", "id-ID")` menghasilkan `Rp 2.896.504.125`.
- Kartu KPI: Display units = None.
- Tidak ada `$` atau `1.23B` tersisa.

## Rubrik (100 poin)

| Aspek | Poin | Tolok ukur penuh |
|---|---|---|
| Extract & rekonsiliasi | 20 | 3 sumber terbaca; baris sumber vs hasil tercatat dan cocok (180 / 150 / 120 / 450) |
| Append & struktur | 25 | Satu tabel 450 baris; tanpa kolom ganda/`null` tak wajar; tipe data benar; `Total_Penjualan` benar (Rp 2.896.504.125) |
| Format Rupiah | 20 | Locale benar; semua nilai uang berformat Indonesia di kartu, tabel, tooltip, sumbu |
| Tampilan dashboard | 25 | Semua visual wajib; maksimal 4 warna konsisten; tata letak rapi; judul berupa insight; slicer berfungsi |
| Insight & dokumentasi | 10 | Laporan 1 halaman; ≥3 masalah dengan solusi; 3 insight + 1 rekomendasi berangka benar |

## Insight yang bisa muncul (pembanding)

- Elektronik menyumbang ±73% pendapatan; Makanan kurang dari 3%.
- Pendapatan Februari–Maret turun sekitar 40% dari Januari, lalu naik kembali di April–Juni (Juni tertinggi).
- Jawa memimpin per cabang, tetapi kota tertinggi justru Palembang (Sumatera).

## Catatan teknis

- Skrip `.sql` memakai `CREATE DATABASE IF NOT EXISTS nusamart` lalu tabel `penjualan_timur`. Sudah diuji isi dan jumlah barisnya (120 baris).
- Jika lab tidak punya MySQL, beri mahasiswa alternatif: SQL Server/PostgreSQL perlu penyesuaian kecil pada `CREATE DATABASE` dan `USE`.
