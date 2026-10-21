// buka semua <details> di tab soal lalu dump jumlah pembahasan kosong
const fs=require('fs'),cp=require('child_process'),path=require('path');
const f=process.argv[2],tmp=path.join(process.env.TEMP,'bi-open.html');
let h=fs.readFileSync(path.join(__dirname,'..','dist',f),'utf8').replace('<head>','<head><script>addEventListener("load",function(){setTimeout(function(){var d=[].slice.call(document.querySelectorAll("#soal details")).filter(function(x){return x.textContent.indexOf("pembahasan")>-1});var e=d.filter(function(x){return x.querySelector("div").textContent.trim()===""}).length;document.title="R:"+d.length+" kosong:"+e},300)})</script>');
fs.writeFileSync(tmp,h);
const o=cp.execFileSync('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--disable-gpu','--virtual-time-budget=3000','--dump-dom','file:///'+tmp.split(path.sep).join('/')],{encoding:'utf8',maxBuffer:1e8});
console.log((o.match(/<title>(R:[^<]*)/)||[])[1]);
