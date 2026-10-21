/* ===== Bank Soal P2: ETL, dataset & kasus berbeda ===== */
const _R = BI.rng, _sum = BI.sum;
const _grp = (rows, k, f, agg) => BI.groupBy(rows, k, f, agg).sort((a, b) => b.value - a.value);
const _pad = (n, l = 3) => String(n).padStart(l, '0');
const _dt = (r, y, m) => `${y}-${_pad(m, 2)}-${_pad(1 + Math.floor(r() * 28), 2)}`;
const NL = String.fromCharCode(10);

/* Set A: distribusi sembako, pemisah titik koma */
const sem = (() => {
  const r = _R(11), brg = [['Beras 5kg', 68000], ['Minyak 2L', 36000], ['Gula 1kg', 17500], ['Telur 1kg', 29000], ['Tepung 1kg', 13500], ['Mie Instan Dus', 112000]], gd = ['Jakarta', 'Surabaya', 'Medan', 'Makassar'], rows = [];
  for (let i = 0; i < 200; i++) { const b = brg[Math.floor(r() * 6)]; rows.push({ PesananID: 'PS' + _pad(i + 1, 4), Tanggal: _dt(r, 2024, 1 + Math.floor(r() * 3)), Gudang: gd[Math.floor(r() * 4)], Barang: b[0], Jumlah: 1 + Math.floor(r() * r() * 30), HargaSatuan: b[1] }); }
  return rows;
})();
const semCsv = () => { const ks = Object.keys(sem[0]); return [ks.join(';'), ...sem.map(r => ks.map(k => r[k]).join(';'))].join(NL); };

/* Set B: tiket travel 3 bulan */
const tiket = (() => {
  const r = _R(22), rute = ['JKT-SUB', 'JKT-DPS', 'SUB-DPS', 'JKT-KNO', 'BDO-DPS'], hrg = { 'JKT-SUB': 950000, 'JKT-DPS': 1250000, 'SUB-DPS': 700000, 'JKT-KNO': 1450000, 'BDO-DPS': 1100000 }, kls = ['Ekonomi', 'Bisnis'], out = {};
  [[1, 90], [2, 110], [3, 130]].forEach(([m, n]) => { out[m] = []; for (let i = 0; i < n; i++) { const rt = rute[Math.floor(r() * 5)], k = kls[r() < 0.8 ? 0 : 1]; out[m].push({ TiketID: `TK${m}${_pad(i + 1)}`, Tanggal: _dt(r, 2024, m), Rute: rt, Kelas: k, Harga: Math.round(hrg[rt] * (k === 'Bisnis' ? 1.8 : 1) / 5000) * 5000, Jumlah: 1 + Math.floor(r() * 4) }); } });
  return out;
})();
const tkAll = [].concat(tiket[1], tiket[2], tiket[3]);

/* Set C: laporan kasir berantakan */
const kasir = (() => {
  const r = _R(33), it = [['Sabun', 12000], ['Sampo', 22000], ['Pasta Gigi', 15000], ['Deterjen', 28000]], rows = [];
  for (let i = 0; i < 60; i++) { const x = it[Math.floor(r() * 4)], q = 1 + Math.floor(r() * 5); rows.push({ KasirID: 'KS' + (1 + Math.floor(r() * 3)), Tanggal: _dt(r, 2024, 3), Item: x[0], Qty: q, Subtotal: q * x[1] }); }
  return rows;
})();
const kasirTxt = () => ['LAPORAN PENJUALAN HARIAN', 'Toko Sinar Jaya', 'Dicetak: 2024-04-01', '', 'KasirID,Tanggal,Item,Qty,Subtotal', ...kasir.map(x => `${x.KasirID},${x.Tanggal},${x.Item},${x.Qty},${x.Subtotal}`), `TOTAL,,,${_sum(kasir.map(x => x.Qty))},${_sum(kasir.map(x => x.Subtotal))}`].join(NL);

/* Set D: database elektronik (SQL) */
const db = (() => {
  const r = _R(44), kota = ['Bandung', 'Semarang', 'Malang', 'Palembang'], pel = [], ps = [];
  for (let i = 0; i < 80; i++) pel.push({ PelangganID: 'C' + _pad(i + 1, 3), Nama: 'Pelanggan ' + (i + 1), Kota: kota[Math.floor(r() * 4)] });
  for (let i = 0; i < 150; i++) ps.push({ PesananID: 'O' + _pad(i + 1, 4), PelangganID: pel[Math.floor(r() * r() * 70)].PelangganID, Tanggal: _dt(r, 2024, 1 + Math.floor(r() * 3)), Total: Math.round((150000 + r() * 4850000) / 1000) * 1000 });
  return { pel, ps };
})();
const dbKota = {}; db.pel.forEach(p => dbKota[p.PelangganID] = p.Kota);

const T2 = [
  { title: 'Distribusi sembako: CSV dengan titik koma', lvl: 'D', mnt: 25, desc: 'Skenario: distributor sembako mengekspor pesanan dari sistem lama. File memakai <b>titik koma (;)</b> sebagai pemisah. Muat dengan delimiter yang benar, lalu rekonsiliasi.',
    files: [{ name: 'soal2A_pesanan_sembako.csv', get: semCsv }],
    tasks: [
      { type: 'choice', q: 'Saat dibuka, semua kolom menyatu menjadi satu kolom. Pengaturan yang harus diubah pada pratinjau Get Data:', o: ['Tipe data', 'Delimiter menjadi Semicolon', 'File Origin menjadi Excel', 'Menambah kolom baru'], a: 1, ex: 'Delimiter harus sesuai pemisah di file.' },
      { type: 'num', q: 'Berapa <b>jumlah baris</b> setelah dimuat dengan benar (tanpa header)?', ans: () => sem.length, tol: 0, ex: 'Rekonsiliasi: bandingkan dengan jumlah baris sumber.' },
      { type: 'num', q: 'Berapa <b>total nilai pesanan</b> (Σ Jumlah × HargaSatuan, Rp)?', ans: () => _sum(sem.map(x => x.Jumlah * x.HargaSatuan)), tol: 1, tip: 'Buat Custom Column: [Jumlah] * [HargaSatuan] sebelum menjumlah.' },
      { type: 'text', q: 'Barang dengan <b>total Jumlah terbanyak</b>?', ans: () => _grp(sem, 'Barang', x => x.Jumlah)[0].key, ex: () => _grp(sem, 'Barang', x => x.Jumlah).map(x => x.key + ' ' + x.value).join('<br>') },
      { type: 'num', q: 'Berapa <b>jumlah gudang unik</b> pada data?', ans: () => new Set(sem.map(x => x.Gudang)).size, tol: 0, tip: 'Count (Distinct) pada kolom Gudang.' },
      { type: 'num', q: 'Berapa pesanan dari gudang <b>Surabaya</b> pada bulan Februari?', ans: () => sem.filter(x => x.Gudang === 'Surabaya' && x.Tanggal.slice(5, 7) === '02').length, tol: 0, hint: 'Pastikan kolom Tanggal bertipe Date lalu filter bulan 2.' }
    ] },
  { title: 'Travel "TripKu": menggabung 3 file bulanan (Append)', lvl: 'M', mnt: 30, desc: 'Skenario: sistem tiket mengekspor satu file per bulan dengan struktur kolom sama. Gabungkan dengan <b>Append Queries</b> (atau <i>Folder</i> connector) sebelum analisis.',
    files: [{ name: 'soal2B_tiket_jan.csv', get: () => tiket[1] }, { name: 'soal2B_tiket_feb.csv', get: () => tiket[2] }, { name: 'soal2B_tiket_mar.csv', get: () => tiket[3] }],
    tasks: [
      { type: 'num', q: 'Berapa <b>jumlah baris</b> setelah ketiga file digabung?', ans: () => tkAll.length, tol: 0, hint: 'Jan 90 + Feb 110 + Mar 130 jika benar; periksa file yang terlewat atau terhitung dua kali.' },
      { type: 'num', q: 'Berapa <b>total tiket terjual</b> (Σ Jumlah)?', ans: () => _sum(tkAll.map(x => x.Jumlah)), tol: 0 },
      { type: 'text', q: 'Rute dengan <b>pendapatan</b> (Σ Jumlah × Harga) tertinggi?', ans: () => _grp(tkAll, 'Rute', x => x.Jumlah * x.Harga)[0].key, ex: () => _grp(tkAll, 'Rute', x => x.Jumlah * x.Harga).map(x => x.key + ': ' + BI.rp(x.value)).join('<br>') },
      { type: 'num', q: 'Berapa <b>pendapatan bulan Maret</b> kelas Bisnis (Rp)?', ans: () => _sum(tiket[3].filter(x => x.Kelas === 'Bisnis').map(x => x.Jumlah * x.Harga)), tol: 1 },
      { type: 'choice', q: 'Tiga file bulanan dengan kolom sama sebaiknya digabung memakai…', o: ['Merge (join)', 'Append (menumpuk baris)', 'Pivot', 'Group By'], a: 1, ex: 'Append menumpuk baris dari tabel berstruktur sama; Merge menggabung kolom berdasarkan kunci.' },
      { type: 'do', q: 'Dokumentasikan langkah <b>Append</b>: nama query, jumlah baris tiap file, jumlah baris gabungan, dan tambahkan kolom <i>SumberFile</i> agar bisa ditelusuri.', rubric: ['3 query dimuat', 'Query gabungan Append', 'Kolom SumberFile ada', 'Total baris direkonsiliasi'] }
    ] },
  { title: 'Kasir "Sinar Jaya": file dengan judul laporan & baris total', lvl: 'M', mnt: 25, desc: 'Skenario: laporan kasir ini dicetak dari aplikasi lama. Ada <b>judul di atas header</b> dan <b>baris TOTAL di bawah</b>. Bersihkan agar hanya data transaksi yang termuat.',
    files: [{ name: 'soal2C_laporan_kasir.csv', get: kasirTxt, text: true }],
    tasks: [
      { type: 'num', q: 'Berapa <b>baris teratas</b> yang harus dibuang (Remove Top Rows) sebelum header kolom?', ans: 4, tol: 0, ex: 'Judul, nama toko, tanggal cetak, dan satu baris kosong = 4 baris.' },
      { type: 'num', q: 'Berapa <b>baris data transaksi</b> sebenarnya (tanpa baris TOTAL)?', ans: () => kasir.length, tol: 0, tip: 'Remove Bottom Rows 1, atau filter KasirID ≠ "TOTAL".' },
      { type: 'num', q: 'Berapa <b>total Subtotal</b> yang benar (Rp)?', ans: () => _sum(kasir.map(x => x.Subtotal)), tol: 1, hint: 'Jika angka Anda dua kali lipat, baris TOTAL ikut dijumlahkan.' },
      { type: 'choice', q: 'Mengapa baris "TOTAL" harus dibuang sebelum analisis?', o: ['Agar file kecil', 'Karena akan terhitung ganda saat dijumlahkan', 'Karena berwarna berbeda', 'Tidak perlu dibuang'], a: 1, ex: 'Total bawaan sumber menggandakan hasil.' },
      { type: 'text', q: 'Kasir dengan <b>jumlah Qty terbanyak</b>? (misal KS2)', ans: () => _grp(kasir, 'KasirID', x => x.Qty)[0].key, ex: () => _grp(kasir, 'KasirID', x => x.Qty).map(x => x.key + ' ' + x.value).join(', ') },
      { type: 'choice', q: 'Langkah Power Query yang tepat untuk mengubah baris pertama (setelah baris dibuang) menjadi nama kolom:', o: ['Transpose', 'Use First Row as Headers', 'Unpivot', 'Fill Down'], a: 1 }
    ] },
  { title: 'Database toko elektronik (SQL): dua tabel', lvl: 'M', mnt: 30, desc: 'Skenario: data berada di database relasional. Jalankan skrip SQL pada SQLite/MySQL lab, lalu <b>Get Data → Database</b> dan muat tabel <i>pelanggan</i> dan <i>pesanan</i>. Jika belum ada server, jawab dengan memuat tabel dari file (kolom sama).',
    files: [{ name: 'soal2D_toko_elektronik.sql', get: () => BI.sqlDump({ pelanggan: db.pel, pesanan: db.ps }), text: true }, { name: 'soal2D_pelanggan.csv', get: () => db.pel }, { name: 'soal2D_pesanan.csv', get: () => db.ps }],
    tasks: [
      { type: 'num', q: 'Berapa <b>jumlah pelanggan</b> terdaftar?', ans: () => db.pel.length, tol: 0 },
      { type: 'num', q: 'Berapa <b>pelanggan unik yang pernah memesan</b>?', ans: () => new Set(db.ps.map(x => x.PelangganID)).size, tol: 0, tip: 'Count (Distinct) PelangganID pada tabel pesanan.' },
      { type: 'num', q: 'Berapa <b>pelanggan yang belum pernah memesan</b>?', ans: () => db.pel.length - new Set(db.ps.map(x => x.PelangganID)).size, tol: 0, ex: 'Pelanggan − pelanggan yang memesan. Dasar analisis pelanggan tidak aktif.' },
      { type: 'num', q: 'Berapa <b>total nilai seluruh pesanan</b> (Rp)?', ans: () => _sum(db.ps.map(x => x.Total)), tol: 1 },
      { type: 'text', q: 'Kota pelanggan dengan <b>total nilai pesanan tertinggi</b>? (butuh gabungan tabel)', ans: () => _grp(db.ps.map(x => ({ k: dbKota[x.PelangganID], t: x.Total })), 'k', x => x.t)[0].key, ex: () => 'Hubungkan pesanan[PelangganID] ke pelanggan[PelangganID]; hasil per kota: ' + _grp(db.ps.map(x => ({ k: dbKota[x.PelangganID], t: x.Total })), 'k', x => x.t).map(x => x.key + ' ' + BI.short(x.value)).join(', ') },
      { type: 'choice', q: 'Tabel pesanan berisi jutaan baris dan perlu data terbaru menit-menit. Mode koneksi yang paling relevan:', o: ['Import saja', 'DirectQuery', 'CSV manual', 'Tidak bisa'], a: 1, ex: 'DirectQuery tidak menyalin data; pertimbangkan kinerja sumber.' },
      { type: 'do', q: 'Tulis <b>alasan memilih Import atau DirectQuery</b> untuk kasus ini (ukuran data, frekuensi pembaruan, beban pada database operasional).', rubric: ['Menyebut ukuran data', 'Menyebut kebutuhan kesegaran', 'Menyebut dampak ke sistem OLTP'] }
    ] },
  { title: 'Konsep ETL, OLTP vs OLAP (pilihan ganda kasus)', lvl: 'D', mnt: 15, desc: 'Tanpa dataset. Tentukan jenis sistem atau tahap ETL untuk tiap situasi.',
    tasks: [
      { type: 'choice', q: 'Menyimpan pembayaran pelanggan saat checkout adalah beban kerja…', o: ['OLTP', 'OLAP', 'Data mart', 'Staging'], a: 0 },
      { type: 'choice', q: 'Menghitung tren penjualan per wilayah per bulan selama 5 tahun cocok pada…', o: ['OLTP', 'OLAP / data warehouse', 'Spreadsheet kasir', 'Email'], a: 1 },
      { type: 'choice', q: 'Mengubah "Sby", "SBY", "sby" menjadi "Surabaya" adalah tahap…', o: ['Extract', 'Transform', 'Load', 'Report'], a: 1 },
      { type: 'choice', q: 'Menyalin tabel penjualan dari server ke area transit tanpa mengubah isi adalah tahap…', o: ['Extract', 'Transform', 'Load', 'Visualize'], a: 0 },
      { type: 'choice', q: 'Hasil akhir yang sudah bersih ditulis ke tabel fakta di warehouse adalah tahap…', o: ['Extract', 'Transform', 'Load', 'Profil'], a: 2 },
      { type: 'choice', q: 'Setelah Load, 10.000 baris sumber menjadi 9.870 baris. Tindakan terbaik:', o: ['Abaikan', 'Telusuri 130 baris yang hilang (rekonsiliasi)', 'Hapus data', 'Tambah visual'], a: 1 },
      { type: 'choice', q: 'Fungsi utama staging area:', o: ['Menampilkan dashboard', 'Menampung data mentah sebelum transformasi', 'Menyimpan password', 'Mempercantik tabel'], a: 1 },
      { type: 'choice', q: 'File Excel dengan sel gabungan dan banyak baris judul sebagai sumber data berisiko karena…', o: ['Terlalu aman', 'Struktur tidak konsisten sehingga sulit diotomatisasi', 'Ukuran kecil', 'Tidak ada alasan'], a: 1 }
    ] },
  { title: 'Tantangan: rancang pipeline ETL marketplace', lvl: 'T', mnt: 30, desc: 'Skenario: marketplace punya 3 sumber: database pesanan (MySQL), file CSV iklan dari agensi, dan Excel target dari tim sales. Rancang alur ETL.',
    tasks: [
      { type: 'do', q: 'Buat <b>diagram alur</b> Extract → Staging → Transform → Load → Dashboard dengan nama sumber dan tabel tujuan.', rubric: ['3 sumber digambar', 'Ada staging', 'Tabel fakta & dimensi tujuan disebut'] },
      { type: 'do', q: 'Daftarkan <b>8 aturan transformasi</b> (mis. standarisasi kota, format tanggal, mata uang, deduplikasi pesanan).', rubric: ['≥ 8 aturan', 'Tiap aturan punya contoh sebelum/sesudah', 'Ada aturan penanganan null'] },
      { type: 'do', q: 'Rancang <b>uji rekonsiliasi</b> setelah Load: minimal 3 pemeriksaan (jumlah baris, total nilai, tanggal terbaru).', rubric: ['Pemeriksaan jumlah baris', 'Pemeriksaan total nilai', 'Pemeriksaan kesegaran data'] }
    ] }
];
BI.soal('#soal-box', T2);
