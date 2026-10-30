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
fs.writeFileSync(out,h);
console.log('ok', (h.length/1024).toFixed(0)+' KB');
