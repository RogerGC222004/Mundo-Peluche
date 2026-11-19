# v236 (Modo libre): chorros de verdad. Las cascadas son gotitas de sustancia que caen con su peso; los chorros de la máquina se unen
# como chorro y cada sustancia se ve como es; chocan con paredes (escurren), techos (no los atraviesan), contigo (te escurren y caen a
# tus pies) y empujan las cosas con física.
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
    pg.on("console", lambda m: errs.append(m.text) if m.type=='warning' and ('juguetes' in m.text or 'gadgets' in m.text or 'maquina' in m.text or 'sustancias' in m.text) else None)
    await pg.add_init_script("localStorage.clear(); localStorage.setItem('mundoPelucheOpciones', JSON.stringify(%s)); localStorage.setItem('mundoPelucheEcon124','1');"%json.dumps(OPTS))
    async def route(r):
      if r.request.url.startswith("https://test.local"): await r.fulfill(body=html.encode(), content_type="text/html; charset=utf-8")
      elif "three" in r.request.url: await r.fulfill(body=REAL, content_type="application/javascript")
      else: await r.abort()
    await pg.route("https://**/*", route); await pg.goto("https://test.local/"); await pg.wait_for_function("window.__T", timeout=180000)
    await pg.wait_for_function("(()=>{const l=document.getElementById('loader'); return !l || l.hidden || getComputedStyle(l).display==='none';})()", polling=250, timeout=120000)
    ev=lambda s: asyncio.wait_for(pg.evaluate("s=>__T.ev(s)", s), 600)
    await ev("(()=>{ freeEnter(); return 1; })()"); await ev(STEP)

    await ev("""(()=>{ window.__LAKE=(p,d,a,b)=>{ for(let ci=a;ci<=b;ci++) for(let cj=a;cj<=b;cj++){ const C=suChunk(ci,cj,true); if(C) suDec(C,'F|'+p+'|'+(p===5?'f00':'0')+'|'+Math.round(d/.003).toString(36)); } suRecount(); };
      window.__WALK=(k)=>{ const x=player.pos.x, z=player.pos.z; keys.KeyW=true; __S(k); keys.KeyW=false; return Math.hypot(player.pos.x-x,player.pos.z-z); }; return 1; })()""")
    T="""const __VOL=()=>{ suRecount(); return SU.vol+FU.pts.reduce((a,P)=>a+(P.v||0),0)+[...SU.falls.values()].reduce((a,F)=>a+F.acc+(F.q||[]).filter((_,i)=>i%2).reduce((x,y)=>x+y,0),0)+(typeof wlVol==='function'?wlVol():0); }; window.__VOL=__VOL;   // (v236: y lo que está en las paredes)
      window.__PLAT=(x0,z0,n,h)=>{ for(let a=0;a<n;a++) for(let b=0;b<n;b++) for(let y=0;y<h;y++) freeAddStatic({k:'b',a:0,b:2},FREE.X+x0+a+.5,FREE.Y+y,FREE.Z+z0+b+.5,0,true); }; 1"""
    await ev(T)
    # 1. cascada de verdad: lo que se cae de un bloque son gotitas de sustancia que caen con su peso (y se unen en chorro)
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); __PLAT(-1,-1,2,2); const v0=__VOL(); suPour(FREE.X,FREE.Z,1,0,.6,.5); let mx=0, link=0, below=0;
        for(let i=0;i<40;i++){ __S(1); const C=FU.pts.filter(P=>!P.o); mx=Math.max(mx,C.length); link=Math.max(link,(FU_FL.rib[1]?FU_FL.rib[1].geometry.drawRange.count/12:0)); for(const P of C) if(Math.abs(P.x-FREE.X)<.98 && Math.abs(P.z-FREE.Z)<.98 && P.y<FREE.Y+1.9) below++; }
        for(let i=0;i<150;i++) __S(1); return [mx, link, below, +(__VOL()-v0).toFixed(3), FU.pts.every(P=>P.v>0)]; })()""")
    ok(r[0]>5 and r[1]>3, '💧 lo que se cae del bloque son gotitas de agua de verdad (%s a la vez) unidas en chorro (%s pedacitos de chorro)'%(r[0],r[1]))
    ok(r[2]==0, 'y caen por fuera: ninguna se mete al bloque (%s)'%r[2])
    ok(abs(r[3]-.6)<.01, 'no se pierde ni se inventa sustancia (%s m³ de 0.6)'%r[3])
    # 2. los chorros chocan: con una pared (se pegan y escurren), con un techo (no lo atraviesan)
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,0,true); for(let z=-2;z<=2;z++) for(let y=0;y<3;y++) freeAddStatic({k:'b',a:0,b:4},FREE.X+5.5,FREE.Y+y,FREE.Z+z,0,true);
        fuSet(o,[0,1,2,3].map(i=>({on:i===3?1:0,p:1,q:2,x:2,col:0}))); let wall=0, through=0; for(let i=0;i<70;i++){ __S(1); for(const P of FU.pts){ if(P.st===1) wall++; if(P.x>FREE.X+6.05) through++; } for(const W of SU.wl.values()) for(let k=0;k<1024;k++) if(W.h[k]>0) wall++; }   /* (v236: el agua que pega se queda escurriendo en la pared como capita) */
        suRecount(); let behind=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.h[k]>0){ const [x]=suXZ(C,k); if(x>FREE.X+6.1) behind++; }
        __CLR(); suClear(); FU.pts.length=0; const o2=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,0,true); for(let x=-3;x<=3;x++) for(let z=-3;z<=3;z++) freeAddStatic({k:'b',a:2,b:3},FREE.X+x,FREE.Y+4.2,FREE.Z+z,0,true);
        const C2=fuCfg(o2); C2[1].on=1; C2[1].q=2; C2[1].x=3; fuSet(o2,C2); let up=0, under=0; for(let i=0;i<60;i++){ __S(1); for(const P of FU.pts){ if(P.y>FREE.Y+4.25) up++; if(P.vy<0 && P.y>FREE.Y+3.5) under++; } }
        suRecount(); let topV=0, lowV=0; for(const C of SU.list) for(let k=0;k<256;k++){ const h=C.h[k]+C.h2[k]; if(!(h>0)) continue; if(suB(C,k)>FREE.Y+4) topV+=h*.04; else lowV+=h*.04; } return [wall, through, behind, up, under, +topV.toFixed(3), +lowV.toFixed(3)]; })()""")
    ok(r[0]>50 and r[1]==0 and r[2]==0, '🧱 el chorro de la manguera pega en la pared, escurre pegadito y no la atraviesa (%s veces escurriendo; atravesaron %s)'%(r[0],r[1]))
    ok(r[3]==0 and r[4]>0, '🏠 la fuente debajo de un techo no lo atraviesa: rebota y gotea de ahí (pasaron %s)'%r[3])
    ok(r[5]==0 and r[6]>.1, 'y lo que cae queda abajo, no arriba del techo (abajo %s m³, arriba %s)'%(r[6],r[5]))
    # 3. los chorros chocan contigo (te escurren y caen a tus pies; la pintura te deja huellitas) y empujan las cosas con física
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; SU.feet=null; __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,0,true); fuSet(o,[0,1,2,3].map(i=>({on:i===3?1:0,p:5,q:2,x:1,col:3})));
        const S=fuSrc(o,3,fuCfg(o)[3]); const px=FREE.X+4.2, pz=S.z; let body=0, past=0; for(let i=0;i<60;i++){ player.pos.set(px,FREE.Y+.05,pz); player.vel.set(0,0,0); __S(1); for(const P of FU.pts){ if(P.st===2) body++; if(P.x>px+.6 && P.y>FREE.Y+.4) past++; } }
        const pf=!!SU.feet; suRecount(); let feet=0, far=0; for(const C of SU.list) for(let k=0;k<256;k++) if(C.h[k]>0){ const [x,z]=suXZ(C,k); if(Math.hypot(x-px,z-pz)<.9) feet++; if(x>px+1.5) far++; }
        __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const o2=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,0,true); const d=freeAddDyn('balon',FREE.X+5.6,FREE.Y,FREE.Z+fuSrc(o2,3,fuCfg(o2)[3]).z-FREE.Z); const x0=d.root.position.x; fuSet(o2,[0,1,2,3].map(i=>({on:i===3?1:0,p:1,q:3,x:1,col:0})));
        for(let i=0;i<60;i++) __S(1); return [body, past, feet, far, pf, +(d.root.position.x-x0).toFixed(2)]; })()""")
    ok(r[0]>20 and r[1]<6, '🧸 el chorro choca contigo: te escurre (%s veces) y casi nada pasa de largo (%s)'%(r[0],r[1]))
    ok(r[2]>3 and r[3]==0 and r[4], 'y cae a tus pies (%s cuadritos ahí, %s detrás); la pintura te deja huellitas'%(r[2],r[3]))
    ok(r[5]>.3, '⚽ el chorro empuja un balón (se movió %s m)'%r[5])
    # 4. cada sustancia se ve como es
    r=await ev("""(()=>{ const m=[1,2,3,4,5,6].map(p=>{ const M=fuFlowMat(p); return [p, M.transparent?+M.opacity.toFixed(2):1, +M.roughness.toFixed(2)]; }); return m; })()""")
    ok(r[0][1]<.7 and r[2][1]==1 and r[2][2]>.8 and r[3][2]<.1 and r[0][2]<.1, 'cada chorro con su aspecto: agua transparente y brillante, lodo opaco y mate, miel brillante %s'%r)
    # 5. lo que cuesta
    r=await ev("""(()=>{ __CLR(); suClear(); FU.pts.length=0; __AT(-20,-20); const o=freeAddStatic({k:'p',a:'fuentes',b:0},FREE.X,FREE.Y,FREE.Z,0,true); fuSet(o,[{on:1,p:1,q:3,x:0,col:0},{on:1,p:1,q:3,x:2,col:0},{on:1,p:4,q:3,x:2,col:0},{on:1,p:3,q:3,x:2,col:0}]); for(let i=0;i<40;i++) __S(1);
        const f=fuPtsTick; let t=0, c=0, n=0; fuPtsTick=(dt)=>{ const a=performance.now(); f(dt); t+=performance.now()-a; c++; n+=FU.pts.length; }; for(let i=0;i<40;i++) __S(1); fuPtsTick=f; return [+(t/c).toFixed(2), Math.round(n/c)]; })()""")
    ok(r[0]<4, 'con las 4 salidas a todo: %s gotitas, %s ms por cuadro (aquí, sin tarjeta de video)'%(r[1],r[0]))
    ok(not errs,'sin errores %s'%errs[:3]); await ctx.close(); await b.close()
asyncio.run(m())
