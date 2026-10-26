# Kunci Dosen: Praktikum Mandiri Pertemuan 3 (SegarMart)

Dokumen ini khusus dosen. Jangan dibagikan ke mahasiswa.

## Paket

| Berkas | Untuk |
|---|---|
| `praktikum-p03-mandiri.html` | Soal mahasiswa (buka di browser) |
| `data/pelanggan_segarmart.csv` | Tabel pelanggan |
| `data/produk_segarmart.xlsx` | Katalog produk (sheet `Produk`, sheet pengecoh `Catatan`) |
| `data/transaksi_segarmart.sql` | Transaksi, dialek MySQL, database `segarmart` |
| `dataset-segarmart-kotor.zip` | Ketiganya dalam satu paket |

Hubungan: `transaksi.ID_Pelanggan` ke `pelanggan.ID_Pelanggan`, `transaksi.Kode_Produk` ke `produk.Kode_Produk`. Kunci kotor di transaksi, sehingga relasi gagal sebelum kunci dibersihkan.

## Angka acuan baris

| Tabel | Baris di file | Duplikat yang harus dihapus | Baris bersih |
|---|---|---|---|
| Pelanggan | 126 | 6 | 120 |
| Produk (data, tanpa judul/total) | 42 | 2 | 40 |
| Transaksi | 462 | 12 | 450 |

`SELECT COUNT(*)` di MySQL harus 462.

Setelah kunci bersih, ada transaksi yatim yang memang tidak punya pasangan (bukan salah mahasiswa, jangan dihapus):
- Transaksi tanpa pelanggan terdaftar: **8** (ID pelanggan PLG-0121 sampai PLG-0130).
- Transaksi tanpa produk terdaftar: **5** (kode PRD-041 sampai PRD-045).

## Total penjualan bersih (angka pembanding)

Syarat: baris setelah dedup, `Status_Kualitas = OK`, `Status` bukan `Batal`, `Harga_Satuan` null diisi dari harga produk, diskon kosong dihitung 0.

| Ukuran | Nilai |
|---|---|
| **Total penjualan bersih** | **Rp 25.908.030** |
| Baris dihitung | 335 |
| Dikecualikan karena Qty (kosong / tidak wajar) | 37 |
| Dikecualikan karena status Batal | 78 |

Per kategori produk:

| Kategori | Total |
|---|---|
| Sembako | Rp 6.697.280 |
| Minuman | Rp 6.005.850 |
| Segar | Rp 4.771.500 |
| Kebersihan | Rp 4.686.100 |
| Snack | Rp 3.550.400 |
| Tidak Terdaftar (produk yatim) | Rp 196.900 |

Urutan pengecualian: Qty tidak valid dicek lebih dulu, baru Batal. Itu sebabnya 37 dan 78 tidak saling tumpang tindih.

Dua produk harganya kosong di Excel dan memang tidak bisa dipulihkan: `PRD-004` dan `PRD-022`. Transaksi untuk keduanya tidak pernah punya `Harga_Satuan` null, jadi tidak memengaruhi total.

## Masalah yang sengaja ditanam

### Pelanggan (CSV, 126 baris file)

| Masalah | Jumlah baris |
|---|---|
| Nama huruf besar atau kecil semua | 27 |
| Nama spasi di tepi | 13 |
| Nama spasi ganda di dalam | 10 |
| Kota variasi huruf atau spasi | 24 |
| Kota alias (Jkt, DKI Jakarta, Sby, Bdg) | 2 |
| Email huruf besar | 6 |
| Email kosong | 7 |
| Email tanpa `@` | 6 |
| Email spasi di tepi | 7 |
| No_HP format campur (strip, +62, 62, tanpa 0) | 40 |
| No_HP kosong | 3 |
| Tanggal `dd/MM/yyyy` | 32 |
| Tanggal `dd-MM-yyyy` | 11 |
| Tanggal teks Indonesia (`21 Juni 2024`) | 19 |
| Segmen kosong | 9 |
| Segmen huruf kapital atau kecil | 11 |
| Duplikat persis | 6 |

### Produk (Excel, 42 baris data)

Struktur: 3 baris di atas bukan data (judul, tanggal pembaruan, baris kosong), header di baris 4, dua baris di bawah (kosong dan `Total: 42 baris`) harus dibuang.

| Masalah | Jumlah baris |
|---|---|
| Kode huruf kecil | 3 |
| Kode spasi di tepi | 1 |
| Nama huruf besar semua | 4 |
| Kategori variasi (kecil, besar+spasi, spasi di depan) | 15 |
| Harga teks `Rp 12.500` | 13 |
| Harga kosong | 2 |
| Stok negatif | 4 |
| Stok kosong | 3 |
| Stok teks `habis` | 2 |
| Aktif variasi (Y, ya, TRUE, Aktif, N, tidak, FALSE, Nonaktif) | 22 |
| Duplikat persis | 2 |

### Transaksi (SQL, 462 baris)

| Masalah | Jumlah baris |
|---|---|
| `ID_Pelanggan` huruf kecil | 69 |
| `ID_Pelanggan` spasi di tepi | 40 |
| `ID_Pelanggan` tanpa tanda hubung (`PLG0045`) | 25 |
| `Kode_Produk` huruf kecil | 54 |
| `Kode_Produk` spasi di tepi | 38 |
| `Kode_Produk` tanpa tanda hubung (`PRD007`) | 31 |
| Tanggal `dd/MM/yyyy` | 112 |
| Tanggal `dd-MM-yyyy` | 57 |
| Qty kosong | 13 |
| Qty tidak wajar (negatif, 0, atau 100 kali lipat) | 24 |
| `Harga_Satuan` null | 27 |
| Diskon format campur (`10%`, `10 %`, `10`) | 210 |
| Diskon kosong | 26 |
| `Metode_Bayar` variasi | 167 |
| `Status` variasi huruf atau spasi | 77 |
| `Status` null | 17 |
| Duplikat persis | 12 |
| Yatim pelanggan | 8 |
| Yatim produk | 5 |

Catatan: angka di tabel dihitung dari generator saat penanaman. Satu baris bisa punya lebih dari satu masalah, jadi kolom tidak dijumlahkan.

## Pemetaan nilai yang diharapkan

`Metode_Bayar` ke 4 nilai:

| Nilai mentah | Hasil |
|---|---|
| `transfer`, `TRANSFER BANK`, `Transfer  Bank`, `Transfer bank ` | Transfer Bank |
| `cod`, `Cash on Delivery`, `COD ` | COD |
| `ewallet`, `E Wallet`, `e-wallet`, `Gopay`, `OVO` | E-Wallet |
| `kartu kredit`, `CC`, `KARTU KREDIT` | Kartu Kredit |

`Status` ke 5 nilai: Selesai, Dikirim, Diproses, Batal, Tidak Diketahui.

## Urutan kerja yang benar

1. Profiling ketiga sumber.
2. Bersihkan kunci (trim, huruf besar, sisipkan `-`) di semua tabel sebelum apa pun yang melibatkan penggabungan.
3. Dedup berdasarkan kunci yang sudah bersih. Dedup sebelum kunci dibersihkan akan meninggalkan duplikat terselubung.
4. Merge transaksi dengan produk untuk mengisi `Harga_Satuan`, setelah `Kode_Produk` bersih.
5. Hitung `Total_Penjualan`, buat relasi, validasi.

## Rubrik (100 poin)

| Aspek | Poin | Tolok ukur penuh |
|---|---|---|
| Profiling dan tabel temuan | 15 | Masalah tiap tabel tercatat dengan jumlah baris yang mendekati tabel di atas |
| Pembersihan sesuai aturan | 35 | Teks, tanggal, nilai terstandar, dan tipe data benar di tiga tabel; baris bersih 120 / 40 / 450 |
| Kunci bersih dan relasi | 20 | Relasi Many-to-One tanpa peringatan; yatim dilaporkan (8 pelanggan, 5 produk), tidak dihapus |
| Total penjualan bersih | 20 | Rp 25.908.030 (toleransi nol); format Rupiah Indonesia |
| Dokumentasi Applied Steps | 10 | Nama langkah jelas, query bernama `Pelanggan_Bersih`, `Produk_Bersih`, `Transaksi_Bersih` |

## Kesalahan umum dan dampaknya pada total

| Kesalahan | Gejala |
|---|---|
| Dedup pelanggan atau produk sebelum kunci dibersihkan (`plg-0001` dan `PLG-0001` dianggap beda) | Duplikat tersisa, relasi Many-to-Many |
| Tidak mengisi `Harga_Satuan` dari produk | Total lebih kecil, 27 baris sebelum filter tidak punya harga |
| Menghapus Qty tidak wajar, lalu mengubahnya (misalnya membagi 100) | Total tidak sama dengan kunci |
| Tidak mengecualikan Batal | Total terlalu besar |
| Diskon kosong diperlakukan null | `Total_Penjualan` null pada 26 baris |
| Tanggal dibaca satu locale | Error atau tanggal tertukar bulan dan hari |

## Cara membuat ulang

Generator ada di `generator/gen2.py` (seed 303). Jalankan dengan `python generator/gen2.py` (butuh `openpyxl`). Ubah seed untuk data baru. Skrip menulis ulang `data/` dan `generator/key2.json`, jadi perbarui angka di dokumen ini dari `key2.json`, lalu buat ulang ZIP.
