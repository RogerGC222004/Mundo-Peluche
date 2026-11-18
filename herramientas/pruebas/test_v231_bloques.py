# v231 (Modo libre): los bloques con física (torre, montones) chocan completos entre sí y con las piezas fijas: ya no se quedan
# metidos unos en otros (ni cruzados por las orillas). El arco es más grande (3×3, tu peluche pasa por el hueco) y las piezas
# anchas (arco, losa) se pegan a un lado sin quedar medio metidas en el bloque de junto.
import asyncio, json
from playwright.async_api import async_playwright
REAL=open('threerepo/build/three.min.js').read()
html='<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>'+open('/home/claude/mundo-peluche.html').read().replace("function frame(){","window.__T={ev(s){return eval(s);}}; function frame(){",1)
OPTS={"quality":"low","qDef":1,"hints":False,"weather":False}
STEP="""window.requestAnimationFrame=()=>0; window.__S=(k)=>{ let t=clock.elapsedTime; for(let i=0;i<k;i++){ clock.elapsedTime=(t+=.033); update(.033,t); } };
  window.__CLR=()=>{ for(const o of [...FREE.objs]) freeDrop(o); for(const d of [...FREE.dyn]) freeDrop(d); FREE.hold=null; freeSelect(null); };
  window.__AT=(x,z)=>{ player.pos.set(FREE.X+x,FREE.Y+.05,FREE.Z+z); player.vel.set(0,0,0); player.vy=0; player.facing=0; yaw=Math.PI; FREE.ppPrev=null; __S(2); };
  window.__LOOK=(x,y,z)=>{ camMode='first'; camera.position.set(player.pos.x,player.pos.y+1.6,player.pos.z); camera.lookAt(x,y,z); camera.updateMatrixWorld(); };
  window.__UPQ=(I,k)=>{ const m=new THREE.Matrix4(), q=new THREE.Quaternion(), p=new THREE.Vector3(), s=new THREE.Vector3(); I.getMatrixAt(k,m); m.decompose(p,q,s); return [new THREE.Vector3(0,0,1).applyQuaternion(q).y, p.y]; }; 1"""
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
    ok=lambda c,t: print(('BIEN ' if c else 'MAL  ')+t, flush=True)
    ctx=await b.new_context(viewport={"width":780,"height":360}, has_touch=True); pg=await ctx.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('juguetes' in m.text or 'gadgets' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)
    DEPTH="""window.__WORST=()=>{ const L=FREE.dyn.filter(d=>d.bx); let m=0; for(let i=0;i<L.length;i++) for(let j=i+1;j<L.length;j++) m=Math.max(m,bxDepth(L[i],L[j])); return +m.toFixed(3); };
      window.__RND=(()=>{ let s=11; return ()=>{ s=(s*16807)%2147483647; return s/2147483647; }; })(); 1"""
    await ev(DEPTH)
    # 1. la torre derrumbada desde varios lados: ningún bloque queda metido en otro
    r=await ev("""(()=>{ const out=[]; for(let t=0;t<4;t++){ __CLR(); __AT(-10,-10); const L=bxPlaceMulti('torre',FREE.X,FREE.Y+.01,FREE.Z,t); __S(5); const a=t*Math.PI/2+.4, b=freeAddDyn('boliche',FREE.X-Math.cos(a)*4,FREE.Y,FREE.Z-Math.sin(a)*4); b.root.position.y=FREE.Y+.4+t*.35; b.v.set(Math.cos(a)*14,0,Math.sin(a)*14); __S(170); out.push([__WORST(), L.filter(d=>d.root.position.y<FREE.Y+1).length, L.filter(d=>d.sleep).length]); } return out; })()""")
    ok(all(x[0]<.03 and x[1]>=6 for x in r), 'la torre derrumbada 4 veces desde distintos lados: los bloques chocan y ninguno queda metido en otro (lo más metido: %s m) %s'%(max(x[0] for x in r),r))
    # 2. un montón de bloques soltados girados
    r=await ev("""(()=>{ const out=[]; for(let t=0;t<3;t++){ __CLR(); __AT(-10,-10); for(let k=0;k<14;k++){ const d=freeAddDyn('bloque'+(k%6),FREE.X+(__RND()-.5)*1.2,FREE.Y,FREE.Z+(__RND()-.5)*1.2); d.root.position.y=FREE.Y+1+k*.45; d.root.quaternion.setFromEuler(new THREE.Euler(__RND()*3,__RND()*3,__RND()*3)); bxInit(d); bxWake(d); }
      __S(220); out.push([__WORST(), +Math.max(...FREE.dyn.map(d=>d.root.position.y-FREE.Y)).toFixed(2)]); } return out; })()""")
    ok(all(x[0]<.03 and x[1]>.35 for x in r), 'un montón de 14 bloques soltados girados: quedan unos encima de otros, sin meterse (lo más metido: %s m) %s'%(max(x[0] for x in r),r))
    # 3. dos bloques cruzados en X (metidos a propósito): se separan
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const a=freeAddDyn('bloque0',FREE.X,FREE.Y,FREE.Z), b=freeAddDyn('bloque3',FREE.X,FREE.Y,FREE.Z); a.root.position.y=FREE.Y+.16; a.root.quaternion.setFromEuler(new THREE.Euler(0,.8,0)); b.root.position.set(FREE.X+.05,FREE.Y+.3,FREE.Z+.05); b.root.quaternion.setFromEuler(new THREE.Euler(.5,-.7,.3)); bxInit(a); bxInit(b); bxWake(a); bxWake(b);
      const d0=bxDepth(a,b); __S(90); const d1=bxDepth(a,b), v=Math.max(a.v.length(),b.v.length());
      const c=freeAddDyn('bloque1',FREE.X+3,FREE.Y,FREE.Z), e=freeAddDyn('bloque2',FREE.X+3,FREE.Y,FREE.Z); c.root.position.y=FREE.Y+.16; e.root.position.y=FREE.Y+1.4; e.root.quaternion.setFromEuler(new THREE.Euler(.9,.785,0)); bxInit(c); bxInit(e); bxWake(c); bxWake(e); e.v.set(0,-6,0); __S(90);
      return [+d0.toFixed(3), +d1.toFixed(3), +v.toFixed(2), +bxDepth(c,e).toFixed(3), +(e.root.position.y-FREE.Y).toFixed(2)]; })()""")
    ok(r[0]>.05 and r[1]<.01 and r[2]<.5 and r[3]<.02 and r[4]>.3, 'dos bloques cruzados en X se separan solos sin salir disparados (de %s a %s m) y uno que cae de orilla sobre otro se queda encima %s'%(r[0],r[1],r))
    # 4. contra un bloque fijo
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const o=freeAddStatic({k:'b',a:0,b:0},FREE.X+.5,FREE.Y,FREE.Z+.5,0); for(let k=0;k<8;k++){ const d=freeAddDyn('bloque'+(k%6),FREE.X+.5+(__RND()-.5)*1.4,FREE.Y,FREE.Z+.5+(__RND()-.5)*1.4); d.root.position.y=FREE.Y+2+k*.5; d.root.quaternion.setFromEuler(new THREE.Euler(__RND()*3,__RND()*3,__RND()*3)); bxInit(d); bxWake(d); }
      __S(220); const S=o.box, he=[.5,.5,.5]; let m=0; for(const d of FREE.dyn){ const b=d.bx, n=bxCollide(b.x.x,b.x.y,b.x.z,b.R,b.he,(S.min.x+S.max.x)/2,(S.min.y+S.max.y)/2,(S.min.z+S.max.z)/2,BX_ID,he); for(let c=0;c<n;c++){ const q=c*9, K=_bxK; m=Math.max(m,(K[q]-K[q+3])*K[q+6]+(K[q+1]-K[q+4])*K[q+7]+(K[q+2]-K[q+5])*K[q+8]); } }
      return [+m.toFixed(3), __WORST(), FREE.dyn.filter(d=>d.root.position.y>FREE.Y+1).length]; })()""")
    ok(r[0]<.03 and r[1]<.03 and r[2]>=1, 'bloques que caen sobre un cubo fijo: se quedan encima o a los lados, sin meterse en él %s'%r)
    # 5. el arco
    r=await ev("""(()=>{ __CLR(); __AT(-10,-10); const X=FREE.X-6.5, Z=FREE.Z-3.5; const A=freeAddStatic({k:'b',a:5,b:2},X,FREE.Y,Z,0); const B=A.box, sz=[B.max.x-B.min.x,B.max.y-B.min.y,B.max.z-B.min.z].map(v=>+v.toFixed(2));
      player.pos.set(X,FREE.Y+.05,Z-1.6); for(let i=0;i<40;i++){ player.pos.z+=.08; freeCollide(player.pos); } const thru=+(player.pos.z-Z).toFixed(2), px=+(player.pos.x-X).toFixed(2);
      player.pos.set(X+1.2,FREE.Y+.05,Z-1.6); for(let i=0;i<40;i++){ player.pos.z+=.08; freeCollide(player.pos); } const leg=+(player.pos.z-Z).toFixed(2);
      player.pos.set(X,FREE.Y+3.2,Z); const top=freeGround(X,Z,FREE.Y+3.3); return [sz, thru, px, leg, top!==null?+(top-FREE.Y).toFixed(2):null]; })()""")
    ok(r[0]==[3,3,1] and r[1]>1.2 and abs(r[2])<.05 and r[3]<-.8 and r[4]==3, 'el arco ahora mide 3 de ancho y 3 de alto (%s); tu peluche pasa caminando por el hueco, choca con las patas y se puede parar arriba %s'%(r[0],r[1:]))
    r=await ev("""(()=>{ __CLR(); __AT(-8.5,-8); const X=FREE.X-8.5, Y=FREE.Y, Z=FREE.Z-4.5; const cubo=freeAddStatic({k:'b',a:0,b:0},X,Y,Z,0); const out=[];
      const T=(cx,cy,cz,x,y,z)=>{ camMode='first'; camera.position.set(cx,cy,cz); camera.lookAt(x,y,z); camera.updateMatrixWorld(); return freeAim(); };
      const ov=(a,b)=>Math.max(0,Math.min(a.max.x,b.max.x)-Math.max(a.min.x,b.min.x))*Math.max(0,Math.min(a.max.y,b.max.y)-Math.max(a.min.y,b.min.y))*Math.max(0,Math.min(a.max.z,b.max.z)-Math.max(a.min.z,b.min.z));
      for(const [a,rot,face] of [[5,0,'e'],[5,1,'e'],[5,0,'s'],[5,1,'s'],[2,0,'e'],[2,0,'s'],[0,0,'e']]){ freeSelect({k:'b',a,b:3}); FREE.rot=rot; __S(2);
        const h=face==='e'?T(X+4,Y+.5,Z, X+.5,Y+.5,Z):T(X,Y+.5,Z-4, X,Y+.5,Z-.5); const o=freeAddStatic({k:'b',a,b:3},h.x,h.y,h.z,rot); const B=o.box, C=cubo.box;
        const gap=face==='e'?B.min.x-C.max.x:C.min.z-B.max.z; out.push([FREE_SHAPES[a].id, rot, face, +ov(B,C).toFixed(3), +gap.toFixed(2), +((B.min.x-FREE.X)%1).toFixed(2), h.ok]); freeDrop(o); }
      camMode='third'; FREE.rot=0; freeSelect(null); return out; })()""")
    ok(all(x[3]<.001 and abs(x[4])<.01 and x[6] for x in r), 'el arco, la losa y el cubo se pegan al lado de un bloque sin quedar metidos en él (también girados) %s'%r)
    ok(all(abs(abs(x[5])-0)<.01 or abs(abs(x[5])-1)<.01 for x in r), 'y quedan justo en la cuadrícula %s'%[x[5] for x in r])
    # 6. lo que tarda la física
    r=await ev("""(()=>{ __CLR(); for(let k=0;k<4;k++) bxPlaceMulti('fila',FREE.X-6+k*3,FREE.Y+.01,FREE.Z,0); bxPlaceMulti('torre',FREE.X+7,FREE.Y+.01,FREE.Z,0); FREE.dyn.forEach(d=>{ if(d.bx) bxWake(d); }); FREE.dyn.filter(d=>d.id==='domino').forEach((d,i)=>{ if(i%8===0) d.bx.w.set(3,0,0); });
      const t0=performance.now(); for(let i=0;i<30;i++) bxPhys(.033,FREE.dyn); return [+((performance.now()-t0)/30).toFixed(2), FREE.dyn.length]; })()""")
    ok(r[0]<25, 'con %s piezas cayendo, la física tarda %s ms por cuadro (aquí, sin tarjeta de video)'%(r[1],r[0]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
