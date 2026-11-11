// Genera la versión web (GitHub Pages) a partir del juego de claude.ai.
const fs=require('fs'), path=require('path');
const [src,out]=process.argv.slice(2);
let h=fs.readFileSync(src,'utf8');
const net=fs.readFileSync(path.join(__dirname,'net_peer.js'),'utf8');
const rep=(a,b)=>{ if(!h.includes(a)) throw new Error('No encontré: '+a.slice(0,80)); h=h.replace(a,b); };
rep('<meta name="claude:viewport-fit-sides" content="cover">\n','');
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>\n<script>\n'+net+'</script>');
rep(`const roomPromise = (window.claude && typeof window.claude.use==='function')
  ? window.claude.use('room').catch(()=>null) : Promise.resolve(null);`,
    `const roomPromise = Promise.resolve(window.__fakeNet || peerNet);`);
rep(/const UNAVAILABLE='[^']*';/.exec(h)[0],
    `const UNAVAILABLE='No se pudo cargar el sistema de salas. Revisa tu conexión a internet y vuelve a cargar la página.';`);
rep('const r=lobbyRoom(room, code);', 'const r=await room.join(code);');
rep(`: 'No se pudo conectar a la sala.`, `: c==='timeout' ? 'No se pudo conectar con la sala (la red puede estar bloqueando la conexión). Inténtalo de nuevo o prueba con otra red.'
        : 'No se pudo conectar a la sala.`);
h='<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">\n<meta name="theme-color" content="#a6d24f">\n<style>*,*::before,*::after{box-sizing:border-box}html,body{margin:0;padding:0}[hidden]{display:none!important}</style>\n'+h.replace('</style>','</style>\n</head>\n<body>')+'\n</body>\n</html>\n';
rep(`function getLobby(){ return roomPromise; }    // en claude.ai la sala compartida del juego hace de vestíbulo
function lobbyAnnounce(){}                     // (en claude.ai ya se anuncia con la presencia de la sala)`,
`// Vestíbulo por PeerJS: todos los que abren el juego se conectan aquí y avisan en qué sala están (sin el código a la vista)
let webLobby=null, lobbyRef=null;
function getLobby(){ if(!webLobby){ webLobby = peerNet ? peerNet.join('LOBBY0').then(L=>{ lobbyRef=L; lobbyAnnounce(); return L; }).catch(()=>{ webLobby=null; return null; }) : Promise.resolve(null); } return webLobby; }
function lobbyAnnounce(){ if(!lobbyRef){ getLobby(); return; } try{ lobbyRef.presence({rm:mp.code?lobbyKey(mp.code,mp.pub):null, n:cleanName(profile.name)||'Peluche', pub:mp.code&&mp.pub?1:0}); }catch(e){} }
setTimeout(getLobby,1200);`);
rep(`function lobbyKey(code,pub){ return code; }      // en claude.ai la sala se identifica por su código`,
`function lobbyKey(code,pub){ if(pub) return code; let h=7; for(const ch of code) h=(Math.imul(h,31)+ch.charCodeAt(0))>>>0; return 'p'+h.toString(36).padStart(7,'0').slice(-7); }   // las privadas se anuncian con una clave disfrazada`);
// ---- v125: se instala como app (PWA) y abre sin internet ----
// manifest + íconos + un service worker que guarda el juego, three.js, PeerJS y las letras en el teléfono.
const ver=(/const GAME_VERSION='([^']+)'/.exec(h)||[])[1]||'0';
const dir=path.dirname(path.resolve(out)), web=path.join(__dirname,'web');
rep('<meta name="theme-color" content="#a6d24f">',
    '<meta name="theme-color" content="#a6d24f">\n<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icono-48.png" sizes="48x48">\n<link rel="apple-touch-icon" href="icono-180.png">\n<meta name="mobile-web-app-capable" content="yes">');
h=h.replace(/\n<\/body>\n<\/html>\n$/, `\n<script>if('serviceWorker' in navigator && (location.protocol==='https:'||location.hostname==='localhost')) addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>\n</body>\n</html>\n`);
if(!h.includes("serviceWorker.register('sw.js')")) throw new Error('No pude agregar el service worker');
for(const f of ['icono-48.png','icono-180.png','icono-192.png','icono-512.png']) fs.copyFileSync(path.join(web,f), path.join(dir,f));
fs.writeFileSync(path.join(dir,'manifest.webmanifest'), JSON.stringify({
  name:'Mundo Peluche', short_name:'Mundo Peluche', lang:'es', description:'Un mundo de peluche para explorar, pescar, minar, volar y jugar con amigos.',
  start_url:'./', scope:'./', display:'fullscreen', orientation:'any', background_color:'#cfe7f2', theme_color:'#a6d24f',
  icons:[{src:'icono-192.png', sizes:'192x192', type:'image/png', purpose:'any'}, {src:'icono-512.png', sizes:'512x512', type:'image/png', purpose:'any'},
         {src:'icono-512.png', sizes:'512x512', type:'image/png', purpose:'maskable'}]}, null, 2)+'\n');
fs.writeFileSync(path.join(dir,'sw.js'), `// Mundo Peluche ${ver}: guarda el juego en el dispositivo para que abra rápido y sin internet.
const CACHE='mundo-peluche-${ver}';
const CORE=['./','./manifest.webmanifest','./icono-48.png','./icono-180.png','./icono-192.png','./icono-512.png'];
const LIBS=['https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js'];
self.addEventListener('install',e=>{ e.waitUntil((async()=>{ const c=await caches.open(CACHE);
  for(const u of CORE){ try{ await c.add(new Request(u,{cache:'reload'})); }catch(err){} }
  for(const u of LIBS){ try{ if(!(await c.match(u))) await c.put(u, await fetch(u,{mode:'no-cors'})); }catch(err){} }
  await self.skipWaiting(); })()); });
self.addEventListener('activate',e=>{ e.waitUntil((async()=>{ for(const k of await caches.keys()) if(k.startsWith('mundo-peluche-') && k!==CACHE) await caches.delete(k); await self.clients.claim(); })()); });
self.addEventListener('fetch',e=>{ const r=e.request; if(r.method!=='GET') return; const u=new URL(r.url);
  // el juego: primero internet (así siempre llega la última versión); si tarda o no hay, la copia guardada
  if(r.mode==='navigate' && u.origin===location.origin && /\\/(index\\.html)?$/.test(u.pathname)){ /* solo el juego, no otras páginas como privacidad.html */ e.respondWith((async()=>{ const c=await caches.open(CACHE), saved=await c.match('./');
    const net=fetch(r).then(res=>{ if(res.ok) c.put('./',res.clone()); return res; });
    if(!saved) return net;
    return Promise.race([net.catch(()=>saved), new Promise(ok=>setTimeout(()=>ok(saved),4000))]); })()); return; }
  // librerías, letras e íconos: la copia guardada; si no está, se descarga y se guarda
  if(u.origin===location.origin || /^(cdnjs\\.cloudflare\\.com|unpkg\\.com|fonts\\.googleapis\\.com|fonts\\.gstatic\\.com)$/.test(u.host)){
    e.respondWith((async()=>{ const c=await caches.open(CACHE), hit=await c.match(r,{ignoreVary:true})||await c.match(r.url); if(hit) return hit;
      const res=await fetch(r); if(res.ok || res.type==='opaque') c.put(r,res.clone()); return res; })()); }
});
`);
fs.writeFileSync(out,h);
console.log('ok', (h.length/1024).toFixed(0)+' KB', '· PWA', ver);
