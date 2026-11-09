// Mundo Peluche 166: guarda el juego en el dispositivo para que abra rápido y sin internet.
const CACHE='mundo-peluche-166';
const CORE=['./','./manifest.webmanifest','./icono-48.png','./icono-180.png','./icono-192.png','./icono-512.png'];
const LIBS=['https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js'];
self.addEventListener('install',e=>{ e.waitUntil((async()=>{ const c=await caches.open(CACHE);
  for(const u of CORE){ try{ await c.add(new Request(u,{cache:'reload'})); }catch(err){} }
  for(const u of LIBS){ try{ if(!(await c.match(u))) await c.put(u, await fetch(u,{mode:'no-cors'})); }catch(err){} }
  await self.skipWaiting(); })()); });
self.addEventListener('activate',e=>{ e.waitUntil((async()=>{ for(const k of await caches.keys()) if(k.startsWith('mundo-peluche-') && k!==CACHE) await caches.delete(k); await self.clients.claim(); })()); });
self.addEventListener('fetch',e=>{ const r=e.request; if(r.method!=='GET') return; const u=new URL(r.url);
  // el juego: primero internet (así siempre llega la última versión); si tarda o no hay, la copia guardada
  if(r.mode==='navigate' && u.origin===location.origin){ e.respondWith((async()=>{ const c=await caches.open(CACHE), saved=await c.match('./');
    const net=fetch(r).then(res=>{ if(res.ok) c.put('./',res.clone()); return res; });
    if(!saved) return net;
    return Promise.race([net.catch(()=>saved), new Promise(ok=>setTimeout(()=>ok(saved),4000))]); })()); return; }
  // librerías, letras e íconos: la copia guardada; si no está, se descarga y se guarda
  if(u.origin===location.origin || /^(cdnjs\.cloudflare\.com|unpkg\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)$/.test(u.host)){
    e.respondWith((async()=>{ const c=await caches.open(CACHE), hit=await c.match(r,{ignoreVary:true})||await c.match(r.url); if(hit) return hit;
      const res=await fetch(r); if(res.ok || res.type==='opaque') c.put(r,res.clone()); return res; })()); }
});
