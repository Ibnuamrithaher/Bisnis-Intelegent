// node merge-soal.js 01  -> sisipkan src/soal-pNN.js ke src/content/pNN.html (sekali saja)
const fs=require('fs'),n=process.argv[2],p=`src/content/p${n}.html`;let s=fs.readFileSync(p,'utf8');
if(s.includes('id="soal"')){console.log('sudah ada');process.exit()}
const code=fs.readFileSync(`src/soal-p${n}.js`,'utf8');
const pane=`<section class="pane" id="soal"><h2>Bank Soal Tes &amp; Latihan</h2><div class="callout"><b class="t">Cara pakai</b>Setiap set memakai <b>dataset berbeda</b> dan perintah berbeda. Unduh dataset, kerjakan di tool BI, lalu masukkan jawaban untuk dicek otomatis. Soal bertanda <i>Kerjakan</i> dinilai dengan rubrik.</div><div id="soal-box"></div></section>\n\n`;
s=s.replace('<section class="pane" id="kuis">',pane+'<section class="pane" id="kuis">');
const i=s.lastIndexOf('</script>');s=s.slice(0,i)+'\n'+code+'\n'+s.slice(i);
fs.writeFileSync(p,s);console.log('ok');
