/* ===== Bank Soal P1: 5 set, dataset & perintah berbeda ===== */
const _R = BI.rng, _sum = BI.sum;
const _grp = (rows, k, f, agg) => BI.groupBy(rows, k, f, agg).sort((a, b) => b.value - a.value);
const _pad = (n, l = 3) => String(n).padStart(l, '0');
const _date = (r, y, m, span = 28) => `${y}-${_pad(m, 2)}-${_pad(1 + Math.floor(r() * span), 2)}`;

/* Set A: kafe */
const kafe = (() => {
  const r = _R(101), menu = [['Kopi Susu', 'Kopi', 22000], ['Americano', 'Kopi', 20000], ['Latte', 'Kopi', 28000], ['Teh Tarik', 'Non-Kopi', 18000], ['Matcha', 'Non-Kopi', 26000], ['Roti Bakar', 'Makanan', 20000], ['Croissant', 'Makanan', 25000]];
  const cab = ['Bandung', 'Jakarta', 'Yogyakarta'], met = ['Tunai', 'QRIS', 'Kartu'], rows = [];
  for (let i = 0; i < 240; i++) { const m = menu[Math.floor(r() * r() * 7 + r() * 0.5) % 7], bl = 1 + Math.floor(r() * 3); rows.push({ TransaksiID: 'K' + _pad(i + 1), Tanggal: _date(r, 2024, bl), Cabang: cab[Math.floor(r() * 3)], Menu: m[0], Kategori: m[1], Qty: 1 + Math.floor(r() * 4), Harga: m[2], Metode: met[Math.floor(r() * 3)] }); }
  rows.forEach(x => x.Total = x.Qty * x.Harga);
  return rows;
})();
const BLN = ['', 'januari', 'februari', 'maret'];
/* Set B: ride-hailing */
const trip = (() => {
  const r = _R(202), kota = ['Jakarta', 'Surabaya', 'Medan', 'Makassar'], lay = ['Motor', 'Mobil', 'Kirim Barang'], rows = [];
  for (let i = 0; i < 400; i++) { const l = lay[Math.floor(r() * 3)], km = Math.round((1 + r() * r() * 24) * 10) / 10, rate = l === 'Motor' ? 2800 : l === 'Mobil' ? 4200 : 3200, kt = kota[Math.floor(Math.pow(r(), 1.4) * 4)]; rows.push({ TripID: 'T' + _pad(i + 1, 4), Tanggal: _date(r, 2024, 1 + Math.floor(r() * 3)), Kota: kt, Layanan: l, JarakKm: km, Tarif: Math.round((8000 + km * rate) / 500) * 500, DurasiMenit: Math.round(km * 3.2 + 5 + r() * 8), Rating: Math.max(1, Math.min(5, Math.round(5 - r() * r() * 3.6))) }); }
  return rows;
})();
/* Set C: kursus online */
const kursus = (() => {
  const r = _R(303), kr = [['Excel Bisnis', 350000], ['Dasar SQL', 450000], ['Digital Marketing', 500000], ['Power BI', 650000]], kn = ['Instagram', 'Google', 'Referral', 'TikTok'], rows = [];
  for (let i = 0; i < 300; i++) { const k = kr[Math.floor(r() * 4)], x = r(), st = x < 0.55 ? 'Lulus' : x < 0.8 ? 'Berhenti' : 'Aktif'; rows.push({ PesertaID: 'P' + _pad(i + 1, 4), TglDaftar: _date(r, 2024, 1 + Math.floor(r() * 4)), Kursus: k[0], Kanal: kn[Math.floor(Math.pow(r(), 1.3) * 4)], Biaya: k[1], Status: st, Skor: st === 'Lulus' ? Math.round(70 + r() * 30) : '' }); }
  return rows;
})();

const T1 = [
  { title: 'Kafe "Kopi Nusantara": ringkasan transaksi', lvl: 'D', mnt: 25, desc: 'Skenario: pemilik 3 cabang kafe ingin tahu kinerja Januari–Maret 2024. Dataset: 240 transaksi. <b>Tambahkan kolom Total = Qty × Harga</b> sebelum menjawab.',
    files: [{ name: 'soal1A_kafe.csv', get: () => kafe }],
    tasks: [
      { type: 'num', q: 'Impor CSV. Berapa <b>jumlah baris</b> transaksi?', ans: () => kafe.length, tol: 0, ex: 'Home → Get data → Text/CSV → Load. Cek jumlah baris di Data view atau visual Card Count of TransaksiID.' },
      { type: 'num', q: 'Berapa <b>total pendapatan</b> (Rp) seluruh cabang?', ans: () => _sum(kafe.map(x => x.Total)), tol: 1, tip: 'Buat kolom Total (Qty × Harga) lalu Sum. Jangan menjumlah kolom Harga.', ex: () => 'Total = ' + BI.rp(_sum(kafe.map(x => x.Total))) },
      { type: 'text', q: 'Cabang mana yang pendapatannya <b>tertinggi</b>? (nama cabang)', ans: () => _grp(kafe, 'Cabang', x => x.Total)[0].key, ex: () => _grp(kafe, 'Cabang', x => x.Total).map(x => x.key + ': ' + BI.rp(x.value)).join('<br>') },
      { type: 'num', q: 'Berapa <b>persen kontribusi kategori "Kopi"</b> terhadap total pendapatan? (satu desimal)', ans: () => _sum(kafe.filter(x => x.Kategori === 'Kopi').map(x => x.Total)) / _sum(kafe.map(x => x.Total)) * 100, tol: 0.15, tip: 'Pakai visual donut atau Show value as → Percent of grand total.' },
      { type: 'text', q: 'Pada bulan apa pendapatan <b>tertinggi</b>? (nama bulan)', ans: () => { const b = _grp(kafe, x => +x.Tanggal.slice(5, 7), x => x.Total)[0].key; return [BLN[b], String(b)]; }, ex: () => [1, 2, 3].map(b => BLN[b] + ': ' + BI.rp(_sum(kafe.filter(x => +x.Tanggal.slice(5, 7) === b).map(x => x.Total)))).join('<br>') },
      { type: 'num', q: 'Berapa <b>jumlah transaksi dengan metode QRIS</b> di cabang Jakarta?', ans: () => kafe.filter(x => x.Metode === 'QRIS' && x.Cabang === 'Jakarta').length, tol: 0, tip: 'Gunakan filter pane atau slicer Cabang + Metode lalu Count.' },
      { type: 'do', q: 'Bangun <b>dashboard 1 halaman</b>: 3 kartu (Total, Jumlah transaksi, Rata-rata per transaksi), bar pendapatan per cabang, line tren per bulan, dan slicer Metode.', rubric: ['3 kartu angka benar', 'Bar cabang terurut menurun', 'Line tren per bulan', 'Slicer Metode berfungsi', 'Judul visual berupa insight'] }
    ] },
  { title: 'Aplikasi transportasi "GoTrip": perilaku perjalanan', lvl: 'M', mnt: 30, desc: 'Skenario: analis operasional ingin memahami 400 perjalanan Jan–Mar 2024 di 4 kota. Fokus: agregasi bersyarat dan rata-rata.',
    files: [{ name: 'soal1B_gotrip.csv', get: () => trip }],
    tasks: [
      { type: 'num', q: 'Berapa <b>rata-rata tarif</b> (Rp) layanan <i>Motor</i>?', ans: () => BI.avg(trip.filter(x => x.Layanan === 'Motor').map(x => x.Tarif)), tol: 50, tip: 'Pilih agregasi Average (bukan Sum) dan filter Layanan = Motor.' },
      { type: 'text', q: 'Kota dengan <b>jumlah trip terbanyak</b>?', ans: () => _grp(trip, 'Kota', null, 'count')[0].key, ex: () => _grp(trip, 'Kota').map(x => x.key + ' ' + x.n).join(', ') },
      { type: 'num', q: 'Berapa trip dengan <b>rating ≤ 3</b>?', ans: () => trip.filter(x => x.Rating <= 3).length, tol: 0 },
      { type: 'num', q: 'Berapa <b>tarif rata-rata per km</b> secara keseluruhan (total tarif ÷ total jarak)? Bulatkan ke rupiah.', ans: () => _sum(trip.map(x => x.Tarif)) / _sum(trip.map(x => x.JarakKm)), tol: 5, hint: 'Hitung ratio-of-sums (jumlah ÷ jumlah), bukan rata-rata dari tarif per km tiap baris.', ex: 'Ini pelajaran awal measure rasio (Pertemuan 5).' },
      { type: 'num', q: 'Berapa <b>total tarif</b> layanan Kirim Barang di kota Surabaya (Rp)?', ans: () => _sum(trip.filter(x => x.Layanan === 'Kirim Barang' && x.Kota === 'Surabaya').map(x => x.Tarif)), tol: 1 },
      { type: 'choice', q: '"Mengapa rating layanan Mobil di Makassar turun pada Maret?" termasuk jenis analitik…', o: ['Deskriptif', 'Diagnostik', 'Prediktif', 'Preskriptif'], a: 1, ex: 'Pertanyaan "mengapa" = mencari penyebab: diagnostik.' },
      { type: 'do', q: 'Buat <b>scatter</b> JarakKm (X) vs Tarif (Y), warna = Layanan, aktifkan trend line. Tulis 2 kalimat insight tentang layanan yang paling mahal per km.', rubric: ['Scatter dengan 3 warna layanan', 'Trend line aktif', '2 kalimat insight tertulis'] }
    ] },
  { title: 'Kursus online "Belajar.id": funnel peserta', lvl: 'M', mnt: 30, desc: 'Skenario: tim produk menilai 300 pendaftar kursus. Status: Lulus, Berhenti, Aktif. Skor hanya ada untuk peserta Lulus (sel kosong = null).',
    files: [{ name: 'soal1C_kursus.csv', get: () => kursus }],
    tasks: [
      { type: 'num', q: '<b>Completion rate</b> = Lulus ÷ (Lulus + Berhenti), dalam persen (satu desimal). Peserta Aktif tidak dihitung.', ans: () => { const l = kursus.filter(x => x.Status === 'Lulus').length, b = kursus.filter(x => x.Status === 'Berhenti').length; return l / (l + b) * 100; }, tol: 0.15, hint: 'Filter Status ≠ Aktif dulu.' },
      { type: 'text', q: 'Kanal pendaftaran dengan <b>peserta terbanyak</b>?', ans: () => _grp(kursus, 'Kanal', null, 'count')[0].key, ex: () => _grp(kursus, 'Kanal').map(x => x.key + ' ' + x.n).join(', ') },
      { type: 'num', q: 'Total <b>biaya kursus</b> (Rp) dari peserta berstatus Lulus atau Aktif (bukan yang Berhenti)?', ans: () => _sum(kursus.filter(x => x.Status !== 'Berhenti').map(x => x.Biaya)), tol: 1 },
      { type: 'num', q: '<b>Rata-rata skor</b> peserta Lulus (dua desimal).', ans: () => BI.avg(kursus.filter(x => x.Status === 'Lulus').map(x => x.Skor)), tol: 0.06, hint: 'Skor kosong tidak ikut dihitung oleh Average; pastikan kolom bertipe angka.' },
      { type: 'text', q: 'Kursus dengan <b>completion rate tertinggi</b>? (nama kursus)', ans: () => { const g = [...new Set(kursus.map(x => x.Kursus))].map(k => { const l = kursus.filter(x => x.Kursus === k && x.Status === 'Lulus').length, b = kursus.filter(x => x.Kursus === k && x.Status === 'Berhenti').length; return { k, v: l / (l + b) }; }).sort((a, b) => b.v - a.v); return g[0].k; }, tip: 'Perlu measure rasio per kursus; atau hitung Lulus & Berhenti per kursus lalu bagi.' },
      { type: 'choice', q: 'Visual terbaik untuk membandingkan completion rate antar 4 kursus:', o: ['Pie chart', 'Bar chart terurut', 'Line chart', 'Peta'], a: 1, ex: 'Perbandingan antar kategori = bar. Pie sulit dibandingkan.' },
      { type: 'do', q: 'Tulis <b>1 pertanyaan bisnis</b> dan <b>1 rekomendasi</b> untuk tim produk berdasar dashboard Anda (misal: kanal mana yang perlu ditambah anggaran?). Sertakan 1 visual pendukung.', rubric: ['Pertanyaan bisnis jelas', 'Visual mendukung', 'Rekomendasi spesifik dan terukur'] }
    ] },
  { title: 'Konsep BI: pilihan ganda kasus', lvl: 'D', mnt: 15, desc: 'Tanpa dataset. Latihan konsep: ruang lingkup BI, DIKW, siklus data, jenis analitik, dan pemilihan tool.',
    tasks: [
      { type: 'choice', q: 'Toko mencatat 10.000 transaksi. Tabel ringkasan penjualan per bulan berada di tingkat DIKW…', o: ['Data', 'Informasi', 'Pengetahuan', 'Wawasan'], a: 1, ex: 'Data yang diringkas dan diberi konteks = informasi.' },
      { type: 'choice', q: 'Manakah yang BUKAN tujuan utama BI?', o: ['Mempercepat keputusan', 'Menyatukan data dari banyak sumber', 'Menggantikan semua keputusan manajer', 'Menyajikan KPI terpercaya'], a: 2, ex: 'BI mendukung, bukan menggantikan, pengambil keputusan.' },
      { type: 'choice', q: '"Berapa stok optimal agar tidak kehabisan saat promo 12.12?" adalah analitik…', o: ['Deskriptif', 'Diagnostik', 'Prediktif', 'Preskriptif'], a: 3, ex: 'Merekomendasikan tindakan terbaik = preskriptif.' },
      { type: 'choice', q: 'Tahap yang menjaga satu definisi KPI untuk seluruh perusahaan:', o: ['Sumber data', 'Model semantik', 'Slicer', 'Warna'], a: 1, ex: 'Model semantik menyimpan measure dan relasi bersama.' },
      { type: 'choice', q: 'Perusahaan sangat bergantung pada Microsoft 365 dan Excel dengan anggaran terbatas. Tool yang paling mudah diadopsi:', o: ['Power BI', 'Tidak perlu tool', 'Hanya kertas', 'Bahasa assembly'], a: 0, ex: 'Integrasi ekosistem Microsoft memudahkan adopsi (pertimbangan, bukan aturan mutlak).' },
      { type: 'choice', q: 'Dashboard menunjukkan penjualan turun, namun tim tidak melakukan apa pun. Dari sudut pandang BI, nilai yang hilang ada di tahap…', o: ['ETL', 'Keputusan & aksi', 'Warehouse', 'Visual'], a: 1, ex: 'Insight tanpa tindakan tidak bernilai.' },
      { type: 'choice', q: 'Urutan siklus yang benar:', o: ['Dashboard → ETL → Sumber → Keputusan', 'Sumber → ETL → Warehouse → Model → Dashboard → Keputusan', 'ETL → Sumber → Dashboard', 'Keputusan → Sumber → Model'], a: 1, ex: 'Lihat peta siklus di tab Teori.' }
    ] },
  { title: 'Tantangan: rancang rencana BI untuk UMKM', lvl: 'T', mnt: 30, desc: 'Tanpa dataset khusus. Pilih satu UMKM (laundry, toko kue, bengkel, bimbel). Susun rencana singkat 1 halaman.',
    tasks: [
      { type: 'do', q: 'Tulis <b>3 keputusan bisnis</b> yang bisa dibantu BI beserta data yang dibutuhkan dan sumbernya.', rubric: ['3 keputusan spesifik', 'Data & sumber tiap keputusan', 'Dikelompokkan jenis analitik'] },
      { type: 'do', q: 'Gambar <b>alur siklus data</b> (sumber → ETL → warehouse → dashboard → keputusan) untuk UMKM tersebut.', rubric: ['Sumber realistis (kasir, WhatsApp, Excel)', 'Ada langkah pembersihan', 'Jelas siapa pengguna dashboard'] },
      { type: 'do', q: 'Sketsa <b>wireframe dashboard</b> pemilik: 4 KPI + 2 grafik. Jelaskan alasan pemilihan tiap visual.', rubric: ['4 KPI beralasan', '2 grafik tepat', 'Tata letak kiri-atas penting'] }
    ] }
];
BI.soal('#soal-box', T1);
