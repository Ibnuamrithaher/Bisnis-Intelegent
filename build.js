// Jalankan: node build.js  -> hasil di folder dist/ (tiap file HTML mandiri, tanpa dependensi)
const fs = require('fs'), path = require('path');
const R = f => fs.readFileSync(path.join(__dirname, f), 'utf8');
const css = R('src/base.css'), lib = R('src/lib.js'), meta = require('./src/meta.js');
const pcss = R('src/premium.css'), pjs = R('src/premium.js'), PREMIUM = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]); // halaman bertema high-end-visual-design
const FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">';
const CPMK = {
  1: ['Kognitif · Pemahaman', 'Menjelaskan konsep dasar Business Intelligence (BI), arsitektur data, serta peran penting Data Warehouse dalam mendukung ekosistem bisnis digital.'],
  2: ['Psikomotorik · Pengolahan Data', 'Mengelola proses ETL (Extract, Transform, Load) untuk mengintegrasikan dan membersihkan data terstruktur dari berbagai sumber ke dalam repositori data.'],
  3: ['Psikomotorik · Analisis & Visualisasi', 'Membangun laporan interaktif, analitik data, dan dashboard bisnis yang komunikatif menggunakan perangkat lunak BI terkini.'],
  4: ['Afektif/Kognitif · Pengambilan Keputusan', 'Merumuskan rekomendasi bisnis dan informasi strategis yang siap pakai berdasarkan hasil interpretasi visualisasi data bisnis.'],
  5: ['Keterampilan Khusus · Berbasis Proyek', 'Menghasilkan proyek solusi BI akhir secara mandiri atau berkelompok yang merepresentasikan kompetensi nyata sebagai seorang BI Analyst atau Data Specialist.']
};
const REFS = [
  ['sherman', 'Rick Sherman. <i>Business Intelligence Guidebook: From Data Integration to Analytics</i> (1st Edition). Morgan Kaufmann, 2014.'],
  ['wexler', 'Steve Wexler, Jeffrey Shaffer, Andy Cotgreave. <i>The Big Book of Dashboards: Visualizing Your Data Using Real-World Business Scenarios</i> (1st Edition). Wiley, 2017.']
];
const cpmkHtml = m => m.cpmk.map(c => { const n = +((c.match(/CPMK-([0-9])/) || [])[1]); return n ? '<li><b>CPMK-' + n + '</b> (' + CPMK[n][0] + '): ' + CPMK[n][1] + '</li>' : ''; }).join('');
const refUse = (m, k) => { const r = m.ref; if (!r.toLowerCase().includes(k)) return ''; if (r.includes('&') || r.includes('(')) return 'seluruh bab terkait'; return r.replace(/^(Sherman|Wexler),?\s*/i, ''); };
const refHtml = m => REFS.map(([k, t]) => { const u = refUse(m, k); return '<li' + (u ? '' : ' class="muted"') + '>' + t + (u ? ' <span class="chip">dipakai: ' + esc(u) + '</span>' : '') + '</li>'; }).join('');
const out = path.join(__dirname, 'dist'); fs.mkdirSync(out, { recursive: true });
const pad = n => String(n).padStart(2, '0'), file = n => `pertemuan-${pad(n)}.html`;
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const COURSE = 'Bisnis Intelegent · Bisnis Digital';

meta.forEach(m => {
  const fp = path.join(__dirname, 'src/content', `p${pad(m.n)}.html`);
  const frag = fs.existsSync(fp) ? fs.readFileSync(fp, 'utf8') : `<section class="pane" id="teori"><p>Konten belum dibuat.</p></section><section class="pane" id="praktik"></section><section class="pane" id="kuis"></section>`;
  const prev = m.n > 1 ? `<a href="${file(m.n - 1)}">← Pertemuan ${m.n - 1}</a>` : '<a href="index.html">← Daftar</a>';
  const next = m.n < 14 ? `<a href="${file(m.n + 1)}">Pertemuan ${m.n + 1} →</a>` : '<a href="index.html">Daftar →</a>';
  const P = PREMIUM.has(m.n), ic = e => (P ? '' : e + ' ');
  const html = `<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pertemuan ${m.n} – ${esc(m.title)} | ${COURSE}</title>
<style>${css}</style>${P ? FONT + '<style>' + pcss + '</style>' : ''}</head><body${P ? ' class="hv"' : ''}>
<header class="hero"><div class="wrap">
 <div class="topnav">${prev}<a href="index.html">☰ Semua pertemuan</a>${next}</div>
 <div class="meta"><span class="pill">Pertemuan ${m.n} / 14</span><span class="pill">Minggu ke-${m.week} RPS</span><span class="pill">45' teori + 100' praktik</span></div>
 <h1>${esc(m.title)}</h1><p>${esc(m.sub)}</p>
</div></header>
<nav class="tabs"><div class="wrap">
 <button data-pane="ringkasan">${ic('🧭')}Ringkasan</button><button data-pane="teori">${ic('📘')}Teori · 45'</button><button data-pane="praktik">${ic('💻')}Praktik · 100'</button><button data-pane="kuis">${ic('❓')}Kuis</button>${frag.includes('id="soal"') ? '<button data-pane="soal">' + ic('🧪') + 'Bank Soal</button>' : ''}<button data-pane="tugas">${ic('📝')}Rangkuman & Tugas</button>
</div></nav>
<main><div class="wrap">
<section class="pane" id="ringkasan">
${P ? `<div class="bento">
 <div class="card b-hero"><span class="eyebrow">Kemampuan akhir</span><p class="lead">${esc(m.goal)}</p><p class="small muted">${m.cpmk.map(esc).join(' · ')} · Referensi: ${esc(m.ref)}</p></div>
 <div class="card b-top"><span class="eyebrow">Pokok bahasan</span><ol>${m.topics.map(t => `<li>${esc(t)}</li>`).join('')}</ol></div>
 <div class="card b-how"><span class="eyebrow">Cara memakai</span><ul class="small"><li>Ikuti agenda dengan tombol <b>timer</b>.</li><li>Di tab Teori, <b>klik, geser, dan ubah</b> setiap visualisasi.</li><li>Progres praktik tersimpan di browser.</li></ul>
  <div class="row"><button class="btn pri" data-goto="teori">Mulai teori</button><button class="btn" data-goto="praktik">Langsung praktik</button></div></div>
 <div class="card b-ag1"><span class="eyebrow">Capaian pembelajaran (CPMK)</span><ul class="small">${cpmkHtml(m)}</ul></div>
 <div class="card b-ag2"><span class="eyebrow">Sumber referensi</span><ol class="small">${refHtml(m)}</ol></div>
</div>` : ` <div class="card"><h3>🎯 Kemampuan akhir</h3><p>${esc(m.goal)}</p>
  <p class="small muted">${m.cpmk.map(esc).join(' · ')} · Referensi: ${esc(m.ref)}</p></div>
 <div class="grid2">
  <div class="card"><h3>Pokok bahasan</h3><ol>${m.topics.map(t => `<li>${esc(t)}</li>`).join('')}</ol></div>
  <div class="card"><h3>Cara memakai bahan ajar</h3><ul><li>Ikuti agenda dengan tombol <b>timer</b>.</li><li>Di tab Teori, <b>klik, geser, dan ubah</b> setiap visualisasi.</li><li>Di tab Praktik, centang langkah; progres tersimpan di browser.</li><li>Tab Kuis untuk cek pemahaman.</li></ul>
  <div class="row"><button class="btn pri" data-goto="teori">Mulai teori →</button><button class="btn" data-goto="praktik">Langsung praktik</button></div></div>
 </div>
 <div class="grid2"><div class="card"><h3>🎓 Capaian pembelajaran (CPMK)</h3><ul class="small">${cpmkHtml(m)}</ul></div><div class="card"><h3>📚 Sumber referensi</h3><ol class="small">${refHtml(m)}</ol></div></div>
`}
</section>
${frag}
<section class="pane" id="tugas">
 <div class="card"><h3>📌 Rangkuman</h3><ul>${m.summary.map(s => `<li>${esc(s)}</li>`).join('')}</ul></div>
 <div class="card"><h3>📝 Tugas: ${esc(m.tugas.judul)}</h3><p>${esc(m.tugas.desc)}</p><h4>Kriteria penilaian</h4><ul>${m.tugas.kriteria.map(s => `<li>${esc(s)}</li>`).join('')}</ul>
  <p class="small muted">Bobot nilai mata kuliah: 40% tugas, 30% UTS, 30% UAS.</p></div>
 <div class="card"><h3>✍ Catatan & refleksi pribadi</h3><p class="small muted">Tersimpan otomatis di browser Anda. Apa satu hal paling berguna hari ini? Apa yang masih membingungkan?</p><textarea id="notes" rows="5" placeholder="Tulis di sini…"></textarea>
  <div class="row"><button class="btn" onclick="window.print()">🖨 Cetak / simpan PDF halaman ini</button></div></div>
</section>
</div></main>
<footer>${COURSE} · Dosen: Ibnu Amri Thaher · Pertemuan ${m.n}</footer>
<script>${lib}</script>
<script>
(function(){var n=document.getElementById('notes'),k='bi-notes-p${m.n}';try{n.value=localStorage.getItem(k)||'';n.oninput=function(){localStorage.setItem(k,n.value)}}catch(e){}})();
</script>
<script>
${(frag.match(/<script>[\s\S]*?<\/script>/g) || []).join('\n').replace(/<\/?script>/g, '')}
</script>
${P ? '<script>' + pjs + '</script>' : ''}
<script>BI.init();</script>
</body></html>`;
  // fragmen: hapus <script> dari markup (sudah dipindahkan ke bawah, setelah DOM siap)
  const clean = html.replace(frag, () => frag.replace(/<script>[\s\S]*?<\/script>/g, ''));
  fs.writeFileSync(path.join(out, file(m.n)), clean);
});

// index
const idx = `<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bahan Ajar ${COURSE}</title>${FONT}<style>${css}${pcss}
.pcard{display:block;text-decoration:none;color:inherit;transition:.15s}.pcard:hover{transform:translateY(-3px);border-color:var(--acc)}.pcard .no{font-size:2rem;font-weight:800;color:var(--acc);line-height:1}
</style></head><body class="hv">
<header class="hero"><div class="wrap"><div class="meta"><span class="pill">Program Studi Bisnis Digital</span><span class="pill">T:1 · P:2 SKS</span></div>
<h1>Bahan Ajar Interaktif: Bisnis Intelegent</h1><p>14 pertemuan tatap muka, masing-masing 45 menit teori + 100 menit praktik, dilengkapi visualisasi interaktif. Dosen pengampu: Ibnu Amri Thaher.</p></div></header>
<main><div class="wrap">
<div class="callout"><b class="t">Cara pakai</b>Buka file HTML langsung di browser (tanpa internet). Pemetaan ke RPS: pertemuan 1–7 = minggu 1–7, <b>UTS minggu 8</b>, pertemuan 8–14 = minggu 9–15, <b>UAS minggu 16</b>.</div>
<div class="grid3">${meta.map(m => `<a class="card pcard" href="${file(m.n)}"><div class="no">${pad(m.n)}</div><h3 style="margin-top:6px">${esc(m.title)}</h3><p class="small muted">${esc(m.sub)}</p><span class="chip">Minggu ${m.week}</span></a>`).join('')}</div>
<div class="grid2 mt"><div class="card"><h3>UTS · Minggu 8</h3><p>Ujian praktik mandiri di lab: membangun relasi data dan visualisasi dasar dari studi kasus baru. Persiapan: pertemuan 1–7. Penilaian: hasil dashboard, ketepatan relasi, kebenaran kalkulasi. Bobot 30%.</p></div>
<div class="card"><h3>UAS · Minggu 16</h3><p>Presentasi proyek akhir berkelompok berbasis data industri nyata. Penilaian: kebenaran teknis & insight, kualitas visual, komunikasi. Bobot 30%.</p></div></div>
<div class="card"><h3>Referensi</h3><ol><li>Rick Sherman. <i>Business Intelligence Guidebook: From Data Integration to Analytics</i>. Morgan Kaufmann, 2014.</li><li>Steve Wexler, Jeffrey Shaffer, Andy Cotgreave. <i>The Big Book of Dashboards</i>. Wiley, 2017.</li></ol></div>
</div></main><footer>${COURSE}</footer><script>${lib}</script><script>${pjs}</script><script>(function(){try{var t=localStorage.getItem('bi-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}})()</script></body></html>`;
fs.writeFileSync(path.join(out, 'index.html'), idx);
console.log('OK ->', out);
