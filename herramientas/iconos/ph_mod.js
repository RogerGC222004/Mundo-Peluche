// ======================================================================================
// ---------------- v243: FOTOS DE LA ROPA Y LAS MASCOTAS (sin fondo) ----------------
// En la tienda cada prenda se ve como es de verdad: el juego le toma una foto a la prenda sola, sin el peluche y sin fondo, y
// otra a cada mascota. El peluche está ahí pero invisible: solo tapa lo que queda por dentro (como cuando la traes puesta).
// Las fotos se hacen de una en una mientras ves la lista y se guardan mientras el juego está abierto.
// ======================================================================================
const PH_SZ=256, PH_OUT=128, PH_CACHE=new Map();
const PH_SLOTS=new Set(['top','hat','gloves','socks','shoes','glasses','ctop','cbot','cshoe','chat','cacc','cacf','cacn','cacb','cach','atop','abot','ashoe','ahat','aacc','aacf','aacn','aacb','aach']);
let phRig=null, PH_MS=0, PH_N=0;   // (cuánto tardan, para medir)
const _phV=new THREE.Vector3(), _phW=new THREE.Vector3();
function phIsCloth(it){ return !!(it && PH_SLOTS.has(it.slot) && !it.gest && !it.paint && !it.lscr); }
function phRigGet(){ if(phRig) return phRig; const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff,0xd8d0c8,1.05)); const d=new THREE.DirectionalLight(0xffffff,.75); d.position.set(2,4,5); sc.add(d);
  const d2=new THREE.DirectionalLight(0xffffff,.3); d2.position.set(-3,1.5,-1); sc.add(d2);
  const cam=new THREE.OrthographicCamera(-1,1,1,-1,.1,50), rt=new THREE.WebGLRenderTarget(PH_SZ,PH_SZ); rt.texture.encoding=THREE.sRGBEncoding;
  const src=document.createElement('canvas'); src.width=src.height=PH_SZ;
  return phRig={sc,cam,rt,src,px:new Uint8Array(PH_SZ*PH_SZ*4),occ:new THREE.MeshBasicMaterial({colorWrite:false}),hid:new THREE.MeshBasicMaterial({visible:false}),o:null}; }
const phVis=m=>{ for(let q=m;q;q=q.parent) if(!q.visible) return false; return true; };
// foto de "root" (que ya está en la escena de las fotos): show(m) dice si la pieza sale en la foto; las demás solo tapan lo que
// queda por dentro (el cuerpo dentro de la playera, la cabeza dentro del gorro). Lo que está más arriba que la prenda no tapa
// (la cabezota del Chibi no tapa su playera; las piernas no tapan el zapato por dentro).
function phShoot(root, show){ const R=phRigGet(), t0=performance.now(); root.updateMatrixWorld(true); const sw=[], oth=[]; let x0=1e9,y0=1e9,z0=1e9,x1=-1e9,y1=-1e9,z1=-1e9;
  root.traverse(m=>{ if(m.isSprite || m.isPoints || m.isLine){ if(m.visible){ sw.push([m,null]); m.visible=false; } return; } if(!m.isMesh) return;
    if(!show(m)){ oth.push(m); return; } if(!phVis(m)) return; const p=m.geometry && m.geometry.attributes.position; if(!p) return; const st=Math.max(1,Math.floor(p.count/300));
    for(let i=0;i<p.count;i+=st){ _phV.fromBufferAttribute(p,i).applyMatrix4(m.matrixWorld); if(_phV.x<x0) x0=_phV.x; if(_phV.x>x1) x1=_phV.x; if(_phV.y<y0) y0=_phV.y; if(_phV.y>y1) y1=_phV.y; if(_phV.z<z0) z0=_phV.z; if(_phV.z>z1) z1=_phV.z; } });
  for(const m of oth){ const mt=m.material; if(!phVis(m) || !mt || (Array.isArray(mt) ? !mt.some(x=>x.visible) : !mt.visible)) continue;   // (lo que no se dibuja tampoco tapa)
    const g=m.geometry; let up=false; if(g){ if(!g.boundingSphere) g.computeBoundingSphere(); if(g.boundingSphere) up=_phV.copy(g.boundingSphere.center).applyMatrix4(m.matrixWorld).y>y1; } sw.push([m,m.material]); m.material=up?R.hid:R.occ; }
  let url='';
  if(x1>x0){ const s=Math.max(x1-x0,y1-y0)*.56+.01, cx=(x0+x1)/2, cy=(y0+y1)/2, C=R.cam; C.left=-s; C.right=s; C.top=s; C.bottom=-s; C.near=.05; C.far=(z1-z0)+20; C.position.set(cx,cy,z1+10); C.updateProjectionMatrix(); C.updateMatrixWorld();
    const prev=renderer.getRenderTarget(), sm=renderer.shadowMap.enabled, cc=renderer.getClearColor(new THREE.Color()), ca=renderer.getClearAlpha();
    try{ renderer.shadowMap.enabled=false; renderer.setClearColor(0x000000,0); renderer.setRenderTarget(R.rt); renderer.clear(); renderer.render(R.sc,C); renderer.readRenderTargetPixels(R.rt,0,0,PH_SZ,PH_SZ,R.px); }
    finally{ renderer.setRenderTarget(prev); renderer.setClearColor(cc,ca); renderer.shadowMap.enabled=sm; }
    url=phPng(R); }
  for(const [m,mat] of sw){ if(mat) m.material=mat; else m.visible=true; }
  PH_MS+=performance.now()-t0; PH_N++; return url; }
// de los puntos de la foto a una imagen chiquita, recortada a lo que sí se ve (y sin fondo)
function phPng(R){ const N=PH_SZ, px=R.px, g=R.src.getContext('2d'), im=g.createImageData(N,N), d=im.data; let bx0=N,by0=N,bx1=-1,by1=-1;
  for(let y=0;y<N;y++){ const r=(N-1-y)*N*4, w=y*N*4; for(let x=0;x<N;x++){ const i=r+x*4, a=px[i+3], o=w+x*4; if(a<6){ d[o+3]=0; continue; }
      const k=a<255?255/a:1; d[o]=Math.min(255,px[i]*k); d[o+1]=Math.min(255,px[i+1]*k); d[o+2]=Math.min(255,px[i+2]*k); d[o+3]=a;   // (lo que se pintó encima de lo transparente queda con su color de verdad)
      if(x<bx0) bx0=x; if(x>bx1) bx1=x; if(y<by0) by0=y; if(y>by1) by1=y; } }
  if(bx1<0) return ''; g.putImageData(im,0,0); const bw=bx1-bx0+1, bh=by1-by0+1, k=Math.min(1,(PH_OUT-6)/Math.max(bw,bh)), dw=Math.round(bw*k), dh=Math.round(bh*k);
  const c=document.createElement('canvas'); c.width=dw+6; c.height=dh+6; const o=c.getContext('2d'), t=R.tint||(R.tint=document.createElement('canvas')); t.width=c.width; t.height=c.height;   // (la foto es del tamaño de la prenda: ancha si es ancha)
  const tg=t.getContext('2d'); tg.imageSmoothingQuality='high'; o.imageSmoothingQuality='high';
  tg.drawImage(R.src,bx0,by0,bw,bh,3,3,dw,dh); tg.globalCompositeOperation='source-in'; tg.fillStyle='rgba(90,68,38,.42)'; tg.fillRect(0,0,t.width,t.height); tg.globalCompositeOperation='source-over';
  for(const [ax,ay] of [[-1,0],[1,0],[0,-1],[0,1],[-.7,-.7],[.7,-.7],[-.7,.7],[.7,.7]]) o.drawImage(t,ax,ay+.4);   // (un contornito café, así lo blanco se ve sobre el fondo claro)
  o.drawImage(R.src,bx0,by0,bw,bh,3,3,dw,dh); return c.toDataURL('image/png'); }
// la foto de una prenda (sola, como la traería puesta tu peluche)
function itemPhoto(it){ const key='i'+it.id; if(PH_CACHE.has(key)) return PH_CACHE.get(key); let url='';
  try{ const R=phRigGet(); if(!R.o) R.o=makePlush(0); const o=R.o, u=o.userData; R.sc.add(o);
    const eq={}; if(it.av==='c') eq.body='av_chibi'; else if(it.av==='a') eq.body='av_amigu'; eq[it.slot]=it.id;
    applyOutfit(o,eq); poseLimbs(o,0,.05,0,false,0,false,null,0,0,false);
    const back=it.as==='espalda' || it.view==='espalda' || it.view==='aespalda' || it.k==='cape';
    o.position.set(0,0,0); o.rotation.set(.38,back?Math.PI-.6:(it.slot==='cbot'||it.slot==='abot')?.18:.45,0); o.updateMatrixWorld(true);   // (un poco desde arriba, de tres cuartos)
    const C=new Set(u.cloth||[]), A=u.arms||[], armOf=m=>{ let r=null; for(let q=m;q && q!==o;q=q.parent) if(A.includes(q)) r=q; return r; }, inC=m=>{ for(let q=m;q && q!==o;q=q.parent) if(C.has(q)) return true; return false; };
    let arm=null;   // (de los guantes se ve solo el de enfrente; el reloj, en el brazo donde está)
    if(it.slot==='gloves'){ const has=new Set(); o.traverse(m=>{ if(m.isMesh && inC(m)){ const a=armOf(m); if(a) has.add(a); } }); let bz=-1e9; for(const a of has){ const z=a.getWorldPosition(_phW).z; if(z>bz){ bz=z; arm=a; } } }
    const cl=m=>{ if(!inC(m)) return false; if(!arm) return true; const a=armOf(m); return !a || a===arm; };
    url=phShoot(o,cl); R.sc.remove(o);
  }catch(e){ console.warn('foto de prenda',e); }
  PH_CACHE.set(key,url); return url; }
// la foto de una mascota
function petPhoto(id){ const key='p'+id; if(PH_CACHE.has(key)) return PH_CACHE.get(key); let url='';
  try{ const R=phRigGet(), spec=PET_BY[id], P=buildPet(spec); GOOGLY.list=GOOGLY.list.filter(e=>{ let q=e.g; while(q && q!==P.root) q=q.parent; return q!==P.root; });   // (sus ojitos no se mueven solos)
    P.root.rotation.set(.22,.55,0); R.sc.add(P.root); url=phShoot(P.root,()=>true); R.sc.remove(P.root);
  }catch(e){ console.warn('foto de mascota',e); }
  PH_CACHE.set(key,url); return url; }
