// Arma la carpeta www/ de la app a partir del juego (fuente/mundo-peluche.html).
// Usa la misma versión web (salas por PeerJS), pero con three.js, PeerJS y las letras DENTRO de la app:
// así abre rápido y sin internet (el multijugador sí necesita internet).
// Uso: node construir.js   (necesita antes: npm install)
const fs=require('fs'), path=require('path'), os=require('os'), {execFileSync}=require('child_process');
const D=__dirname, ROOT=path.join(D,'..'), WWW=path.join(D,'www'), LIB=path.join(WWW,'lib');
const NM=process.env.MP_NODE_MODULES || path.join(D,'node_modules');
const cfg=JSON.parse(fs.readFileSync(path.join(D,'config.json'),'utf8'));
fs.rmSync(WWW,{recursive:true,force:true}); fs.mkdirSync(LIB,{recursive:true});

// 1) la versión web de siempre (herramientas/build.js) en una carpeta temporal
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'mp-'));
execFileSync(process.execPath,[path.join(ROOT,'herramientas','build.js'), path.join(ROOT,'fuente','mundo-peluche.html'), path.join(tmp,'index.html')],{stdio:'inherit'});
let h=fs.readFileSync(path.join(tmp,'index.html'),'utf8');
const rep=(a,b)=>{ if(!h.includes(a)) throw new Error('No encontré: '+a.slice(0,90)); h=h.split(a).join(b); };

// 2) librerías locales
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="lib/three.min.js"></script>');
rep('<script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>',
    '<script src="lib/peerjs.min.js"></script>\n<script>window.__MP_APP='+JSON.stringify({premio:cfg.admobPremio, pruebas:!!cfg.pruebas})+';</script>\n<script src="puente.js"></script>');
fs.copyFileSync(path.join(NM,'three','build','three.min.js'), path.join(LIB,'three.min.js'));
fs.copyFileSync(path.join(NM,'peerjs','dist','peerjs.min.js'), path.join(LIB,'peerjs.min.js'));
fs.copyFileSync(path.join(D,'puente.js'), path.join(WWW,'puente.js'));

// 3) letras locales (Sniglet y Nunito, las mismas de Google Fonts)
rep('<link rel="preconnect" href="https://fonts.googleapis.com">','');
h=h.replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com\/css2[^"]*">/, '<link rel="stylesheet" href="lib/letras.css">');
if(!h.includes('lib/letras.css')) throw new Error('No encontré las letras de Google Fonts');
let css='';
for(const [fam,id,ws] of [['Sniglet','sniglet',[400,800]],['Nunito','nunito',[500,700,800]]]){
  const dir=path.join(NM,'@fontsource',id,'files');
  for(const w of ws){ const f=`${id}-latin-${w}-normal.woff2`; if(!fs.existsSync(path.join(dir,f))) throw new Error('Falta la letra '+f+' (hay: '+fs.readdirSync(dir).filter(x=>x.includes('latin-')).slice(0,8).join(', ')+')');
    fs.copyFileSync(path.join(dir,f), path.join(LIB,f));
    css+=`@font-face{font-family:'${fam}';font-style:normal;font-weight:${w};font-display:swap;src:url(${f}) format('woff2');}\n`; } }
fs.writeFileSync(path.join(LIB,'letras.css'),css);

// 4) lo que es solo de la web: instalar como PWA (la app ya es una app)
h=h.replace(/<link rel="manifest"[^>]*>\n?/,'').replace(/<link rel="icon"[^>]*>\n?/,'').replace(/<link rel="apple-touch-icon"[^>]*>\n?/,'').replace(/<meta name="mobile-web-app-capable"[^>]*>\n?/,'');
h=h.replace(/<script>if\('serviceWorker' in navigator[^<]*<\/script>\n?/,'');
if(/serviceWorker\.register|fonts\.googleapis|cdnjs\.cloudflare|unpkg\.com/.test(h)) throw new Error('Quedó algo que necesita internet');
fs.writeFileSync(path.join(WWW,'index.html'),h);
fs.rmSync(tmp,{recursive:true,force:true});
const ver=(/const GAME_VERSION='([^']+)'/.exec(h)||[])[1];
console.log('www listo · versión', ver, '·', (h.length/1024).toFixed(0)+' KB');
