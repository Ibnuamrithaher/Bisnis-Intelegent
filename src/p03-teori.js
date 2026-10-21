/* ===== Pengayaan teori P3 (dibungkus IIFE agar tidak bentrok nama) ===== */
(function () {
  const { h, $, fmt, rp, short, pct } = BI, sum = BI.sum;
  const M = messy(); // 300 baris kotor (didefinisikan di bagian praktik)

  /* 1. berburu masalah */
  const D = BI.data.dirty(), HC = ['ID', 'Tanggal', 'Kota', 'Produk', 'Qty', 'Harga', 'Pelanggan'];
  const TRUTH = new Set(['1:Tanggal', '1:Kota', '1:Produk', '1:Pelanggan', '3:Qty', '3:Kota', '4:ID', '5:Tanggal', '5:Qty', '6:Kota', '6:Pelanggan', '8:Qty', '9:Harga']);
  const WHY = { '1:Tanggal': 'T002: format dd/mm/yyyy, berbeda dari baris lain', '1:Kota': 'T002: huruf kecil + spasi di akhir', '1:Produk': 'T002: huruf kecil semua', '1:Pelanggan': 'T002: huruf kecil', '3:Qty': 'T004: Qty kosong (null)', '3:Kota': 'T004: BANDUNG huruf besar semua', '4:ID': 'Baris duplikat T003 (identik dengan baris ke-3)', '5:Tanggal': 'T005: format "10 Jan 2024"', '5:Qty': 'T005: Qty negatif (melanggar aturan bisnis)', '6:Kota': 'T006: singkatan "Sby" bukan nama baku', '6:Pelanggan': 'T006: nama pelanggan kosong', '8:Qty': 'T008: Qty 400, kemungkinan salah ketik/outlier', '9:Harga': 'T009: "N/A" bukan angka' };
  let flagged = new Set(), shown = false;
  const hunt = $('#hunt');
  function hr() {
    hunt.innerHTML = '';
    hunt.append(h('thead', {}, h('tr', {}, HC.map(c => h('th', {}, c)))));
    hunt.append(h('tbody', {}, D.map((r, i) => h('tr', {}, HC.map(c => {
      const k = i + ':' + c, f = flagged.has(k), t = TRUTH.has(k);
      let cls = f ? 'warnc' : '';
      if (shown) cls = t && f ? 'good' : t ? 'bad' : f ? 'warnc' : '';
      return h('td', { class: cls, style: 'cursor:pointer;' + (f ? 'outline:2px solid var(--acc);outline-offset:-2px' : ''), title: shown && t ? WHY[k] : '', onclick() { if (shown) return; flagged.has(k) ? flagged.delete(k) : flagged.add(k); hr(); } }, r[c] === '' ? '∅' : String(r[c]));
    })))));
    const hit = [...flagged].filter(k => TRUTH.has(k)).length;
    $('#hunt-sc').textContent = flagged.size ? `Ditandai ${flagged.size} · tepat ${hit} dari ${TRUTH.size} · salah tandai ${flagged.size - hit}` : 'Belum ada sel ditandai';
  }
  $('#hunt-ans').onclick = () => {
    shown = true; hr();
    const miss = [...TRUTH].filter(k => !flagged.has(k));
    $('#hunt-txt').style.display = '';
    $('#hunt-txt').innerHTML = '<b class="t">Pembahasan</b><ul style="margin:4px 0;padding-left:18px">' + [...TRUTH].map(k => `<li>${flagged.has(k) ? '✅' : '❌'} ${WHY[k]}</li>`).join('') + `</ul>Hijau = ditemukan, merah = terlewat. Sel kuning hasil tandai Anda yang bukan masalah utama. Selain itu seluruh kolom <b>Harga</b> bertipe teks ("Rp 85.000"), sehingga tidak bisa dijumlahkan.`;
  };
  $('#hunt-reset').onclick = () => { flagged = new Set(); shown = false; $('#hunt-txt').style.display = 'none'; hr(); };
  hr();

  /* 2. taksonomi */
  const TX = [
    ['Format tidak konsisten', 'Tanggal "05/01/2024", "2024-01-05", "5 Jan 2024" dalam satu kolom.', 'Profiling distribusi pola; Column distribution menunjukkan banyak pola.', 'Seragamkan dengan Change Type Using Locale, Format.', 'Pengurutan dan filter tanggal salah.'],
    ['Nilai kosong (null)', 'Qty atau Pelanggan kosong.', 'Column quality: persen Empty.', 'Replace Values, Fill Down, isi median, atau hapus baris (sesuai konteks).', 'Rata-rata dan hitung jumlah menyimpang.'],
    ['Duplikat', 'Baris T003 muncul dua kali.', 'Column distribution: "Distinct" ≠ "Unique".', 'Remove Duplicates pada kolom kunci.', 'Total penjualan berlipat.'],
    ['Outlier / anomali', 'Qty 400 padahal biasanya 1–6.', 'Column profile (statistik, nilai min/maks), aturan IQR.', 'Verifikasi ke sumber; koreksi, tandai, atau kecualikan.', 'Rata-rata dan skala grafik terdistorsi.'],
    ['Tipe data salah', 'Harga bertipe Text: "Rp 85.000".', 'Ikon tipe data (ABC vs 123) pada header kolom.', 'Bersihkan simbol, lalu Change Type.', 'Tidak bisa dijumlahkan; urutan salah.'],
    ['Nilai tidak seragam', '"Sby", "SBY", "Surabaya".', 'Distribusi nilai unik terlalu banyak untuk kategori kecil.', 'Trim, Capitalize, tabel pemetaan (Merge) atau Replace Values.', 'Satu kota terpecah menjadi beberapa batang.'],
    ['Pelanggaran aturan bisnis', 'Qty negatif, tanggal di masa depan, diskon > 100%.', 'Filter kondisi aturan; Column profile.', 'Filter/Replace Errors, tandai untuk investigasi.', 'Angka tidak masuk akal.'],
    ['Integritas referensial', 'PelangganID di penjualan tidak ada di master pelanggan.', 'Merge dengan Left Anti Join terhadap master.', 'Lengkapi master atau tandai "Tidak diketahui".', 'Baris hilang saat dihubungkan di model.']
  ];
  TX.forEach((t, i) => $('#tx-sel').append(h('span', { class: 'node', onclick(e) { BI.$$('#tx-sel .node').forEach(n => n.classList.remove('on')); e.currentTarget.classList.add('on'); tx(i); } }, t[0])));
  function tx(i) {
    const t = TX[i]; $('#tx-info').innerHTML = '';
    [['Contoh', t[1]], ['Cara mendeteksi', t[2]], ['Cara memperbaiki', t[3]]].forEach(([a, b]) => $('#tx-info').append(h('div', { class: 'card' }, h('h4', {}, a), b)));
    $('#tx-info').append(h('div', { class: 'callout warn', style: 'grid-column:1/-1' }, h('b', { class: 't' }, 'Risiko bila dibiarkan'), t[4]));
  }
  $('#tx-sel .node').click();

  /* 4. profiling */
  const pfSel = { col: 'Kota', clean: false };
  const prop = s => String(s).toLowerCase().replace(/(^|\s)\S/g, c => c.toUpperCase());
  BI.select('#pf-ctl', 'Kolom', ['Kota', 'Produk', 'Qty', 'Harga', 'Tanggal'], 'Kota', v => { pfSel.col = v; pf(); });
  BI.seg('#pf-seg', [[false, 'Sebelum dibersihkan'], [true, 'Sesudah dibersihkan']], false, v => { pfSel.clean = v; pf(); });
  function pf() {
    const c = pfSel.col, cl = pfSel.clean; let labels = [], data = [], txt = '', kp = [];
    if (c === 'Kota' || c === 'Produk') {
      const g = BI.groupBy(M, r => '"' + (cl ? prop(String(r[c]).trim()) : r[c]) + '"').sort((a, b) => b.value - a.value);
      const sorted = g.sort((a, b) => b.value - a.value).slice(0, 14);
      labels = sorted.map(x => x.key); data = sorted.map(x => x.n);
      kp = [{ label: 'Nilai unik (distinct)', value: g.length }, { label: 'Baris', value: M.length }];
      txt = cl ? `Nilai unik turun menjadi <b>${g.length}</b>: setiap ${c.toLowerCase()} kini tepat satu penulisan.` : `Ada <b>${g.length}</b> penulisan berbeda untuk sedikit ${c.toLowerCase()} asli. Spasi dan huruf besar/kecil memecah satu entitas menjadi beberapa.`;
    } else if (c === 'Qty') {
      const f = r => (r.Qty === '' ? 'Kosong' : r.Qty < 0 ? 'Negatif' : r.Qty > 100 ? 'Ekstrem (>100)' : 'Valid 1–100');
      const L = ['Valid 1–100', 'Kosong', 'Negatif', 'Ekstrem (>100)'], g = BI.groupBy(M, r => (cl ? 'Valid 1–100' : f(r)));
      labels = L; data = L.map(l => (g.find(x => x.key === l) || { n: 0 }).n);
      kp = [{ label: 'Valid', value: pct(data[0] / M.length) }, { label: 'Bermasalah', value: M.length - data[0] }];
      txt = cl ? 'Setelah anomali dikoreksi dan kosong diisi, semua baris valid.' : 'Column quality memisahkan valid, kosong, dan error. Negatif dan ekstrem baru terlihat dari profil nilai (min/maks), bukan dari ikon tipe data.';
    } else if (c === 'Harga') {
      const L = ['Angka (123)', 'Teks "Rp …" (ABC)'], g = BI.groupBy(M, r => (cl || typeof r.Harga === 'number' ? L[0] : L[1]));
      labels = L; data = L.map(l => (g.find(x => x.key === l) || { n: 0 }).n);
      kp = [{ label: 'Bertipe angka', value: pct(data[0] / M.length) }];
      txt = cl ? 'Semua harga angka: aman untuk dijumlahkan dan dikalikan Qty.' : 'Satu kolom berisi dua tipe. Power Query memberi ikon ABC/123 campuran; Sum hanya membaca baris bertipe angka.';
    } else {
      const L = ['ISO yyyy-mm-dd', 'dd/mm/yyyy'], g = BI.groupBy(M, r => (cl || /^\d{4}-/.test(r.Tanggal) ? L[0] : L[1]));
      labels = L; data = L.map(l => (g.find(x => x.key === l) || { n: 0 }).n);
      kp = [{ label: 'Pola format', value: cl ? 1 : 2 }];
      txt = cl ? 'Satu pola format: tanggal dapat diurutkan, difilter, dan dibuat hierarki.' : 'Dua pola format bercampur. Tanpa penyeragaman, "05/01" bisa terbaca 5 Januari atau 1 Mei.';
    }
    BI.hbar('#pf-chart', { labels, data, rowH: 26, fmt: v => v, valFmt: v => v + ' baris', title: `Column distribution: ${c}`, colorBy: (i) => (cl || i === 0 ? 'var(--c3)' : 'var(--c4)') });
    BI.kpi('#pf-kpi', kp); $('#pf-txt').innerHTML = txt;
  }
  pf();

  /* 5. tipe data */
  const nums = ['120', '95', '1250', '40'];
  BI.seg('#ty-a-seg', [['t', 'Tipe Text'], ['n', 'Tipe Number']], 't', v => {
    $('#ty-a').innerHTML = `<div class="small">Nilai: ${nums.join(' · ')}</div><div class="kpi" style="margin-top:8px"><div class="l">SUM</div><div class="v">${v === 't' ? 'Error' : fmt(sum(nums.map(Number)))}</div><div class="d ${v === 't' ? 'down' : 'up'}">${v === 't' ? 'teks tidak dapat dijumlahkan' : 'agregasi berjalan'}</div></div>`;
  });
  const sn = ['10', '100', '2', '25', '3'];
  BI.seg('#ty-b-seg', [['t', 'Sebagai Text'], ['n', 'Sebagai Number']], 't', v => {
    const s = [...sn].sort(v === 't' ? (a, b) => (a > b ? 1 : a < b ? -1 : 0) : (a, b) => a - b);
    $('#ty-b').innerHTML = `<div class="small">Urutan naik:</div><div class="flow" style="justify-content:flex-start">${s.map(x => `<span class="node">${x}</span>`).join('')}</div><div class="small muted">${v === 't' ? '"100" muncul sebelum "2" karena dibandingkan huruf per huruf.' : 'Urutan numerik sesuai harapan.'}</div>`;
  });
  const MON = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  const tc = { v: '05/01/2024', l: 'id' };
  const tin = h('input', { type: 'text', value: tc.v, style: 'width:120px', oninput(e) { tc.v = e.target.value; tcd(); } });
  $('#ty-c-ctl').append(h('label', {}, 'Teks tanggal', tin));
  BI.select('#ty-c-ctl', 'Locale', [['id', 'Indonesia (dd/mm/yyyy)'], ['us', 'English US (mm/dd/yyyy)']], 'id', v => { tc.l = v; tcd(); });
  function tcd() {
    const m = tc.v.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/); let out;
    if (!m) out = '<span class="chip bad">Format tidak dikenali</span>';
    else { const a = +m[1], b = +m[2], y = +m[3], d = tc.l === 'id' ? a : b, mo = tc.l === 'id' ? b : a; out = mo > 12 || mo < 1 || d > 31 ? `<span class="chip bad">Error: bulan ${mo} tidak ada</span>` : `<div class="kpi"><div class="l">Terbaca sebagai</div><div class="v" style="font-size:1.2rem">${d} ${MON[mo - 1]} ${y}</div></div>`; }
    $('#ty-c').innerHTML = out + '<div class="small muted" style="margin-top:6px">Coba "13/01/2024" pada locale US. Gunakan <b>Change Type → Using Locale</b>.</div>';
  }
  tcd();

  /* 7. struktur */
  const P = [['Budi Santoso', 'Jl. Merdeka 10, Bandung', 3, 85000], ['Sari Dewi Lestari', 'Jl. Asia Afrika 5, Bandung', 1, 245000], ['Andi Wijaya', 'Jl. Basuki Rahmat 22, Surabaya', 2, 520000], ['Rina Marlina', 'Jl. Gatot Subroto 8, Medan', 5, 310000], ['Putu Ayu Kartika', 'Jl. Sunset Road 3, Denpasar', 2, 150000], ['Dewi Lestari', 'Jl. Sudirman 1, Jakarta', 4, 95000]];
  const st = { split: 'first', sep: ' - ', thr: 500000 };
  BI.select('#st-ctl', 'Pecah Nama (Split Column)', [['first', 'Pada spasi pertama (left-most)'], ['last', 'Pada spasi terakhir (right-most)']], 'first', v => { st.split = v; stp(); });
  BI.select('#st-ctl', 'Pemisah gabungan (Merge)', [[' - ', '" - "'], [', ', '", "'], ['|', '"|"']], ' - ', v => { st.sep = v; stp(); });
  BI.slider('#st-ctl', 'Ambang kolom bersyarat (Total ≥)', 0, 2000000, 50000, st.thr, v => { st.thr = v; stp(); }, rp);
  function stp() {
    const rows = P.map(([n, a, q, hg]) => {
      const i = st.split === 'first' ? n.indexOf(' ') : n.lastIndexOf(' '), dep = n.slice(0, i), bel = n.slice(i + 1), [jl, kt] = a.split(', '), tot = q * hg;
      return { Depan: dep, Belakang: bel, Jalan: jl, Kota: kt, Gabungan: kt + st.sep + n, Total: tot, Ukuran: tot >= st.thr ? 'Besar' : 'Kecil' };
    });
    BI.table('#st-tbl', { cols: [{ k: 'Depan', l: 'Nama Depan' }, { k: 'Belakang', l: 'Nama Belakang' }, { k: 'Jalan', l: 'Jalan' }, { k: 'Kota', l: 'Kota' }, { k: 'Gabungan', l: 'Kota & Nama (merge)' }, { k: 'Total', l: 'Total', r: 1, f: fmt }, { k: 'Ukuran', l: 'Ukuran Order', cls: v => (v === 'Besar' ? 'good' : '') }], rows, sort: false });
    $('#st-code').textContent = `// Pecah nama: ${st.split === 'first' ? 'left-most' : 'right-most'} delimiter spasi\nTable.SplitColumn(Sumber, "Nama", Splitter.SplitTextByEachDelimiter({" "}, QuoteStyle.None, ${st.split === 'first' ? 'false' : 'true'}), {"Depan","Belakang"})\n// Gabung kolom\nTable.CombineColumns(Hasil, {"Kota","Nama"}, Combiner.CombineTextByDelimiter("${st.sep}"), "Gabungan")\n// Kolom bersyarat\nTable.AddColumn(Hasil, "Ukuran", each if [Total] >= ${st.thr} then "Besar" else "Kecil")`;
  }
  stp();
  const WIDE = [{ Produk: 'Kaos Polos', Jan: 120, Feb: 135, Mar: 150 }, { Produk: 'Jaket Hoodie', Jan: 80, Feb: 95, Mar: 70 }, { Produk: 'Tas Ransel', Jan: 60, Feb: 65, Mar: 110 }];
  BI.seg('#up-seg', [['w', 'Tabel lebar (bulan = kolom)'], ['l', 'Tabel panjang (setelah Unpivot)']], 'w', v => {
    if (v === 'w') {
      BI.table('#up-tbl', { cols: ['Produk', 'Jan', 'Feb', 'Mar'].map(k => ({ k, l: k, r: k !== 'Produk' })), rows: WIDE, sort: false });
      $('#up-chart').innerHTML = '<p class="muted small">Grafik tren per bulan tidak dapat dibuat dengan mudah: bulan tersebar di tiga kolom berbeda.</p>';
      $('#up-txt').innerHTML = '<b class="t">Tabel lebar</b>Bagus untuk dibaca manusia di Excel, buruk untuk analisis. Menambah bulan baru berarti menambah kolom baru.';
    } else {
      const L = []; WIDE.forEach(r => ['Jan', 'Feb', 'Mar'].forEach(b => L.push({ Produk: r.Produk, Bulan: b, Nilai: r[b] })));
      BI.table('#up-tbl', { cols: [{ k: 'Produk', l: 'Produk' }, { k: 'Bulan', l: 'Atribut → Bulan' }, { k: 'Nilai', l: 'Nilai', r: 1 }], rows: L, sort: false });
      BI.line('#up-chart', { labels: ['Jan', 'Feb', 'Mar'], series: WIDE.map(r => ({ name: r.Produk, data: [r.Jan, r.Feb, r.Mar] })), height: 190 });
      $('#up-txt').innerHTML = '<b class="t">Tabel panjang</b>Pilih kolom bulan → <b>Transform → Unpivot Columns</b>. Satu kolom Bulan + satu kolom Nilai: siap untuk grafik, slicer, dan measure.';
    }
  });

  /* 8. duplikat */
  const DUP = [{ ID: 'T100', Jam: '10:00', Qty: 2 }, { ID: 'T100', Jam: '10:00', Qty: 2 }, { ID: 'T100', Jam: '10:05', Qty: 3 }, { ID: 'T101', Jam: '11:00', Qty: 1 }, { ID: 'T101', Jam: '11:00', Qty: 1 }, { ID: 'T102', Jam: '12:00', Qty: 4 }];
  BI.seg('#dp-seg', [['none', 'Biarkan'], ['exact', 'Hapus duplikat persis (semua kolom)'], ['first', 'Pertahankan pertama per ID'], ['last', 'Pertahankan terbaru per ID']], 'none', v => {
    let r = DUP, note;
    if (v === 'exact') { const s = new Set(); r = DUP.filter(x => { const k = JSON.stringify(x); if (s.has(k)) return false; s.add(k); return true; }); note = 'T100 masih muncul dua kali: baris revisi bukan duplikat persis, sehingga ikut terhitung. Total 10 (salah).'; }
    else if (v === 'first') { r = DUP.filter((x, i) => DUP.findIndex(y => y.ID === x.ID) === i); note = 'Revisi (Qty 3) terbuang; yang tersisa data lama. Total 7 (salah).'; }
    else if (v === 'last') { r = DUP.filter((x, i) => DUP.map(y => y.ID).lastIndexOf(x.ID) === i); note = 'Kunci ID dengan urutan jam terbaru: revisi dipertahankan. Total 8 (benar). Syaratnya data diurutkan menurut waktu sebelum dedup.'; }
    else note = 'Seluruh enam baris dihitung: total 13 (salah, berlipat).';
    const tot = sum(r.map(x => x.Qty));
    BI.table('#dp-tbl', { cols: [{ k: 'ID', l: 'ID' }, { k: 'Jam', l: 'Jam' }, { k: 'Qty', l: 'Qty', r: 1 }], rows: r, sort: false });
    BI.kpi('#dp-kpi', [{ label: 'Baris', value: r.length }, { label: 'Total Qty', value: tot, sub: 'seharusnya 8', delta: tot === 8 ? 0.0001 : -0.0001, note: tot === 8 ? 'tepat' : 'meleset' }]);
    $('#dp-txt').innerHTML = `<b class="t">${tot === 8 ? '✅' : '⚠'} Hasil</b>${note}`;
  });

  /* 9. IQR */
  let kIQR = 1.5;
  BI.slider('#iq-ctl', 'Pengali k', 0.5, 3, 0.5, kIQR, v => { kIQR = v; iqr(); }, v => v.toFixed(1));
  function iqr() {
    const a = vals.filter(v => v != null).sort((x, y) => x - y), q = p => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return a[lo] + (a[hi] - a[lo]) * (i - lo); };
    const q1 = q(0.25), q3 = q(0.75), iq = q3 - q1, lo = q1 - kIQR * iq, hi = q3 + kIQR * iq, out = a.filter(v => v < lo || v > hi);
    $('#iq-out').innerHTML = `Q1 = <b>${fmt(q1)}</b>, Q3 = <b>${fmt(q3)}</b>, IQR = <b>${fmt(iq)}</b> → batas wajar <b>${fmt(lo)} s.d. ${fmt(hi)}</b>.<br>Ditandai: ${out.length ? out.map(v => `<span class="chip bad">${fmt(v)}</span>`).join(' ') : 'tidak ada'}.<br><span class="small muted">Catatan: 500 ditandai statistik padahal benar. Outlier statistik bukan berarti salah; <b>verifikasi dengan sumber</b> sebelum mengubahnya.</span>`;
  }
  iqr();

  /* 10. rekonsiliasi */
  const hn = v => { if (typeof v === 'number') return v; const t = String(v).replace(/[^\d]/g, ''); return t ? +t : NaN; };
  const num = v => (typeof v === 'number' ? v : NaN);
  const nm = M.map(r => r.Qty).filter(v => typeof v === 'number' && v >= 1 && v <= 100).sort((a, b) => a - b), med = nm[Math.floor(nm.length / 2)];
  const total = (rows, hf, qf) => sum(rows.map(r => { const q = qf(r), p = hf(r.Harga); return isFinite(q) && isFinite(p) ? q * p : 0; }));
  const dedup = rows => rows.filter((r, i) => rows.findIndex(x => x.OrderID === r.OrderID) === i);
  const S0 = total(M, num, r => num(r.Qty));
  const S1 = total(M, hn, r => num(r.Qty));
  const D1 = dedup(M), S2 = total(D1, hn, r => num(r.Qty));
  const S3 = total(D1, hn, r => { const q = num(r.Qty); return q >= 1 && q <= 100 ? q : NaN; });
  const S4 = total(D1, hn, r => { const q = num(r.Qty); return r.Qty === '' ? med : q >= 1 && q <= 100 ? q : NaN; });
  const RC = [
    ['Analis A: apa adanya', S0, 'Harga bertipe teks ("Rp …") dikecualikan karena bukan angka; Qty kosong, negatif, dan ekstrem ikut terhitung; duplikat ikut terhitung.'],
    ['+ ubah Harga ke angka', S1, 'Ratusan baris yang hilang karena Harga teks kini masuk. Angka melonjak.'],
    ['+ hapus duplikat (OrderID)', S2, 'Baris ganda dibuang; total turun.'],
    ['+ buang Qty negatif & ekstrem', S3, 'Qty negatif mengurangi total dan Qty ×100 menggelembungkan; keduanya disingkirkan.'],
    ['Analis B: + isi Qty kosong (median ' + med + ')', S4, 'Baris tanpa Qty diisi median agar tidak hilang dari total. Ini angka akhir yang paling dapat dipertanggungjawabkan, dengan asumsi didokumentasikan.']
  ];
  BI.seg('#rc-seg', RC.map((r, i) => [i, i + 1 + '. ' + r[0].split(':')[0].replace('+ ', '+ ')]), 0, i => {
    BI.bar('#rc-chart', { labels: RC.map((_, k) => 'L' + (k + 1)), series: [{ name: 'Total (Rp)', data: RC.map((r, k) => (k <= i ? r[1] : 0)) }], height: 240, highlight: i, title: 'Total penjualan pada tiap langkah', fmt: short, tipFmt: rp });
    BI.kpi('#rc-kpi', [{ label: 'Total saat ini', value: 'Rp ' + short(RC[i][1]) }, { label: 'Selisih vs langkah sebelumnya', value: i ? (RC[i][1] >= RC[i - 1][1] ? '+' : '−') + 'Rp ' + short(Math.abs(RC[i][1] - RC[i - 1][1])) : '—' }, { label: 'Selisih vs angka akhir', value: pct((RC[i][1] - S4) / S4, 0) }]);
    $('#rc-txt').innerHTML = `<b class="t">${RC[i][0]}</b>${RC[i][2]}`;
  });

  /* 11. peta teknik */
  BI.table('#sum-tbl', { sort: false, cols: [{ k: 'a', l: 'Masalah' }, { k: 'b', l: 'Teknik di Power Query' }, { k: 'c', l: 'Fungsi M' }], rows: [
    { a: 'Spasi/huruf tidak seragam', b: 'Format → Trim / Capitalize Each Word', c: 'Text.Trim, Text.Proper' },
    { a: 'Nilai bervariasi', b: 'Replace Values / tabel pemetaan', c: 'Table.ReplaceValue' },
    { a: 'Harga bertipe teks', b: 'Replace + Change Type', c: 'Text.Remove, Number.From' },
    { a: 'Tanggal beragam format', b: 'Change Type Using Locale', c: 'Date.FromText(…, "id-ID")' },
    { a: 'Duplikat', b: 'Remove Duplicates (kolom kunci)', c: 'Table.Distinct' },
    { a: 'Null', b: 'Replace Values / Fill Down', c: 'Table.FillDown' },
    { a: 'Kolom menyatu / terpisah', b: 'Split Column / Merge Columns', c: 'Table.SplitColumn, Table.CombineColumns' },
    { a: 'Bulan sebagai kolom', b: 'Unpivot Columns', c: 'Table.UnpivotOtherColumns' },
    { a: 'Kategori turunan', b: 'Conditional Column', c: 'Table.AddColumn + if … then' }] });
})();
