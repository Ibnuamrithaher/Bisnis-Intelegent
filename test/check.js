// node test/check.js [nomor...]  -> uji tiap halaman di Edge headless, laporkan error JS
const fs=require('fs'),path=require('path'),cp=require('child_process');
const dist=path.join(__dirname,'..','dist'),tmp=path.join(process.env.TEMP||'/tmp','bi-test');fs.mkdirSync(tmp,{recursive:true});
const edge='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const inj=`<script>window.__e=[];onerror=function(m,s,l,c){__e.push(m+' @'+l+':'+c)};
addEventListener('load',function(){setTimeout(function(){
document.querySelectorAll('button,.node,.zone,.opt,summary').forEach(function(b){if(b.classList.contains('themebtn'))return;try{b.click()}catch(e){__e.push('click:'+e.message)}});
document.querySelectorAll('svg rect,svg circle,svg path').forEach(function(n,i){if(i%7)return;try{n.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX:50,clientY:50}));n.dispatchEvent(new MouseEvent('click',{bubbles:true}))}catch(e){__e.push('ev:'+e.message)}});
setTimeout(function(){document.title='RESULT:'+JSON.stringify(__e)},300)},200)})</script>`;
const arg=process.argv.slice(2);let files=fs.readdirSync(dist).filter(f=>f.endsWith('.html'));
if(arg.length)files=files.filter(f=>arg.some(a=>f.includes(a.padStart(2,'0'))||f===a));
let bad=0;
for(const f of files){
  const html=fs.readFileSync(path.join(dist,f),'utf8').replace('<head>','<head>'+inj);
  const p=path.join(tmp,f);fs.writeFileSync(p,html);
  let out='';
  try{out=cp.execFileSync(edge,['--headless=new','--disable-gpu','--virtual-time-budget=4000','--dump-dom','file:///'+p.split(path.sep).join('/')],{encoding:'utf8',timeout:60000,maxBuffer:1e8})}catch(e){out=String(e.stdout||'')+e.message}
  const m=out.match(/<title>RESULT:(.*?)<\/title>/);
  const res=m?m[1].replace(/&quot;/g,'"'):'NO RESULT';
  const ok=res==='[]';if(!ok)bad++;
  console.log((ok?'OK   ':'FAIL ')+f+(ok?'':' '+res.slice(0,600)));
}
process.exit(bad?1:0);
