// Genera el relieve de la isla (montañas, meseta, cañones, río) y lo guarda DENTRO del juego.
// Uso:  node herramientas/relieve/gen.js fuente/mundo-peluche.html
// - Lee del juego las fórmulas compartidas (costa, pista, aeropuerto, río…) y usa relief_gen.js (montañas, cañones, llanos).
// - Calcula la rejilla de alturas (585×585, cada 5 m), la comprime y reescribe en el juego las líneas RL_DATA / RL_BED / RL_PLUNGE.
// Si cambias algo de relief_gen.js (o del bloque "Relieve (v119)" del juego), vuelve a correrlo.
const fs=require('fs'), zlib=require('zlib'), path=require('path');
const GAME=process.argv[2]; if(!GAME){ console.log('uso: node gen.js juego.html'); process.exit(1); }
let html=fs.readFileSync(GAME,'utf8');
const cut=(a,b)=>{ const i=html.indexOf(a); const j=html.indexOf(b,i); if(i<0||j<0) throw new Error('no encontré: '+a.slice(0,40)); return html.slice(i,j); };
const prefix=cut('const SEA_Y=-1.2;','function terrainH(x,z){')+cut('const PG={x:-185','\n')+'\n';
const shared=cut('// ---------- Relieve (v119)','// alturas del relieve nuevo');
const gen=fs.readFileSync(path.join(__dirname,'relief_gen.js'),'utf8');
const t0=Date.now();
(0,eval)(prefix+shared+gen+';globalThis.G={RG,RL_PLUNGE,RL_BED,RL_RIVER,rlBedAt};');
const {N,h:H}=G.RG, Q=20, q=new Int32Array(N*N); for(let k=0;k<N*N;k++) q[k]=Math.round(H[k]*Q);
const bytes=[]; for(let j=0;j<N;j++) for(let i=0;i<N;i++){ const k=j*N+i, a=i?q[k-1]:0, b=j?q[k-N]:0, c=(i&&j)?q[k-N-1]:0; const r=q[k]-(i&&j?a+b-c:(i?a:b)); let z=(r<<1)^(r>>31); while(z>=128){ bytes.push((z&127)|128); z>>>=7; } bytes.push(z); }
const b64=zlib.deflateRawSync(Buffer.from(bytes),{level:9}).toString('base64');
const bed=Array.from(G.RL_BED,v=>+v.toFixed(2));
const block=`// alturas del relieve nuevo, ya calculadas (rejilla de ${N}×${N} cada ${G.RG.S} m, en vigésimos de metro, comprimidas)\nconst RL_DATA={E:${G.RG.E}, S:${G.RG.S}, N:${N}, Q:${Q}, z:'${b64}'};\nconst RL_BED=new Float32Array([${bed.join(',')}]);   // fondo del río cada ~4 m (siempre baja)\nconst RL_PLUNGE=${JSON.stringify(G.RL_PLUNGE,(k,v)=>typeof v==='number'?+v.toFixed(2):v)};   // poza al pie de la cascada\n`;
const a=html.indexOf('// alturas del relieve nuevo'), e=html.indexOf('\n',html.indexOf('const RL_PLUNGE=',a))+1;
html=html.slice(0,a)+block+html.slice(e); fs.writeFileSync(GAME,html);
let mx=-1e9; for(const v of H) if(v>mx) mx=v;
console.log('listo en', Date.now()-t0, 'ms · altura máxima', mx.toFixed(1), 'm · datos', b64.length, 'letras');
const prof=[]; for(let s=0;s<=G.RL_RIVER.total;s+=100) prof.push(s+'m:'+G.rlBedAt(s).toFixed(1)); console.log('fondo del río', prof.join(' '));
